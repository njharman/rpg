#!/usr/bin/python
'''Berserk Probabilitiy Experiements
2010 njharman@gmail.com placed into the public domain
'''

from collections import defaultdict
from dice import *


def sustain_berserk(count, wis, damage=0):
    '''How long berserk lasts.'''
    durations = defaultdict(int)
    for i in range(count):
        rounds = 1
        while True:
            if ((2 * d6()) + damage) > wis or rounds == 10:
                durations[rounds] += 1
                break
            rounds += 1
    return durations


def berserk(count, val):
    '''2d6+modifer >= val (2 always fail).'''
    counts = defaultdict(int)
    for i in range(count):
        for modifier in range(0, 10):
            roll = d6() + d6()
            if roll != 2 and roll + modifier >= val:
                counts[modifier] += 1
    values = list()
    for i in range(0, 10):
        values.append(counts.get(i, 0))
    return ' '.join('{1:2.0f}%'.format(x, (x * 100.0) / count) for x in values)


def out(text):
    #text = text.replace(' ', '&nbsp;')
    print text


if __name__ == '__main__':
        #print 'sustain ' + format_durations(sustain_berserk(count, wiz))
        count = 10000
        out('2d6 + mod >= value, 2 always fail, "rolled" {0} times.'.format(count))
        out('            modifier')
        out('value ' + '    '.join('{0:+2}'.format(r) for r in range(0, 10)))
        for wiz in range(3, 19):
            out(' {0:2}    '.format(wiz) + berserk(count, wiz))
