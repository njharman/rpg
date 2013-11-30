'''Various "dice" for use in simulating/analyzing pen & paper RPG systems/rules.

Classes:
    Die
    ExplodingDie
    FighterExplodingDie

Dice; d2, d3, d4, d6, d8, d10, d12, d16, d20, d24, d30, d100:
    d?   standard RPG dice notation.
    d?x  exploding. If max value rolled, add re-roll, recurse.
    d?p  penetration such as in Hackmaster Basic.  If max value rolled, subtract one, add re-roll, recurse.

Other Stuff:
    do_roll  interpret simple textual RPG dice roll conventions


Notes:

The probability for k successes rolling n dice is

n! / (k!((n-k)!)) p^k q^{n-k}

Where p=1/6 is the probability of success and q=1-p=5/6 is the probability of failure.
'''

import random

__all__ = (
    'do_roll',
    'Die', 'ExplodingDie', 'FighterExplodingDie',
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


class BaseDie(object):
    '''Create 'labels' that make 1d(size) 'die rolls' when called, used as int
    or converted to str.
    '''
    def __init__(self, size, name_fmt, die_func):
        assert size > 1  # Infinite loops are overrated.
        self.name = name_fmt % size
        self.die = die_func

    def __str__(self):
        self._roll = self.die()
        return str(self._roll)

    def __call__(self):
        self._roll = self.die()
        return self._roll

    def __int__(self):
        self._roll = self.die()
        return self._roll

    def __add__(self, other):
        return int(self) + other

    def __sub__(self, other):
        return int(self) - other

    def __radd__(self, other):
        return int(self) + other

    def __rsub__(self, other):
        return int(self) - other

    @property
    def natural(self):
        return self._roll


class Die(BaseDie):
    '''Create 'labels' that make 1d(size) 'die rolls' when called, used as int
    or converted to str.
    '''
    def __init__(self, size):
        def d(size=size):
            return random.randint(1, size)
        super(Die, self).__init__(size, 'd%i', d)


class ExplodingDie(BaseDie):
    '''Explode on highest roll. d20 -> d12.'''

    def __init__(self, size, xsize=None, explode_range=1, math_correct=False):
        ''':param xsize: exploding die size, = size if None'''
        if xsize is None:
            xsize = size
        assert xsize > 1
        assert explode_range < size
        assert explode_range < xsize

        def d(size=size, xsize=xsize, expode_range=explode_range):
            self._rolls = list()
            while True:
                roll = random.randint(1, size)
                self._rolls.append(roll)
                if roll + expode_range <= size:
                    break
                if math_correct:
                    self._rolls[-1] -= 1  # Decrement last roll so d8p (8+1) = 8.
                size = xsize
            return sum(self._rolls)

        super(ExplodingDie, self).__init__(size, 'd%ip', d)


class FighterExplodingDie(BaseDie):
    '''Fighters roll 2 damage dice, take highest initial roll, explode that as
    appropriate.
    '''
    def __init__(self, size, expode_range=1):
        super(FighterExplodingDie, self).__init__(size, 'd%ifx')

        def d(explode=False):
            if not explode:
                roll = max(random.randint(1, size), random.randint(1, size))
                self._roll = roll
            else:
                roll = random.randint(1, size)
            if roll > (size - expode_range):
                roll += (d(True) - 1)
            return roll
        self.die = d


d2 = Die(2)
d3 = Die(3)
d4 = Die(4)
d6 = Die(6)
d8 = Die(8)
d10 = Die(10)
d12 = Die(12)
d16 = Die(16)
d20 = Die(20)
d24 = Die(24)
d30 = Die(30)
d100 = Die(100)

d2x = ExplodingDie(2)
d3x = ExplodingDie(3)
d4x = ExplodingDie(4)
d6x = ExplodingDie(6)
d8x = ExplodingDie(8)
d10x = ExplodingDie(10)
d12x = ExplodingDie(12)
d16x = ExplodingDie(16)
d20x = ExplodingDie(20)
d24x = ExplodingDie(24)
d30x = ExplodingDie(30)
d100x = ExplodingDie(100)

# Hackmaster style exploding dice
#   Subtract 1 from each exploded die.
#   Some dice explode to lower die, e.g. d20 explodes to d6.
d2p = ExplodingDie(2, math_correct=True)
d3p = ExplodingDie(3, math_correct=True)
d4p = ExplodingDie(4, math_correct=True)
d6p = ExplodingDie(6, math_correct=True)
d8p = ExplodingDie(8, math_correct=True)
d10p = ExplodingDie(10, math_correct=True)
d12p = ExplodingDie(12, math_correct=True)
d16p = ExplodingDie(16, math_correct=True)
d20p = ExplodingDie(20, 6, math_correct=True)
d24p = ExplodingDie(24, 8, math_correct=True)
d30p = ExplodingDie(30, 12, math_correct=True)
d100p = ExplodingDie(100, 20, math_correct=True)
