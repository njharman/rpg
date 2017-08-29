#!/usr/bin/env python2
from __future__ import print_function
import re
import random

import click

#     Copper     Silver      Gold        Gems       Jewelry     Magic
# A   1-6:25%    1-6:30%     2-12:35%    6-36:50%   3-18:50%    40%: any 3
# B   1-8:50%    1-6:25%     1-3:25%     1-6:25%    1-6:25%     10%: Weapon, Armor, or misc. weapon
# C   1-12:20%   1-4:30%     Nil         1-4:25%    1-4:25%     10%: any 2
# D   1-8:10%    1-12:15%    1-6:60%     1-8:30%    1-8:30%     20%: any 2 + 1 Potion
# E   1-10:05%   1-12:30%    1-8:25%     1-10:10%   1-10:10%    30%: any 3 + 1 Scroll
# F   Nil        2-20:10%    1-12:45%    2-24:20%   2-24:20%    35%: any 3 non-weapons + 1 Potion and 1 Scroll
# G   Nil        Nil         10-40:75%   3-18:25%   1-10:25%    40%: any 4 + 1 Scroll
# H   3-24:25%   1-100:50%   10-60:75%   1-100:50%  10-40:50%   20%: any 4 + 1 Potion and 1 Scroll
# I   Nil        Nil         Nil         2-16:50%   2-16:50%    20%: any 1


# Greyhawk modified
SWORD = [
    (30, 'Sword +1'),
    (35, 'Sword +1, +2 vs. Lycanthropes'),
    (40, 'Sword +1, +2 vs. Magic-Users and Enchanted Monsters'),
    (45, 'Sword +1, Locating Objects Ability'),
    (50, 'Sword +1, +3 vs. Undead (Clerics)'),
    (55, 'Sword Flaming: +1, +3 vs. Trolls (Ents)'),  # simplified
    (60, 'Sword +2'),
    (65, 'Sword +1, +3 vs. Dragons'),
    (68, 'Sword +1, 2-8 Wishes'),  # reduced chance
    (70, 'Sword +2, Charm Person Ability'),
    (72, 'Sword +3'),
    (73, 'Sword, Energy Draining'),
    (74, 'Sword +2, Nine Steps Draining'),
    (75, 'Sword +4'),
    (76, 'Holy Sword +5'),
    (78, 'Sword of Cold: +3, +5 vs. Fire Using/Dwelling Creatures'),
    (82, 'Sword +2, Slaying'),  # any slaying
    (87, 'Sword +1, Cursed Beserker'),  # more chance of this less of next
    (92, 'Sword -1, Cursed'),
    (97, 'Sword -2, Cursed'),
    (98, 'Dancing Sword'),
    (99, 'Sword of Sharpness'),
    (100, 'Vorpal Blade'),
    ]

# Greyhawk, modified to say Mithral, only plate, added vulnerabil shield
ARMOR = [
    (20, 'Shield +1'),
    (40, 'Plate +1'),
    (50, 'Plate & Shield +1'),
    (57, 'Shield +2'),
    (64, 'Plate +2'),
    (70, 'Plate & Shield +2'),
    (73, 'Shield +3'),
    (76, 'Plate +3'),
    (78, 'Plate & Shield +3'),
    (80, 'Mithral Shield +4'),
    (82, 'Mithral Plate +4'),
    (83, 'Mithral Plate & Shield + 4'),
    (85, 'Adamantite Shield +5'),
    (86, 'Adamantite Plate +5'),
    (87, 'Adamantite Plate & Shield +5'),
    (90, 'Shield of Missile Attraction'),
    (93, '-1-3 Shield of Vulnerability'),
    (99, '-1-3 Plate of Vulnerability'),
    (100, 'Plate of Etherealness'),
    ]

