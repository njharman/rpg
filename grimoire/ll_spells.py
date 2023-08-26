#!/usr/bin/env python
# Parse LL AEC and TT to produced various combined spell listings.

import re
import sys
from collections import defaultdict

import rpg.parse
import rpg.legal
import rpg.rst
import spell_data

level_names = ('', '1st Circle', '2nd Circle', '3rd Circle', '4th Circle', '5th Circle', '6th Circle', '7th Circle', '8th Circle', '9th Circle')


def strip_college(spell):
    if spell.endswith(')'):
        return spell[:-4]
    return spell


class Spell(object):
    def __init__(self):
        self.name = None        # Just name not including college.
        self.college = None     # Things like cleric, necromancer.
        self.level = None
        self.range = None
        self.duration = None
        self.source = None      # What book it comes from.
        self.body = list()      # Body text.
        self.variants = list()  # "Indentical to cleric spell of same name.

    def __str__(self):
        return '\n'.join(self.format())

    @property
    def fullname(self):
        '''Name and college.'''
        return '%s (%s)' % (self.name, self.college)

    def as_dict(self):
        return dict(name=self.name, college=self.college, level=self.level, range=self.range, duration=self.duration, source=self.source)

    def format(self):
        self.variants.sort(key=lambda x: x.name)
        lines = list()
        levels = list()
        ranges = list()
        durations = list()
        for varmit in self.variants:
            levels.append(varmit)
            if varmit.range != self.range:
                ranges.append(varmit)
            if varmit.duration != self.duration:
                durations.append(varmit)
        if levels:
            levels.insert(0, self)
            level = ', '.join('%s (%s)' % (s.level, s.college) for s in levels)
        else:
            level = self.level
        if ranges:
            ranges.insert(0, self)
            range = ', '.join('%s (%s)' % (s.range, s.college) for s in ranges)
        else:
            range = self.range
        if durations:
            durations.insert(0, self)
            duration = ', '.join('%s (%s)' % (s.duration, s.college) for s in durations)
            duration = duration.replace('rounds per level', 'rnds/lvl').replace('round per level', 'rnd/lvl').replace('hour per level', 'hr/lvl').replace(' per level', '/lvl')
        else:
            duration = self.duration
        lines.append('.. _%s:\n' % self.name.lower())
        lines.append(self.fullname)
        lines.append('-' * len(self.fullname))
        lines.append(':Circle: %s' % level)
        lines.append(':Range: %s' % range)
        lines.append(':Duration: %s' % duration)
        for para in self.body:
            if not para.strip().startswith('-'):
                lines.append('')
            lines.append(para)
        return lines


def spell_index():
    '''Mapping of all spells to their source.'''
    re_tt_index = re.compile(r'^(.+)\s+\((.+)\)\s*(.+)$')
    index = dict()
    for line in spell_data.spell_index:
        try:
            name, college, source = re_tt_index.match(line).groups()
        except AttributeError as e:
            print e
            print line
        if college:
            name = '%s (%s)' % (name, college)
        if not source.startswith('AEC'):
            source = 'TT %s' % source
        index[name.lower()] = source
    return index


def merge_variants(spells):
    '''Given list of spells find and merge spells that vary only by
    college, level, range, duration.
    '''
    grouped = defaultdict(list)
    for spell in spells:
        grouped[spell.name].append(spell)
    merged = list()
    for group in grouped.values():
        merged.extend(merge_dupe(group))
    merged.sort(key=lambda x: x.name)
    return merged


def merge_dupe(spells):
    '''Given group of spells, find the main one and (possibly) make all the
    others variants.
    '''
    if len(spells) == 1:
        return spells
    unique = list()
    by_college = dict((s.college, s) for s in spells)
    for spell in spells:
        body = (' '.join(spell.body)).lower()
        if 'same name' in body:
            #print >> sys.stderr, spell.fullname
            if 'divine' in body:
                college = 'D'
            elif 'magic-user' in body:
                college = 'M'
            else:
                college = None
            core = by_college.get(college, None)
            if core:
                #print >> sys.stderr, '  variant of', core.fullname
                core.variants.append(spell)
                continue
            #else:
                #print >> sys.stderr, '  no', college, 'college found', spell.fullname
        unique.append(spell)
    return unique


