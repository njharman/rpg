#!/usr/bin/env python
# vim: set fileencoding=utf-8 name> :
# Author: Norman J. Harman Jr. <njharman@gmail.com>
# License: Released into Public Domain Nov 2012

# Parses 'text' versions of various OGL RPG monster tomes. Text versions are
# created using pdftotext, and unfortunately, some hand munging.

# Supported Tombs:
#  * Swords & Wizardary Core / Complete
#    pdftotext -f 92 -l 116 -eol unix -raw -nopgbrk "S&W - Rules (complete).pdf" data/swcomplete.txt
#  * Tome of Horrors Complete
#  * Monster Compendium (Swords & Wizardary)
#  * Varlets and Vermin
#  * Barrow Maze New Monsters
#  * Dwimmermount New Monsters
#
# Tome of Horrors Complete is a trademark of Frog God Games.
# Swords & Wizardry, S&W, and Mythmere Games are trademarks of Matthew J. Finch.
# This software and author are not affiliated with Matthew J. Finch, Mythmere Games™, Frog God Games, Necromancer Games.

import os
import re
import sys
from collections import defaultdict

import rpg.munge.rst
from rpg.munge import RE_EMPTYLINE, alpha_sort, by_para, slurp_re, replace_typography, \
        strip_emptylines, strip_newlines, strip_comments, by_page, dehyphenate
from rpg.munge.out import parapper
from known import known

ODD_DAMAGE = {
        '1d2':  'd2',
        '1d3':  'd3',
        '1d4':  'd4',
        '1d6':  'd6',
        '1d8':  'd6',
        '1d10': 'd6+1',
        '1d12': '2d6',
        '2d4':  'd6',
        '2d8':  '2d6',
        '2d10': '2d6+2',
        '2d12': '3d6',
        '3d4':  '2d6',
        '3d8':  '3d6',
        '3d10': '3d6+3',
        '3d12': '4d6',
        '4d4':  '3d6',
        '4d8':  '4d6',
        '4d10': '4d6+4',
        '4d12': '6d6',
        }

ODD_SV = {
        '1d2':      18,
        '1d4':      18,
        '1d4 hp':   18,
        '1d4 hit points': 18,
        '1d6':      17,
        }

ODD_XP = {
        '1d2':    50,    # <1hd
        '1d4':    50,    # <1hd
        '1d4 hp':    50,    # <1hd
        '1d4 hit points':    50,    # <1hd
        '1d6':    100,
        1:    100,
        2:    200,
        3:    300,
        4:    400,
        5:    500,
        6:    600,
        7:    700,
        8:    800,
        9:    1100,
        10:   1400,
        11:   1700,
        12:   2000,
        13:   2300,
        14:   2600,
        15:   3000,
        16:   4000,
        17:   5000,
        18:   6000,
        }

re_attribute = re.compile(r'^[ \/A-Za-z]+:')    # Entry attribute.
re_numbers = re.compile(r'(-?[\d,]+)')          # Positive/Negative numbers only.
re_ac = re.compile(r'(-?\d+)\s*\[(\d+)\]')      # Format: descending [ascending]

# Challenge Level / Experience formats
#  can have comma's in xp
#  one entry cl/xp: 2/30
#  multiple number first: 7 HD (7/600), 8 HD (8/800), 9 HD (9/1,100)
#  multiple hitdie first: HD 7 (10/1400); HD 8 (11/1700); HD 9 (12/2000)
re_clxp = re.compile(r'\s*(?:[HD\s]*(\d+)[HD\s]*\s)?\(?([AB\d]+)/([\d,]+)\)?,?;?\s*')

# Match names with comma: "1st, 2nd (additional)"
# So they can be reordered "2nd 1st (additional)"
re_name = re.compile(r'([^(),]+),\s*([^()]+)\s*(\(.+\))?')

re_ll_move = re.compile(r"([1-5]0)'")

save_chart = {
#        'F': range(15, 0, -1),
        'T': [15, 15, 13, 11, 9, 7, 5, 3, 3, 3, 3, 3, 3],
        'M': range(16, 0, -1),
        'MU': range(16, 0, -1),
        'C': range(16, 0, -1),
        'CL': range(16, 0, -1),
        }


