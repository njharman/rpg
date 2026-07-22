#!/usr/bin/env python
"""Exploratory tests on hit probabilities of sheetless (draft name) RPG.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain June 2026.
Website: http://trollandflame.blogspot.com/
"""

import random
from collections import defaultdict

from die import d0, d3d6, d6, d8, d10, d20, d24, parse


class Character:
    def __init__(self, name, hit_die, hd=1, combat=1):
        self.name = name
        self.hit_die = hit_die
        self.health = d3d6() # same as Con
        #TODO: str, dex
        self.wounds = list()
        self.hd = hd

        self.ranks_combat = combat
        # rolled on start_combat()
        self.hp = 0

        # set by armor
        self.arm = 0
        # set by shield
        self.block = d0
        self.cover = 0
        # set by weapon
        self.dmg = d6
        self.attack = d20

    def __str__(self):
        dead = 'DEAD ' if self.dead else ''
        return f"{self.name} - {dead}Health:{self.health}{self.wounds} HP:{self.hp} Arm:{self.arm} Blk:{self.block.notation} Cov:{self.cover}+ {self.attack.notation}/{self.dmg.notation}"

    @property
    def dead(self):
        return self.health - sum(self.wounds) <= 0

    def start_combat(self):
        self.hp = sum(self.hit_die() for _ in range(self.hd))

    def take_damage(self, dmg):
        """First taken from hit protection, then absorbed by armor and then health"""
        if dmg <= 0:
            return ''
        if self.hp > 0:
            self.hp -= dmg
            if self.hp < 0:
                self.hp = 0
            return 'absorbed by hit protection'
        if self.arm == 0:
            self.wounds.append(dmg)
            if self.dead:
                return f"killed by {dmg} point wound"
            return f"took {dmg} point wound"
        new = dmg - self.arm
        if new > 0:
            self.wounds.append(new)
            if self.dead:
                return f"killed by {new} point wound after arm{self.arm} absorption"
            return f"took {new} point wound after arm{self.arm} absorption"
        return 'absorbed by armor'



class Item:
    def __init__(self, name, **kwargs):
        self.name = name
        self.attributes = kwargs

    def equip(self, character):
        for attr, value in self.attributes.items():
            setattr(character, attr, value)


class Mook:
    def __init__(self, name, ac, hd, dmg=d6):
        self.name = name
        self.ac = ac
        self.hd = hd
        self.dmg = dmg
        self.hits = 0

    def __str__(self):
        if self.taken_out:
            return f"{self.name} TAKEN OUT"
        return f"{self.name} {self.hd-self.hits}/{self.hd}HD {self.ac}AC {self.dmg.notation}"

    @property
    def taken_out(self):
        return self.hits >= self.hd


class Ogre(Mook):
    _counter = 0
    def __init__(self):
        Ogre._counter += 1
        super().__init__(f"Ogre{Ogre._counter}", ac=5, hd=4, dmg=d10)


class Orc(Mook):
    _counter = 0
    def __init__(self):
        Orc._counter += 1
        super().__init__(f"Orc{Orc._counter}", ac=6, hd=1, dmg=d6)


class Gnoll(Mook):
    _counter = 0
    def __init__(self):
        Gnoll._counter += 1
        super().__init__(f"Gnoll{Gnoll._counter}", ac=5, hd=2, dmg=d8)


class HillGiant(Mook):
    _counter = 0
    def __init__(self):
        HillGiant._counter += 1
        super().__init__(f"HillGiant{HillGiant._counter}", ac=4, hd=8, dmg=parse('2d8'))


class Noble(Mook):
    def __init__(self):
        super().__init__('Noble', ac=2, hd=3, dmg=d6)




def picktarget(targets):
    for x in targets:
        if not x.taken_out:
            return x


