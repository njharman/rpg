#!/usr/bin/env python3
"""Random treasure generation for B/X or Original D&D.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: http://trollandflame.blogspot.com/
"""
import random
import re

import click

from dice import d6, d12, d100


def reduce_groups(things):
    """Combine (count, value, thing)."""
    things = sorted(things, key=lambda x: (x[1], x[2]))
    truecount = 0
    for i, stuff in enumerate(things):
        count, value, thing = stuff
        truecount += count
        try:
            _, nvalue, nthing = things[i + 1]
        except IndexError:
            nvalue = nthing = None
        if value == nvalue and thing == nthing:
            continue
        else:
            yield truecount, value, thing
            truecount = 0


def replace_quantity(text):
    """Roll N-NN return int(result) and replace in text."""
    match = re.match(r'(\d+-\d+)', text)
    if match is None:
        return 1, text
    dice, total = map(int, match.group(1).split('-'))
    value = sum(random.randint(1, total / dice) for x in range(dice))
    return value, re.sub(r'(\d+-\d+)', lambda x: f'{value:,}', text)


def table(chart, roll=None):
    """Roll on chart using roll."""
    if roll is None:
        roll = random.randint(1, chart[-1][0])  # auto detect highest value.
    for row in chart:
        val = row[0]
        if roll <= val:
            if len(row) == 2:
                return row[1]
            else:
                return row[1:]


def _2d8_potions(rules, roll=None):
    things = list()
    for i in range(random.randint(1, 4) + random.randint(1, 4)):
        things.append(_potion(rules, roll))
    return ', '.join(things)


def _d4_scrolls(rules, roll=None):
    things = list()
    for i in range(random.randint(1, 4)):
        things.append(_scroll(rules, roll))
    return ', '.join(things)


def _item(rules, roll=None):
    return table(rules.item, roll)[1](rules)


def _martial(rules, roll=None):
    func = random.choice((_sword, _armor, _weapon))
    return func(rules, roll)


def _noweap(rules, roll=None):
    """Rings, wsr, and misc only."""
    func = random.choice((_ring, _wsr, _misc))
    return func(rules, roll)


def _armor(rules, roll=None):
    result = replace_quantity(table(rules.armor, roll))[1]
    return re.sub(r'(Armor)', rules.armor_type, result)


def _misc(rules, roll=None):
    return replace_quantity(table(rules.misc, roll))[1]


def _potion(rules, roll=None):
    """Last 6+d6 turns."""
    result = table(rules.potion, roll)
    if 'delusion' in result.lower():
        result = f'{table(rules.potion)} (delusion)'
    return f'Potion of {result}'


def _ring(rules, roll=None):
    result = replace_quantity(table(rules.ring, roll))[1]
    if 'delusion' in result.lower():
        result = f'{table(rules.ring)} (delusion)'
    return f'Ring of {result}'


def _sword(rules, roll=None):
    sword = replace_quantity(table(rules.sword, roll))[1]
    if ',' not in sword and d100() <= 10:  # Only if not already funky, double to 2 in 20.
        sword = f'{sword} {rules.special_sword()}'
    elif d100() >= 30:
        sword = f'{sword}: {rules.sentient_sword()}'
    return sword


def _scroll(rules, roll=None):
    """Spells and maps.

    25% are cleric
    level d4+dungeon level
    """
    result = table(rules.scroll, roll)
    if 'trap' == result.lower():
        return f'Trapped Scroll  {table(rules.scroll_trap)}'
    if 'spell' in result.lower():
        caster = random.choice(['Cleric', 'Magic-user', 'Magic-user', 'Magic-user'])
        spells = ', '.join(f'{c}x{x}' for c, _, x in reduce_groups(map(
            lambda x: (1, 0, table(rules.scroll_levels)),
            range(int(re.match(r'(\d+)', result).group(1))),
            )))
        return f'{caster} scroll {spells}'
    return f'Scroll of {result}'


def _weapon(rules, roll=None):
    return replace_quantity(table(rules.weapon, roll))[1]


def _wsr(rules, roll=None):
    result = table(rules.wsr, roll)
    # BX, changed charge dice d12 instead d10.
    if 'wand' in result.lower():
        charges = f' ({d12() + d12()} charges)'
    elif 'staff' in result.lower():
        if 'Healing' in result or 'Snek' in result:
            charges = ''
        else:
            charges = ' ({d12() + d12() + d12()} charges)'
    elif 'rod' in result.lower():
        charges = f' ({d12()} charges)'
    return f'{result}{charges}'
    # Greyhawk
    div = 1
    if '*' in result:
        return result
    if 'wand' in result.lower():
        charges = ' [6th, %i charges]' % random.randint(80 / div, 200 / div)
    elif 'staff' in result.lower():
        charges = ' [8th, %i charges]' % random.randint(40 / div, 100 / div)
    elif 'rod' in result.lower():
        charges = ' [%i charges]' % random.randint(15 / div, 25 / div)
    return f'{result}{charges}'


