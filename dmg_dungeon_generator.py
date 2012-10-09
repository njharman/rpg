#!/usr/bin/python
'''Generate dungeons. Closely based off of AD&D DMG's appendix A.

Version: 12/28/2008
Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain 2008.
Website: http://trollandflame.blogspot.com/
'''
import cmd
import random


class Table(object):
    '''Object that when evaluated into string will return random result from table.'''
    def __init__(self, dice, *table):
        '''
        @param dice: callable that returns something comparable to x.
        @param *table: list of tuples (x,foo1,foo2,fooN) where x is comparable to return value of dice and foo? are evaluatable into strings.
        '''
        self.dice = dice
        self.table = table

    def __str__(self):
        '''@return: foo1,foo2,fooN stringified and space separated, from row in table where x >= return value of dice.'''
        return ' '.join(str(s) for s in self.get_result())

    def get_result(self):
        roll = self.dice()
        for row in self.table:
            if row[0] >= roll:
                return row[1:]
        return self.table[-1][1:]


def table_d20(*table):
    return Table(lambda: random.randint(1, 20), *table)


def table_d100(*table):
    return Table(lambda: random.randint(1, 100), *table)


class fwd_ref(object):
    '''Allows forward referencing of Table objects'''
    def __init__(self, table):
        self.table = table

    def __str__(self):
        return str(globals().get(self.table))


Gas = table_d20(
    ( 7, '''gas obscures vision.''', ),
    ( 9, '''gas blinds for 1d6 turns.''', ),
    (12, '''gas fear!''', ),
    (13, '''gas sleep 2d6 turns.''', ),
    (18, '''gas strength +1d6 str.''', ),
    (19, '''gas sickness.''', ),
    (20, '''gas deadly poison.''', ),
    )

Illusionary_Wall = table_d20(
    ( 6, '''Illusionary wall concealing a spiked pit 10' deep.''', ),
    (10, '''Illusionary wall concealing a chute down 1 level that cannot be ascended in any manner.''', ),
    (20, '''Illusionary wall concealing a''', fwd_ref('Room'), fwd_ref('Monster'), fwd_ref('Treasure'), fwd_ref('Treasure')),
    )

Trick_or_Trap = table_d20(
    ( 5, '''Secret door.''', ),
    ( 7, '''Pit 10' deep.''', ),
    ( 8, '''Spiked pit 10' deep.''', ),
    ( 9, '''20'x20' elevator room descends 1 level and will not ascend for 30 turns.''', ),
    (10, '''20'x20' elevator room descends 2 levels and will not ascend for 30 turns.''', ),
    (11, '''20'x20' elevator room descends 2-5 levels plus 1 level per unsuccessful door opening attempt and will not ascend for 60 turns.''', ),
    (12, '''Wall 10' behind slides across passage for 40-60 turns.''', ),
    (13, '''Oil followed by flame falls on random chacters 2d6 fire damage.''', ),
    (14, '''Pit 10' deep with crushing sides.''', ),
    (15, '''Arrow trap 1-3 arrows 1 in 20 are poisoned.''', ),
    (16, '''Spear trap 1-3 spears 1 in 20 are poisoned.''', ),
    (17, '''60' of passage contains''', Gas, ),
    (18, '''Door falls outward causeing 1d10 damage or ceiling collapses 2d10 damage.''', ),
    (19, Illusionary_Wall, ),
    (20, '''Chute down 1 level. Cannot be ascended in any manner.''', ),
    )

Monster = table_d20(
    (12, '''Oh no a monster!''', ),
    )

Treasure_Guarded = table_d20(
    ( 2, '''with contact poison.''', ),
    ( 4, '''with contact poison on treasure.''', ),
    ( 6, '''with poisoned needles in lock.''', ),
    ( 7, '''with poisoned needles in handles.''', ),
    ( 8, '''with spring darts firing from front of container.''', ),
    ( 9, '''with spring darts firing from top of container.''', ),
    (10, '''with spring darts firing from inside bottom of container.''', ),
    (12, '''with blade scything across inside.''', ),
    (13, '''with poisonous vermin living inside.''', ),
    (14, '''with''', Gas, ),
    (15, '''with trapdoor opening infront of container.''', ),
    (16, '''with trapdoor opening 6' infront of container.''', ),
    (17, '''with stone block dropiping in front of container.''', ),
    (18, '''with spears from walls when container is opened.''', ),
    (19, '''with Explosive Runes.''', ),
    (20, '''with Symbol.''', ),
    )

