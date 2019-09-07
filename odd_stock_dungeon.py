#!/usr/bin/env python3
'''Given level of dungeon roll monster/treasure stocking for 5 rooms.

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


rooms = 5
if len(sys.argv) == 1:
    level = 1
else:
    level = min(9, max(1, int(sys.argv[1])))


print('Level', level)
for i in range(rooms):
    contents = list()
    treasure = False
    if d6() <= 2:
        contents.append('%dHD monster' % MONSTER[level]())
        treasure = d6() <= 3
    else:
        treasure = d6() == 1
    if treasure:
        contents.append(f'{SILVER[level]():,}sp')
        if d6() <= 3:
            contents.append(f'{GOLD[level]():,}gp')
        if d100() <= GEMS[level]:
            contents.append('gems')
        if d100() <= JEWLERY[level]:
            contents.append('jewlery')
        if d100() <= MAGIC[level]:
            contents.append('magic')
    print(f'  Room {i + 1}: {", ".join(contents)}')