def parse_spells(parse_me, skip=()):
    '''Given properly munged text_files, parsers and list of spells to skip.
    :param parse_me: seq of ('S', 'file', parser) where 'S' is one-letter college name.
    :param skip: spells matching these names will be skipped.
    :return: sorted list of Spell instances.
    '''
    skip_these = [s.lower() for s in skip]
    source_index = spell_index()
    spells = list()
    for college, file, parser in parse_me:
        for spell in parser(open(file)):
            if spell.college is None:
                spell.college = college
            # Verify spell is "known".
            basename = spell.name.lower()
            fullname = spell.fullname.lower()
            if basename in skip_these or fullname in skip_these:
                #print >> sys.stderr, 'Skipping Spell:', spell.fullname
                continue
            source = source_index.get(fullname, source_index.get(basename, None))
            if source is None:
                raise Exception('Unknown Spell: %s' % spell.fullname)
            spell.source = source
            spells.append(spell)
    spells.sort(key=lambda x: x.name)
    #print >> sys.stderr, len(spells), 'spells found'
    return spells


def split_spells(lines):
    '''Generator of spell stanzas.'''
    re_name = re.compile(r'([^(]+)\s*\((.+)\)')
    valid_colleges = spell_data.college_lookup.keys()
    spell = Spell()
    body = list()
    table = list()
    in_table = 0
    for line in lines:
        if not line.strip():
            continue
        if line.startswith('==='):
            if in_table == 0:  # End previous para, start table.
                spell.body.append(' '.join(body))
                body = list()
            if in_table < 2:  # Tables, have three === seperator lines.
                in_table += 1
            else:  # End table.
                table.append(line.rstrip())
                spell.body.append('\n'.join(table))
                in_table = 0
                table = list()
                continue
        if in_table:
            table.append(line.rstrip())
        elif line.startswith('Level:'):  # Start of new spell.
            name = body.pop().replace(' (reversible)', '').replace(' radius', 'r').replace(' Radius', 'r')
            match = re_name.match(name)
            if match:
                name = match.group(1)
                if match.group(2) not in valid_colleges:
                    raise Exception('Unknown college: %s (%s)' % (name, match.group(2)))
            if body:  # End previous para if any.
                spell.body.append(' '.join(body))
                body = list()
            if spell.name:  # If good spell, return it.
                yield spell
            spell = Spell()
            spell.name = name.strip()
            spell.level = line.split(':', 1)[1].strip()
        elif line.startswith('Duration:'):
            spell.duration = line.split(':', 1)[1].strip()
        elif line.startswith('Range:'):
            spell.range = line.split(':', 1)[1].strip()
        else:
            line = line.rstrip()
            body.append(line)
            # Start new paragraph.
            if len(line) < 70 and line.endswith('.'):
                spell.body.append(' '.join(body))
                body = list()
    # Don't forget the last spell/para.
    if body:  # End previous para if any.
        spell.body.append(' '.join(body))
    if spell.name:  # If good spell, return it.
        yield spell


def parse_tt(lines):
    tt = rpg.parse.strip_tt_pagebreaks(lines)
    tt = rpg.parse.strip_comments(tt)
    tt = split_spells(tt)
    return list(tt)


def parse_aec(lines):
    aec = rpg.parse.strip_aec_pagebreaks(lines)
    aec = rpg.parse.strip_comments(aec)
    aec = split_spells(aec)
    return list(aec)


def by_things(spells):
    '''Group sequence of spells by name, level, and class.'''
    byname = dict()
    bylevel = defaultdict(list)
    byclass = defaultdict(lambda: defaultdict(list))
    for spell in spells:
        byname[spell.fullname.lower()] = spell
        byname[spell.name.lower()] = spell
        bylevel[int(spell.level)].append(spell)
        byclass[spell.college][int(spell.level)].append(spell)
    return byname, bylevel, byclass


def list_to_bylevel(spell_list, byname):
    '''Convert spell_list to mapping of spells bylevel.'''
    bylevel = defaultdict(list)
    for i, level in enumerate(spell_list):
        for name in level:
            spell = byname[name.lower()]
            bylevel[i + 1].append(spell)
    return bylevel


def output_tm(trademarks):
    print rpg.rst.title('=', 'Trademarks')
    print rpg.rst.paragraphs(trademarks)


