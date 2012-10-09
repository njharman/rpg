#!/usr/bin/python
'''Generate K'jorian Deathguards.

Version: 5/06/2009
Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain 2009.
Website: http://trollandflame.blogspot.com/
'''
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
        return ' '.join(f for f in (str(s) for s in self.get_result()) if f)

    def get_result(self):
        roll = self.dice()
        for row in self.table:
            if row[0] >= roll:
                return row[1:]
        return self.table[-1][1:]


class AutoTable(Table):
    '''Table that figures out it's own dice and uses slots instead of actual die rolls in table'''

    def __init__(self, *table):
        new_table = list()
        total = 0
        for line in table:
            total += line[0]
            new_line = [total]
            new_line[1:] = line[1:]
            new_table.append(new_line)
        super(AutoTable, self).__init__(lambda: random.randint(1, total), *new_table)


class fwd_ref(object):
    '''Allows forward referencing of Table objects'''

    def __init__(self, table):
        self.table = table

    def __str__(self):
        return str(globals().get(self.table))


class Maybe(object):
    '''Returns emptystring instea of table entry 1/3 time'''

    def __init__(self, table):
        self.table = table

    def __str__(self):
        if random.randint(0, 2):
            return ''
        else:
            return str(self.table)


# the 2nd parm is base DC
ArmorEffect = AutoTable(
    (1, 13, '''Corona of Hate (10/heal, 10'r Attack random + Rage(+4 str/con, -2 AC) / DC%(dc)i Will negate'''),
    (1, 13, '''Corona of Cold (10/fire, 10'r 1d12 + shivers(-2 dex/str, 1/2 move) / DC%(dc)i Fort negate'''),
    (1, 13, '''Corona of Black (10/elec, 10'r 1d12 + shocked(-2 dex/str, 1/2 move) / DC%(dc)i Fort negate'''),
    (1, 13, '''Corona of Purple (10/-, 10'r 1d12 taint + Nauseated / DC%(dc)i Fort Sickened'''),
    (1, 17, '''Repulsion 10' (can't approach) / DC%(dc)i Will negate'''),
    (2,  0, '''Spell Reflect 1d4+6 lvls'''),
    (2,  0, '''Mantle of K'jore SR 12+%(level)s'''),
    (2,  0, '''Cloak of Shadow (+4 AC, +2 saves vs Ian/light effects)'''),
    (1,  0, '''Cloak of K'jore (+4 AC, +4 save, SR 25 vs Ian, Ian confused 1rnd if he hits)'''),
    )

WeaponEffect = AutoTable(
    (2, '''+1d6 Black (elec)'''),
    (4, '''+1d6 Vibraion (sonic)'''),
    (2, '''+1d6 Purple melt (acid/taint diseased / DC10+dam Fort negate)'''),
    (2, '''+2d4 Purple flame (taint diseased / DC10+dam Fort negate)'''),
    (2, '''+1 wound(vampire)'''),
    (1, '''shatter(DC10+1/2HD)'''),
    )

GrappleEffect = AutoTable(
    (2, '''clinging'''),
    (1, '''+1 wound (vampire)'''),
    (1, '''bonds on crit'''),
    (4, Maybe(WeaponEffect)),
    )

MeleeWeapon = AutoTable(
    (2, '''%(melee_tohit)+3i Tenticle 1d8%(melee_damage)+i', GrappleEffect, '[auto grapple]'''),
    (2, '''%(melee_tohit)+3i Pincer 2d8%(melee_damage)+i', GrappleEffect, '[auto grapple]'''),
    (4, '''%(melee_tohit)+3i Razor Chain 3d4%(melee_damage)+i', GrappleEffect, '[+2 disarm, trip, opt reach]'''),
    (4, '''%(melee_tohit)+3i Three-piece-mace 1d8%(melee_damage)+i', GrappleEffect, '[trip, opt reach]'''),
    (2, '''%(melee_tohit)+3i (18-20) Wavy two-hander 2d4%(melee_damage)+i''', WeaponEffect),
    (4, '''%(melee_tohit)+3i (18-20) Pick 1d6%(melee_damage)+i', Maybe(WeaponEffect), 'or (20) Flail 1d8%(melee_damage)+i', GrappleEffect, '[+2 disarm, trip]'''),
    (2, '''%(melee_tohit)+3i (19-20) Bardiche 1d12%(melee_damage)+i', Maybe(WeaponEffect), 'or (18-20) Scythe 2d4%(melee_damage)+i', Maybe(WeaponEffect), '[trip]'''),
    (4, '''%(melee_tohit)+3i (19-20) Chain Axe 1d8%(melee_damage)+i', GrappleEffect, '[30' range entangle DC25 burst, DC20 escape, DC15 concentrate]'''),
    (4, '''%(melee_tohit)+3i (19-20) Demon Axe 1d12%(melee_damage)+i', WeaponEffect, '[opt reach]'''),
    (4, '''%(melee_tohit)+3i (19-20) Polearm 1d10%(melee_damage)+i', WeaponEffect, '[reach]'''),
    (4, '''%(range_tohit)+3i (x4) Bone shooter 1d4 or %(melee_tohit)+3i (19-20) Bone slicer 2d4%(melee_damage)+i '''),
    (1, '''%(melee_tohit)+3i (17-20) Purple Lightsword 3d4 taint 1d4%(melee_damage)+i wound on crit'''),
    )

