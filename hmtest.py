#!/usr/bin/python
'''Hack Master 5ed combat tests.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain 2012.
Website: http://trollandflame.blogspot.com/
'''
import sys
from collections import defaultdict

from dice import *


class BaseProtection(object):

    def __init__(self, name, damage_reduction, defense, initiative=0, speed=0):
        self.name = name
        self.dr = damage_reduction
        self.defense = defense
        self.initiative = initiative    # modifier / penalty
        self.speed = speed              # modifier / penalty

    def __str__(self):
        return self.name


class Armor(BaseProtection):
    def hit(self, damage, hvydr):
        '''Reduce damage by DR.'''
        return max(0, damage - (self.dr + hvydr))


class Shield(BaseProtection):
    def __init__(self, *args, **kwargs):
        self._threshold = kwargs.get('threshhold', list())
        if 'threshhold' in kwargs:
            del kwargs['threshhold']
        super(Shield, self).__init__(*args, **kwargs)
        self.shattered = False

    def hit(self, damage):
        '''Reduce damage by DR, test for shatter.'''
        if self.shattered or not self._threshold:
            return damage
        passed = damage - self.dr
        if damage >= self._threshold[3]:
            self.shatter()
        elif damage >= self._threshold[0]:
            # Opposed die rolls to see if shield destroyed.
            attacker = d20()
            defender = d20()
            if damage >= self._threshold[2] and attacker > (defender - 6):
                self.shatter()
            elif damage >= self._threshold[1] and attacker > defender:
                self.shatter()
            elif damage >= self._threshold[0] and attacker > (defender + 6):
                self.shatter()
        return max(0, passed)

    def shatter(self):
        if not self.shattered:
            self.name = "shattered %s" % self.name
            self.defense = 0
            self.dr = 0
        self.shattered = True


class Weapon(object):
    def __init__(self, name, size, speed, reach, hvydr, damage_dice, shield_dice, damage_bonus=0):
        self.name = name
        self.size = size
        self.speed = speed
        self.reach = reach
        self.hvydr = hvydr                  # Adjusts heavy (>= 5) DR
        self.damage_dice = damage_dice      # Regular damage
        self.shield_dice = shield_dice      # Damage vs shield
        self.damage_bonus = damage_bonus    # Applies to both regular and shield
        self.last_roll = list()

    def __str__(self):
        return self.name

    def roll_damage(self, shield, critical=False):
        total = 0
        roll = list()
        dice = self.shield_dice if shield else self.damage_dice
        for die in dice:
            total += die()
            roll.append('+'.join(str(d) for d in die._rolls))
        if critical:
            for die in dice:
                total += die()
                roll.append('+'.join(str(d) for d in die._rolls))
        roll.append('+%i' % self.damage_bonus)
        self.last_roll = ' '.join(roll)
        return total + self.damage_bonus


