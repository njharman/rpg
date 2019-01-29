#!/usr/bin/python
import random
import sys
import locale

"""
Find average values for each LBB D&D treasure type. It doesn't include magic or maps.

Paul Gorman (http://quicklyquietlycarefully.blogspot.com/)
10 August 2012
"""

numberOfRuns = 6000 # Set to whatever. Higher gives more accurate averages.
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

allGems = [] # Values of all rolled gems, for later averaging
allJewelry = [] # Values of all rolled gems, for later averaging

def median(a):
    sortedArray = sorted(a)
    aLength = len(sortedArray)
    return 0.5 * ( sortedArray[(aLength - 1)//2] + sortedArray[aLength//2])

def mode(values):
    return max(set(values), key=values.count)

def gem():
    # Returns the value of a gem in gold pieces
    valueLevels = [10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000, 100000, 500000]
    valueIndex = 0
    d100 = random.randint(1,100)
    if d100 <= 10:
        valueIndex = 0
    elif d100 <= 25:
        valueIndex = 1
    elif d100 <= 75:
        valueIndex = 2
    elif d100 <= 90:
        valueIndex = 3
    else:
        valueIndex = 4
    while random.randint(1,6) == 1 and valueIndex < (len(valueLevels) - 1):
        valueIndex += 1
    allGems.append(valueLevels[valueIndex])
    return valueLevels[valueIndex]

def jewelry():
    # Returns the value of a piece of jewelry in gold pieces
    value = 0
    d100 = random.randint(1,100)
    if d100 <= 20:
        value = (
            random.randint(1,6)
            + random.randint(1,6)
            + random.randint(1,6)) * 100
    elif d100 <= 80:
        value = random.randint(1,6) * 1000
    else:
        value = random.randint(1,10) * 1000
    allJewelry.append(value)
    return value

def calcTreasure(treasureType, copperRolls, copperDie, copperOdds, silverRolls, silverDie, silverOdds, goldRolls, goldDie, goldOdds, gemRolls, gemDie, gemOdds, jewelryRolls, jewelryDie, jewelryOdds):
    treasure = {}
    treasure['type'] = treasureType
    treasure['copper'] = 0
    treasure['silver'] = 0
    treasure['gold'] = 0
    treasure['gems'] = 0
    treasure['jewelry'] = 0
    treasure['total'] = 0
    if (random.randint(1,100) <= copperOdds): # Copper in gold pieces
        for n in range(copperRolls):
            treasure['copper'] = treasure['copper'] \
                + ((random.randint(1,copperDie) * 1000)/50)
        treasure['total'] = treasure['total'] + treasure['copper']
    if (random.randint(1,100) <= silverOdds): # Silver in gold pieces
        for n in range(silverRolls):
            treasure['silver'] = treasure['silver'] \
                + ((random.randint(1,silverDie) * 1000)/10)
        treasure['total'] = treasure['total'] + treasure['silver']
    if (random.randint(1,100) <= goldOdds): # Gold pieces
        for n in range(goldRolls):
            treasure['gold'] = treasure['gold'] \
                + (random.randint(1,goldDie) * 1000)
        treasure['total'] = treasure['total'] + treasure['gold']
    if (random.randint(1,100) <= gemOdds): # Gems
        numberOfGems = 0
        for n in range(gemRolls):
            numberOfGems = numberOfGems + random.randint(1,gemDie)
        for n in range(numberOfGems):
            treasure['gems'] = treasure['gems'] + gem()
        treasure['total'] = treasure['total'] + treasure['gems']
    if (random.randint(1,100) <= jewelryOdds): # Jewelry
        numberOfJewelry = 0
        for n in range(jewelryRolls):
            numberOfJewelry = numberOfJewelry + random.randint(1,jewelryDie)
        for n in range(numberOfJewelry):
            treasure['jewelry'] = treasure['jewelry'] + jewelry()
        treasure['total'] = treasure['total'] + treasure['jewelry']
    return treasure

treasureTypes = [
    ['A Land', 1, 6, 25, 1, 6, 30, 2, 6, 35, 6, 6, 50, 6, 6, 50],
    ['A Dsrt', 1, 4, 20, 1, 4, 25, 1, 6, 30, 10, 4, 50, 10, 4, 50],
    ['A Wtr', 0, 0, 0, 0, 0, 0, 5, 6, 60, 10, 6, 60, 10, 6, 60],
    ['B ', 1, 8, 50, 1, 6, 25, 1, 3, 25, 1, 6, 25, 1, 6, 25],
    ['C ', 1, 12, 20, 1, 4, 30, 0, 0, 0, 1, 4, 25, 1, 4, 25],
    ['D ', 1, 8, 10, 1, 12, 15, 1, 6, 60, 1, 8, 30, 1, 8, 30],
    ['E ', 1, 10, 5, 1, 12, 30, 1, 8, 25, 1, 10, 10, 1, 10, 10],
    ['F ', 0, 0, 0, 2, 10, 10, 1, 12, 45, 2, 12, 20, 2, 12, 20],
    ['G ', 0, 0, 0, 0, 0, 0, 10, 4, 75, 3, 6, 25, 1, 10, 25],
    ['H ', 3, 8, 25, 1, 100, 50, 10, 6, 75, 1, 100, 50, 4, 10, 50],
    ['I ', 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 50, 2, 8, 50]
]

def testGems():
    gems = []
    for n in range(numberOfRuns):
        g = gem()
        if g >= 10 and g <= 500000: # Expected
            gems.append(gem())
        else:
            return "Error, unexpected gem value: " + str(g)
    return (sum(gems) / len(gems))

def testJewelry():
    jewelries = []
    for n in range(numberOfRuns):
        j = jewelry()
        if j >= 300 and j <= 10000: # Expected
            jewelries.append(jewelry())
        else:
            return "Error, unexpected jewelry value: " + str(j)
    return (sum(jewelries) / len(jewelries))

def reportTreasureTypes():
    print 'ODnD Treasure Type Values: Minimum > 0 / Average / Maximum'
    print '----------------------------------------------------------'
    for t in treasureTypes:
        hoards = []
        for n in range(numberOfRuns):
            hoards.append(calcTreasure(*t))
        totals = []
        for h in hoards:
            totals.append(h['total'])
        totals.sort()
        minimum = 0
        for total in totals:
            if total != 0:
                minimum = total
                break
        average = (sum(totals) / len(totals))
        print t[0] + '\t' \
            + str(locale.format("%d", minimum, grouping=True)) + ' gp\t ' \
            + str(locale.format("%d", average, grouping=True)) + ' gp\t ' \
            + str(locale.format("%d", max(totals), grouping=True)) + ' gp'
    print '(Actual values from ' \
        + str(locale.format("%d", numberOfRuns, grouping=True)) + ' rolls.)'

def reportDetails():
    print 'ODnD Treasure Type Values (All values show in gold pieces)'
    print 'Type\tCopper\tSilver\tGold\tGems\tJewelry\tTotal'
    print '----------------------------------------------------------'
    for t in treasureTypes:
        hoards = []
        for n in range(numberOfRuns):
            hoards.append(calcTreasure(*t))
        avgCopper = (sum([h['copper'] for h in hoards]) / len(hoards))
        avgSilver = (sum([h['silver'] for h in hoards]) / len(hoards))
        avgGold = (sum([h['gold'] for h in hoards]) / len(hoards))
        avgGems = (sum([h['gems'] for h in hoards]) / len(hoards))
        avgJewelry = (sum([h['jewelry'] for h in hoards]) / len(hoards))
        avgTotal = (sum([h['total'] for h in hoards]) / len(hoards))
        print t[0] + ' \t' + str(locale.format("%d", avgCopper, grouping=True)) \
            + ' \t' + str(locale.format("%d", avgSilver, grouping=True)) \
            + ' \t' + str(locale.format("%d", avgGold, grouping=True)) \
            + ' \t' + str(locale.format("%d", avgGems, grouping=True)) \
            + ' \t' + str(locale.format("%d", avgJewelry, grouping=True)) \
            + ' \t' + str(locale.format("%d", avgTotal, grouping=True))
    print '(Values averaged from ' \
        + str(locale.format("%d", numberOfRuns, grouping=True)) + ' rolls.)'

#reportTreasureTypes()
reportDetails()

print 'Average (Mean) Gem: ' + \
    str(locale.format("%d", (sum(allGems) / len(allGems)), grouping=True))
print 'Average (Median) Gem: ' + \
    str(locale.format("%d", median(allGems), grouping=True))
print 'Average (Mode) Gem: ' + \
    str(locale.format("%d", mode(allGems), grouping=True))
print 'Average (Mean) Jewelry: ' + \
    str(locale.format("%d", (sum(allJewelry) / len(allJewelry)), grouping=True))
print 'Average (Median) Jewelry: ' + \
    str(locale.format("%d", median(allJewelry), grouping=True))
print 'Average (Mode) Jewelry: ' + \
    str(locale.format("%d", mode(allJewelry), grouping=True))