WEAPON = [
    (10, '3-18 Magic Arrows +1'),
    (15, '2-12 Magic Arrows +2'),
    (16, '1-6 Magic Arrows +3'),
    (17, 'Arrow/Bolt of Slaying'),
    (27, '3-18 Magic Bolts +1'),
    (32, '2-12 Magic Crossbow Bolts +2'),
    (42, 'Dagger +1, +2 vs. Smaller man-sized'),
    (47, 'Dagger +1, +3 vs. Bigger man-sized'),
    (48, 'Dagger +3'),
    (50, 'Magic Bow +1'),
    (55, 'Sling +1'),
    (57, 'Crossbow of Accuracy (+3)'),
    (59, 'Crossbow of Speed'),
    (61, 'Crossbow of Distance'),
    (66, 'Axe +1'),
    (67, 'Axe +2'),
    (68, 'Axe +3'),
    (73, '"Unusual Misc Weapon" +1'),
    (78, 'Mace +1'),
    (80, 'Mace +2'),
    (81, 'Mace of Disruption'),
    (86, 'War Hammer +1'),
    (89, 'War Hammer +2'),
    (90, 'War Hammer +3, 6" Throwing Range with Return'),
    (95, 'Spear +1'),
    (96, 'Spear +2'),
    (97, 'Spear +3'),
    (98, 'Axe of Missing'),
    (99, 'Sticky Mace'),
    (100, 'Cursed Spear of Backbiting'),
    ]

# made up low-level
BASIC_WEAPON = [
    (10, '2-12 Magic Arrows +1'),
    (20, '2-12 Magic Bolts +1'),
    (40, 'Dagger +1'),
    (45, 'Sling +1'),
    (50, 'Axe +1'),
    (55, 'Mace +1'),
    (60, 'War Hammer +1'),
    (65, 'Spear +1'),
    (70, '"Unusual Misc Weapon" +1'),
    (80, 'Cursed friend strike'),
    (81, 'Arrow/Bolt of Slaying'),
    ]

POTION = [
    (3, 'Clairaudience'),
    (7, 'Clairvoyance'),
    (10, 'Control Animal'),
    (13, 'Control Dragon'),
    (16, 'Control Giant'),
    (19, 'Control Human'),
    (22, 'Control Plant'),
    (25, 'Control Undead'),
    (28, 'Diminution'),
    (35, 'Delusion'),
    (39, 'ESP'),
    (43, 'Fire Resistance (F)'),
    (47, 'Flying'),
    (51, 'Gaseous Form'),
    (55, 'Giant Strength (F)'),
    (59, 'Growth'),
    (63, 'Healing'),
    (68, 'Heroism (F)'),
    (72, 'Invisibility'),
    (76, 'Invulnerability (F)'),
    (80, 'Levitation'),
    (84, 'Longevity'),
    (86, 'Poison'),
    (89, 'Polymorph Self'),
    (97, 'Speed (F)'),
    (100, 'Treasure Finding'),
    ]

SCROLL_TRAP = [
    (2, 'Summons Monster'),
    (4, '+/-2 penalty to Attack/Saves/AC'),
    (6, 'Death like paralysis 2-8 days (no save)'),
    (7, '4-24 fire to reader (no save).'),
    (8, 'Fatal disease 2d6 turns (no save)'),
    ]

# Greyhawk Scroll
SCROLL = [
    (10, 'trap'),
    (30, '1 Spell'),
    (45, '2 Spells'),
    (55, '3 Spells'),
    (60, 'Protection: Demons'),  # replaced 7 spells
    (70, 'Protection: Lycanthropes'),
    (80, 'Protection: Undead'),
    (90, 'Protection: Elementals'),
    (100, 'Protection: Magic'),
    ]

RING = [
    (5, 'Invisibility'),
    (10, 'Animal Control'),
    (15, 'Human Control'),
    (30, 'Weakness'),
    (35, 'Protection +1'),
    (36, 'Protection +3'),
    (40, 'Three Wishes'),
    (60, 'Delusion'),
    (65, 'Water Walking'),
    (70, 'Fire Resistance'),
    (72, 'Protection +2, 5ft radius'),
    (74, 'Regeneration'),
    (76, 'Djinn Summoning'),
    (78, 'Shooting Stars'),
    (80, 'X-Ray Vision'),
    (82, 'Telekinesis'),
    (95, 'Contrariness'),
    (97, 'Spell Turning'),
    (99, 'Spell Storing'),
    (100, 'Many Wishes'),
    ]

BASIC_RING = [
    (1, 'Animal Control'),
    (2, 'Fire Resistance'),
    (3, 'Invisibility'),
    (4, 'Protection +1'),
    (5, 'Water Walking'),
    (6, 'Protection +1'),
    (7, 'Delusion'),
    (8, 'Weakness'),
    ]

