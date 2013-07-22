#!/usr/bin/env python
'''Generate ReStructuredText calendar.

Quick hack for author's Gold and Glory campaign.

Day is split into four "watches" 'Morning', 'Afternoon', 'Evening' are 4 hours each.
'Night' last 12 hours

Use rst2pdf to create PDF.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Oct 2012.
Website: http://trollandflame.blogspot.com/
'''

import random
from collections import namedtuple, deque


class Weather(object):
    def __init__(self, temps):
        ''':param temps: sequence of temps from coldest to hottest'''
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
            temp = min(mymax, max(mymin, idx))
            # Also, increasing chance to back off from extremes.
            if temp == mymin or temp == mymax:
                cum = 0
                for i in range(len(self._past_temp)):
                    if temp == self._past_temp[i]:
                        cum += 1
                if random.randint(0, len(self._past_temp)) < cum:
                    temp += cmp(1, temp)
            return temp

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
            forecast = (to_avg, to_avg, to_trend)
        else:
            forecast = (to_avg, to_trend, to_trend)
        self._idx = normalize(avg_idx, random.choice(forecast)(avg_idx))
        self._past_temp.rotate(1)
        self._past_temp[0] = self._idx
        return self.temps[self._idx]

    def _calc_rain(self, season, temp):
        '''Percipitation per "watch".
        '''
        rainy = list()
        self._rain_chance += season.chance
        if self._raining:  # double chance if already raining
            self._rain_chance += season.chance
        self._raining = False
        chance = self._rain_chance
        for i in range(4):
            rain = ''
            if random.randint(1, 100) <= chance:
                chance += 10
                self._raining = True
                if random.randint(1, 100) == 100:
                    rain = '**%s**' % random.choice(season.freak)
                else:
                    rain = '*%s*' % random.choice(season.rain[temp])
            rainy.append(rain)
        if not self._raining or self._rain_chance > 80:
            self._rain_chance = 0
        return rainy

    def forecast(self, season, avg):
        '''set self.temp and self.rain'''
        self.temp = self._calc_temp(self.temps.index(avg))
        self.rain = self._calc_rain(season, self.temp)


