from die import *

heritages = [
    (1, "heritage great dishonor"),
    (15, "heritage dishonor"),
    (45, None),
    (76, "heritage honor"),
    (00, "heritage great honor"),
    ]

siblings = [
    (15, 0),
    (35, 1),
    (50, 2),
    (60, 3),
    (68, 4),
    (75, 5),
    (81, 6),
    (86, 7),
    (90, 8),
    (95, 9),
    (999, d4),
    ]

socialclasses = [
    (1, "SLC"),
    (6, "LLC"),
    (11, "MLC"),
    (20, "ULC"),
    (35, "LMC"),
    (55, "MMC"),
    (87, "UMC"),
    (96, "LUC"),
    (99, "MUC"),
    (999, "UUC"),
    ]

titles = [
    (999, None),
    (2, ("Emperor", "Empress")),
    (4, ("King", "Queen")),
    (2, ("Duke", "Duchess")),
    (2, ("Prince", "Princess")),
    ]

offices = [
    (999, None),
    ]

entitlements = [
    (50, None),
    (59, "%(social)s entitlement, doubled starting money"),
    (68, "%(social)s entitlement, free weapon from PHB"),
    (75, "%(social)s entitlement, free set of fine garments"),
    (84, "%(social)s entitlement, free religious item"),
    (90, "%(social)s entitlement, expensive bottle of wine/keg of ale/etc"),
    (92, "%(social)s entitlement, free mount with tack"),
    (94, "%(social)s entitlement, 10%% discount on services in home territory"),
    (96, "%(social)s entitlement, free choice of any armor and shield from PHB"),
    (98, "%(social)s entitlement, %(d4)s men-at-arms for use as personal guards while in home territory"),
    (999, "%(social)s entitlement, free room and board while in home territory"),
    ]

crimes = [
    [2, "Arson"],
    [7, "Banditry"],
    [13, "Battery"],
    [18, "Bearing Arms"],
    [19, "Blackmail"],
    [21, "Bribery of an Official"],
    [26, "Burglary"],
    [37, "Destruction of Property"],
    [38, "Embezzlement of Funds"],
    [39, "Exortion"],
    [43, "Forgery"],
    [48, "Defrauding Government"],
    [53, "Theft"],
    [55, "Impersonation of an Official"],
    [56, "Kidnapping"],
    [63, "Murder"],
    [68, "Piracy"],
    [79, "Possession of Illegal Items"],
    [87, "Rioting"],
    [92, "Robbery"],
    [96, "Sedition"],
    [100, "Theft"],
    ]

starting_money = [
    (10, "0d1"),
    (15, "20+1d4"),
    (20, "25+1d4"),
    (25, "30+1d4"),
    (30, "35+1d4"),
    (35, "45+1d6"),
    (40, "50+1d6"),
    (45, "55+1d6"),
    (50, "60+1d6"),
    (55, "70+1d8"),
    (60, "80+1d8"),
    (65, "90+1d8"),
    (70, "100+1d8"),
    (75, "110+1d10"),
    (80, "120+1d10"),
    (85, "130+1d10"),
    (90, "140+1d10"),
    (95, "145+1d20"),
    (100, "150+1d20"),
    (105, "160+1d20"),
    (110, "170+1d20"),
    (115, "180+2d20"),
    (999, "190+2d20"),
    ]

races = {
    'Dwarf': {'age': "40+5d6", 'maxage': "250+2d100", 'mheight': "45+2d4", 'mweight': "130+2d6", 'fheight': "43+2d4"},
    'Elf': {},
    'Gnome': {},
    'Half-elf': {},
    'Half-orc': {},
    'Halfling': {},
    'Human': {},
    }

professions = {
    'Fighter': {'age': "1d4", },
    }

add_honors = {
    "SLC": ("Social class", -10),
    "LLC": ("Social class", -10),
    "MLC": ("Social class", -5),
    "ULC": ("Social class", -1),
    "LUC": ("Social class", 1),
    "MUC": ("Social class", 5),
    "UUC": ("Social class", 10),
    "abandoned": ("Abandoned at birth", -3),
    "son of rapist": ("Son of rapist", -5),
    "prostitute mother": ("Mother was a prostitue", -10),
    "illegitimate birth": ("Illegitimate birth", -3),
    "surrogate mother": ("Surrogate mother", -1),
    "heritage great dishonor": ("Greatly dishonrable heritage", -5),
    "heritage dishonor": ("Dishonrable heritage", -2),
    "heritage honor": ("Honrable heritage", 2),
    "heritage great honor": ("Greatly honrable heritage", 5),
    }

