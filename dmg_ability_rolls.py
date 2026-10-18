#!/usr/bin/env python3
"""Roll character ability scores using the methods from the AD&D 1e Dungeon Masters Guide.

(DMG p.11, "Generation of Ability Scores"; p.12 "Secondary Skills Table".)

Player characters, four alternatives:

    Method I    6 scores, each 4d6 with the lowest die discarded. Arrange as desired.
    Method II   12 rolls of 3d6, the highest 6 retained. Arrange as desired.
    Method III  Per ability, in order, 3d6 rolled 6 times, the highest retained.
    Method IV   12 characters of 3d6 per ability, in order. Player chooses the best set.

Non-player characters:

    General     3d6, but a 1 counts as 3 and a 6 as 4 (average scoring).
    Special     3d6, but abilities germane to the profession (str for fighters, etc.)
                add 1 to each die that scored under 6. Used for henchmen too.

Version: 10/18/2026
Author: Norman J. Harman Jr. <njharman@gmail.com>
Copyright: Released into Public Domain Jan 2021.
Website: https://github.com/njharman/rpg
"""

from collections import namedtuple

import click
from die import d6, d100

ABILITIES = ('Str', 'Int', 'Wis', 'Dex', 'Con', 'Cha')
# Roles of special NPCs and the ability scores germane to them, DMG p.11
NPC_ROLES = {
    'fighter': ('Str', 'Con'),
    'cleric': ('Wis', 'Con'),
    'magic-user': ('Int', 'Cha'),
    'thief': ('Int', 'Dex'),
}
NO_SKILL = 'No skill of measurable worth'
ROLL_TWICE = 'Roll twice, ignoring this result'
# (highest d100 score, result), DMG p.12 Secondary Skills Table, 00 is 100
SECONDARY_SKILLS = (
    (2, 'Armorer'),
    (4, 'Bowyer/fletcher'),
    (10, 'Farmer/gardener'),
    (14, 'Fisher (netting)'),
    (20, 'Forester'),
    (23, 'Gambler'),
    (27, 'Hunter/fisher (hook and line)'),
    (32, 'Husbandman (animal husbandry)'),
    (34, 'Jeweler/lapidary'),
    (37, 'Leather worker/tanner'),
    (39, 'Limner/painter'),
    (42, 'Mason/carpenter'),
    (44, 'Miner'),
    (46, 'Navigator (fresh or salt water)'),
    (49, 'Sailor (fresh or salt)'),
    (51, 'Shipwright (boats or ships)'),
    (54, 'Tailor/weaver'),
    (57, 'Teamster/freighter'),
    (60, 'Trader/barterer'),
    (64, 'Trapper/furrier'),
    (67, 'Woodworker/cabinetmaker'),
    (85, NO_SKILL),
    (100, ROLL_TWICE),
)
ARRANGE_NOTE = 'Assign to ability scores as desired.'
IV_NOTE = 'total: scores  * = score >= 15'
GERMANE_NOTE = '+ = germane ability, added 1 to each die that scored under 6'
# note is printed once before all characters
# lines is the full output
# brief_lines and brief_note the --brief one
Result = namedtuple('Result', 'note lines brief_note brief_lines')


def roll_dice(count):
    """List with count d6 rolls."""
    return [d6() for _ in range(count)]


def three_dsix():
    """(sum, dice_list) of 3d6 roll."""
    dice = roll_dice(3)
    return sum(dice), dice


def four_dsix_drop_lowest():
    """(sum, dice_list) of 4d6 roll less the lowest die.

    Dice sorted high to low so the last one is dropped.
    """
    dice = sorted(roll_dice(4), reverse=True)
    return sum(dice[:3]), dice


def average_die(die):
    """General NPC ability die roll: 1 counts as 3, 6 as 4."""
    return {1: 3, 6: 4}.get(die, die)


def germane_die(die):
    """Special NPC primary ability die roll: add 1 to dice that scored under 6."""
    return die + 1 if die < 6 else die


def sum_and_scores():
    """Total and the six 3d6 ability scores, in order."""
    scores = [three_dsix()[0] for _ in ABILITIES]
    return sum(scores), scores


def dice_string(dice):
    return ' '.join(str(x) for x in dice)


def scores_string(named_scores):
    """Brief 'Str: 17 Int: 12 ...' line from (name, text) pairs."""
    return ' '.join(f'{name}: {text}' for name, text in named_scores)


def method_i():
    """6 scores of 4d6 drop lowest, best first."""
    rolls = sorted((four_dsix_drop_lowest() for _ in range(6)), reverse=True)
    lines = [f'{total:2} ({dice_string(dice)})' for total, dice in rolls]
    return Result(ARRANGE_NOTE, lines, ARRANGE_NOTE, [', '.join(str(total) for total, _ in rolls)])


