#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

import re
import sys

import rpg.rst
from rpg.rst import parapper, escape_asterisk
from rpg.parse import replace, by_para, strip_newlines, strip_empty
from rpg.mobs import MOBS

# munge MOBS
for mob in MOBS.values():
    mob['atk'] = ', '.join(mob['atk'])
    if mob['special']:
        mob['special'] = '; %s' % ', '.join(mob['special'])
    else:
        mob['special'] = ''

names = (
        'Arnd Cobblestone', 'Fecal Nul', 'Garmeth the Wicked', 'Gurn Hammerhand', 'Kallic the Unmerciful',
        'Minos the Minotaur', 'Minos the Minotaur-Ghast', 'Nathalas the Despicable', 'Nileed Enad',
        'Ossithrax Pejorative', 'Randar Serouc', 'Red Fangs', 'Rendar Serouc', 'Rorteb Meerab',
        'Sir Guy de O\'Veargne', 'Sir Huxley Tallbow', 'The Keeper of the Tablet', 'Uthuk Amon Thar',
        'Zur the Black', 'Zvin Lorktho', 'Leggatos', 'Nulbar',
        'Applewood', 'Arcos', 'Arnaxelda', 'Arnson', 'Baalbek', 'Bannock', 'Barsnowik', 'Brymgn',
        'Crab-Claw', 'Dhekeon', 'Dingo-Baby', 'Dirtin', 'Diveen', 'Emnuron', 'Gak', 'Gallock',
        'Gargar', 'Gblug', 'Gerg', 'Gethron', 'Grizelda', 'Gulwag', 'Gurn', 'Hephecates',
        'Ibex-ibydl' 'Jabbard', 'Jurkgal', 'Kakta', 'Kelingard', 'O\'Veargne', 'Kelmok', 'Kohl',
        'Leggat', 'Lesieg', 'Li\'On-Ess', 'Lorktho', 'Manon-itziq', 'Meerab', 'Meray', 'Minos',
        'Moniphine', 'Mortimer', 'Nathalas', 'Nul', 'Octus', 'Ogbog', 'Oggle', 'Orthos', 'Ossithrax',
        'Panther-man', 'Parnel', 'Rosilk', 'Sarla', 'Sayer of the Truth', 'Serella', 'Serouc' 'Shagrot',
        'Sinnis', 'Sir Pelinore', 'Spider-Pig', 'Tallbow', 'Thala-Kul', 'Thar', 'The Keeper', 'Tumbledown',
        'Uzgot', 'Valtor', 'Ventis', 'Vizix\'Vol', 'Vultrix', 'Willock', 'Wortbad', 'Xxaxik', 'Yark-Bree',
        'Yasuq-Jac', 'Zur', 'Zygstral', 'Grr\'Woof-nub', 'Arnd',
        )

RE_ROOMS = re.compile(r'^(\d+)\. ')
RE_CRYPT = re.compile(r'^(\w+ Crypt \d+:)')
RE_ALPHA = re.compile(r'^([A-Z]\.)')
RE_QUOTE = re.compile(r'("[^"]+")')
RE_ILLUS = re.compile(r'Show the players illustration #\d+ from the Barrowmaze I*\s*Illustration Booklet\.?\s*', flags=re.I)
RE_NAMES = re.compile(r'(%s)' % '|'.join('(?:%s\'?s?)' % n for n in names))
RE_LLMOB = re.compile(
    r"""(?P<name>(?:Greater )?(?:Giant )?[A-Z][-'\w]+(?: of)?(?: [A-Z][-'\w]+)?)(?:\s+\((?P<count>\d+)\))?"""
    r"""\s+AL: [CLN], AC: [^,]+, HD: (?P<hd>[^,]+), HP: [^#]+, #AT: [^,]+, DMG: [^,]+, [A-Z]+\s*\(\d+\)(?:,\s+Spell[^\.]+\.)?''""")


def parse(lines):
    """Parse."""
    collecting = False
    redo = False
    while True:
        if not redo:
            line = lines.next()
        redo = False
        if collecting:
            for stuff in collecting(line):
                if not stuff:
                    break
                yield stuff
            else:
                collecting = False
            continue
        if line.startswith('Burial Alcoves:'):
            accum = list()
            if 'Contents:' in line:
                redo = True
            else:
                accum.append(line)
            collecting = rpg.parse.lookfor(lambda l: l.endswith('.'), accum, rpg.parse.space_reduce)
            continue
        yield line
    if collecting:
        yield collecting(line)