def output_ogl(sec15=(), open='This entire work is designated as Open Game Content under the OGL.', product=''):
    print '\n.. page:: oneColumn'
    print rpg.rst.title('=', 'Open Game License')
    print '\n', open
    if product:
        print '\n', product
    print rpg.rst.title('-', 'License')
    print rpg.rst.paragraphs(rpg.legal.ogl)
    print rpg.rst.paragraphs(rpg.legal.merge_ogl(sec15))


def output_descriptions(spells):
    '''Output spell descriptions, alphabetically.'''
    print '\n.. page:: twoColumn\n'
    startswith = spells[0].name[0]
    for spell in spells:
        if spell.name[0] != startswith and spell.name[0] not in ('K', 'O', 'Y', 'Z'):
            startswith = spell.name[0]
            print '\n.. page:: twoColumn\n'
        print spell
        print '\n'
    for spell in spells:
        print '.. |%s| replace:: *%s*' % (spell.name, spell.name)


def output_unlisted(byname):
    '''Spells not part of normal spell lists.
    Including tomes, excluding divine, rituals and wizard.
    '''
    def funknsort(x):
        # put tome spells last
        if x.college in ('T',):
            return 'zzzzzz%s' % x.name
        return x.name
    listed = set()
    for college in ['Elementalist', 'Illusionist', 'Mage', 'Necromancer', 'Vivimancer']:
        for level in spell_data.lists[college.lower()]:
            listed |= set(strip_college(s).lower() for s in level)
    all = set(strip_college(s.name).lower() for s in byname.values() if s.college not in ('D', 'W', 'R'))
    byname, bylevel, byclass = by_things(byname[s] for s in (all - listed))
    output_college_list('unlisted', bylevel, '#. %(name)s (%(college)s)', sort=funknsort)


def get_college_list(college, byname):
    return list_to_bylevel(spell_data.lists[college.lower()], byname)


def output_level(level, spells, template, sort=lambda x: x.name):
    '''Output one level of spells.'''
    print
    for spell in sorted(spells, key=sort):
        print template % spell.as_dict()


def output_college_list(college, spells, template='#. %(name)s', page=5, sort=lambda x: x.name):
    '''College's list of spells.'''
    if page:
        print '\n.. page:: spellList\n'
        print rpg.rst.title('-', '%s Spell List' % college)
        print '\n.. raw:: pdf\n\n   FrameBreak'
    for level in sorted(spells.keys()):
        if level == page:
            print '\n.. raw:: pdf\n\n   FrameBreak'
        print rpg.rst.title('~', level_names[level])
        output_level(level, spells[level], template, sort)


def do_spell_sheet(spells, college):
    '''Back side of char sheet, five columns.'''
    byname, bylevel, byclass = by_things(spells)
    spells = get_college_list(college.lower(), byname)
    print >> sys.stderr, '%s Spell List' % college
    for level in sorted(spells.keys()):
        print rpg.rst.title('-', level_names[level])
        print
        for spell in sorted(spells[level], key=lambda x: x.name):
            print  '#. %(name)s' % spell.as_dict()
        if level >= 5:
            break
        print '\n.. raw:: pdf\n\n   FrameBreak'


def do_spell_list(spells):
    '''Spell listings'''
    byname, bylevel, byclass = by_things(spells)

    print rpg.rst.title('*', 'Mage Lists')
    output_college_list('Hermeticist', get_college_list('mage', byname))
    output_college_list('Elementalist', get_college_list('Elementalist', byname))
    output_college_list('Illusionist', get_college_list('Illusionist', byname))
    output_college_list('Necromancer', get_college_list('Necromancer', byname))
    output_college_list('Vivimancer', get_college_list('Vivimancer', byname))
    print '\n.. page:: twoColumn\n'
    print rpg.rst.title('*', 'Other Lists')
    output_college_list('Divine', byclass['D'], page=4)
    output_unlisted(byname)
    output_college_list('All', bylevel, '#. %(name)s (%(college)s)')


