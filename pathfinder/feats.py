#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Feat selector/printer for Pathfinder RPG.

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

The following text is the property of Wizards of the Coast, Inc. and is Copyright 2000 Wizards of the Coast, Inc ('Wizards').  All Rights Reserved.

1. Definitions: (a)'Contributors' means the copyright and/or trademark owners who have contributed Open Game Content; (b)'Derivative Material' means copyrighted material including derivative works and translations (including into other computer languages), potation, modification, correction, addition, extension, upgrade, improvement, compilation, abridgment or other form in which an existing work may be recast, transformed or adapted; (c) 'Distribute' means to reproduce, license, rent, lease, sell, broadcast, publicly display, transmit or otherwise distribute; (d)'Open Game Content' means the game mechanic and includes the methods, procedures, processes and routines to the extent such content does not embody the Product Identity and is an enhancement over the prior art and any additional content clearly identified as Open Game Content by the Contributor, and means any work covered by this License, including translations and derivative works under copyright law, but specifically excludes Product Identity. (e) 'Product Identity' means product and product line names, logos and identifying marks including trade dress; artifacts; creatures characters; stories, storylines, plots, thematic elements, dialogue, incidents, language, artwork, symbols, designs, depictions, likenesses, formats, poses, concepts, themes and graphic, photographic and other visual or audio representations; names and descriptions of characters, spells, enchantments, personalities, teams, personas, likenesses and special abilities; places, locations, environments, creatures, equipment, magical or supernatural abilities or effects, logos, symbols, or graphic designs; and any other trademark or registered trademark clearly identified as Product identity by the owner of the Product Identity, and which specifically excludes the Open Game Content; (f) 'Trademark' means the logos, names, mark, sign, motto, designs that are used by a Contributor to identify itself or its products or the associated products contributed to the Open Game License by the Contributor (g) 'Use', 'Used' or 'Using' means to use, Distribute, copy, edit, format, modify, translate and otherwise create Derivative Material of Open Game Content. (h) 'You' or 'Your' means the licensee in terms of this agreement.
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
'''

import codecs
import locale
import textwrap
import sys

from collections import namedtuple, defaultdict
from itertools import islice

import app

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)


# raw csv
RawFeatTuple = namedtuple('RawFeat', [
        'id', 'name', 'type', 'description', 'prerequisites', 'prerequisite_feats',
        'benefit', 'normal', 'special', 'source', 'fulltext',
        'teamwork', 'critical', 'grit', 'style', 'peformance', 'racial',
        'companion_familiar', 'race_name', 'note',
        'goal', 'completion_benefit', 'multiples', 'suggested_traits',
        ])


class Feat(object):
    def __init__(self, id, name, description, prerequisites, prerequisite_feats, benefit, normal, special, source, types, feat_name):
        self.id = id
        self.name = name
        self.description = description
        self.prerequisites = prerequisites
        self.prerequisite_feats = prerequisite_feats
        self.benefit = benefit
        self.normal = normal
        self.special = special
        self.source = source
        self.types = types
        self.feat_name = feat_name


class FeatParser(object):
    def parse_mrt(self, mrt):
        def dooter(stuff):
            for bit in stuff:
                yield bit
        def by_section(mrt):
            section = list()
            for line in mrt:
                line = unicode(line.strip(), 'utf-8')
                if line == '=' * 80:
                    if section:
                        yield dooter(stuff=section)
                    section = list()
                else:
                    section.append(line)
            if section:
                yield dooter(section)
        def by_paragraph(section):
            prevs = [a_paragraph(section), ]
            while True:
                para = a_paragraph(section)
                if para.startswith('**'):
                    yield '\n\n'.join(prevs)
                    prevs = [para, ]
                elif para:
                    sys.stderr.write('append %s\n' % para)
                    prevs.append(para)
                elif prevs:
                    yield '\n\n'.join(prevs)
                    raise StopIteration
                else:
                    raise StopIteration
        def a_line(section):
            return section.next().strip()
        def a_paragraph(section):
            paragraph = list()
            for line in section:
                line = line.strip()
                # nuke leading blank lines
                if not line and not paragraph:
                    continue
                if line:
                    paragraph.append(line)
                else:
                    return ' '.join(paragraph)
            return ' '.join(paragraph)
        entries = list()
        for section in by_section(mrt):
            prerequisites = ''
            prerequisite_feats = ''
            benefit = ''
            normal = ''
            special = ''
            name = a_line(section)
            feat_name = a_line(section)
            id = a_line(section)
            types = a_line(section)
            if types:
                types = types.split(', ')
            for paragraph in by_paragraph(section):
                if paragraph.startswith('**Leads:** '):
                    continue
                elif paragraph.startswith('**Description:** '):
                    description = paragraph[len('**Description:** '):]
                elif paragraph.startswith('**Prerequisite_feats:** '):
                    prerequisite_feats = paragraph[len('**Prerequisite_feats:** '):]
                elif paragraph.startswith('**Prerequisites:** '):
                    prerequisites = paragraph[len('**Prerequisites:** '):]
                elif paragraph.startswith('**Benefit:** '):
                    benefit = paragraph[len('**Benefit:** '):]
                elif paragraph.startswith('**Normal:** '):
                    normal = paragraph[len('**Normal:** '):]
                elif paragraph.startswith('**Special:** '):
                    special = paragraph[len('**Special:** '):]
                elif paragraph.startswith('**Source:** '):
                    source = paragraph[len('**Source:** '):]
                else:
                    raise Exception(paragraph)
            feat = Feat(id, name, description, prerequisites, prerequisite_feats, benefit, normal, special, source, types, feat_name)
            entries.append(feat)
        return entries

    def parse_csv(self, csv):
        self.sources = set()
        self.types = set()
        entries = list()
        # islice == strip off csv header.
        for row in islice(app.unicode_csv_reader(csv), 1, None):
            feat = RawFeatTuple(*row)
            # Fix errors in source CSV.
            wrong = [
                    ('Point-Blank Shot', 'Point Blank Shot'),
                    ('Spell focus', 'Spell Focus'),
                    ('Close Quarters Thrower', 'Close-Quarters Thrower'),
                    ]
            for find, replace in wrong:
                if find in feat.prerequisites or find in feat.name or find in feat.prerequisite_feats or find in feat.description:
                    feat = feat._replace(
                            name=feat.name.replace(find, replace),
                            prerequisites=feat.prerequisites.replace(find, replace),
                            prerequisite_feats=feat.prerequisite_feats.replace(find, replace),
                            description=feat.description.replace(find, replace),
                            )
            # Expand/Change source CSV.
            if 'See Armor Proficiency, Light' in feat.benefit:
                feat = feat._replace(
                        benefit=feat.benefit.replace('See Armor Proficiency, Light', 'When you wear a type of armor with which you are proficient, the armor check penalty for that armor applies only to Dexterity and Strength-based skill checks.'),
                        normal=feat.normal.replace('See Armor Proficiency, Light', 'A character who is wearing armor with which he is not proficient applies its armor check penalty to attack rolls and to all skill checks that involve moving.'),
                        )
            types = list()
            if feat.type and feat.type != 'General':
                types.append(feat.type)
                self.types.add(feat.type)
            for type in ['teamwork', 'critical', 'grit', 'style', 'peformance', 'racial']:
                text = getattr(feat, type)
                if text == '1':
                    types.append(type.capitalize())
                    self.types.add(type.capitalize())
            # Rename "Armor, Light" to "Light Armor".
            if ',' in feat.name:
                parts = feat.name.split(', ')
                if len(parts) > 2:
                    raise Exception('wtf [%s]' % feat.name)
                feat_name = '%s %s' % (parts[1], parts[0])
            else:
                feat_name = feat.name
            entries.append(Feat(feat.id, feat.name, feat.description, feat.prerequisites, feat.prerequisite_feats, feat.benefit, feat.normal, feat.special, feat.source, types, feat_name))
            self.sources.add(feat.source)
        return entries


class FeatApp(app.App):
    '''Pathfinder RPG Feat search / output.'''
    VERSION = '1.0.0'

    def init_parser(self):
        super(FeatApp, self).init_parser(description=__doc__)
        self.cmdline.add_argument('-i', '--input', metavar='<csv or mrt>')
        self.cmdline.add_argument('-m', '--mrt', action='store_true', default=False, help='''Machine readable output''')
        self.cmdline.add_argument('--sources', nargs='*', default=['PFRPG Core', 'Ultimate Combat', 'Ultimate Magic', 'Advanced Player\'s Guide', 'Bestairy'])
        #'Peformance', 'Style', u'Grit', u'Monster', u'Combat', u'Mythic', u'Item Creation', u'Metamagic', u'Story', 'Critical', 'Teamwork', 'Racial', u'Monster, Combat', u'Achievement'
        self.cmdline.add_argument('--bad_benefits', nargs='*', type=str.lower, default=['hero point', 'bloodline'])

        self.cmdline.add_argument('--exclude_types', nargs='*', type=str.lower, default=[
                'achievement',
                'grit',
                'item creation',
                'monster',
                'mythic',
                'racial',
                'story',
                #'style',
                ])

        self.cmdline.add_argument('--bad_names', nargs='*', type=str.lower, default=[
                'additional traits',
                #'arcane',
                'blighted',
                #'bloody assualt',
                'bludgeoner',
                'bolstered resilience',
                'channeled revival',
                'channeled shield wall',
                'clustered shots',
                'cooperative crafting',
                'cosmopolitan',
                'crushing blow',
                #'deadly finish',
                #'deadly stroke',
                #'deflect arrows',
                'detect expertise',
                'dispelling fist',
                'dispel synergy',
                'disposable weapon',
                #'domain strike',
                'driver',
                'eidolon',
                'eldritch claws',
                #'elemental fist',
                'ensemble',
                'extra cantrips or orisons',
                'extra summons',
                'familiar',
                'feral combat training',
                #'final embrace',
                'guided hand',
                'gunsmithing',
                'hammer the gap',
                #'ki ',
                'leadership',
                'master craftsman',
                'moonlight summons',
                'music',
                'mystic stride',
                'nightmare',
                #'perfect strike',
                'preferred spell',
                'prodigy',
                #'prone',
                #'punishing kick',
                'quarterstaff master',
                'ray shield',
                'rebuffing reduction',
                #'rending claws',
                #'rending fury',
                'sea legs',
                'shapeshifter foil',
                'siege',
                'spell expertise',
                'spell mastery',
                #'splintering weapon',
                'split major hex',
                #'stalwart',
                #' stance',
                #'strong comeback',
                #'style',
                'sunder',
                'sunlight summons',
                'sword and pistol',
                'theurgy',
                'touch of serenity',
                'trick riding',
                #'tripping staff',
                ])

        self.cmdline.add_argument('--bad_prerequisites', nargs='*', type=str.lower, default=[
                'abundant step class feature',
                'alchemist archetype',
                'aura class feature',
                'aura of courage class feature',
                'aura of resolve class feature',
                'bane class feature',
                'bardic performance class',
                'bloodline',
                'bomb class feature',
                'bond senses class feature',
                'cunning initiative class feature',
                'detect alignment class feature',
                'detect evil class feature',
                'detect undead paladin class feature',
                'discern lies class feature',
                'discovery',
                'divine health class feature',
                'drunken ki class feature',
                'eidolon class feature',
                'expert trainer class feature',
                'familiar class feature',
                'flurry of blows class feature',
                'gnome',
                'grit',
                'hex class feature',
                #'ki pool',
                'lay on hands class feature',
                'leaping lance class feature',
                'magus',
                'mercy class feature',
                #'monk level',
                'monster lore class feature',
                'mystery class feature',
                'paladin spells',
                'revelation class feature',
                'shield ally class feature',
                'small size',
                'smite evil class feature',
                'sorcerer bloodline class feature',
                'spell recall class feature',
                'still mind class feature',
                'tactician class feature',
                'true healer class feature',
                'weapon expertise class feature',
                #'wild empathy class feature',
                #'wild shape class feature',
                'witch',
                'wizard school class feature',
                ])

        self.cmdline.add_argument('--only_types', nargs='*')

#search improved unarmed
#missing greater dispel magic

    def _filter_feats(self, feats):
        excluded = set()
        # TODO: change to using id
        feats_to_sources = defaultdict(set)
        for feat in feats:
            feats_to_sources[feat.feat_name].add(feat.source)
            if feat.source not in self.config.sources:
                #sys.stderr.write('Excluded %s for source %s\n' % (feat.feat_name, feat.source))
                excluded.add((feat.feat_name, feat.source))
                continue
            types = [t.lower() for t in feat.types]
            bads = [bad for bad in self.config.exclude_types if bad in types]
            if bads:
                sys.stderr.write('Excluded %s for type %s %s\n' % (feat.feat_name, bads, types))
                excluded.add((feat.feat_name, feat.source))
                continue
            lower_name = feat.name.lower()
            bads = [bad for bad in self.config.bad_names if bad in lower_name]
            if bads:
                sys.stderr.write('Excluded %s for bad name "%s"\n' % (feat.feat_name, bads))
                excluded.add((feat.feat_name, feat.source))
                continue
            lower_beni = feat.benefit.lower()
            bads = [bad for bad in self.config.bad_benefits if bad in lower_beni]
            if bads:
                sys.stderr.write('Excluded %s for bad beni "%s" %s\n' % (feat.feat_name, bads, feat.benefit))
                excluded.add((feat.feat_name, feat.source))
                continue
            lower_pre = feat.prerequisites.lower()
            bads = [bad for bad in self.config.bad_prerequisites if bad in lower_pre]
            if bads:
                sys.stderr.write('Excluded %s for bad prereq "%s" %s\n' % (feat.feat_name, bads, feat.prerequisites))
                excluded.add((feat.feat_name, feat.source))
                continue
        # Exclude any feat with prerequisites that are excluded.
        for feat in feats:
            if (feat.feat_name, feat.source) in excluded:
                continue
            prerequisites = [p.strip() for p in feat.prerequisite_feats.split(',') if p]
            for prerequisite in prerequisites:
                sources = feats_to_sources.get(prerequisite, None)
                if sources is None:
                    if '(' not in prerequisite:
                        sys.stderr.write('Prereq (%s) not found for %s, %s\n' % (prerequisite, feat.feat_name, prerequisites))
                    continue
                if all((prerequisite, source) in excluded for source in sources):
                    sys.stderr.write('Excluded %s for prereq %s %s\n' % (feat.feat_name, prerequisite, prerequisites))
                    excluded.add((feat.feat_name, feat.source))
                    break
        filtered = list()
        names = set()
        for feat in feats:
            if (feat.feat_name, feat.source) not in excluded:
                if feat.feat_name in names:
                    sys.stderr.write('Excluded %s for dupe name %s\n' % (feat.feat_name, feat.source))
                    continue
                names.add(feat.feat_name)
                filtered.append(feat)
        return filtered

    def _by_type(self, feats):
        '''mapping of type -> (feats, )'''
        types = defaultdict(list)
        for feat in feats:
            for type in feat.types:
                types[type].append(feat)
        return types

    def _by_prereq(self, feats):
        '''mapping feat -> (prerequsites, )'''
        def sortem(feats):
            stuff = defaultdict(int)
            for feat in feats:
                stuff[feat.id] = len(parents.get(feat.id, []))
            def _cmp(a, b):
                return cmp(stuff[a.id], stuff[a.id])
            return _cmp
        names = dict()
        ids = dict()
        for feat in feats:
            ids[feat.id] = feat
            names[feat.name] = feat
        prereqs = defaultdict(list)
        parents = defaultdict(list)
        for feat in feats:
            prerequisites = [p.strip() for p in feat.prerequisite_feats.split(',') if p]
            for prerequisite in prerequisites:
                beat = names.get(prerequisite, None)
                if beat is None:
                    sys.stderr.write('%s not found\n' % (prerequisite, ))
                else:
                    prereqs[feat.id].append(beat)
                    parents[beat.id].append(feat)
        return parents

    def _feat_ref(self, feat):
        return ':ref:`feat-%s`' % feat.feat_name.lower().replace(' ', '-')

    def _format_feat_rst(self, feat, names, trees):
        '''
        :param feat: FeatTuple
        :param names: list of feat names, for matching feat's prerequisites.
        :param trees: mapping feat.id -> (feats this feats leads to)
        '''
        def munge_it(prerequisites):
            foo = list()
            for prerequisite in [f.strip().strip('.') for f in prerequisites]:
                if ' or ' in prerequisite:
                    foo.extend(munge_it(prerequisite.split(' or ')))
                elif '(' in prerequisite:
                    stuff = prerequisite.split('(')
                    if len(stuff) > 2:
                        raise Exception('Too much stuff"%s", %s %s %s' % (stuff, prerequisite, feat.name, prerequisites))
                    foo.append('%s (%s' % (munge_it(stuff[0:1])[0], stuff[1]))
                elif 'Weapon Focus' in prerequisite:
                    foo.append(prerequisite.replace('Weapon Focus', ':ref:`Weapon Focus <feat-weapon-focus>`'))
                elif prerequisite in names:
                    foo.append(':ref:`%s <feat-%s>`' % (prerequisite, prerequisite.lower().replace(' ', '-')))
                elif prerequisite.lower().startswith('base attack bonus '):
                    foo.append('BAB %s' % prerequisite[len('base attack bonus '):])
                elif prerequisite:
                    foo.append(prerequisite)
            return foo
        type = '**[%s]** ' % (', '.join(feat.types)) if feat.types else ''
        bits = list()
        bits.append('.. source; %s' % feat.source)
        bits.append('.. index:: %(name)s (feat), Feat; %(name)s, %(type)s Feats; %(name)s' % dict(name=feat.name, type=type))
        bits.append('.. _feat-%s:' % feat.feat_name.lower().replace(' ', '-'))
        bits.append('')
        bits.append(feat.name)
        bits.append('-' * len(bits[-1]))
        bits.append(self.fill(type+feat.description))
        if feat.prerequisites:
            bits.append('')
            bits.append(self.fill('**Prerequisites:** %s.' % ', '.join(munge_it(feat.prerequisites.split(',')))))
        tree = trees.get(feat.id, ())
        if tree:
            bits.append('')
            bits.append('**Leads to:** %s.' % ', '.join(self._feat_ref(f) for f in tree))
        for special in ['benefit', 'normal', 'special']:
            text = getattr(feat, special)
            if text:
                bits.append('')
                bits.append(self.fill('**%s:** %s' % (special.capitalize(), text)))
        return '\n'.join(bits)

    def _rst_output(self, feats):
        wrapper = textwrap.TextWrapper(break_long_words=False, break_on_hyphens=False, width=80)
        self.fill = wrapper.fill
        feats.sort(key=lambda x: x.name)
        trees = self._by_prereq(feats)
        types = self._by_type(feats)
        for type in sorted(types):
            print '.. index:: %s Feats, Feats; %s' % (type, type)
            print '.. _%s-feats:' % type.lower().replace(' ', '-')
            print
            print type+' Feats'
            print '=' * len(type+' Feats')
            print ', '.join(self._feat_ref(f) for f in sorted(types[type], key=lambda x: x.name))
            print
        print '\n.. index:: Feats, Feats; Alphabetical Listing\n'
        print 'Available Feats\n===============\n'
        names = [f.feat_name for f in feats]
        for feat in feats:
            print self._format_feat_rst(feat, names, trees)
            print
            print

    def _mrt_output(self, feats):
        wrapper = textwrap.TextWrapper(break_long_words=False, break_on_hyphens=False, width=80)
        feats.sort(key=lambda x: (x.types, x.prerequisites, x.name))
        trees = self._by_prereq(feats)
        for feat in feats:
            tree = trees.get(feat.id, ())
            print feat.name
            print feat.feat_name
            print feat.id
            print ', '.join(feat.types)
            if tree:
                print
                print '**Leads:** %s.' % ', '.join(str(f.name) for f in tree)
            for special in ['description', 'prerequisites', 'prerequisite_feats', 'benefit', 'normal', 'special', 'source']:
                text = getattr(feat, special)
                if text:
                    bits = unicode.splitlines(text)
                    print
                    print wrapper.fill('**%s:** %s' % (special.capitalize(), bits[0]))
                    for b in bits[1:]:
                        print wrapper.fill(b)
            print
            print '=' * 80

    def main(self):
        parser = FeatParser()
        if self.config.input.endswith('csv'):
            feats = parser.parse_csv(open(self.config.input))
        else:  # Asssume Machine Readable Text.
            feats = parser.parse_mrt(open(self.config.input))
        feats = self._filter_feats(feats)
        if self.config.mrt:
            self._mrt_output(feats)
        else:
            self._rst_output(feats)
        sys.stderr.write('\n%i feats\n' % len(feats))


if __name__ == '__main__':
    FeatApp().run()
