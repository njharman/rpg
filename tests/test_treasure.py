"""Every ruleset must roll every table and treasure type without error, from valid tables."""

import collections
import itertools
import random
import re

import click
import pytest
from click.testing import CliRunner

import treasure

RULESETS = [
    treasure.BasicRules,
    treasure.BasicRawRules,
    treasure.ExpertRules,
    treasure.ExpertRawRules,
    treasure.AdvancedRawRules,
    treasure.OddRules,
    treasure.GreyhawkRawRules,
    treasure.GreyhawkRules,
    treasure.DmgRules,
]
ODD_RULESETS = [rules for rules in RULESETS if issubclass(rules, treasure.OddRules)]
OSE_RULESETS = [rules for rules in RULESETS if issubclass(rules, treasure.ExpertRawRules)]
FUNCS = ('item', 'sword', 'armor', 'weapon', 'potion', 'scroll', 'ring', 'wsr', 'misc', 'odd_map')
D100_TABLES = ('item', 'sword', 'armor', 'weapon', 'potion', 'scroll', 'ring', 'wsr', 'misc')


def keys(chart):
    return [row[0] for row in chart]


def tables(rules):
    """Yield (name, chart) including Greyhawk misc sub-tables."""
    for name in D100_TABLES:
        chart = getattr(rules, name)
        yield name, chart
        for row in chart:
            if isinstance(row[1], list):
                yield f'{name}{row[0]}', row[1]


@pytest.fixture(autouse=True)
def seeded():
    random.seed(1974)


@pytest.mark.parametrize('rules', RULESETS)
def test_tables_ascending(rules):
    for name, chart in tables(rules):
        assert keys(chart) == sorted(set(keys(chart))), f'{rules.name} {name}'


@pytest.mark.parametrize('rules', ODD_RULESETS)
def test_odd_tables_are_d100(rules):
    for name, chart in tables(rules):
        assert keys(chart)[-1] == 100, f'{rules.name} {name}'
    assert keys(rules()._spell_level('Magic-user')) == [1, 2, 3, 4, 5, 6]
    assert keys(rules()._spell_level('Cleric')) == [1, 2, 3, 4, 5]
    assert keys(rules.scroll_curse)[-1] == 8


@pytest.mark.parametrize('rules', RULESETS)
@pytest.mark.parametrize('func', FUNCS)
def test_functions_roll(rules, func):
    ruleset = rules()
    for _ in range(300):
        result = getattr(treasure, f'entry_{func}')(ruleset)
        assert result
        assert not re.search(r'[<>{}]', result), result


@pytest.mark.parametrize('rules', RULESETS)
def test_treasure_types_roll(rules):
    ruleset = rules()
    for code in ruleset.TREASURE_TYPES:
        for _ in range(100):
            list(ruleset.treasure_type(code))


@pytest.mark.parametrize('rules', RULESETS)
def test_every_item_reachable(rules):
    """Every table entry can be rolled."""
    ruleset = rules()
    for name, chart in tables(rules):
        if name == 'item':
            continue
        for row in chart:
            if isinstance(row[1], list):
                continue
            result = ruleset.random_details(treasure.table(chart, row[0]))
            assert result
            assert '<' not in result, f'{rules.name} {name} {row}'


