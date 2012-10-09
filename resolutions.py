#!/usr/bin/python
'''No idea.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain.
Website: http://trollandflame.blogspot.com/
'''

from collections import defaultdict

from dice import *


def stat_testor(count, func):
    results = list()
    for stat in range(3, 19, 3):
        winnar = 0
        for i in range(count):
            if func(stat):
                winnar += 1
        results.append(dict(chance=stat, count=count, win=winnar, percent=((winnar * 100.0) / count)))
    return results


def target20_d6(count):
    pass


def x_in_d6_calculated():
    results = list()
    for chance in range(1, 6):
        results.append(dict(chance='1-{0}'.format(chance), count=0, win='na', percent=((chance * 100.0) / 6)))
    return results


def x_in_d6_multiple_d6(count):
    # test if 1, 2, 3 rolls of d6 are within chance
    results = list()
    for chance in range(1, 6):
        one = two = tre = 0
        pants = range(1, chance + 1)
        for i in range(count):
            if d6() in pants:
                one += 1
                two += 1
                tre += 1
            elif d6() in pants:
                two += 1
                tre += 1
            elif d6() in pants:
                tre += 1
        data = dict(chance='1-{0}'.format(chance), count=count, one=one, onep=(one * 100.0) / count, two=two, twop=(two * 100.0) / count, tre=tre, trep=(tre * 100.0) / count)
        results.append('{chance:3}  {one} / {onep:.4}%  {two} / {twop:.4}%  {tre} / {trep:.4}%'.format(**data))
    return '\n'.join(results)


def format_results(results):
    result = list()
    result.append('stat sucessess')
    for data in results:
        result.append('{chance:3}  {win} / {percent:.4}%'.format(**data))
    return '\n'.join(result)


def rolld6():
    count = 10000
    print '|    | {0} |'.format(' | '.join('{0:^5}'.format(i) for i in range(11)))
    for times in range(1, 11):
        results = defaultdict(int)
        for i in range(count):
            asix = 0
            for d in range(times):
                roll = d6()
                if roll == 6:
                    asix += 1
            results[asix] += 1
        print '| {0:<2} | {1} |'.format(times, ' | '.join('{0:5.2f}'.format((results.get(i, 0) * 100.0) / count) for i in range(0, 11)))


if __name__ == '__main__':
    count = 100000

    print '\nx in d6 chance: calculated'
    print format_results(x_in_d6_calculated())
    print '\nx in d6 chance: {0} iterations'.format(count)
    print 'chance  1d6          2d6          3d6'
    print x_in_d6_multiple_d6(count)

    print '\nd20 + stat >= 20: {0} iterations'.format(count)
    print format_results(stat_testor(count, lambda stat: stat + d20() >= 20))
    print '\nd20 + stat > 20: {0} iterations'.format(count)
    print format_results(stat_testor(count, lambda stat: stat + d20() > 20))
    print '\nd20 <= stat: {0} iterations'.format(count)
    print format_results(stat_testor(count, lambda stat: d20() <= stat))