def save_ll_to_sw(save, hd):
    save = save.strip()
    try:
        if save[0:2] in save_chart:
            return save_chart[save[0:2]][int(save[2:])]
        elif save[0] in save_chart:
            return save_chart[save[0]][int(save[1:])]
        return (18, 17, 16, 14, 13, 12, 11, 9, 8, 6, 5, 4, 3)[min(int(hd), 12)]
    except Exception as e:
        return save


def move_ll_to_sw(movement):
    match = re_ll_move.search(movement)
    if match:
        return ('', '3', '6', '9', '12', '15', '18')[int(match.group(1)[0])]
    else:
        return movement


class Monster(object):
    '''One entry from tome of "monsters".'''

    def __init__(self, name):
        self.name = name
        self.hd = None              # Numeric or "complex" Hit Dice.
        self.hd_bonus = None        # The +3 in "3+3 HD"k
        self.hp = None              # Some entries list specific hit points.
        self.ac_raw = ''
        self.ac_asc = 0
        self.ac_dsc = 0
        self.save = ''
        self.attack = list()
        self.special = list()
        self.move = ''
        self.alignment = ''
        self.morale = ''
        self.number = ''
        self.cl = 0
        self.xp = 0
        self.description = list()
        self.s15 = ''
        self.source = 'unknown'
        self.mini_adventure = list()

    def __str__(self):
        return self.format(True)

    @property
    def hitdice(self):
        '''Reformatted hitdice.'''
        bonus = ''
        hp = ''
        if self.hd_bonus:
            bonus = '+%s' % self.hd_bonus
        if self.hp:
            hp = ' (%s hp)' % self.hp
        return '%s%s%s' % (self.hd, bonus, hp)

    def odd_line(self):
        '''OD&D One line statblock.'''
        # keys = ('name', 'hd', 'ac', 'sv', 'atk', 'special', 'mv', 'al', 'ml', 'ne', 'cl', 'xp', 'body', 'source', 's15')
        def reduce_damage(match):
            return ODD_DAMAGE.get(match.group(1), match.group(1))
        foo = re.compile(r'([-\d]*)\s*([^(]+)\s*\(([^)]+)\)')
        bits = list()
        attacks = list()
        for old in self.attack:
            old = old.lower()
            old = re.sub(r'weapon or strike', 'strike', old)
            options = list()
            for atk in old.split(' or '):
                match = foo.match(atk)
                #print old,
                if match:
                    count, attack, damage = match.groups()
                    attack = attack.strip()
                    damage = ODD_DAMAGE.get(damage, damage)
                    damage = re.sub(' \+ ', '+', damage)
                    damage = re.sub(' plus ', '+', damage)
                    try:
                        if int(count) == 1:
                            count = ''
                    except:
                        pass
                    if count:
                        bit = '%sx %s (%s)' % (count, damage, attack)
                    else:
                        bit = '%s (%s)' % (damage, attack)
                    if attack == 'weapon' and not count and damage == 'd6':
                        bit = 'weapon'
                else:
                    bit = '(%s)' % atk
                options.append(bit)
            new = ' or '.join(options)
            #print '|', new
            attacks.append(new)
        data = self.as_dict()
        data['atk'] = ', '.join(attacks)
        data['ac'] = self.ac_dsc
        data['mv'] = re.sub(r'\s*\(flying\)', '(fly)', data['mv'])
        data['xp'] = ODD_XP.get(self.hd, 'WTF %s' % self.hd)
        if self.hd in ODD_SV:
            data['sv'] = ODD_SV[self.hd]
        else:
            data['sv'] = max(3, 18-self.hd)
        if self.hd_bonus and isinstance(self.hd_bonus, (int, long)):
            data['xp'] += 25 * self.hd_bonus
        bits.append('''%(name)s: %(hd)shd %(ac)sAC %(sv)s+ %(mv)s", %(atk)s,''' % data)
        if data['special']:
            bits.append('**%s**' % ', '.join(a.lower() for a in data['special']))
        if data['ml']:
            bits.append('ML%s' % data['ml'])
        bits.append('''%(xp)sXP''' % data)
        return ' '.join(bits)

    def stat_line(self):
        '''One line statblock.'''
        # keys = ('name', 'hd', 'ac', 'sv', 'atk', 'special', 'mv', 'al', 'ml', 'ne', 'cl', 'xp', 'body', 'source', 's15')
        bits = list()
        data = self.as_dict()
        data['atk'] = ', '.join(a for a in data['atk']).replace(')', '').replace('(', '')
        bits.append('''%(name)s %(hd)sHD [%(atk)s] AC%(ac)s %(sv)s+ %(mv)s\' ''' % data)
        if data['special']:
            bits.append('(**%s**)' % ', '.join(a for a in data['special']))
        if data['ml']:
            bits.append('ML%s' % data['ml'])
        bits.append('''CL%(cl)s %(xp)sXP''' % data)
        return ' '.join(bits)

    def format(self, legal=False):
        '''ReStructuredText output of entry.'''
        lines = [
                self.name,
                '-' * len(self.name),
                ]
        if self.hd:
            lines.extend([
                ':Hit Dice: %s' % self.hitdice,
                ':Attack: %s' % ', '.join(self.attack),
                ':AC: %s' % self.ac_asc,
                ':Save: %s' % self.save,
                ':Special: %s' % ', '.join(self.special),
                ':Move: %s' % self.move,
                ':Alignment: %s' % self.alignment,
                ':CL/XP: %s/%s' % (self.cl, self.xp),
                ])
        if self.number:
            lines.append('')
            lines.append('Number encountered: %s' % (self.number, ))
        if self.description:
            lines.append('')
            lines.append('\n\n'.join(parapper(p) for p in self.description))
        else:
            print >> sys.stderr, self.name
        if legal and self.s15:
            lines.append('\nSource: %s' % self.source)
            lines.append('\nCopyright: %s' % self.s15)
        return '\n'.join(lines)

    def as_tuple(self):
        '''Suitable for JSONification.'''
        return (
            self.name,
            self.hitdice,
            self.hd,
            self.hd_bonus,
            self.hp,
            self.ac_raw,
            self.save,
            self.attack,
            self.special,
            self.move,
            self.alignment,
            self.morale,
            self.number,
            self.cl,
            self.xp,
            self.description,
            self.source,
            self.s15,
            )

    def as_dict(self, skip=(), only=()):
        '''Suitable for JSONification.'''
        keys = ('name', 'hd', 'ac', 'sv', 'atk', 'special', 'mv', 'al', 'ml', 'ne', 'cl', 'xp', 'body', 'source', 's15')
        attr = {'hd': 'hitdice', 'ac': 'ac_asc', 'sv': 'save', 'atk': 'attack', 'mv': 'move', 'al': 'alignment', 'ml': 'morale', 'ne': 'number', 'body': 'description'}
        data = dict()
        for key in (k for k in keys if k not in skip):
            data[key] = getattr(self, attr.get(key, key))
        return data

    def clone(self):
        clone = self.__class__(self.name)
        clone.hd = self.hd
        clone.hd_bonus = self.hd_bonus
        clone.hp = self.hp
        clone.ac_raw = self.ac_raw
        clone.ac_asc = self.ac_asc
        clone.ac_dsc = self.ac_dsc
        clone.save = self.save
        clone.attack = list(self.attack)
        clone.special = list(self.special)
        clone.move = self.move
        clone.alignment = self.alignment
        clone.morale = self.morale
        clone.number = self.number
        clone.cl = self.cl
        clone.xp = self.xp
        clone.description = list(self.description)
        clone.source = self.source
        clone.s15 = self.s15
        return clone

    @classmethod
    def from_entry(cls, lines):
        '''Convert entry into one or more Monster instances.
        Entries with multiple hit dice are split into individual instances.
        :param lines: entry split into lines.
        '''
        stop = len(lines)
        name = lines[0].strip()
        # Change mc "foo demon" do "demon, foo"
        if name.lower().endswith(' demon prince'):
            name = 'Demon Prince, ' + name.replace(' Demon Prince', '')
        elif name.lower().endswith(' demon'):
            name = 'Demon, ' + name.replace(' Demon', '')
        if name not in known:
            if name.startswith('Giant '):
                name = name[6:] + ', Giant'
            if name not in known:
                if name:
                    raise Exception('Not known [%s]' % name)
                else:
                    raise Exception('No name!\n%s' % '\n'.join(lines))
        try:
            entry = cls(name)
            # if entry.name.endswith(', Giant'):
            #    entry.name = 'Giant %s' % entry.name.rsplit(', ', 1)[0]
            #    entry.name = 'Giant %s' % entry.name.rsplit(', ', 1)[0]
            challenge = False  # Some entries don't have regular stats.
            l = 1  # Start past name.
            while l < stop:
                key, _, value = [b.strip() for b in lines[l].partition(':')]
                if key == 'Source':
                    entry.source = value
                elif key == 'S15':
                    entry.s15 = value
                elif key == 'Hit Dice':
                    parse_hd(entry, value)
                elif key == 'Armor Class':
                    entry.ac_raw = value
                    try:
                        entry.ac_dsc = int(value)
                        entry.ac_asc = 20 - (int(value) + 1)
                    except Exception:
                        try:
                            entry.ac_dsc, entry.ac_asc = map(int, re_ac.match(value).groups())
                        except Exception:
                            print >> sys.stderr, 'FAIL AC "%s" %s' % (value, entry.name)
                elif key == 'Saving Throw' or key == 'Save':
                    entry.save = value
                elif key == 'Attack' or key == 'Attacks':
                    l, raw = slurp_re(re_attribute, l, lines, ':')
                    entry.attack = [s.strip().rstrip('.') for s in raw.split(',')]
                elif key == 'Damage':
                    entry.attack = [value, ]
                elif key == 'Special':
                    l, raw = slurp_re(re_attribute, l, lines, ':')
                    entry.special = [s.strip().rstrip('.').replace('magic resistance ', 'MR') for s in raw.split(',') if s.lower() != 'none']
                elif key.startswith('Move'):
                    entry.move = value
                elif key == 'Alignment':
                    entry.alignment = value
                elif key == 'Morale':
                    entry.morale = value
                elif key == 'Hoard Class':
                    entry.hoard = value
                elif key == 'Number Encountered' or key == 'No. Enc':
                    l, raw = slurp_re(re_attribute, l, lines, ':')
                    entry.number = raw
                elif key == 'XP':
                    entry.xp = value
                    l += 1
                    break  # XP is last stat for LL style monsters.
                elif key in ('Challenge Level/XP', 'CL/XP'):
                    challenge = value
                    l += 1
                    break  # CL/XP is last stat for SW style monsters.
                else:
                    # No stats.
                    break
                l += 1
            for para in strip_emptylines(by_para(lines[l:], (custom_break, ))):
                key, _, text = [b.strip() for b in para.partition(':')]
                if key == 'Credit':  # tohc only thing we aren't allowed to use.
                    pass
                elif key == 'Copyright Notice':  # tohc only authors.
                    entry.s15 = '%s; %s' % (entry.s15, text)
                elif key == 'MiniAdventure':
                    entry.mini_adventure.append(text)
                # Assume rest of paras after mini-adventure is mini-adventure.
                elif entry.mini_adventure:
                    entry.mini_adventure.append(para)
                # Skip Author
                elif para.startswith('<author>'):
                    pass
                else:
                    entry.description.append(para)
            # LL style.
            if entry.source in ('bm', 'dw'):
                entry.save = save_ll_to_sw(entry.save, entry.hd)
                entry.move = move_ll_to_sw(entry.move)
            # LL style or No Stats.
            if not challenge:
                yield entry
                return
            # One entry per HD.
            saves = [b.replace('or ', '').strip() for b in entry.save.split(',')]
            for x, match in enumerate(re_clxp.finditer(challenge)):
                hd, cl, xp = match.groups()
                entry.cl = cl
                entry.xp = int(xp.replace(',', ''))
                try:
                    # Some entries vary save by hit die.
                    entry.save = saves[x]
                except IndexError:
                    pass
                yield entry
                if hd:  # Multiple entries with different HD.
                    entry.hd = int(hd)
                    entry.name = '%s (%sHD)' % (entry.name.split('(')[0].strip(), hd)
                    entry = entry.clone()
        except:
            print >> sys.stderr, 'Line #%i Mob: %s\n' % (l, entry.__dict__)
            print 'Some Lines:\n', ''.join(lines[l - 10:l + 5])
            raise


