#!/usr/bin/python
"""No idea.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: http://trollandflame.blogspot.com/
"""

from collections import defaultdict

from dice import d6, d20


def stat_testor(count, func):
    results = list()
    for stat in range(3, 19, 3):
        winnar = 0
        for _ in range(count):
            if func(stat):
                winnar += 1
        results.append({'chance': stat, 'count': count, 'win': winnar, 'percent': ((winnar * 100.0) / count)})
    return results


def x_in_d6_calculated():
    results = list()
    for chance in range(1, 6):
        results.append({'chance': f'1-{chance}', 'count': 0, 'win': 'na', 'percent': ((chance * 100.0) / 6)})
    return results


def x_in_d6_multiple_d6(count):
    # test if 1, 2, 3 rolls of d6 are within chance
    results = list()
    for chance in range(1, 6):
        one = two = tre = 0
        pants = range(1, chance + 1)
        for _ in range(count):
            if d6() in pants:
                one += 1
                two += 1
                tre += 1
            elif d6() in pants:
                two += 1
                tre += 1
            elif d6() in pants:
                tre += 1
        data = {'chance': f'1-{chance}', 'count': count, 'one': one, 'onep': (one * 100.0) / count, 'two': two, 'twop': (two * 100.0) / count, 'tre': tre, 'trep': (tre * 100.0) / count}
        results.append(
            f"{data['chance']:3}  {data['one']} / {data['onep']:.4}%  "
            f"{data['two']} / {data['twop']:.4}%  {data['tre']} / {data['trep']:.4}%",
        )
    return '\n'.join(results)


def format_results(results):
    result = list()
    result.append('stat sucessess')
    for data in results:
        result.append(f"{data['chance']:3}  {data['win']} / {data['percent']:.4}%")
    return '\n'.join(result)


def rolld6():
    count = 10000
    print(f"|    | {' | '.join(f'{i:^5}' for i in range(11))} |")
    for times in range(1, 11):
        results = defaultdict(int)
        for _ in range(count):
            asix = 0
            for _ in range(times):
                roll = d6()
                if roll == 6:
                    asix += 1
            results[asix] += 1
        print(f"| {times:<2} | {' | '.join(f'{(results.get(i, 0) * 100.0) / count:5.2f}' for i in range(11))} |")


if __name__ == '__main__':
    count = 100000
    print('\nx in d6 chance: calculated')
    print(format_results(x_in_d6_calculated()))
    print(f'\nx in d6 chance: {count} iterations')
    print('chance  1d6          2d6          3d6')
    print(x_in_d6_multiple_d6(count))
    print(f'\nd20 + stat >= 20: {count} iterations')
    print(format_results(stat_testor(count, lambda stat: stat + d20() >= 20)))
    print(f'\nd20 + stat > 20: {count} iterations')
    print(format_results(stat_testor(count, lambda stat: stat + d20() > 20)))
    print(f'\nd20 <= stat: {count} iterations')
    print(format_results(stat_testor(count, lambda stat: d20() <= stat)))