# Greyhawk
WSR = [
    (10, 'Wand of Metal Detection (M)'),
    (15, 'Wand of Enemy Detection (M)'),
    (20, 'Wand of Magic Detection (M)'),
    (25, 'Wand of Secret Doors & Traps Detection (M)'),
    (30, 'Wand of Illusion (M)'),
    (35, 'Wand of Fear (M)'),
    (39, 'Wand of Cold (M)'),
    (43, 'Wand of Paralization (M)'),
    (47, 'Wand of Fire Balls (M)'),
    (51, 'Wand of Lightning Bolts (M)'),
    (55, 'Wand of Polymorph (M)'),
    (59, 'Wand of Negation (M)'),
    (63, 'Staff of Healing (C) *'),
    (67, 'Staff of Commanding (C, M)'),
    (71, 'Snake Staff (C) *'),
    (75, 'Staff of Striking (C, M) *'),
    (77, 'Staff of Withering (C)'),
    (78, 'Staff of Power (M)'),
    (79, 'Staff of Wizardry (M)'),
    (89, 'Rod of Cancellation (All)'),
    (91, 'Rod of Beguiling (M, T)'),
    (93, 'Rod of Absorption (M)'),
    (98, 'Rod of Lordly Might (F)'),
    (99, 'Rod of Rulership (All)'),
    (100, 'Rod of Resurrection (C)'),
    ]

# Modified
BASIC_WSR = [
    (10, 'Wand of Enemy Detection (M)'),
    (15, 'Wand of Magic Detection (M)'),
    (20, 'Wand of Negation (M)'),
    (30, 'Wand of Magic Missiles (M)'),
    (35, 'Staff of Healing (C) *'),
    (40, 'Snake Staff (C) *'),
    (50, 'Rod of Cancellation (All)'),
    ]

"""
d6x larger small large huge enormous legendary
["small", "large", "huge", "enormous", "legendary"]

d100    Small gem
01-10   10
11-25   50
26-75   100
76-90   500
91-00   1000
        5000
        10000
        25000
        50000

10 GP Gems
----------
1. "Agate: Translucent circles of gray, white, brown, blue and/or green"
2. "Hematite: Gray-black"
3. "Tiger Eye: Translucent rich brown with golden center under-hue"
4. "Turquoise: Light blue-green"

50 GP Gems
----------
1. "Bloodstone: Dark gray with red flecks"
2. "Carnelian: Orange to reddish brown"
3. "Jasper: Blue, black to brown"
4. "Moonstone: Translucent white with pale blue glow"

100 GP Gems
-----------
1. "Amber: Transparent watery gold to rich gold"
2. "Amethyst: Transparent deep purple"
3. "Coral: Pinkish"
4. "Jade: Translucent light green, deep green, green and white, white"

500 GP Gems
-----------
1. "Aquamarine: Transparent pale blue green"
2. "Garnet: Translucent red, brown-green, or violet"
3. "Pearl: Lustrous white, yellowish, pinkish, to pure black"
4. "Topaz: Transparent golden yellow"

1000 GP Gems
------------
1. "Diamond: Transparent clear blue-white"
2. "Emerald: Transparent deep bright green"
3. "Ruby: Transparent clear red to deep crimson"
4. "Sapphire: Transparent clear to medium blue"


Furs:    Pelt   Trimming* Cape / Jacket  Coat
beaver   2      20 g.p.   200 g.p.       400 g.p.
ermine   4      120 g.p.  3,600S.P.      7,200g.p.
fox      3      90 S.P.   300 g.p.       600 g.p.
marten   4      10 g.p.   400 g.p.       800 g.p.
mink     3      30 g.p.   100 g.p.       5,400g.p.
muskrat  1      40 g.p.   4,500S.P.      200 g.p.
sable    5      150 g.p.  2,700g.p.      9,000 S.P.
seal     5      25 g.p.   125 g.p.       250 g.p

* on collar cuffs and edges of garment
"""


def d8():
    return random.randint(1, 8)


def d100():
    return random.randint(1, 100)


def table(roll, chart):
    for row in chart:
        val = row[0]
        if roll <= val:
            if len(row) == 2:
                return row[1]
            else:
                return row[1:]


def roll_quantity(text):
    '''replace 2-24 and with roll.'''
    def roll(match):
        dice, total = map(int, match.group(1).split('-'))
        return str(sum(random.randint(1, total / dice) for x in range(dice)))
    return re.sub(r'(\d+-\d+)', roll, text)


