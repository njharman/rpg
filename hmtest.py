#!/usr/bin/python
from collections import defaultdict
'''Hack Master Basic combat tests.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain 2012.
Website: http://trollandflame.blogspot.com/
'''

from dice import *


def test_dieroll(die_func, count=100000):
    bucket = defaultdict(int)
    for i in range(count + 1):
        bucket[die_func()] += 1
    return bucket, count


def calc_dieroll_results(bucket, count):
    count = float(count)
    rolls = bucket.keys()
    rolls.sort()
    total = 0
    ptotal = 100
    results = list()
    for i in range(1, max(rolls) + 1):
        if bucket[i]:
            percent = (bucket[i] / count) * 100
            results.append('%-3i %5i %5.2f%% %6.2f%%' % (i, bucket[i], percent, ptotal))
            ptotal -= percent
            total += i * bucket[i]
        else:
            results.append('%-3i         not rolled' % (i, ))
    return results, (total / count), rolls[-1]


def dieroll_average_n_max(roll, count=100000):
    rolls, avg, max = calc_dieroll_results(*test_dieroll(roll, count))
    print roll.__name__, '%.2f' % avg, max


def dieroll_detail(roll, count=100000):
    rolls, avg, max = calc_dieroll_results(*test_dieroll(roll, count))
    print roll.__name__
    for roll in rolls:
        print roll
    print


def roll_damage(bonus, *damage):
    rolls = [d() for d in damage]
    half = bonus + sum(rolls[:(len(rolls) / 2)])
    full = bonus + sum(rolls)
    if full <= 0:
        full = 1
    if half <= 0:
        half = 1
    return full, half


def shield_use(def_bonus, atk_bonus, dr, *damage):
    output = list()
    atk_roll = d20p() + atk_bonus
    def_roll = d20p() + def_bonus
    full, half = roll_damage(0, *damage)
    if atk_roll > def_roll:
        if atk_roll == 20:
            full += roll_damage(0, *damage)[0]
        no = sm = lg = max(0, full - dr)
        output.append('Damage: %i' % full)
    else:
        # no shield is d20p-4 defense
        if atk_roll > (def_roll - 4):
            if atk_roll == 20:
                no = max(0, (full + roll_damage(0, *damage)[0]) - dr)
            else:
                no = max(0, full - dr)
        else:
            no = 0
        sm = max(0, half - (4 + dr))
        lg = max(0, half - (6 + dr))
        output.append('Damage: %i' % half)
    output.append('No Shield: %i' % no)
    output.append('Sm Shield: %i' % sm)
    output.append('Lg Shield: %i' % lg)
    return no, sm, lg, '\n'.join(output)


def test_sheild_use(def_bonus, atk_bonus, dr, *damage):
    top = 10
    rolls = 1000
    no_tot = 0.0
    sm_tot = 0.0
    lg_tot = 0.0
    no_tot_top = 0.0
    sm_tot_top = 0.0
    lg_tot_top = 0.0
    for i in range(rolls):
        no, sm, lg, output = shield_use(def_bonus, atk_bonus, dr, *damage)
        no_tot += no
        sm_tot += sm
        lg_tot += lg
        if no > top:
            no_tot_top += 1
        if sm > top:
            sm_tot_top += 1
        if lg > top:
            lg_tot_top += 1
    print 'Atk+: %i  Def+: %i' % (atk_bonus, def_bonus)
    print 'DR: ', dr, 'Damage: (', ' '.join(d.__name__ for d in damage), ')'
    print 'No Shield: %4.2f  ToP[%i]: %0.2f%%' % ((no_tot / rolls), top, (no_tot_top / rolls))
    print 'Sm Shield: %4.2f  ToP[%i]: %0.2f%%' % ((sm_tot / rolls), top, (sm_tot_top / rolls))
    print 'Lg Shield: %4.2f  ToP[%i]: %0.2f%%' % ((lg_tot / rolls), top, (lg_tot_top / rolls))


