# 17 15 13 10 10 8     15 15 13 13 10 8
# +3 +2 +1            -1     +2 +2 +1 +1     -1
import random

from die import *
from chargen_data import *


def do_table(table, roll=None):
    """Return item from table based on roll"""
    if roll is None:
        roll = d100
    for target, item in table:
        if roll <= target:
            return item


class Relative(object):
    """
    Parents, siblings, etc
    """

    def __init__(self, relation):
        self.relation = relation
        self.deceased = False

    def __str__(self):
        return self.relation


class Unknown(object):
    """
    Missing parent
    """

    def __init__(self, relation):
        self.relation = relation

    def __nonzero__(self):
        """always claim to not be here"""
        return False

    def __str__(self):
        return self.relation + " Unknown"


class Character(object):
    """
    Assign Abilities
    Pick Gender
    Pick Race
    Roll Birth & Parents
    Roll Heritage
    Roll Social
    Pick Class
    """

    def __init__(self):
        self._gender = "Male"
        self._money_modifier = 0   # number modifier
        self._race_dict = {}  # race info dict
        self._profession_dict = {}  # class info dict
        self._honor = []    # list of honor adjustments ("reason", adj)
        self._info = []     # list of informations about character
        self.siblings = []
        self.buildpoints = 5

    def __getattr__(Self, name):
        return ""

    def _prop_set_gender(self, gender):
        self._gender = gender
        self.calc_physical()
    gender = property(lambda s: s._gender, _prop_set_gender)

    def _prop_set_race(self, race):
        self._race = race
        self._race_dict = races[race]
        self.calc_physical()
    race = property(lambda s: s._race, _prop_set_race)

    def _prop_set_social(self, value):
        self._social = value
        self._add_honor(value)
    social = property(lambda s: s._social, _prop_set_social)

    def _race_value(self, key, default=0):
        """Silly helper to pull value from race dictionary"""
        return self._race_dict.get(key, default)

    def _add_honor(self, cause):
        """Add tuple(reason adjustment) to honor list"""
        honor = add_honors.get(cause, (None, 0))
        if honor[0] != None:
            self._honor.append(honor)

    def _add_info(self, info):
        """Add string to info list"""
        self._info.append(info)

    def calc_physical(self):
        gender = self.gender.lower()[0]
        self.height = do_roll(self._race_value('%sheight' % gender, "0d1"))
        self.weight = do_roll(self._race_value('%sweight' % gender, "0d1"))
        self.age = do_roll(self._race_value('age', "0d1"))

    def set_attributes(self, stats):
        self.strength = stats[0]
        self.dexterity = stats[1]
        self.constitution = stats[2]
        self.intelligence = stats[3]
        self.wisdom = stats[4]
        self.charisma = stats[5]

    def roll_birthdate(self):
        return "todo"

    def roll_birth(self):
        """set stuff based on birth 4g+4h"""
        self.birthdate = self.roll_birthdate()
        self.father = Relative("Father")
        self.mother = Relative("Mother")

        roll = d100 + self._race_value("4g")
        if roll > 90:
            illegitimate = d100 + self._race_value("4h")
            if illegitimate <= 5:
                self.illegitimate = "You were abandoned at birth."
                self.father = Unknown("Father")
                self.mother = Unknown("Mother")
                self._add_honor("abandoned")
                self.social = "LLC"
            elif illegitimate <= 30:
                self.illegitimate = "Birth was result of rape."
                self.father = Unknown("Father")
                self._add_honor("son of rapist")
            elif illegitimate <= 60:
                self.illegitimate = "Mother was a prostitue."
                self.father = Unknown("Father")
                self._add_honor("prostitute mother")
            elif illegitimate <= 90:
                self.illegitimate = "Birth was result of an adulterous affair."
                if d100 <= 25:
                    self.father = Unknown("Father")
                self._add_honor("illegitimate birth")
            else:
                self.illegitimate = "Birth was arranged through a surrogate mother."
                if d100 <= 75:
                    self.mother = Unknown("Mother")
                self._add_honor("surrogate mother")

        def _remarry(parent):
            attr = getattr(self, parent)
            roll = d20
            if roll == 1:
                attr.famous = True
            if roll >= 15:
                setattr(self, "birth%s" % parent, attr)
                setattr(self, parent, Relative("Step Father"))

        if self.father and d100 >= 81:
            self.father.deceased = True
        if self.mother and d100 >= 81:
            self.mother.deceased = True

        if (not self.mother or self.mother.deceased) and (not self.father or self.father.deceased):
            self.orphan = True
        elif self.mother and not self.father:
            _remarry("mother")
        elif self.father and not self.mother:
            _remarry("father")

    def roll_parental_quaity(self):
        """4I"""

    def roll_heritage(self):
        result = do_table(heritages)
        if result:
            self._add_honor(result)

    def roll_siblings(self):
        roll = d100
        if roll >= 96:
            illegitimate = -20
        else:
            illegitimate = 0
        for i in range(do_table(siblings, roll)):
            sibling = Relative(random.choice(["Sister", "Brother"]))
            # todo make them illegitimate
            self.siblings.append(sibling)
            if d100 > 80:
                sibling.deceased = True
            else:
                roll = d100 + self.charisma + illegitimate
                if roll <= 25:
                    sibling.something = "bitter rival"
                elif roll > - 85:
                    sibling.something = "devoted"
                else:
                    sibling.something = "meh"
                roll = d100
                # > 95 twins > 99 identical twins

    def roll_order_of_birth(self):
        count = len([s for s in self.siblings if not s.deceased])
        count = len(self.siblings)
        if count == 0:
            self._add_info("First born")
        elif count == 1:
            self._add_info(random.choice["First born", "Second born"])
        elif count == 2:
            self._add_info(random.choice["First born", "Middle born", "Last born"])
        elif count == 3:
            self._add_info(random.choice["First born", "Second born", "Second to last born", "Last born"])
        else:
            self._add_info(random.choice["First born", "Second born", "Middle born", "Middle born", "Second to last born", "Last born"])
        if "Middle born" in self._info:
            pass
            # roll minor personality quirk
        if "First born" in self._info:
            self._money_modifier += 5
        if "Second born" in self._info:
            self._money_modifier += 2
        if "Second to last born" in self._info:
            self._money_modifier -= 2
        if "Last born" in self._info:
            self._money_modifier -= 5

    def roll_social(self):
        """4f"""
        def _set_parents_social(social):
            if self.mother:
                self.mother.social = social
            if self.father:
                self.father.social = social

        def _shift_social(social, amount):
            ranks = [x[1] for x in socialclasses]
            index = ranks.index(social)
            index += amount
            index = max(index, 0)
            index = min(index, len(ranks))
            return ranks[index]

        social = do_table(socialclasses)
        if social == "SLC":
            roll = d20
            if roll <= 5:
                self._add_info("Runaway slave.")
            elif roll <= 15:
                self._add_info("Criminal, charged with %s" % do_table(crimes))
            else:
                self._add_info("Stripped of former status and banished.")
            self.social = social
            _set_parents_social(do_table(socialclasses))
            return

        _set_parents_social(social)
        if self.orphan:
            if self.father:
                social = _shift_social(social, -2)
            else:
                social = "LLC"
        elif self.illegitimate:
            if self.father and d100 <= 85:
                social = _shift_social(social, -1)
        self.social = social

        if social == "MUC":
            self.roll_office()
            self.roll_entitlements()
        if social == "UUC":
            self.roll_title()
            self.roll_entitlements()

    def roll_title(self):
        """UUC have chance of special office held"""
        result = do_table(titles)
        if result:
            self._add_info(result)

    def roll_office(self):
        """MUC have chance of special office held"""
        result = do_table(offices)
        if result:
            self._add_info(result)

    def roll_entitlements(self):
        """DMG 3C, for UUC and MUC"""
        data = {'social': self.social, 'd4': d4}
        count = 1
        while count > 0:
            roll = d100
            if self.social == "UUC":
                roll += 20
            if roll > 100:
                count += 1
                continue
            result = do_table(entitlements, roll)
            if result:
                result = result % data
                if result not in self._info:
                    self._add_info(result)
            count -= 1

    def roll_money(self):
        """must do class first"""
        mod = dict(SLC=-30, LLC=-20, MLC=-15, ULC=-10, LMC=-5, MMC=0, UMC=+5, LUC=+10, MUC=+15, UUC=+20)
        roll = d100 + self._money_modifier + mod[self.social]
        if self.orphan:
            roll -= 20
        if len(self.siblings) == 0:
            roll += 10
        # fg +10 mu -10 th +5
        # bp = +2d12
        if roll <= 5:
            self.roll_debt()
        if roll > 101:
            self.roll_weapon()
        if roll > 106:
            self.roll_armor()
        if roll > 111:
            self.roll_mount()
        if roll > 116:
            self.roll_deed()
        self.money = do_roll(do_table(starting_money))
        if self.orphan:
            self.money /= 2

    def roll_debt(self):
        pass

    def roll_deed(self):
        count = 1
        while count > 0:
            roll = d100
            if self.social == "UUC":
                roll += 20
            if roll <= 100:
                break
            count += 1
        result = do_table(inheirited_deeds, roll)
        data = dict(country="country")
        if "biz" in result:
            data['biz'] = self.roll_business(result)
        self._add_info("Inherited deed to %s." % (result % data))

    def roll_business(self, result):
        if "city" in result:
            biz = city_biz
        elif "town" in result:
            biz = town_biz
        elif "village" in result:
            biz = village_biz
        else:
            biz = hamlet_biz
        return random.choice(biz)

    def roll_weapon(self):
        mod = dict(SLC=-1000, LLC=-500, MLC=-200, ULC=-100, LMC=-50, MMC=0, UMC=+50, LUC=+100, MUC=+200, UUC=+500)
        self._add_info("Inherited weapon, %s." % do_table(inheirited_weapons, random.randint(1, 10000)))

    def roll_armor(self):
        mod = dict(SLC=-500, LLC=-200, MLC=-100, ULC=-50, LMC=-25, MMC=0, UMC=+25, LUC=+50, MUC=+100, UUC=+200)
        self._add_info("Inherited armor, %s." % do_table(inheirited_armors, random.randint(1, 4000)))

    def roll_mount(self):
        mod = dict(SLC=-500, LLC=-200, MLC=-100, ULC=-50, LMC=-25, MMC=0, UMC=+25, LUC=+50, MUC=+100, UUC=+200)
        self._add_info("Inherited mount, %s." % do_table(inheirited_mounts, random.randint(1, 6000)))