class Combatant(object):

    def __init__(self, name, hitpoints, top_save, atk_bonus, dmg_bonus, def_bonus, spd_bonus, weapon, shield, armor):
        '''
        def_bonus does not include armor or shield
        '''
        self.name = name
        self.original_hp = hitpoints
        # threshold of pain!!!
        self.top = int(hitpoints * 0.32)    # 30% + 1%/lvl or 2%/lvl for fighters
        self.top_save = top_save            # 1/2 Con
        self.atk_bonus = atk_bonus
        self.dmg_bonus = dmg_bonus
        self._def_bonus = def_bonus     # natural, not including equipment
        self._spd_bonus = spd_bonus     # natural, not including equipment
        self.weapon = weapon            # Weapon instance
        self.gimmie_shield = shield     # func() returns new shield
        self.armor = armor              # Armor instance
        self.reset()
        self.reset_stats()

    def reset(self):
        '''Internal values'''
        self.hitpoints = self.original_hp
        self.shield = self.gimmie_shield()
        self.topped = False             # False or count at which no longer topped
        self.prone = False
        self.next_attack = 1            # next count I can acton
        self.free_attack = False        # free attack from defender
        self.attacked = False           # been attacked since my last swing
        if hasattr(self, 'stat_dict'):
            self._calc_percent(self.stat_dict)
            self._aggregate_stats.append(self.stat_dict)
        self.stat_dict = defaultdict(int)

    def reset_stats(self):
        self._aggregate_stats = list()

    def __str__(self):
        prone = '_' if self.prone else ''
        topped = '*' if self.topped else ''
        return '%s[%ihp%s%s]' % (self.name, self.hitpoints, prone, topped)

    @property
    def def_bonus(self):
        '''from armor, shields, weapon,'''
        defense = self._def_bonus
        if self.armor:
            defense += self.armor.defense
        if not (self.topped or self.prone):
            if self.shield:
                defense += self.shield.defense
            elif self.weapon.name.lower() == 'halberd':
                # halberds are always 20p
                pass
            elif self.weapon.size == 'L' and self.attacked:
                # 2-handed defense d20p first attack, d20p-4 others
                defense -= 4
        return defense

    @property
    def def_die(self):
        '''Die rolled for defense'''
        if self.topped or self.prone:
            return d8p
        else:
            return d20p

    @property
    def speed(self):
        return self._spd_bonus + self.armor.speed + self.weapon.speed

    @property
    def dead(self):
        return self.hitpoints <= 0

    @property
    def stats(self):
        self._calc_percent(self.stat_dict)
        return self._format_stats(self.stat_dict)

    @property
    def aggregate_stats(self):
        stats = self._calc_aggreagate(self._aggregate_stats)
        return [
                '%(swings)i swings hit/miss %(hits)i/%(misses)i %(percent)0.1f%%: %(max_hit)i maxdmg, %(topsaves)i top saves' % stats,
                '%(crits)i/%(pcrits)0.1f%% crits, %(afumble)i/%(pafumble)0.1f%% %(dfumble)i/%(pdfumble)0.1f%% a/d fumbles, %(pdefense)i/%(npdefense)i p/n defenses' % stats,
               ]

    @property
    def aggregate_averages(self):
        stats = self._calc_aggreagate_averages(self._aggregate_stats)
        return 'hit/miss: %(hits_avg)i/%(misses_avg)i (%(percent_avg)0.1f%%), %(crits_avg)i/%(max_hit_avg)ihp crits/max, %(afumble_avg)i/%(dfumble_avg)i a/d fumbles, %(pdefense_avg)i/%(npdefense_avg)i p/n defenses, %(knockouts_avg)i/%(longest_ko_avg)i k/r/l' % stats

    def _calc_aggreagate_averages(self, aggregates):
        stats = defaultdict(int)
        count = len(aggregates) + 0.0
        sums = self._calc_aggreagate(aggregates)
        for k, v in sums.items():
            stats[k + '_avg'] = v / count
        if stats['swings_avg']:
            stats['percent_avg'] = stats['hits_avg'] / \
                (stats['swings_avg'] / 100.0)
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
            stats['pdefense'] += stat['pdefense']
            stats['npdefense'] += stat['npdefense']
            stats['recovery'] += stat['recovery']
            stats['knockouts'] += stat['knockouts']
            stats['topsaves'] += stat['topsaves']
            stats['max_hit'] = max(stats['max_hit'], stat['max_hit'])
            stats['longest_combat'] = max(
                stats['longest_combat'], stat['longest_combat'])
            stats['longest_ko'] = max(stats['longest_ko'], stat['longest_ko'])
        self._calc_percent(stats)
        return stats

    def _calc_percent(self, stats):
        if stats['swings']:
            stats['percent'] = stats['hits'] / (stats['swings'] / 100.0)
            stats['pafumble'] = stats['afumble'] / (stats['swings'] / 100.0)
            stats['pdfumble'] = stats['dfumble'] / (stats['swings'] / 100.0)
            stats['pcrits'] = stats['crits'] / (stats['swings'] / 100.0)
        else:
            stats['percent'] = 0.0

    def _format_stats(self, stats):
        return 'hit/miss: %(hits)i/%(misses)i (%(percent)0.1f%%), %(crits)i crits, max hit %(max_hit)i, %(afumble)i/%(dfumble)i a/d fumbles, %(pdefense)s/%(npdefense)s p/n defenses' % stats

    def can_act(self, count):
        '''
        :param count: current count up.
        '''
        if self.dead:
            return False
        elif self.topped is not False:
            if self.topped > count:
                self.topped -= 1
            else:
                self.topped = False
                self.stat_dict['recovery'] += 1
            return False
        elif self.prone: # hack with attack() performs standup
            return True
        elif self.free_attack:
            return True
        elif self.next_attack > count:
            return False
        else:
            return True

    def attack(self, count, defender, free=False):
        '''
        :param defender: Combatant I am attacking
        :param free: a free attack that does not reset my count
        '''
        if self.prone:
            # 1 sec to standup
            self.prone = False
            self.next_attack = count + self.speed
            return '%s standing up' % (self, )
        if self.free_attack:
            self.free_attack = False
            return self.attack(count, defender, free=True)
        self.stat_dict['swings'] += 1
        self.stat_dict['longest_combat'] = max(self.stat_dict['longest_combat'], count)
        atk_roll = d20p()
        atk_tot = atk_roll + self.atk_bonus
        def_roll = defender.def_die()
        def_tot = def_roll + defender.def_bonus
        # Must come after tot calcs.
        self.attacked = False
        defender.attacked = True
        # nat 1 attacker is auto-miss
        # nat 1 attacker and not > def_tot is auto-miss and fumble
        # nat 1 defender is not auto, but attacker gets free attack (see below)
        # nat 20 attacker is auto-hit. Critical if total > def_tot
        # nat 20 defender is auto-miss
        # both nat 20's then compare totals
        text = ''
        shieldhit = False
        if atk_roll == 1:
            hit = False
        elif atk_roll >= 20 and def_roll < 20:
            hit = True
        elif def_roll >= 20 and atk_roll < 20:
            hit = False
        else:
            hit = atk_tot > def_tot  # Defender wins ties.
            # shield hit only on non-auto miss.
            if defender.shield and atk_tot > (def_tot - 10):
                shieldhit = True
                text = 'shield '
        # only count true hit, not shieldhit.
        if hit:
            self.stat_dict['hits'] += 1
        else:
            self.stat_dict['misses'] += 1
        bits = list()
        bits.append('%s(%i+%i) -> %s(%i+%i)' % (self, atk_roll, atk_tot - atk_roll, defender, def_roll, def_tot - def_roll))
        if hit or shieldhit:
            if atk_roll >= 20 and atk_tot > def_tot:
                self.stat_dict['crits'] += 1
                text += 'crit'
                damage = self.weapon.roll_damage(defender.shield, critical=True)
            else:
                text += 'hit'
                damage = self.weapon.roll_damage(defender.shield)
            if damage >= 30:
                text += ' & 2xkb'
            elif damage >= 15:
                text += ' & kb'
            self.stat_dict['max_hit'] = max(self.stat_dict['max_hit'], damage)
            if defender.shield and not (defender.topped or defender.prone):
                passed, shattered = defender.hit_shield(damage)
                took = defender.hit(passed, 0) # No hvydr when hitting shield.
                bits.append('%s for %i(%s), %spassed %i%s%s' % (text, damage, self.weapon.last_roll, 'shattered and ' if shattered else '', passed, ', took %i damage' % took if took else '', defender.check_for_top(count, took)))
            else:
                took = defender.hit(damage, self.weapon.hvydr)
                bits.append('%s for %i(%s), took %i damage%s' % (text, damage, self.weapon.last_roll, took, defender.check_for_top(count, took)))
            # Must come after application of damage.
            if damage >= 30:
                defender.prone = True
        else:
            bits.append('missed')
        results = [' '.join(t.strip() for t in bits if t), ]
        # Fumbles.el
        if atk_roll == 1 and atk_tot <= def_tot:
            results.append('Attacker fumble: Not implemented.')
            self.stat_dict['afumble'] += 1
        if def_roll == 1:
            results.append('Defender fumble: Attacker gets free attack next second.')
            self.free_attack = True
            defender.stat_dict['dfumble'] += 1
        # Perfect and near perfect defenses.
        if def_tot > atk_tot and not (defender.topped or defender.dead or defender.prone):
            if def_roll == 19:  # ignore armor/shield DR
                pass
                # TODO: make this a real attack()
