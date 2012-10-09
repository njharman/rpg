#!/usr/bin/env python
'''Generate ReStructuredText calendar.

Use rst2pdf to create PDF.

Tuned for my personal home Gold and Glory campaign.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Oct 2012.
Website: http://trollandflame.blogspot.com/
'''

import random
from collections import namedtuple, deque


class Weather(object):
    def __init__(self, temps):
        self.temps = temps
        self._idx = None
        self._past_temp = deque([None] * 4)  # four position ring buffer
        self._raining = False
        self._rain_chance = 0

    def _calc_temp(self, avg_idx):
        def normalize(avg, idx):
            length = len(self.temps)
            # Keep in range of our temps array.  Not too far from avg.
            mymin = max(0, avg - 2)  # (length / 2))
            mymax = min(length - 1, avg + 2)  # (length / 2))
            new = min(mymax, max(mymin, idx))
            # Also, increasing chance to back off from extremes.
            if new == mymin or new == mymax:
                cum = 0
                for i in range(len(self._past_temp)):
                    if new == self._past_temp[i]:
                        cum += 1
                if random.randint(0, len(self._past_temp)) < cum:
                    new += cmp(1, new)
            return new

        def front(past, direction):
            'Cold or Hot front.'
            # Chance of jumping > 1 temp.
            delta = direction * random.choice((1, 1, 1, 1, 1, 2, 2, 3))
            value = past + delta
            return value

        def to_avg(avg):
            'Move temp to average.'
            past = self._past_temp[0]
            direction = cmp(avg, past)
            return front(past, direction)

        def to_trend(avg):
            'Continue temp trend from past.'
            past = self._past_temp[0]
            directions = list()
            for temp in self._past_temp:
                directions.append(cmp(past, temp))
            # Perturb if stable weather.
            if sum(abs(t) for t in directions) == 0:
                directions = (-1, 1)
            return front(past, random.choice(directions))
        # One time prep of ring buffer.
        while self._past_temp[0] is None:
            self._past_temp[0] = avg_idx
            self._past_temp.rotate(1)
        # If past weather was not avg, increase trend chance.
        if avg_idx == self._past_temp[0]:
            forcast = (to_avg, to_avg, to_trend)
        else:
            forcast = (to_avg, to_trend, to_trend)
        self._idx = normalize(avg_idx, random.choice(forcast)(avg_idx))
        self._past_temp.rotate(1)
        self._past_temp[0] = self._idx
        self.temp = self.temps[self._idx]

    def _calc_rain(self, season, temp):
        '''Percipitation per "watch".'''
        self.rain = list()
        self._rain_chance += season.chance
        if self._raining:
            self._rain_chance += season.chance
            self._raining = False
        chance = self._rain_chance
        for i in range(4):
            roll = random.randint(1, 100)
            if roll == 100:
                rain = '**%s**' % random.choice(season.freak)
            if roll <= chance:
                chance += 10
                self._raining = True
                rain = '*%s*' % random.choice(season.rain[temp])
            else:
                rain = ''
            self.rain.append(rain)
        if not self._raining or self._rain_chance > 80:
            self._rain_chance = 0

    def forcast(self, season, avg):
        self.bits = list()
        avg_idx = self.temps.index(avg)
        self._calc_temp(avg_idx)
        self._calc_rain(season, self.temp)


class Calendar(object):
    def __init__(self, month_data, weather, lunar_cycle):
        self.months = month_data
        self.weather = weather
        self.lunar_cycle = lunar_cycle
        self.day = 1
        self._month = self.months[0]
        self.length_of_year = sum(m.length for m in self.months.values())
        self._lunar_meteors = False

    @property
    def day_of_year(self):
        day = 0
        for month in self.months.values():
            if month == self._month:
                break
            day += month.length
        day += self.day
        return day

    @property
    def moon_phase(self):
        '''Moon phase.
        Starts with new moon on the (cycle/4)th day of year 1.
        Real moon cycle is complicated, this is good enough for fantasy.
        '''
        # ('new', 'waxing crescent', 'first quarter', 'waxing gibbous', 'full ', 'waning gibbous', 'third quarter', 'waning crescent')
        days = (self.year * self.length_of_year) + self.day_of_year
        day = (days % self.lunar_cycle) + 1
        if day == self.lunar_cycle / 4:
            if day == (days % ((self.lunar_cycle * 4) + 3)) + 1 and random.choice((True, False)):
                return 'solar'
            return 'new'
        if day == (self.lunar_cycle / 4) * 2:
            return '1st'
        if day == (self.lunar_cycle / 4) * 3:
            if day == (days % ((self.lunar_cycle * 5) + 4)) + 1 and random.choice((True, False, False)):
                return 'lunar'
            return 'full'
        if day == self.lunar_cycle:
            return '3rd'
        return ''

    @property
    def moon_shower(self):
        '''Moon is "broken", chance around new moon of moon meteor shower.
        '''
        days = (self.year * self.length_of_year) + self.day_of_year
        day = (days % self.lunar_cycle) + 1
        new = self.lunar_cycle / 4
        near = range(new - 2, new + 3)  # 2 days before and after new moon.
        try:
            chance = (3, 9, 27, 9, 3)[near.index(day)]
            if self._lunar_meteors:
                chance *= 6
            if chance >= random.randint(1, 100):
                self._lunar_meteors = True
                return 'lunar meteors'
        except ValueError:
            self._lunar_meteors = False
        return ''

    def a_day(self):
        '''Return dictionary of values for day.'''
        self.weather.forcast(self._month.season, self._month.temp)
        return Day(
                self.day,
                self._month.name,
                self.year,
                self.weather.temp,
                self.weather.rain,
                self.moon_phase,
                self.moon_shower,
                )

    def a_month(self):
        '''Generates each day for current month.'''
        for i in range(1, self._month.length + 1):
            self.day = i
            yield self.a_day()

    def a_year(self, year):
        '''Generates one year's worth of month generators.'''
        self.year = year
        for i in range(len(self.months)):
            self._month = self.months[i]
            self.month = self._month.name
            yield self.a_month


