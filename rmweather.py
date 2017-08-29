#!/usr/bin/env python3
'''Roll weather according to 16.0 Gamemaster Law RMFRP'''
from __future__ import print_function

import sys
import math
import random
import datetime
import operator

from dice import drm, d100


#    V        IV       III      II       I
temp_mod_table_src = '''
1   01-05    1-10     01-12    01-16    01-25
2   06-10    11-20    13-24    17-32    26-50
3   11-15    21-30    25-36    33-48    51-75
4   16-20    31-40    37-48    49-64    76-100*
5   21-25    41-50    49-60    65-80    101-116*
6   26-30    51-60    61-72    81-96*   117-132*
7   31-35    61-70    73-84    97-107*  133-148r
8   36-40    71-80    85-96*   108-118* 149-164r
9   41-45    81-90    97-104*  119-129* 165-173r
10  46-50    91-100*  105-112* 130-140r 174-182r
11  51-55    101-106* 113-120* 141-151r 183-199e
12  56-60    107-112* 121-128* 152-162r 200+e
13  61-65    113-118* 129-136r 163-167r
14  66-70    119-124* 135-144r 168-172r
15  71-75    125-130* 143-152r 173-177r
16  76-80    131-136r 151-160r 178-182e
17  81-85    137-142r 159-168r 183-187e
18  86-90    143-148r 169-172r 188+e
19  91-95    149-154r 173-176r
20  96-100*  155-160r 177-180r
21  101-103* 161-163r 181-184e
22  104-106* 164-166r 185-188e
23  107-109* 167-169r 189-192e
24  110-112* 170-172r 193+e
25  113-115* 173-175r
26  116-118* 176-178e
27  119-121* 179-182e
28  122-124* 183-185e
29  125-127* 186-188e
30  128-130* 189+e
31  131-133r
32  134-136r
33  137-139r
34  140-142r
35  143-145r
36  146-148r
37  149-151r
38  152-154r
39  155-157r
40  158-160r
41  161r
42  162r
43  163r
44  164r
45  165r
46  166r
47  167r
48  168r
49  169r
50  170r
51  171e
52  172e
53  173e
54  174e
55  175e
56  176e
57  177e
58  178e
59  179e
60  180+e
'''

precipitation_table = [        # Min Max Dur Mod   In Mod Wind Mod Move Awareness Tracking Direction
        (0, 'Calm ',             -99, 999, 0, 0,   0,  0,  1, -10,   0,    0,   0,    0),
        (2, 'Heavy Blizzard ',   -99, 10,  2, -5,  2, 5,   3,  60, -85, -100, -200, -50),
        (5, 'Light Blizzard ',   -99, 20,  2, 10,  2, 5,   2,  30, -75,  -90, -40,  -35),
        (10, 'Heavy Snowstorm ', -99, 25,  2, 5,   2, -5,  2, -20, -50,  -50, -25,  -20),
        (20, 'Light Snowstorm ', -99, 35,  2, -15, 1, 10,  2, -25, -25,  -25, -10,  -10),
        (25, 'Sleetstorm ',      -99, 35,  1, -15, 1, -35, 2, -20, -25,  -25, -10,  -5),
        (27, 'Hailstorm ',       -99, 65,  1, -30, 0, 0,   2, -10, -25,    0, -10,  -10),
        (30, 'Heavy Fog ',        20, 60,  1, 25,  0, 0,   1,   0, -75, -100, -30,  -50),   # adjusted tracking -60 to -30
        (38, 'Light Fog ',        30, 70,  2, -5,  0, 0,   1, -25, -50,  -75, -10,   -30),  # adjusted tracking -30 to -10
        (40, 'Mist ',             30, 999, 2, -20, 0, 0,   1, -25,   0,    0, -5,     0),
        (45, 'Drizzle ',          25, 999, 1, 10,  1, -45, 1,   0,   0,    0, '-5/hour',  0),
        (60, 'Light Rainstorm ',  25, 999, 1, 45,  1, -20, 1,   0,   0,    0, '-50/hour',  0),
        (70, 'Heavy Rainstorm ',  25, 999, 1, 30,  1, 20,  2, -10, -25,  -25, '-50/hour',  '-5/hour'),
        (84, 'Thunderstorm ',     30, 999, 1, -20, 1, 0,   2, -10, -50,  -25, '-50/hour',  -10),
        (89, 'Tropical Storm ',   40, 999, 3, 0,   3, -5,  2,  30, -75,  -50, -200,  -30),
        (99, 'Thunderstorm ',     30, 999, 1, -20, 1, 0,   2, -10, -50,  -25, '-50/hour',  -10),  # Austin, more thunderstorm.
        # (94, 'Monsoon ',          55, 999, 3, 80,  3, 25,  3,   0, -75,  -75, -200,  -30),
        # (97, 'Gale ',             40, 999, 3, 0,   3, 10,  3,  30, -75,  -75, -200,  -20),
        # (99, 'Hurricane ',        55, 999, 3, 5,   3, 20,  3, 100, -75,  -75, -200,  -30),
        (999, 'Special ',        -99, 999, 0, 0,   0, 0,   0,   0,   0,    0,    0,    0),
        ]

