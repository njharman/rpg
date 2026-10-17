#!/usr/bin/env python
"""Parse 'text' versions of various OGL RPG monster tomes.

Text versions are created using pdftotext, and unfortunately, some hand munging.

Supported Tomes:
 * Swords & Wizardry Core / Complete
   pdftotext -f 92 -l 116 -eol unix -raw -nopgbrk "S&W - Rules (complete).pdf" data/swcomplete.txt
 * Tome of Horrors Complete
 * Monster Compendium (Swords & Wizardry)
 * Varlets and Vermin
 * Barrow Maze New Monsters
 * Dwimmermount New Monsters
 * Labyrinth Lord conversions (data/ll.txt)

Building PDFs:
 ./build-pdfs writes build/menagerie.rst and two PDFs from it, one per style sheet.
 Requires rst2pdf (its "preprocess" extension provides the ".. page::" directive).
 * handbook.yaml: 6x9in, 12pt, headers/footers, embeds Liberation Sans/Serif
   (needs the ttf-liberation package; rst2pdf finds the fonts via fontconfig).
 * menagerie.yaml: Letter, 10pt, no headers/footers, blue links, built-in PDF
   fonts (Times/Helvetica/Courier) so nothing needs to be installed.

Tome of Horrors Complete is a trademark of Frog God Games.
Swords & Wizardry, S&W, and Mythmere Games are trademarks of Matthew J. Finch.
This software and author are not affiliated with Matthew J. Finch, Mythmere Games™, Frog God Games, Necromancer Games.

Version: 10/16/2026
Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Nov 2012.
Website: https://github.com/njharman/rpg
"""


import contextlib
import re
import sys
from collections import defaultdict
from pathlib import Path

import mungetext.rst
from known import aliases, known
from mungetext import (
    RE_EMPTYLINE,
    alpha_sort,
    by_page,
    by_para,
    dehyphenate,
    replace_typography,
    slurp_re,
    strip_comments,
    strip_emptylines,
    strip_newlines,
)
from mungetext.out import parapper

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

SOURCES = {
        'swc':  'Swords & Wizardry Complete Rules',
        'tohc': 'Tome of Horrors Complete',
        'mon':  'Monstrosities',
        'mc':   'Monster Compendium: 0e',
        'bm':   'Barrow Maze',
        'dw':   'Dwimmermount',
        'vv':   'Varlets and Vermin',
        'll':   'Labyrinth Lord',
        }

re_attribute = re.compile(r'^[ \/A-Za-z]+:')    # Entry attribute.
re_numbers = re.compile(r'(-?[\d,]+)')          # Positive/Negative numbers only.
# Format: [label] descending [ascending] or descending/ascending.
# Label is for entries with an AC per body part: "Goat 6 [13], Lion 5 [14]".
re_ac = re.compile(r'(?:([A-Za-z][A-Za-z ]*?)\s+)?(-?\d+)\s*(?:\[(\d+)\]|/(\d+))')

# Challenge Level / Experience formats
#  can have commas in xp
#  one entry cl/xp: 2/30
#  multiple number first: 7 HD (7/600), 8 HD (8/800), 9 HD (9/1,100)
#  multiple hitdie first: HD 7 (10/1400); HD 8 (11/1700); HD 9 (12/2000)
re_clxp = re.compile(r'\s*(?:[HD\s]*(\d+)[HD\s]*\s)?\(?([AB\d]+)/([\d,]+)\)?,?;?\s*')

# Match names with comma: "1st, 2nd (additional)"
# So they can be reordered "2nd 1st (additional)"
# MC stats are ';' separated, except where the source used ',' before a stat name.
re_mc_split = re.compile(r';\s*|,\s*(?=(?:HD|AC|Atk|Move|Save|AL|CL/XP|Special)\b)')

re_name = re.compile(r'([^(),]+),\s*([^()]+)\s*(\(.+\))?')

# One LL speed: "60' (20')" or "20'"; the encounter (parenthetical) rate wins.
re_ll_move = re.compile(r"(\d+)'(?:\s*\((\d+)'\))?")

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
        if save[0] in save_chart:
            return save_chart[save[0]][int(save[1:])]
        return (18, 17, 16, 14, 13, 12, 11, 9, 8, 6, 5, 4, 3)[min(int(hd), 12)]
    except (ValueError, IndexError, TypeError):
        return save


