#!/usr/bin/env python
'''Generating a Random Treasure Hoard according to Sword & Wizardry Complete Rules.

Quick, dirty, incomplete.  Changes from Swords & Wizardy include; gem & jewerly
values are rounded, reorded potions and Minor Magic roll so healing more common
than Diminution and the Clair*, cosmetic changes to text.

Swords & Wizardry, S&W, and Mythmere Games are trademarks of Matthew J. Finch.
Author is not affiliated with Matthew J. Finch, Mythmere Games(TM), or Frog God
Games(TM).

Author: Norman J. Harman Jr. <njharman@gmail.com>
Website: http://trollandflame.blogspot.com/

This entire work is designated as Open Game Content under the OGL

Open Game Content may only be Used under and in terms of the Open Game License (OGL).

OPEN GAME LICENSE Version 1.0a The following text is the property of Wizards of the Coast, Inc. and is Copyright 2000 Wizards of the Coast, Inc ("Wizards").  All Rights Reserved.

1. Definitions: (a)"Contributors" means the copyright and/or trademark owners who have contributed Open Game Content; (b)"Derivative Material" means copyrighted material including derivative works and translations (including into other computer languages), potation, modification, correction, addition, extension, upgrade, improvement, compilation, abridgment or other form in which an existing work may be recast, transformed or adapted; (c) "Distribute" means to reproduce, license, rent, lease, sell, broadcast, publicly display, transmit or otherwise distribute; (d)"Open Game Content" means the game mechanic and includes the methods, procedures, processes and routines to the extent such content does not embody the Product Identity and is an enhancement over the prior art and any additional content clearly identified as Open Game Content by the Contributor, and means any work covered by this License, including translations and derivative works under copyright law, but specifically excludes Product Identity. (e) "Product Identity" means product and product line names, logos and identifying marks including trade dress; artifacts; creatures characters; stories, storylines, plots, thematic elements, dialogue, incidents, language, artwork, symbols, designs, depictions, likenesses, formats, poses, concepts, themes and graphic, photographic and other visual or audio representations; names and descriptions of characters, spells, enchantments, personalities, teams, personas, likenesses and special abilities; places, locations, environments, creatures, equipment, magical or supernatural abilities or effects, logos, symbols, or graphic designs; and any other trademark or registered trademark clearly identified as Product identity by the owner of the Product Identity, and which specifically excludes the Open Game Content; (f) "Trademark" means the logos, names, mark, sign, motto, designs that are used by a Contributor to identify itself or its products or the associated products contributed to the Open Game License by the Contributor (g) "Use", "Used" or "Using" means to use, Distribute, copy, edit, format, modify, translate and otherwise create Derivative Material of Open Game Content. (h) "You" or "Your" means the licensee in terms of this agreement.
2. The License: This License applies to any Open Game Content that contains a notice indicating that the Open Game Content may only be Used under and in terms of this License. You must affix such a notice to any Open Game Content that you Use. No terms may be added to or subtracted from this License except as described by the License itself.  No other terms or conditions may be applied to any Open Game Content distributed using this License.
3. Offer and Acceptance: By Using the Open Game Content You indicate Your acceptance of the terms of this License.
4. Grant and Consideration: In consideration for agreeing to use this License, the Contributors grant You a perpetual, worldwide, royalty-free, non-exclusive license with the exact terms of this License to Use, the Open Game Content.
5. Representation of Authority to Contribute: If You are contributing original material as Open Game Content, You represent that Your Contributions are Your original creation and/or You have sufficient rights to grant the rights conveyed by this License.
6. Notice of License Copyright: You must update the COPYRIGHT NOTICE portion of this License to include the exact text of the COPYRIGHT NOTICE of any Open Game Content You are copying, modifying or distributing, and You must add the title, the copyright date, and the copyright holder's name to the COPYRIGHT NOTICE of any original Open Game Content you Distribute.
7. Use of Product Identity: You agree not to Use any Product Identity, including as an indication as to compatibility, except as expressly licensed in another, independent Agreement with the owner of each element of that Product Identity. You agree not to indicate compatibility or co-adaptability with any Trademark or Registered Trademark in conjunction with a work containing Open Game Content except as expressly licensed in another, independent Agreement with the owner of such Trademark or Registered Trademark.  The use of any Product Identity in Open Game Content does not constitute a challenge to the ownership of that Product Identity. The owner of any Product Identity used in Open Game Content shall retain all rights, title and interest in and to that Product Identity.
8. Identification: If you distribute Open Game Content You must clearly indicate which portions of the work that you are distributing are Open Game Content.
9. Updating the License: Wizards or its designated Agents may publish updated versions of this License. You may use any authorized version of this License to copy, modify and distribute any Open Game Content originally distributed under any version of this License.
10. Copy of this License: You MUST include a copy of this License with every copy of the Open Game Content You Distribute.
11. Use of Contributor Credits: You may not market or advertise the Open Game Content using the name of any Contributor unless You have written permission from the Contributor to do so.
12. Inability to Comply: If it is impossible for You to comply with any of the terms of this License with respect to some or all of the Open Game Content due to statute, judicial order, or governmental regulation then You may not Use any Open Game Material so affected.
13. Termination: This License will terminate automatically if You fail to comply with all terms herein and fail to cure such breach within 30 days of becoming aware of the breach.  All sublicenses shall survive the termination of this License.
14. Reformation: If any provision of this License is held to be unenforceable, such provision shall be reformed only to the extent necessary to make it enforceable.

15. COPYRIGHT NOTICE
Open Game License v 1.0a Copyright 2000, Wizards of the Coast, Inc.
System Reference Document Copyright 2000-2003, Wizards of the Coast, Inc.; Authors
Jonathan Tweet, Monte Cook, Skip Williams, Rich Baker, Andy Collins, David
Noonan, Rich Redman, Bruce R. Cordell, John D. Rateliff, Thomas Reid, James
Wyatt, based on original material by E. Gary Gygax and Dave Arneson.
Swords & Wizardry Core Rules, Copyright 2008, Matthew J. Finch
Swords & Wizardry Complete Rules, Copyright 2010, Matthew J. Finch
sw_hoard.py, Copyright 2012, Norman J. Harman Jr.
'''

