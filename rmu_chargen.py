#!/usr/bin/env python3
"""Generate Rolemaster Unified stats

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Mar 2026.
Website: http://trollandflame.blogspot.com/
"""

import cmd
import random
from collections import namedtuple

from dice import d100

POWERLEVELS = {
    # name: (stat minimum, average temp, average potential, stat boosts)
    'Average':   ( 1, 51, 76, 1),
    'Superior':  (11, 56, 78, 2),
    'Heroic':    (21, 61, 76, 3),
    'Legendary': (31, 66, 83, 4),
    'Epic':      (41, 71, 86, 5),
    }
STATS = ('Agility', 'Constitution', 'Empathy', 'Intuition', 'Memory', 'Presence', 'Quickness', 'Reasoning', 'Self Discipline', 'Strength')
STAT_GAIN = [
    # stat or less, (min, max)
    (6, (0, 2)),
    (8, (1, 3)),
    (18, (1, 6)),
    (81, (1, 10)),
    (90, (1, 6)),
    (92, (1, 3)),
    (99, (0, 2)),
]
STAT_BONUS = [
    # stat or less, bonus
    (1, -15),
    (2, -14),
    (3, -13),
    (4, -12),
    (5, -11),
    (6, -10),
    (8, -9),
    (11, -8),
    (14, -7),
    (17, -6),
    (23, -5),
    (29, -4),
    (35, -3),
    (41, -2),
    (47, -1),
    (53, 0),
    (59, 1),
    (65, 2),
    (71, 3),
    (77, 4),
    (83, 5),
    (86, 6),
    (89, 7),
    (92, 8),
    (94, 9),
    (95, 10),
    (96, 11),
    (97, 12),
    (98, 13),
    (99, 14),
    (100, 15),
]


class Stat:
    def __init__(self, name, minimum):
        rolls = sorted([statd100(minimum), statd100(minimum), statd100(minimum)])
        self.temporary = rolls[1] # middle in temp
        self.potential = rolls[2] # highest in potential
        self.name = name
        self.short = 'SD' if name == 'Self Discipline' else name[:2]
        self.bonus_species = 0

    def __str__(self):
        return f'{self.short}:{self.bonus:3} {self.temporary:3}/{self.potential}'

    @property
    def long_str(self):
        """Long string representation of stat with bonus breakdown."""
        bits = ', '.join(f'{x} {y}' for x, y in self.get_bonus_list())
        if bits:
            bits = f' ({bits})'
        return f'{self.name:15} {self.temporary:3}/{self.potential} {self.bonus:3}{bits}'

    @property
    def stat(self):
        """tempoary / potential."""
        return f'{self.temporary}/{self.potential}'

    @property
    def bonus(self):
        """Total stat bonus."""
        return self.bonus_base + self.bonus_species

    @property
    def bonus_base(self):
        """Base stat bonus."""
        return chart_lookup(STAT_BONUS, self.temporary)

    def get_bonus_list(self):
        """Return list of (bonus, source)."""
        return list(filter(lambda x: x[0] != 0, [
            (self.bonus_base, 'base'),
            (self.bonus_species, 'species'),
            ]))


class Species(namedtuple('Species', [
    'Name', 'BonusDP',
    'Ag', 'Co', 'Em', 'In', 'Me', 'Pr', 'Qu', 'Re', 'SD', 'St',
    'RR_Cha', 'RR_Ess', 'RR_Men', 'RR_Phy',
    'Endurance', 'Hits', 'Recovery',
    ])):

    def __str__(self):
        return self.Name

SPECIES = {
    'Human, common': Species(
        'Human, common', 50,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0,
        0, 25, 1.0,
        ),
    'Half-Elf': Species(
        'Half-Elf', 18,
        2, 0, 0, 0, 0, 2, 2, 0, -3, 2,
        -5, -5, -5, 5,
        5, 25, 1.0,
        ),
    }

class Culture(namedtuple('Culture', [
    'Name', 'SkillRanks', 'Crafts', 'Vocations',
    ])):

    def __str__(self):
        return self.Name
# CULTURES = {
#     # *max 2 ranks per specialization excep langaugages
#     'Cosmopolitan': Culture(
#         'Cosmopolitan',
#         ((2, 'Perception'), (1, 'Body Development'), (1, 'Unarmed*'), (4, 'COMPOSITION|PERFORMANCE ART'), (6, 'CRAFTING|VOCATION'),
#          (5, 'Region(own)'), (5, 'Region(neighboring)'), (19, 'Language'), (2, 'Religion/Philosophy'), (7, 'LORE'),
#          (1, 'Running'),
#          (2, 'Influence*'), (3, 'Social Awareness'), (1, 'Trading'),
#          ),
#         ('any'),
#         ('bookkeeper', 'guardsman', 'librarian', 'manager', 'merchant', 'officer', 'scribe', 'soldier', 'valet', 'craftsman'),
#         ),
#     }