class Treasures:
    def format(self, things):
        for count, value, thing in sorted(things, key=lambda x: x[1] or 99999):
            yield f'{count:2} x {value or "":4}{"gp" if value else "  "} {thing}'

    def lines(self, count, group):
        return list(self.format(reduce_groups(self._roll(count, group))))

    def roll(self, count, group):
        """List of (count, value, gem)."""
        return list(reduce_groups(self._roll(count, group)))


class Jewelries(Treasures):
    def __init__(self, ruleset):
        if ruleset == 'bx':
            pass
        elif ruleset == 'odd':
            pass
        else:
            raise ValueError(f'Unknown ruleset [{ruleset}]')

    def _roll(self, count, group):
        """Roll up count pieces of jewlery, group ignored."""
        for x in range(count):
            value = (d6() + d6() + d6()) * 100
            if value >= 1800:
                type = 'jewelry platinum and gems'
            elif value >= 1600:
                type = 'jewelry gold with gems'
            elif value >= 1200:
                type = 'jewelry sivler with gems'
            elif value >= 1000:
                type = 'jewelry wrought platinum'
            elif value >= 700:
                type = 'jewelry wrought gold'
            else:
                type = 'jewelry wrought silver'
            yield 1, value, type


class Gems(Treasures):
    def __init__(self, ruleset):
        if ruleset == 'bx':
            self.gem_value_chance = [20, 45, 75, 95, 100]
            self.gem_value_chance = [20, 45, 75, 95, 99, 100]  # modified to give 1% chance of diamond
        elif ruleset == 'odd':
            self.gem_value_chance = [10, 25, 75, 90, 99, 100]
        else:
            raise ValueError(f'Unknown ruleset [{ruleset}]')
        self.values = [10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000]
        self.gems = [
            [  # 10 GP Gems (multicolored)
                'Agate: Multi-colored circles',  # Safe sleep
                'Tiger Eye: Brown with golden center under-hue',
                ],
            [  # 50 GP Gems (stone)
                'Bloodstone: Dark gray with red flecks',  # Weather Control
                'Moonstone: Lustrous white with pale blue glow',  # Lycanthropy
                ],
            [  # 100 GP Gems (solid color)
                'Carnelian: Orange to reddish brown',  # Protection from Evil
                'Jade: Light green, deep green, green and white',  # Protection from poison
                ],
            [  # 500 GP Gems (translucent)
                'Pearl: Lustrous white, pinkish, to pure black',  # Wisdom
                'Topaz: Translucent golden yellow',  # Earth Wards of evil
                ],
            [  # 1000 GP Gems (transparent)
                'Emerald: Transparent deep green',  # Water Undead protection / control
                'Ruby: Transparent crimson',  # Fire Good luck
                'Sapphire: Transparent vivid blue',  # Air inteligence, boosts magic
                ],
            [  # 5000 GP Gems
                'Diamond: Transparent clear blue-white',
                ],
            ]  # noqa
        self.unusual = [
            'Crystal Ball',
            'of Controlling Earth Elementals',
            'Amulet of Non-detection',
            'Scarab of Protection from Level Drain',
            'Scarab of Enraging Enemies',
            'Glowstone as light spell',
            'Warstone +1 if built into weapon',
            'Ioun Stone absorbs d20 spell levels',
            'Ioun Stone geas',
            'Ioun Stone 16 Int',
            'Ioun Stone regen 1hp turn',
            'Ioun Stone +1 spell slot',
            'of Prayer',
            'of Poison Detection',
            'Demonstone',
            ]

    def _roll(self, count, group):
        """Roll up count gems, in groups of size group."""
        size = value = 0
        only_one = False  # Only one magical gem.
        for x in range(count):
            # Roll in groups; but reset when larger, magical or valueable.
            if x % group == 0 or size or value == 0 or value > 500:
                roll = d100()
                for i, v in enumerate(self.gem_value_chance):
                    if roll <= v:
                        gem = random.choice(self.gems[i])
                        value = self.values[i]
                        break
            size = ''
            if x % 10 == 1:  # 1 in 10 gems have chance of being special.
                # 30% chance to be magical, only if 100gp or greator and only one.
                if d100() <= 30 and value >= 100 and not only_one:
                    value = 0
                    if 'Diamond' in gem:  # All magical Diamonds are True Seeing Gems.
                        gem = 'Diamond of True Seeing'
                    else:
                        gem = f'{gem[0:gem.index(":")]} {random.choice(self.unusual)}'
                    only_one = True  # Only one magic gem per hoard.
                # 20% of non-magical gems are larger than usual.
                elif d100() <= 20:
                    mult = random.choice([2, 2, 2, 4, 4, 8])
                    value = value * mult
                    size = {
                        2: 'large',
                        4: 'giant',
                        8: 'enormous',
                        }[mult] + ' '
            yield 1, value, f'{size}{gem}'


