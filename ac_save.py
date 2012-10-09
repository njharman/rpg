#!/usr/bin/python
'''Armor class vs shield save experiments.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain.
Website: http://trollandflame.blogspot.com/
'''

from dice import *


def hitcha(count, AC, tohit, bonus):
    '''AC + tohit + d20 >= 20 = hit
    xdlucky comes up number = save where x = bonus
    '''
    lucky10 = d10()
    lucky20 = d20()
    AB = AC - bonus
    hitab = 0
    hitac = 0
    hit10 = 0
    hit20 = 0
    sav10 = 0
    sav20 = 0
    for i in range(count):
        roll = d20()
        if roll + tohit + AC >= 20:
            hitac += 1
            if lucky10 in [d10() for i in range(bonus)]:
                sav10 += 1
            else:
                hit10 += 1
            if lucky20 in [d20() for i in range(bonus)]:
                sav20 += 1
            else:
                hit20 += 1
        if roll + tohit + AB >= 20:
            hitab += 1
    total = float(count / 100)
    sotal = float(hitac / 100)
    return dict(count=count, tohit=tohit, bonus=bonus,
                ac=AC,
                ab=AB,
                hitab=hitab, hab_p=hitab / total,
                hitac=hitac, hac_p=hitac / total,
                hit10=hit10, h10_p=hit10 / total,
                hit20=hit20, h20_p=hit20 / total,
                sav10=sav10, s10_p=sav10 / sotal,
                sav20=sav20, s20_p=sav20 / sotal,
                diff10_p=(hitab / total) - (hit10 / total),
                diff20_p=(hitab / total) - (hit20 / total),
               )


def oneser(stats):
    print '{count}: hit AC {ab} {hitab:6} {hab_p:5.2f}%'.format(**stats)
    print '{count}: hit AC {ac} {hitac:6} {hac_p:5.2f}%'.format(**stats)
    print '{0:{1}}: difference      {diff_p:5.2f}%'.format(' ', len(str(stats['count'])), **stats)
    print '{count}: sav10    {sav10:6} {s10_p:5.2f}%'.format(**stats)


def ac_rangefull(count, tohit, bonus):
    print '{count} iterations of +{tohit} tohit vs +{bonus} todef.'.format(count=count, tohit=tohit, bonus=bonus)
    print '     modifying AC  |    d10 save(s)      diff |'
    for armor in range(10, 1, -1):
        stats = hitcha(count, armor, tohit, bonus)
        print 'AC {ab:2} {hitab}/{hab_p:.2f}% | AC {ac:2} {hit10}/{h10_p:.2f}% {diff10_p:5.2f}% | sav10 {sav10}/{s10_p:5.2f}% sav20 {sav20}/{s20_p:5.2f}% of {hitac} |'.format(**stats)


def ac_range(count, tohit, bonus):
    print '{count} iterations of +{tohit} tohit vs +{bonus} to AC or {bonus}d10 save rolls.'.format(count=count, tohit=tohit, bonus=bonus)
    print 'hit w/ bonus | hit w/ saves |  diff  |'
    for armor in range(10, 1, -2):
        stats = hitcha(count, armor, tohit, bonus)
        print 'AC {ab:2} {hab_p:5.2f}% | AC {ac:2} {h10_p:5.2f}% | {diff10_p:5.2f}% |'.format(**stats)


if __name__ == '__main__':
    count = 10000
    armor = 4
    tohit = 5
    lucky = d20
    for bonus in range(1, 8):
        ac_range(count, tohit, bonus)
        print

#    for tohit in range(1,10):
#        for bonus in range(1, 4):
#            ac_range(count, tohit, bonus)
#            print
#        print
