#!/usr/bin/env python
'''Generate ReStructuredText chart of hit die rolls.

Redirect to file, rst2pdf, print and bunch of monster hitdice easily grouped and
marked off during play.

Rolls d6+2, prints 8 pages.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Oct 2012.
Website: http://trollandflame.blogspot.com/
'''

import random


def line(columns, template):
    bits = list()
    for col in range(1, columns + 1):
        hits = random.randint(3, 8)
        bits.append(template % ('O' * hits))
    return ''.join(bits)


def page(columns, page_length, page_width):
    column = page_width / columns
    table = ' '.join(['=' * column] * columns)
    template = '%%%is' % (page_width / columns)

    print 'Notes:\n'
    print table
    for i in range(page_length):
        print line(columns, template)
    print table

for i in range(8):
    page(4, 40, 80)
    print
