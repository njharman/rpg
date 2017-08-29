#!/usr/bin/env python2
from __future__ import print_function
'''Given level of dungeon roll monster/treasure stocking for 9 rooms.

According to OD&D
'''

import sys
import random

d6 = lambda: random.randint(1, 6)
d12 = lambda: random.randint(1, 12)
d100 = lambda: random.randint(1, 100)


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


rooms = 9
level = int(sys.argv[1])


print('Level', level)
print()
for i in range(rooms):
    things = list()
    treasure = False
    if d6() <= 2:
        things.append('%dHD monster' % MONSTER[level]())
        treasure = d6() <= 3
    else:
        treasure = d6() == 1
    if treasure:
        things.append('%dsp' % SILVER[level]())
        if d6() <= 3:
            things.append('%dgp' % GOLD[level]())
        if d100() <= GEMS[level]:
            things.append('gems')
        if d100() <= JEWLERY[level]:
            things.append('jewlery')
        if d100() <= MAGIC[level]:
            things.append('magic')
    print('Room %i: %s' % (i + 1, ', '.join(things)))
