#!/usr/bin/env python3
"""Simple command line dice roller.

One or more rolls seperated by whitespace.

Understands RPG dice notation: 3d6 d20+4 2d4-2 d6*3.
Drop lowest: 3d6d1.
Repeat rolls: 6x 3d6.
Single number '20' will be assumed to mean "roll die with that number sides", d20.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021
Website: http://trollandflame.blogspot.com/
"""

import re
import sys
import time
import random

random.seed(time.time())

DICE = re.compile(r'(\d+d)?(\d+)([-+*]\d+)?(d\d)?')

def parse(text, verbose):
    """Parse dice string."""
    match = DICE.match(text)
    count, die, mod, drop = match.groups()
    if count:
        count = int(count[:-1])
    else:
        count = 1
    die = int(die)
    rolls = [random.randint(1, die) for x in range(count)]
    if drop:
        drop = int(drop[1:])
        total = sum(sorted(rolls)[drop:])
    else:
        total = sum(rolls)
    match list(mod or ''):
        case ['+', *numbers]:
            op, mod = ' +', int(''.join(numbers))
            total += mod
        case ['-', *numbers]:
            op, mod = ' -', int(''.join(numbers))
            total -= mod
        case ['*', *numbers]:
            op, mod = ' *', int(''.join(numbers))
            total *= mod
        case _:
            op = mod = ''
    if verbose:
        text = ','.join(str(x) for x in rolls)
        if len(rolls) > 1 or mod:
            return f'{text}{op}{mod} = {total}'
        else:
            return f'{text}'
    else:
        return total


if __name__ == '__main__':
    rolls = 1
    verbose = True
    for arg in sys.argv[1:]:
        if '-q' == arg:
            verbose = False
            continue
        if 'x' in arg:
            rolls = int(arg[:-1])
            continue
        print('\n'.join(str(parse(arg, verbose)) for x in range(rolls)))
