"""From  Dragon #9 "Tombs & Crypts" by James M. Ward

The mystery, challenge and pleasure of any wargamer in discover- ing and opening a tomb of some unknown being is well
known to those that have done it. The creation of these tombs can be a very drawn out, head scratching process for the
judge. I have created a set of graphs to ease this creation process.

First roll a 12 sided die to see what is buried in the tomb. Then roll for each of the 9 items using the charts given
below. For each item check the row to add, subtract, or leave alone the resulting percentile roll. When going over the
possible 100% total just assume that you rolled a 100 and roll again without the bonus given for the person in the tomb.
If the number rolled totals less than 0% just assume you have a 01% roll.

The pair Factor stands for more than one being buried in the tomb, for example: 2 brave fighters that killed each other in battle.
The mated pair stands for a husband and wife type tomb not necessarily a human type.
The being refers to a intelligent creature whose followers thought enough of it to place it in a special crypt of honor.

1. Soldier, 2. Hero, 3. Priest, 4. Pair, 5. Mated. Pair, 6. Lord, 7. King, 8. Patriarch, 9. EHP, 10. Magic User, 11. Wiz- ard, 12. Being

              1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12.
Gold Pieces   - 15 20 25 20 25 20 25 20 25 30 45
Gems          10 15 20 25 40 30 35 40 45 20 40 45
Maps          - - 5 5 5 10 20 25 10 - 30 40
Jewelry       -10 -5 - 10 15 25 10 5 5 20 30 40
Magic Item    -15 -5 -5 - - 5 15 10 10 10 15 20
Misc. M. Item -30 -20 -15 -15 -20 -10 - -5 -5 - 5 10
Special Item  -14 -12 -11 -10 -9 - 5 - -5 - - 5
Artifact       No No No No - -9 -5 -4 -4 No - 5
Tomb Itself   -50 -40 -40 -10 -9 -9 -1 -1 -1 -30 30 45
Guardian      -31 -25 -25 -20 -20 - 10 10 - -20 30 40

Gold Pieces
    1-50% 1-100 pieces
    51-60 1-100(x2)
    61-70 1-6 Thousand
    71-80 1-12 Thousand
    81-90 1-20 Thousand
    91-99 2-40 Thousand
    100 100,00 Thousand

Magic Item
    1-50% None
    51-60 Sword
    61-70 Armor
    71-80 Misc. Weapon
    81-90 1-6 Potions
    91-99 Ring
    100 Good Misc. Magic item

Maps
    1-80% None
    81-100 Judges option as to what map contains.

Gems
    1-50% 1-6 base 100
    51-60 1-6 base 500
    61-70 1-8 base 500
    71-80 1-12 base 500
    81-90 1-12 base 1,000 81-90
    91-99 1-6 base 5,000
    100   1-20 base 10,000

Jewelry
    1-50% 1-6 base 500
    51-60 1-6 base 1,000
    61-70 1-6 base 5,000
    71-80 1-6 base 10,000
    81-90 1-6 base 20,000
    91-99 1-6 base 30,000
    100   1-20 base 50,000

Misc. Magic item
    1-60% None
    61-70 Table I of Greyhawk
    71-80 Table II of Greyhawk
    81-90 Table III of Greyhawk
    91-99 Table IV of Greyhawk
    100   Table V of Greyhawk

Special Item
    1-85% None
    86-100 Any item of the judges own manufacture.

Guardian
    1-30% None
    31-50 Magic spell (wizard lock, curse, etc.)
    51-80 Invisible stalker(s) 1-4
    81-99 Creature from the 6 level monster chart
    100 A stronger monster in the tomb and roll again for another guard.

Artifact
    1-90% None
    91-100 A judge made object of great power

Tomb Itself
    1-40% 1 room/cave/mound of dirt
    41-50 Hall with spring trap of some type and a secret door at the end of it.
    51-60 2-6 room/cave complex with many doors leading to other areas trying to lure the robbers away.
    61-80 1-10 rooms/caves with a secret door to the tomb and 1-10 traps in the rooms.
    81-90 1-10 rooms with 1-20 corridors, with 2-20 traps guarding the rooms and tombs and a secret door.
    91-99 1-10 connecting rooms with traps, secret doors, and magical guard spells (wiz- ard locks, symbols, etc,) guarding the way.
    100   1-20 rooms with traps, secret doors, and a being guard. It requires special word to open the final door to the tomb. The word should not be found in the tomb.
"""

import random

TYPES = [
    "Soldier", "Hero", "Priest", "Pair", "Mated Pair",
    "Lord", "King", "Patriarch", "EHP", "Magic User", "Wizard", "Being",
]

# Modifier per tomb type (index 0-11). None = category not possible.
MODS = {
    #               Sol  Her  Pri  Pai  MPa  Lor  Kin  Pat  EHP   MU  Wiz  Bei
    "gold":       [   0,  15,  20,  25,  20,  25,  20,  25,  20,  25,  30,  45],
    "gems":       [  10,  15,  20,  25,  40,  30,  35,  40,  45,  20,  40,  45],
    "maps":       [   0,   0,   5,   5,   5,  10,  20,  25,  10,   0,  30,  40],
    "jewelry":    [ -10,  -5,   0,  10,  15,  25,  10,   5,   5,  20,  30,  40],
    "magic":      [ -15,  -5,  -5,   0,   0,   5,  15,  10,  10,  10,  15,  20],
    "misc_magic": [ -30, -20, -15, -15, -20, -10,   0,  -5,  -5,   0,   5,  10],
    "special":    [ -14, -12, -11, -10,  -9,   0,   5,   0,  -5,   0,   0,   5],
    "artifact":   [None,None,None,None,   0,  -9,  -5,  -4,  -4,None,   0,   5],
    "tomb":       [ -50, -40, -40, -10,  -9,  -9,  -1,  -1,  -1, -30,  30,  45],
    "guardian":   [ -31, -25, -25, -20, -20,   0,  10,  10,   0, -20,  30,  40],
}