import sys
import random
import collections

from dice import *


POTIONS = [
        (3, 'Animal Control'),
        (6, 'Clairaudience'),
        (9, 'Clairvoyance'),
        (12, 'Diminution'),
        (15, 'Dragon Control'),
        (18, 'Ethereality'),
        (21, 'Fire Resistance'),
        (24, 'Flying'),
        (25, 'Frozen Concoction'),
        (27, 'Gaseous Form'),
        (30, 'Giant Strength'),
        (33, 'Growth'),
        (36, 'Slipperiness'),
        (39, 'Invisibility'),
        (42, 'Invulnerability'),
        (45, 'Levitation'),
        (48, 'Plant Control'),
        (55, 'Poison'),
        (58, 'Heroism'),
        (61, 'Treasure Finding'),
        (64, 'Undead Control'),
        (75, 'Extra Healing'),
        (100, 'Healing'),
        ]

SCROLLS_PROTECTION = [
        '''Protection from Demons: All within a 10' radius around the reader are protected from the attacks of 1 demon per round. Duration: 40 minutes.''',
        '''Protection from Drowning: All within a 10' radius of the reader gain the ability to breathe underwater. Duration: 1 full day.''',
        '''Protection from Elementals: This scroll protects against a single elemental.  Duration: 40 minutes.''',
        '''Protection from Magic: An anti-magic shell with a radius of 10' surrounds and moves with the reader; spells cannot pass in or out of the shell. Duration: 1 hour.''',
        '''Protection from Metal: Metal cannot harm the reader. Duration: 1 hour.''',
        '''Protection from Poison: Poisons have no effect upon one who reads such a scroll aloud; moreover, any poisons, active or quiescent, in the scroll reader's body are instantly removed. Duration: 6 hours.''',
        '''Protection from Undead: All within a 10' radius of the reader are protected against undead, but only to a limited degree. In any given round, 2d12 undead with fewer than 4 HD, and 2d6 undead with 4-5 HD, and d6 undead with 6+ HD are foiled by the protection of the scroll. Thus, the scroll is effective against all but a vast horde of undead. Duration: 1 hour.''',
        '''Protection from Were-creatures: All within a 10' radius around the reader are protected from lycanthropes. Duration: 1 hour.''',
        ]