Treasure_Hidden = table_d20(
    ( 3, '''and is invisible.''', ),
    ( 5, '''and is illsioned to hide appearance.''', ),
    ( 6, '''secret space under.''', ),
    ( 8, '''secret compartment.''', ),
    ( 9, '''in plain view.''', ),
    (10, '''disguised to be something else.''', ),
    (11, '''under trash/dung.''', ),
    (13, '''under loose stone in floor.''', ),
    (15, '''behind loose stone in wall.''', ),
    (20, '''in secret room nearby.''' ),
    )

Treasure_Disposition = table_d20(
    ( 8, Treasure_Guarded ),
    (20, Treasure_Hidden ),
    )

Treasure_Container = table_d20(
    ( 2, '''in bags''', ),
    ( 4, '''in sacks''', ),
    ( 6, '''in small coffers''', ),
    ( 8, '''in chests''', ),
    (10, '''in a huge chest''', ),
    (12, '''in pottery jars''', ),
    (14, '''in metal urns''', ),
    (16, '''in stone containers''', ),
    (18, '''in iron trunks''', ),
    (20, '''loose''', ),
    )

Treasure = table_d100(
    (25, '''1000 copper/level''',        Treasure_Container, Treasure_Disposition, ),
    (50, '''1000 silver/level''',        Treasure_Container, Treasure_Disposition, ),
    (65, '''750 electrum/level''',       Treasure_Container, Treasure_Disposition, ),
    (80, '''250 gold/level''',           Treasure_Container, Treasure_Disposition, ),
    (90, '''100 platinum/level''',       Treasure_Container, Treasure_Disposition, ),
    (94, '''1-4 gems/level''',           Treasure_Container, Treasure_Disposition, ),
    (97, '''1 piece of jewelry/level''', Treasure_Container, Treasure_Disposition, ),
    (100, '''a magic item''',            Treasure_Container, Treasure_Disposition, ),
    )

Chasm = table_d20(
    (10, '''bridged''', ),
    (15, '''jumpable''', ),
    (20, '''unbridged''', ),
    )

River = table_d20(
    (10, '''bridged''', ),
    (15, '''boats''', ),
    (20, '''unbridged''', ),
    )

Stream = table_d20(
    (15, '''bridged''', ),
    (20, '''unbridged''', ),
    )

PassageSpecial_Width = table_d20(
    ( 4, '''40' wide with columns down center''', ),
    ( 7, '''40' wide with double row of columns''', ),
    (10, '''50' wide with double row of columns''', ),
    (12, '''50' wide, columns 10' right and left support 10' wide upper galleries 20' above''', ),
    (15, '''10' wide''', Stream, '''stream bisecting''', ),
    (17, '''20' wide''', River, '''river bisecting''', ),
    (18, '''40' wide''', River, '''river bisecting''', ),
    (19, '''60' wide''', River, '''river bisecting''', ),
    (20, '''20' wide 150-200' deep''', Chasm, ''' chasm bisecting''', ),
    )

DMGPassage_Width = table_d20(
    (12, '''10' wide''', ),
    (16, '''20' wide''', ),
    (17, '''30' wide''', ),
    (18, '''5' wide''', ),
    (20, PassageSpecial_Width, ),
    )

# Very modified from DMG
Passage_Width = table_d20(
    (10, '''5' wide''', ),
    (16, '''10' wide''', ),
    (18, '''20' wide''', ),
    (20, PassageSpecial_Width, ),
    )

Magic_Pool = table_d20(
    ( 8, '''magic pool turns gold into (1-11) lead or (12-20) platinum''', ),
    (15, '''magic pool ads or subtracts 1d3 points from random ability score''', ),
    (17, '''talking pool that will grant 1 wish''', ),
    (20, '''teleporter pool''', ),
    )

Pool = table_d20(
    ( 8, '''''', ),
    (10, '''pool.''', ),
    (12, '''pool and''', Monster, ),
    (18, '''pool and''', Monster, Treasure, Treasure),
    (20, Magic_Pool, ),
    )

