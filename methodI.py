#!/usr/bin/env python3
"""Quick hack to roll D&D character abilities.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: http://trollandflame.blogspot.com/
"""

import sys

import die


d6 = die.Standard(6)
d6m = lambda: max(1, d6() - 1)
d6p = lambda: d6() + 1
three = die.Roll([d6, d6, d6], '3d6')
four = die.Roll([d6, d6, d6, d6], '4d6')


def fourdsix():
    """Sum, 4d6 drop lowest."""
    roll = four(func=lambda x: x)
    return sum(roll) - min(roll), roll


def threedsix():
    """Sum 3d6."""
    roll = three(func=lambda x: x)
    return sum(roll), roll


if len(sys.argv) == 3:
    level = int(sys.argv[1])
    hitdie = {'mu': d6m}[(sys.argv)[2]]
    roll = [hitdie() for x in range(level)]
    print(sum(roll), roll)
    sys.exit()
elif len(sys.argv) > 1:
    roll = fourdsix
else:
    roll = threedsix

for ability in ('Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha'):
    total, dice = roll()
    rolls = ''.join(str(x) for x in dice)
    print(f'{ability}: {total:2} ({rolls})')

# scores = list()
# for i in range(33):
#     abilities = sorted([fourdsix()[0] for i in range(8)], reverse=True)
#     scores.append((sum(abilities[1:7]), abilities[1:7], (abilities[0], abilities[7])))
# abilities = (9999, 15, 14, 13, 12, 10, 8, 0)
# scores.append((sum(abilities[1:7]), abilities[1:7], (abilities[0], abilities[7])))

# scores.sort(reverse=True)

# for abilities in scores:
#     print '%-3s %-20s : %s' % (abilities[0], ' '.join(map(str, abilities[1])), abilities[2])
