#!/usr/bin/env python
import sys

from rpg.munge import replace_typography


if __name__ == '__main__':
    file = open(sys.argv[1])
    for line in replace_typography(file):
        sys.stdout.write(line)
