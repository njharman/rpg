'''Quick hack to roll D&D character abilities'''

import die
d6 = die.Standard(6)

stat = die.Roll([d6, d6, d6], '3d6')

for ability in ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'):
    print ability, stat()