Contents_Stairs = table_d20(
    ( 5, '''up 1 level.''', ),
    ( 8, '''up 2 levels.''', ),
    (14, '''down 1 level.''', ),
    (19, '''down 2 levels.''', ),
    (20, '''down 3 levels.''', ),
    )

DMGContents = table_d20(
    (12, '''\n  It is empty.''', ),
    (14, '''\n  It contains a''', Monster, ),
    (17, '''\n  It contains:''', Monster, Treasure, Treasure),  # DMG says add 10%
    (18, '''\n  It contains DM Choice or stairs''', Contents_Stairs, ),
    (19, '''\n ''', Trick_or_Trap, ),
    (20, '''\n  It contains''', Treasure),
    )

Contents = table_d20(
    (10, '''\n  It is empty.''', ),
    (13, '''\n  It contains a''', Monster, ),
    (17, '''\n  It contains:''', Monster, Treasure, Treasure),  # DMG says add 10%
    (18, '''\n  It contains DM Choice or stairs''', Contents_Stairs, ),
    (19, '''\n ''', Trick_or_Trap, ),
    (20, '''\n  It contains''', Treasure),
    )

Beyond_Door = table_d20(
    ( 4, Passage_Width, '''parallel passage extending 30' in both directions. Or 10'x10'.''', ),
    ( 8, Passage_Width, '''passage straight ahead.''', ),
    ( 9, Passage_Width, '''passage ahead/behind 45deg.''', ),
    (10, Passage_Width, '''passage behind/ahead 45deg.''', ),
    (18, fwd_ref('Room'), Contents, ),
    (20, fwd_ref('Chamber'), Contents, ),
    )

Beyond_Exit = table_d20(
    (16, Passage_Width, '''passage straight ahead.''', ),
    (18, Passage_Width, '''passage left/right 45 deg.''', ),
    (20, Passage_Width, '''passage right/left 45 deg.''', ),
    )

Exit_Location = table_d20(
    ( 7, '''In opposite wall a''', ),
    (12, '''In left wall a''', ),
    (17, '''In right wall a''', ),
    (20, '''In same wall a''', ),
    )

# diverges from DMG cause I want more than 1-20 chance for doors in rooms
Exit = table_d20(
    (10, '''\n ''', Exit_Location, Beyond_Exit, ),
    (20, '''\n ''', Exit_Location, '''door.''', ),
    )

_D4Exits = table_d20(
    ( 5, '''with 1 exit:''', Exit, ),
    (10, '''with 2 exits:''', Exit, Exit,),
    (15, '''with 3 exits:''', Exit, Exit, Exit,),
    (20, '''with 4 exits:''', Exit, Exit, Exit, Exit,),
    )

# The entire Small/Large thing diverges from DMG
Exits_Small = table_d20(
    ( 3, '''with 1 exit:''', Exit, ),
    ( 6, '''with 2 exits:''', Exit, Exit,),
    ( 9, '''with 3 exits:''', Exit, Exit, Exit,),
    (12, '''with a chance of (1-5 secret door, 6-10 one-way door, 11-20 nothing) per 10' abutting previously explored areas.''', ),
    (15, '''with a chance of (1-5 secret door, 6-10 one-way door, 11-20 nothing) per 10' abutting previously explored areas.''', ),
    (18, _D4Exits, ),
    (20, '''with 1 exit:''', Exit, ),  # DMG says door for chamber and passage for room, but I want more doors dammit!
    )

Exits_Large = table_d20(
    ( 3, '''with 2 exits:''', Exit, Exit, ),
    ( 6, '''with 3 exits:''', Exit, Exit, Exit,),
    ( 9, '''with 4 exits:''', Exit, Exit, Exit, Exit,),
    (12, '''with 1 exit:''', Exit, ),
    (15, '''with 1 exit:''', Exit, ),
    (18, _D4Exits, ),
    (20, '''with 1 exit:''', Exit, ),  # DMG says door for chamber and passage for room, but I want more doors dammit!
    )

Room_or_Chamber = table_d20(
    (15, '''room''', ),
    (20, '''chamber''', ),
    )