CURSES = [
        '''Blindness (3d6 turns)''',
        '''Causes an aversion: roll d6. The character gains a strong aversion to: (1) Swords, (2) Spiders, (3) Armor, (4) Spell casting, (5) Bathing, (6) Being underground.''',
        '''Confusion. Character acts randomly.''',
        '''Despondency (d6 days' duration).  The character will refuse to go anywhere, as there is simply no point to it.''',
        '''Dimensional Vortex. The character is physically sucked up into the scroll, appearing as a new word on the page until rescued by a remove curse spell.''',
        '''Hallucinations (3d6 turns). The exact nature of the hallucinations varies, but in general the character will either begin casting spells and/or attacking nearby people, or will remain fascinated by the colors, unwilling to move.''',
        '''Instant Death''',
        '''Levitation. The character levitates one inch off the ground, and cannot get back down.''',
        '''Lose 1d10 x100 experience points''',
        '''Lose one point of a randomly-determined ability score''',
        '''Magically adhesive scroll''',
        '''Obedience (3d6 turns). The character does what anyone suggests.''',
        '''Paralysis (3d6 turns)''',
        '''Paralysis: Everyone in a radius of 20' must make a saving throw or be paralyzed for 3d6 turns, with the exception of the reader of the scroll, who is unaffected.''',
        '''Permanent diminution in size. Some of these reduce the reader to half size (50%) and the rest reduce the reader to 6 inches tall.''',
        '''Polymorph: roll d6. The character turns into (1) a pig, (2) a mouse, (3) a flamingo, (4) a talking parrot, (5) a dog, (6) a water buffalo''',
        '''Sleep (until curse is removed). In some cases, magical sleep can be broken by a kiss. Otherwise, the curse can only be removed by magic.''',
        '''Smell. The character becomes foul-smelling for 1d8 days''',
        '''Turned to Stone''',
        '''Uncontrollable sneezing (3d6 turns). The reader is likely to attract wandering monsters, especially those that prey upon the weak.''',
        ]

ARMORS = ['Chain mail', 'Leather armor', 'Plate mail', 'Ring mail']

MELEE_WEAPONS = [
        (2, 'Battle Axe'),
        (3, 'Hand Axe'),
        (5, 'Dagger'),
        (6, 'Warhammer'),
        (7, 'Lance'),
        (10, 'Heavy Mace'),
        (11, 'Light Mace'),
        (12, 'Spear'),
        (13, 'Staff'),
        (14, 'Short Sword'),
        (15, 'Two-handed Sword'),
        (20, 'Long Sword'),
        ]

MISSILE_WEAPONS = [
        (8, '2d6 arrows'),
        (10, '1d10 sling stones'),
        (11, '1 javelin'),
        (15, '2d4 darts'),
        (20, '2d6 crossbow bolts'),
        ]

MINOR_WEAPON_ABILITY = [
        (5, 'Inflicts +1 damage in addition to its regular bonus to damage'),
        (6, 'Sheds light, 15\' radius'),
        (7, 'Sheds light, 30\' radius'),
        (8, 'Inflicts an additional +4 points of damage against a particular opponent type such as undead, dragons, demons, giants, etc.'),
        ]

CURSED_ARMS = [
        (2, '-1 weapon or armor'),
        (4, '-2 weapon or armor'),
        (5, '-3 weapon or armor'),
        (6, 'Attracts missiles (even those fired at others nearby), and grants +1 to hit on such missiles'),
        (7, 'Causes the wearer to run away from combat'),
        (8, 'Causes the wearer to charge into combat'),
        ]

LESSER_RINGS = [
        (1, 'Ring of Fire Resistance (A)'),
        (2, 'Ring of Invisibility (A)'),
        (3, 'Ring of Mammal Control (A)'),
        (4, 'Ring of Poison Resistance (A)'),
        (5, 'Ring of Protection, +1 (A)'),
        (6, 'Ring of Protection, +2 (A)'),
        ]

GREATER_RINGS = [
        (1, 'Ring of Djinni Summoning (A)'),
        (2, 'Ring of Human Control (A)'),
        (3, 'Ring of Regeneration (A)'),
        (4, 'Ring of Shooting Stars (A)'),
        (5, 'Ring of Spell Storing, Magic-User (M)'),
        (6, 'Ring of Spell Storing, Cleric (C)'),
        (7, 'Ring of Spell Turning (A)'),
        (8, 'Ring of Telekinesis (A)'),
        (9, 'Ring of Three Wishes (A)'),
        (10, 'Ring of X-ray Vision (A)'),
        ]

LESSER_WANDS = [
        (2, 'Wand, level 1 spell, 10 charges'),
        (4, 'Wand, level 2 spell, 5 charges'),
        (6, 'Wand, level 3 spell, 2 charges'),
        ]

