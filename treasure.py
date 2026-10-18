#!/usr/bin/env python3
"""Random treasure generation for OSE, OD&D or AD&D 1e.

Rulesets (command line flag, rules name):
    -b   Basic              OSE levels 1-3 rules with tweaks.
    -x   Expert (default)   OSE Expert rules with tweaks.
    -a   Advanced           OSE Advanced rules as written.
    -g   OD&D + Greyhawk    OD&D Vol 2 + Greyhawk supplement with tweaks.
    -o   OD&D               OD&D Vol 2 (Monsters & Treasure), rules as written.
    -d   AD&D 1e            1e Dungeon Masters Guide treasure and Monster Manual treasure types, rules as written.
    -r/--raw                rules as written
    -rb  Basic rules as written
    -rx  Expert rules as written
    -rg  OD&D + Greyhawk rules as written
    -ro  OD&D rules as written, the same as -o.
    -ra  Advanced rules as written, the same as -a.
    -rd  AD&D 1e rules as written, the same as -d.

Version: 10/17/2026
Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: https://github.com/njharman/rpg
"""
import collections
import functools
import itertools
import operator
import random
import re

import click
from die import d4, d6, d8, d10, d12, d20, d100

NO_WEAPONS = ('Sword', 'Misc. Weapon')
# Order of kinds of thing in a listing, see present.
KINDS = ('money', 'gem', 'jewelry', 'potion', 'scroll', 'weapon', 'sword', 'armor', 'ring', 'wsr', 'misc', 'map')
COINS = ('cp', 'sp', 'ep', 'gp', 'pp')
NUMBER_WORDS = ('Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten')


class Item(str):
    """Text of a rolled thing that remembers its kind (one of KINDS), for present."""

    def __new__(cls, text, kind):
        item = super().__new__(cls, text)
        item.kind = kind
        return item


