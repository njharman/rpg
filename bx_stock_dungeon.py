#!/usr/bin/env python3
'''Given level of dungeon roll monster/treasure stocking for 5 rooms.

According to B/X
'''

import sys
import random

d2 = lambda: random.randint(1, 2)
d4 = lambda: random.randint(1, 4)
d6 = lambda: random.randint(1, 6)
d12 = lambda: random.randint(1, 12)
d100 = lambda: random.randint(1, 100)

MONSTER = {
    1: lambda: (1, 1, 1, 2, 2, 3)[d6() - 1],
    2: lambda: (1, 2, 2, 2, 3, 4)[d6() - 1],
    3: lambda: (2, 3, 3, 3, 4, 4)[d6() - 1],
    4: lambda: (3, 4, 4, 4, 5, 6)[d6() - 1],
    5: lambda: (3, 4, 5, 5, 5, 6)[d6() - 1],
    6: lambda: (4, 5, 6, 6, 6, 7)[d6() - 1],
    7: lambda: (5, 6, 7, 7, 7, 8)[d6() - 1],
    8: lambda: (6, 7, 7, 8, 8, 9)[d6() - 1],
    9: lambda: (7, 8, 8, 9, 9, 19)[d6() - 1],
    }


def jewelry(x):
    foo = [f'{100*(d6()+d6()+d6()):,}' for x in range(x)]
    return f' {", ".join(foo)} jewelry;'


rooms = 5
if len(sys.argv) == 1:
    level = 1
else:
    level = min(9, max(1, int(sys.argv[1])))


print('Level', level)
for i in range(rooms):
    contents = list()
    treasure = False
    roll = d6()
    if roll <= 2:
        contents.append('Empty')
        treasure = d6() == 1
    elif roll <= 4:
        guarantee = ' guaranteed treasure' if d6() <= 3 else ''
        contents.append(f'{MONSTER[level]()}HD monster{guarantee}')
    elif roll == 5:
        contents.append('Special')
    elif roll == 6:
        contents.append('Trap')
        treasure = d6() <= 2
    if treasure:
        if level == 1:
            gp = f' {d6()*10}gp;' if d100() <= 50 else ''
            gem = f' {d6()} gems;' if d100() <= 5 else ''
            jew = jewelry(1) if d100() <= 2 else ''
            magic = f' 1 magic;' if d100() <= 2 else ''
            contents.append(f'{d6()*100:,}sp;{gp}{gem}{jew}{magic}')
        elif level <= 3:
            gp = f' {d6()*100:,}gp;' if d100() <= 50 else ''
            gem = f' {d6()} gems;' if d100() <= 10 else ''
            jew = jewelry(d2()) if d100() <= 5 else ''
            magic = f' 1 magic;' if d100() <= 8 else ''
            contents.append(f'{d12()*100:,}sp;{gp}{gem}{jew}{magic}')
        elif level <= 5:
            gem = f' {d6()} gems;' if d100() <= 20 else ''
            jew = jewelry(d4()) if d100() <= 10 else ''
            magic = f' 1 magic;' if d100() <= 10 else ''
            contents.append(f'{d6()*1000:,}sp; {d6()*200:,}gp;{gem}{jew}{magic}')
        elif level <= 7:
            gem = f' {d6()} gems;' if d100() <= 30 else ''
            jew = jewelry(d6()) if d100() <= 15 else ''
            magic = f' 1 magic;' if d100() <= 15 else ''
            contents.append(f'{d6()*2000:,}sp; {d6()*500:,}gp;{gem}{jew}{magic}')
        else:
            gem = f' {d6()} gems;' if d100() <= 40 else ''
            jew = jewelry(d6()) if d100() <= 20 else ''
            magic = f' 1 magic;' if d100() <= 20 else ''
            contents.append(f'{d6()*5000:,}sp; {d6()*1000:,}gp;{gem}{jew}{magic}')
    print(f'  Room {i + 1}: {", ".join(contents)}')