#                self.attacked = True
#                defender.attacked = False
#                # knife / dagger use weapon's damage
#                damage = (d4p - 2) + (d4p - 2) + defender.dmg_bonus  # TODO: add str and unarmed.
#                text = ''
#                if damage >= 30:
#                    text = ' & 2xkb'
#                    defender.prone = True
#                elif damage >= 15:
#                    text = ' & kb'
#                self.hitpoints -= damage  # Bypasses armor/shield.
#                top_text = self.check_for_top(count, damage)
#                results.append('Near perfect defense: %s took %i damage%s%s' % (self, damage, text, top_text))
#                defender.stat_dict['npdefense'] += 1
            if def_roll >= 20:
                results.append('Perfect defense: %s' % defender.attack(count, self, True))
                defender.stat_dict['pdefense'] += 1
        if not free:  # update count
            if defender.topped or defender.prone:
                self.next_attack = count + (self.speed / 2)
            else:
                self.next_attack = count + self.speed
        return '\n    '.join(results)

    def hit(self, damage, hvydr):
        '''
        return damage getting through armor.
        hvydr: amount of heavy (>= 5) DR ignored.
        '''
        damage = self.armor.hit(damage, hvydr)
        if damage > 0:
            self.hitpoints -= damage
        return max(0, damage)

    def hit_shield(self, damage):
        '''return damage getting through shield, T/F if shattered'''
        if not self.shield:
            raise Exception('I got no shield')
        damage = self.shield.hit(damage)
        if self.shield.shattered:
            self.shield = False
            return damage, True
        else:
            return damage, False

    def check_for_top(self, count, damage):
        if self.hitpoints <= 0:
            return ', dead!'
        if damage <= self.top:
            return ''
        roll = d20()
        if roll > self.top_save:
            top = 5 * (roll - self.top_save)
            self.stat_dict['longest_ko'] = max(top, self.stat_dict['longest_ko'])
            if self.topped is False:
                self.stat_dict['knockouts'] += 1
                self.topped = count
            self.topped += top  # Add seconds topped.
            self.prone = True
            self.free_attack = False
            return ', topped[%i] (%i>%i) for %i seconds!' % (self.top, roll, self.top_save, top)
        else:
            self.stat_dict['topsaves'] += 1
            return ', made ToP[%i] (%i<=%i) save!' % (self.top, roll, self.top_save)