class Calendar(object):
    def __init__(self, month_data, lunar_cycle, weather):
        self.months = month_data
        self.lunar_cycle = lunar_cycle
        self.weather = weather
        self.length_of_year = sum(m.length for m in self.months.values())
        self.day = 1  # current day of the year
        self._month = self.months[0]  # current month structure
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
        # 'new', 'first quarter', 'full ', 'third quarter'
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
        '''Moon is "broken", chance around full moon of moon meteor shower.
        '''
        days = (self.year * self.length_of_year) + self.day_of_year
        day = (days % self.lunar_cycle) + 1  # + 1 cause?
        full = ((self.lunar_cycle / 4) * 3) + 1
        near = range(full - 2, full + 3)  # 2 days before and after full moon.
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
        self.weather.forecast(self._month.season, self._month.temp)
        return Day(
                self.day,
                self.day_of_year,
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


Season = namedtuple('Season', ['chance', 'rain', 'freak'])
spring = Season(
        10,
        {
            'froz': ('sleet', 'flury', ),
            'cold': ('sleet', ),
            'cool': ('driz', 'rain'),
            'mild': ('driz', 'rain', 'storm'),
            'warm': ('driz', 'rain', 'storm'),
            'hot ': ('driz', 'rain', 'storm', 'storm'),
            'boil': ('driz', 'rain', 'storm', 'storm'),
        },
        ('hail',),
        )
summer = Season(
        3,
        {
            'froz': ('fluries', 'snow'),
            'cold': ('sleet', 'driz', 'rain'),
            'cool': ('driz', 'rain', 'rain',),
            'mild': ('driz', 'rain', 'rain',),
            'warm': ('driz', 'rain', 'rain', 'storm'),
            'hot ': ('driz', 'rain', 'storm'),
            'boil': ('driz', 'rain', 'storm'),
        },
        ('tornado',),
        )
autumn = Season(
        5,
        {
            'froz': ('flury', 'flury', 'snow'),
            'cold': ('driz', 'sleet', 'sleet', 'flury'),
            'cool': ('driz', 'rain'),
            'mild': ('driz', 'rain'),
            'warm': ('driz', 'rain'),
            'hot ': ('driz', 'rain'),
            'boil': ('driz', 'rain'),
        },
        ('icestorm',),
        )
winter = Season(
        5,
        {
            'froz': ('flury', 'snow', 'snow', 'bliz'),
            'cold': ('flury', 'snow', 'snow'),
            'cool': ('sleet', 'sleet', 'flury', 'flury', 'snow'),
            'mild': ('driz', 'driz', 'rain', 'rain', 'flury'),
            'warm': ('driz', 'driz', 'rain'),
            'hot ': ('driz', 'driz', 'rain'),
            'boil': ('driz', 'driz', 'rain'),
        },
        ('whiteout',),
        )

Day = namedtuple('Day', ['day', 'day_of_year', 'month', 'year', 'temp', 'rain', 'moon', 'meteor'])

Month = namedtuple('Month', ['name', 'length', 'season', 'temp'])
MONTHS = {
    #  idx        name,  days season   temp
        0: Month('Janus', 36, winter, 'cold'),
        1: Month('Marus', 36, spring, 'mild'),
        2: Month('Apris', 36, spring, 'warm'),
        3: Month('Maius', 36, summer, 'hot '),
        4: Month('Iunis', 36, summer, 'hot '),
        5: Month('Sexti', 36, summer, 'hot '),
        6: Month('Septi', 36, summer, 'warm'),
        7: Month('Octus', 36, autumn, 'mild'),
        8: Month('Novus', 36, autumn, 'cool'),
        9: Month('Decus', 36, winter, 'cold'),
        10: Month('Festivus', 5, winter, 'cold'),
        }


temperatures = (
        'froz',
        'cold',
        'cool',
        'mild',
        'warm',
        'hot ',
        'boil',
        )

weather = Weather(temperatures)
# twelve 36 day months, followed by one 5 day winter festival
#   winter solstice is 3rd day of winter festival
# 28 day lunar cycle
calendar = Calendar(MONTHS, 28, weather)

for month_number, month in enumerate(calendar.a_year(374)):
    month_number += 1
    table = '======================== ========================== ========================== ========================== =========================='
    print table
    print '%24s %26s %26s %26s %26s' % (
            '[%i] %s, %s' % (month_number, calendar.month, calendar.year),
            'Morning', 'Afternoon', 'Evening', 'Night')
    print table
    for day in month():
        event_bits = list()
        if day.moon:
            event_bits.append('%s' % day.moon)      # moon phase
        elif day.moon in ('lunar', 'solar'):
            event_bits.append('**%s**' % day.moon)  # highlight eclipses
        if day.day_of_year == 363 - 180:
            event_bits.append('*sols*')
        elif day.day_of_year == 363 - 90:
            event_bits.append('*equx*')
        elif day.day_of_year == 363 - 270:
            event_bits.append('*equx*')
        elif day.day_of_year == 363:
            event_bits.append('*sols*')
        elif month_number == 11:
            event_bits.append('*fest*')     # Festivus!
        else:
            if day.moon == 'new':
                event_bits.append('*mkt*')  # new moon is market day
            if day.day == 13:
                event_bits.append('*pit*')  # 13th of month is Pit Fight Night!
        day_bits = ['%02i %-5s %-15s' % (day.day, day.temp, ' '.join(event_bits)), ]
        for i in range(4):
            if i == 3:
                watch_bits = ['OOO OOO', ]      # 3x 4hr
            else:
                watch_bits = ['oooo oooo', ]    # 4x 1hr
            if day.rain[i]:
                watch_bits.append(day.rain[i])
            if i == 3 and day.meteor:  # lunar meteor storm always at night
                watch_bits.append('**\***')
            if random.randint(1, 400) == 1:  # 1 in 100 chance (per day) of special event
                watch_bits.append('**!** ')
            day_bits.append('%-26s' % ' '.join(watch_bits))
        print ' '.join(day_bits)
    print table
    print
