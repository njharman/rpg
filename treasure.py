#!/usr/bin/env python3
"""Random treasure generation for B/X or Original D&D.

Rulesets (command line flag, class):
    -b basic        B/X levels 1-3 tables.
    -x expert       B/X Expert tables (default).
    -o odd          OD&D Vol 2 (Monsters & Treasure), exactly as written.
    -g greyhawk     OD&D Vol 2 + Greyhawk supplement, exactly as written.
    -a alt-greyhawk Greyhawk with Norm's tweaks; each tweak is commented in the class.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: http://trollandflame.blogspot.com/
"""
import collections
import random
import re

import click
from die import d6, d12, d100


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
    """Roll every N-M (N dice, max M) in text; return (first roll, text with the rolls in place).

    N000-M000 is in thousands, e.g. 1000-6000 is 1d6 x 1000.
    A range that is not N dice (2-5) is uniform.
    """
    rolls = []

    def roll(match):
        dice, total = map(int, match.groups())
        scale = 1
        if dice and dice % 1000 == 0 and total % 1000 == 0:
            dice, total, scale = dice // 1000, total // 1000, 1000
        if dice and total % dice == 0:
            value = sum(random.randint(1, total // dice) for _ in range(dice))
        else:
            value = random.randint(dice, total)
        rolls.append(value * scale)
        return f'{value * scale:,}'
    result = re.sub(r'(\d+)-(\d+)', roll, text)
    return (rolls[0] if rolls else 1), result


def table(chart, roll=None):
    """Roll on chart using roll."""
    if roll is None:
        roll = random.randint(1, chart[-1][0])  # auto detect highest value.
    for row in chart:
        val = row[0]
        if roll <= val:
            if len(row) == 2:
                return row[1]
            return row[1:]


def _2d8_potions(rules, roll=None):
    return ', '.join(_potion(rules, roll) for _ in range(random.randint(1, 4) + random.randint(1, 4)))


def _d4_scrolls(rules, roll=None):
    return ', '.join(_scroll(rules, roll) for _ in range(random.randint(1, 4)))


def _rolled(rules, name, roll=None):
    """Roll on rules.<name>, fill in any <details>, roll any quantities."""
    return replace_quantity(rules.detail(table(getattr(rules, name), roll)))[1]


def _item(rules, roll=None, skip=()):
    """Roll item category and item, rerolling categories named in skip."""
    while True:
        name, func = table(rules.item, roll)
        if name not in skip:
            return func(rules)
        roll = None


NO_WEAPONS = ('Sword', 'Misc. Weapon')


def _any(rules, roll=None, skip=()):
    """OD&D Vol 2 Magic/Maps Determination table: 75% magic item, 25% map."""
    if (roll or d100()) > 75:
        return _map(rules)
    return _item(rules, skip=skip)


def _noweap_any(rules, roll=None):
    """OD&D Vol 2 Type F: "no weapons, any other"."""
    return _any(rules, roll, skip=NO_WEAPONS)


def _martial(rules, roll=None):
    func = random.choice((_sword, _armor, _weapon))
    return func(rules, roll)


def _noweap(rules, roll=None):
    """Rings, wsr, and misc only."""
    func = random.choice((_ring, _wsr, _misc))
    return func(rules, roll)


def _armor(rules, roll=None):
    return re.sub(r'(Armor)', rules.armor_type, _rolled(rules, 'armor', roll))


def _misc(rules, roll=None):
    result = table(rules.misc, roll)
    if isinstance(result, list):  # Greyhawk, roll for which table, then on it.
        result = table(result, roll)
    return replace_quantity(rules.detail(result))[1]


def _potion(rules, roll=None):
    """Last 6+d6 turns."""
    result = _rolled(rules, 'potion', roll)
    liar = next((word for word in rules.mislead if word in result.lower()), None)
    if liar:  # Referee misleads, potion looks like another.
        fake = result
        while any(word in fake.lower() for word in rules.mislead):
            fake = _rolled(rules, 'potion')
        result = f'{fake} ({liar})'
    return result if result.startswith('Oil') else f'Potion of {result}'


def _ring(rules, roll=None):
    result = _rolled(rules, 'ring', roll)
    if 'delusion' in result.lower():
        fake = result
        while 'delusion' in fake.lower():
            fake = _rolled(rules, 'ring')
        result = f'{fake} (delusion)'
    return f'Ring of {result}'


def _sword(rules, roll=None):
    return rules.sword_extras(_rolled(rules, 'sword', roll))


def _scroll(rules, roll=None):
    """Spells and maps.

    25% are cleric
    level d4+dungeon level
    """
    result = table(rules.scroll, roll)
    if result.lower() == 'trap':
        return f'Trapped Scroll  {table(rules.scroll_trap)}'
    if result.lower() == 'curse':
        return f'Cursed Scroll: {table(rules.scroll_trap)}'
    if 'spell' in result.lower():
        caster = random.choice(['Cleric', 'Magic-user', 'Magic-user', 'Magic-user'])
        count = int(re.match(r'(\d+)', result).group(1))
        spells = ', '.join(f'{c}x{x}' for c, _, x in reduce_groups((1, 0, rules.spell_level(caster)) for x in range(count)))
        return f'{caster} scroll {spells}'
    return f'Scroll of {result}'


def _weapon(rules, roll=None):
    return _rolled(rules, 'weapon', roll)


def _wsr(rules, roll=None):
    result = _rolled(rules, 'wsr', roll)
    return f'{result}{rules.charges(result)}'


# OD&D Vol 2, Maps.  Magic/Maps Determination: 76-00 is a map; Maps table picks kind.
MAP_KINDS = [(60, 'treasure'), (90, 'magic'), (100, 'both')]
# Treasure maps, d8.  Quantities are N-M dice (000s are thousands).
MAP_TREASURE = [
    ('10000-40000 silver', ),
    ('5000-30000 gold', ),
    ('10000-40000 silver', '5000-30000 gold'),
    ('10000-40000 silver', '2-20 gems'),
    ('5000-30000 gold', '5-30 gems'),
    ('10000-40000 silver', '5000-30000 gold', '1-100 gems'),
    ('10-60 gems', '2-20 jewelry'),
    ('10000-40000 silver', '5000-30000 gold', '10-60 gems', '2-20 jewelry'),
    ]
# Magic maps, d8: (items from item table, item categories to skip, then these items).
MAP_MAGIC = [
    (1, (), ()),
    (1, (), ()),
    (1, (), ()),
    (2, (), ()),
    (2, (), ()),
    (3, ('Sword', ), ()),
    (3, (), (_potion, )),
    (3, (), (_scroll, _potion)),
    ]
# Magic & Treasure maps, d8: (treasure map #, magic map #, already there).
MAP_BOTH = [
    (1, 1, False),
    (2, 1, False),
    (3, 4, False),
    (7, 6, True),
    (5, 4, False),
    (1, 1, True),
    (6, 8, False),
    (8, 7, False),
    ]


def _map_treasure(rules, number):
    parts = []
    for spec in MAP_TREASURE[number - 1]:
        count, text = replace_quantity(spec)
        if spec.endswith('gems'):
            text += f' worth {sum(c * v for c, v, _ in rules.gems.roll(count, 10)):,}gp'
        elif spec.endswith('jewelry'):
            text += f' worth {sum(c * v for c, v, _ in rules.jewelries.roll(count, 1)):,}gp'
        parts.append(text)
    return ', '.join(parts)


def _map_magic(rules, number):
    count, skip, forced = MAP_MAGIC[number - 1]
    return '; '.join([_item(rules, skip=skip) for _ in range(count)] + [func(rules) for func in forced])


def _map(rules, roll=None):
    """Roll up a map, and what it leads to."""
    kind = table(MAP_KINDS, roll)
    if kind == 'treasure':
        return f'Map to treasure: {_map_treasure(rules, random.randint(1, 8))}'
    if kind == 'magic':
        return f'Map to magic: {_map_magic(rules, random.randint(1, 8))}'
    treasure, magic, there = MAP_BOTH[random.randint(1, 8) - 1]
    text = f'Map to treasure: {_map_treasure(rules, treasure)}; magic: {_map_magic(rules, magic)}'
    return f'{text} (already there)' if there else text


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
        if ruleset == 'expert' or ruleset == 'altgreyhawk':
            pass
        else:
            raise ValueError(f'Unknown ruleset [{ruleset}]')

    def _roll(self, count, group):
        """Roll up count pieces of jewlery, group ignored."""
        for _x in range(count):
            value = (d6() + d6() + d6()) * 100
            if value >= 1800:
                design = 'jewelry platinum and gems'
            elif value >= 1600:
                design = 'jewelry gold with gems'
            elif value >= 1200:
                design = 'jewelry sivler with gems'
            elif value >= 1000:
                design = 'jewelry wrought platinum'
            elif value >= 700:
                design = 'jewelry wrought gold'
            else:
                design = 'jewelry wrought silver'
            yield 1, value, design


class Gems(Treasures):
    def __init__(self, ruleset):
        if ruleset == 'expert':
            self.gem_value_chance = [20, 45, 75, 95, 100]
            self.gem_value_chance = [20, 45, 75, 95, 99, 100]  # modified to give 1% chance of diamond
        elif ruleset == 'altgreyhawk':
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
                'Sapphire: Transparent vivid blue',  # Air intelligence, boosts magic
                ],
            [  # 5000 GP Gems
                'Diamond: Transparent clear blue-white',
                ],
            ]
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
            # Roll in groups; but reset when larger, magical or valuable.
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