#      Roll Short Medium Long
precipitation_duration_table = [
        (0, 0.5, 1, 12),
        (8, 1, 2, 24),
        (16, 2, 5, 24),
        (24, 3, 8, 24),
        (32, 4, 10, 48),
        (40, 5, 13, 48),
        (48, 6, 16, 72),
        (56, 7, 18, 72),
        (64, 8, 21, 96),
        (72, 9, 24, 96),
        (80, 10, 26, 120),
        (88, 11, 29, 120),
        (96, 12, 32, 144),
        (112, 14, 37, 192),
        (128, 16, 42, 216),
        (144, 18, 48, 240),
        (160, 20, 53, 264),
        (176, 22, 58, 288),
        (192, 24, 64, 336),
        (216, 27, 72, 384),
        (240, 30, 80, 432),
        (264, 33, 88, 480),
        (999, 36, 96, 600),
        ]

precipitation_inches_table = [
        # Roll Light Heavy Prolonged
        (0,   0.1, 1,  1),
        (5,   0.5, 1,  1),
        (10,  1,   3,  1),
        (15,  1.5, 5,  2),
        (20,  2,   6,  2),
        (25,  2.5, 8,  3),
        (30,  3,   10, 3),
        (40,  4,   13, 4),
        (50,  5,   16, 5),
        (60,  6,   20, 6),
        (70,  7,   23, 7),
        (80,  8,   26, 8),
        (90,  9,   30, 9),
        (100, 10,  33, 10),
        (120, 12,  40, 12),
        (140, 14,  46, 14),
        (160, 16,  53, 16),
        (180, 18,  60, 18),
        (200, 20,  66, 20),
        (230, 23,  76, 23),
        (260, 26,  86, 26),
        (999, 29,  96, 29),
        ]

wind_table = [  # Light Heavy Storm
        (0, 0, 1, 1),
        (5, 1, 2, 2),
        (10, 2, 5, 4),
        (15, 3, 8, 6),
        (20, 4, 11, 8),
        (25, 5, 14, 11),
        (30, 6, 17, 14),
        (35, 7, 20, 17),
        (40, 8, 23, 20),
        (45, 9, 26, 24),
        (50, 10, 29, 28),
        (55, 11, 32, 32),
        (60, 12, 35, 36),
        (65, 13, 38, 39),
        (70, 14, 41, 42),
        (75, 15, 44, 45),
        (80, 16, 47, 48),
        (85, 17, 50, 50),
        (90, 18, 53, 52),
        (95, 19, 56, 54),
        (100, 20, 59, 56),
        (110, 21, 63, 60),
        (120, 22, 67, 65),
        (130, 23, 71, 70),
        (140, 24, 75, 80),
        (150, 25, 79, 90),
        (160, 26, 83, 100),
        (170, 27, 87, 115),
        (180, 28, 91, 130),
        (190, 29, 95, 145),
        (200, 30, 100, 165),
        (220, 31, 105, 185),
        (240, 32, 110, 205),
        (260, 33, 115, 230),
        (280, 34, 120, 255),
        (9999, 35, 125, 300),
        ]