def move_ll_to_sw(movement):
    def convert(match):
        for rate in (match.group(2), match.group(1)):
            if rate and int(rate) % 10 == 0 and int(rate):
                return str(int(rate) * 3 // 10)
        return match.group(0)
    return re_ll_move.sub(convert, movement)


class Monster:
    """One entry from tome of "monsters"."""

    def __init__(self, name):
        self.name = name
        self.hd = None              # Numeric or "complex" Hit Dice.
        self.hd_bonus = None        # The +3 in "3+3 HD"
        self.hp = None              # Some entries list specific hit points.
        self.ac_raw = ''
        self.ac_asc = 0
        self.ac_dsc = 0
        self.ac_parts = list()      # (label, ascending) when AC varies by body part.
        self.hoard = ''
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
        """Reformatted hitdice."""
        bonus = ''
        hp = ''
        if self.hd_bonus:
            bonus = f'+{self.hd_bonus}'
        if self.hp:
            hp = f' ({self.hp} hp)'
        return f'{self.hd}{bonus}{hp}'

    @property
    def ac_text(self):
        """Ascending AC, per part if it varies, raw text if not numeric."""
        if len(self.ac_parts) > 1:
            return ', '.join(f'{label} {asc}'.strip() for label, asc in self.ac_parts)
        if self.ac_parts:
            return self.ac_asc
        return self.ac_raw

    @property
    def source_title(self):
        """Full title of source document."""
        return SOURCES.get(self.source, self.source)

    def odd_line(self):
        """OD&D One line statblock."""
        # keys = ('name', 'hd', 'ac', 'sv', 'atk', 'special', 'mv', 'al', 'ml', 'ne', 'cl', 'xp', 'body', 'source', 's15')
        def reduce_damage(match):
            return ODD_DAMAGE.get(match.group(1), match.group(1))
        foo = re.compile(r'([-\d]*)\s*([^(]+)\s*\(([^)]+)\)')
        bits = list()
        attacks = list()
        for old_ in self.attack:
            old = old_.lower()
            old = re.sub(r'weapon or strike', 'strike', old)
            options = list()
            for atk in old.split(' or '):
                match = foo.match(atk)
                #print old,
                if match:
                    count, attack, damage = match.groups()
                    attack = attack.strip()
                    damage = ODD_DAMAGE.get(damage, damage)
                    damage = re.sub(r' \+ ', '+', damage)
                    damage = re.sub(' plus ', '+', damage)
                    with contextlib.suppress(ValueError):
                        if int(count) == 1:
                            count = ''
                    if count:
                        bit = f'{count}x {damage} ({attack})'
                    else:
                        bit = f'{damage} ({attack})'
                    if attack == 'weapon' and not count and damage == 'd6':
                        bit = 'weapon'
                else:
                    bit = f'({atk})'
                options.append(bit)
            new = ' or '.join(options)
            #print '|', new
            attacks.append(new)
        data = self.as_dict()
        data['atk'] = ', '.join(attacks)
        data['ac'] = self.ac_dsc
        data['mv'] = re.sub(r'\s*\(flying\)', '(fly)', data['mv'])
        data['xp'] = ODD_XP.get(self.hd, f'WTF {self.hd}')
        if self.hd in ODD_SV:
            data['sv'] = ODD_SV[self.hd]
        else:
            data['sv'] = max(3, 18-self.hd)
        if self.hd_bonus and isinstance(self.hd_bonus, int) and isinstance(data['xp'], int):
            data['xp'] += 25 * self.hd_bonus
        bits.append(f'''{data['name']}: {data['hd']}hd {data['ac']}AC {data['sv']}+ {data['mv']}", {data['atk']},''')
        if data['special']:
            bits.append(f"**{', '.join(a.lower() for a in data['special'])}**")
        if data['ml']:
            bits.append(f"ML{data['ml']}")
        bits.append(f'''{data['xp']}XP''')
        return ' '.join(bits)

    def stat_line(self):
        """One line statblock."""
        # keys = ('name', 'hd', 'ac', 'sv', 'atk', 'special', 'mv', 'al', 'ml', 'ne', 'cl', 'xp', 'body', 'source', 's15')
        bits = list()
        data = self.as_dict()
        data['atk'] = ', '.join(a for a in data['atk']).replace(')', '').replace('(', '')
        bits.append(f'''{data['name']} {data['hd']}HD [{data['atk']}] AC{data['ac']} {data['sv']}+ {data['mv']}\' ''')
        if data['special']:
            bits.append(f"(**{', '.join(a for a in data['special'])}**)")
        if data['ml']:
            bits.append(f"ML{data['ml']}")
        bits.append(f'''CL{data['cl']} {data['xp']}XP''')
        return ' '.join(bits)

    def format(self, legal=False):
        """ReStructuredText output of entry."""
        lines = [
                self.name,
                '-' * len(self.name),
                ]
        if self.hd:
            lines.extend([
                f':Hit Dice: {self.hitdice}',
                f":Attack: {', '.join(self.attack)}",
                f':AC: {self.ac_text}',
                f':Save: {self.save}',
                f":Special: {', '.join(self.special)}",
                f':Move: {self.move}',
                f':Alignment: {self.alignment}',
                f':CL/XP: {self.cl}/{self.xp}',
                ])
        lines.append(f':Source: {self.source_title}')
        if self.number:
            lines.append('')
            lines.append(f'Number encountered: {self.number}')
        if self.description:
            lines.append('')
            lines.append('\n\n'.join(parapper(p) for p in self.description))
        else:
            print(self.name, file=sys.stderr)
        if legal and self.s15:
            lines.append(f'\nCopyright: {self.s15}')
        return '\n'.join(lines)

    def as_tuple(self):
        """Suitable for JSONification."""
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
        """Suitable for JSONification."""
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
        clone.ac_parts = list(self.ac_parts)
        clone.hoard = self.hoard
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
        """Convert entry into one or more Monster instances.

        Entries with multiple hit dice are split into individual instances.
        :param lines: entry split into lines.
        """
        stop = len(lines)
        name = aliases.get(lines[0].strip(), lines[0].strip())
        # Change mc "foo demon" to "demon, foo"
        if name.lower().endswith(' demon prince'):
            name = 'Demon Prince, ' + name.replace(' Demon Prince', '')
        elif name.lower().endswith(' demon'):
            name = 'Demon, ' + name.replace(' Demon', '')
        if name not in known:
            if name.startswith('Giant '):
                name = name[6:] + ', Giant'
            if name not in known:
                if name:
                    raise ValueError(f'Not known [{name}]')
                else:
                    raise ValueError(f'No name!\n{"\n".join(lines)}')
        try:
            entry = cls(name)
            # if entry.name.endswith(', Giant'):
            #    entry.name = 'Giant %s' % entry.name.rsplit(', ', 1)[0]
            #    entry.name = 'Giant %s' % entry.name.rsplit(', ', 1)[0]
            challenge = False  # Some entries don't have regular stats.
            start = 1  # Start past name.
            while start < stop:
                key, _, value = [b.strip() for b in lines[start].partition(':')]
                if key == 'Source':
                    entry.source = value
                elif key == 'S15':
                    entry.s15 = value
                elif key == 'Hit Dice':
                    parse_hd(entry, value)
                elif key == 'Armor Class':
                    value = value.replace('–', '-')  # noqa: RUF001 en-dash on purpose.
                    entry.ac_raw = value
                    parse_ac(entry, value)
                elif key == 'Saving Throw' or key == 'Save':
                    entry.save = value
                elif key == 'Attack' or key == 'Attacks':
                    start, raw = slurp_re(re_attribute, start, lines, ':')
                    entry.attack = [s.strip().rstrip('.') for s in raw.split(',')]
                elif key == 'Damage':
                    entry.attack = [value, ]
                elif key == 'Special':
                    start, raw = slurp_re(re_attribute, start, lines, ':')
                    entry.special = [s.strip().rstrip('.').replace('magic resistance ', 'MR') for s in raw.split(',') if s.strip().rstrip('.').lower() != 'none']
                elif key.startswith('Move'):
                    # Secondary speeds (Fly, Swim) follow on indented lines.
                    speeds = [value] if value else []
                    while start + 1 < stop and lines[start + 1][:1].isspace():
                        start += 1
                        speeds.append(lines[start].strip())
                    entry.move = ', '.join(speeds)
                elif key == 'Alignment':
                    entry.alignment = value
                elif key == 'Morale':
                    entry.morale = value
                elif key == 'Hoard Class':
                    entry.hoard = value
                elif key in ('Number Encountered', 'No. Enc', 'No. Enc.'):
                    start, raw = slurp_re(re_attribute, start, lines, ':')
                    entry.number = raw
                elif key == 'XP':
                    entry.xp = value
                    start += 1
                    break  # XP is last stat for LL style monsters.
                elif key in ('Challenge Level/XP', 'CL/XP'):
                    challenge = value
                    start += 1
                    break  # CL/XP is last stat for SW style monsters.
                else:
                    # No stats.
                    break
                start += 1
            for para in strip_emptylines(by_para(lines[start:], (custom_break, ))):
                key, _, text = [b.strip() for b in para.partition(':')]
                if key == 'Credit':  # tohc only thing we aren't allowed to use.
                    pass
                elif key == 'Copyright Notice':  # tohc only authors.
                    entry.s15 = f'{entry.s15}; {text}'
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
                entry = entry.clone()
                if hd:  # Multiple entries with different HD.
                    entry.hd = int(hd)
                    entry.name = f"{entry.name.split('(')[0].strip()} ({hd}HD)"
                entry.cl = cl
                entry.xp = int(xp.replace(',', ''))
                # Some entries vary save by hit die.
                with contextlib.suppress(IndexError):
                    entry.save = saves[x]
                yield entry
        except Exception:
            print(f'Line #{start} Mob: {entry.__dict__}\n', file=sys.stderr)
            print('Some Lines:\n', '\n'.join(lines[max(0, start - 10):start + 5]), file=sys.stderr)
            raise


def custom_break(line, accum):
    if '-- Author:' in line:
        return '<author>' + line
    if line and len(line) < 40 and not ('Copyright Notice:' in line or 'Credit:' in line or line.endswith('.')):
        return 'MiniAdventure:' + line


def parse_ac(entry, value):
    """Parse armor class; numeric AC is the worst (easiest to hit) part."""
    if re.fullmatch(r'-?\d+', value):
        entry.ac_dsc = int(value)
        entry.ac_asc = 20 - (int(value) + 1)
        entry.ac_parts = [('', entry.ac_asc)]
        return
    parts = list()
    for label, dsc, asc_bracket, asc_slash in re_ac.findall(value):
        parts.append((label.strip(), int(dsc), int(asc_bracket or asc_slash)))
    if not parts:  # Not numeric: "n/a", "Always hit", etc. Keep ac_raw.
        return
    entry.ac_parts = [(label, asc) for label, _, asc in parts]
    _, entry.ac_dsc, entry.ac_asc = max(parts, key=lambda p: p[1])


re_hp = re.compile(r'^(\d+)\s*hp$')
re_hd = re.compile(r'^(\d+)(?:\+(\d+d?\d*))?\s*(?:\((\d+) hp\))?$')
#re_hd = re.compile(r'^(\d+)(?:\+(\d+d?\d*))?\s*(?:hit points)?\s*(?:\((\d+) hp\))?$')


def parse_hd(entry, value):
    """Complicated parsing of hit dice attribute."""
    try:
        entry.hd = int(value)
    except ValueError:
        match = re_hd.match(value)
        if match:
            hd, bonus, hp = match.groups()
            entry.hd = int(hd)
            entry.hd_bonus = int(bonus) if bonus and bonus.isdigit() else bonus
            if hp:
                entry.hp = int(hp)
        else:
            entry.hd = value
            match = re_hp.match(value)
            if match:
                entry.hp = int(match.group(1))


def split_mc_entries(source, s15, lines):
    """Entry splitter that works on Monster Compendium."""
    entry = list()
    description = list()
    for line in lines:
        if line.startswith('##'):      # Comment line.
            continue
        if RE_EMPTYLINE.match(line):   # Empty lines separate entries.
            entry = list()
            description = list()
            continue
        if len(line) < 30:             # Skip the redundant entry names.
            continue
        # MC has attributes all on one line. Reformat them into style
        # Entry.from_entry understands.
        match = re.match(r'(^[^:]+):\s+(HD .*;.*)$', line)
        if match:
            name, rest = match.groups()
            bits = [b.strip() for b in re_mc_split.split(rest)]
            clxp = None
            entry.append(name)
            entry.append(f'Source: {source}')
            entry.append(f'S15: {s15 % {"name": name}}')
            for bit in bits:
                name, _, value = bit.partition(' ')
                name = name.rstrip(':')
                if name == 'HD':
                    entry.append(f'Hit Dice: {value}')
                elif name == 'AC':
                    entry.append(f"Armor Class: {' ['.join(value.split('['))}")
                elif name == 'Atk':
                    entry.append(f'Attacks: {value}')
                elif name == 'Save':
                    entry.append(f'Saving Throw: {value}')
                elif name == 'Move':
                    entry.append(f'Move: {value}')
                elif name == 'CL/XP':
                    clxp = value
                else:
                    entry.append(bit)
            if clxp is None:
                raise ValueError(f'No CL/XP [{line}]')
            # CL/XP must be last, used to detect end of attributes.
            entry.append(f'CL/XP: {clxp}')
            for para in description:
                entry.append('')
                entry.append(para)
            yield entry
            # Multiple entries under one description.
            entry = list()
        else:
            description.append(line)


def monsterfy(entries):
    """Convert sequence of entry sections into sequence of Monster instances."""
    for entry in entries:
        yield from Monster.from_entry(entry)


def remove_dupes(seq):
    """Prefer in order bm, mon, swc, tohc, vv, mc, dw, ll."""
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
    """Given two-column pages (say from pdftotext -layout), return lines of one column."""
    def good_mid(mid, page):
        return all(len(x) <= mid or x[mid] == ' ' for x in page)

    def calc_mid(page):
        for mid in (39, 38, 40, 37, 41, 36, 42, 35, 43, 34, 44):
            if good_mid(mid, page):
                return mid
    for i, page in enumerate(pages):
        mid = calc_mid(page)
        if mid:
            two = list()
            two.append('')
            for x in page:
                yield x[:mid].strip()
                if len(x) > mid:
                    two.append(x[mid:].strip())
            for x in two:
                yield x
        else:
            print(f'Did not find mid point for page {i}', file=sys.stderr)
            for x in page:
                yield x


def tuco(sources):
    # Tool to use when hand munging text files.
    # Output one column of two column source
    with Path(sources).open() as file:
        pages = list(by_page(strip_newlines(replace_typography(file))))
    print(f'Found {len(pages)} pages', file=sys.stderr)
    print('\n'.join(two_to_one_columns(pages)))


def split_on_monster(source, s15, lines):
    """Parse lines into entry "sections"."""
    if source == 'mc':
        yield from split_mc_entries(source, s15, lines)
        return
    # Delimiter is line after name
    delimiter, skip_delimiter = {
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
    for line in lines:
        if line.startswith(delimiter):
            name = entry.pop()
            if name.startswith('('):  # Some names split onto two lines.
                name = entry.pop() + ' ' + name
            if not first:
                yield entry
            first = False
            entry = [name]
            entry.append(f'Source: {source}')
            entry.append(f'S15: {s15 % {"name": name}}')
            if skip_delimiter:
                continue
        entry.append(line)
    yield entry


def make_menagerie(sources):
    menagerie = list()
    for filename in sources:
        with Path(filename).open() as file:
            s15 = file.readline()
            if not s15.startswith('s15: '):
                raise ValueError('Bad section 15 line.')
            source = Path(filename).name.partition('.')[0].partition('_')[0]
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
            print(mungetext.rst.page('twoColumn'))
        print(thing.format(False))
        print('\n')


def print_one_per_page(seq):
    for thing in seq:
        print(thing.format(False))
        print(mungetext.rst.page('oneColumn'))


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
        return parser.parse_args()

    config = command_line()
    if config.tuco:
        tuco(config.sources)
    else:
        menagerie = make_menagerie(config.sources)
        names = ', '.join(Path(s).name for s in config.sources)
        print(f'Found {len(menagerie)} entries in {names}', file=sys.stderr)
        if config.json:
            print('MOBS =', json.dumps([m.as_dict() for m in menagerie], sort_keys=True, indent=2))
        elif config.minify:
            print('MOBS =', json.dumps([m.as_dict() for m in menagerie], sort_keys=True, separators=(',', ':')))
        elif config.python:
            entries = ',\n    '.join(f'"{m.name.lower()}": {m.as_dict(skip=("body", "source", "s15"))}' for m in menagerie)
            print(f'MOBS = {{\n    {entries}\n    }}')
        elif config.oddline:
            print('\n'.join(m.odd_line() for m in menagerie if isinstance(m.hd, int)))
        elif config.statline:
            print('\n'.join(m.stat_line() for m in menagerie))
        else:
            print(mungetext.rst.title('=', 'Menagerie'))
            # print(mungetext.rst.page('twoColumn'))
            print(mungetext.rst.page('oneColumn'))
            print_one_per_page(menagerie)
