#!/usr/bin/env python
'''Quick hack to roll D&D character abilities.'''

import sys
import die


d6 = die.Standard(6)
three = die.Roll([d6, d6, d6], '3d6')
four = die.Roll([d6, d6, d6, d6], '4d6')


if len(sys.argv) > 1:
    def roll():
        fuck = four(func=lambda x: x)
        return sum(fuck) - min(fuck), fuck
else:
    def roll():
        fuck = three(func=lambda x: x)
        return sum(fuck), fuck

for ability in ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'):
    total, dice = roll()
    print ability, '%2s (%s)' % (total, ''.join(str(x) for x in dice))
