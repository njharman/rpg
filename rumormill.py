"""Rumor Mill, generates random rumors from a list of parts.

Usage: python rumormill.py parts.py [count]

count  - how many rumors to generate, default is 10.
parts.py  - should by Python source with parts dictionary of lists defined like this:

parts = {'Who': [], 'What': [], 'When': [], 'Where': [], 'Why': [], 'How': []}
"""

import sys
import random


def rumor(parts):
  """parts: dict name -> list"""
  rumor = list()
  count = random.randint(2, len(parts))
  for part in random.sample(parts.keys(), count):
      rumor.append(f'{part}:  {random.choice(parts[part])}')
  return ', '.join(rumor)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        count = int(sys.argv[2])
    else:
        count = 10
    execfile(sys.argv[1], globals())
    for i in range(count):
        print rumor(parts), '\n'
