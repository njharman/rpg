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
FUNCS = ('item', 'sword', 'armor', 'weapon', 'potion', 'scroll', 'ring', 'wsr', 'misc', 'map')
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
    assert keys(rules.scroll_levels) == [1, 2, 3, 4, 5, 6]
    assert keys(rules.scroll_trap)[-1] == 8


@pytest.mark.parametrize('rules', RULESETS)
@pytest.mark.parametrize('func', FUNCS)
def test_functions_roll(rules, func):
    ruleset = rules()
    for _ in range(300):
        result = getattr(treasure, f'_{func}')(ruleset)
        assert result
        if rules in ODD_RULESETS:
            assert not re.search(r'[<>{}]', result), result


@pytest.mark.parametrize('rules', RULESETS)
def test_treasure_types_roll(rules):
    ruleset = rules()
    for code in ruleset.TREASURE_TYPES:
        for _ in range(100):
            list(ruleset.type(code))


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
            result = ruleset.detail(treasure.table(chart, row[0]))
            assert result
            assert '<' not in result, f'{rules.name} {name} {row}'


def test_odd_type_codes():
    assert set(treasure.OddRules.TREASURE_TYPES) == {'a', 'a-desert', 'a-water', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'}
    assert {'o', 'q', 's'} <= set(treasure.AltGreyhawkRules.TREASURE_TYPES)


def test_potion_s_type_alt():
    assert list(treasure.AltGreyhawkRules().type('s', 1))


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