def _sword(roll=None, basic=False):
    # TODO: determine slaying
    if basic:
        # 10% cursed -1 sword
        if d100() <= 10:
            return 'Sword -1, Cursed'
        return table(random.randint(1, 60), SWORD)
    else:
        return table(roll or d100(), SWORD)


def _armor(roll=None, basic=False):
    if basic:
        # 10% curse
        if d100() <= 10:
            result = random.choice(('-1-3 Shield of Vulnerability', '-1-3 Shield of Vulnerability', '-1-3 Plate of Vulnerability'))
        else:
            result = table(random.randint(1, 57), ARMOR)
    else:
        result = table(roll or d100(), ARMOR)
    return roll_quantity(result)


def _weapon(roll=None, basic=False):
    if basic:
        result = table(random.randint(1, 81), BASIC_WEAPON)
    else:
        result = table(roll or d100(), WEAPON)
    return roll_quantity(result)


def _potion(roll=None, basic=False):
    '''Last 6+d6 turns.'''
    result = table(roll or d100(), POTION)
    if 'delusion' in result.lower():
        result = '%s (delusion)' % table(d100(), POTION)
    return 'Potion of %s' % result


def _scroll(roll=None, basic=False):
    '''Spells 25% cleric
    level d4+dungeon level
    '''
    result = table(roll or d100(), SCROLL)
    if 'trap' in result.lower():
        result = 'Trapped! %s' % table(d8(), SCROLL_TRAP)
    if 'spell' in result.lower():
        if basic:
            level = random.choice(('1st', '1st', '2nd', '2nd', '3rd'))
        else:
            level = 'random'
        count = int(re.match(r'(\d+)', result).group(1))
        result = '%dx %s level spells (%s)' % (count, level, random.choice(('C', 'M', 'M', 'M',)))
    return 'Scroll %s' % result


def _ring(roll=None, basic=False):
    if basic:
        result = table(roll or d8(), BASIC_RING)
    else:
        result = table(roll or d100(), RING)
    if 'delusion' in result.lower():
        result = '%s (delusion)' % table(d100(), RING)
    return 'Potion of %s' % result


def _wsr(roll=None, basic=False):
    '''
    Wands 200 charges, 6th level effect.
    Staves 100 charges, 8th level effect.
    Rods 25 charges.

    Chargeless: Metal Detection, Enemy Detection, Secret Doors & Traps
    Detection, Healing, Snake Staff, Staff of Striking.
    '''
    if basic:
        result = table(random.randint(1, 50), BASIC_WSR)
        div = 10
    else:
        result = table(roll or d100(), WSR)
        div = 1
    if '*' in result:
        return result
    if 'wand' in result.lower():
        charges = ' [6th, %i charges]' % random.randint(80 / div, 200 / div)
    elif 'staff' in result.lower():
        charges = ' [8th, %i charges]' % random.randint(40 / div, 100 / div)
    elif 'rod' in result.lower():
        charges = ' [%i charges]' % random.randint(15 / div, 25 / div)
    return '%s%s' % (result, charges)


def _misc(roll=None, basic=False):
    return 'misc item'


# Item Expert with map chance into potion
MAGIC_ITEM = [
    (20, 'Sword', _sword),  # Greyhawk
    (30, 'Armor', _armor),  # Greyhawk, slight mod
    (35, 'Weapon', _weapon),  # DMG,
    (65, 'Potion', _potion),  # Expert
    (85, 'Scroll', _scroll),  # Greyhawk slight mod
    (90, 'Ring', _ring),  # Greyhawk
    (95, 'W/S/R', _wsr),
    (100, 'Misc', _misc),
    ]


def _item(roll=None, basic=False):
    result, func = table(roll or d100(), MAGIC_ITEM)
    if func:
        return func(basic=basic)
    else:
        return result


def _martial(roll=None, basic=False):
    foo = random.choice((_sword, _armor, _weapon))
    return foo(roll, basic)


def _noweap(roll=None, basic=False):
    '''Just for type F no potions/scrolls.'''
    foo = random.choice((_ring, _wsr, _misc))
    return foo(roll, basic)


