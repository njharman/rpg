import click

from dice import d6, d12, d100

# CSIO
# 1 Attacked by Surprise
# 2 Attacked
# 3 Slanders / Insults
# 4 Question Characetrs
# 5 PROPOSITION
# 6 SPECIAL
#
# 1-4 Men (3 SL)
# 5 unusual
# 6 per-quarter
#
# UNUSUAL
# 1  troll
# 2  paladin
# 3  shadows
# 4  harpies
# 5  lammasu
# 6  giant
# 7  thief
# 8  wight
# 9  golem
# 10 wraith
# 11 blink dog
# 12 zombies
# 13 skeletions
# 14 dervicshes
# 15 illusionist
# 16 invisible stalker
# 17 mind flayer
# 18 dragon
# 19 priest
# 20 mage
#
# SPECIAL
# 1  spit on
# 2  dishwater
# 3  meathook
# 4  chamber pot emptied upon
# 5  clay pot hits
# 6  brik hits
# 7  runaway carriage
# 8  street caves
# 9  impress gang
# 10 were-rats kidnap
# 11 begger
# 12 drunks
# 13 messenger
# 14 performaer
# 15 lamplighter
# 16 buffon
# 17 vigilantes
# 18 town crier
# 19 fugitive
# 20 hypnotive
#
# PROPOSITION
# 1 challenge
# 2 search
# 3 task/mission
# 4 work offer
# 5 sexual
# 6 kidnap player
#
# noble
# 1 Sheriif
# 2 Knight
# 3 Genera
# 4 Gentleman
# 5 noble
# 6 noble
#
# common quarter
# 1 goblin
# 2 orc
# 3 orgre
# 4 bandit
# 5 dwarf
# 6 g. rat
#
# plazas quarter
# 1 sharper
# 2 begger
# 3 slaver
# 4 performaer
# 5 bard
# 6 mercenary
#
# seafront quarter
# 1 sailor
# 2 sailor
# 3 bucanner
# 4 pirate
# 5 sea capt
# 6 begger
#
# merchant quarter
# 1 robber
# 2 guard
# 3 merchant
# 4 merchant
# 5 merchant
# 6 merchant
#
# thieves quarter
# 1 apprentice
# 2 apprentice
# 3 footpad
# 4 robber
# 5 burglar
# 6 cutpurse


@click.group()
@click.option('-r', '--roll', default=None, type=int, help='Use this d100 roll.')
@click.pass_context
def cli(ctx, low_level, odd, roll):
    '''Roll up BX random encounters.'''
    ctx.obj['roll'] = roll



if __name__ == '__main__':
    cli(obj={})
