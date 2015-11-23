'''Various Roleplaying game systems/rules "dice".

Classes::
    Die()
    ExplodingDie()
    FighterExplodingDie()

    All create callables that return die 'rolls'.

Die roll "functions" (actually instances of Die or subclasses::
    d?   Standard RPG dice notation.
    d?x  Exploding. If max value rolled, recurse roll += d().
    d?p  Hackmaster penetration dice.  If max value rolled, subtract one, recurse roll += d().
    drm  Rolemaster high open-ended d100.

Other functions::
    do_roll() interpret simple dice notation. I.e "d6+10", "2d10", etc.


Notes::
    The probability for k successes rolling n dice is::

        n! / (k!((n-k)!)) p^k q^{n-k}

    Where p=1/6 is the probability of success and q=1-p=5/6 is the probability of failure.

History::
    2.0.0 first version with a number
      - added drm().
      - changed do_roll to expect +x after. 2d6+10 vs 10+2d6.
      - changed ExplodingDie math_correct parameter to correct_math.
      - added __repr__ to classes.
'''

import random

__version__ = '2.0.0'

__all__ = (
    'do_roll',
    'Die', 'ExplodingDie', 'FighterExplodingDie',
    'd4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100',
    'd2', 'd3', 'd4', 'd6', 'd8', 'd10', 'd12', 'd16', 'd20', 'd24', 'd30', 'd100',
    'd2x', 'd3x', 'd4x', 'd6x', 'd8x', 'd10x', 'd12x', 'd16x', 'd20x', 'd24x', 'd30x', 'd100x',
    'd2p', 'd3p', 'd4p', 'd6p', 'd8p', 'd10p', 'd12p', 'd16p', 'd20p', 'd24p', 'd30p', 'd100p',
    'drm',
    )


def do_roll(notation):
    '''Given simple roll formula 2d6[+2] return integer result of making that roll.'''
    if '+' in notation:
        notation, roll = notation.split('+')
        roll = int(roll)
    else:
        roll = 0
    count, die = [int(x) for x in notation.split('d')]
    for i in range(count):
        roll += random.randint(1, die)
    return roll


class BaseDie(object):
    '''Create 'labels' that make 1d(size) 'die rolls' when called, used as int
    or converted to str.

    :param size: Number of faces on die.
    :param name_fmt: Used with size to set self.name.
    :param die_func: Callable, returns a roll of die.
    '''
    def __init__(self, size, name_fmt, die_func):
        assert size > 1  # Infinite loops are overrated.
        self.name = name_fmt % size
        self.die = die_func

    def __repr__(self):
        return '%s()' % (self.__class__.__name__, )

    def __call__(self):
        '''Return roll as integer when called.'''
        self._roll = self.die()
        return self._roll

    def __str__(self):
        '''Return roll when evaluated in string context.'''
        return str(self())

    def __int__(self):
        '''Return roll when evaluated in string context.'''
        return int(self())

    def __add__(self, other):
        '''Return roll + other.'''
        return int(self) + other

    def __sub__(self, other):
        '''Return roll - other.'''
        return int(self) - other

    def __radd__(self, other):
        '''Return roll + other.'''
        return int(self) + other

    def __rsub__(self, other):
        '''Return roll - other.'''
        return int(self) - other

    @property
    def natural(self):
        '''Return natural die roll, i.e. before any modifications.'''
        return self._roll


class Die(BaseDie):
    '''Create callables that make 1d(size) 'die rolls' when called, used in
    math or converted to str.

    :param size: Number of faces on die.
    '''
    def __init__(self, size):
        def d(size=size):
            return random.randint(1, size)
        super(Die, self).__init__(size, 'd%i', d)


class ExplodingDie(BaseDie):
    '''Create callables that make 1d(size) 'die rolls' when called, used in
    math or converted to str.

    On highest possible result, roll exploding die and add to total roll, recurse.

    :param size: Number of faces on die.
    :param xsize: [size]  Number of faces on exploding die.
    :param explode_range: [1] Explode on any roll > (max-n).
    :param correct_math: [False] Subtract 1 from roll for every exploding roll.
    '''
    def __init__(self, size, xsize=None, explode_range=1, correct_math=False):
        '''
        '''
        if xsize is None:
            xsize = size

        def d(size=size, xsize=xsize, explode_range=explode_range):
            self._rolls = list()
            while True:
                roll = random.randint(1, size)
                self._rolls.append(roll)
                if roll + explode_range <= size:
                    break
                if correct_math:
                    self._rolls[-1] -= 1  # Decrement last roll so d8p (8,1) = 8.
                size = xsize
            return sum(self._rolls)

        assert xsize > 1
        assert explode_range < size
        assert explode_range < xsize
        if correct_math:
            name = 'd%ip'
        else:
            name = 'd%ix'
        super(ExplodingDie, self).__init__(size, name, d)


class FighterExplodingDie(BaseDie):
    '''Create callables that make 1d(size) 'die rolls' when called, used in
    math or converted to str.

    Keep highest of two rolls. On highest possible result, roll exploding die
    and add to total roll, recurse.

    Note: Only initial roll is two dice.

    :param size: Number of faces on die.
    :param explode_range: [1] Explode on any roll > (max-n).
    '''
    def __init__(self, size, explode_range=1):
        super(FighterExplodingDie, self).__init__(size, 'd%ifx')

        def d(explode=False):
            if not explode:
                roll = max(random.randint(1, size), random.randint(1, size))
                self._roll = roll
            else:
                roll = random.randint(1, size)
            if roll > (size - explode_range):
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

# Hackmaster style exploding dice.
#   Subtract 1 from each exploded die.
#   Some dice explode to lower die, e.g. d20 explodes to d6.
d2p = ExplodingDie(2, correct_math=True)
d3p = ExplodingDie(3, correct_math=True)
d4p = ExplodingDie(4, correct_math=True)
d6p = ExplodingDie(6, correct_math=True)
d8p = ExplodingDie(8, correct_math=True)
d10p = ExplodingDie(10, correct_math=True)
d12p = ExplodingDie(12, correct_math=True)
d16p = ExplodingDie(16, correct_math=True)
d20p = ExplodingDie(20, 6, correct_math=True)
d24p = ExplodingDie(24, 8, correct_math=True)
d30p = ExplodingDie(30, 12, correct_math=True)
d100p = ExplodingDie(100, 20, correct_math=True)

# Rolemaster high open-ended d100.
drm = ExplodingDie(100, explode_range=5)
