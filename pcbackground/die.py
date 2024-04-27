import random


def do_roll(roll):
    """Given simple roll forumula [40+]2d6 return integer"""
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
    """Create "labels" that make 1d(size) "die rolls" when called, used as int
    or converted to str.
    """

    def __init__(self, size):
        def d(size=size):
            return random.randint(1, size)
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


d4 = DieFactory(4)
d6 = DieFactory(6)
d8 = DieFactory(8)
d10 = DieFactory(10)
d12 = DieFactory(12)
d20 = DieFactory(20)
d100 = DieFactory(100)

__all__ = ("do_roll", "d4", "d6", "d8", "d10", "d12", "d20", "d100")