GREATER_WANDS = [
        (1, 'Wand, level 3 spell, 10 charges'),
        (2, 'Wand, level 4 spell, 10 charges'),
        (3, 'Wand of Cold'),
        (4, 'Wand of Detection, enemies'),
        (5, 'Wand of Detection, magic'),
        (6, 'Wand of Detection, metal'),
        (7, 'Wand of Detection, traps & secret doors'),
        (8, 'Wand of Fear'),
        (9, 'Wand of Paralyzing'),
        (10, 'Wand of Polymorph'),
        ]

STAVES = [
        (1, 'Stave of Absorption (M)'),
        (2, 'Stave of Beguiling (C, M)'),
        (3, 'Stave of Command (C, M)'),
        (4, 'Stave of Healing (C)'),
        (5, 'Stave of Power (M)'),
        (6, 'Stave of Resurrection (C)'),
        (7, 'Stave of Snake (C)'),
        (8, 'Stave of Striking (C, M)'),
        (9, 'Stave of Withering (C)'),
        (10, 'Stave of Wizardry (M)'),
        ]

LESSER_MISC = [
        (1, 'Arrow of Direction (A)'),
        (2, 'Bag of Holding (A)'),
        (3, 'Boots of Elvenkind (A)'),
        (4, 'Boots of Speed or Boots of Leaping (50%/50%) (A)'),
        (5, 'Bracers of Defense, AC 6 [13] (A)'),
        (6, 'Chime of Opening (A)'),
        (7, 'Cloak of Elvenkind (A)'),
        (8, 'Cloak of Protection, +1 (C, M, T)'),
        (9, 'Cursed Item (A)'),
        (10, 'Decanter of Endless Water (A)'),
        (11, 'Dust of Appearance or Disappearance (50%/50%) (A)'),
        (12, 'Dust of Sneezing and Choking (A)'),
        (13, 'Gauntlets of Swimming and Climbing (C, F, T)'),
        (14, 'Horseshoes of Speed (horses)'),
        (15, 'Luckstone (A)'),
        (16, 'Manual of Beneficial Exercise (A)'),
        (17, 'Pipes of the Sewers (A)'),
        (18, 'Rope of Climbing (A)'),
        (19, 'Rope of Entanglement (A)'),
        (20, 'Spade of Excavation (F)'),
        ]

MEDIUM_MISC = [
        (1, 'Amulet against Scrying (A)'),
        (2, 'Boots of Flying (A)'),
        (3, 'Bracers of Defense, AC 4 [15] or AC 2 [17] (50%/50%) (A)'),
        (4, 'Carpet of Flying (A)'),
        (5, 'Cloak of Displacement (A)'),
        (6, 'Cloak of Protection, +2 or +3 (50%/50%)(C, M, T)'),
        (7, 'Deck of Many Things (A)'),
        (8, 'Figurine of the Onyx Dog (A)'),
        (9, 'Gauntlets of Ogre Power (C, F, T)'),
        (10, 'Helm of Reading Magic and Languages (A)'),
        (11, 'Hole, Portable (A)'),
        (12, 'Horn of Valhalla, Bronze (C, F)'),
        (13, 'Horn of Valhalla, Silver (A)'),
        (14, 'Jug of Alchemy (A)'),
        (15, 'Manual of Quickness (A)'),
        (16, 'Medallion of ESP (A)'),
        (17, 'Mirror of Mental Scrying (A)'),
        (18, 'Robe of Blending (A)'),
        (19, 'Robe of Eyes (M)'),
        (20, 'Robe of Wizardry (M)'),
        ]

GREATER_MISC = [
        (1, 'Amulet of Demon Control (C, M)'),
        (2, 'Beaker of Potions (A)'),
        (3, 'Censer, Bowl, Brazier, or Stone of Controlling Elementals (M)'),
        (4, 'Crystal Ball (M)'),
        (5, 'Efreeti Bottle (A)'),
        (6, 'Figurine of the Golden Lion (A)'),
        (7, 'Gauntlets of Dexterity (A)'),
        (8, 'Gem of Seeing (A)'),
        (9, 'Girdle of Giant Strength (A)'),
        (10, 'Helm of Fiery Brilliance (A)'),
        (11, 'Helm of Teleportation (M)'),
        (12, 'Horn of Blasting (A)'),
        (13, 'Horn of Valhalla, Iron (F)'),
        (14, 'Lenses of Charming (A)'),
        (15, 'Libram, Magical (level gain) (specific to one class)'),
        (16, 'Manual of Golems (M)'),
        (17, 'Manual of Intelligence (A)'),
        (18, 'Manual of Wisdom (A)'),
        (19, 'Necklace of Firebaubles (A)'),
        (20, 'Scarab of Insanity (A)'),
        ]


