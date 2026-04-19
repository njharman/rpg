#!/usr/bin/env python3
"""Roll HackMaster 5e ability scores.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Feb 2025.
Website: http://trollandflame.blogspot.com/
"""

import random
from dice import d6, d100


class Ability:
    def __init__(self, name):
        self.name = name
        self.short = 'LKS' if name == 'Looks' else name[:3].upper()
        self.score = d6() + d6() + d6()
        self.fractional = d100()

    def __str__(self):
        return f'{self.short}: {self.score:2}/{self.fractional:02}'


for name in ('Strength', 'Intelligence', 'Wisdom', 'Dexterity', 'Constitution', 'Looks', 'Charisma'):
    print(Ability(name))
print()