inheirited_weapons = [
    (2000, "Sling"),
    (2200, "Quatersaff"),
    (2400, "Shortspear"),
    (2500, "Darts"),
    (2700, "Club"),
    (2800, "Knife"),
    (3000, "Light Mace"),
    (3400, "Spear"),
    (3500, "Whip"),
    (3700, "Dagger"),
    (3800, "Javelin"),
    (3900, "Spiked Gauntlet"),
    (4100, "Hand axe"),
    (4200, "Throwing axe"),
    (4400, "Warhammer"),
    (4500, "Sickle"),
    (4700, "Glaive"),
    (4900, "Morning star"),
    (5000, "Scimitar"),
    (5200, "Flail"),
    (5500, "Short sword"),
    (5600, "Light Pick"),
    (5700, "Light Hammer"),
    (5800, "Greatclub"),
    (6100, "Longspear"),
    (6300, "Halberd"),
    (6500, "Guisarme"),
    (6700, "Ranseur"),
    (6900, "Battlaaxe"),
    (7100, "Short Bow"),
    (7300, "Light Crossbow"),
    (7400, "Kukri"),
    (7600, "Heavy Flail"),
    (7800, "Heavy Pick"),
    (7900, "Light Spiked Shield"),
    (8000, "Heavy Spiked Shield"),
    (8500, "Longsword"),
    (8600, "Trident"),
    (8800, "Warhamer"),
    (9000, "Greataxe"),
    (9100, "Rapier"),
    (9200, "Scythe"),
    (9400, "Heavy Crossbow"),
    (9600, "Greatsword"),
    (9700, "Falchion"),
    (9800, "Bastard Sword"),
    (9900, "Lance"),
    (9950, "Long Bow"),
    (9990, "Combposite Shortbow"),
    (9999, "Hand Crossbow"),
    (99999, "Composite Longbow")
    ]

inheirited_armors = [
    (1500, "Padded"),
    (2000, "Leather"),
    (2300, "Hide"),
    (2700, "Studded"),
    (3000, "Scale"),
    (3100, "Chain shirt"),
    (3400, "Chainmail"),
    (3500, "Breastplate"),
    (3700, "Splint"),
    (3950, "Banded"),
    (3999, "Half plate"),
    (9999, "Full plate"),
    ]

inheirited_mounts = [
    (2000, "Mule"),
    (3000, "Donkey"),
    (3500, "Ox"),
    (3700, "Ox, cart"),
    (3900, "Pony"),
    (4000, "Riding Dog"),
    (5000, "Light Horse"),
    (5300, "Heavy Horse"),
    (5400, "Warpony"),
    (5700, "Light Warhorse"),
    (5900, "Heavy Warhorse"),
    (5950, "Heavy Horse x 2, wagon"),
    (9999, "Light Horse x 4, carriage"),
    ]

inheirited_deeds = [
    (5, "parcel of land in wilderness - harsh climate"),
    (10, "parcel of land in wilderness - inhabited by monsters"),
    (15, "parcel of land in wilderness - inhabited by humanoids"),
    (20, "parcel of land in territory of %(country)s - rugged terrain"),
    (25, "parcel of land in territory of %(country)s - arable"),
    (30, "parcel of land in territory of %(country)s - forest"),
    (35, "parcel of land in territory of %(country)s - hamlet, undeveloped"),
    (40, "parcel of land in territory of %(country)s - village, undeveloped"),
    (45, "parcel of land in territory of %(country)s - village, house"),
    (50, "parcel of land in territory of %(country)s - village, %(biz)s"),
    (55, "parcel of land in %(country)s borders - farm"),
    (60, "parcel of land in %(country)s borders - forest"),
    (65, "parcel of land in %(country)s borders - hamlet, home"),
    (70, "parcel of land in %(country)s borders - hamlet, %(biz)s"),
    (75, "parcel of land in %(country)s borders - village, home"),
    (80, "parcel of land in %(country)s borders - village, %(biz)s"),
    (85, "parcel of land in %(country)s borders - town, home"),
    (90, "parcel of land in %(country)s borders - town, %(biz)s"),
    (95, "parcel of land in %(country)s borders - city, home"),
    (999, "parcel of land in %(country)s borders - city, %s(biz)s"),
    ]

hamlet_biz = ["Smith", "Alehouse"]
village_biz = hamlet_biz + ["Armorer", "Bakers", "Butchers", "Fisthmongers", "Inn", "Hay Merchant", "Livestock Merchant", "Food Merchant", "Basket Weaver"]
town_biz = village_biz + ["Barbers", "Brewer", "Carpenters", "Coopers", "Leathworkers", "Locksmiths", "Masons", "General Merchant", "Painters", "Saddlers", "Stable", "Shoemakers", "Tailors", "Tannery", "Tavern", "Wood Merchant", "Cloth Weaver", "Undertaker", "Weapon makers"]
city_biz = town_biz + ["Alchemist", "Bathers", "Booksellers", "Scribes", "Chandlers", "Chicken Butchers", "Doctors", "Furriers", "Glassblowers", "Glovemakers", "Hatmakers", "Jewlers", "Musical Instruments", "Spice Merchant", "Used Cloths", "Pastrycooks", "Plasterers", "Purcemakers", "Rugmakers", "Scabbardmakers", "Sculpteors", "Restaurant", "Wine Merchant"]