Circular_Chamber = table_d20(
    ( 5, '''circular''', Room_or_Chamber, Pool, ),
    ( 7, '''circular''', Room_or_Chamber, '''and well''', ),
    (10, '''circular''', Room_or_Chamber, '''and shaft''', ),
    (20, '''circular''', Room_or_Chamber, ),
    )

UnusualShape = table_d20(
    ( 5, Circular_Chamber, ),
    ( 8, '''triangular''', Room_or_Chamber, ),
    (11, '''trapezoidal''', Room_or_Chamber, ),
    (13, '''room/chamber, whatever shape/size fits map.''', ),
    (15, '''oval''', Room_or_Chamber, ),
    (15, '''hexagonal''', Room_or_Chamber, ),
    (19, '''octangonal''', Room_or_Chamber, ),
    (20, '''cave''', ),
    )

Unusual_Chamber = table_d20(
    ( 3, '''A ~500 sq. ft.''', UnusualShape, Exits_Small, ),
    ( 6, '''A ~900 sq. ft.''', UnusualShape, Exits_Small, ),
    ( 8, '''A ~1300 sq. ft.''', UnusualShape, Exits_Large, ),
    (10, '''A ~2000 sq. ft.''', UnusualShape, Exits_Large, ),
    (12, '''A ~2700 sq. ft.''', UnusualShape, Exits_Large, ),
    (14, '''A ~3400 sq. ft.''', UnusualShape, Exits_Large, ),
    (20, '''Big as you want''', UnusualShape, '''with whatever exits floats your boat.'''),  # diverges from DMG cause it would be pain in the ass to implement
    )

Room = table_d20(
    ( 2, '''10'x10' room''', Exits_Small, ),
    ( 4, '''20'x20' room''', Exits_Small, ),
    ( 6, '''30'x30' room''', Exits_Large, ),
    ( 8, '''40'x40' room''', Exits_Large, ),
    (10, '''10'x20' room''', Exits_Small, ),
    (13, '''20'x30' room''', Exits_Small, ),
    (15, '''20'x40' room''', Exits_Large, ),
    (17, '''30'x40' room''', Exits_Large, ),
    (20, Unusual_Chamber, ),
    )

Door = table_d20(
    ( 6, '''Door left leading to a''', Beyond_Door, ),
    (12, '''Door right leading to a''', Beyond_Door, ),
    (20, '''Door ahead leading to a''', Beyond_Door, ),
    )

SidePassage = table_d20(
    ( 2, Passage_Width, '''side passage to left 90 deg.''', ),
    ( 4, Passage_Width, '''side passage to right 90 deg.''', ),
    ( 5, Passage_Width, '''side passage ahead left 45 deg.''', ),
    ( 6, Passage_Width, '''side passage behind right 45 deg.''', ),
    ( 7, Passage_Width, '''side passage ahead left 45 deg.''', ),
    ( 8, Passage_Width, '''side passage behind right 45 deg.''', ),
    ( 9, Passage_Width, '''side passage curves ahead left 45 deg.''', ),
    (10, Passage_Width, '''side passage curves ahead right 45 deg.''', ),
    (13, Passage_Width, '''T intersection.''', ),
    (15, '''Y intersection.''', ),
    (19, Passage_Width, '''4-way intersection.''', ),
    (20, Passage_Width, '''X intersection (horizontal or vertical present passage forms fifth passage into X).''', ),
    )

PassageTurns = table_d20(
    ( 8, '''left 90 deg.''', ),
    ( 9, '''left ahead 45 deg.''', ),
    (10, '''left behind 45 deg.''', ),
    (18, '''right 90 deg.''', ),
    (19, '''right ahead 45 deg.''', ),
    (20, '''right behind 45 deg.''', ),
    )

Chamber = table_d20(
    ( 4, '''20'x20' chamber''', Exits_Small, ),
    ( 6, '''30'x30' chamber''', Exits_Large, ),
    ( 8, '''40'x40' chamber''', Exits_Large, ),
    (13, '''20'x30' chamber''', Exits_Small, ),
    (15, '''30'x50' chamber''', Exits_Large, ),
    (17, '''40'x60' chamber''', Exits_Large, ),
    (20, Unusual_Chamber, ),
    )