class Party:
    def __init__(self, *characters):
        self.combatants = characters

    def __str__(self):
        return '\n'.join(str(c) for c in self.combatants)

    def combat(self, *mooks):
        def party_attacks(melees):
            for character, targets in melees.items():
                if character.dead:
                    continue
                target = picktarget(targets)
                if not target:
                    print(f"{character.name} has no targets left", end='')
                    target = picktarget(mooks)
                    if not target:
                        print('.')
                        continue
                    print(f", jumps on {target.name} ...")
                target_number = 20 - target.ac - character.ranks_combat
                attack_roll = character.attack()
                if attack_roll >= target_number and attack_roll >= 20:
                    target.hits += 2
                    takeout = ' and takes out' if target.taken_out else ''
                    print(f"{character.name} crits{takeout} {target.name} {attack_roll} >= {target_number}")
                elif attack_roll >= target_number:
                    target.hits += 1
                    takeout = ' and takes out' if target.taken_out else ''
                    print(f"{character.name} hits{takeout} {target.name} {attack_roll} >= {target_number}")
                else:
                    print(f"{character.name} misses {target.name} {attack_roll} >= {target_number}")

        def mook_attacks(melees):
            for character, targets in melees.items():
                attacks = [(t.dmg(), t) for t in targets if not t.taken_out]
                if not attacks:
                    continue
                print(f"{character.name} Health:{character.health}{character.wounds} HP:{character.hp} attacked:")
                block = character.block()
                if block > 0:
                    dmg, t = attacks.pop()
                    if block > dmg:
                        print(f"  blocks {dmg} damage from {t.name} with {block} roll")
                    elif block == dmg:
                        print(f"  blocks {dmg} damage from {t.name} shattering their shield")
                        character.block = d0
                    else:
                       print(f"  {block} block fails, {t.name} inflicts {dmg} damage, {character.take_damage(dmg)}")
                for dmg, t in attacks:
                    print(f"  {t.name} inflicts {dmg} damage, {character.take_damage(dmg)}")
                    if character.dead:
                        # TODO: redirect attacks
                        break

        def distribute(melees, characters=(), mooks=()):
            """Check for dead characters and redistribute their targets to other characters."""
            for character in characters:
                melees[character] = list()
            redistribute = list(mooks)
            for character in list(melees.keys()):
                if character.dead:
                    redistribute.extend(melees[character])
                    del melees[character]
            if not melees:
                return
            characters = list(melees.keys())
            for mook in redistribute:
                melees[random.choice(characters)].append(mook)

        melees = defaultdict(list)
        distribute(melees, self.combatants, mooks)
        for character in self.combatants:
            character.start_combat()
        complete = False
        turn = 0
        while not complete:
            if all(c.dead for c in melees):
                print('All characters are dead. Combat over.')
                complete = True
                break
            if all(m.taken_out for m in mooks):
                print('All oppenents are takenout. Combat over.')
                complete = True
                break
            turn += 1
            party, mon = d6(), d6()
            print(f"\nRound {round}: Initiative party:{party} Monsters:{mon}")
            distribute(melees)
            for character, targets in melees.items():
                if character.dead:
                    print(f"  {character.name} died")
                else:
                    print(f"  {character.name} vs {', '.join(str(t) for t in targets if not t.taken_out)}")
            if party > mon:
                party_attacks(melees)
                mook_attacks(melees)
            elif mon > party:
                mook_attacks(melees)
                party_attacks(melees)
            else:
                mook_attacks(melees)
                party_attacks(melees)



sword = Item('Sword', dmg=d6, attack=d20)
battle_axe = Item('Battle Axe', dmg=d8, attack=d24)
arm_lgt = Item('Light Armor', arm=2)
arm_med = Item('Medium Armor', arm=3)
arm_hvy = Item('Heavy Armor', arm=4)
sh_med= Item('Medium Shield', block=d6, cover=5)
sh_lrg = Item('Large Shield', block=d8, cover=3)

def equip(character, *args):
    for item in args:
        item.equip(character)
    return character


if __name__ == '__main__':
    tzin = Character('Tzin', d6, hd=2, combat=2)
    lauf = Character('Luaf', d6, hd=1, combat=1)
    equip(tzin, sword, arm_med, sh_med)
    equip(lauf, battle_axe, arm_hvy)

    gang = Party(tzin, lauf)
    print(gang)
    # gang.combat(Orc(), Orc(), Orc(), Orc(), Ogre())
    gang.combat(Noble(), Noble())
    print()
    print(gang)
