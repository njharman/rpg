'''Various "dice" for use in simulating/analyzing pen & paper RPG systems/rules.

Classes:
    DieFactory
    ExplodingDieFactory
    PenetrationDieFactory

Dice; d2, d3, d4, d6, d8, d10, d12, d16, d20, d24, d30, d100:
    d?   standard RPG dice notation.
    d?x  exploding. If max value rolled, add re-roll, recurse.
    d?p  penetration such as in Hackmaster Basic.  If max value rolled, subtract one, add re-roll, recurse.

Other Stuff:
    do_roll  interpret simple textual RPG dice roll conventions


The probability for k successes rolling n dice is

n! / (k!((n-k)!)) p^k q^{n-k}

Where p=1/6 is the probability of success and q=1-p=5/6 is the probability of failure.
'''

import random

__all__ = (
    'do_roll',
    'DieFactory', 'PenetrationDieFactory', 'ExplodingDieFactory',
    'd4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100',
    'd2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd12', 'd16', 'd20', 'd24', 'd30', 'd100',
    'd2x', 'd3x', 'd4x', 'd6x', 'd8x', 'd10x', 'd12x', 'd16x', 'd20x', 'd24x', 'd30x', 'd100x',
    'd2p', 'd3p', 'd4p', 'd6p', 'd8p', 'd10p', 'd12p', 'd16p', 'd20p', 'd24p', 'd30p', 'd100p',
    )


def do_roll(roll):
    '''Given simple roll formula [40+]2d6 return integer.'''
    if '+' in roll:
        result, roll = roll.split('+')
        result = int(result)
    else:
        result = 0
    count, die = [int(x) for x in roll.split('d')]
    for i in range(count):
        result += random.randint(1, die)
    return result


class DieFactory(object):
    '''Create 'labels' that make 1d(size) 'die rolls' when called, used as int
    or converted to str.
    '''

    def __init__(self, size):
        self.name = 'd%i' % size

        def d(size=size):
            self._roll = random.randint(1, size)
            return self._roll
        self.die = d

    def __str__(self):
        return str(self.die())

    def __call__(self):
        return self.die()

    def __int__(self):
        return self.die()

    def __add__(self, other):
        return self.die() + other

    def __sub__(self, other):
        return self.die() - other

    def __radd__(self, other):
        return self.die() + other

    def __rsub__(self, other):
        return self.die() - other

    def __cmp__(self, other):
        return self.die() - other

    @property
    def natural(self):
        return self._roll


class PenetrationDieFactory(DieFactory):
    '''Explode on highest roll, with proper maths. d20 -> d12, d100 -> d20.'''

    def __init__(self, size, explode_on=1):
        assert size > 1  # Infinite loops are overrated.
        self.__name__ = 'd%ip' % size
        if size == 20:
            self._pdie = 6
        elif size == 100:
            self._pdie = 20
        else:
            self._pdie = size

        def d(size=size, penetration=False):
            roll = random.randint(1, size)
            if not penetration:
                self._roll = roll
            if roll > (size - explode_on):
                roll += (d(self._pdie, True) - 1)
            return roll
        self.die = d


class ExplodingDieFactory(DieFactory):
    '''Explode on highest roll. d20 -> d12.'''

    def __init__(self, size, explode_on=1):
        assert size > 1  # Infinite loops are overrated.
        self.__name__ = 'd%ix' % size
        if size == 20:
            self._pdie = 12
        else:
            self._pdie = size

        def d(size=size, explode=False):
            roll = random.randint(1, size)
            if not explode:
                self._roll = roll
            if roll > (size - explode_on):
                roll += d(self._pdie, True)
            return roll
        self.die = d


class FighterExplodingDieFactory(DieFactory):
    '''Fighters roll 2 damage dice, take highest initial roll, explode that as
    appropriate.
    '''

    def __init__(self, size, explode_on=1):
        assert size > 1  # Infinite loops are overrated.
        self.__name__ = 'd%ifx' % size

        def d(explode=False):
            if not explode:
                roll = max(random.randint(1, size), random.randint(1, size))
                self._roll = roll
            else:
                roll = random.randint(1, size)
            if roll > (size - explode_on):
                roll += (d(True) - 1)
            return roll
        self.die = d


d2 = DieFactory(2)
d3 = DieFactory(3)
d4 = DieFactory(4)
d6 = DieFactory(6)
d8 = DieFactory(8)
d10 = DieFactory(10)
d12 = DieFactory(12)
d16 = DieFactory(16)
d20 = DieFactory(20)
d24 = DieFactory(24)
d30 = DieFactory(30)
d100 = DieFactory(100)

d2x = ExplodingDieFactory(2)
d3x = ExplodingDieFactory(3)
d4x = ExplodingDieFactory(4)
d6x = ExplodingDieFactory(6)
d8x = ExplodingDieFactory(8)
d10x = ExplodingDieFactory(10)
d12x = ExplodingDieFactory(12)
d16x = ExplodingDieFactory(16)
d20x = ExplodingDieFactory(20)
d24x = ExplodingDieFactory(24)
d30x = ExplodingDieFactory(30)
d100x = ExplodingDieFactory(100)

d2xp = PenetrationDieFactory(2)
d3xp = PenetrationDieFactory(3)
d4xp = PenetrationDieFactory(4)
d6xp = PenetrationDieFactory(6)
d8xp = PenetrationDieFactory(8)
d10xp = PenetrationDieFactory(10)
d12xp = PenetrationDieFactory(12)
d16xp = PenetrationDieFactory(16)
d20xp = PenetrationDieFactory(20)
d24xp = PenetrationDieFactory(24)
d30xp = PenetrationDieFactory(30)
d100xp = PenetrationDieFactory(100)