# really twisting table here.
# the 2nd parm is base DC
Power = AutoTable(
    (4, 11, '''Doom(shaken) DC%(dc)i Will'''),
    (4, 13, '''Contagion Taint disease d4 taint + same damage to random stat/day DC%(dc)i Fort'''),
    (2, 17, '''Repulsion 10'(can't approach) DC%(dc)i Will'''),
    (2, 17, '''Dictum DC%(dc)i Will see chart'''),
    (1, 17, '''Anti-magic ray DC%(dc)i Will'''),
    (1, 17, '''Anti-magic 5' sphere DC%(dc)i Will'''),
    (1, 19, '''Storm of Vengence'''),
    (1, 17, '''Prismatic Spray DC%(dc)i varies'''),
    (3, 13, '''Slow DC%(dc)i Will'''),
    (3,  0, '''True Strike +20'''),
    (3,  0, '''Summon K'jore beasts'''),
    (3,  0, '''4d6 vitality drain when grappled'''),
    (3,  0, '''Dimension Door'''),
    (2,  0, '''Blacklight spell'''),
    (2,  0, '''Wall of K'Jore(Chaos)'''),
    (2,  0, '''Stop Teleport/etc'''),
    (2,  0, '''Animate world to attack foes +%(level)i tohit 2d6 damage'''),
    (2,  0, '''Regeneration 5/rnd'''),
    (1,  0, '''Balefull Regeneration 2/per creature w/in 30'''),
    (1,  0, '''Familiar beholder 4 stalks'''),
    (1,  0, '''Reverse Gravity'''),
    (1,  0, '''Alter structure of world (move/create walls, + gravity + slow + animate etc.)'''),
    )

Feats = AutoTable(
    (1, '''Whirlwind, attack all in reach'''),
    (1, '''Sprink Attack'''),
    (1, '''Deflect Arrows'''),
    (1, '''Deflect Arrows+magical'''),
    (2, '''+2 Save'''),
    (4, '''+3 wound points'''),
    )


def mod(stat):
    '''Stat mod'''
    return (stat / 2) - 5


