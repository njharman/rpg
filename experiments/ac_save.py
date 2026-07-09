#!/usr/bin/python
"""Armor class vs shield save experiments.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: http://trollandflame.blogspot.com/
"""

from dice import d10, d20


def hitcha(count, AC, tohit, bonus):
    """AC + tohit + d20 >= 20 = hit
    xdlucky comes up number = save where x = bonus
    """
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
    print(f"{stats['count']}: hit AC {stats['ab']} {stats['hitab']:6} {stats['hab_p']:5.2f}%")
    print(f"{stats['count']}: hit AC {stats['ac']} {stats['hitac']:6} {stats['hac_p']:5.2f}%")
    print(f"{' ':{len(str(stats['count']))}}: difference      {stats['diff_p']:5.2f}%")
    print(f"{stats['count']}: sav10    {stats['sav10']:6} {stats['s10_p']:5.2f}%")


def ac_rangefull(count, tohit, bonus):
    print(f'{count} iterations of +{tohit} tohit vs +{bonus} todef.')
    print('     modifying AC  |    d10 save(s)      diff |')
    for armor in range(10, 1, -1):
        stats = hitcha(count, armor, tohit, bonus)
        print(
            f"AC {stats['ab']:2} {stats['hitab']}/{stats['hab_p']:.2f}% | "
            f"AC {stats['ac']:2} {stats['hit10']}/{stats['h10_p']:.2f}% {stats['diff10_p']:5.2f}% | "
            f"sav10 {stats['sav10']}/{stats['s10_p']:5.2f}% "
            f"sav20 {stats['sav20']}/{stats['s20_p']:5.2f}% of {stats['hitac']} |",
        )


def ac_range(count, tohit, bonus):
    print(f'{count} iterations of +{tohit} tohit vs +{bonus} to AC or {bonus}d10 save rolls.')
    print('hit w/ bonus | hit w/ saves |  diff  |')
    for armor in range(10, 1, -2):
        stats = hitcha(count, armor, tohit, bonus)
        print(
            f"AC {stats['ab']:2} {stats['hab_p']:5.2f}% | "
            f"AC {stats['ac']:2} {stats['h10_p']:5.2f}% | {stats['diff10_p']:5.2f}% |",
        )


if __name__ == '__main__':
    count = 10000
    armor = 4
    tohit = 5
    for bonus in range(1, 8):
        ac_range(count, tohit, bonus)
        print()

#    for tohit in range(1,10):
#        for bonus in range(1, 4):
#            ac_range(count, tohit, bonus)
#            print
#        print