def TableFactory(table):
    def func(die, table=table):
        roll = die()
        for x, p in table:
            if roll <= x:
                return p
        raise Exception('roll [%i] is past end of table' % x)
    return func


potion = TableFactory(POTIONS)
lesser_ring = TableFactory(LESSER_RINGS)
greater_ring = TableFactory(GREATER_RINGS)
lesser_wand = TableFactory(LESSER_WANDS)
greater_wand = TableFactory(GREATER_WANDS)
staves = TableFactory(STAVES)
lesser_misc = TableFactory(LESSER_MISC)
medium_misc = TableFactory(MEDIUM_MISC)
greater_misc = TableFactory(GREATER_MISC)
_melee_weapon = TableFactory(MELEE_WEAPONS)
missile_weapon = TableFactory(MISSILE_WEAPONS)
minor_weapon_ability = TableFactory(MINOR_WEAPON_ABILITY)


def melee_weapon(die):
    '''25% of swords are unique'''
    weapon = _melee_weapon(die)
    if d4() == 4:
        weapon.replace('Sword', 'Unique Sword')
    return weapon


def scroll(roll):
    def pick(count, die):
        spells = list()
        for i in range(count):
            spells.append(levels[die() - 1])
        spells.sort()
        return 'scroll of %i spells; %s' % (len(spells), ', '.join(spells))
    d1 = lambda: 1
    d2 = lambda: random.randint(1, 1)
    d3 = lambda: random.randint(1, 3)
    levels = ('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th')
    prot = 'Scroll of ' + random.choice(SCROLLS_PROTECTION)
    curse = 'Cursed scroll! ' + random.choice(CURSES)
    sphere = random.choice(('Magic-user', 'Cleric'))
    return [
        '%s %s' % (sphere, pick(1, d1)),
        '%s %s' % (sphere, pick(1, d3)),
        '%s %s' % (sphere, pick(2, d2)),
        '%s %s' % (sphere, pick(3, d1)),
        curse,
        prot,
        '%s %s' % (sphere, pick(2, d4)),
        '%s %s' % (sphere, pick(2, lambda: d6() + 1)),
        '%s %s' % (sphere, pick(1, lambda: d6() + (1, 3)[sphere == 'Magic-user'])),
        '%s %s' % (sphere, pick(5, d3)),
        curse,
        prot + ' (double duration)',
        '%s %s' % (sphere, pick(5, d6)),
        '%s %s' % (sphere, pick(6, d6)),
        '%s %s' % (sphere, pick(7, d6)),
        '%s %s' % (sphere, pick(8, d6)),
        curse,
        prot + ' (triple duration and double effect if applicable)',
        ][roll - 1]  # Zero indexed.


def arms_n_armor(roll):
    curse = random.choice(CURSED_ARMS)
    armor = random.choice(ARMORS)
    return [
        'Cursed %s; %s' % (armor, curse),
        '+1 %s' % missile_weapon(d20),
        '+1 shield',
        '+1 %s' % melee_weapon(d20),
        '+1 %s' % armor,
        'Cursed %s; %s' % (melee_weapon(d20), curse),
        '+2 %s' % missile_weapon(d20),
        '+2 shield',
        '+2 %s' % melee_weapon(d20),
        '+2 %s' % armor,
        '+2 %s' % melee_weapon(d20),
        '+1 %s; %s' % (melee_weapon(d20), minor_weapon_ability(d8)),
        '+3 %s' % missile_weapon(d20),
        '+3 %s' % melee_weapon(d20),
        '+3 shield',
        '+3 %s' % armor,
        random.choice(('+1 blunt %(w)s that destroys undead', '+1 thrown %(w)s that returns to hand', '+1 %(w)s, extra attack', '%(w)s, +1, +2 vs. particular type of foe', '%(w)s, +1, +4 vs. particular type of foe', '%(w)s, +2, +3 vs. particular type of foe', '+4 %(w)s', '+5 %(w)s', 'Flaming %(w)s', 'Freezing %(w)s', 'Dancing %(w)s', 'Intelligent %(w)s')) % {'w': melee_weapon(d20)},
        random.choice(('+4 %(a)s', '+4 shield', '+5 %(a)s', '+5 shield', '%(a)s of Arrow Deflection', 'Demonic %(a)s', 'Ethereal %(a)s', 'Fiery %(a)s')) % {'a': armor},
        #][roll - 1]  # Zero indexed.
        ][roll - 1]  # Zero indexed.


