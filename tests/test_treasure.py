"""Every ruleset must roll every table and treasure type without error, from valid tables."""

import random
import re

import pytest
from click.testing import CliRunner

import treasure

RULESETS = [
    treasure.BasicRules,
    treasure.BasicRawRules,
    treasure.ExpertRules,
    treasure.ExpertRawRules,
    treasure.OddRules,
    treasure.GreyhawkRawRules,
    treasure.GreyhawkRules,
]
ODD_RULESETS = [rules for rules in RULESETS if issubclass(rules, treasure.OddRules)]
BX_RULESETS = [rules for rules in RULESETS if issubclass(rules, treasure.ExpertRawRules)]
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
        assert f'Using {name}.' in result.output


def test_cli_one_ruleset_only():
    result = CliRunner().invoke(treasure.cli, ['-o', '-g', 'potion'], obj={})
    assert result.exit_code == 2


def test_cli_type_s_only_tweaked_greyhawk():
    runner = CliRunner()
    assert runner.invoke(treasure.cli, ['-o', 'type', 's'], obj={}).exit_code == 2
    assert runner.invoke(treasure.cli, ['-rg', 'type', 's'], obj={}).exit_code == 2
    assert runner.invoke(treasure.cli, ['-g', 'type', '-s', 's'], obj={}).exit_code == 0


def test_cli_alt_greyhawk_flag_removed():
    assert CliRunner().invoke(treasure.cli, ['-a', 'potion'], obj={}).exit_code == 2


def test_table_roll_above_maximum():
    with pytest.raises(treasure.RollOutOfRange):
        treasure.table([(1, 'a'), (2, 'b')], 3)


def test_cli_roll_above_maximum_is_usage_error():
    result = CliRunner().invoke(treasure.cli, ['-b', '-d', '50', 'potion'], obj={})
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


@pytest.mark.parametrize('rules', BX_RULESETS)
def test_bx_table_sizes(rules):
    """Expert tables are d%, Basic magic tables are the book's die."""
    basic = issubclass(rules, (treasure.BasicRawRules, treasure.BasicRules))
    for name, chart in tables(rules):
        if name == 'item' or not basic:
            assert keys(chart)[-1] == 100, f'{rules.name} {name}'
    if basic:
        assert keys(treasure.BasicRawRules.armor)[-1] == 4
        assert keys(treasure.BasicRawRules.sword)[-1] == 8
        assert keys(treasure.BasicRawRules.weapon)[-1] == 4


@pytest.mark.parametrize('rules', BX_RULESETS)
def test_bx_type_codes(rules):
    assert set(rules.TREASURE_TYPES) == set('abcdefghijklmnopqrstuv')
    assert rules.TREASURE_TYPES['v'][2] == ('ep', 5, '1-100')
    assert list(rules().treasure_type('p'))


def test_bx_raw_spell_levels():
    rules = treasure.ExpertRawRules()
    assert treasure.table(rules._spell_level('Cleric'), 100) == '5th'
    assert treasure.table(rules._spell_level('Magic-user'), 100) == '6th'


@pytest.mark.parametrize('rules', BX_RULESETS)
def test_bx_charges(rules):
    ruleset = rules()
    assert ruleset.charges('Rod of Cancellation') == ' [single use]'
    assert ruleset.charges('Staff of Healing (D)') == ''


def test_bx_raw_charges():
    rules = treasure.ExpertRawRules()
    assert rules.charges('Staff of Snakes') == ''
    for _ in range(200):
        assert 2 <= int(re.search(r'(\d+) charges', rules.charges('Wand of Fear')).group(1)) <= 20
        assert 3 <= int(re.search(r'(\d+) charges', rules.charges('Staff of Power')).group(1)) <= 30


@pytest.mark.parametrize('rules', BX_RULESETS)
def test_bx_special_purpose_sword(rules):
    ruleset = rules()
    for _ in range(300):
        sword = ruleset._sentient_sword(special=True)
        alignment = sword.split(',')[0]
        assert 'Int 12, Ego 12' in sword
        assert f'Slay {alignment} creatures' not in sword


class FixedTreasures(treasure.Treasures):
    def __init__(self, things, noun='gem', plural='gems'):
        self.things, self.noun, self.plural = things, noun, plural

    def _roll(self, count, group):
        return iter(self.things)


def test_lines_header_and_indent():
    things = [(1, 100, 'Jade - Light green'), (1, 100, 'Jade - Light green'), (1, 200, 'large Carnelian - Orange')]
    assert FixedTreasures(things).lines(3, 10) == [
        '3 gems:',
        ' 2 x 100gp Jade - Light green',
        ' 1 x 200gp large Carnelian - Orange',
        ]


def test_lines_single_piece_no_header():
    assert FixedTreasures([(1, 1000, 'jewelry wrought platinum')], 'jewelry', 'jewelry').lines(1, 1) == ['1,000gp jewelry wrought platinum']
    assert FixedTreasures([(1, 0, 'Jade Crystal Ball')]).lines(1, 10) == ['Jade Crystal Ball']


def test_lines_odd_generic_noun_plural():
    assert FixedTreasures([(1, 50, 'gem'), (1, 50, 'gem'), (1, 10, 'gem')]).lines(3, 1) == [
        '3 gems:',
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
