#!/usr/bin/env python3
"""Parse / reformat text from RPG PDFs."""
# vim: set fileencoding=utf-8 :

import re
import sys
from pathlib import Path

import munge
from munge import by_para, replace_typography, strip_emptylines, strip_newlines
from munge.out import parapper
from munge.rst import escape_asterisk

from rpg.mobs import MOBS

# munge MOBS
for mob in MOBS.values():
    mob['atk'] = ', '.join(mob['atk'])
    if mob['special']:
        mob['special'] = f"; {', '.join(mob['special'])}"
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
        'Ibex-ibydlJabbard', 'Jurkgal', 'Kakta', 'Kelingard', 'O\'Veargne', 'Kelmok', 'Kohl',
        'Leggat', 'Lesieg', 'Li\'On-Ess', 'Lorktho', 'Manon-itziq', 'Meerab', 'Meray', 'Minos',
        'Moniphine', 'Mortimer', 'Nathalas', 'Nul', 'Octus', 'Ogbog', 'Oggle', 'Orthos', 'Ossithrax',
        'Panther-man', 'Parnel', 'Rosilk', 'Sarla', 'Sayer of the Truth', 'Serella', 'SeroucShagrot',
        'Sinnis', 'Sir Pelinore', 'Spider-Pig', 'Tallbow', 'Thala-Kul', 'Thar', 'The Keeper', 'Tumbledown',
        'Uzgot', 'Valtor', 'Ventis', 'Vizix\'Vol', 'Vultrix', 'Willock', 'Wortbad', 'Xxaxik', 'Yark-Bree',
        'Yasuq-Jac', 'Zur', 'Zygstral', 'Grr\'Woof-nub', 'Arnd',
        )

RE_ROOMS = re.compile(r'^(\d+)\. ')
RE_CRYPT = re.compile(r'^(\w+ Crypt \d+:)')
RE_ALPHA = re.compile(r'^([A-Z]\.)')
RE_QUOTE = re.compile(r'("[^"]+")')
RE_ILLUS = re.compile(r'Show the players illustration #\d+ from the Barrowmaze I*\s*Illustration Booklet\.?\s*', flags=re.I)
_names_pattern = '|'.join(f"(?:{n}'?s?)" for n in names)
RE_NAMES = re.compile(f'({_names_pattern})')
RE_LLMOB = re.compile(
    r"""(?P<name>(?:Greater )?(?:Giant )?[A-Z][-'\w]+(?: of)?(?: [A-Z][-'\w]+)?)(?:\s+\((?P<count>\d+)\))?"""
    r"""\s+AL: [CLN], AC: [^,]+, HD: (?P<hd>[^,]+), HP: [^#]+, #AT: [^,]+, DMG: [^,]+, [A-Z]+\s*\(\d+\)(?:,\s+Spell[^\.]+\.)?''""")


def strip_tt_pagebreaks(lines):
    """TT has pagenumber preceding pagebreak."""
    previous = None
    for line in lines:
        if munge.PAGE_BREAK in line:
            line = line.replace(munge.PAGE_BREAK, '')
            previous = None
        if previous is not None:
            yield previous
        previous = line
    if previous:
        yield previous


def strip_aec_pagebreaks(lines):
    """AEC has pagenumber after pagebreak and page break line is garbage."""
    skip = False
    for line in lines:
        if munge.PAGE_BREAK in line:
            skip = True
            continue
        if skip:
            skip = False
            continue
        yield line


def parse(lines):
    """Parse."""
    collecting = False
    redo = False
    while True:
        if not redo:
            line = next(lines)
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
            collecting = munge.lookfor(lambda x: x.endswith('.'), accum, munge.space_reduce)
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
        yield f'dinosaur, {name}'
    yield f"{name} ({bits['hd']}hd)"
    yield f"{name.rstrip('s')} ({bits['hd']}hd)"
    # Maybe regex pulled in some shit like 'Four', or 'Several'
    yield name.split()[-1].rstrip('s')
    if name.endswith('ies'):
        name = name[:-3] + 'y'
        yield name
    for monster in (
            'golem', 'pudding', 'scorpion', 'demon', 'wight', 'elemental', 'zombie', 'clockwork', 'naga',
            'giant', 'mold', 'eagle', 'vulture', 'clockwork', 'spider', 'harpy', 'crab', 'fly', 'swarm',
            'rat', 'ooze', 'fungi', 'snake', 'barrow', 'crypt',
            ):
        if f' {monster}' in name:
            head, tail = name.rsplit(f' {monster}', 1)
            funtime = f"{monster}{tail.rstrip('s')}, {head}"
            yield funtime
            if funtime.endswith('ies'):
                yield funtime[:-3] + 'y'
            yield f"{funtime} ({bits['hd']}hd)"


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
            mob = MOBS[name]
            body = (
                f"MV{mob['mv']}, {mob['hd']}HD, {mob['atk']}{mob['special']}; "
                f"{mob['ac']}AC, {mob['sv']}+, ML{mob['ml']}, {mob['cl']}/{mob['xp']}"
            )
            break
        fail.append(name)
    else:
        foo = '\n  '.join(fail)
        sys.stderr.write(f'missing {bits["name"]}\n{foo}')
    label = f"{bits['count']} {bits['name']}".strip()
    return f'*{label}*: {body}'


def output(paragraphs):
    """Print all the things."""
    for para in paragraphs:
        if para.startswith('<title>'):
            print()
            print(para[7:].strip())
            print()
            continue
        para = escape_asterisk(para)
        if para.startswith(('<order>', '<table>')):
            print(para[7:].strip())
        elif para.startswith('Burial Alcoves:'):
            alcoves, contents = para.split('Contents: ')
            # print(indenter(f"Alcoves:\n{alcoves[len('Burial Alcoves: '):]}"))
            # print(indenter(f'Contents:\n{contents}'))
            print('*Alcoves:*', alcoves[len('Burial Alcoves: '):])
            print()
            print('*Contents:*', contents)
        elif para.endswith(':') and len(para) < 50 and munge.is_cap(para[0]):
            print(munge.rst.title(3, para))
        else:
            if RE_ROOMS.search(para):
                number, para = para.split('. ', 1)
                print(munge.rst.title(2, number))
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
    lines = parse(strip_emptylines(by_para(replace_typography(strip_newlines(Path(sys.argv[1]).open())))))
    output(lines)