# Added temps above 35.
windchill_table = [
        (999, 50,  45,  40,  35,  30,  25,  20,  15,  10,  5,  0,  -5,  -10,  -15,  -20),   # Temperature.
# Wind speed
        (5,   0,  -1,  -1,  -2,  -3,  -3,  -3,  -4,  -4,  -4,  -5,  -6,  -6,  -7,  -8),
        (10, -12, -13, -13, -14, -14, -16, -17, -18, -19, -20, -21, -22, -22, -22, -23),
        (15, -15, -17, -17, -19, -19, -24, -26, -26, -28, -30, -33, -35, -35, -36, -38),
        (20, -18, -19, -21, -23, -27, -29, -29, -32, -34, -37, -40, -41, -42, -43, -44),
        (25, -22, -24, -26, -28, -30, -32, -35, -37, -39, -42, -45, -47, -48, -50, -52),
        (30, -23, -27, -28, -30, -32, -36, -38, -41, -43, -46, -49, -51, -53, -55, -58),
        (35, -25, -28, -30, -32, -34, -38, -40, -42, -45, -48, -52, -55, -57, -60, -62),
        (40, -27, -29, -31, -33, -36, -40, -42, -44, -46, -50, -54, -57, -59, -61, -63),
        (45, -29, -31, -32, -34, -38, -42, -44, -46, -48, -51, -55, -58, -60, -62, -64),
        (50, -31, -32, -33, -35, -39, -43, -45, -47, -49, -53, -56, -59, -61, -63, -65),
        (55, -32, -33, -34, -36, -40, -44, -46, -48, -50, -54, -57, -60, -62, -64, -66),
        (60, -34, -35, -36, -38, -41, -45, -47, -49, -51, -55, -58, -61, -63, -65, -67),
        (999,-36, -36, -37, -40, -42, -46, -47, -50, -52, -56, -59, -62, -64, -66, -68),  # Made up last row.
        ]


# months_table = [
#         # name       sunrise  sunset    high,var low,var
#         ('2nd winter', (7, 15), (17, 00), (32, 3), (32, 4), 46, (25, 54, 999)),
#         ('3rd winter', (7, 00), (17, 30), (38, 1), (30, 3), 41, (20, 53, 999)),
#         ('1st spring', (6, 15), (18, 15), (46, 2), (38, 3), 45, (26, 45, 999)),
#         ('2nd spring', (5, 30), (18, 45), (58, 3), (48, 2), 43, (25, 52, 999)),
#         ('3rd spring', (4, 45), (19, 15), (69, 3), (57, 3), 42, (24, 52, 999)),
#         ('1st summer', (4, 30), (19, 30), (79, 2), (65, 1), 36, (22, 67, 999)),
#         ('2nd summer', (4, 45), (19, 30), (81, 1), (71, 1), 33, (31, 58, 999)),
#         ('3rd summer', (5, 15), (19, 00), (81, 0), (69, 1), 33, (31, 63, 999)),
#         ('1st autumn', (5, 45), (18, 15), (74, 1), (62, 2), 33, (31, 60, 999)),
#         ('2nd autumn', (6, 15), (17, 15), (72, 3), (52, 3), 36, (29, 54, 999)),
#         ('3rd autumn', (6, 45), (16, 45), (52, 3), (42, 3), 40, (19, 42, 999)),
#         ('1st winter', (7, 15), (16, 30), (38, 2), (33, 4), 43, (25, 55, 999)),
#         ]

