#!/usr/bin/python
"""Hack Master 5ed combat tests.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain 2012.
Website: http://trollandflame.blogspot.com/
"""
import sys
from collections import defaultdict

from dice import (
    d3p,
    d4p,
    d4x,
    d6p,
    d6x,
    d8p,
    d8x,
    d10p,
    d12p,
    d12x,
    d20,
    d20p,
    d20x,
    d100p,
    d100x,
)


class BaseProtection:

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
        """Reduce damage by DR."""
        return max(0, damage - (self.dr + hvydr))


class Shield(BaseProtection):
    def __init__(self, *args, **kwargs):
        self._threshold = kwargs.get('threshold', list())
        kwargs.pop('threshold', None)
        super().__init__(*args, **kwargs)
        self.shattered = False

    def hit(self, damage):
        """Reduce damage by DR, test for shatter."""
        if self.shattered or not self._threshold:
            return damage
        passed = damage - self.dr
        if damage >= self._threshold[3]:
            self.shatter()
        elif damage >= self._threshold[0]:
            # Opposed die rolls to see if shield destroyed.
            attacker = d20()
            defender = d20()
            if (damage >= self._threshold[2] and attacker > (defender - 6)) or (damage >= self._threshold[1] and attacker > defender) or (damage >= self._threshold[0] and attacker > (defender + 6)):
                self.shatter()
        return max(0, passed)

    def shatter(self):
        if not self.shattered:
            self.name = f"shattered {self.name}"
            self.defense = 0
            self.dr = 0
        self.shattered = True


class Weapon:
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
        roll.append(f'+{self.damage_bonus}')
        self.last_roll = ' '.join(roll)
        return total + self.damage_bonus


class Combatant:

    def __init__(self, name, hitpoints, top_save, atk_bonus, dmg_bonus, def_bonus, spd_bonus, weapon, shield, armor):
        """
        def_bonus does not include armor or shield
        """
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
        """Internal values"""
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
        return f'{self.name}[{self.hitpoints}hp{prone}{topped}]'

    @property
    def def_bonus(self):
        """from armor, shields, weapon,"""
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
        """Die rolled for defense"""
        if self.topped or self.prone:
            return d8p
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
                f"{stats['swings']} swings hit/miss {stats['hits']}/{stats['misses']} {stats['percent']:0.1f}%: {stats['max_hit']} maxdmg, {stats['topsaves']} top saves",
                f"{stats['crits']}/{stats['pcrits']:0.1f}% crits, {stats['afumble']}/{stats['pafumble']:0.1f}% {stats['dfumble']}/{stats['pdfumble']:0.1f}% a/d fumbles, {stats['pdefense']}/{stats['npdefense']} p/n defenses",
               ]

    @property
    def aggregate_averages(self):
        stats = self._calc_aggreagate_averages(self._aggregate_stats)
        return (f"hit/miss: {stats['hits_avg']}/{stats['misses_avg']} ({stats['percent_avg']:0.1f}%), {stats['crits_avg']}/{stats['max_hit_avg']}hp crits/max,"
          f" {stats['afumble_avg']}/{stats['dfumble_avg']} a/d fumbles, {stats['pdefense_avg']}/{stats['npdefense_avg']} p/n defenses,"
          f" {stats['knockouts_avg']}/{stats['longest_ko_avg']} k/r/l")

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
        return f"hit/miss: {stats['hits']}/{stats['misses']} ({stats['percent']:0.1f}%), {stats['crits']} crits, max hit {stats['max_hit']}, {stats['afumble']}/{stats['dfumble']} a/d fumbles, {stats['pdefense']}/{stats['npdefense']} p/n defenses"

    def can_act(self, count):
        """
        :param count: current count up.
        """
        if self.dead:
            return False
        if self.topped is not False:
            if self.topped > count:
                self.topped -= 1
            else:
                self.topped = False
                self.stat_dict['recovery'] += 1
            return False
        if self.prone or self.free_attack: # hack with attack() performs standup
            return True
        return not self.next_attack > count

    def attack(self, count, defender, free=False):
        """
        :param defender: Combatant I am attacking
        :param free: a free attack that does not reset my count
        """
        if self.prone:
            # 1 sec to standup
            self.prone = False
            self.next_attack = count + self.speed
            return f'{self} standing up'
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
        bits.append(f'{self}({atk_roll}+{atk_tot - atk_roll}) -> {defender}({def_roll}+{def_tot - def_roll})')
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
                bits.append(f"{text} for {damage}({self.weapon.last_roll}), {'shattered and ' if shattered else ''}passed {passed}{f', took {took} damage' if took else ''}{defender.check_for_top(count, took)}")
            else:
                took = defender.hit(damage, self.weapon.hvydr)
                bits.append(f'{text} for {damage}({self.weapon.last_roll}), took {took} damage{defender.check_for_top(count, took)}')
            # Must come after application of damage.
            if damage >= 30:
                defender.prone = True
        else:
            bits.append('missed')
        results = [' '.join(t.strip() for t in bits if t) ]
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
                results.append(f'Perfect defense: {defender.attack(count, self, True)}')
                defender.stat_dict['pdefense'] += 1
        if not free:  # update count
            if defender.topped or defender.prone:
                self.next_attack = count + (self.speed / 2)
            else:
                self.next_attack = count + self.speed
        return '\n    '.join(results)

    def hit(self, damage, hvydr):
        """
        return damage getting through armor.
        hvydr: amount of heavy (>= 5) DR ignored.
        """
        damage = self.armor.hit(damage, hvydr)
        if damage > 0:
            self.hitpoints -= damage
        return max(0, damage)

    def hit_shield(self, damage):
        """return damage getting through shield, T/F if shattered"""
        if not self.shield:
            raise ValueError('I got no shield')
        damage = self.shield.hit(damage)
        if self.shield.shattered:
            self.shield = False
            return damage, True
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
            return f', topped[{self.top}] ({roll}>{self.top_save}) for {top} seconds!'
        self.stat_dict['topsaves'] += 1
        return f', made ToP[{self.top}] ({roll}<={self.top_save}) save!'