def method_ii():
    """12 rolls of 3d6, highest 6 retained."""
    rolls = sorted((three_dsix() for _ in range(12)), reverse=True)
    lines = [f'{total:2} ({dice_string(dice)})' for total, dice in rolls[:6]]
    lines.append('Discarded: ' + ' '.join(str(total) for total, _ in rolls[6:]))
    return Result(ARRANGE_NOTE, lines, ARRANGE_NOTE, [', '.join(str(total) for total, _ in rolls[:6])])


def method_iii():
    """Per ability in order, 6 rolls of 3d6 and the highest retained."""
    lines = []
    kept = []
    for name in ABILITIES:
        rolls = sorted((three_dsix()[0] for _ in range(6)), reverse=True)
        lines.append(f'{name}: {rolls[0]:2}  (also rolled {dice_string(rolls[1:])})')
        kept.append((name, rolls[0]))
    return Result(None, lines, None, [scores_string(kept)])


def method_iv():
    """12 characters of 3d6 per ability, in order, best total first."""
    rolls = sorted((sum_and_scores() for _ in range(12)), reverse=True)
    lines = []
    brief = []
    for total, scores in rolls:
        abilities = '  '.join(f'{x}: {y:2}' for x, y in zip(ABILITIES, scores, strict=True))
        lines.append(f'{total}: {abilities} {"*" * sum(x >= 15 for x in scores)}')
        brief.append(scores_string(zip(ABILITIES, scores, strict=True)))
    return Result(IV_NOTE, lines, None, brief)


def npc_general():
    """3d6 per ability, 1 counts as 3 and 6 as 4."""
    lines = []
    totals = []
    for name in ABILITIES:
        dice = [average_die(x) for x in roll_dice(3)]
        lines.append(f'{name}: {sum(dice):2} ({dice_string(dice)})')
        totals.append((name, sum(dice)))
    return Result(None, lines, None, [scores_string(totals)])


def npc_special(germane):
    """3d6 per ability, +1 per die under 6 for the germane abilities."""
    lines = []
    totals = []
    for name in ABILITIES:
        dice = roll_dice(3)
        if name in germane:
            dice = [germane_die(x) for x in dice]
        mark = ' +' if name in germane else ''
        lines.append(f'{name}: {sum(dice):2} ({dice_string(dice)}){mark}')
        totals.append((name, sum(dice)))
    return Result(GERMANE_NOTE if germane else None, lines, None, [scores_string(totals)])


def lookup_secondary_skill(score):
    """Result for a d100 score (00 is 100)."""
    return next(skill for highest, skill in SECONDARY_SKILLS if score <= highest)


def roll_secondary_skills():
    """List of skills, two if the table said to roll twice (re-rolling that result and duplicates)."""
    skill = lookup_secondary_skill(d100())
    if skill != ROLL_TWICE:
        return [skill]
    skills = []
    while len(skills) < 2:
        skill = lookup_secondary_skill(d100())
        if skill != ROLL_TWICE and skill not in skills:
            skills.append(skill)
    return skills


def secondary_skill_line():
    skills = roll_secondary_skills()
    return f'Secondary skill{"s" if len(skills) > 1 else ""}: {", ".join(skills)}'


def show(ctx, count, skill, brief, roller):
    """Echo count characters from roller, group options apply when the command's own aren't given."""
    inherited = ctx.obj or {}
    count = count or inherited.get('count') or 1
    skill = skill or inherited.get('skill', False)
    brief = brief or inherited.get('brief', False)
    characters = [(roller(), secondary_skill_line() if skill else None) for _ in range(count)]
    note = characters[0][0].brief_note if brief else characters[0][0].note
    if note:
        click.echo(note)
    for i, (result, skill_line) in enumerate(characters):
        lines = result.brief_lines if brief else result.lines
        if brief and len(lines) == 1:
            click.echo('; '.join([*lines, *([skill_line] if skill_line else [])]))
            continue
        if count > 1:
            click.echo(f'--- Character {i + 1} ---')
        for line in lines:
            click.echo(line)
        if skill_line:
            click.echo(skill_line)
        if i < count - 1:
            click.echo()


def common_options(func):
    func = click.option(
        '-b',
        '--brief',
        'brief',
        is_flag=True,
        default=False,
        help='One line per character: scores only, no dice or other rolls.',
    )(func)
    func = click.option(
        '--skill',
        'skill',
        is_flag=True,
        default=False,
        help='Include Secondary Skill for each character.',
    )(func)
    return click.option(
        '-n', '--count', type=click.IntRange(min=1), default=None, help='Roll n characters (default 1).'
    )(func)


class AliasedGroup(click.Group):
    """Case insensitive; also accepts ALIASES and any unique prefix of a command or alias."""

    ALIASES = {}

    def get_command(self, ctx, cmd_name):
        commands = {name.lower(): name for name in self.commands}
        candidates = {
            **{lower: lower for lower in commands},
            **{alias: target.lower() for alias, target in self.ALIASES.items()},
        }
        key = cmd_name.lower()
        if key in candidates:
            return super().get_command(ctx, commands[candidates[key]])
        names = {commands[target] for name, target in candidates.items() if name.startswith(key)}
        if len(names) > 1:
            ctx.fail(f'Ambiguous command {cmd_name!r}: could be {", ".join(sorted(names))}.')
        return super().get_command(ctx, names.pop()) if names else None


