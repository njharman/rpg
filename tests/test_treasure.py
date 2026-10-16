"""Every ruleset must roll every table and treasure type without error, from valid tables."""

import random
import re

import pytest
from click.testing import CliRunner

import treasure

RULESETS = [
    treasure.BasicRules,
    treasure.ExpertRules,
    treasure.OddRules,
    treasure.GreyhawkRules,
    treasure.AltGreyhawkRules,
]
ODD_RULESETS = [rules for rules in RULESETS if issubclass(rules, treasure.OddRules)]
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


@pytest.mark.parametrize('rules', ODD_RULESETS)
def test_tables_ascending(rules):
    for name, chart in tables(rules):
        assert keys(chart) == sorted(set(keys(chart))), f'{rules.name} {name}'


@pytest.mark.parametrize('rules', ODD_RULESETS)
def test_odd_tables_are_d100(rules):
    for name, chart in tables(rules):
        assert keys(chart)[-1] == 100, f'{rules.name} {name}'
    assert keys(rules()._spell_level('Magic-user')) == [1, 2, 3, 4, 5, 6]
    assert keys(rules()._spell_level('Cleric')) == [1, 2, 3, 4, 5]
    assert keys(rules.scroll_trap)[-1] == 8


@pytest.mark.parametrize('rules', RULESETS)
@pytest.mark.parametrize('func', FUNCS)
def test_functions_roll(rules, func):
    ruleset = rules()
    for _ in range(300):
        result = getattr(treasure, f'entry_{func}')(ruleset)
        assert result
        if rules in ODD_RULESETS:
            assert not re.search(r'[<>{}]', result), result


@pytest.mark.parametrize('rules', RULESETS)
def test_treasure_types_roll(rules):
    ruleset = rules()
    for code in ruleset.TREASURE_TYPES:
        for _ in range(100):
            list(ruleset.treasure_type(code))


@pytest.mark.parametrize('rules', ODD_RULESETS)
def test_odd_every_item_reachable(rules):
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
    assert {'o', 'q', 's'} <= set(treasure.AltGreyhawkRules.TREASURE_TYPES)


def test_potion_s_type_alt():
    assert list(treasure.AltGreyhawkRules().treasure_type('s', 1))


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
        ('-b', 'basic'),
        ('-x', 'expert'),
        ('-o', 'odd'),
        ('-g', 'greyhawk'),
        ('-a', 'altgreyhawk'),
        (None, 'expert'),
    ):
        result = runner.invoke(treasure.cli, [flag, 'potion'] if flag else ['potion'], obj={})
        assert result.exit_code == 0, result.output
        assert f'Using {name} rules.' in result.output


def test_cli_one_ruleset_only():
    result = CliRunner().invoke(treasure.cli, ['-o', '-g', 'potion'], obj={})
    assert result.exit_code == 2


def test_cli_odd_type_s_is_unknown_but_alt_works():
    runner = CliRunner()
    assert runner.invoke(treasure.cli, ['-o', 'type', 's'], obj={}).exit_code == 2
    assert runner.invoke(treasure.cli, ['-a', 'type', '-s', 's'], obj={}).exit_code == 0


def test_table_roll_above_maximum():
    with pytest.raises(treasure.RollOutOfRange):
        treasure.table([(1, 'a'), (2, 'b')], 3)


def test_cli_roll_above_maximum_is_usage_error():
    result = CliRunner().invoke(treasure.cli, ['-b', '-r', '50', 'potion'], obj={})
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
def test_charges_greyhawk(item, expected):
    assert treasure.GreyhawkRules().charges(item) == expected


def test_charges_alt_greyhawk_ranges():
    rules = treasure.AltGreyhawkRules()
    assert rules.charges('Rod of Cancellation (All)') == ' [single use]'
    assert rules.charges('Staff of Healing (C)') == ''
    for _ in range(200):
        wand = int(re.search(r'(\d+) charges', rules.charges('Wand of Fear (M)')).group(1))
        staff = int(re.search(r'(\d+) charges', rules.charges('Staff of Power (M)')).group(1))
        rod = int(re.search(r'(\d+) charges', rules.charges('Rod of Lordly Might (F)')).group(1))
        assert 80 <= wand <= 200
        assert 40 <= staff <= 100
        assert 15 <= rod <= 25
