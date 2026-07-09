#!/usr/bin/env python3
'''Quick hack to compare d20 vs d24 vs d30 for D&D to-hit rolls.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Oct 2010.
Website: http://trollandflame.blogspot.com/
'''

import die


def print_summary(roll, count):
    stat = die.stats.Statistic(roll)
    stat.do_run(count)
    print(f'{count:<4} {roll}s')
    cumulative = 0.0
    count = float(count)
    for rolled, times in stat.bucket:
        percent = (times / count) * 100
        cumulative += percent
        print(f'{rolled:>5} -> {times:<5} {percent:6.2f}% {cumulative:6.2f}%', end='')
        if rolled == stat.avr:
            print(' "average"')


def print_summaries(rolls, count):
    stats = list()
    print(f'{count:<9}', end='')
    for roll in rolls:
        stat = die.stats.Statistic(roll)
        stat.do_run(count)
        stat.cumulative = 0.0
        stats.append(stat)
        print(f'{roll!s:<15}', end='')
    print()
    count = float(count)
    for rolled in range(1, 21):
        print(f'{rolled:>4} -> ', end='')
        for stat in stats:
            try:
                times = stat._bucket[rolled]
                highest = stat.bucket[-1][0]
                if rolled == 20 and highest > 20:
                    times += sum(stat._bucket[x] for x in range(21, highest + 1))
                    # print('\n', stat.roll, [(x, stat._bucket[x]) for x in range(21, len(stat._bucket)+1)])
                percent = (times / count) * 100
                stat.cumulative += percent
            except KeyError:
                percent = 0
            if rolled == stat.avr:
                avr = 'a'
            else:
                avr = ' '
            print(f'{percent:5.2f}% {stat.cumulative:6.2f}%{avr}', end='')
        print()


def add(mod):
    def func(rolls):
        return rolls[0] + mod
    return func

d6 = die.Standard(6)
d20 = die.Standard(20)
d24 = die.Standard(24)
d30 = die.Standard(30)

d20_attack = die.Roll([d20, ], 'd20')
d24_attack = die.Roll([d24, ], 'd24')
d30_attack = die.Roll([d30, ], 'd30')
d20plus2_attack = die.FuncRoll(add(2), [d20, ], 'd20+2')
d20plus4_attack = die.FuncRoll(add(4), [d20, ], 'd20+4')
best_attack = die.FuncRoll(max, [d20, d20], '2d20(best)')
worst_attack = die.FuncRoll(min, [d20, d20], '2d20(worst)')

best_d6 = die.FuncRoll(max, [d6, d6], '2d6(best)')
worst_d6 = die.FuncRoll(min, [d6, d6], '2d6(worst)')

rolls = [worst_attack, best_attack, d20plus2_attack, d20plus4_attack, d24_attack, d30_attack]
rolls = [best_d6, worst_d6]
print_summaries(rolls, 10000)
