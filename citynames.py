#!/usr/bin/python
'''English sounding citynames.

from http://inkwellideas.com/?page_id=631
'''

import random


one = ['A', 'Birm', 'Chi', 'Cov', 'Ed', 'Ex', 'Glou', 'Lan', 'Lei', 'Lic', 'Mar', 'New', 'Nott', 'Ox', 'Pet', 'Sal', 'South', 'Sund', 'West', 'Win', ]
two = ['Amp', 'Bang', 'Ber', 'Cam', 'Carl', 'Cas', 'Cest', 'Chest', 'Dur', 'En', 'Et', 'In', 'Ing', 'Is', 'Lich', 'Lon', 'Minst', 'New', 'Ply', 'Ver', ]
tre = ['Borough', 'Bridge', 'Burgh', 'Bury', 'Dee', 'Deen', 'Derry', 'Dom', 'Er', 'Field', 'Ford', 'Ham', 'Isle', 'Land', 'Or', 'Port', 'Pool', 'Tle', 'Ton', 'Try', ]

for i in range(20):
    c = lambda w: random.choice(w)
    print ''.join([c(one), c(two), c(tre)]).title()