def fight(a, b, play_by_play=False, deathmatch=False):
    '''
    :param a: combatant 'a'.
    :param b: combatant 'b'.
    :return: winner of fight or None on draw
    '''
    def status(dude):
        if dude.dead:
            return 'Dead'
        elif dude.topped:
            return 'Writhing in pain unti %i' % (dude.topped, )
        elif dude.prone:
            return 'Prone'
        elif count == dude.next_attack:
            return 'Ready'
        else:
            return 'Waiting until %i' % (dude.next_attack, )

    if play_by_play:
        pbp = lambda t: (sys.stdout.write(t), sys.stdout.write('\n'))
    else:
        pbp = lambda t: None
    pbp('')
    for count in range(1, 10000):  # Count here is hackmaster initiative count.
        # Support simultaneous attacks.
        attacks = list()
        if count == 1 and a.weapon.reach != b.weapon.reach: # First attack by reach.
            if b.weapon.reach > a.weapon.reach:
                a, b = b, a
            attacks.append((a, b))
        else:
            if a.can_act(count):
                attacks.append((a, b))
            if b.can_act(count):
                attacks.append((b, a))
        for attacker, defender in attacks:
            pbp('%-3i %s' % (count, attacker.attack(count, defender)))
        winnars = [d for d in (a, b) if not (d.dead or (not deathmatch and d.topped))]
        if len(winnars) != 2:
            break
    pbp('%s %s\n  %s' % (a, status(a), a.stats))
    pbp('%s %s\n  %s' % (b, status(b), b.stats))
    if len(winnars) == 1:
        win = winnars[0]
        pbp('%s wins!' % (win, ))
        return win


def fight_stats(a, b, func, count, play_by_play=False):
    '''
    :param a: combatant 'a'.
    :param b: combatant 'b'.
    :param func: resolve one fight func(a, b)
    :param count: how many fights to run
    '''
    def bubba(d):
        if d.shield:
            return '%s in %s with %s & %s' % (d, d.armor, d.weapon, d.shield)
        else:
            return '%s in %s with %s' % (d, d.armor, d.weapon)
    wins = {a.name: 0, b.name: 0}
    deaths = {a.name: 0, b.name: 0}
    knockouts = {a.name: 0, b.name: 0}
    foo = bubba(a)
    bar = bubba(b)
    print '%s\n%svs\n%s' % (foo, ' ' * ((len(foo) - 2) / 2), bar)
    for i in range(count):
        winner = func(a, b, play_by_play)
        if winner:
            wins[winner.name] += 1
        for dude in a, b:
            if dude.dead:
                deaths[dude.name] += 1
            elif dude.topped:
                knockouts[dude.name] += 1
            dude.reset()
    pount = count / 100.0
    awins = wins[a.name] / 100.0
    bwins = wins[b.name] / 100.0
    print '''%-12s %i/%0.1f%% wins (%0.1f%% by death, %0.1f%% by ko). Killed %4i and ko'd %4i times.''' % (a.name, wins[a.name], wins[a.name] / pount, deaths[b.name] / awins, knockouts[b.name] / awins, deaths[a.name], knockouts[a.name])
    for line in a.aggregate_stats:
        print ' ' * 12, line
    print '''%-12s %i/%0.1f%% wins (%0.1f%% by death, %0.1f%% by ko). Killed %4i and ko'd %4i times.''' % (b.name, wins[b.name], wins[b.name] / pount, deaths[a.name] / bwins, knockouts[a.name] / bwins, deaths[b.name], knockouts[b.name])
    for line in b.aggregate_stats:
        print ' ' * 12, line
    print ''
    a.reset_stats()
    b.reset_stats()