class FighterType(object):
    def __init__(self, level=1, spell_warped=False):
        self.hitdie = 10
        self.spell_warped = spell_warped
        self.set_level(level)
        if self.spell_warped:
            self.type = '''Level %i K'jore Deathguard Spellwarped Fighter (medium abberation)'''
            self.special_defenses.insert(0, 'SR %i' % (11 + self.level))
        else:
            self.type = '''Level %i K'jore Deathguard Fighter (medium abberation)'''

    def pretty_print(self):
        indent_level = 1

        def indent(text, indent_level=1):
            lines = list()
            for line in text.split('\n'):
                lines.append('%s%s' % ('  ' * indent_level, line))
            return '\n'.join(lines)

        def stuff(text):
            return indent(text, indent_level + 1)

        print self.type % (self.level), self.cr
        print indent('Hits: %s' % ' / '.join(map(str, self.hitpoints)))
        print indent('Move: %s' % (', '.join(self.moves)))
        print indent('\n'.join(self.stats))
        print indent(', '.join(self.saves))
        print indent('AC: ' + ', '.join(self.armorclasses))
        print indent('SD: ' + '; '.join(self.special_defenses))
        print indent('Attacks: %s, %s' % (self.bab, self.grapple))
        print stuff('\n'.join(self.attacks))
        print indent('Powers:')
        print stuff('\n'.join(self.powers))
        print indent('Feats:')
        print stuff('\n'.join(self.feats))
        print indent('Equipment:')
        print stuff('\n'.join(self.items))

    def _get_DC_result(self, table):
        (save, thing) = table.get_result()
        args = dict(dc=save + mod(self.cha), level=self.level)
        return str(thing) % args

    def set_level(self, level):
        self.level = level
        self.base_move = 30
        self.armor_ac = 8    # plate
        self.force_ac = 0    # amount of natural+armor ac that is effective vs touch
        self.natural_ac = 0
        self._set_base_stats()
        self._set_base_powers()
        self._set_base_magic()
        self._set_base_feats()
        self.special_defenses = list()
        self.special_defenses.append('immune fear, disease, polymorph')

    def _set_base_stats(self):
        self.str = 16
        self.dex = 10
        self.con = 16
        self.int = 8
        self.wis = 10
        self.cha = 14
        if self.spell_warped:
            self.str += 4
            self.dex += 2
            self.con += 4
            self.cha += 2
        if level >= 4:
            self.con += 1
        if level >= 8:
            self.con += 1
            self.natural_ac += 1
        if level >= 12:
            self.cha += 1
            self.natural_ac += 1
        if level >= 16:
            self.cha += 1
            self.natural_ac += 1
        if level >= 20:
            self.str += 1
            self.natural_ac += 1

    def _set_base_powers(self):
        cha_mod = mod(self.cha)
        half_hd = self.level / 2
        self.powers = list()
        self.powers.insert(0, '''10' Darkness Despair(-1 actions) DC%i Will''' % (10 + half_hd + cha_mod))
        if self.spell_warped:
            self.powers.insert(0, '''Absorb Spell (+4 Str/Dex/Con, 10/energy, lvl*5 vitality, lvl*5' speed''')
        for i in range(self.level / 5):
            self.powers.append(self._get_DC_result(Power))

    def _set_base_magic(self):
        def bonii(bonus, item, extra=''):
            things = []
            if bonus:
                things.append('%+i' % (bonus,))
            things.append(item)
            if extra:
                things.append('[%s]' % extra)
            return ' '.join(things)
        self.items = list()
        self.ring_bonus = 0  # ac and saves
        self.armor_bonus = 0
        self.weapon_bonus = 0
        if level >= 4:
            armor = 'Black Plate'
        if level >= 8:
            self.armor_bonus += 1
            self.weapon_bonus += 1
        if level >= 10:
            armor = 'Demon Plate'
            self.armor_bonus += 1
        if level >= 11:
            self.ring_bonus += 1
        if level >= 12:
            self.armor_bonus += 1
            self.weapon_bonus += 1
        if level >= 14:
            self.armor_bonus += 1
        if level >= 15:
            self.ring_bonus += 1
        if level >= 16:
            armor = 'Elder Demon Plate'
            self.armor_bonus += 1
            self.weapon_bonus += 1
        if level >= 18:
            self.armor_bonus += 1
        if level >= 19:
            self.ring_bonus += 1
        if level >= 20:
            self.weapon_bonus += 1
        self.items.append(bonii(self.armor_bonus, armor, self._get_DC_result(ArmorEffect)))
        if self.weapon_bonus > 0:
            self.items.append(bonii(self.weapon_bonus, 'weapon'))
        if self.ring_bonus > 0:
            self.items.append(bonii(self.ring_bonus, 'ring of protection'))

    def _set_base_feats(self):
        self.feats = list()
        if level >= 4:
            self.feat_tohit = 1
            self.feat_damage = 2
        if level >= 8:
            self.feat_tohit += 1
        if level >= 10:
            self.feats.append(str(Feats))
        if level >= 12:
            self.feat_damage += 2
        if level >= 14:
            self.feats.append(str(Feats))
        if level >= 16:
            pass
        if level >= 18:
            self.feats.append(str(Feats))
        self.feats.insert(0, 'Specialization Series %+i/%+i' % (self.feat_tohit, self.feat_damage))
        self.feats

    @property
    def moves(self):
        moves = list()
        moves.append('%s\'' % self.base_move)
        return moves

    @property
    def hitpoints(self):
        vitality = sum(random.randint(1, 10) for i in range(level)) + (self.level * mod(self.con))
        wounds = self.con
        return (vitality, wounds)

    @property
    def stats(self):
        stats = list()
        for stat in ('str', 'dex', 'con', 'int', 'wis', 'cha'):
            value = getattr(self, stat)
            stats.append('%s %2i (%+i)' % (stat.title(), value, mod(value)))
        return stats

    @property
    def saves(self):
        poor = self.level / 3
        good = (self.level + 4) / 2
        fort = poor + mod(self.con) + mod(self.cha) + self.ring_bonus
        ref = poor + mod(self.dex) + mod(self.cha) + self.ring_bonus
        will = good + mod(self.wis) + mod(self.cha) + self.ring_bonus
        return ['Fort %+2i' % fort, 'Ref %+2i' % ref, 'Will %+2i' % will]

    @property
    def attacks(self):
        weapon = str(MeleeWeapon)
        range_bonus = self.weapon_bonus + mod(self.dex) + self.feat_tohit
        melee_bonus = self.weapon_bonus + mod(self.str) + self.feat_tohit
        melee_damage = self.weapon_bonus + mod(self.str) + self.feat_damage
        attacks = list()
        for tohit in range(self._bab_value, 0, -5):
            args = dict(melee_tohit=tohit + melee_bonus, melee_damage=melee_damage, range_tohit=tohit + range_bonus)
            attacks.append(weapon % args)
        return attacks

    @property
    def bab(self):
        return 'Bab %+i' % self._bab_value

    @property
    def grapple(self):
        return 'Grap %+i' % (self._bab_value + mod(self.str))

    @property
    def armorclasses(self):
        physical = self.natural_ac + self.armor_ac + self.armor_bonus
        ac = 10 + self.ring_bonus + mod(self.dex) + physical
        touch = 10 + self.ring_bonus + mod(self.dex) + self.force_ac
        flat = 10 + self.ring_bonus + physical
        return ['%+2i' % ac, 'Touch %+2i' % touch, 'Flat %+2i' % flat]

    @property
    def cr(self):
        cr = self.level + 1
        if self.spell_warped:
            cr += 1
            if self.level >= 11:
                cr += 1
        if self.level >= 12:
            cr += 1
        return 'CR%i' % cr

    @property
    def _bab_value(self):
        return self.level

if __name__ == '__main__':
    for level in range(7, 15):
        FighterType(level).pretty_print()
        print
