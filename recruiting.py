#!/usr/bin/env python3
import random
from collections import defaultdict

import click


def d(pips):
    return random.randint(1, pips)


def d4():
    return random.randint(1, 4)


def d6():
    return random.randint(1, 6)


def ability():
    return d6() + d6() + d6()


def positive_ability():
    while True:
        score = d6() + d6() + d6()
        if score > 8:
            return score


def modifier(score):
    if score <= 3:
        return -3
    if score <= 5:
        return -2
    if score <= 8:
        return -1
    if score >= 18:
        return +3
    if score >= 16:
        return +2
    if score >= 13:
        return +1
    return 0


prefix = ['Am', 'Banth', 'Carth', 'Dur', 'Flor', 'Gant', 'Haj', 'Ham', 'Il',
    'Jad', 'Kand', 'Kant', 'Lan', 'Mat', 'Nast', 'Or', 'Pand', 'Parth', 'Roj',
    'Sark', 'Sol', 'Sor', 'Tal', 'Tar', 'Tark', 'Tav', 'Thor', 'Thur', 'Thuv',
    'Ul', 'Um', 'Val', 'Vor', 'Xax', 'Yerst', 'Zand']
suffix = [
    'a', 'ab', 'ad', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ang',
    'ar', 'ark', 'as', 'at', 'ed', 'ek', 'el', 'i', 'ia', 'ion', 'is',
    'o', 'ok', 'olian', 'on', 'or', 'oris', 'os', 'u', 'ul', 'um', 'un',
    'ur', 'uren', 'us']


def human_name():
    return f'{random.choice(prefix)}{random.choice(suffix)}'


def pick(table):
    """Table is list [weight, thing]jjj"""
    choices, weights = table
    return random.choices(choices, weights)[0]


class SortThings:
    def __lt__(self, other):
        if isinstance(self, Dog):
            return True
        if isinstance(other, Dog):
            return False
        if isinstance(self, NonCombatant):
            return True
        if isinstance(other, NonCombatant):
            return False
        if isinstance(self, ZeroLevel):
            return True
        if isinstance(other, ZeroLevel):
            return False
        return self.level < other.level


class Dog(SortThings):
    def __str__(self):
        hp = max(2, d6() - 1)
        gp = [20, 25, 25, 30, 30][hp - 1]
        dex = ability()
        return f'Dog: {hp}hp F0, AC7, 11/d6-1 dmg, {dex} Dex. {gp}gp.'

    def day(self):
        return 0


class NonCombatant(SortThings):
    def __str__(self):
        what = pick((['Human', 'Hobbit'], [5, 1]))
        hp = random.randint(1, 3)
        weapon = random.choice(['Dagger', 'Club'])
        name = human_name()
        return f'{what} {name}: {hp}hp, F0, AC9, 11/{weapon}, 8 Dex. 5gp per job + room/board.'

    def day(self):
        return random.choice([0, 0, 0, 1, 1, 1, 2, 2, 3])


class ZeroLevel(SortThings):
    table = list(zip(*[
        # HP  Armor   Weapon/Shield What
        (3, 'Clothes', 'Hand Axe and Shield', 'Hobbit'),
        (4, 'Leather', 'Spear, dagger and Shield', 'Hobbit'),
        (5, 'Leather', 'Spear, dagger and Shield', 'Female'),
        (6, 'Leather', 'Spear, Hand Axe and Mace', 'Female'),
        (0, 'Chain', 'Sword, dagger and Shield', 'Male'),
        (0, 'Chain', 'Sword, Bow and dagger', 'Male'),
        (0, '', 'Bow and hand axe', 'Male'),
        (0, '', 'Battleaxe (2h)', 'Male'),
        (0, '', '', 'Male'),
        (0, '', '', 'Male'),
        ]))

    def __str__(self):
        hp = random.choice(self.table[0][:4])
        armor = random.choice(self.table[1][:6])
        weapon = random.choice(self.table[2][:8])
        what = random.choice(self.table[3])
        if what == 'Female':
            race = random.choice(['Altanian', 'Roglar', 'Amazon'])
            what = f'{what} ({race})'
        if what == 'Male':
            race = random.choice(['Altanian', 'Altanian', 'Altanian', 'Roglar', 'Roglar', 'Dunael'])
            what = f'{what} ({race})'
        dex = ability()
        hire = (d(3) + 1) * 10
        if 'Cloths' in armor:
            hire -= 10
        if 'Battleaxe' in weapon:
            hire -= 10
        if 'Chain' in armor:
            hire += 10
        if 'Sword' in weapon:
            hire += 10
        if 'Bow' in weapon:
            hire += 10
        name = human_name()
        return f'0-lvl {what} {name}: {hp}hp, F0, {armor}, 11/{weapon}, {dex} Dex. {hire}gp to hire + 2gp/day.'

    def day(self):
        return random.choice([0, 0, 1, 1, 1, 2, 2, 2, 3, 4, 5])