def do_grimoire(spells):
    merged = merge_variants(spells)
    byname, bylevel, byclass = by_things(spells)
    print >> sys.stderr, '%i spells, %i after merge' % (len(spells), len(merged))

    print rpg.rst.title('*', 'Gold & Glory Grimoire')
    print '''A compact reference of %i spells for use at the game table, ver 2.1.''' % len(merged)
    print '''Compiled and **heavily** edited by Norman J. Harman Jr. <njharman@gmail.com>.'''
    print '''\nSourced from Daniel Proctor's *"AEC"*, Gavin Norman's *"T&T"*, Greg Gillespie's *"BMI & BMII"*. With a few original creations.  No compatibility is claimed with those or any other product. Any mistakes, typos, etc. are assuredly Norm's fault.'''
    print '\n', ' '.join(rpg.legal.aecTM)

    print '''\n.. raw:: pdf\n\n  FrameBreak\n'''
    print rpg.rst.title('=', 'Colleges of Magic')
    print '\nThere are innumerable traditions of magic. Over time, five major colleges have emerged;'
    print '**Hermetics (M)** the original Magi taught by Thoth-Hermes.'
    print '**Elementalists (E)** air, earth, fire, water.'
    print '**Illusionists (I)** like *jazz hands* in your mind!'
    print '**Necromancers (N)** Thantosian black arts survived the empire that spawned them.'
    print '**Vivimancers (V)** manipulators of flesh and nature.'

    print '\nEach college has a traditional set of spells.'
    print '''Magi are generally able to comprehend formulae they find and research (create) formulae for spells from their college. To comprehend other arcane formulae will be more difficult and research is nearly impossible.'''

    print '\nSome spells are not associated with any college;'
    print 'Some may only be cast as **Rituals (R)**.'
#    print 'A handful of spells are exclusive to **Wizards (W)**.'
    print 'Several spells have identical effects to **Divine (D)** prayers.'
    print 'Finally there are **Tomes (T)** of "lost" formulae or the specialized creations of an obscure school.'

    print rpg.rst.title('=', 'Ritual Casting')
    print '''\nAny mage may perform rituals of arcane formulae they have and can read.'''
    print '''\nRituals take **10 minutes** and require concentrated magical energy, known as *Viz* (typically square of spell's circle). But, they need not be memorized ahead of time.'''
    print '''\n*Viz* comes in "pawns" which generally costs 10-20sp per pawn.  In addition, all sorts of mystical plants, substances, animal parts and the like provide "free" *Viz*.'''

    print '''\n.. raw:: pdf\n\n  FrameBreak\n'''
    print rpg.rst.title('-', 'Partial Ritual List')
    output_college_list('Arcane Rituals', byclass['R'], template='#. `%(name)s`_', page=False)
    output_college_list('Hermeticist', get_college_list('mage', byname), template='#. `%(name)s`_')
    output_college_list('Elementalist', get_college_list('Elementalist', byname), template='#. `%(name)s`_')
    output_college_list('Illusionist', get_college_list('Illusionist', byname), template='#. `%(name)s`_')
    output_college_list('Necromancer', get_college_list('Necromancer', byname), template='#. `%(name)s`_')
    output_college_list('Vivimancer', get_college_list('Vivimancer', byname), template='#. `%(name)s`_')
    output_descriptions(merged)

    output_ogl(rpg.legal.aec15 + rpg.legal.tt15 + rpg.legal.bm15)


parse_me = (
    ('I', 'data/illusionist.txt', parse_aec),
    ('M', 'data/mage.txt', parse_aec),
    ('E', 'data/elementalist.txt', parse_tt),
    ('N', 'data/necromancer.txt', parse_tt),
    ('V', 'data/vivimancer.txt', parse_tt),
    ('T', 'data/tome.txt', parse_tt),
    ('T', 'data/bm_spells.txt', parse_tt),
    ('R', 'data/rituals.txt', parse_tt),
    ('D', 'data/zealot.txt', parse_aec),
#    ('W', 'data/wizard.txt', parse_tt),
    )


spells = parse_spells(parse_me)

if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'divine':
        byname, bylevel, byclass = by_things(spells)
        output_college_list('Divine', byclass['D'], page=4)
    elif sys.argv[1].lower() == 'list':
        do_spell_list(spells)
    elif  sys.argv[1].lower() == 'other':
        byname, bylevel, byclass = by_things(spells)
        output_unlisted(byname)
    else:
        do_spell_sheet(spells, sys.argv[1])
else:
    do_grimoire(spells)
