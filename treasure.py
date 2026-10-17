#!/usr/bin/env python3
"""Random treasure generation for OSE or OD&D.

Rulesets (command line flag, rules name):
    -b   Basic              OSE levels 1-3 rules with tweaks.
    -x   Expert (default)   OSE Expert rules with tweaks.
    -a   Advanced           OSE Advanced rules as written.
    -g   OD&D + Greyhawk    OD&D Vol 2 + Greyhawk supplement with tweaks.
    -o   OD&D               OD&D Vol 2 (Monsters & Treasure), rules as written.
    -r/--raw                rules as written
    -rb  Basic rules as written
    -rx  Expert rules as written
    -rg  OD&D + Greyhawk rules as written
    -ro  OD&D rules as written, the same as -o.
    -ra  Advanced rules as written, the same as -a.

Version: 10/17/2026
Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: https://github.com/njharman/rpg
"""
import collections
import itertools
import operator
import random
import re

import click
from die import d6, d10, d12, d100

NO_WEAPONS = ('Sword', 'Misc. Weapon')


def reduce_groups(things):
    """Combine (count, value, thing) with the same value and thing, summing the counts."""
    ordered = sorted(things, key=operator.itemgetter(1, 2))
    for (value, thing), group in itertools.groupby(ordered, key=operator.itemgetter(1, 2)):
        yield sum(count for count, _, _ in group), value, thing


