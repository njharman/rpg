import unittest

import background
import die
from background import Character, Relative, Unknown

__copyright__ = 'Copyright (c) 2007 Norman J. Harman Jr. njharman@gmail.com'
__license__ = """Licensed under the FSF GPL

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""
__doc__ = f"""
{__copyright__}
{__license__}
"""


class CyclingRng:
    """Deterministic rng: choice() walks a fixed value sequence, cycling, returning the
    matching face. Injected into a die so it rolls scripted values.
    """

    def __init__(self, values):
        self.values = list(values)
        self.i = 0

    def choice(self, seq):
        value = self.values[self.i % len(self.values)]
        self.i += 1
        for face in seq:
            if face[1] == value:
                return face
        raise ValueError(f'{value} not in {seq}')


def SequentialDieFactory(size):
    """Die rolling 1,2,...,size, repeating."""
    return die.Standard(size, rng=CyclingRng(range(1, size + 1)))


def ListDieFactory(values):
    """Die rolling the given values in order, repeating; d100 faces cover every value used."""
    return die.Standard(100, rng=CyclingRng(values))


background.d4 = SequentialDieFactory(4)
background.d20 = SequentialDieFactory(20)
background.d100 = SequentialDieFactory(100)


class Test_Unknown(unittest.TestCase):
    def test_creation(self):
        t = Unknown('Father')
        assert str(t) == 'Father Unknown'
        assert not t, 'Unknown should be False'


class Test_Relative(unittest.TestCase):
    def test_creation(self):
        t = Relative('Father')
        assert str(t) == 'Father'
        assert t, 'Relative should not be False'


class Test_Character(unittest.TestCase):
    def test_social_property(self):
        t = Character()
        t.social = 'LLC'
        assert t._honor == [('Social class', -10)]

    def test_gender_property(self):
        t = Character()
        t.gender = 'Female'

    def test_race_property(self):
        t = Character()
        t.race = 'Dwarf'

    def test_set_attributes(self):
        t = Character()
        t.set_attributes([17, 15, 13, 11, 10, 8])
        assert t.strength == 17
        assert t.dexterity == 15
        assert t.constitution == 13
        assert t.intelligence == 11
        assert t.wisdom == 10
        assert t.charisma == 8

    def test_birthdate(self):
        t = Character()
        t.roll_birthdate()

    def test_birth(self):
        t = Character()
        background.d100 = ListDieFactory([1, 80, 81])
        t.roll_birth()
        assert not t.illegitimate
        assert t.father
        assert t.mother
        assert not t.father.deceased
        assert t.mother.deceased
        # go through other paths
        background.d20 = ListDieFactory([1, 2, 15])
        for seq in [[10, 99, 99], [10, 99, 80], [95, 5], [95, 30], [95, 60],
                    [95, 90, 25], [95, 90, 99], [95, 99, 75], [95, 99, 99] ]:
            background.d100 = ListDieFactory(seq)
            t = Character()
            t.roll_birth()

    def test_heritage(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_heritage()

    def test_siblings(self):
        t = Character()
        t.charisma = 10
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_siblings()

    def test_order_of_birth(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_order_of_birth()

    def test_social(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_social()

    def test_title(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_title()

    def test_office(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_office()

    def test_entitlements(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_entitlements()

    def test_money(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_social()
            t.roll_money()

    def test_debt(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_debt()

    def test_deed(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for _i in range(101):
            t.roll_deed()