def custom_break(line, accum):
    if '-- Author:' in line:
        return '<author>' + line
    if line and len(line) < 40 and not ('Copyright Notice:' in line or 'Credit:' in line or line.endswith('.')):
        return 'MiniAdventure:' + line


re_hp = re.compile(r'^(\d+)\s*hp$')
re_hd = re.compile(r'^(\d+)(?:\+(\d+d?\d*))?\s*(?:\((\d+) hp\))?$')
#re_hd = re.compile(r'^(\d+)(?:\+(\d+d?\d*))?\s*(?:hit points)?\s*(?:\((\d+) hp\))?$')


def parse_hd(entry, value):
    '''Complicated parsing of hit dice attribute.'''
    try:
        entry.hd = int(value)
    except ValueError:
        match = re_hd.match(value)
        if match:
            hd, bonus, hp = match.groups()
            entry.hd = int(hd)
            entry.hd_bonus = bonus
            if hp:
                entry.hp = int(hp)
        else:
            entry.hd = value
            match = re_hp.match(value)
            if match:
                entry.hp = int(match.group(1))


def split_mc_entries(source, s15, lines):
    '''Entry splitter that works on Monster Compendium.'''
    entry = list()
    description = list()
    for l in lines:
        if l.startswith('##'):      # Comment line.
            continue
        if RE_EMPTYLINE.match(l):   # Empty lines separate entries.
            entry = list()
            description = list()
            continue
        if len(l) < 30:             # Skip the redundant entry names.
            continue
        # MC has attributes all on one line.  Reformat them into style
        # Entry.from_entry understands.
        match = re.match(r'(^[^:]+):\s+(HD .*;.*)$', l)
        if match:
            name, rest = match.groups()
            bits = [b.strip() for b in rest.split(';')]
            entry.append(name)
            entry.append('Source: %s' % source)
            entry.append('S15: %s' % (s15 % {'name': name}))
            for bit in bits:
                name, value = bit.split(' ', 1)
                if name == 'HD':
                    entry.append('Hit Dice: %s' % value)
                elif name == 'AC':
                    entry.append('Armor Class: %s' % ' ['.join(value.split('[')))
                elif name == 'Atk':
                    entry.append('Attacks: %s' % value)
                elif name == 'Save':
                    entry.append('Saving Throw: %s' % value)
                elif name == 'Move':
                    entry.append('Move: %s' % value)
                elif name == 'CL/XP':
                    clxp = value
                else:
                    entry.append(bit)
            # CL/XP must be last, used to detect end of attributes.
            entry.append('CL/XP: %s' % clxp)
            for para in description:
                entry.append('')
                entry.append(para)
            yield entry
            # Multiple entries under one description.
            entry = list()
        else:
            description.append(l)