class MethodGroup(AliasedGroup):
    ALIASES = {
        'i': 'methodI',
        '1': 'methodI',
        'ii': 'methodII',
        '2': 'methodII',
        'iii': 'methodIII',
        '3': 'methodIII',
        'iv': 'methodIV',
        '4': 'methodIV',
    }


class NpcGroup(AliasedGroup):
    ALIASES = {'ftr': 'fighter', 'mu': 'magic-user'}

    def list_commands(self, ctx):
        """Help lists in registration order (general, professions, then abilities) rather than alphabetical."""
        return list(self.commands)


@click.group(cls=MethodGroup, invoke_without_command=True, context_settings={'help_option_names': ['-h', '--help']})
@common_options
@click.pass_context
def cli(ctx, count, skill, brief):
    """Roll character ability scores by the AD&D 1e DMG methods, Method I by default.

    See DMG p.11, "Generation of Ability Scores".
    """
    ctx.obj = {'count': count, 'skill': skill, 'brief': brief}
    if ctx.invoked_subcommand is None:
        show(ctx, None, False, False, method_i)


@cli.command('methodI', short_help='Method I (I, 1): 4d6 drop lowest, arrange as desired.')
@common_options
@click.pass_context
def method_i_command(ctx, count, skill, brief):
    """Method I (aliases I, 1): All scores are recorded and arranged in the order the player desires.

    4d6 are rolled, and the lowest die (or one of the lower) is discarded. Six scores, highest first, with the
    dice rolled (the last die is the one dropped).
    """
    show(ctx, count, skill, brief, method_i)


@cli.command('methodII', short_help='Method II (II, 2): best six of twelve 3d6, arrange as desired.')
@common_options
@click.pass_context
def method_ii_command(ctx, count, skill, brief):
    """Method II (aliases II, 2): All scores are recorded and arranged as in Method I.

    3d6 are rolled twelve times and the best six scores are retained. Shows the six kept and the totals discarded.
    """
    show(ctx, count, skill, brief, method_ii)


@cli.command('methodIII', short_help='Method III (III, 3): best of six 3d6 per ability, in order.')
@common_options
@click.pass_context
def method_iii_command(ctx, count, skill, brief):
    """Method III (aliases III, 3): Scores are rolled for each ability category, in order.

    Order is Strength, Intelligence, Wisdom, Dexterity, Constitution, Charisma. 3d6 are rolled six times for each
    ability and the highest score in each category is retained. Shows the other five rolls too.
    """
    show(ctx, count, skill, brief, method_iii)


@cli.command('methodIV', short_help='Method IV (IV, 4): twelve characters of 3d6 in order, choose one.')
@common_options
@click.pass_context
def method_iv_command(ctx, count, skill, brief):
    """Method IV (aliases IV, 4): 3d6 are rolled sufficient times to generate the six ability scores, in order.

    Order is Strength, Intelligence, Wisdom, Dexterity, Constitution, Charisma. Done for twelve characters, the player
    then selects the single set of scores he or she finds most desirable. Sets are listed best total first,
    with a * for each score of 15 or more. Secondary skill is rolled once per -n character, not per set.
    """
    show(ctx, count, skill, brief, method_iv)


@cli.group('npc', cls=NpcGroup, short_help='Non-player character: general, fighter, cleric, ...')
def npc():
    """Non-player character ability scores.

    See DMG p.11.

    \b
    general     3d6 per ability, but 1 counts as 3 and 6 as 4 (average scoring).
    fighter     3d6, +1 to each Str and Con die under 6. (alias ftr)
    cleric      3d6, +1 to each Wis and Con die under 6.
    magic-user  3d6, +1 to each Int and Cha die under 6. (alias mu)
    thief       3d6, +1 to each Int and Dex die under 6.
    str, int, wis, dex, con, cha
                3d6, +1 to each die under 6 for that one ability.
    """  # noqa: D301


def add_npc_command(name, germane, help_text):
    @click.command(name, help=help_text)
    @common_options
    @click.pass_context
    def command(ctx, count, skill, brief):
        show(ctx, count, skill, brief, lambda: npc_special(germane))

    npc.add_command(command)


@npc.command('general')
@common_options
@click.pass_context
def npc_general_command(ctx, count, skill, brief):
    """3d6, 1 changed to 3 and any 6 to 4."""
    show(ctx, count, skill, brief, npc_general)


for _role, _germane in NPC_ROLES.items():
    add_npc_command(
        _role,
        _germane,
        f'3d6, +1 to each {" and ".join(_germane)} die under 6.',
    )
for _ability in ABILITIES:
    add_npc_command(
        _ability.lower(),
        (_ability,),
        f'3d6, +1 to each {_ability} die under 6.',
    )


if __name__ == '__main__':
    cli()