def test_odd_type_codes():
    assert set(treasure.OddRules.TREASURE_TYPES) == {'a', 'a-desert', 'a-water', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'}
    assert {'o', 'q', 's'} <= set(treasure.GreyhawkRules.TREASURE_TYPES)


def test_potion_s_type_greyhawk():
    assert list(treasure.GreyhawkRules().treasure_type('s', 1))


def test_replace_quantity_thousands():
    for _ in range(200):
        count, text = treasure.replace_quantity('1000-6000')
        assert count in range(1000, 6001, 1000)
        assert text == f'{count:,}'


def test_replace_quantity_mid_text_and_ranges():
    for _ in range(200):
        count, text = treasure.replace_quantity('Many Wishes (4-24), 2-5 Javelins')
        wishes, javelins = map(int, re.findall(r'\d+', text))
        assert 4 <= wishes <= 24
        assert 2 <= javelins <= 5
        assert count == wishes
    assert treasure.replace_quantity('Sword +1') == (1, 'Sword +1')


def test_cli_rulesets():
    runner = CliRunner()
    for flag, name in (
        ('-b', 'Basic rules'),
        ('-x', 'Expert rules'),
        ('-g', 'OD&D + Greyhawk rules'),
        ('-o', 'OD&D rules as written'),
        (None, 'Expert rules'),
        ('-rb', 'Basic rules as written'),
        ('-rx', 'Expert rules as written'),
        ('-r', 'Expert rules as written'),
        ('-rg', 'OD&D + Greyhawk rules as written'),
        ('--raw', 'Expert rules as written'),
        ('-ro', 'OD&D rules as written'),
    ):
        result = runner.invoke(treasure.cli, [flag, 'potion'] if flag else ['potion'], obj={})
        assert result.exit_code == 0, result.output
        assert f'One potion using {name}.' in result.output


def test_cli_one_ruleset_only():
    result = CliRunner().invoke(treasure.cli, ['-o', '-g', 'potion'], obj={})
    assert result.exit_code == 2


def test_cli_type_s_only_tweaked_greyhawk():
    runner = CliRunner()
    assert runner.invoke(treasure.cli, ['-o', 'type', 's'], obj={}).exit_code == 2
    assert runner.invoke(treasure.cli, ['-rg', 'type', 's'], obj={}).exit_code == 2
    assert runner.invoke(treasure.cli, ['-g', 'type', '-s', 's'], obj={}).exit_code == 0


def test_table_roll_above_maximum():
    with pytest.raises(treasure.RollOutOfRange):
        treasure.table([(1, 'a'), (2, 'b')], 3)


def test_cli_roll_above_maximum_is_usage_error():
    result = CliRunner().invoke(treasure.cli, ['-b', '--roll', '50', 'potion'], obj={})
    assert result.exit_code == 2
    assert 'higher than the table maximum' in result.output


@pytest.mark.parametrize(
    ('item', 'expected'),
    [
        ('Wand of Fear (M)', ' [100 charges]'),
        ('Staff of Power (M)', ' [200 charges]'),
        ('Staff of Healing (C)', ''),
        ('Wand of Metal Detection (M)', ''),
        ('Rod of Cancellation (All)', ' [single use]'),
        ('Rod of Rulership (All)', ' [10 charges]'),
        ('Rod of Absorption (M)', ' [100 spell levels]'),
        ('Rod of Lordly Might (F)', ' [25 charges]'),
        ('Ring of Protection', ''),
    ],
)
def test_charges_greyhawk_raw(item, expected):
    assert treasure.GreyhawkRawRules().charges(item) == expected


def test_charges_greyhawk_ranges():
    rules = treasure.GreyhawkRules()
    assert rules.charges('Rod of Cancellation (All)') == ' [single use]'
    assert rules.charges('Staff of Healing (C)') == ''
    for _ in range(200):
        wand = int(re.search(r'(\d+) charges', rules.charges('Wand of Fear (M)')).group(1))
        staff = int(re.search(r'(\d+) charges', rules.charges('Staff of Power (M)')).group(1))
        rod = int(re.search(r'(\d+) charges', rules.charges('Rod of Lordly Might (F)')).group(1))
        assert 80 <= wand <= 200
        assert 40 <= staff <= 100
        assert 15 <= rod <= 25


@pytest.mark.parametrize('rules', OSE_RULESETS)
def test_ose_table_sizes(rules):
    """Expert tables are d%, Basic magic tables are the book's die."""
    basic = issubclass(rules, (treasure.BasicRawRules, treasure.BasicRules))
    for name, chart in tables(rules):
        if name == 'item' or not basic:
            assert keys(chart)[-1] == 100, f'{rules.name} {name}'
    if basic:
        assert keys(treasure.BasicRawRules.armor)[-1] == 4
        assert keys(treasure.BasicRawRules.sword)[-1] == 8
        assert keys(treasure.BasicRawRules.weapon)[-1] == 4


@pytest.mark.parametrize('rules', OSE_RULESETS)
def test_ose_type_codes(rules):
    assert set(rules.TREASURE_TYPES) == set('abcdefghijklmnopqrstuv')
    assert rules.TREASURE_TYPES['v'][2] == ('ep', 5, '1-100')
    assert list(rules().treasure_type('p'))


def test_ose_raw_spell_levels():
    rules = treasure.ExpertRawRules()
    assert treasure.table(rules._spell_level('Cleric'), 100) == '5th'
    assert treasure.table(rules._spell_level('Magic-user'), 100) == '6th'


@pytest.mark.parametrize('rules', OSE_RULESETS)
def test_ose_charges(rules):
    ruleset = rules()
    assert ruleset.charges('Rod of Cancellation') == ' [single use]'
    assert ruleset.charges('Staff of Healing (D)') == ''


def test_ose_raw_charges():
    rules = treasure.ExpertRawRules()
    assert rules.charges('Staff of Snakes') == ''
    for _ in range(200):
        assert 2 <= int(re.search(r'(\d+) charges', rules.charges('Wand of Fear')).group(1)) <= 20
        assert 3 <= int(re.search(r'(\d+) charges', rules.charges('Staff of Power')).group(1)) <= 30


@pytest.mark.parametrize('rules', OSE_RULESETS)
def test_ose_special_purpose_sword(rules):
    ruleset = rules()
    for _ in range(300):
        traits, lines = ruleset._sentient_sword(special=True)
        assert traits[1:3] == ['Int 12', 'Ego 12']
        assert not any(line.startswith(f'special purpose: slay {traits[0]} creatures') for line in lines)


class FixedTreasures(treasure.Treasures):
    def __init__(self, things, noun='gem', plural='gems'):
        self.things, self.noun, self.plural = things, noun, plural

    def _roll(self, count, group):
        return iter(self.things)


def test_lines_header_and_indent():
    things = [(1, 100, 'Jade - Light green'), (1, 100, 'Jade - Light green'), (1, 200, 'large Carnelian - Orange')]
    assert FixedTreasures(things).lines(3, 10) == [
        '3 gems (400gp total):',
        ' 2 x 100gp Jade - Light green',
        ' 1 x 200gp large Carnelian - Orange',
    ]


def test_lines_single_piece_no_header():
    assert FixedTreasures([(1, 1000, 'jewelry wrought platinum')], 'jewelry', 'jewelry').lines(1, 1) == [
        '1,000gp jewelry wrought platinum'
    ]
    assert FixedTreasures([(1, 0, 'Jade Ioun geas')]).lines(1, 10) == ['Jade Ioun geas']


def test_lines_odd_generic_noun_plural():
    assert FixedTreasures([(1, 50, 'gem'), (1, 50, 'gem'), (1, 10, 'gem')]).lines(3, 1) == [
        '3 gems (110gp total):',
        ' 1 x 10gp gem',
        ' 2 x 50gp gems',
    ]


def test_amount_plurals():
    assert treasure.GemsOdd().amount(1) == '1 gem'
    assert treasure.GemsOdd().amount(2) == '2 gems'
    assert treasure.JewelriesOdd().amount(2) == '2 jewelry'


def test_magic_gem_name_strips_description():
    gems = treasure.Gems([0, 0, 100], specials=True)
    names = {thing for _ in range(200) for _, value, thing in gems._roll(20, 10) if value == 0}
    assert names
    assert not any(' - ' in name for name in names)


def test_brief_combines_gems_by_value():
    gems = treasure.Gems([100, 100, 100])
    gems.brief = True
    rolled = gems.roll(30, 10)
    assert {thing for _, _, thing in rolled} == {'gem'}
    assert len({value for _, value, _ in rolled}) == len(rolled)
    result = CliRunner().invoke(treasure.cli, ['--brief', 'gem', '30', '10'], obj={})
    assert result.exit_code == 0, result.output
    assert ' - ' not in result.output
    result = CliRunner().invoke(treasure.cli, ['--brief', 'jewelry', '20'], obj={})
    assert result.exit_code == 0, result.output
    assert 'wrought' not in result.output
    assert 'gems' not in result.output.split('\n', 1)[1]


def test_advanced_cli():
    runner = CliRunner()
    for args in (['-a', 'item', '5'], ['-ra', 'item', '5'], ['--advanced-OSE', 'misc', '5'], ['-a', 'type', 'h']):
        result = runner.invoke(treasure.cli, args, obj={})
        assert result.exit_code == 0, result.output
        assert 'using Advanced rules as written.' in result.output
    result = runner.invoke(treasure.cli, ['-a', '-b', 'item'], obj={})
    assert result.exit_code != 0


def test_advanced_rolls_have_no_placeholders():
    rules = treasure.AdvancedRawRules()
    for roll_function in (
        treasure.entry_item,
        treasure.entry_misc,
        treasure.entry_sword,
        treasure.entry_weapon,
        treasure.entry_wsr,
    ):
        for _ in range(500):
            result = roll_function(rules)
            assert '<' not in result, result
            assert '>' not in result, result


def test_advanced_every_table_row_rolls():
    rules = treasure.AdvancedRawRules()
    for name in ('sword', 'weapon', 'wsr'):
        for threshold, _ in getattr(rules, name):
            assert treasure._roll_table(rules, name, threshold)
    for _, chart in rules.misc:
        for threshold, _ in chart:
            assert treasure.entry_misc(rules, threshold)


def test_advanced_charges():
    rules = treasure.AdvancedRawRules()
    assert rules.charges('Immovable Rod') == ''
    assert rules.charges('Rod of Parrying') == ''
    assert rules.charges('Rod of Absorption') == ' [50 charges]'
    assert rules.charges('Rod of Cancellation') == ' [single use]'
    assert rules.charges('Staff of the Healer').endswith(' charges]')


def test_advanced_sword_type():
    rules = treasure.AdvancedRawRules()
    types = {rules.sword_extras('Sword +1').split(' +1')[0] for _ in range(200)}
    assert types == {'Short Sword', 'Sword', 'Two-handed Sword'}
    assert rules.sword_extras('Short Sword +2, Quickness').startswith('Short Sword +2, Quickness')


def test_advanced_ioun_stones():
    rules = treasure.AdvancedRawRules()
    for _ in range(200):
        result = rules._random_ioun()
        assert result.startswith(tuple(f'{count} stones' for count in range(1, 11)))


def test_replace_quantity_multiplier():
    for _ in range(200):
        count, text = treasure.replace_quantity('5-20x100')
        assert count in range(500, 2001, 100)
        assert text == f'{count:,}'
    for _ in range(200):
        assert treasure.replace_quantity('2-5x10000')[0] in range(20000, 50001, 10000)


def test_dmg_cli():
    runner = CliRunner()
    for args in (['-d', 'item', '5'], ['-rd', 'misc', '5'], ['--dmg', 'map', '3'], ['-d', 'type', 'h']):
        result = runner.invoke(treasure.cli, args, obj={})
        assert result.exit_code == 0, result.output
        assert 'using AD&D 1e rules as written.' in result.output
    assert runner.invoke(treasure.cli, ['-d', '-o', 'item'], obj={}).exit_code == 2
    result = runner.invoke(treasure.cli, ['-d', '--roll', '12', 'sword'], obj={})
    assert result.exit_code == 0
    assert 'word +1' in result.output


def test_dmg_type_codes():
    rules = treasure.DmgRules
    assert set(rules.TREASURE_TYPES) == set('abcdefghijklmnopqrstuvwxyz')
    assert rules.TREASURE_TYPES['a'][4] == ('pp', 25, '1-4x100')
    assert rules.TREASURE_TYPES['r'][1] == ('pp', 50, '10-60x100')
    assert [row[:2] for row in rules.TREASURE_TYPES['j']] == [('cp', 100)]
    assert list(rules().treasure_type('q', 1)) != []


def test_dmg_tables_are_d100():
    rules = treasure.DmgRules
    for name, chart in tables(rules):
        assert keys(chart)[-1] == 100, name


@pytest.mark.parametrize(
    ('table_name', 'roll', 'expected'),
    [
        ('potion', 42, 'Healing'),
        ('potion', 47, 'Healing'),
        ('potion', 48, 'Heroism (F)'),
        ('sword', 80, 'Sword +5, holy avenger'),
        ('sword', 96, 'Sword, cursed berserking'),
        ('armor', 97, 'Shield, large, +1, +4 vs. missiles (<size>)'),
        ('weapon', 100, 'Trident (Military Fork) +3'),
        ('wsr', 73, 'Wand of Metal & Mineral Detection (any)'),
    ],
)
def test_dmg_book_rows(table_name, roll, expected):
    assert treasure.table(getattr(treasure.DmgRules, table_name), roll) == expected


def test_dmg_misc_rows():
    rules = treasure.DmgRules
    assert treasure.table(rules.misc_3, 31) == 'Helm of Comprehending Languages & Reading Magic'
    assert treasure.table(rules.misc_3, 35) == 'Helm of Comprehending Languages & Reading Magic'
    assert treasure.table(rules.misc_1, 60) == 'Bracers of Defense (<bracers>)'
    assert treasure.table(rules.misc_4, 100) == "Quaal's Feather Token (<feather_token>)"
    assert treasure.table(rules.misc_5, 100) == 'Wings of Flying'
    assert treasure.table(rules.item, 46)[0] == 'Misc. Magic'
    assert treasure.table(rules.item, 87)[0] == 'Misc. Weapon'


def test_dmg_scroll_levels_by_row():
    rules = treasure.DmgRules()
    for _ in range(300):
        scroll = rules.scroll_spells('1 spell|2-9|2-7')
        level = int(re.search(r'1x(\d)', scroll).group(1))
        assert 2 <= level <= (7 if scroll.startswith(('Cleric', 'Druid')) else 9)
    for _ in range(100):
        scroll = rules.scroll_spells('7 spells|1-8')
        assert sum(int(count) for count in re.findall(r'(\d)x', scroll)) == 7


def test_dmg_scroll_casters():
    rules = treasure.DmgRules()
    casters = collections.Counter(rules._caster() for _ in range(4000))
    assert set(casters) == {'Magic-user', 'Illusionist', 'Cleric', 'Druid'}
    assert 0.6 < (casters['Magic-user'] + casters['Illusionist']) / 4000 < 0.8
    assert 0.2 < casters['Cleric'] / 4000 < 0.3


def test_dmg_charges():
    rules = treasure.DmgRules()
    assert rules.charges('Rod of Absorption (C, M)') == ' [50 spell levels]'
    assert rules.charges('Rod of Cancellation (any)') == ' [single use]'
    assert rules.charges('Staff of the Serpent (C)') == ''
    for _ in range(300):
        for item, low, high in (
            ('Rod of Smiting (C, F)', 41, 50),
            ('Staff of Power (M)', 20, 25),
            ('Wand of Fear (C, M)', 81, 100),
        ):
            assert low <= int(re.search(r'(\d+) charges', rules.charges(item)).group(1)) <= high


def test_dmg_every_sword_has_ego():
    assert {text for _, text in treasure.DmgRules.sword} == set(treasure.DmgRules._sword_ego)


def test_dmg_unusual_swords():
    rules = treasure.DmgRules()
    kinds = {}
    for _ in range(3000):
        for _roll, text in treasure.DmgRules.sword:
            result = rules.sword_extras(text)
            if ', Int ' in result.split('\n')[0]:
                kinds.setdefault(text, []).append(result)
    assert any('holy avenger' in text for text in kinds)
    assert all('Lawful Good' in result for result in kinds['Sword +5, holy avenger'])
    assert all('Chaotic' in result for result in kinds['Sword of Sharpness'])
    assert all('Lawful' in result for result in kinds['Sword, vorpal weapon'])
    assert all(' - Neutral, Int ' in result for text in kinds if 'cursed' in text for result in kinds[text])
    egos = [int(re.search(r'Ego (\d+)', result).group(1)) for results in kinds.values() for result in results]
    assert min(egos) >= 1


def test_dmg_sword_type_mix():
    rules = treasure.DmgRules()
    types = collections.Counter(rules.sword_extras('Sword +1').split(' +1')[0] for _ in range(5000))
    assert set(types) == {'Longsword', 'Broadsword', 'Short Sword', 'Bastard Sword', 'Two-handed Sword'}
    assert 0.65 < types['Longsword'] / 5000 < 0.75


def test_dmg_gem_values():
    gems = treasure.GemsDmg()
    ladder = gems.values
    gp = treasure.GP
    values = collections.Counter(value for _ in range(300) for _, value, _ in gems.roll(10, 10))
    assert min(values) > 0
    assert all(isinstance(value, int) for value in values)
    assert max(values) <= 5000 * gp * 2**7 * 2 * 1.6 * 100  # Never beyond 7 places up of the 5,000 base.
    for base in (10 * gp, 100 * gp, 5000 * gp):
        results = {gems._vary(base)[0] for _ in range(3000)}
        assert base in results
        assert base * 2 in results
        assert ladder[ladder.index(base) + 1] in results
        assert ladder[ladder.index(base) - 1] in results
        assert all(isinstance(value, int) for value in results)
        assert max(results) <= ladder[min(ladder.index(base) + 7, len(ladder) - 1)] * 2 * 1.6


def test_dmg_gem_decrease_floor():
    gems = treasure.GemsDmg()
    base = 10 * treasure.GP
    assert min(gems._vary(base)[0] for _ in range(20000)) >= gems.values[gems.values.index(base) - 5] * 0.6


def test_dmg_gem_ladder_below_10gp():
    gems = treasure.GemsDmg()
    assert [treasure.price(value, gems.per_gp) for value in gems.values[:6]] == [
        '1sp',
        '5sp',
        '10sp',
        '1gp',
        '5gp',
        '10gp',
    ]


def test_dmg_gem_words():
    gems = treasure.GemsDmg()
    base = 100 * treasure.GP
    seen = {}
    for _ in range(20000):
        value, words = gems._vary(base)
        seen.setdefault(words, []).append(value)
    assert {'', 'medium', 'large', 'small', 'tiny', 'flawed', 'perfect', 'extraordinary'} <= set(seen)
    assert set(seen['']) == {base}
    assert all(value in gems.values for value in seen['medium'] + seen['small'])
    assert set(seen['extraordinary']) <= {value * 2 for value in gems.values}
    assert all(value < base for value in seen['small'])
    assert all(value > base for value in seen['medium'])


def test_dmg_gem_named_by_base_value():
    gems = treasure.GemsDmg()
    words = {*gems.larger, *gems.smaller, 'flawed', 'perfect', 'extraordinary'}
    names = set()
    for stone in (stone for stones in gems.stones.values() for stone in stones):
        parts = re.split(r'\{([^}]*)\}', stone)  # Text, options, text, options ... text.
        choices = [part.split('|') if position % 2 else [part] for position, part in enumerate(parts)]
        names.update(''.join(chosen) for chosen in itertools.product(*choices))
    for _ in range(200):
        for _, _, described in gems.roll(10, 10):
            name = described
            while name not in names:
                prefix = next((prefix for prefix in words if prefix and name.startswith(prefix + ' ')), None)
                assert prefix, described
                name = name.removeprefix(prefix + ' ')


def test_dmg_gem_picks_one_alternative():
    gems = treasure.GemsDmg()
    assert {gems._choose('Jasper - {blue|black|brown}') for _ in range(200)} == {
        'Jasper - blue',
        'Jasper - black',
        'Jasper - brown',
    }
    assert gems._choose('Amber - watery gold to rich gold') == 'Amber - watery gold to rich gold'
    for _ in range(200):
        for _, _, described in gems.roll(10, 10):
            assert not set('{}|') & set(described), described


def test_dmg_jewelry_values():
    jewelry = treasure.JewelriesDmg()
    pieces = [value for _ in range(500) for _, value, _ in jewelry.roll(10, 1)]
    assert min(pieces) >= 100
    assert max(pieces) <= 12000 + 640000
    plain = {piece for _ in range(3000) for piece in [jewelry._piece()]}
    assert any(description == 'ivory or wrought silver' for _, description, _, _ in plain)
    assert all(not gems for _, description, gems, _ in plain if 'with gems' not in description)
    assert any(exceptional for *_, exceptional in plain)


def test_dmg_jewelry_notes():
    jewelry = treasure.JewelriesDmg()
    descriptions = {description for _ in range(300) for _, _, description in jewelry.roll(20, 1)}
    assert any('exceptional workmanship' in description for description in descriptions)
    assert any(re.search(r'exceptional stone \(\d[\d,]*gp\)', description) for description in descriptions)


def test_dmg_monetary_table():
    rules = treasure.DmgRules()
    assert treasure._dmg_monetary(rules, 1)[0].endswith('cp')
    assert treasure._dmg_monetary(rules, 1)[1].endswith('sp')
    assert treasure._dmg_monetary(rules, 4)[0].endswith('ep')
    assert treasure._dmg_monetary(rules, 7)[0].endswith('gp')
    assert treasure._dmg_monetary(rules, 11)[0].endswith('pp')
    assert re.match(r'\d+ gems \([\d,]+gp total\):\n', treasure._dmg_monetary(rules, 14)[0])
    assert re.match(r'\d+ jewelry \([\d,]+gp total\):\n', treasure._dmg_monetary(rules, 16)[0])
    everything = treasure._dmg_monetary(rules, 20)
    assert [part[-2:] for part in everything[:5]] == ['cp', 'sp', 'ep', 'gp', 'pp']
    assert len(everything) == 7
    for roll in (18, 19):
        assert treasure._dmg_monetary(rules, roll)


def test_dmg_monetary_amounts():
    rules = treasure.DmgRules()
    for _ in range(300):
        cp, sp = treasure._dmg_monetary(rules, 1)
        assert 20000 <= int(cp.removesuffix('cp').replace(',', '')) <= 80000
        assert 20000 <= int(sp.removesuffix('sp').replace(',', '')) <= 50000
        (pp,) = treasure._dmg_monetary(rules, 11)
        assert 500 <= int(pp.removesuffix('pp').replace(',', '')) <= 2000


def test_dmg_magic_treasure_rows():
    rules = treasure.DmgRules()
    assert len(treasure._dmg_magic(rules, 1)) == 5
    assert len(treasure._dmg_magic(rules, 8)) == 2
    assert len(treasure._dmg_magic(rules, 11)) == 3
    assert len(treasure._dmg_magic(rules, 16)) == 12
    assert len(treasure._dmg_magic(rules, 20)) == 5
    assert treasure.table(treasure.DMG_MAGIC, 14) == (treasure.entry_dmg_noswordpotion,) * 3


def test_dmg_no_sword_or_potion():
    rules = treasure.DmgRules()
    for _ in range(1000):
        result = treasure.entry_dmg_noswordpotion(rules)
        assert not result.startswith(('Potion of', 'Oil of', 'Philter of'))
        assert not result.startswith(('Longsword', 'Broadsword', 'Short Sword', 'Bastard Sword', 'Two-handed Sword'))


def test_dmg_hoard_rows():
    rules = treasure.DmgRules()
    for roll in range(1, 101):
        assert treasure._dmg_hoard(rules, roll)
    on_hand = treasure._dmg_hoard(rules, 85)
    assert [thing for thing in on_hand if thing.startswith('Treasure map')] == [on_hand[-1]]
    assert on_hand[0].endswith('cp')
    for roll in (97, 100):
        things = treasure._dmg_hoard(rules, roll)
        assert len(things) == 1
        assert things[0].startswith('Treasure map')
    assert not treasure._dmg_hoard(rules, 91)[0].startswith('Treasure map')
    assert sum(thing.startswith('Treasure map') for thing in treasure._dmg_hoard(rules, 91)) == 1


def test_dmg_map_format():
    rules = treasure.DmgRules()
    assert treasure.entry_dmg_map(rules, 1) == 'False map'
    for _ in range(300):
        for roll in (6, 71, 91):
            lines = treasure.entry_dmg_map(rules, roll).split('\n')
            if len(lines) == 1:
                assert re.fullmatch(r'Treasure map to ([\d,]+[cegps]p(, )?)+ \(.+\)', lines[0])
            else:
                assert re.fullmatch(r'Treasure map \(.+\) to:', lines[0])
                assert all(line.startswith(' ') for line in lines[1:])
                assert all(
                    len(line) - len(line.lstrip()) <= len(before) - len(before.lstrip()) + 1
                    for before, line in itertools.pairwise(lines[1:])
                )
    single = treasure.entry_dmg_map(rules, 6)
    assert single.startswith('Treasure map')


def test_format_sword():
    assert treasure.format_sword('Sword +1', ['Lawful'], []) == 'Sword +1 - Lawful'
    assert treasure.format_sword('Sword +1', ['Lawful', 'Int 8'], ['a', 'b']) == 'Sword +1 - Lawful, Int 8\n a\n b'
    assert treasure.indent('a\n b') == ' a\n  b'


@pytest.mark.parametrize(
    'rules', [treasure.OddRules, treasure.ExpertRules, treasure.AdvancedRawRules, treasure.DmgRules]
)
def test_sentient_sword_layout(rules):
    rules = rules()
    header = re.compile(
        r'.+ - [A-Z][\w ]*, Int \d+, Ego \d+, (empathy|semi-empathy|speaks [A-Z][\w ]* \+ \d+ others?|speaks [A-Z][\w ]* \+ \d+ others? and telepathy|telepathy(, speaks [A-Z][\w ]* \+ \d+ others?)?)'
    )
    seen = 0
    for _ in range(3000):
        lines = rules.sword_extras('Sword +1').split('\n')
        if ', Int ' not in lines[0]:
            continue
        seen += 1
        assert header.fullmatch(lines[0]), lines[0]
        assert all(line.startswith(' ') for line in lines[1:])
    assert seen


def test_dmg_hoard_map_keeps_nesting():
    rules = treasure.DmgRules()
    for _ in range(300):
        text = treasure.entry_dmg_map(rules, 91)
        lines = text.split('\n')
        inner = next((i for i, line in enumerate(lines) if line.startswith(' Treasure map')), None)
        if inner is not None and any(' - ' in line and line.startswith('  ') for line in lines[inner:]):
            sword = next(i for i, line in enumerate(lines) if i > inner and ' - ' in line and line.startswith('  '))
            if sword + 1 >= len(lines) or not lines[sword + 1].startswith('   '):
                continue
            ability = lines[sword + 1]
            assert ability.startswith('   ')
            assert not ability.startswith('    ')
            return


def test_odd_map_one_item_per_line():
    rules = treasure.OddRules()
    for _ in range(200):
        text = treasure.entry_odd_map(rules)
        assert '; ' not in text


def test_dmg_each_twice_lines():
    assert len(treasure.entry_dmg_each_twice(treasure.DmgRules())) == 12


def test_dmg_map_or_magic_determination():
    rules = treasure.DmgRules()
    assert treasure.entry_dmg_any(rules, 10).startswith(('Treasure map', 'False map'))
    for _ in range(200):
        assert not treasure.entry_dmg_any(rules, 11).startswith(('Treasure map', 'False map'))
    counts = collections.Counter(
        treasure.entry_dmg_any(rules).startswith(('Treasure map', 'False map')) for _ in range(5000)
    )
    assert 0.07 < counts[True] / 5000 < 0.13


def test_dmg_type_magic_counts():
    """MM Types: F is 3 items and a potion and a scroll, U is one of each non-potion non-scroll."""
    rules = treasure.DmgRules()
    f_magic = next(check for check in rules.TREASURE_TYPES['f'] if check[0] == 'magic')
    assert f_magic[1:] == (30, (treasure.entry_dmg_noweap_any,) * 3 + (treasure.entry_potion, treasure.entry_scroll))
    for _ in range(200):
        result = treasure.entry_dmg_each(rules)
        assert len(result) == 6


def test_dmg_potion_details():
    rules = treasure.DmgRules()
    for roll, fragment in (
        (2, 'Animal Control ('),
        (20, 'Dragon Control ('),
        (36, 'Giant Control ('),
        (97, 'Undead Control ('),
    ):
        assert fragment in treasure.entry_potion(rules, roll)


def test_dmg_ring_details():
    rules = treasure.DmgRules()
    assert treasure.entry_ring(rules, 44).startswith('Ring of Multiple Wishes (')
    assert treasure.entry_ring(rules, 61) in ('Ring of Regeneration', 'Ring of Vampiric Regeneration')
    assert 'Ring of Spell Storing (' in treasure.entry_ring(rules, 64)
    for _ in range(300):
        spells = rules._random_spells()
        assert 2 <= sum(int(count) for count in re.findall(r'(\d+)x', spells)) <= 5
        assert max(int(level) for level in re.findall(r'x(\d)', spells)) <= (
            7 if spells.startswith('Magic-user') else 5
        )


def test_dmg_misc_details():
    rules = treasure.DmgRules()
    assert re.fullmatch(r'Chime of Opening \[\d+ charges\]', rules.random_details(treasure.table(rules.misc_2, 13)))
    for roll in range(1, 101):
        for chart in (rules.misc_1, rules.misc_2, rules.misc_3, rules.misc_4, rules.misc_5):
            result = rules.random_details(treasure.table(chart, roll))
            assert '<' not in result
    assert re.search(r'\d+ stones:', rules._random_ioun())
    assert re.search(r'\d+ special beads:', rules._random_beads())
    assert 'dagger' in rules._random_useful_items()
    assert 2 <= len(rules._random_beaker().split(', ')) <= 5
    assert 40 <= int(rules._random_chime().split()[0]) <= 80


def test_command_prefix_and_aliases():
    ctx = click.Context(treasure.cli)
    for name, expected in (
        ('j', 'jewelry'),
        ('jew', 'jewelry'),
        ('jewel', 'jewelry'),
        ('gems', 'gem'),
        ('we', 'weapon'),
        ('ws', 'wsr'),
        ('wsr', 'wsr'),
    ):
        assert treasure.cli.get_command(ctx, name).name == expected
    assert treasure.cli.get_command(ctx, 'zzz') is None
    with pytest.raises(click.UsageError, match='Ambiguous'):
        treasure.cli.get_command(ctx, 's')


def test_cli_says_what_is_rolled():
    runner = CliRunner()
    for args, line in (
        (['-d', 'gem', '20'], '20 gems using AD&D 1e rules as written.'),
        (['-d', 'type', 'a'], 'Type A treasure using AD&D 1e rules as written.'),
        (['-b', 'jewelry'], 'One jewelry piece using Basic rules.'),
        (['-g', 'gem', '11'], '11 gems using OD&D + Greyhawk rules.'),
        (['-o', 'sword', '3'], 'Three magic swords using OD&D rules as written.'),
    ):
        result = runner.invoke(treasure.cli, args, obj={})
        assert result.exit_code == 0, result.output
        assert line in result.output


def test_ose_maps_roll_their_contents():
    rules = treasure.AdvancedRawRules()
    for numeral in treasure.OSE_MAPS:
        text = treasure._ose_map(rules, f'Treasure Map {numeral}: x')
        assert text.startswith('Treasure map to')
        assert 'Treasure Map' not in text
    five = treasure._ose_map(rules, 'Treasure Map V: x')
    assert five.startswith('Treasure map to:\n ')
    assert len(five.split('\n')) >= 5


def test_format_map():
    assert treasure.format_map(['5,000sp', '1,000gp']) == 'Treasure map to 5,000sp, 1,000gp'
    assert treasure.format_map(['5,000sp'], 'near') == 'Treasure map to 5,000sp (near)'
    mixed = treasure.format_map(['5,000sp', '2 gems (20gp total):\n 2 x 10gp gem', 'Potion of Healing'], 'far')
    assert mixed == 'Treasure map (far) to:\n 5,000sp\n 2 gems (20gp total):\n  2 x 10gp gem\n Potion of Healing'


@pytest.mark.parametrize(
    'rules', [treasure.BasicRules, treasure.ExpertRules, treasure.AdvancedRawRules, treasure.ExpertRawRules]
)
def test_ose_map_command_rolls_ose_maps(rules):
    rules = rules()
    for _ in range(200):
        assert treasure.entry_map(rules).startswith('Treasure map to')
        assert 'Treasure Map' not in treasure.entry_map(rules)


def test_odd_map_magic_is_never_a_map():
    rules = treasure.OddRules()
    for number in range(1, 9):
        for _ in range(100):
            assert not any(thing.lower().startswith('treasure map') for thing in treasure._map_magic(rules, number))


def test_odd_map_gems_are_listed():
    rules = treasure.OddRules()
    text = treasure.format_map(treasure._map_treasure(rules, 7))
    assert re.search(r'^ \d+ gems \([\d,]+gp total\):$', text, re.MULTILINE)
    assert re.search(r'^ \d+ jewelry \([\d,]+gp total\):$', text, re.MULTILINE)


@pytest.mark.parametrize(
    'rules',
    [
        treasure.OddRules,
        treasure.GreyhawkRules,
        treasure.ExpertRules,
        treasure.ExpertRawRules,
        treasure.AdvancedRawRules,
        treasure.DmgRules,
    ],
)
def test_sentient_sword_powers_are_lower_case(rules):
    rules = rules()
    for _ in range(2000):
        lines = rules.sword_extras('Sword +1').split('\n')[1:]
        for line in lines:
            checked = (
                re.sub(r'\b(Lawful|Neutral|Chaotic)\b', '', line) if line.startswith(' special purpose:') else line
            )
            assert not re.search(r'(^| )[A-Z][a-z]', checked), line


def test_dmg_gem_prices_are_whole():
    gems = treasure.GemsDmg()
    for _ in range(200):
        for line in gems.lines(30, 10):
            assert not re.search(r'\d\.\d', line), line
    assert treasure.price(50, 200) == '5sp'
    assert treasure.price(1300, 200) == '130sp'
    assert treasure.price(11, 200) == '11cp'
    assert treasure.price(400, 200) == '2gp'
    assert treasure.price(1200) == '1,200gp'
    assert treasure.price(0) == ''


def test_language_trait():
    assert treasure.language_trait('speech', 'Lawful', 2) == 'speaks Lawful + 2 others'
    assert treasure.language_trait('speech', 'Neutral', 1) == 'speaks Neutral + 1 other'
    assert treasure.language_trait('telepathy', 'Chaotic', 3) == 'telepathy, speaks Chaotic + 3 others'
    assert (
        treasure.language_trait('speech and telepathy', 'Lawful Good', 1)
        == 'speaks Lawful Good + 1 other and telepathy'
    )


def test_present_merges_and_sorts():
    item = treasure.Item
    lines = treasure.present(
        [
            item('Map to nowhere', 'map'),
            item('2 Arrows +1', 'weapon'),
            item('4 Arrows +1', 'weapon'),
            item('Dagger +1', 'weapon'),
            item('Potion of Healing', 'potion'),
            item('Potion of Healing', 'potion'),
            item('Oil of Slipperiness', 'potion'),
            item('Longsword +1', 'sword'),
            item('Longsword +1', 'sword'),
            item('1,000gp', 'money'),
            item('500gp', 'money'),
            item('200cp', 'money'),
            item('Scroll of Protection', 'scroll'),
        ]
    )
    assert lines == [
        '200cp',
        '1,500gp',
        'Oil of Slipperiness',
        'Two Potions of Healing',
        'Scroll of Protection',
        '6 Arrows +1',
        'Dagger +1',
        'Longsword +1',
        'Longsword +1',
        'Map to nowhere',
    ]


def test_item_commands_have_no_one_x():
    runner = CliRunner()
    for command in ('sword', 'weapon', 'ring', 'scroll'):
        result = runner.invoke(treasure.cli, [command, '30'], obj={})
        assert result.exit_code == 0
        assert not re.search(r'^1 x ', result.output, re.MULTILINE)
