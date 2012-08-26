'''Various "dice" for use in simulating/analyzing Pen & Paper RPG systems/rules.

Contents:
    d4   std RPG dice notation
    d4p  pentration such as in Hackmaster Basic.  if max value rolled, subtract one, add reroll, recurse.
    d4x  exploding. if max value rolled, add reroll, recurse.
    d4fx see FighterExplodingDieFactory

Other Stuff:
    do_roll  interpret simple textual RPG dice roll conventions


The probability for k successes rolling n dice is

n! / (k!((n-k)!)) p^k q^{n-k}

Where p=1/6 is the probability of success and q=1-p=5/6 is the probability of failure.
'''

import random

__all__ = (
    'do_roll', 'DieFactory', 'PenetrationDieFactory', 'FighterExplodingDieFactory',
    'd4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100',
    'd4p', 'd6p', 'd8p', 'd10p', 'd12p', 'd20p', 'd100p',
    'd4x', 'd6x', 'd8x', 'd10x', 'd12x', 'd20x', 'd100x',
    )


def do_roll(roll):
    '''Given simple roll forumula [40+]2d6 return integer.'''
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
    '''Create 'lables' that make 1d(size) 'die rolls' when called, used as int
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
        assert size > 1  # infinte loops are overrated
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
        assert size > 1  # infinte loops are overrated
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
    '''Fighters roll 2 damage dice, take highest inital roll, explode that as
    appropriate.
    '''

    def __init__(self, size, explode_on=1):
        assert size > 1  # infinte loops are overrated
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


d4 = DieFactory(4)
d6 = DieFactory(6)
d8 = DieFactory(8)
d10 = DieFactory(10)
d12 = DieFactory(12)
d20 = DieFactory(20)
d100 = DieFactory(100)

d4p = PenetrationDieFactory(4)
d6p = PenetrationDieFactory(6)
d8p = PenetrationDieFactory(8)
d10p = PenetrationDieFactory(10)
d12p = PenetrationDieFactory(12)
d20p = PenetrationDieFactory(20)
d100p = PenetrationDieFactory(100)

d4x = ExplodingDieFactory(4)
d6x = ExplodingDieFactory(6)
d8x = ExplodingDieFactory(8)
d10x = ExplodingDieFactory(10)
d12x = ExplodingDieFactory(12)
d20x = ExplodingDieFactory(20)
d100x = ExplodingDieFactory(100)

d6fx = FighterExplodingDieFactory(6)
d8fx = FighterExplodingDieFactory(8)
d10fx = FighterExplodingDieFactory(10)
d12fx = FighterExplodingDieFactory(12)