Stairs = table_d20(
    ( 5, '''Stairs down 1 level to a''', fwd_ref('Onward'), ),
    ( 6, '''Stairs down 2 levels to a''', fwd_ref('Onward'), ),
    ( 7, '''Stairs down 3 levels to a''', fwd_ref('Onward'), ),
    ( 8, '''Stairs up 1 level to a''', fwd_ref('Onward'), ),
    ( 9, '''Stairs up to dead end.''', ),
    (10, '''Stairs down to dead end.''', ),
    (11, '''Chimney up 1 level to a''', fwd_ref('Onward'), '''\nPassage continues check again after 30'.''', ),
    (12, '''Chimney up 2 levels to a''', fwd_ref('Onward'), '''\nPassage continues check again after 30'.''', ),
    (13, '''Chimney down 1 level to a''', fwd_ref('Onward'), '''\nPassage continues check again after 30'.''', ),
    (16, '''Trap door down 1 level to a''', fwd_ref('Onward'), '''\nPassage continues check again after 30'.''', ),
    (17, '''Trap door down 2 level to a''', fwd_ref('Onward'), '''\nPassage continues check again after 30'.''', ),
    (20, '''Trap door up 1 level to a''', fwd_ref('Onward'), '''\nPassage continues check again after 30'.''', ),  # modification of DMG's wonky result
    )

Onward = table_d20(
    ( 2, '''Straight ahead. Check again after 60'.''', ),
    ( 5, Door, '''Check again after 30'.''', ),
    (10, SidePassage, '''Check again after 30'.''', ),
    (13, '''Passage turns''', PassageTurns, '''Check again after 30'.''', ),
    (16, Chamber, Contents, '''\nCheck again after leaving for 30'.''', ),
    (17, Stairs, ),
    (18, '''Dead end. Chance of a (1-5 secret door, 6-10 one-way door, 11-20 nothing) per 10' abutting previously explored areas.''', ),
    (19, Trick_or_Trap, '''Check again after 30'.''', ),
    # no wandering monsters double chance of trick/trap
    #(20, fwd_ref('Onward'), '''Wandering Monster!''', ),
    )


if __name__ == '__main__':
    class OnwardToAdventure(cmd.Cmd):
        '''Simple text intefrace to random dungeon generator'''
        intro = '''Random Dungeon Delve.\nBased off of 1st edition AD&D Dungeon Master's Guide. A tool for DM's to use while generating random dungeons.\n\n? for help.\n<enter> to explore!'''
        prompt = '\nAdventure awaits: '

        def __init__(self, *arg, **kwarg):
            cmd.Cmd.__init__(self, *arg, **kwarg)  # Cmd is not a new style class wtf? super(OnwardToAdventure, self).__init__(*arg, **kwarg)
            # Cmd is stupid, why not use doc strings for help?
            for name, func in self.__dict__.items():
                if name.startswith('do_') and func.__doc__:
                    def help_foo(self):
                        print func.__doc__
                        setattr(self, 'help_%s' % name[2:], help_foo)

        def emptyline(self):
            '''Default action'''
            print Onward

        def help_about(self):
            print '''Written by njharman@gmail.com Dec, 2008.  source code is in the public domain.'''

        def help_help(self):
            print '''You're not the sharpest sword in the rack, are you?'''

        def do_flee(self, line):
            '''Run bravely away and exit dungeon.'''
            print 'Till next time...'
            return True

        def do_onward(self, line):
            '''Onward to adventure!  Generates new dungeon feature.  Same as pressing <enter>.'''
            print Onward

        def do_opendoor(self, line):
            '''See what's beyond. Creaaaak.'''
            print Beyond_Door

        def do_room(self, line):
            '''Generate a room(smaller) complete with contents.'''
            print Room, Contents

        def do_chamber(self, line):
            '''Generate a chamber(larger) complete with contents.'''
            print Chamber, Contents

        def do_trick_or_trap(self, line):
            '''Ha!'''
            print Trick_or_Trap

        def do_pools_are_cool(self, line):
            '''There's a chance for no pool :( keep trying.'''
            print Pool

        def do_contents(self, line):
            '''Generate room or chamber contents.'''
            print Contents

        def do_treasure(self, line):
            '''Generate fabulous riches.'''
            print Treasure

    dungeon = OnwardToAdventure()
    dungeon.cmdloop()