class Protection(object):
    def __init__(self, name, defence, damage_reduction, speed=0):
        self._name = name
        self.defence = defence
        self.dr = damage_reduction
        self.speed = speed

    def __str__(self):
        return self._name

    def hit(self, damage):
        damage -= self.dr
        if damage > 0:
            return damage
        else:
            return 0


class Shield(Protection):
    def __init__(self, *args, **kwargs):
        self._threshold = kwargs.get('threshhold', list())
        if 'threshhold' in kwargs:
            del kwargs['threshhold']
        super(Shield, self).__init__(*args, **kwargs)
        self.shattered = False

    def __len__(self):
        return len(self._threshold)

    def shatter(self):
        if not self.shattered:
            self._name = "shattered %s" % self._name
            self.defense = -4
            self.dr = 0
        self.shattered = True

    def hit(self, damage):
        if self._threshold is None:
            return damage
        attacker = d20()
        defender = d20()
        if damage >= self._threshold[3]:
            self.shatter()
        elif damage >= self._threshold[2] and attacker > (defender - 6):
            self.shatter()
        elif damage >= self._threshold[1] and attacker > defender:
            self.shatter()
        elif damage >= self._threshold[0] and attacker > (defender + 6):
            self.shatter()
        return super(Shield, self).hit(damage)


class Armor(Protection):
    pass


class Weapon(object):
    def __init__(self, name, speed, *damage_dice):
        self.name = name
        self.speed = speed
        self.damage_dice = damage_dice

    def __str__(self):
        return self.name