def fight(a, b, play_by_play=False, deathmatch=False):
    """
    :param a: combatant 'a'.
    :param b: combatant 'b'.
    :return: winner of fight or None on draw
    """
    def status(dude):
        if dude.dead:
            return 'Dead'
        if dude.topped:
            return f'Writhing in pain unti {dude.topped}'
        if dude.prone:
            return 'Prone'
        if count == dude.next_attack:
            return 'Ready'
        return f'Waiting until {dude.next_attack}'

    if play_by_play:
        def pbp(t):
            return (sys.stdout.write(t), sys.stdout.write('\n'))
    else:
        def pbp(t):
            return None
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
            pbp(f'{count:<3} {attacker.attack(count, defender)}')
        winnars = [d for d in (a, b) if not (d.dead or (not deathmatch and d.topped))]
        if len(winnars) != 2:
            break
    pbp(f'{a} {status(a)}\n  {a.stats}')
    pbp(f'{b} {status(b)}\n  {b.stats}')
    if len(winnars) == 1:
        win = winnars[0]
        pbp(f'{win} wins!')
        return win
    return None


def fight_stats(a, b, func, count, play_by_play=False):
    """
    :param a: combatant 'a'.
    :param b: combatant 'b'.
    :param func: resolve one fight func(a, b)
    :param count: how many fights to run
    """
    def bubba(d):
        if d.shield:
            return f'{d} in {d.armor} with {d.weapon} & {d.shield}'
        return f'{d} in {d.armor} with {d.weapon}'
    wins = {a.name: 0, b.name: 0}
    deaths = {a.name: 0, b.name: 0}
    knockouts = {a.name: 0, b.name: 0}
    foo = bubba(a)
    bar = bubba(b)
    print(f"{foo}\n{' ' * int((len(foo) - 2) / 2)}vs\n{bar}")
    for _ in range(count):
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
    print(f"{a.name:<12} {wins[a.name]}/{wins[a.name] / pount:0.1f}% wins ({deaths[b.name] / awins:0.1f}% by death, {knockouts[b.name] / awins:0.1f}% by ko). Killed {deaths[a.name]:4} and ko'd {knockouts[a.name]:4} times.")
    for line in a.aggregate_stats:
        print(' ' * 12, line)
    print(f"{b.name:<12} {wins[b.name]}/{wins[b.name] / pount:0.1f}% wins ({deaths[a.name] / bwins:0.1f}% by death, {knockouts[a.name] / bwins:0.1f}% by ko). Killed {deaths[b.name]:4} and ko'd {knockouts[b.name]:4} times.")
    for line in b.aggregate_stats:
        print(' ' * 12, line)
    print()
    a.reset_stats()
    b.reset_stats()


#   damage reduction, defense, splinter thresholds [d20p+6, d20p, d20p-6, automatic]
buckler = lambda: Shield('buckler', 4, 2, threshold=[8, 12, 16, 20])
small_shield = lambda: Shield('small shield', 4, 4, threshold=[8, 12, 16, 20])
medium_shield = lambda: Shield('medium shield', 6, 6, threshold=[12, 18, 24, 30])
large_shield = lambda: Shield('large shield', 6, 6, threshold=[12, 18, 24, 30])


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


def dieroll_test(die_func, count=100000):
    bucket = defaultdict(int)
    for _ in range(count + 1):
        bucket[die_func()] += 1
    return bucket, count

def calc_dieroll_results(bucket, count):
    count = float(count)
    rolls = list(bucket.keys())
    rolls.sort()
    total = 0
    ptotal = 100
    results = list()
    for i in range(1, max(rolls) + 1):
        if bucket[i]:
            percent = (bucket[i] / count) * 100
            results.append(f'{i:<3} {bucket[i]:5} {percent:5.2f}% {ptotal:6.2f}%')
            ptotal -= percent
            total += i * bucket[i]
        else:
            results.append(f'{i:<3}         not rolled')
    return results, (total / count), rolls[-1]


def dieroll_average_n_max(roll, count=100000):
    _, avg, highest = calc_dieroll_results(*dieroll_test(roll, count))
    print(roll.name, f'{avg:.2f}', highest)



def dieroll_detail(roll, count=100000):
    rolls, _, _ = calc_dieroll_results(*dieroll_test(roll, count))
    print(roll.name)
    for roll in rolls:
        print(roll)
    print()


if __name__ == '__main__':
    if True:
        count = 12000
        #dieroll_detail(d4p, count)
        #dieroll_detail(d6p, count)
        dieroll_average_n_max(d4p, count)
        dieroll_average_n_max(d6p, count)
        dieroll_average_n_max(d8p, count)
        dieroll_average_n_max(d12p, count)
        dieroll_average_n_max(d20p, count)
        dieroll_average_n_max(d100p, count)
        print()
        dieroll_average_n_max(d4x, count)
        dieroll_average_n_max(d6x, count)
        dieroll_average_n_max(d8x, count)
        dieroll_average_n_max(d12x, count)
        dieroll_average_n_max(d20x, count)
        dieroll_average_n_max(d100x, count)


    if False:
        fight_stats(dude, zwei, fight, 10, True)

    if False:
        for looser in (hamr, baxe, halb, zwei):
            fight_stats(dude, looser, fight, 1000)
