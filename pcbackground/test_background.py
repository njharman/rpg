import unittest

import background
from background import Character, Relative, Unknown
from die import DieFactory, do_roll

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


class SequentialDieFactory(DieFactory):
    def __init__(self, size):
        def inner(size=size):
            while (True):
                yield from range(1, size + 1)
        foo = inner()

        def d():
            return next(foo)
        self.die = d


class ListDieFactory(DieFactory):
    def __init__(self, die_list):
        def inner(die_list=die_list):
            while (True):
                yield from die_list
        foo = inner()

        def d():
            return next(foo)
        self.die = d


background.d4 = SequentialDieFactory(4)
background.d20 = SequentialDieFactory(20)
background.d100 = SequentialDieFactory(100)


class Test_stuff(unittest.TestCase):
    def test_do_roll(self):
        answer = do_roll('2d6')
        answer = do_roll('40+2d6')
        answer = do_roll('40+2d1')
        assert answer == 42

    def test_DieFactory(self):
        d20 = DieFactory(20)
        10 + d20
        d20 + 10
        f"{d20}"
        '%i' % d20 # noqa: UP031
        assert d20 < 21


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