def monsterfy(entries):
    '''Convert sequence of entry sections into sequence of Monster instances.'''
    for entry in entries:
        for m in Monster.from_entry(entry):
            yield(m)


def remove_dupes(seq):
    '''Prefer in order swc, tohc, vv, others, mc'''
    grouped = defaultdict(list)
    for entry in seq:
        grouped[entry.name.lower()].append(entry)
    new = list()
    for group in grouped.values():
        if len(group) != 1:
            group.sort(key=lambda x: ('bm', 'mon', 'swc', 'tohc', 'vv', 'mc', 'dw', 'll').index(x.source))
        new.append(group[0])
    return new


def two_to_one_columns(pages):
    '''Given two-column pages (say from pdftotext -layout), return lines of one column.'''
    def good_mid(mid, page):
        for l in page:
            if len(l) > mid:
                if l[mid] != ' ':
                    return False
        return True

    def calc_mid(page):
        for mid in (39, 38, 40, 37, 41, 36, 42, 35, 43, 34, 44):
            if good_mid(mid, page):
                return mid
    for i, page in enumerate(pages):
        mid = calc_mid(page)
        if mid:
            two = list()
            two.append('')
            for l in page:
                yield l[:mid].strip()
                if len(l) > mid:
                    two.append(l[mid:].strip())
            for l in two:
                yield l
        else:
            print >> sys.stderr, 'Did not find mid point for page %i' % i
            for l in page:
                yield l