class Leveled(SortThings):
    def __str__(self):
        return f'{self.what} {self.name}: {self.equipment}. {self.hp}hp, AC{self.ac}, to-hit 10, Saves: {self.saves},'\
                ' Abilities: ' + ' '.join(f'{modifier(x):+}' for x in [self.str, self.int, self.wis, self.dex, self.con, self.cha]) + \
                f'. {self.hire}'

    def _calc_hp(self, first_lvl_max):
        return first_lvl_max + modifier(self.con) + sum(self.hd() for i in range(self.level - 1))

    @property
    def saves(self):
        # BW Poison/Death Petrify/Paralyze Wands Spells
        # Modify for abilities, con; poison, wis; rsw spell
        saves = [int(x) for x in self.saves_chart[self.level - 1].split()]
        saves[1] += modifier(self.con)
        saves[3] += modifier(self.wis)
        saves[4] += modifier(self.wis)
        return ' '.join(str(x) for x in saves)

    @property
    def what(self):
        return f'{self.level}-lvl {self.type}'

    def day(self):
        return random.choice([0, 0, 0, 1, 1, 2, 2])


class Cleric(Leveled):
    type = 'Cleric'
    hire = 'On mission'
    ac = 2
    hd = lambda s: max(1, d(4) + 2 + modifier(s.con))
    saves_chart = [
        '16 11 14 12 15',
        '16 11 14 12 14',
        '15 10 13 11 13',
        '15 10 13 11 13',
        '14 9 12 10 12',
        '14 9 12 10 11',
        '13 8 11 9 10',
        '13 8 11 9 9',
        '12 7 10 8 9',
        '11 6 9 7 8',
        ]

    @property
    def equipment(self):
        bits = ['Plate mail, Shield, Holy Symbol, 1 flask (un)holy water']
        bits.extend(sorted(random.sample(['Club', 'Club', 'Mace', 'Mace', 'Staff'], 1)))
        return ', '.join(bits)

    def __init__(self):
        self.level = random.choice([1, 1, 1, 2, 2, 2, 3, 3, 4])
        self.str = ability()
        self.dex = ability()
        self.con = ability()
        self.int = ability()
        self.wis = ability()
        self.cha = ability()
        self.hp = self._calc_hp(6)
        self.name = human_name()


class Dwarf(Leveled):
    type = 'Dwarf'
    hire = '100gp to hire + 1/2 share treasure'
    ac = 2
    hd = lambda s: max(1, d(4) + 3 + modifier(s.con))
    saves_chart = [
        # TODO: not sure chart is correct.
        '10 13 8 10 9 12',
        '10 13 8 10 9 12',
        '10 13 8 10 9 12',
        ]

    @property
    def equipment(self):
        bits = ['Plate mail, Shield']
        bits.extend(sorted(random.sample(['Hammer', 'Hammer', 'Axe', 'Axe', 'Mace', 'Crossbow', 'Sword'], 3)))
        return ', '.join(bits)

    def __init__(self):
        self.level = max(1, d6() - 3)
        self.str = positive_ability()
        self.dex = ability()
        self.con = positive_ability()
        self.int = ability()
        self.wis = ability()
        self.cha = ability()
        self.hp = self._calc_hp(8)
        self.name = 'Bob'