def d(n):
    """Random die of n sides, 1 to n."""
    return random.randint(1, n)


def percent(modifier):
    """Roll d100 + modifier. Returns (result, extra) where extra is an unmodified d100 roll if result exceeded 100."""
    raw = d(100) + modifier
    if raw > 100:
        return 100, d(100)
    return max(1, raw), None


def gen_gold(roll):
    if roll <= 50: return f"{d(100)} gp"
    if roll <= 60: return f"{d(100) * 2} gp"
    if roll <= 70: return f"{d(6) * 1000:,} gp"
    if roll <= 80: return f"{d(12) * 1000:,} gp"
    if roll <= 90: return f"{d(20) * 1000:,} gp"
    if roll <= 99: return f"{random.randint(2, 40) * 1000:,} gp"
    return "100,000 gp"


def gen_gems(roll):
    if roll <= 50: return f"{d(6)} gems (base 100 gp)"
    if roll <= 60: return f"{d(6)} gems (base 500 gp)"
    if roll <= 70: return f"{d(8)} gems (base 500 gp)"
    if roll <= 80: return f"{d(12)} gems (base 500 gp)"
    if roll <= 90: return f"{d(12)} gems (base 1,000 gp)"
    if roll <= 99: return f"{d(6)} gems (base 5,000 gp)"
    return f"{d(12)} gems (base 5,000 gp)"  # change base from 10,000 and number from d20


def gen_maps(roll):
    return "None" if roll <= 80 else "Map (referee's option)"


def gen_jewelry(roll):
    if roll <= 50: return f"{d(6)} jewelry (base 500 gp)"
    if roll <= 60: return f"{d(6)} jewelry (base 1,000 gp)"
    if roll <= 70: return f"{d(6)} jewelry (base 5,000 gp)"
    if roll <= 80: return f"{d(6)} jewelry (base 10,000 gp)"
    if roll <= 90: return f"{d(6)} jewelry (base 20,000 gp)"
    if roll <= 99: return f"{d(6)} jewelry (base 30,000 gp)"
    return f"{d(20)} jewelry (base 50,000 gp)"


def gen_magic(roll):
    if roll <= 50: return "None"
    if roll <= 60: return "Sword"
    if roll <= 70: return "Armor"
    if roll <= 80: return "Misc. Weapon"
    if roll <= 90: return f"{d(6)} Potion(s)"
    if roll <= 99: return "Ring"
    return "Good Misc. Magic Item"


def gen_misc_magic(roll):
    if roll <= 60: return "None"
    if roll <= 70: return "Greyhawk Misc. Magic Table I"
    if roll <= 80: return "Greyhawk Misc. Magic Table II"
    if roll <= 90: return "Greyhawk Misc. Magic Table III"
    if roll <= 99: return "Greyhawk Misc. Magic Table IV"
    return "Greyhawk Misc. Magic Table V"


def gen_special(roll):
    return "None" if roll <= 85 else "Special Item (referee's manufacture)"


def gen_artifact(roll):
    return "None" if roll <= 90 else "Artifact"


def gen_tomb(roll):
    if roll <= 40: return "1 room/cave/mound"
    if roll <= 50: return "Hall with spring trap + secret door at end"
    if roll <= 60: return f"{d(5) + 1} room/cave complex, many misleading doors"
    if roll <= 80: return f"{d(10)} rooms/caves, secret door to tomb, {d(10)} traps"
    if roll <= 90: return f"{d(10)} rooms, {d(20)} corridors, {d(19) + 1} traps, secret door"
    if roll <= 99: return f"{d(10)} rooms with traps, secret doors, and magical guard spells"
    return f"{d(20)} rooms with traps, secret doors, being guard; special word opens final door"


def gen_guardian(roll, depth=0):
    if roll <= 30: return "None"
    if roll <= 50: return "Magic spell (wizard lock, curse, etc.)"
    if roll <= 80: return f"{d(4)} Invisible Stalker(s)"
    if roll <= 99: return "Monster from 6th level chart"
    extra = gen_guardian(d(100), depth + 1) if depth < 3 else "additional guard (referee's choice)"
    return f"Powerful monster + {extra}"


CATEGORIES = [
    ("Gold",        "gold",       gen_gold),
    ("Gems",        "gems",       gen_gems),
    ("Maps",        "maps",       gen_maps),
    ("Jewelry",     "jewelry",    gen_jewelry),
    ("Magic Item",  "magic",      gen_magic),
    ("Misc. Magic", "misc_magic", gen_misc_magic),
    ("Special",     "special",    gen_special),
    ("Artifact",    "artifact",   gen_artifact),
    ("Tomb",        "tomb",       gen_tomb),
    ("Guardian",    "guardian",   gen_guardian),
]


def generate():
    type_idx = d(12) - 1
    print(f"Tomb Type: {TYPES[type_idx]}\n")
    for label, mod_key, gen_fn in CATEGORIES:
        modifier = MODS[mod_key][type_idx]
        if modifier is not None:
            roll, extra = percent(modifier)
            result = gen_fn(roll)
            if result == "None":
                continue
            if extra is not None:
                extra_result = gen_fn(extra)
                if extra_result != "None":
                    result += f", {extra_result}"
            print(f"  {label:<12}: {result}")


if __name__ == "__main__":
    generate()
