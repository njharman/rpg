#!/usr/bin/env python3
"""Given level of dungeon roll monster/treasure stocking for X rooms.

According to B/X or ODD Rules.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: http://trollandflame.blogspot.com/
"""

import random

import click

d2 = lambda: random.randint(1, 2)
d4 = lambda: random.randint(1, 4)
d6 = lambda: random.randint(1, 6)
d12 = lambda: random.randint(1, 12)
d100 = lambda: random.randint(1, 100)


class OddStocking:
    name = 'ODD'
    SILVER = {
        1: lambda: 100 * d6(),
        2: lambda: 100 * d12(),
        3: lambda: 100 * d12(),
        4: lambda: 1000 * d6(),
        5: lambda: 1000 * d6(),
        6: lambda: 2000 * d6(),
        7: lambda: 2000 * d6(),
        8: lambda: 5000 * d6(),
        9: lambda: 5000 * d6(),
        }
    GOLD = {
        1: lambda: 10 * d6(),
        2: lambda: 100 * d6(),
        3: lambda: 100 * d6(),
        4: lambda: 200 * d6(),
        5: lambda: 200 * d6(),
        6: lambda: 500 * d6(),
        7: lambda: 500 * d6(),
        8: lambda: 1000 * d6(),
        9: lambda: 1000 * d6(),
        }
    GEMS = {
        1: 5,
        2: 10,
        3: 10,
        4: 20,
        5: 20,
        6: 30,
        7: 30,
        8: 40,
        9: 40,
        }
    JEWLERY = GEMS
    MAGIC = {
        1: 5,
        2: 5,
        3: 5,
        4: 10,
        5: 10,
        6: 15,
        7: 15,
        8: 20,
        9: 20,
        }
    MONSTER = {
        1: lambda: (1, 1, 2, 2, 3, 4)[d6() - 1],
        2: lambda: (1, 2, 3, 3, 4, 5)[d6() - 1],
        3: lambda: (2, 3, 4, 4, 5, 6)[d6() - 1],
        4: lambda: (3, 4, 4, 5, 5, 6)[d6() - 1],
        5: lambda: (3, 4, 4, 5, 5, 6)[d6() - 1],
        6: lambda: (4, 5, 5, 5, 6, 6)[d6() - 1],
        7: lambda: (4, 5, 5, 5, 6, 6)[d6() - 1],
        8: lambda: (5, 5, 6, 6, 6, 6)[d6() - 1],
        9: lambda: (5, 5, 6, 6, 6, 6)[d6() - 1],
        }

    def __init__(self, level):
        self.level = level

    def stock_rooms(self, rooms):
        """Contents of X rooms iterator."""
        for i in range(rooms):
            contents = list()
            treasure = False
            if d6() <= 2:
                contents.append('%dHD monster' % self.MONSTER[self.level]())
                treasure = d6() <= 3
            else:
                treasure = d6() == 1
            if treasure:
                contents.append(f'{self.SILVER[self.level]():,}sp')
                if d6() <= 3:
                    contents.append(f'{self.GOLD[self.level]():,}gp')
                if d100() <= self.GEMS[self.level]:
                    contents.append('gems')
                if d100() <= self.JEWLERY[self.level]:
                    contents.append('jewlery')
                if d100() <= self.MAGIC[self.level]:
                    contents.append('magic')
            yield ', '.join(contents)


