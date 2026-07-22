#!/usr/bin/env python
"""No idea.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: http://trollandflame.blogspot.com/
"""

from collections import defaultdict

from die import d20x


def dieroll_test(die_func, count=100000):
    bucket = defaultdict(int)
    for _ in range(count + 1):
        bucket[die_func()] += 1
    return bucket, count


def calc_dieroll_results(bucket, count):
    count = float(count)
    rolls = bucket.keys()
    rolls.sort()
    total = 0
    ptotal = 100
    results = []
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
    _rolls, _avg, _max = calc_dieroll_results(*dieroll_test(roll, count))


def dieroll_detail(roll, count=100000):
    rolls, _avg, _max = calc_dieroll_results(*dieroll_test(roll, count))
    for roll in rolls:
        print(roll) # TODO: implement


def miscast():
    return ''


def wizcast(to_cast_bonus, delayed=True, roll=None):
    if roll is None:
        roll = d20x()
        if delayed:
            roll += 5
    if roll == 1:
        return f'miscast({roll}) - {miscast()}'
    roll += to_cast_bonus
    if roll >= 20:
        return f'cast({roll})'
    if roll >= 15:
        return f'delayed({roll})'
    if roll >= 10:
        return f'failed({roll})'
    if roll >= 5:
        return f'lost({roll})'
    return f'miscast({roll}) - {miscast()}'


def do_wizcast(to_cast_bonus=4):
    results = []
    delayed = False
    while True:
        results.append(wizcast(to_cast_bonus, delayed))
        if 'delayed' in results[-1]:
            delayed = True
        else:
            break
    cast = results[-1]
    time = len(results)
    text = ' '.join(results)
    return (cast, time, text)


def test_wizcast(runcount, to_cast_bonus):
    """success/fail chances."""
    results = defaultdict(int)
    casted = defaultdict(int)
    failed = defaultdict(int)
    for _ in range(runcount):
        cast, time, _text = do_wizcast(to_cast_bonus)
        cast = cast[:cast.find('(')].lower()
        results[cast] += 1
        if cast == 'cast':
            casted[time] += 1
        else:
            failed[time] += 1
    for result in ('miscast', 'lost', 'failed', 'cast'):
        results[result]
    running = 0
    for i in sorted(casted.keys()):
        running += casted[i]


def test_wizspell(runcount, to_cast_bonus):
    """How many times can one spell be cast before miscast/lost"""
    results = defaultdict(int)
    for _ in range(runcount):
        count = 0
        while True:
            result, time, text = do_wizcast(to_cast_bonus)
            result = result[:result.find('(')].lower()
            print(result, time, text)
            if result in ('lost', 'miscast'):
                break
            if result in ('cast', ):
                count += 1
        results[count] += 1
        print(count, '\n')
    total = sum(results.values())
    results[0]
    lost_percentage = (results[0] * 100.0) / total
    del results[0]
    sum(results.values())
    100 - lost_percentage
    running = 0
    for i in sorted(results.keys()):
        running += results[i]


if __name__ == '__main__':
    count = 1000
    bonus = 6
    test_wizspell(count, bonus)
    test_wizcast(count, bonus)
