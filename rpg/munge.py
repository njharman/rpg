#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Fix ascii in pdf -> txt converted files.'''

import sys


if __name__ == '__main__':
    files = sys.argv[1:]
    for file in files:
        old = open(file)
        lines = old.readlines()
        old.close()
        new = open(file, 'w')
        for line in lines:
            line = line.replace('–', '-')
            line = line.replace('’', "'")
            line = line.replace('mêlée', 'melee')
            new.write(line)
        new.close()