def translate(bits):
    """MOB name."""
    name = bits['name'].lower()
    name = name.replace('mummies', 'mummy')
    name = name.replace('zombies', 'zombie')
    name = name.replace('mongrelmen', 'mongrelman')
    name = name.replace('s of', ' of')
    name = name.replace('margoyle', 'gargoyle, margoyle')
    name = name.replace('clockwork cobra', 'clockwork, cobra')
    name = name.replace('balor demon', 'demon, baalroch')
    name = name.replace('spitting cobra', 'snake, cobra')
    yield name
    yield name.rstrip('s')
    if name.startswith('giant centiped'):
        yield 'centipede, giant (small, non-lethal)'
    if name.startswith('fire beetle'):
        yield 'beetle, giant fire'
    if 'saurus' in name:
        yield 'dinosaur, %s' % name
    yield '%s (%shd)' % (name, bits['hd'])
    yield '%s (%shd)' % (name.rstrip('s'), bits['hd'])
    # Maybe regex pulled in some shit like 'Four', or 'Several'
    yield name.split()[-1].rstrip('s')
    if name.endswith('ies'):
        name = name[:-3] + 'y'
        yield name
    for type in (
            'golem', 'pudding', 'scorpion', 'demon', 'wight', 'elemental', 'zombie', 'clockwork', 'naga',
            'giant', 'mold', 'eagle', 'vulture', 'clockwork', 'spider', 'harpy', 'crab', 'fly', 'swarm',
            'rat', 'ooze', 'fungi', 'snake', 'barrow', 'crypt',
            ):
        if ' %s' % type in name:
            head, tail = name.rsplit(' %s' % type, 1)
            funtime = '%s%s, %s' % (type, tail.rstrip('s'), head)
            yield funtime
            if funtime.endswith('ies'):
                yield funtime[:-3] + 'y'
            yield '%s (%shd)' % (funtime, bits['hd'])


def monsterate(match):
    """Thing with monster."""
    if not match:
        return ''
    bits = match.groupdict('')
    body = match.group(0)
    if bits['count'] == '1':
        bits['count'] = ''
    if bits['name'] in names:
        sys.stderr.write(f'found {bits["name"]}\n')
        return body
    fail = list()
    for name in translate(bits):
        if name in MOBS:
            body = 'MV%(mv)s, %(hd)sHD, %(atk)s%(special)s; %(ac)sAC, %(sv)s+, ML%(ml)s, %(cl)s/%(xp)s' % MOBS[name]
            break
        else:
            fail.append(name)
    else:
        foo = '\n  '.join(fail)
        sys.stderr.write(f'missing {bits["name"]}\n{foo}')
    return '*%s*: %s' % (('%(count)s %(name)s' % bits).strip(), body)


def output(paragraphs):
    """Print all the things."""
    for para in paragraphs:
        if para.startswith('<title>'):
            print()
            print(para[7:].strip())
            print()
            continue
        para = escape_asterisk(para)
        if para.startswith('<order>'):
            print(para[7:].strip())
        elif para.startswith('<table>'):
            print(para[7:].strip())
        elif para.startswith('Burial Alcoves:'):
            alcoves, contents = para.split('Contents: ')
            # print(indenter('Alcoves:\n%s' % alcoves[len('Burial Alcoves: '):]))
            # print(indenter('Contents:\n%s' % contents))
            print('*Alcoves:*', alcoves[len('Burial Alcoves: '):])
            print()
            print('*Contents:*', contents)
        elif para.endswith(':') and len(para) < 50 and rpg.parse.is_cap(para[0]):
            print(rpg.rst.title(3, para))
        else:
            if RE_ROOMS.search(para):
                number, para = para.split('. ', 1)
                print(rpg.rst.title(2, number))
            para = RE_CRYPT.sub(r'**\1**', para)
            para = RE_ALPHA.sub(r'**\1**', para)
            para = RE_ILLUS.sub(r'', para)
            para = RE_NAMES.sub(r'**\1**', para)
            monsters = (monsterate(m) for m in RE_LLMOB.finditer(para))
            para = RE_LLMOB.sub(r'**\g<name>**', para)
            para = RE_QUOTE.sub(r'*\1*', para)
            print(parapper(para))
            for monster in monsters:
                print()
                print(monster)
        print()


if __name__ == '__main__':
    lines = parse(strip_empty(by_para(replace(strip_newlines(open(sys.argv[1]))))))
    output(lines)