class BookGems(Treasures):
    """OD&D Vol 2, Treasure: Gems, as written.

    Base value by d100; then d6 per gem (or group of gems), each 1 moves up a category.
    Judgement: book doesn't say if a 1 can repeat, listing categories up to 500,000 implies yes.
    Book groups "5 or 10 gems where large numbers are involved", so up to 10 gems are rolled singly.
    """
    base = [(10, 10), (25, 50), (75, 100), (90, 500), (100, 1000)]
    values = [10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 500000]

    def _roll(self, count, group):
        """Roll up count gems, in groups of size group."""
        if count <= 10:
            group = 1
        value = 0
        for x in range(count):
            if x % group == 0:
                index = self.values.index(table(self.base))
                while d6() == 1 and index < len(self.values) - 1:
                    index += 1
                value = self.values[index]
            yield 1, value, 'gem'


class BookJewelries(Treasures):
    """OD&D Vol 2, Treasure: Jewelry, as written."""

    def _roll(self, count, group):
        """Roll up count pieces of jewlery, group ignored."""
        for _x in range(count):
            roll = d100()
            if roll <= 20:
                value = (d6() + d6() + d6()) * 100
            elif roll <= 80:
                value = d6() * 1000
            else:
                value = random.randint(1, 10) * 1000
            yield 1, value, 'jewelry'


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
    mislead = ('delusion', )  # Potions that look like another potion.
    no_cleric = ()  # Spell levels Clerics don't have, for scrolls.

    def armor_type(self, match):
        return match.group(1)

    def charges(self, result):
        """Text for the charges of a wand, staff or rod."""
        return ''

    def sword_extras(self, sword):
        """Alignment, intelligence, special powers and such for a rolled sword."""
        return sword

    def spell_level(self, caster):
        """Roll the level of one spell."""
        while True:
            level = table(self.scroll_levels)
            if caster != 'Cleric' or level not in self.no_cleric:
                return level

    def detail(self, text):
        """Replace <name> with a roll on detail_name (table or method); leave unknown names."""
        return re.sub(r'<(\w+)>', lambda match: self._detail(match.group(1), match.group(0)), text)

    def _detail(self, name, default):
        value = getattr(self, f'detail_{name}', None)
        if value is None:
            return default
        return value() if callable(value) else table(value)

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
    """Original D&D, Vol 2 Monsters & Treasure (1974), exactly as written.

    Tables are transcribed from the Vol 2 text; "00" is 100.
    Where the book is ambiguous the choice is commented "Judgement".
    """
    name = 'odd'
    jewelries = BookJewelries()
    gems = BookGems()
    mislead = ('delusion', 'poison')  # "Referee will mislead", even a sip of poison kills.
    no_cleric = ('6th', )  # Judgement: Vol 1 Clerics have no 6th level spells.
    # Wands 100, Staves 200 charges, except these (Vol 2, Wands and Staves).
    chargeless = ('Metal Detection', 'Enemy Detection', 'Secret Doors', 'Healing', 'Snake Staff', 'Striking')
    # Treasure Types, thousands of coins are written 1000-6000 (d6 x 1000).  Columns: cp sp gp gems jewelry magic.
    # Roll for each of Gems and Jewelry.  Magic "any" is a roll on the Magic/Maps table, 25% maps.
    TREASURE_TYPES = {
        'a': (('cp', 25, '1000-6000'),  ('sp', 30, '1000-6000'),   ('gp', 35, '2000-12000'),  ('gems', 50, '6-36'),  ('jewelry', 50, '6-36'),  ('magic', 40, (_any, _any, _any))),
        'a-desert': (('cp', 20, '1000-4000'), ('sp', 25, '1000-4000'), ('gp', 30, '1000-6000'), ('gems', 50, '10-40'), ('jewelry', 50, '10-40'), ('magic', 60, (_item, _item, _item))),
        'a-water': (None,               None,                      ('gp', 60, '5000-30000'),  ('gems', 60, '10-60'), ('jewelry', 60, '10-60'), ('magic', 50, (_map, ))),
        'b': (('cp', 50, '1000-8000'),  ('sp', 25, '1000-6000'),   ('gp', 25, '1000-3000'),   ('gems', 25, '1-6'),   ('jewelry', 25, '1-6'),   ('magic', 10, (_martial, ))),  # Weapon, Armor, or Misc. Weapon.
        'c': (('cp', 20, '1000-12000'), ('sp', 30, '1000-4000'),   None,                      ('gems', 25, '1-4'),   ('jewelry', 25, '1-4'),   ('magic', 10, (_any, _any))),
        'd': (('cp', 10, '1000-8000'),  ('sp', 15, '1000-12000'),  ('gp', 60, '1000-6000'),   ('gems', 30, '1-8'),   ('jewelry', 30, '1-8'),   ('magic', 20, (_any, _any, _potion))),
        'e': (('cp',  5, '1000-10000'), ('sp', 30, '1000-12000'),  ('gp', 25, '1000-8000'),   ('gems', 10, '1-10'),  ('jewelry', 10, '1-10'),  ('magic', 30, (_any, _any, _any, _scroll))),
        'f': (None,                     ('sp', 10, '2000-20000'),  ('gp', 45, '1000-12000'),  ('gems', 20, '2-24'),  ('jewelry', 20, '2-24'),  ('magic', 35, (_noweap_any, _noweap_any, _noweap_any, _potion, _scroll))),
        'g': (None,                     None,                      ('gp', 75, '10000-40000'), ('gems', 25, '3-18'),  ('jewelry', 25, '1-10'),  ('magic', 40, (_any, _any, _any, _any, _scroll))),
        'h': (('cp', 25, '3000-24000'), ('sp', 50, '1000-100000'), ('gp', 75, '10000-60000'), ('gems', 50, '1-100'), ('jewelry', 50, '10-40'), ('magic', 20, (_any, _any, _any, _any, _potion, _scroll))),
        'i': (None,                     None,                      None,                      ('gems', 50, '2-16'),  ('jewelry', 50, '2-16'),  ('magic', 20, (_any, ))),
        }
    # Magic/Maps Determination: Magic Items.
    item = [
        (20, 'Sword', _sword),
        (35, 'Armor', _armor),
        (40, 'Misc. Weapon', _weapon),
        (65, 'Potion', _potion),
        (85, 'Scroll', _scroll),
        (90, 'Ring', _ring),
        (95, 'Wand/Staff', _wsr),
        (100, 'Misc. Magic', _misc),
        ]
    sword = [
        (35, 'Sword +1'),
        (40, 'Sword +1, +2 vs. Lycanthropes'),
        (45, 'Sword +1, +2 vs. Magic-Users and Enchanted Monsters'),
        (50, 'Sword +1, Locating Objects Ability'),
        (60, 'Sword +1, +3 vs. {Trolls|Clerics}'),  # {Lawful or Neutral|Chaotic} target, see sword_extras.
        (65, 'Sword, Flaming: +1, +2 vs. {Trolls|Pegasi, Hippogriffs, Rocs}, +3 vs. {Undead|Treants}'),
        (70, 'Sword +1, Wishes Included (2-8 Wishes)'),
        (75, 'Sword +1, +3 vs. Dragons'),
        (78, 'Sword +2'),
        (80, 'Sword +2, Charm Person Ability'),
        (82, 'Sword +3'),
        (83, 'Sword, One Life Energy Draining Ability'),
        (100, 'Sword -2, Cursed'),
        ]
    # Judgement: "Armor" is not typed, e.g. leather, chain or plate.
    armor = [
        (30, 'Shield +1'),
        (60, 'Armor +1'),
        (75, 'Armor & Shield +1'),
        (83, 'Shield +2'),
        (90, 'Armor +2'),
        (97, 'Armor & Shield +2'),
        (100, 'Shield +3'),
        ]
    # Judgement: Explanation says Magic Arrows are +1.
    weapon = [
        (25, '10 Magic Arrows +1'),
        (40, '3-30 Magic Arrows +1'),
        (55, 'Dagger +1 vs. Man-Sized Opponents, +2 vs. Goblins and Kobolds'),
        (60, 'Dagger +2 vs. Man-Sized Opponents, +3 vs. Orcs, Goblins and Kobolds'),
        (65, 'Magic Bow'),
        (70, 'Axe +1'),
        (80, 'Mace +2'),
        (85, 'War Hammer +1'),
        (89, 'War Hammer +2'),
        (90, 'War Hammer +3, 6" Throwing Range with Return'),
        (96, 'Spear +1'),
        (99, 'Spear +2'),
        (100, 'Spear +3'),
        ]
    potion = [
        (4, 'Growth'),
        (8, 'Diminution'),
        (12, 'Giant Strength (<giant> Giant)'),
        (16, 'Invisibility'),
        (20, 'Gaseous Form'),
        (24, 'Polymorph (Self)'),
        (28, 'Speed'),
        (32, 'Levitation'),
        (36, 'Flying'),
        (38, 'ESP'),
        (40, 'Delusion'),
        (44, 'Healing'),
        (48, 'Longevity'),
        (52, 'Clairvoyance'),
        (55, 'Clairaudience'),
        (60, 'Animal Control'),
        (64, 'Undead Control'),
        (68, 'Plant Control'),
        (72, 'Human Control'),
        (76, 'Giant Control (<giant> Giants)'),
        (80, 'Dragon Control (<dragon> Dragons)'),
        (84, 'Poison'),
        (88, 'Invulnerability'),
        (92, 'Fire Resistance'),
        (96, 'Treasure Finding'),
        (100, 'Heroism'),
        ]
    # Referee rolls which Giants.  Hill 60%, others 10% each.
    detail_giant = [(60, 'Hill'), (70, 'Stone'), (80, 'Frost'), (90, 'Fire'), (100, 'Cloud')]
    # Referee rolls which of the six Dragons.
    detail_dragon = [(1, 'White'), (2, 'Black'), (3, 'Green'), (4, 'Blue'), (5, 'Red'), (6, 'Golden')]
    # Spell level is d6.
    scroll_levels = [(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th'), (5, '5th'), (6, '6th')]
    scroll = [
        (20, '1 Spell'),
        (35, '2 Spells'),
        (45, '3 Spells'),
        (50, '7 Spells'),
        (60, 'Curse'),
        (70, 'Protection: Lycanthropes'),
        (80, 'Protection: Undead'),
        (90, 'Protection: Elementals'),
        (100, 'Protection: Magic'),
        ]
    # Curse die roll, d8, 3" diameter.
    scroll_trap = [
        (2, 'Any monster of the referee\'s choice'),
        (4, 'Disease, fatal in 3 turns unless healed'),
        (6, 'Polymorph to insect of referee\'s choice'),
        (7, 'Transportation 1,000 miles, random direction'),
        (8, 'Transportation to another planet'),
        ]
    ring = [
        (9, 'Invisibility'),
        (15, 'Mammal Control'),
        (21, 'Human Control'),
        (30, 'Weakness'),
        (39, 'Protection +1'),
        (49, 'Three Wishes'),
        (60, 'Delusion'),
        (70, 'Water Walking'),
        (80, 'Fire Resistance'),
        (85, 'Protection +1, 5\' radius'),  # Judgement: book gives no bonus, ring of Protection is +1.
        (90, 'Regeneration'),
        (92, 'Djinn Summoning'),
        (94, 'Telekinesis'),
        (96, 'X-Ray Vision'),
        (98, 'Spell Turning'),
        (99, 'Spell Storing (<spells>)'),
        (100, 'Many Wishes (4-24)'),
        ]
    # Wands: Magic-Users only.  Staves: (C)lerics, (M)agic-Users.
    wsr = [
        (15, 'Wand of Metal Detection (M)'),
        (20, 'Wand of Enemy Detection (M)'),
        (25, 'Wand of Magic Detection (M)'),
        (30, 'Wand of Secret Doors & Traps Detection (M)'),
        (35, 'Wand of Illusion (M)'),
        (40, 'Wand of Fear (M)'),
        (45, 'Wand of Cold (M)'),
        (50, 'Wand of Paralization (M)'),
        (55, 'Wand of Fire Balls (M)'),
        (60, 'Wand of Lightning Bolts (M)'),
        (65, 'Wand of Polymorph (M)'),
        (70, 'Wand of Negation (M)'),
        (80, 'Staff of Healing (C)'),
        (85, 'Staff of Commanding (C, M)'),
        (90, 'Snake Staff (C)'),
        (95, 'Staff of Striking (C, M)'),
        (97, 'Staff of Withering (C)'),
        (99, 'Staff of Power (M)'),
        (100, 'Staff of Wizardry (M)'),
        ]
    # (All) is usable by all classes, the book's asterisk.
    misc = [
        (4, 'Crystal Ball'),
        (6, 'Crystal Ball with Clairaudience'),
        (7, 'Crystal Ball with ESP'),
        (12, 'Medallion of ESP, 3" Range (All)'),
        (15, 'Medallion of ESP, 9" Range (All)'),
        (18, 'Amulet vs. Crystal Balls and ESP (All)'),
        (24, 'Scarab of Protection from Evil High Priests (All)'),
        (29, 'Bag of Holding (All)'),
        (30, 'Censor Controlling Air Elementals'),
        (31, 'Stone Controlling Earth Elementals'),
        (32, 'Brazier Commanding Fire Elementals'),
        (33, 'Bowl Commanding Water Elementals'),
        (35, 'Efreet Bottle (All)'),
        (38, 'Displacer Cloak (All)'),
        (47, 'Elven Cloak and Boots (All)'),
        (52, 'Boots of Speed (All)'),
        (57, 'Boots of Levitation (All)'),
        (62, 'Boots of Traveling and Leaping (All)'),
        (67, 'Broom of Flying'),
        (72, 'Helm of Reading Magic and Languages (All)'),
        (75, 'Helm of Telepathy (All)'),
        (76, 'Helm of Teleportation'),
        (87, 'Helm of Chaos (Law) (All)'),
        (88, 'Flying Carpet (All)'),
        (89, 'Drums of Panic, 24" Range (All)'),
        (90, 'Horn of Blasting, 10" Range (All)'),
        (97, 'Gauntlets of Ogre Power (All)'),
        (99, 'Girdle of Giant Strength (All)'),
        (100, 'Mirror of Life Trapping'),
        ]
    # Sword Alignment; percentages reversed (Lawful and Chaotic swapped) for the Energy Draining sword.
    sword_alignment = [(65, 'Lawful'), (90, 'Neutral'), (100, 'Chaotic')]
    # Primary Powers.  96-99 is two rolls ignoring 96-99 (00 allowed), 00 is an Extraordinary Ability.
    sword_primary = [
        (15, 'Note Shifting Walls & Rooms'),
        (30, 'Detect Sloping Passages'),
        (40, 'Locate Secret Doors'),
        (50, 'Detect Traps'),
        (60, 'See Invisible Objects'),
        (70, 'Detect Evil and/or Gold'),
        (80, 'Detect Meal & What Kind'),
        (90, 'Detect Magic'),
        (95, 'Detect Gems (# and Size)'),
        ]
    # Languages, in addition to alignment's.  Judgement: book has 86-95 Four and 90-99 Five, took 96-99.
    # 00 is two rolls ignoring 00.
    sword_languages = [(50, 1), (70, 2), (85, 3), (95, 4), (99, 5)]
    # Extraordinary Abilities.  98-99 is two rolls ignoring over 97, 00 is three rolls.
    sword_extraordinary = [
        (10, 'Clairaudience'),
        (20, 'Clairvoyance'),
        (30, 'ESP'),
        (40, 'Telepathy'),
        (50, 'Telekinesis'),
        (59, 'Teleportation'),
        (68, 'X-Ray Vision'),
        (77, 'Illusion Generation'),
        (82, 'Levitation'),
        (87, 'Flying'),
        (92, 'Healing (1 point/6 turns or 6 points/day)'),
        (97, '1-4 x Normal Strength for 1-10 Turns, once/day'),
        ]
    sword_purposes = ['Slay Magic-Users', 'Slay Clerics', 'Slay Fighting-Men', 'Slay Monsters', 'Defeat Law', 'Defeat Chaos']
    sword_purpose_powers = {
        'Lawful': 'paralyze Chaotic opponents',
        'Neutral': '+1 to all saving throws',
        'Chaotic': 'disintegrate Lawful opponents',
        }

    def sword_extras(self, sword):
        """Alignment, Intelligence, Egoism and Origin/Purpose.  Vol 2, Explanations of Magic Items: Swords."""
        alignment = table(self.sword_alignment)
        if 'Energy Draining' in sword:
            alignment = {'Lawful': 'Chaotic', 'Chaotic': 'Lawful'}.get(alignment, alignment)
        if any(word in sword for word in ('Holy', 'Sharpness', 'Vorpal')):  # Judgement: Paladin / Lawful only swords.
            alignment = 'Lawful'
        sword = re.sub(r'\{([^|}]*)\|([^}]*)\}', lambda match: match.group(2 if alignment == 'Chaotic' else 1), sword)
        parts = [alignment]
        intelligence = d12()
        special = d100() >= 91  # Special purpose.
        if special:
            intelligence = 12
        if intelligence >= 7:
            ego = 12 if special else d12()
            powers = self.sword_primary_powers({7: 1, 8: 2}.get(intelligence, 3))
            parts += [f'Int {intelligence}', f'Ego {ego}', 'telepathy' if intelligence == 12 else 'speech' if intelligence >= 10 else 'empathy']
            if intelligence >= 10:
                languages = self.sword_language_count()
                parts.append(f'{languages} language{"" if languages == 1 else "s"} besides {alignment}')
            if intelligence >= 11:
                parts.append('reads magic')
            if intelligence == 12:
                powers += self.sword_extraordinary_powers()
            if special:
                purpose = random.choice(self.sword_purposes)
                while (alignment, purpose) in (('Lawful', 'Defeat Law'), ('Chaotic', 'Defeat Chaos')):  # Judgement: can't defeat itself.
                    purpose = random.choice(self.sword_purposes)
                powers.append(f'{purpose}, {self.sword_purpose_powers[alignment]}')
            if powers:
                parts.append(', '.join(f'{power} x{count}' if count > 1 else power for power, count in collections.Counter(powers).items()))
        return f'{sword} ({", ".join(parts)})'

    def sword_primary_powers(self, count):
        found = []
        for _ in range(count):
            roll = d100()
            rolls = [roll]
            if 96 <= roll <= 99:
                rolls = []
                while len(rolls) < 2:
                    sub = d100()
                    if not 96 <= sub <= 99:
                        rolls.append(sub)
            for result in rolls:
                found += self.sword_extraordinary_powers() if result == 100 else [table(self.sword_primary, result)]
        return found

    def sword_extraordinary_powers(self):
        roll = d100()
        if roll <= 97:
            return [replace_quantity(table(self.sword_extraordinary, roll))[1]]
        return [replace_quantity(table(self.sword_extraordinary, random.randint(1, 97)))[1] for _ in range(2 if roll < 100 else 3)]

    def sword_language_count(self):
        roll = d100()
        if roll < 100:
            return table(self.sword_languages, roll)
        return sum(table(self.sword_languages, random.randint(1, 99)) for _ in range(2))

    def max_charges(self, result):
        """(most, unit) or None.  Vol 2, Wands and Staves."""
        if any(word in result for word in self.chargeless):
            return None
        if 'Wand' in result:
            return 100, 'charges'
        if 'Staff' in result:
            return 200, 'charges'
        return None

    def found_charges(self, most):
        return most

    def charges(self, result):
        maximum = self.max_charges(result)
        if maximum is None:
            return ''
        most, unit = maximum
        return f' ({self.found_charges(most)} {unit})'

    def detail_spells(self):
        """Ring of Spell Storing: 1-6 spells, 20% Clerical, half of those Chaotic.  Never mixed."""
        caster = 'Magic-user'
        if d100() <= 20:
            caster = 'Chaotic Cleric' if d100() <= 50 else 'Cleric'
        levels = reduce_groups((1, 0, self.spell_level(caster.split()[-1])) for _ in range(d6()))
        return f'{caster} spells {", ".join(f"{c}x{x}" for c, _, x in levels)}'


class GreyhawkRules(OddRules):
    """Original D&D Vol 2 plus Greyhawk Supplement I (1975), exactly as written.

    Greyhawk's Magic/Maps Determination Additions and Changes replace the Vol 2 tables
    for swords, misc. weapons, armor, potions, rings, wands/staves/rods and misc. magic.
    Item categories, scrolls, treasure types and sword sentience stay as Vol 2.
    """
    name = 'greyhawk'
    # Greyhawk corrects Staff of Striking, it uses charges.
    chargeless = ('Metal Detection', 'Enemy Detection', 'Secret Doors', 'Healing', 'Snake Staff')
    sword = [
        (30, 'Sword +1'),
        (35, 'Sword +1, +2 vs. Lycanthropes'),
        (40, 'Sword +1, +2 vs. Magic-Users and Enchanted Monsters'),
        (45, 'Sword +1, Locating Objects Ability'),
        (50, 'Sword +1, +3 vs. {Trolls|Clerics}'),  # {Lawful or Neutral|Chaotic} target, see sword_extras.
        (55, 'Sword, Flaming: +1, +2 vs. {Trolls|Pegasi, Hippogriffs, Rocs}, +3 vs. {Undead|Ents}'),
        (60, 'Sword +1, Wishes Included (2-8 Wishes)'),
        (65, 'Sword +1, +3 vs. Dragons'),
        (68, 'Sword +2'),
        (70, 'Sword +2, Charm Person Ability'),
        (72, 'Sword +3'),
        (73, 'Sword, One Life Energy Draining Ability'),
        (74, 'Sword +2, Nine Steps Draining Ability'),
        (75, 'Sword +4'),
        (76, 'Holy Sword +5'),
        (78, 'Sword of Cold: +3, +5 vs. Fire Using/Dwelling Creatures'),
        (82, 'Dragon Slaying Sword +2 (<dragon> Dragons, 4d10 damage)'),
        (83, 'Sword +1, Cursed'),
        (97, 'Sword -2, Cursed'),
        (98, 'Dancing Sword'),
        (99, 'Sword of Sharpness'),
        (100, 'Vorpal Blade'),
        ]
    # Armor/Shield +4 are Mithral, +5 Adamantite.  Vulnerable armor looks +1 to +4 but is -1 to -4.
    armor = [
        (20, 'Shield +1'),
        (40, 'Armor +1'),
        (50, 'Armor & Shield +1'),
        (57, 'Shield +2'),
        (64, 'Armor +2'),
        (70, 'Armor & Shield +2'),
        (73, 'Shield +3'),
        (76, 'Armor +3'),
        (78, 'Armor & Shield +3'),
        (80, 'Mithral Shield +4'),
        (82, 'Mithral Armor +4'),
        (83, 'Mithral Armor & Shield +4'),
        (85, 'Adamantite Shield +5'),
        (86, 'Adamantite Armor +5'),
        (87, 'Adamantite Armor & Shield +5'),
        (93, 'Shield of Missile Attraction -1 (appears +1-5)'),
        (99, '-1-4 Armor of Vulnerability'),
        (100, 'Armor of Etherealness'),
        ]
    weapon = [
        (15, '10 Magic Arrows +1'),
        (25, '3-30 Magic Arrows +1'),
        (29, '2-12 Magic Arrows +2'),
        (30, '1-8 Magic Arrows +3'),
        (31, 'Arrow of Slaying (<slaying>)'),
        (34, '2-16 Magic Crossbow Bolts +2'),
        (45, 'Dagger +1 vs. Man-Sized Opponents, +2 vs. Goblins and Kobolds'),
        (50, 'Dagger +2 vs. Man-Sized Opponents, +3 vs. Orcs, Goblins, and Kobolds'),
        (55, 'Magic Bow'),
        (57, 'Crossbow of Accuracy (+3)'),
        (59, 'Crossbow of Speed'),
        (61, 'Crossbow of Distance'),
        (66, 'Axe +1'),
        (67, 'Axe +2'),
        (68, 'Axe +3'),
        (80, 'Mace +2'),
        (81, 'Mace of Disruption'),
        (86, 'War Hammer +1'),
        (89, 'War Hammer +2'),
        (90, 'War Hammer +3, 6" Throwing Range with Return'),
        (95, 'Spear +1'),
        (96, 'Spear +2'),
        (97, 'Spear +3'),
        (100, 'Cursed Spear of Backbiting (appears +1-3)'),
        ]
    # (F)ighters only.  Referee rolls which Giants and Dragons.
    potion = [
        (3, 'Growth'),
        (6, 'Diminution'),
        (10, 'Giant Strength (<giant> Giant) (F)'),
        (13, 'Invisibility'),
        (16, 'Gaseous Form'),
        (19, 'Polymorph (Self)'),
        (23, 'Speed (F)'),
        (26, 'Levitation'),
        (29, 'Flying'),
        (32, 'ESP'),
        (35, 'Delusion'),
        (39, 'Healing'),
        (42, 'Longevity'),
        (45, 'Extra-healing'),
        (49, 'Oil of Slipperiness'),
        (52, 'Clairvoyance'),
        (55, 'Clairaudience'),
        (58, 'Animal Control'),
        (63, 'Undead Control'),
        (66, 'Plant Control'),
        (69, 'Human Control'),
        (72, 'Giant Control (<giant> Giants)'),
        (75, 'Dragon Control (<dragon> Dragons)'),
        (79, 'Poison'),
        (83, 'Invulnerability (F)'),
        (87, 'Fire Resistance (F)'),
        (90, 'Treasure Finding'),
        (94, 'Heroism (F)'),
        (97, 'Super-heroism (F)'),
        (100, 'Oil of Etherealness'),
        ]
    # Judgement: Storm Giants are in Greyhawk's monsters, Hill Giants lose a share to them.
    detail_giant = [(50, 'Hill'), (60, 'Stone'), (70, 'Frost'), (80, 'Fire'), (90, 'Cloud'), (100, 'Storm')]
    # Greyhawk adds Brass, Copper, Bronze, Silver Dragons (and calls Golden, Gold).
    detail_dragon = [(1, 'White'), (2, 'Black'), (3, 'Green'), (4, 'Blue'), (5, 'Red'), (6, 'Gold'), (7, 'Brass'), (8, 'Copper'), (9, 'Bronze'), (10, 'Silver')]
    detail_slaying = [(1, 'Giant Class'), (2, 'Undead Class'), (3, 'Flying Monsters'), (4, 'Other Monsters'), (5, 'Enchanted Monsters')]
    # Many Wishes: Greyhawk doesn't repeat Vol 2's number.
    ring = [
        (5, 'Invisibility'),
        (10, 'Mammal Control'),
        (15, 'Human Control'),
        (30, 'Weakness'),
        (35, 'Protection +1'),
        (36, 'Protection +3'),
        (40, 'Three Wishes'),
        (60, 'Delusion'),
        (65, 'Water Walking'),
        (70, 'Fire Resistance'),
        (72, 'Protection +2, 5\' radius'),
        (74, 'Regeneration'),
        (76, 'Djinn Summoning'),
        (78, 'Shooting Stars'),
        (80, 'X-Ray Vision'),
        (82, 'Telekinesis'),
        (95, 'Contrariness'),
        (97, 'Spell Turning'),
        (99, 'Spell Storing (<spells>)'),
        (100, 'Many Wishes (4-24)'),
        ]
    # Wands, Staves and Rods.  (A)ll, (C)lerics, (F)ighters, (M)agic-Users, (T)hieves.
    # Book prints Magic Detection as 15-20, overlapping Enemy Detection, took 16-20.
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
        (63, 'Staff of Healing (C)'),
        (67, 'Staff of Commanding (C, M)'),
        (71, 'Snake Staff (C)'),
        (75, 'Staff of Striking (C, M)'),
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
    # Miscellaneous Magic: roll which table (Table I 01-30, II 31-60, III 61-75, IV 76-90, V 91-00), then on it.
    misc_i = [
        (5, 'Crystal Ball'),
        (9, 'Crystal Ball with Clairaudience'),
        (12, 'Crystal Ball with ESP'),
        (15, 'Crystal Hypnosis Ball'),
        (20, 'Medallion of ESP, 3" Range (All)'),
        (25, 'Medallion of ESP, 9" Range (All)'),
        (30, 'Medallion of Thought Projection'),
        (33, 'Amulet vs. Crystal Balls and ESP (All)'),
        (35, 'Amulet of Inescapable Locating (All)'),
        (40, 'Scarab of Protection from Evil High Priests (All)'),
        (42, 'Scarab of Enraging Enemies (All)'),
        (45, 'Scarab of Insanity (All)'),
        (47, 'Scarab of Death'),
        (49, 'Bag of Holding (All)'),
        (51, 'Bag of Tricks (All)'),
        (55, 'Bean Bag (All)'),
        (58, 'Bag of Transmuting (All)'),
        (61, 'Bag of Devouring (All)'),
        (63, 'Censor Controlling Air Elementals'),
        (67, 'Censor Summoning Hostile Air Elementals'),
        (69, 'Stone Controlling Earth Elementals (All)'),
        (71, 'Luckstone (All)'),
        (75, 'Loadstone (All)'),
        (77, 'Brazier Commanding Fire Elementals'),
        (80, 'Brazier of Sleep Smoke'),
        (82, 'Bowl Commanding Water Elementals'),
        (85, 'Bowl of Watery Death'),
        (88, 'Elven Boots (All)'),
        (92, 'Boots of Speed (All)'),
        (95, 'Boots of Levitation (All)'),
        (98, 'Boots of Traveling and Leaping (All)'),
        (100, 'Boots of Dancing (All)'),
        ]
    misc_ii = [
        (2, 'Efreet Bottle (All)'),
        (8, 'Flask of Curses (All)'),
        (10, 'Jug of Alchemy (All)'),
        (15, 'Decanter of Endless Water (All)'),
        (17, 'Beaker of Plentiful Potions (All)'),
        (23, 'Broom of Flying (All)'),
        (29, 'Animated Broom (All)'),
        (34, 'Helm of Reading Magic and Languages (All)'),
        (37, 'Helm of Telepathy (All)'),
        (39, 'Helm of Teleportion'),
        (41, 'Helm of Brilliance (All)'),
        (47, 'Helm of Chaos (Law) (All)'),
        (49, 'Flying Carpet (All)'),
        (55, 'Rug of Smothering (All)'),
        (57, 'Drums of Panic (All)'),
        (60, 'Drums of Deafness (All)'),
        (62, 'Horn of Blasting (All)'),
        (65, 'Horn of Collapsing (All)'),
        (70, 'Horn of Valhalla, Silver (All)'),
        (73, 'Horn of Valhalla, Bronze (F, C)'),
        (75, 'Horn of Valhalla, Iron (F)'),
        (80, 'Horn of Bubbles'),
        (84, 'Gauntlets of Ogre Power (F, C, T)'),
        (87, 'Gauntlets of Swimming and Climbing (F, C, T)'),
        (90, 'Gauntlets of Dexterity (All)'),
        (93, 'Gauntlets of Fumbling (All)'),
        (94, 'Girdle of Giant Strength (All)'),
        (96, 'Girdle of Femininity/Masculinity (All)'),
        (98, 'Necklace of Missiles (All)'),
        (100, 'Necklace of Strangulation (All)'),
        ]
    misc_iii = [
        (5, 'Cloak of Protection +1 (M, C, T)'),
        (9, 'Cloak of Protection +2 (M, C, T)'),
        (11, 'Cloak of Protection +3 (M, C, T)'),
        (14, 'Displacer Cloak (All)'),
        (20, 'Elven Cloak (All)'),
        (25, 'Poisonous Cloak (All)'),
        (29, 'Mirror of Mental Prowess (All)'),
        (30, 'Mirror of Life Trapping'),
        (35, 'Mirror of Opposition (All)'),
        (37, 'Trident of Warning (F, C, T)'),
        (39, 'Trident of Commanding Water Creatures (All)'),
        (41, 'Trident of Submission (F)'),
        (45, 'Trident of Yearning (All)'),
        (50, 'Eyes of Charming (All)'),
        (55, 'Eyes of Petrification (All)'),
        (57, 'Gem of Brightness (All)'),
        (61, 'Gem of Seeing (All)'),
        (65, 'Jewel of Attacks upon the Owner (All)'),
        (70, 'Bracers of Defense, Armor Class 6 (All)'),
        (75, 'Bracers of Defense, Armor Class 4 (All)'),
        (80, 'Bracers of Defense, Armor Class 2 (All)'),
        (85, 'Bracers of Defenselessness, Armor Class 12 (All)'),
        (87, 'Rope of Entanglement (All)'),
        (89, 'Rope of Climbing (All)'),
        (91, 'Rope of Constriction (All)'),
        (93, 'Dust of Appearance (All)'),
        (95, 'Disappearance Dust (All)'),
        (97, 'Dust of Sneezing and Choking (All)'),
        (98, 'Talisman of Lawfulness (All)'),
        (99, 'Talisman of Chaos Supreme (All)'),
        (100, 'Talisman of the Sphere'),
        ]
    misc_iv = [
        (15, '2-5 Javelins of Lightning (F)'),
        (20, 'Arrow of Direction (All)'),
        (25, 'Saw of Mighty Cutting (F)'),
        (30, 'Mattock of the Titans (F)'),
        (35, 'Spade of Colossal Excavation (F)'),
        (40, 'Wings of Flying (All)'),
        (42, 'Cube of Force (All)'),
        (45, 'Portable Hole (All)'),
        (50, 'Horseshoes of Speed (All)'),
        (51, 'Sphere of Annihilation'),
        (58, 'Chime of Opening (All)'),
        (63, 'Pipes of the Sewers (All)'),
        (65, 'Lyre of Building (All)'),
        (70, 'Figurines of Wondrous Power, Ebony Fly (All)'),
        (73, 'Figurines of Wondrous Power, Onyx Dog (All)'),
        (75, 'Figurines of Wondrous Power, Marble Elephant (All)'),
        (80, 'Figurines of Wondrous Power, 2 Golden Lions (All)'),
        (84, 'Figurines of Wondrous Power, 3 Ivory Goats (All)'),
        (88, 'Wizard\'s Robe'),
        (94, 'Robe of Blending (All)'),
        (98, 'Robe of Eyes'),
        (100, 'Robe of Powerlessness (All)'),
        ]
    misc_v = [
        (5, 'Manual of Puissant Skill at Arms (F)'),
        (10, 'Manual of Gainful Exercise (All)'),
        (15, 'Manual of Bodily Health (All)'),
        (20, 'Manual of Stealthy Pilfering (T)'),
        (25, 'Manual of Golems'),
        (30, 'Manual of Quickness of Action (All)'),
        (35, 'Book of Exalted Deeds (C)'),
        (40, 'Book of Vile Darkness (C)'),
        (45, 'Book of Infinite Spells (M, C, T)'),
        (50, 'Libram of Silver Magic'),
        (55, 'Libram of Gainful Conjurations'),
        (60, 'Libram of Ineffable Damnation'),
        (65, 'Tome of Understanding (All)'),
        (70, 'Tome of Clear Thought (All)'),
        (75, 'Tome of Leadership and Influence (All)'),
        (100, 'Deck of Many Things (All)'),
        ]
    misc = [(30, misc_i), (60, misc_ii), (75, misc_iii), (90, misc_iv), (100, misc_v)]

    def max_charges(self, result):
        """Greyhawk: Rods typically 25 charges unless noted."""
        if 'Rulership' in result:
            return 10, 'charges'
        if 'Absorption' in result:
            return 100, 'spell levels'
        if 'Rod' in result:
            return 25, 'charges'
        return super().max_charges(result)

    def charges(self, result):
        if 'Cancellation' in result:
            return ' (single use)'
        return super().charges(result)


class AltGreyhawkRules(GreyhawkRules):
    """Greyhawk with Norm's tweaks.  Everything not listed here is as Greyhawk.

    Differences from the books:
    - Treasure Type F's magic is rings, wands/staves/rods and misc. magic (no maps, nor armor, potion or scroll)
      plus a potion and a scroll.
    - Treasure Types O, Q, S are added, they are not OD&D (AD&D Monster Manual style).
    - Gems and Jewelry are the Gems / Jewelries classes (not the book's rolls).
    - Swords: cursed swords are 83-87 +1 Cursed Berserker, 88-92 -1 Cursed, 93-97 -2 Cursed (book 83 +1, 84-97 -2).
    - Armor, misc. weapons and scrolls are Norm's tables, see below.
    - Wand, staff and rod charges are found partly used, 40% to 100% of the book's number.
    """
    name = 'altgreyhawk'
    jewelries = Jewelries('altgreyhawk')
    gems = Gems('altgreyhawk')
    TREASURE_TYPES = {
        **GreyhawkRules.TREASURE_TYPES,
        'f': (None,                     ('sp', 10, '2000-20000'),  ('gp', 45, '1000-12000'),  ('gems', 20, '2-24'),  ('jewelry', 20, '2-24'),  ('magic', 35, (_noweap, _noweap, _noweap, _potion, _scroll))),
        'o': (('cp', 25, '1000-4000'),  ('sp', 20, '1000-3000'),   None,                      None,                  None,                     None),
        'q': (None,                     None,                      None,                      ('gems', 50, '1-4'),   None,                     None),
        's': (None,                     None,                      None,                      None,                  None,                     ('magic', 40, (_2d8_potions, ))),
        }
    sword = [row for row in GreyhawkRules.sword if row[0] < 83] + [
        (87, 'Sword +1, Cursed Berserker'),
        (92, 'Sword -1, Cursed'),
        (97, 'Sword -2, Cursed'),
        (98, 'Dancing Sword'),
        (99, 'Sword of Sharpness'),
        (100, 'Vorpal Blade'),
        ]

    # Greyhawk but: "Armor" is always Plate; Shield of Missile Attraction is 88-90 (book 88-93);
    # Shield of Vulnerability added 91-93; Vulnerability is Plate and -1 to -3 (book Armor, -1 to -4).
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
    # Misc. weapons: Norm's own table, only loosely Greyhawk's.  Same kinds of items but re-balanced odds and counts
    # (3-18 +1 arrows, 3-18 +1 bolts, 2-12 +2 bolts, Arrow/Bolt of Slaying, own daggers, Magic Bow +1, Axe +1 to +3,
    # Mace +1 to +3).  Added: Sling +1, "Unusual Misc Weapon" +1, Axe of Missing, Sticky Mace.
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
    # Scrolls: Norm's table, not the book's.  Differs: Curse (book 51-60) is a 1-10 trap using Rules.scroll_trap
    # instead of the book's Curse table; Protection: Demons replaces the book's 7 Spells.
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

    def found_charges(self, most):
        return random.randint(max(1, most * 2 // 5), most)


class ExpertRules(Rules):
    name = 'expert'
    jewelries = Jewelries('expert')
    gems = Gems('expert')
    TREASURE_TYPES = {
        'a': (('cp', 25, '1000-6000'),  ('sp', 30, '1000-6000'),   ('ep', 20, '1000-4000'),   ('gp', 35, '2000-12000'),  ('pp', 25, '1000-2000'),   ('gems', 50, '6-36'),  ('jewelry', 50, '6-36'),  ('magic', 30, (_item, _item, _item))),
        'b': (('cp', 50, '1000-8000'),  ('sp', 25, '1000-6000'),   ('ep', 25, '1000-4000'),   ('gp', 25, '1000-3000'),   None,                      ('gems', 25, '1-6'),   ('jewelry', 25, '1-6'),   ('magic', 10, (_martial, ))),
        'c': (('cp', 20, '1000-12000'), ('sp', 30, '1000-4000'),   ('ep', 10, '1000-4000'),   None,                      None,                      ('gems', 25, '1-4'),   ('jewelry', 25, '1-4'),   ('magic', 10, (_item, _item))),
        'd': (('cp', 10, '1000-8000'),  ('sp', 15, '1000-12000'),  None,                      ('gp', 60, '1000-6000'),   None,                      ('gems', 30, '1-8'),   ('jewelry', 30, '1-8'),   ('magic', 15, (_item, _item, _potion))),
        'e': (('cp',  5, '1000-10000'), ('sp', 30, '1000-12000'),  ('ep', 25, '1000-4000'),   ('gp', 25, '1000-8000'),   None,                      ('gems', 10, '1-10'),  ('jewelry', 10, '1-10'),  ('magic', 25, (_item, _item, _item, _scroll))),
        'f': (None,                     ('sp', 10, '2000-20000'),  ('ep', 20, '1000-8000'),   ('gp', 45, '1000-12000'),  ('pp', 30, '1000-3000'),   ('gems', 20, '2-24'),  ('jewelry', 10, '1-12'),  ('magic', 30, (_noweap, _noweap, _noweap, _potion, _scroll))),
        'g': (None,                     None,                      None,                      ('gp', 50, '10000-40000'), ('pp', 50, '1000-6000'),   ('gems', 25, '3-18'),  ('jewelry', 25, '1-10'),  ('magic', 35, (_item, _item, _item, _item, _scroll))),
        'h': (('cp', 25, '3000-24000'), ('sp', 50, '1000-100000'), ('ep', 50, '10000-40000'), ('gp', 50, '10000-60000'), ('pp', 25, '5000-20000'),  ('gems', 50, '1-100'), ('jewelry', 50, '10-40'), ('magic', 15, (_item, _item, _item, _item, _potion, _scroll))),
        'i': (None,                     None,                      None,                      None,                      ('pp', 30, '1000-8000'),   ('gems', 50, '2-12'),  ('jewelry', 50, '2-12'),  ('magic', 15, (_item, ))),
        'j': (('cp', 25, '1000-4000'),  ('sp', 10, '1000-3000'),   None,                      None,                      None,                      None,                  None,                     None),
        'k': (None,                     ('sp', 30, '1000-6000'),   ('ep', 10, '1000-2000'),   None,                      None,                      None,                  None,                     None),
        'l': (None,                     None,                      None,                      None,                      None,                      ('gems', 50, '1-4'),   None,                     None),
        'm': (None,                     None,                      None,                      ('gp', 40, '2000-8000'),   ('pp', 50, '5000-30000'),  ('gems', 55, '5-20'),  ('jewelry', 45, '2-12'),  None),
        'o': (None,                     None,                      None,                      None,                      None,                      None,                  None,                     ('magic', 50, (_d4_scrolls, ))),
        'u': (('cp', 10, '1-100'),      ('sp', 10, '1-100'),       None,                      ('gp', 5, '1-100'),        None,                      ('gems', 5, '1-4'),    ('jewelry', 5, '1-4'),    ('magic', 2, (_item, ))),
        'v': (None,                     ('sp', 10, '1-100'),       ('ep', 10, '1-100'),       ('gp', 10, '1-100'),       ('pp', 5, '1-100'),        ('gems', 10, '1-4'),   ('jewelry', 10, '1-4'),   ('magic', 5, (_item, ))),
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
        # (11, 'Helm of Reading Languages'), # Instead of change alignment
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

    def sword_extras(self, sword):
        if ',' not in sword and d100() <= 10:  # Only if not already funky, double to 2 in 20.
            sword = f'{sword} {self.special_sword()}'
        elif d100() <= 30:
            sword = f'{sword}: {self.sentient_sword()}'
        return sword

    def charges(self, result):
        # BX, changed charge dice d12 instead d10.
        charges = ''
        if 'wand' in result.lower():
            charges = f' ({d12() + d12()} charges)'
        elif 'staff' in result.lower():
            charges = '' if 'Healing' in result or 'Snek' in result else f' ({d12() + d12() + d12()} charges)'
        elif 'rod' in result.lower():
            charges = f' ({d12()} charges)'
        return charges
        # TODO: resolve dead code, Greyhawk charges, unreachable (it was after the return in _wsr).
        div = 1
        if '*' in result:
            return ''
        if 'wand' in result.lower():
            charges = f' [6th, {random.randint(80 // div, 200 // div)} charges]'
        elif 'staff' in result.lower():
            charges = f' [8th, {random.randint(40 // div, 100 // div)} charges]'
        elif 'rod' in result.lower():
            charges = f' [{random.randint(15 // div, 25 // div)} charges]'
        return charges

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
        powers = []
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
            elif result not in powers or '3x damge' in result or 'Heas as spell' in result:
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


class BasicRules(ExpertRules):
    name = 'basic'
    jewelries = Jewelries('expert')
    gems = Gems('expert')
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
        (7, 'Helm of Reading Languages'),  # Instead of change alignment.
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
        return None


@click.command(cls=AliasedGroup)
@click.option('-b', '--basic', default=False, is_flag=True, help='Use B/X level 1-3 tables.')
@click.option('-x', '--expert', default=False, is_flag=True, help='Use B/X tables (default).')
@click.option('-o', '--odd', default=False, is_flag=True, help='Use ODD tables.')
@click.option('-g', '--greyhawk', default=False, is_flag=True, help='Use ODD + Greyhawk tables.')
@click.option('-a', '--alt-greyhawk', default=False, is_flag=True, help='Use ODD + Greyhawk tweaked tables.')
@click.option('-r', '--roll', default=None, type=int, help='Use this d100 roll.')
@click.pass_context
def cli(ctx, basic, expert, odd, greyhawk, alt_greyhawk, roll):
    """Roll up treasure hoards and items. B/X Expert by default."""
    chosen = [rules for flag, rules in (
        (basic, BasicRules), (expert, ExpertRules), (odd, OddRules), (greyhawk, GreyhawkRules), (alt_greyhawk, AltGreyhawkRules),
        ) if flag]
    if len(chosen) > 1:
        raise click.UsageError('Choose only one of -b, -x, -o, -g, -a.')
    treasure = (chosen or [ExpertRules])[0]()
    click.echo(f'Using {treasure.name} rules.')
    ctx.obj['treasure'] = treasure
    ctx.obj['roll'] = roll


for name in ('item', 'sword', 'armor', 'weapon', 'potion', 'scroll', 'ring', 'wsr', 'misc', 'map'):
    def _inner(name=name):
        def func(ctx, count):
            click.echo('\n'.join(f'{c} x {x}' for c, v, x in reduce_groups((1, 0, globals()[f'_{name}'](ctx.obj['treasure'], ctx.obj['roll'])) for x in range(count))))
        func.__name__ = name
        func.__doc__ = 'Roll up ' + {
                'wsr': 'wand, staff, rod.',
                'item': 'magic item.',
                'misc': 'miscellaneous magic items.',
                'map': 'treasure and magic maps.',
                'scroll': 'magic scrolls.',
                'potion': 'potions.'}.get(name, f'magic {name}s.')
        return func
    subcommand = _inner()
    subcommand = click.pass_context(subcommand)
    subcommand = click.argument('count', default=1, type=int)(subcommand)
    cli.command()(subcommand)


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


@cli.command('type')
@click.option('-s', '--something', default=False, is_flag=True, help='Re-roll until something.')
@click.argument('code')
@click.pass_context
def treasure_type(ctx, code, something):
    """Roll up treasure type."""
    t = ctx.obj['treasure']
    if code.lower() not in t.TREASURE_TYPES:
        raise click.BadParameter(f'{code} is not one of {", ".join(sorted(t.TREASURE_TYPES))} for {t.name} rules.')
    stuff = list(t.type(code.lower()))
    while something and not stuff:
        stuff = list(t.type(code.lower()))
    click.echo('\n'.join(stuff) or 'Nothing')


if __name__ == '__main__':
    cli(obj={})