class MagicUser(Leveled):
    type = 'Magic-User'
    hire = '100gp to hire + 2nd choice magic item or if none, 1/2 share treasure'
    ac = 9
    hd = lambda s: max(1, d(4) + 1 + modifier(s.con))
    saves_chart = [
        '16 13 13 13 12',
        '16 13 13 13 12',
        '16 13 13 13 12',
        '15 12 12 12 10',
        '15 12 12 12 10',
        '15 12 12 12 10',
        '14 11 11 11 8',
        '14 11 11 11 8',
        '14 11 11 11 8',
        '13 10 10 10 6',
        ]

    @property
    def equipment(self):
        bits = random.sample(['Wand', 'Staff', 'Skull', 'Crystal Ball', 'Shrunken Head', 'Juju Doll', 'Mask'], 1)
        bits.append('Dagger, 4 darts, lantern, 4 flasks of oil')
        return ', '.join(bits)

    def __init__(self):
        self.level = random.choice([1, 1, 1, 2])
        self.str = ability()
        self.dex = ability()
        self.con = ability()
        self.int = positive_ability()
        self.wis = ability()
        self.cha = ability()
        self.hp = self._calc_hp(5)
        self.name = human_name()


class Thief(Leveled):
    # 2-6th level thief masquarding
    type = 'Thief'
    hire = '30gp + 2gp/day'
    ac = 7
    hd = lambda s: max(1, d(4) + 2 + modifier(s.con))
    saves_chart = [
        '16 14 13 15 14',
        '16 14 13 15 14',
        '15 13 12 14 13',
        '15 13 12 14 13',
        '14 12 11 13 12',
        '14 12 11 13 12',
        ]

    @property
    def equipment(self):
        return 'Leather, Sword, and Bow'

    def __init__(self):
        self.level = random.randint(2, 6)
        self.str = ability()
        self.dex = positive_ability()
        self.con = ability()
        self.int = ability()
        self.wis = ability()
        self.cha = ability()
        self.hp = self._calc_hp(6)
        self.name = human_name()


class Exotic(Leveled):
    level = 0
    def __str__(self):
        return 'Exotic Animal'


class Settlement:
    def dogs(self, modifier):
        return [Dog() for i in range(max(0, d(2) + modifier))]

    def recruit(self, attempts, modifier=0):
        number = 0
        for x in range(attempts):
            number += max(0, (d6() - 2 + modifier))
        byday = defaultdict(list)
        for x in (self.what() for i in range(number)):
            byday[x.day()].append(x)
        for x in self.dogs(modifier):
            byday[x.day()].append(x)
        print(f'{number} total respondents from {attempts} attempts.')
        for day in range(7):
            print(f'day {day+1}')
            for x in sorted(byday[day]):
                print(' ', x)


class HumanSettlement(Settlement):
    def what(self):
        choices = [NonCombatant, ZeroLevel, self.special]
        weights = [2, 3, 1]
        return pick((choices, weights))()

    def special(self):
        choices = [Dwarf, MagicUser, Cleric, Thief, Exotic]
        weights = [2, 3, 2, 2, 1]
        return pick([choices, weights])()


class DwarvenSettlement(Settlement):
    def dogs(self, modifier):
        'MineMutt'
        return [Dog() for i in range(max(0, d(4) - 3))]

    def what(self):
        choices = [NonCombatant, ZeroLevel, Dwarf, self.special]
        weights = [1, 2, 2, 1]
        return pick((choices, weights))()

    def special(self):
        choices = [MagicUser, Cleric, Thief, Exotic]
        weights = [2, 1, 1, 2]
        return pick([choices, weights])()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-m', '--modifier', default=0, type=int)
@click.option('-d', '--dwarven', is_flag=True)
@click.argument('attempts', default=1)
@click.pass_context
def cli(ctx, attempts, modifier, dwarven):
    if dwarven:
        settlement = DwarvenSettlement()
    else:
        settlement = HumanSettlement()
    settlement.recruit(attempts, modifier)


if __name__ == '__main__':
    cli()