#   damage reduction, defense, splinter thresholds [d20p+6, d20p, d20p-6, automatic]
buckler = lambda: Shield('buckler', 4, 2, threshhold=[8, 12, 16, 20])
small_shield = lambda: Shield('small shield', 4, 4, threshhold=[8, 12, 16, 20])
medium_shield = lambda: Shield('medium shield', 6, 6, threshhold=[12, 18, 24, 30])
large_shield = lambda: Shield('large shield', 6, 6, threshhold=[12, 18, 24, 30])

#   damage reduction, defense, initiative, speed penalty
no_armor = Armor('no armor',     0,  0, -1, 0)
leather = Armor('leather',       2, -2, 0, 0)
padded = Armor('padded',         2, -3, 1, 0)
studded = Armor('studded',       3, -3, 1, 0)
ringmail = Armor('ringmail',     4, -4, 1, 1)
scalemail = Armor('scalemail',   5, -6, 3, 2)
bandedmail = Armor('bandedmail', 6, -4, 2, 1)
platemail = Armor('bandedmail',  7, -5, 2, 2)

#   size, speed, reach, hvy DR reduction, damage, shield_damage):
battleaxe = Weapon('battleaxe', 'M', 12, 3.0, -2, (d3p, d3p, d3p, d3p), (d3p, d3p, d3p))
longsword = Weapon('longsword', 'M', 10, 3.5, 0, (d8p, d8p), (d8p,))
greathammer = Weapon('greathammer', 'M', 12, 2.5, -1, (d8p, d10p), (d10p, ))
twohandsword = Weapon('two-handsword', 'L', 16, 6.0, -2, (d12p, d12p), (d12p, ), +3)
halberd = Weapon('halberd', 'L', 14, 7, -2, (d10p, d10p), (d10p, ), +3)  # -2DR if hvy >=5, d20p defense

armor = platemail
#                 name,        hp, top_save, atk, dmg, def, speed
dude = Combatant('The Dude',   53, 8, 4, 3, 4, -2, longsword, medium_shield, armor)
hamr = Combatant('Hammertime', 53, 8, 4, 3, 4, -2, greathammer, medium_shield, armor)
baxe = Combatant('Axeman',     53, 8, 4, 3, 4, -2, battleaxe, medium_shield, armor)
halb = Combatant('Halberder',  53, 8, 4, 3, 4, -2, halberd, lambda: None, armor)
zwei = Combatant('Compensatr', 53, 8, 4, 3, 4, -2, twohandsword, lambda: None, armor)


if __name__ == '__main__':

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
                results.append('%-3i %5i %5.2f%% %6.2f%%' %
                            (i, bucket[i], percent, ptotal))
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

    if False:
        count = 12000
        foo = PenetrationDieFactory(6, 2)
        bar = PenetrationDieFactory(12, 2)
        dieroll_detail(foo, count)
        dieroll_detail(bar, count)
        dieroll_average_n_max(dice.d4p, count)
        dieroll_average_n_max(dice.d6p, count)
        dieroll_average_n_max(dice.d8p, count)
        dieroll_average_n_max(dice.d12p, count)
        dieroll_average_n_max(dice.d20p, count)
        dieroll_average_n_max(dice.d100p, count)

    if False:
        fight_stats(dude, zwei, fight, 10, True)
    else:
        for looser in (hamr, baxe, halb, zwei):
            fight_stats(dude, looser, fight, 1000)