class Combatant(object):
    def __init__(self, name, hitpoints, top_save, atk_bonus, dmg_bonus, def_bonus, spd_bonus, weapon, shield, armor):
        '''
        def_bonus does not include armor or shield
        '''
        self.name = name
        self._hitpoints = hitpoints
        self.top = int(hitpoints * 0.32)
        self.top_save = top_save
        self.atk_bonus = atk_bonus
        self.dmg_bonus = dmg_bonus
        self._def_bonus = def_bonus
        self._spd_bonus = spd_bonus
        self.weapon = weapon
        self._shield = shield
        self.armor = armor
        self.in_pain = 0
        self.reset()
        self.reset_stats()

    def __str__(self):
        return '%s(%i)' % (self.name, self.hitpoints)

    @property
    def def_bonus(self):
        return self._def_bonus + self.armor.defence + self.shield.defence

    @property
    def speed(self):
        return self._spd_bonus + self.armor.speed + self.weapon.speed

    @property
    def can_act(self):
        if self._count > self.count:
            return False
        elif self.down:
            self.down = False
            self._count = self.count + 1
            self.stat_dict['recovery'] += 1
            return False
        elif self.dead or self.down:
            return False
        else:
            return True

    @property
    def dead(self):
        return self.hitpoints <= 0

    @property
    def status(self):
        if self.dead:
            return 'Dead'
        elif self.down:
            return 'Writhing in pain for %i seconds' % (self._count - self.count)
        elif self.count == self._count:
            return 'Ready'
        else:
            return 'Waiting'

    @property
    def stats(self):
        self._calc_percent(self.stat_dict)
        return self._format_stats(self.stat_dict)

    @property
    def aggregate_stats(self):
        stats = self._calc_aggreagate(self._aggregate_stats)
        return 'hit/miss: %(hits)i/%(misses)i (%(percent)0.1f%%), %(crits)i/%(max_hit)ihp crits/max, %(afumble)i/%(dfumble)i a/d fumbles, %(pdefence)i/%(npdefence)i p/n defences, %(knockouts)i/%(recovery)i/%(longest_ko)i k/r/l' % stats

    @property
    def aggregate_averages(self):
        stats = self._calc_aggreagate_averages(self._aggregate_stats)
        return 'hit/miss: %(hits_avg)i/%(misses_avg)i (%(percent_avg)0.1f%%), %(crits_avg)i/%(max_hit_avg)ihp crits/max, %(afumble_avg)i/%(dfumble_avg)i a/d fumbles, %(pdefence_avg)i/%(npdefence_avg)i p/n defences, %(knockouts_avg)i/%(recovery_avg)i/%(longest_ko_avg)i k/r/l' % stats

    def _calc_aggreagate_averages(self, aggregates):
        stats = defaultdict(int)
        count = len(aggregates) + 0.0
        sums = self._calc_aggreagate(aggregates)
        for k, v in sums.items():
            stats[k + '_avg'] = v / count
        if stats['swings_avg']:
            stats['percent_avg'] = stats['hits_avg'] / (stats['swings_avg'] / 100.0)
        else:
            stats['percent_avg'] = 0.0
        stats.update(sums)
        return stats

    def _calc_aggreagate(self, aggregates):
        stats = defaultdict(int)
        for stat in aggregates:
            stats['hits'] += stat['hits']
            stats['misses'] += stat['misses']
            stats['swings'] += stat['swings']
            stats['crits'] += stat['crits']
            stats['afumble'] += stat['afumble']
            stats['dfumble'] += stat['dfumble']
            stats['pdefence'] += stat['pdefence']
            stats['npdefence'] += stat['npdefence']
            stats['recovery'] += stat['recovery']
            stats['knockouts'] += stat['knockouts']
            stats['topsaves'] += stat['topsaves']
            stats['max_hit'] = max(stats['max_hit'], stat['max_hit'])
            stats['longest_combat'] = max(stats['longest_combat'], stat['longest_combat'])
            stats['longest_ko'] = max(stats['longest_ko'], stat['longest_ko'])
        self._calc_percent(stats)
        return stats

    def _calc_percent(self, stats):
        if stats['swings']:
            stats['percent'] = stats['hits'] / (stats['swings'] / 100.0)
        else:
            stats['percent'] = 0.0

    def _format_stats(self, stats):
        return 'hit/miss: %(hits)i/%(misses)i (%(percent)0.1f%%), %(crits)i crits, max hit %(max_hit)i, %(afumble)i/%(dfumble)i a/d fumbles, %(pdefence)s/%(npdefence)s p/n defences' % stats

    def reset(self):
        self.hitpoints = self._hitpoints
        self.shield = self._shield()
        self.down = False
        self.count = 0
        self._count = 1
        if hasattr(self, 'stat_dict'):
            self._calc_percent(self.stat_dict)
            self._aggregate_stats.append(self.stat_dict)
        self.stat_dict = defaultdict(int)

    def reset_stats(self):
        self._aggregate_stats = list()

    def attack(self, defender, free=False):
        texts = list()
        if defender.down:
            def_roll = d8p()
            def_natural = 0
            if not free:
                self._count = self.count + (self.speed / 2)
        else:
            def_roll = d20p()
            def_natural = d20p.natural
            if not free:
                self._count = self.count + self.speed
        def_tot = def_roll + defender.def_bonus
        atk_roll = d20p()
        atk_natural = d20p.natural
        atk_tot = atk_roll + self.atk_bonus
        texts.append(str(self))
        if atk_natural == 20 and atk_tot > def_tot:
            self.stat_dict['crits'] += 1
            texts.append('critical')
            full, half = roll_damage(self.dmg_bonus, *(self.weapon.damage_dice * 2))
        else:
            full, half = roll_damage(self.dmg_bonus, *self.weapon.damage_dice)
        self.stat_dict['longest_combat'] = max(self.stat_dict['longest_combat'], self.count)
        self.stat_dict['swings'] += 1
        self.stat_dict['max_hit'] = max(self.stat_dict['max_hit'], full)
        if atk_tot > def_tot:
            self.stat_dict['hits'] += 1
            texts.append('hits')
            if defender.down:
                texts.append('downed')
            texts.append(str(defender))
            texts.append(defender.hit(full))
        else:
            self.stat_dict['misses'] += 1
            texts.append('misses')
            if defender.down:
                texts.append('downed')
            texts.append(str(defender))
            texts.append(defender.miss(half))
        texts = [t.strip() for t in texts if t]
        if  texts[-1].endswith(','):
            texts[-1] = texts[-1][:-1]
        if not texts[-1].endswith('!'):
            texts[-1] = '%s.' % texts[-1]
        results = [' '.join(texts), ]
        # fumbles and defences
        if atk_tot > def_tot:
            if def_natural == 1:
                # this makes next swing 1 second later than it should
                results.append('Defender fumble free attack next second.')
                self._count = self.count + 1
                defender.stat_dict['dfumble'] += 1
        elif def_tot > atk_tot and not (defender.down or defender.dead):
            if atk_natural == 1:
                results.append('Attacker fumble %s' % defender.attack(self, True))
                self.stat_dict['afumble'] += 1
            if def_natural == 19:
                damage = (d4p - 2) + (d4p - 2) + defender.dmg_bonus
                results.append('Near perfect defence %i %s' % (damage, 'not implemented.'))
                defender.stat_dict['npdefence'] += 1
            if def_natural == 20:
                results.append('Perfect defence %s' % defender.attack(self, True))
                defender.stat_dict['pdefence'] += 1
        return '\n  '.join(results)

    def hit(self, damage):
        texts = list()
        texts.append('for %i' % damage)
        damage = self.armor.hit(damage)
        if damage > 0:
            self.hitpoints -= damage
            texts.append('took %i damage' % damage)
            texts.append(self.check_top(damage))
        else:
            texts.append('absorbed')
        return ', '.join(texts)

    def miss(self, damage):
        if not self.shield:
            return ''
        texts = list()
        texts.append('for %i' % damage)
        damage = self.shield.hit(damage)
        if self.shield.shattered:
            self.shield = no_shield()
            texts.append('shield shattered')
        damage = self.armor.hit(damage)
        if damage > 0:
            self.hitpoints -= damage
            texts.append('took %i damage' % damage)
            texts.append(self.check_top(damage))
        else:
            texts.append('absorbed')
        return ', '.join(texts)

    def check_top(self, damage):
        text = ''
        if self.hitpoints <= 0:
            return 'dead!'
        if damage > self.top:
            top = (d20() - self.top_save) * 5
            if top > 0:
                self.stat_dict['longest_ko'] = max(top, self.stat_dict['longest_ko'])
                if not self.down:
                    self.stat_dict['knockouts'] += 1
                text = 'down for %i seconds!' % top
                self.down = True
                self._count = self.count + top
            else:
                self.stat_dict['top_saves'] += 1
                text = 'made ToP(%i) save!' % self.top
        return text