def replace_quantity(text):
    """Roll every N-M (N dice, max M) in text; return (first roll, text with the rolls in place).

    N000-M000 is in thousands, e.g. 1000-6000 is 1d6 x 1000.
    A range that is not N dice (2-5) is uniform.
    """
    rolls = []

    def roll_range(match):
        dice, maximum = map(int, match.groups())
        scale = 1
        if dice and dice % 1000 == 0 and maximum % 1000 == 0:
            dice, maximum, scale = dice // 1000, maximum // 1000, 1000
        if dice and maximum % dice == 0:
            value = sum(random.randint(1, maximum // dice) for _ in range(dice))
        else:
            value = random.randint(dice, maximum)
        rolls.append(value * scale)
        return f'{value * scale:,}'
    result = re.sub(r'(\d+)-(\d+)', roll_range, text)
    return (rolls[0] if rolls else 1), result


def table(chart, roll=None):
    """Roll on chart using roll; a row's remaining columns are returned, one column alone is not wrapped."""
    if roll is None:
        roll = random.randint(1, chart[-1][0])  # auto detect highest value.
    for threshold, *columns in chart:
        if roll <= threshold:
            return columns[0] if len(columns) == 1 else tuple(columns)
    raise RollOutOfRange(f'Roll {roll} is higher than the table maximum {chart[-1][0]}.')


def _roll_table(rules, name, roll=None):
    """Roll on rules.<name>, fill in any <random details>, roll any quantities."""
    return replace_quantity(rules.random_details(table(getattr(rules, name), roll)))[1]


def _disguised(rules, name, result, words):
    """Referee misleads: if result contains any of words, it looks like another roll on rules.<name>."""
    liar = next((word for word in words if word in result.lower()), None)
    if liar is None:
        return result
    fake = result
    while any(word in fake.lower() for word in words):
        fake = _roll_table(rules, name)
    return f'{fake} ({liar})'


def _map_treasure(rules, number):
    parts = []
    for spec in MAP_TREASURE[number - 1]:
        count, text = replace_quantity(spec)
        for kind, treasures, group in (('gems', rules.gems, 10), ('jewelry', rules.jewelries, 1)):
            if spec.endswith(kind):
                worth = sum(quantity * value for quantity, value, _ in treasures.roll(count, group))
                text = f'{treasures.amount(count)} worth {worth:,}gp'
        parts.append(text)
    return ', '.join(parts)


def _map_magic(rules, number):
    count, skip, forced = MAP_MAGIC[number - 1]
    return '; '.join([entry_item(rules, skip=skip) for _ in range(count)] + [roll_function(rules) for roll_function in forced])


def entry_2d4_potions(rules, roll=None):
    return ', '.join(entry_potion(rules, roll) for _ in range(random.randint(1, 4) + random.randint(1, 4)))


def entry_d4_scrolls(rules, roll=None):
    return ', '.join(entry_scroll(rules, roll) for _ in range(random.randint(1, 4)))


def entry_item(rules, roll=None, skip=()):
    """Roll item category and item, rerolling categories named in skip."""
    while True:
        category, roll_function = table(rules.item, roll)
        if category not in skip:
            return roll_function(rules)
        roll = None


def entry_martial(rules, roll=None):
    roll_function = random.choice((entry_sword, entry_armor, entry_weapon))
    return roll_function(rules, roll)


def entry_ose_noweap(rules, roll=None):
    """OSE "magic items (not weapons)": any item category but Sword and Weapon."""
    return entry_item(rules, roll, skip=('Sword', 'Weapon'))


def entry_noweap(rules, roll=None):
    """Rings, wsr, and misc only."""
    roll_function = random.choice((entry_ring, entry_wsr, entry_misc))
    return roll_function(rules, roll)


def entry_armor(rules, roll=None):
    return re.sub(r'(Armor)', rules.armor_type, _roll_table(rules, 'armor', roll))


def entry_misc(rules, roll=None):
    result = table(rules.misc, roll)
    if isinstance(result, list):  # Greyhawk, roll for which table, then on it.
        result = table(result, roll)
    return replace_quantity(rules.random_details(result))[1]


def entry_potion(rules, roll=None):
    """Last 6+d6 turns."""
    result = _disguised(rules, 'potion', _roll_table(rules, 'potion', roll), rules.mislead)
    return result if result.startswith('Oil') else f'Potion of {result}'


def entry_ring(rules, roll=None):
    return f'Ring of {_disguised(rules, "ring", _roll_table(rules, "ring", roll), ("delusion", ))}'


def entry_sword(rules, roll=None):
    return rules.sword_extras(_roll_table(rules, 'sword', roll))


def entry_scroll(rules, roll=None):
    """Spells, protections, traps, curses and (OSE) treasure maps."""
    result = table(rules.scroll, roll)
    match result.lower():
        case 'trap':
            return f'Trapped Scroll: {table(rules.scroll_trap)}'
        case 'curse':
            return f'Cursed Scroll: {table(rules.scroll_curse)}'
        case lowered if lowered.startswith('treasure map'):
            return result
        case lowered if 'spell' in lowered:
            caster = random.choice(['Cleric', 'Magic-user', 'Magic-user', 'Magic-user'])
            return f'{caster} scroll {rules.spell_summary(caster, int(result.split()[0]))}'
        case _:
            return f'Scroll of {result}'


def entry_weapon(rules, roll=None):
    return _roll_table(rules, 'weapon', roll)


def entry_wsr(rules, roll=None):
    """Wand, Staff, Rod."""
    result = _roll_table(rules, 'wsr', roll)
    return f'{result}{rules.charges(result)}'


def entry_odd_map(rules, roll=None):
    """Roll up a map, and what it leads to."""
    kind = table(MAP_KINDS, roll)
    if kind == 'treasure':
        return f'Map to treasure: {_map_treasure(rules, random.randint(1, 8))}'
    if kind == 'magic':
        return f'Map to magic: {_map_magic(rules, random.randint(1, 8))}'
    treasure, magic, there = MAP_BOTH[random.randint(1, 8) - 1]
    text = f'Map to treasure: {_map_treasure(rules, treasure)}; magic: {_map_magic(rules, magic)}'
    return f'{text} (already there)' if there else text


def entry_odd_any(rules, roll=None, skip=()):
    """OD&D Vol 2 Magic/Maps Determination table: 75% magic item, 25% map."""
    if (roll or d100()) > 75:
        return entry_odd_map(rules)
    return entry_item(rules, skip=skip)


def entry_odd_noweap_any(rules, roll=None):
    """OD&D Vol 2 Type F: "no weapons, any other"."""
    return entry_odd_any(rules, roll, skip=NO_WEAPONS)


# OD&D Vol 2, Maps. Magic/Maps Determination: 76-00 is a map; Maps table picks kind.
MAP_KINDS = [(60, 'treasure'), (90, 'magic'), (100, 'both')]
# Treasure maps, d8. Quantities are N-M dice (000s are thousands).
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
    (3, (), (entry_potion, )),
    (3, (), (entry_scroll, entry_potion)),
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


class RollOutOfRange(ValueError):
    """A roll is higher than the highest row of the table it was made on."""


class Treasures:
    """Base for gems and jewelry; subclasses yield (1, value, description) per piece from _roll."""

    noun, plural = 'gem', 'gems'

    def roll(self, count, group):
        """List of (count, value, description)."""
        return list(reduce_groups(self._roll(count, group)))

    def _roll(self, count, group):
        raise NotImplementedError

    def amount(self, count):
        """'1 gem', '4 gems'."""
        return f'{count:,} {self.noun if count == 1 else self.plural}'

    def lines(self, count, group):
        """Header ('4 gems:') then an indented line per group; one piece alone is a single unindented line."""
        things = self.roll(count, group)
        if count == 1:
            _, value, thing = things[0]
            return [f'{value:,}gp {thing}' if value else thing]
        return [f'{self.amount(count)}:', *self._format(things)]

    def _format(self, things):
        things = sorted(things, key=lambda row: row[1] or 99999)
        count_width = max(len(str(count)) for count, _, _ in things)
        width = max((len(f'{value:,}') for _, value, _ in things if value), default=4)
        for count, value, thing in things:
            name = self.plural if count > 1 and thing == self.noun else thing  # Generic OD&D 'gem'.
            yield f' {count:>{count_width}} x {f"{value:,}" if value else "":>{width}}{"gp" if value else "  "} {name}'


class Gems(Treasures):
    values = [10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000]
    gems = [
        [  # 10 GP Gems (multicolored)
            'Agate - Multi-colored circles',  # Safe sleep
            'Tiger Eye - Brown with golden center under-hue',
            ],
        [  # 50 GP Gems (stone)
            'Bloodstone - Dark gray with red flecks',  # Weather Control
            'Moonstone - Lustrous white with pale blue glow',  # Lycanthropy
            ],
        [  # 100 GP Gems (solid color)
            'Carnelian - Orange to reddish brown',  # Protection from Evil
            'Jade - Light green, deep green, green and white',  # Protection from poison
            ],
        [  # 500 GP Gems (translucent)
            'Pearl - Lustrous white, pinkish, to pure black',  # Wisdom
            'Topaz - Translucent golden yellow',  # Earth Wards of evil
            ],
        [  # 1000 GP Gems (transparent)
            'Emerald - Transparent deep green',  # Water Undead protection / control
            'Ruby - Transparent crimson',  # Fire Good luck
            'Sapphire - Transparent vivid blue',  # Air intelligence, boosts magic
            ],
        [  # 5000 GP Gems
            'Diamond - Transparent clear blue-white',
            ],
        ]
    unusual = [
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
    sizes = {2: 'large', 4: 'giant', 8: 'enormous'}

    def __init__(self, chances, specials=True):
        """chances: cumulative d100 chance of each value in values. specials: 1 in 10 gems may be magical or larger."""
        self.chances = chances
        self.specials = specials

    def _roll(self, count, group):
        """Roll up count gems, in groups of size group."""
        size = value = 0
        magical_found = False  # Only one magical gem.
        for position in range(count):
            # Roll in groups; but reset when larger, magical or valuable.
            if position % group == 0 or size or value == 0 or value > 500:
                roll = d100()
                tier = next(index for index, chance in enumerate(self.chances) if roll <= chance)
                gem = random.choice(self.gems[tier])
                value = self.values[tier]
            size = ''
            if self.specials and position % 10 == 1:  # 1 in 10 gems have chance of being special.
                # 30% chance to be magical, only if 100gp or greater and only one.
                if d100() <= 30 and value >= 100 and not magical_found:
                    value = 0
                    if 'Diamond' in gem:  # All magical Diamonds are True Seeing Gems.
                        gem = 'Diamond of True Seeing'
                    else:
                        gem = f'{gem[0:gem.index(" - ")]} {random.choice(self.unusual)}'
                    magical_found = True  # Only one magic gem per hoard.
                # 20% of non-magical gems are larger than usual.
                elif d100() <= 20:
                    multiplier = random.choice([2, 2, 2, 4, 4, 8])
                    value *= multiplier
                    size = f'{self.sizes[multiplier]} '
            yield 1, value, f'{size}{gem}'


class Jewelries(Treasures):
    noun = plural = 'jewelry'
    designs = [  # (minimum value, design), highest first.
        (1800, 'jewelry platinum and gems'),
        (1600, 'jewelry gold with gems'),
        (1200, 'jewelry silver with gems'),
        (1000, 'jewelry wrought platinum'),
        (700, 'jewelry wrought gold'),
        (0, 'jewelry wrought silver'),
        ]

    def _roll(self, count, group):
        """Roll up count pieces of jewelry, group ignored."""
        for _ in range(count):
            value = (d6() + d6() + d6()) * 100
            design = next(design for minimum, design in self.designs if value >= minimum)
            yield 1, value, design


# TODO: implement fur Treasures.
# Furs:    Pelt   Trimming* Cape / Jacket  Coat
# beaver   2      20 g.p.   200 g.p.       400 g.p.
# ermine   4      120 g.p.  3,600S.P.      7,200g.p.
# fox      3      90 S.P.   300 g.p.       600 g.p.
# marten   4      10 g.p.   400 g.p.       800 g.p.
# mink     3      30 g.p.   100 g.p.       5,400g.p.
# muskrat  1      40 g.p.   4,500S.P.      200 g.p.
# sable    5      150 g.p.  2,700g.p.      9,000 S.P.
# seal     5      25 g.p.   125 g.p.       250 g.p
#
# * on collar cuffs and edges of garment


class GemsOdd(Treasures):
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
        for position in range(count):
            if position % group == 0:
                index = self.values.index(table(self.base))
                while d6() == 1 and index < len(self.values) - 1:
                    index += 1
                value = self.values[index]
            yield 1, value, 'gem'


class JewelriesOdd(Treasures):
    """OD&D Vol 2, Treasure: Jewelry, as written."""

    noun = plural = 'jewelry'

    def _roll(self, count, group):
        """Roll up count pieces of jewelry, group ignored."""
        for _ in range(count):
            roll = d100()
            if roll <= 20:
                value = (d6() + d6() + d6()) * 100
            elif roll <= 80:
                value = d6() * 1000
            else:
                value = random.randint(1, 10) * 1000
            yield 1, value, 'jewelry'


class Rules:
    """Base of the rulesets: the tables to roll on and the hooks that adjust a roll.

    A ruleset subclass supplies:
    - name: shown by the CLI, see title.
    - raw: True if rules as written, no tweaks.
    - TREASURE_TYPES: treasure type code -> rows of (kind, chance, amount), None for kinds the type lacks.
      Kind is a coin, 'gems', 'jewelry' or 'magic'. Amount is a quantity (N-M, see replace_quantity);
      for magic it is the entry_* functions to roll.
    - gems, jewelries: Treasures instances.
    - item: magic item categories, rows of (highest roll, category, entry_* function).
    - sword, armor, weapon, potion, scroll, ring, wsr, misc: rows of (highest roll, text), see table().
      Text may hold <name> placeholders, filled by random_details from _random_<name>.
    - _spell_level(caster): method returning the table of spell levels for a scroll's spells.
    - scroll_trap: effects of a trapped scroll (scroll table 'trap'), custom table.
    - scroll_curse: effects of a cursed scroll (scroll table 'Curse'), the ruleset's book table.

    Class attributes below can be overridden to change how rolls are adjusted: mislead.
    Subclasses override armor_type, charges and sword_extras to post-process a rolled item.
    """

    scroll_trap = [
        (2, 'Summons Monster'),
        (4, '+/-2 penalty to Attack/Saves/AC'),
        (6, 'Death like paralysis 2-8 days (no save)'),
        (7, '4-24 fire to reader (no save).'),
        (8, 'Fatal disease 2d6 turns (no save)'),
        ]
    mislead = ('delusion', )  # Potions that look like another potion.
    raw = False

    @property
    def title(self):
        """'Expert rules', 'Expert rules as written'."""
        return f'{self.name} rules as written' if self.raw else f'{self.name} rules'

    def armor_type(self, match):
        return match.group(1)

    def random_details(self, text):
        """Replace each <name> with a roll on self._random_name (a table or a method); leave unknown names."""
        def roll_detail(match):
            source = getattr(self, f'_random_{match.group(1)}', None)
            if source is None:
                return match.group(0)
            return source() if callable(source) else table(source)
        return re.sub(r'<(\w+)>', roll_detail, text)

    def spell_summary(self, caster, count):
        """Roll the levels of count spells, as '2x1st, 1x3rd'."""
        levels = reduce_groups((1, 0, table(self._spell_level(caster))) for _ in range(count))
        return ', '.join(f'{quantity}x{level}' for quantity, _, level in levels)

    def sword_extras(self, sword):
        """Alignment, intelligence, special powers and such for a rolled sword."""
        return sword

    def treasure_type(self, code, roll=None):
        """Roll a treasure type."""
        for check in self.TREASURE_TYPES[code]:
            if check:
                yield from self._roll_check(*check, roll)

    def _roll_check(self, kind, chance, amount, roll=None):
        """For single check of Treasure Type; amount is a quantity (N-M), or for magic the functions to roll."""
        if roll is None:
            roll = d100()
        if roll > chance:
            return
        if kind == 'magic':
            for roll_function in amount:
                yield roll_function(self)
        else:
            count, text = replace_quantity(amount)
            if kind == 'gems':
                yield from self.gems.lines(count, 10)
            elif kind == 'jewelry':
                yield from self.jewelries.lines(count, 1)
            else:
                yield f'{text}{kind}'

    def charges(self, item):
        """Text for the charges of a wand, staff or rod."""
        return ''


class OddRules(Rules):
    """OD&D three LBB, Vol 2 Monsters & Treasure (1974), rules as written.

    Where the book is ambiguous the choice is commented "Judgement".
    """
    name = 'OD&D'
    raw = True
    gems = GemsOdd()
    jewelries = JewelriesOdd()
    mislead = ('delusion', 'poison')  # "Referee will mislead", even a sip of poison kills.
    # Referee rolls which Giants. Hill 60%, others 10% each.
    _random_giant = [(60, 'Hill'), (70, 'Stone'), (80, 'Frost'), (90, 'Fire'), (100, 'Cloud')]
    # Referee rolls which of the six Dragons.
    _random_dragon = [(1, 'White'), (2, 'Black'), (3, 'Green'), (4, 'Blue'), (5, 'Red'), (6, 'Golden')]
    # Wands 100, Staves 200 charges, except these (Vol 2, Wands and Staves).
    _chargeless = ('Metal Detection', 'Enemy Detection', 'Secret Doors', 'Healing', 'Snake Staff', 'Striking')
    # Treasure Types, thousands of coins are written 1000-6000 (d6 x 1000). Columns: cp sp gp gems jewelry magic.
    # Roll for each of Gems and Jewelry. Magic "any" is a roll on the Magic/Maps table, 25% maps.
    TREASURE_TYPES = {
        'a': (('cp', 25, '1000-6000'),  ('sp', 30, '1000-6000'),   ('gp', 35, '2000-12000'),  ('gems', 50, '6-36'),  ('jewelry', 50, '6-36'),  ('magic', 40, (entry_odd_any, entry_odd_any, entry_odd_any))),
        'a-desert': (('cp', 20, '1000-4000'), ('sp', 25, '1000-4000'), ('gp', 30, '1000-6000'), ('gems', 50, '10-40'), ('jewelry', 50, '10-40'), ('magic', 60, (entry_item, entry_item, entry_item))),
        'a-water': (None,               None,                      ('gp', 60, '5000-30000'),  ('gems', 60, '10-60'), ('jewelry', 60, '10-60'), ('magic', 50, (entry_odd_map, ))),
        'b': (('cp', 50, '1000-8000'),  ('sp', 25, '1000-6000'),   ('gp', 25, '1000-3000'),   ('gems', 25, '1-6'),   ('jewelry', 25, '1-6'),   ('magic', 10, (entry_martial, ))),  # Weapon, Armor, or Misc. Weapon.
        'c': (('cp', 20, '1000-12000'), ('sp', 30, '1000-4000'),   None,                      ('gems', 25, '1-4'),   ('jewelry', 25, '1-4'),   ('magic', 10, (entry_odd_any, entry_odd_any))),
        'd': (('cp', 10, '1000-8000'),  ('sp', 15, '1000-12000'),  ('gp', 60, '1000-6000'),   ('gems', 30, '1-8'),   ('jewelry', 30, '1-8'),   ('magic', 20, (entry_odd_any, entry_odd_any, entry_potion))),
        'e': (('cp',  5, '1000-10000'), ('sp', 30, '1000-12000'),  ('gp', 25, '1000-8000'),   ('gems', 10, '1-10'),  ('jewelry', 10, '1-10'),  ('magic', 30, (entry_odd_any, entry_odd_any, entry_odd_any, entry_scroll))),
        'f': (None,                     ('sp', 10, '2000-20000'),  ('gp', 45, '1000-12000'),  ('gems', 20, '2-24'),  ('jewelry', 20, '2-24'),  ('magic', 35, (entry_odd_noweap_any, entry_odd_noweap_any, entry_odd_noweap_any, entry_potion, entry_scroll))),
        'g': (None,                     None,                      ('gp', 75, '10000-40000'), ('gems', 25, '3-18'),  ('jewelry', 25, '1-10'),  ('magic', 40, (entry_odd_any, entry_odd_any, entry_odd_any, entry_odd_any, entry_scroll))),
        'h': (('cp', 25, '3000-24000'), ('sp', 50, '1000-100000'), ('gp', 75, '10000-60000'), ('gems', 50, '1-100'), ('jewelry', 50, '10-40'), ('magic', 20, (entry_odd_any, entry_odd_any, entry_odd_any, entry_odd_any, entry_potion, entry_scroll))),
        'i': (None,                     None,                      None,                      ('gems', 50, '2-16'),  ('jewelry', 50, '2-16'),  ('magic', 20, (entry_odd_any, ))),
        }
    # Magic/Maps Determination: Magic Items.
    item = [
        (20, 'Sword', entry_sword),
        (35, 'Armor', entry_armor),
        (40, 'Misc. Weapon', entry_weapon),
        (65, 'Potion', entry_potion),
        (85, 'Scroll', entry_scroll),
        (90, 'Ring', entry_ring),
        (95, 'Wand/Staff', entry_wsr),
        (100, 'Misc. Magic', entry_misc),
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
    scroll_curse = [
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
    # Wands: Magic-Users only. Staves: (C)lerics, (M)agic-Users.
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
    _sword_alignment = [(65, 'Lawful'), (90, 'Neutral'), (100, 'Chaotic')]
    # Primary Powers. 96-99 is two rolls ignoring 96-99 (00 allowed), 00 is an Extraordinary Ability.
    _sword_primary = [
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
    # Languages, in addition to alignment's. Judgement: book has 86-95 Four and 90-99 Five, took 96-99.
    # 00 is two rolls ignoring 00.
    _sword_languages = [(50, 1), (70, 2), (85, 3), (95, 4), (99, 5)]
    # Extraordinary Abilities. 98-99 is two rolls ignoring over 97, 00 is three rolls.
    _sword_extraordinary = [
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
    _sword_purposes = ['Slay Magic-Users', 'Slay Clerics', 'Slay Fighting-Men', 'Slay Monsters', 'Defeat Law', 'Defeat Chaos']
    _sword_purpose_powers = {
        'Lawful': 'paralyze Chaotic opponents',
        'Neutral': '+1 to all saving throws',
        'Chaotic': 'disintegrate Lawful opponents',
        }

    def sword_extras(self, sword):
        """Alignment, Intelligence, Egoism and Origin/Purpose. Vol 2, Explanations of Magic Items: Swords."""
        alignment = table(self._sword_alignment)
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
            powers = self._sword_primary_powers({7: 1, 8: 2}.get(intelligence, 3))
            parts += [f'Int {intelligence}', f'Ego {ego}', 'telepathy' if intelligence == 12 else 'speech' if intelligence >= 10 else 'empathy']
            if intelligence >= 10:
                languages = self._sword_language_count()
                parts.append(f'{languages} language{"" if languages == 1 else "s"} besides {alignment}')
            if intelligence >= 11:
                parts.append('reads magic')
            if intelligence == 12:
                powers += self._sword_extraordinary_powers()
            if special:
                purpose = random.choice(self._sword_purposes)
                while (alignment, purpose) in (('Lawful', 'Defeat Law'), ('Chaotic', 'Defeat Chaos')):  # Judgement: can't defeat itself.
                    purpose = random.choice(self._sword_purposes)
                powers.append(f'{purpose}, {self._sword_purpose_powers[alignment]}')
            if powers:
                parts.append(', '.join(f'{power} x{count}' if count > 1 else power for power, count in collections.Counter(powers).items()))
        return f'{sword} ({", ".join(parts)})'

    def _sword_primary_powers(self, count):
        found = []
        for _ in range(count):
            roll = d100()
            rolls = [roll]
            if 96 <= roll <= 99:
                rolls = []
                while len(rolls) < 2:
                    reroll = d100()
                    if not 96 <= reroll <= 99:
                        rolls.append(reroll)
            for rolled in rolls:
                found += self._sword_extraordinary_powers() if rolled == 100 else [table(self._sword_primary, rolled)]
        return found

    def _sword_extraordinary_powers(self):
        roll = d100()
        if roll <= 97:
            return [replace_quantity(table(self._sword_extraordinary, roll))[1]]
        return [replace_quantity(table(self._sword_extraordinary, random.randint(1, 97)))[1] for _ in range(2 if roll < 100 else 3)]

    def _sword_language_count(self):
        roll = d100()
        if roll < 100:
            return table(self._sword_languages, roll)
        return sum(table(self._sword_languages, random.randint(1, 99)) for _ in range(2))

    def charges(self, item):
        """The maximum charges, wands 100, staves 200, Greyhawk rods 25."""
        non_standard = self._non_standard_charges(item)
        if non_standard is not None:
            return non_standard
        if 'Wand' in item:
            return ' [100 charges]'
        if 'Staff' in item:
            return ' [200 charges]'
        if 'Rod' in item:
            return ' [25 charges]'
        return ''

    def _non_standard_charges(self, item):
        """Charges text for items that don't use the standard wand, staff or rod rule; None for the standard.

        Vol 2 and Greyhawk, Wands and Staves. Items that only exist in Greyhawk never match in Vol 2.
        """
        if any(word in item for word in self._chargeless):
            return ''
        if 'Cancellation' in item:
            return ' [single use]'
        if 'Rulership' in item:
            return ' [10 charges]'
        if 'Absorption' in item:
            return ' [100 spell levels]'
        return None

    def _random_spells(self):
        """Ring of Spell Storing: 1-6 spells, 20% Clerical, half of those Chaotic. Never mixed."""
        spell_type = 'Magic-user'
        if d100() <= 20:
            spell_type = 'Chaotic Cleric' if d100() <= 50 else 'Cleric'
        return f'{spell_type} spells {self.spell_summary(spell_type.split()[-1], d6())}'

    def _spell_level(self, caster):
        """Spell level is d6. Judgement: Vol 1 Clerics have no 6th level spells, so d5."""
        levels = [(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th'), (5, '5th'), (6, '6th')]
        return levels[:5] if caster == 'Cleric' else levels


class GreyhawkRawRules(OddRules):
    """OD&D three LBB plus Greyhawk Supplement I (1975), rules as written.

    Greyhawk's Magic/Maps Determination Additions and Changes replace the Vol 2 tables
    for swords, misc. weapons, armor, potions, rings, wands/staves/rods and misc. magic.
    Item categories, scrolls, treasure types and sword sentience stay as Vol 2.
    """
    name = 'OD&D + Greyhawk'
    # Judgement: Storm Giants are in Greyhawk's monsters, Hill Giants lose a share to them.
    _random_giant = [(50, 'Hill'), (60, 'Stone'), (70, 'Frost'), (80, 'Fire'), (90, 'Cloud'), (100, 'Storm')]
    # Greyhawk adds Brass, Copper, Bronze, Silver Dragons (and calls Golden, Gold).
    _random_dragon = [(1, 'White'), (2, 'Black'), (3, 'Green'), (4, 'Blue'), (5, 'Red'), (6, 'Gold'), (7, 'Brass'), (8, 'Copper'), (9, 'Bronze'), (10, 'Silver')]
    _random_slaying = [(1, 'Giant Class'), (2, 'Undead Class'), (3, 'Flying Monsters'), (4, 'Other Monsters'), (5, 'Enchanted Monsters')]
    # Greyhawk corrects Staff of Striking, it uses charges.
    _chargeless = ('Metal Detection', 'Enemy Detection', 'Secret Doors', 'Healing', 'Snake Staff')
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
    # Armor/Shield +4 are Mithral, +5 Adamantite. Vulnerable armor looks +1 to +4 but is -1 to -4.
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
    # (F)ighters only. Referee rolls which Giants and Dragons.
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
    # Wands, Staves and Rods. (A)ll, (C)lerics, (F)ighters, (M)agic-Users, (T)hieves.
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
        (39, 'Helm of Teleportation'),
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


class GreyhawkRules(GreyhawkRawRules):
    """Greyhawk with tweaks. Everything not listed here is as GreyhawkRawRules.

    Differences from the books:
    - Treasure Type F's magic is rings, wands/staves/rods and misc. magic (no maps, nor armor, potion or scroll)
      plus a potion and a scroll.
    - Treasure Types O, Q, S are added, they are not OD&D (AD&D Monster Manual style).
    - Gems and Jewelry are the Gems / Jewelries classes (not GemsOdd / JewelriesOdd).
    - Swords: cursed swords are 83-87 +1 Cursed Berserker, 88-92 -1 Cursed, 93-97 -2 Cursed (book 83 +1, 84-97 -2).
    - Armor, misc. weapons and scrolls are custom tables, see below.
    - Wand, staff and rod charges are rolled: wand 80-200 (6th level), staff 40-100 (8th), rod 15-25.
      Chargeless items, Rods of Cancellation, Rulership and Absorption are as Greyhawk.
    """
    raw = False
    gems = Gems([10, 25, 75, 90, 99, 100])
    jewelries = Jewelries()
    TREASURE_TYPES = {
        **GreyhawkRawRules.TREASURE_TYPES,
        'f': (None,                     ('sp', 10, '2000-20000'),  ('gp', 45, '1000-12000'),  ('gems', 20, '2-24'),  ('jewelry', 20, '2-24'),  ('magic', 35, (entry_noweap, entry_noweap, entry_noweap, entry_potion, entry_scroll))),
        'o': (('cp', 25, '1000-4000'),  ('sp', 20, '1000-3000'),   None,                      None,                  None,                     None),
        'q': (None,                     None,                      None,                      ('gems', 50, '1-4'),   None,                     None),
        's': (None,                     None,                      None,                      None,                  None,                     ('magic', 40, (entry_2d4_potions, ))),
        }
    sword = [row for row in GreyhawkRawRules.sword if row[0] < 83] + [
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
        (83, 'Mithral Plate & Shield +4'),
        (85, 'Adamantite Shield +5'),
        (86, 'Adamantite Plate +5'),
        (87, 'Adamantite Plate & Shield +5'),
        (90, 'Shield of Missile Attraction'),
        (93, '-1-3 Shield of Vulnerability'),
        (99, '-1-3 Plate of Vulnerability'),
        (100, 'Plate of Etherealness'),
        ]
    # Misc. weapons: custom table, only loosely Greyhawk's. Same kinds of items but re-balanced odds and counts
    # (3-18 +1 arrows, 3-18 +1 bolts, 2-12 +2 bolts, Arrow/Bolt of Slaying, own daggers, Magic Bow +1, Axe +1 to +3,
    # Mace +1 to +3). Added: Sling +1, "Unusual Misc Weapon" +1, Axe of Missing, Sticky Mace.
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
    # Scrolls: custom table, not the book's. Differs: Curse (book 51-60) is a 1-10 trap using Rules.scroll_trap
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

    def charges(self, item):
        non_standard = self._non_standard_charges(item)
        if non_standard is not None:
            return non_standard
        if 'Wand' in item:
            return f' [6th, {random.randint(80, 200)} charges]'
        if 'Staff' in item:
            return f' [8th, {random.randint(40, 100)} charges]'
        if 'Rod' in item:
            return f' [{random.randint(15, 25)} charges]'
        return ''


class ExpertRawRules(Rules):
    """OSE Expert treasure and magic items, rules as written from OSE Rules Tome v1.4.

    Magic item tables use the Expert (character level 4+) column. Where the book is ambiguous the choice is
    commented "Judgement". Gem names and jewelry designs are flavor; the book gives only their values.
    """
    name = 'Expert'
    raw = True
    gems = Gems([20, 45, 75, 95, 100], specials=False)
    jewelries = Jewelries()
    # Treasure Types, thousands of coins are written 1000-6000 (d6 x 1000). Columns: cp sp ep gp pp gems jewelry magic.
    # Individual treasure P-T have no percentage, it is always there.
    TREASURE_TYPES = {
        'a': (('cp', 25, '1000-6000'),  ('sp', 30, '1000-6000'),   ('ep', 20, '1000-4000'),   ('gp', 35, '2000-12000'),  ('pp', 25, '1000-2000'),   ('gems', 50, '6-36'),  ('jewelry', 50, '6-36'),  ('magic', 30, (entry_item, entry_item, entry_item))),
        'b': (('cp', 50, '1000-8000'),  ('sp', 25, '1000-6000'),   ('ep', 25, '1000-4000'),   ('gp', 25, '1000-3000'),   None,                      ('gems', 25, '1-6'),   ('jewelry', 25, '1-6'),   ('magic', 10, (entry_martial, ))),
        'c': (('cp', 20, '1000-12000'), ('sp', 30, '1000-4000'),   ('ep', 10, '1000-4000'),   None,                      None,                      ('gems', 25, '1-4'),   ('jewelry', 25, '1-4'),   ('magic', 10, (entry_item, entry_item))),
        'd': (('cp', 10, '1000-8000'),  ('sp', 15, '1000-12000'),  None,                      ('gp', 60, '1000-6000'),   None,                      ('gems', 30, '1-8'),   ('jewelry', 30, '1-8'),   ('magic', 15, (entry_item, entry_item, entry_potion))),
        'e': (('cp',  5, '1000-10000'), ('sp', 30, '1000-12000'),  ('ep', 25, '1000-4000'),   ('gp', 25, '1000-8000'),   None,                      ('gems', 10, '1-10'),  ('jewelry', 10, '1-10'),  ('magic', 25, (entry_item, entry_item, entry_item, entry_scroll))),
        'f': (None,                     ('sp', 10, '2000-20000'),  ('ep', 20, '1000-8000'),   ('gp', 45, '1000-12000'),  ('pp', 30, '1000-3000'),   ('gems', 20, '2-24'),  ('jewelry', 10, '1-12'),  ('magic', 30, (entry_ose_noweap, entry_ose_noweap, entry_ose_noweap, entry_potion, entry_scroll))),
        'g': (None,                     None,                      None,                      ('gp', 50, '10000-40000'), ('pp', 50, '1000-6000'),   ('gems', 25, '3-18'),  ('jewelry', 25, '1-10'),  ('magic', 35, (entry_item, entry_item, entry_item, entry_item, entry_scroll))),
        'h': (('cp', 25, '3000-24000'), ('sp', 50, '1000-100000'), ('ep', 50, '10000-40000'), ('gp', 50, '10000-60000'), ('pp', 25, '5000-20000'),  ('gems', 50, '1-100'), ('jewelry', 50, '10-40'), ('magic', 15, (entry_item, entry_item, entry_item, entry_item, entry_potion, entry_scroll))),
        'i': (None,                     None,                      None,                      None,                      ('pp', 30, '1000-8000'),   ('gems', 50, '2-12'),  ('jewelry', 50, '2-12'),  ('magic', 15, (entry_item, ))),
        'j': (('cp', 25, '1000-4000'),  ('sp', 10, '1000-3000'),   None,                      None,                      None,                      None,                  None,                     None),
        'k': (None,                     ('sp', 30, '1000-6000'),   ('ep', 10, '1000-2000'),   None,                      None,                      None,                  None,                     None),
        'l': (None,                     None,                      None,                      None,                      None,                      ('gems', 50, '1-4'),   None,                     None),
        'm': (None,                     None,                      None,                      ('gp', 40, '2000-8000'),   ('pp', 50, '5000-30000'),  ('gems', 55, '5-20'),  ('jewelry', 45, '2-12'),  None),
        'n': (None,                     None,                      None,                      None,                      None,                      None,                  None,                     ('magic', 40, (entry_2d4_potions, ))),
        'o': (None,                     None,                      None,                      None,                      None,                      None,                  None,                     ('magic', 50, (entry_d4_scrolls, ))),
        'p': (('cp', 100, '3-24'),      None,                      None,                      None,                      None,                      None,                  None,                     None),
        'q': (None,                     ('sp', 100, '3-18'),       None,                      None,                      None,                      None,                  None,                     None),
        'r': (None,                     None,                      ('ep', 100, '2-12'),       None,                      None,                      None,                  None,                     None),
        's': (None,                     None,                      None,                      ('gp', 100, '2-8'),        None,                      None,                  None,                     None),
        't': (None,                     None,                      None,                      None,                      ('pp', 100, '1-6'),        None,                  None,                     None),
        'u': (('cp', 10, '1-100'),      ('sp', 10, '1-100'),       None,                      ('gp', 5, '1-100'),        None,                      ('gems', 5, '1-4'),    ('jewelry', 5, '1-4'),    ('magic', 2, (entry_item, ))),
        'v': (None,                     ('sp', 10, '1-100'),       ('ep', 5, '1-100'),        ('gp', 10, '1-100'),       ('pp', 5, '1-100'),        ('gems', 10, '1-4'),   ('jewelry', 10, '1-4'),   ('magic', 5, (entry_item, ))),
        }
    item = [
        (10, 'Armor', entry_armor),
        (15, 'Misc', entry_misc),
        (35, 'Potion', entry_potion),
        (40, 'Ring', entry_ring),
        (45, 'W/S/R', entry_wsr),
        (75, 'Scroll', entry_scroll),
        (95, 'Sword', entry_sword),
        (100, 'Weapon', entry_weapon),
        ]
    # Each "Armor" is replaced by a rolled type, see armor_type. Cursed armor tests as +1.
    armor = [
        (15, 'Armor +1'),
        (25, 'Armor +1, Shield +1'),
        (27, 'Armor +1, Shield +2'),
        (28, 'Armor +1, Shield +3'),
        (33, 'Armor +2'),
        (36, 'Armor +2, Shield +1'),
        (41, 'Armor +2, Shield +2'),
        (42, 'Armor +2, Shield +3'),
        (45, 'Armor +3'),
        (46, 'Armor +3, Shield +1'),
        (47, 'Armor +3, Shield +2'),
        (48, 'Armor +3, Shield +3'),
        (51, 'Cursed Armor -1'),
        (53, 'Cursed Armor -2'),
        (54, 'Cursed Armor -2, Shield +1'),
        (56, 'Cursed Armor, AC 9'),
        (62, 'Cursed Shield -2'),
        (65, 'Cursed Shield, AC 9'),
        (85, 'Shield +1'),
        (95, 'Shield +2'),
        (100, 'Shield +3'),
        ]
    _armor_type = [(2, 'Leather'), (6, 'Chain'), (8, 'Plate')]
    misc = [
        (3, 'Amulet of Protection Against Scrying'),
        (5, 'Bag of Devouring'),
        (11, 'Bag of Holding'),
        (16, 'Boots of Levitation'),
        (21, 'Boots of Speed'),
        (26, 'Boots of Travelling and Leaping'),
        (31, 'Broom of Flying'),
        (35, 'Crystal Ball'),
        (37, 'Crystal Ball with Clairaudience'),
        (38, 'Crystal Ball with ESP'),
        (40, 'Displacer Cloak'),
        (41, 'Drums of Panic'),
        (42, 'Efreeti Bottle'),
        (43, 'Elemental Summoning Device: Air'),
        (44, 'Elemental Summoning Device: Earth'),
        (45, 'Elemental Summoning Device: Fire'),
        (46, 'Elemental Summoning Device: Water'),
        (56, 'Elven Cloak and Boots'),
        (57, 'Flying Carpet'),
        (64, 'Gauntlets of Ogre Power'),
        (66, 'Girdle of Giant Strength'),
        (77, 'Helm of Alignment Changing'),
        (82, 'Helm of Reading Languages and Magic'),
        (83, 'Helm of Telepathy'),
        (84, 'Helm of Teleportation'),
        (85, 'Horn of Blasting'),
        (90, "Medallion of ESP 30'"),
        (93, "Medallion of ESP 90'"),
        (94, 'Mirror of Life Trapping'),
        (97, 'Rope of Climbing'),
        (100, 'Scarab of Protection'),
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
        (5, 'Control Animals'),
        (10, 'Control Humans'),
        (16, 'Control Plants'),
        (26, 'Delusion'),
        (29, 'Djinni Summoning'),
        (39, 'Fire Resistance'),
        (50, 'Invisibility'),
        (55, "Protection +1, 5' radius"),
        (70, 'Protection +1'),
        (72, 'Regeneration'),
        (74, 'Spell Storing (<spells>)'),
        (80, 'Spell Turning'),
        (82, 'Telekinesis'),
        (88, 'Water Walking'),
        (94, 'Weakness'),
        (96, 'Wishes (1-2)'),
        (97, 'Wishes (1-3)'),
        (98, 'Wishes (2-4)'),  # Judgement: Wishes 2-4 is rolled 2d2.
        (100, 'X-Ray Vision'),
        ]
    # Treasure maps are not rolled, the referee prepares them in advance.
    scroll = [
        (15, '1 Spell'),
        (25, '2 Spells'),
        (31, '3 Spells'),
        (34, '5 Spells'),
        (35, '7 Spells'),
        (40, 'Curse'),
        (50, 'Protection: Elementals'),
        (60, 'Protection: Lycanthropes'),
        (65, 'Protection: Magic'),
        (75, 'Protection: Undead'),
        (78, 'Treasure Map I: 1 magic item'),
        (80, 'Treasure Map II: 1d6 × 10 gems and 2d10 pieces of jewellery'),
        (82, 'Treasure Map III: 2 magic items'),
        (83, 'Treasure Map IV: 3 magic items (no swords)'),
        (84, 'Treasure Map V: 3 magic items and 1 potion'),
        (85, 'Treasure Map VI: 3 magic items, 1 scroll, 1 potion'),
        (86, 'Treasure Map VII: 5d6 gems and 2 magic items'),
        (90, 'Treasure Map VIII: Hoard worth 1d4 × 1,000gp'),
        (95, 'Treasure Map IX: Hoard worth 5d6 × 1,000gp'),
        (96, 'Treasure Map X: Hoard worth 5d6 × 1,000gp and 1 magic item'),
        (98, 'Treasure Map XI: Hoard worth 5d6 × 1,000gp and 5d6 gems'),
        (100, 'Treasure Map XII: Hoard worth 6d6 × 1,000gp'),
        ]
    # Judgement: the book has the referee choose a curse, these are its examples rolled on a d6.
    scroll_curse = [
        (1, 'Transformed into a harmless creature (e.g. a frog)'),
        (2, 'Wandering monster of equal level appears and attacks, with surprise'),
        (3, 'A magic item the reader possesses vanishes'),
        (4, 'Energy drain, permanently loses one level'),
        (5, 'Re-roll prime requisite'),
        (6, 'Slow healing, natural healing takes double, healing spells cure half'),
        ]
    sword = [
        (2, 'Sword -1, Cursed'),
        (4, 'Sword -2, Cursed'),
        (44, 'Sword +1'),
        (50, 'Sword +1, +2 vs Lycanthropes'),
        (56, 'Sword +1, +2 vs Spell Users'),
        (61, 'Sword +1, +3 vs Dragons'),
        (66, 'Sword +1, +3 vs Enchanted Creatures'),
        (71, 'Sword +1, +3 vs Regenerating Creatures'),
        (76, 'Sword +1, +3 vs Undead'),
        (77, 'Sword +1, Energy Drain (5-8 levels)'),
        (81, 'Sword +1, Flaming'),
        (89, 'Sword +1, Light'),
        (92, 'Sword +1, Locate Objects'),
        (93, 'Sword +1, Wishes (1-4)'),
        (96, 'Sword +2'),
        (98, 'Sword +2, Charm Person'),
        (100, 'Sword +3'),
        ]
    wsr = [
        (8, 'Rod of Cancellation'),
        (11, 'Staff of Commanding'),
        (21, 'Staff of Healing'),
        (23, 'Staff of Power'),
        (28, 'Staff of Snakes'),
        (31, 'Staff of Striking'),
        (34, 'Staff of Withering'),
        (35, 'Staff of Wizardry'),
        (40, 'Wand of Cold'),
        (45, 'Wand of Enemy Detection'),
        (50, 'Wand of Fear'),
        (55, 'Wand of Fire Balls'),
        (60, 'Wand of Illusion'),
        (65, 'Wand of Lightning Bolts'),
        (70, 'Wand of Magic Detection'),
        (75, 'Wand of Metal Detection'),
        (80, 'Wand of Negation'),
        (85, 'Wand of Paralysation'),
        (90, 'Wand of Polymorph'),
        (95, 'Wand of Secret Door Detection'),
        (100, 'Wand of Trap Detection'),
        ]
    weapon = [
        (2, '3-30 Arrows +1'),
        (12, '2-12 Arrows +1'),
        (18, '1-6 Arrows +2'),
        (27, 'Axe +1'),
        (30, 'Axe +2'),
        (33, 'Bow +1'),
        (43, '2-12 Crossbow Bolts +1'),
        (45, '3-30 Crossbow Bolts +1'),
        (52, '1-6 Crossbow Bolts +2'),
        (55, 'Dagger +1'),
        (56, 'Dagger +2, +3 vs Orcs, Goblins, and Kobolds'),
        (64, 'Mace +1'),
        (67, 'Mace +2'),
        (68, 'Mace +3'),
        (74, 'Sling +1'),
        (82, 'Spear +1'),
        (86, 'Spear +2'),
        (87, 'Spear +3'),
        (94, 'War Hammer +1'),
        (99, 'War Hammer +2'),
        (100, 'War Hammer +3, Dwarven Thrower'),
        ]
    # Sentient Swords. Special purpose swords are always sentient, Int 12 and Ego 12.
    _sword_special_chance = 5  # 1-in-20.
    _sword_sentient_chance = 30
    _sword_alignment = [(13, 'Lawful'), (18, 'Neutral'), (20, 'Chaotic')]
    # Languages, in addition to alignment's. 00 is two rolls, adding results.
    _sword_languages = [(50, 1), (70, 2), (85, 3), (95, 4), (99, 5)]
    # Duplicates are re-rolled.
    _sword_sensory = [
        (10, 'Detect evil or good'),
        (15, 'Detect gems'),
        (25, 'Detect magic'),
        (35, 'Detect metals'),
        (50, 'Detect shifting architecture'),
        (65, 'Detect slopes'),
        (75, 'Detect traps'),
        (85, 'Locate secret doors'),
        (95, 'See invisible objects'),
        (99, 'roll extraordinary'),
        (100, 'roll twice'),
        ]
    # Duplicates are re-rolled, except those in _sword_duplicates.
    _sword_extraordinary = [
        (10, 'Clairaudience'),
        (20, 'Clairvoyance'),
        (30, 'ESP'),
        (35, 'Extra damage'),
        (40, 'Flying'),
        (45, 'Healing'),
        (54, 'Illusion'),
        (59, 'Levitation'),
        (69, 'Telekinesis'),
        (79, 'Telepathy'),
        (88, 'Teleportation'),
        (97, 'X-ray vision'),
        (99, 'roll twice'),
        (100, 'roll thrice'),
        ]
    _sword_duplicates = ('Extra damage', 'Healing')
    # Lawful/Chaotic creatures become the other if the sword is that alignment.
    _sword_purposes = [
        (1, 'Arcane spell casters'),
        (2, 'Divine spell casters'),
        (3, 'Warriors'),
        (4, 'a specific type of monster (determine randomly)'),
        (5, 'Lawful creatures'),
        (6, 'Chaotic creatures'),
        ]
    _sword_purpose_powers = {
        'Lawful': 'Chaotic foes hit save vs spells or are paralysed',
        'Neutral': '+1 to all saving throws',
        'Chaotic': 'Lawful foes hit save vs spells or are turned to stone',
        }

    def armor_type(self, match):
        return table(self._armor_type)

    def charges(self, item):
        """Rods 1d10, staves 3d10, wands 2d10. Rod of Cancellation is single use; Healing and Snakes staves need none."""
        if 'Cancellation' in item:
            return ' [single use]'
        if 'Staff of Healing' in item or 'Staff of Snakes' in item:
            return ''
        if 'Wand' in item:
            return f' [{d10() + d10()} charges]'
        if 'Staff' in item:
            return f' [{d10() + d10() + d10()} charges]'
        if 'Rod' in item:
            return f' [{d10()} charges]'
        return ''

    def sword_extras(self, sword):
        if d100() <= self._sword_special_chance:
            return f'{sword}: {self._sentient_sword(special=True)}'
        if d100() <= self._sword_sentient_chance:
            return f'{sword}: {self._sentient_sword()}'
        return sword

    def _sentient_sword(self, special=False):
        """Alignment, Int, Ego, communication, languages, powers and special purpose of a sentient sword."""
        alignment = table(self._sword_alignment)
        intelligence = 12 if special else d6() + 6
        ego = 12 if special else d12()
        parts = [alignment, f'Int {intelligence}', f'Ego {ego}', 'speech' if intelligence >= 10 else 'empathy']
        if intelligence >= 10:
            languages = self._sword_language_count()
            parts.append(f'{languages} language{"" if languages == 1 else "s"} besides {alignment}')
        if intelligence >= 11:
            parts.append('reads magic')
        parts += self._sword_powers(min(3, intelligence - 6), 1 if intelligence == 12 else 0)
        if special:
            purpose = table(self._sword_purposes)
            if purpose == f'{alignment} creatures':
                purpose = 'Chaotic creatures' if alignment == 'Lawful' else 'Lawful creatures'
            parts.append(f'Slay {purpose} ({self._sword_purpose_powers[alignment]})')
        return ', '.join(parts)

    def _sword_powers(self, sensory, extraordinary):
        powers = []
        senses = {name for _, name in self._sword_sensory if not name.startswith('roll')}
        while sensory > 0 and not senses <= set(powers):
            result = table(self._sword_sensory)
            if result == 'roll twice':
                sensory += 1
            elif result == 'roll extraordinary':
                extraordinary += 1
                sensory -= 1
            elif result not in powers:
                powers.append(result)
                sensory -= 1
        while extraordinary > 0:
            result = table(self._sword_extraordinary)
            if result == 'roll twice':
                extraordinary += 1
            elif result == 'roll thrice':
                extraordinary += 2
            elif result not in powers or result in self._sword_duplicates:
                powers.append(result)
                extraordinary -= 1
        return [f'{power} x{count}' if count > 1 else power for power, count in collections.Counter(powers).items()]

    def _sword_language_count(self):
        roll = d100()
        if roll < 100:
            return table(self._sword_languages, roll)
        return self._sword_language_count() + self._sword_language_count()

    def _random_spells(self):
        """Ring of Spell Storing: 1d6 spells, 20% divine. Judgement: levels rolled as for scrolls."""
        caster = 'Cleric' if d100() <= 20 else 'Magic-user'
        return f'{caster} spells {self.spell_summary(caster, d6())}'

    def _spell_level(self, caster):
        """Divine spells top out at 5th, 96-00 is 5th."""
        levels = [(25, '1st'), (50, '2nd'), (70, '3rd'), (85, '4th'), (95, '5th'), (100, '6th')]
        return [*levels[:4], (100, '5th')] if caster == 'Cleric' else levels


# Custom OSE misc. items: these book items are replaced.
OSE_MISC_SWAPS = {'Crystal Ball': 'Scarab of Protection', 'Helm of Alignment Changing': 'Helm of Reading Languages and Magic'}


class ExpertRules(ExpertRawRules):
    """OSE Expert treasure and magic items with tweaks. Everything not listed here is as ExpertRawRules.

    Differences from the book (each is also commented where made, "Book:" is what the book has):
    - Gems give a 1% chance of a 5,000gp Diamond, and 1 in 10 gems may be magical or larger.
    - Treasure Type F's magic is rings, wands/staves/rods and misc. magic (equally likely) plus a potion and a scroll.
    - Armor, misc. items, rings, scrolls, swords, wands/staves/rods and weapons tables, see below.
    - Armor type odds, charges, and sentient sword chances and powers.
    """
    raw = False
    gems = Gems([20, 45, 75, 95, 99, 100])  # Book: [20, 45, 75, 95, 100], no Diamonds, no magical or larger gems.
    TREASURE_TYPES = {
        **ExpertRawRules.TREASURE_TYPES,
        # Book: 3 items of any category but Sword and Weapon.
        'f': (None,                     ('sp', 10, '2000-20000'),  ('ep', 20, '1000-8000'),   ('gp', 45, '1000-12000'),  ('pp', 30, '1000-3000'),   ('gems', 20, '2-24'),  ('jewelry', 10, '1-12'),  ('magic', 30, (entry_noweap, entry_noweap, entry_noweap, entry_potion, entry_scroll))),
        }
    # Book: Armor +1 rows roll the armor type, like +2 and +3.
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
        (54, '+4 Adamantite Plate'),  # Book: Cursed Armor -2, Shield +1.
        (56, 'AC9 Armor Cursed'),
        (62, '-2 Cursed Shield'),
        (65, 'Shield of Missile Attraction'),  # Book: Cursed Shield, AC 9.
        (85, '+1 Shield'),
        (95, '+2 Shield'),
        (99, '+3 Shield'),
        (100, 'Armor of Etherealness'),  # Added from Greyhawk. Book: +3 Shield.
        ]
    misc = [(roll, OSE_MISC_SWAPS.get(item, item)) for roll, item in ExpertRawRules.misc]
    ring = [
        (5, 'Animal Control'),
        (10, 'Human Control'),
        (16, 'Plant Control'),
        (26, 'Delusion'),
        (29, 'Djinn Summoning'),
        (39, 'Fire Resistance'),
        (50, 'Invisibility'),
        (55, 'Protection +2'),  # Book: Protection +1, 5' radius.
        (70, 'Protection +1'),
        (72, 'Regeneration'),
        (74, 'Spell Storing (<spells>)'),
        (80, 'Spell Turning'),
        (82, 'Telekinesis'),
        (88, 'Water Walking'),
        (94, 'Weakness'),
        (98, '1-4 Wishes'),  # Book: 95-96 Wishes 1-2, 97 Wishes 1-3, 98 Wishes 2-4.
        (100, 'X-Ray Vision'),
        ]
    scroll = [
        (15, '1 Spell'),
        (25, '2 Spells'),
        (31, '3 Spells'),
        (34, '5 Spells'),
        (35, 'Protection: Demons'),  # Book: 7 Spells.
        (40, 'trap'),  # Book: Curse. Trap uses Rules.scroll_trap.
        (50, 'Protection: Elementals'),
        (60, 'Protection: Lycanthropes'),
        (65, 'Protection: Magic'),
        (75, 'Protection: Undead'),
        ] + [row for row in ExpertRawRules.scroll if row[1].startswith('Treasure Map')]
    sword = [
        (2, '-1 Sword, Cursed'),
        (4, '-2 Sword, Cursed Berserker'),  # Added Berserker.
        (40, '+1 Sword'),
        # Book: 41-44 +1 Sword, replaced with these.
        (42, '+1 Sword of Cold: +3 vs. Fire Creatures'),
        (43, 'Dancing Sword'),
        (44, 'Vorpal Blade'),
        (50, '+1 Sword, +2 vs. Lycanthropes'),
        (56, '+1 Sword, +2 vs. Spell Users'),
        (60, '+1 Sword, +3 vs. Dragons'),
        (61, '+1 Sword, Dragon Slaying'),  # Book: 61 +1 Sword, +3 vs. Dragons.
        (66, '+1 Sword, +3 vs. Enchanted'),
        (71, '+1 Sword, +3 vs. Regenerating'),
        (76, '+1 Sword, +3 vs. Undead'),
        (77, '+1 Sword, Energy Drain'),
        (81, '+1 Sword, Flaming, +2 vs troll, flying, +3 vs plant, undead'),
        (89, '+1 Sword, Light'),
        (92, '+1 Sword, Locate Objects'),
        (93, '+1 Sword, 1-4 Wishes'),
        (96, '+2 Sword'),
        (98, '+2 Sword, Charm Humanoid'),  # Book: Charm Person.
        (100, '+3 Sword'),
        ]
    # Book: no class notes; Staff of Snakes, Wand of Fire Balls, Wand of Lightning Bolts.
    # (A)rcane, (D)ivine casters, (any) class. Book: rods any class, staves casters, wands arcane casters.
    wsr = [
        (8, 'Rod of Cancellation (any)'),
        (11, 'Staff of Commanding (DA)'),
        (21, 'Staff of Healing (D)'),
        (23, 'Staff of Power (A)'),
        (28, 'Snek Staff (D)'),
        (31, 'Staff of Striking (any)'),  # Book: casters only.
        (34, 'Staff of Withering (D)'),
        (35, 'Staff of Wizardry (A)'),
        (40, 'Wand of Cold'),
        (45, 'Wand of Enemy Detection'),
        (50, 'Wand of Fear'),
        (55, 'Wand of Fire'),
        (60, 'Wand of Illusion'),
        (65, 'Wand of Lightning'),
        (70, 'Wand of Magic Detection'),
        (75, 'Wand of Metal Detection (any)'),  # Book: arcane casters only.
        (80, 'Wand of Negation'),
        (85, 'Wand of Paralysation'),
        (90, 'Wand of Polymorph'),
        (95, 'Wand of Secret Door Detection'),
        (100, 'Wand of Trap Detection'),
        ]
    weapon = [
        (2, '3-30 +1 Arrows'),
        (12, '2-12 +1 Arrows'),
        (17, '1-6 +2 Arrows'),
        (18, 'Arrow of Slaying'),  # Book: 18 is 1-6 +2 Arrows.
        (27, 'Axe +1'),
        (30, 'Axe +2'),
        (33, 'Bow +1'),
        (43, '2-12 +1 Bolts'),
        (45, '3-30 +1 Bolts'),
        (51, '1-6 +2 Bolts'),
        (52, 'Bolts of Slaying'),  # Book: 52 is 1-6 +2 Bolts.
        (55, 'Dagger +1'),
        (56, 'Dagger +2, +3 vs Orcs, Goblins, and Kobolds'),
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
    # Book: Extra damage is x4 for 1d10 rounds (3/day), Healing is 1hp/round for 6 rounds (1/day).
    _sword_extraordinary = [
        (10, 'Clairaudience'),
        (20, 'Clairvoyance'),
        (30, 'ESP (3/day)'),
        (35, '3x damage for d6 rnds (1/day)'),
        (40, 'Flying (3/day)'),
        (45, 'Heal as spell (1/day)'),
        (54, 'Illusion (3/day)'),
        (59, 'Levitation'),
        (69, 'Telekinesis (3/day)'),
        (79, 'Telepathy (3/day)'),
        (88, 'Teleportation (3/day)'),
        (97, 'X-Ray Vision (3/day)'),
        (99, 'roll twice'),
        (100, 'roll thrice'),
        ]
    _sword_duplicates = ('3x damage for d6 rnds (1/day)', 'Heal as spell (1/day)')
    _sword_sensory = [
        (5, 'Know Depth & Direction'),  # Book: 01-10 Detect evil or good, see Sense Chaos/Law.
        (10, 'Detect Slopes & Shifting/Teleports'),  # Book: 36-50 shifting architecture, 51-65 slopes; added teleports.
        (15, 'Locate Gems 60 ft. (3/day)'),
        (25, 'Sense Magic 20 ft. (3/day)'),
        (35, 'Locate Named Metal 60 ft. (3/day)'),
        (50, 'Sense Chaos 20 ft.'),  # Book: Detect evil or good split in two, at slopes/shifting's odds.
        (65, 'Sense Law 20 ft.'),
        (75, 'See Traps (3/day)'),
        (85, 'See Secret Doors (3/day)'),
        (95, 'See Invisible'),
        (99, 'roll extraordinary'),
        (100, 'roll twice'),
        ]

    def armor_type(self, match):
        # Book: d8 1-2 Leather, 3-6 Chain, 7-8 Plate.
        return random.choice(['Leather', 'Leather', 'Chain', 'Chain', 'Chain', 'Plate', 'Plate'])

    def charges(self, item):
        # Book: rods 1d10, staves 3d10, wands 2d10; changed to d12s.
        if 'Cancellation' in item:
            return ' [single use]'
        lowered = item.lower()
        if 'wand' in lowered:
            return f' [{d12() + d12()} charges]'
        if 'staff' in lowered:
            return '' if 'Healing' in item or 'Snek' in item else f' [{d12() + d12() + d12()} charges]'
        if 'rod' in lowered:
            return f' [{d12()} charges]'
        return ''

    def sword_extras(self, sword):
        # Book: 1-in-20 of all swords have a special purpose; here 2-in-20 and only swords without other powers.
        if ',' not in sword and d100() <= 10:
            return f'{sword}: {self._sentient_sword(special=True)}'
        if d100() <= self._sword_sentient_chance:
            return f'{sword}: {self._sentient_sword()}'
        return sword


class BasicRawRules(ExpertRawRules):
    """OSE Basic (character levels 1-3) magic items, rules as written from OSE Rules Tome v1.4.

    Treasure types, gems, jewelry and swords' sentience are as ExpertRawRules.
    """
    name = 'Basic'
    item = [
        (10, 'Armor', entry_armor),
        (15, 'Misc', entry_misc),
        (40, 'Potion', entry_potion),
        (45, 'Ring', entry_ring),
        (50, 'W/S/R', entry_wsr),
        (70, 'Scroll', entry_scroll),
        (90, 'Sword', entry_sword),
        (100, 'Weapon', entry_weapon),
        ]
    armor = [
        (1, 'Armor +1'),
        (2, 'Armor +1, Shield +1'),
        (3, 'Cursed Armor, AC 9'),
        (4, 'Shield +1'),
        ]
    misc = [
        (1, 'Bag of Devouring'),
        (2, 'Bag of Holding'),
        (3, 'Broom of Flying'),
        (4, 'Crystal Ball'),
        (5, 'Elven Cloak and Boots'),
        (6, 'Gauntlets of Ogre Power'),
        (7, 'Helm of Alignment Changing'),
        (8, 'Helm of Telepathy'),
        (9, "Medallion of ESP 30'"),
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
        (1, 'Control Animals'),
        (2, 'Fire Resistance'),
        (3, 'Invisibility'),
        (4, 'Protection +1'),
        (5, 'Water Walking'),
        (6, 'Weakness'),
        ]
    scroll = [
        (1, '1 Spell'),
        (2, '2 Spells'),
        (3, '3 Spells'),
        (4, 'Curse'),
        (5, 'Protection: Lycanthropes'),
        (6, 'Protection: Undead'),
        (7, 'Treasure Map I: 1 magic item'),
        (8, 'Treasure Map VIII: Hoard worth 1d4 × 1,000gp'),
        ]
    sword = [
        (1, 'Sword -1, Cursed'),
        (2, 'Sword +1'),
        (3, 'Sword +1, +2 vs Lycanthropes'),
        (4, 'Sword +1, +2 vs Spell Users'),
        (5, 'Sword +1, +3 vs Dragons'),
        (6, 'Sword +1, +3 vs Undead'),
        (7, 'Sword +1, Light'),
        (8, 'Sword +2'),
        ]
    wsr = [
        (1, 'Rod of Cancellation'),
        (2, 'Staff of Healing'),
        (3, 'Staff of Snakes'),
        (4, 'Wand of Enemy Detection'),
        (5, 'Wand of Magic Detection'),
        (6, 'Wand of Paralysation'),
        ]
    weapon = [
        (1, '10 Arrows +1'),
        (2, 'Axe +1'),
        (3, 'Dagger +1'),
        (4, 'Mace +1'),
        ]

    def _spell_level(self, caster):
        return [(3, '1st'), (5, '2nd'), (6, '3rd')]


class BasicRules(ExpertRules):
    """OSE Basic (character levels 1-3) magic items with tweaks. Everything else is as ExpertRules.

    Differences from the book (each is also commented where made): misc. items, scrolls, swords and weapons tables,
    and the ExpertRules differences (gems, Treasure Type F, armor type odds, charges and sentient swords).
    """
    name = 'Basic'
    item = BasicRawRules.item
    armor = BasicRawRules.armor
    potion = BasicRawRules.potion
    ring = BasicRawRules.ring
    misc = [(roll, OSE_MISC_SWAPS.get(item, item)) for roll, item in BasicRawRules.misc]
    # Book: Curse. Trap uses Rules.scroll_trap.
    scroll = [(roll, 'trap' if text == 'Curse' else text) for roll, text in BasicRawRules.scroll]
    # Book: d8, 1 -1 Cursed, 2 +1, 3 +2 vs Lycanthropes, 4 +2 vs Spell Users, 5 +3 vs Dragons, 6 +3 vs Undead,
    # 7 +1 Light, 8 +2. Changed to d14: much increased chances of +1 and Light, double chance of cursed.
    sword = [
        (2, '-1 Sword, Cursed'),
        (3, '+1 Sword, +2 vs. Lycanthropes'),
        (4, '+1 Sword, +2 vs. Spell Users'),
        (5, '+1 Sword, +3 vs. Dragons'),
        (7, '+1 Sword, +3 vs. Undead'),
        (8, '+2 Sword'),
        (10, '+1 Sword, Light'),
        (14, '+1 Sword'),
        ]
    # (A)rcane, (D)ivine casters. Book: Staff of Snakes.
    wsr = [
        (1, 'Rod of Cancellation'),
        (2, 'Staff of Healing (D)'),
        (3, 'Snek Staff (D)'),
        (4, 'Wand of Enemy Detection (A)'),
        (5, 'Wand of Magic Detection (A)'),
        (6, 'Wand of Paralysation (A)'),
        ]
    weapon = [
        (1, '10 +1 Arrows'),
        (2, 'Axe +1'),
        (3, 'Dagger +1'),
        (4, 'Mace +1'),
        (5, 'Spear +1'),  # Added Spear. Book: d4.
        ]

    def _spell_level(self, caster):
        return BasicRawRules._spell_level(self, caster)  # noqa: SLF001


class AdvancedRawRules(ExpertRawRules):
    """OSE Advanced Fantasy treasure and magic items, rules as written in Advanced Fantasy Referee's Tome v1-3.

    The Referee's Tome has the Advanced Treasures v1-1 items merged into the classic tables, so unlike Basic and
    Expert there is no tweaked ruleset. Uses the Expert (character level 4+) column of the magic item type table;
    Advanced has no level 1-3 column. Treasure types, gems, jewelry, armor, potions, rings, scrolls and sentient
    swords are as ExpertRawRules, the Referee's Tome has identical tables. Where the book is ambiguous the choice
    is commented "Judgement".
    """
    name = 'Advanced'
    # Judgement: book says "chosen randomly (e.g. red, white)", the ten non-multichromatic dragons are equally likely.
    _random_dragon = [
        (1, 'Black'), (2, 'Blue'), (3, 'Brass'), (4, 'Bronze'), (5, 'Copper'),
        (6, 'Gold'), (7, 'Green'), (8, 'Red'), (9, 'Silver'), (10, 'White'),
        ]
    # d20.
    _random_feather_token = [(4, 'Anchor'), (7, 'Bird'), (10, 'Fan'), (13, 'Swan boat'), (18, 'Tree'), (20, 'Whip')]
    # d20.
    _random_figurine = [
        (3, 'Ebony fly'),
        (6, 'Pair of golden lions'),
        (8, 'Trio of ivory goats (travelling, travail and terror)'),
        (11, 'Marble elephant'),
        (13, 'Obsidian steed'),
        (17, 'Onyx dog'),
        (20, 'Serpentine owl'),
        ]
    # d%. Each blast summons the number of berserkers, of the Hit Dice, once per week.
    _random_valhalla = [
        (40, 'Silver: 2d4+2 berserkers of 2HD, any class'),
        (75, 'Brass: 2d4+1 berserkers of 3HD, clerics, fighters, thieves'),
        (90, 'Bronze: 2d4 berserkers of 4HD, clerics, fighters'),
        (100, 'Iron: 1d4+1 berserkers of 5HD, fighters'),
        ]
    # d20.
    _random_necklace = [
        (4, '1 × 5d6, 2 × 3d6'),
        (8, '1 × 6d6, 2 × 4d6, 2 × 2d6'),
        (12, '1 × 7d6, 2 × 5d6, 4 × 3d6'),
        (16, '1 × 8d6, 2 × 6d6, 2 × 4d6, 4 × 2d6'),
        (18, '1 × 9d6, 2 × 8d6, 2 × 5d6, 2 × 3d6'),
        (19, '1 × 10d6, 2 × 8d6, 2 × 6d6, 4 × 4d6'),
        (20, '1 × 11d6, 2 × 9d6, 2 × 7d6, 2 × 5d6, 2 × 3d6'),
        ]
    # d20, maximum spell level.
    _random_pearl = [(5, '1st'), (10, '2nd'), (14, '3rd'), (17, '4th'), (19, '5th'), (20, '6th')]
    # d10.
    _random_periapt = [
        (4, '10% vs poison with no save, +1 to poison saves'),
        (7, '20% vs poison with no save, +2 to poison saves'),
        (9, '30% vs poison with no save, +3 to poison saves'),
        (10, '40% vs poison with no save, +4 to poison saves'),
        ]
    # d20, 15+ is burned out.
    _ioun_stone = [
        (1, 'Pale blue rhomboid: +1 STR (max 18)'),
        (2, 'Scarlet and blue sphere: +1 INT (max 18)'),
        (3, 'Incandescent blue sphere: +1 WIS (max 18)'),
        (4, 'Deep red sphere: +1 DEX (max 18)'),
        (5, 'Pink rhomboid: +1 CON (max 18)'),
        (6, 'Pink and green sphere: +1 CHA (max 18)'),
        (7, 'Pale green prism: +1 experience level'),
        (8, 'Clear spindle: sustains without food or water'),
        (9, 'Iridescent spindle: sustains without air'),
        (10, 'Pearly white spindle: heals 1hp per turn'),
        (11, 'Pale lavender ellipsoid: absorbs spells of 3rd level or lower (1d3 × 10 levels)'),
        (12, 'Lavender and green ellipsoid: absorbs spells of 5th level or lower (2d3 × 10 levels)'),
        (13, 'Vibrant purple prism: stores 2d4 levels of spells'),
        (14, 'Dusty rose prism: +1 to AC and saves'),
        (20, 'Dull grey ellipsoid: burned out'),
        ]
    # Miscellaneous items: roll 1d4 for Table I-IV, then d%. The d4 is rolled as d100 (25 each) like Greyhawk's tables.
    misc_i = [
        (2, "Alchemist's Beaker"),
        (3, 'Amulet of Protection Against Possession'),
        (6, 'Amulet of Protection Against Scrying'),
        (8, 'Apparatus of the Crab'),
        (11, 'Arrow of Location'),
        (12, 'Bag of Devouring'),
        (17, 'Bag of Holding'),
        (18, 'Bag of Transformation'),
        (19, 'Book of Foul Corruption'),
        (20, 'Book of Infinite Spells'),
        (21, 'Book of Sublime Holiness'),
        (22, 'Boots of Dancing'),
        (27, 'Boots of Levitation'),
        (31, 'Boots of Speed'),
        (35, 'Boots of Travelling and Leaping'),
        (50, 'Bracers of Armour'),
        (52, 'Bracers of Defencelessness'),
        (59, 'Brooch of Shielding'),
        (64, 'Broom of Flying'),
        (70, 'Candle of Invocation'),
        (72, 'Chime of Opening [4-80 soundings]'),
        (73, 'Chime of Ravening'),
        (85, 'Cloak of Defence'),
        (95, 'Cloak of Flight'),
        (97, 'Cloak of Poison'),
        (100, 'Cloak of the Manta Ray'),
        ]
    misc_ii = [
        (5, 'Crystal Ball'),
        (7, 'Crystal Ball with Clairaudience'),
        (8, 'Crystal Ball with ESP'),
        (9, 'Crystal Hypnosis Ball'),
        (11, 'Cube of Force'),
        (13, 'Cube of Frost Resistance'),
        (16, 'Decanter of Endless Water'),
        (20, 'Deck of Many Things'),
        (24, 'Displacer Cloak'),
        (26, 'Drums of Panic'),
        (27, 'Drums of Thunder'),
        (33, 'Dust of Appearance'),
        (39, 'Dust of Disappearance'),
        (40, 'Dust of Sneezing and Choking'),
        (41, 'Efreeti Bottle'),
        (43, 'Elemental Summoning Device: Air'),
        (45, 'Elemental Summoning Device: Earth'),
        (47, 'Elemental Summoning Device: Fire'),
        (49, 'Elemental Summoning Device: Water'),
        (59, 'Elven Cloak and Boots'),
        (60, 'Eyes of Charming'),
        (62, 'Eyes of Minuscule Sight'),
        (63, 'Eyes of Petrification'),
        (65, 'Eyes of the Eagle'),
        (80, 'Feather Token (<feather_token>)'),
        (95, 'Figurine of Wondrous Power (<figurine>)'),
        (97, 'Flying Carpet'),
        (98, 'Folding Boat'),
        (100, 'Gauntlets of Ogre Power'),
        ]
    misc_iii = [
        (1, 'Gem of Brightness [50 charges]'),
        (2, 'Gem of Monster Attraction'),
        (3, 'Gem of Pristine Faceting [10-100 charges]'),
        (4, 'Gem of Seeing'),
        (5, 'Girdle of Giant Strength'),
        (7, 'Gloves of Dexterity'),
        (10, 'Gloves of Swimming and Climbing'),
        (12, 'Helm of Alignment Changing'),
        (17, 'Helm of Reading Languages and Magic'),
        (19, 'Helm of Telepathy'),
        (20, 'Helm of Teleportation'),
        (21, 'Horn of Blasting'),
        (22, 'Horn of Cave-Ins'),
        (24, 'Horn of Frothing'),
        (28, 'Horn of the Tritons'),
        (35, 'Horn of Valhalla (<valhalla>)'),
        (37, 'Horseshoes of a Zephyr'),
        (40, 'Horseshoes of Speed'),
        (45, 'Incense of Meditation (2-8 blocks)'),
        (46, 'Incense of Obsession (2-8 blocks)'),
        (48, 'Instant Fortress'),
        (49, 'Ioun Stones (<ioun>)'),
        (51, 'Iron Flask'),
        (53, 'Jug of Endless Liquids'),
        (54, 'Libram of Arcane Power'),
        (56, 'Loadstone'),
        (58, 'Luckstone'),
        (59, 'Lyre of Building'),
        (61, 'Marvellous Pigments'),
        (64, "Medallion of ESP 30'"),
        (66, "Medallion of ESP 90'"),
        (68, 'Medallion of Thought Projection'),
        (69, 'Mirror of Life Trapping'),
        (70, 'Mirror of Mental Prowess'),
        (71, 'Mirror of Opposition'),
        (74, 'Necklace of Adaptation'),
        (78, 'Necklace of Fireballs (<necklace>)'),
        (80, 'Necklace of Strangulation'),
        (84, 'Net of Aquatic Snaring'),
        (87, 'Net of Snaring'),
        (90, 'Oil of Insubstantiality'),
        (93, 'Oil of Slipperiness'),
        (95, 'Pearl of Power (maximum <pearl> level)'),
        (97, 'Pearl of Wisdom'),
        (100, 'Periapt of Foul Rotting'),
        ]
    misc_iv = [
        (2, 'Periapt of Health'),
        (9, 'Periapt of Proof Against Poison (<periapt>)'),
        (13, 'Periapt of Wound Closure'),
        (15, 'Phylactery of Betrayal'),
        (21, 'Phylactery of Faithfulness'),
        (25, 'Phylactery of Longevity'),
        (33, 'Pipes of the Sewers'),
        (34, 'Portable Hole'),
        (36, 'Purse of Plentiful Coin'),
        (44, 'Restorative Ointment'),
        (51, 'Robe of Blending'),
        (52, 'Robe of Eyes'),
        (53, 'Robe of Powerlessness'),
        (54, 'Robe of Scintillating Colours'),
        (55, 'Robe of the Archmagi'),
        (63, 'Robe of Useful Items'),
        (69, 'Rope of Climbing'),
        (73, 'Rope of Entanglement'),
        (75, 'Rope of Strangulation'),
        (76, 'Rug of Suffocation'),
        (77, 'Saw of Felling'),
        (79, 'Scarab of Chaos [9-16 charges]'),
        (80, 'Scarab of Death'),
        (86, 'Scarab of Protection'),
        (89, 'Scarab of Rage [19-24 charges]'),
        (90, 'Spade of Mighty Digging'),
        (91, 'Sphere of Annihilation'),
        (94, 'Sweet Water'),
        (95, 'Talisman of the Sphere'),
        (97, 'Vacuous Grimoire'),
        (100, 'Well of Many Worlds'),
        ]
    misc = [(25, misc_i), (50, misc_ii), (75, misc_iii), (100, misc_iv)]
    sword = [
        (3, 'Short Sword +2, Quickness'),
        (6, 'Sword -1, Berserker (Cursed)'),
        (9, 'Sword -1, Cursed'),
        (12, 'Sword -2, Cursed'),
        (28, 'Sword +1'),
        (31, 'Sword +1, +2 vs Lycanthropes'),
        (34, 'Sword +1, +2 vs Spell Users'),
        (37, 'Sword +1, +3 vs Dragons'),
        (40, 'Sword +1, +3 vs Enchanted Creatures'),
        (43, 'Sword +1, +3 vs Regenerating Creatures'),
        (46, 'Sword +1, +3 vs Reptiles'),
        (49, 'Sword +1, +3 vs Shape Changers'),
        (52, 'Sword +1, +3 vs Undead'),
        (55, 'Sword +1, Dragon Slayer (<dragon> Dragons)'),
        (56, 'Sword +1, Energy Drain (5-8 levels)'),
        (59, 'Sword +1, Flaming'),
        (61, 'Sword +1, Frost Brand'),
        (64, 'Sword +1, Giant Slayer'),
        (69, 'Sword +1, Light'),
        (71, 'Sword +1, Locate Objects'),
        (72, 'Sword +1, Luck Blade (1-4 wishes)'),
        (73, 'Sword +1, Sharpness'),
        (78, 'Sword +1, Sun Blade'),
        (79, 'Sword +1, Wishes (1-4)'),
        (80, 'Sword +1, Wounding'),
        (85, 'Sword +2'),
        (87, 'Sword +2, Charm Person'),
        (88, 'Sword +2, Dancing'),
        (89, 'Sword +2, Nine Lives Stealer'),
        (94, 'Sword +2, Venger'),
        (95, 'Sword +2, Vorpal'),
        (98, 'Sword +3'),
        (99, 'Sword +3, Defender'),
        (100, 'Sword +3, Holy Avenger'),
        ]
    # d6, for swords not of a specific type.
    _sword_type = [(2, 'Short Sword'), (5, 'Sword'), (6, 'Two-handed Sword')]
    wsr = [
        (2, 'Immovable Rod'),
        (5, 'Rod of Absorption'),
        (11, 'Rod of Cancellation'),
        (12, 'Rod of Captivation'),
        (14, 'Rod of Lordly Might'),
        (15, 'Rod of Parrying'),
        (16, 'Rod of Resurrection'),
        (17, 'Rod of Striking'),
        (18, 'Staff of Commanding'),
        (20, 'Staff of Dispelling'),
        (26, 'Staff of Healing'),
        (27, 'Staff of Power'),
        (30, 'Staff of Snakes'),
        (33, 'Staff of Striking'),
        (36, 'Staff of Swarming Insects'),
        (38, 'Staff of the Healer'),
        (40, 'Staff of Withering'),
        (41, 'Staff of Wizardry'),
        (44, 'Staff of the Woodlands'),
        (47, 'Wand of Cold'),
        (51, 'Wand of Enemy Detection'),
        (54, 'Wand of Fear'),
        (57, 'Wand of Fire Balls'),
        (61, 'Wand of Illusion'),
        (64, 'Wand of Lightning Bolts'),
        (69, 'Wand of Magic Detection'),
        (74, 'Wand of Magic Missiles'),
        (79, 'Wand of Metal Detection'),
        (84, 'Wand of Negation'),
        (87, 'Wand of Paralysation'),
        (90, 'Wand of Polymorph'),
        (94, 'Wand of Radiance'),
        (97, 'Wand of Secret Door Detection'),
        (98, 'Wand of Summoning'),
        (100, 'Wand of Trap Detection'),
        ]
    weapon = [
        (1, 'Arrow +1, Slaying'),
        (10, 'Arrows +1 (2-12 arrows)'),
        (12, 'Arrows +1 (3-30 arrows)'),
        (15, 'Arrows +2 (1-6 arrows)'),
        (19, 'Axe +1'),
        (21, 'Axe +2'),
        (24, 'Bow +1'),
        (25, 'Crossbow +1, Distance'),
        (26, 'Crossbow +1, Speed'),
        (27, 'Crossbow +2, Accuracy'),
        (29, 'Crossbow Bolts +1 (2-12 bolts)'),
        (31, 'Crossbow Bolts +1 (3-30 bolts)'),
        (36, 'Crossbow Bolts +2 (1-6 bolts)'),
        (39, 'Dagger +1'),
        (40, 'Dagger +1, Buckle'),
        (41, 'Dagger +1, Throwing'),
        (42, 'Dagger +1, Venomous'),
        (45, 'Dagger +2, +3 vs Orcs, Goblins, and Kobolds'),
        (46, 'Dagger +2, Biter'),
        (50, 'Javelin of Lightning (2-5 javelins)'),
        (54, 'Javelin of Seeking (2-8 javelins)'),
        (58, 'Mace +1'),
        (59, 'Mace +1, Disrupting'),
        (62, 'Mace +2'),
        (63, 'Mace +3'),
        (68, 'Sling +1'),
        (69, 'Sling Bullet +1, Impact (1-4 bullets)'),
        (71, 'Spear -1, Backbiter (Cursed)'),
        (75, 'Spear +1'),
        (77, 'Spear +2'),
        (78, 'Spear +3'),
        (80, 'Staff +1, Growing'),
        (82, 'Trident -2, Yearning (Cursed)'),
        (87, 'Trident +1, Fish Command (17-20 charges)'),
        (89, 'Trident +1, Submission'),
        (93, 'Trident +2, Warning'),
        (96, 'War Hammer +1'),
        (98, 'War Hammer +2'),
        (99, 'War Hammer +3, Dwarven Thrower'),
        (100, 'War Hammer +3, Thunderbolts'),
        ]

    def _random_ioun(self):
        """1d10 stones, a duplicate of a type in the cache is burned out."""
        stones = []
        for _ in range(d10()):
            stone = table(self._ioun_stone)
            stones.append(table(self._ioun_stone, 20) if stone in stones else stone)
        counts = collections.Counter(stones)
        return f'{len(stones)} stones; ' + '; '.join(f'{count} × {stone}' if count > 1 else stone for stone, count in counts.items())

    def charges(self, item):
        """Immovable Rod and Rod of Parrying use no charges, Rod of Absorption has 50, otherwise as Expert."""
        if 'Immovable' in item or 'Parrying' in item:
            return ''
        if 'Absorption' in item:
            return ' [50 charges]'
        return super().charges(item)

    def sword_extras(self, sword):
        """Unless the sword is a specific type, roll its type; sentience is as Expert."""
        if sword.startswith('Sword'):
            sword = f'{table(self._sword_type)}{sword.removeprefix("Sword")}'
        return super().sword_extras(sword)


# --raw: each ruleset's rules as written. OD&D and Advanced are only as written.
RAW_RULES = {BasicRules: BasicRawRules, ExpertRules: ExpertRawRules, AdvancedRawRules: AdvancedRawRules, GreyhawkRules: GreyhawkRawRules, OddRules: OddRules}


class AliasedGroup(click.Group):
    """Also accepts 'gems' for the 'gem' command."""

    def get_command(self, ctx, cmd_name):
        command = super().get_command(ctx, cmd_name)
        if command is None and cmd_name == 'gems':
            return super().get_command(ctx, 'gem')
        return command


@click.group(cls=AliasedGroup)
@click.option('-b', '--basic', default=False, is_flag=True, help='Use OSE level 1-3 tables, tweaked.')
@click.option('-x', '--expert', default=False, is_flag=True, help='Use OSE Expert tables, tweaked (default).')
@click.option('-a', '--advanced-OSE', 'advanced', default=False, is_flag=True, help='Use OSE Advanced Fantasy tables, always as written.')
@click.option('-g', '--greyhawk', default=False, is_flag=True, help='Use OD&D + Greyhawk tables, tweaked.')
@click.option('-o', '--odd', default=False, is_flag=True, help='Use OD&D tables, always as written.')
@click.option('-r', '--raw', default=False, is_flag=True, help='Use rules as written without tweaks.')
@click.option('-d', '--roll', default=None, type=int, help='Use this d100 roll.')
@click.pass_context
def cli(ctx, basic, expert, advanced, greyhawk, odd, raw, roll):
    """Roll up treasure hoards and items. OSE Expert by default.

    Rulesets are tweaked unless -r/--raw: -rb, -rx, -rg are rules as written. -a and -o are always as written.
    """
    chosen = [rules_class for flag, rules_class in (
        (basic, BasicRules), (expert, ExpertRules), (advanced, AdvancedRawRules), (greyhawk, GreyhawkRules), (odd, OddRules),
        ) if flag]
    if len(chosen) > 1:
        raise click.UsageError('Choose only one of -b, -x, -a, -g, -o.')
    rules_class = chosen[0] if chosen else ExpertRules
    if raw:
        rules_class = RAW_RULES[rules_class]
    rules = rules_class()
    click.echo(f'Using {rules.title}.')
    ctx.obj['rules'] = rules
    ctx.obj['roll'] = roll


def _add_roll_item_cli_commands():
    def _add(name, roll_function, description):
        @cli.command(name, help=f'Roll up {description}')
        @click.argument('count', default=1, type=int)
        @click.pass_context
        def command(ctx, count):
            rules = ctx.obj['rules']
            try:
                rolled = reduce_groups((1, 0, roll_function(rules, ctx.obj['roll'])) for _ in range(count))
                click.echo('\n'.join(f'{quantity} x {thing}' for quantity, _, thing in rolled))
            except RollOutOfRange as error:
                raise click.UsageError(str(error)) from error
    # CLI subcommand name: (function to roll one, what the help says it rolls up).
    ROLL_COMMANDS = {
        'item': (entry_item, 'magic item.'),
        'sword': (entry_sword, 'magic swords.'),
        'armor': (entry_armor, 'magic armors.'),
        'weapon': (entry_weapon, 'magic weapons.'),
        'potion': (entry_potion, 'potions.'),
        'scroll': (entry_scroll, 'magic scrolls.'),
        'ring': (entry_ring, 'magic rings.'),
        'wsr': (entry_wsr, 'wand, staff, rod.'),
        'misc': (entry_misc, 'miscellaneous magic items.'),
        'map': (entry_odd_map, 'treasure and magic maps.'),
        }
    for name, (func, description) in ROLL_COMMANDS.items():
        _add(name, func, description)
_add_roll_item_cli_commands()


@cli.command()
@click.argument('count', default=1)
@click.argument('group', default=1)
@click.pass_context
def gem(ctx, count, group):
    """Roll up gems."""
    click.echo('\n'.join(ctx.obj['rules'].gems.lines(count, group)))


@cli.command()
@click.argument('count', default=1)
@click.argument('group', default=1)
@click.pass_context
def jewelry(ctx, count, group):
    """Roll up jewelry."""
    click.echo('\n'.join(ctx.obj['rules'].jewelries.lines(count, group)))


@cli.command('type')
@click.option('-s', '--something', default=False, is_flag=True, help='Re-roll until something.')
@click.argument('code')
@click.pass_context
def treasure_type(ctx, code, something):
    """Roll up treasure type."""
    rules = ctx.obj['rules']
    type_code = code.lower()
    if type_code not in rules.TREASURE_TYPES:
        raise click.BadParameter(f'{code} is not one of {", ".join(sorted(rules.TREASURE_TYPES))} for {rules.title}.')
    results = list(rules.treasure_type(type_code))
    while something and not results:
        results = list(rules.treasure_type(type_code))
    click.echo('\n'.join(results) or 'Nothing')


if __name__ == '__main__':
    cli(obj={})
