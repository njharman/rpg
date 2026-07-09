#!/usr/bin/env python3
"""Generate ReStructuredText chart of hit die rolls.

Redirect to file, rst2pdf, print. And Bam! Bunch of grouped monster hit points
easily marked off during play.

Rolls d6+2, prints 8 pages.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Oct 2012.
Website: http://trollandflame.blogspot.com/
"""

import random


def hp_line(columns, template):
    """Line of hit points."""
    bits = []
    bits.append(template % '\\')
    for _ in range(1, columns):
        hits = random.randint(3, 8)
        bits.append(template % ('O' * hits))
    return ''.join(bits)


def ac_line(columns, template):
    """Line of armor class."""
    bits = []
    bits.append(template % 'AC \\___')
    for _ in range(1, columns):
        bits.append(template % 'O O O O O X /')
    bits.append('\n')
    bits.append(template % '')
    for _ in range(1, columns):
        bits.append(template % 'O O O O O X')
    return ''.join(bits)


def page(columns, page_length, page_width):
    """One page."""
    column = page_width // columns
    table = ' '.join(['=' * column] * columns)
    template = '%%-%is' % (column + 1)  # noqa: UP031
    print('Notes:\n')
    print(table)
    for _ in range(6):
        print(ac_line(columns, template))
    for _ in range(page_length - 6):
        print(hp_line(columns, template))
    print(table)


for _ in range(8):
    page(4, 40, 80)
    print()
