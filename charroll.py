#!/usr/bin/env python
'''Quick hack to roll D&D character abilities.'''

import sys

import die


d6 = die.Standard(6)
d6m = lambda: max(1, d6()-1)
d6p = lambda: d6()+1
three = die.Roll([d6, d6, d6], '3d6')
four = die.Roll([d6, d6, d6, d6], '4d6')


def fourdsix():
    roll = four(func=lambda x: x)
    return sum(roll) - min(roll), roll


def threedsix():
    roll = three(func=lambda x: x)
    return sum(roll), roll


if len(sys.argv) == 3:
    level = int(sys.argv[1])
    hitdie = {'mu':d6m}[(sys.argv)[2]]
    roll = [hitdie() for x in range(level)]
    print sum(roll), roll
    sys.exit()
elif len(sys.argv) > 1:
    roll = fourdsix
else:
    roll = threedsix

for ability in ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'):
    total, dice = roll()
    print ability, '%2s (%s)' % (total, ''.join(str(x) for x in dice))

# scores = list()
# for i in range(33):
#     abilities = sorted([fourdsix()[0] for i in range(8)], reverse=True)
#     scores.append((sum(abilities[1:7]), abilities[1:7], (abilities[0], abilities[7])))
# abilities = (9999, 15, 14, 13, 12, 10, 8, 0)
# scores.append((sum(abilities[1:7]), abilities[1:7], (abilities[0], abilities[7])))

# scores.sort(reverse=True)

# for abilities in scores:
#     print '%-3s %-20s : %s' % (abilities[0], ' '.join(map(str, abilities[1])), abilities[2])
