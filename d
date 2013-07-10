#!/usr/bin/env python
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

add = lambda o: o
sub = lambda o: -o


def parse(text):
    op = add
    total = 0
    for bit in re.split(r'([+-])', text):
        if bit == '+':
            op = add
            continue
        if bit == '-':
            op = sub
            continue
        if 'd' in bit:
            count, die = bit.split('d')
            if not count:
                count = 1
            value = sum(random.randint(1, int(die)) for i in range(int(count)))
        else:
            value = int(bit)
        total += op(value)
    return total


if __name__ == '__main__':
    for roll in sys.argv[1:]:
        if 'd' in roll:
            print parse(roll),
        else:
            print parse('1d' + roll),
    print