def chart_lookup(chart, value):
    """Lookup value in chart constructed with entries [value or less, (result)]."""
    for threshold, result in chart:
        if value <= threshold:
            return result
    raise ValueError(f'Value {value} exceeds all thresholds in chart.')


def statd100(minimum):
    """d100 rerolling minimum or less."""
    roll = d100()
    if roll < minimum:
        return statd100(minimum)
    return roll


def parse_choice(text, count):
    """Parse a 1-based menu choice, raising ValueError if out of range."""
    value = int(text)
    if value <= 0 or value > count:
        raise ValueError()
    return value


def match_stat(stats, name):
    """Given list of Stats() return Stat() matching name or None."""
    name = name.strip().lower()
    for stat in stats:
        if stat.short.lower() == name or stat.name.lower().startswith(name):
            return stat


class Skill:
    def __init__(self, name):
        self.name = name
        self.ranks = 0
        self.dp_cost = 0


class Character:
    def __init__(self, power_level):
        self.power_level = power_level  # Campaign power level
        self._stat_minimum = POWERLEVELS[power_level][0]
        self.stat_avg_temporary = POWERLEVELS[power_level][1]
        self.stat_avg_potential = POWERLEVELS[power_level][2]
        self.stat_boosts = POWERLEVELS[power_level][3]
        self.stat_swaps = 2
        self.stats = tuple()
        self.name = 'nameless'
        self.set_species(SPECIES['Human, common'])

    def __str__(self):
        return f'{self.name} {self.species}'

    @property
    def hits(self):
        return self.species.Hits

    @property
    def endurance(self):
        return self.species.Endurance

    @property
    def rr_cha(self):
        return self.species.RR_Cha

    @property
    def rr_ess(self):
        return self.species.RR_Ess

    @property
    def rr_men(self):
        return self.species.RR_Men

    @property
    def rr_phy(self):
        return self.species.RR_Phy

    def _update_species_stat_bonuses(self):
        for stat in self.stats:
            stat.bonus_species = self.species.__getattribute__(stat.short)

    def set_species(self, species):
        self.species = species
        self.bonus_dp = self.species.BonusDP
        self._update_species_stat_bonuses()

    def generate_stats(self):
        self.stats = tuple(Stat(name, self._stat_minimum) for name in STATS)
        self._update_species_stat_bonuses()
        self.stat_boosts = POWERLEVELS[self.power_level][3]
        self.stat_swaps = 2

    def character_sheet(self):
        """String representation of character sheet."""
        bits = [
            f'Name: {self.name}',
            f'Species: {self.species}',
            f'Hits: {self.hits} Recovery: {self.species.Recovery}',
            f'Endurance: {self.endurance}',
            f'Resistances: {self.rr_cha} Channeling, {self.rr_ess} Essence, {self.rr_men} Mentalism, {self.rr_phy} Physical',
            ]
        for stat in self.stats:
            bits.append(str(stat))
        if self.bonus_dp:
            bits.append(f'Bonus DP: {self.bonus_dp}')
        if self.stat_boosts > 0:
            bits.append(f'Stat boosts remaining: {self.stat_boosts}')
        if self.stat_swaps > 0:
            bits.append(f'Stat swaps remaining: {self.stat_swaps}')
        return '\n'.join(bits)