class BxStocking:
    name = 'B/X'
    MONSTER = {
        1: lambda: (1, 1, 1, 2, 2, 3)[d6() - 1],
        2: lambda: (1, 2, 2, 2, 3, 4)[d6() - 1],
        3: lambda: (2, 3, 3, 3, 4, 4)[d6() - 1],
        4: lambda: (3, 4, 4, 4, 5, 6)[d6() - 1],
        5: lambda: (3, 4, 5, 5, 5, 6)[d6() - 1],
        6: lambda: (4, 5, 6, 6, 6, 7)[d6() - 1],
        7: lambda: (5, 6, 7, 7, 7, 8)[d6() - 1],
        8: lambda: (6, 7, 7, 8, 8, 9)[d6() - 1],
        9: lambda: (7, 8, 8, 9, 9, 19)[d6() - 1],
        }
    SPECIAL = [
        'alarm',
        'animating object(s)',
        'construction change',
        'illusion',
        'strange water/gas',
        'teleport',
        'trapdoor to hidden area',
        'architectural feature',
        'voices',
        'art',
        'statue',
        'fungal/other growth',
        'extreme odor'
        ]
    ROOMTRAP = [
        'pit {self.level*10}ft',
        'falling block (save vs petr)',
        'gas (save or die)',
        'mist (looks like poison gas)',
        'scything blade ({self.level+4}HD atk, 2d6dmg)',
        'spiked log ({self.level+4}HD atk, 2d6dmg)',
        'floor spear (2x {self.level+2}HD atk)',
        'floor spear (2x {self.level+2}HD atk)',
        'wall darts (6x {self.level}HD atks)',
        'wall darts (6x {self.level}HD atks)',
        'tripwire xbow ({self.level+3}HD atk)',
        'tripwire xbow ({self.level+3}HD atk)',
        'door sludge bucket (encounter checks)',
        'green slime',
        'caltrops',
        ]
    TREASURETRAP = [
        'poison needle',
        'poison needle',
        'poison needle',
        'monster (snakes, jellies, construct)',
        'monster (snakes, jellies, construct)',
        'darts (d4x {self.level}HD atks)',
        'darts (d4x {self.level}HD atks)',
        'scything blade ({self.level+1}HD atk)',
        'acid spray ({1 if self.level == 1 else 2}d6 save vs breath)',
        'monster illusion',
        'hazard illusion',
        'gas',
        'light flash (save vs spells or blind 2d6 Turns)',
        'curse (save vs spells)',
        'fiery explosion ({self.level}d6 save vs breath)',
        'stink bomb (save vs death)',
        ]

    def __init__(self, level):
        self.level = level
        self.STOCKING_TABLE = {
            1: self._empty,
            2: self._empty,
            3: self._monster,
            4: self._monster,
            5: self._special,
            6: self._trap,
            }

    def fstr(self, template):
        return eval(f"f'{template}'", globals(), locals())

    def _jewelry(self, x):
        """Roll up some jewelry."""
        # TODO: use treasure gen
        jewels = [f'{100*(d6()+d6()+d6()):,}' for x in range(x)]
        return f', {", ".join(jewels)} jewelry'

    def _treasure(self, roll):
        if self.level == 1:
            gp = f', {d6()*10}gp' if d100() <= 50 else ''
            gem = f', {d6()} gems' if d100() <= 5 else ''
            jew = self._jewelry(1) if d100() <= 2 else ''
            magic = ', 1 magic' if d100() <= 2 else ''
            return f'{d6()*100:,}sp{gp}{gem}{jew}{magic}'
        elif self.level <= 3:
            gp = f', {d6()*100:,}gp' if d100() <= 50 else ''
            gem = f', {d6()} gems' if d100() <= 10 else ''
            jew = self._jewelry(d2()) if d100() <= 5 else ''
            magic = ', 1 magic' if d100() <= 8 else ''
            return f'{d12()*100:,}sp{gp}{gem}{jew}{magic}'
        elif self.level <= 5:
            gem = f', {d6()} gems' if d100() <= 20 else ''
            jew = self._jewelry(d4()) if d100() <= 10 else ''
            magic = ', 1 magic' if d100() <= 10 else ''
            return f'{d6()*1000:,}sp, {d6()*200:,}gp{gem}{jew}{magic}'
        elif self.level <= 7:
            gem = f', {d6()} gems' if d100() <= 30 else ''
            jew = self._jewelry(d6()) if d100() <= 15 else ''
            magic = ', 1 magic' if d100() <= 15 else ''
            return f'{d6()*2000:,}sp, {d6()*500:,}gp{gem}{jew}{magic}'
        else:
            gem = f', {d6()} gems' if d100() <= 40 else ''
            jew = self._jewelry(d6()) if d100() <= 20 else ''
            magic = ', 1 magic' if d100() <= 20 else ''
            return f'{d6()*5000:,}sp, {d6()*1000:,}gp{gem}{jew}{magic}'

    def _empty(self, roll):
        """1-in-6 hidden treasure"""
        if d6() == 1:
            if d6() <= 4:
                return self.fstr(f'Hidden and trapped {self._treasure(roll)}; {random.choice(self.TREASURETRAP)}')
            else:
                return self.fstr(f'Hidden {self._treasure(roll)}')
        else:
            return 'Empty'

    def _monster(self, roll):
        """3-in-6 w/treasure"""
        treasure = ' w/ treasure' if d6() <= 3 else ''
        return f'{self.MONSTER[self.level]()}HD monster{treasure}'

    def _special(self, roll):
        return f'Special: {random.choice(self.SPECIAL)}'

    def _trap(self, roll):
        """2-in-6 trapped treasure, else room trap."""
        if d6() <= 2:
            return self.fstr(f'Trapped {self._treasure(roll)}; {random.choice(self.TREASURETRAP)}')
        else:
            return self.fstr(f'Trap: {random.choice(self.ROOMTRAP)}')

    def stock_rooms(self, rooms):
        """Contents of X rooms iterator."""
        for i in range(rooms):
            roll = d6()
            yield self.STOCKING_TABLE[roll](roll)


class MegadungeonStocking(BxStocking):
    name = 'Stonehell'
    HELLROCK = [
        'Chaos event',
        'Doom lure',
        'Lawful geometries',
        'Vaedium',
        ]

    def __init__(self, level):
        self.level = level
        self.STOCKING_TABLE = {
            1: self._monster,
            2: self._monster,
            3: self._empty,
            4: self._empty,
            5: self._empty,
            6: self._funk,
            }

    def _hellrock(self, roll):
        """hellrock special"""
        return random.choice(self.HELLROCK)

    def _funk(self, roll):
        """1 empty, 2-4 trap, 5 hellrock, 6 special."""
        return {
            1: self._empty,
            2: self._trap,
            3: self._trap,
            4: self._trap,
            5: self._hellrock,
            6: self._special,
            }[d6()](roll)


@click.command()
@click.option('-r', '--rooms', default=5, type=int, help='For this many rooms.')
@click.option('-l', '--level', default=1, type=int, help='For this dungeon level.')
@click.option('-m', '--megadungeon', default=False, is_flag=True, help='Use Roll20 Megadungeon tables.')
@click.option('-o', '--odd', default=False, is_flag=True, help='Use ODD/Greyhawk tables.')
@click.pass_context
def cli(ctx, rooms, level, megadungeon, odd):
    """Roll up stocking dungeon rooms. B/X by default."""
    level = min(9, max(1, level))
    if megadungeon:
        ruleset = MegadungeonStocking(level)
    elif odd:
        ruleset = OddStocking(level)
    else:
        ruleset = BxStocking(level)
    print(f'Using {ruleset.name} rules to stock {rooms} rooms of level {level}.')
    for i, room in enumerate(ruleset.stock_rooms(rooms)):
        print(f'  Room {i + 1}: {room}')


if __name__ == '__main__':
    cli(obj={})
