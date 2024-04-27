import background
from die import do_roll, DieFactory
from background import Unknown, Relative, Character
import unittest
__copyright__ = "Copyright (c) 2007 Norman J. Harman Jr. njharman@gmail.com"
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
__doc__ = """
%(copyright)s
%(license)s
""" % {'copyright': __copyright__, 'license': __license__}


class SequentialDieFactory(DieFactory):
    def __init__(self, size):
        def inner(size=size):
            while (True):
                for i in range(1, size + 1):
                    # print i
                    yield i
        foo = inner()

        def d():
            return foo.next()
        self.die = d


class ListDieFactory(DieFactory):
    def __init__(self, list):
        def inner(list=list):
            while (True):
                for i in list:
                    # print i
                    yield i
        foo = inner()

        def d():
            return foo.next()
        self.die = d


background.d4 = SequentialDieFactory(4)
background.d20 = SequentialDieFactory(20)
background.d100 = SequentialDieFactory(100)


class Test_stuff(unittest.TestCase):
    def test_do_roll(self):
        answer = do_roll("2d6")
        answer = do_roll("40+2d6")
        answer = do_roll("40+2d1")
        self.assertEqual(42, answer)

    def test_DieFactory(self):
        d20 = DieFactory(20)
        10 + d20
        d20 + 10
        "%s" % d20
        "%i" % d20
        self.failUnless(d20 < 21)


class Test_Unknown(unittest.TestCase):
    def test_creation(self):
        t = Unknown("Father")
        self.assertEqual("Father Unknown", str(t))
        self.failIf(t, "Unknown should be False")


class Test_Relative(unittest.TestCase):
    def test_creation(self):
        t = Relative("Father")
        self.assertEqual("Father", str(t))
        self.failUnless(t, "Relative should not be False")


class Test_Character(unittest.TestCase):
    def test_social_property(self):
        t = Character()
        t.social = "LLC"
        self.assertEqual([('Social class', -10)], t._honor)

    def test_gender_property(self):
        t = Character()
        t.gender = "Female"

    def test_race_property(self):
        t = Character()
        t.race = "Dwarf"

    def test_set_attributes(self):
        t = Character()
        t.set_attributes([17, 15, 13, 11, 10, 8])
        self.assertEqual(17, t.strength)
        self.assertEqual(15, t.dexterity)
        self.assertEqual(13, t.constitution)
        self.assertEqual(11, t.intelligence)
        self.assertEqual(10, t.wisdom)
        self.assertEqual(8, t.charisma)

    def test_birthdate(self):
        t = Character()
        t.roll_birthdate()

    def test_birth(self):
        t = Character()
        background.d100 = ListDieFactory([1, 80, 81])
        t.roll_birth()
        self.failIf(t.illegitimate)
        self.failUnless(t.father and t.mother)
        self.assertEqual(False, t.father.deceased)
        self.assertEqual(True, t.mother.deceased)
        # go through other paths
        background.d20 = ListDieFactory([1, 2, 15])
        for seq in [[10, 99, 99], [10, 99, 80], [95, 5], [95, 30], [95, 60],
                    [95, 90, 25], [95, 90, 99], [95, 99, 75], [95, 99, 99], ]:
            background.d100 = ListDieFactory(seq)
            t = Character()
            t.roll_birth()

    def test_heritage(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_heritage()

    def test_siblings(self):
        t = Character()
        t.charisma = 10
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_siblings()

    def test_order_of_birth(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_order_of_birth()

    def test_social(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_social()

    def test_title(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_title()

    def test_office(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_office()

    def test_entitlements(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_entitlements()

    def test_money(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_social()
            t.roll_money()

    def test_debt(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_debt()

    def test_deed(self):
        t = Character()
        background.d100 = SequentialDieFactory(100)
        for i in range(101):
            t.roll_deed()