def deathmatch(a, b):
    return fight(a, b, True)


def deathmatch_silent(a, b):
    return fight_silent(a, b, True)


def fight(a, b, to_the_death=False):
    print 'count action'
    for count in range(1, 10000):
        a.count = b.count = count
        for dude, wuss in ((a, b), (b, a)):
            if dude.can_act:
                print '%-5i %s' % (count, dude.attack(wuss))
            if wuss.dead or (not to_the_death and wuss.down):
                print '%s wins! %s %s.' % (dude, wuss, wuss.status)
                print dude.name, dude.stats
                if wuss.stat_dict['hits'] == 0:
                    print 'Total shutout!'
                else:
                    print wuss.name, wuss.stats
                print ''
                return dude


def fight_silent(a, b, to_the_death=False):
    for count in range(1, 10000):
        a.count = b.count = count
        for dude, wuss in ((a, b), (b, a)):
            if dude.can_act:
                dude.attack(wuss)
            if wuss.dead or (not to_the_death and wuss.down):
                return dude


def fight_stats(a, b, func, count):
    wins = {a.name: 0, b.name: 0}
    deaths = {a.name: 0, b.name: 0}
    knockouts = {a.name: 0, b.name: 0}
    fight_name = func.__name__.replace('_', ' ').title()
    foo = '%s in %s with %s and %s' % (a, a.armor, a.weapon, a.shield)
    bar = '%s in %s with %s and %s' % (b, b.armor, b.weapon, b.shield)
    print '%s\n%s\n%svs\n%s' % (fight_name, foo, ' ' * ((len(foo) - 2) / 2), bar)
    for i in range(count):
        wins[func(a, b).name] += 1
        for dude in a, b:
            if dude.dead:
                deaths[dude.name] += 1
            elif dude.down:
                knockouts[dude.name] += 1
            dude.reset()
    pount = count / 100.0
    awins = wins[a.name] / 100.0
    bwins = wins[b.name] / 100.0
    print '%-15s %i(%0.1f%%) wins(%0.1f%% by death, %0.1f%% by ko), killed %4i and ko\'d %4i times.' % (a.name, wins[a.name], wins[a.name] / pount, deaths[b.name] / awins, knockouts[b.name] / awins, deaths[a.name], knockouts[a.name])
    print '  ', a.aggregate_stats
    print '%-15s %i(%0.1f%%) wins(%0.1f%% by death, %0.1f%% by ko), killed %4i and ko\'d %4i times. ' % (b.name, wins[b.name], wins[b.name] / pount, deaths[a.name] / bwins, knockouts[a.name] / bwins, deaths[b.name], knockouts[b.name])
    print '  ', b.aggregate_stats
    print ''
    a.reset_stats()
    b.reset_stats()