def _2d8_potions(roll=None, basic=False):
    foo = list()
    for i in range(random.randint(1, 4) + random.randint(1, 4)):
        foo.append(_potion(roll, basic))
    return ', '.join(foo)


TREASURE_TYPES = {
    'a':(('cp', 25, '1000-6000'),  ('sp', 30, '1000-6000'),   ('gp', 35, '2000-12000'),  ('gems', 50, '6-36'),  ('jewelry', 50, '3-18'),  ('magic', 40, (_item, _item, _item))),
    'b':(('cp', 50, '1000-8000'),  ('sp', 25, '1000-6000'),   ('gp', 25, '1000-3000'),   ('gems', 25, '1-6'),   ('jewelry', 25, '1-6'),   ('magic', 10, (_martial, ))),
    'c':(('cp', 20, '1000-12000'), ('sp', 30, '1000-4000'),   None,                      ('gems', 25, '1-4'),   ('jewelry', 25, '1-4'),   ('magic', 10, (_item, _item))),
    'd':(('cp', 10, '1000-8000'),  ('sp', 15, '1000-12000'),  ('gp', 60, '1000-6000'),   ('gems', 30, '1-8'),   ('jewelry', 30, '1-8'),   ('magic', 20, (_item, _item, _potion))),
    'e':(('cp',  5, '1000-10000'), ('sp', 30, '1000-12000'),  ('gp', 25, '1000-8000'),   ('gems', 10, '1-10'),  ('jewelry', 10, '1-10'),  ('magic', 30, (_item, _item, _item, _scroll))),
    'f':(None,                     ('sp', 45, '2000-20000'),  ('gp', 45, '1000-12000'),  ('gems', 20, '2-24'),  ('jewelry', 20, '1-12'),  ('magic', 35, (_noweap, _noweap, _noweap, _potion, _scroll))),
    'g':(None,                     None,                      ('gp', 75, '10000-40000'), ('gems', 25, '3-18'),  ('jewelry', 25, '1-10'),  ('magic', 40, (_item, _item, _item, _item, _scroll))),
    'h':(('cp', 25, '3000-24000'), ('sp', 75, '1000-100000'), ('gp', 75, '10000-60000'), ('gems', 50, '1-100'), ('jewelry', 50, '1-40'),  ('magic', 20, (_item, _item, _item, _item, _potion, _scroll))),
    'i':(None,                     None,                      None,                      ('gems', 50, '2-16'),  ('jewelry', 50, '2-16'),  ('magic', 20, (_item, ))),
    'o':(('cp', 25, '1000-4000'),  ('sp', 20, '1000-3000'),   None,                      None,                  None,                     None),
    'q':(None,                     None,                      None,                      ('gems', 50, '1-4'),   None,                     None),
    's':(None,                     None,                      None,                      None,                  None,                     ('magic', 40, (_2d8_potions, ))),
    }


@click.group()
@click.option('-b', '--basic', default=False, is_flag=True, help='Use Basic tables')
@click.option('-r', '--roll', default=None, type=int, help='% roll')
@click.pass_context
def cli(ctx, basic, roll):
    ctx.obj['basic'] = basic
    ctx.obj['roll'] = roll

for name in ('item', 'sword', 'armor', 'weapon', 'potion', 'scroll', 'ring', 'wsr'):
    def inner(name=name):
        def func(ctx, count):
            basic = ctx.obj['basic']
            for x in range(count):
                click.echo(globals()['_%s' % name](ctx.obj['roll'], basic))
        func.__name__ = name
        return func
    func = inner()
    func = click.pass_context(func)
    func = click.argument('count', default=1, type=int)(func)
    cli.command()(func)


@cli.command()
@click.argument('code')
def type(code):
    '''Roll up treasure type A-Z'''
    def doit(bits, data):
        if not data:
            return
        what, chance, result = data
        if d100() <= chance:
            bits.append('%s %s' % (roll_quantity(result), what))

    cp, sp, gp, gem, jewelry, magic = TREASURE_TYPES[code.lower()]
    bits = list()
    doit(bits, cp)
    doit(bits, sp)
    doit(bits, gp)
    doit(bits, gem)
    doit(bits, jewelry)
    if magic:
        what, chance, items = magic
        if d100() <= chance:
            for item_func in items:
                bits.append(item_func())
    click.echo('\n'.join(bits))


if __name__ == '__main__':
    cli(obj={})