def kinded(kind):
    """Decorate a roll function so its text is an Item of kind, unless it already is one (e.g. a map on a scroll table)."""
    def decorate(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result if isinstance(result, Item) else Item(result, kind)
        return wrapper
    return decorate


def _flatten(things):
    for thing in things:
        if isinstance(thing, str):
            yield thing
        else:
            yield from _flatten(thing)


def present(things):
    """List of lines for things (text, Items or lists of them): like things combined, sorted by kind and then alphabetically.

    Numbered things ('2 Arrows +1', '300gp') of the same kind and name are added together. Potions are grouped ('Two Potions of
    Healing'). Anything else is on its own line, with no count. Coins sort by value.
    """
    rows = {}  # key: [kind, name, count, style, text]
    unique = itertools.count()
    for thing in _flatten(things):
        kind = getattr(thing, 'kind', None) or ('money' if re.fullmatch(r'[\d,]+[cegps]p', thing) else 'misc')
        if kind == 'money' and (match := re.fullmatch(r'([\d,]+)([cegps]p)', thing)):
            key, name, count, style = (kind, match.group(2)), match.group(2), match.group(1), 'coin'
        elif kind == 'potion':
            key, name, count, style = (kind, thing), thing, '1', 'potion'
        elif kind not in ('gem', 'jewelry') and (match := re.fullmatch(r'([\d,]+) (.+)', thing, re.DOTALL)):
            key, name, count, style = (kind, match.group(2)), match.group(2), match.group(1), 'counted'
        else:
            key, name, count, style = (kind, next(unique)), thing, '1', 'single'
        if key in rows:
            rows[key][2] += int(count.replace(',', ''))
        else:
            rows[key] = [kind, name, int(count.replace(',', '')), style]

    def sort_key(row):
        kind, name, _, style = row
        return KINDS.index(kind), COINS.index(name) if style == 'coin' else 0, name.lower()

    def line(row):
        _, name, count, style = row
        match style:
            case 'coin':
                return f'{count:,}{name}'
            case 'counted':
                return f'{count:,} {name}'
            case 'potion' if count > 1:
                word, _, rest = name.partition(' ')
                return f'{NUMBER_WORDS[count] if count < len(NUMBER_WORDS) else count} {word}s {rest}'
        return name
    return [line(row) for row in sorted(rows.values(), key=sort_key)]


def reduce_groups(things):
    """Combine (count, value, thing) with the same value and thing, summing the counts."""
    ordered = sorted(things, key=operator.itemgetter(1, 2))
    for (value, thing), group in itertools.groupby(ordered, key=operator.itemgetter(1, 2)):
        yield sum(count for count, _, _ in group), value, thing


def price(value, per_gp=1):
    """'1,200gp'; the smallest whole coin that holds value, '130sp', '11cp'; nothing for a magical (worth 0) piece.

    value: whole units, per_gp of them to the gp. Below a gp the units are copper, 10cp to the sp.
    """
    if not value:
        return ''
    if value % per_gp == 0:
        return f'{value // per_gp:,}gp'
    if value % 10 == 0:
        return f'{value // 10:,}sp'
    return f'{value:,}cp'


def indent(text):
    """Indent every line of text one space, so nesting shows however deep."""
    return '\n'.join(f' {line}' for line in text.split('\n'))


def format_map(things, note=''):
    """Treasure map text: only coins are one line, otherwise every thing is on its own indented line.

    things: the text of each thing the map leads to, gems and jewelry are their (multi-line) lines() text.
    note: where it leads, or other remark, in parentheses.
    """
    where = f' ({note})' if note else ''
    things = present(things)
    if all(re.fullmatch(r'[\d,]+[cegps]p', thing) for thing in things):
        return Item(f'Treasure map to {", ".join(things)}{where}', 'map')
    return Item('\n'.join([f'Treasure map{where} to:', *(indent(thing) for thing in things)]), 'map')


def language_trait(communication, alignment, languages):
    """'speaks Lawful + 2 others'; the sword's 'speech' becomes this, other communication ('telepathy') precedes it."""
    speaks = f'speaks {alignment} + {languages} other{"" if languages == 1 else "s"}'
    if 'speech' in communication:
        return communication.replace('speech', speaks)
    return f'{communication}, {speaks}'


def format_sword(sword, traits, lines):
    """'Longsword +3 - Neutral, Int 12, Ego 4, semi-empathy' then one indented line per ability."""
    return '\n'.join([f'{sword} - {", ".join(traits)}', *(f' {line}' for line in lines)])


def replace_quantity(text):
    """Roll every N-M (N dice, max M) in text; return (first roll, text with the rolls in place).

    N000-M000 is in thousands, e.g. 1000-6000 is 1d6 x 1000. N-MxS is multiplied by S, e.g. 5-20x100 is 5d4 x 100.
    A range that is not N dice (2-5) is uniform.
    """
    rolls = []

    def roll_range(match):
        dice, maximum = int(match.group(1)), int(match.group(2))
        scale = int(match.group(3) or 1)
        if scale == 1 and dice and dice % 1000 == 0 and maximum % 1000 == 0:
            dice, maximum, scale = dice // 1000, maximum // 1000, 1000
        if dice and maximum % dice == 0:
            value = sum(random.randint(1, maximum // dice) for _ in range(dice))
        else:
            value = random.randint(dice, maximum)
        rolls.append(value * scale)
        return f'{value * scale:,}'
    result = re.sub(r'(\d+)-(\d+)(?:x(\d+))?', roll_range, text)
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
    """OD&D treasure map #number: list of text for each thing it leads to."""
    return [rules.monetary(kind, amount) for kind, amount in MAP_TREASURE[number - 1]]


def _map_magic(rules, number):
    """OD&D magic map #number: list of text for each item it leads to."""
    count, skip, forced = MAP_MAGIC[number - 1]
    return [_map_item(entry_item, rules, skip=skip) for _ in range(count)] + [_map_item(roll_function, rules) for roll_function in forced]


def _ose_map(rules, text):
    """OSE scroll 'Treasure Map V: ...': roll everything it leads to."""
    things = []
    for kind, amount in OSE_MAPS[text.split()[2].rstrip(':')]:
        match kind:
            case 'magic':
                count, skip = amount
                things += [_map_item(entry_item, rules, skip=skip) for _ in range(count)]
            case 'potion':
                things.append(_map_item(entry_potion, rules))
            case 'scroll':
                things.append(_map_item(entry_scroll, rules))
            case _:
                things.append(rules.monetary(kind, amount))
    return format_map(things)


def _map_item(roll_function, *args, **kwargs):
    """A map's magic is never another treasure map."""
    item = roll_function(*args, **kwargs)
    while item.lower().startswith('treasure map'):
        item = roll_function(*args, **kwargs)
    return item


def entry_2d4_potions(rules, roll=None):
    return [entry_potion(rules, roll) for _ in range(random.randint(1, 4) + random.randint(1, 4))]


def entry_d4_scrolls(rules, roll=None):
    return [entry_scroll(rules, roll) for _ in range(random.randint(1, 4))]


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


@kinded('armor')
def entry_armor(rules, roll=None):
    return re.sub(r'(Armor)', rules.armor_type, _roll_table(rules, 'armor', roll))


@kinded('misc')
def entry_misc(rules, roll=None):
    result = table(rules.misc, roll)
    if isinstance(result, list):  # Greyhawk, roll for which table, then on it.
        result = table(result, roll)
    return replace_quantity(rules.random_details(result))[1]


@kinded('potion')
def entry_potion(rules, roll=None):
    """Last 6+d6 turns."""
    result = _disguised(rules, 'potion', _roll_table(rules, 'potion', roll), rules.mislead)
    return result if result.startswith(('Oil', 'Philter')) else f'Potion of {result}'


@kinded('ring')
def entry_ring(rules, roll=None):
    return f'Ring of {_disguised(rules, "ring", _roll_table(rules, "ring", roll), ("delusion", ))}'


@kinded('sword')
def entry_sword(rules, roll=None):
    return rules.sword_extras(_roll_table(rules, 'sword', roll))


@kinded('scroll')
def entry_scroll(rules, roll=None):
    """Spells, protections, traps, curses and (OSE) treasure maps."""
    result = table(rules.scroll, roll)
    match result.lower():
        case 'trap':
            return f'Trapped scroll: {table(rules.scroll_trap)}'
        case 'curse':
            return f'Cursed scroll: {table(rules.scroll_curse)}'
        case lowered if lowered.startswith('treasure map'):
            return _ose_map(rules, result)
        case lowered if 'spell' in lowered:
            return rules.scroll_spells(result)
        case _:
            return f'Scroll of {rules.random_details(result)}'


@kinded('weapon')
def entry_weapon(rules, roll=None):
    return _roll_table(rules, 'weapon', roll)


@kinded('wsr')
def entry_wsr(rules, roll=None):
    """Wand, Staff, Rod."""
    result = _roll_table(rules, 'wsr', roll)
    return f'{result}{rules.charges(result)}'


def entry_map(rules, roll=None):
    """Roll up a map, and what it leads to, as the ruleset has it."""
    return rules.roll_map(roll)


@kinded('map')
def entry_odd_map(rules, roll=None):
    """Roll up a map, and what it leads to."""
    kind = table(MAP_KINDS, roll)
    if kind == 'treasure':
        return format_map(_map_treasure(rules, random.randint(1, 8)))
    if kind == 'magic':
        return format_map(_map_magic(rules, random.randint(1, 8)))
    treasure, magic, there = MAP_BOTH[random.randint(1, 8) - 1]
    return format_map(_map_treasure(rules, treasure) + _map_magic(rules, magic), 'magic already there' if there else '')


def entry_odd_any(rules, roll=None, skip=()):
    """OD&D Vol 2 Magic/Maps Determination table: 75% magic item, 25% map."""
    if (roll or d100()) > 75:
        return entry_odd_map(rules)
    return entry_item(rules, skip=skip)


def entry_odd_noweap_any(rules, roll=None):
    """OD&D Vol 2 Type F: "no weapons, any other"."""
    return entry_odd_any(rules, roll, skip=NO_WEAPONS)


def entry_dmg_any(rules, roll=None, skip=()):
    """AD&D 1e DMG Map or Magic Determination: 01-10 is a map, 11-00 a magic item."""
    if (roll or d100()) <= 10:
        return entry_dmg_map(rules)
    return entry_item(rules, skip=skip)


def entry_dmg_noweap_any(rules, roll=None):
    """MM Type F: "any 3 except swords or misc. weapons"."""
    return entry_dmg_any(rules, roll, skip=NO_WEAPONS)


def entry_dmg_noswordpotion(rules, roll=None):
    """DMG Magic Treasure: "any 3 items, no Sword or Potions"."""
    return entry_item(rules, roll, skip=('Sword', 'Potion'))


def entry_dmg_each(rules, roll=None):
    """MM Type U: 1 of each magic excluding potions and scrolls."""
    return [roll_function(rules) for roll_function in DMG_EACH]


def entry_dmg_each_twice(rules, roll=None):
    """MM Type V: 2 of each magic excluding potions and scrolls."""
    return [roll_function(rules) for roll_function in DMG_EACH * 2]


def _dmg_monetary(rules, roll=None):
    """DMG II.A Monetary Treasure, d20: list of text."""
    roll = roll or d20()
    if roll >= 18:
        rolls = {18: [random.randint(1, 17) for _ in range(2)], 19: [random.randint(1, 17) for _ in range(3)], 20: [row[0] for row in DMG_MONETARY]}[roll]
        return [part for each in rolls for part in _dmg_monetary(rules, each)]
    return [rules.monetary(kind, amount) for kind, amount in table(DMG_MONETARY, roll)]


def _dmg_magic(rules, roll=None, in_map=False):
    """DMG II.B Magic Treasure, d20: list of text. A map's magic is never another treasure map."""
    items = []
    for roll_function in table(DMG_MAGIC, roll or d20()):
        item = roll_function(rules)
        while in_map and item.lower().startswith('treasure map'):
            item = roll_function(rules)
        items.append(item)
    return items


def _dmg_hoard(rules, roll=None):
    """DMG II.C Combined Hoard, d%: list of what is there, and of what a map in it leads to."""
    monetary, magic, map_monetary, map_magic = table(DMG_HOARD, roll)
    things = [part for lowest, _ in monetary for part in _dmg_monetary(rules, lowest)]
    things += [part for lowest, _ in magic for part in _dmg_magic(rules, lowest)]
    if map_monetary or map_magic:
        led_to = [part for lowest, _ in map_monetary for part in _dmg_monetary(rules, lowest)]
        led_to += [part for lowest, _ in map_magic for part in _dmg_magic(rules, lowest, in_map=True)]
        things.append(format_map(led_to))
    return things


@kinded('map')
def entry_dmg_map(rules, roll=None):
    """DMG II Map Table; what it leads to, and where. One thing is on the line, more are a list under it."""
    kind = table(DMG_MAP_KINDS, roll)
    if kind == 'False map':
        return kind
    place, shown = table(DMG_MAP_PLACE)
    where = f'{place}, {table(DMG_MAP_GUARD)}' if shown else place
    match kind:
        case 'monetary treasure':
            things = _dmg_monetary(rules)
        case 'magic treasure':
            things = _dmg_magic(rules, in_map=True)
        case _:
            things = _dmg_hoard(rules)
    return format_map(things, where)


# OD&D Vol 2, Maps. Magic/Maps Determination: 76-00 is a map; Maps table picks kind.
MAP_KINDS = [(60, 'treasure'), (90, 'magic'), (100, 'both')]
# Treasure maps, d8: rows of (kind, quantity). Quantities are N-M dice (000s are thousands).
MAP_TREASURE = [
    (('sp', '10000-40000'), ),
    (('gp', '5000-30000'), ),
    (('sp', '10000-40000'), ('gp', '5000-30000')),
    (('sp', '10000-40000'), ('gems', '2-20')),
    (('gp', '5000-30000'), ('gems', '5-30')),
    (('sp', '10000-40000'), ('gp', '5000-30000'), ('gems', '1-100')),
    (('gems', '10-60'), ('jewelry', '2-20')),
    (('sp', '10000-40000'), ('gp', '5000-30000'), ('gems', '10-60'), ('jewelry', '2-20')),
    ]
# OSE Treasure Maps by numeral: (kind, quantity N-M dice or (count, categories to skip) for magic).
OSE_MAPS = {
    'I': (('magic', (1, ())), ),
    'II': (('gems', '1-6x10'), ('jewelry', '2-20')),
    'III': (('magic', (2, ())), ),
    'IV': (('magic', (3, ('Sword', ))), ),
    'V': (('magic', (3, ())), ('potion', None)),
    'VI': (('magic', (3, ())), ('scroll', None), ('potion', None)),
    'VII': (('gems', '5-30'), ('magic', (2, ()))),
    'VIII': (('gp', '1000-4000'), ),
    'IX': (('gp', '5000-30000'), ),
    'X': (('gp', '5000-30000'), ('magic', (1, ()))),
    'XI': (('gp', '5000-30000'), ('gems', '5-30')),
    'XII': (('gp', '6000-36000'), ),
    }
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


# AD&D 1e DMG (1979) Treasure, Random Determination. Dice are d%, except where a table says d20.
# II. Map Table.
DMG_MAP_KINDS = [(5, 'False map'), (70, 'monetary treasure'), (90, 'magic treasure'), (100, 'combined hoard')]
# Where a map leads (text, whether the treasure it shows is placed by DMG_MAP_GUARD).
DMG_MAP_PLACE = [
    (20, 'labyrinth of caves found in the lair', False),
    (60, 'outdoors, 5 to 8 miles distant', True),
    (90, 'outdoors, 10 to 40 miles distant', True),
    (100, 'outdoors, 50 to 500 miles distant', True),
    ]
DMG_MAP_GUARD = [
    (10, 'buried and unguarded'), (20, 'hidden in water'), (70, 'guarded in a lair'),
    (80, 'somewhere in a ruins'), (90, 'in a burial crypt'), (100, 'secreted in a town'),
    ]
# II.A Monetary Treasure, d20: rows of (kind, amount), rows 18-20 roll more of these (see _dmg_monetary).
DMG_MONETARY = [
    (2, (('cp', '2-8x10000'), ('sp', '2-5x10000'))),
    (5, (('ep', '5-30x1000'), )),
    (10, (('gp', '3-18x1000'), )),
    (12, (('pp', '5-20x100'), )),
    (15, (('gems', '1-10x10'), )),
    (17, (('jewelry', '5-50'), )),
    ]
# II.B Magic Treasure, d20.
DMG_MAGIC = [
    (5, (entry_item, entry_potion, entry_potion, entry_potion, entry_potion)),
    (8, (entry_item, entry_item)),
    (12, (entry_sword, entry_armor, entry_weapon)),  # Sword, Armor or Shield, Miscellaneous Weapon.
    (14, (entry_dmg_noswordpotion, entry_dmg_noswordpotion, entry_dmg_noswordpotion)),
    (18, (entry_potion, ) * 6 + (entry_scroll, ) * 6),
    (19, (entry_ring, entry_wsr, entry_item, entry_item)),  # Any 4 items, 1 is a Ring, 1 is a Rod.
    (20, (entry_wsr, entry_misc, entry_item, entry_item, entry_item)),  # Any 5 items, 1 is a Rod, 1 is Miscellaneous Magic.
    ]
# II.C Combined Hoard, d%: (monetary, magic, map to monetary, map to magic), each the d20 rows (lowest, highest) of II.A / II.B.
# Row 97-00 is one map to a hoard of monetary 11-12 & 13-15 and magic 15-18 & 20, nothing on hand.
DMG_HOARD = [
    (20, ((1, 2), ), ((1, 5), ), (), ()),
    (40, ((6, 10), ), ((1, 5), ), (), ()),
    (55, ((3, 5), (6, 10)), ((1, 5), (15, 18)), (), ()),
    (65, ((1, 2), (3, 5), (6, 10)), ((9, 12), (13, 14)), (), ()),
    (75, ((6, 10), (11, 12)), ((6, 8), (15, 18)), (), ()),
    (80, ((3, 5), (6, 10), (11, 12), (16, 17)), ((1, 5), (9, 12)), (), ()),
    (85, ((20, 20), ), (), (), ((1, 5), )),
    (90, ((20, 20), ), (), (), ((19, 19), )),
    (96, (), ((20, 20), ), ((1, 2), (3, 5)), ()),
    (100, (), (), ((11, 12), (13, 15)), ((15, 18), (20, 20))),
    ]
# MM Types U and V, "of each magic excluding potions & scrolls": rings, rods, staves & wands, misc. magic, armor, swords, misc. weapons.
DMG_EACH = (entry_ring, entry_wsr, entry_misc, entry_armor, entry_sword, entry_weapon)


class RollOutOfRange(ValueError):
    """A roll is higher than the highest row of the table it was made on."""


class Treasures:
    """Base for gems and jewelry; subclasses yield (1, value, description) per piece from _roll."""

    noun, plural = 'gem', 'gems'
    per_gp = 1  # Units of value to the gp, see price.
    brief = False  # Combine pieces of the same value, dropping gem type and size, jewelry design.

    def roll(self, count, group):
        """List of (count, value, description)."""
        pieces = self._roll(count, group)
        if self.brief:
            pieces = ((quantity, value, self.noun if value else thing) for quantity, value, thing in pieces)  # Keep magical (worth 0).
        return list(reduce_groups(pieces))

    def _roll(self, count, group):
        raise NotImplementedError

    def amount(self, count):
        """'1 gem', '4 gems'."""
        return f'{count:,} {self.noun if count == 1 else self.plural}'

    def lines(self, count, group):
        """Header ('4 gems (800gp total):') then an indented line per group; one piece alone is a single unindented line."""
        things = self.roll(count, group)
        if count == 1:
            _, value, thing = things[0]
            return [f'{price(value, self.per_gp)} {thing}' if value else thing]
        total = sum(quantity * value for quantity, value, _ in things) // self.per_gp  # Drops under 1gp.
        return [f'{self.amount(count)} ({total:,}gp total):', *self._format(things)]

    def _format(self, things):
        things = sorted(things, key=lambda row: row[1] or 99999)
        count_width = max(len(str(count)) for count, _, _ in things)
        width = max((len(price(value, self.per_gp)) for _, value, _ in things), default=4)
        for count, value, thing in things:
            if not value:  # Magical, no count or price column.
                yield f' {thing}'
                continue
            name = self.plural if count > 1 and thing == self.noun else thing  # Generic OD&D 'gem'.
            yield f' {count:>{count_width}} x {price(value, self.per_gp):>{width}} {name}'


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
        'Ioun absorbs d20 spell levels',
        'Ioun geas',
        'Ioun 16 Int',
        'Ioun regen 1hp turn',
        'Ioun +1 spell slot',
        'Warstone +1 if built into weapon',
        'Amulet of non-detection',
        'of light as Light spell',
        'of Prayer',
        'of Poison Detection',
        'of clairvoyance as spell',  # only transparent gems prepended
        # These are standalone, do not get gemstone prepended
        'Demonstone',
        'Topaz of Controlling Earth Elementals',
        'Emerald of Controlling Water Elementals',
        'Ruby of Controlling Fire Elementals',
        'Sapphire of Controlling Air Elementals',
        'Scarab of Protection from Level Drain',
        'Scarab of Enraging Enemies',
        ]
    standalone = ('Demonstone', 'Scarab', 'of Controlling')  # Unusual gems not preceded by a gem type (Controlling names its own).
    transparent = ('Emerald', 'Ruby', 'Sapphire', 'Diamond')  # Gems that can be of clairvoyance.
    sizes = {2: 'large', 4: 'giant', 8: 'enormous'}

    def __init__(self, chances, specials=True):
        """chances: cumulative d100 chance of each value in values. specials: 1 in 10 gems may be magical or larger."""
        self.chances = chances
        self.specials = specials

    def _roll(self, count, group):
        """Roll up count gems, in groups of size group."""
        size = value = 0
        unusual_found = False  # Only one magical gem.
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
                if d100() <= 30 and value >= 100 and not unusual_found:
                    value = 0
                    if 'Diamond' in gem:  # All magical Diamonds are True Seeing Gems.
                        gem = 'Diamond of True Seeing'
                    else:
                        found = random.choice(self.unusual)
                        if any(word in found for word in self.standalone):  # Not made from a rolled gem type.
                            gem = found
                        elif found.startswith('of clairvoyance'):
                            gem = f'{random.choice(self.transparent)} {found}'
                        else:
                            gem = f'{gem[0:gem.index(" - ")]} {found}'
                    unusual_found = True  # Only one magic gem per hoard.
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


SP = 10  # Copper pieces to the silver piece, AD&D coins.
GP = 20 * SP  # AD&D: 20sp to the gp.


class GemsDmg(Treasures):
    """AD&D 1e DMG, Value and Reputed Properties of Gems, as written.

    Values are whole copper pieces (10cp = 1sp, 20sp = 1gp), no fractions; a total drops what is under 1gp.
    Base value by d% (in lots of group stones); each stone is then varied by d10, see _vary.
    The description says how: a higher or lower base value is a size (medium, large ... down to small, tiny, chip ...),
    a 2 on the d10 is extraordinary, a 3 perfect, a 9 flawed. Base size is nothing.
    Judgement: Garnet, Pearl and Spinel are 100gp, or 500gp for "the most prized" colour; the 1,000gp stones listed
    without a value in the book are 1,000gp. Stones below 10gp are 5gp, 1gp, 10sp, 5sp and 1sp.
    A description of alternatives (blue, black or brown) shows one of them, equally likely; "X to Y" ranges stay whole.
    """
    per_gp = GP
    base = [(25, 10), (50, 50), (70, 100), (90, 500), (99, 1000), (100, 5000)]  # Value in gp.
    values = [
        1 * SP,
        5 * SP,
        10 * SP,
        1 * GP,
        5 * GP,
        10 * GP,
        50 * GP,
        100 * GP,
        500 * GP,
        1000 * GP,
        5000 * GP,
        10000 * GP,
        25000 * GP,
        50000 * GP,
        100000 * GP,
        250000 * GP,
        500000 * GP,
        1000000 * GP,
        ]
    larger = ['', 'medium', 'large', 'huge', 'enormous', 'giant', 'colossal', 'epical']  # By places up.
    smaller = ['', 'small', 'tiny', 'pebble', 'chip', 'fleck']  # By places down.
    stones = {
        10: [  # Ornamental stones.
            'Azurite - mottled deep blue',
            'Banded Agate - striped brown and blue and white and reddish',
            'Blue Quartz - pale blue',
            'Eye Agate - circles of gray, white, brown, blue and/or green',
            'Hematite - gray-black',
            'Lapis Lazuli - light and dark blue with yellow flecks',
            'Malachite - striated light and dark green',
            'Moss Agate - {pink|yellow-white} with {grayish|greenish} "moss markings"',
            'Obsidian - black',
            'Rhodochrosite - light pink',
            'Tiger Eye - rich brown with golden center under-hue',
            'Turquoise - light blue-green',
            ],
        50: [  # Semi-precious stones.
            'Bloodstone - dark gray with red flecks',
            'Carnelian - orange to reddish-brown (also called Sard)',
            'Chalcedony - white',
            'Chrysoprase - apple green to emerald green',
            'Citrine - pale yellow-brown',
            'Jasper - {blue|black|brown}',
            'Moonstone - white with pale blue glow',
            'Onyx - {bands of black and white|pure black|pure white}',
            'Rock Crystal - clear',
            'Sardonyx - {bands of sard (red) and onyx (white)|sard}',
            'Smoky Quartz (Cairngorm) - light {gray|yellow|blue}',
            'Star Rose Quartz - translucent rosy stone with white "star" center',
            'Zircon - clear pale blue-green',
            ],
        100: [  # Fancy stones.
            'Amber - watery gold to rich gold',
            'Alexandrite - dark green',
            'Amethyst - deep purple',
            'Chrysoberyl - yellow-green to green',
            'Coral - crimson',
            'Garnet - {red|brown-green}',
            'Jade - {light green|deep green|green and white|white}',
            'Jet - deep black',
            'Pearl - lustrous {white|yellowish|pinkish}',
            'Spinel - {red|red-brown|deep green}',
            'Tourmaline - {green|blue|brown|reddish} pale',
            ],
        500: [  # Fancy stones, precious.
            'Aquamarine - pale blue-green',
            'Garnet - violet',
            'Pearl - pure black',
            'Peridot - rich olive green (Chrysolite)',
            'Spinel - very deep blue',
            'Topaz - golden yellow',
            ],
        1000: [
            'Black Opal - dark green with black mottling and golden flecks',
            'Emerald - deep bright green',
            'Fire Opal - fiery red',
            'Opal - pale blue with green and golden mottling',
            'Oriental Amethyst - rich purple (Corundum)',
            'Oriental Topaz - fiery yellow (Corundum)',
            'Sapphire - clear to medium blue (Corundum)',
            'Star Ruby - translucent ruby with white "star" center',
            'Star Sapphire - translucent sapphire with white "star" center',
            ],
        5000: [
            'Black Sapphire - lustrous black with glowing highlights',
            'Diamond - clear blue-white with lesser stones clear white or pale tints',
            'Jacinth - fiery orange (Corundum)',
            'Oriental Emerald - clear bright green (Corundum)',
            'Ruby - clear red to deep crimson (Corundum)',
            ],
        }

    def _vary(self, base):
        """Roll d10 for the stone, up and down a base value (in cp), doubling or +/-10% steps.

        Returns (value in cp, words), words are the stone's size and quality, '' for neither.
        """
        start = index = self.values.index(base)
        roll = random.randint(1, 10)
        while roll in (1, 10):
            if roll == 1:  # Next higher base value, roll again ignoring results above 8. At most 7 places up.
                index = min(index + 1, start + 7, len(self.values) - 1)
                roll = random.randint(1, 8)
            else:  # 0: next lower base value, roll again ignoring results below 2. At most 5 places down.
                index = max(index - 1, start - 5, 0)
                roll = random.randint(2, 10)
        worth = self.values[index]
        quality = ''
        if roll == 2:
            worth *= 2
            quality = 'extraordinary'
        elif roll == 3:
            worth = worth * (10 + d6()) // 10
            quality = 'perfect'
        elif roll == 9:
            worth = worth * (10 - d4()) // 10
            quality = 'flawed'
        places = index - start
        size = self.larger[places] if places >= 0 else self.smaller[-places]
        return worth, ' '.join(word for word in (size, quality) if word)

    @staticmethod
    def _choose(text):
        """Replace each {a|b|c} in a stone's description with one of its options."""
        return re.sub(r'\{([^}]*)\}', lambda match: random.choice(match.group(1).split('|')), text)

    def _roll(self, count, group):
        """Roll up count gems, base value in groups of size group."""
        base = 0
        for position in range(count):
            if position % group == 0:
                base = table(self.base)
            value, words = self._vary(base * GP)
            yield 1, value, ' '.join(part for part in (words, self._choose(random.choice(self.stones[base]))) if part)


class JewelriesDmg(Treasures):
    """AD&D 1e DMG, Value and Reputed Properties of Gems and Jewelry: Jewelry, as written.

    Judgement: the book gives each class a range of values; they are taken as a die times the lowest value,
    d10 x 100, d6 x 200, d6 x 300, d6 x 500, d6 x 1,000, d4 x 2,000 and d6 x 2,000. An exceptional piece (1 on d10)
    is the highest value of its class or, 50% of the time, a re-rolled and re-checked piece of the next class.
    The 1 in 8 exceptional stone adds 5,000gp, doubled for each 1 on d6, no more than 640,000gp.
    A description of alternatives (ivory or wrought silver) shows one of them, equally likely.
    The description notes an exceptional workmanship and an exceptional stone.
    """
    noun = plural = 'jewelry'
    # (highest d% roll, description, die sides, die multiplier, set with gems).
    classes = [
        (10, 'ivory or wrought silver', 10, 100, False),
        (20, 'wrought silver and gold', 6, 200, False),
        (40, 'wrought gold', 6, 300, False),
        (50, 'jade, coral or wrought platinum', 6, 500, False),
        (70, 'silver with gems', 6, 1000, True),
        (90, 'gold with gems', 4, 2000, True),
        (100, 'platinum with gems', 6, 2000, True),
        ]

    def _piece(self):
        """(value, description, set with gems, exceptional workmanship)."""
        index = next(position for position, row in enumerate(self.classes) if d100() <= row[0])
        exceptional = False
        while True:
            _, description, sides, multiplier, gems = self.classes[index]
            value = random.randint(1, sides) * multiplier
            if d10() != 1:
                return value, description, gems, exceptional
            exceptional = True
            if index < len(self.classes) - 1 and random.randint(1, 2) == 1:
                index += 1
            else:
                return sides * multiplier, description, gems, exceptional

    def _roll(self, count, group):
        """Roll up count pieces of jewelry, group ignored."""
        for _ in range(count):
            value, description, gems, exceptional = self._piece()
            notes = [f'jewelry, {random.choice(re.split(', | or ', description))}']
            if gems and d8() == 1:
                extra = 5000
                while d6() == 1 and extra < 640000:
                    extra *= 2
                value += extra
                notes.append(f'exceptional stone ({extra:,}gp)')
            if exceptional:
                notes.append('exceptional workmanship')
            yield 1, value, ', '.join(notes)


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
    Subclasses may override scroll_spells (rows of the scroll table that are spells) and roll_map.

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
        """E.g. 'Expert rules', 'Expert rules as written'."""
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

    def scroll_spells(self, result):
        """Text for a scroll table row of spells, 'N spells': a random caster and the levels of its spells."""
        caster = random.choice(['Cleric', 'Magic-user', 'Magic-user', 'Magic-user'])
        return f'{caster} scroll {self.spell_summary(caster, int(result.split()[0]))}'

    def roll_map(self, roll=None):
        """Roll up a map, and what it leads to."""
        return entry_odd_map(self, roll)

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
                yield from _flatten([roll_function(self)])
        else:
            yield self.monetary(kind, amount)

    def monetary(self, kind, amount):
        """Text for a coin, 'gems' or 'jewelry' of a quantity (N-M, see replace_quantity); gems and jewelry are lines() text."""
        count, text = replace_quantity(amount)
        if kind == 'gems':
            return Item('\n'.join(self.gems.lines(count, 10)), 'gem')
        if kind == 'jewelry':
            return Item('\n'.join(self.jewelries.lines(count, 1)), 'jewelry')
        return Item(f'{text}{kind}', 'money')

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
        (40, 'Sword +1, +2 vs. lycanthropes'),
        (45, 'Sword +1, +2 vs. magic-users and enchanted monsters'),
        (50, 'Sword +1, locating objects ability'),
        (60, 'Sword +1, +3 vs. {trolls|clerics}'),  # {Lawful or Neutral|Chaotic} target, see sword_extras.
        (65, 'Sword, flaming: +1, +2 vs. {trolls|pegasi, hippogriffs, rocs}, +3 vs. {undead|treants}'),
        (70, 'Sword +1, wishes included (2-8 wishes)'),
        (75, 'Sword +1, +3 vs. dragons'),
        (78, 'Sword +2'),
        (80, 'Sword +2, charm person ability'),
        (82, 'Sword +3'),
        (83, 'Sword, one life energy draining ability'),
        (100, 'Sword -2, cursed'),
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
        (15, 'note shifting walls & rooms'),
        (30, 'detect sloping passages'),
        (40, 'locate secret doors'),
        (50, 'detect traps'),
        (60, 'see invisible objects'),
        (70, 'detect evil and/or gold'),
        (80, 'detect meal & what kind'),
        (90, 'detect magic'),
        (95, 'detect gems (# and size)'),
        ]
    # Languages, in addition to alignment's. Judgement: book has 86-95 Four and 90-99 Five, took 96-99.
    # 00 is two rolls ignoring 00.
    _sword_languages = [(50, 1), (70, 2), (85, 3), (95, 4), (99, 5)]
    # Extraordinary Abilities. 98-99 is two rolls ignoring over 97, 00 is three rolls.
    _sword_extraordinary = [
        (10, 'clairaudience'),
        (20, 'clairvoyance'),
        (30, 'ESP'),
        (40, 'telepathy'),
        (50, 'telekinesis'),
        (59, 'teleportation'),
        (68, 'x-ray vision'),
        (77, 'illusion generation'),
        (82, 'levitation'),
        (87, 'flying'),
        (92, 'healing (1 point/6 turns or 6 points/day)'),
        (97, 'strength 1d4 x normal for 1d10 turns, once/day'),  # Rolled when used.
        ]
    _sword_purposes = ['slay magic-users', 'slay clerics', 'slay fighting-men', 'slay monsters', 'defeat law', 'defeat chaos']
    _sword_purpose_powers = {
        'Lawful': 'paralyze Chaotic opponents',
        'Neutral': '+1 to all saving throws',
        'Chaotic': 'disintegrate Lawful opponents',
        }

    def sword_extras(self, sword):
        """Alignment, Intelligence, Egoism and Origin/Purpose. Vol 2, Explanations of Magic Items: Swords."""
        alignment = table(self._sword_alignment)
        lowered = sword.lower()
        if 'energy draining' in lowered:
            alignment = {'Lawful': 'Chaotic', 'Chaotic': 'Lawful'}.get(alignment, alignment)
        if any(word in lowered for word in ('holy', 'sharpness', 'vorpal')):  # Judgement: Paladin / Lawful only swords.
            alignment = 'Lawful'
        sword = re.sub(r'\{([^|}]*)\|([^}]*)\}', lambda match: match.group(2 if alignment == 'Chaotic' else 1), sword)
        parts, lines = [alignment], []
        intelligence = d12()
        special = d100() >= 91  # Special purpose.
        if special:
            intelligence = 12
        if intelligence >= 7:
            ego = 12 if special else d12()
            powers = self._sword_primary_powers({7: 1, 8: 2}.get(intelligence, 3))
            communication = 'telepathy' if intelligence == 12 else 'speech' if intelligence >= 10 else 'empathy'
            parts += [f'Int {intelligence}', f'Ego {ego}']
            parts.append(language_trait(communication, alignment, self._sword_language_count()) if intelligence >= 10 else communication)
            if intelligence >= 11:
                lines.append('read magic')
            if intelligence == 12:
                powers += self._sword_extraordinary_powers()
            lines += [f'{power} x{count}' if count > 1 else power for power, count in collections.Counter(powers).items()]
            if special:
                purpose = random.choice(self._sword_purposes)
                while (alignment, purpose) in (('Lawful', 'defeat law'), ('Chaotic', 'defeat chaos')):  # Judgement: can't defeat itself.
                    purpose = random.choice(self._sword_purposes)
                lines.append(f'special purpose: {purpose}, {self._sword_purpose_powers[alignment]}')
        return format_sword(sword, parts, lines)

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
            return [table(self._sword_extraordinary, roll)]
        return [table(self._sword_extraordinary, random.randint(1, 97)) for _ in range(2 if roll < 100 else 3)]

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
        (35, 'Sword +1, +2 vs. lycanthropes'),
        (40, 'Sword +1, +2 vs. magic-users and enchanted monsters'),
        (45, 'Sword +1, locating objects ability'),
        (50, 'Sword +1, +3 vs. {trolls|clerics}'),  # {Lawful or Neutral|Chaotic} target, see sword_extras.
        (55, 'Sword, flaming: +1, +2 vs. {trolls|pegasi, hippogriffs, rocs}, +3 vs. {undead|ents}'),
        (60, 'Sword +1, wishes included (2-8 wishes)'),
        (65, 'Sword +1, +3 vs. dragons'),
        (68, 'Sword +2'),
        (70, 'Sword +2, charm person ability'),
        (72, 'Sword +3'),
        (73, 'Sword, one life energy draining ability'),
        (74, 'Sword +2, nine steps draining ability'),
        (75, 'Sword +4'),
        (76, 'Holy Sword +5'),
        (78, 'Sword of Cold: +3, +5 vs. fire using/dwelling creatures'),
        (82, 'Dragon Slaying Sword +2 (<dragon> Dragons, 4d10 damage)'),
        (83, 'Sword +1, cursed'),
        (97, 'Sword -2, cursed'),
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
        (87, 'Sword +1, cursed berserker'),
        (92, 'Sword -1, cursed'),
        (97, 'Sword -2, cursed'),
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
        (80, 'Treasure Map II: 1d6 x 10 gems and 2d10 jewelry'),
        (82, 'Treasure Map III: 2 magic items'),
        (83, 'Treasure Map IV: 3 magic items (no swords)'),
        (84, 'Treasure Map V: 3 magic items and 1 potion'),
        (85, 'Treasure Map VI: 3 magic items, 1 scroll, 1 potion'),
        (86, 'Treasure Map VII: 5d6 gems and 2 magic items'),
        (90, 'Treasure Map VIII: Hoard worth 1d4 x 1,000gp'),
        (95, 'Treasure Map IX: Hoard worth 5d6 x 1,000gp'),
        (96, 'Treasure Map X: Hoard worth 5d6 x 1,000gp and 1 magic item'),
        (98, 'Treasure Map XI: Hoard worth 5d6 x 1,000gp and 5d6 gems'),
        (100, 'Treasure Map XII: Hoard worth 6d6 x 1,000gp'),
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
        (2, 'Sword -1, cursed'),
        (4, 'Sword -2, cursed'),
        (44, 'Sword +1'),
        (50, 'Sword +1, +2 vs lycanthropes'),
        (56, 'Sword +1, +2 vs spell users'),
        (61, 'Sword +1, +3 vs dragons'),
        (66, 'Sword +1, +3 vs enchanted creatures'),
        (71, 'Sword +1, +3 vs regenerating creatures'),
        (76, 'Sword +1, +3 vs undead'),
        (77, 'Sword +1, energy drain (5-8 levels)'),
        (81, 'Sword +1, flaming'),
        (89, 'Sword +1, light'),
        (92, 'Sword +1, locate objects'),
        (93, 'Sword +1, wishes (1-4)'),
        (96, 'Sword +2'),
        (98, 'Sword +2, charm person'),
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
        (10, 'detect evil or good'),
        (15, 'detect gems'),
        (25, 'detect magic'),
        (35, 'detect metals'),
        (50, 'detect shifting architecture'),
        (65, 'detect slopes'),
        (75, 'detect traps'),
        (85, 'locate secret doors'),
        (95, 'see invisible objects'),
        (99, 'roll extraordinary'),
        (100, 'roll twice'),
        ]
    # Duplicates are re-rolled, except those in _sword_duplicates.
    _sword_extraordinary = [
        (10, 'clairaudience'),
        (20, 'clairvoyance'),
        (30, 'ESP'),
        (35, 'extra damage'),
        (40, 'flying'),
        (45, 'healing'),
        (54, 'illusion'),
        (59, 'levitation'),
        (69, 'telekinesis'),
        (79, 'telepathy'),
        (88, 'teleportation'),
        (97, 'x-ray vision'),
        (99, 'roll twice'),
        (100, 'roll thrice'),
        ]
    _sword_duplicates = ('extra damage', 'healing')
    # Lawful/Chaotic creatures become the other if the sword is that alignment.
    _sword_purposes = [
        (1, 'arcane spell casters'),
        (2, 'divine spell casters'),
        (3, 'warriors'),
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

    def roll_map(self, roll=None):
        """A Treasure Map row of the scroll table, as likely as it is on that table (the maps are its last rows)."""
        first = max(threshold for threshold, text in self.scroll if not text.startswith('Treasure Map')) + 1
        if roll is None or roll < first:
            roll = random.randint(first, self.scroll[-1][0])
        return _ose_map(self, table(self.scroll, roll))

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
            return format_sword(sword, *self._sentient_sword(special=True))
        if d100() <= self._sword_sentient_chance:
            return format_sword(sword, *self._sentient_sword())
        return sword

    def _sentient_sword(self, special=False):
        """(traits, lines): alignment, Int, Ego and communication; then magic reading, powers and special purpose of a sentient sword."""
        alignment = table(self._sword_alignment)
        intelligence = 12 if special else d6() + 6
        ego = 12 if special else d12()
        communication = 'speech' if intelligence >= 10 else 'empathy'
        traits = [alignment, f'Int {intelligence}', f'Ego {ego}', language_trait(communication, alignment, self._sword_language_count()) if intelligence >= 10 else communication]
        lines = ['read magic'] if intelligence >= 11 else []
        lines += self._sword_powers(min(3, intelligence - 6), 1 if intelligence == 12 else 0)
        if special:
            purpose = table(self._sword_purposes)
            if purpose == f'{alignment} creatures':
                purpose = 'Chaotic creatures' if alignment == 'Lawful' else 'Lawful creatures'
            lines.append(f'special purpose: slay {purpose}, {self._sword_purpose_powers[alignment]}')
        return traits, lines

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
        (2, '-1 Sword, cursed'),
        (4, '-2 Sword, cursed berserker'),  # Added Berserker.
        (40, '+1 Sword'),
        # Book: 41-44 +1 Sword, replaced with these.
        (42, '+1 Sword of Cold: +3 vs. fire creatures'),
        (43, 'Dancing Sword'),
        (44, 'Vorpal Blade'),
        (50, '+1 Sword, +2 vs. lycanthropes'),
        (56, '+1 Sword, +2 vs. spell users'),
        (60, '+1 Sword, +3 vs. dragons'),
        (61, '+1 Sword, dragon slaying'),  # Book: 61 +1 Sword, +3 vs. Dragons.
        (66, '+1 Sword, +3 vs. enchanted'),
        (71, '+1 Sword, +3 vs. regenerating'),
        (76, '+1 Sword, +3 vs. undead'),
        (77, '+1 Sword, energy drain'),
        (81, '+1 Sword, flaming, +2 vs troll, flying, +3 vs plant, undead'),
        (89, '+1 Sword, light'),
        (92, '+1 Sword, locate objects'),
        (93, '+1 Sword, 1-4 wishes'),
        (96, '+2 Sword'),
        (98, '+2 Sword, charm humanoid'),  # Book: Charm Person.
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
        (2, '3-30 Arrows +1'),
        (12, '2-12 Arrows +1'),
        (17, '1-6 Arrows +2'),
        (18, 'Arrow of Slaying'),  # Book: 18 is 1-6 +2 Arrows.
        (27, 'Axe +1'),
        (30, 'Axe +2'),
        (33, 'Bow +1'),
        (43, '2-12 Bolts +1'),
        (45, '3-30 Bolts +1'),
        (51, '1-6 Bolts +2'),
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
        (10, 'clairaudience'),
        (20, 'clairvoyance'),
        (30, 'ESP (3/day)'),
        (35, '3x damage for d6 rnds (1/day)'),
        (40, 'flying (3/day)'),
        (45, 'heal as spell (1/day)'),
        (54, 'illusion (3/day)'),
        (59, 'levitation'),
        (69, 'telekinesis (3/day)'),
        (79, 'telepathy (3/day)'),
        (88, 'teleportation (3/day)'),
        (97, 'x-ray vision (3/day)'),
        (99, 'roll twice'),
        (100, 'roll thrice'),
        ]
    _sword_duplicates = ('3x damage for d6 rnds (1/day)', 'heal as spell (1/day)')
    _sword_sensory = [
        (5, 'know depth & direction'),  # Book: 01-10 Detect evil or good, see sense chaos/law.
        (10, 'detect slopes & shifting/teleports'),  # Book: 36-50 shifting architecture, 51-65 slopes; added teleports.
        (15, 'locate gems 60 ft. (3/day)'),
        (25, 'sense magic 20 ft. (3/day)'),
        (35, 'locate named metal 60 ft. (3/day)'),
        (50, 'sense chaos 20 ft.'),  # Book: Detect evil or good split in two, at slopes/shifting's odds.
        (65, 'sense law 20 ft.'),
        (75, 'see traps (3/day)'),
        (85, 'see secret doors (3/day)'),
        (95, 'see invisible'),
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
            return format_sword(sword, *self._sentient_sword(special=True))
        if d100() <= self._sword_sentient_chance:
            return format_sword(sword, *self._sentient_sword())
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
        (8, 'Treasure Map VIII: Hoard worth 1d4 x 1,000gp'),
        ]
    sword = [
        (1, 'Sword -1, cursed'),
        (2, 'Sword +1'),
        (3, 'Sword +1, +2 vs lycanthropes'),
        (4, 'Sword +1, +2 vs spell users'),
        (5, 'Sword +1, +3 vs dragons'),
        (6, 'Sword +1, +3 vs undead'),
        (7, 'Sword +1, light'),
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
        (2, '-1 Sword, cursed'),
        (3, '+1 Sword, +2 vs. lycanthropes'),
        (4, '+1 Sword, +2 vs. spell users'),
        (5, '+1 Sword, +3 vs. dragons'),
        (7, '+1 Sword, +3 vs. undead'),
        (8, '+2 Sword'),
        (10, '+1 Sword, light'),
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
        (1, '10 Arrows +1'),
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
        (4, '1 x 5d6, 2 x 3d6'),
        (8, '1 x 6d6, 2 x 4d6, 2 x 2d6'),
        (12, '1 x 7d6, 2 x 5d6, 4 x 3d6'),
        (16, '1 x 8d6, 2 x 6d6, 2 x 4d6, 4 x 2d6'),
        (18, '1 x 9d6, 2 x 8d6, 2 x 5d6, 2 x 3d6'),
        (19, '1 x 10d6, 2 x 8d6, 2 x 6d6, 4 x 4d6'),
        (20, '1 x 11d6, 2 x 9d6, 2 x 7d6, 2 x 5d6, 2 x 3d6'),
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
        (11, 'Pale lavender ellipsoid: absorbs spells of 3rd level or lower (1-3x10 levels)'),
        (12, 'Lavender and green ellipsoid: absorbs spells of 5th level or lower (2-6x10 levels)'),
        (13, 'Vibrant purple prism: stores 2-8 levels of spells'),
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
        (100, 'Cloak of Manta Ray'),
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
        (3, 'Short Sword +2, quickness'),
        (6, 'Sword -1, berserker (cursed)'),
        (9, 'Sword -1, cursed'),
        (12, 'Sword -2, cursed'),
        (28, 'Sword +1'),
        (31, 'Sword +1, +2 vs lycanthropes'),
        (34, 'Sword +1, +2 vs spell users'),
        (37, 'Sword +1, +3 vs dragons'),
        (40, 'Sword +1, +3 vs enchanted creatures'),
        (43, 'Sword +1, +3 vs regenerating creatures'),
        (46, 'Sword +1, +3 vs reptiles'),
        (49, 'Sword +1, +3 vs shape changers'),
        (52, 'Sword +1, +3 vs undead'),
        (55, 'Sword +1, dragon slayer (<dragon> dragons)'),
        (56, 'Sword +1, energy drain (5-8 levels)'),
        (59, 'Sword +1, flaming'),
        (61, 'Sword +1, frost brand'),
        (64, 'Sword +1, giant slayer'),
        (69, 'Sword +1, light'),
        (71, 'Sword +1, locate objects'),
        (72, 'Sword +1, luck blade (1-4 wishes)'),
        (73, 'Sword +1, sharpness'),
        (78, 'Sword +1, sun blade'),
        (79, 'Sword +1, wishes (1-4)'),
        (80, 'Sword +1, wounding'),
        (85, 'Sword +2'),
        (87, 'Sword +2, charm person'),
        (88, 'Sword +2, dancing'),
        (89, 'Sword +2, nine lives stealer'),
        (94, 'Sword +2, venger'),
        (95, 'Sword +2, vorpal'),
        (98, 'Sword +3'),
        (99, 'Sword +3, defender'),
        (100, 'Sword +3, holy avenger'),
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
        (10, '2-12 Arrows +1'),
        (12, '3-30 Arrows +1'),
        (15, '1-6 Arrows +2'),
        (19, 'Axe +1'),
        (21, 'Axe +2'),
        (24, 'Bow +1'),
        (25, 'Crossbow +1, Distance'),
        (26, 'Crossbow +1, Speed'),
        (27, 'Crossbow +2, Accuracy'),
        (29, '2-12 Crossbow Bolts +1'),
        (31, '3-30 Crossbow Bolts +1'),
        (36, '1-6 Crossbow Bolts +2'),
        (39, 'Dagger +1'),
        (40, 'Dagger +1, Buckle'),
        (41, 'Dagger +1, Throwing'),
        (42, 'Dagger +1, Venomous'),
        (45, 'Dagger +2, +3 vs Orcs, Goblins, and Kobolds'),
        (46, 'Dagger +2, Biter'),
        (50, '2-5 Javelins of Lightning'),
        (54, '2-8 Javelins of Seeking'),
        (58, 'Mace +1'),
        (59, 'Mace +1, Disrupting'),
        (62, 'Mace +2'),
        (63, 'Mace +3'),
        (68, 'Sling +1'),
        (69, '1-4 Sling Bullets +1, Impact'),
        (71, 'Spear -1, Backbiter (Cursed)'),
        (75, 'Spear +1'),
        (77, 'Spear +2'),
        (78, 'Spear +3'),
        (80, 'Staff +1, Growing'),
        (82, 'Trident -2, Yearning (Cursed)'),
        (87, 'Trident +1, Fish Command [17-20 charges]'),
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
        return f'{len(stones)} stones: ' + '; '.join(f'{count} x {stone}' if count > 1 else stone for stone, count in counts.items())

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


ORDINALS = ('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th')


class DmgRules(Rules):
    """AD&D 1e Dungeon Masters Guide (1979) Treasure, with Monster Manual (1977) Treasure Types, rules as written.

    Where the book is ambiguous the choice is commented "Judgement". Output has no xp or sale values.
    - Coins are 10cp = 1sp, 20sp = 1gp. Gems are whole coins, a value under 1gp is shown in sp or cp and a
      total drops what is under 1gp. A gem's size (medium, large ... small, tiny, chip ...) and quality
      (extraordinary, perfect, flawed) are its value variation from the base value, see GemsDmg.
    - "Any" of a Treasure Type's maps or magic is a roll on the Map or Magic Determination (10% a map).
    - Judgement: "Sword, armor, or misc. weapon" (Type B) is one of the three, equally likely.
    - Judgement: armor is man-sized, elf-sized, dwarf-sized or gnome/halfling-sized as the book's note.
    - Judgement: an unusual sword's Ego counts a conditional plus (vs. creature types) with the base plus, and
      doubles the plus of a sword with extra powers but no extra pluses, see _sword_ego.
    - Artifacts and relics are only named, the book leaves their powers to the DM.
    """
    name = 'AD&D 1e'
    raw = True
    gems = GemsDmg()
    jewelries = JewelriesDmg()
    # Book: delusion and poison potions must be misled, "convince him that it is not harmful".
    mislead = ('delusion', 'poison')
    # Monster Manual, Treasure Types. Coins in 1,000s (platinum in 100s), per individual types are pieces.
    TREASURE_TYPES = {
        'a': (('cp', 25, '1000-6000'), ('sp', 30, '1000-6000'), ('ep', 35, '1000-6000'), ('gp', 40, '1000-10000'), ('pp', 25, '1-4x100'),
              ('gems', 60, '4-40'), ('jewelry', 50, '3-30'), ('magic', 30, (entry_dmg_any, entry_dmg_any, entry_dmg_any))),
        'b': (('cp', 50, '1000-8000'), ('sp', 25, '1000-6000'), ('ep', 25, '1000-4000'), ('gp', 25, '1000-3000'),
              ('gems', 30, '1-8'), ('jewelry', 20, '1-4'), ('magic', 10, (entry_martial, ))),
        'c': (('cp', 20, '1000-12000'), ('sp', 30, '1000-6000'), ('ep', 10, '1000-4000'),
              ('gems', 25, '1-6'), ('jewelry', 20, '1-3'), ('magic', 10, (entry_dmg_any, entry_dmg_any))),
        'd': (('cp', 10, '1000-8000'), ('sp', 15, '1000-12000'), ('ep', 15, '1000-8000'), ('gp', 50, '1000-6000'),
              ('gems', 30, '1-10'), ('jewelry', 25, '1-6'), ('magic', 15, (entry_dmg_any, entry_dmg_any, entry_potion))),
        'e': (('cp', 5, '1000-10000'), ('sp', 25, '1000-12000'), ('ep', 25, '1000-6000'), ('gp', 25, '1000-8000'),
              ('gems', 15, '1-12'), ('jewelry', 10, '1-8'), ('magic', 25, (entry_dmg_any, entry_dmg_any, entry_dmg_any, entry_scroll))),
        'f': (('sp', 10, '1000-20000'), ('ep', 15, '1000-12000'), ('gp', 40, '1000-10000'), ('pp', 35, '1-8x100'),
              ('gems', 20, '3-30'), ('jewelry', 10, '1-10'),
              ('magic', 30, (entry_dmg_noweap_any, entry_dmg_noweap_any, entry_dmg_noweap_any, entry_potion, entry_scroll))),
        'g': (('gp', 50, '10000-40000'), ('pp', 50, '1-20x100'),
              ('gems', 30, '5-20'), ('jewelry', 25, '1-10'),
              ('magic', 35, (entry_dmg_any, entry_dmg_any, entry_dmg_any, entry_dmg_any, entry_scroll))),
        'h': (('cp', 25, '5000-30000'), ('sp', 40, '1000-100000'), ('ep', 40, '10000-40000'), ('gp', 55, '10000-60000'), ('pp', 25, '5-50x100'),
              ('gems', 50, '1-100'), ('jewelry', 50, '10-40'),
              ('magic', 15, (entry_dmg_any, entry_dmg_any, entry_dmg_any, entry_dmg_any, entry_potion, entry_scroll))),
        'i': (('pp', 30, '3-18x100'), ('gems', 55, '2-20'), ('jewelry', 50, '1-12'), ('magic', 15, (entry_dmg_any, ))),
        'j': (('cp', 100, '3-24'), ),
        'k': (('sp', 100, '3-18'), ),
        'l': (('ep', 100, '2-12'), ),
        'm': (('gp', 100, '2-8'), ),
        'n': (('pp', 100, '1-6'), ),
        'o': (('cp', 25, '1000-4000'), ('sp', 20, '1000-3000')),
        'p': (('sp', 30, '1000-6000'), ('ep', 25, '1000-2000')),
        'q': (('gems', 50, '1-4'), ),
        'r': (('gp', 40, '2000-8000'), ('pp', 50, '10-60x100'), ('gems', 55, '4-32'), ('jewelry', 45, '1-12')),
        's': (('magic', 40, (entry_2d4_potions, )), ),
        't': (('magic', 50, (entry_d4_scrolls, )), ),
        'u': (('gems', 90, '10-80'), ('jewelry', 80, '5-30'), ('magic', 70, (entry_dmg_each, ))),
        'v': (('magic', 85, (entry_dmg_each_twice, )), ),
        'w': (('gp', 60, '5000-30000'), ('pp', 15, '1-8x100'), ('gems', 60, '10-80'), ('jewelry', 50, '5-40'), ('magic', 55, (entry_dmg_map, ))),
        'x': (('magic', 60, (entry_misc, entry_potion)), ),
        'y': (('gp', 70, '2000-12000'), ),
        'z': (('cp', 20, '1000-3000'), ('sp', 25, '1000-4000'), ('ep', 25, '1000-4000'), ('gp', 30, '1000-4000'), ('pp', 30, '1-6x100'),
              ('gems', 55, '10-60'), ('jewelry', 50, '5-30'), ('magic', 50, (entry_item, entry_item, entry_item))),
        }
    # III. Magic Items.
    item = [
        (20, 'Potion', entry_potion),
        (35, 'Scroll', entry_scroll),
        (40, 'Ring', entry_ring),
        (45, 'Rod/Staff/Wand', entry_wsr),
        (60, 'Misc. Magic', entry_misc),
        (75, 'Armor & Shield', entry_armor),
        (86, 'Sword', entry_sword),
        (100, 'Misc. Weapon', entry_weapon),
        ]
    # III.A Potions. Book: (F) fighters only.
    potion = [
        (3, 'Animal Control (<animal_control>)'),
        (6, 'Clairaudience'),
        (9, 'Clairvoyance'),
        (12, 'Climbing'),
        (15, 'Delusion'),
        (18, 'Diminution'),
        (20, 'Dragon Control (<dragon_control>)'),
        (23, 'ESP'),
        (26, 'Extra-Healing'),
        (29, 'Fire Resistance'),
        (32, 'Flying'),
        (34, 'Gaseous Form'),
        (36, 'Giant Control (<giant>)'),
        (39, 'Giant Strength (<giant_strength>, F)'),
        (41, 'Growth'),
        (47, 'Healing'),
        (49, 'Heroism (F)'),
        (51, 'Human Control (<human>)'),
        (54, 'Invisibility'),
        (57, 'Invulnerability (F)'),
        (60, 'Levitation'),
        (63, 'Longevity'),
        (66, 'Oil of Etherealness'),
        (69, 'Oil of Slipperiness'),
        (72, 'Philter of Love'),
        (75, 'Philter of Persuasiveness'),
        (78, 'Plant Control'),
        (81, 'Polymorph (self)'),
        (84, 'Poison'),
        (87, 'Speed'),
        (90, 'Super-Heroism (F)'),
        (93, 'Sweet Water'),
        (96, 'Treasure Finding'),
        (97, 'Undead Control (<undead>)'),
        (100, 'Water Breathing'),
        ]
    # d20.
    _random_animal_control = [
        (4, 'mammal/marsupial'), (8, 'avian'), (12, 'reptile/amphibian'), (15, 'fish'),
        (17, 'mammal/marsupial/avian'), (19, 'reptile/amphibian/fish'), (20, 'all of the above'),
        ]
    # d20.
    _random_dragon_control = [
        (2, 'white'), (4, 'black'), (7, 'green'), (9, 'blue'), (10, 'red'), (12, 'brass'), (14, 'copper'), (15, 'bronze'),
        (16, 'silver'), (17, 'gold'), (19, 'evil dragons: black, blue, green, red, white'),
        (20, 'good dragons: brass, bronze, copper, gold, silver'),
        ]
    # d20.
    _random_giant = [(5, 'hill giant'), (9, 'stone giant'), (13, 'frost giant'), (17, 'fire giant'), (19, 'cloud giant'), (20, 'storm giant')]
    # d20.
    _random_giant_strength = [(6, 'hill giant'), (10, 'stone giant'), (14, 'frost giant'), (17, 'fire giant'), (19, 'cloud giant'), (20, 'storm giant')]
    # d20.
    _random_human = [
        (2, 'dwarves'), (4, 'elves/half-elves'), (6, 'gnomes'), (8, 'halflings'), (10, 'half-orcs'), (16, 'humans'),
        (19, 'humanoids (gnolls, orcs, goblins, etc.)'), (20, 'elves, half-elves and humans'),
        ]
    # d10.
    _random_undead = [
        (1, 'ghasts'), (2, 'ghosts'), (3, 'ghouls'), (4, 'shadows'), (5, 'skeletons'),
        (6, 'spectres'), (7, 'wights'), (8, 'wraiths'), (9, 'vampires'), (10, 'zombies'),
        ]
    # III.B Scrolls. Spell rows are 'N spells|levels|clerical levels' (the same for all when there is only one), see scroll_spells.
    scroll = [
        (10, '1 spell|1-4'),
        (16, '1 spell|1-6'),
        (19, '1 spell|2-9|2-7'),
        (24, '2 spells|1-4'),
        (27, '2 spells|1-8|1-6'),
        (32, '3 spells|1-4'),
        (35, '3 spells|2-9|2-7'),
        (39, '4 spells|1-6'),
        (42, '4 spells|1-8|1-6'),
        (46, '5 spells|1-6'),
        (49, '5 spells|1-8|1-6'),
        (52, '6 spells|1-6'),
        (54, '6 spells|3-8|3-6'),
        (57, '7 spells|1-8'),
        (59, '7 spells|2-9'),
        (60, '7 spells|4-9|4-7'),
        (62, 'Protection from Demons'),
        (64, 'Protection from Devils'),
        (70, 'Protection from <protection_elementals>'),
        (76, 'Protection from <protection_lycanthropes>'),
        (82, 'Protection from Magic'),
        (87, 'Protection from Petrification'),
        (92, 'Protection from Possession'),
        (97, 'Protection from Undead'),
        (100, 'Curse'),
        ]
    # d%.
    _random_protection_elementals = [
        (15, 'Air Elementals (including aerial servants, djinn, invisible stalkers, and wind walkers)'),
        (30, 'Earth Elementals (including xorn)'),
        (45, 'Fire Elementals (including efreeti and salamanders)'),
        (60, 'Water Elementals (including tritons and water weirds)'),
        (100, 'All Elementals'),
        ]
    # d%.
    _random_protection_lycanthropes = [
        (5, 'Werebears'), (10, 'Wereboars'), (20, 'Wererats'), (25, 'Weretigers'), (40, 'Werewolves'),
        (98, 'all Lycanthropes'), (100, 'Shape-Changers'),
        ]
    # Cursed scroll, "suggested curses".
    scroll_curse = [
        (25, 'Reader polymorphed to monster of equal level which attacks any creatures nearby'),
        (30, 'Reader turned to liquid and drains away'),
        (40, "Reader and all within 20' radius transported 200 to 1,200 miles in a random direction"),
        (50, "Reader and all in 20' radius transported to another planet, plane or continuum"),
        (75, 'Disease fatal to reader in 2-8 turns unless cured'),
        (90, 'Explosive runes'),
        (99, 'Magic item nearby is "de-magicked"'),
        (100, 'Randomly rolled spell affects reader at 12th level of magic-user'),
        ]
    # III.C Rings. ¶ Rows with <details> are rolled in place.
    ring = [
        (6, 'Contrariness (<contrariness>)'),
        (12, 'Delusion'),
        (14, 'Djinni Summoning'),
        (15, 'Elemental Command (<element>)'),
        (21, 'Feather Falling'),
        (27, 'Fire Resistance'),
        (30, 'Free Action'),
        (33, 'Human Influence'),
        (40, 'Invisibility'),
        (43, 'Mammal Control'),
        (44, 'Multiple Wishes (2-8 wishes)'),
        (60, 'Protection <protection>'),
        (61, '<regeneration>'),
        (63, 'Shooting Stars'),
        (65, 'Spell Storing (<spells>)'),
        (69, 'Spell Turning'),
        (75, 'Swimming'),
        (77, 'Telekinesis'),
        (79, 'Three Wishes'),
        (85, 'Warmth'),
        (90, 'Water Walking'),
        (98, 'Weakness'),
        (99, 'Wizardry (M)'),
        (100, 'X-Ray Vision'),
        ]
    # d%.
    _random_contrariness = [(20, 'Flying'), (40, 'Invisibility'), (60, 'Levitation'), (70, 'Shocking Grasp'), (80, 'Spell Turning'), (100, 'Strength 18/00')]
    # d4.
    _random_element = [(1, 'Air'), (2, 'Earth'), (3, 'Fire'), (4, 'Water')]
    # d%.
    _random_protection = [
        (70, '+1'), (82, '+2'), (83, "+2, 5' radius protection"), (90, '+3'), (91, "+3, 5' radius protection"),
        (97, '+4 on AC, +2 on saving throws'), (100, '+6 on AC, +1 on saving throws'),
        ]
    # d%.
    _random_regeneration = [(90, 'Regeneration'), (100, 'Vampiric Regeneration')]
    # III.D Rods, Staves & Wands. Book: (C) clerics only, (M) magic-users, (T) thieves, (F) fighters.
    wsr = [
        (3, 'Rod of Absorption (C, M)'),
        (4, 'Rod of Beguiling (C, M, T)'),
        (14, 'Rod of Cancellation (any)'),
        (16, 'Rod of Lordly Might (F)'),
        (17, 'Rod of Resurrection (C)'),
        (18, 'Rod of Rulership (any)'),
        (19, 'Rod of Smiting (C, F)'),
        (20, 'Staff of Command (C, M)'),
        (22, 'Staff of Curing (C)'),
        (23, 'Staff of the Magi (M)'),
        (24, 'Staff of Power (M)'),
        (27, 'Staff of the Serpent (C)'),
        (31, 'Staff of Striking (C, M)'),
        (33, 'Staff of Withering (C)'),
        (34, 'Wand of Conjuration (M)'),
        (38, 'Wand of Enemy Detection (any)'),
        (41, 'Wand of Fear (C, M)'),
        (44, 'Wand of Fire (M)'),
        (47, 'Wand of Frost (M)'),
        (52, 'Wand of Illumination (any)'),
        (56, 'Wand of Illusion (M)'),
        (59, 'Wand of Lightning (M)'),
        (68, 'Wand of Magic Detection (any)'),
        (73, 'Wand of Metal & Mineral Detection (any)'),
        (78, 'Wand of Magic Missiles (any)'),
        (86, 'Wand of Negation (any)'),
        (89, 'Wand of Paralyzation (M)'),
        (92, 'Wand of Polymorphing (M)'),
        (94, 'Wand of Secret Door & Trap Location (any)'),
        (100, 'Wand of Wonder (any)'),
        ]
    # III.E Miscellaneous Magic: Table 1-5, each 3% of Magic Items (46-60), so equally likely.
    misc_1 = [
        (2, 'Alchemy Jug'),
        (4, 'Amulet of Inescapable Location'),
        (5, 'Amulet of Life Protection'),
        (7, 'Amulet of the Planes'),
        (11, 'Amulet of Proof Against Detection and Location'),
        (13, 'Apparatus of Kwalish'),
        (16, 'Arrow of Direction'),
        (17, 'Artifact or Relic (<artifact>)'),
        (20, 'Bag of Beans'),
        (21, 'Bag of Devouring'),
        (26, 'Bag of Holding (<bag_of_holding>)'),
        (27, 'Bag of Transmuting'),
        (29, 'Bag of Tricks (<bag_of_tricks>)'),
        (31, 'Beaker of Plentiful Potions (<beaker>)'),
        (32, 'Boat, Folding'),
        (33, 'Book of Exalted Deeds (C)'),
        (34, 'Book of Infinite Spells'),
        (35, 'Book of Vile Darkness (C)'),
        (36, 'Boots of Dancing'),
        (42, 'Boots of Elvenkind'),
        (47, 'Boots of Levitation'),
        (51, 'Boots of Speed'),
        (55, 'Boots of Striding and Springing'),
        (58, 'Bowl Commanding Water Elementals (M)'),
        (59, 'Bowl of Watery Death (M)'),
        (79, 'Bracers of Defense (<bracers>)'),
        (81, 'Bracers of Defenselessness'),
        (84, 'Brazier Commanding Fire Elementals (M)'),
        (85, 'Brazier of Sleep Smoke (M)'),
        (92, 'Brooch of Shielding'),
        (93, 'Broom of Animated Attack'),
        (98, 'Broom of Flying'),
        (100, "Bucknard's Everfull Purse (<purse>)"),
        ]
    misc_2 = [
        (6, 'Candle of Invocation (C)'),
        (8, 'Carpet of Flying (<carpet>)'),
        (10, 'Censer Controlling Air Elementals (M)'),
        (11, 'Censer of Summoning Hostile Air Elementals (M)'),
        (13, 'Chime of Opening [<chime>]'),
        (14, 'Chime of Hunger'),
        (18, 'Cloak of Displacement'),
        (27, 'Cloak of Elvenkind'),
        (30, 'Cloak of Manta Ray'),
        (32, 'Cloak of Poisonousness'),
        (55, 'Cloak of Protection (<cloak>)'),
        (60, 'Crystal Ball (M) (<crystal_ball>)'),
        (61, 'Crystal Hypnosis Ball (M)'),
        (63, 'Cube of Force'),
        (65, 'Cube of Frost Resistance'),
        (67, 'Cubic Gate'),
        (69, "Daern's Instant Fortress"),
        (72, 'Decanter of Endless Water'),
        (76, 'Deck of Many Things (<deck>)'),
        (77, 'Drums of Deafening'),
        (79, 'Drums of Panic'),
        (85, 'Dust of Appearance'),
        (91, 'Dust of Disappearance'),
        (92, 'Dust of Sneezing and Choking'),
        (93, 'Efreeti Bottle'),
        (94, 'Eversmoking Bottle'),
        (95, 'Eyes of Charming (M)'),
        (97, 'Eyes of the Eagle'),
        (99, 'Eyes of Minute Seeing'),
        (100, 'Eyes of Petrification'),
        ]
    misc_3 = [
        (15, 'Figurine of Wondrous Power (<figurine>)'),
        (16, 'Flask of Curses'),
        (18, 'Gauntlets of Dexterity'),
        (20, 'Gauntlets of Fumbling'),
        (22, 'Gauntlets of Ogre Power (C, F, T)'),
        (25, 'Gauntlets of Swimming and Climbing (C, F, T)'),
        (26, 'Gem of Brightness'),
        (27, 'Gem of Seeing'),
        (28, 'Girdle of Femininity/Masculinity (C, F, T)'),
        (29, 'Girdle of Giant Strength (C, F, T) (<girdle>)'),
        (30, 'Helm of Brilliance'),
        (35, 'Helm of Comprehending Languages & Reading Magic'),
        (37, 'Helm of Opposite Alignment'),
        (39, 'Helm of Telepathy'),
        (40, 'Helm of Teleportation'),
        (45, 'Helm of Underwater Action'),
        (46, 'Horn of Blasting'),
        (48, 'Horn of Bubbles'),
        (49, 'Horn of Collapsing'),
        (53, 'Horn of the Tritons (C, F)'),
        (60, 'Horn of Valhalla (<valhalla>)'),
        (63, 'Horseshoes of Speed'),
        (65, 'Horseshoes of a Zephyr'),
        (70, 'Incense of Meditation (C)'),
        (71, 'Incense of Obsession (C)'),
        (72, 'Ioun Stones (<ioun>)'),
        (78, 'Instrument of the Bards (<instrument>)'),
        (80, 'Iron Flask (<flask>)'),
        (85, 'Javelin of Lightning (F)'),
        (90, 'Javelin of Piercing (F)'),
        (91, 'Jewel of Attacks'),
        (92, 'Jewel of Flawlessness'),
        (100, "Keoghtom's Ointment"),
        ]
    misc_4 = [
        (1, 'Libram of Gainful Conjuration (M)'),
        (2, 'Libram of Ineffable Damnation (M)'),
        (3, 'Libram of Silver Magic (M)'),
        (4, 'Lyre of Building'),
        (5, 'Manual of Bodily Health'),
        (6, 'Manual of Gainful Exercise'),
        (7, 'Manual of Golems (C, M) (<golem>)'),
        (8, 'Manual of Puissant Skill at Arms (F)'),
        (9, 'Manual of Quickness of Action'),
        (10, 'Manual of Stealthy Pilfering (T)'),
        (11, 'Mattock of the Titans (F)'),
        (12, 'Maul of the Titans'),
        (15, 'Medallion of ESP (<medallion>)'),
        (17, 'Medallion of Thought Projection'),
        (18, 'Mirror of Life Trapping (M)'),
        (19, 'Mirror of Mental Prowess'),
        (20, 'Mirror of Opposition'),
        (23, 'Necklace of Adaptation'),
        (27, 'Necklace of Missiles (<missiles>)'),
        (33, 'Necklace of Prayer Beads (C) (<beads>)'),
        (35, 'Necklace of Strangulation'),
        (38, 'Net of Entrapment (C, F, T)'),
        (42, 'Net of Snaring (C, F, T)'),
        (44, "Nolzur's Marvelous Pigments"),
        (46, 'Pearl of Power (M) (<pearl>)'),
        (48, 'Pearl of Wisdom (C)'),
        (50, 'Periapt of Foul Rotting'),
        (53, 'Periapt of Health'),
        (60, 'Periapt of Proof Against Poison (<periapt>)'),
        (64, 'Periapt of Wound Closure'),
        (70, 'Phylactery of Faithfulness (C)'),
        (74, 'Phylactery of Long Years (C)'),
        (76, 'Phylactery of Monstrous Attention (C)'),
        (84, 'Pipes of the Sewers'),
        (85, 'Portable Hole'),
        (100, "Quaal's Feather Token (<feather_token>)"),
        ]
    misc_5 = [
        (1, 'Robe of the Archmagi (M) (<archmagi>)'),
        (8, 'Robe of Blending'),
        (9, 'Robe of Eyes'),
        (10, 'Robe of Powerlessness (M)'),
        (11, 'Robe of Scintillating Colors (C, M)'),
        (19, 'Robe of Useful Items (M) (<useful_items>)'),
        (25, 'Rope of Climbing'),
        (27, 'Rope of Constriction'),
        (31, 'Rope of Entanglement'),
        (32, 'Rug of Smothering'),
        (33, 'Rug of Welcome (M)'),
        (34, 'Saw of Mighty Cutting (F)'),
        (35, 'Scarab of Death'),
        (38, 'Scarab of Enraging Enemies'),
        (40, 'Scarab of Insanity'),
        (46, 'Scarab of Protection'),
        (47, 'Spade of Colossal Excavation (F)'),
        (48, 'Sphere of Annihilation (M)'),
        (50, 'Stone of Controlling Earth Elementals'),
        (52, 'Stone of Good Luck (Luckstone)'),
        (54, 'Stone of Weight (Loadstone)'),
        (57, 'Talisman of Pure Good (C)'),
        (58, 'Talisman of the Sphere (M)'),
        (60, 'Talisman of Ultimate Evil (C)'),
        (66, 'Talisman of Zagy'),
        (67, 'Tome of Clear Thought'),
        (68, 'Tome of Leadership and Influence'),
        (69, 'Tome of Understanding'),
        (76, 'Trident of Fish Command (C, F, T)'),
        (78, 'Trident of Submission (F)'),
        (83, 'Trident of Warning (C, F, T)'),
        (85, 'Trident of Yearning'),
        (87, 'Vacuous Grimoire'),
        (90, 'Well of Many Worlds'),
        (100, 'Wings of Flying'),
        ]
    misc = [(20, misc_1), (40, misc_2), (60, misc_3), (80, misc_4), (100, misc_5)]
    # Special: Artifacts and Relics (names only, the book has the DM assign powers).
    _random_artifact = [
        (1, 'Axe of the Dwarvish Lords'),
        (2, "Baba Yaga's Hut"),
        (4, 'Codex of the Infinite Planes'),
        (20, 'Crown of Might'),
        (21, 'Crystal of the Ebon Flame'),
        (22, "Cup and Talisman of Al'Akbar"),
        (24, 'Eye of Vecna'),
        (25, 'Hand of Vecna'),
        (26, "Heward's Mystical Organ"),
        (27, 'Horn of Change'),
        (29, 'Invulnerable Coat of Arnd'),
        (31, 'Iron Flask of Tuerny the Merciless'),
        (32, 'Jocinth of Inestimable Beauty'),
        (33, "Johydee's Mask"),
        (35, "Kuroth's Quill"),
        (37, 'Mace of Cuthbert'),
        (38, 'Machine of Lum the Mad'),
        (40, 'Mighty Servant of Leuk-O'),
        (47, 'Orb of the Dragonkind'),
        (63, 'Orb of Might'),
        (64, "Queen Ehlissa's Marvelous Nightingale"),
        (66, "Recorder of Ye'Cind"),
        (68, 'Ring of Gaxx'),
        (74, 'Rod of Seven Parts'),
        (91, 'Sceptre of Might'),
        (92, 'Sword of Kas'),
        (98, 'Teeth of Dahlver-Nar'),
        (99, 'Throne of the Gods'),
        (100, 'Wand of Orcus'),
        ]
    # III.F Armor and Shield.
    armor = [
        (5, 'Chain Mail +1 (<size>)'),
        (9, 'Chain Mail +2 (<size>)'),
        (11, 'Chain Mail +3 (<size>)'),
        (19, 'Leather Armor +1 (<size>)'),
        (26, 'Plate Mail +1 (<size>)'),
        (32, 'Plate Mail +2 (<size>)'),
        (35, 'Plate Mail +3 (<size>)'),
        (37, 'Plate Mail +4 (<size>)'),
        (38, 'Plate Mail +5 (<size>)'),
        (39, 'Plate Mail of Etherealness (<size>)'),
        (44, 'Plate Mail of Vulnerability (<size>)'),
        (50, 'Ring Mail +1 (<size>)'),
        (55, 'Scale Mail +1 (<size>)'),
        (59, 'Scale Mail +2 (<size>)'),
        (63, 'Splint Mail +1 (<size>)'),
        (66, 'Splint Mail +2 (<size>)'),
        (68, 'Splint Mail +3 (<size>)'),
        (69, 'Splint Mail +4 (<size>)'),
        (75, 'Studded Leather +1 (<size>)'),
        (84, 'Shield +1 (<size>)'),
        (89, 'Shield +2 (<size>)'),
        (93, 'Shield +3 (<size>)'),
        (95, 'Shield +4 (<size>)'),
        (96, 'Shield +5 (<size>)'),
        (97, 'Shield, large, +1, +4 vs. missiles (<size>)'),
        (100, 'Shield -1, missile attractor (<size>)'),
        ]
    # d%. Book: "65% of all armor is man-sized, 20% is elf-sized, 10% is dwarf-sized, and but 5% gnome or halfling-sized".
    _random_size = [(65, 'man-sized'), (85, 'elf-sized'), (95, 'dwarf-sized'), (100, 'gnome or halfling-sized')]
    # III.G Swords. Book: "70% of swords are longswords, 20% are broadswords, 5% are short (small) swords,
    # 4% are bastard swords, 1% are two-handed swords", see _sword_type.
    sword = [
        (25, 'Sword +1'),
        (30, 'Sword +1, +2 vs. magic-using & enchanted creatures'),
        (35, 'Sword +1, +3 vs. lycanthropes & shape changers'),
        (40, 'Sword +1, +3 vs. regenerating creatures'),
        (45, 'Sword +1, +4 vs. reptiles'),
        (49, 'Sword +1, flame tongue: +2 vs. regenerating creatures, +3 vs. cold-using, inflammable, or avian creatures, +4 vs. undead'),
        (50, 'Sword +1, luck blade'),
        (58, 'Sword +2'),
        (62, 'Sword +2, giant slayer'),
        (66, 'Sword +2, dragon slayer'),
        (67, 'Sword +2, nine lives stealer'),
        (71, 'Sword +3'),
        (74, 'Sword +3, frost brand: +6 vs. fire using/dwelling creatures'),
        (76, 'Sword +4'),
        (77, 'Sword +4, defender'),
        (78, 'Sword +5'),
        (79, 'Sword +5, defender'),
        (80, 'Sword +5, holy avenger'),
        (81, 'Sword of Dancing'),
        (82, 'Sword of Wounding'),
        (83, 'Sword of Life Stealing'),
        (84, 'Sword of Sharpness'),
        (85, 'Sword, vorpal weapon'),
        (90, 'Sword +1, cursed'),
        (95, 'Sword -2, cursed'),
        (100, 'Sword, cursed berserking'),
        ]
    _sword_type = [(70, 'Longsword'), (90, 'Broadsword'), (95, 'Short Sword'), (99, 'Bastard Sword'), (100, 'Two-handed Sword')]
    # Ego points of the sword's pluses, see the class docstring: Table 7 "each + of sword", the example gives the
    # Flame Tongue +1/+4 as 5. Judgement: Dancing, Wounding, Sharpness (+1), Life Stealing (+2) and Vorpal (+3) double
    # their plus, as swords with extra powers and no extra pluses; the cursed swords' ego is that of their plus.
    _sword_ego = {
        'Sword +1': 1,
        'Sword +1, +2 vs. magic-using & enchanted creatures': 3,
        'Sword +1, +3 vs. lycanthropes & shape changers': 4,
        'Sword +1, +3 vs. regenerating creatures': 4,
        'Sword +1, +4 vs. reptiles': 5,
        'Sword +1, flame tongue: +2 vs. regenerating creatures, +3 vs. cold-using, inflammable, or avian creatures, +4 vs. undead': 5,
        'Sword +1, luck blade': 2,
        'Sword +2': 2,
        'Sword +2, giant slayer': 5,
        'Sword +2, dragon slayer': 6,
        'Sword +2, nine lives stealer': 4,
        'Sword +3': 3,
        'Sword +3, frost brand: +6 vs. fire using/dwelling creatures': 9,
        'Sword +4': 4,
        'Sword +4, defender': 8,
        'Sword +5': 5,
        'Sword +5, defender': 10,
        'Sword +5, holy avenger': 10,
        'Sword of Dancing': 2,
        'Sword of Wounding': 2,
        'Sword of Life Stealing': 4,
        'Sword of Sharpness': 2,
        'Sword, vorpal weapon': 6,
        'Sword +1, cursed': 1,
        'Sword -2, cursed': 0,
        'Sword, cursed berserking': 2,
        }
    # Unusual Swords, Table 1 for d% 76-00: (highest roll, intelligence, primary abilities, communication).
    _sword_intelligence = [
        (83, 12, 1, 'semi-empathy'),
        (89, 13, 2, 'empathy'),
        (94, 14, 2, 'speech'),
        (97, 15, 3, 'speech'),
        (99, 16, 3, 'speech, reads languages and maps of any non-magical sort'),
        (100, 17, 3, 'speech and telepathy, reads languages and magical writings'),
        ]
    # Table 2, alignment. Judgement: "Neutral" is the book's neutral (absolute).
    _sword_alignment = [
        (5, 'Chaotic Good'), (15, 'Chaotic Neutral'), (20, 'Chaotic Evil'), (25, 'Neutral Evil'), (30, 'Lawful Evil'),
        (55, 'Lawful Good'), (60, 'Lawful Neutral'), (80, 'Neutral'), (100, 'Neutral Good'),
        ]
    # Table 3, primary abilities, rolls above 92 are handled by _sword_abilities.
    _sword_primary = [
        (11, 'detect "elevator"/shifting rooms/walls in a 1" radius'),
        (22, 'detect sloping passages in a 1" radius'),
        (33, 'detect traps of large size in a 1" radius'),
        (44, 'detect evil/good in a 1" radius'),
        (55, 'detect precious metals, kind, and amount in a 2" radius'),
        (66, 'detect gems, kind, and number in a 1/2" radius'),
        (77, 'detect magic in a 1" radius'),
        (82, 'detect secret doors in a 1/2" radius'),
        (87, 'detect invisible objects in a 1" radius'),
        (92, 'locate object in a 12" radius'),
        ]
    # Table 4, extraordinary powers, rolls above 94 are handled by _sword_powers.
    _sword_extraordinary = [
        (7, 'charm person on contact, 3 times/day'),
        (15, 'clairaudience, 3" range, 3 times/day, 1 round per use'),
        (22, 'clairvoyance, 3" range, 3 times/day, 1 round per use'),
        (28, 'determine directions and depth, 2 times/day'),
        (34, 'ESP, 3" range, 3 times/day, 1 round per use'),
        (41, 'flying, 12"/turn, 1 hour/day'),
        (47, 'heal, 1 time/day'),
        (54, 'illusion, 12" range, 2 times/day, as the wand'),
        (61, 'levitation, 1 turn duration, 3 times/day, at 6th level of magic use'),
        (67, 'strength, 1 time/day (upon wielder only)'),
        (75, 'telekinesis, 2,500 g.p. wt. maximum, 2 times/day, 1 round each use'),
        (81, 'telepathy, 6" range, 2 times/day'),
        (88, 'teleportation, 1 time/day, 6,000 g.p. wt. maximum, 2 segments to activate'),
        (94, 'x-ray vision, 4" range, 2 times/day, 1 turn per use'),
        ]
    # Table 5.A, special purposes.
    _sword_purpose = [
        (10, 'defeat/slay diametrically opposed alignment'),
        (20, 'kill clerics'),
        (30, 'kill fighters'),
        (40, 'kill magic-users'),
        (50, 'kill thieves'),
        (55, 'kill bards/monks'),
        (65, 'overthrow law and/or chaos'),
        (75, 'slay good and/or evil'),
        (100, 'slay non-human monsters'),
        ]
    # Table 5.B, special purpose power, the opponent saves vs. magic on a hit except for the last.
    _sword_purpose_power = [
        (10, 'blindness for 2-12 rounds'),
        (20, 'confusion for 2-12 rounds'),
        (25, 'disintegrate'),
        (55, 'fear for 1-4 rounds'),
        (65, 'insanity for 1-4 rounds'),
        (80, 'paralysis for 1-4 rounds'),
        (100, '+2 on saving throws, -1 on each die of damage sustained'),
        ]
    # Table 6, languages other than alignment, rolls above 99 are handled by _sword_language_count.
    _sword_languages = [(40, 1), (70, 2), (85, 3), (95, 4), (99, 5)]
    # III.H Miscellaneous Weapons. Quantities are N-M dice.
    weapon = [
        (8, '2-24 Arrows +1'),
        (12, '2-16 Arrows +2'),
        (14, '2-12 Arrows +3'),
        (15, 'Arrow of Slaying (<slaying>)'),
        (20, 'Axe +1'),
        (22, 'Axe +2'),
        (23, 'Axe +2, Throwing'),
        (24, 'Axe +3'),
        (27, 'Battle Axe +1'),
        (32, '2-20 Bolts +2'),
        (35, 'Bow +1'),
        (36, 'Crossbow of Accuracy, +3'),
        (37, 'Crossbow of Distance'),
        (38, 'Crossbow of Speed'),
        (46, 'Dagger +1, +2 vs. creatures smaller than man-sized'),
        (50, 'Dagger +2, +3 vs. creatures larger than man-sized'),
        (51, 'Dagger of Venom'),
        (56, 'Flail +1'),
        (60, 'Hammer +1'),
        (62, 'Hammer +2'),
        (63, 'Hammer +3, Dwarven Thrower'),
        (64, 'Hammer of Thunderbolts'),
        (67, 'Javelin +2'),
        (72, 'Mace +1'),
        (75, 'Mace +2'),
        (76, 'Mace of Disruption'),
        (77, 'Mace +4'),
        (80, 'Military Pick +1'),
        (83, 'Morning Star +1'),
        (88, 'Scimitar +2'),
        (89, 'Sling of Seeking +2'),
        (94, 'Spear +1'),
        (96, 'Spear +2'),
        (97, 'Spear +3'),
        (99, 'Spear, Cursed Backbiter'),
        (100, 'Trident (Military Fork) +3'),
        ]
    # d24, "the following list comprises only a portion of the possible kinds" of Arrow of Slaying.
    _random_slaying = [
        (1, 'arachnids'), (2, 'avians'), (3, 'bards'), (4, 'clerics'), (5, 'demons'), (6, 'devils'), (7, 'dragons'),
        (8, 'druids'), (9, 'elementals'), (10, 'fighters'), (11, 'giants'), (12, 'golems'), (13, 'illusionists'),
        (14, 'ki-rin'), (15, 'magic-users'), (16, 'mammals'), (17, 'monks'), (18, 'paladins'), (19, 'rangers'),
        (20, 'reptiles'), (21, 'sea monsters'), (22, 'thieves'), (23, 'titans'), (24, 'undead'),
        ]
    # Miscellaneous magic details.
    # d%.
    _random_bag_of_holding = [
        (30, 'weighs 15 lb, holds 250 lb and 30 cubic feet'),
        (70, 'weighs 15 lb, holds 500 lb and 70 cubic feet'),
        (90, 'weighs 35 lb, holds 1,000 lb and 150 cubic feet'),
        (100, 'weighs 60 lb, holds 1,500 lb and 250 cubic feet'),
        ]
    # d10, 1-5, 6-8 and 9-0 each summon one of 8 animals (d8).
    _random_bag_of_tricks = [
        (5, 'weasel, skunk, badger, wolf, giant lynx, wolverine, boar, giant stag'),
        (8, 'rat, owl, dog, goat, ram, bull, bear, lion'),
        (10, 'jackal, eagle, baboon, ostrich, leopard, jaguar, buffalo, tiger'),
        ]
    # d%, armor class.
    _random_bracers = [(5, 'AC 8'), (15, 'AC 7'), (35, 'AC 6'), (50, 'AC 5'), (70, 'AC 4'), (85, 'AC 3'), (100, 'AC 2')]
    # d%, 26 each per day.
    _random_purse = [
        (50, '26 sp, 26 ep, 26 gp'),
        (90, '26 cp, 26 ep, 26 pp'),
        (100, '26 cp, 26 ep, 26 gems of 10gp base value, to 100gp'),
        ]
    # d%.
    _random_carpet = [
        (20, "3' x 5', 1 person, 42\" speed"),
        (55, "4' x 6', 2 persons, 36\" speed"),
        (80, "5' x 7', 3 persons, 30\" speed"),
        (100, "6' x 9', 4 persons, 24\" speed"),
        ]
    # d%, plus of protection.
    _random_cloak = [(35, '+1'), (65, '+2'), (85, '+3'), (95, '+4'), (100, '+5')]
    # d%.
    _random_crystal_ball = [(50, 'plain'), (75, 'with clairaudience'), (90, 'with ESP'), (100, 'with telepathy, communication only')]
    # d%, 13 or 22 plaques.
    _random_deck = [(75, '13 plaques'), (100, '22 plaques')]
    # d%.
    _figurine = [
        (15, 'ebony fly'), (30, 'golden lions (pair)'), (40, 'ivory goats (trio)'), (55, 'marble elephant: <elephant>'),
        (65, 'obsidian steed'), (85, 'onyx dog'), (100, 'serpentine owl'),
        ]
    # d%.
    _random_elephant = [(50, 'Asiatic (elephant)'), (90, 'African (loxodont)'), (93, 'prehistoric (mammoth)'), (100, 'prehistoric (mastodon)')]
    # d%.
    _random_girdle = [(30, 'hill giant'), (50, 'stone giant'), (70, 'frost giant'), (85, 'fire giant'), (95, 'cloud giant'), (100, 'storm giant')]
    # d20.
    _random_valhalla = [
        (8, 'silver, 4 to 10 berserkers of 2nd level, any class'),
        (15, 'brass, 3 to 9 berserkers of 3rd level, C, F, T'),
        (18, 'bronze, 2 to 8 berserkers of 4th level, C, F'),
        (20, 'iron, 2 to 5 berserkers of 5th level, F'),
        ]
    # d20.
    _random_instrument = [
        (5, 'Fochlucan Bandore'), (9, 'Mac-Fuirmidh Cittern'), (12, 'Doss Lute'), (15, 'Canaith Mandolin'),
        (17, 'Cli Lyre'), (19, 'Anstruth Harp'), (20, 'Ollamh Harp'),
        ]
    # d%.
    _random_flask = [
        (50, 'empty'), (54, 'air elemental'), (56, 'demon (type I-III)'), (57, 'demon (type IV-VI)'), (59, 'devil (lesser)'),
        (60, 'devil (greater)'), (65, 'djinni'), (69, 'earth elemental'), (72, 'efreeti'), (76, 'fire elemental'),
        (81, 'invisible stalker'), (83, 'mezzodaemon'), (85, 'night hag'), (86, 'nycadaemon'), (89, 'rakshasa'),
        (93, 'salamander'), (97, 'water elemental'), (99, 'wind walker'), (100, 'xorn'),
        ]
    # d20, burned out from 15.
    _ioun_stone = [
        (1, 'pale blue rhomboid: adds 1 point to strength (18 maximum)'),
        (2, 'scarlet & blue sphere: adds 1 point to intelligence (18 maximum)'),
        (3, 'incandescent blue sphere: adds 1 point to wisdom (18 maximum)'),
        (4, 'deep red sphere: adds 1 point to dexterity (18 maximum)'),
        (5, 'pink rhomboid: adds 1 point to constitution (18 maximum)'),
        (6, 'pink & green sphere: adds 1 point to charisma (18 maximum)'),
        (7, 'pale green prism: adds 1 level of experience'),
        (8, 'clear spindle: sustains person without food or water'),
        (9, 'iridescent spindle: sustains person without air'),
        (10, 'pearly white spindle: regenerates 1 hp of damage/turn'),
        (11, 'pale lavender ellipsoid: absorbs spells up to 4th level, burns out after 1-4x10 levels'),
        (12, 'lavender & green ellipsoid: absorbs spells up to 8th level, burns out after 2-8x10 levels'),
        (13, 'vibrant purple prism: stores 2-12 levels of spells'),
        (14, 'dusty rose prism: gives +1 protection'),
        (20, 'dull gray, any shape: burned out'),
        ]
    # d20.
    _random_golem = [(5, 'clay'), (17, 'flesh'), (18, 'iron'), (20, 'stone')]
    # d20.
    _random_medallion = [(15, "30' range"), (18, "30' range with empathy"), (19, "60' range"), (20, "90' range")]
    # d20, missiles and the Hit Dice of their fireballs.
    _random_missiles = [
        (4, '1 x 5HD, 2 x 3HD'),
        (8, '1 x 6HD, 2 x 4HD, 2 x 2HD'),
        (12, '1 x 7HD, 2 x 5HD, 4 x 3HD'),
        (16, '1 x 8HD, 2 x 6HD, 2 x 4HD, 4 x 2HD'),
        (18, '1 x 9HD, 2 x 7HD, 2 x 5HD, 2 x 3HD'),
        (19, '1 x 10HD, 2 x 8HD, 2 x 6HD, 4 x 4HD'),
        (20, '1 x 11HD, 2 x 9HD, 2 x 7HD, 2 x 5HD, 2 x 3HD'),
        ]
    # d20, special beads.
    _prayer_bead = [(5, 'atonement'), (10, 'blessing'), (15, 'curing'), (17, 'karma'), (18, 'summons'), (20, 'wind walking')]
    # d%, the level of spell recalled by the pearl, 00 is see _random_pearl.
    _pearl_level = [(25, '1st'), (45, '2nd'), (60, '3rd'), (75, '4th'), (85, '5th'), (92, '6th'), (96, '7th'), (98, '8th'), (99, '9th')]
    # d20, plus of periapt.
    _random_periapt = [(8, '+1'), (14, '+2'), (18, '+3'), (20, '+4')]
    # d20.
    _random_feather_token = [(4, 'anchor'), (7, 'bird'), (10, 'fan'), (13, 'swan boat'), (18, 'tree'), (20, 'whip')]
    # d%.
    _random_archmagi = [(45, 'white, good alignment'), (75, 'gray, neutral'), (100, 'black, evil alignment')]
    # d%, Robe of Useful Items, 4 to 16 more patches.
    _patch = [
        (8, 'bag of 100 gold pieces'),
        (15, "coffer (1/2' x 1/2' x 1'), silver (500 g.p. value)"),
        (22, "door, iron (up to 10' wide and 10' high and barred on 1 side)"),
        (30, 'gems, 10 of 100 gold piece value each'),
        (44, "ladder, wooden (24' long)"),
        (51, 'mule (with saddle bags)'),
        (59, 'pit (10 cubic feet), open'),
        (68, 'potion of extra healing'),
        (75, "rowboat (12' long)"),
        (83, 'scroll of 1 spell'),
        (90, 'war dogs, pair'),
        (96, "window (2' x 4', up to 2' deep)"),
        (100, 'roll twice more'),
        ]

    def _random_figurine(self):
        return self.random_details(table(self._figurine))

    def _random_beaker(self):
        """2-5 potions."""
        return ', '.join(entry_potion(self) for _ in range(d4() + 1))

    def _random_pearl(self):
        """The level of spell recalled; 00 recalls 2 spells, each of 1st to 6th level (d6)."""
        roll = d100()
        if roll < 100:
            return table(self._pearl_level, roll)
        return 'recalls 2 spells: ' + ', '.join(f'{ORDINALS[level - 1]} level' for level in sorted((d6(), d6())))

    def _random_chime(self):
        return f'{20 + d6() * 10} charges'

    def _random_ioun(self):
        """1-10 stones, a duplicate of a type in the cache is burned out."""
        stones = []
        for _ in range(d10()):
            stone = table(self._ioun_stone, d20())
            stones.append(table(self._ioun_stone, 20) if stone in stones else stone)
        counts = collections.Counter(stones)
        return f'{len(stones)} stones: ' + '; '.join(f'{count} x {stone}' if count > 1 else stone for stone, count in counts.items())

    def _random_beads(self):
        """3-6 special beads."""
        beads = collections.Counter(table(self._prayer_bead, d20()) for _ in range(d4() + 2))
        return f'{sum(beads.values())} special beads: ' + ', '.join(f'{count} x {bead}' if count > 1 else bead for bead, count in sorted(beads.items()))

    def _random_useful_items(self):
        """2 each of the dagger, lantern, mirror, pole, rope and sack, and 4 to 16 more patches."""
        patches = []
        pending = random.randint(4, 16)
        while pending:
            pending -= 1
            patch = table(self._patch)
            if patch == 'roll twice more':
                pending += 2
            else:
                patches.append(patch)
        counts = collections.Counter(patches)
        return ('2 each of dagger, lantern (filled and lit), mirror (large), pole (10\'), rope (50\' coil), sack (large); '
                + ', '.join(f'{count} x {patch}' if count > 1 else patch for patch, count in sorted(counts.items())))

    def _caster(self):
        """Spell caster of a scroll or ring: 30% clerical, 25% of those druids, 10% of magic-user are illusionists."""
        if d100() <= 70:
            return 'Illusionist' if d100() <= 10 else 'Magic-user'
        return 'Druid' if d100() <= 25 else 'Cleric'

    def _random_spells(self):
        """Ring of Spell Storing: 2-5 spells, class as scrolls; magic-user d8 (6 if 8), others d6 (d4 if 6)."""
        caster = self._caster()
        sides, lower = (8, 6) if caster == 'Magic-user' else (6, 4)
        levels = []
        for _ in range(d4() + 1):
            level = random.randint(1, sides)
            levels.append(ORDINALS[(random.randint(1, lower) if level == sides else level) - 1])
        return f'{caster} spells ' + ', '.join(f'{quantity}x{level}' for quantity, _, level in reduce_groups((1, 0, level) for level in levels))

    def scroll_spells(self, result):
        """A spell row of the scroll table: caster, then each spell's level from the row's range (clerical casters use the second)."""
        spells, *ranges = result.split('|')
        caster = self._caster()
        low, high = map(int, (ranges[-1] if caster in ('Cleric', 'Druid') else ranges[0]).split('-'))
        levels = reduce_groups((1, 0, ORDINALS[random.randint(low, high) - 1]) for _ in range(int(spells.split()[0])))
        return f'{caster} scroll ' + ', '.join(f'{quantity}x{level}' for quantity, _, level in levels)

    def roll_map(self, roll=None):
        return entry_dmg_map(self, roll)

    def charges(self, item):
        """Charges when found: rods 50 less d10-1, staves 25 less d6-1, wands 100 less d20-1."""
        if 'Absorption' in item:
            return ' [50 spell levels]'
        if 'Cancellation' in item:
            return ' [single use]'
        if 'Serpent' in item:
            return ''
        for kind, most, die in (('Rod', 50, d10), ('Staff', 25, d6), ('Wand', 100, d20)):
            if kind in item:
                return f' [{most - die() + 1} charges]'
        return ''

    def sword_extras(self, sword):
        """Roll the type of sword, then Table 1 for whether it is unusual."""
        kind = sword
        if sword.startswith('Sword'):
            sword = f'{table(self._sword_type)}{sword.removeprefix("Sword")}'
        if d100() <= 75:
            return sword
        return format_sword(sword, *self._unusual_sword(kind))

    def _unusual_sword(self, kind):
        """(traits, lines): alignment, Int, Ego and communication; then abilities, powers, purpose and drawbacks of an unusual sword."""
        intelligence, count, communication = table(self._sword_intelligence, random.randint(76, 100))
        alignment = self._sword_alignment_for(kind)
        abilities, powers, purpose = self._sword_abilities(count)
        if intelligence == 17:  # 3 primary abilities plus 1 extraordinary power.
            more, special = self._sword_powers(1)
            powers, purpose = powers + more, purpose or special
        ego = self._sword_ego[kind] + len(abilities) + 2 * len(powers)
        ego += {16: 1, 17: 3}.get(intelligence, 0) + (2 if 'telepathy' in communication else 0)
        communication, _, reads = communication.partition(', reads ')
        if 'speech' in communication:
            languages = self._sword_language_count()
            ego += (languages + 1) // 2
            communication = language_trait(communication, alignment, languages)
        lines = [f'reads {reads}'] if reads else []
        lines += self._counted(abilities, 'range x') + self._counted(powers, 'uses x')
        if purpose:
            ego += 5
            lines.append(f'special purpose: {self._sword_purpose_for(alignment)}, {table(self._sword_purpose_power)}')
        if 'dragon slayer' in kind.lower():
            lines.append('will not slay dragons of its own alignment')
        return [alignment, f'Int {intelligence}', f'Ego {ego}', communication], lines

    @staticmethod
    def _counted(things, times):
        """['a', 'b (range x2)']: the same ability or power rolled more than once doubles its range, uses/day."""
        return [f'{thing} ({times}{count})' if count > 1 else thing for thing, count in collections.Counter(things).items()]

    def _sword_alignment_for(self, kind):
        """Table 2, Holy Avengers are lawful good, Swords of Sharpness chaotic, Vorpal Weapons lawful, cursed swords neutral."""
        lowered = kind.lower()
        if 'holy avenger' in lowered:
            return 'Lawful Good'
        if 'cursed' in lowered:
            return 'Neutral'
        required = 'Chaotic' if 'sharpness' in lowered else 'Lawful' if 'vorpal' in lowered else ''
        while True:
            alignment = table(self._sword_alignment)
            if alignment.startswith(required):
                return alignment

    def _sword_abilities(self, count):
        """(primary abilities, extraordinary powers, special purpose): 93-98 rolls twice more, 99-00 an extraordinary power instead."""
        abilities, powers, purpose = [], [], False
        for _ in range(count):
            roll = d100()
            if roll >= 99:
                more, special = self._sword_powers(1)
                powers, purpose = powers + more, purpose or special
            elif roll >= 93:
                abilities += [table(self._sword_primary, random.randint(1, 92)) for _ in range(2)]
            else:
                abilities.append(table(self._sword_primary, roll))
        return abilities, powers, purpose

    def _sword_powers(self, count):
        """(extraordinary powers, special purpose): 95-97 rolls twice more, 98-99 and 00 are the wielder's choice, 00 adds a purpose."""
        powers, purpose = [], False
        for _ in range(count):
            roll = d100()
            if roll <= 94:
                powers.append(table(self._sword_extraordinary, roll))
            elif roll <= 97:
                powers += [table(self._sword_extraordinary, random.randint(1, 94)) for _ in range(2)]
            else:
                powers.append(f"wielder's choice of 1 power (rolled {table(self._sword_extraordinary, random.randint(1, 94))})")
                purpose = purpose or roll == 100
        return powers, purpose

    def _sword_language_count(self):
        """Table 6, 00 is 6 or the total of 2 more rolls, whichever is greater."""
        roll = d100()
        if roll < 100:
            return table(self._sword_languages, roll)
        return max(6, sum(table(self._sword_languages, random.randint(1, 99)) for _ in range(2)))

    def _sword_purpose_for(self, alignment):
        """Table 5.A, made to suit the sword's alignment: good swords kill and slay only evil, neutral ones preserve the balance."""
        purpose = table(self._sword_purpose)
        good, evil = alignment.endswith('Good'), alignment.endswith('Evil')
        if purpose.startswith('defeat'):
            return 'preserve the balance (defeat/slay powerful beings of extreme alignment)' if alignment == 'Neutral' else purpose
        if purpose.startswith('kill'):
            return purpose.replace('kill', 'kill evil', 1) if good else purpose
        if purpose.startswith('overthrow'):
            return 'overthrow chaos' if alignment.startswith('Lawful') else 'overthrow law' if alignment.startswith('Chaotic') else purpose
        if purpose.startswith('slay good'):
            return 'slay evil' if good else 'slay good' if evil else purpose
        return 'slay evil or neutral non-human monsters' if good else 'slay good or neutral non-human monsters' if evil else purpose


# --raw: each ruleset's rules as written. OD&D, Advanced and AD&D 1e are only as written.
RAW_RULES = {BasicRules: BasicRawRules, ExpertRules: ExpertRawRules, AdvancedRawRules: AdvancedRawRules, GreyhawkRules: GreyhawkRawRules, OddRules: OddRules, DmgRules: DmgRules}


class AliasedGroup(click.Group):
    """Also accepts 'gems' for 'gem', 'jewel' for 'jewelry', and any unique prefix of a command: 'j', 'we', 'ws'."""

    ALIASES = {'gems': 'gem', 'jewel': 'jewelry'}

    def get_command(self, ctx, cmd_name):
        command = super().get_command(ctx, cmd_name)
        if command is not None:
            return command
        if cmd_name in self.ALIASES:
            return super().get_command(ctx, self.ALIASES[cmd_name])
        names = {self.ALIASES.get(name, name) for name in [*self.commands, *self.ALIASES] if name.startswith(cmd_name)}
        if len(names) > 1:
            ctx.fail(f'Ambiguous command {cmd_name!r}: could be {", ".join(sorted(names))}.')
        return super().get_command(ctx, names.pop()) if names else None


@click.group(cls=AliasedGroup)
@click.option('-b', '--basic', default=False, is_flag=True, help='Use OSE level 1-3 tables, tweaked.')
@click.option('-x', '--expert', default=False, is_flag=True, help='Use OSE Expert tables, tweaked (default).')
@click.option('-a', '--advanced-OSE', 'advanced', default=False, is_flag=True, help='Use OSE Advanced Fantasy tables, always as written.')
@click.option('-g', '--greyhawk', default=False, is_flag=True, help='Use OD&D + Greyhawk tables, tweaked.')
@click.option('-o', '--odd', default=False, is_flag=True, help='Use OD&D tables, always as written.')
@click.option('-d', '--dmg', default=False, is_flag=True, help='Use AD&D 1e DMG tables and Monster Manual treasure types, always as written.')
@click.option('-r', '--raw', default=False, is_flag=True, help='Use rules as written without tweaks.')
@click.option('--brief', default=False, is_flag=True, help='Combine gems and jewelry: no type, size or design, so all of a value group on one line.')
@click.option('--roll', default=None, type=int, help='Use this d100 roll.')
@click.pass_context
def cli(ctx, basic, expert, advanced, greyhawk, odd, dmg, raw, brief, roll):
    """Roll up treasure hoards and items. OSE Expert by default.

    Rulesets are tweaked unless -r/--raw: -rb, -rx, -rg are rules as written. -a, -o and -d are always as written.
    """
    chosen = [rules_class for flag, rules_class in (
        (basic, BasicRules), (expert, ExpertRules), (advanced, AdvancedRawRules), (greyhawk, GreyhawkRules), (odd, OddRules),
        (dmg, DmgRules),
        ) if flag]
    if len(chosen) > 1:
        raise click.UsageError('Choose only one of -b, -x, -a, -g, -o, -d.')
    rules_class = chosen[0] if chosen else ExpertRules
    if raw:
        rules_class = RAW_RULES[rules_class]
    rules = rules_class()
    rules.gems.brief = rules.jewelries.brief = brief
    ctx.obj['rules'] = rules
    ctx.obj['roll'] = roll


def announce(ctx, count, noun):
    """Say what is rolled and with which rules, e.g. Four potions using Expert rules."""
    number = NUMBER_WORDS[count] if 0 <= count < len(NUMBER_WORDS) else count
    click.echo(f'{number} {noun}{"" if count == 1 else "s"} using {ctx.obj["rules"].title}.')


def _add_roll_item_cli_commands():
    def _add(name, roll_function, description, noun, maps=True):
        @cli.command(name, help=f'Roll up {description}')
        @click.argument('count', default=1, type=int)
        @click.pass_context
        def command(ctx, count):
            rules = ctx.obj['rules']
            roll = ctx.obj['roll']

            def roll_one():
                result = roll_function(rules, roll)
                while not maps and getattr(result, 'kind', None) == 'map':
                    if roll is not None:
                        raise click.UsageError(f'Roll {roll} is a treasure map, use the map command.')
                    result = roll_function(rules)
                return result
            announce(ctx, count, noun)
            try:
                click.echo('\n'.join(present([roll_one() for _ in range(count)])))
            except RollOutOfRange as error:
                raise click.UsageError(str(error)) from error
    # CLI subcommand name: (function to roll one, what the help says it rolls up, noun for the 'using' line).
    ROLL_COMMANDS = {
        'item': (entry_item, 'magic item.', 'magic item', False),
        'sword': (entry_sword, 'magic swords.', 'magic sword'),
        'armor': (entry_armor, 'magic armors.', 'magic armor'),
        'weapon': (entry_weapon, 'magic weapons.', 'magic weapon'),
        'potion': (entry_potion, 'potions.', 'potion'),
        'scroll': (entry_scroll, 'magic scrolls.', 'magic scroll', False),
        'ring': (entry_ring, 'magic rings.', 'magic ring'),
        'wsr': (entry_wsr, 'wand, staff, rod.', 'wand/staff/rod item'),
        'misc': (entry_misc, 'miscellaneous magic items.', 'miscellaneous magic item'),
        'map': (entry_map, 'treasure and magic maps.', 'treasure map'),
        }
    for name, (func, description, noun, *maps) in ROLL_COMMANDS.items():
        _add(name, func, description, noun, *maps)
_add_roll_item_cli_commands()


@cli.command()
@click.argument('count', default=1)
@click.argument('group', default=1)
@click.pass_context
def gem(ctx, count, group):
    """Roll up gems."""
    announce(ctx, count, 'gem')
    click.echo('\n'.join(ctx.obj['rules'].gems.lines(count, group)))


@cli.command()
@click.argument('count', default=1)
@click.argument('group', default=1)
@click.pass_context
def jewelry(ctx, count, group):
    """Roll up jewelry."""
    announce(ctx, count, 'jewelry piece')
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
    click.echo(f'Type {code.upper()} treasure using {rules.title}.')
    results = list(rules.treasure_type(type_code))
    while something and not results:
        results = list(rules.treasure_type(type_code))
    click.echo('\n'.join(present(results)) or 'Nothing')


if __name__ == '__main__':
    cli(obj={})