"""
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


class Rules:
    scroll_trap = [
        (2, 'Summons Monster'),
        (4, '+/-2 penalty to Attack/Saves/AC'),
        (6, 'Death like paralysis 2-8 days (no save)'),
        (7, '4-24 fire to reader (no save).'),
        (8, 'Fatal disease 2d6 turns (no save)'),
        ]

    def type(self, tt, roll=None):
        """Roll a treasure type."""
        for check in self.TREASURE_TYPES[tt]:
            if check:
                yield from self.roll(*check, roll)

    def roll(self, what, chance, treasure, roll=None):
        """For single check of Treasure Type."""
        if roll is None:
            roll = d100()
        if roll > chance:
            return
        if what == 'magic':
            for item_func in treasure:
                yield item_func(self)
        else:
            count, text = replace_quantity(treasure)
            yield f'{text} {what}'
            if what == 'gems':
                yield from self.gems.lines(count, 10)
            if what == 'jewelry':
                yield from self.jewelries.lines(count, 1)


class OddRules(Rules):
    name = 'odd'
    jewelries = Jewelries('odd')
    gems = Gems('odd')
    TREASURE_TYPES = {
        'a': (('cp', 25, '1000-6000'),  ('sp', 30, '1000-6000'),   ('gp', 35, '2000-12000'),  ('gems', 50, '6-36'),  ('jewelry', 50, '3-18'),  ('magic', 40, (_item, _item, _item))),  # noqa: E241
        'b': (('cp', 50, '1000-8000'),  ('sp', 25, '1000-6000'),   ('gp', 25, '1000-3000'),   ('gems', 25, '1-6'),   ('jewelry', 25, '1-6'),   ('magic', 10, (_martial, ))),  # noqa: E241
        'c': (('cp', 20, '1000-12000'), ('sp', 30, '1000-4000'),   None,                      ('gems', 25, '1-4'),   ('jewelry', 25, '1-4'),   ('magic', 10, (_item, _item))),  # noqa: E241
        'd': (('cp', 10, '1000-8000'),  ('sp', 15, '1000-12000'),  ('gp', 60, '1000-6000'),   ('gems', 30, '1-8'),   ('jewelry', 30, '1-8'),   ('magic', 20, (_item, _item, _potion))),  # noqa: E241
        'e': (('cp',  5, '1000-10000'), ('sp', 30, '1000-12000'),  ('gp', 25, '1000-8000'),   ('gems', 10, '1-10'),  ('jewelry', 10, '1-10'),  ('magic', 30, (_item, _item, _item, _scroll))),  # noqa: E241
        'f': (None,                     ('sp', 45, '2000-20000'),  ('gp', 45, '1000-12000'),  ('gems', 20, '2-24'),  ('jewelry', 20, '1-12'),  ('magic', 35, (_noweap, _noweap, _noweap, _potion, _scroll))),  # noqa: E241
        'g': (None,                     None,                      ('gp', 75, '10000-40000'), ('gems', 25, '3-18'),  ('jewelry', 25, '1-10'),  ('magic', 40, (_item, _item, _item, _item, _scroll))),  # noqa: E241
        'h': (('cp', 25, '3000-24000'), ('sp', 75, '1000-100000'), ('gp', 75, '10000-60000'), ('gems', 50, '1-100'), ('jewelry', 50, '1-40'),  ('magic', 20, (_item, _item, _item, _item, _potion, _scroll))),  # noqa: E241
        'i': (None,                     None,                      None,                      ('gems', 50, '2-16'),  ('jewelry', 50, '2-16'),  ('magic', 20, (_item, ))),  # noqa: E241
        'o': (('cp', 25, '1000-4000'),  ('sp', 20, '1000-3000'),   None,                      None,                  None,                     None),  # noqa: E241
        'q': (None,                     None,                      None,                      ('gems', 50, '1-4'),   None,                     None),  # noqa: E241
        's': (None,                     None,                      None,                      None,                  None,                     ('magic', 40, (_2d8_potions, ))),  # noqa: E241
        }
    item = [
        (20, 'Sword', _sword),  # Greyhawk
        (30, 'Armor', _armor),  # Greyhawk, slight mod
        (35, 'Weapon', _weapon),  # DMG,
        (65, 'Potion', _potion),  # Expert
        (85, 'Scroll', _scroll),  # Greyhawk slight mod
        (90, 'Ring', _ring),  # Greyhawk
        (95, 'W/S/R', _wsr),
        (100, 'Misc', _misc),
        ]
    # Greyhawk, modified to say Mithral, only plate, added vulnerabil shield
    armor = [
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
    misc = [
        (1, '<misc>'),
        ]
    # Greyhawk Scroll
    scroll = [
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
    # Greyhawk modified
    sword = [
        (30, 'Sword +1'),
        (35, 'Sword +1, +2 vs. Lycanthropes'),
        (40, 'Sword +1, +2 vs. Magic-Users and Enchanted Monsters'),
        (45, 'Sword +1, Locating Objects Ability'),
        (50, 'Sword +1, +3 vs. Undead (Clerics)'),
        (55, 'Sword Flaming: +1, +3 vs. Trolls (Ents)'),  # Simplified
        (60, 'Sword +2'),
        (65, 'Sword +1, +3 vs. Dragons'),
        (68, 'Sword +1, 1-4 Wishes'),  # reduced chance
        (70, 'Sword +2, Charm Person Ability'),
        (72, 'Sword +3'),
        (73, 'Sword, Energy Draining'),
        (74, 'Sword +2, Nine Steps Draining'),
        (75, 'Sword +4'),
        (76, 'Holy Sword +5'),
        (78, 'Sword of Cold: +3, +5 vs. Fire Using/Dwelling Creatures'),
        (82, 'Sword +2, Slaying'),  # any slaying
        (87, 'Sword +1, Cursed Beserker'),  # More chance of this less of next
        (92, 'Sword -1, Cursed'),
        (97, 'Sword -2, Cursed'),
        (98, 'Dancing Sword'),
        (99, 'Sword of Sharpness'),
        (100, 'Vorpal Blade'),
        ]
    weapon = [
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
    # Greyhawk
    # Wands 200 charges, 6th level effect.
    # Staves 100 charges, 8th level effect.
    # Rods 25 charges.
    # Chargeless: Metal Detection, Enemy Detection, Secret Doors & Traps Detection, Healing, Snake Staff, Staff of Striking.
    wsr = [
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


class BxRules(Rules):
    name = 'bx'
    jewelries = Jewelries('bx')
    gems = Gems('bx')
    TREASURE_TYPES = {
        'a': (('cp', 25, '1000-6000'),  ('sp', 30, '1000-6000'),   ('ep', 20, '1000-4000'),   ('gp', 35, '2000-12000'),  ('pp', 25, '1000-2000'),   ('gems', 50, '6-36'),  ('jewelry', 50, '6-36'),  ('magic', 30, (_item, _item, _item))),  # noqa: E241
        'b': (('cp', 50, '1000-8000'),  ('sp', 25, '1000-6000'),   ('ep', 25, '1000-4000'),   ('gp', 25, '1000-3000'),   None,                      ('gems', 25, '1-6'),   ('jewelry', 25, '1-6'),   ('magic', 10, (_martial, ))),  # noqa: E241
        'c': (('cp', 20, '1000-12000'), ('sp', 30, '1000-4000'),   ('ep', 10, '1000-4000'),   None,                      None,                      ('gems', 25, '1-4'),   ('jewelry', 25, '1-4'),   ('magic', 10, (_item, _item))),  # noqa: E241
        'd': (('cp', 10, '1000-8000'),  ('sp', 15, '1000-12000'),  None,                      ('gp', 60, '1000-6000'),   None,                      ('gems', 30, '1-8'),   ('jewelry', 30, '1-8'),   ('magic', 15, (_item, _item, _potion))),  # noqa: E241
        'e': (('cp',  5, '1000-10000'), ('sp', 30, '1000-12000'),  ('ep', 25, '1000-4000'),   ('gp', 25, '1000-8000'),   None,                      ('gems', 10, '1-10'),  ('jewelry', 10, '1-10'),  ('magic', 25, (_item, _item, _item, _scroll))),  # noqa: E241
        'f': (None,                     ('sp', 10, '2000-20000'),  ('ep', 20, '1000-8000'),   ('gp', 45, '1000-12000'),  ('pp', 30, '1000-3000'),   ('gems', 20, '2-24'),  ('jewelry', 10, '1-12'),  ('magic', 30, (_noweap, _noweap, _noweap, _potion, _scroll))),  # noqa: E241
        'g': (None,                     None,                      None,                      ('gp', 50, '10000-40000'), ('pp', 50, '1000-6000'),   ('gems', 25, '3-18'),  ('jewelry', 25, '1-10'),  ('magic', 35, (_item, _item, _item, _item, _scroll))),  # noqa: E241
        'h': (('cp', 25, '3000-24000'), ('sp', 50, '1000-100000'), ('ep', 50, '10000-40000'), ('gp', 50, '10000-60000'), ('pp', 25, '5000-20000'),  ('gems', 50, '1-100'), ('jewelry', 50, '10-40'), ('magic', 15, (_item, _item, _item, _item, _potion, _scroll))),  # noqa: E241
        'i': (None,                     None,                      None,                      None,                      ('pp', 30, '1000-8000'),   ('gems', 50, '2-12'),  ('jewelry', 50, '2-12'),  ('magic', 15, (_item, ))),  # noqa: E241
        'j': (('cp', 25, '1000-4000'),  ('sp', 10, '1000-3000'),   None,                      None,                      None,                      None,                  None,                     None),  # noqa: E241
        'k': (None,                     ('sp', 30, '1000-6000'),   ('ep', 10, '1000-2000'),   None,                      None,                      None,                  None,                     None),  # noqa: E241
        'l': (None,                     None,                      None,                      None,                      None,                      ('gems', 50, '1-4'),   None,                     None),  # noqa: E241
        'm': (None,                     None,                      None,                      ('gp', 40, '2000-8000'),   ('pp', 50, '5000-30000'),  ('gems', 55, '5-20'),  ('jewelry', 45, '2-12'),  None),  # noqa: E241
        'o': (None,                     None,                      None,                      None,                      None,                      None,                  None,                     ('magic', 50, (_d4_scrolls, ))),  # noqa: E241
        'u': (('cp', 10, '1-100'),      ('sp', 10, '1-100'),       None,                      ('gp', 5, '1-100'),        None,                      ('gems', 5, '1-4'),    ('jewelry', 5, '1-4'),    ('magic', 2, (_item, ))),  # noqa: E241
        'v': (None,                     ('sp', 10, '1-100'),       ('ep', 10, '1-100'),       ('gp', 10, '1-100'),       ('pp', 5, '1-100'),        ('gems', 10, '1-4'),   ('jewelry', 10, '1-4'),   ('magic', 5, (_item, ))),  # noqa: E241
        }
    item = [  # Expert
        (10, 'Armor', _armor),
        (15, 'Misc', _misc),
        (35, 'Potion', _potion),
        (40, 'Ring', _ring),
        (70, 'Scroll', _scroll),
        (90, 'Sword', _sword),
        (95, 'W/S/R', _wsr),
        (100, 'Weapon', _weapon),
        ]

    def armor_type(self, x):
        return random.choice(['Leather', 'Leather', 'Chain', 'Chain', 'Chain', 'Plate', 'Plate'])

    armor = [
        (15, '+1 Plate'),
        (25, '+1 Plate & +1 Shield'),
        (27, '+1 Plate & +2 Shield'),
        (28, '+1 Plate & +3 Shield'),
        (33, '+2 Armor'),
        (36, '+2 Armor & +1 Shield'),
        (41, '+2 Armor & +2 Shield'),
        (42, '+2 Armor & +3 Shield'),
        (45, '+3 Armor'),
        (46, '+3 Armor & +1 Shield'),
        (47, '+3 Armor & +2 Shield'),
        (48, '+3 Armor & +3 Shield'),
        (51, '-1 Cursed Armor'),
        (53, '-2 Cursed Armor'),
        (54, '+4 Adamantite Plate'),  # Instead of curse
        (56, 'AC9 Armor Cursed'),
        (62, '-2  Cursed Shield'),
        (65, 'Shield of Missile Attraction'),  # Instead of -2 shield
        (85, '+1 Shield'),
        (95, '+2 Shield'),
        (99, '+3 Shield'),
        (100, 'Armor of Etherealness'),  # Added from ODD
        ]
    misc = [
        (1, '<misc>'),
        # (3, 'Amulet against Scrying'),
        # (5, 'Bag of Devouring'),
        # (11, 'Bag of Holding'),
        # (11, 'Boots of Levitation'),
        # (11, 'Boots of Speed'),
        # (11, 'Boots of Traveling and Leaping'),
        # (11, 'Broom of Flying'),
        # (11, 'Crystal Ball'),
        # (11, 'Crystal Ball w/ Clariaudience'),
        # (11, 'Crystal Ball w/ ESP'),
        # (11, 'Displacer Clock'),
        # (11, 'Drums of Panic'),
        # (11, 'Efreeti Bottle'),
        # (11, 'Elven Cloak and Boots'),
        # (11, 'Gauntlets of Ogre Power'),
        # (11, 'Helm of Reading Languages'), # Intead of change alignment
        # (11, 'Helm of Telepathy'),
        # (11, 'Medallion of ESP'),
        # (11, 'Rope of Climbing'),
        ]
    potion = [
        (3, 'Clairaudience'),
        (7, 'Clairvoyance'),
        (10, 'Control Animal'),
        (13, 'Control Dragon'),
        (16, 'Control Giant'),
        (19, 'Control Human'),
        (22, 'Control Plant'),
        (25, 'Control Undead'),
        (32, 'Delusion'),
        (35, 'Diminution'),
        (39, 'ESP'),
        (43, 'Fire Resistance'),
        (47, 'Flying'),
        (51, 'Gaseous Form'),
        (55, 'Giant Strength'),
        (59, 'Growth'),
        (63, 'Healing'),
        (68, 'Heroism'),
        (72, 'Invisibility'),
        (76, 'Invulnerability'),
        (80, 'Levitation'),
        (84, 'Longevity'),
        (86, 'Poison'),
        (89, 'Polymorph Self'),
        (97, 'Speed'),
        (100, 'Treasure Finding'),
        ]
    ring = [
        (5, 'Animal Control'),
        (10, 'Human Control'),
        (16, 'Plant Control'),
        (26, 'Delusion'),
        (29, 'Djinn Summoning'),
        (39, 'Fire Resistance'),
        (50, 'Invisibility'),
        (55, 'Protection +2'),  # Instead of 5' raidius
        (70, 'Protection +1'),
        (72, 'Regeneration'),
        (74, 'Spell Storing'),
        (80, 'Spell Turning'),
        (82, 'Telekinesis'),
        (88, 'Water Walking'),
        (94, 'Weakness'),
        (98, '1-4 Wishes'),  # Replaced multiple 1-2, 1-3, 2-4 to this.
        (100, 'X-Ray Vision'),
        ]
    scroll_levels = [
        (25, '1st'),
        (50, '2nd'),
        (70, '3rd'),
        (85, '4th'),
        (95, '5th'),
        (100, '6th'),
        ]
    scroll = [
        (15, '1 Spell'),
        (25, '2 Spells'),
        (31, '3 Spells'),
        (34, '5 Spells'),
        (35, 'Protection: Demons'),  # Replaced 7 spells.
        (40, 'trap'),  # Replaced cursed
        (50, 'Protection: Elementals'),
        (60, 'Protection: Lycanthropes'),
        (65, 'Protection: Magic'),
        (75, 'Protection: Undead'),
        (80, 'Map to magic item.'),
        (82, 'Map to 1d6×10 gems and 2d10 pieces of jewellery.'),
        (82, 'Map to 2 magic items.'),
        (83, 'Map to 3 magic items (no swords).'),
        (84, 'Map to 3 magic items and 1 potion.'),
        (85, 'Map to 3 magic items, 1 scroll, 1 potion.'),
        (86, 'Map to 5d6 gems and 2 magic items.'),
        (90, 'Map to Hoard worth 1d4 × 1,000gp.'),
        (95, 'Map to Hoard worth 5d6 × 1,000gp.'),
        (96, 'Map to Hoard worth 5d6 × 1,000gp and 1 magic item.'),
        (98, 'Map to Hoard worth 5d6 × 1,000gp and 5d6 gems.'),
        (100, 'Map to Hoard worth 6d6 × 1,000gp.'),
        ]
    sword = [
        (2, '-1 Sword, Cursed'),
        (4, '-2 Sword, Cursed Beserker'),  # Added Beserker
        (40, '+1 Sword'),
        # Replaced 4 +1 with these
        (42, '+1 Sword of Cold: +3 vs. Fire Creatures'),
        (43, 'Dancing Sword'),
        (44, 'Vorpal Blade'),
        (50, '+1 Sword, +2 vs. Lycanthropes'),
        (56, '+1 Sword, +2 vs. Spell Users'),
        (60, '+1 Sword, +3 vs. Dragons'),
        (61, '+1 Sword, Dragon Slaying'),  # Replaced 1 vs Dragons
        (66, '+1 Sword, +3 vs. Enchanted'),
        (71, '+1 Sword, +3 vs. Regenerating'),
        (76, '+1 Sword, +3 vs. Undead'),
        (77, '+1 Sword, Energy Drain'),
        (81, '+1 Sword, Flaming, +2 vs troll, flying, +3 vs plant, undead'),
        (89, '+1 Sword, Light'),
        (92, '+1 Sword, Locate Objects'),
        (93, '+1 Sword, 1-4 Wishes'),
        (96, '+2 Sword'),
        (98, '+2 Sword, Charm Humanoid'),
        (100, '+3 Sword'),
        ]

    def special_sword(self):
        # 1/20 are special purpose (also sentient)
        purpose = table([
            (1, 'Arcane casters'),
            (2, 'Divine casters'),
            (3, 'Warriors'),
            (4, '<roll for monster>'),
            (5, 'Lawfuls'),
            (6, 'Chaotics'),
            ])
        alignment = purpose[:-1] if purpose in ('Lawfuls', 'Chaotics') else None
        return f'of Slaying {purpose}: {self.sentient_sword(alignment=alignment, ego=12)}'

    def sentient_sword(self, alignment=None, ego=None):
        extraordinary_powers = [
            (10, 'Clairaudience'),
            (20, 'Clairvoyance'),
            (30, 'ESP (3/day)'),
            (35, '3x damage for d6 rnds (1/day)'),  # Can be duplicated.
            (40, 'Flying (3/day)'),
            (45, 'Heal as spell (1/day)'),  # Can be duplicated.
            (54, 'Illusion (3/day)'),
            (59, 'Levitation'),
            (69, 'Telekinesis (3/day)'),
            (79, 'Telepatthy (3/day)'),
            (88, 'Teleportation (3/day)'),
            (97, 'X-Ray Vision (3/day)'),
            (99, 'roll twice'),
            (100, 'roll thrice'),
            ]
        sensory_powers = [
            (5, 'Know Depth & Direction'),  # Replaced slopes with this and swapped with detect good/evil.
            (10, 'Detect Slopes & Shifting/Teleports'),  # Combined, added teleport and swapped with detect good/evil.
            (15, 'Locate Gems 60 ft. (3/day)'),
            (25, 'Sense Magic 20 ft. (3/day)'),
            (35, 'Locate Named Metal 60 ft. (3/day)'),
            (50, 'Sense Chaos 20 ft.'),  # Split and trippled rarity.
            (65, 'Sense Law 20 ft.'),  # Split and trippled rarity.
            (75, 'See Traps (3/day)'),
            (85, 'See Secret Doors (3/day)'),
            (95, 'See Invisible'),
            (99, 'roll for extraordinary'),
            (100, 'roll twice'),
            ]
        # 30% and all special purpose re sentient.
        if alignment is None:
            alignment = table([(13, 'Lawful'), (18, 'Neutral'), (20, 'Chaotic')])
        if ego is None:
            ego = d12()
        intelligent = d6() + 6
        powers = list()
        if intelligent >= 10:
            powers.append('speech')
        elif intelligent >= 7:
            powers.append('empathy')
        if intelligent >= 11:
            powers.append('reads')
        extra = min(1, (intelligent - 11))
        power = min(3, (intelligent - 6))
        while power > 0:
            result = table(sensory_powers)
            if result == 'roll twice':
                power += 1
            elif result == 'roll for extraordinary':
                extra += 1
                power -= 1
            elif result not in powers:
                powers.append(result)
                power -= 1
        while extra > 0:
            result = table(extraordinary_powers)
            if result == 'roll twice':
                extra += 1
            elif result == 'roll thrice':
                extra += 2
            elif result not in powers:
                powers.append(result)
                extra -= 1
            elif '3x damge' in result or 'Heas as spell' in result:
                powers.append(result)
                extra -= 1
        return f'{alignment} {ego} Ego, {intelligent} Int, {", ".join(powers)}'

    wsr = [
        # Rods d10 charges
        (8, 'Rod of Cancellation (any)'),
        # Staffs 3d10 charges
        (11, 'Staff of Commanding (DA)'),
        (21, 'Staff of Healing (D)'),  # Chargeless.
        (23, 'Staff of Power (A)'),
        (28, 'Snek Staff (D)'),  # Chargeless.
        (31, 'Staff of Striking (any)'),  # Allow any.
        (34, 'Staff of Withering (D)'),
        (35, 'Staff of Wizardry (A)'),
        # Wands 2d10 charges
        (40, 'Wand of Cold'),
        (45, 'Wand of Enemy Detection'),
        (50, 'Wand of Fear'),
        (55, 'Wand of Fire'),  # Changed from Fire Balls
        (60, 'Wand of Illiusion'),
        (65, 'Wand of Lighting'),  # Changed from Lighting Bolts
        (70, 'Wand of Magic Detection'),
        (75, 'Wand of Metal Detection (any)'),  # Allow any
        (80, 'Wand of Negation'),
        (85, 'Wand of Paralysation'),
        (90, 'Wand of Polymorph'),
        (95, 'Wand of Secret Door Detection'),
        (100, 'Wand of Trap Detection'),
        ]
    weapon = [
        (2, '3-30 +1 Arrows'),
        (12, '2-24 +1 Arrows'),
        (17, '1-6 +2 Arrows'),
        (18, 'Arrow of Slaying'),  # Replace 1 +2 arrow
        (27, 'Axe +1'),
        (30, 'Axe +2'),
        (33, 'Bow +1'),
        (43, '2-24 +1 Bolts'),
        (45, '3-30 +1 Bolts'),
        (51, '1-6 +2 Bolts'),
        (52, 'Bolts of Slaying'),  # Replace 1 +2 bolt
        (55, 'Dagger +1'),
        (56, 'Dagger +2, +3 vs bad things'),
        (64, 'Mace +1'),
        (67, 'Mace +2'),
        (68, 'Mace +3'),
        (74, 'Sling +1'),
        (82, 'Spear +1'),
        (86, 'Spear +2'),
        (87, 'Spear +3'),
        (94, 'War Hammer +1'),
        (99, 'War Hammer +2'),
        (100, 'Dwarven Hammer +3'),
        ]


class BasicRules(BxRules):
    name = 'basic'
    jewelries = Jewelries('bx')
    gems = Gems('bx')
    item = [  # Expert
        (10, 'Armor', _armor),
        (15, 'Misc', _misc),
        (40, 'Potion', _potion),
        (45, 'Ring', _ring),
        (65, 'Scroll', _scroll),
        (85, 'Sword', _sword),
        (90, 'W/S/R', _wsr),
        (100, 'Weapon', _weapon),
        ]
    armor = [
        (1, 'Armor +1'),
        (2, 'Armor +1 & Shield +1'),
        (3, 'Cursed Armor AC9'),
        (4, 'Shield +1'),
        ]
    misc = [
        (1, 'Bag of Devouring'),
        (2, 'Bag of Holding'),
        (3, 'Broom of Flying'),
        (4, 'Scarab of Protection'),  # Instead of Crystal Ball.
        (5, 'Elven Cloak and Boots'),
        (6, 'Gauntlets of Ogre Power'),
        (7, 'Helm of Reading Languages'),  # Intead of change alignment.
        (8, 'Helm of Telepathy'),
        (9, 'Medallion of ESP'),
        (10, 'Rope of Climbing'),
        ]
    potion = [
        (1, 'Diminution'),
        (2, 'ESP'),
        (3, 'Gaseous Form'),
        (4, 'Growth'),
        (5, 'Healing'),
        (6, 'Invisibility'),
        (7, 'Levitation'),
        (8, 'Poison'),
        ]
    ring = [
        (1, 'Animal Control'),
        (2, 'Fire Resistance'),
        (3, 'Invisibility'),
        (4, 'Protection +1'),
        (5, 'Water Walking'),
        (6, 'Weakness'),
        ]
    scroll_levels = [
        (50, '1st'),
        (83, '2nd'),
        (100, '3rd'),
        ]
    scroll = [
        (1, '1 Spell'),
        (2, '2 Spells'),
        (3, '3 Spells'),
        (4, 'trap'),
        (5, 'Protection: Lycanthropes'),
        (6, 'Protection: Undead'),
        (7, 'Map to magic item.'),
        (8, 'Map to Hoard worth 1d4 × 1,000gp.'),
        ]
    sword = [  # totally changed much increased chances of +1, light, double chance of cursed
        (2, '-1 Sword, Cursed'),
        (3, '+1 Sword, +2 vs. Lycanthropes'),
        (4, '+1 Sword, +2 vs. Spell Users'),
        (5, '+1 Sword, +3 vs. Dragons'),
        (7, '+1 Sword, +3 vs. Undead'),
        (8, '+2 Sword'),
        (10, '+1 Sword, Light'),
        (14, '+1 Sword'),
        ]
    wsr = [
        (1, 'Rod of Cancellation'),
        (2, 'Staff of Healing (D)'),
        (3, 'Snek Staff (D)'),
        (4, 'Wand of Enemy Detection (A)'),
        (5, 'Wand of Magic Detection (A)'),
        (6, 'Wand of Paralysation (A)'),
        ]
    weapon = [
        (1, '2-24 +1 Arrows'),
        (2, 'Axe +1'),
        (3, 'Dagger +1'),
        (4, 'Mace +1'),
        (5, 'Spear +1'),  # Added Spear
        ]


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        if cmd_name == 'gems':
            return click.Group.get_command(self, ctx, 'gem')


@click.command(cls=AliasedGroup)
@click.option('-l', '--low-level', default=False, is_flag=True, help='Use B/X level 1-3 tables.')
@click.option('-o', '--odd', default=False, is_flag=True, help='Use ODD/Greyhawk tables.')
@click.option('-r', '--roll', default=None, type=int, help='Use this d100 roll.')
@click.pass_context
def cli(ctx, low_level, odd, roll):
    """Roll up treasure hoards and items. B/X by default."""
    if low_level:
        treasure = BasicRules()
    elif odd:
        treasure = OddRules()
    else:
        treasure = BxRules()
    click.echo(f'Using {treasure.name} rules.')
    ctx.obj['treasure'] = treasure
    ctx.obj['roll'] = roll


for name in ('item', 'sword', 'armor', 'weapon', 'potion', 'scroll', 'ring', 'wsr'):
    def _inner(name=name):
        def func(ctx, count):
            click.echo('\n'.join(f'{c} x {x}' for c, v, x in reduce_groups(map(
                lambda x: (1, 0, globals()[f'_{name}'](ctx.obj['treasure'], ctx.obj['roll'])),
                range(count),
                ))))
        func.__name__ = name
        func.__doc__ = 'Roll up ' + {
                'wsr': 'wand, staff, rod.',
                'item': 'misc magic item.',
                'scroll': 'magic scrolls and maps.',
                'potion': 'potioins.'}.get(name, f'magic {name}s.')
        return func
    func = _inner()
    func = click.pass_context(func)
    func = click.argument('count', default=1, type=int)(func)
    cli.command()(func)


@cli.command()
@click.argument('count', default=1)
@click.argument('group', default=1)
@click.pass_context
def jewelry(ctx, count, group):
    """Roll up Jewelries."""
    if count > 1:
        click.echo(f'{count} jewelries in groups of {group}:')
    t = ctx.obj['treasure']
    click.echo('\n'.join(t.jewelries.lines(count, group)))


@cli.command()
@click.argument('count', default=1)
@click.argument('group', default=1)
@click.pass_context
def gem(ctx, count, group):
    """Roll up gems."""
    if count > 1:
        click.echo(f'{count} gems in groups of {group}:')
    t = ctx.obj['treasure']
    click.echo('\n'.join(t.gems.lines(count, group)))


@cli.command()
@click.option('-s', '--something', default=False, is_flag=True, help='Re-reoll until something.')
@click.argument('code')
@click.pass_context
def type(ctx, code, something):
    """Roll up treasure type."""
    t = ctx.obj['treasure']
    stuff = list(t.type(code.lower()))
    while something and not stuff:
        stuff = list(t.type(code.lower()))
    click.echo('\n'.join(stuff) or 'Nothing')


if __name__ == '__main__':
    cli(obj={})