def remarkable(roll):
    if roll in (1, 21, 22):
        return lesser_wand(d6)
    if roll in (23, 41, 42):
        return greater_wand(d10)
    if roll in (2, 23, 25):
        return lesser_ring(d6)
    if roll in (26, 43, 44):
        return greater_ring(d10)
    if 3 <= roll <= 20:
        return lesser_misc(d20)
    if 27 <= roll <= 40:
        return medium_misc(d20)
    if 46 <= roll <= 60:
        return greater_misc(d20)
    if roll == 45:
        return staves(d10)


def round_gem(gem):
    '''Round gems to regular values.'''
    if gem < 3:
        return 1
    if gem < 7:
        return 5
    if gem < 100:
        return int(round(gem, -1))
    if gem < 2500:
        return int(round(gem, -2))
    return int(round(gem, -3))


def round_gems(gems):
    return [round_gem(g) for g in gems]


def group_gems(gems):
    '''Group gems of similar values.'''
    grouped = list()
    for value, count in sorted(collections.Counter(gems).items()):
        if count > 1:
            grouped.append('%ix%i' % (count, value))
        else:
            grouped.append('%i' % (value,))
    return grouped


def group_potions(potions):
    '''Group like potions.'''
    grouped = list()
    for potion, count in sorted(collections.Counter(potions).items()):
        if count > 1:
            grouped.append('%s x %i' % (potion, count))
        else:
            grouped.append('%s' % (potion,))
    return grouped


def generate(amount):
    d75 = lambda: random.randint(1, 75)
    d50_100 = lambda: random.randint(50, 100)
    gp = amount
    gems = list()
    potions = list()
    scrolls = list()
    other = list()
    for i in range(amount / 100):
        if d10() == 10:
            gp -= 100
            if d20() == 20:
                random.choice([
                        lambda: potions.append(potion(d50_100)),
                        lambda: scrolls.append(scroll(d6())),
                        lambda: other.append(arms_n_armor(d6())),
                        lambda: other.append(remarkable(d20())),
                        ])()
            else:
                gems.append(random.choice([
                        lambda: d6(),
                        lambda: d100() + 25,
                        lambda: d100() + 75,
                        lambda: d100() * 10,
                        ])())
    for i in range(amount / 1000):
        if d10() == 10:
            gp -= 1000
            if d20() == 20:
                random.choice([
                        lambda: potions.extend(potion(d75) for _ in range(3)),
                        lambda: scrolls.append(scroll(d6() + 6)),
                        lambda: other.append(arms_n_armor(d6() + 6)),
                        lambda: other.append(remarkable(d20() + 20)),
                        ])()
            else:
                gems.append(random.choice([
                        lambda: d100(),
                        lambda: d6() * 200,
                        lambda: d6() * 300,
                        lambda: d100() * 100,
                        ])())
    for i in range(amount / 5000):
        if d10() == 10:
            gp -= 5000
            if d20() == 20:
                random.choice([
                        lambda: potions.extend(potion(d75) for _ in range(6)),
                        lambda: scrolls.append(scroll(d6() + 12)),
                        lambda: other.append(arms_n_armor(d6() + 12)),
                        lambda: other.append(remarkable(d20() + 40)),
                        ])()
            else:
                gems.append(random.choice([
                        lambda: d100() * 10,
                        lambda: d100() * 80,
                        lambda: d100() * 120,
                        lambda: d100() * 200,
                        ])())
    gems = round_gems(gems)
    potions = group_potions(potions)
    if len(potions) > 1:
        print 'Potions of %s, and %s' % (', '.join(potions[:-1]), potions[-1])
    elif potions:
        print 'Potion of %s' % potions[0]
    if scrolls:
        scrolls.sort()
        print '\n'.join(scrolls)
    if other:
        other.sort()
        print '\n'.join(other)
    print '\nTotal monetary value: %i' % (gp + sum(gems))
    if gp:
        print 'Coins: %i gp' % gp
    if gems:
        print 'Gems & Jewelry: %sgp' % 'gp, '.join(group_gems(gems))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage:'
        print '%s <gp value of hoard>' % sys.argv[0]
    else:
        generate(int(sys.argv[1]))