# Austin
months_table = [
        # name         sunrise  sunset    high,var low,var  percep %   cloudcover_table
        ('2nd winter', (7, 00), (18, 00), (37, 3), (37, 4), 46, (25, 54, 999)),
        ('3rd winter', (6, 45), (18, 30), (43, 1), (35, 3), 41, (20, 53, 999)),
        ('1st spring', (6, 15), (18, 15), (50, 2), (40, 3), 45, (26, 45, 999)),
        ('2nd spring', (5, 30), (18, 45), (58, 3), (48, 2), 43, (25, 52, 999)),
        ('3rd spring', (5, 15), (19, 15), (69, 3), (57, 3), 42, (24, 52, 999)),
        ('1st summer', (5, 00), (19, 45), (79, 2), (65, 1), 36, (22, 67, 999)),
        ('2nd summer', (5, 15), (19, 45), (81, 1), (71, 1), 33, (31, 58, 999)),
        ('3rd summer', (5, 30), (19, 15), (81, 0), (69, 1), 33, (31, 63, 999)),
        ('1st autumn', (5, 45), (18, 45), (74, 1), (62, 2), 33, (31, 60, 999)),
        ('2nd autumn', (6, 15), (18, 15), (72, 3), (52, 3), 36, (29, 54, 999)),
        ('3rd autumn', (6, 45), (17, 45), (57, 3), (47, 3), 40, (19, 42, 999)),
        ('1st winter', (7, 00), (17, 45), (43, 2), (38, 4), 43, (25, 55, 999)),
        ]


def normalize_time(h, m):
    '''Convert minutes > 60 to additional hours.'''
    if m >= 60:
        m -= 60
        h += 1
    elif m < 0:
        m += 60
        h -= 1
    if h > 23:
        h -= 23
    elif h < 0:
        h += 23
    return h, m


def _calc_windchill(temp, wind):
    '''Return windchill for temperature and wind speed.'''
    # Windchill only applies to lower temps and wind 5mph or above.
    if temp > windchill_table[0][1] or wind < windchill_table[1][0]:  # Only valid for ranges in table.
        return temp
    temp_row = windchill_table[0]
    table = windchill_table[1:]
    for column, row_temp in enumerate(temp_row):
        if row_temp <= temp:
            break
    for speed, *row in table:
        if wind <= speed:
            return temp + row[column - 1]  # Column is indexed off of full row, with speed.


class Hour(object):
    '''
    :param hour: 1-24
    :param temp: temperature F defg
    '''
    def __init__(self, hour, temp, wind, precipitation, precipitation_mods):
        self.hour = hour
        self.temp = temp
        self.wind = wind
        self.chill = _calc_windchill(temp, wind)  # Windchill temp.
        self.precipitation = precipitation
        self.precipitation_move_mod = precipitation_mods[0]
        self.precipitation_awareness_mod = precipitation_mods[1]
        self.precipitation_tracking_mod = precipitation_mods[2]
        self.precipitation_direction_mod = precipitation_mods[3]


