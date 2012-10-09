#!/usr/bin/python
'''No idea.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain.
Website: http://trollandflame.blogspot.com/
'''

from collections import defaultdict
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


def miscast():
    return ''


def wizcast(to_cast_bonus, delayed=True, roll=None):
    if roll is None:
        roll = d20x()
        if delayed:
            roll += 5
    if roll == 1:
        return 'miscast(%i) - %s' % (roll, miscast())
    roll += to_cast_bonus
    if roll >= 20:
        return 'cast(%i)' % (roll, )
    elif roll >= 15:
        return 'delayed(%i)' % (roll, )
    elif roll >= 10:
        return 'failed(%i)' % (roll, )
    elif roll >= 5:
        return 'lost(%i)' % (roll, )
    else:
        return 'miscast(%i) - %s' % (roll, miscast())


def do_wizcast(to_cast_bonus=4):
    results = list()
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
    '''success/fail chances.'''
    results = defaultdict(int)
    casted = defaultdict(int)
    failed = defaultdict(int)
    for i in range(runcount):
        cast, time, text = do_wizcast(to_cast_bonus)
        cast = cast[:cast.find('(')].lower()
        results[cast] += 1
        if cast == 'cast':
            casted[time] += 1
        else:
            failed[time] += 1
    print '\nChance for various outcomes of casting attempt.'
    print '        count percentage'
    for result in ('miscast', 'lost', 'failed', 'cast'):
        count = results[result]
        print '%-8s %3i  %2.0f%%' % (result.title() + ':', count, (count * 100.0) / runcount)
    print '\nCasting times:'
    running = 0
    for i in sorted(casted.keys()):
        running += casted[i]
        print '%2i rnds %4i  %5.2f%% %6.2f%%' % (i, casted[i], (casted[i] * 100.0) / results['cast'], (running * 100.0) / results['cast'])
    print
    print 'avg casting time: %.1f rnds' % (sum(k * v for k, v in casted.items()) / (results['cast'] + 0.0), )
    print 'avg failure time: %.1f rnds' % (sum(k * v for k, v in failed.items()) / (runcount - results['cast'] + 0.0), )


def test_wizspell(runcount, to_cast_bonus):
    '''How many times can one spell be cast before miscast/lost'''
    results = defaultdict(int)
    for i in range(runcount):
        count = 0
        while True:
            result, time, text = do_wizcast(to_cast_bonus)
            result = result[:result.find('(')].lower()
            #print result, time, text
            if result in ('lost', 'miscast'):
                break
            elif result in ('cast', ):
                count += 1
        results[count] += 1
        #print count, '\n'
    total = sum(results.values())
    lost_total = results[0]
    lost_percentage = (results[0] * 100.0) / total
    del results[0]
    cast_total = sum(results.values())
    cast_percentage = 100 - lost_percentage
    running = 0
    print '\nChance spell is cast x number of times before being lost.'
    for i in sorted(results.keys()):
        print '%2i times %4i  %5.2f%% %6.2f%%' % (i, results[i], (results[i] * 100.0) / total, cast_percentage - ((running * 100.0) / total))
        running += results[i]
    print 'Cast     %4i  %5.2f%% %6.2f%%' % (cast_total, cast_percentage, cast_percentage, )
    print 'Lost     %4i  %5.2f%% %6.2f%%' % (lost_total, lost_percentage, lost_percentage, )


if __name__ == '__main__':
    count = 1000
    bonus = 6
    test_wizspell(count, bonus)
    test_wizcast(count, bonus)
