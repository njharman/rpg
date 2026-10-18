rpg
===

Norm's collection of small tools and experiments for table top RPGs.
Created over many years, I don't remember what some of this stuff is...
Here mostly so I can point at it from my blog http://trollandflame.blogspot.com/

Contents
========

Generic
-------

``d``
    Command line dice roller; understands 3d6, d20+4, drop lowest, repeats.
``calendar.py``, ``calendar.style``
    Campaign calendar generator with watches and weather, as reStructuredText for rst2pdf.
``citynames.py``
    English sounding city name generator.
``encounters.py``
    "What are the monsters doing" encounter activity tables using monsters from OSE (stat free).
``hitdice.py``, ``hitdice.style``, ``hitdice.rst``
    Printable sheet of monster hit points to mark off during play, as reStructuredText for rst2pdf.
``jgislandgenerator.py``
    Island feature generator from Island Book 1.
``namegen.py``
    Context-free grammar random name generator.
``word_scramble.py``
    Simple word scrambler (for name generation).
``experiments/``
    Rule mechanic and probability experiments.
``marchingorder/``
    Browser page for arranging a party's marching order.
``rpglib/``
    Python library for ttrpg "things", imported as ``rpg``.


Dungeons & Dragons
------------------

``deathguard_maker.py``
    K'jorian Deathguard NPC generator (D&D 3.5). Used in my `Dirt Campaign <https://friendorfoe.com/rpg/campaigns/dirt/>`_.
``dmg_dungeon_generator.py``
    Random dungeon generator from AD&D DMG Appendix A.
``methodI.py``
    AD&D character ability score generation DMG Method I.
``methodIV.py``
    AD&D character ability score generation DMG Method IV.
``recruiting.py``
    What hirelings are available from my Wilderlands campaign.
``stock_dungeon.py``
    Room monster and treasure stocking by dungeon level, B/X or OD&D.
``sw_hoard.py``
    Treasure hoard generator from Swords & Wizardry Complete.
``tombgenerator.py``
    Tomb content generator from Dragon #9 "Tombs & Crypts".
``treasure.py``
    Random treasure generator for OD&D, OD&D + Greyhawk, OSE (Basic, Expert,
    and Advanced options) and AD&D 1e.
``grimoire/``
    Combined spell listings and PDF built from Labyrinth Lord AEC.
``menagerie/``
    Monsters from Swords & Wizardry and Tome of Horrors.


HackMaster
----------

``pcbackground/``
    Character background generator: heritage, siblings, social class, honor.


Rolemaster
----------

``rmu_chargen.py``
    Rolemaster Unified character stat generator.
``rmweather.py``
    Weather generator from RMFRP Gamemaster Law 16.0.


Setup
=====

`uv <https://docs.astral.sh/uv/>`_ manages the environment::

    uv sync
    uv run python treasure.py --help


License
=======

MIT, see ``LICENSE``. ``ogl_*.txt`` are the Open Game License texts covering the
OGL-derived content they accompany.
