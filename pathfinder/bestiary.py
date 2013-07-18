#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Bestairy statblock generator for Pathfinder RPG.

Author: Norman J. Harman Jr. <njharman@gmail.com>
Website: http://trollandflame.blogspot.com/

CSV data available from http://d20pfsrd.com

This software uses trademarks and/or copyrights owned by Paizo Publishing, LLC,
which are used under Paizo's Community Use Policy. We are expressly prohibited
from charging you to use or access this content. This software is not published,
endorsed, or specifically approved by Paizo Publishing. For more information
about Paizo's Community Use Policy, please visit paizo.com/communityuse. For
more information about Paizo Publishing and Paizo products, please visit
paizo.com.

http://paizo.com/paizo/about/communityuse


OPEN GAME LICENSE Version 1.0a

The following text is the property of Wizards of the Coast, Inc. and is Copyright 2000 Wizards of the Coast, Inc ("Wizards").  All Rights Reserved.

1. Definitions: (a)"Contributors" means the copyright and/or trademark owners who have contributed Open Game Content; (b)"Derivative Material" means copyrighted material including derivative works and translations (including into other computer languages), potation, modification, correction, addition, extension, upgrade, improvement, compilation, abridgment or other form in which an existing work may be recast, transformed or adapted; (c) "Distribute" means to reproduce, license, rent, lease, sell, broadcast, publicly display, transmit or otherwise distribute; (d)"Open Game Content" means the game mechanic and includes the methods, procedures, processes and routines to the extent such content does not embody the Product Identity and is an enhancement over the prior art and any additional content clearly identified as Open Game Content by the Contributor, and means any work covered by this License, including translations and derivative works under copyright law, but specifically excludes Product Identity. (e) "Product Identity" means product and product line names, logos and identifying marks including trade dress; artifacts; creatures characters; stories, storylines, plots, thematic elements, dialogue, incidents, language, artwork, symbols, designs, depictions, likenesses, formats, poses, concepts, themes and graphic, photographic and other visual or audio representations; names and descriptions of characters, spells, enchantments, personalities, teams, personas, likenesses and special abilities; places, locations, environments, creatures, equipment, magical or supernatural abilities or effects, logos, symbols, or graphic designs; and any other trademark or registered trademark clearly identified as Product identity by the owner of the Product Identity, and which specifically excludes the Open Game Content; (f) "Trademark" means the logos, names, mark, sign, motto, designs that are used by a Contributor to identify itself or its products or the associated products contributed to the Open Game License by the Contributor (g) "Use", "Used" or "Using" means to use, Distribute, copy, edit, format, modify, translate and otherwise create Derivative Material of Open Game Content. (h) "You" or "Your" means the licensee in terms of this agreement.
2. The License: This License applies to any Open Game Content that contains a notice indicating that the Open Game Content may only be Used under and in terms of this License. You must affix such a notice to any Open Game Content that you Use. No terms may be added to or subtracted from this License except as described by the License itself.  No other terms or conditions may be applied to any Open Game Content distributed using this License.
3. Offer and Acceptance: By Using the Open Game Content You indicate Your acceptance of the terms of this License.
4. Grant and Consideration: In consideration for agreeing to use this License, the Contributors grant You a perpetual, worldwide, royalty-free, non-exclusive license with the exact terms of this License to Use, the Open Game Content.
5. Representation of Authority to Contribute: If You are contributing original material as Open Game Content, You represent that Your Contributions are Your original creation and/or You have sufficient rights to grant the rights conveyed by this License.
6. Notice of License Copyright: You must update the COPYRIGHT NOTICE portion of this License to include the exact text of the COPYRIGHT NOTICE of any Open Game Content You are copying, modifying or distributing, and You must add the title, the copyright date, and the copyright holder's name to the COPYRIGHT NOTICE of any original Open Game Content you Distribute.
7. Use of Product Identity: You agree not to Use any Product Identity, including as an indication as to compatibility, except as expressly licensed in another, independent Agreement with the owner of each element of that Product Identity. You agree not to indicate compatibility or co-adaptability with any Trademark or Registered Trademark in conjunction with a work containing Open Game Content except as expressly licensed in another, independent Agreement with the owner of such Trademark or Registered Trademark.  The use of any Product Identity in Open Game Content does not constitute a challenge to the ownership of that Product Identity. The owner of any Product Identity used in Open Game Content shall retain all rights, title and interest in and to that Product Identity.
8. Identification: If you distribute Open Game Content You must clearly indicate which portions of the work that you are distributing are Open Game Content.
9. Updating the License: Wizards or its designated Agents may publish updated versions of this License. You may use any authorized version of this License to copy, modify and distribute any Open Game Content originally distributed under any version of this License.
10. Copy of this License: You MUST include a copy of this License with every copy of the Open Game Content You Distribute.
11. Use of Contributor Credits: You may not market or advertise the Open Game Content using the name of any Contributor unless You have written permission from the Contributor to do so.
12. Inability to Comply: If it is impossible for You to comply with any of the terms of this License with respect to some or all of the Open Game Content due to statute, judicial order, or governmental regulation then You may not Use any Open Game Material so affected.
13. Termination: This License will terminate automatically if You fail to comply with all terms herein and fail to cure such breach within 30 days of becoming aware of the breach.  All sublicenses shall survive the termination of this License.
14. Reformation: If any provision of this License is held to be unenforceable, such provision shall be reformed only to the extent necessary to make it enforceable.
15. COPYRIGHT NOTICE
Open Game License v 1.0a Copyright 2000, Wizards of the Coast, Inc.
System Reference Document. Copyright 2000, Wizards of the Coast, Inc.; Authors Jonathan Tweet, Monte Cook, Skip Williams, based on material by E. Gary Gygax and Dave Arneson.
Pathfinder Roleplaying Game Reference Document. © 2011, Paizo Publishing, LLC; Author: Paizo Publishing, LLC.
Pathfinder Roleplaying Game Core Rulebook. © 2009, Paizo Publishing, LLC; Author: Jason Bulmahn, based on material by Jonathan Tweet, Monte Cook, and Skip Williams.
Pathfinder Roleplaying Game Bestiary. © 2009, Paizo Publishing, LLC; Author: Jason Bulmahn, based on material by Jonathan Tweet, Monte Cook, and Skip Williams.
Pathfinder Roleplaying Game Bestiary 2. © 2010, Paizo Publishing, LLC; Authors Wolfgang Baur, Jason Bulmahn, Adam Daigle, Graeme Davis, Crystal Frasier, Joshua J. Frost, Tim Hitchcock, Brandon Hodge, James Jacobs, Steve Kenson, Hal MacLean, Martin Mason, Rob McCreary, Erik Mona, Jason Nelson, Patrick Renie, Sean K Reynolds, F. Wesley Schneider, Owen K.C. Stephens, James L. Sutter, Russ Taylor, and Greg A. Vaughan, based on material by Jonathan Tweet, Monte Cook, and Skip Williams.
Pathfinder Roleplaying Game Bestiary 3. © 2011, Paizo Publishing, LLC; Authors: Jesse Benner, Jason Bulmahn, Adam Daigle, James Jacobs, Michael Kenway, Rob McCreary, Patrick Renie, Chris Sims, F. Wesley Schneider, James L. Sutter, and Russ Taylor, based on material by Jonathan Tweet, Monte Cook, and Skip Williams.
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
  {{ description_visual }}
  Init {{ "%+d"|format(init|int) }}; Senses {{ senses }}
{% if aura %}  {{ aura|title }}
{% endif -%}
DEFENSE {% if weaknesses %}
  Weakness; {{ weaknesses|title }} {% endif %}
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
{% if feats %}  {{ feats|wordwrap(wrapstring="\n    ") }}{% endif %}{% if languages %}; {{ languages }}
{% endif -%}
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
  {{ environment|wordwrap(wrapstring="\n    ") }}
  {{ organization|wordwrap(wrapstring="\n    ") }}
  {{ treasure|wordwrap(wrapstring="\n    ") }}
{%- endif -%}
{% if _do_description %}
DESCRIPTION
  {{ description|wordwrap(wrapstring="\n  ") }}
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

    def statblock(self, environment=True, description=False):
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

    def parse_csv(self, csv, sources):
        def strip_parens(text):
            return text.strip(')').strip('(').strip()
        self.prd = list()
        self.all_sources = set()
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
            self.all_sources.add(entry.source)
            for s in sources:
                if s.lower() in entry.source.lower():
                    self.prd.append(entry)
                    break
            else:
                self.prd.append(entry)