def tuco(sources):
    # Tool to use when hand munging text files.
    # Output one column of two column source
    pages = list(by_page(strip_newlines(replace_typography(open(sources)))))
    print >> sys.stderr, 'Found %i pages' % len(pages)
    print '\n'.join(two_to_one_columns(pages))


def split_on_monster(source, s15, lines):
    '''Parse lines into entry "sections".'''
    if source == 'mc':
        for e in split_mc_entries(source, s15, lines):
            yield e
        return
    # Delimiter is line after name
    delimeter, skip_delimeter = {
            'tohc': ('-------------------------------------------------------------------------', True),
            'mon': ('Hit Dice:', False),
            'swc': ('Hit Dice:', False),
            'll': ('Hit Dice:', False),
            'bm': ('No. Enc:', False),
            'dw': ('No. Enc.:', False),
            'vv': ('Armor Class:', False),
            }[source]
    entry = list()
    first = True
    for l in lines:
        if l.startswith(delimeter):
            name = entry.pop()
            if name.startswith('('):  # Some names split onto two lines.
                name = entry.pop() + ' ' + name
            if not first:
                yield entry
            first = False
            entry = list((name, ))
            entry.append('Source: %s' % source)
            entry.append('S15: %s' % (s15 % {'name': name}))
            if skip_delimeter:
                continue
        entry.append(l)
    else:
        yield entry