class CharacterGen(cmd.Cmd):
    def preloop(self):
        self.prompt = '> '
        self.char = Character('Superior')
        self._state = dict()

    def emptyline(self):
        """Show character empty input (default is to repeat last command)."""
        self.onecmd('show')

    def do_EOF(self, arg):
        """Exit on Ctrl-D."""
        print()
        self.onecmd('show')
        return True

    def do_show(self, arg):
        """Display character sheet."""
        print(self.char.character_sheet())

    def do_show_stats(self, arg):
        """Display character stats."""
        for stat in self.char.stats:
            print(stat)

    def do_show_long(self, arg):
        """Display character stats."""
        for stat in self.char.stats:
            print(stat.long_str)

    def do_new(self, arg):
        """Generate a new character of given Power Level."""
        match arg.strip().lower():
            case x if x.startswith('av'):
                self.char = Character('Average')
            case x if x == '' or x.startswith('su'):
                self.char = Character('Superior')
            case x if x.startswith('he'):
                self.char = Character('Heroic')
            case x if x.startswith('le'):
                self.char = Character('Legendary')
            case x if x.startswith('ep'):
                self.char = Character('Epic')
            case _:
                print(f'Unknown Power Level: {arg}')
                return
        print(f'Created {self.char.power_level} character')
        self.onecmd('generate_stats')

    def do_name(self, arg):
        """Set character name."""
        self.char.name = arg.strip()
        print(f'Character name set to {self.char.name}')

    def do_species(self, arg):
        """Set character species."""
        choices = list()
        for species in SPECIES.values():
            choices.append((str(species), lambda s=species: self.char.set_species(s)))
        for i, (x, _) in enumerate(choices):
            print(f' {i+1}) {x}')
        choice = input('choice > ')
        if not choice.strip():
            print('')
            return
        try:
            choice = parse_choice(choice, len(choices))
        except ValueError:
            print('Invalid choice\n')
        else:
            choices[choice-1][1]()

    def do_generate_stats(self, arg):
        """Generate stats."""
        if self.char.stats:
            self.onecmd('show_stats')
            if 'y' != input('Regenerate stats? (y/N) > ').lower():
                return
        self.char.generate_stats()
        self.onecmd('boost')

    def do_boost(self, arg):
        """Choose stat boosts."""
        def boost(stat, temp, potential):
            print(f'Boosted {stat.temporary}/{stat.potential} to {temp}/{potential}')
            stat.temporary = temp
            stat.potential = potential

        if self.char.stat_boosts <= 0:
            print('No stat boosts remaining.')
            return
        self.onecmd('show_stats')
        print()
        # TODO: this should be figured out once and not dynamically.
        stats = sorted(self.char.stats, key=lambda x: x.temporary, reverse=True)
        choices = list()
        print(f'Pick any {self.char.stat_boosts} of the following boosts:')
        choices.append(lambda: print('make the gains'))
        print(f' {len(choices)}) Make two stat gain rolls for the same or two different stats')
        for replace in (0, 1):
            key = f'replace {replace}'
            if key not in self._state:
                stat = stats[replace]
                temp = max(stat.temporary, 90 if replace == 0 else 85)
                potential = min(100, stat.potential + 10)
                if temp > stat.temporary or potential > stat.potential:
                    choices.append(lambda k=key, s=stat, t=temp, p=potential: self._state.setdefault(k, True) and boost(s, t, p))
                    print(f' {len(choices)}) Replace {stat} with {temp}/{potential}')
        for stat in self.char.stats:
            temp = max(stat.temporary, self.char.stat_avg_temporary)
            potential = max(stat.potential, self.char.stat_avg_potential)
            if temp > stat.temporary or potential > stat.potential:
                choices.append(lambda s=stat, t=temp, p=potential: boost(s, t, p))
                print(f' {len(choices)}) Replace {stat} with {temp}/{potential}')
        choice = input('choice > ')
        if not choice.strip():
            print(f'run "boost" to pick {self.char.stat_boosts} remaining boosts.')
            return
        try:
            choice = parse_choice(choice, len(choices))
        except ValueError:
            print('Invalid choice\n')
        else:
            choices[choice-1]()
            self.char.stat_boosts -= 1
        if self.char.stat_boosts > 0:
            self.onecmd('boost')

    def do_swap(self, arg):
        """Swap position of two named stats."""
        if self.char.stat_swaps <= 0:
            print('No stat swaps remaining.')
            return
        parts = arg.split()
        if len(parts) != 2:
            print('Usage: swap <stat1> <stat2>')
            return
        first, second = [match_stat(self.char.stats, x.strip().lower()) for x in parts]
        if not first or not second:
            print(f'Unknown stats: {arg}')
            return
        print(f'Swapped {first.short} {first.stat} with {second.short} {second.stat}')
        first.temporary, second.temporary = second.temporary, first.temporary
        first.potential, second.potential = second.potential, first.potential
        self.char.stat_swaps -= 1

    def do_stat_gain(self, arg):
        """Make a stat gain roll for named stat."""
        if not (stat := match_stat(self.char.stats, arg)):
            print(f'Unknown stat: {arg}')
            return
        if stat.temporary >= stat.potential:
            print(f'{stat.short} is already at potential.')
            return
        min_gain, max_gain = chart_lookup(STAT_GAIN, stat.temporary)
        gain = random.randint(min_gain, max_gain)
        new = min(stat.temporary + gain, stat.potential)
        print(f'{stat} + {gain} = {new}')
        stat.temporary = new

if  __name__ == '__main__':
    CharacterGen().cmdloop()
