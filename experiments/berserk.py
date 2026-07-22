#!/usr/bin/env python
"""Berserk Probabilitiy Experiments.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain 2010.
Website: http://trollandflame.blogspot.com/
"""

from collections import defaultdict

from die import d6


def sustain_berserk(count, wis, damage=0):
    """How long berserk lasts."""
    durations = defaultdict(int)
    for _ in range(count):
        rounds = 1
        while True:
            if ((2 * d6()) + damage) > wis or rounds == 10:
                durations[rounds] += 1
                break
            rounds += 1
    return durations


def berserk(count, val):
    """2d6+modifier >= val (2 always fail)."""
    counts = defaultdict(int)
    for _ in range(count):
        for modifier in range(10):
            roll = d6() + d6()
            if roll != 2 and roll + modifier >= val:
                counts[modifier] += 1
    values = []
    for i in range(10):
        values.append(counts.get(i, 0))
    return ' '.join(f'{(x * 100.0) / count:2.0f}%' for x in values)


def out(text):
    # text = text.replace(' ', '&nbsp;')
    print(text)


if __name__ == '__main__':
    # print('sustain ' + format_durations(sustain_berserk(count, wiz)))
    count = 10000
    out(f'2d6 + mod >= value, 2 always fail, "rolled" {count} times')
    out('       modifier')
    out('value   ' + '  '.join(f'{r:+2}' for r in range(10)))
    for wiz in range(3, 19):
        out(f' {wiz:2}    ' + berserk(count, wiz))
