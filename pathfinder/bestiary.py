#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Pathfinder RPG Bestairy statblock generator.

CSV data available from d20pfsrd.com

USAGE:
  bestiary --help
'''

import re
from collections import namedtuple, OrderedDict
from itertools import islice

from app import App, unicode_csv_reader
import jinja2

ENGINE = jinja2.Environment(trim_blocks=False, lstrip_blocks=True, autoescape=False)


FIELDS = ['name', 'cr', 'xp', 'race', 'character_class', 'monster_source', 'alignment', 'size', 'type', 'subtype', 'init', 'senses', 'aura', 'ac', 'ac_mods', 'hp', 'hd', 'hp_mods', 'saves', 'fort', 'ref', 'will', 'save_mods', 'defensive_abilities', 'dr', 'immune', 'resist', 'sr', 'weaknesses', 'speed', 'speed_mod', 'melee', 'ranged', 'space', 'reach', 'special_attacks', 'spelllike_abilities', 'spells_known', 'spells_prepared', 'spell_domains', 'abilitiy_scores', 'abilitiy_score_mods', 'bab', 'cmb', 'cmd', 'feats', 'skills', 'racial_mods', 'languages', 'sq', 'environment', 'organization', 'treasure', 'description_visual', 'group', 'source', 'is_template', 'special_abilities', 'description', 'full_text', 'gender', 'bloodline', 'prohibited_schools', 'before_combat', 'during_combat', 'morale', 'gear', 'other_gear', 'vulnerability', 'note', 'character_flag', 'companion_flag', 'fly', 'climb', 'burrow', 'swim', 'land', 'templates_applied', 'offense_note', 'base_statistics', 'extracts_prepared', 'age_category', 'dontuseracialhd', 'variantp_arent', 'mystery', 'class_archetypes', 'patron', 'companion_familiar_link', 'focused_school', 'traits', 'alternate_name', 'statistics_note', 'link_text', 'id', 'unique']
EntryTuple = namedtuple('Entry', FIELDS)
BLOCKTEMPLATE = ENGINE.from_string(u'''
{{ name }} CR{{ cr }} {{ xp }}XP {{ alignment }} {{ size }} {{ type }}{% if subtype %}({{ subtype }}){% endif %}
  {{ description_visual|wordwrap(wrapstring="\n    ") }}
  Init {{ "%+d"|format(init|int) }}; Senses {{ senses }}
{% if aura %}  {{ aura|title }}
{% endif -%}
{% if weaknesses %}  Weakness; {{ weaknesses|title }}
{% endif -%}
DEFENSE
  AC {{ ac }}{% if ac_mods %} ({{ ac_mods }}){% endif %}
  {%+ if dr %}{{ dr }}; {% endif %}hp {{ hp }} {{ hd }} {% if hp_mods %} ({{ hp_mods }}){% endif %}
  {%+ if sr %}SR{{ sr }}; {% endif %}{% if immune %}Immune {{ immune }}; {% endif %}Fort {{ "%+d"|format(fort|int) }}, Ref {{ "%+d"|format(ref|int) }}, Will {{ "%+d"|format(will|int) }}{% if save_mods %} ({{ save_mods }}){% endif %}
{% if defensive_abilities %}  SD {{ defensive_abilities|title }}
{% endif -%}
OFFENSE {{ speed }}{% if speed_mod %} ({{ speed_mod }}){% endif %}{% if space != '5 ft.' %}; {{ space }} space{% endif %}{% if reach != '5 ft.' %}; {{ reach }} reach{% endif %}
{% if melee %}  {{ melee }}
{% endif -%}
{% if ranged %}  {{ ranged }}
{% endif -%}
{% if special_attacks %}  {{ special_attacks|title }}
{% endif -%}
{% if spelllike_abilities -%}
  {% for title, spells in spelllike_abilities.items() %}  {{ title }}
    {% for s in spells %}    {{ s }}
    {% endfor -%}
  {%- endfor -%}
{%- endif -%}
STATISTICS {{ abilitiy_scores }}{% if abilitiy_score_mods %} ({{ abilitiy_score_mods }}){% endif %}
  BAB {{ "%+d"|format(bab|int) }}; CMB {{ cmb }}; CMD {{ cmd }}
{% if skills %}  {{ skills|wordwrap(wrapstring="\n    ") }}{% if racial_mods %}; Racial ({{ racial_mods }}){% endif %}
{% endif -%}
{% if feats %}  {{ feats|wordwrap(wrapstring="\n    ") }}{% endif %}{% if languages %}; {{ languages }}{% endif %}
{% if sq %}  SQ {{ sq|title }}
{% endif -%}
{% if special_abilities -%}
SPECIAL ABILITIES
  {%- for s in special_abilities %}
  {{ s|wordwrap(wrapstring="\n    ") }}
  {%- endfor -%}
{%- endif -%}
{% if _do_environment %}
ENVIRONMENT
  {{ environment }}
  {{ organization }}
  {{ treasure }}
{% endif -%}
{% if _do_description %}
DESCRIPTION
  {{ description }}
{% endif -%}
'''.strip())


class Entry(object):
    NAMES = ['Name', 'CR', 'XP', 'Race', 'Class', 'MonsterSource', 'Alignment', 'Size', 'Type', 'SubType', 'Init', 'Senses', 'Aura', 'AC', 'AC_Mods', 'HP', 'HD', 'HP_Mods', 'Saves', 'Fort', 'Ref', 'Will', 'Save_Mods', 'DefensiveAbilities', 'DR', 'Immune', 'Resist', 'SR', 'Weaknesses', 'Speed', 'Speed_Mod', 'Melee', 'Ranged', 'Space', 'Reach', 'SpecialAttacks', 'SpellLikeAbilities', 'SpellsKnown', 'SpellsPrepared', 'SpellDomains', 'AbilitiyScores', 'AbilitiyScore_Mods', 'BaseAtk', 'CMB', 'CMD', 'Feats', 'Skills', 'RacialMods', 'Languages', 'SQ', 'Environment', 'Organization', 'Treasure', 'Description_Visual', 'Group', 'Source', 'IsTemplate', 'SpecialAbilities', 'Description', 'FullText', 'Gender', 'Bloodline', 'ProhibitedSchools', 'BeforeCombat', 'DuringCombat', 'Morale', 'Gear', 'OtherGear', 'Vulnerability', 'Note', 'CharacterFlag', 'CompanionFlag', 'Fly', 'Climb', 'Burrow', 'Swim', 'Land', 'TemplatesApplied', 'OffenseNote', 'BaseStatistics', 'ExtractsPrepared', 'AgeCategory', 'DontUseRacialHD', 'VariantParent', 'Mystery', 'ClassArchetypes', 'Patron', 'CompanionFamiliarLink', 'FocusedSchool', 'Traits', 'AlternateNameForm', 'StatisticsNote', 'LinkText', 'id', 'UniqueMonster']

    def __init__(self, *row):
        object.__setattr__(self, 'data', EntryTuple(*row))
        try:
            self.cmb = '%+d' % int(self.cmb)
        except Exception as e:
            pass

    def __getattr__(self, name):
        return getattr(self.__dict__['data'], name)

    def __setattr__(self, name, value):
        object.__setattr__(self, 'data', self.data._replace(**{name: value}))

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def dump(self):
        return '\n'.join('%s: %s' % (k, v) for k, v in self.data._asdict().items() if v)

    def statblock(self, environment=False, description=False):
        data = self.data._asdict()
        data['_do_environment'] = environment
        data['_do_description'] = description
        text = BLOCKTEMPLATE.render(data).encode('utf=8')
        text = text.replace(' ft.', "'").replace('DC ', 'DC')
        return text.strip()


class BestiaryParser(object):

    def split_spelllike_abilities(self, text):
        '''
        Into dict[type of ability] -> list of individual spells
        '''
        if not text.strip():
            return list()
        bits = dict()
        abilities = [f for f in re.split(r'((?:Domain )?Spell-Like Abilit\w+ \(CL [^)]+\))', text) if f]
        for title, spells in zip(*[iter(abilities)] * 2):
            bits[title] = list()
            crap = [f for f in re.split(r'\s*((?:\d/day)|(?:At Will)|(?:Constant))-', spells) if f]
            for pair in zip(*[iter(crap)] * 2):
                bits[title].append('%s - %s' % pair)
        return bits

    def split_special_abilities(self, text):
        '''Into list.'''
        def internal(text):
            prev = None
            for item in re.split(r'\. ([a-zA-Z ]+\()', text):
                if prev is None:
                    yield item
                    prev = False
                elif prev:
                    yield '%s%s.' % (prev, item.strip('.'))
                    prev = False
                else:
                    prev = item
        if not text.strip():
            return list()
        return list(internal(text))

    def parse_csv(self, csv):
        def strip_parens(text):
            return text.strip(')').strip('(').strip()
        self.prd = list()
        #self.toh = list()
        self.sources = set()
        for row in islice(unicode_csv_reader(csv), 1, None):
            entry = Entry(*row)
            if entry.is_template == '1':
                continue
            for field in 'bab ref'.split():
                setattr(entry, field, int(getattr(entry, field)))
            entry.subtype = strip_parens(entry.subtype)
            entry.hp_mods = strip_parens(entry.hp_mods)
            entry.ac_mods = strip_parens(entry.ac_mods)
            entry.save_mods = strip_parens(entry.save_mods)
            entry.abilitiy_score_mods = strip_parens(entry.abilitiy_score_mods)
            entry.racial_mods = strip_parens(entry.racial_mods)
            entry.special_abilities = self.split_special_abilities(entry.special_abilities)
            entry.spelllike_abilities = self.split_spelllike_abilities(entry.spelllike_abilities)
            if entry.source == 'PFRPG" Bestiary':
                entry.source = 'PFRPG Bestiary'
            self.sources.add(entry.source)
            source = entry.source.lower()
            if 'bestiary' in source:
                self.prd.append(entry)
            #if 'tome of horrors complete' in source:
            #    self.toh.append(entry)


class BestiaryApp(App):
    '''Pathfinder BestiaryApp.'''
    VERSION = '1.0.0'

    def init_parser(self):
        super(BestiaryApp, self).init_parser(description=__doc__)
        self.actions.choices['search'].add_argument('terms', metavar='<terms>', nargs='+')
        self.cmdline.add_argument('-n', '--name', action='store_true')
        self.cmdline.add_argument('-l', '--line', action='store_true')

    def _byname(self):
        self.name_dict = OrderedDict((e.name.lower(), e) for e in self.prd)

    def _parse(self):
        parser = BestiaryParser()
        parser.parse_csv(open('monster_bestiary_full.csv'))
        self.prd = parser.prd

    def _search(self, field):
        self._parse()
        find = self.config.search.lower()
        for mob in self.prd:
            if find in getattr(mob, field).lower():
                print mob.statblock()
                print

    def _print_mobs(self, mobs):
        for mob in mobs:
            if self.config.name:
                print mob.name
            elif self.config.line:
                print '%s CR%s %s %s(%s)' % (mob.name, mob.cr, mob.size, mob.type, mob.subtype)
            else:
                print mob.statblock()
                print

    def action_search(self):
        self._parse()
        # pre-munge field term1,term2
        searches = list()
        for field, terms in zip(*[iter(t.lower() for t in self.config.terms)] * 2):
            if field == 'type':
                field = 'subtype'
            searches.append((field, [t.strip() for t in terms.split(',')]))
        mobs = set()
        for mob in self.prd:
            found = True
            for field, terms in searches:
                if not found:
                    break
                for term in terms:
                    if term not in getattr(mob, field).lower():
                        # either sub or main type
                        if field == 'subtype' and term in getattr(mob, 'type').lower():
                            continue
                        found = False
                        break
            if found:
                mobs.add(mob)
        self._print_mobs(sorted(mobs))

    def action_book(self):
        self._parse()
        self.prd.sort()
        self._print_mobs(self.prd)


if __name__ == '__main__':
    app = BestiaryApp()
    app.run()
