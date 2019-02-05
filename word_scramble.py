#!/usr/bin/env python
'''Simple word scrambler.'''

import random


def fuxate(text):
    '''Split text into two lists, vowels and consonants.'''
    vowels = list()
    consts = list()
    for letter in text:
        if letter in 'aeiou':
            vowels.append(letter)
        else:
            consts.append(letter)
    return vowels, consts


def progmulagate(v, c):
    '''Alternate consonants and vowels.'''
    vowels = list(v)
    consts = list(c)
    random.shuffle(vowels)
    random.shuffle(consts)
    word = list()
    if 1 == random.randint(1, 3):
        word.append(vowels.pop())
    for letter in consts:
        word.append(letter)
        if vowels and 1 != random.randint(1, 4):
            word.append(vowels.pop())
    return ''.join(word)


def simple(text):
    '''Pure jumble.'''
    word = list(text)
    random.shuffle(word)
    return ''.join(word)


if __name__ == '__main__':
    import sys
    text = sys.argv[1]
    vowels, consts = fuxate(text)

    for x in range(5):
        print(simple(text))

    for x in range(10):
        print(progmulagate(vowels, consts))