no_shield = lambda: Shield('no shield', -4, 0)
small_shield = lambda: Shield('small shield', 4, 4, threshhold=[8, 12, 16, 20])
medium_shield = lambda: Shield('medium shield', 6, 6, threshhold=[12, 18, 24, 30])

no_armor = Armor('no armor', 0, 0)
leather = Armor('leather', -2, 2)
padded = Armor('padded', -3, 2)
studded = Armor('studded', -3, 3)
ringmail = Armor('ringmail', -4, 4, 1)
scalemail = Armor('scalemail', -6, 5, 2)

longsword = Weapon('longsword', 10, d8p, d8p)
greatsword = Weapon('greatsword', 12, d8p, d10p)
twohandsword = Weapon('two-handsword', 16, d12p, d12p)
greataxe = Weapon('greataxe', 14, d8p, d12p)
battleaxe = Weapon('battleaxe', 12, d4p, d4p, d4p, d4p)
warhammer = Weapon('warhammer', 8, d6p, d6p)


if __name__ == '__main__':
    if False:
        count = 12000
        foo = PenetrationDieFactory(6, 2)
        bar = PenetrationDieFactory(12, 2)
        dieroll_detail(foo, count)
        dieroll_detail(bar, count)
#        dieroll_average_n_max(dice.d4p, count)
#        dieroll_average_n_max(dice.d6p, count)
#        dieroll_average_n_max(dice.d8p, count)
#        dieroll_average_n_max(dice.d12p, count)
#        dieroll_average_n_max(dice.d20p, count)
#        dieroll_average_n_max(dice.d100p, count)

    if False:
        for i in range(5):
            test_sheild_use(0, 0, i, d8p, d8p)

    if True:
        armor = scalemail
        dude = Combatant('The Dude',     33, 8, 1, 2, 0, 0, longsword,  medium_shield, armor)
        hamr = Combatant('Hammertime',   33, 8, 1, 2, 0, 0, warhammer,  medium_shield, armor)
        baxe = Combatant('Axeman',       33, 8, 1, 2, 0, 0, battleaxe,  medium_shield, armor)
        gaxe = Combatant('Death Dealer', 33, 8, 1, 2, 0, 0, greataxe,   no_shield, armor)
        hope = Combatant('Great Hope',   33, 8, 1, 2, 0, 0, greatsword, no_shield, armor)
        zwei = Combatant('Compensator',  33, 8, 1, 2, 0, 0, twohandsword, no_shield, armor)
        for looser in (hamr, baxe, gaxe, hope, zwei):
            fight_stats(dude, looser, fight_silent, 1000)
        #fight_stats(dude, zwei2, deathmatch_silent, 1000)