class Day(object):
    '''
    :param prev_day: previous Day() instance
    :param precipitation_chance: chance of precipitation this day (unless previous day's precip carries over)
    :param cloud_table: roll for cloud cover
    :param lowavg: avg low temp
    :param low_mod: modifer for table roll
    :param lowtable: roll on table for low temp variation
    :param highavg: avg low temp
    :param high_mod: modifer for table roll
    :param hightable: roll on table for high temp variation
    :param wind_mod: modifier for wind speed table roll
    :param sunrise: data from month table
    :param sunset: data from month table
    :param latitude: modifies sun rise/set
    '''
    def __init__(self, prev_day, precipitation_chance, cloud_table, lowavg, low_mod, lowtable, highavg, high_mod, hightable, wind_mod, sunrise, sunset, latitude):
        self.prev_day = prev_day
        self.low, self.low_mod = self._roll_temp(lowavg, operator.sub, low_mod - high_mod, lowtable)
        self.high, self.high_mod = self._roll_temp(highavg, operator.add, high_mod - low_mod, hightable)
        self.wind_mod = wind_mod
        self._calc_sun(latitude, sunrise, sunset)
        self._calc_temperature(prev_day)
        self._calc_precipitation(prev_day, precipitation_chance, cloud_table)

    @property
    def hours(self):
        '''Hour instance for each hour of day.'''
        for hour, temp in enumerate(self._hours[1:], start=1):
            if self.precipitation_start <= hour <= self.precipitation_end:
                precipitation = self.precipitation
                mods = self.precipitation_mods
            else:
                precipitation = None
                mods = (0, 0, 0, 0)
            yield Hour(datetime.time(hour=hour), temp, self.wind, precipitation, mods)

    def _calc_sun(self, latitude, sunrise, sunset):
        '''Return Time instances (sunrise, midday, sunset).
        :param latitude: latitude
        :param sunrise: data from month table
        :param sunset: data from month table
        '''
        # WTF doesn't datetime.time support arithmetic!!!
        def calc_midday(rise, sets):
            hour = sets.hour - rise.hour
            minute = sets.minute - rise.minute
            if minute < 0:
                minute += 60
                hour -= 1
            minute = minute // 2
            if hour % 2:
                minute += 30
            hour = hour // 2
            if minute >= 60:
                minute -= 60
                hour += 1
            return rise + datetime.timedelta(hours=hour, minutes=minute)

        mod = 15 * ((latitude - 40) // 7)
        rhour, rmin = sunrise
        shour, smin = sunset
        rhour, rmin = normalize_time(rhour, rmin + mod)
        shour, smin = normalize_time(shour, smin + mod)
        rise = datetime.datetime.utcnow()
        rise = rise.replace(hour=rhour, minute=rmin, second=0, microsecond=0)
        sets = datetime.datetime.utcnow()
        sets = sets.replace(hour=shour, minute=smin, second=0, microsecond=0)
        mids = calc_midday(rise, sets)
        self.sunrise = rise.time()
        self.midday = mids.time()
        self.sunset = sets.time()

    def _calc_temperature(self, prev_day):
        '''Calculate temp for every hour in the day.
        :param prev_day: previous Day() instance.
        '''
        # high around midday, low hour before sunrise
        # let d = high-low possible from previous day
        # evenly distribute 1/3 prevd between prevmidday and prevsunset
        # evenly distribute 2/3 prevd between prevsunset and low
        # evenly distribute d between low and midday
        # day0 midday -> day1 sunrise-1
        self._hours = list([0] * 24)  # 1 indexed
        low = self.sunrise.hour - 1
        if prev_day and prev_day._hours:
            afternoon_delta = ((prev_day.high - self.low) / 3.0) / (prev_day.sunset.hour - prev_day.midday.hour)
            last = prev_day._set_hours_temperatures(prev_day.midday.hour, prev_day.sunset.hour + 1, prev_day.high, -afternoon_delta)
            evening_delta = (((prev_day.high - self.low) / 3.0) * 2) / ((24 - prev_day.sunset.hour) + low)
            last = prev_day._set_hours_temperatures(prev_day.sunset.hour + 1, 24, last, -evening_delta)
            last = self._set_hours_temperatures(0, low, last, -evening_delta)
        morning_delta = (self.high - self.low) / (self.midday.hour - low)
        self._set_hours_temperatures(low, self.midday.hour, self.low, morning_delta)

    def _calc_precipitation(self, prev_day, chance, cloud_table):
        '''Is it raining?
        :param chance: % chance of precipitation
        :param cloud_table: data from month table
        '''
        if prev_day and prev_day.precipitation_end > 24:
            self.precipitation = prev_day.precipitation
            self.precipitation_start = 1
            self.precipitation_end = prev_day.precipitation_end - 24
            self.precipitation_mods = prev_day.precipitation_mods
            self.wind = prev_day.wind  # todo roll my own wind
            cloud_mod = 30
        else:
            roll = drm() + chance
            if roll > 100:
                self.precipitation = None
                while self.precipitation is None:
                    # Note: sets start/end.
                    self.precipitation, self.wind = self._roll_precipitation()
                cloud_mod = 30
            else:
                self.precipitation = None
                self.precipitation_start = 0
                self.precipitation_end = 0
                self.precipitation_mods = (0, 0, 0, 0)
                self.wind = self._roll_wind(1, -10)  # clear
                cloud_mod = 0
        # Cloud cover
        roll = d100() + cloud_mod
        if roll <= cloud_table[0]:
            self.cloud = 'Clear'
        elif roll <= cloud_table[1]:
            self.cloud = 'Partly'
        else:
            self.cloud = 'Cloudy'

    def _roll_precipitation(self):
        '''Determine precipitation parameters.'''
        def _roll_duration(base, mod):
            '''Look up precipitation duration from table.'''
            roll = drm() + mod
            for row in precipitation_duration_table:
                if roll <= row[0]:
                    return row[base]
            return precipitation_duration_table[-1][base]

        def _roll_inches(base, mod):
            '''Look up precipitation inches from table.'''
            roll = drm() + mod
            for row in precipitation_inches_table:
                if roll <= row[0]:
                    return row[base]
            return precipitation_inches_table[-1][base]

        roll = d100()
        for i, precipitation, mintemp, maxtemp, duration, duration_mod, inches, inchmod, wind, windmod, movemod, awaremod, trackmod, directionmod in precipitation_table:
            if roll <= i:
                if self.high > maxtemp or self.low < mintemp:
                    return None, 0
                self.precipitation_mods = movemod, awaremod, trackmod, directionmod
                self.precipitation_start = random.randint(1, 24)
                self.precipitation_end = self.precipitation_start + _roll_duration(duration, duration_mod)
                # stupidly high inches = _roll_inches(inches, inchmod)
                return precipitation, self._roll_wind(wind, windmod)

    def _roll_wind(self, base, storm_mod):
        '''Look up wind speed from table.'''
        roll = drm() + storm_mod + self.wind_mod
        # Only modify non-storm winds.
        if base == 1:
            roll += self.wind_mod
        for row in wind_table:
            if roll <= row[0]:
                return row[base]
        return wind_table[0][base]

    def _roll_temp(self, avg, op, mod, table):
        '''Look up temp variation from table.'''
        roll = drm() + mod
        # todo: replace with table lookup func
        for i, var, newmod in table:
            if i > roll:
                return op(avg, var), newmod

    def _set_hours_temperatures(self, start, end, initial, delta):
        '''Update temp for hours in day.
        :param start: start hour
        :param end: end our
        :param initial:  temp at start hour
        :param delta: hourly change in temp
        '''
        temp = initial
        for h in range(start, end):
            self._hours[h] = int(temp)
            temp += delta
        return temp


class Month(object):
    '''One month of weather/climate data.
    :param month: the month number 1-12, 1 being 2nd month of winter
    :param climate: type of climate, causes some modifiers
    :param latitude: latitude
    :param elevation: elevation
    '''
    def __init__(self, month, climate, latitude, elevation):
        self.month = month
        self.month_data = months_table[month - 1]
        self.climate = climate
        self.lat = latitude
        self.elevation = elevation
        self._temp_table = self._munge_temp_data(temp_mod_table_src)

    def calc_days(self, start, end):
        '''Calculate data for Month.'''
        self.days = list()
        # Some of current day is calculated from prev day, so create one.
        day = self._next_day(None)
        for i in range(start, end + 1):
            day = self._next_day(day)
            day.nth = i
            self.days.append(day)
        # Some of current day is calculated for next day so, do one more.
        self._next_day(day)

    def _next_day(self, prev_day):
        '''Calc values for next day of month, return Day instance.'''
        sunrise = self.month_data[1]
        sunset = self.month_data[2]
        highavg, highvar = self.month_data[3]
        lowavg, lowvar = self.month_data[4]
        precip_chance = self.month_data[5]
        cloud_table = self.month_data[6]
        # Die roll modifiers on temp table.
        if prev_day:
            low_mod = prev_day.low_mod
            high_mod = prev_day.high_mod
        else:
            low_mod = 0
            high_mod = 0
        temp_avg = -3 * math.floor(self.elevation / 1000)  # Mountain -3 per 1000'.
        wind_mod = 10 * math.floor(self.elevation / 1000)  # Mountain +5mph per 1000, changed to table mod.
        if 'forest' in self.climate or 'wood' in self.climate:
            wind_mod -= 10  # -5mph
            temp_avg -= 5  # -5deg
        if 'hill' in self.climate:
            wind_mod += random.randint(-10, 10)  # +/-5mph
        if 'plain' in self.climate:
            wind_mod += 10  # +5mph
        if 'city' in self.climate:
            lowavg += 5
            wind_mod -= 10
        if 'arid' in self.climate:
            highavg += 5
            lowavg -= 5
            precip_chance -= 20
        if 'desert' in self.climate:
            # Desert +10 day temp -10 night temp,  -30% precip chance.
            highavg += 10
            lowavg -= 10
            precip_chance -= 30
        # Custom Austin winds.
        if self.month in (3, 4, 5):  # Spring
            wind_mod += 5
        if self.month in (12, 1, 2):  # Winter
            wind_mod -= 10
        day = Day(prev_day, precip_chance, cloud_table, lowavg + temp_avg, low_mod, self._temp_table[lowvar], highavg + temp_avg, high_mod, self._temp_table[highvar], wind_mod, sunrise, sunset, self.lat)
        return day

    def _munge_temp_data(self, data):
        '''Rearrange table from book, convert codes to numbers.'''
        table = list(([], [], [], [], []))
        for row in data.strip().split('\n'):
            bits = row.strip().split()
            temp = bits[0]
            for i, bit in enumerate(bits[1:]):
                if '*' in bit:
                    bit = bit[:-1]
                    futuremod = 25
                elif 'r' in bit:
                    bit = bit[:-1]
                    futuremod = 50
                elif 'e' in bit:
                    bit = bit[:-1]
                    futuremod = 75
                else:
                    futuremod = 0
                if '-' in bit:
                    bit = bit.split('-')[1]
                if '+' in bit:
                    bit = sys.maxsize
                table[i].append((int(bit), int(temp), futuremod))
        table.reverse()
        return table


def print_chart(days):
    for day in days:
        print('\n%2s' % (day.nth, ), c.climate, day.cloud, day.wind, 'mph %s/%s low/high' % (day.low, day.high), 'rise', day.sunrise, 'mid', day.midday, 'set', day.sunset)
        if day.nth == 10:
            print('check lvl %i bubonic' % random.randint(1, 10))
        if day.nth == 20:
            print('check lvl %i pneumonic' % random.randint(1, 10))
        for h in day.hours:
            notes = list()
            if h.temp == day.low:
                low_high = 'l'
            elif h.temp == day.high:
                low_high = 'h'
            else:
                low_high = ' '
            if h.hour.hour == day.sunrise.hour:
                sun = '%02i:%02i rise' % (day.sunrise.hour, day.sunrise.minute)
            elif h.hour.hour == day.midday.hour:
                sun = '%02i:%02i' % (day.midday.hour, day.midday.minute)
            elif h.hour.hour == day.sunset.hour:
                sun = '%02i:%02i set' % (day.sunset.hour, day.sunset.minute)
            else:
                sun = ''
            rain = h.precipitation or ''
            if rain and h.precipitation_move_mod:
                notes.append('Maneuvers(%s)' % h.precipitation_move_mod)
            if rain and h.precipitation_awareness_mod:
                notes.append('Awareness(%s)' % h.precipitation_awareness_mod)
            if rain and h.precipitation_tracking_mod:
                notes.append('Tracking(%s)' % h.precipitation_tracking_mod)
            if rain and h.precipitation_direction_mod:
                notes.append('Direction Sense(%s)' % h.precipitation_direction_mod)
            if sun:
                notes.append(sun)
            if h.chill != h.temp:
                if h.temp > 35:  # Hi-temp wind chill only factor if exposed.
                    temp = '%2i[%i]' % (h.temp, h.chill)
                else:
                    temp = '%2i(%i)' % (h.temp, h.chill)
            else:
                temp = '%2i' % h.temp
            print('  %s%02i:%02i %s%s deg %s%s' % (sun and '*' or ' ', h.hour.hour, h.hour.minute, low_high, temp, rain, ', '.join(notes)))


if __name__ == '__main__':
    month = 11
    # one or more   'forest' 'city' 'wood' 'hill' 'plain'
    # one           'arid' 'desert'
    climate = 'arid'
    latitude = 30
    if len(sys.argv) > 1:
        month = int(sys.argv[1])
    elevation = 2100
    c = Month(month, climate, latitude, elevation)
    c.calc_days(11, 31)
    print_chart(c.days)
