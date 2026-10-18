"""DMG ability score methods: dice math, command names and aliases, secondary skills table."""

import itertools
import random

import pytest
from click.testing import CliRunner

import dmg_ability_rolls as dmg


def feed(monkeypatch, values):
    """Make d6 return values in turn, then keep returning 3s."""
    sequence = itertools.chain(values, itertools.repeat(3))
    monkeypatch.setattr(dmg, 'd6', lambda: next(sequence))


def invoke(*args):
    return CliRunner().invoke(dmg.cli, list(args))


def test_four_drop_lowest(monkeypatch):
    feed(monkeypatch, [1, 6, 2, 5])
    total, dice = dmg.four_dsix_drop_lowest()
    assert total == 13
    assert dice == [6, 5, 2, 1]


def test_method_i_six_sorted_scores(monkeypatch):
    feed(monkeypatch, [6, 6, 6, 1] * 3 + [1, 1, 1, 1] * 3)
    result = dmg.method_i()
    assert result.lines[:3] == ['18 (6 6 6 1)'] * 3
    assert result.lines[3:6] == [' 3 (1 1 1 1)'] * 3
    assert result.note == dmg.ARRANGE_NOTE
    assert result.brief_lines == ['18, 18, 18, 3, 3, 3']


def test_method_ii_keeps_highest_six(monkeypatch):
    feed(monkeypatch, [i % 6 + 1 for i in range(36)])
    lines = dmg.method_ii().lines
    assert len(lines) == 7
    assert lines[6].startswith('Discarded: ')
    kept = [int(x.split()[0]) for x in lines[:6]]
    discarded = [int(x) for x in lines[6].split(': ')[1].split()]
    assert min(kept) >= max(discarded)


def test_method_iii_keeps_highest_per_ability(monkeypatch):
    feed(monkeypatch, [6, 6, 6] + [1, 1, 1] * 5 + [2, 2, 2] * 30)
    result = dmg.method_iii()
    lines = result.lines
    assert [line.split(':')[0] for line in lines] == list(dmg.ABILITIES)
    assert lines[0].startswith('Str: 18')
    assert lines[1].startswith('Int:  6')
    assert result.brief_lines[0].startswith('Str: 18 Int: 6 Wis:')


def test_method_iv_twelve_sets_best_first():
    random.seed(4)
    result = dmg.method_iv()
    assert len(result.lines) == 12
    assert len(result.brief_lines) == 12
    totals = [int(line.split(':')[0]) for line in result.lines]
    assert totals == sorted(totals, reverse=True)


def test_npc_general_average_scoring(monkeypatch):
    feed(monkeypatch, [1, 6, 2] * 6)
    assert dmg.npc_general().lines[0] == 'Str:  9 (3 4 2)'


def test_npc_special_only_germane_boosted(monkeypatch):
    feed(monkeypatch, [1, 5, 6] * 6)
    result = dmg.npc_special(('Str', 'Con'))
    lines = result.lines
    assert lines[0] == 'Str: 14 (2 6 6) +'
    assert lines[1] == 'Int: 12 (1 5 6)'
    assert lines[4] == 'Con: 14 (2 6 6) +'
    assert 'germane' in result.note
    assert result.brief_lines == ['Str: 14 Int: 12 Wis: 12 Dex: 12 Con: 14 Cha: 12']


@pytest.mark.parametrize('score', range(1, 101))
def test_secondary_skill_table_covers_every_score(score):
    assert dmg.lookup_secondary_skill(score)


def test_secondary_skill_table_edges():
    assert dmg.lookup_secondary_skill(1) == 'Armorer'
    assert dmg.lookup_secondary_skill(67) == 'Woodworker/cabinetmaker'
    assert dmg.lookup_secondary_skill(68) == dmg.NO_SKILL
    assert dmg.lookup_secondary_skill(85) == dmg.NO_SKILL
    assert dmg.lookup_secondary_skill(86) == dmg.ROLL_TWICE
    assert dmg.lookup_secondary_skill(100) == dmg.ROLL_TWICE


def test_roll_twice_ignores_roll_twice(monkeypatch):
    rolls = iter([90, 100, 2, 99, 44])
    monkeypatch.setattr(dmg, 'd100', lambda: next(rolls))
    assert dmg.roll_secondary_skills() == ['Armorer', 'Miner']


def test_roll_twice_rerolls_duplicates(monkeypatch):
    rolls = iter([90, 1, 2, 44])
    monkeypatch.setattr(dmg, 'd100', lambda: next(rolls))
    assert dmg.roll_secondary_skills() == ['Armorer', 'Miner']


@pytest.mark.parametrize(
    'args',
    [
        (),
        ('methodI',),
        ('I',),
        ('1',),
        ('methodII',),
        ('ii',),
        ('2',),
        ('methodIII',),
        ('III',),
        ('3',),
        ('methodIV',),
        ('iv',),
        ('4',),
        ('npc', 'general'),
        ('npc', 'fighter'),
        ('npc', 'ftr'),
        ('npc', 'cleric'),
        ('npc', 'magic-user'),
        ('npc', 'mu'),
        ('npc', 'thief'),
        *[('npc', ability.lower()) for ability in dmg.ABILITIES],
        ('n', 'g'),
    ],
)
def test_commands_and_aliases_run(args):
    result = invoke(*args, '--skill')
    assert result.exit_code == 0, result.output
    assert 'Secondary skill' in result.output


def test_default_is_method_i():
    result = invoke()
    assert result.output.splitlines()[0] == dmg.ARRANGE_NOTE
    assert len(result.output.splitlines()) == 7


def test_note_printed_once_first():
    output = invoke('-n', '3', 'I').output
    assert output.count(dmg.ARRANGE_NOTE) == 1
    assert output.startswith(dmg.ARRANGE_NOTE)
    output = invoke('npc', 'fighter', '-n', '2').output
    assert output.count('germane') == 1
    assert output.startswith('+ = germane')


def test_brief_one_line_per_character():
    lines = invoke('I', '--brief', '--skill', '-n', '2').output.splitlines()
    assert lines[0] == dmg.ARRANGE_NOTE
    assert len(lines) == 3
    assert all('Secondary skill' in x and ', ' in x for x in lines[1:])
    assert 'Discarded' not in invoke('II', '--brief').output
    assert 'also rolled' not in invoke('--brief', 'III').output
    assert invoke('npc', 'general', '--brief').output.count('\n') == 1


def test_count_group_and_command_options():
    assert invoke('-n', '3', 'I').output.count('--- Character') == 3
    assert invoke('I', '-n', '2').output.count('--- Character') == 2
    assert invoke('npc', 'thief', '-n', '2').output.count('--- Character') == 2


def test_group_secondary_skill_applies_to_command():
    assert 'Secondary skill' in invoke('--skill', 'IV').output


def test_ambiguous_prefix_fails():
    result = invoke('method')
    assert result.exit_code != 0
    assert 'Ambiguous' in result.output


@pytest.mark.parametrize('args', [('-h',), ('npc', '-h'), ('IV', '-h'), ('npc', 'mu', '-h')])
def test_help(args):
    result = invoke(*args)
    assert result.exit_code == 0
    assert 'Method' in result.output or 'ability' in result.output or '3d6' in result.output


def test_brief_npc_has_no_germane_marks_or_note():
    output = invoke('npc', 'fighter', '--brief').output
    assert '+' not in output
    assert 'germane' not in output
    assert len(output.splitlines()) == 1
