#!/usr/bin/env python2
'''Simple command line dice roller.
Understands "RPG" dice notation 3d6 d20+4 2d4+2-2d6.
Also single number '20' will be assumed to mean "roll die with that number sides", d20.
One or more rolls seperated by whitespace.
'''

import re
import sys
import time
import random

random.seed(time.time())


def parse(text, verbose):
    op = ''
    rolls = []
    total = 0
    modifier = 0
    for bit in re.split(r'([+-])', text):
        if bit in ('+', '-'):
            op = bit
            continue
        if 'd' in bit:
            count, die = bit.split('d')
            if not count:
                count = 1
            rolls = [random.randint(1, int(die)) for i in range(int(count))]
        else:
            modifier = op(bit)
    total = sum(rolls) + modifier
    if verbose:
        poop = '%s %s' % (total, rolls)
        if modifier:
            poop += '%s%s' % (op, modifier)
        return poop
    else:
        return '%2d' % total


if __name__ == '__main__':
    count = 1
    verbose = False
    for arg in sys.argv[1:]:
        if '-v' == arg:
            verbose = True
            continue
        if 'x' in arg:
            count = int(arg[:-1])
            continue
        if 'd' not in arg:
            arg = '1d' + arg
        for i in range(count):
            print parse(arg, verbose),
    print