temperatures = (
        'froz',
        'cold',
        'cool',
        'mild',
        'warm',
        'hot',
        'boil',
        )

Season = namedtuple('Season', ['chance', 'rain', 'freak'])
spring = Season(
        10,
        {
        'froz': ('sleet', 'flury', ),
        'cold': ('sleet', ),
        'cool': ('driz', 'rain'),
        'mild': ('driz', 'rain', 'storm'),
        'warm': ('driz', 'rain', 'storm'),
         'hot': ('driz', 'rain', 'storm', 'storm'),
        'boil': ('driz', 'rain', 'storm', 'storm'),
        },
        ('hailstorm',),
        )
summer = Season(
        3,
        {
        'froz': ('fluries', 'snow'),
        'cold': ('sleet', 'driz', 'rain'),
        'cool': ('driz', 'rain', 'rain',),
        'mild': ('driz', 'rain', 'rain',),
        'warm': ('driz', 'rain', 'rain', 'storm'),
         'hot': ('driz', 'rain', 'storm'),
        'boil': ('driz', 'rain', 'storm'),
        },
        ('tornado',),
        )
autumn = Season(
        5,
        {
        'froz': ('sleet', 'flury', 'snow'),
        'cold': ('driz', 'sleet', 'flury'),
        'cool': ('driz', 'rain'),
        'mild': ('driz', 'rain'),
        'warm': ('driz', 'rain'),
         'hot': ('driz', 'rain'),
        'boil': ('driz', 'rain'),
        },
        ('icestorm',),
        )
winter = Season(
        5,
        {
        'froz': ('snow', 'icestorm'),
        'cold': ('flury', 'snow', 'snow'),
        'cool': ('flury', 'flury', 'sleet', 'sleet', 'snow'),
        'mild': ('driz', 'driz', 'rain', 'rain', 'flury'),
        'warm': ('rain',),
         'hot': ('rain',),
        'boil': ('rain',),
        },
        ('blizzard',),
        )

Day = namedtuple('Day', ['day', 'month', 'year', 'temp', 'rain', 'moon', 'meteor'])
Month = namedtuple('Month', ['name', 'length', 'season', 'temp'])
MONTHS = {
      # idx       name,   days season   temp
        0: Month('Janus', 35, winter, 'cold'),
        1: Month('Marus', 35, spring, 'mild'),
        2: Month('Apris', 35, spring, 'warm'),
        3: Month('Maius', 35, summer, 'hot'),
        4: Month('Iunis', 35, summer, 'hot'),
        5: Month('Sexti', 35, summer, 'hot'),
        6: Month('Septi', 35, summer, 'warm'),
        7: Month('Octus', 35, autumn, 'mild'),
        8: Month('Novus', 35, autumn, 'cool'),
        9: Month('Decus', 35, winter, 'cold'),
        }


weather = Weather(temperatures)
calendar = Calendar(MONTHS, weather, 28)

for month in calendar.a_year(1288):
    table = '======================== ========================== ========================== ========================== =========================='
    print table
    print '%24s %26s %26s %26s %26s' % ('%s, %s' % (calendar.month, calendar.year), 'Morning', 'Afternoon', 'Evening', 'Night')
    print table
    for d in month():
        if d.moon in ('lunar', 'solar'):
            first = '**%s**' % d.moon  # hilight eclipses
        elif d.moon:
            first = '%s' % d.moon  # moon_phase
        else:
            first = ''
        if d.meteor:
            special = '**\***'  # lunar meteor storm
            special_watch = 3
        elif random.randint(1, 100) == 1:
            special = '**!** '  # 1 in 100 chance of special event
            special_watch = random.randint(1, 4)
        else:
            special = ''
            special_watch = 0
        bits = ['%2i %9s %4s %6s' % (d.day, d.temp, first, ''), ]
        for i in range(4):
            if special and i == special_watch:
                watch = '%s %s' % (special, d.rain[i])
            else:
                watch = d.rain[i]
            bits.append('%-26s' % watch)
        print ' '.join(bits)
    print table
    print
