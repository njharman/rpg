#!/usr/bin/env python3
'''Simple command line dice roller.

One or more rolls seperated by whitespace.

Understands "RPG" dice notation 3d6 d20+4 2d4+2-2d6.
Also single number '20' will be assumed to mean "roll die with that number sides", d20.
'''

import re
import sys
import time
import random

random.seed(time.time())


def parse(text, verbose):
    op = int
    rolls = list()
    for bit in re.split(r'([+-])', text):
        if bit == '+':
            op = int
        elif bit == '-':
            op = lambda x: -(int(x))
        elif 'd' in bit:
            count, die = bit.split('d')
            if not count:
                count = 1
            rolls.extend(op(random.randint(1, int(die))) for x in range(int(count)))
        else:
            rolls.append(op(bit))
            op = int
    total = sum(rolls)
    if verbose:
        foo = [f'{rolls[0]:_}', ]
        foo.extend(f'{x:+}' for x in rolls[1:])
        return f'{total} [{"".join(foo)}]'
    else:
        return total


if __name__ == '__main__':
    count = 1
    verbose = True
    for arg in sys.argv[1:]:
        if '-q' == arg:
            verbose = False
            continue
        if 'x' in arg:
            count = int(arg[:-1])
            continue
        if 'd' not in arg:
            arg = '1d' + arg
        print('\n'.join(str(parse(arg, verbose)) for x in range(count)))