def make_menagerie(sources):
    menagerie = list()
    for filename in sources:
        file = open(filename)
        s15 = file.readline()
        if not s15.startswith('s15: '):
            raise Exception('Bad section 15 line.')
        source = os.path.basename(filename).partition('.')[0].partition('_')[0]
        lines = dehyphenate(strip_newlines(strip_comments(replace_typography(file))))
        monsters = list(monsterfy(split_on_monster(source, s15[5:], lines)))
        menagerie.extend(monsters)
    menagerie = remove_dupes(menagerie)
    menagerie.sort(key=lambda m: alpha_sort(m.name))
    return menagerie


def print_by_alpha(seq):
    chapter = seq[0].name[0]
    for thing in seq:
        if thing.name[0] != chapter:
            chapter = thing.name[0]
            print rpg.munge.rst.page('twoColumn')
        print thing.format(False)
        print '\n'


def print_one_per_page(seq):
    for thing in seq:
        print thing.format(False)
        print rpg.munge.rst.page('oneColumn')


# TODO: null align = neutral
# special "" not None
if __name__ == '__main__':
    import argparse
    import json

    def command_line():
        parser = argparse.ArgumentParser()
        parser.add_argument('sources', metavar='<file>', nargs='+')
        parser.add_argument('--statline', action='store_true', help='''Output stat, one per line''')
        parser.add_argument('--oddline', action='store_true', help='''OD&D stats, one per line''')
        parser.add_argument('--python', action='store_true', help='''Output python data structure''')
        parser.add_argument('--minify', action='store_true', help='''Output minified JSON''')
        parser.add_argument('--json', action='store_true', help='''Output prettified JSON''')
        parser.add_argument('--tuco', action='store_true', help='''Output one column version of two-column source''')
        cmdline = parser.parse_args()
        return cmdline

    config = command_line()
    if config.tuco:
        tuco(config.sources)
    else:
        menagerie = make_menagerie(config.sources)
        print >> sys.stderr, 'Found %i entries' % len(menagerie)
        if config.json:
            print 'MOBS =', json.dumps([m.as_dict() for m in menagerie], sort_keys=True, indent=2)
        elif config.minify:
            print 'MOBS =', json.dumps([m.as_dict() for m in menagerie], sort_keys=True, separators=(',', ':'))
        elif config.python:
            print 'MOBS = {\n    %s\n    }' % ',\n    '.join('"%s": %s' % (m.name.lower(), m.as_dict(skip=('body', 'source', 's15'))) for m in menagerie)
        elif config.oddline:
            print '\n'.join(m.odd_line() for m in menagerie if isinstance(m.hd, (int, long)))
        elif config.statline:
            print '\n'.join(m.stat_line() for m in menagerie)
        else:
            print rpg.munge.rst.title('=', 'Menagerie')
            # print rpg.munge.rst.page('twoColumn')
            print rpg.munge.rst.page('oneColumn')
            print_one_per_page(menagerie)