class BestiaryApp(App):
    '''Pathfinder Bestiary search / output App.'''
    VERSION = '1.0.0'

    def init_parser(self):
        super(BestiaryApp, self).init_parser(description=__doc__)
        self.actions.choices['search'].add_argument('terms', metavar='<terms>', nargs='+')
        self.cmdline.add_argument('-i', '--input', metavar='<csv>', default='monster_bestiary.csv')
        self.cmdline.add_argument('-s', '--sources', nargs='*', default=['pfrpg', 'inner sea', 'irrisen', 'reign of winter', 'isles of the shackles', 'linnorm', 'golarion', 'magnimar', 'ap ', 'd20pfsrd'])
        self.cmdline.add_argument('-f', '--format', default='statblock', choices=['name', 'line', 'source', 'statblock', 'block'])

    def _byname(self):
        self.name_dict = OrderedDict((e.name.lower(), e) for e in self.prd)

    def _load_input(self):
        '''Parse csv file into Entry instances.'''
        self.parser = BestiaryParser()
        self.parser.parse_csv(open(self.config.input), self.config.sources)
        return self.parser.prd

    def _print_mobs(self, mobs, format):
        '''
        :param mobs: Sequence of Entry instances.
        :param format: One of the valid output formats.
        '''
        formatter = dict(
                name=lambda m: m.name,
                line=lambda m: '%s CR%s %s %s(%s)' % (m.name, m.cr, m.size, m.type, m.subtype),
                source=lambda m: '%-28s %s' % (m.source, m.name),
                block=lambda m: '%s\n' % (m.statblock(True, True), ),
                statblock=lambda m: '%s\n' % (m.statblock(), ),
                )[format]
        for mob in mobs:
            print formatter(mob)

    def _search(self, mobs, criteria):
        '''Filter mobs based on search criteria.
        :param mobs: Sequence of Entry instances.
        :param criteria: sequence of tuples (field, [term1, term2, termN]).
        :return: list of mobs matching search criteria.
        '''
        matches = list()
        for mob in mobs:
            # Must match all search terms.
            match = True
            for field, terms in criteria:
                if field == 'type':
                    field = 'subtype'
                for term in terms:
                    if term not in getattr(mob, field).lower():
                        # Match either subtype or type.
                        if field == 'subtype' and term in getattr(mob, 'type').lower():
                            continue
                        match = False
                        break
                if not match:
                    break
            if match:
                matches.append(mob)
        return matches

    def action_book(self):
        '''Output all entries.'''
        mobs = self._load_input()
        mobs.sort()
        self._print_mobs(mobs, self.config.format)

    def action_search(self):
        '''Output entries matching all search terms.'''
        criteria = list()
        # Pre-munge (lower, comma split) field term1,term2.
        for field, terms in zip(*[iter(t.lower() for t in self.config.terms)] * 2):
            criteria.append((field, [t.strip() for t in terms.split(',')]))
        mobs = self._load_input()
        mobs = self._search(mobs, criteria)
        mobs.sort()
        self._print_mobs(mobs, self.config.format)

    def action_sources(self):
        '''List all sources found in input.'''
        self._load_input()
        print '\n'.join(sorted(self.parser.all_sources))


if __name__ == '__main__':
    app = BestiaryApp()
    app.run()
