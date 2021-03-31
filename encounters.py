#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

"""Extensive "What are monsters doing".

Content created by ktrey and used with permission

Original tables are available on their blog at
https://blog.d4caltrops.com/p/ose-encounter-activity-tables.html
"""

import random
import click

# from dice import d6, d12, d100

# CSIO
# 1 Attacked by Surprise
# 2 Attacked
# 3 Slanders / Insults
# 4 Question Characetrs
# 5 PROPOSITION
# 6 SPECIAL
#
# 1-4 Men (3 SL)
# 5 unusual
# 6 per-quarter
#
# UNUSUAL
# 1  troll
# 2  paladin
# 3  shadows
# 4  harpies
# 5  lammasu
# 6  giant
# 7  thief
# 8  wight
# 9  golem
# 10 wraith
# 11 blink dog
# 12 zombies
# 13 skeletions
# 14 dervicshes
# 15 illusionist
# 16 invisible stalker
# 17 mind flayer
# 18 dragon
# 19 priest
# 20 mage
#
# SPECIAL
# 1  spit on
# 2  dishwater
# 3  meathook
# 4  chamber pot emptied upon
# 5  clay pot hits
# 6  brik hits
# 7  runaway carriage
# 8  street caves
# 9  impress gang
# 10 were-rats kidnap
# 11 begger
# 12 drunks
# 13 messenger
# 14 performaer
# 15 lamplighter
# 16 buffon
# 17 vigilantes
# 18 town crier
# 19 fugitive
# 20 hypnotive
#
# PROPOSITION
# 1 challenge
# 2 search
# 3 task/mission
# 4 work offer
# 5 sexual
# 6 kidnap player
#
# noble
# 1 Sheriif
# 2 Knight
# 3 Genera
# 4 Gentleman
# 5 noble
# 6 noble
#
# common quarter
# 1 goblin
# 2 orc
# 3 orgre
# 4 bandit
# 5 dwarf
# 6 g. rat
#
# plazas quarter
# 1 sharper
# 2 begger
# 3 slaver
# 4 performaer
# 5 bard
# 6 mercenary
#
# seafront quarter
# 1 sailor
# 2 sailor
# 3 bucanner
# 4 pirate
# 5 sea capt
# 6 begger
#
# merchant quarter
# 1 robber
# 2 guard
# 3 merchant
# 4 merchant
# 5 merchant
# 6 merchant
#
# thieves quarter
# 1 apprentice
# 2 apprentice
# 3 footpad
# 4 robber
# 5 burglar
# 6 cutpurse


# What are monsters doing for each OSE monster.
wamd_data = """
Table: human, acolyte
Affixing leeches to foreheads and eyelids
Installing an ornate altar
Apoplectically searching for a relic mislaid
Interrogating an apostate
Arguing over constellations and their meanings
Joyfully jumping with linked arms over a fire
Auguring upcoming weather events by observing bat-flight
Leading tribute lambs to a local sacred monster
Baptizing an unwilling convert
Lugging a consecrated anvil
Begging for alms
Masquerading as members of a friendlier faith
Bleaching bloodstains from grimy vestments
Milking a hallowed nanny-goat
Bleeding from the palms over a colony of mushrooms
Mixing acrid body paints in ivory bowls
Blessing a batch of holy water
Nonchalantly mixing ink pigments
Bottling purple smoke from a burning brazier
Officiating the marriage of a serpent and a hen
Branding an initiate with strange symbols
Over-indulging in sacramental wines
Brewing an enormous kettle of holy tea
Parading around a painted horse skull
Burying a broken icon
Piling heretical tomes into a makeshift bonfire
Carefully tending to an "eternal" flame
Piously charring their fingertips in penance
Carving ominous stone masks
Prognosticating via the contents of owl-bear pellets
Casting holy symbols from molten metal
Pushing a wheelbarrow of natron for mummy-making
Celebrating a recent revelation come to pass
Putting the finishing touches on an effigy
Chasing after a runaway keg of ale, rolling away
Raking sand into complex geometric patterns
Chipping colored stones for mosaic making
Rapidly transcribing cricket chirps in a massive tome
Chiseling maledictions into a stone surface
Rehearsing the handling of venomous asps
Circling a sacrifice with torches raised high
Releasing sacred songbirds from tiny tin cages
Collecting suitably shaped sling-stones
Ritually removing all body hair
Consulting charred tortoise shells for divine guidance
Roasting a sow, salivating as they break a long fast
Defacing script on a stone from another religion
Roughly forming a grimacing golem from clay
Desperately repairing a binding circle as smog forms
Rubbing salve on sunburnt pates
Disinterring the skeleton of a suspected saint
Scattering strong-smelling ashes across a sacred circle
Dousing a burning bush
Self-flagellating with thorny flails
Dowsing for a spring to consecrate/desecrate
Setting the broken arm of a congregant
Dressing an indignant wolf as a sheep
Sifting the pyre remains that consumed a comrade
Drying garlands of pungent herbs
Signing a pledge outlining their vow of silence
Dunking a neophyte's head in a basin of water
Singing the feathers from fortune-telling poultry
Eating under-done eggs
Smashing expensive looking hourglasses
Engraving the hilts of maces with holy words
Smuggling apocryphal scriptures
Escorting an orphaned infant, dressed in red
Soaking up spilled lamp oil with spare scrolls
Excommunicating a corpse in papal regalia
Softly intoning a repetitive chant in dragon-tongue
Exorcizing opposing spirits
Solemnly swinging censers of acrid smoke
Fiercely debating doctrinal differences
Spreading blasphemous rumors
Fleeing from an inadvertently summoned fire elemental
Sprinkling holy water on a dying white ape
Flensing flesh from a body to skeletonize
Strewing moldering flower petals along a pathway
Fomenting a schismatic reformation
Sweeping silver shavings, a successful summoning
Forlornly burning the quills/writings of a departed brother
Taking turns inhaling a sacred smoke elemental
Frantically fanning a sneering iron idol
Tending a roiling cauldron of foul-smelling stew
Frugally melting candle ends into molds
Tossing enruned raven bones into air for divination
Gathering kindling to immolate a heretic
Totaling tithes in a tiny pile
Gleefully tattooing a screaming novice
Trepanning an elder to extract fleeting wisdom
Gorging themselves on stinking over-ripe fruit
Tuning macabre femur wind-chimes
Hammering dents out of shields
Tying ceremonial streamers around everything
Harvesting medicinal maggots from a bloated corpse
Warming wrinkled hands over a fragrant campfire
Hollowing out the horns of rams
Weary from a week-long pilgrimage
Hysterically attempting to re-ignite incense cones
Wincing as baby manticore spines are removed

Table: ape, white
Attempting to nap, rambunctious offspring vie for attention
Panicking - one of their number trapped in a snare
Bickering over the best bedding materials
Peeling thin strips of bark from tender trunks
Bounding gracefully across treacherous rocks
Piling uniformly sized stones into a pyramid shape
Brandishing flaming branches, but how?
Playing tug-of-war with a mastodon tusk
Brushing out scabs from a large, battle-scarred male
Preparing to smash open an enormous speckled egg
Call-and-response whistling over distances
Protectively cradling clingy newborns
Carefully picking prickly leaves off thorn-laden branches
Raising hue and cry after spotting a deadly snake
Caring for a suitably hairy infant dwarf
Rapturously back-scratching on a special boulder
Carrying around tattered tent fabric in their mouths
Raucously drunk on over-ripe stone fruits
Cautiously sniffing a bound sacrificial villager
Refusing to concede territory to rock baboons
Chewing on a root with medicinal properties
Repeatedly licking mineral-rich rocks
Clearing sharper stones from an area to bed-down
Rolling in rust-colored dust with contented grunts
Climbing a large tree with uncanny grace
Scaling a sort of spire, fending off giant dragonflies
Comparing the acoustics of different drummed trunks
Scattering foul smelling fronds to mask scents
Competing to see who can lift the heaviest stone
Scooping aside soil with powerful forelimbs
Cracking open hard seeds on stones flattened by centuries
Scraping special lichens from boulders with teeth
Daintily feasting on magical lice during grooming
Scything down grasses with a sharpened jawbone
Demonstrating a honed peeling technique to bored juveniles
Searching the area for a new dry den after a flood
Digging up tasty tubers with teeth-sharpened sticks
Seemingly sweeping the ground with leafy branches
Dragging spiked brambles to construct a crude fence
Selecting larger leaves for makeshift umbrellas
Driving away impetuous post-pubescent males
Sequentially admiring a shiny coin
Enthusiastically drumming on a hollow log
Shaking a skinny tree creating a rain of sharp nuts
Exchanging astonishingly complex hand gestures
Shifting a humongous log to serve as a bridge
Fascinated by a very frightened tortoise
Sizing up potential mates and selecting an alpha
Feasting on fat greasy grubs from a rotten log
Sketching perplexing designs on a patch of sand
Flinging feces at an embarrassed ogre
Sniffing a stranger to the troop disapprovingly
Flustered and swatting away blood-hungry flies
Snorting the spores from purple puffball mushrooms
Foraging for fruit for their neanderthal masters
Soaking rapturously in a warm spring
Gazing philosophically upon their reflections in water
Somberly mourning the death of an elderly cohort
Placing colored buds at the foot of a stone idol
Squabbling over a large sparkling stone
Gingerly removing moss from stylized ape-carvings
Squeezing hydration from damp mosses into mouths
Gnawing on fistfuls of foliage
Strategically bending brush into a crude lean-to
Greedily drinking with cupped hands from a pool
Sundering massive melon-like fruits
Hooting and laughing at splashed stones in water
Swinging on a large rusty chain of mysterious origin
Howling a strangely melodious song
Taking turns watching over napping companions
Hurling a large femur at the foot of an onyx obelisk
Tearing open the carapace of a giant ant
Idly sharpening claws on tough tree bark
Testing the depth of water with a long stick
Inquisitively circling around a new mother
Tossing a bleached orc skull to-and-fro
Investigating troubling tracks
Trying to tickle the sleeping alpha with a twig
Lazily floating leaves on the surface of water
Twisting open woody shoots for the tender heartwood
Leading a limping troop member down a steep incline
Uncharacteristically slurping marrow from bones
Lobbing large rocks at a cave lion
Uprooting shrubs and small trees angrily
Loudly chest-thumping at a rival troop
Using thin twigs to fish for termites
Lugging the broken bodies of goblins out of their territory
Violently hammering trees in a show of dominance
Making a glorious racket hitting a steel helm on a stone
Walking upright with armfuls of apples
Mimicking birdsong surprisingly well
Washing blood off white arm fur
Munching casually on juicy pink blossoms
Watching the young roll repeatedly down a hill
Nursing a member of the troop with a bad stomachache
Weighing the odds of raiding a humming hive
Ostracizing one of their number - cyclopean and horned
Wrestling a giant alligator
Painting unusual hand-glyphs with ochre mud
You could swear that they are sowing seeds

Table: human, bandit
A time-tested strategy - block the path with large tree trunks
Indistinguishable from circus performers, rob towns blind
Admiring a powerful new weapon - semi-trained elephant
Intimidating a gnome to appraise some purloined jewelry
Amusing themselves by trying on extravagant plumed hats
Inventing outrageous tales about narrow escapes from justice
An elf prince is proving to be a troublesome ransom
Irritable after breaking open a strongbox to discover rocks
Arguing over who should claim a dagger with a pearl/horn hilt
Keeping a ghoul at bay with burning torches
Assembling a care package of illicit gains for their home village
Lighting pitch-tipped arrows in a cast-iron camp stove
Barbequing a stolen calf over low-and-slow coals
Loading up mules to move to a more lucrative hideout
Beginning to suspect that one of their number is a devil swine
Looking to unload several crates of fine and exotic furs
Being lectured by a leader after stealing alms from a friar
Lugging splashing buckets of well-water and griping
Berating a scribe as he forges official-looking pardons
Making a killing selling colored water as magic potions
Bewitched by a local dryad, compulsively planting trees
Masquerading as nuns to catch their victims unaware
Bilking farmers by claiming a "magic" wand can create rain
Mixing foul things to make good on a promise to poison a well
Brushing their fine and obviously stolen horses
Moonlighting as mercenaries for a cruel local lord
Building a bonfire to destroy evidence
Nearly starving, their supply caches are spoilt
Celebrating a pagan holy day with a feast and dancing
Passing themselves off as the law with stolen uniforms
Cheering a wrestling match that will determine leadership
Paying child informants with sweets
Complaining about stale bread/moldy cheese for meals...again
Posing as travelers, in league with a corrupt innkeeper
Conspiring to turn their leader in for the bounty on her head
Raking through the remains of a burnt building, finding coins
Coping with the revelation that their leader is of royal blood
Regretting the kidnapping of a stubborn noblewoman
Counting protection-money from a local halfing community
Remarkably cosmopolitan, almost all demi-humans
Cursed by a cyclops for mutton rustling
Retrieving a petrified comrade after a run in with cockatrice
Cutting down an apprehended comrade from his noose
Returning from a successful fishing trip, impressive catch
Daring each other to drink thoul blood to gain healing powers
Running a successful ferry scam - customers are drowned
Debating how to safely fence a stolen skull (holy relic)
Salving burns after trying to open a stolen spellbook
Digging trenches to make an area more defensible from calvary
Seeking new leader, the hill giant in charge isn't very smart
Disguised as charcoal burners with pit traps all around
Seemingly oblivious that half of their band are zombies
Divvying loot from a recent raid on a tax collector's strongbox
Selling firewood to size up the coin purses potential victims
Dressed in holy garb, claim to have returned from a crusade
Sending a greenhorn recruit on a snipe-hunt
Dueling with shadows after a run in with the fair folk
Signing an uneasy treaty with a local thieves guild
Dunking a suspected spy to extract a confession
Singing loud and lewd sea-shanties, most are ex-pirates
Easily underestimated as all are beautiful young women
Soot covered faces, having just escaped a burning barn
Enrobed with staves and beards, make convincing wizards
Starting a conflagration to raze their hideout
Excellent axe-throwers to a one
Strategizing how to free their leader from a giant spider web
Extorting a local miller to smuggle contraband in grain
Studiously watching an archery demonstration by an elf
Fending off the flapping wings and stings of stirges
Studying the tracks of a mark that got away
Fiercely protective of their hapless kobold mascot
Suspicious of a new cleric after the prior's mysterious death
Fleeing from a haunted barrow they just tried to pilfer
Tapping a keg of purloined pilsner with great aplomb
Fomenting mutiny over garish matching uniforms
Teaching a captured goblin rude words
Fresh from robbing dwarf prospectors of their ore and gear
Test firing a stolen catapult and searching for suitable ammo
Gleefully waving burning wanted posters in celebration
Tossing some scrap metal to their caged pet rust monster
Glumly patching tent canvas after an overnight owlbear attack
Trading horseshoes for arrows with a herd of centaurs
Hands up and disarmed by hobgoblins working for the crown
Training hawks to snatch purses from wooden dummies
Hard to tell apart from all the other pilgrims in these parts
Trying to come up with a suitably flash name for their band
Having captured a rival bandit leader, holding a mock trial
Unconvincingly disguising the tallest as a minotaur
Hawking patent medicine, some of it actually works
Unknowingly led by doppelganger for the past three decades
Hollowing reeds for a daring amphibious raid across a moat
Using a scale model to plan an attack on a wizard's tower
Hopelessly lost after following a wil-o-wisp
Watched over by local pixies who defend them with pranks
Horribly hungover and broke from a three-day long carouse
Wearing finery and impersonating foreign nobility
Impersonating a trading caravan with a broken wagon wheel
Whiling away the hours gambling with dice
In cahoots with the local constabulary, who turn a blind eye
Willing to pay dearly for help dealing with a bounty hunter

Table: basilisk
Adeptly camouflaged by clumps of verdant moss
Hollowing out the side of a hornblende hill giant
Admiring their larder, stacked high with diorite dwarfs
Hooded like a cobra, drooling sizzling spittle
Assembling a noisy nest of perfectly sculpted fragile flint fronds
Idly swatting away tiny, dice-sized gelatinous cubes
Atypically frugivorous, admiring their pile of petrified fruits
Investigating droppings of a rival in their territory
Battle-scared from a recent run-in with skeletons
Just roused from hibernation and positively famished
Beginning to brumate, and yawning constantly
Lapping up a broken philter of love, yikes
Being "fang-milked" for potion reagents by a blindfolded alchemist
Last of their sub-species - speckled with several ruby scales
Belching contentedly over a column covered in teeth marks
Licking cinnabar inclusions in a piece of granite goat
Bellowing loudly, tail caught in a trap
Locked in deadly combat with a griffon immune
Bemused by a skittish giant mole
Morosely sniffing a petrified potential mate
Bickering with itself - a very rare and deadly two-headed variant
Nibbling on a pumice pixie, grimacing at the funny taste
Bit of more than they could chew - those are caryatid columns
Noshing on a gneiss gnome champion
Bleeding from several javelins still stuck in their scaly hide
Nuzzling a large gem, set in a scepter
Breakfasting on a kimberlite kobold
On hind legs, struggling to reach a travertine pterodactyl
Carefully coaxing a bloated toad onto a hen's nest
Overindulging on a cache of fossilized ammonites
Charmed permanently by a mishap, seeking a wizard-friend
Pinned under a petrified pachyderm
Chased by a mob of mongooses, naturally immune
Plagued by itchy tufts of colorful, scale-hungry lichen
Chomping on a calcified cave locust
Playing 'possum to surprise prey
Coiled atop a half-eaten stone wyvern
Proudly frilled like a styracosaurus, but molting slightly
Conversing slowly in halting medusa with a lizard man shaman
Rattling loudly, this variant has an interesting tail
Craving silence - glancing at birds who fall and shatter
Relaxing in a hot-spring fed fountain
Crunching on sheets of slate like peanut brittle
Rubbing barnacle like parasites from their hide
Crushing limestone pebbles with flat back-teeth
Sapped in strength from a run in with sadistic shadows
Daydreaming of eons past, when the world was ruled by the scaly
Sharpening their massive horn on a natural whetstone
Dining on quartz quasit
Shuffling about, blind in one eye due to green slime
Distended belly from devouring a herd of asbestos sheep
Sitting patiently for a sketch by a brave (or stupid) sage
Distending jaws to swallow a bulbous giant beetle whole
Slithering throughout a warband of petrified orc warriors
Dragging around a chert ram with a scraping sound
Slurping up a muddy slurry of wet sandstone slugs
Especially swift from a recent bask, hunting
Smashing a mirror into silver slivers with satisfaction
Eyes firmly shut and circling each other, males square off
Snacking on crumbly chalk chipmunks
Face covered with intumescent stirges, scratching at them
Somehow crowned with a fragile diadem of plant control
Famished, escaped medusa pet, muzzled to prevent ruining art
Struggling with the spines of a porphyry porcupine
Feasting on a creamy white marble sculpture of a satyr
Supping on an obsidian svirfneblin
Feigning slumber unconvincingly with too-rhythmic snores
Swallowing an olivine elf, head-first
Fiercely protecting a clutch of sparkling geode-like eggs
Tainting a water source with venomous secretions
Fireball blasted and especially ornery
Tangled in noisy iron fetters
Fitted with special saddle and tack for lizard men riders
Tenderly carrying squirming hatchlings in mouth
Flummoxed by a terra-cotta living statue of a soldier
Testing the air with an ultramarine forked tongue
Fortunately, has somewhat cloudy eyes due to upcoming ecdysis
The stone lion ate a hungry poet, but is now being eaten
Gifted with sibilant speech by a grateful henge druid
Trained to find choice marble, leash-led by dwarf masons
Gnawing at the rippled base of a stalactite like ice cream
Unsuccessfully attempting to sneak up on a bear
Goaded by enterprising ghouls who sale very lifelike sarcophagi
Waiting patiently for a gargoyle to groom him
Grunting as they receive belly scratches from a gauntleted goblin
Wary of men, escaped from a sculptor of renown (a fraud)
Gumming the wings of an alabaster aarakocra
Well-fed and fattened by local cultists for a grand sacrifice
Harangued by blessedly blind bats
Widening a burrow with powerful hind claws
Has a hitchhiker - a symbiotic grey ooze rides on their back
Worshipped by lizard men, who leave tail-tips as offerings
Hauling a hematite hafted halberd toward her hoard
Wounded by now petrified jewel thief nest robbers
Helping young teeth on a basalt horse leg
Wrapped around a stone altar covered in nibble marks
Hissing loudly at a resilient team of halfling slingers
Wrinkling their snout after a strong whiff of weasel urine
Holding court over all manner of slithering snakes and serpents
Yanking the shield off the arm of a miserable myrmidon

Table: bat, giant
Adopted and protected by local townsfolk, seen as good omens
One inadvertently swallowed a wand, and belches green fire
Being studied by an inventor who seeks their secret of flight
Pampered by a local goblin bat-cult
Capable of an incredible racket if disturbed by light sources
Returned from an unsuccessful hunt and still hungry
Carrying off a helpless halfling child
Roused from slumber to come to the aid of a nearby vampire
Chittering defensively after spying dwarf guano prospectors
Scattering at the cry that sounds like a giant eagle
Divebombing a giant toad
Scavenging on large insects drawn to the corpse of a hippogriff
Dogfight with giant killer bees
Squabbling over the choice bits of a giant spider carcass
Drinking greedily from a water seeping
Stunning their robber fly prey with subsonic chirps
Driven from their roost by green slime, seeking a new home
Suckling pale pups, the size of an infant
Grooming fastidiously with sour smelling spittle
Suspended over a heap of guano bearing toxic mold
Gulping down some very large rats
The claws of this species are easily confused with dragon teeth
Harassing a hapless farmer, armed only with a pitchfork
Unhappily sharing their home with a noisy owlbear
Have somehow acquired a taste for ghoulflesh, and feasting
Used as mounts for lamp oil flinging kobolds
Lazily hanging upside down, seemingly unbothered
Wing bones make flutes that play eerie melodies
Narrowly avoiding the strike of a giant snake as they take flight
Wing-leather is prized by enchanters and spell bookbinders

Table: bat, giant vampire
After drinking dragon blood, possess weak breath weapons
Held at bay by a terrified dwarf waving a poleaxe
Bearing potbellies after draining a whole herd of sheep
Hunched awkwardly over an unconscious cleric
Bred as blood banks for a vampire vivimancer, explode when hit
Inflicted by mange, their furless, naked bodies more terrifying
Circling a stone font full of bubbling vermillion liquid
Keeping their distance from a large stone holy symbol
Clucking contentedly toward the moon
Lapping scarlet trickles from a sleeping mule
Docile and complacent after being charmed by harpy song
Migrating for a semi-annual mating ritual
Domesticated by a dark sect, willingly bit in hopes of turning
Mourning their matriarch, staked by mistake
Drooling over a dead deer
Once kept as pets by an eccentric elf, still know a few commands
Drunk after drinking from a dryad
Orcs prize their guano for burning in special ceremonies
Eerily albino, with blazing red eyes and bloodstained chins
Protective of an obese ogre they feed from frequently
Engaged in a turf war with a local sting of stirges
Relentlessly guarding a coffin, empty save a layer of soil
Extremely antagonized by the sound of church bells
Resting, engorged, atop a desiccated cow
Granted minor regenerative powers from a diet of troll blood
Seeking a shady spot to shy away from sunlight
Harrying a healer who seeks their saliva as an anti-coagulant
Skittish after a run in with a warhorse shod in silver shoes
Have learned to douse torches with their prodigious spittle
Stuck in an enormous web, as a huge black widow approaches

Table: bat
Attaching coins to the surface of the ceiling with adhesive spittle
Indispensable for keeping the shrieker population down
Attracted to light and surprisingly flammable
Known to cache sharp stones in niches to drop on invaders
Barbed bats - covered in sharp spines beneath their fur, don't grab!
Make excellent familiars, rumored to smell magical items
Blessing bats - patches on fur resemble holy symbols
Necromancer's friend - swarm can strip corpse to bone in turns
Blossom headed - hangs with sweet breath, insects come to them
Ooze drinkers - strangely immune to most common oozes
Burglar bats - wing bones make excellent lockpicks
Prized for their thick, black, darkvision resistant fur
Covered in white dust, fungal zombies really
Riven with rabies, the foaming fever
Distantly related to bugbears, these bats are eerily silent
Selectively elf-bred as messengers, can learn word each
Drawn to dwarfs for warmth, make adorable sounds/nuzzle a lot
Sentries for a bona-fide vampire, they report to their master
Due to a quirk, can speak to gnomes, but are very chatty/annoying
Serve as mounts for neanderthal like cave pixies
Echolocation can cause harmless nosebleeds in halflings/gnomes
So noisy, most denizens of the area avoid this place
Excreting constantly, their droppings burn the eyes and throat
Strangely bioluminescent (dull orange) when they sleep
Fox headed frugivores, fling sticky rotten fruit at interlopers
Surprisingly delicious, many explorers saved from starving
If exterminated or displaced, local crops will fall to blister locusts
Their guano is in high demand for alchemical purposes
If followed may reveal a surprising route out of the area
Through strange magical mishap, these bats have scorpion tails

Table: bear, black
Cautiously sniffing a baited deadfall
Making short work of a group of goblins
Chasing after a blonde child
Recently wakeful after hibernation and hungry
Companion of a local were-bear, patrolling
Searching sullenly for a ranger companion
Eating a dead elk/reindeer while wolves circle
Soft-spoken, gifted speech by a local druid
Intrigued by a scent, nose to the ground
Trying to dislodge an arrow from their shoulder
Coaxing cubs to come down from a shipsinger tree
Investigating a suspended snare containing a deer
Decimating a darkberry bush, covered in tiny burrs
Munching loudly on fallen cellarnuts
Escaped circus performer, just wants a hug
Scaling a tall tree to paw at a buzzing beehive
Gouging tree bark to mark a boundary
Shimmying back-and-forth on a rough rock to scratch
Habituated to the local halfling population, friendly
Slapping the ground to frighten a porcupine

Table: bear, cave
Cautiously sniffing a baited deadfall
Making short work of a group of goblins
Chasing after a blonde child
Recently wakeful after hibernation and hungry
Companion of a local were-bear, patrolling
Searching sullenly for a ranger companion
Eating a dead elk/reindeer while wolves circle
Soft-spoken, gifted speech by a local druid
Intrigued by a scent, nose to the ground
Trying to dislodge an arrow from their shoulder
Crunching marrow-rich mastodon bones
Roaring at a rival male, teeth bared and bloody
Defending a giant sloth meal from hungry ravens
Rolling large boulders down a slope
Dragging a dead neanderthal
Searching for a new den, after being displaced by a dragon
Locked in combat with a sabre tooth cat
Slapping away a pack of hungry wolves
Pin-cushioned with stone-tipped spears
Snorting loudly over bloodstained tracks

Table: bear, grizzly
Cautiously sniffing a baited deadfall
Making short work of a group of goblins
Chasing after a blonde child
Recently wakeful after hibernation and hungry
Companion of a local were-bear, patrolling
Searching sullenly for a ranger companion
Eating a dead elk/reindeer while wolves circle
Soft-spoken, gifted speech by a local druid
Intrigued by a scent, nose to the ground
Trying to dislodge an arrow from their shoulder
Absolutely wrecking an orderly campsite
Receiving woven baskets of berries from berserkers
Bending down branches of devil pear trees
Ripping open a rotten log to reach tasty dire grubs
Devouring a mountain goat as a fox watches intently
Snatching salmon from a stream
Foaming mad, caught in a steel-jawed trap
This man-eater has developed a taste for manflesh
Huffing loudly in a standoff with dwarfs
Two curious cubs, angry protective mother nearby

Table: bear, polar
Cautiously sniffing a baited deadfall
Making short work of a group of goblins
Chasing after a blonde child
Recently wakeful after hibernation and hungry
Companion of a local were-bear, patrolling
Searching sullenly for a ranger companion
Eating a dead elk/reindeer while wolves circle
Soft-spoken, gifted speech by a local druid
Intrigued by a scent, nose to the ground
Trying to dislodge an arrow from their shoulder
Bounding after an ice-bound walrus
Isolated on an ice float, resting from a long swim
Chewing chunks of rancid flesh, a beached narwhal
On patrol for frost giant keepers
Clawing a hole into the thinnest part of the ice
Pulling a sledge, loaded with the warlike rime elfs
Crunching through the shell of a giant crab
Ravaging a seal with a blood-stained snout
Dragging a large fish to just weaned cubs
Sliding down snowy slopes for amusement

Table: beetle, fire
A fascinating sub-tribe - nodule glow illuminates secret doors
Nervous from the undetectable odor of gelatinous cube
Attracted to a foul-smelling cave blossom's pollen
No apparent glow, glands work in the infrared spectrum
Battling for mates/territory by yanking on each others legs
Nosily nosing through leaf litter
Capable of making loud clicks that startle predators
Pulsating contentedly as they sniff around a giant rat carcass
Circling defensively around a glowing glove
Repeatedly stumbling as they try to scale a smooth surface
Combing through debris for tasty toadstools
Romantic attraction to torchlight leads to confused males
Extremely well-fed, nodules glow for twice as long
Scraping slimy mold from atop a pyramid of skulls
Feeding on tasty oil beetle larvae
Shoving detritus into cozy piles as part of the nesting process
Flashing a heliographic warning to predators
Skittish and likely to flee to the ceiling and disturb the bats
Gnawing lichen off a large timber, possibly structurally important
Unbelievably docile, fitted with harnesses for portaging gear
Greedily devouring a pile of lumpy, rotten, etrogs
Unexpectedly alighting in very clumsy, collision-course flight
Ignoring a clutch of glowing eggs, the size/shape of watermelons
Unstartled by shrill shouts of shriekers as they snack
In the glow of their glands, magic is undetectable by detect magic
Using forelimbs to drink dew from twitching antennae
Lugging luminous larvae to a new food source after a recent flood
Wounded by rats and leaving a trail of glowing spatters
Meticulously munching mushrooms with mesmerizing mandibles
Zombified and aggressive due to parasitic giant wasp larvae

Table: beetle, oil
Being taunted by blink dog pups - someone's going to get hurt
Recent sprays have revealed strange carvings on the walls
Blindingly bright in infravision due to their chemical reactions
Ripping soggy chunks from a decaying log in search of grubs
Burrowing to escape a hungry giant toad
Roped/wrangled by soldiers, devastating new siege weapon?
Circling a magic-user with dagger, face covered in large pustules
Secretions of this species turn to toxic fog on air contact
Civilly sharing a fighter's corpse with a rust monster
Semi-tamed by an inquisitive alchemist, expect food now
Coaxed by powerful pheromones to guard area with their lives
Slurping up rope-sized worms like spaghetti
Cornering a cave locust, moments from spraying
Sought by beggars, as blisters make marks more empathetic
Devouring a robber fly with gusto
Startled by a breeze-blown cloth, spraying uncontrollably
Erupting up from the ground, on the hunt
Successfully blinding a hungry giant gecko
Flustered that their defense seems to fail against giant slugs
Surprising parents, dragging a dead giant bee to larvae
Injured from the recent raid of a giant ant mound
Tearing strips of flesh from the corpse of a kobold
Knocking over barrels of brine and pickles and feasting
The spray of this sub-tribe - like napalm if it encounters flame
Lapping at sap from thick, gnarled roots
Traipsing victoriously over a pile of scorched zombies
Patrolling a potential nesting ground
Tunneling carefully, their diggings lead to a new area
Preparing to defensively spray at a curious giant ferret
Twitching in a giant spider's web to an unblinking audience

Table: beetle, tiger
Antagonized by a column/tree trunk, continue to try and crush it
Occasionally raced for sport by denizens of the dark
Begrudgingly tolerating each other as they rest
Parading around a twitching treant limb
Chasing down a crab spider with spectacular speed
Reeling from a swift mule kick, but closing in
Clicking huge mandibles, could bisect an ogre at the torso
Ripping a weaker beetle limb from limb
Collared with heavy iron chains, but alert and angry
Scrambling to escape from a hungry rhagodessa
Devouring a huge caterpillar, can't help but imagine the butterfly
Shimmering iridescent green, might reflect some magics
Fast fliers, accompanied by a deafening buzzing sound
Staking out a path frequented by driver ants
Garishly striped, shells sometimes used as shields
Stock still and peering at shadows with bulbous eye stalks
Gobbling an unlucky goblin
Tamed as guard beetles, gnomish miners prospecting nearby
Hated by local shepherds, they've developed a taste for mutton
Thwarted by a defensively curled giant pill bug
Ignoring and ignored by a group of skeletons patrolling
Tug-of-war over a terror-stricken troglodyte
Jerking violently to escape a constricting giant centipede's sting
Undeterred by the flailing tentacles of a carcass crawler
Laying long, sticky eggs in oddly uniform divots
Very odd, trying to communicate/writing - polymorphed cleric
Mate-guarding to discourage other suitors
Voraciously gorging on robber fly larvae
Oblivious to larval burrows - fanged grubs ambush non-beetle prey
Wrenching the fortunately greaved leg of a desperate dwarf

Table: human, berserker
Act completely in concert without speaking
Laying out the body of the dead, on bearskin
All bearing the same bat-shaped scars on their faces
Led by a vengeful banshee, all women
Arguing over interpreting a treasure map
Listening intently to a druid's parable
Assembling cowhide yurts in record time
Loudly uttering oaths
Attack elfs on sight - they resemble an evil deity
Making quick work of a tun of purloined wine
Bedecked in bull imagery/decorations
Melting silver coins into ingots for transport
Braiding long, beautiful hair prior to battle
Might want to keep a wide berth - gorgon rodeo
Branding a young initiate on the ribs
Negotiating a toll with hobgoblins, growing testy
Breaking the bows of a defeated elf patrol
New converts to a lawful faith, have questions
Buying pilfered grain from orc brigands
Not to be trifled with - carving up purple worm steaks
Carrying armfuls of firewood to build a pyre
Orienteering with a primitive lodestone
Carving eerie owl totems of all sizes
Painfully implanting wyvern-scale under skin
Celebrating a successful razing of a monastery
Painting hallucinogenic pigments on their bodies
Chanting hymns in the language of the dead
Passing around a chimera heart and taking bites
Cloaked in sabre-tooth tiger pelts
Playing an ornate board-game
Cloud-gazing and interpreting auspicious signs
Preparing offerings for a local storm giant
Convincing a skald to play a jawbone kantele
Previously prisoners, still bear iron bracelets
Defending a barrow from tomb-robbers
Protected by pet panthers
Different tribes, rallied under the same standard
Pulling the arm off a troll in a pool
Donning crocodile leather armor
Receiving marching orders from a rhyming raven
Drawing lots for guard duty
Recently lost horses to a griffon attack, sullen
Dressed with complete disregard for temperature
Reciting exaggerated family histories
Drinking water out of wolf-prints
Reduced in number after a bugbear ambush
Each seems to be tattooed with a large python
Relaxing with mastodon tusk scrimshaw
Eager to upgrade crude weapons, have pelts to trade
Revering a statue of an owl bear
Eerily silent even in the grasp of frenzy
Riding giant tuatara
Enthralled by a local dryad who grows bored with them
Roasting a brace of hares, smells delicious
Erecting triceratops-hide tents
Rubbing an amber amulet for luck
Feeding a fire with parchment and scrolls
Salting fillets of fish to preserve them for a journey
Fighting each other, their goblin foes defeated
Saluting a bear skull atop a tree
Filling waterskins for a long journey
Seeking to reclaim an ancestral hoard from a dragon
Fleeing the undead blight that plagues their homeland
Sheepishly hammering teeth marks from shields
Foggy and lethargic, post-frenzy
Slathering grizzly bear fat on hair, beards, and bodies
Foraging for a particularly frenzy-friendly fungus
Soundly besting an npc adventuring party
Girded in warm, bearskin breeches
Spear throwing contest
Goading two dogs to fight over a tied hare
Stampeding elk off a cliff
Gouging angular runes into a stone surface
Stringing beads that commemorate kills
Grinding herbs with a skull mortar and bone pestle
Superstitiously terrified of displays of magic
Gutting a ten-point buck with dirks
Taking turns snorting an acrid yellow powder
Hailing from the sea on dragon-shaped ships
Tenderly caring for a cutting from the world tree
Happily dying at the draining touch of a wight
Testing their mettle by taunting a ghoul
Harvesting globular roe from a giant sturgeon
Their elderly matriarch is the most potent fighter
Heating buckets of pitch over a fire
Tracking a family of wild boars
Honing blades with whetstones in unison
Trade in trained rocs, jealously guard eggs
Howling gleefully like wild animals
Transporting a mummy to an ancestral burial ground
Huddled for warmth around a sickly fire
Treat dwarfs as divine beings
Hunting a warp beast as a rite of passage
Wearing wolf-pelt headgear
Hysterically laughing in bitter incense smoke
Well-spoken and civilized until angered
Intentionally trying to contract lycanthrope
When enraged, eyes "glow" a baleful black
Lamenting the loss of an infant to illness
Worshiping a weird spider god

Table: black pudding
Accumulating bleached bones, poking at odd angles
Falling in fat droplets, only to meld like mercury
Adhering in an inky blot on a ceiling mural of the heavens
Fattening up on writhing cave locust larvae
Beating like a heart as it clings to an archway
Flooding the floor of a corridor from wall-to-wall
Bloated to bursting and seeking injury in order to split
Overflowing from a pit, about a spear-length wide
Bulging like a greasy oil bubble from a stone font
Plumping prodigiously as it senses a heartbeat
Coagulating into a large globule with slurps and plops
Quaking its way around a profanely carved pillar
Disintegrating a sturdy table and chairs by drawing them in
Recoiling from a floor-strewn, burning torch
Distending across a doorway to trap a fleeing kobold
Rippling rhythmically as the dwarf inside it struggles
Enveloping an unconscious elf in finely woven chain
Shivering as it slides slowly up a wall toward a window
Eroding through a cast-iron ceiling grate
Undulating beneath a ceiling of screaming bats

Table: green slime
Brimming up from a fish-themed fount
Leaking down from a crack in the ceiling
Cascading down an open passageway in slimy sheets
Oozing over the body of an orc
Clotting on contact with a lit torch sconce
Quivering, seemingly embedded with tiny shells
Congealing slightly in the chilly air
Sliding down from the top of a doorway
Corroding the metal chains that support a bridge
Soaking a partially burned cleric
Crackling on contact with a chalky powder on the floor
Sticking to a frenzied berserker, about to self-immolate
Dribbling in gooey smears over a devil face carving
Streaming down onto a heavily decorated chest
Flowing from cistern spigots in phlegmy gobs
Swathing a gem-studded scabbard, sword useless
Gliding towards an unsuspecting perched carcass crawler
Trickling down the back of the neck of a medium
Gushing out of a loose piece of masonry
Weeping from the opal eyes of a living statue

Table: grey ooze
Breaking down an ornate magic helm, slowly
Mimicking the molding at the base of a wall
Coating the jambs of a doorway, hinges smoking
Perfectly camouflaged in a clear cave pool
Constant trembling betrays its stony guise
Pitting the surface of a silver shield
Exuding medicinal smelling liquids as it digests
Scouring a crypt niche sparkling clean
Flowing beneath a locked and barred door
Seeping from a ceramic drainpipe
Grinding down the remains of a goblin bodyguard
Sizzling with several javelins sticking out of it
Indistinguishable from a pebbly and treacherous floor
Sluicing slowly down a gutter, feeding on moss
Liquifying to drip through a sealed trapdoor
Sweeping up leaves as it skates along the flagstones
Lurking beneath damp bolts of cloth, corner stacked
Throbbing contentedly on the back of a gargoyle
Masquerading as the cornerstone of an archway
Uncannily blending into a bas-relief of barbarians

Table: ochre jelly
Conforming inside a cauldron, beginning mitosis
Pouring out of a wall mounted fountain
Convulsing as it consumes a kobold trap-smith
Roiling in waves to cross uneven terrain
Destroying what's left of a mattress and bed
Sputtering as it inadvertently oozes over a flame
Dissolving a door, down to its hinges and bands
Squeezing itself into a sarcophagus
Drawn to a dripping sound from the ceiling
Stuck to the still warm body of a dead mule
Extruding itself through a shiny keyhole
Surging swiftly towards a troll
Flattening to fit through a crack revealing a secret door
Swelling in defense from a gout of chimera fire
Gurgling as it engulfs a flailing ghoul
Tattering the bottoms of valuable tapestries
Impaled by a spike trap, unharmed and throbbing
Tumbling from a tall bookshelf, burned through
Melting through leather straps that secure a boulder
Unmaking an armoire from the inside out


Table: yellow mould
Asphyxiating a band of unfortunate bugbears
Latest fashion for gargoyles - startling saffron body art
Blighting a once beautiful statue of a nixie maiden
Only starting to spread onto a wood golem warhorse
Blooming with tiny purple polyps that smell of butter
Protruding slightly, on the pages of a large tome
Choking the mining gnomes who broke through a wall
Puffing an anemic mist - ignored by skeletons marching past
Completely carpeting several leaky glass flasks of lamp oil
Pulsating gently as the bodies of several hobgoblins decay
Dilating from the heat of a passing fire elemental
Releasing puffs, perfectly timed with a minotaur's cough
Efflorescing with sheets of sickly spores
Shuddering as masked dwarfs char the edges from a door
Emanating from zombies that spread it throughout
Slowly eating a thief's magnificently tooled leather armor
Healing mushrooms depend on its prey for sustenance
Teeming with carcass crawler larvae, symbiotic
Incrusting a thick iron portcullis, the only way forward
Weakening wooden supports that hold up the ceiling here

Table: blink dog
Accepting a string of sausages from a trader
Listening politely to a curate's sermon
After generations, have turned local kobolds lawful
Looking to unseat a local despotic leader
Aiding a kind-hearted medium, locating a lost familiar
Lugging an unconscious and corpulent friar to safety
Allied with a nearby werebear
Mediating between two rival neanderthal clans
Arranging mirrors to reflect sunlight into a crypt
Mirthfully annoyed at a pleasure of pixies
Attempting to save a man pinned under a rock
Monitoring a merchant, to ensure deals are fair
Baying somberly at the death of a packmate
Morosely masticating spear hafts
Bearing silver capped canines to help hunt werewolves
Nervous about new neighbors - a salamander clan
Begrudgingly working with a wishy-washy ranger
Nipping at the heels of a desperate ogre
Being groomed by a very nervous acolyte
Panting after treeing a warp beast
Beleaguered by cold iron collars that prevent blinking
Participating in a dizzyingly fast game of blink fetch
Biting through the ropes that bind an innocent man
Paying a visit to a reformed doppelganger
Blinking into a body of water, returning with fish
Playing "keep-a-way" with a large, silvered mace
Bounding after skeletons, salivating heavily
Positively prehistoric - wolves that go melt into earth
Burying a cursed axe
Rabid, and seeking a merciful death
Can bestow "blinking" for week with a lick (and a geas)
Reinforcing a squire trying to defend his fallen master
Carrying a birch-bark plea for a treant in need
Ruefully regarding hellhound tracks in their territory
Chewing blasphemies off a squat stone stela
Running carefree, "bamfing" through obstacles
Comforting a young lady, fleeing forced betrothal
Scouting ahead for a group of penitent pilgrims
Corrupted by a collar of alignment change
Searching for a way to destroy a vile spellbook
Curled up at the foot of a saint's tomb
Seeking to purchase books on justice for their collection
Defending an ossuary containing a holy blade
Seen as a good omen by local villagers
Digging a spartan den
Serving as suitable foils for a local wicked bandit king
Disdainfully treating with druids
Shadowing a suspected necromancer
Distrustful of flighty elfs after a recent bad experience
Shaken and shivering after encountering a spectre
Dragging a spilling sack of silver to tithe
Silently judging a trial by combat between gnomes
Drooling over a tablecloth covered in fancy cakes
Slowly circling a giant rattler
Eagerly lapping holy water from a silver bowl
Snarling at a gargoyle, flying just out of reach
Ears alert to the sound of a distant whipping
Snatching a belt pouch from a wicked tax collector
Enjoying liturgical music from a shy bard
Soliciting someone to light a carried torch - fire went out
Escorting two abandoned, orphan children from danger
Spelling out words with carved ivory sticks
Fetching water in an engraved silver tea kettle
Spying on a local witch, unsure of her intent
Fiercely protective of a local halfling hamlet
Stalking an orc patrol
Fighting a mountain lion alongside a mule
Standing guard over a unicorn mare foaling
Fleeing from a wraith, warning with barks
Stranded atop a boulder by a huge insect swarm
Gathering wildflowers to leave on graves
Stretching after a satisfying nap
Gnawing on the bones of a ghoul
Struggling to rescue a snared pup too young to blink
Good-naturedly startling a herd of jackalope
Taunting a group of zombies - playing with their food
Growling at a ghost they can't seem to harm
Temporarily allied with hobgoblins vs a vampire threat
Guarding the bones of a high priest
Trying to reunite a knight with his lost magic spurs
Guiding dervishes to a clean water source
Tymenes, the centaur foal, has fallen down a well
Helping to right a giant tortoise, stuck on her back
Ushering a beautiful bride to her wedding
Hounding a would-be usurper
Very sick, poisoned by a dastardly assassin
Howling mournfully at the death of a paladin
Wagging tails after hearing distant church bells
In cahoots with a distant gold dragon
Warp beast hunting party, with elf archers
Inspecting property boundaries
Watching over a lovesick shepherd
Insuring an evil count is properly interred
Weaning pups defend a wounded mother
Leading a weep of lepers to medical care
Whimpering, half-stuck in a boulder somehow
Leaping from a height, and blinking at the last minute
Wreaking vengeance on a wraith
Led by three-legs, who casts potent cleric spells
Yapping a warning about gnolls on the move

Table: boar
Agitated, with brindled back bristles standing erect
Luxuriating in the fragrant filth of a muddy hollow
Alarming the rest of the sounder with worried cries
Marking territory with pungent scent glands
Ambling down a shady path in search of food
Mauling a merchant after frightening away her horse
Basking in the sun after weathering a cool night
Munching loudly on mealy pears
Bellowing loudly to locate their piglets
Nibbling inquisitively on fern fronds
Binging blissfully on fallen figs
Nosing through pine needles in search of crunchy seed cones
Blindsiding a yowling mountain lion
Overgrazing a clearing, barely a blade of grass still stands
Bolting through the underbrush away from a bear
Patrolling their territory, stopping to sniff scent markings
Bounding across flooded fields, splashing wildly
Peeling bark and lichen from tree trunks
Bristling at the distant howl of a dire wolf
Perforating the greaves of a worried veteran
Brutally gouging a hapless hunter
Probing a gravelly scree for a beetle breakfast
Bulldozing a halfling's vegetable garden
Protecting just farrowed squealers
Burrowing into the side of a hill
Purring as their snouts turn up some wild turnips
Challenging another male for dominance
Quickly unearthing a freshly dug grave
Chaperoning several sows and juveniles
Raiding a row upon row of a parcel of parsnips
Charging directly at a startled chimera
Rampaging towards a truculent owlbear
Chasing a cowardly bobcat up a tree
Reclining under a stony overhang, near a dwarf skeleton
Chewing on a cyclops' grapevines
Relishing the contents of a cracked cracker barrel
Contentedly gorging on fallen acorns
Resting on their sides, half submerged in fragrant black mud
Covering themselves in pine needles and soil
Rolling around on rough ground detach parasites
Crashing through brambles, fleeing a grizzly
Rooting around, a squeal reveals a cache of radishes
Crunching on acorns, punctuated by happy grunts
Rummaging through a rubbish dump
Defending young from a swooping hawk
Running directly at an unprepared ranger
Delighting in the mud puddles recent rain created
Rustling through underbrush with no regard for stealth
Digging for tubers with their sturdy snouts
Rutting, and therefore exceptionally dangerous
Dredging a creekbank for delicious roots
Scampering across an open field in search of cover
Driving away a tongue-flicking draco lizard
Scarfing down savory mushrooms
Encroaching on a farmer's fennel fields
Scooping snoutfuls of dirt, seeking salt rich soils
Enjoying a cooling bath in a babbling brook
Scrambling through the wood, arrows peppering their hides
Fattening up on fist-sized toadstools
Seeking shade before the hottest part of the day
Fearlessly bull rushing a hungry hellhound
Snorting with satisfaction as a wolf pack retreats
Fighting off rivals for prime grazing ground
Snuffling as they crunch wild walnuts
Fleeing from a persistent tiger
Sprinting with impressive speed after a loud tree fall
Foaming at the mouth after eating toxic herbs
Squealing piglets fight over free teats on a temperamental sow
Foraging through the leaf litter for yummy grubs
Stampeding a hobgoblin campsite
Furrowing dry soil with sharp tusks
Startling a dryad's husband, out gathering flowers
Galloping away from a fireball detonation
Stomping the ground as a last warning to a game warden
Goring a brigand who encroached to close
Swaggering around, drunk on fermented fruit
Grazing on succulent shoots
Swatting large bottle-blue flies with their tails
Grunting with snouts to the ground
Tossing a yelping coyote after stabbing it with tusks
Guarding a rich muddy wallow from another herd
Trained by elfs to seek out truffles with magical properties
Harrowing the dirt to stir up wriggling worms
Trampling a hedge witch's herbary
Huffing gruffly to warn an impertinent raven
Trotting alongside their orc trainers
Hungrily gobbling up grain from a gnome tender
Uprooting bulbs prized for their value and beauty
Impaling the thigh of a thief
Vacuuming up pine nuts on the needle strewn floor
Jogging on spindly legs toward a water source
Venting surplus rage on a defenseless fence post
Jostling with each other as they ravage a ghost berry bush
Wading into a deep creek, oblivious to a nearby crocodile
Jutting, dagger-like tusks are prized for their ivory
Wallowing with audible pleasure in a muck pit
Knocking over a handcart full of witch apples
Whining warning squeals reveal a piglet stuck in a pit trap
Lounging under the dappled shade of a patient treant
Wounding a silent anchorite severely

Table: human, brigand
Ambushing a group of wealthy halfling merchants
Practicing several unnervingly accurate archery volleys
Assassinating the camp leader of a rival company
Press-ganging pilgrims into service as camp followers
Attacking settlers on their way to the frontier
Punishing a footman who led the enemy to the last camp
Beheading a captured berserker chieftain
Quenching barbed spearheads, just forged
Bivouacking with ruthless efficiency
Raiding the winter stores of an impoverished hamlet
Brawling over the only available bachelor
Raining missile fire on a platoon of veterans
Building a bridge to cross a precarious chasm
Ransacking a temple, dying priests pleading for aid
Burning down a grain-filled barn as farmers watch
Ravaging a fishing community that failed to pay tribute
Camping for the day to rest before an engagement
Reconnoitering the site of a new stronghold
Carousing raucously with stolen dwarf spirits
Recounting stories of a headless soldier, thirsty for blood
Celebrating a successful raid, divvying up the spoils
Recruiting new members with attractive pay and benefits
Conscripting local youths from a nearby village
Redistributing supplies after a pack horse went lame
Conspiring with an unscrupulous earl to start a coup
Reduced to boiling boot-leather for food
Defending a trade route from those who don't pay tolls
Reinforcing ditches with sharpened stakes
Delivering a cache of weapons to their fortified camp
Relieving an almost routed regiment as a last resort
Despoiling a caravan from far off lands
Requisitioning horses from a noblewoman's stables
Digging a defensive perimeter under protest
Robbing a wizard's tower, leader polymorphed into a frog
Disguising themselves in the uniforms of a holy order
Roughhousing and wrestling as a dignitary watches
Dispatching a rider to retrieve reinforcements
Rustling sheep from a shepherd to feed their camp
Displaying the symptoms of a virulent plague
Sabotaging an ancient dam, which could flood the area
Dissuading their leader from continued forced march
Saddling their temperamental hippogriff mounts
Doling out weekly pay from a large, locked strongbox
Salting the fields after razing a farmstead
Drilling pike formations in an open area
Scheming with local hobgoblins to carve up the region
Escorting traders through the wilderness, for a price
Securing safe passage for their leader through ogre lands
Ferreting out a confederate in their ranks
Seizing weapons from an inexperienced peasant militia
Foraging for food to supplement stale rations
Serving powerful doppelganger, a pretender to the throne
Fortifying a ruined manor house as a home base
Skirmishing with surprisingly tenacious goblins
Goading two rival factions into all-out war
Slaughtering quarantined suspected lycanthropes
Granting quarter to a cleric who fought bravely
Soliciting passersby for assistance with a ruse
Guarding the only traversable route to their camp
Sowing seeds of rebellion with vociferous speeches
Hanging a group of deserters for all to see
Spying on a tribe of centaurs, unsure of their alliances
Having just sacked a city, heavy with the spoils of war
Standing watch - a lieutenants funeral, died suspiciously
Heckling a new conscript who fell from a horse
Starving due to broken supply lines, desperate for food
Helping with a harvest in exchange for a share of crops
Strategizing - how to defeat a cyclops that defends their foe
Hijacking a richly appointed abbess and her acolytes
Stripping fallen of arms and armor after a pyrrhic victory
Hunkering down for a potentially long siege
Struggling with blood loss due to vampiric vines
Inciting riots to take advantage of the political chaos
Suppressing a local gnome revolt by force
Initiating new members with a solemn ceremony
Surrendering to a band of dervishes, outmatched
Looting a wealthy village on trade day
Surrounding an enemy encampment, waiting to strike
Marauding through the countryside, pillaging villages
Swindling townsfolk by pretending to be tax collectors
Moonlighting as bounty hunters to apprehend bandits
Switching loyalties to the highest bidder
Nursing their wounds after a sound defeat by an army
Temporarily allied with a hill giant, eating all their food
Occupying a very superstitious hamlet
Tending to numerous wounded after a staggering defeat
On a peace-keeping visit, brokering good will
Torching the huts of peaceful lizard men
Outriding and pathfinding to head off enemy forces
Undermining a sturdy stone battlement
Overseeing a treaty between rival mercenary companies
Waiting for orders from their leader, it's been days
Patrolling a disputed border, itching for action
Warmongering by pitting nomads against each other
Pilfering a barrow, unleashing undead
Warring with a rival mercenary company that hires orcs
Plotting to overthrow an inexperienced prince
Watering their horses and relaxing with song
Plundering an elf haven, no defenders in sight
Waylaying a group of knights to steal steeds and armor

Table: human, buccaneer
Auguring omens in the salty bottle-green sea foam
Keelhauling a spy for the crown found in their ranks
A-weighing anchor on rougher waters than they'd like
Landing a scow ashore to maroon a mutineer
Bailing water out of a damaged lifeboat
Lashing a scurvy-riddled captain to the mast
Battening down hatchways as a distant squall approaches
Launching lifeboats - a woman was discovered on board
Beached on a concealed sandbar, sitting ducks
Luring new sailors with help from their harpy leader
Belaying bowlines to catch a balmy breeze
Mending nets to maintain an air of respectability
Boarding a trade ship that wisely surrendered
Mourning the foreboding death of a giant albatross
Breaming barnacles and seaweed from a beached long ship
Mutinying - discovered the captain was cooking books
Broadsiding the ship of a famous naval bounty hunter
Nailing horseshoes to the masts to protect from storms
Burning a small galley after stripping it of valuables
Navigating narrow straits deftly via a close-kept route
Burnishing cutlasses and knives until they shine in the sun
Oiling water with a few drops & prayers to calm waves
Burying booty on a secluded beach under watchful eyes
Painting eyes on the bow their ships out of superstition
Butchering a sperm whale for blubber and baleen
Paying primage to loaders and stevedores
Capsizing from the constriction of an enormous squid
Pillaging a halfling hamlet, halflings themselves
Captained by a distant relative of one of the pcs
Plank-walking an angry dwarf
Casting lines over the bulwarks in hopes of catching fish
Proudly bearing "official" letters of marque from the king
Charmed by sultry sirens and spending pay on baubles
Prowling for prey in new lands, blown off course
Christening a new member of the fleet with a grand party
Purchasing salt pork, tack, grog from a fortified town
Clearing the deck after sighting their prey
Quarantining a ship after uncovering a case of mer-pox
Combing a beach for a misplaced magic spyglass
Raiding an important port soon, practicing maneuvers
Commandeering local fishing vessels by force
Raining coin on an impoverished village - a new haven
Crewed entirely by sea elfs with deadly grace
Ransoming a peasant, disguised as a prince
Decoying with colors indicating a deadly disease is on board
Reeving magical ropes through cold iron rings
Delirious from drinking seawater for weeks
Releasing prisoners liberated from pirates
Delivering a band of brigands to new shores to ravage
Replacing a mast, wrenched down in a gale
Disrupting local trade routes by blockading ports
Resupplying with water poisoned by fed-up locals
Dividing shares of loot loudly but fairly
Returning from long voyage, worshipping new deep gods
Dragging a merfolk war machine with their anchor
Roasting boar on the beach, while crew remains hungry
Dressing down a crew member for sleeping on dogwatch
Rowing out to greet a vessel with news of war
Drinking in excess after looting rich casks of brandy
Salvaging treasure from a ship sunk in shallow waters
Drydocking their flagship to make crucial repairs
Salving sunburns with secret herbal remedies
Excising the escutcheon of a stolen vessel
Sanctioned by local warlord to tackle a pirate problem
Feared by the locals, because children are drawn to the life
Sea-daughters - gills let them attack below waterlines
Fishing waveson from the water's surface with large hooks
Self-deafened to protect from harpies
Flogging the cook for his terrible cuisine
Sheltering in a cove, these sea-faring orcs prize honor
Flying a flag of truce...is it a ruse?
Singing lewd sea-shanties to an embarrassed noble
Forbidden from setting foot on land for a fortnight
Slurring demands to a vessel with superior numbers
Foundering in becalmed waters, growing desperate
Smuggling a priceless prize aboard - a seasick unicorn
Gathering under the same brutal banner to make war
Spinning yarns to scare landlubbers brought aboard
Giving no quarter to a defenseless merchant convoy
Starved after rats devoured rations, may eat each other
Hauling supplies aboard smaller boats to take them aboard
Suspicious of captain's guard - bugbear freebooters
Haunted by the ghost of a former captain who kills at night
Swabbing decks with animated mops, growing lazier
Hugging coastal reefs to evade pursuit by pirates
Terrified - stalked by an undead crewed ghost ship
Increasing numbers by kidnapping drunks from taverns
Towing a merchant galley who is paying handsomely
Influencing the winds with the help of a magic quarterstaff
Trading with a town secretly composed of were-sharks
Insisting on a week of shore leave in a local village
Unloading crates of arms to improve a haven's defenses
Inspecting the damage from a sea serpent strike
Untwisting old and fraying ropes for oakum
Intoxicated on exotic drugs from far-off lands
Voting on a new captain after the last was hung in port
Jettisoning a wizard's lab equipment, much to her dismay
Weather-watching and nervous about potential storms
Junking rope to re-head threadbare mops
Wrecking on rocks due to a lazy lighthouse keeper

Table: bugbear
About to teach a lesson to two Orphans who ran away
Lying in wait for a Shepherd who uses this path
Ambushing a Veteran on Watch for his camp
Muffling their scabbards with feathers and fur
Asphyxiating an Acolyte and licking their lips
Noiselessly soiling laundry on a line
Bickering over spoils, about to tear an Elf Cloak to shreds
On tiptoe, so as not to wake a sleeping Manticore
Blocking the quickest path to your destination
Patching a hole in their filthy Elf-leather bags
Building a big bower of bloody bones
Plunging a festival into darkness by dousing a fire
Bullying the smallest - A whelp of four years
Pouncing on the slower of two lovers canoodling
Bushwhacking a band of Mercenaries for their gold
Punishing children who don't clean up their toys
Catching a Caravan completely unawares
Pursuing the Dark Aims of an Evil Bat Cult
Cautiously sweeping a dry twig-strewn pathway
Quelching a force of Villagers armed with crude spears
Chasing after their Dinner, a buttered Bard
Quietly pretending to not know that you see them
Chewing on a root that prevents growling stomachs
Re-cobbling hob-nailed boots
Choking the life from a Comely Lass
Restraining a sacred Goat, stolen from a Temple
Clandestinely delivering their Thieves' Guild dues
Retreating after being sapped by real Shadows
Cleaning up blood-spattered stones - leave no trace
Rubbing furry palms before climbing down a well
Cloaked in thick Giant Ferret Furs
Salivating uncontrollably - Bugbear Rabies
Coating their daggers with pitch to dull reflections
Sawing almost all the way through rungs on a ladder
Covertly casing out a Barn to sleep through the day
Scaring a Shrine Keeper with blasphemous graffiti
Creeping across fallen leaves, utterly silent
Seeking a child's bed to hide beneath
Diving towards an escaping Cleric
Sewing a noisy Goblin's mouth shut with twine
Dropping a trail of sweets down a darkened path
Shadowing an Orc Patrol, taking down the last in line
Eating something crunchy. Was that a finger?
Shoving several small children into a sack
Experimenting with a Magic Wand
Seizing a Dwarf by his beard, shears at the ready
Extinguishing perimeter torches
Silently striding in shell-covered coats
Feeding crumbs of moldy dough to loyal Rat spies
Skulking just out of the eye-line of a Troll
Fighting over a Teddy Bear, stuffing flying everywhere
Slaying the last Berserker of at least six
Filing their teeth with rusty rasps
Slinking down a gravelly slope without a sound
Freezing, absolutely motionless as an Owl hoots
Slipping into a cranny that seems impossibly small
Frightening a Friar by putting spiders in his bed
Slurping out the eyes from rancid fish heads
Furtively glancing at their leader, watching for weakness
Smothering an old Veteran as he sleeps
Gagging the Alchemist who brews their poisons
Snarling as a Medium invokes magical Light
Garroting a mounted Knight, no mean feat
Soundly thrashing the one who made a noise
Gesturing complex signs. Are they talking?
Souring milk left out for the Good Folk
Getting the drop on a party of resting Elfs
Squeezing down the chimney of a cozy cottage
Grinding sausages filled with disgusting things
Stalking an Ogre who owes them money
Grinning ear to ear at a defenseless Bunny Rabbit
Standing impatiently, waiting for their Scout to return
Grunting agreement as they drag boots over dirt plans
Startling a sleeping lad who didn't finish his supper
Hampering a Traveler by constantly changing signs
Strangling an Illusionist who ceased to amuse them
Haunting a ruined Manor, where they hold court
Stretching out a hairless hide for tanning
Hiding from Dervishes, whose leader they killed
Subduing a Watchman with a blackjack to the skull
Hired muscle for a local Goblin tribe, lazier than most
Tar-and-Feathering a Gnome
Holding the lid closed on a boiling pot and laughing
Testing wooden floorboards for squeaks
Howling with sadistic glee as one of their traps' springs
Tormenting a Sage by gluing his books shut
Hunting a Ranger, said to be able to smell them
Tracking down a boy who sold them these magic beans
Interrupting a Griffon's dinner - An armored Warhorse
Trailing a Brigand train, picking off stragglers
Kidnapping children who don't do their chores
Trussing up a couple Kobolds to throw 'em in a lake
Knifing every tree they see, looking for a Dryad
Unblinking eyes from within dark brambles
Leaping from the shadows to panic a Dwarf camp out
Vaulting over fences and barricades, pursued by Dogs
Loping lazily along, the gait disguising their grace
Waylaying Bandits who were already waiting in Ambush
Lounging beneath a bridge, whittling disturbing things
Wearing wickedly carved pumpkins on their heads

Table: caecilia
Has recently eaten a disorientated lizard man crocodile hunter
Fighting a frenzied whiff of troglodytes
Has recently eaten a dwarf heroine - agnatha oldseam
Floundering as segmented skin begins to dry out
Has recently eaten a dying dryad, far from her tree home
Gliding effortlessly through dark, rich soils
Has recently eaten an earth elemental, just along for the ride
Glissading down a slope, surprisingly silent
Has recently eaten an elderly orc, fed to the beast after a broken leg
Gnawing on a horse in barding, denting the plates
Has recently eaten an elf sage, specializing in the surprising ecology of these beasts
Gobbling up goblins, effortlessly and at leisure
Has recently eaten a four gnomes following a treasure map
Gouging ditches in the earth to collect run-off
Has recently eaten a gargoyle with blunted claws and teeth
Gulping a pool of water in just a few raspy draughts
Has recently eaten a gilt box containing three sadistic shadows
Gushing forth from below the feet of an ogre
Has recently eaten a grateful goblin king, surviving on his bodyguards
Inadvertently unearthing guardians of an ancient barrow
Has recently eaten a halfling midwife, late for an important delivery
Inching, accordion-like around twisting curves
Has recently eaten an inconvenienced, impatient djinni
Inhaling damp air to bellow loudly
Has recently eaten an inert but fully sculpted bronze golem
Intertwined with local mythology - used to live in a well
Has recently eaten a kobold shaman, on a vision quest to save her tribe
Leaking blue bile that smells of cucumbers
Has recently eaten a laughing gnoll champion, warhammer in hand
Looped around a magically warm living statue of a saint
Has recently eaten nearly a dozen nixies, eager to return to their grotto
Losing teeth with every chomp on an iron living statue
Has recently eaten a nomad from distant desert lands, immune to digestion
Nibbling on a mushroom the size of a tree
Has recently eaten a notorious bugbear assassin - blackteeth
Oozing a lubricating coating that burns the eyes
Has recently eaten a relic-bearing acolyte - the hyoid of st. Herbert
Perforating an earthen dam, could flood fields
Has recently eaten several treant seeds from extinct species
Polymorphed prince, spurned the advances of a vivimancer
Has recently eaten six partially digested skeletons, fight at half strength
Probing a pile of detritus, snatching fleeing giant rats
Has recently eaten a son of a very wealthy merchant prince
Ramming repeatedly into a stone wall
Has recently eaten a surprisingly calm berserker, resigned to his fate
Recoiling from the sting of a giant scorpion
Has recently eaten a thoul sergeant of the league of terror
Rending asunder a hill giant's club with a powerful bite
Has recently eaten a three stunned hobgoblin sappers
Rooting around to turn soil beneath a druid grove
Has recently eaten a troll hermit, a contemplative pacifist after years
Rupturing suddenly with the slice of a dervishes' scimitar
Has recently eaten an unconscious medium, very near death
Searching for a nesting site, gravid with live young
Has recently eaten an unlucky bandit, who was burying treasure
Seen as ring-bringers by the local neanderthals - lucky
Has recently eaten a very peeved mummy
Shattering glass with a high-pitched screech
Has recently eaten a veteran who had nearly given up hope
Shoveling through pebbly scree with a spade-like head
Allowing young to feed on her skin (dematotrophy)
Sifting through a graveyard for easy pickings
Being carefully groomed by an undead alchemist
Sinuating slowly, bloated from a mule meal
Bleeding profusely from a gash on their side
Slinking to avoid becoming an early roc's breakfast
Blindly bowling over a bugbear
Slurping a tangy gelatinous cube
Boring through sandy soil, toward a tasty target
Snaking to surround a troop of white apes
Breaking off stony skin-crust from a cockatrice encounter
Spewing ichorous phlegm that sizzles on every surface
Burrowing into the ground with a low grumbling sound
Splintering wooden barrels via constriction
Chewing loudly on a cow
Spurting slimy discharge from both ends
Coiling around a clutch of pale pink, pulsating eggs
Squirming to squeeze through a small opening - stuck
Devouring a patrol of giant termites
Swallowing an owlbear in a single, resonant, gulp
Dipping its snout inquisitively into a deep puddle
Thrashing, locked in mortal combat with a rhagodessa
Drawn to ancestral mating grounds in a farmer's field
Tunneling connections to a new dungeon level
Dredging through stony substrate, undermining structures
Twisted around several stone columns, ceiling cracking
Emerging toward the surface due to recent rains
Undulating uncontrollably as muffled music plays within
Entwined around a rock python - a serpentine braid
Violently twitching to-and-fro
Erupting from the ground to catch a camel unawares
Weeping viscous mucus from between segments
Excavating a chamber to vomit forth stomach treasures
Worshipped by transdimensional cultists of kyuss
Expelling indigestible rocks with the glimmer of metal
Wound around a large boulder - petrified hydra
Extricating from a writhing mating knot
Wriggling as kobold worm-tenders scrub their skin
Feasting upon a giant slug
Writhing as they shake off carcass crawler toxins

Table: camel
Alerting the herd after spotting a deadly giant sand spider
Licking their frowning cameleers face
Appearing suddenly from the far-side of a massive dune
Limping from a festering leg wound
Attempting to peel tender bark from a spiky desert plant
Loping along in a line, shying from strangers
Batting long eyelashes to keep out stinging sand
Lurching wildly, drunk after gorging on fermented figs
Bearing an opulent howdah, containing a lost noblewoman
Marching to war, glimmering in sun with thin armored plates
Being milked by expert elfs in indigo dyed shemaghs
Motivated by starchy vegetables, raiding a bedraggled garden
Bellowing ungraciously into the ear of their handler
Muddying their haunches trying to ford a dying river
Belonging to a wicked goblin chieftain, seeking kinder master
Munching on ripe dates, fallen at the feet of their palm
Biting their hobgoblin handler playfully
Negotiating a narrow, treacherous wadi crossing
Bolting down a spilt basket of prickly pears
Noisily slaking their thirst after a rare rain fills a pond
Browsing straggly desert grasses for tender green shoots
Nuzzling a newborn calf, encouraging it to stand wobblily
Calving in the shade of a large formation on a bed of dry leaves
Operating an ingenious turn-style well pump
Carrying large baked clay jugs of brackish but drinkable water
Overburdened with weapons and armor, destined for orcs
Charging down a dune - fleeing from a giant scorpion
Padding along a bleak expanse of cracked, sunbaked clay
Chewing cud, comically disinterested in their surroundings
Plodding doggedly up a steep sandstone slope
Closing their nostrils against the blowing sands
Prostrating on command during an acolytes prayer
Convoying in a long line, strung together by silken ropes
Proudly strutting, hide adorned with intricately shaved sigils/patterns
Crossing a stretch of steaming hot, smooth black pebbles
Pulling ramshackle chariot, manned by javelin slinging ghouls
Crouching slightly as a gnoll merchant adjusts their load
Pungently stinking, one can smell them before they see them
Devouring a small clump of flowering succulents
Quavering tremulously from afar in the shimmering heat
Digging for fleeting moisture with their sturdy, splayed feet
Racing for a valuable bounty of incense, nomad riders whipping
Dislodging sand grains with their third eyelid
Rearing abruptly to the strident sound of a rattlesnake
Dragging a nearly dead rider, stuck in stirrups
Reclining in the slender spear of shade from a wind-worn obelisk
Drinking deeply from a flooded creek bed
Refusing to budge, despite the urgings of their frustrated medium
Eating their last lunch again - constantly munching
Running from a hungry roc's ominous, blotting shadow
Enduring a suffocating, sand-laden simoom
Scattering their cargo after bolting in terror from a manticore
Enjoying a thorough grooming from their nomad owner
Scowling as their traders haggle over textiles
Exhaling gruffly, after a dervish yanks on their harness
Snorting to warn drinking companions of a crocodile
Extravagantly caparisoned for an upcoming festival
Spitting directly in the face of a bandit
Extruding his dulla from his mouth to assert dominance
Starving after getting lost in a fierce sandstorm, ribs poking out
Flocking to a spring-fed oasis
Stepping in each others tracks to minimize exertion
Following a flight of pigeons and doves to lead them to water
Stewing after being traded to a dwarf for a skin of precious water
Foraging for hardy plants, buried under a layer of sand
Stopping abruptly as sword wielding skeletons rise from the sands
Foundering in a fechfech (dry quicksand)
Straying from their cameleer in pursuit of pathetic pastures
Galloping to enthusiastically greet their fodder-bearing owner
Struggling under a massive load of exotic woven carpets
Grazing on an upset mesquite dryad's leaves
Stumbling from dehydration, been three weeks since the last drink
Groaning and grousing from a goblin rider's crop
Swaying precariously due to unbalanced cargo
Grunting with satisfaction after blinding a bugbear with spit
Teetering, like a tripod as they lean down to drink from a puddle
Guarding young calves from circling, hungry hyenas
Transporting fragrant firewood, conjured by a djinni's magic
Gulping down a proffered amphora of water greedily
Trekking to a seasonally reliable water source
Hobbled, back leg bent and tied to prevent them from wandering
Tripping their tender with a well-timed kick
Huddling together in the sparse shade of a gnarled mulga acacia
Unceremoniously dumping their bounty hunter rider
Ignoring gruff commands and stubbornly lying down
Undergoing branding by a group of friendly nomads
Infuriating their owner by chewing through tent straps
Vexing a merchant by expectorating on their ostentatious outfit
Jingling pleasantly thanks to the shiny silver bells on their tack
Wading into a flooded wadi to cool off
Journeying to a celebration, featuring frantic camel races
Walking deliberately around a suspected chimera den
Kicking their kobold attendant squarely in the backside
Wallowing in sand to remove irritating fleas
Kneeling for a dervish archer's dismount
Wandering among the desolate and eroded yardangs
Laden with enough exotic spices to buy a tavern
Weaning a pure white calf, seen as a favorable omen
Lashed to an abandoned wagon with a broken axle
Wearing the patience of their halfling owner thin

Table: carcass crawler
About to molt, flees immediately when struck
Lingering for scraps as a larger one finishes eating
Adhering in a coil of legs, high on a wall
Lunging at a giant bat, asleep on the ceiling
Annoying a ghoul pack - eating cadavers they're saving
Lurking in the damp of a deep, dark, alcove
Benumbing a foaming berserker band
Nibbling on the nose of an unblinking gnome
Besieging a kobold's armory, none dare approach
Nuzzling a dead tiger beetle that smells of rot
Brawling with a black crabs over a stinking catfish
Palpating the floor before it with its squirming face
Buried under a mound of dead leaves and detritus
Paralyzing a plate mail wearing paladin
Caressing the terrified, frozen face of a friar
Patrolling a corridor, trained by local denizens
Chasing after rats, dripping tentacles flailing wildly
Pestering a ghoul, who keeps kicking it away
Chittering with contentment over a dead goblin
Poking at a moldy cushion with its forelimb
Clambering across an iron grate noisily
Prowling towards a secret dungeon exit
Clasping mandibles together with staccato snaps
Pulverizing a troglodyte skull with its' mouthparts
Clicking with spiny legs across the flagstones
Pursuing a smaller crawler ravenously
Climbing toward you on the ceiling, dripping gore
Rasping the last bits of meat from a discarded ham
Clinging on the underside of a large wooden table
Reeking of rancid carrion and decaying flesh
Clutching tightly onto a maggot-filled severed arm
Regurgitating a handful of coins, swallowed by mistake
Competing for the corpse of a cleric clad in white
Scabbing over from a nasty bite from a troll
Consuming a still living white ape, leisurely
Scaling the side of a deep spiked pit, kobold in mouth
Creeping along the corners, shying from light
Scampering down a wall after stepping in green slime
Curled up in a defensive ball to protect itself
Scrambling to avoid a hungry giant toad
Dangling tentacles down from over a doorway
Scraping bits of brain out of a dented helmet
Dining on a dead dwarf, feet first
Setting off shrieker colony, oblivious or attracting meals?
Dodging a sling stone, flung by a worried halfling
Sheltering in a crumbling ceramic drainpipe
Dragging the still body of an acolyte up a wall
Shivering and twitching with anticipation - dead wolf
Draped over the back of a chair, like a bloated stole
Shyly scurrying to a hiding place among several chests
Drooping and limping, hasn't eaten in weeks
Skittering across a caltrop covered floor easily
Effortlessly ascending a vaulted ceiling, upside-down
Slurping as it starts to eat a still twitching giant shrew
Emerging from a weirdly geometric cocoon
Snuffling an old discarded and quite smelly boot
Enticing a mate by piercing a bloated dead mule
Squirming in the strands of a giant spider's web
Exhausted by the effort of egg-laying on a dead horse
Squirreling away choice bits of a thief's body for later
Feasting on a shallow-breathing medium
Stalking a group of lost teenage treasure hunters
Fighting over a paralyzed hobgoblin
Steering clear of a swarm of robber flies
Flourishing due to abundant giant rat prey
Sticking to the other side of a trap door on the floor
Flushing out bats from crannies in the ceiling
Stinking sharply of a charnel house in summer
Flustered by a resilient elf, beating it with a club
Stroking a door handle, coating it in numbing toxins
Fondling the fingers of a frozen fisherman
Struggling to paralyze a sleeping thoul
Gorging on a rotting rock baboon, dragging it around
Stuffing itself tightly within a burial niche to sleep
Grasping, erect on hindmost legs, as stirges fly by
Taste-testing a skeleton, standing at attention
Grazing on larvae of its own kind, recently hatched
Throbbing with inner light, just ate a dead fire beetle
Grinding a ripe zombie arm within its mouthparts
Tossing aside chainmail to feast on the fighter within
Hanging from a stalactite in the shadows
Tracking an orc, wounded by a spear trap
Hatching eggs that begin to devour it immediately
Trapped at the bottom of a pit by alchemically slick sides
Hiding beneath a toppled statue, hissing
Trembling slightly in a sudden frigid breeze form below
Hugging walls as it senses a predator - giant wasp
Twisting off the head of a lizard man a sickening sound
Immobilizing the last member of a party before dining
Vexing a goblin tribe by blockading their shortcut
Incapacitating a fleeing bugbear with a touch
Waiting patiently to be fed by the local kobold tribe
Inch-worming its way up a slick, mossy wall
Wedged under a rusty tower shield
Lashing a living statue futilely with its tentacles
Wretch-inducing and fetid, you can smell it from here
Laying eggs on a large paralyzed owl bear
Writhing tentacles glistening in the dim light
Leashed with a green copper chain, obviously hungry
Zigzagging across a wall, apparently avoiding the lichen

Table: cat, great (lion)
Crouching stealthily, preparing to pounce on prey
Lazily watching animals drink at a water source
Full bellies, relaxing in the shade with toothy yawns
Meticulously grooming fur with their large tongues
Gouging the bark of a tree with mighty claws
Roaring a warning to territorial interlopers
Guarding a recent kill from scavengers
Rubbing their face on a stump - scent marking
Keeping a watchful eye over curious cubs
Surveying the area from a high vantage point
Bounding after a young zebra, leaping for the kill
Aggressively defending territory from a young male
Dining on a dead ranger who got too close
Emaciated from a recent drought and lack of game
On their way to a coronation for the king of beasts
Furiously licking at a wicked thorn wedged in front paw
Snarling at hyenas and vultures stealing parts of prey
Panting in the simmering shade of a scraggly tree
Habituated to nearby nomads, no attacks in weeks
Scavenging the vulture-pecked carcass of a hippopotamus

Table: cat, great (mountain lion)
Crouching stealthily, preparing to pounce on prey
Lazily watching animals drink at a water source
Full bellies, relaxing in the shade with toothy yawns
Meticulously grooming fur with their large tongues
Gouging the bark of a tree with mighty claws
Roaring a warning to territorial interlopers
Guarding a recent kill from scavengers
Rubbing their face on a stump - scent marking
Keeping a watchful eye over curious cubs
Surveying the area from a high vantage point
Ambushing an adult mule deer from above
Hunting on behalf of their ranger companion
Avoiding a large clearing by skirting the wooded edges
Sharing a dead boar with gossiping ravens
Clawing futilely at the entrance to a rabbit warren
Sparring with a peeved porcupine, and it isnt going well
Eating the innards of a downed pronghorn
Wary - being hunted ruthlessly by local ranchers
Grimacing with a lip curling response to a rival's scent
Yielding to a grizzly with a low growl

Table: cat, great (panther)
Crouching stealthily, preparing to pounce on prey
Lazily watching animals drink at a water source
Full bellies, relaxing in the shade with toothy yawns
Meticulously grooming fur with their large tongues
Gouging the bark of a tree with mighty claws
Roaring a warning to territorial interlopers
Guarding a recent kill from scavengers
Rubbing their face on a stump - scent marking
Keeping a watchful eye over curious cubs
Surveying the area from a high vantage point
Climbing a large tree to check on a kill
Protected fiercely by local jungle dwelling elfs
Concealing their lycanthrope nature well
Rending the hide from a freshly slain baboon
Gliding through water with surprising determination
Standing their ground fiercely against some nervous gnolls
Melanistic and majestic - barely visible in shadows
Symbiotic relationship with treants - they protect each other
Picking choice bits from a just slain doe
Yowling as a courtship turns violent

Table: cat, great (sabre-tooth tiger)
Crouching stealthily, preparing to pounce on prey
Lazily watching animals drink at a water source
Full bellies, relaxing in the shade with toothy yawns
Meticulously grooming fur with their large tongues
Gouging the bark of a tree with mighty claws
Roaring a warning to territorial interlopers
Guarding a recent kill from scavengers
Rubbing their face on a stump - scent marking
Keeping a watchful eye over curious cubs
Surveying the area from a high vantage point
A tribal totem - any injury will be brutally avenged
Kept at bay by firebrand waving neanderthals
Circling a wounded mastodon cautiously
Leaping from a great height onto the back of a titanothere
Dragging a slain white ape back to their den
Limping from a recent kick from an angry terror bird
Expanding an abandoned glyptodon burrow
Semi-domesticated by savage stone age halflings
Gulping down huge chunks of wooly rhino flesh
Surprisingly curious and docile around dwarfs

Table: cat, great (tiger)
Crouching stealthily, preparing to pounce on prey
Lazily watching animals drink at a water source
Full bellies, relaxing in the shade with toothy yawns
Meticulously grooming fur with their large tongues
Gouging the bark of a tree with mighty claws
Roaring a warning to territorial interlopers
Guarding a recent kill from scavengers
Rubbing their face on a stump - scent marking
Keeping a watchful eye over curious cubs
Surveying the area from a high vantage point
Burning bright with gorgeous emerald eyes
Oozing blood from a gnarly arrow wound
Devouring a lizard man warrior
Stalking villagers - has acquired a taste for the flesh of man
Dragging a dead crocodile across the mud
Storing a dead boar high in a tree for later
Jaws clamped around the carotid of an antelope
Visiting a temple, locals sometimes leave tasty votives
Nuzzling in lap of a beautiful maiden - banyan dryad
Watchfully lapping water from a stream

Table: cave locust
Agitated due to a lack of food
Hanging onto a pendulum blade trap
Attracting unwanted attention by rummaging in a pile of coins
Headbutting a gnome mushroom farmer playfully
Battling a rust monster who wandered into feeding grounds
Hiding behind a dislodged door, leaning against a wall
Bearing strange, almost arcane sigil-like markings
Hightailing away from a hungry giant shrew
Biting large thick strips from a shelf-lichen
Hissing vociferously at hobgoblin guards
Blundering into a pile of bones
Hugging an archway as a gelatinous cube glides past
Bolting after being startled by a sudden sound
Ingesting strange spores that grant speech and a sense of morals
Bounding from wall to wall in short, swift flights
Jumping away from a giant tarantula
Bred as tireless watch-crickets by gnomes
Lashing antennae from its perch atop a statue of a saint
Burrowing into loamy, fragrant soils
Launching itself against a wooden door
Burying lemon sized eggs under leaf litter
Laying eggs in a mildewed mattress
Buzzing joyously while munching on pale green mushrooms
Leaping inadvertently into a group of orc warriors
Careening headlong into a kobold patrol
Lethargically sampling pages from a sagging bookshelf
Chasing away a fire beetle
Loosening soil from a shattered floor tile
Chewing on the yellow mould growing on a door
Manducating a crimson colony of poisonous blood caps
Chirping loudly to attract a mate
Marching confidently toward a startled troglodyte child
Chomping chunks of the corners of a carpet
Munching somberly on a slimy sack of torches
Chopping the caps off tall mushroom stalks with its mandibles
Nibbling on shriekers and making a tremendous racket
Clambering across a dusty flagstone floor
Nosing a filthy chamber pot
Clasping firmly onto a pillar
Patiently observing two males duking it out
Clicking quietly to itself under a table
Patrolling his territory after hearing a rival's chirps
Climbing over the body of a paralyzed veteran
Piercing the silence with a rapturous song
Clinging tightly to a chest defensively
Prized by their taste by kobold cooks
Clutching the concealed side of a moth-eaten curtain
Rasping threateningly by rubbing hind legs together
Coated in stinky spittle after a run in with a rival
Restlessly marching from one corner of a room to another
Concealed among decorative stonework
Rooting around in the debris from a collapsed cabinet
Defending a wounded goblin pest-whisperer
Scampering across a caltrop covered floor
Digging diligently into a pile of goblin rubbish
Seeking warmth from the cooling coals in a hearth
Dining on delicate mosses at the foot of a dais
Shedding a silvery exoskeleton during a molt
Discharging thick brown spittle on a fuming dwarf
Shrieking shrilly, stuck in a spider's web
Divebombing a draco lizard
Singing a surprisingly catchy tune
Dribbling gooey gunk all over a spectacular painting
Skulking behind several barrels
Drumming abdomens against the ground, repetitive thumps
Slavering at the sight of a humungous mushroom
Excavating a shallow hole
Sluggish due to cooler temperatures
Excited as a female cave locust approaches
Spewing brown ichor at a giant snake
Eyeing tasty candle stubs
Spiting its stinky spray at an acolyte
Fattening up on powdery puffballs, filling the air with spores
Spluttering horrendously smelling liquid at a lizard man
Favorable conditions led to a population surge - worrying farmers
Springing to a perch atop an iron chandelier
Feasting upon flavorful fungi
Squeaking at the base of a stalagmite
Fidgeting with its forelegs atop a termite ridden bench
Stridently stridulating, in search of love
Flaring mandibles as a giant centipede passes nearby
Strutting on spindly legs to impress a female
Fleeing from a hungry tiger beetle
Stumbling away from a giant scorpion
Fluttering from column to column
Surprisingly delicious when roasted with vegetables
Gnawing on the wooden leg of a chair
Swooping suddenly from the ceiling in a swarm of bats
Gorging on rations, spilled from a bloody backpack
Taking wing after being startled by a distant crash
Grappling with another male in a battle for dominance
Trilling with a nearly deafening volume
Grasping onto thick, gnarled roots erupting from the wall
Tussling with a giant toad
Grazing upon luminous lichens, near the ceiling
Vaulting over a deep pit with a thrumming leap
Grooming antennae and stretching out wings
Victoriously singing after defeating a rival for his mate's affections
Guarding a giant wheel of fuzzy cheese
Warbling weirdly after lapping up spilled wine

Table: centaur
Applying poultices to a severely injured elf
Leaping over low fallen trees as they pursue an ogre
Backing the dwarfs in a territorial dispute with gnomes
Lined up patiently for the attentions of a farrier-for-hire
Balking at a rickety bridge over a rushing river
Listening intently to a lecture from an elder
Bandaging the injured fetlock of their blacksmith
Loping towards home, exhausted from an unfruitful hunt
Bartering for shoe-nails with baskets of ripe blinkberries
Migrating to a new meadow soon, packing up their camp
Bathing in a pristine pool of crystal-clear water
Mustering a gnome militia to help fight hobgoblin loggers
Befriending a local village by performing plow-work
Negotiating a price for passage with a friendly bridge troll
Boiling gorgon leather to make braces for archery
Nickering to calm a frightened stallion
Bolting from lasso bearing orc slavers
On their way to crown a new khan
Braiding the beard and tail of the groom for a wedding
Picking feral figs from gnarled branches
Breaking bread with a group of exhausted dervishes
Plucking only ripest wild grapes for their fantastic wine
Brewing spirits in a wagon-mounted still
Pounding glowing iron brands to remove impurities
Brooding over troll tracks and spoor - at least ten
Prancing in choreographed formation, forced march
Burdened by grief after the loss of their matriarch
Pulling an old rulley that's about to lose a wheel
Cantering solemnly as pall bearers for a paladin
Racing after a pack of wolves to drive them away
Carousing enthusiastically with elfs and their murky wine
Raking chestnuts from the base of an ancient tree
Cavorting with sprites in a circle of toadstools
Reaping wheat with sharp borrowed scythes
Chasing goblin poachers from a unicorn's grove
Rearing suddenly at the sound of a deathrattle serpent
Colts courting fillies with fragrant floral tokens
Roasting mutton over a fire of seasoned wood
Cooking a prodigious amount of food, eager to share
Rounding-up a flock of grazing sheep
Crushing herbal preparations to trade in town
Rowdy colts cornering trespassing and terrified bandits
Currying favor with a local king's calvary
Sabotaging a paddock to free horses from servitude
Daisy-cutting across a sweet-smelling meadow
Safeguarding a sacred sylvan shrine
Dancing with agile hoof-work to a satyr's syrinx
Scouting a suitable clearing to plant a seedling treant
Decanting an exotic vintage of firewine, carefully
Scrumping apples from a noble's orchard
Defending a verdant pass that leads to their settlement
Searching for a lost and frightened foal
Delivering the dowry of a pixie princess
Securing a chest laden with silver ingots
Discussing discovered hobgoblin tracks in hushed tones
Selecting straight saplings for spear wood
Dredging a pond, searching for their anvil post-barge-wreck
Serving as sentries for a nearby hidden elf settlement
Escorting their healer to a royal patient, best in the land
Shaggy steppe transplants, speaking in strange tongues
Feasting to celebrate a momentous victory from long ago
Shearing their flock and carding quality wool
Fishing from the sandy bank of a nixie's lake
Stampeding under the banner of their champion paladin
Fleeing for cover from a gluttonous griffon's screeching dives
Steaming yew staves for bowyery
Fletching masterfully crafted arrows with owlbear feathers
Stomping vast vats of grapes and in good spirits
Gallivanting throughout the woodlands, unsettled nomads
Striding among shady lanes of the wood, almost silently
Galloping thunderously, lances set against a wyvern
Summoning the shaman to mend a broken bone
Gathering flowers for a funerary bower - a dryad's death
Swindled by an unscrupulous trader and seeking revenge
Glumly chewing on bland and incredibly dry oat cakes
Tapping a tun of osage cider, an acquired taste
Guiding an impetuous ranger to a giant's lair
Tending to honeybee hives in preparation for mead season
Haggling with dwarfs over their inflated iron price
Testing the depth of a ford prior to crossing
Hammering dents from barding plates on a portable forge
Throwing large nets into a lake teeming with fish
Harvesting medicinal barks from threadbare trees
Tilting at a giant windmill golem
Helping a local druid haul huge sarsen stones
Tossing javelins in contest at scarred wooden dummies
Hitching a troublemaker to a wagon as penance
Tracking a sounder of suspected devil swine
Hungover from a weeklong bender and irritable
Trading finely woven tapestries for candied sweets
Hunting deer, just bagged an impressive buck
Travelling to the great moot to tell tales from their tribe
Imperiled by recent torrential rains, traipsing carefully
Trotting alongside an injured knight, leading him to safety
Jogging briskly as they patrol their sun-dappled paths
Unfurling sacred scrolls to banish a barrow wight
Jousting for sport - fragile wooden lances and strong shields
Willing to trade almost anything for a new anvil
Kneading sticky, fragrant dough to bake a hearty bread
Wincing as they help clip each other's hooves

Table: centipede, giant
A profane and eldritch toxin - you can now be turned as undead
Holing up in a bathing elfs chain armor
Befuddling venom - as the spell confusion
Infesting a sack that containing rotting rations/several pitons
Crawling in unseemly places - bite inflicts disease (as spell)
Injecting a too curious fire beetle with their venom
Develop an allergy to iron, subsides on a strict vegetarian diet
Inside a decaying log strewn across your path, waiting to strike
Drowsy/droopy - as spell sleep, but with remarkably vivid dreams
Lashing out flutily at a fearless giant shrew
Heartbeat slows, breathing shallows - mistaken for dead by most
Licking their eggs to protect them from fungi
Irrational hydrophobia - affected by fear (as spell) around water
Mandibles twitching as two rivals size each other up
Magic jar with centipede, better hurry up and bite before they get away
Navigating a scree of broken glass with ease
Neurotoxin alters brain in weird way - replace a known language
Nibbling on the foreleg of a giant spider
Ovipositor - days you see em writhing under skin, in they burst forth
Optimistically tasting a dead cave locust
Paralyzes vocal cords first, slowly clouds vision - mute/blind in a week
Patiently hiding in a dark cavity that holds an important lever
Potentially beneficial choking hazard - breath only water
Piercing the stiff chitin of a scorpion with ease
Prized by orcs - adrenaline rush acts as haste spell, must rest afterward
Preying on former mate to nourish the development of young
Remarkably painless, but random limb is paralyzed
Pricking hairs on necks as it slithers out the mouth of a corpse
Rooted to the spot, as if you've forgotten which foot comes first to walk
Protecting a large, bulbous egg mass by carrying it under their tail
Searing pain courses throughout your body from the wound (as blight)
Quickly scrambling away from a giant toad
Taste buds dull, food tastes of ashes, drink is bitter grapefruit juice
Racing after a giant springtail
Tremors/spasms - drop items held in right hand when a
Is rolled
Rapid staccato clicking as spindly feet meet stone
Used to mark and locate prey - bite sheds light as spell for days
Rattling a chain, being used as a ladder
Wound festers and leaks foul smelling puss until treated
Rolling around in a pool of their venom to kill off parasites
Ambling noisily over a pile of leaves and twigs
Rustling through leaf litter in search of large worms and grubs
Amphibiously lurking in a small, muddy puddle
Scratching faintly on a glass jar containing a very frightened sprite
Aposematically colored - advertising it's toxicity in bright red and blue
Scurrying underfoot, to the yelps of patrolling orcs
Blending in rather well with discarded coils of rotting rope
Secreting smelly defensive chemicals - like sour milk and gasoline
Burrowing into a patch of soil, kicking up a surprising amount of dirt
Seeking water to avoid drying out completely and dying
Chewing a large, dead lizard meticulously
Seemingly spring-loaded as it swiftly strikes at a shadow
Chittering to scare off a hungry giant rat
Seizing a resting stirge from its precarious perch
Chomping down on a frog/toad - it kicks a few times then is still
Sheltering within a very finely made helmet
Clambering across a flagstone floor, on the prowl
Sinuating confidently in the open - most predators know better
Clinging to the underside of a doorway arch
Skittering in the cushions of a comfortable-looking chair
Coiled within a footlocker's moldering fabrics
Snaking around the unsuspecting ankle of a dwarf
Covering the intriguing writings of an open grimoire
Sneaking up on a warm, snoring goblin
Creeping along, where walls meet the floor, stealthily and unexposed
Somehow found its way into a now screaming acolytes' hood
Curled up, inhabiting a bucket beneath a layer of sand
Stalking their preferred prey - venomous snakes
Dashing suddenly out from under a bench
Startling a mule, now stomping furiously and braying loudly
Depredating a nest of squirmy pink giant rat pups
Stuck to the underside of a trapdoor and easily agitated
Devouring a starling after stumbling across their nest
Suspended from the ceiling, snatching bats on the wing
Dragging a smaller centipede in its mandibles
Swiftly crawling from hiding place to hiding place
Dripping blackish green venom onto a discarded silk handkerchief
This littoral species enjoys eating barnacles
Dropping down from the ceiling onto a table laden with dishes
Tightly curled around a dead rabbit, feeding
Dwelling within a curious skull, their home sweet home
Trained hunting centipedes, a pixie innovation
Effortless climbing a sheer surface
Underneath a conspicuously loose stone
Encircling a door handle to survey for prey
Viciously biting it's kobold trainer, fortunately immune
Falling from their perch on the side of bookshelf to scurry behind it
Weaving through the wrappings of an unbothered mummy
Feeding on an unlucky and very hairy tarantula
Worming through keyhole (large chest) - hind parts visible
Finding a terrifying place to sleep in an unattended boot
Worrying a group of lizard men, trying to find a place to camp
Flicking sensitive antennae after a change in temperature
Wounding a medium, mistook this for his nearly identical familiar
Gnawing on a mouse with massive mandibles
Wreathed around a clumsily gilt bust of a forgotten philosopher
Guarding clutch of eggs - rare example of invertebrate maternity instinct
Wriggling on the end of a kobold's spear
Helically slithering down a column - a spiral with too many legs
Zigzagging across a table, laden with alchemist equipment

Table: chimera
Abandoning a den after being driven off by a dragon
Immolating an unlucky thief who traipsed to close
Abducting a fire giant child from a mountain fortress
Injuring a wyvern with a bite, the battle rages on
Alarming a local town, by flying low and burning crops
Inspecting offerings laid at its feet by evil acolytes
Alighting from a ruined rampart to hunt for prey
Just escaped from a vivamancers laboratory, ravenous
Bellowing with booming cries that echo throughout
Maiming a medium trying to collect chimera dung
Bickering amongst its heads over where to spend the night
Mangling a windmill, the town's only source of water
Bleating haunted blats from atop a ruined parapet
Marauding across the countryside, burning buildings
Blighting the nearby countryside by poisoning the water
Marring an ancient mural of the deities of light
Broiling a herd of cattle on the hoof
Melting a sack of gold into a sizzling lump, easy transport
Building a ziggurat of skulls, all shapes and sizes
Mutilating a dryad's tree with glee
Burning a trader's wagon and whinnying maniacally
Nesting beneath a toppled petrified frost giant
Burrowing into a hillside to establish a new nest
Panicking a hamlet - torching their winter grain stores
Butchering the body of a camel with wicked front claws
Perched on a craggy bluff, pleased with the barren view
Charring the hide off a horse, fell from a precarious path
Plummeting sharply after wings were riddled with arrows
Chewing sullenly on plate armor, dragon & lion grumble
Plundering a hippogriff nest, high on the rocks
Circling cautiously above signs of recent dragon passage
Poaching prize stallions from a noble's pastures
Collecting shields of slain challengers, polishing them
Preening wings and fur, in search of a mate
Commandeering a new lair in a lighthouse
Purloining a forsaken roc's nest to raise her young
Conflagrating a cache of supplies, left by explorers
Ransacking a kobold caravan
Conniving with nearby flame salamanders, uneasy alliance
Ransoming access to a newly discovered dungeon
Contorting to squeeze through a door frame
Reconnoitering an old dwarf mine that still bears seams
Cremating a challenger who sought its mate
Reducing a sturdy cabin to ashes
Defacing the ancient marble columns of a temple
Relinquishing a stolen holy relic to a powerful priest
Delighting in the fear of a gnome family held hostage
Rending deep wounds on a frenzied ogre champion
Deserting a dungeon home, not enough to eat
Renouncing an allegiance with local hobgoblins
Desolating swathes of countryside, not a grass blade grows
Roaring at the discovery that a treasure was stolen
Despoiling a pond by placing carcasses and corpses within
Roasting mountain goats, still clinging to the cliffsides
Devouring boiled griffon eggs
Rummaging through a dented pile of plate mail pieces
Dismissing cries from help in common from below
Sacking a village, already decimated by plague
Diving towards grazing deer
Scalding a surprised and fleeing troll
Dropping a giant tortoise from a great height
Scorching treetops, starting a forest fire
Encouraging the adulation of a local goblin tribe
Scouring self-made desolation for something to eat
Ensorcelled to serve as a sentry for this pass
Scrutinizing its reflection in a polished shield surface
Eradicating a village, one member a week
Searing the wool from sheep and skin from shepherd
Exploring an evacuated elf outpost, cautiously
Setting alight the tent of an adventuring party
Extorting a group of merchants for safe passage
Sharpening its horns on a granite statue
Ferreting out a family of halflings from their hillside home
Shattering the stained glass on a local roadside shrine
Fighting over a dead ox, each head wants the liver
Sifting a burned hamlet, for charred corpses to consume
Flapping furiously to drive away a swarm of carrion flies
Slightly singed rock baboon for breakfast
Frustrating friars, by blockading their monastery
Soaring in a cloudy sky, ahead of a storm
Gliding clumsily, surveying its domain for prey
Stockpiling the heads of heroes sent to defeat him
Gnawing on gory moose bones
Swooping upon startled group of dwarf prospectors
Goring a warhammer wielding ghoul
Tearing down colorful prayer flags
Gouging the eyes from an owlbear
Terrorizing barefoot pilgrims by lacing a path with thorns
Grooming itself with its long, wet, lion tongue
Testing wind from a high cliff, looking for the lazy thermals
Gutting a giant bat that flew into its home
Toppling the steeple of a church
Headbutting a knight, unhorsing her with a sound clang
Tumbling down a slope, wrestling a warp beast
Hiding among exotic statuary in a medusa's garden
Vandalizing a monument to a monster slayer
Hoarding coins/shiny stones to attract tastier meals
Wearing enchanted triple collar - part of a travelling circus
Hovering above a deep crevasse, searching for life
Yowling after a direct hit from a stone giants boulder

Table: cockatrice
Alerting fellows to an aerial predator with a screech
Imprinted on an unlucky medium, faithfully following her
Alighting clumsily atop a basalt bugbear
In a stupor, staring at a chalk mark on the ground
Asserting territory with obnoxious calls
Incubating infertile, igneous eggs
Attacking an egg-stealing serpent
Jabbing their spurs into the statue of a shield bearer
Balancing precariously on a petrified pike mans head
Landing from a long flight, panting and nervous
Being carefully gaffed by enterprising goblin bookmakers
Letting out a warning shriek, bounding at a blink dog
Bellowing noisily at a truculent sun
Molting feathers and scales, a skin-crawling sight
Blustering about a clearing, stoning rabbits
Murmuring encouraging noises to a clutch of eggs
Boastfully crowing after pecking a rival to death
Nibbling at the stone toes of a marble bandit bowman
Bowing and waltzing in an elaborate courtship ritual
Pecking at the eyes of a petrified ogre
Brooding on a tempting, gemstone-strewn nest
Peeling delicious lichen from a weathered dervish statue
Browbeating an impetuous, younger cockerel
Perched upon an impressively life-like sculpture of a troll
Burbling contentedly over strewn seeds and millet
Petrifying a willing dwarf missionary to the plane of earth
Cackling as a large cat calcifies before your very eyes
Plumed like a peacock, feathers prized as scroll quills
Caught in a ground snare, flapping furiously
Pouncing on a giant rat, soon to be stone
Cawing a call-and-response to others in the area
Prancing about a statue studded clearing
Chasing down a frightened fox
Preening and stretching after a brief nap
Chattering from a high perch, preparing to roost
Protecting their chicks from a stealthy warp beast
Chortling and dancing around a statuette of a hawk
Puffing out chests to intimidate a giant tuatara
Circling above a field of crops, scaring farmers
Raking their beaks across the trunks of withering trees
Clucking as they examine a granite gnoll
Rambling around a rock ranger, drawing her sword
Coaxing chicks from a nest with hissing purrs
Restless hens stomp the ground, waiting for their cockerel
Coiled around a calcified cleric, rattling unique tails
Roosting on shoulders of a petrified, grimacing hill giant
Completely flustered by a living statue
Rubbing their tails on a rough rock, scraping off shed
Cooing as they munch on wriggling worms
Ruffling scales and feathers to warm up
Crouching defensively, about to strike at a shadow
Scanning the sky after hearing a bird-of-prey shriek
Crowing defiantly atop a limestone lizard man
Scraping and eating verdant moss from an orc statue
Defending their territory from hungry hellhounds
Scratching at detritus, swallowing fleeing mice whole
Deftly dodging a halfling hunter's crossbow bolt
Screaming cacophonously at an immune mongoose
Digging at the dirt for choice miniature mushrooms
Settling on the antlers of a very accurate deer statue
Diving for a brightly colored lizard, scrambling away
Sitting on small mounds, brooding
Dustbathing in a patch of shimmering sand
Sought for their feathers for high-fashion millinery
Eagerly awaiting the gnome sage who feeds them
Sparring as medusa place jewelry-laden wagers
Easily spooked after an encounter with skeletons
Spurring a rapidly solidifying soldier of fortune
Escaped from an orc cockfighting ring, very ornery
Squabbling over a twitching giant centipede
Escorting a hen to a newly discovered den
Squawking with maniacal glee, rolling around in dirt
Flapping furiously as they fight a giant ferret
Stalking snails, leaving behind beautiful fossilized shells
Flitting swiftly to-and-fro, on high alert
Stammering out a staccato cock-a-doodle-do
Flogging a flint friar, frozen with a look of shock on his face
Staring down a grizzly bear, rearing up and roaring
Flouncing combs and tails to impress disinterested hens
Stomping over statues of sleeping figures in bedrolls
Fluffing feathers and spines to become more imposing
Stridently peeping as they search for missing nestlings
Fluttering clumsily from perch to perch, falling occasionally
Strutting confidently after stoning a berserker
Foraging on a leaf-strewn floor for food
Stumbling their way up a tree to find a place to sleep
Gathering the flock around a saltlick with strident clucks
Sunning themselves on a large flat rock
Gobbling up grubs from a splintered, rotting log
Swallowing gastroliths to stock their gizzards
Growling at the ghoul who tends them
Swooping with speed at a dodging kobold
Guiding pullets away from a dangerous drop
Tapping their beaks against stones to attract prey
Hackles raised at a gorgon stomping through their nests
Trilling quavering calls after the death of their rooster
Harassing a hobgoblin camp, barely kept at bay by spears
Turning a knight's warhorse to stone underneath him
Hissing at a gargoyle, who swats them off when they land
Utilized for divination by some particularly brave acolytes

Table: crab, giant
Abandoning a dried-out burrow, filled with sun-bleached shells
Managing to wrest a harp from a distracted harpy's hands
Absconding with a sleeping sailor's sword
Mechanically squeezing the life out of a kobold
Adorning itself with stinging anemones
Migrating en masse to the nearest shore
Alerting others to a dead seal, just washed in
Molting and timid, avoiding confrontations with each other
Ambushing a brave beachcomber in search of salvage
Munching on a cracked cask of spilled hard tack
Attempting to repel a hungry leper, armed with a pitchfork
Navigating spiny shards of coral with ease
Barreling into a bunch of buccaneers burying treasure
Nipping at annoyed wyvern, feasting on a beached humpback
Basking in the sun after receiving a sudden chill
Nosily scurrying across the rocks
Being decimated by a giant tuatara's teeth
Occupying a giant's helm as an ersatz shell
Burrowing into the shady side of a dune
Ousting a normal-sized otter from a favorite den
Cannibalizing one of their own, soft/vulnerable from molting
Painstakingly investigating the water line for tasty flotsam
Circling each other, clacking claws in courtship
Pale, peeling carapaces reveal that they will soon need to shed
Clinging to an impossibly large (think sequoia) piece of driftwood
Picking at a very large starfish, the size of a wagon-wheel
Crushing open a sea-encrusted wine bottle
Preventing a small rowboat from landing here
Daintily nibbling on a dead dolphin
Prized dish of a nearby bribe-able halfling sheriff
Dancing around to the tune of a bard's flute
Proudly raising their larger, more colorful claws in unison
Dashing towards the shadow of a sea gull
Quibbling over the contents of a turtle nest
Decorating a tidal pool with shiny finds
Racing side-ways, away from a giant toad
Defending a choice boulder, tossing aside smaller interlopers
Ransacking a small hut, door blown off its hinges by a storm
Deftly side-stepping a merman's trident
Rapidly withdrawing, several are smashed by a troll's mighty club
Depositing gelatinous eggs inside a damp divot
Receding in a wave as a roc's shadow slinks across the sand
Developed a taste for human flesh after a recent flood
Ridden by sand pixies, armed with wickedly barbed lances
Digging a pebbly pit to store sea water when the tide leaves
Rummaging through an overturned cart as a nervous horse whinnies
Displaying upraised claws while an unimpressed female looks on
Scampering crabwise after a giant rat
Ducking under a shady outcrop before the hottest part of the day
Scavenging the still-twitching catch from an old net
Each has a carapace that looks like a warrior's face
Scrambling for the best position atop a giant stone head
Eating a shipwrecked pirate, dead for weeks
Scuttling atop an overturned lifeboat, muffled yells inside
Evading a hungry giant hawk
Serving a vivimancer, has replaced her left hand with massive claw
Even when severed, claws won't unclamp for days/nights
Sheltering in an intriguing cave, only accessible when the water is low
Evicting a smaller rival from its burrow
Skirting the edges of a lizard man camp
Excavating a new den higher up the beach
Sprinting away from a gluttonous crocodile
Favorite food of a nomadic pack of gnolls
Stacking uniformly sized rocks into pyramidal cairns
Feasting on rotting fruits, washed up in the foam
Starting to outgrow the rusty bucklers and shields they use as shells
Fighting over stinking strips of blubber
Stubbornly grasping at a ghoul in an iron gibbet
Filling the air with loud, threatening claw-clacks
Surprisingly adept at tree climbing to rob nests
Flaunting new spiny nautiloid shells
Tamed long ago by a nearby kelp dryad
Gorging themselves silly on rotting remains of a sea serpent
Tenaciously pinching a trader, screaming for help
Grappling with each other, occasionally tearing off a claw
Terrorizing a local fishing community due to population boom
Grazing on washed up seaweed and kelp leaves
They seem drawn to a claw-topped staff, stuck upright in the ground
Guarding a mermaid, unconscious and washed up on the rocks
Toppling a magically lit obelisk, carved with strange runes
Hiding a secret - their dance tells the tide when to come in
Towing a tattered fishing net, caught on a leg
Holding a hungry, hook-handed goblin at bay
Trying on a larger, more colorful, shell on for size
Holing up after sensing an upcoming squall
Upsetting local fisherman by camping out on the pier
Ignoring the toppled over chest, spilling out gold on the beach
Venturing cautiously from crevasse to crevasse
Inhabiting a wind-blasted and beached brigantine
Voraciously ravaging the shallows after spawning fishes
Inspecting the sands with beady eyestalks
Wading into the water in search of mollusks
Jerking a rusty chain, half buried in the beach sand
Watching the largest male for signs of weakness
Jostling for pungent scraps from a washed-up whale
When seen at night, bioluminescent algae on them glows eerily
Lashing out half-heartedly at a squawking bird
Wrenching a golden hand-mirror away from a weeping mermaid
Luring pterodactyls to land by feigning injury
Zigzagging to flee from a diving griffon

Table: crocodile
Allowing brave birds to clean between their teeth
Parting thick reeds and plants as they swim
Ambushing an unsuspecting thirsty deer
Prized for their rune patterned scales
Bothered by omnipresent mosquitos
Proudly bearing recent wounds and an arrow shaft
Bound to a local swamp druid via ritual
Rare leucistic specimen
Chomping stubbornly on a hapless tortoise
Retreating from the loud crash of a falling branch
Draped in a flowering water lily disguise
Serves as eyes and ears for the lizard man shaman
Drowning a stubborn dwarf veteran
Shedding salty tears above gently smiling jaws
Emitting guttural chirps and calls to hatchlings
Splashing about loudly, wrestling a giant snake
Former loggers, fey cursed into this form
Stealing a giant catfish from a panther
Gripping a severed, mail covered arm in their teeth
Sunning on a boggy bank
Throwing head back, gulping a feathered heron
Swimming swiftly through the duckweed
Guarding a muddy mound that has begun to chirp
Thrashing in a fisherman's net
Juggling a giant crab in powerful jaws
Tolerating their use in a swamp sprite regatta
Lazily impersonating logs
Transporting hatchlings with lightly clenched jaws
Looking for a nesting site to lay ovoid eggs
Wallowing in a muddy gully to stay moist

Table: crocodile, large
Bellowing low, vibrating the waters to attract females
Plagued by pulsating leeches and irritable
Clamping down on the tough shell of a giant crab
Protector of an ancient cypress treant
Coated in magical mud that makes them immune to arrows
Prowling the perimeter of an abandoned barge
Death-rolling a swamp elk as scavenging ravens squawk
Slinking in the spaces between massive mangrove roots
Dragging the rotting remains of an ogre, stashed in the depths
Slosh through shallows, nosing out giant clams to crush
Flailing, locked in the embrace of a huge constrictor snake
Sulking after defeat by a larger interloper
Frenzied free-for-all over a dead ox
Waylaying a trader's raft, laden with pelts and trade goods
Growing fat on a weekly feedings by lizard men
Wearing an ancient, un-rusted iron collar
Hauling itself slowly ashore with a distended belly
Writhing from recent meal - troll is disagreeing with them
Hissing at smaller crocs as they jockey for sunning spots
Yawning with a gaping mouth large enough to walk through
Leaping from the water to snatch a treed troglodyte
Unblinkingly staring at a canoe cutting through the water
Local folklore has named this maneater - old tetch
Towing a shredded caecilia to feed wolf-sized young
Lurking below a tree as monkeys chatter above
Loitering near to the surface, acting as an ersatz sandbar
Mauling a horse, half-sunk in the mire
Startling a hobgoblin war party by ramming their flatboat
Mouth open and panting to cool off in the hot, humid air
Sunbathing as a brownie scrubs her scales, whistling

Table: crocodile, giant
Accepting swamp boar offerings from fearful lizard men
Learned the language of all things long ago, loves riddles
Agape as a gutsy ranger chisels a rotting tooth, tall as herself
Lunging at a lapping sabre tooth cat
Alarming a local stilt village by swimming too close
Mobilized for war vs dry skins, bearing howdah and archers
Basking amid toppled trees, could be mistaken for an island
One eye is replaced with a crystal ball
Being stalked by swamp giants who've already lost hunters
Only challenger is a terrestrial dragon turtle
Capsizing a caravel, laden with pirates and their treasure
Slipping their way down a wide river toward a vital dam
Crushing the throat of a thirsty titanothere
Spooking a young black dragon, just setting up a lair
Dragging a dead mastodon away from the shore
Studded with buckler-sized barnacles, additional armor
Drawn to an crumbling ziggurat built by ophidians of old
Submerging (st time in decades), flooding a village she carries
Feasting on a gold dragon, scales glittering in the sun
Surprising a stegosaurus wading in the swamp
Felling ancient trees of an elf village, spells/arrows flying
Swallowing a warhorse whole
Floating in a lake, dug herself centuries ago
Swimming seaward, to deliver a message to the brine queen
Generating huge waves with a slap of the tail
Tolerating the wizard's tower perched on his back
Gnawing on the neck of a lesser sea serpent
Triumphantly toting a tyrannosaurus leg
Impossibly ancient, covered in moss and lichens
Worshipped and dreaded by a local crocodile cult

Table: cyclops
Curses - alcohol is now a deadly poisonous
Harvesting voluptuous clusters of deep indigo grapes
Curses - beleaguered by swarms of biting gnats
Hauling bath-tub sized buckets of water uphill to water the slopes
Curses - blades held dull in an hour
Heavy eyed, drowsily blinking as they count their sheep
Curses - clerical spells fail half of the time
Hurling hewn boulders at a hydra
Curses - clothing worn tatters in days, shoe soles spring holes
In desperate need of small hands to help milk their ewes
Curses - coins touched debase by a metal, down to lead
Inebriated and bloodshot after being swindled by a shepherd
Curses - enjoy new, dangling donkey ears
Jubilantly tipsy, singing bawdy songs learned from sailors
Curses - languages possessed change to others (reading only)
Known far and wide for valuable varietals
Curses - magnet for lightning strikes during next three storms
Lecturing a sage on oenology with stammering speech
Curses - no longer able to perceive or describe the color blue
Lobbing rocks at bugbear sheep rustlers
Curses - nose falls off, still works for smelling, just don't lose it
Locating a lost lamb, carrying a thirty-foot crook
Curses - over the course of a night, eyes merge into one
Loves to tell rambling tales of their former adventuring life
Curses - peculiar form of lycanthrope - were-sheep
Making offerings to the brine queen
Curses - perceived as a wolf by horses, cows, sheep
Melting pine resin to seal amphorae
Curses - suffer minor harm when proper names are uttered
Not amused by mischievous mutton-busting sprites
Curses - teeth blacken and fall out, grow back in a month
Overseeing halfling hired hands, picking precious grapes
Curses - the hafts of any wooden implement held sprout thorns
Painstakingly selecting specific grapes for a special vintage
Curses - upon waking, one owned item goes missing
Paying marooned pirates handsomely for pigéage
Curses - vomit forth worms when a weapon name is spoken
Peacemaking between two rutting rams
Curses - waterborne vessels set foot in will spring leaks
Peeling off large strips of bark from gnarled cork trees
An accomplished druid - all grapes are goodberries
Pouring jugs of blood on trellis bases as fertilizer
Arguing about religion with a visiting hill giant
Putting the finishing touches on an immense pergola
Bending down to trim treetops, more sun for grapes
Retrieving wicker wrapped feta wheels, cooling in a cave
Blendindg troll-blood into their wine for added "kick"
Roasting mutton, at least seven sheep worth on spits
Boiling a humungous haggis in a coracle-sized cauldron
Rolling a giant rock to seal prisoners inside their sleeping cave
Burying a toad beneath each grapevine to fight blight
Rounding up a fluffy flock for shearing
Carding wool and humming ancient hymns
Sacrificing a prized silver ram to induce rain for her vines
Carving an ornate cithara from a still growing cypress
Sharpening shears on a spinning wheel-sized whetstone
Clumsily plucking pests from their vines
Slaughtering the hobgoblin patrol that trampled their vines
Collecting herbs and plants to flavor libations
Squinting through a cataract - losing their sight
Completely in their cups after tapping a cask of claret
Staking in trellises - old spears from a nearby battlefield
Conned into buying "magic" grapeseed by a clever halfling
Stirring a vat of dark, blood-colored must
Constructing an enormous wall from boulders
Straining sheep milk yoghurt into stone troughs
Coopering ogre-sized oaken barrels to store their plonk
Studied magic under famous wizard - flock is their spell book
Defending their flock from a pack of hungry dire wolves
Supervising thirsty satyrs as they operate a winepress
Digging irrigation canals by dragging a huge axe
Sweetening wine with honey from giant beehives
Docking the tails of bleating lambs
Swindled by gnomes into building a cyclopean palisade
Drunk on their potent retsina and hungry for man flesh
Tenderly tending to an ewe lambing
Famous among clerics for a very special, sacramental vintage
Terroir turf-war between elf neighbors
Fearing the impact a sudden frost will have on his vines
Their small flock of ewes with gilded wool is heavily guarded
Fishing a very drunk faun from their fermentation vats
Tilling deep red earth with a team of gorgons
Fleeced out of twenty bushels of wool by a savvy trader
Tricked into trading their gold for platinum plated copper
Forging magical javelins - turn to thunderbolts when thrown
Using semi-trained hellhounds to corral a slightly singed flock
Forming man-sized amphorae from fragrant umber clay
Very impressed with an enslaved dwarfs' wool-spinning
Glowering with their eye, like a shield fourfold hide in size
Whittling nubile nymph scrimshaw from mastodon tusk
Green-harvesting grapes for a more potent yield
Will do anything to rid his vines of a creeping grey mildew
Grieving loudly after leaf damage from a recent hailstorm
Wines treasured for medicinal properties, can cure most diseases
Grimacing after being rebuked by a dryad
With just a single step, treading an entire tank of grapes
Grinding bones, not for bread, but to enrich the soil
Worried about a suspected werewolf attack on his flock
Haggling a dyer, growing more delicious by the minute
Yelling at their vines to encourage them to climb stakes

Table: human, dervish
Accompanied by a powerful magic-user and her golems
On a holy pilgrimage, will broker no delays
Allied with a local werebear convert to their faith
Peerless riders, fire bows from beneath their steeds
Anointing a new commander according to special strictures
Perfuming thick padded gambesons
Basting a spit-skewered goat with delicious smelling spices
Polishing chain mail by rolling it in a barrel of sand
Beating clouds of colorful dust out of rugs
Pounding sticky, almond-studded dough into flat sheets
Being stalked by a ferocious manticore
Praying prostrate with fervent devotion
Bending their recurve bowstaves to unstring them
Preparing fastidiously for a visit from their leader
Beset by ravenous ghouls, losing the battle
Putting a blaspheming acolyte to the sword
Burning a pungent incense that allows them to forego food
Raising a fallen ally from the dead with powerful prayers
Burnishing exotic helms and gauntlets
Ranks bolstered by porcelain living statues
Carefully packing sacred scroll tubes
Receiving a holy blessing of sacred waters
Celebrating after routing a hobgoblin army
Recent encounter with a wraith has shaken their faith
Cheerfully breaking a fast with a sumptuous feast
Rely on intelligence gleaned from animal speech
Clearing an area in order to bivouac for the night
Riding cantankerous but quick camels
Considering a ransom offer for a captured leader
Safeguarding a sisterhood of six gifted seers
Convincing a storm giant to help their crusade
Searching for a stolen sacred relic
Count a surprising number of zealous gnolls among them
Sent by visions to consecrate a dangerous dungeon
Covering the sacred symbols on their shields
Settling a doctrinal dispute between their two best warriors
Defending women and children from skeletal soldiers
Shaken by recent ill-omens and bad fortune
Dining on morsels of meat, impaled en brochette
Shifting an intricately engraved boulder onto a sledge
Discussing the merits of martyrdom
Signing a peace treaty with a powerful pontiff
Dismounting to negotiate a treacherous rocky slope
Singing soft psalms and pious prayers
Dressed like lepers, covered head to toe in cloth
Solemnly burying a champion of the faith
Drinking a fragrant black tea from ground up berry piths
Spurring on their steeds after an escaped prisoner
Erecting a heavily decorated, but temporary shrine
Startled to discover spoiled food stores/supplies
Escorting gnome merchants in a lucrative arrangement
Stopped suddenly, a warhorse appears to be injured
Evangelizing to a cleric of a similar faith
Subsisting solely on cleric created food
Exhausted from a campaign against brigands
Suffering bitter defeat at the hands of heathen druids
Exposing a chaotic cult's influence in a nearby city
Suspicious of elf allies, fighting orcs at their side
Faces concealed by beautiful metal masks
Swaying rhythmically to ecstatic music
Fastidiously washing their hands in rose-scented waters
Swearing oaths to defend a crucial hilltop fort
Fasting today and surprisingly irritable
Swinging censers that billow blinding smoke
Follow the orders of an unusual leader - a minotaur paladin
Taking down the colorful tents of their camp
Gagging a captured medium to prevent spellcasting
Talented musicians, to a one
Guiding their mounts across a shallow ford
The cleric that leads them is a reformed medusa
Handing out loaves of bread to starving villagers
Their mobile camp is transported with the help of friendly rocs
Infiltrated by a doppelganger, shifting them towards chaos
Tracking an infamous heretic with dangerous, idolatrous ideas
Invading with the secret blessing of a dwarf king
Transporting a sacred, undying flame in a mithril lantern
Keeping tabs on surrendered bandit prisoners
Travelling to a quarantined village to cure plague
Known far and wide as excellent judges of horseflesh
Unfurling elaborately woven carpets
Laden with valuable plunder from their campaigns
Unknowing carriers of a devastating new disease
Leading a group of fettered berserkers
Unsheathing arms for inspection
Led by a surprisingly devout, disguised gold dragon
Using magic to converse with a slow speaking oak tree
Lifting an incredibly heavy and gilt sacred altar onto a wagon
Uttering prayers over every link of a suit of chain
Listening intently to a sermon from a cleric
Vigorously debating a religious interpretation
Loading plunder into saddlebags
Warring against a faith that preaches pacifism
Loudly chanting melodious litanies in lawful
Watering their horses at an ancient mule-powered well
Milking strange livestock from foreign lands
Welcomed by a local halfling community for the spices they trade
Need additional mounts, will commandeer any they see
Whirling gracefully with weapons drawn in a ceremonial dance
Oiling ornate leather armor
Wielding wavy swords of superior steel

Table: djinni (lesser)
Advising their master on the finer points of diplomacy
Gaslighting a prince who thinks he's haunted by ghosts
Billowing forth from beneath a door
Giggling as she dumps a sack of gold coins at a trader's feet
Blinding a group of avaricious acolytes with a cloud of sand
Hauling his master's enemy into the heavens
Breaking iron chains with their bare hands
Lounging on sumptuously stitched silken cushions
Calling forth a fantastic feast, fit for an emperor
Lugging part of the hoard of a very peeved dragon
Cautioning their master against the follies of greed
Playing a cheerful tune on a mithril flute
Charming a queen's consort with witty repartee
Rolling a huge stone to seal a treasure-laden cave
Chortling unseen as he frees hitched horses
Scattering a company of brigands with a furious samiel
Conjuring a golden medusa bust from thin air
Smoking ornate pipes with a group of air elementals
Constructing a stone tower in record time
Sneaking up on a royal escort to steal the crown of a king
Debating with a dervish who's beginning to doubt
Steering their master subtly toward good deeds
Directing an illusory morality play for children
Toppling troops as a tremendous tornado
Evaporating into a billowing chartreuse cloud
Transporting their master to their newly minted mansion
Fabricating an intricate copper cage to house a phoenix finch
Tricking a tribe of lizard men into thinking he's their leader
Fading from view with a finger on the lips of a sly grin
Wooing the object of their master's desire
Serving an ambitious acolyte - motivated to build a tremendous temple
Serving a merman missionary - travelling dry lands to spread sea gospel
Serving a blinded beggar - can't believe things are looking up
Serving a miserly mudlark - never know what washes ashore
Serving a blue-blooded bandit - can't seem to pawn it serving a naïve gnome - think they can make a better world
Serving a cautious cartwright - well-versed in all the old tales
Serving a newly minted gnoll matriarch - her pack decimated by orcs
Serving a deported dwarf - looking to get back in their clan's good graces
Serving an odious ogre - each task grows more outlandish
Serving an elf entertainer - spreading their fame far and wide
Serving a playful princess - gift from a foolish suitor
Serving a formerly unlucky fisherman - reeled it in, expecting a fish
Serving a pure-hearted pirate - pining for his own fleet
Serving a gormless goblin - squandering power on puerile pranks
Serving a reformed rakehell - making amends for all those they wronged
Serving a happy halfling gourmand - stuffing their face silly
Serving a secretive centaur smith - wants what's best for his tribe
Serving a heartbroken harpy - rebuffed by a handsome sailor
Serving a simpleminded cyclops - found it tilling their vineyards
Serving an infamous footpad - won the pocket-picking lottery
Serving a troublesome treant - left unchecked, cities will fall to the wild
Serving a jealous giantess - hoarding princes
Serving a vainglorious vampire - pampered and well-fed
Serving a lovesick satyr - seeks soul of soulmate from the underworld
Serving a veracious veteran - rewarding good deeds
Serving a maimed minotaur - hunting down his nemesis
Wishy-washy wyrm - just one of many trinkets in her hoard
Serving a megalomaniac medium - with predictable outcomes
Serving a wistful wife - spouse off at war for almost a decade

Table: doppelganger
Affecting the mien and mannerisms of a wealthy majordomo
Impersonating a well-known and impossibly pious paladin
Assuming the guise of a well-loved bandit leader
Inciting the overthrow of an ogre empress
Back-stabbing allies by turning them in
Infiltrating a tribe of lizard men after slaying their shaman
Beguiling a skulk of bugbears by impersonating their chieftain
Informing on a spy-network to monopolize the market
Betraying an orc enclave to a powerful sorcerer
Inveigling favors from a love-struck elf prince
Bilking berserkers out of hard-won treasures
Inventing a pretender to the throne and gaining followers
Blackmailing a princess with incriminatingly accurate etchings
Keeping tabs on their lackeys by posing as one of them
Brainwashing villagers, starting a chaotic cult
Luring heroes into the jaws of a dragon as a purported princess
Bribing dwarf merchants with counterfeit coins
Machinating with nearby harpies to poach prime maritime lanes
Cheating a widower out of his wergild
Masquerading as a gnoll matriarch with a loyal, laughing pack
Colluding with the goblin king to eliminate an npc party
Mimicking the parent of a pc perfectly
Commandeering supplies under the guise of a knight
Misleading gnome prospectors with deeds to salted mines
Concocting convoluted conspiracy theories for their leaflets
Orchestrating an invasion from an empire overseas
Conniving their way into kobold leadership
Ordering thoul stoolpigeons around
Conspiring to overthrow the king of the dwarfs
Outwitting a bounty hunter who suspects their true nature
Corrupting enlisted men with seditious speeches
Overthrowing the don of a powerful crime family
Debasing the rule of law as a famous magistrate
Playing both sides of an escalating conflict between dukes
Deceiving dervishes, as a long-dead prophet resurrected
Plotting to topple a potentate through strategic blackmail
Defrauding a wealthy warlord as an itinerant bard
Poisoning the relationship two aristocratic families
Deluding the king's only daughter to take the cloth
Portraying a beloved bishop to sow heresies
Devising plans for sparking a hundred-year civil war
Posing as a well-loved sovereign, disguised among the masses
Disconcertingly asphyxiating a copy of themselves
Pretending to be a medusa, replete with petrifying wand
Displacing the head of a local thieves guild
Prevaricating frantically during interrogation by their mark
Disrupting the chain of succession by assassinating heirs
Promoting an overlord their sure to overthrow
Diverting a hobgoblin hoard to fund further schemes
Ransoming themselves for the fourth time
Double-crossing their own cabal
Sabotaging a clandestine treaty between bellicose barons
Duping local brigands out of hard-earned hazard pay
Scamming local villagers as a tax collector for the crown
Employed as an assassin, but surprisingly remorseful
Scheming alongside duped troll enforcers
Eroding confidence in a priest by appearing in unseemly places
Seducing each of the queen's ladies in waiting in turn
Extorting a merchant, after selling him contraband
Seizing command of a band of brigands
Fabricating witnesses for an upcoming crime and ensuing trial
Serving as a mole in a tavern, bushwhacking lucky adventurers
Falsifying a wanted poster to collect a bounty on another identity
Sowing seeds of disharmony in an otherwise peaceful elf village
Fanning flames of feud betwixt noble houses by jilting a patriarch
Spying on another of their kind - elaborate courtship rituals
Feigning helplessness as a halfling rabbit rancher
Strangling an archduchess on their wedding night
Finagling their way into the good graces of a fire giant fiefdom
Studying the mannerisms of the gargoyle king
Fleecing a shrine of all its holy relics by impersonating a saint
Subverting their discovery by pinning murders on a medium
Foiling a peace treaty between the elfs and dwarfs
Successfully imitating a sage, famous the world-over
Fomenting discord between dungeon factions
Suffocating an illusionist who saw through their disguise
Fooling even a familiar after replacing their master
Supplanting a highborn heir of a wealthy estate
Framing local adventurers for a foul murder
Swindling the grieving bereft with help from a chaotic cleric
Funneling filched funds into the coffers of orc mercenaries
Tempting a chaste cleric from his vows
Gagging their mark to study their mannerisms more fully
Throttling an assassin, sent to slay them as an ersatz czarina
Garroting a gambler, whose luck ran out
Thwarting inheritance by posing as a midwife, stealing children
Goading goblin bodyguards to make a play for the throne
Treacherously turning on the trusting tomb raiders they hired
Hampering a kidnapping investigation by turning up safe
Undercover as an urbane urchin
Hatching a scheme to have a local druid burned as a witch
Undermining the ruler's confidence in his once trusted advisors
Hijacking a ransom drop by impersonating the recipient
Usurping the role of gnome brewmeister
Hindering a witch-hunter by planting evidence
Working off indentured servitude to their vivimancer creator
Hoodwinking authority by resurfacing as a long-dead highwayman
Wresting control of a travelling circus after a series of accidents
Impairing peace-talks between kingdoms embroiled in embargo
Wringing the neck of a mark as their face contorts to match

Table: dragon turtle
Aquatic goblin hitchhikers - tolerated for parasite control
Generating a great wake, where blink seals frolic
Back flipper impaled by an impossibly large narwhal horn
Gulping sailors, swimming to land from a sinking ship
Biting off the bow of a buccaneer's frigate
Half-buried on a shallow seabed - dangling a golden tongue
Blinded in one eye from barnacle growth
Hauling itself up a sandy beach to destroy a lighthouse
Camouflaged by the vast school of fish, feeding on shell algae
Holding a port town's docked vessels hostage for tribute
Capsizing a fleet by swimming a whirlpool
Painting the sky with vast plumes of steam
Caught on a titanic iron hook, baited by a caecilia
Recent residency has disrupted prime shipping lanes
Chomping a giant squid clean in half
Reefs on the shell are habitat for desirable alchemical reagents
Circled by scavenging mako sharks, patient for scraps
Rune-scribed shell binds it to do no harm to elfs
Devastating an undersea merfolk settlement
Shell covered in intelligent, magic using giant crabs
Diving deep to drown an orca in her jaws
Snacking on barn-sized jellyfish
Dragging a net full of at least a dozen muskmelon-sized pearls
Surrounded by breathable bubbles from a bound djinni
Dredging the site of a legendary shipwreck to augment his hoard
Tracking a pod of sperm whales by sound
Encircled by a sea serpent, locked in combat
Utilized as a formidable war machine by seahorse centaurs
Fitfully dreaming of flight on the floor of the sea
Visiting the ancient kelp forest dryads for advice

Table: driver ant
Abandoning their lair due to a slow-burning fire
Hauling a statue of a hobgoblin out of the nest
Accidentally entombing a hibernating vampire
Heaping uniform hay sheaves into piles for a gnome friend
Amassing undigestible metal into an organized pile
Kneading the pulsating abdomen of their egg-laying queen
Ambling aimlessly, seeking a scent-trail home
Lugging an impossibly large writhing caterpillar
Amputating the arm of a screaming goblin
Mangling an equipment-laden mule
Anointing themselves with acidic secretions to kill parasites
Marching interminably, always on the move
Avoiding an inert earth elemental they inadvertently unearthed
Meandering listlessly due to conflicting pheromones
Beheading a fire beetle in a single, swift strike
Mechanistically shoveling small stones to form a tall hill
Biting at the bases of tree trunks for sickeningly sweet sap
Meticulously deracinating all plants for yards around nest
Blazing a trail from their mound to a nearby pond
Mysteriously unearthing coffins from beneath a nearby cemetery
Blundering into the insatiable mouth of a hungry giant tuatara
Nibbling inquisitively on a sack of dryad apples
Brick red, invasives with an excruciatingly painful sting
Oblivious to the myconids who share their nest
Burrowing tirelessly in extremely hard soils
Patiently trudging, stopping only to greet returning comrades
Busily excavating around a strange, symbol carved boulder
Plastering the entrance to their anthill with poisonous plants
Capable of spurting defensive formic acid
Plodding back and forth from a dead purple worm, carrying food
Caressing each others antennae to communicate
Proudly parading pieces of dead tiger beetle back to the nest
Carrying large, tower-shield sized eggs to a new nesting area
Pursuing a team of kobold egg-stealers
Chewing through thick beams, left by long dead miners
Quarrying strange cuneiform covered slabs to tile floors
Chomping ravenously on a dead cave locust
Ranching wolf-sized aphids for their sweet excretions
Climbing over a yellow mould infested bone-pile
Ravenously gnawing through tough scales of a giant snake
Collapsing the chamber a giant tarantella has moved into
Regulating mound temperature by sealing ventilation holes
Conveying comrades across a river with an ant-built bridge
Regurgitating food for bloated, ceiling suspended nest mates
Creeping along walls to avoid green slime on the floor
Relentlessly patrolling, on high alert due to alarm pheromones
Crunching large nuts into a digestible paste
Repeatedly ripping apart stubbornly re-animating skeletons
Cultivating a breathtakingly beautiful fungal garden
Scooping moist, loamy soil around giant mushrooms
Dawdling down a path, stopping to stroke everything thrice
Scrabbling frantically up the sides of a sandy funnel
Depositing corpses in a pit of mulch and leaves to decay
Scraping downy lichens from strategically placed stones
Diligently delving next to an ancient barrow
Severing a troll leg, hes trapped in a gluey amberish prison
Dividing a giant grasshopper into more portable portions
Shield-headed, used to seal off entrances/passageways
Dogpiling on a ferociously thrashing giant wasp
Shunning a nest-mate, infested with cordyceps
Drinking deeply from a magical spring that provides crude speech
Smearing themselves with strange, bioluminescent goo
Earnestly dragging a dead and still heavy horse
Snipping off shrieker caps, unconcerned with the noise
Eerily motionless, save for the infrequent flick of antennae
Stalking an adventuring party by scent
Escorting their bloated queen on their backs
Stockpiling prodigious grain stores, pilfered from farms nearby
Executing a decrepit queen while her successor watches excitedly
Strangely stick-like, scouring the ground for fallen fruit
Expertly evading strikes from a giant scorpion invader
Sundering the spear of a surrounded veteran
Explosive - charge toward any foes and burst in a shower of acid
Tending reverently to a chthonian shrine of black basalt
Extirpating enemy invaders from a rival hive
Tilling furrows around their hill in preparation for heavy rains
Feasting upon the carcass of a moose
Tirelessly defending their nesting chamber from robber flies
Feeding an antling royal jelly to replace their dead queen
Towing a dead but still oxidizing rust monster
Fending off an elephantine dire armadillo
Transferring gold-laden quartz to a disused chamber
Ferociously rending a rhagodessa limb from limb from limb
Treading dirt-beaten paths, radiating from a spire-like mound
Ferrying pupae away from a flooded chamber
Tugging a defeated tiger by the tail
Fleeing from a hungry caecilia
Tunneling too close to an aquifer, unaware of the flooding danger
Following a druid through a glowing portal
Uprooting leafy bushes and saplings to feed their fungal gardens
Fortifying a crumbling tunnel with layers of spittle-mud
Vomiting a nourishing fluid for their queen to feast upon
Grasping at the legs of a giant spider, trying to pull it apart
Voraciously digging after a population boom
Grooming obsessively with their forelimbs before harvesting molds
Waving brands covered in toxic spores in their mandibles
Guarding a noisily chittering nursery brood
Wresting open an ancient iron seal, covered in binding runes
Harnessed to a wagon to haul a family of halfling travelers
Yanking playfully on a leg of a pet bard (music pleases the queen)

Table: dryad
Admiring an ancient, clonal colony of aspen
Interrogating a captured bandit found collecting firewood
Admonishing a greedy dwarf, digging at the foot of her tree
Jealous of an elf who would not succumb to her charms
Asking politely before plucking a berry from a bush
Jilting a journeyman who hasn't been seen in years
Attended by several sprites, assisting her with her beryl braids
Judging a pixie/sprite bake off featuring delicious tarts
Attending the birth-planting of a treant's acorn
Laying a false trail of flower petals to deceive pursuers
Baby-sitting two young centaur siblings
Longing for the love of a penitent priestess
Bathing bashfully in a brook
Loyally served by several lizard men
Beguiling a merchant, heaping finery at her feet
Misjudged a journey - too far from her tree,slowly dying
Being courted by a very handsome hobgoblin
Never far from her werebear husband
Beseeching a bugbear to lay down his battle-axe
Nursing an injured medium back to health
Besotted by a dashing young bard who sings sweetly
Officiating an elf wedding - two trees planted to entwine
Bewitching a chaste and steadfast knight
Pining for the paladin who wooed her, but hasn't returned
Bleeding sap as blindfolded lumberjacks hack at her home
Planting a kiss on a stupefied friar
Blushing after being offered flowers from a centaur suitor
Playfully teasing her most recent champion - a minotaur
Captivated by a found cameo containing a portrait of a princess
Pockmarked from intractable termite infestation
Catching up on the scuttlebutt with a local nixie
Preening with a magical mirror, gift from a witch admirer
Chaperoning a dryad debutante held for their daughters
Protecting her "children" ten toddler-sized wood golems
Chasing fickle butterflies to influence where they pollinate
Raised by fishermen, unaware of her powers to charm
Cherishing the heart-shaped scar lovers carved on her tree long ago
Recycling a former paramour as compost, his last wishes
Combing her tresses with a chimera bone comb
Re-homing a bodkin billed woodpecker from her tree
Coveting exotic species of trees, will pay handsomely for cuttings
Routing a goblin search-party with superb swordplay
Crowning her champion's hair with laurel leaves
Rubbing the belly of a big, battle-scarred blink dog
Cultivating colorful chrysanthemums and cream-colored cala lilies
Ruefully releasing an ogre in exchange for a unicorn's life
Daintily dining on tiny mounds of mulch, spread across a cloth
Sacrificing her tree to build a special coffin for her beloved
Dancing delicately to the sounds of songbirds
Scouring the forest floor for a misplaced engagement ring
Darning woolen socks that have seen better days
Singing lullabies as her lover drifts off to dream only of her
Delivering a sternly worded edict, from druid to a local hamlet
Slaughtering sheep - her sister was turned to fenceposts
Deserting a changeling child near the reeds of a river
Sobbing unconsolably - discovered a voracious tree blight
Don't let her youthful beauty fool you - her trees as old as the forest
Softly stroking a tiger that purrs contentedly
Enrapturing a ranger, against her better judgement
Soliciting assistance to deal with a shroud of ghouls
Enthralled woodsmen, planting saplings at her direction
Soubrettishly goading thralls to fight to death for her love
Fidgeting as she sits for a portrait, painted by an artistic paramour
Sought by the royal gardener for her green thumb
Fleeing flirtatious fauns
Soundly defeating a war band of axe-wielding orcs
Frantically scrubbing paint from trees marked for culling
Spoon-feeding hungry faces trapped in the trunks of trees
Freeing a bear from a hunter's snare
Sprucing up a clearing, so a pegasus can land and foal
Fretting over a visit from her judgmental mother
Still learning to read, struggling with a ponderous tome
Gathering gnomes for an ambitious transplanting project
Strolling through memory - tracing fingertips on tree rings
Gingerly tending a fire to cause cones to open
Struggling to shift a large, loose boulder - threatens her tree
Gouging out the eyes of one who spurned her
Swaying softly, murmuring the names of former flames
Grafting blossoms into an apple tree
Swinging, carefree, on a vine-swing
Gravid and about to bear child
Tending a dragon topiary could easily be mistaken for real
Greedily gulping wine proffered by a pixie
Trysting with a thief, far from his adventuring party
Grieving over the loss of her lover due to pesky old age
Unable to remove the mistletoe that's slowly killing her
Hanging skull windchimes to frighten superstitious lumberjacks
Visiting the local treant grove with baskets of exotic soils
Harvesting honey from her dripping giant beehives
Waging a guerilla war on encroaching charcoal burners
Helping halflings harvest wild mushrooms
Waited on hand-and-foot by well-groomed gnolls
Hiding unsightly scars on her shins from a run-in with loggers
Watching over the construction of an orc sawmill
Hunted for refusing to abandon her half-human child
Watering deadly noose vines, growing in boughs above
Idly decapacitating rose blossoms into a basket
Weaving wreaths of forget-me-nots and weeping
In love with a fiery efreeti, will end in in tragic embrace
Wringing out her hair after a long, soaking, rain

Table: dwarf
Adding dirt from distant lands to spiced cider boiling in a stewpot
Nervously navigating a scree of stones
Adjusting the position of a massive menhir for changes in the stars
Nursing singed beards from a recent salamander raid
Baiting a trap with a suckling pig for a delicacy - dire crayfish
One-upping each other with smoke rings from ornate pipes
Bargaining with a minotaur for passage through a maze
Operating a bellows to melt down silver coins for transport
Being dragged about by leashed sows that are hungry for truffles
Passing a gorgon drinking horn around
Biting chunks from a barbequed troll heart
Peeling an impressive pile of potatoes rather rapidly
Boiling boot-leather on the verge of starvation
Planking timbers that will serve as mine supports
Building a bonfire to smoke a chimera out of her den
Plucking ptarmigans for supper and fletching
Carefully rolling a large millstone down a steep grade
Poking a minecart shaped mimic with long poles
Carving a sarcophagus lid in situ
Poulticing pink sunburned pates and noses with healing muds
Casting tiny pewter game pieces in molds
Purchasing a flock from a shepherd with a single shiny coin
Celebrating the inaugural trickle of a recently built sluice box
Quarrelling over ownership of a holy hand axe
Charing just the edges of a special lichen prior to prayers
Reeking after being sprayed by a dire skunk
Chortling as they spar with shoddy goblin weapons
Resetting a deadfall trap after dragging out an owlbear
Cobbling tiny boots for a few grateful brownies
Returning from trade, laden with bread and fresh vegetables
Collecting ancient driftwood for a special, ceremonial forge
Roasting a large capercaillie on a spit, stuffed with shrooms
Combing the wooly manes of their pygmy rhinocerotes
Rushing to meet a copper ore quota
Constructing a massive charcoal kiln
Savoring the first stout droplets from a steaming copper still
Cooking ground glass in a kiln to enamel scabbards
Scouting the future route of a rivulet to power a water-wheel
Crossbow target shooting at an old tarnished tin pitcher
Sealing the bottom of a crude dugout with stinking pitch
Cutting peat cubes and stacking them in neat rows
Searching for a misplaced mithril piece
Deconstructing an impromptu forge
Sharing stories of the witch wars whilst braiding beards
Deliriously trying to wake a very dead, caged canary
Shouting swears and laughing at the echoes
De-scaling an impossibly large gar with adzes
Shucking strange albino beans into a cauldron
Dressing stone steps that lead downward
Slurping raw baby piercers on the half-shell
Driving horizontal pitons into a rock face
Smashing gold-flecked quartz with hammers
Escorting a babble of nixies to a new home after dam construction
Snacking loudly on a barrel of pickled cave herring
Examining bent trees to fell for an alpenhorn
Spinning hair into silver thread, as a bald maiden cries nearby
Excitedly filling skins and flasks from a mineral rich spring
Stoically mourning a keg that fell from a cart, cracked open
Extracting a slimy comrade from the belly of a massive cave toad
Stretching wet leather over a giant-sized shoe last
Eyeballing a chunk of granite for use in a column
Struggling to retrieve an anvil from a sinkhole
Faring badly in a fight with a flail snail
Stuffing themselves silly on huge blackened spider legs
Flavoring and warming a hearty stew with heated stones
Sweeping soot from a massive flue that leads deep into earth
Fleeing from a flaming sword wielding spectre
Taking turns biting a gold coin and remarking on it's purity
Flensing a wyvern head for the stew pot
Tanning scaly reptilian hides of various sizes
Frantically trying to save someone from beneath a fallen fir/stone
Tapping gently on stones as they search for seams
Frying catfish with a fragrant bone-meal breading
Tearing pages from an ancient spellbook for kindling
Gathering up spilt grain into rough sacks
Tenderly tending the pyre of a fallen human ally
Gingerly moving a companion, petrified from basilisk encounter
Tensely negotiating passage from a clan of feral gnomes
Glumly and crudely sewing canvas after a grizzly raided their camp
Testing out different, ineffective, hiccup cures
Gouging deep furrows in the earth with goat-powered plows
Tossing a heavy ingot of strange red metal back and forth
Hammering bronze into large flat pans
Transporting shovelheads, horseshoes to a village for trade
Hanging sodden cloaks and clothing to dry in the wind
Trying to coax a goat down from an escarpment with onions
Helplessly boiling water as their human companion goes into labor
Tuning an enormous bronze bell for a local cathedral
Holding a whistling contest for all comers
Up to their waists in thick clay, cramming clumps into baskets
Installing a hook-handed prosthesis on a willing patient
Urging a temperamental donkey across a stream
Listening politely to a missionary from the plane of fire
Using specially trained squirrels to retrieve hazelnuts
Making corrections to runes carved on a boulder
Wagering on a stone-skipping contest, the record is
Hops
Making quick work of a nuisance of kobolds
Wafting fragrant laurel leaf smoke to calm giant bees for wax
Mapping out a suitable route for an annual secret pilgrimage
Whittling impressively detailed wooden ducks

Table: efreeti (lesser)
Attacking an unsuspecting djinni with wild abandon
Laughing maniacally as plans to gain her freedom come to fruition
Bending the truth to the point of breaking
Lying to their master after completing a task
Burning brightly and fuming at their bondage
Melting an intricate lock with a single touch of a finger
Carrying a roc egg, pilfered from a nearby nest
Puzzling on how to entrap a master who seemingly wants little
Coaxing a flame salamander to join their mission
Seducing their master with hollow promises
Counselling a more worthy master on how to steal her bottle
Slowly dominating a weak-willed master
Creating a temporary treasure hoard to bargain with an ogre
Smiling like a reptile, replete with a forked tongue
Fastidiously grooming in front of a melting mirror
Snorting with derision as they fulfill a pathetically simple task
Forming a flaming wall to protect their master
Spiritlessly schlepping chintzy gewgaws and baubles
Gossiping with a fire elemental about goings-on back home
Stoking vengeful urges in an otherwise even-headed master
Grudgefully vanishing when she's needed most
Subverting a wish for wealth with ill-gotten gains
Guffawing at an off-color fire giant joke
Summoning a sumptuous smorgasbord for hungry master
Heat-shimmering slightly as they evanesce
Tempting a virtuous paladin with cleverly forged quest object
Howling with rage after being tricked by clever deception
Warping the wishes and requests of their master
Immolating an insect swarm as a conflagrant column
Withering under increasingly outrageous demands
Serving an ambitious acolyte - motivated to build a tremendous temple
Serving a merman missionary - travelling dry lands to spread sea gospel
Serving a blinded beggar - can't believe things are looking up
Serving a miserly mudlark - never know what washes ashore
Serving a blue-blooded bandit - can't seem to pawn it serving a naïve gnome - think they can make a better world
Serving a cautious cartwright - well-versed in all the old tales
Serving a newly minted gnoll matriarch - her pack decimated by orcs
Serving a deported dwarf - looking to get back in their clan's good graces
Serving an odious ogre - each task grows more outlandish
Serving an elf entertainer - spreading their fame far and wide
Serving a playful princess - gift from a foolish suitor
Serving a formerly unlucky fisherman - reeled it in, expecting a fish
Serving a pure-hearted pirate - pining for his own fleet
Serving a gormless goblin - squandering power on puerile pranks
Serving a reformed rakehell - making amends for all those they wronged
Serving a happy halfling gourmand - stuffing their face silly
Serving a secretive centaur smith - wants what's best for his tribe
Serving a heartbroken harpy - rebuffed by a handsome sailor
Serving a simpleminded cyclops - found it tilling their vineyards
Serving an infamous footpad - won the pocket-picking lottery
Serving a troublesome treant - left unchecked, cities will fall to the wild
Serving a jealous giantess - hoarding princes
Serving a vainglorious vampire - pampered and well-fed
Serving a lovesick satyr - seeks soul of soulmate from the underworld
Serving a veracious veteran - rewarding good deeds
Serving a maimed minotaur - hunting down his nemesis
Wishy-washy wyrm - just one of many trinkets in her hoard
Serving a megalomaniac medium - with predictable outcomes
Serving a wistful wife - spouse off at war for almost a decade

Table: elemental, air
Begetting tiny dust devils with a parching harmattan
Rattling fetters of strange, transparent metal
Brooding grey, coruscating with rapid flashes of lightning
Roiling like a coming storm, flinging a kobold down
Bull-rushing an ogre with the fury of a hurricane
Shaping smoke into intoxicatingly complex shapes
Catapulting an asphyxiated acolyte into a wall
Sibilantly scurrying to-and-fro as if patrolling
Curling and unfurling loose vellum scrolls, rustling
Slowly heaving against a wax-sealed portal
Decrepitating giggles, filled with sparkling grains of sand
Smugly snuffing out a pewter candelabra
Distracting a group of goblins with murmuring whispers
Sucking up chirping sparrows/bats in a cacophonous vortex
Dramatically billowing every loose cloak and curtain
Suffocating soldiers in a sand-laden simoom
Filling your ears with corybantic gulping
Surging through a rusty grate without slowing
Gently blowing, a pleasant khamsin concealing its wrath
Sweeping detritus in a fussy, frenetic spiral
Gusting intensely, enough to topple a stack of coins
Swelling sand into a blinding sirocco
Hazy and humid, gasping as if grasping for your breath
Swirling in place, watchfully scanning all directions
Languidly making detritus dance across the floor
Violently churning, full of dead leaves and twigs
Popping eardrums with a powerful shift in pressure
Wheezing like belabored breathing
Puffing cheeks and pursing cloud-like lips
Whirling savagely, uprooting trees/flinging furniture

Table: elemental, earth
Angrily smashing through doors in pursuit of a cocky medium
Quaking with spleen as its compelled to mix mud for bricks
Attacking a water weird with splashes and earth-shuddering strikes
Reverberating like an avalanche after going on a rampage
Carefully crushing an orc's windpipe with clumsy granite fingers
Roaring with grating guffaws at a gargoyle's joke
Covered in valuable lichens from distant planes
Rumbling ruefully and shaking a fist at a babbling brook
Crumbling like a clod of soil, only to reform as solid stone
Running mitten-like fingers across a wall, generating cracks
Dragging massive block-like feet, and scraping gouges in the ground
Shattering clay jugware with something approximating glee
Greasy bones creak and crack as it uppercuts an ogre ghoul
Slamming a lizard man into the dirt by his tail
Grinding a dull heel into the ground as a fault erupts
Slumped over, inert as spiders weave webs on its face
Knocking down a formation of hobgoblins like bowling pins
Sprouting tiny tufts of scraggly grass and green moss
Lurching ardently, on patrol for intruders
Staggering to a stand-still as a druidess waves a wand
Milking sludge-like sluice from a grateful gorgon
Stomping through a settlement as a man steps on an anthill
Moping about with a dead daisy in its beefy basalt fist
Swelling stone, attempting to collapse a carved column
Plodding under the weight of a massive carried dolmen
Treading slowly, sparkling with mineral inclusions
Pounding rhythmically on the bare earth, calling out for kin
Triggering tremors as stones hear its grumbling howl
Pulverizing glass to free the trapped motes of its brethren
With earth-shaking steps, marching, indomitable & oblivious

Table: elemental, fire
Adopting the form of an amazon with a smoldering gaze
Melting gooey gold as it reclines atop a treasure hoard
Air shimmering and fuliginous, stewing in a sigil-covered circle
Nibbling incense like grapes and smoking contentedly
Blackening the bodies of dead berserkers
Obeying orders from a snide vampire, begrudgingly
Burning through thick cobwebs as they glide by
Pacing with sooty steps as a cultist prepares a sacrifice
Cauterizing the neck stump of a twitching troll
Raining florid embers as it swats at a rattle of skeletons
Consuming expensive teak furniture, swear you hear lips' smack
Scalding the feathers of a whimpering owlbear
Dripping napalm-like beads of flame that sizzle and smoke
Scrupulously scorching hempen ropes that bind its binder
Evaporating the colorful contents of stoppered vials
Seething as it stands of the shores of a brackish river
Flickering with fury as water drips on its shoulder
Selfishly charring a discarded spell book
Gently licking the face of a terrified frost salamander
Setting alight a colony of yellow mould at a sorceress' request
Glowing intensely, like slag in a forge
Singing the cloak of a fleeing halfling
Humiliated as it heats a cast-iron kettle to boiling
Sweltering heatwaves cook a carcass crawler instantly
Igniting the beard of a dwarf, a horrible smell
Tracing strange, searing symbols onto a stone wall
Immolating a merchant caravan as the traders run
Vexing an alchemist by warming her potions into poisons
Livid and sparking at the sight of a pail of water
Weeping white-hot tears of joy after burning down a village

Table: elemental, water
Accidentally drenching an acolytes holy books
Immersing itself in a pool, completely invisible
Arguing with a boiling cauldron
Jetting steady spurts of water at an intractable golem
Being used to brew exotic, magical teas by a brash wizard
Lightly rippling as their reflective surface petrifies a basilisk
Brimming with sharp shards of ice
Managing to completely soak a stack of supplies
Bubbling inquisitively as a medium draws on a narghile
Neutralizing the flaming breath of a chimera with a splash
Cascading across the area, inadvertently cleaning
Overheated by a fireball and starting to steam
Churning violently as it wrestles with a were-rat
Playfully showering a dryad with shimmering droplets
Confused that submerging a zombie seems to have no effect
Rubbing a portly belly that contains a confused goldfish
Dousing impudent torches and flames
Simmering slightly, whole body blessed by a priest
Drowning an elf by engulfing his finely chiseled face
Spouting like a geyser, up from the ground beneath gnolls
Erasing chalk marks, left by hopelessly lost adventures
Surging forward, swinging a liquid trident
Flushing a gelatinous cube down a corridor
Swelling in size due to the state of the moon
Frothing with white-capped anticipation
Temperamentally sputtering, bored guarding a shore
Gladly flooding a settlement at its masters request
Threatening a troglodyte in a gurgling, deep voice
Hackles up and foaming at the sight of a camel
Undulating in a thin sheet, covering the floor

Table: elephant
Alarming a jumpy giant grasshopper
Jubilantly squirting water on their back to cool off
Approaching a crocodile infested river cautiously
Kicking down a tree trunk to feast on the fallen fruit
Avoiding a vigilant crash of tetchy rhinocerotes
Leaning lazily against a root-choked temple ruin
Awkwardly swaying, a bit drunk on fermented fire limes
Lifting a halfling to a sentry post, high in a tree with their trunk
Barreling into a brigand bivouac
Lumbering down ancestral paths, eroded by centuries of heavy steps
Bathing in a lake, wide and deep
Marauding and bloodthirsty after a kobold calf-napping
Bellowing loudly at a male challenger
Marking a tree by debarking it with their tusks
Blazing a trail through thorn-bearing bushes
Modifying a branch to use it as a flyswatter
Blowing dust on their wet skin to form a protective crust
Negotiating a narrow but sturdy bridge with their mahout's urging
Breaking the back of a yowling leopard
Nonchalantly pulling up tasty grey tubers by their stalks
Chaperoned by overprotective and very warlike sprites
Nudging an overly cautious calf into the water for the first time
Charging, trunk failing, towards a chimera
Overwhelming a goblin warband, there will be no survivors
Chasing after a group of gnolls, giggling with terror
Panicking local villagers by overturning a cart in the middle of town
Chewing and crunching loudly on tall sugarcane
Parading, bedecked in sumptuous damask and vibrant paints
Coating themselves in thick black mud to soothe sunburn
Playfully splashing in a deep pond
Collapsing a crudely built barn
Plodding down a steep slope, skidding periodically
Crashing through the undergrowth, away from poachers
Plucking ripe bunches of banana from branches
Crossing a fish-filled stream, stopping to drink midway
Quizzically regarding their reflection in the still surface of a pool
Delighting in the bristled brush of their human minder
Raging due to musth, secreting ichor from cheek glands
Destroying a dwarf's meticulously constructed sluicing trough
Rearing onto hind legs, startled by a small rodent
Devouring sticky, sweet melons from a frantic farmer's garden
Recruited for calvary by hobgoblins craving victory
Disobeying their ankus-waving minotaur mahout
Remembering a cleric's kindness, coming to their aid against ghouls
Dragging a sledge, piled high with pottery
Retreating after hearing the buzz of a beehive
Driving away a feisty rogue male
Running down a tiger that crept to close to their calf
Dwarfing the gnome merchants who trained them as mounts
Savaging the trunk of a tree, stripping off delicious bark
Earnestly scratching on a very patient, but slightly worried treant
Seizing a troglodyte with their trunk and flailing them about
Emerging from dense jungle, looking for a lost calf
Shaking the ground with massive, trudging steps
Encroaching on a fishing village, intent on an ancient salt lick
Sneezing suddenly after stirring up some pale-yellow pollen
Enjoying a lightshow as they wave a glowing wand with their trunk
Snorkeling with their trunks, completely submerged
Escaped from captivity, still dragging massive iron chains
Splintering a sturdy wooden fence
Excavating a cliffside with their tusks for mineral rich deposits
Squashing a driver ant that ambled too close for comfort
Feeding deftly on still tender shoots of grass
Stampeding, spooked by a roc that snatched their matriarch
Felling a dead tree, angering a swarm of hand-sized ants
Stomping to deliver a firm warning to a warp beast
Flanking a pair of calves to shield them from a pack of wolves
Swatting away stinging insects with their rope-like tails
Flapping their floppy ears to swat away flies
Swinging a large branch to intimidate white apes
Flattening a vegetable patch with broad, determined steps
Tenderly touching the sun-bleached skull of a deceased loved one
Following sullenly on a leash, behind a hill giant hunter
Thundering through an extremely claustrophobic bamboo grove
Gathering at the behest of a druid, ready to raze a town
Tirelessly trekking to pay respects at an elephant graveyard
Gingerly picking prickly rambutans
Tossing an unlucky lioness aside
Goring a gorgon as fine granite dust falls from their flanks
Towering over adoring dung beetlefolk attendants
Grasping for high leaves with a snake-like trunk
Towing a plow, turning the rich soil for their cyclopean tender
Grinding tightly bundled bunches of grasses with massive molars
Tracking their herd with their exceptional sense of smell
Halting at a wide dirt road, looking both ways before proceeding
Trampling a hermit's pumpkin patch
Harnessed with a wondrously glittering, gilt panoply
Transporting the bones of a saint in an ornate howdah
Hauling massive logs intended for a goblin forts palisades
Trumpeting with excitement upon catching sight of an old friend
Heaving a huge boulder out of a furrowed farro field
Uprooting a tree to rescue a ranger asphyxiating by stranglevines
Impaling an incompetent ivory hunter
Utterly smashing a clandestine shrine to chaos
Inopportunely shuffling into a sacred site, interrupting a ritual
Vehemently snorting, stuck in an extremely strong snare
Irritable due to itchy skin, caused by a stinging sap
Violently rampaging through a lizard man settlement
Journeying to a seasonally available water source
Whitewashing the walls of a holy temple, using their trunk to paint

Table: elf
About to slice open a man-sized cocoon with a ceremonial dagger
Pouring glowing fey steel into arrowhead sand molds
Arranging foraged berries on tree-bark trays
Properly preparing for a visiting harpy dignitary
Attempting to spatchcock a small roc beneath a very large rock
Proving honed swords by bisecting grassblades tossed alight
Blazing a false game trail, indistinguishable from the real thing
Putting a few finishing flourishes on a funereal pyre
Blisteringly critiquing a spider's web for symmetry and aesthetics
Quickly copying slug trails as they shimmer in the sun
Burning the exquisite poetry of a compatriot who recently passed
Recoiling from a horseshoe, nailed to a tree trunk
Carefully applying gold leaf to the already exquisite petals of a lily
Remarkably unmuddied, gathering clays for urn-making
Carving decorative knotted swirls on a wondrous boat
Re-silvering hand mirrors
Cauterizing the twitching remains of a dying troll
Retuning the sound of a babbling brook by shifting stones
Celebrating a honey-harvest by tapping a keg of mead
Ruefully examining hobnailed bugbear tracks in the mud
Chiseling mocking self-portraits into a druid dolmen
Scouring the ground for werewolf sign
Clipping the tops off every-other cattail with deft sword swings
Scrubbing sharp satyr hooves prior to pigéage à pied
Coercing some moss to grow on the other side of tree trunks
Sculpting brooches in giant beeswax for lost wax casting
Confiding secrets to dead leaves and feeding embarrassed bonfire
Searching shallows for a single awakened minnow
Cooing gently to a storm-struck tree
Seated at a leaf-bearing table, shaped over years as it grew
Counting out equal piles of electrum pieces and deciduous teeth
Selecting straight saplings for spear wood
Dancing to show bees a nearby bloom in need of pollination
Sewing ornate silver buttons onto boots
Deftly harvesting honey-suckle nectar for fermentation
Showing birds how to weave horsehair into their nests
Dismantling an ancient, lichen-laced cairn
Sifting ashes for eggshells from a recent phoenix re-birth
Donning antlered deer skulls to frighten local villagers
Smashing kilns to retrieve their ceramics inside
Dribbling magical elixirs onto a fire and recording the flame color
Smoking a manticore out of his den to retrieve stolen scrolls
Dripping molten copper into perfect circles on the sod
Solving a dispute between a nixie and a colony of beavers
Dueling over who's eyes most closely match nearby lavender bloom
Somberly feeding figs to a drunken donkey
Engineering the fall of a tree to land directly on a roadside shrine
Sorting feathers by sound and smell for fletching purposes
Escorting a grumpy treant to make for a more pleasing landscape
Squabbling with vultures over last bits of unicorn carrion
Examining a wooly-bear caterpillar to divine end of the age of man
Stalking a hobgoblin patrol by smell
Fastening a message to the leg of an obedient giant owl
Standing stock still, staring at a turtle flailing on its back
Feeding a freshwater pearl necklace to a temperamental wild sow
Starting a campfire with light through a faceted glass gem
Filling an already overflowing basket with morel mushrooms
Strategically sowing century acorns; won't grow for decades
Floating a wreath of blossoms as a gift to a pair of swans
Stringing lemniscate flower garlands
Furiously whittling a perfect flute, pile of serviceable ones nearby
Studying a foreign arrow in the ground for angle of entry
Gingerly collecting dew from certain blossoms in a vial
Sullenly chewing a special leaf that staves off thirst
Gleefully smashing hourglasses, with glass and sand a-flying
Summoning a light drizzle to mourn the death of a nymph
Greedily filling flasks from an idyllic mineral spring
Suspending stones from an oak to form a trail-marker tree
Hanging threaded thrashing fish around a yew tree
Systematically re-homing stones from around a campfire
Helping a centaur with a shard in her hoof
Tasting rainwater in hopes of locating a mithril seam
Idly following the gossipy chatter of squirrels and songbirds
Tattooing wings on the back of a pig for it to fly
Installing strategically placed aeolian harps
Teaching a few key words in elftongue to otters
Instructing coven of hags on the proper technique for sucking eggs
Tempering the tips of sharp stakes by charring flame
Interceding on behalf of a warlock being broken on the wheel
Testing the disguise of a changeling for suitability
Inveigling grapevines to take to a trellis
Threatening a dwarf prospector with pogonotomy
Laughing as they prick their perfect faces with thorns/ quills
Transplanting the sapling of a rebellious teenage dryad
Laying out ginger-bread party members on a rock to firm and cool
Transporting an ornate urn of cremains
Lecturing a racoon on the importance of handwashing
Treating an infected gadfly bite on the flank of a pegasus
Listening intently to leaf-rustling to predict the weather
Uncharacteristically drunk on potent-pixie gin
Measuring exactly one hundred drops of drake-blood into a bowl
Using fine gossamer nets to ensnare sweet southerly breeze
Mocking a ghoul, caged in a gibbet formed of living branches
Waltzing, colorful toadstools sprouting behind each step
Officiating a messy dryad divorce
Waxing nostalgic as they wax their bowstrings
Organizing stream pebbles by size, shape, and flavor
Weaving a pile of straw into silken threads
Patiently taking turns as each suckles from a she-wolf
Wrinkling their noses at a rose bush

Table: ferret, giant
Accumulating shiny objects in small piles
Muzzled with well-made leather masks, for now
Ambushing an unsuspecting gnome
Nipping at the calloused heels of their halfling handler
Appearing suddenly out of surprisingly small holes
Nonchalantly pushing open a door with their forepaws
Arching their backs as they play-fight
Obeying a diligent gnome in exchange for tasty treats
Barging in on a magical ritual
Obliterating the carcass of a deer
Bending and contorting to squeeze into an alcove
Outfoxing a giant hawk by going to ground
Bickering over the remains of a rabbit
Overpowering a crunchy rust monster
Biting each other playfully on the tail
Overtaking a troglodyte, fleeing for his life
Bounding rapidly across the ground, grinning
Playing with their food - juggling bits of bone and meat
Burrowing underneath a toppled statue of a minotaur
Pouncing on a giant rat with incredible celerity
Caching tasty morsels in nooks and crannies
Prancing across uneven flagstones
Cambering under tension, about to spring on a rat
Prowling through a dried creek bed/sluice
Capering and cavorting, a mass of fur and teeth
Quarrelling in a friendly fashion as ferrets are wont to do
Catching up with their trainers after being distracted
Rolling into surprisingly round, fury balls
Challenging an interloper with writhing displays
Running to the top of an incline and sliding down
Charging headlong towards a pile of firewood
Scent-marking absolutely everything as eyes water
Chattering loudly as they crack open large snails
Scouting on behalf of their hobgoblin masters
Chewing through leather leashes with sharp incisors
Scurrying away from a marauding golem
Clucking contentedly, being stroked by their dwarf
Shredding an entire bookshelf full of papers and tomes
Cornering a carcass crawler cautiously
Slinking up a ladder to their mulchy nests
Crushing the carapace of a tiger beetle in their jaws
Slithering into a narrow gap after a giant rat
Curving around corners on nearly silent paws
Snaking their way through a window
Devouring bread loaves, left as offerings at the foot of a shrine
Springing up from beneath a massive pile of leaves
Digging furiously after a fleeing giant centipede
Squabbling over the tastiest bits of a giant scorpion - claws
Diligently policing their territory of interlopers
Squeaking as they cower from a cruel goblin's whip
Dodging a sticky drizzle of green slime
Stealing a shiny helmet from a sleeping veteran
Dooking happily as they sniff under piles of detritus
Stretching to a surprising length to cross a crevasse
Eating a giant spider, starting with the legs
Swiftly striking a giant pit viper and grabbing its neck
Encircling a rattlesnake, more inquisitive than hungry
Tamed as mounts by kobold calvary
Eying their kobold handler for signs of weakness
Tangling themselves in a knotted net trap
Feinting deftly to induce a giant cobra to strike and miss
Taunting a medium after stealing their staff
Fleeing after accidentally waking a sleeping grizzly
Toying with a chirping cave locust
Frizzing their tails as they hear a distant yelp
Tracking down prospective mates by scent markings
Gamboling across a scree of rocks and boulders
Trampling right into a pitched battle between orcs and ghouls
Gnawing on roughly hewn lumber to keep teeth healthy
Turning on the gnoll that starved them into submission
Grooming their fury faces with frantically stroking feet
Tussling joyfully with their ranger companion
Hiding out in a cozy bleached titanothere skull
Unravelling arm-thick ropes holding up a suspended boulder
Hissing loudly at some goblins with outstretched nets
Upsetting a treant by clambering around their boughs
Hollowing out a new home in the roots of a massive tree
Urged on by bugbears whispers from the shadows
Hopping madly as they toy with a nest of scorpions
Utterly destroying a sack containing some rations
Hunting giant shrew, battle-scarred and ornery
Vaulting over a large log after a frightened jackalope
Interrupting the rest of an adventuring party
Veering suddenly after triggering a trap
Isolating a driver ant from their nest mates
Waggling their way over to a cleric for a handout
Jingling thanks to the belled collars from their minders
Wandering blindly, whimpering after a dire skunk encounter
Jumping in place, trying to snatch a very worried giant bat
Warning everything of their arrival with self-confident squeaks
Killing a giant toad, rather gruesomely
Weaving their way between the legs of an ogre overseer
Knocking down a cauldron, suspended over a doused fire
Whining pathetically as they struggle against chains
Leaping onto a still twitching fish
Wildly war-dancing, after turning over a large rock
Lurking in a lair, expecting kits any minute
Wounding a mule in a bloodthirsty frenzy
Messily excavating a new den, flinging dirt everywhere
Zig-zagging their way up the steps of a stubby ziggurat

Table: fish, giant (bass)
Avoiding a spear fishing hill giant
Just under a rickety wooden pier, lurking
Bolting down a giant toad
Narrowly escaping the jaws of a hungry crocodile
Capsizing a coracle, helmed by a dwarf that can't swim
Overturning an ore-boat hauling gold-flecked quartz
Dragging a fisherman and his line across the water
Protecting fry, still longer than an elf arm-span
Feasting on a colony of water termites
Rushing to the aid of a ripple of nixies
Gulping a twitching giant crab/crayfish in a single bite
Seemingly speech-capable (actually invisible sprites)
Hiding in a shady spot beneath the pond weed/algae
Spitting out a foul tasting thoul
Hooked by a team of hungry hobgoblins, taking to reel in
Swallowed a stolen chest of coins recently
Inhaling an entire school of smaller fish
Thrashing about in a strongly woven net
Leaping out of the water with a tremendous splash
Used as a bogeyman to keep children from the shore

Table: fish, giant (catfish)
Adeptly crunching large, freshwater mussels
Jagged magical harpoon juts from its back
Bludgeoning a bugbear with its massive barbels
Lazily skulking in shadier spots, all other fish flee
Clouding clear water by kicking up silt while bottom-feeding
Patrolling a sunken barge exceptional statue cargo
Digging through sand with its shovel shaped head
Ramming a raft with broad body, gnomes overboard
Encased in protective slime and able to create shocking jolts
Regarded with reverence by uncanny catfish cultists
Famous local mascot, subject of many a fish story
Scouring delicious algae off of submerged stones
Feeling its way through murky waters with twitching whiskers
Slicing hands of over-eager ogre noodler with spurs
Guarding a nest of eggs until their brood hatches
Surging ashore to grab a thirsty goat unawares
Half-buried in the silty bed, hiding from a giant eagle overhead
Swimming close to the surface, humped back exposed
Ingested elemental by accident, can create earthquakes
Wallowing in muddy shallows after a recent drought

Table: fish, giant (piranha)
Attracted to the splashing of a suspected witch being swum
Local lizard men use impossibly sharp teeth as arrowheads
Baited with a wriggling kobold, sadistic trolls fish for them
Nibbling at the fetlocks of a warhorse fording with his knight
Churning the waters surface into a foaming, roiling vortex
One has magic ring in stomach after biting off a mediums hand
Circling small island where marooned minotaur pleads for help
Rapidly devouring deer, driven into water by a stalking panther
Congregating in a round inlet, awaiting their weekly sacrifice
River teeming, the brave/foolish could walk across their backs
Drawn to scent of giant leech, feeding on a bedraggled veteran
Shoaling together for protection from a river serpent
Ferociously flensing the feet of a frantic friar
Skeletonizing an unfortunate owlbear that tried to swim across
Forcefully biting the bargepole of a boater clean in two
Starving due to lack of prey, starting to cannibalize each other
Gorging on a gorgon, riverbed dotted with perfect piranha statues
Swarming around large crocodile, stealing bites from her kill
Helpful warning signs, in several languages are face down nearby
Tearing brutal bites from the body of a bloated bull

Table: fish, giant (rockfish)
Almost invisible, even in these crystal-clear waters
Nearby coastal halflings enjoy their mouth numbing flesh
Ambushing a grumpy grouper
Partially buried in on a pebbly lagoon bed
Blending in with anemones near a finely forged anchor
Ranched by local merfolk, who envenom their harpoons
Concealed among blood-drinking corals
Scooping frantically to rebury itself after a meal
Crunching a very large crab in its mouth, spitting out shells
Settled near the shipwreck of a long-lost pirate vessel
Disturbed by an inquisitive eel who now floats motionless
Sticking out like a sore thumb as it swims across a sandy seabed
Furry algae that occasionally grows on them grants water breathing
Suddenly engulfing lobster as long as your arm
Glittering coin-shaped scales make it attractive for grasping
Unbothered - swimming away, after slaying an unlucky pearl diver
Has found its way under a worm-eaten chest to rest
Well-camouflaged among the reef-flats
Hollow spines are prized by both scroll-scribes and assassins alike
Wrestling with a large octopus

Table: fish, giant (sturgeon)
Attacking an aquatic caecila for supper
Missing a few plates after a run-in with a sea serpent
Colliding with a caravel, sharp ridges puncturing the hull
Overfished by sages for parchment protecting isinglass
Faintly glowing pale barbels flickering in the murk
Plates protect it from the tridents/harpoons of a dozen mermen
Fighting paralytic juices, famous paladin inside frantically stabs
Rapidly syphoning in water, wiping out a huge school of fish
Giant sturgeon scales resist dragon turtle steam
Recently swallowed the spouse of a weeping willow dryad
Has learned that sinking ships leads to succulent sailors
Scouring the benthos for crustaceans and aquatic worms
Hurling itself into the air, breeching with a tremendous splash
Slurping up the writhing tentacles of a giant octopus
Impossibly ancient, a source of underwater druidic magic
Sucking in prodigious amount of water to swallow a fleeing pike
Larger boney scales could outfit a squadron with shields or bucklers
Swollen with roe, in high demand as cloud giant caviar
Migrating upriver to spawn after destroying a wooden dam
Widening a clogged estuary with its massive bulk

Table: gargoyle
Acquiescing after being paid a heft toll, mostly in gemstones
Hurling loose bits of masonry at passers-by
Allied with the church grim that haunts nearby ruins
Imperiously smirking as an adventuring party prepares to camp
Amusing themselves with a game of draughts
Impersonating the unfortunately prevalent statuary in this area
Arrogantly grinning as they spy a group of hobgoblin soldiers
Installing a precariously balanced boulder over an obvious route
Balancing precariously on the tips of obelisk grave markers
Jeering at one of their number, grounded due to a smashed wing
Bending swords into bulky bracelets
Landing gracefully atop a steeple piercing the sky
Bounding on all fours after a delicious giant rat
Lanky and emaciated due to lack of food
Bowing to blushing caryatid columns
Lashing their barbed tails to-and-fro like a cat
Breathtakingly beautiful - crystalline specimens in the form of angels
Laughing at a medium loosing a sleep spell
Capturing a kobold with a weighted net
Leaping upon a lizard man and tearing him limb from limb
Chasing a fleeing philosopher, tripping on her robes
Lurking behind a screen of dying ivy
Cheaply made from hollow, fired clay painted to look like stone
Managing to subdue a mangy, maze-less manticore
Chiseling a blended likeness in stone, as a mated pair models
Mimicking the cherubs' poses on a non-functional fountain
Circling like stone vultures above a veteran, bleeding out
Mutated by a nearby magic portal - vulnerable flesh patches in places
Clawing their way up a crumbling wall
Nesting near a humongous bronze bell
Comically tonsured interpretations of long dead monks/friars
Off-color caricatures of legendary heroes, perfectly still
Confidently charging at a group of under-equipped orcs
Panicking from a recent sighting of a hungry basilisk
Cooing like doves, convincingly
Parodying/poking fun at a manticore, geased to guard this place
Covertly stalking a cleric, hoping they can remove a curse
Perching precariously on the shoulders of a stone giant
Crouching in alcoves with unblinking gazes
Plunging into a deep pool, surfacing with handfuls of gold
Decorating their aerie with bits of bone and skulls
Positioning themselves over doors to blend in with decorations
Defending an altar from the blessings of an acolyte
Positively covered in thick, velvety moss
Depicting the deadly sins in their form and personalities
Pouncing on an elf, distracted from sensing a secret
Destroying artfully engraved slabs of stone that crackle on cracking
Practicing making faces in a still puddle
Distracted by a brave swarm of bats that decided to dangle here
Pretending to surrender to a score of dervishes
Divebombing a warp beast, missing most of the time
Protecting their mascot - an orphaned urchin child
Drifting lazily from perch to perch on patrol
Ready to spring on an unsuspecting halfling
Engraved extensively with spidery intaglio, grants them each a spell
Regretting a truce they made with a conniving medusa
Excellent archers/snipers, rain volleys from above
Remarkably indistinguishable from all other large cornice carvings
Flaunting their powers of flight as an ogre shakes a frustrated fist
Resembling devilish dwarfs with long lichen beards
Flinging gooey globs of grey ooze at foes
Roosting atop an abandoned wizard's tower
Fluttering silently on feather carved wings
Scaring off a cautious and somewhat superstitious orc warband
Glaring at a rock living statue, unsure what to make of it
Scowling as their sorceress issues new, grueling orders
Glistening with dew that serves as holy water if harvested
Sharing spooky stories of a crazed berserker with a magical mattock
Glowering at a paladin with a glowing sword
Sneering scornfully alongside their severed shadow allies
Goading a trader into leaving tribute
Soaring clumsily due to heavy gusts of wind
Gouging rude graffiti into plaster covered walls
Spouting rainwater, identical to their inanimate cousins
Granting sanctuary to those speaking their grating/guttural tongue
Squatting like toads in a circle facing outward
Grasping for a bejeweled amulet, dropped in a narrow crack
Surprisingly friendly toward a local bishop
Grimacing contest with no clear winners
Swooping in silence, but landing with very loud scraping sounds
Grotesquely endowed with exaggerated facial features
Taking turns gargling the waters of a mysterious faintly glowing pool
Guarding a glass alembic containing a fetal homunculus
Taunting a troll marooned on an island in the middle of an acidic lake
Gurgling as they spew jets of brackish water
Terrorizing a nearby village that lacks magical armaments to fight
Harassing a harpy on a mission of diplomacy
Throwing canopic jars that explode in stinking, toxic clouds
Having their spiny stone backs scrubbed by a terrified gnome
Toiling to repair a cave in and re-unite with loved ones
Headless - featuring exaggerated faces embedded in their torsos
Trying in vain to wake a statue they suspect is sleeping
Hovering over a pit of zombies, tossing in the occasional rock
Uncannily accurate at spitting wads of green slime
Huddling around a bas-relief of a fireplace
Vexing a plan-drawing architect by moving when she isn't looking
Hunched from centuries spent occupying alcoves
Weathered and wind-worn, faces eerily effaced
Hunkering down after a recent lightning strike scarred their leader
When eaten, furry lichen on their wings allows brief, erratic flight

Table: gelatinous cube
Absorbing a swarm of rats, with sickening slurping sounds
Messily agglomerating stubborn bits of bone and broken coffin
Accruing a complete dining set - four chairs and part of a table
Mopping up detritus from very smooth flagstones
Accumulating contents of an alchemy lab - alembics/vials/etc.
Occluding a rotating wall, it somehow managed to jam open
Being goaded into a maze by a very tidy minotaur
Oozing menacingly toward a medium
Billowing to fill a cylindrical corridor
Osmosing an ogre - frozen in place
Blending in well with a damp, slick wall
Overflowing from a small cellar door it inadvertently entered
Bloating slightly as it flows over a large stone
Overwhelming an orc, completely benumbed
Blocking a hallway with its shimmering mass
Painstakingly gliding up a steep incline
Breaking down an unlucky nuisance of kobolds
Patiently dismantling a dead driver ant
Bulging obscenely as it surrounds a statue
Plugging a drain in the center of the floor amid ankle deep water
Catching a goblin bodyguard completely unaware
Politely sweeping up a colony of yellow mould
Choking an inviting hallway completely
Pouring itself out of a narrow gap in the wall
Clanging loudly as it drags a discarded shield along the floor
Pressing against a barricade of furniture, placed against a door
Clinging precariously to a narrow walkway
Prowling silently, in search of prey
Clouded with metal shavings after wandering into an old forge
Pulsating as glands from a digesting fire beetle glow
Coating the walls in stinking ectoplasm
Quaking with satisfaction after a lizard man meal
Collecting several unusually large shells and carapaces
Quivering after a curious cave locust takes a bite from it
Comically stuffing itself into a stone trough
Rambling over caltrop strewn floor, conveniently clearing a path
Conforming to the circular sides of a shallow pit
Recoiling after brushing past a sconce containing a lit torch
Congesting an already high traffic area
Sagging slightly to avoid the green slime on the ceiling
Cramming itself into a concave niche
Scouring walls clean of moss and moisture
Creeping around a blind corner
Seamlessly camouflaged in an arched doorway
Damming a drainage pipe and skimming scum from the liquid
Seeping its way down from a dais
Decomposing a dwarf, appears to levitate in the middle of a hall
Shivering slightly as a dozen darts launch into its bulk
Destroying a stout wooden door, a splinter at a time
Shoving its way past a gang of gargoyles
Deterring a pack of hungry ghouls
Sinking into a pool of water, dining on algae
Disintegrating several barrels slowly
Skeletons inside are animate, just along for the ride
Drawn toward a dying dervish
Skulking at the bottom of a descending ladder
Drifting across an open area, a trail of slime in its wake
Sliding into a crypt niche to feast on tasty bones
Engulfing the corpse of an elf
Slinking away from an angry carcass crawler
Extruding itself through a portcullis, creating tiny cubes
Slowly crumbling a shrieker, suspended inside of itself
Faltering as a giant cave snail rasps it with its radula
Sluicing down a chute with a sickening sound
Filling a fountain as frightened fishes flee
Sneaking up on a giant spider, busy wrapping a robber fly
Flowing quickly down a ramp and picking up speed
Sputtering over a paralyzed paladin
Foundering across an iron grate in the floor
Squeezing itself through an arrow slit
Gathering a morbid collection of humanoid skulls
Stymieing a group of gnomes, keeping it at bay with torches
Gradually dissolving a struggling zombie
Surging rapidly down a hallway after ingesting a potion of haste
Gurgling as a suit of tarnished plate mail is ejected
Surprising a troop of troglodytes
Having subsumed a grey ooze, very acidic and immune to fire
Surrounding a benumbed berserker
Hindering a hobgoblin patrol
Swelling upwards to reach roosting bats
Hugging the side as it traverses a narrow ledge
Teetering on a narrow walkway traversing a chasm
Impeded by the flames of an irritated hellhound
Throbbing as it surrounds a helpless halfling
Inadvertently caching several hundred rusty nails
Thwarting a thoul, who can't tear chunks from it fast enough
Intercepting a swarm of beetles feeding on a dead mule
Transuding through an ornately filigreed gate
Leisurely enveloping a couple of crates
Trembling slightly as pots and pans its picked up shift around
Lurching itself out of a shallow divot
Turning the tables on some stealthy bugbears
Lurking in an alcove, completely surrounding a statue of a saint
Undergoing mitosis - splitting into smaller, identical cubes
Meandering away from a bright beam of light
Utterly clogging a stairwell with its massive bulk
Melding with another cube to exchange memory maps
Waiting patiently at the bottom of a pit trap
Melting through a beautifully woven silk curtain
Wobbling after a mighty blow from a troll's club

Table: ghoul
Abstaining from flesh as part of some strange penance
Misunderstood - these are holy morticians for a local village
Alerting others after spotting some tracks
Numbing a nomad as his fellows flee
Babbling incoherently, brains addled by kuru
Opening a bear skull with a sharpened rock
Backstabbing their de facto pack leader
Organizing stolen funerary offerings into untidy piles
Banging pots and pans together to attract prey
Overtaking an orc outrider
Baring blackened, chipped teeth in simpering grins
Playing with their food - a now repentant cultist
Benumbing a bandit in search of plunder
Pouring over a series of gibberish filled recipe books
Bickering over the body of a basket-maker
Prying open a finely appointed casket
Butchering the common tongue by inserting dark invectives
Raving starkly from starvation
Cackling with stygian glee
Reeking of the charnel house and rotting roses
Carefully slicing portions off what appears to be a leg
Rending their way out of woolen wrappings
Celebrating a companions day of rising
Rummaging through crypt niches for a quick snack
Challenging all comers to a disgusting eating competition
Salivating as they test a very still dwarf for tenderness
Chewing on gristly chunks of cartilage
Sautéing what appears to be liver and eyeballs in a cast iron pan
Clamoring after inadvertently unearthing a holy symbol
Scabbing over after being caught out in the sun
Clawing at the lids of their coffins
Scrambling out of the way of an angry ogre
Cracking open green bones with sickening snaps
Screaming out the names of their still living relatives
Crowbarring open a heavy marble sarcophagus
Scurrying swiftly into the shadows
Dancing frantically around a frozen fighter
Seizing a scurrying spider to and eating it immediately
Decomposing slightly due to a lack of food
Serenading each other with joyless jeremiads
Delivering a bucket of gore to a wounded pack member
Shackling a packmate to a wall as some form of punishment
Devouring dead doppelgänger, faces fluctuate with every bite
Shredding through the hide of a dead horse
Digging up a hastily buried adventurer for a quick snack
Shunning a corner of the room where shadows lurk
Disemboweling a paralyzed gnoll warrior
Sifting through rich, fragrant soil in search of worms
Dodging a vial of holy water, flung by a prepared party
Slashing at an obstinate elf
Dragging a stock-still squire
Slurping the entrails of an ex-expedition porter
Dumping out funerary urns
Smacking their cracked, blood caked lips
Eating an incapacitated and ill-starred explorer
Smashing religious icons in a constant state of agitation
Enshrouding a corpse in linen sheets
Snatching an albino fish from a pool
Escaping from a crazed necromancer's experiments
Spiriting away a blind beggar by claiming to be clerics
Eulogizing a pile of ashes - a packmate turned to dust by faith
Splintering a femur to munch on rich yellow marrow
Eviscerating a giant rat, only its whiskers slightly twitching
Stinking of the grave, bloated with putrefaction
Ferociously biting at ropes that bind their wrists together
Swinging down from a rope suspended chandelier
Festering with grubs and maggots adapted to undead flesh
Tackling a trespassing thoul
Flinching from the light emitted from a paladin's shield
Taunting an affrighted medium
Gnashing and foaming, fettered by sturdy chains - for now
Tearing out their stringy, dirty hair - just risen
Gnawing on a carnage covered ribcage
Threatening a group of lost gnomes
Greedily swallowing huge hunks of offal from a cauldron
Toasting with ghastly chalices, brimming with congealed blood
Gulping down greasy goblin guts
Transporting a frozen halfling herbalist to their "kitchen"
Hacking through a wooden door with dull hatchets
Tugging on strange silver collars that prevent them from killing
Hesitating at the edge of a salt and silver circle
Uncontrollably drooling pea-soup colored, curdling spittle
Hissing at a wavering acolyte, brandishing her holy symbol
Underestimating the sway a just arrived vampire has on them
Incapacitating a luckless rat catcher
Unsealing a barrow by burrowing furiously
Injecting their foul fluids into the roots of a treant
Uttering unsettling blasphemies in hoarse whispers
Interrupting a transaction between traders
Voting on who deserves the best bits of a berserker
Jabbering nonsense rhymes about grave-digging
Welcoming a new pack member with open arms
Keening eerily in unison as they snuff out candles
Wholly paralyzing a flock of pilgrims
Laughing macabrely at a drowning bat
Wounding a witch-hunter, rooted in place
Leaping upon a sleeping veteran
Wrapping one of their pack in woolen strips as a morbid joke
Lifting a heavy stone slab
Yielding to the alpha - a hill giant turned ghoul some time ago

Table: giant, cloud
Admonishing their aarakocra acuepses
Hoisting a brace of large roc over a shoulder
Blockading an essential and speedy mountain pass
Leading a hunt, aided by their immense wolves
Brailing the wing of their prized white giant hawk
Levying tremendous tolls on those who wish to use a road
Causing an avalanche to rain down rubble on ogres
Lugging a positively massive cart up a steep incline
Charging down the slope toward a merchant caravan
Mewing their molting giant hawks
Demanding tribute from a dwarf mining expedition
Obstructing the only path to an isolated monastery
Demolishing an ancient stone bridge across a crevasse
Partaking of a gigantic wheel of mountain goat cheese
Deterring a group of pilgrims from visiting a sacred shrine
Plowing mile-long furrows in a verdant valley
Dragging cyclopean masonry to repair their fortress
Returning to their cloud wreathed castle
Extracting gold with perforated pans from a raging river
Squinting into a distant canyon, on the lookout for invaders
Feeding their howling, hungry dire wolves with table scraps
Stockpiling diminutive weaponry, to accouter an army
Fortifying their brobdingnagian beanstalk stairway
Swinging an owlbear feathered lure
Grazing an immense flock of alabaster fleeced sheep
Throwing colossal boulders at a cliff-side pathway
Hauling an immense gilded harp
Treading carefully near an unstable glacier
Hawking with their giant raptors snatching hardy elk
Washing voluminous robes in a crisp mountain stream

Table: giant, fire
Abandoning an extinct volcano redoubt
Melting down salvaged bronze to make a breastplate
Barbequing a mammoth on a massive bonfire
Overwhelming an army of orcs
Constructing an incredibly tall blast furnace
Plundering a peaceful mountain village
Corralling some unruly fire elemental thralls
Provoking the wrath of a nearby dwarf delve
Devouring heavily spiced caecilia steaks
Quaffing potent spirits, distilled in huge copper kettles
Doling out payment to flame salamander mercenaries
Rallying surprisingly canny kobolds under their singed banner
Draining a pristine crater lake to quench their ironworks
Razing a high-altitude grassland
Felling entire forests of trees to feed their furnaces
Relaxing in scalding, thermally heated pools
Forging immense blocks of pig iron to fortify a wall
Releasing a pack of hellhounds after a winged wyvern
Garrisoning a hobgoblin regiment, an uneasy truce
Scowling at a distant red dragon in flight
Hammering incessantly as they flatten gigantic blades
Striking a huge anvil, as hard as they can, to test their might
Heaving huge chunks of charcoal into a burning pit
Subjugating a tribe of now charred ogres
Intercepting a shipment of ore destined for human kingdoms
Transporting massive sledges, brimming with copper ore
Kidnapping a flame-haired berserker prince
Trapping a fire-breathing hydra in a massive iron cage
Laughing as a flung boulder barely misses a pegasus
Wrestling on the lip of a magma filled crater

Table: giant, frost
Abducting frost nixies from their frozen lake
Gathering long strips of nutritious blue lichen
Assembling a massive wall from cube-cut ice bricks
Guzzling hefty draughts from impossibly large drinking horns
Barraging bugbears with massive snowballs
Hitching several dozen excited wolves to massive sleds
Bracing a snowdrift precariously, as an avalanche trap
Pelting boulders at the den of a white dragon
Challenging each other to a boulder throwing contest
Penning a pack of polar bear guard animals
Corralling a massive herd of dire reindeer
Quibbling over who's turn it is to do the hunting
Crushing a snow goblin settlement underfoot
Sledding cut stone from far off quarries to expand their castle
Decorating a cliffside with massive glyphs and murals
Slinging barbed boulders at frost trolls
Dredging up massive snow drift dunes to form a perimeter
Spiriting away a clutch of frost salamander eggs
Exhausting the taiga by over-grazing their yak
Stomping to shower frostbitten zombies with sharp icicles
Extirpating the few trees for miles for firewood
Thwarting a berserker incursion into their territory
Fashioning huge snowshoes from purple worm gut
Unchaining an only slightly tamed war mammoth
Ferrying cargo across the frozen wastes for a fee
Uniting their forces with elementals of the permafrost
Fishing for narwhal and sturgeon atop a deeply frozen lake
Wielding bone bows of prodigious size, with ballista-like arrows
Flinging drifts of rime from humongous crampons
Wilting a bit in an unseasonably warm breeze

Table: giant, hill
Ambushing some well-armed traders, foolishly
Packing their treasures into a new, sturdier sack
Bellowing in agony after stepping on a bear trap
Raiding a helpless halfling village once-a-week
Breaking clay pots and jugs while a potter weeps
Ransacking a windmill for grain
Chucking a boulder at the broadside of a barn, and missing
Reeling in a giant pike on a sturdy line
Clobbering an entire goblin war band with one club swing
Robbing an evil tax collector, giving it back to his tiny friends
Drinking a keg of stolen cyclops wine
Rubbing a tender bump atop a hairy, sunburned head
Drooling as a sacred cow cooks on a campfire
Slouching against a currently sleeping treant
Extorting travelers for toll money
Stalking a donkey that keeps outsmarting them at every turn
Gobbling down a greasy pile of meat pies
Stampeding a herd of kine while creeping clumsily
Grinding bones to make their bread
Stealing stinky gnomish cheeses from frightened merchants
Grumbling to themselves, or is that their stomach?
Surrendering to a knight astride a skewbald steed
Hijacking a shepherd's flock for supper
Swinging a large chain at a roaring chimera
Lobbing part of a stone circle at fleeing druids
Trampling over a farmer's crops discourteously
Marauding from hamlet to hamlet, stomping cottages
Uprooting a sturdy trunk to fashion a new club
Nursing festering boils
Working for the local goblins, who pay with food

Table: giant, stone
Assaulting a determined group of white apes
Inadvertently squashing a gnome caravan, apologizing
Barricading the entrance to a cursed cavern
Judging the stonework of an ancient dwarf wall
Bidding farewell to an elemental emissary from the plane of earth
Keening low, rumbling songs to wake the stones
Bombarding a sabre-toothed tiger to drive it away
Laboring unremittingly with chisel and hammer to shape blocks
Breaking bread with a friendly neanderthal tribe
Marching to make war against haughty cloud giants
Burying a highly respected shaman who spoke with stone
Pulverizing grains with giant pestles
Carrying massive amphorae filled with water
Pummeling a wicked manticore with well-aimed boulders
Carving strange runes on strategically placed way-markers
Quarrying a colossal obelisk in a single, seamless piece
Diverting a mountain river that far-away farmers depend on
Reinforcing the slate roofs of their humble, but huge, huts
Erecting stoic statues of their ancestors
Sculpting a massive likeness of their medusa queen
Foraging far from home for a curative plant
Shaping decorative war cudgels from cultivated stalactites
Goading their surly cave bears into a palisaded camp
Shoring up a crumbling wall for some friendly dwarfs
Herding horse-sized mountain goats with multiple sets of horns
Smashing the place where they thought the warp beast was
Hindering a hobgoblin logging camp with rockslides
Unshackling their mountain lions for a hunt
Igniting fragrant woods and large piles of herbs for a ritual
Watching children taunt a basilisk by grabbing its tail

Table: giant, storm
Admiring the distant fulmination from a violent tempest
Lowering a bucket of food to a starving village
Aiding a pegasus, blown off course by high winds
Negotiating a peace treaty between mermen and sailors
Bulwarking their fortress with silver sigils
Overthrowing a cruel and vindictive dragon turtle, need aid
Calling forth dark clouds and high winds
Quelling a savage storm, so that pilgrims may proceed
Conquering a new cloudbank, with the aid of giant roc
Rallying their giant crab allies for inspection
Contemplating a cacophonous cloudburst
Requisitioning jagged magical javelins - lightning when thrown
Crushing a minotaur invasion force
Rewarding a pious paladin with a hippogriff mount
Dispensing justice between representatives of the giant clans
Saturating the air with ozone and static electricity
Flooding a chaotic pirate haven with a massive tsunami
Striking the same evil wizard's tower, for the second time
Gloating as they drive off a sea serpent
Surging atop waves/cloudbanks, reveling in high winds
Guzzling heavenly killer bee mead
Swamping a merchant consortium, that deals in evil relics
Harvesting magical apples from their cloud orchards
Taking their griffons out of the hawkery to hunt wyverns
Hurling massive tridents at a blue dragon
Taxing all trade near their castle, and donating to the needy
Immuring an evil wight within their forsaken barrow
Trouncing a band of brutish fire giants for equipping gnolls
Launching lightning bolts at an invading hobgoblin army
Wallowing in a violent windstorm, smiling contently

Table: gnoll
Abducting a hyena-headed sacred statue from a rival pack
Laughing contagiously as they interrogate a captive
Attacking a caravan from both sides, starting with pack animals
Licking chops as they build a fire, plump prisoner looks terrified
Avoiding the watchful gaze of a cyclops sentry
Lovingly grooming their dire hyena companion (as dire wolf)
Baring their teeth to intimidate a group of goblins
Making short work of an undercooked warhorse
Barking orders to downtrodden subordinates
Manes bristling and raised as a scout returns with dire news
Bickering over a marrow-rich femur
Mocking a simpering merchant they've captured
Biting fleas keep them in a constant state of scratching
Needling each other, vying for higher rank within the pack
Bluffing about their prowess/numbers to skeptical brigand leader
Ogling a charred, rune carved skull in the hands of their shaman
Bounding into battle with an owlbear
On the prowl for an easy meal - shadowing a hunting lion
Brandishing filthy bodkins, tipped with trichinosis
Over-indulging on spirits, stolen from the cellar of a nearby tavern
Bullying an ogre out of his dinner - a roasting horse
Pausing suddenly with perked ears at an unexpected sound
Cackling gleefully while hacking open a stolen chest
Plundering a cache of supplies, dead ranger nearby
Capturing a shipment of weapons, sent to stop them
Poaching sheep from shepherd's paddocks
Challenging the current matriarch for dominance
Quarrelling over who's turn it is to take watch
Chattering loudly as they pack up sleeping mats
Ransacking a helpless hamlet, gleefully chasing villagers
Chewing on strips of mule meat ruefully
Regrouping after a cowardly retreat
Circling a nomad encampment, hoping to steal supplies
Relentlessly pursuing an illusionist - tricked them out of their treasure
Clashing with a clan of dwarfs
Resting after defeating a dervish champion
Congregating at a desecrated roadside shrine to split up spoils
Running after an elf sniper who wounded their leader
Cornering a pack member, accused of holding out on them
Salivating as their matriarch gorges on a sumptuous feast
Cracking whips as prisoners pull a sledge of stolen goods
Scarfing down skewered rats, lightly signed
Dashing after a giant rat, starving
Scattering after accidentally waking a hill giant
Defending their territory from berserkers
Scavenging shoddy weapons from an old battlefield
Desecrating a barrow in search of treasure
Shrieking to summon distant comrades in for dinner
Devouring rustled livestock from a nearby village
Smiling broadly as they invite strangers to share potent faerie wine
Disinterring bones of a former matriarch so shaman can ask advice
Snapping long legbones in their powerful jaws to extract juicy marrow
Double-crossing some hobgoblins at an inopportune moment
Snarling as they try to free a mud stuck wheel
Driving off a dire vulture, trying to steal from a kill
Sprinting swiftly over broken terrain
Drooling as they raid a trader's brined fish
Squabbling over the sparkling contents of a sarcophagus
Eerily sneering with eyes glowing in campfire light
Stalking an adventuring party in utter silence
Extorting protection money from a cash-strapped kobold clan
Stampeding cattle toward a cliff-side to make for easy pickings
Feigning fast surrender to ambush the merciful
Stealing provisions from powerless pilgrims
Fleeing from one of their kind, risen as a ghoul
Subsisting solely on giant ants, unusual aardwolf-like subspecies
Foaming in a frenzy due to ritually inflicted rabies
Tasting carrion on the air with mottled tongues
Foraging for fruit and berries as part of a strange penance
Taunting a trussed-up paladin
Forcefully splintering an oaken door with a two-handed axe
Tearing down posters offering a bounty on their kind
Frenzied yelping fills the air as a matriarch defeats a challenger
Threatening a halfling for taking too long to cook their meal
Giggling involuntarily as one of them springs a trap
Tirelessly tracking the scent of a veteran who slew their leader
Gorging on commandeered cattle
Tussling to determine who has to carry a load
Grinning broadly after ingesting spores that increase speed
Uncontrolled snickering and tittering spreads through their ranks
Grousing as they're forced to dig a deep pit
Using scavenged crossbows that have seen better days
Howling reflexively after driving away a troglodyte war band
Vandalizing a local hedge witch's herb garden
Hunting a member of their pack who broke a cultural taboo
Venerating the ghoul queen with cadaverous offerings
Illtreating stolen mounts, hoping they'll drop from exhaustion
Warning their bandit allies about soldiers seen in the area
Imitating convincing cries for help in common
Whimpering as they remove quills - a disastrous porcupine encounter
Infested with mange-inducing mites and balding in raw pink patches
Whining as their wizard master assigns duties
Intercepting a courier bearing important documents
Whooping maniacally as they perform a delirious dance
Japing interrupted by the appearance of a large, powerful female
Wielding a profane relic that allows them to command the undead
Knocking down a door with a crudely carved battering ram
Wolfing down rations found in a dead medium's backpack
Lapping foul liquid from an iron cauldron
Yowling dismally to commemorate a dark day in their pack's history

Table: gnome
Adjusting the speed at which a waterwheel rotates
Mapping the area around dwarf ruins for a future expedition
Administering antidotes, some succumbed to carcass crawler
Methodically panning for gold with help from tireless golems
Arguing with a group of dwarfs about ownership of a seam
Mincing cucumbers, carrots and chilis for a spicy chutney
Assisting a shepherdess looking for her sheep
Mining moonlight, to melt into one of the scarcest alloys
Baking mouth-wateringly fragrant plum and lavender tarts
Negotiating with the xenophobic naked mole rat hive mind
Binge-drinking cyclops wine, traded for gopher pest control
Numbering the pieces of a dismantled windmill
Blowing intricate glassware to sell to alchemists
Nursing a wounded werefox (in animal form), caught in a snare
Brewing a potent stout, so thick you can stand a spoon in it
Offering food/drink to peaceful parties, part of a hospitality mitzvah
Carousing with a group of somewhat shady sprites
Opening a stuck door with an intricate, several-step process
Carrying an important message from their chieftain to the elfs
Outfoxing orc sentries, sabotaging their tent poles
Celebrating a strange holiday, seemingly centered around leeks
Packing up an unsuccessful mining camp and in sullen spirits
Checking on a local priest, who fed and sheltered them decades ago
Peeling a pile of potatoes, as tall as a troll
Cheering loudly after driving away a greedy ogre
Planting a pangolin spy behind enemy lines
Christening a new, ornately carved goat cart
Polishing their masterfully cobbled, silver-buckled boots
Conspiring with local moles to undermine a kobold warren
Puffing on baroquely carved pipes, smoke rings reaching buckler-size
Debating loudly about whether or not they're lost
Quarrelling with characteristically contrary prairie dogs
Deciding through voting if it is safe to set up camp
Questioning their hired dwarf cooks' culinary ability
Delivering a wedding gift to a centaur chieftain, ancient tradition
Receiving a dire report from their hyper-vigilant meerkat sentries
Distilling syrupy blightberry cordial in portable copper boilers
Refilling water skins from a cursed spring - turns drinkers wrathful
Drying their conical hats near a fire, after being storm soaked
Researching the still-nascent field of gnomed balloon flight
Electing a new expedition leader, last one was turned into a frog
Resting in the company of some neighborly nixies
Embroiled in trench warfare with a nearby kobold stronghold
Retrieving a stolen painting at the behest of their queen
Escorting the badger king on a tour of his subterranean subjects
Twisting sausage links from an ingenious steam-powered grinder
Establishing a military presence deep in traditional kobold territory
Searching for a relic said to bring the utter destruction of koboldkind
Excavating the fossilized remains of a prehistoric creature for study
Shaking out beautiful quilts that function as family trees
Experimenting with new self-contained fire-starter, slightly singed
Uneasily sharing a campfire with a group of lawful goblin pilgrims
Failing to spot a lurking crab spider in time
Shivering and soaked to the bone after their coracle capsized
Fawning over a warrior - elderly hero from the xvii kobold wars
Sowing treant seeds as a favor for an antediluvian friend
Fitting a saddle on an absolutely massive blue jay
Strategizing about what to do with a captured cockatrice
Foraging for awfully specific spores - ultrasonic shriekers
Surveying a site for potential gnome settlement
Fussing over their meticulously maintained mustaches
Tabulating an unexpected bill for adventurers that shared their camp
Gathering ore samples from an exposed seam for future testing
Thronging around a deposit of gemstones
Gossiping about the weather with a repetition of groundhogs
Thwarting kobold incursion by poisoning their rust monster calvary
Grafting preciously rare pear cultivars - cider made from it magical
Tinkering with the inner workings of a remarkably complex trap
Guarding one of several secret routes into a gnome community
Transplanting a grateful dryad, hobgoblins decimating her forest
Guiding a group of halflings safely through hobgoblin territory
Trimming their outrageous nose hairs
Harnessing their semi-trained giant shrews to a sledge
Tumbling down a slope, gear and supplies flying as their mules bray
Harvesting special mushrooms, used to dye their characteristic caps
Underestimating a confusing fog, conjured by a kobold shaman
Hauling a minecart, laden with half-finished crossbow quarrels
Undertaking a secret mission to treat with lizard men
Helping a family of blink dogs dig a new den
Unloading a patient donkey to more carefully cross a rickety bridge
Hiding from a prowling manticore
Unproductively re-prospecting a played-out strike
Hoisting a large menhir into place to repay a debt to local druids
Vanishing from view after hearing a giant's earth-shaking footfalls
Hollowing out a log from a pitchlock pine into a serviceable sluice
Visiting a local wizard's tower, bearing rare components to barter
Infiltrating a gnoll tent-shrine to steal scandalous scrolls
Volunteering to help reap, looking to test an experimental thresher
Inventing a new type of dowsing rod, currently only works on beer
Wagering a month's mine-takings on racing rats
Junketeering by order of the king after a particularly brutal battle
Walloping a warp beast with their well-crafted warhammers
Kindling a small fire, burning with a sweet-smoking flame
Warming their gnarled knuckles over a strange, green glowing gem
Laughing at a mirthful marmot's jokes
Weaving their way through clandestine, circuitous routes for safety
Laying siege to a driver ant mound with an army of dire aardvarks
Woodworking indefatigably, this new catapult will surely work
Lifting the boom from a toll booth to allow human traders to pass
Yodeling family clan's deeds/accomplishments in a boasting contest

Table: goblin
Accusing the king's bodyguard of canoodling with the queen
Lurking beneath beds, up chimneys, and in cupboards
Assembling a flaming oil flinging contraption, poorly
Lying to their living statue leader about a recent defeat
Attacking a lone dwarf brewmeister
Marching to war against a manticore, soliciting aid
Attempting to cut the ropes suspending a rickety bridge
Meddling with a wedding by releasing ravenous stirges
Baiting and owlbear to steal its flecked blue eggs
Melting down copper coins into fat lumpy ingots for transport
Blandishing a grizzled bugbear into joining their tribe
Milking a very tired and incredibly ornery nanny goat
Blowing a prodigious amount of eyewatering soot out of a flue
Mixing a ton of potions in a cauldron and daring to drink
Boiling tatterdemalion clothing in acrid liquid to eliminate lice
Mocking a merchant by selling her own wares back to her
Bootlicking (sometimes literally) to impress a hobgoblin usurper
Mudlarking lost mementos in muck - can find almost anything
Carrying stolen hogsheads of cyclops wine to their hideout
Overturning a lemon cart with a rather ingenious trip line
Carving morbid, but surprisingly good scrimshaw from alicorn
Perching on high, lanky legs dangling in ragged, garish tights
Catching their supper - fluttering bats with motheaten nets
Pestering a pirate captain for permission to join their crew
Climbing up a wall to gather giant gecko eggs
Plotting to assassinate their king, but can't find any togas
Clutching their wickedly barbed clubs as they listen at a door
Positively plaguing after a cool wet, unseasonably smelly season
Cobbling bespoke shoes, magical ones, but not exactly fashionable
Puffing out candles/light sources with a special magic charm
Cooking down a stinking vat of bubbling tallow
Raiding a minotaur's larder, too lazy to stockpile their own food
Cowering from a domineering chimera, their new leader
Ridiculing one of number, born incredibly beautiful and kind
Crewing a leaky coracle across an eel infested pool
Riding their dire wolves on a sortie against a local village
Curdling milk on sight and giggling maniacally
Saluting a pile of dead fish as they file past
Dancing like throttled rag dolls to discordant thumb harps
Scouting a potential path for optimum booby trapping
Deceiving an orc overseer by smuggling in visitors for a price
Scowling at the thought of a sunny day
Destroying a perfectly good wagon by trying to outfit it for war
Scurrying like ants as they burnish a giant brass sphinx
Dipping their blades in refined crab spider toxins
Seizing a treasured spawning pit back from the kobolds
Dragging a dead gorgon, ropes fraying and snapping
Selling all sorts of useless trinkets for exorbitant prices
Drinking monumental amounts of sour gin
Shoveling out their pungent weasel kennels
Drudging for a scheming medium with grandiose plans
Sniveling as they petition their king for a pay increase
Dwelling at the bottom of a well - impressive collection of buckets
Spoiling for a fight, after ceding territory to gnolls
Eating two dozen grackles baked in a pie
Jealously squealing and squabbling over a set of ivory dice
Erecting a precarious pyramid of rubbish and offal
Squinting angrily in brighter-than-normal conditions
Flatulently trumpeting to signal the arrival of their king
Standing watch over a cockatrice cage, very jumpy
Fleeing after inadvertently disturbing a sleeping grizzly
Stealing abandoned children to bolster their numbers
Foraging for fungi, ears stuffed with wax due to the shriekers
Surrendering immediately to a wererat
Forcing open a stolen chest with crude crowbars
Swarming to defeat wight, it's not working well for them
Fouling a pond with pails of voracious giant toad tadpoles
Swindling a noble by claiming to be able to spin straw into gold
Grinning ear-to-cauliflowered ear as they watch a boxing match
Taunting a translator - wildly inaccurate definitions for goblin words
Grooming their haughty dire wolf masters
Teasing a carrion crawler out of hiding with salt pork on a string
Groveling ambitiously at the foot of a hill giant
Thatching the roof of a poor widow's cottage, not well, mind you
Guarding their hissing serpent hatchery
Throwing rotten vegetables at a talented bard
Hauling a sledge piled high with pyrite-rich rocks to their smelter
Tipping over a cauldron of boiling swine fat on invading delvers
Hiring an ogre for muscle, draining treasury nearly completely
Toiling under the cruel lash of a troll - mining corruptive minerals
Hoarding books of all shapes and sizes, utterly illiterate
Tormenting a somewhat holy hermit by driving him slowly insane
Hobbling a centaur captive to prevent escape
Trussing up a trespassing trapper
Hoodwinking a halfling farmer with debased coinage
Tunneling into a well-provisioned root cellar, after those onions
Infesting an abandoned mill, have repurposed the stone as an altar
Underhandedly hatching plans to betray their cloud giant mistress
Instructing a gnome on the proper uses of poisons
Unlocking an intricate mechanism with surprising skill
Jumping around yelping after stepping on their own caltrop trap
Warring with white apes over prime real estate
Kicking a metal helmet around as some form of sport
Wearing oddly fitting, tarnished, and cast-off dwarf armor
Laughing uproariously at an acolyte's sermon
Wheedling their rooster king to plan an invasion of a local hamlet
Loudly shouting words of warning with no threat in sight
Wounding a giant tuatara who has already eaten three of them
Lugging around immense mounds of junk on their backs
Yielding completely after a medium's sleight of hand demonstration

Table: golem, amber
Activating suddenly at a faint, distant sound
Noiselessly padding down a narrow hallway, dripping confidence
Burning brightly with a brilliant internal glow
Obeying orders from an acolyte in an ornate, feline mask
Carefully stalking some silent bugbears, relishing the challenge
Pouncing on a paladin, distracted by salacious frescoes
Crouching, shoulder blades askew, about to leap
Purring rapturously as they roll around in petrified catnip
Dreaming fitful dreams of being waited on hand and foot
Rasping as they lick their paws clean, occasional spark flying
Dropping yet another giant rat in a pile near an altar
Returning to their bejeweled dais after slaying a sorcerer
Examining their sublime reflection in a still pool ruefully
Scanning a dimly lit room with narrow, luminous eyes
Exploring their well-traveled territory once more, memorized
Scratching their ear with a furiously moving hind leg
Following a group of goblins, savoring the chase
Sensing an intruder, caramel colored ears twitching
Guarding a crypt containing an incorruptible saint's corpse
Swishing their golden, honey colored tail impatiently
Halting and bowing before a statue of a strange, snakelike figure
Testing their territorial limits cautiously with a sizzling amber paw
Honing hunting skills to the finest of points by eliminating all life
Toying with a troop of troglodytes, savoring the thrill of a rare hunt
Inspecting their scimitar sized, crystalline claws
Traversing an extremely narrow ledge with miraculous grace
Locating an invisible intruder, who blinks into sight with a swipe
Unravelling the wrappings of a mummified medium
Marring strange hieroglyphic carvings with their claws
Viciously mauling a medusa, searching for divine secrets

Table: golem, bone
Articulating from a large pile of bones, all of the sudden
Nosily rattling as they stiffly march down geometric paths
Battling an entire band of berserkers, barbed blades swinging
Orienting robotically to turn toward a distant sound
Climbing over the dusty remains of past victims
Pressing a recessed button with their four blades to open a vault
Collecting trophy skulls to line the hallways - hundreds
Protecting a completely pilfered throne room
Decisively lumbering along a predictable route
Reacting automatically with a salute as a lizard man passes
Escorting a confused mummified princess back to her crypt
Roving from ruin to ruin, searching for misplaced purpose
Finishing off a fighter after shattering his shield
Speaking with the voice of their long dead creator/master
Grating as they perform complex ceremonial drills
Standing utterly still among several standard skeletons
Hesitating just long enough to intone a request for a passphrase
Stirring after sensing the warmth emanating from a stray bat
Inhuming its most recent victims, digging with four shovels
Switching off suddenly, slumping and becoming inert
Jerkily positioning itself on a decorated plinth
Tracing sacred symbols tenderly with bony fingers
Keening eerily as a faint breeze blows through hollow bones
Unsettlingly grinning with echoing, empty laughter
Laughing maniacally, having long since slipped the bonds of sanity
Vibrating with clangorous mirth as a cleric presents a holy symbol
Lugging a defeated warrior to the edge of its territory as a warning
Wading through a warband of orcs, slicing and swinging
Menacing a medium, safely sheltered within a protective spell
Wielding wickedly curved swords that drip with ichor

Table: golem, bronze
Actuating with a groan and whistling plumes of steam
Malfunctioning after a blow to the head tore their shem
Behaving erratically, capturing foes instead of killing them
Notifying others of intruders using its thundering chest gong
Burnishing their massive metal fists against a worn boulder
Overpowering an ogre laden with purloined treasurers
Charging at a formation of worried hobgoblins
Pondering their purpose - slowly gaining sentience
Deactivating with a whining whirr after defeating an interloper
Processing a bard's clever answer to their riddle
Discharging jets of flame from large flaring nostrils
Quaking with rage after being targeted with a charm spell
Eradicating a wererat colony that recently moved in
Reducing a pack of thieving ghouls to pulverized cinders
Flailing as a thief hangs onto her golembane dagger lodged in back
Resetting complex mechanical traps as part of its programming
Gripping the haft of an absolutely massive blazing battle axe
Rotating torso to face a sound with a cacophonous grating sound
Hulkingly huge, showering dust as it squeezes through narrow halls
Searching through melted slag for suitable parts for self-repair
Infested with tiny fire gremlins constantly insulting and cackling
Spurting gouts of sticky, liquid fire from fissures along its shiny skin
Introducing itself with a long-winded speech in a forgotten tongue
Tirelessly tracking down a stolen sacred relic
Jolting awake after centuries of sleep with a grinding sound
Uncharacteristically swaying with a very damaged leg
Kicking down a door with massive metal feet, clad in spiked boots
Venerating at a shrine, coated with centuries of dust and dead insects
Loudly chewing on huge chunks of charcoal to refuel
Welding a metal door shut with a white-hot thumbprint

Table: golem, wood
Accompanying a medium, possessing a controlling circlet
Nocking an arrow, one arm ends in a permanent longbow
Backtracking after chasing intruders out of their domain
Oozing a sweet smelling, sticky sap that holds weapons fast
Creaking conspicuously as they support ceiling with arms overhead
Operating instinctively after termites began boring into their head
Crumbling from an unfortunate infestation of woodworm
Planting ancient tree seeds wherever they travel
Defending a doorway earnestly, with another entrance nearby
Programmed with politeness, bows deeply before disemboweling
Eliminating a party of adventurers with seven swift strikes
Quenching a flaming leg in a conveniently placed pool of water
Emerging suddenly from a wonderfully whittled wooden wall
Remembering their former life as a treant, wistfully
Festooned with small, green sprigs of healing leaves
Roughly hewn, blocky, unfinished and bitter about this
Forlornly chiseling a spruce spouse from a tree trunk
Shaving a mossy mustache with a scavenged blade
Guiding an appropriately reverent elf to a tomb
Slightly charred from a run in with a chimera
Housekeeping - meticulously cleaning up after a battle with gnomes
Swinging their battering ram like arms against a stone panel
Identifying itself in the halfling tongue and asking intentions
Talking tenderly to a table
Longing for salty sea spray - once lived on as the figurehead of a ship
Uniformly covered with spidery carvings that protect it from flame
Lumbering creakily down a well swept corridor
Utterly stumped by a sphinx's riddle
Maintaining their wooden joints with the application of herbal oils
Wishing upon a star, yearning to be remade in flesh

Table: gorgon
Adopting an intimidating, widened stance toward a tree
Nursing two adorable and dangerous calves, very defensive
Ambling down somewhat steep foothills, cautiously
Obstreperously blaring for any challengers to hear
Bellowing resonantly, trying to attract a mate
On a tear, just left a hamlet now inhabited only by art
Billowing noxious green mist from their nostrils
Outraged by the presence of a giant weasel
Blundering down a steep riverbank to have a drink
Pausing their browse of bitterberry bushes to bugle blusterously
Bucking in response to a stabbing stirge bite
Pawing the fragrant sod, sage colored steam billowing
Charging a cougar, crouched in tall grass
Petrifying a paladin's warhorse, tied outside a cave
Chasing a rival bull to the edge of his territory
Plunging his keen horns into a haybale, where a gnome hides
Chewing loudly on a mouthful of pale grey grass
Powdering hard clods of clay beneath its hearty hooves
Circling a driver ant colony, itching for a fight
Puffing small gouts of gasses as it grinds grasses
Coddling a blaring calf, to keep it quiet
Pulverizing a chalky talc troll statue
Completely calcifying a halfling commandant
Quarrelling with enterprising gargoyle ranchers
Cornering a bandit on a treacherous cliff
Ramming a merchant's cart, laden with cyclops wine-barrels
Crashing through thorny brambles, protected by iron scales
Rampaging nearby farmsteads, leaving behind livestock statuary
Crumbling the outstretched arm of a cleric statue
Rearing onto its hind legs to try to crush a crafty warp beast
Crushing a sandstone rattlesnake under hoof
Roaming near the outskirts of a nervous hobgoblin camp
Defending a piece of pasture, dotted with sculpture
Roaring with rage as he senses another bull in the distance
Demolishing a diorite dwarf
Rushing down a steep slope, chased by barrow wights
Destroying a wagon, as frightened traders flee on foot
Rutting and therefore wise to avoid
Discharging sparks as they roll on flint shard-strewn ground
Sauntering up to a grizzled farmer (ex-adventurer) to be fed
Entombing a tonsured friar in travertine
Savaging a stand of trees to mark the edge of their domain
Exhaling chartreuse miasma in a flowering meadow
Scowling as skeletons burnish her scales with stiff bristled brushes
Exploited by a talentless sculptor - his works adorn several shrines
Scratching their scaly hide against a well-worn boulder
Flaring their cavernous nostrils menacingly
Shattering a shale shield bearer
Fording a rushing river, with snorts and splashes
Shrugging off a sling stone, barely noticeable
Fragmenting an exquisite sculpture of an elf firing an arrow
Smashing into a potter's kiln, seeking hot ash to eat
Galloping towards an unfortunately dressed bard - crimson cloak
Sniffing fallen apples near a worried dryad's tree
Glaring at a goblin, treed out of reach
Snorting defiantly after encasing a curious sage in stone
Goring a hill giant's thigh with his steel-sharp horns
Splintering a once sturdy wooden fence by leaning up against it
Grazing confidently amidst broken bodies on a battlefield
Staggering unpredictably after dining on unusual mushrooms
Grinding down flavorful pebbles with their tenacious molars
Stampeding in circles after a pack of cleverly winking blink dogs
Grunting in acknowledgment of their medusa milkmaid
Staring at a peaceful procession of acolytes
Headbutting an extremely detailed centaur statue, tipping it over
Stomping on siltstone crab spider
Hulking and huge, an extremely hefty specimen
Surprisingly acclimated to local lizard men
Immortalizing an illusionist in colorfully flecked igneous rock
Swatting away persistent gadflies with her flail-like tail
Impaling a paladin, locked in fierce combat
Sweating a frothy liquid, said to remove rust from weapons
Infuriated by falling leaves, thrashing their horns about
Swerving a charge to stab a stubbornly animate ogre
Inhaling giant gulps of air, preparing to unleash its horrid breath
Thrashing to escape an intrepid trapper's snare
Jumping over a halfling's hedges, leaving behind stone sheep
Thundering down a well-worn path after a dire wolf
Kicking a granite game warden with sharp year hooves
Tossing a gored thoul into the air with a swift jerk of their neck
Laboriously respiring, pollen from the wrackblister bush is awful
Towering over standard kine, taller than a warhorse
Lapidifying a now-limestone lion
Trampling down a patch of grass to lie down and rest
Lowing deep, discordant moos
Treading water to cross a deep lake
Lumbering through a circle of toadstools, upsetting sprites
Turning an entire band of berserkers to blue granite
Lunging at their wavering reflection in a pond
Uprooting a windmill, perceived as a challenger
Milling mineral deposits with their teeth, gouged from a cliffside
Utterly cantankerous after a recent wyvern wound
Munching on the calcified cape of a cut purse
Vexing an elfin enclave, their best hunters succumbing
Narrowing their glowing ruby eyes after hearing a distant howl
Warning others thanks to the presence of a feverishly placed cowbell
Negotiating a narrow cobblestone bridge, with clumsy clatter
Wrecking a group of basalt bugbear statues
Nosing at a freshly filled grave
Yoked to till rocky fields for geode planting by stoic stone giants

Table: griffon
Absent-mindedly flapping their massive wings to cool off
Nesting atop a positively enormous tree
Accepting eohippus tribute from superstitious neanderthals
Nibbling at their hairy hide, itching from sky fleas
Alighting atop a giant skull, glistening with dew
Nodding their aquiline head as they drink from a lake
Almost spooking a herd of grazing antelope
Nuzzling their nomad ranger companion affectionately
Basking contentedly, flexing their talons and claws
Observing a vine-tending cyclops shrewdly
Bounding blithely across a blossom blanketed meadow
Occupying an abandoned bear den
Bright, scarlet face, like a bateleur, sunbathing
Panting to thermoregulate, pink tongue flicking
Bristling and tensing after hearing a distant whinny
Perching majestically on a bluff, silhouetted like heraldry
Carrying a basket in their beak, containing a dwarf infant
Performing a perfect barrel-roll to avoid a hill giants bola
Chasing after a sheep-sized rabbit
Picking at the carcass of a grizzly bear
Clacking their beak constantly, looking for their cubs
Plummeting suddenly to avoid a bolt of lightning
Climbing to a vantage point, high among stringy clouds
Pouncing on their shadow for hunting practice
Consuming a mountain goat, snatched from a cliffside
Preening their plumed mane tenderly with their talons
Countenance of a condor, panther-black fur and wings
Prowling along the edge of a wood, wary of losing open sky
Cresting over thick treetops, scanning the canopy
Purring with pleasure as their paladin scratches their back
Darting into cover, sensing a dragon's flight
Pursuing a pack of dire wolves, hoping to steal a kill
Defending a fallen ranger from gnolls with nets
Questing for a mate, leaving sign and scratches on trees
Devouring a destrier, barding and all
Quickly springing onto a giant rat, silencing its squeaks
Diving towards a dervish archer
Raking their talons across the tough hide of a rhinoceros
Dragging a humungous snake up a steep slope
Ravenously hungry and emboldened by starvation
Dropping rotting stink melons on a hobgoblin camp
Regurgitating food into the beaks of cacophonous cubs
Emerging from a bank of clouds briefly
Rending an ogre's shoulder with a swooping attack
Entangled in a cloud giant's net
Ripping strips of meat from a mule with their sharp beak
Eviscerating an egg thief, found creeping toward her nest
Roar-shrieking, a blood-curdling and terrifying sound
Fawning over a shiny, gem-studded crown
Rolling around enthusiastically on some sort of strange herb
Feasting on fish, expertly caught near the water's surface
Savaging a spear-wielding band of orcs
Fighting over a prime roosting location, very violent
Screaming their piercing call from an echoing bluff
Fluttering rapidly as they select a suitable landing site
Seizing a halfling, bent over to investigate mushrooms
Glaring at distant thermal-hogging wyverns
Sharpening wickedly curved talons on a sap weeping treant
Gliding effortlessly, folding their wings to suddenly dive
Snapping at their seller - a wily bugbear trader
Gripping onto the outstretched arm of a titanic statue
Soaring high above a galloping herd of zebra
Growling at encircling goblins, armed with pitchforks
Sprinting to build up speed for a leap into flight
Harpy crested and regal as they survey for prey
Stampeding wild horses, looking to pick off the weakest
Hissing, punctuated with chirps, as a tasty badger escapes
Stealing a foal from hobgoblin stables
Honing their huge beak on a sparkling, smoothed boulder
Stooping to stare a brave gnome directly in the eyes
Horse-hunting - frantic whinnies punctuated with screeches
Striped, like a tiger with a vulture's head
Hunting bighorn sheep for their storm giant keepers
Stunning a stone giant after striking them with incredible force
Hurling towards a hippogriff in a spat over territory
Swallowing chunks of meat, being tamed by a ranger
Idly circling a nomad camp as they clean and dress a kill
Swooping in a dogfight with a pegasus
Ignoring their master's commands in favor of horseflesh
Systematically selecting the appropriate feathers to pluck
Incubating a clutch of large mottled eggs, ready to hatch
Tearing the slate roof tiles off a church, priest in tears
Joyfully crunching and cracking deer bones
Tethered to a wizard's tower, ensorcellment wearing thin
Jumping off a precipice, taking flight at the last minute
Tormenting a pterosaur, blown far off course by a storm
Keening mournfully over the body of a dead elf
Unfurling their wings, using beak to spread musky oils
Lashing their tail furiously to swat at gadflies
Vainly strutting, letting out the occasional aloof squawk
Launching themselves at a bellowing ox
Vexing a roc by flying low among the trees
Locked in death-defying aerial battle with a manticore
Viciously gouging into the hide of a dead bull
Mauling an overturned wagon, as screams echo inside
Watching a trio of travelling centaurs hungrily
Mewing inquisitively as a druid offers an empty hand
Wheeling in the gyre of an angry air elemental
Molting slightly, shedding feathers prized by warlocks
Wounding a chimera on the wing

Table: halfling
Accusing an itinerant merchant of swindling
Knocking politely on each passed boulder with knobby canes
Admiring an ornate, bulging belt pouch on the waist of an elf
Leering at a plump and glistening rotisserie chicken
Annoying a dwarf with persistent questions about their beard
Liberating a veteran from a harpy's thrall
Awarding a prize for the most massive parsnip
Listening intently at a thick oaken door
Baking fluffy flat breads on the coals of a campfire
Loaning some billy goats to local dwarfs to stud
Basting a turkey to tenderness as it roasts in a big cast iron pot
Loudly testifying against a suspected goat rustler
Befuddling a hobgoblin scout by changing road signs
Maundering aimlessly after being exposed to confusing spores
Borrowing a teacup of honey from a local giant beehive
Meddling with the local economy by shorting the shallot market
Bragging to each other about how far they can lob a pebble
Milking docile nightwool sheep for a sought-after local cheese
Breaking their fast for the fourth time today
Mournfully strumming broad-bodied balalaika/tap sad tambourines
Cheerfully eulogizing a foolhardy folk hero, taken by a wight
Munching on a seemingly endless supply of pocketed apples
Clucking as they painstakingly choose betwixt sausages/lambchops
Neutralizing a glob of green slime with burning torches
Clustering around a statue of a halfling child, near gorgon tracks
Nourishing an underground fungal farm with night soil
Complaining - insufficient sunshine/too little rain, same sentence
Observing troop movements of raucous brigands, nervously
Confounding a goblin warband with a clever net trap
Ostracizing a community member for dabbling in sorcery
Conning an acolyte out of their rations by convincing them to fast
Overindulging on fried catfish/unusually strong dogpear cider
Coveting a medium's gemstone studded brooch
Pickling delicious duck eggs in a spicy, sour brine
Cultivating super savory mushrooms that taste just like steak
Planting shortapple seeds wherever their travels take them
Dancing uncontrollably after a tarantella bite
Plowing a stone-tablet riddled field with an ornery donkey
Deceiving a dim-witted hill giant into repositioning a boulder
Prying open a wax-sealed iron coffer with a crowbar
Deputizing next adventurer they see to deal with a troll problem
Pulling together on a fishing pole - hooked a nixie's giant bass
Digging a well, accidentally discovering a dungeon passage
Queueing impatiently to purchase imported pipeweed from a dervish
Dining on a sumptuous five-course feast with plenty to go around
Raking up abundant pecans after a bumper crop
Ducking under the lanky legs of an over-sized ogre
Recounting a tale of a brave fighter, terror-stricken by giant shrews
Embellishing a story about how they bamboozled a bugbear clan
Rescuing a prized pet rabbit from an over-eager owl
Escorting an elderly matriarch on a visit to a sacred barrow
Riddling patiently with an almond treant in flower
Evicting a kobold tribe from a nearby forest
Roasting courgettes and aubergines with pungent grave garlic
Excavating a new home in a sod-covered hillside
Scheming with local sprites to trick a cloud giant
Farrowing a litter of pink piglets from a sighing sow
Settling a score with a greedy orc warlord
Feeding a weary wizard, hoping she can undo a cyclops' curse
Shaking a white rind peach tree to collect the ripe and fuzzy fruit
Fidgeting in their hiding places as dastardly bandits pass
Shouting shrilly, being chased by thirsty stirges
Foddering their remarkable ponies with oats fit for a noble's table
Simpering & dumbstruck by a corpulent trader (secretly devil swine)
Gathering firewood, deadfall only, in a dryad's wood
Skipping smooth stones across a lake - the record is forty-seven skips
Giving a minotaur the slip, as he stomps in frustration
Smelling awful after a run-in with a dire skunk
Gossiping about local scandals, mostly involving turpitude
Smoking punchy pipeweed out of self-lighting, magical pipes
Grinning ear-to-ear as they carry bushels of corn
Sneaking up on a bouquet of pheasants, slings at the ready
Growing exotic pipeweed, prized by pirates to treat seasickness
Snooping around a ruined shrine, following rumors of gold
Haggling with a trader over high prices of saffron and cinnamon
Sowing sorghum and spelt seeds in tidy furrows
Harvesting hazelnuts by shaking trees over a blanket
Storming the suspected crypt of a vampire, girded in garlic garlands
Hiding from a hungry wyvern, plaguing these parts
Strolling stealthily across a twig-strewn floor
Hurrying burlap-bag footed brightbill geese to market
Stuffing a scarecrow with straw, satirizing a local sheriff
Idling around an extremely large tree stump, puffing on their pipes
Sullenly eating preserved rations, pining for spices and salt
Imbibing apple brandy from durable tin snifters
Trapping eels with ingeniously woven baskets
Imprisoning infamous highwaymen, hoping to collect bounties
Trudging barefoot among red-tipped devil nettles, unbothered
Inspecting gourd garden, adjusting blocks to shape pipe stems
Unhappily migrating to a new home after a dragon induced wildfire
Insulting an overconfident charlatan, subtly
Virtually vanishing among verdant undergrowth
Jeering at a bedraggled goblin, stuck in a deep pit
Volunteering to squire for a comely knight
Joking jovially with a gnomish jeweler
Weeding headstones, inscriptions obliterated by the passage of time
Journeying to visit a holy /ling relic of questionable authenticity
Whittling whimsical pipe bowls out of valuable meerschaum
Kneading the sticky brown dough, used for durable trail braid
Yearning for a warm, cozy hearth and a comfy, cushioned chair

Table: harpy
Accosting a giant bat trying to find a roost
Luring a lizard man toward them with seductive shanties
Allowing a paladin thrall to lavish them with compliments
Manically primping while a stupefied gnome holds a glass
Ascending on surprisingly warm air currents
Mesmerizing a minotaur away from his maze
Atop a tall, barbed spire, an easy climb for most
Mincing giant centipede into tiny chunks to feed hatchlings
Bathing in a brackish, stagnant mud puddle
Nagging a spellbound nomad to choose the fairest
Beckoning a befuddled bandit near
Nauseating all who approach their nest due to the foul stench
Being fanned by thralls, with large fronds
Neglecting a nest mate with a wounded wing
Bribing a medium with molted feathers and eggshells
Nesting for the night atop a petrified treant
Building an untidy nest of bleached bones and straw
Noisily thronging to a too-small aerie
Cantillating quietly as they prepare a prisoner for death
Ogling a beautiful neck scarf, worn by a noblewoman
Carrying off a whimpering bugbear whelp
Outwitting an orc shaman, sent to drive them away
Castigating a member of their clamor for falling in love
Perching within the sides of a deep pit
Cavorting on an overturned rowboat
Plucking out random feathers for inscrutable reasons
Charming an archer into feeding them grapes
Plunging poste-haste after hearing a hobgoblin hunting horn
Compelling a frightened midwife to care for an egg
Pouncing idly on a very confused rat
Completely captivating a cultist with their canticles
Precariously balanced on a jutting banner pole
Crooning a deceptively soft song about vengeance
Preening as they fight over a cracked hand-mirror
Cutting quills from their shed feathers to write bad poetry
Promptly plummeting after a dropped diadem
Defiling an ornate shrine with rubbish and offal
Punishing a hypnotized houri for cleaning
Delighting in a battle between two of their thralls
Quavering tremulously as they attempt a difficult descant
Directing a charmed thug to fetch some firewood
Quickly beguiling a goblin bodyguard
Dislodging and retrieving arrows after a recent attack
Reeking of ammonia and rotten eggs
Diving suddenly to spook a smuggler
Resting on flea-eaten, moth-infested silk pillows
Dropping turtles from great heights to crack open their shells
Roosting on a precarious ledge
Easily offended if their garish makeup goes uncomplemented
Ruffling their plumage as they pose for a painter
Enrapturing a trader, to steal all of her spices
Scratching deep gouges in a mahogany desk with their claws
Ensorcelling the sage's apprentice, sent to study them
Serenading spellbound sailors
Enthralling a new poet, to compose odes to their beauty
Shrieking as they alight to avoid a draco lizard
Feeding on exotic fruits, hand delivered by their thralls
Singing their trademark tunes to control a neanderthal tribe
Fighting over a confiscated, albeit chintzy crown
Snatching a catchpenny lavaliere from the neck of a thrall
Fitfully laying large, mottled eggs
Stinking of sweat and cheap incense
Flapping frantically to avoid a giant rattlesnake
Strutting assuredly across a narrow ledge
Flaunting floridly rococo hand-fans
Stubbornly occupying the top of an abandoned tower
Floating clumsily on the surface of a pool
Surveying the area from the sky - on the lookout for food
Flocking around a sack of shiny baubles and bagatelles
Swatting at a persistent swarm of flies
Fluttering just out of an angry ogre's grasp
Swooping down to snatch a sack from a merchant's mule
Fussing with their feathered coiffures
Tending to their disgusting daily anti-ablutions
Gathering bushels of fish daily from famished fishermen
Tormenting a confused cleric
Giggling contagiously at a joke told in their own tongue
Trilling loud territorial calls
Gliding awkwardly against a gusty wind
Unfurling a grimy tapestry, filling the air with mold and mildew
Grooming their matriarch in preparation for a party
Urging a thrall to ambush the troll that annoys them
Hanging garlands of fragrant herbs around their messy nest
Utterly bewitching a berserker with their song
Harassing a halfling, wisely ear-waxed against their charms
Vainly vamping to a dumbstruck audience of kobolds
Hissing and lobbing stones at a group of ghouls
Visiting with an old friend - a malicious manticore
Huddling around a helpless hermit
Vying for a higher place in the pecking order via gossip
Inhabiting a hollowed-out giant's skull
Waddling in a huff after their wings got too wet
Insulting a nest mate and cackling maniacally
Wailing vociferously to drown out an acolyte's hymns
Landing atop a statues arranged in a circle
Warbling to themselves as they sift through rubbish
Laughing as they shave a besotted dwarf's beard
Weakening the resolve of a resilient friar, verse by verse
Loudly screeching after losing a gaudy brooch
Wooing a wood-spouse away from their dryad wife

Table: hawk
Ascending gracefully to gain a better vantage point
Regurgitating their last hunt into the gaping mouths of chicks
Banking hard to avoid an incoming arrow
Resting atop the peaked roof of a gnarled wizard's tower
Coasting calmly on warm thermals, letting currents do the work
Ruffling their feathers, puffing up against a cool breeze
Drifting lazily over a lake, looking for delicious fish
Sailing through the sky, on the lookout for their master
Eyeing approaching hobgoblins from a high perch
Scowling at a thin black curl of distant smoke
Flapping a shower of dew from their damp wings
Screaming as they careen through a canopy of trees
Floating, almost stationary, fighting a strong, sudden wind
Soaring above a bloody battlefield in search of easy pickings
Fluttering tentatively from tree to tree, looking for their mate
Spiraling into tighter/smaller circles on territorial patrol
Gliding between the clouds, flexing their talons
Squinting from their nest at an egg-hungry snake
Hovering briefly before folding their wings into a rapid dive
Surveying a forest for interlopers on behalf of their elf-friends
Molting awkwardly, looking rather bedraggled & weatherworn
Swooping down to rake a bandit with their talons
Passing overhead, startling all manner of small animals
Turning and turning in the widening gyre
Plucking the juicy eyeball out of a dead cow's head
Unfurling their wings to bask in the warmth of the sun
Preening meticulously, so that no pinion is out of place
Veering abruptly in response to a distant clap of thunder
Quickly descending after catching sight of a roc
Watching over a wounded ranger, bringing her food
Attacking a mischief of magpies, living up to their name
Pecking at the carapace of a driver ant reluctantly
Bathing in a still operating, but long abandoned fountain
Plummeting suddenly, winged by a volley of crossbow fire
Catching salmon as they leap upstream to surmount falls
Pouncing on a squirrel, actually a polymorphed priest
Chasing one another playfully, honing their flying skills
Puffing up their chest feathers and becoming quite round
Clutching a dead rabbit tightly in their talons
Refusing to return to their master's arm
Diving toward a scurrying rat
Ripping out beakfuls of feathers from a dead chicken
Dropping a luckless tortoise, in hopes of cracking it's shell
Roosting in the secure boughs of a bellicose treant
Eating scraps from the leather gloved hand of her handler
Screeching at the top of their lungs at a gnoll scout
Entrusted with an important message to a distant elf kingdom
Snapping to attention for inspection by their pixie riders
Fanning out their wing in a satisfying yawn and stretch
Spreading wings, perched on a gibbet housing a horsethief
Feathering a third-year nest with soft chest down
Struggling to untangle from an intricately woven kobold net
Gorging on the carcass of a goat
Swallowing a vole whole
Gripping a hawker's arm tightly as he stifles a scream
Tethered to a signpost, occasionally croaking mournful cries
Hunting foxes, prized by their trainer for their fur
Tinkling due to the platinum bells tied to their left leg
Nodding and bobbing their head at a murmuring medium
Whistling and clicking their beak contentedly as they groom

Table: hawk, giant
Ascending gracefully to gain a better vantage point
Regurgitating their last hunt into the gaping mouths of chicks
Banking hard to avoid an incoming arrow
Resting atop the peaked roof of a gnarled wizard's tower
Coasting calmly on warm thermals, letting currents do the work
Ruffling their feathers, puffing up against a cool breeze
Drifting lazily over a lake, looking for delicious fish
Sailing through the sky, on the lookout for their master
Eyeing approaching hobgoblins from a high perch
Scowling at a thin black curl of distant smoke
Flapping a shower of dew from their damp wings
Screaming as they careen through a canopy of trees
Floating, almost stationary, fighting a strong, sudden wind
Soaring above a bloody battlefield in search of easy pickings
Fluttering tentatively from tree to tree, looking for their mate
Spiraling into tighter/smaller circles on territorial patrol
Gliding between the clouds, flexing their talons
Squinting from their nest at an egg-hungry snake
Hovering briefly before folding their wings into a rapid dive
Surveying a forest for interlopers on behalf of their elf-friends
Molting awkwardly, looking rather bedraggled & weatherworn
Swooping down to rake a bandit with their talons
Passing overhead, startling all manner of small animals
Turning and turning in the widening gyre
Plucking the juicy eyeball out of a dead cow's head
Unfurling their wings to bask in the warmth of the sun
Preening meticulously, so that no pinion is out of place
Veering abruptly in response to a distant clap of thunder
Quickly descending after catching sight of a roc
Watching over a wounded ranger, bringing her food
Alighting on the corpse of an ogre, driving away crows
Nesting atop a weathered monument, defaced by lichen
Beating their massive wings, low and creating dust
Perching on the outstretched arm of their cloud giant keeper
Brooding huge speckled eggs, tenderly turning them
Piercing the skies with their shrill, cacophonous cries
Building an enormous nest, braiding large boughs/small trees
Plunging their talons into a large crocodile
Carrying away a struggling goblin as a courtship gift
Preying on a giant snake, intends to share with fledging chicks
Circling above a over-zealous logger, signaling to druids
Pursuing a quiver of wyverns out of their territory
Defending their airspace from an intrusive griffon
Questing alongside their plumed paladin rider
Devouring a deer, atop a large bloodstained boulder
Reconnoitering for their first nest, seeking the perfect spot
Feeding their young bits of what appears to be bugbear
Shrieking loudly as they wheel into a rapid dive
Fishing over a lake, deftly snatching a giant catfish
Skimming the surface of water with their wide wingtips
Glaring menacingly at adventurer's setting up a camp
Slamming into a troll, the full force nearly knocking it down
Grabbing a helpless gnome to larder for later
Spirting away a halfling farmer, with rake still in hand
Guarding a shrine to a feathered deity, well-fed & mostly tame
Straying nearer and nearer to a cyclops's flock of sheep
Harrying a hippogriff herd, about to create an aerial stampede
Tearing gory strips from a giant tuatara
Landing near a stream to dip their beak for a drink
Trained to respond to commands in giant, escaped long ago

Table: hellhound
Agitating an ochre jelly
Melting a beautiful elf breastplate into lumpy slag
Alerting each other of potential prey with loud yelps
Miserable from recent rains
Ambushing an unsuspecting owlbear
Muzzles blazing as they embark on a unicorn hunt
Arching their coal-black backs as they stretch and yawn
Nibbling at fire flea infested shanks
Awakening at the sound of a distant, noisy clang
Nipping the heels of a sage turned prisoner
Badgering a runt in the litter
Obeying orders from their flame salamander stewards
Basking atop a big bonfire
Outsmarting a torment of ogres
Baying with a sound a bit like a blast furnace
Panting happily, generating a micro-sirocco
Bedeviling a scorched rust monster
Pawing at the bottom of a stubborn iron door
Belching ash and cinders after eating giant rats
Perking pointy, pitch colored ears at a distant sound
Bounding after a pack of blink dogs
Picking at a barbecued berserker
Burning embroidered curtains with sadistic glee
Protecting pups, so young they still spit sparks
Burying charred bones, covered in chain mail slag
Pursuing prankster pixies who doused them with water
Cautiously shadowing a water elemental
Reducing a wooden statue of a saint to ashes
Charring the feathers from a fleeing owlbear
Retrieving an escaped orc drudge
Chasing after a warp beast for sport
Returning from the scene of a barn arson
Completely cremating an unlucky kobolds
Roasting a giant tuatara, scales and all
Defending their sweltering den from any interlopers
Rolling around on embers from a burnt bed
Dragging a burnt bugbear somewhere to eat in peace
Romping around, playfighting to defeat boredom
Driving singed sheep into a stone pen
Rubbing their hides against a rough stone wall to scratch
Drooling viscous trickles of sizzling napalm
Running after a wounded manticore
Eerily yapping with strange, infernal calls
Scorching a tethered horse
Encircling a very worried troll
Scratching cinders from behind their ears
Enkindling a huge pile of straw
Searing an inquisitive tiger beetle
Enthusiastically tracking a tiger
Setting ablaze a bandit enclave
Following a dwarf's distinctive scent trail
Shaking the soot from their coats with pleasure
Frolicking amid flames of their own fabrication
Slavering molten spittle as they bring down a deer
Giving chase to a carcass crawler
Slightly singeing a sell-sword
Glowing orange eyes sneer from the shadows
Snapping through burnt bones with powerful jaws
Gnawing on a large lump of lignite
Snarling at a newcomer with dire wolf stock
Gouting jets of flame to signal to distant packmates
Sniffing the air for signs of their quarry
Growling and groaning like green wood, tossed on a fire
Spewing small curls of smoke from their nostrils
Guarding an enormous cradle, carrying a fire giant infant
Sprinting after a garishly colored giant centipede
Harrying a hippogriff, feathers scorched and unable to fly
Stalking morosely around an icy wall
Haunting an abandoned fire elemental summoning circle
Tail-chasing while they await their warlock's commands
Heating the entire area to an uncomfortable level
Their constant barking sounds like campfires crackling
Heckling a medium, desperately stomping on flaming robes
These are the even-awfuller three-headed variety
Herding a group of goblins to their fire giant master
Touching off a pile of scrolls and scriptures
Hounding the owner of a magical staff of ice
Trailing behind a pack of gnolls, potential allies
Howling mournfully on the edge of a body of water
Unhappily leashed to an obstinate, nonflammable boulder
Hunting giant toads for blackened fricassee
Unleashing their fire-breath in spurts as they howl
Igniting a winter store of grain out of sheer malevolence
Using their breath to steam their salmon supper in situ
Incinerating the ties suspending a rope bridge
Vanquishing a mummy, who encroached to close to their turf
Irreverently torching a traveler's shrine
Vexing a halfling hamlet by setting gardens alight each night
Judiciously smelling an efreeti's proffered palm
Wagging wiry tails with joy as an alpha returns from a hunt
Leaping upon a frost salamander with fury
Watching over a route, obviously trained to guard
Licking their course ebon fur, each lap sizzles slightly
Whimpering after inadvertently treading in a puddle
Lighting arrowheads afire for hobgoblin allies
Whining to their thoul masters for morsels
Making short work of an ill-prepared adventuring party
Worrying a wizard by straying too near his bookshelves
Maligning their master behind her back
Yelping in solidarity with a young red dragon

Table: herd animal, large
Avidly rubbing their sides against ancient trees to scratch
Gnawing on shed antlers to reclaim vital nutrients
Beginning to starve as food grows scarce
Happily wading to feast on duckweed covered, tender lily pads
Charging at a roaring grizzly bear
Licking at minerals in the side of an exposed creek bank
Colliding, head to head to compete for a mate
Looming in thick fog as they lumber through overgrowth
Consuming magical grasses that allow them to see invisible
Migrating to cooler climbs as their coats grow shaggy
Declining in numbers to overhunting by ravenous ogres
Nuzzling the outstretched hand of a taiga druid
Defending their calves from a pack of hungry wolves
Obstreperously bleating to drive demarcate territory
Destroying a beaver dam as they swim upstream
Overrunning an inexperienced trapper
Drooling continuously as they confidently stroll
Pausing from their incessant bugling to drink
Enthusiastically snorting as they greet a familiar face
Permitting a herd of shaggy horses to graze nearby
Fattening up for lean months ahead on huge acorns
Roaming alongside nomads that rely on them for milk and meat
Foraging among scraggly, bare branched shrubs
Shedding bloody velvet strips from their massive antlers
Fording a raging river of freezing meltwater
Striding majestically, stopping to scrape at dew covered lichen
Friendly with feral gnomes that hide nearby
Trampling a camp of brigands, now stuck up trees
Furiously chasing away a mountain lion
Watching a sabre toothed cat intently

Table: herd animal, medium
Avoiding a rambling mountain lion
Loudly bellowing after being struck by orc arrows
Browsing tender leaves on low branches
Munching on the tender tops of beautiful wildflowers
Chewing on dry twigs and thorny stems
Nibbling inquisitively on some squat mushrooms
Congregating around the dwarf ranchers who feed them
Ruminating on dry, nutrient poor grasses
Crossing a stream carefully, wary of ambush
Rutting season has made the males extra ornery
Drinking at a watering hole, oblivious to predators
Stampeding a group of surprised berserkers
Encircling their young defensively, as a troll salivates
Stomping a warning, prior to charging a dire wolf
Exhaling plumes of steam in the cool air
Straying into a farmer's fields to feast on lettuce
Fanning away persistent flies with flicking tails
Surrounding a calving cow protectively
Following obediently behind a centaur ranger
Trotting swiftly to rejoin an exceptionally large herd
Galloping wildly in all directions after being spooked
Trudging in thick black mud, up to their ankles
Gorging on crunchy fallen pears
Viciously goring a neanderthal hunter
Honing their horns on an exasperated treant
Wallowing in a drying pond to keep away biting bugs
Huddling together against a blustery wind
Wandering aimlessly after the loss of their leader
Loping along a treacherous ridge after a landslide
Whistling echoes throughout a verdant valley

Table: herd animal, small
Agilely bounding over bushes and hedgerows
Playfully gamboling young attract attention from a hawk
Bolting after a distant rumble of thunder
Protecting a grove of dryad saplings
Carefully eating around the poisonous portions of plants
Quickly scattering after a panther's pounce
Deftly spotting an approaching hunter
Running frantically away from a hobgoblin quartermaster
Expertly stripping thick curls of bark from tree trunks
Scampering through dense undergrowth to avoid wolves
Frolicking in a clearing as a unicorn watches on
Scent-marking on the trunks of trees
Grazing among sheep bones on abandoned pasture,
Sharpening antlers/horns on a statue of a dwarf
Gulping huge breaths of air to smell for rivals
Springing gracefully away from a snapping crocodile
Headbutting males do little to distract watchful mothers
Startled by the slightest sound after smelling a lion
Jovially prancing with horns/antlers on full display
Straining, held fast with thick and sticky spider webs
Leaping a muddy ravine, carved by a flooding creek
Thriving thanks to the ministrations of a local hermit
Milling about a large male, leg caught in a snare
Travelling cautiously through an open area
Obstinately swimming across a large lake
Unconsciously gathering around hallowed ground
Overpopulating the area due to a lack of predators
Vanishing suddenly after hearing the snap of a twig
Panting in the sun, searching for a place to drink
Visiting a shrine to nature, where the pilgrims feed them

Table: hippogriff
Abruptly swooping after spotting a pear orchard from the air
Kicking an apple tree with hind hooves to knock down fruit
Adroitly fishing for giant bass in a secluded tarn
Launching from their rookery atop an abandoned tower
Alighting gracefully atop a moist turf-covered knoll
Leaping onto a bleating mountain goat
Ascending as one after the reverberating twang of a bowstring
Mercilessly chasing down a lone griffon cub
Attacking a shepherdess's defenseless flock - she hides near a rock
Meticulously plucking out certain feathers to line a nest
Baffling a cautious, carefully sneaking tiger by taking flight
Mournfully crying as they nudge a limp and lifeless foal
Battering a helpless scarecrow savagely
Nesting at the base of a tremendous treant
Bestially clawing at rotting logs to sharpen their talons
Nickering mares watch a strutting stallion with disinterest
Brooding a clutch of large eggs, speckled for camouflage
Noisily screaming as they clip the canopies of trees
Carrying their elf riders confidently on patrol
Nursing newly hatched foals who still have soft beaks
Carving chunks from a dead cow with their vicious beaks
Nuzzling their gnome trainer playfully, nearly knocking her over
Challenging a rogue male from another herd for pecking order
Obsessively rearranging shiny bits of treasure to impress mares
Charging down a hill to pick up speed, in order to take wing
Overconfidently divebombing an enormous tortoise
Circling high above a herd of wild donkeys
Pecking at a flustered, but unhurt gargoyle
Clinging stubbornly to a craggy bluff, surveying surroundings
Piercing the air with stringent territorial calls and cries
Coasting to a stop after suddenly landing in a field of flowers
Plummeting suddenly after seeing a roc on the horizon
Collapsing a dilapidated shack, home to a helpless hermit
Preening with the aid of a magic quill seeking medium
Congregating around an elephant that the strongest slew
Preying on prized deer from a local lord's preserve
Cresting a moss-covered mesa, scouting out nesting sites
Protecting a shrine to the godling of cumulus clouds
Darting in high grasses, trying fruitlessly to out-run flies
Pursuing an unlucky lioness to drive her away from the herd
Dazzlingly adorned with golden feathers and colorful coats
Quickly springing to their feet after a distant howl
Descending in lazy circles as the wind begins to pick up
Quietly grazing in a field of floridly flowering artichokes
Devouring a trader's horse as he scrambles up a tree
Rearing on hind legs to mangle a minotaur
Diving in turn to harry a grumpy grizzly bear
Regurgitating bits of purple worm to screeching young
Drinking watchfully from a cool melt-fed stream
Resting in the shade of a humongous granite foot
Dropping stones from great heights to crack tough fruits
Ripping chunks of chainmail off a dead hobgoblin
Encouraging warbling hatchlings out of their shells with coos
Roosting on a treacherously inaccessible peak
Energetically prancing across a prairie of purple flowers
Scattering at the distinctive shriek of a pride of griffons
Expertly skimming the surface of a pristine lake
Seizing a squealing boar with their wicked talons
Fanning themselves with their beautiful wings to cool off
Shaking of water from a recent downpour, bedraggled
Fleeing from a hungry flock of griffons
Sheltering from ominous clouds in an abandoned stable
Flicking their tails to try to drive away irritating gadflies
Singling out the weakest wild horse from a herd
Flying in a majestic "v" formation, taking turns at the crook
Snatching the shiny helmet from the head of a cursing dwarf
Following behind a centaur clan for safety
Soaring high above the heads of orcs on the war march
Furiously flapping their massive wingspans in gale force winds
Squawking defiantly at their nomad trainer
Galloping on scorched lands from recent fires, kicking up ash
Stealing a huge fish from a giant hawk, midflight
Gnawing off tough scales from a dead rock python
Stretching out their wings to bask in the sun
Gobbling, like turkeys - wings fanned out to make them larger
Sweeping through a narrow pass on the funneled currents
Grabbing an unsuspecting goblin, hunched over a stew pot
Teaching yearlings how to hunt by releasing a wounded sheep
Greedily scavenging a dead wyvern as ravens croak nearby
Tearing into sacks of oats on a halfling farmer's cart
Grunting as they gouge the ground for tender tubers
Trotting sullenly along a road with a wounded left wing
Guarding a organized complex of standing stones
Unexpectedly plunging to evade a high-flying blue dragon
Harnessed and clad in armor plates, pawing at a dead paladin
Unfurling their wings in unison to shield flightless foals
Herding a mass of skittish antelope into a dead-end pass
Vaulting across a wide river, barely avoiding a crocodile's jaws
Hovering above a hissing cockatrice, cautiously
Viciously rending a hill giant who invaded their nesting ground
Imperiously clicking their razor-sharp beaks
Violently screeching, their lead stallion caught in a trap
Inadvertently trampling a ring of mushrooms as pixies protest
Watching a slowly approaching ranger warily
Incubating a clutch, periodically rising to turn the eggs
Wheeling without warning, down from thick fluffy clouds
Jubilantly ganging up on a pegasus in an airborne dogfight
Whistling to assure the herd of everyone's safety
Jumping and bucking as they frolic in a forest clearing
Wounding a gibbering ghoul after nibbling on grave moss

Table: hobgoblin
Advancing under covering fire from longbow archers
Irritating a temperamental enemy with jeers and taunts
Allowing a defeated enemy army to return home
Issuing clear and distinct orders that each soldier repeats
As is custom, the general prepares a meal for their troops
Leading cowardly goblin irregulars by courageous example
Assaulting a brigand camp
Looting a burned caravan for any salvageable supplies
Assembling for inspection in full panoply
Maneuvering outskirts to put their calvary in better position
Assigning daily duties to a roster of soldiers
Marching to the eerie cadence of an elf skin drum
Attacking an enemy, after waiting for half to cross a bridge
Marshalling a unit into proper ranks and subdivisions
Baiting an undisciplined enemy in order to split their forces
Navigating a winding, tight pass and wary of an ambush
Begrudgingly using a doppelgänger ally to devastating effect
Nursing the wounded with cauterizing troll-blood tinctures
Besieging the fortress of a rival warlord
Outflanking foes thanks to the bugbear scout intelligence
Bivouacking in a painstakingly orderly fashion
Patrolling the bramble-topped walls of a prison camp
Blazing a trail for mules heavily laden with matériel
Paying off a bandit spy
Bodyguard tryouts, only the biggest and most brutal need apply
Pillaging a village that refused terms of surrender
Breaking through a berserker line to take the higher ground
Playing complicated strategic board games
Burning boats and bridges after crossing a river
Plotting impenetrable plans for a lightning fast strike
Calling a temporary truce to allow an enemy to bury their dead
Polishing their lacquered lamellar armor to a blinding shine
Calmly plundering winter stores of an abandoned hamlet
Pondering a risky course of action prior to taking it
Camping near the entrance of a recently discovered dungeon
Practicing temper control by trading provocative insults
Cannibalizing wagons for funeral pyre fuel
Preparing to take an unprepared, unexpecting enemy
Capturing a group of bandits, interrogating them about the area
Presiding over a tribunal to punish a rank-breaking mercenary
Clobbering levied conscripts with their superior armaments
Promoting a soldier for valor on the battlefield
Commending a lowly foot soldier for bravery in the face of defeat
Razing a wooden watchtower, still stacking the wood
Conforming tactics to an enemy, looking for a favorable opening
Reconnoitering the area with the help of dire vulture mounts
Conquering smaller settlements prior to a major engagement
Recruiting a minotaur into their ranks
Coordinating attacks with their expendable orc mercenaries
Refusing to surrender to tenacious elf guerillas
Defeating a group of heavily armored knights, led by a paladin
Relaxing by carefully grooming their riding horses
Defending a dervish encampment, recent converts to their faith
Repeatedly cleaning and re-assembling powerful crossbows
Deploying a siege contraption that fires fifty flaming javelins
Requisitioning supplies from a surprisingly plump quartermaster
Deterring reconnaissance with the aid of an experienced ranger
Rescuing soldiers, enslaved in a quarry cutting catapult ammo
Digging trenches to bolster a defensive line
Retreating from a desperate foe that summoned a wraith
Disrupting the suspected supply lines of an enemy force
Reverently folding the banner of a decimated regiment
Distributing rewards for exceptional service with joyous ceremony
Sabotaging troop transport barges by drilling into them from below
Drawing water from a well to fill dozens of well-made barrels
Saluting the daughter of the hobgoblin king, come to inspect them
Elite janissaries on a mission to retrieve a runaway king
Scouring mess dishes and singing songs of pyrrhic victory
Ensuring a surplus of pungent beer for an upcoming celebration
Scouting terrain prior to leading an army on a march
Enticing an enemy by presenting a deceptive advantage
Searching for the secrets to animate excavated terra cotta golems
Entrenched, sending runners for reinforcements
Seeking necromancer to learn a dead generals battle plans
Escorting an enemy general to a jury-rigged barn brig
Separating united forces by sowing discord between dwarfs
Establishing friendly relations with nearby fire giants
Skirmishing with shell-shield bearing lizard men
Evacuating in chaos after the assassination of their leader
Sniping generals/mediums/clerics from camouflaged positions
Evading an enemy with superior strength
Sparring mercilessly, occasionally resulting in minor wounds
Expediating victory by leveraging their thoul reserves
Staggering crossbow volleys for maximum efficiency
Feigning disorderly retreat to encircle an overconfident enemy
Starving their giant tuatara siege-breakers
Fighting off a virulent plague that's wiping out their ranks
Strategizing on how best to use animated skeleton reinforcements
First to the field and freshly awaiting an enemy's exhausted arrival
Subduing an enemy through intimidation, not a blood drop spilled
Foraging spicy herbs to augment the flavorless fare of their rations
Surveying a rocky outcrop for defensibility, plans drawn for a keep
Garrisoning in a very worried halfling village
Treating captured soldiers with kindness, sharing their food
Generating chaos and its companion - opportunity
Trying to coach an ogre on best position to take in battle
Harshly disciplining a soldier for dereliction during watch
Unleashing several slavering hellhounds to track a deserter
Inspecting a merchant's wares before paying a fair price
Whipping a soldier who misplaced their weapon

Table: horse, draft
Ambling slowly along a crumbling wooden fence-line
Plodding up to the bank of a pond to have a hearty drink
Being tenderly groomed by a one-eyed halfling farmer
Raptly champing on freshy mown hay
Chafing under an ill-fitting yoke
Scratching at dry, barren soil in frustration
Devouring fallen sour apples with toothy gusto
Slobbering as they take a proffered carrot from a cleric's hand
Hauling a cart, piled high with tanned hides, no driver in sight
Struggling with an overladen wagon, on a narrow bridge
Knocking down the crude gate to a paddock made of saplings
Swatting away sprites with a long, lively tail
Loping in lazy circles as they graze on sweet grass
Utterly bemired in rich brown muck, tired from struggling
Munching with melancholy on wild green onions
Viciously biting the bandit who stole him
Nibbling the shoulder of a nomad playfully
Wearing a dusty blanket that is actually a valuable tapestry
Overworked and old, but surprisingly fearless
Whinnying as they gallop away from a group of goblins

Table: horse, riding
Abruptly bucking at the sight of a rattlesnake
Mischievously gnawing through their leather tether
Agilely cantering at the direction of their ranger rider
Neighing softly as a knight brushes their mane
Bolting down a sack of spilled oats
Nuzzling the lifeless body of a brigand
Clattering as they stroll over cobbled stones
Outrunning a pack of ravenous gnolls, hungry for horseflesh
Curvetting over hedgerows/dense undergrowth
Prancing across a pleasantly scented field
Faltering as they attempt to scale a rocky slope
Racing to the aid of an injured illusionist
Galloping away from a bellowing gorgon
Snuffling as they gorge on a barrel of beets
Hobbled hind leg, gently tied with a elf silk rope
Stopping suddenly to investigate some pears, rider flummoxed
Jumping a crumbling wall, wizard astride her back
Stumbling due to a sharp stone in their shoe
Lathering under the lash of a hobgoblin rider
Violently swerving, nearly tossing their rider to avoid a pit

Table: horse, war
Aimlessly pacing around a dead paladin
Nickering softly after escaping from a griffon
Balking at a fast-flowing river
Nudging a squire into a dark and dismal cave
Charging, full clip at a band of bugbears
Overburdened with bulging saddlebags, full of sand as bait
Foundering within the web of a giant black widow
Pawing the ground in preparation for their rider's joust
Hitched to an unhappy dryad's tree
Pursuing a scrambling squad of hobgoblins at breakneck speed
Hooves clopping loudly on a path worn to bedrock
Rearing suddenly to trample a troll
Impatiently stomping as their rider sleeps nearby
Rejoicing upon being reunited with their templar rider
Jangling in exquisitely crafted barding, replete with bells
Shod with magic shoes that allow it to speak, very eloquent
Leaping over a narrow ravine, effortlessly
Sneezing from thick spores of puffball mushrooms
Muzzled and hungry, no owner in sight
Tethered near an excavated entrance to a barrow

Table: horse, wild
Awkwardly scrambling among frequent gopher holes
Perking their ears at a distant rumble of thunder
Chewing on a spiny succulent for crucial moisture
Protecting a foaling mare by standing in a circle
Crossbred with pegasi, tiny, vestigial wings
Shying away from lasso bearing locals, wary
Dueling for dominance, two males fight fiercely
Heartily snorting as they romp and caper
Flicking their thick tales to frighten away flies
Spooked by the shadow of a roc overhead
Grazing peacefully on a windswept prairie
Stampeding as a herd after an attack by a big cat
Joyfully cavorting among tall blades of vibrant grass
Trampling over the bones littering an ancient battlefield
Kicking at a rock python that slithered to close
Trekking to a nearby watering hole, thirsty and nervous
Limping from a badly healed leg wound
Trotting and shaking their bristling manes
Panicking at the sight of lizard men poachers
Whickering contentedly as their teeth clip flowering shrubs

Table: hydra
Which drools a foul venom that causes nearby plants to become poisonous
Howling as a head is severed by a veteran's axe
Which spits a poison that clouds vision/makes victims see figments
Hunting stegosaurus, a favorite meal
Which regrows heads unless stump is blessed/doused with holy water
Investigating a barrow chamber, opened by recent earthquake
Which when head is severed, a giant grasping hand sprouts in its place
Joining forces with a conniving black dragon
Which, if decapitated, head slithers and attacks as giant snake
Knotting around most prized possession - an inert amber golem
Whose one of every heads bites with a potent paralytic
Lumbering through the brush, leaving a wake of destruction
Whose bony collars must be broken (blunt weapon) before heads can be severed
Lunging at a circling gargoyle with snapping jaws
With vile, coagulating blood that acts as green slime
Making a large nest out of the bones of heroes
Which only flame or acid can prevent heads sprouting where one is cut off
Mesmerized by an emerald the size of a giant's fist
Which can breathe gouts of flame (as hellhound)
Munching on a giant ant colony
Which exhales a choking miasma (as yellow mould)
Napping, one head always painfully alert and perceptive
Where four skeleton warriors climb out of neck stumps when a head is removed
Nuzzling the powerful wizard that charmed them gently
Which has one vital head which, when severed, the others won't regrow
Ousting a family of white apes from their cave by force
Which flails neck stumps for additional bludgeoning attacks
Overtaking a fleeing flame salamander
With rapidly distending jaws - can swallow elf or smaller (as giant sturgeon)
Pacing at the perimeter of a huge, crystalline wall of ice
With hypnotically swaying heads and confusing gaze - charm person thrice daily
Piling another set of armor atop a glittering hoard
Which spurts a black, blinding bile when head is severed
Placated by sacrifices, regularly tied to a gnarled tree
Which is capable of vomiting forth a swarm of stirges
Quibbling with itself - which direction to go, majority favors east
With constricting, flexible necks (as giant octopus)
Raging berserkers are severed in half by snapping bites
Which, by sowing the teeth in salted soil, will generate a group of ferocious fighters
Reaching after a treed halfling, extending a long neck to the limit
Approaching a drinking gorgon stealthily
Recoiling after one of its heads is caught in a steel bear trap
Attacking an unfortified hamlet stands absolutely no chance
Rending the hide of a rhinoceros with its serrated teeth
Avenging the death of mate by tracking the paladin slayer
Roaring proudly as it writhes atop a defeated dragon
Basking uncomfortably atop a toppled statue of an elephant
Rumored to keep a cache of holy texts hidden among its hoard
Bellowing loudly to assert a territory from other predators
Scowling at a flight of sprites, buzzing around a head
Bickering amongst itself, two heads ganging up on a third
Scratching scaly necks by encircling tree trunks
Biting at mineral rich clumps of soil, sullen mouthfuls
Seizing an ogre by the leg and shaking it around like a rag doll
Burrowing beneath a terrified treant
Settling a dispute among heads with a decisive self-decapitation
Chasing after a group of bandits who invaded her den
Slavering over the shell of an enormous turtle
Coiling around a warm iron pillar, miraculously free of rust
Snapping at a murder of daredevil crows, drawn to its deer kill
Concealing all heads but one under water
Stalking a nearby tribe of centaurs
Crawling laboriously along muddy banks
Stockpiling a dead sheep for a future snack
Defending their lair from a tenacious stone giant
Struggling to swallow a fully armored acolyte
Deforesting large swaths of wilderness, creating a barren plain
Swallowing sacks of coins - aiding digestion, many gizzards to fill
Devouring an elf, each head squabbling over chunks of meat
Tangled intentionally disguising the number of heads it possesses
Dragging itself out of a dank burrow to hunt
Tasting air with forked tongues, baleful eyes staring all directions
Easily decimating a platoon of hobgoblin soldiers
Tearing apart a warhorse, cleric rider unconscious nearby
Eating a dead (and crunchy) basilisk
Terrorizing a dwarf delve, now recruiting brave or foolish souls
Eliminating an elf knight sent to slay him
Throbbing/pulsating after swallowing too many magic wands
Fascinated by nixies, who keep it fed with giant bass
Twisting to avoid a giant spear, hurled from afar
Finishing off a drowsy grizzly bear that wandered into its cave
Tyrannizing its troglodyte subjects - feeding on strongest warriors
Flinging a fighter several feet, he lands with a dull thud
Unsettling even a vampire, looking for a champion to slay it
Fortifying lair by lining it with irritating brambles and nettles
Uprooting every dryad tree it comes across
Frustrated by lizard men archers, who snipe from a distance
Vacating den after accidentally opening a mummy's sarcophagus
Gnashing mouths defiantly as he squares up against a wyvern
Was once enslaved as a war machine and especially wary of men
Gnawing at the enchanted chains that bind them to this cave
Weaving with surprising grace through trees, following a scent
Growling heard for miles, all birds take wing and fly away
Winning a battle with an ill-prepared adventuring party
Gulping down a kobold, left as tribute by the tribe
Worrying a monastery by drawing closer with each passing year
Hissing a warning to a giant crocodile
Wresting arm from an orc with head, while another grabs a leg
Hoarding captured mediums in an anti-magic den
Yawning with half of its heads and turning towards its lair

Table: insect swarm, creeping
Absconding with a bejeweled dagger on their backs
Persistently surging forth from a sack of moldering grain
Bustling busily around the base of a basilisk statue
Pulsating abdomens leave a trail of stinking ichor
Clustering atop the carapace of a cave locust
Quizzically forming "arrow" shapes on the ground
Condensing into a massive dark blot
Raiding a roost of bats, unsatisfied with their guano
Crawling on the ceiling in a chittering clot
Returning seasonally to pester a cursed acolyte
Devouring an unlucky veteran, flesh to bones in mere minutes
Scavenging a hearty meal among hurried halfling tracks
Dripping off a wall in furiously clinging chunks
Seething as a torch waving shield bearer keeps them at bay
Emerging from a huge, conical hive of uniform gravel
Streaming from the eyes of a single elf skull
Flourishing on a farmer's fresh vegetables
Surrounding a twitching caecilla
Flowing from the belly of a bloated zombie
Thickening into arcane sigils in the presence of magic
Following the commands of a kobold shaman
Threatening to chew right through a locked wooden door
Hanging tenaciously on a braying mule's flanks
Thriving on offerings in tin bowls, left by faithful gnolls
Mingling in a chilly stupor after an icy spell
Utterly covering a flailing carcass crawler
Noisily droning as they consume a skeleton
Worming their way into a dwarf's mail hauberk
Overwhelming an orc gathering, seen as an auspicious omen
Writhing atop a monstrously large mushroom cap

Table: insect swarm, flying
Alighting on a tree, their weight causing twigs to snap
Humming menacingly in response to a sudden sound
Buzzing cacophonously, the sound filling all ears
Migrating in search of food, after stripping an area bare
Changing direction suddenly, as if by some command
Milling about, somewhat stunned by fading smoke
Chewing their way through the hide of a horse
Nesting inside a water-logged armoire
Circling a pool, where a gnome holds her breath
Plaguing a paladin, fallen from grace
Clouding the air in a dark, undulating mass
Pouring out of a surprisingly tiny crack
Colonizing the carcass of a cave bear
Resonating loudly as the throng competes for mates
Damaging fruit trees with their rapacious appetite
Settling on a shield, polished to a shine, to dull its glow
Darning the air in intricate, synchronized patterns
Stinging a frantic giant toad
Descending on a bandit's roasting boar
Stripping every stalk of plant life in their path
Devastating the food supplies of a dervish
Surrounding a stone sarcophagus, as if drawn to it
Drifting on a stiff breeze, toward a settlement
Swirling in a vociferous vortex, blocking an archway
Fluttering around a flickering torch
Swooping down to drink in stinking, wet mud
Gorging on a goblin garbage pit
Unceasingly hungering among bare tree branches
Hovering near a hollow log, where a magic user hides
Whirling around a decaying wyvern

Table: insect swarm, creeping and flying
Aggressively marching over anything in their way
Issuing forth from the mouth of a wight
Burrowing into a motionless mummy
Jostling for prime dining position on a giant rat
Carrying away a dead deer
Menacing a cornered fire beetle
Chattering as they pulverize old bone in their mandibles
Nibbling on the toes of a sleeping thoul
Cleaning every trace of detritus from the floor
Overturning furniture as they swell across a room
Clinging doggedly to a dangling rope
Passing beneath a sizzling green slime
Crowding on a conjurer's corpse
Pursuing only those of a particular faith
Darting out from beneath a rotting rhagodessa
Relentlessly surging from a crack above
Filling a desecrated font, beating like a heart
Scattering after a flask of oil ignites
Forcing hobgoblin hunters into organized retreat
Settling on the surface of a massive stone face
Gathering in the charnel wake of a pack of ghouls
Staining everywhere they land with a noxious odor
Gnawing through the cushions on a chair
Stridulating wildly at a volume that is maddening
Growing and swelling in size before your very eyes
Teeming on the flailing body of a giant snake
Huddling atop an abandoned harpy nest
Thronging around a druid with faceted eyes
Invading an entire area, apart from a circle lined with runes
Whistling a warning in call-and-response fashion to their flock

Table: invisible stalker
Alembics clink as a vial of sizzling venom pours itself
Escorting an expedition to a planar portal
Alongside impatient tapping, an hourglass upends itself
Examining a contract carefully for crucial exploits
Belt pouch slit, a merchant's coin spills and rolls all over
Fetching a dented, copper oil lamp of little apparent value
Bent over in agony, a halfling clutches their stomach
Flushing out rats, a menial task beneath their station
Bloody stab-wounds appear on a medium's robes
Following inquisitively behind a rust monster
Candles sequentially snuffing with a sizzle to hide shadows
Fulfilling a wizard's request to steal all spell books
Crooked mirror, fogs slightly as it straightens itself
Grousing at having to undertake another banal burglary
Curtains parting without any sign of breeze
Guarding a chest instead of its contents (long since emptied)
Floating jeweled crown, disappears from view
Heaving up a heavy portcullis with a humongous racket
Foreboding footfalls suddenly cease, only to increase in pace
Hunting down one of their own kind per an oracle's orders
Grindstone turns with a rasping sound, sparks fly but no knife
Inciting an argument between two ghouls by stealing a bone
Have you ever seen a potion drink itself?
Jostling their way through a perplexed crowd of kobolds
Iron fetters spark with loud strikes, a gnome is freed
Knocking on surfaces randomly to pass the time
Leaves and detritus seem to eddy and whirl, sweeping
Lurking in a darkened room, gossiping with shadows
Loud clang as a dwarf's helm falls and they slump to the ground
Nabbing an orc child, destined to unite the tribes
Mule's mane, standing on end as they whicker nervously
Only taking these contracts to support an extraplanar family
Open tome titled "famous assassinations," a page turns
Opening a noisy door, haltingly for maximum tension
Pale ash footprints, appearing in sequence across the floor
Perfumed redolently in only the finest colognes, fit for kings
Pillow pressed to the face of a sleeping paladin
Perverting instructions by draining a wand they were sent to steal
Quill crossing off a list of names, drops suddenly
Pilfering a golem crafters notebook and life's work
Rapid puffs completely extinguish four candles on a candelabra
Playing with their prey by leaving black roses at the scene
Sentient sword screams telepathically as it's being stolen
Plunging a knife into a noisy, snitching shrieker
Strangling himself, a jewel thief struggles
Poisoning a pit fighter to rig a match
Suddenly tripping, a veteran fumbles with her blade
Protecting pilgrims on their long and arduous journey
Thin red line, appearing across the neck of an illusionist
Prowling a crypt to guard an ornate sarcophagus
Twisting with a sickening crack - an acolyte's neck
Pursuing the pixies that threw pink paint on them as a prank
Very strange how a pile of coins is stacking itself
Reeking of blood and sweat hounded by a cloud of mosquitos
Was that hot breath on the back of your neck?
Refusing to murder innocents, desperate for a technicality
With a twang, an elf's bowstring snaps
Remaining precisely where they promised as their caller dies
Hackles raised, a tabby cat hisses and spits
Retrieving a priceless painting of a pegasus from a medusa
Alarming a swarm of bats, unable to fool their echolocation
Returning a relic to a lizard man shaman
Ambushing a pack of gnolls standing between it and its prize
Secreting stolen jewelry on an unsuspecting adventurer
Announcing the name of their summoner before slaying
Securing the perimeter around a pregnant prophetess
Assassinating a truculent noble, to deal with a land dispute
Seeking someone that can be seen to convey a message
Baffling bugbears, by systematically thinning their ranks
Seizing sprites and sealing them in glass jars
Biding its time as its master dies of old age nearby
Slamming shut a strongbox in frustration
Blinking briefly into amorphous form as it crosses a circle
Slipping on a slick of spilt lamp oil
Burgling a goblin king's crown to fulfill a poorly worded task
Smelling distinctively of lilacs and oiled leather
Catching up with their quarry - a troublesome druid
Snapping their fingers cheerfully to even the odds
Chasing down the owner of the ring that holds them here
Sneaking a swig of incredibly potent spirits, wants to share
Climbing down a well to rescue a familiar
Stifling excited laughter as they locate a loophole
Collecting inscrutable payments in song from a sorcerer
Toying with their quarry - an overconfident doppelgänger
Creeping along a corridor, disturbing cobwebs
Tracking a unicorn, half-heartedly
Crouching low to kneecap a passing neophyte
Trapping a special kind of centipede to extract their venom
Cursing in neutral as they step on a noisy twig
Untightening straps on a nervous warhorse's saddle
Darting across a wet floor, puddles splashing softly
Waiting impatiently, for a missive from their master
Discovering their werebat quarry can see them, and fleeing
Watching from within an "empty" suit of armor
Dispatching an orc guardsman with silent precision
Wielding a sentient blade that grants only regrets
Drowning a delinquent debtor
Wincing as they inadvertently knock over a clay jug
Escaping a heat-sensing golem's grasp
Working with the beggar's guild, who sell charms of protection

Table: killer bee
Aggressively thrumming at a passing minotaur
Hunting goblins who unwisely decided to raid their hive
Alighting on an enormous azalea
Infesting an abandoned temple
Assaulting a rival hive, dead bees abound
Injecting an intruding, welt-covered ogre
Avoiding a pool of giant toads after losing several drones
Intruding on an acolyte's ablutions
Banishing a former king, outlived his usefulness
Joyously dancing to announce a brobdingnagian blossom
Bearing black and yellow garbed, lance-wielding pixies
Keeping their queen safe from a hungry crab spider
Befriending a colossal oleander treant
Kneading wax to warm it for repairs
Bewildered by a cherry dryad's bouquet, blundering boozily
Landing clumsily on a startled lizard man
Blotting out the light with their swarming
Loaded down with slumber inducing pollen
Building their huge hexagon hive in an ancient amphitheatre
Locating a troglodyte trespasser by smell
Bumbling into buckler-sized buttercups
Marauding among massive marigolds
Burning up an intrusive giant hornet with their body heat
Mercilessly culling a venerable queen
Buzzing cacophonously, it rings in ears for hours
Mining armfuls of pebbles and dirt to dig a deeper hive cave
Carrying sneeze-inducing pollen on their hairy knees
Nesting down an abandoned well after kicking out a troll
Chasing an embarrassed cave bear away from their hive
Noisily bombinating to greet returning scouts
Circling a field of cyclopean sunflowers
Overturning logs to lap at moist soil
Climbing a wizard's tower with a gaudily painted roof
Overwhelming a band of brigands, selecting a campsite
Clustering around a returned scout, to watch their dance
Partaking in a puddle of spilled plonk, intoxicated and clumsy
Collecting moisture/morning dew to drink later
Perching precariously on a pear tree
Congregating within a honey-dripping dragon skull
Plundering lily pads while helpless nixies watch
Constructing their hive in a hibernating owl bear's cave
Plunging their stings futilely into an oblivious skeleton
Crawling along the ground, exhausted from lengthy flight
Pollinating a breathtaking bloom, opens only every century
Darting after a terrified dwarf
Producing a peculiar product - their honey removes curses
Defending their hive from an intrusive alchemist
Protecting an ancient stone circle, spiral hexagon glyphs
Discovering a field of giant dandelions
Pulping plant matter to make a sought-after paper for scrolls
Divebombing a bugbear who was trying to be stealthy
Putting the final touches on a pixie bower
Domesticated somewhat by local gnome apiarists
Questing far and wide for flowers of sufficient size
Droning contentedly with nectar filled bellies
Racing after a rhagodessa that raided their eggs
Emerging from a hollow in a monstrously large log
Repairing hive damage, caused by a clumsy hill giant
Encrusting the exterior of their hive with shiny stones/gold
Rubbing their fuzzy faces to shed brilliant yellow pollen
Entombing an inert golem in wax
Sacrificing themselves to drive away white apes
Excavating a new entrance burrow into an abandoned barn
Searching for a suitable site for their swarm to sleep
Executing a member of the colony, corrupted by cordyceps
Stinging a bucking centaur stallion
Extracting nectar from elephantine honey suckle
Straying far from home in search of wraith-blossoms
Fanning their wings to thermoregulate
Struggling in a black widow spider's web
Feeding valuable royal jelly to larva, coronation soon
Stumbling into a satyr celebration
Fiercely clinging to stalactites/tree trunks on watch
Supplying sweeteners for clever, smoke bearing confectioners
Flitting to and fro among unforgettably big forget-me-nots
Swarming on a hobgoblin siege engine
Flying high in formation, on kamikaze missions
Tasting each of several tulips in succession
Foraging dangerously close to an immense venus fly trap
Thriving near an ancient green glass house, built by elfs
Frequenting a halfling village green, combing the clover
Toiling tirelessly, tessellating six-sided egg chambers
Gathering glaucous bloom from melon sized plums
Transporting secret messages between forbidden lovers
Guarding the bard that somehow charmed them with dance
Travelling to a werebear's carefully cultivated garden
Hanging heavily from blossom filled apple branches
Troubling a trader, specializing in sweets
Harvesting nectar from nelumbo, while a huge gar watches
Understanding the elf tongue, thanks to a magical mishap
Hatching warrior larva, to be fed solely on blood honey
Venturing underground, addicted to a strange glowing fungus
Hoarding yellow mould pollen in their knee sacs
Visiting a vast purple plain of violets
Homing in on a huge field of heather
Working day and night on a citadel shaped wax palace
Hovering patiently around their hive's entrance
Worrying a warrior, furiously waving his torch
Humming with energy, eager to follow queen's commands
Zooming greedily among fragrant zinnias

Table: kobold
Adjusting a precariously balanced floor-beam
Kobold soccer uses a gnome head, gnome soccer - just as bad
Aiming automatic arrows by test-firing at a wall
Laundry day - boiling clothes in giant vats
Allied with new-comer lizard men, for now
Leading a sneak of leashed giant weasels on patrol
Applying camouflaging pigments to their skin
Led by an elder who survived the mummification process
Baiting a basilisk trap with exotic minerals
Lifting a large boulder into place above a door
Barking orders to the less-clever kobolds
Lurking in alcoves, their seer suspects visitors soon
Baying soft songs of love to their partners
Mapping a lower level of a dungeon from memory
Breeding giant scorpions as mounts and pack animals
Milking a drugged caecilia, a disgusting process
Bushwhacking some unsuspecting orcs
Moonlighting as merchants for demi-humans of the deep
Capturing giant centipedes for children to play with
Overseeing construction of a pit-trap
Checking snares set last week
Peering through a perfectly camouflaged peephole
Chirping an "all's well" to nearby guards
Planning a surface raid meticulously
Choking on yellow mould spores
Preparing a feast of mule meat to celebrate success
Coiling lengths of rope to set the tension of a trap
Reapplying poison to doorknob needles
Concealing a ceiling net with stuffed bats
Recent attacks from a shadow have them all nervous
Cultivating a form of shrieker that only they can hear
Resetting a spring-loaded oil-flinger
Cursed by sprites and can no longer tell lies
Retelling myths about their ancient enmity
Daydreaming of a world without gnomes
Retrieving treasure from a spike pit
Decorating decoys to make their numbers look larger
Roasting a well-seasoned cave locust
Defending nesting area from an ovivorous giant snake
Rolling large barrels of lamp oil along
Delivering "protection money" to a local orc chieftain
Saddling up their giant bat mounts for a scouting mission
Diagramming convoluted family trees
Skulking into position to ambush a bugbear
Digging a new warren into a wall
Snapping shut the jaws of a steel trap with a spear
Disguising an obviously false flagstone
Snarling at a chef for serving rat-on-a-stick again
Dislodging a jam in a crossbow mechanism
Sniveling for mercy at the foot of a minotaur
Domesticating oil beetles as a front-line defense
Snorting at a joke about the stupidity of gnomes
Donning elaborate head-dresses for a merging of tribes
Spreading rumors about a gnoll chief's gnomish blood
Dumping out jars of very angry scorpions
Squeaking with delight as a test fire of a trap goes off
Eating crunchy dried cave newts
Steadily building an immunity to carcass crawler venom
Encouraging a gelatinous cube down a dirty hallway
Stealing prized grapevines from a cyclops
Enjoying their bond with a lesser djinni
Stringing a tripwire, guillotine warning system
Feeding a friendly crab spider with a dead robber fly
Stuffing a taxidermized manticore with straw
Fishing out severed fingers from a clever chest trap
Surprising a medium by displaying minor magics
Friendly with a fire giant - rid her home of giant rats
Swindling a troll, trading tons of cp for fewer gp
Gambling on a fight between rats
Tending to a gnome flavored variety of mushroom
Getting the drop on a group of gnome delegates
Territorial turf war with neanderthals
Gingerly placing eggs near a fire to influence the sex
Testing the action of a volley of poisoned darts
Goading a rust monster into a wooden cage
Tiring of their weekly tribute to a greedy red dragon
Growling as they discover a trap was sprung, but empty
Torturing a trespassing thoul
Harvesting poison from domesticated black widows
Training bats to attack when a bone whistle is blown
Hauling bundles of javelins to an armory
Tripping an ogre with coordinated rope-work
Hiding their share of treasure from the boss
Turning a wall-mounted wheel to open a trapdoor
Hoarding foodstuffs to prepare for predicted lean times
Tying knots that loosen, every other rung of a rope ladder
Howling with laughter as one gets stuck in a snare
Under the thumb of a local hobgoblin king
Infected with a rare form of lycanthrope - were-bats
Wagging stubby tails as they dig into gnome gumbo
Inspecting a trick-staircase
Waylaying a troglodyte hunting party
Interrogating a suspected gnomish spy
Whining to a superior about long shifts
Itching uncontrollably during their monthly molt
Winding rusty gears for a complex booby trap
Knitting ghillie suits, suitable for dungeon terrain
Worshipping an itinerant flame salamander as a god
Know the secrets of making kobold sized living statues
Yapping a warning cry to their were-wyvern leader

Table: leech, giant
Alarming merchants after being discovered on their mule
Meandering clumsily, intumescent from a recent meal
Ambushing prey in a knee-high flooded plain
Moving lethargically due to chilly weather
Anesthetizing an inattentive troglodyte
Nauseating a novice, distracted by smaller cousins
Arching their bulbous body as they lope along
Noisily slurping as it seeks warm victims
Attaching their greedy mouthparts to a marsh goat
Numbing a moose, munching on lily pads in deep water
Bidding its time, half-buried in the sand near fresh water
Nuzzling their bayou druid master
Bleeding a dead goblin dry
On the hunt and hungry, swimming surprisingly fast
Bloating to a prodigious size after gorging on a deer
Overindulging, attached to a bog giant's ankle
Burrowing into moist leaf litter to stay damp
Plumping up on the blood of a swamp-bound sea serpent
Camouflaging itself among muddy mangrove roots
Probing the mud and muck, tasting racoon tracks
Carrying parasites that cause bog boils in its saliva
Pulling itself out of an old muskrat burrow
Clinging to the leg of a cleric
Pulsating as it sups on troll blood
Coiling around cocooned young
Quivering as it feeds on the flanks of a stegosaurus
Constricting the hind quarters of a catoblepa
Rapidly fastening around the foreleg of a fawn
Crawling along a massive mossy log
Reaching for the feathered belly of a dire crane
Dangling disgustingly from an ogre's haunches
Recoiling with disgust after sampling a ghoul
Detaching from a dead giant toad
Reeking of gore after feasting on a giant ferret
Distending as they fill with bugbear blood
Refusing to unlatch from a veteran's leg
Dragging themselves across a dry patch, seeking shade
Regurgitating cruor in blackened, jagged chunks
Draining a sleeping draco lizard
Roaming far and wide thanks to ancient irrigation canals
Drawn to the warmth of a thermal spring
Rummaging near the entrance of a warp beast den
Dropping out of mossy tree branches onto prey
Rustling leaves and detritus to find a damp place to rest
Engorging on a warhorse, stuck in thick black mire
Savoring a swamp panther supper
Escaping from an alchemist, interested in their secretions
Secreting saliva with pacificating properties
Exploring an abandoned camp site noisily
Seeking a mate, trailing pheromone-laden slime behind
Exsanguinating an explorer
Shrilly screaming as a startling defense mechanism
Falling into the muck after a rotten trunk snaps from weight
Shunning a bright, searing light
Fattening on a giant catfish
Slackening their grip on a gnoll after a being burnt
Feeling its way around blindly with its puckering mouth
Slithering from a muddy hole beneath an antediluvian dolmen
Glistening with slimy secretions
Slowly worming up to a high perch to get the drop on lunch
Gorging on a bellowing gorgon
Sought by a hill giant healer for bloodletting
Grabbing onto an alligator, having a hard time with the scales
Squirming into the gills of a giant gar
Greedily extracting every last drop of blood from a bandit
Starving and desperate due to a lack of prey
Growing plump on a dead poacher's blood
Stretching to a spear length as it shimmies up a tree
Hanging from the haunches of a black bear
Struggling to move its well-fed, turgid segments
Hiding near the banks of a promising ford
Stubbornly lurching along the edge of a pond
Hitching a ride on a triceratops belly
Sucking stubbornly on the leg of a living statue
Hobbling a horse crossing a creek
Surprisingly graceful as it glides through the water
Holding fast to the underside of a smuggler's raft
Swelling as it shrivels a hobgoblin bodyguard
Inching laboriously across marsh grass
Terrifying tales proceed them in these parts
Infesting a flooded fishing cabin
Thrashing uncontrollably, being stung by inferno ants
Investigating an abandoned boot, mired in the mud
Throbbing on the rump of a swamp rhino
Jerking away from a driver ant's bite
Twitching as it touches some swinging swamp nettles
Kept as pets and emergency meals by a local vampire
Unbalancing a dwarf, regretting his weekly washing
Landing on the back of a brigand from above
Unclasping from the shriveled body of a beaver
Languishing, marooned in a tiny puddle after a drought
Wallowing in hot mud, occasional belching bubble
Laying yolkless eggs at the base of a cypress dryad's tree
Well-fed by kobold worm-tenders
Liberally feeding on an oblivious lizard man
Wetly gurgling and blowing slimy, scarlet tinted bubbles
Looping for locomotion, comical and revolting simultaneously
Wriggling its way into an unattended sleeping bag
Lounging atop a mushroom covered log
Writhing as it tries to latch onto a wolf

Table: living statue, crystal
Able to concentrate light into focused beams igniting cloth/paper
Hypnotizingly beautiful, a group of kobolds stand enraptured
Armed with a spell reflecting faceted shield
Judging a dispute between a dwarf and an earth elemental
Bending light when viewed directly, causing headaches
Obsessively collecting jewelry and gemstones, all that glitters
Bowing as if in prayer beside an urn-holding alcove
Opalescent and lit by an internal diffracting flame
Brightly gleaming, surrounded by torches of multicolored flame
Perched upon a rose marble dais, perfectly motionless
Calmly filling a jug of water from a cistern
Projecting prismatic rainbows as light sources shine upon them
Composed of jagged, milky prisms - change color based on mood
Repairing themselves with a pouch of colored sand
Deciphering a slab of ancient pictograms
Serving as a guardian for a sacred relic of law
Difficult to stare at directly, refracting light into limpid shards
Sighing as they clasp a cut ruby rose to their breast
Dispensing unreliable prophesies to visitors for a modest fee
Singing hymns in a high-pitched but hollow voice
Emerging from a mineral rich pool, encrusted with accretions
Supporting a crumbling ceiling while gnomes escape
Faintly glinting under a thick covering of centuries of dust
Tending to their bed-ridden creator, not long for this world
Fashioned from translucent blue stone, cool to the touch
Their shimmering two-handed sword cuts iron like butter
Fretting over a missing gem from the hilt of an ornate sword
Tinkling pleasantly as they glide about on patrol
Giggling like the sound of tinkling bells, admiring a carving
Venerated by local acolytes as an avatar of their faith

Table: living statue, iron
Battering a berserker with his own battle-axe blade
Imprisoning a paladin in their own plate armor
Brandishing sickle-like grasping claws
Leaping across a chasm with a resonant clang
Burnishing bits of rust from the soles of their feet
Loud rasping sounds accompany even the most minor movement
Deforming a flail strike, while a hobgoblin watches in horror
Pounding steel into paper thin sheets for inscription
Demolishing inferior stone statues with powerful fists
Rankled by a steady drip from the ceiling
Dragging a cast iron cauldron, melded to their foot
Roaring like a blast furnace as they battle a manticore
Festooned with the hilts of over a dozen swords
Slicing through spider's webbing with wicked shear-like hands
Forging a blade with a hammer hand, on an anvil knee
Snapping off spear shafts stuck in their torso
Fusing an iron door shut with a touch
Somehow under the sway of a lizard man shaman
Gouging large furrows in the floor, dragging a massive blade
Splintering animate skeletons easily with powerful blows
Guarding the family crypt of a long-dead alchemist
Steadily lurching back to their post after driving away a thief
Guffawing as they absorb a bugbear's blade
Swinging one of the several massive iron chains draped on them
Held at bay by a ravenous rust monster
Using grappling hook hands to climb a wall
Honing huge knuckle-spikes to a sharp point
Wavering under the influence of a medium's charm spell
Idolized by a local goblin tribe who leave offerings of scrap
Welding their palm to the metal shield of a cleric

Table: living statue, rock
Allied with a flame salamander blackguard
Incinerating the remains of a troll that wandered too close
Blending among several defaced and broken sculptures
Intoning stern warnings in their creator's voice
Burning a pyre of books/scrolls that belonged to their creator
Looming in an archway taunting anyone it sees
Cachinnating with small gouts of flame and steam
Melting a metal helmet to molten slag
Chasing away a curious grey ooze
Protecting a cultist bearing a special amulet
Closely resembling a gargoyle at first glance
Receiving offerings from a tribe of troglodytes
Compelled to stay within fifty paces of a strange obelisk
Reforming a damaged hand with a grimace
Crushing coins into lumpy alloyed ingots
Scraping at a sealed secret door, unable to open it
Dripping magma from open wounds that sizzles on the floor
Shooting scalding globs at an enraged minotaur
Examining humanoid tracks in their territory
Shuddering from a mighty blow from an ogre's club
Fabricating identical simulacra out of thin hollow layers of obsidian
Spraying a steady stream from fingers to seal a doorway with stone
Glowering as it keeps repeating a request for a passphrase
Terrorizing a clan of pacifist ghouls
Hissing and groaning as anger increases its inner heat
Tidying up a chamber after a messy battle with bandits
Igniting a rope ladder, left by a fleeing tomb raider
Wading through a magical pool, generating a great deal of steam
Illuminating the room with a pulsating orange glow
White-hot cracks ripple and close under a blackened crust

Table: lizard man
Arguing about how best to butcher a terrified elf
Making catoblepa cheese
Assisting each other in removing pesky ticks/leeches
Marinating prey in pits of brackish water
Attempting to feed a farmer to giant piranha
Mending barbed nets, spiny branches nearby
Barehandedly breaking driftwood for a campfire
Molting, covered in irritating translucent sheds
Being berated by a stronger and larger female
Nearly shooting each other as they experiment with a crossbow
Bewitched by nixies, seeking beauty to bring back to them
Panicking as one of their number sinks into mud
Binding birch bark books at their leader's behest
Playing "catch" with an annoyed constrictor snake
Blissfully unable to smell the skunk stench that coats them
Plucking a heron, and saving choice feathers for fletching
Carefully pouring grey ooze into thin stone amphorae
Pouring salt on a giant leech
Carving very artful and terrifying wooden totems
Preparing an ambush by overturning a small boat
Checking the temperature of chicory tea with their tongues
Pungently burning the stringy hair off a severed humanoid leg
Cheerfully discussing an upcoming sporting event
Raking drying bog-berries into reed baskets
Chewing sullenly on bundles of succulent leaves
Reciting mighty deeds in turn to one-up each other
Chortling at the tail-loss of an unlucky fellow
Re-tooling a suit of un-rusted chain for their anatomy
Coating spear-tips in a black, viscous, tar-like substance
Ritual bog-mummification of a dead matriarch
Competitively extending/retracting dewlaps
Ritually breaking javelins that missed their mark
Constructing a short fence from supple green wood
Roasting an arm-length catfish on a spit
Consuming shed skin for vital nutrients
Rooted in place with vines by an angry cypress dryad
Cooling a nest to influence hatchling gender
Salivating over a stew pot, water dancing with fingers
Deferring to a leader with a large horn on his snout
Sawing a tree-trunk into more manageable chunks
Delivering a message on behalf of a nearby sacred medusa
Scraping clean an antique iron cauldron with sand
Demonstrating strength via tail wrestling
Scratching a territorial marker for all to see
Destroying the nest of a rival tribe
Seeking aid and muscle to help stop recent bugbear raids
Digging a hole that's rapidly filling with water
Setting strangely shiny spearheads on shafts
Discharging cakey salt from lacrimal glands
Shoving clumps of moss into a gaping, oozing wound
Dividing up egg spoils from nest raiding
Shucking fresh-water mollusks, a pile of bivalve shells nearby
Donning hooded cloaks for a trip to a nearby town
Skewering plump bats for shish kebab
Drawing up plans for a massive ziggurat
Skimming and saving the sludge off boiling water
Drilling bead holes into quahog/cockle shells
Slightly sluggish due to cooler temperatures
Drying elf-beard moss over woodsmoke
Snapping at a helpless halfling, hanging from a height
Even without speaking lizard man - the fish story is apparent
Sneezing after exposure to a noisome weed
Extracting ink from water termites made docile with smoke
Squeezing bloated toads into ornate crockery
Fleeing from an enraged giant shrew
Staining their frill scales bright colors
Frantically searching for a chirping child
Standing stock still to avoid a deadly motion sensing serpent
Gambling, the stakes appear to be a human hand
Strategically removing scales (as tattoos) for a secret society
Gleefully tearing the pages from a mildewed spell book
Stringing impressive teeth collections on twine
Gnawing on five-toed and furry feet
Successfully grafting a giant crab claw onto an arm stump
Grousing from stomach aches due to recently eaten troll
Surprisingly solemn coming-of-age ceremony
Grunting as they pick stringy dwarf meat out of teeth
Taking turns basking near a warm fire
Gutting a huge gator and tanning the leather
Taunting a giant toad with a captured cave locust
Heaping offerings in front of a sculpture of a dragon
Teaching the young the best way to catch crayfish
Hiss-chanting prayers at a carving of the sun
Testing club-wood with loud, snapping, bites
Honing claws on special rough stones
Tossing scraps to trained dimetrodons
Inspecting last season's rotting logs for cultivated mushrooms
Toying with a disarmed berserker
Insisting a newly hollowed blowgun is true and straight
Transporting tribute to a stronger tribe
Intently watching a shaman cast bones
Trussing a gnome with a swamp apple in his mouth
Laying out strips of fish to dry
Tying several dead racoons/opossums on a line for transport
Lazily patting distended bellies
Unblinkingly watching ingenious fishing line floats
Leaping contest
Unsuccessfully trying on a captured helmet
Listening raptly to a captured bard play a flute
Weaving sleeping mats from long blades of grass

Table: lizard, giant (draco)
Arching their spiny back, preparing to leap
Hurling themselves with abandon away from a hungry tiger
Basking on a massive tree branch in dappled shade
Lapping up sticky sap from an oozing gouge in the bark
Chasing after a frantic driver ant
Laying a uniform row of large, lozenge-shaped eggs
Chomping through a nest of bird eggs in a matter of moments
Lunging half-heartedly at a giant dragonfly
Clambering down the side of an old wall
Plunging from incredible heights, taking wing at the last minute
Crawling clumsily across the ground, scanning for prey
Scaling rough rocks, to find a spot to sleep
Devouring large, sickly smelling, messy green fruit
Scampering up the trunk of an enormous oak tree
Extending the colorful frills around their necks
Seizing a dire squirrel and swallowing it in a few fast gulps
Fleeing from a slithering rock python
Soaring serenely overhead, towards another perch
Gliding toward a crumbling cliff side
Unfurling their colorful dewlap to impress a potential mate

Table: lizard, giant (gecko)
Adhering firmly to a faded fresco of forgotten gods
Licking their eyes to keep them clean and moist
Chirping with loud throaty bursts
Molting and covered with translucent shreds of skin
Clinging contentedly to a ceiling to digest their last meal
Opening their mouth widely to intimidate a rival
Crunching on a cave locust loudly
Quickly climbing up a smooth wall, envy of any thief
Darting out from a hiding place to snatch a crab spider
Retreating through a wide crack from a hungry orc
Drinking from a steady drip, saturating the wall
Sacrificing a shed tail to a hungry giant shrew
Dropping onto a startled rust monster
Sticking to a still warm brick chimney
Flashing their tongue in a threat display
Suddenly springing upon a giant bat
Glowing subtly, thanks to a diet of special fungi
Warming up near an iron grate, bellowing steam
Hanging, mostly hidden, on the underside of a table
Ambushing a tasty gnome who was distracted by shriekers

Table: lizard, giant (horned chameleon)
Blending thoroughly among the verdant leaves
Lounging atop a large statue of a gargoyle
Clutching a thick bough with knobby, offset fingers
Mimicking rather drab surroundings perfectly
Dangling from their prehensile tail to descend carefully
Nimbly flinging their tongue to snare a bird/bat
Dazzling their prey with rapid color changes
Sauntering confidently towards a giant rat
Ensnaring a robber fly with a lightning fast flick
Surprising a lizard man, nearly knocking them over
Glaring int two directions at once
Swaying rhythmically as they navigate a precarious limb
Gobbling down an unlucky tiger beetle
Tripping a trapper with a well-timed tail-swipe
Gripping their way across a mostly demolished bridge
Turning as black as anthracite and glowering
Head-bobbing to a completely camouflaged rival
Waylaying a clattering carcass crawler
Launching their sticky tongue at an unsuspecting kobold
Yawning defiantly, pink mouth betraying its position

Table: lizard, giant (tuatara)
Biting a bombardier beetle clean in half
Impossibly old - hatched in a time before elfs
Burying a clutch of eggs in a sandy depression
Revered as a deity by a local troglodyte tribe
Circumducting atop a large sandstone megalith
Mistaken for a dragon by local yokels
Clamping down on a colossal dire weta
Munching on fire beetle, glowing globs dripping down chin
Widening a purloined blink dog burrow
Rolling a boulder over to sup on caecilia larvae
Draping themselves on a toppled, sun-warmed obelisk
Scuttling with speed over a scree of sun-bleached snail shells
Driving away a party of bandits, self-satisfied
Seeking warmth, irritable and somewhat sluggish
Fattening up on a giant toad
Sipping from a magical spring, grants the power of speech
Gouging a group of goblins who wandered too near
Sunning themselves, half-heartedly snapping at stirges
Hissing loudly at an embarrassed grizzly bear
Attacking a caravan of halflings, seeking greener pastures

Table: manticore
Admiring their assortment of stained silk scarves
Leaping with glee into a fracas between orcs and brigands
Alighting upon a barren craggy clifftop
Leisurely trailing a severely wounded warrior
Amassing a pile of heretical texts for bedding
Licking gore from their wicked claws daintily
Ambushing a group of exploring nomads
Marring a marble plinth with gouged graffiti
Avoiding nearby stone giants after a battle ended badly
Menacing the chief trade routes that feed a metropolis
Basking in adulation from goblin cultists
Messily gorging on a dead rival
Befouling the only fresh water source for miles around
Moaning from over-eating mammoth meat
Bellyaching and complaining to itself as it walks
Mutilating masterpiece portraits as they add them to their hoard
Bombarding a troop of rock baboons with spines
Negotiating for a spot on their dastardly council
Bounding after an antelope buck
Objurgating a captured priest to tears
Brutally flinging the hobgoblin sent to bargain with him
Panicking a half-dozen boar hunters
Caching a camel kill up a tree for later
Panting proudly, couchant as in heraldry
Chewing on the glowing tip of an ornate staff
Peppering a paladin's tethered mount with spines
Circling a dervish encampment subtly
Periodically bellowing complaints to mark the time
Clawing large gouges into the tombstone of a saint
Pinning stolen medals and accolades to their matted chest fur
Collecting bent and broken holy symbols
Plundering the treasury of an ogre chieftain
Creeping low in the brush, to spring on a crocodile
Poisoning the soil around a dryad's tree
Crunching on the shell of a giant crab
Pouncing on a majestic pegasus, landing to drink from a lake
Defacing a statue, memorializing a monarch
Preening an expensive wig atop a wax effigy of a famous actress
Defending their den from an angry cave bear
Querulously yielding their lair to a hydra
Defiling a scenic glade with piled bones and corpses
Quietly rummaging in a sleeping hill giant's sack
Devouring a defeated dwarf, beard and all
Rapidly despoiling the surrounding area of all plant life
Dilapidating a once beautiful manor house
Ruining a politician's chances of re-election with written smears
Dining exclusively on fear, with a full belly
Scavenging on the fly-infested remains of a dead ox
Dogfighting with an exasperated griffon
Scourging a goblin scout with their tail
Dragging a mauled brigand back to her cave
Scowling after being summoned by a powerful wizard
Eating rotten fruit and stinking vegetables, cheerlessly
Shadowing a dehydrated veteran as she searches for water
Eerily sneering at unmistakable unicorn tracks
Showering a troll with vicious barbed spikes
Embroiled in a frightful feud with a local chimera
Smirking wryly as an evil thought crosses their warped mind
Encroaching on a resting adventuring party
Snarling at a cyclops' curses
Feasting on the pale flesh of a nixie's giant bass
Stalking some heedless halflings as they gather firewood
Firing their tail spikes into a berserker's shield
Stealing a statue that marks a sacred pilgrimage site
Flying low, paws almost touching the ground
Sullying a once clear pool, by bathing off months of ordure
Following a weapon-laden merchant caravan at a distance
Surprising an inexperienced ranger by leaving false tracks
Forging contradictory lawful decrees and bulls
Swatting away a thirsty stirge
Frowning and furrowing their brow as they read a book aloud
Swishing tails to-and-fro as they strut around
Gathering an unusual collection of scalps together to admire
Swooping suddenly to snatch a knight from atop his mount
Gnawing, insatiable hunger has led them to look under rocks
Tracking down some troglodytes, made easier by their scent
Grooming fur and wings with a disturbingly long tongue
Trashing against eldritch shackles
Gulping down a tun of wine in a single draught
Uncontrollably grimacing as they pick their sharp teeth
Hoarding the juicy diaries of lonely noblewomen
Unleashing a salvo of tail quills at an unwelcome werewolf
Hovering just out of reach of a giant scorpion's sting
Vandalizing exquisite mosaics by levering out tesserae with a claw
Hunting down a thief that stole a blasphemous relic from them
Vanquishing a massive venomous coral snake
Impaling all of their kills on enormous thorns
Veering into a dive to avoid being winged by a wyvern
Invading a lizard man lair, demanding tribute
Volleying barbs at rapidly retreating bugbears
Jabbing a rat with a well-aimed tail spine
Waylaying a princess on her way to be unhappily married
Kneading the filthy cushions they rest upon
Wholly startling some normally observant elfs
Kvetching to themselves constantly in raspy, wizened voices
Wringing their paws after discovering their hoard was looted
Lapping up spilt blood from a recent battle between dragons
Yawning contentedly atop a massive pile of martyr bones
Lashing their quill-filled tail at an axe-wielding gnome
Yawping with an evil necromancer

Table: mastodon
Accompanying a small herd of wooly rhinos across a valley
Nearly trampling a troupe of pixies as they try to dance along
Bearing formidable hide-scars from sabre tooth cat attacks
Noisily crushing tough nuts with massive molars
Bedding down to rest, tramping down circles of grass
Obeying whistles and clicks from their stone giant rancher
Being hunted for ivory by unscrupulous poachers
Overconfidently slaking their thirst as a giant croc watches
Bleeding from freshly acquired javelin wounds
Overheated and desperate for shade and water
Blocking a well-travelled road with their enormous bulk
Panicking after coming across a coiled pit viper
Browsing ground-hugging shrubs for delicious leaves
Pawing at the cooled coals of an abandoned campfire
Carving deep furrows in a cliffside to extract minerals
Picking ripe fruit, and placing it in elf-made baskets
Challenging a nervous titanothere with a bellowing yell
Playfully spraying a juvenile with a stream of trunk-water
Charging at a group of hobgoblin hunters
Plodding through a field of broken statues
Chewing sullenly on flavorless nettles
Plowing deep furrows in frozen earth, searching for shoots
Collapsing unusual wooden burial platforms
Plucking out an embedded magic spear with their trunk
Combing through barren branches for the last of the leaves
Pounding a chimera with an uprooted tree trunk
Crashing through a stand of shrubs, fleeing from something
Pulling a sledge, piled high with a /ling family's worldly goods
Damaging a newly constructed wall, blocking migration paths
Reaching for new growth in the lower canopy
Defoliating a dryad's grove, but sparing her tree
Retreating from a titanic praying mantis
Delighting in the discovery of some apple trees
Roaming outside the ruins of a forgotten ophidian citadel
Dragging seasoned timber, goaded by dwarf mahouts
Separating their family unit - touching trunk-goodbyes
Draped with symbiotic mosses and algae, like a sloth
Shaking nutritious nuts from a bedraggled tree
Drinking deeply from a mysterious stone font
Shedding their shaggy coats in matted clumps
Eating artfully bundled clumps of long leaves
Showering a clearing in cherry blossoms as disturb trees
Enduring warmer weather by wallowing in shrinking waters
Shuffling wearily past a wyvern gorging on a titanothere
Exploring a giant skeleton with their sensitive trunk
Sinking slightly in the oversaturated earth
Facing a bracing northerly wind with heads bowed
Snorting loudly to warn off a rogue male
Feasting on verdant growth, crowding the banks of a creek
Splintering a sturdy tree, pushing it down to feed young
Flapping their vessel-filled ears to thermoregulate
Squashing a driver ant who wandered to close to their turf
Floundering to free a calf from an unseen sinkhole
Standing on their hind legs to push over a massive succulent
Fording a river in single file, disrupting waterfowl
Storming a crudely built gnoll keep
Fumbling with a leafy branch, playful calf guarded closely
Striding in unison across a windswept prairie
Gathering at the behest of a powerful druid
Stripping sheets of lichen from weathered rocks
Gnawing on stacks of dry, bitter twigs
Struggling to gain their footing as they slide down a hillside
Goring a massive, seething dire werewolf
Surrounded by grasping ghouls and zombies
Grunting contentedly as they rub against a stony outcrop
Swinging a dead dire wolf around like a flag
Happily rolling about in dry dust to cleanse their hides
Swishing tails impatiently while their orc minder feeds them
Heaving roughly hewn quarry stones unsupervised
Teaching a calf which plants are safe to eat
Helping an elderly family member by tugging down a tree
Tearing down a decrepit barn, groggy goblins fleeing
Huddling defensively around four bleating calves
Thrashing around, bound with several bugbear lassoes
Hurling a persistent troll into a ravine
Thundering toward a band of ogres
Impaling a neanderthal hunter, surrounded by several more
Tottering on a narrow and treacherous cliffside pass
Journeying to a verdant valley, guided by ancestral memories
Towering above their primitive paladin
Knocking down a tyrannosaurus with an enraged charge
Treading water on their way to an ancestral island graveyard
Laden with commodities and tended by a gnome merchant
Trekking toward cooler climates for the changing seasons
Leaving their family herd after coming of age
Trumpeting triumphantly at the first steps of a still damp calf
Lowering their terrible tusks to intimidate a cave bear
Uprooting a marvelously sculpted medusa statue
Lurching with a limp - leg broken in a recent fall
Utterly terrified of a scurrying shrew
Marching along meandering tracks made by generations
Vanquishing a basilisk, petrified pachyderms stand stoic nearby
Meeting with a treant to telepathically treat
Venturing nonchalantly into the center of a village
Milling mournfully around a fallen matriarch
Visiting a well-maintained shrine, acolytes frequently feed them
Mining subterranean salt deposits from an ancient sea
Wading up to their knees in bubbling, heated springs
Mostly surviving on scraggly dead grass near a necropolis
Witching up a winter storm with ancient magic rituals

Table: human, medium
Abjuring a rock living statue within a protective ward
Memorizing cryptic phrases from the large tome on their lap
Absent-mindedly munching dried fruits/meats while reading
Muttering curses as an elf finds a hidden panel hiding a scroll
Apprenticed to a necromancer, shovel in hand/sore from digging
Nearly blinding an orc warrior with a carefully targeted light spell
Aspiring to great mystical might, at the moment, only knows light
Nursing a swollen giant centipede bite and very woozy
Bewitching a bandit leader to assemble some instant allies
Obsessively collecting samples of fungus and spores
Brandishing daggers desperately, exhausted from running
Organizing their components, strange ingredients arrayed on a cloth
Bumbling about with a sputtering torch as a thief jimmies a lock
Overburdened with supplies, yet somehow still unprepared
Casting ivory runes on a velvet handkerchief to choose a route
Paying good gold for gorgon horn or basilisk bone
Celebrating victory over a rust monster with a swig of wine
Pleading for mercy from an ogre with a sadistic grin
Chanting magical phrases to dim a glowing green, grinning idol
Poring over scribbled notes on a tattered map
Chartering an expedition to gather rare reagents
Preparing their spell as well-paid retainers stand guard
Completing the final steps of a fake ritual to impress a dwarf
Pronouncing an incantation incorrectly - a distant thunderclap
Conjuring a shimmering scarlet arrow to hurl at a hobgoblin
Protected by a pack of gnoll mercenaries
Convoking several small animals to select a familiar
Puffing on halfling pipeweed, lost in contemplation
Cowering as a carcass crawler paralyzes his companions
Quarrelling with an acolyte about the true source of magical power
Debating the principles of flight with a friendly gargoyle
Reading a brass-bound tome on the fundamentals of golemcraft
Decoding a rivals spellbook cyphers, or at least attempting to
Reciting a quick charm to decrypt words under an ancient engraving
Defending a fallen cleric from a driver ant, dagger drawn
Researching the dietary habits of owlbears by dissecting pellets
Demonstrating minor magic to impress halfling children
Resting as dwarf allies chortle, orcs outwit by hold portal
Distracting a group of kobolds by throwing their voice
Rolling up a sheet of vellum to store within a waterproof tube
Driving away a cowardly troll by brandishing a flaming dagger
Sampling proffered pixie plonk, to chagrin of his companions
Dueling on an un-level field, victory is quick thanks to shield
Scattering fine white sand to induce a wererat to slumber
Dusting off a bookshelf, and reading the tome's titles intently
Scheming to corner the market on giant leech secretions
Enchanting a fighter's shield to provide illumination
Searching for a reliable supplier of mummy dust
Ensorcelling a scarred berserker to serve as a faithful bodyguard
Seeking to employ bodyguards for a dangerous dungeon delve
Entertaining their pirate captors by juggling knives, eying an escape
Seizing a wand from the white knuckles of a ghoul-struck ally
Fastidiously sharpening their quills by amber lantern light
Shrieking after discovering one of their allies is a doppelgänger
Fleeing from harm, debating if she should use her charm
Singeing the tip of a beard with candleflame, peering at an epitaph
Flinging flaming oil at an indomitably creeping ochre jelly
Slamming their spellbook shut, brain abuzz with arcane energy
Furiously copying luminous letters before they fade from view
Slaying a bounty hunter with a crackling eldritch bolt
Garbling a couplet, a goblin crossbow bolt grazes their arm
Stirring strange herbs into a boiling cauldron
Gazing deeply into a suspected magic pool
Stole a few scrolls before dismissal, one containing magic missile
Gesturing ostentatiously to browbeat a bugbear
Studying a magic circle closely, making crude sketches on a slate
Grinning as they pull an unlabeled potion from their pack
Summoning a weak, but angry elemental with the aid of a scroll
Hauling a giant rattlesnake carcass, hoping to sell its skin
Surrounded by a glittering field, at times forming mystic symbols
Hiding behind a tattered curtain, tips of pointy shoes visible
Taking a tiny sip of a bubbling vial of purple liquid and gagging a bit
Hiring competent adventurers to retrieve a magic wand
Threatening an ogre with curses beyond their capability
Huddling within a protective ward, an angry wight glowering
Tossing orbs of incandescent energy from hand to hand
Hurling their only dagger at a fleeing goblin
Transcribing a glimmering dedication, above a crypt niche
Illuminating an area with a glowing blue orb on the tip of their staff
Transporting an injured comrade on a slow-moving litter of force
Inscribing a last will & testament for an illiterate, poisoned dwarf
Unfurling a colorful scroll of protection and mouthing the words
Intoning a lawful reprieval, preparing to cast protection from evil
Unlocking the waterproof case that contains their book
Investigating rumors of a potent vivamancer seeking an apprentice
Unsuccessfully trying to transmute copper to silver
Invoking the name of a well-known wizard, claiming relation
Uttering ancient words of power to completely seal a ceiling hatch
Jabbing a thoul with an ornate silver dagger
Vaguely worried about a potential nearby trap
Kneeling to politely address a talking keyhole
Voraciously deciphering ancient glyphs from when lizard men ruled
Loading lucre acquired by risk, atop a shimmering floating disc
Warning thieves of curses tragic, after expending detect magic
Lobbing some of their food at a swarming plague of giant rats
Waving their hands as soporific smoke curls from their fingers
Lording over troglodyte minions, impressed by his magic
Whispering softly, kobolds in a heap, very grateful she prepared sleep
Masquerading as a bard, concealing their magical nature
Wielding a two-handed sword, inefficiently, against some skeletons

Table: medusa
Accusing a lapis lazuli lizard man statue of infidelity
Languishing unloved among an untold number of stony suitors
Adorning herself with selectively salvaged jewelry
Laughing as they pet their teacup basilisk
Atoning for indiscretions at a shrine to the starlit goddess
Locking the glass case containing their sister's covered head
Austerely glaring at a groveling goblin
Looking in askance at an acolyte, receiving only stony silence
Basking languorously near an unquenchable flame
Luring athletic youths to a tournament of sport
Beckoning their living statue servitor with a silver bell
Making her big brass bed as a blind bard strums om saudade
Beguiling a brigand with her shapely shadow
Masking their nature with an elaborate theatrical prop
Beheld by a berserker, swiftly stiffening into basalt
Meddling in local politics, via a charmed noble thrall
Blindfolded corpses attest to her lethal tresses
Milking a gorgon, unbothered by her breath
Bloodletting: garnet droplets flow and form into deadly asps
Morbidly marrying decapitated heads to various stone necks
Blushing before a genuflecting gargoyle
Mourning over a prone, marble, medium
Bottling surplus serpent spittle to sell to assassins
Nervously styling and re-styling her snakes
Cackling cacophonously, causing a cleric statue to crack
Nonchalantly hanging her headwear on a hematite hobgoblin
Clinging seductively to an exquisitely carved column
Ostentatiously trembling to feign fear
Cloaked for her paramour's protection via magical necklace
Painting lurid hues on her statues with a unicorn hairbrush
Coating a wavy bladed dagger in dripping venom
Peering anxiously over a pew after spotting a beam of reflected light
Coiling their coiffure into an intricate, very fashionable, bun
Perplexed by a vampire's dinner party invitation
Confiding in a conglomerate conjurer, enduringly agape
Petrifying an unfailingly polite paladin, bowed to kiss her hand
Conniving to corner the art market to fund her lavish lifestyle
Poring over ancient, crumbling scrolls - searching for a cure
Cooing to an enormous cobra, a constant companion
Practicing her heavenly harp playing
Crowned in crimson, cream, and coal - coral snakes
Prattling about family drama to a nodding golem
Crushing a calcified canary, incessant singing annoyed her
Preening before an ornate, but empty, mirror frame
Cursing a nearby community with crop failure
Presiding over an assembly of summoned serpents, all sizes
Daintily dining on ortolans, head covered with a cloth
Pretending not to notice a hidden halfling
Daydreaming on a dusty settee, idly eating eyeballs
Quavering slightly in a chilly draft, adjusting her serape
Decorating their den - artfully arranged amputated stone arms
Rattled after a recent robbery - her magic quiver missing
Demanding tribute from passing traders
Reading her spell book, bound in purple worm leather
Devouring deliciously juicy apples, swaddled in gold leaf
Recently widowed for the seventeenth time
Differing significantly from the species: lawful in outlook
Reclaiming her domain from aggravatingly resilient undead
Disguising herself via heaume, shushing disgruntled hissing
Reflecting wistfully on a former fling, now storing stoles
Draping statuary with colorful and costly silk scarves
Ruling a nearby hobgoblin tribe clandestinely
Dreading a visit from her mother, tidying the den
Scheming to petrify a handsome priest for her collection
Earnestly pulverizing flaky stone for a special soup
Seething with righteous choler as is her wont
Embracing a petrified elf, frozen in an arms outstretched pose
Shaping sinuous forms in clay with her delicate fingers
Fastening the fibula for her samite shawl
Shielding her eyes as she bathes in a pristine pool
Feeding her hissing hairdo squeaking mouselings
Shrugging at the entreaties of a blind-folded bandit
Firing her magical bow at a resilient, fleeing bugbear
Sidling up to a terrified scribe, eyes glued to his quill
Flinging a glassless hand mirror across the room in frustration
Singing sweet and sibilant psalms to a granite gladiator
Foretelling a fawning fighter's future
Slaying a trespassing templar with her venomous tresses
Gazing into the fractured, felsite face of a former farmer
Smirking wryly as orcs cart away their chieftain
Gingerly dipping her arrowheads in sizzling toxins
Stealing a glance at a partially painted portrait
Holding a swaddled babe to her breast, looking for a rattle
Suddenly shedding her wimple to surprise a sage
Hooded in a chenille cowl, embroidered with leaping pegasi
Tearfully defacing a porphyry princess's loving smile
Hunting in a cluttered drawer for irresistible perfume
Thoughtfully chiseling a new face for a former friend
Imploring her blind beloved not to leave
Uncontrollably weeping over a broken bracelet
Inhabiting an abandoned temple, defiled with shed skins
Veiled chastely, stepping into a curtained carriage
Involuntarily petrifying a pilgrim, come to pay homage
Vengefully encasing a voyeuristic veteran mid-peek
Joyously destroying a gneiss gnome
Watering a garden, full of poisonous plants and mushrooms
Kneeling at an altar dripping with candles, reverently veiled
Weaving a tapestry self-portrait, petrifyingly accurate
Knotting their serpentine plaits in anger while reading a letter
Yawning as she spins wool into silver on a wheel

Table: human, merchant
Accepting payment for several barrels of scrumptiously sour cider
Loading large casks of candied fruit onto their carts
Adjusting wagon distribution after breaking an axle
Logging every transaction in a magical ledger that totals
Advertising their perfume wares to disinterested dwarfs
Looking to employ a medium for entertainment
Arguing with their guard captain over a washed-out route
Lucratively stocked by an ennui stricken efreeti
Bankrupting a halfling tobacco farm, undercutting prices
Meticulously taking inventory after firing a thieving guard
Barking out orders to bored and underpaid guards
Mud stained and trying to right a toppled wagon
Bartering two mules for passage over a troll's bridge
Navigating an area, dotted with deep and deadly pit traps
Blazing a new trade route through inhospitable terrain
Offering unbelievable sums for arms after a rust monster run in
Boycotting a gnome clan after a counterfeit coin scandal
Operating without an official guild license, and on the run
Brokering with a friendly cyclops for rare wines and raw wool
Outfitting their caravan for a grueling journey, seeking muscle
Bustling down a muddy trail, late for an annual bazaar
Partnering in secret with a hobgoblin king
Chaffering over fodder with a local farmer
Paying homage to a deity, seldom worshipped in these parts
Chartering passage with pirates, convincingly disguised
Peddling poor quality goods for exorbitant prices
Cheating centaurs desperate to trade for iron ingots
Plastering trees with reward posters for a bandit leader
Commandeering a campsite after driving away nomads
Pleading with bandits to spare their mounts
Complaining about rough sleeping conditions
Plodding forth on a forced march after being run out of town
Consigning their stock of silk to an enterprising elf
Profiteering by selling arms to both sides of a conflict
Contriving to profit from recent gnoll uprisings
Prospering from a beneficial trade agreement with lizard men
Convoying through a narrow pass, ripe for bugbear ambush
Protesting an increase in tariffs by smuggling goods
Dealing on behalf of a craven devil swine
Purchasing a new wagon from helpful dervishes
Discounting their flour prices for a starving village
Quickening their pace after seeing giant tracks on the trail
Disguising their weapon shipment in bundles of firewood
Rearranging panniers containing supplies on their mules
Dispatching a lieutenant to scout ahead and report back
Receiving stolen merchandise from bandit allies
Donating pickled fish to a roadside shrine attendant
Recovering after a raucous celebration the previous night
Employing a remarkably civilized ogre as their captain
Refusing to charge a hungry family for a bushel of vegetables
Enjoying a relaxing meal of roast boar around a fire
Repairing their last spare wheel and hoping it will hold
Entrusting livestock to a stable hand (secretly a werewolf)
Replacing their guard captain after a deadly snake bite
Exporting expensive furs to colder climates
Retiring after one last run, if they survive the roc attack
Failing to notice a hungry griffon circling overhead
Returning, wounded and bedraggled from a deal gone wrong
Feigning ignorance about local duties/taxes
Rigging up a makeshift road out of logs to cross deep mud
Ferrying their caravan across a treacherously rushing river
Roving far and wide, trying to find a buyer for stale beer
Financing an expedition to untapped markets with profits
Scheming with a local noble to flood a rival's markets
Flogging well-crafted jewelry, surprisingly reasonable prices
Seeking buyers for their surplus supplies, selling for cheap
Furnishing local markets with surprising potions
Setting up camp, a little too close to a hydra's den
Generously loaning a horse to a wounded paladin
Solemnly burying a dead doppelgänger
Greedily eyeing the belt pouches of pilgrims
Specializing in exotic animals and monsters for menageries
Haggling over fresh horses with a mercenary general
Speculating by stockpiling acid after recent troll attacks
Hailing fellow travelers, hoping to find safety in numbers
Supplying a weretiger tainted town with silver weapons
Hauling wagons piled high with remarkably lifelike statues
Swindling some kobolds by selling them spoiled fruit
Hawking sacred reliquaries, most contain tiny bird bones
Trading metal implements to neanderthals for valuable shell
Hesitating after coming across a group of dead soldiers
Trafficking mostly in books, scrolls, and secrets
Hiring adventurers as guards, after their escort died of plague
Transporting a political prisoner in disguise as a guard
Hoarding vital firewood in expectations of a cruel winter
Underestimating the demand for fine silks among berserkers
Importing elf-made mead, said to contain killer bee honey
Utterly silent, conducting business through writing only
Insisting to pay pixies after ruining their mushroom ring
Veering off course after a very severe thunderstorm
Intercepting a rival trader selling goods stolen from them
Visiting a dryad grove to try to bargain back their leader
Inviting any comers along on a difficult leg of the journey
Wandering aimlessly after a befuddling encounter with nixies
Joining up with a line of wagons that lagged behind
Weighing strange sparkling dust on sensitive brass scales
Keeping their mission to spy on local affairs secret, clumsily
Writing long-winded letters home
Leading their horses on foot through thick, thorny brambles
Yelling for help, under attack by a ferocious chimera

Table: merman
Ascending to revel in the torrents of an upcoming cloudburst
Impaling an octopus on the tips of a trident
Assembling to crown a new sea queen
Invading a buccaneer haven
Astride war-seahorse side-saddle, armed with coral lances
Jilting land-locked lovers in favor of the waves
Avoiding a shiver of circling sharks
Kissing a drowning sailor to fill her lungs with air
Babbling instructions to a seal
Knitting intricate shawls out of ultra-fine byssus
Bartering with visiting ogre-sized orca-folk
Languishing in chains atop a dry rock, out of wave-reach
Basking in the warm shallows of a picturesque lagoon
Lazily drifting on the currents, bellies full of butter fish
Beaching a small boat they found adrift at sea
Looting a shipwreck, stealing dishes and silverware
Befriending a sea dragon, new to these waters
Losing a battle with a giant squid
Carving intricate intaglios into nacre
Luring a ship onto a sandbar to pilfer attractive cargo
Catching darting shoals of shimmering anchovies in fine nets
Making intricate jewelry out of fishhooks
Chasing away a saltwater termite
Manufacturing surprisingly fish scale armor
Cloaking themselves by piercing harvested squid ink sacs
Migrating to more fertile waters along with their whales
Collecting coins thrown into the shallows by wistful lovers
Negotiating, via gesture with strange crab-folk
Combing their long wavy tresses
Netting a school of skittish sardines
Concealing themselves among a school of brightly colored fish
On a pilgrimage to visit an ancient mangrove treant
Cracking open langoustines to feast on their meat
Overwhelming a shark-folk scouting party
Cultivating vast leafy columns of kelp
Playing in a small eddy of their own devising
Cutting a sea turtle free from a fishing line
Possess the secrets for crafting coral living statues
Dashing to the aid of a harpooned whale
Pouring out of a sheltered sea cave
Defending themselves from a pack of hungry sea ghouls
Protecting a portal to the elemental plane of water
Desperate for aid against an aquatic vampire
Racing a pod of playful dolphins
Diving with great haste to stop an anchor from crushing a home
Rescuing survivors from a shipwreck
Dressing a skeleton in flotsam finery and jetsam jewelry
Rising from below to ambush a sea troll
Drowning the ruthless pirate that hunts them for sport
Rushing to the aid of a distressed saltwater nixie
Ebbing out to deeper waters, after checking on an island druid
Scavenging through the decks of a sunken galleon
Emerging to taunt a ship of starving sailors
Sculpting ephemeral magical mandalas in the sand
Evading the sword-like teeth of a giant barracuda
Sheltering from a squall in a cave-filled undersea cliffside
Expertly shaping shark teeth into spear points
Shucking oysters, in search of pearls
Extracting lethally envenomed stonefish spines
Shying away from a deadly sea snake
Feasting on giant lobster tails
Singing sonorous strains, within earshot of sailors
Filing into a link of mighty chain, holding an anchor
Skimming just under the surface, riding a ship's wake
Fleeing from a rime wight
Skulking in tall sea grass, hunting tiger shark
Floating near the surface to ambush a diving wyvern
Slowly descending into a vast, impossibly deep trench
Freeing a companion, caught in a tenacious giant oyster
Spearing a sablefish supper
Frolicking in a great roiling rogue wave
Stowing supplies on the back of their domesticated dugongs
Gathering periwinkles and scallops from their beds
Stringing toxic jellyfish to form a fence
Gliding carefully past a reef of vampiric blood coral
Surfacing to sip from wine from a sealed jug
Glissading down the side of an undersea slope
Swapping salvaged gold for steel knives and spearpoints
Glistening amid the tumultuous surf
Swimming alongside a docile whale shark
Guarding their mistress - a sea hag who ensorcelled them
Telling an ancient fable about a great drying
Guiding grateful fishermen to a bountiful shoal
Tending to a garden of subsonic shreiker coral
Haggling with a secretive manta ray-folk traders
Tithing to a tyrannical storm giant who lives nearby
Harnessing dolphins to an ornate chariot
Trading pearls to surface dwellers for metals
Harpooning a massive moray eel
Trumpeting with conch shells
Harrowing the sand with bone rakes, searching for a magic ring
Twirling their tails demurely
Harvesting mussels thriving on submerged statues
Undulating in the current as they keep watch
Hiding among undulating tentacles of giant anemones
Visiting a dragon turtle, bringing lavish gifts
Hunting sea serpent - a coming of age ritual
Warming their hands over a bubbling thermal vent
Illuminating dark depths with strange glowing jellies
Weaving incredibly strong nets from sea grass

Table: minotaur
Abandoning a half-eaten roast boar on cooling embers
Munching loudly on still twitching, very bony fish
Appearing suddenly from behind a concealed door
Nailing pitons through a board to set a crude trap
Attempting to wrest the head from a living statue
Negotiating with a trader who seeks peaceful passage
Baiting the ground with a tinkling trickle of electrum coins
Nosily eating a cart's worth of stolen carrots
Blooding an ogre with his massive battle axe
Obliterating the obelisk that traps him within this room
Brandishing a two-handed sword, engraved in dwarf runes
Obsessing over a misplaced memento
Carving concentric spirals on every available surface
One quick stomp deals with a shield-sized scorpion
Celebrating victory over a limp chimera
Ousting a nest of harpies for failing to pay tribute
Challenging all comers to a complex board game
Overrunning a pack of nervously giggling gnolls
Charging headlong into an npc party battling bugbears
Pawing their hay pile bed to scare away rats and snakes
Chasing after the thief who stole their magic chalice
Plowing through a phalanx of fighters, sent to slay him
Chewing on a bitter root that grants immunity to fire
Plunging their pike into a squealing rust monster
Chuckling to themselves as they nail a door shut
Pounding a pestle into a stone mortar to grind bones
Circling back to catch a nomad unawares
Preparing an owl bear carcass for the stew pot
Conferring casually with a group of bull-headed gargoyles
Protecting a local farmer, to whom he owes a life debt
Cornering a conjuror, fumbling for her wand
Prying open a locked chest with sheer strength alone
Counting their hoard, tally marks on a dusty slate
Quaffing a potion for healing, unfortunately a philter of love
Crashing upward from a trapdoor to surprise a gnoll
Quashing an upstart goblin king's invasion of his territory
Crossbred with gorgons, beware their breath
Rampaging after discovering intruders in his maze
Crusading on behalf of a chaos cult, attended by acolytes
Ransacking a shrine, smashing idols and offerings
Defending the fallen cleric that he foolishly fell in love with
Readying a bow, tall as a dwarf, to aim at a giant bat
Deposing a bandit king, a motley bunch grovels at his hooves
Reciting an ancient ballad in their lowing, melodious language
Destroying a dwarf's steel shield in a punishing strike
Refusing to bow before a powerful sorcerer
Dragging an enormous flail behind him with a grinding sound
Repeatedly ramming a pew into an unbreakable mirror
Drinking a huge cask of ale, received as payment from gnomes
Ripping apart a contract covering their services as bodyguard
Erasing chalk marks left by clever adventurers
Roaming along a high ledge, looking for spider eggs
Escorting a hobgoblin chieftain as hired muscle
Roaring echoes throughout the complex as he extracts an arrow
Fighting in a spike lined pit as berserkers lay bets
Roasting bread loaf-sized grubs on a spit, plenty to go around
Following slimy carcass crawler tracks, for easy pickings
Rushing across a river, dragging a large heavy chain
Forging hand-sized arrowheads for a colossal crossbow
Rutting and especially ornery, even growling at his shadow
Goring a white ape as others pelt him with stones
Sketching out plans for a large labyrinth in the sand
Grappling with a giant crocodile, actually a very playful pet
Slaughtering a giant centipede with an accurately thrown knife
Grunting as goblins stack huge smelly sacks of potatoes
Smashing shelves full of ornately painted canopic jars
Guarding entrance to a "monsters only" underground tavern
Snorting loudly as they pick up a hill giant's scent
Hulking, stinking of sweat as they move a massive stone seal
Spinning shimmering wool into golden clews
Hunting down a wizard to reverse this reincarnated form
Splintering a large oaken table, halfling hiding underneath
Hurling huge javelins at a smelly scarecrow dummy
Staggering after overindulging in mushroom wine
Hurtling down a hallway after a shrieking kobold
Stalking the source of a shrieker's screeching
Illuminating a big bolt hole, hungry for giant rat
Stampeding at full throttle into a snarling hellhound
Inhabiting a carefully cultivated fungal hedge maze
Threatening a troll with a blade licked by flames
Jailing a renegade ranger in a claustrophobic cell
Toppling a statue of a surprised cyclops
Journeying far from his maze in search of a potential mate
Tossing a sharpened and deadly discus to each other for fun
Jumping from stone-to-stone to cross a fizzing pool of acid
Trampling through a black widow spider's hard web-work
Kicking over a table in frustration after being hoodwinked
Trying on a replacement gold nose ring
Knocking down eerily accurate statues of adventurers
Uncharacteristically gregarious and cheerful due to a dryad
Lobbing flaming oil at grasping skeletons
Unerringly navigating through confusing corridors
Lumbering across a sighing, rather rickety, bridge
Vanquishing the vampire that slew most of his tribe
Lunging suddenly to snatch a pesky stirge from the air
Vaulting over a low wall after a snarling giant weasel
Luring a nixie away from her home with a trail of pearls
Waiting patiently before a shimmering magic portal
Messily devouring a bushel of grapes, even eating the stems
Wielding a club that he's named and talks to frequently

Table: mule
Ambling across broken ground, picking deliberate steps
Lunging at a chittering rodent, frightening it away
Attracting a swarm of large, fat flies that buzz and bite
Lurching under the weight of an entire party's supplies
Balking at a barrow entrance, as a paladin pulls their lead
Marching morosely with an arrow sticking out of their rump
Bearing a bulging pannier, brimming with rations and pitons
Meandering nonchalantly among a ravaged battlefield
Begging all comers for scratches behind the ears
Munching loudly on a spilled sack of purple radishes
Behaving erratically after sensing an invisible stalker
Navigating a winding route with cautious hoof-falls
Bellowing protest as a dwarf yanks them from an apple tree
Nibbling playfully at a ranger's pant leg
Biting at their flea-bitten foreleg, as they swish their tail
Noisily braying because their harness is on too tight
Bolting after a puddle of oil catches fire
Nuzzling their best friend, a blue-eyed blink dog
Bringing a trader's goods to a distant halfling enclave
Objecting obtrusively to being led across a rickety span
Browsing among multicolored mushrooms for a tasty treat
Overburdened and swaying on wobbly, shivering legs
Bucking off an inexperienced crossbowman
Pacing impatiently, tethered with a long lead outside a cave
Carrying hastily tied bundles of firewood on her back
Pampered by their halfling handler, being brushed currently
Chewing on leaves that leak blood-red liquid
Plodding doggedly down a wagon-rutted road
Choosing a less steep path, despite their owner's protests
Plowing through a screen of flowering vines, pixie-chased
Clattering to a stop as a saddle strap snaps
Pulling a clinking cart of glittering ore from a mine
Confounding owner at every turn with their stubbornness
Punctuating every few steps with contumacious stamping
Cropping tall grasses short with large, loud teeth
Rearing up with a whinny, scattering kobolds before him
Crossing a dangerously derelict bridge with confidence
Resting in the shade of a dryad's tree, sprites braiding her tail
Dashing a rather large snake against a boulder
Rubbing along a rocky wall, and moaning contentedly
Desponding over the crumpled body of a deceased diplomat
Scrambling on steady legs down a slickened furrow
Devouring fermented figs and getting quite drunk
Shod with a single magical shoe, stomps when lies are told
Dragging a makeshift liter carrying a wounded warrior
Shying away from a grimacing carving of a horned face
Drawing water from an animal powered well
Slick with sweat and chafing under sacks of coin
Drinking deeply from a dervish's clay jug
Snorting its objections to the halfling loading his bags
Eating their weight in cabbages while a farmer is distracted
Splashing across a shallow stream, pursued by wolves
Eying a dark cave entrance suspiciously, ears perked
Squealing out loud hee-haws after becoming hopelessly lost
Flatulating constantly, much to the chagrin of a sneaky thief
Stampeding through a squadron of skeletons
Fleeing from a pack of gibbering ghouls
Starving, with a rope tied around them trapped in a pit
Flicking their dexterous tail to swat away insects
Stealing a loaf of bread from a hungry fighter
Floundering in deep, unstable sands
Stewing sourly, tied to a tree as their owner sleeps nearby
Following their over-excited furrier dutifully, piled with pelts
Stinking to high heaven after antagonizing a skunk
Fording a rushing river, utterly unfazed
Stopping frequently to sample leafy bushes and shrubs
Galloping bravely towards a sniveling manticore
Straining under the weight of a wagon piled high with weapons
Grabbing their owner by the cloak as they slip off a cliff
Struggling within web strands as thick as rope
Grazing happily on an unmown hay field
Stumbling due to a stone lodged in their left back hoof
Guiding a blind pilgrim to a hidden, very sacred shrine
Swerving suddenly to avoid a hidden hole
Hauling a large piece of partially hewn lumber on chains
Tearing down laundry from a line with their teeth
Ignoring commands from a frustrated merchant
Testing muddy ground prudently before continuing forward
Injuring a gnoll with a vicious bite to the arm
Trotting carefree and wild after escaping captivity
Jingling as they strut in a shiny new bridle and harness
Trudging to the crest of a hill in search of good pasture
Jogging merrily after hearing their owner's distinctive whistle
Untying a rope that connects them to a fence with a deft tongue
Joining with others in front of an abandoned cart expectantly
Utterly refusing to go any further, frustrating a bandit
Jumping a narrow ravine surefootedly
Vigilantly guarding a tent containing a sleeping acolyte
Kicking an ogre with both back legs, square in the groin
Walking slowly to keep pace with a limping veteran
Kneeling as a gnome secures a bushel of berries to her back
Wandering fearlessly through dark and frightful terrain
Lagging behind, distracted by delicious lichens
Wearing flowers from a magical plant in her mane
Leading some trader's down a treacherous scree
Whinnying excitedly as his master returns with fodder
Licking sweet sap from the trunk of a ticklish treant
Yanking their owner along, determined to get home
Lumbering with a full belly to drink from a brackish pool
Zigzagging to avoid splashing in bubbling puddles

Table: mummy
Afflicting their horrid necrotic disease on an unlucky dwarf
Missing hands, crawling along corridors of their own volition
Angered after sensing life, shattering clay grave goods
Moldering with the ravages of time needs new coverings badly
Arrayed in ornamental mantle, dripping with dull, dusty gems
Nearby housecat-sized amber golems come quickly when called
Begrudgingly allowing herself to be fanned by skeletal attendants
Noiselessly screaming, unwrapped face contorted in anguish
Benumbing a burglar, subjected to their horrible form
Once a gifted golem maker, still defended by bronze servitors
Binding victims in natron linens to fabricate new companions
Oppressing an order of acolytes that still tends to their tomb
Blackened fingertips from trying to touch a holy relic
Ordering around his skeletal minotaur pretorian guard
Breaking into a gilt wooden casket with a ceremonial rod
Overwhelming a halfling's courage, as he freezes with fright
Briefly remembering their former life, sobbing uncontrollably
Painting bones of sacrificed horses with magical, animating pigments
Brooding as they tenderly caress a carnelian cameo
Pampering his mummified crocodile pets
Celebrating an eon old victory, in perpetuity, with empty goblets
Paralyzing an entire party of pilgrims with terror
Chastising the skeletal remains of a long dead advisor
Perfecting plans for a continent-wide necropolis
Chimerically altered, wielding a giant scorpion's tail
Plotting an eventual return to the throne of a long-forgotten kingdom
Commanding a loyal legion of skeletal retainers to excavate
Preparing an elaborate ceremonial feast, with empty plates and cups
Confronting their reflection in a dust-laden mirror, pausing briefly
Presenting an ornate spear to his wight captain
Containing hordes of voracious, hand-sized, hungry scarabs
Proclaiming sovereignty in a hollow shout to whomever they meet
Cradling their tightly bound child (also a mummy) closely
Pulverizing a skeletal retainer for perceived disobedience
Craving the warmth of life, squeezing a squeaking rat until still
Punishing their distant ancestors with a powerful curse
Cringing as a powerful priest intones a rebuking recitation
Ransacking a room, releasing centuries of rage
Crumbling a brittle papyrus scroll to finish a millennial ritual
Reanimating a legion of laborers, entombed alive with him
Cursing any interlopers with unquenchable thirst
Redolently smelling of exotic unguents & impossibly valuable incense
Damaging ancient inscriptions that extoll his successor
Reining over his skeletal rat and bat subjects justly and fairly
Detesting their surroundings after millennia of monotony
Remaining well within the confines of a powdered silver circle
Drying and brittle with age, its wrappings contain a sacred cipher
Remarkably well-preserved, almost completely incorrupt, save eyes
Endlessly decreeing in halted, hollow voice to an absent audience
Repurposing a ceremonial font as a festering cauldron of snakes
Engulfing enemies with flailing, prehensile strips of wrapping
Returning a sacred relic to rightful resting place, will stop at nothing
Exalting a dated, dying deity with daily devotions
Revered by hobgoblins due to her resemblance to a goddess
Examining tomb paintings of her husband, emotionlessly
Rewarding anyone who can solve an ancient riddle
Fashioning a crude crown from the wing-bones of bats
Rising from their cinnabar sarcophagus, carved with crocodiles
Filled with several dozen skeletal asps that strike from gaps in linen
Rolling a huge canopic jar containing the withered heart of a giant
Finally finishing an ancient alchemical formula in cuneiform clay
Seated on an ivory inlaid throne
Flecked with fatal, choking spores that explode on contact
Seeking news of their kingdom, faded from history long ago
Forever devoted to his mummified feline companion
Sending a series of plagues to a local settlement
Forgetting their state completely, sees everyone else as undead
Shambling stiffly, stopping to salute theriocephalic statues
Grasping withered claws tightly around the neck of a medium
Shriveling the resolve of a paladin with his frightful gaze
Grinning maniacally, tearing the taut skin once around their lips
Shrouded in bandages, emblazoned with firebane glyphs
Haunting the once hallowed hallways of a temple complex
Sifting through a pit of sand, searching for something lost
Hollow body filled with magical papyri and sacred texts
Suffocating a foolhardy cleric, holy symbol falling from limp fingers
Hounding a tomb robber who stole a bejeweled scepter
Summoning servants that never come, by repeatedly ringing a bell
Hurling dry organs that blight on contact, in exploding clay jugs
Sundering a sell-swords two-handed blade with a single blow
Immersing in a pool of sap-like tar to protect from further rot
Swarming with coin-sized, blinding and biting undead flies
Imitating the routine rituals of daily life, irascible if interrupted
Swathed in an impossibly resilient translucent shroud
Interrupting a clandestine meeting between orcs & gnolls
Terrifying a trader, sheltering from horrible weather
Joining in a half-forgotten holy hymn that sings daily by magic
Threatening a local king with dire missives delivered by skeletal ibis
Knows many forgotten magics, seeks a worthy undead apprentice
Tracking greasy footprints of dead ants throughout the area
Laughing - wheezing coughs/flurries of moths as he trudges about
Unwrapping their ancestors, to prop them up and admonish them
Lifting a heavy marble slab with barely any effort at all
Wandering aimlessly, endowed with a purpose long since lost
Lounging upon a palanquin, borne by bone golems
Wearing tarnished, scaly armor that noisily betrays her movements
Lurching towards a distant light source, roused from slumber
Withered and contorted into a tightly hunched posture
Marrying a different, mostly disintegrated groom every morning
Yellowing any living thing they touch with crippling jaundice

Table: human, neanderthal
Acclimating to a dramatic shift in seasons, covered in furs
Lugging a crude liter sledge, bearing a dead unicorn
Acting out a creation myth, with masks made from bird bones
Luring a cave bear from its den, into an engineered avalanche
Ambushing a sabre toothed tiger, lethargic from a recent kill
Making ropes of woven grasses
Approaching a herd of antelope, crouched and cautious
Marking a trail to a reliable and pure water source for future use
Associating metal with death - very wary of the armored
Mixing bright pigments in precious seashells
Bearing intricate and artful charcoal tattoos across their bodies
Mourning over the loss of a companion, faces covered in ashes
Burning birch bark down to make their sticky spear-tip tar
Negotiating silently with a frustrated dwarf trader
Burying a blink dog with a solemn, touching, ceremony
Nursing an injured kinsman's fractured leg with splint/poultices
Camouflaging themselves with woven nets of leaves/twigs
Observing a reindeer herd's movements intently
Carving straight notches in a length of bone for timekeeping
Painting potent totemic depictions of dinosaurs and dragons
Celebrating the birth of a child with a massive feast
Posturing to intimidate some unruly rock baboons
Collecting several varieties of mollusks in shallow pools
Protecting man's first magic from greedy mediums
Crafting delicate flutes from a raven's hollow wing-bones
Puncturing coins with sturdy bone drills to string on necklaces
Creeping quietly around the edges of a hobgoblin camp
Quitting their cave after a devastating plague of sickness
Decorating the walls of their home with ochre handprints
Rhythmically drumming on hollowed out logs
Discovering a trove of tasty tubers, excited
Ritually deflensing a dead triceratops
Disguising themselves with wolf hides to stalk aurochs
Roaming far from home, desperate for water and food
Dowsing for a water source, following a cobra blinded elder
Roasting an elk, intricate hospitality ritual requires sharing
Dressed in impressive lion hides, using claws/teeth as jewelry
Scavenging spear points after a battle with orcs
Driving away a hungry giant tuatara with lobbed rocks
Scraping a stretch cave bear hide clean
Dwelling in a cliff-side complex - several tribes cooperating
Scrutinizing signs and portents on burnt tortoise shells
Ecstatically dancing after ingesting unusual mushrooms
Searching for sacred lichens at the behest of their shaman
Escorting a gnome-friend safely across a rushing river
Sharpening a sacred, meteoric metal hand axe reverently
Expertly butchering a bison, saving sinew and organs
Shouting and whooping to startle deer into a trap
Fashioning impossibly sharp obsidian hand-tools
Showering the corpse of a companion in flower petals
Feeding a stray wolf pup that wandered close to their cave
Sitting around a fire while the elders eat first
Finding a use for a discarded helmet - hauling water
Skinning a titanothere, might take some time
Fishing with multi-tipped spears, while men guard the catch
Snapping bones to extract nutritious marrow
Following ogre tracks, arrayed for all-out war
Setting surprisingly complex snares for game birds
Foraging for edible mushrooms, hide baskets brimming
Harvesting honey after smoking out killer bees
Forming small fertility figurines out of deep red clay
Stalking a herd of wild horse across the land
Ganging up on an enraged mastodon
Stampeding a herd of bison off a cliffside
Gathering poisonous berries for their bright pigments
Stockpiling flint and greenstone after seeing ogres in the area
Gesturally debating the nature of some animal tracks
Stooping to drink from a babbling brook
Grimacing after hearing a distant tyrannosaurus roar
Surviving despite encroachment of halfling homesteaders
Grunting in approval at a juvenile's brace of rabbits
Tanning a rock python hide to trade to primitive elfs
Guarding a strange, glowing stone, incised with runes/glyphs
Teaching a white ape a few key signs in their gestural language
Hauling quickly butchered bits of brontosaurus
Testing the depth of a tar pit with long spruce poles
Hiding a cache of food beneath a stone cairn to keep it safe
Throwing broken spears and throwing sticks into a ritual pit
Hunting wooly rhinoceros with meticulously honed tactics
Tooling hides with ivory awls while the women hunt
Impaling a rabid gnoll foaming and growling
Silent trading with peaceful lizard men
Inhabiting abandoned dragon den, slowly trading hoard to dwarfs
Trepanning an initiate into the shamanistic caste
Investigating a party of dead adventurers, marveling at metal
Understanding a few key words in dwarf, fewer in common
Jabbing their expert bone needles through thick hides to stitch
Using distraction to harvest eggs from a terror bird nest
Kayaking in pterosaur skin canoes
Utterly mute due to taboo - shudder at the sound of speech
Knapping large flint-cores into spear points
Venerating the over-protective gold dragon that lives nearby
Laboriously dragging a slain crocodile back to the cave
Wading with nets in a bountiful lake
Launching a rock fall onto a group of grazing goats
Weaving water-tight baskets from reeds and hide
Listening intently to bird song for signs of coming weather
Wielding spears enchanted to strike ever true by their shaman
Looking for a place to camp, on a journey of spiritual significance
Yielding a fertile valley to a herd of stegosaurus

Table: nixie
Abiding by ancient strictures of hospitality for all
Kibitzing instead of dismantling an unwelcome beaver dam
Accentuating their natural beauty with shell jewelry
Kissing oxygen into a sinking acolyte
Admiring their reflections on the still water's surface
Laughing derisively at a homely gnome
Apologizing profusely to a giant catfish
Lounging seductively on a tiny island of blooming cherries
Avoiding a very hungry, very large crocodile
Luring a lyre-bearing bard into their lagoon
Babbling incessantly with a soporific sibilance
Magically enthralling a formidable fighter
Basking contentedly in the warm sunshine
Mesmerizing a missionary who came to convert them
Bathing an extremely filthy berserker
Modelling for a magical figurehead
Beguilingly beautiful as they fill amphorae
Mustering their giant bass against a greedy ferryman
Bestowing breath upon a drowning dwarf
Nagging a druid to deal with a lecherous ranger
Blushing as they peruse particularly purple prose
Nominating a new spokes-nixie for dealing with landlubbers
Brandishing stonefish spine-tipped spears
Nurturing a wounded warlock
Brilliantly scintillating with a dewy glow
Observing a bivouacking orc army with frightened murmurs
Calling forth a shimmering shoal of fish
Officiating matrimony between two lovers, local tradition
Capering along the shore after satyr's stole their shawls
Ogled by a soon-to-be-enslaved hunter
Captivating a centaur who stopped to fill his waterskin
Paddling along in a shallow draft swan-shaped boat
Caracoling atop their giant bass mounts
Playing complex clapping games with each other
Causing trouble by tying fishing lines together
Plunging under water to flee from a hungry roc-sized stork
Cavorting with some visiting pale-purple wisteria sprites
Ponderously conversing with a shore hoarding treant
Celebrating the momentous hatching of a dragon turtle
Reluctantly imparting water-breathing to a fisherman
Charming a laundress to defy her wicked stepmother
Ripping up a treaty with a local village
Chuckling after trying tea for the first time
Romping gleefully through recently flooded fields
Combing their tresses with codfish bones
Shimmering jewelry - gifts from admirers, adorns their arms
Completely enrapturing a red-haired bandit prince
Shrieking with eldritch rage at a polluting manticore
Conferring water breathing on a veteran troll slayer
Singing sweet lullabies to a drowsy duelist
Dancing in a ring, around a bleached giant snail shell
Slightly glistering in the dappled sunlight
Destroying a newly constructed waterwheel
Soaking themselves in a steamy, mineral-rich spring
Diving for pearls, seem very lucky - never empty handed
Splashing their thrall - a kindly faced ogre playfully
Dousing a frightful fire elemental to keep it at bay
Spraying a troublesome robber fly from a distance
Enchanting a blacksmith, to have her forge tiny tridents
Squealing with pleasure after being presented with gifts
Enhancing the majesty of a cacophonous waterfall
Staring at themselves in silvered hand mirrors
Entertaining themselves with unusual musical instruments
Stringing garlands for their pretty paladin captive
Falling apart completely after the death of their favorite eel
Struggling to raise their petrified queen from the sandy bed
Floating languidly atop humongous lily pads
Submerging out of modesty to address a shy friar
Fooling around atop a crumbling, ancient granite fountain
Summoning striped piscine pals to drive away lizard men
Furiously drenching an unsuspecting goblin
Sunbathing salaciously for any and all to see
Gamboling among mossy boulders and pure pools
Surfacing in unison to receive a swan messenger
Giggling at a private joke about air-breathers
Swimming balletically with lithe and nimble limbs
Giving a haughty elf a piece of their mind
Tastefully adorning themselves with water lilies
Gliding across the water's surface astride giant snakes
Tearing at the weak foundations of a toll-bridge
Glittering with a strategic coating of sparkling sand
Tittering uncontrollably at a drenched philosopher
Gossiping with a dangerously drunk dryad
Twinkling on the surface of an especially limpid pool
Granting breath to a reformed bugbear
Understandably upset at an angler's giant bass catch
Haggling for gaudy glass beads with an enterprising trader
Untangling an otter from fishing nets, ruefully
Hauling sunken treasures up from the deep
Wading in waist-deep brilliant green clinging duckweed
Hurling sharp stones at wicked hobgoblins
Washing their diaphanous dresses to prepare for a ball
Impelling an illusionist to amuse them with magical images
Whispering sweet nothings into the ears of an errant knight
Inhabiting in a verdant, fern frond filled grotto
Wielding tridents tipped with piranha teeth
Jilting their former favorite for a handsome medium
Wreathed in bright bubbles from effervescent waters
Jumping into the drink from precipitous rocks
Yearning for tales of courageous and daring deeds

Table: human, noble
Acceding to a rival duke's demands for troops
Knighting a heroic neanderthal, under protest from their peers
Adorning themselves with expensive rubies and ermine
Knouting a blacksmith for failing to meet a horseshoe quota
Ailing from an injury, acquired in a battle long past
Lamenting the loss of a warship/boat to a giant squid
Appointing a seneschal for a keep on edge of their lands
Lauding frugality while spending excessively on new clothes
Auditioning a new medium to entertain and defend the court
Launching a cruel crusade against rival's religion
Banishing a former squire for courting her daughter
Levying burdensome fines on beard length to punish the dwarfs
Barking orders to insubordinate retainers
Listening disinterestedly to clemency pleas from soon-to-be widows
Beaming with pride at the birth of a son and heir
Lording imperiously, even though their claim is tenuous at best
Belonging to a secret, sororal order of avenging valkyries
Meeting with an envoy from a nearby goblin king to sue for peace
Beseeching their liege to exempt their lands from conscription
Meting harsh punishment to a thief accused of stealing a loaf
Besieging a bandit stronghold at their liege's behest
Ministering to the sick, ancient tradition holds their hand can heal
Celebrating a decisive victory over a dastardly ogre
Naming successor from among squires as he dies from cobra venom
Cherishing a hidden token of love from an infamous outlaw
Offering handsome pay for a detailed survey of a new lands
Commending a retainer for bravery, awarding a fine horse
Ordering their retainers to seize a charlatan alchemist
Conquering a crippling fear of poison by holding a huge feast
Outlawing most art, after embarrassing etching came to light
Cowering from angry serfs, sharpening axes to redress despotism
Overthrowing their ruthless and repressive mother
Declaring an unpopular edict - holidays cancelled for the duration
Pardoning a murderer after receiving a substantial bribe
Demanding fealty from local dwarfs, and being rebuffed
Petitioning liege for new titles to grant to their friends
Deposing a high priest, to their subject's abject horror
Plotting alongside ladies in waiting to commute an unfair sentence
Descended from a cruel tyrant, eager to amend their family's legacy
Presenting an ornate sword to the first to defeat an evil ogre
Desperate to adopt a fair-haired heir
Presiding over a local fishing dispute sagely
Dispatching messengers to all corners of their kingdom
Proclaiming an attractive bounty on bandits and brigands
Distracting themselves from official duties with falconry
Quartering soldiers in temples/shrines, upsetting priests/gods alike
Elevating their cronies to cushy positions of power
Refusing to raise grain taxes despite repeated requests from liege
Entombing a beloved spouse, died under suspicious circumstances
Rejoicing after a rare book shipment, short-lived - one's missing
Entreating with elfs for assistance with a hobgoblin invasion
Remarrying for the th time, last husband found bloodless/pale
Equipping armies with weaponry confiscated from adventures
Renouncing her title to take up study in the magical arts
Exiling true heir apparent under fraudulent pretenses as regent
Replacing important officials with sycophantic toadies
Fomenting sibling rivalry between her two sons
Reviewing plans for the construction of a new castle
Foolishly braving an outbreak of dire plague to visit an oracle
Ruling fairly, but prone to bouts of unbelievably bleak depression
Forced to abdicate at the point of their twin brother's sword
Sentencing a spy to seven years of hard labor
Forfeiting their claim to a new title with an accidental snub
Squinting at a proclamation signature they don't remember signing
Freeing a beloved bandit, after considerable public pressure
Strategizing with mercenaries on invading neighboring kingdom
Frowning as a scribe reads them a valuation of their holdings
Subjugating a peaceful lizard man settlement out of xenophobia
Genuflecting repeatedly, to practice for a visit from a saint
Succeeding a beloved cloud giant monarch soon, big boots to fill
Granting an audience to an envoy from the gnomish kingdoms
Summoning suitors for a homely stepdaughter from distant lands
Grieving over the loss of their son, mandating mourning
Surreptitiously arranging for the assassination of a rival
Grudgingly betrothing only daughter to a wicked wizard
Taxing dungeon takings, claiming most for the crown
Harshly horsewhipping a stable boy for a minor offense
Tolerating an extremely satirical jester's performance, barely
Honoring their fallen squire with a state funeral
Trusting corrupt advisors to handle affairs while they carouse
Hunting a ferocious boar for sport with their retainers
Tyrannizing vassals with draconian curfews/brutal enforcers
Imposing ruthless taxation to fund his exotic monster zoo
Unpopular decree - all must salute their foppish hat, placed on a pole
Impressed by a dwarf demonstration of new siege weaponry
Usurping authority from older sibling with help from a harpy
Imprisoning any veterans who refuse to swear fealty
Utterly convinced that a local bard is behind a recent rebellion
Inheriting a kingdom in the throes of a brewing civil war
Visiting subjects, unconvincingly disguised as a humble beggar
Invading a barrow-dotted land to smite the undead scourge
Wincing as they witness an execution, carried out on their orders
Inviting adventurers to a feast, pretext for hefty taxation
Withdrawing increasing sums from treasury to satisfy blackmailers
Jousting in a tournament soon, wanting to win at any cost
Years of skirmishing with berserkers are taking their toll on morale
Justifiably paranoid of doppelgängers
Yielding to defeat in a duel over a consort's affection
Keeping a dreadful secret, locked in a tower, fed peasants daily
Zealously funding church construction to break a bloodline curse

Table: human, nomad
Anxiously camping in hobgoblin territory
Marauding after being swindled by a charlatan
Arriving in an area where their people are persecuted by locals
Masterfully training eagles and falcons to assist with hunting
Attired in incredibly colorful outfits of amazing artistry
Milking their small titanothere herd, carefully
Baking highly nutritious, nutty flat breads
Moving all buildings in their camp to face a different direction
Betrothing attractive sons to local nobles to cement relations
Navigating mostly via omens and signs from their shaman
Breaking camp to move their magical goats to new pastures
Negotiating for an ogre-held hostage's return
Breeding exceptionally beautiful steeds, known for their speed
Offering delicious food and warm shelter freely to all visitors
Carefully scouting a settlement, abandoned overnight
Officiating a marriage between the scions of chieftains
Carrying large jugs of water, won't drink from sources here
Owning livestock in this culture is a sign of holiness
Catching basket loads of fish from a large lake
Painting sigils/signs on the trunks of trees in a secret code
Celebrating an auspicious event - birth of an albino camel
Passing through a region plagued by bandits
Charging exorbitant prices for "hospitality"
Pitching their tall tents and unfurling pennants and flags
Conquering their xenophobia by treating with dwarfs
Playing some complex strategic board game
Continuing an age-old tradition of weaving rune-rugs
Plundering a merchant caravan, all guards turned to granite
Controlling access to an important ford, bartering for tolls
Practicing a now outlawed form of religion in secret
Dancing joyfully to unusual, but extremely catchy music
Quietly bivouacking, mute as they mourn a dead cleric
Drawing water from a natural spring
Quizzically studying a captured spell book
Dwelling in conical yurts that disassemble quickly
Racing their strange, four-horned horses competitively
Earnestly considering settling here, once dragon is dealt with
Raiding an abandoned watchtower for anything of value
Embroidering the hems of their warrior women's dresses
Raising their tents with the help of brightly painted mules
Encouraging a sow to farrow with special herbs and plants
Relaxing on padded woven mats that float inches above the floor
Farming seasonally, sowing only quick growing tubers
Remaining in the area, even after receiving stern warnings
Fashioning a crude wall around a settlement with logs
Repairing a damaged golem porter, hauling their homes
Feasting at the behest of their seer, predicts lean times ahead
Riding in a gorgon rodeo, miraculously immune to their breath
Fighting with a stubborn mule, ascending a steep slope
Roving from village to village, planting a strange flower in each
Flocking around an itinerant trader for news of new lands
Saddling their camels, preparing to war with an orc tribe
Following the migrating herds of elf, their main source of food
Scattering the ashes of a cremated munificent gold dragon
Foraging for wild onions near a crocodile-laden creek
Seeking a relic sacred to their people, on display in a shrine
Garbed head to toe, with only flashes of scaly skin showing
Selling unusual weapons of masterful make and style
Gathering their flock of emu-like fowl
Settling in for the season, having made peace with gnolls
Grazing their horses near a grass-covered barrow mound
Shepherding according to ancient custom - flocks of driver ants
Guiding some hopelessly lost gnome merchants home
Singing songs of joy that seem to carry for miles
Haggling over horseshoes with a local centaur smith
Sitting at the base of a treant to rest from berry gathering
Harvesting normally poisonous fruit for special processing
Speaking nearly every language, with remarkable fluency
Hauling sledges loaded high with lumber for their stilt lodges
Starving themselves with ritual fasting, almost delirious
Heaping offerings on a local (and embarrassed) nixie
Stopping suddenly to assist a wounded griffon
Herding alpaca with startlingly luxurious coats
Supporting a falling bridge with backs, while a donkey crosses
Hunting bear - part rite-of-passage ritual, part supper
Surrounding a growling manticore with spears at the ready
Importing valuable, but fragile glassware from distant parts
Tending to novel gardens, planted within wheeled wagons
Influencing local diet with their uniquely addictive spices
Trading in pearls and seashells, some extremely exotic
Inspecting a cart for damage after righting it from a roll-over
Transporting their largely immobile, mummified elder
Invading elf territory, driven by an ancient enmity
Travelling on a sacred circuit that takes several centuries
Jailing a visiting acolyte for violating a taboo
Turning a squadron of skeletons with strange holy symbols
Joining forces with a band of halflings against a giant
Unjustly branded as thieves by the locals
Knitting new sails for their strange boat-like wagons
Utilizing hired goblin labor, with mixed results
Leading their livestock to a watering hole, under a lion's gaze
Venerating a fire elemental, trapped in an unburning cage
Listening politely to a proselytizing dervish
Wandering into a bugbear ambush
Living in huge, but still portable hollowed turtle shells
Warning all to stay away from an imagined disease they carry
Loading multi-horned oxen up with bundles of firewood
Wearing unique and dashing headgear, multiple piercings
Looking high-and-low for a lost elephant calf
Zealously welcoming strangers, with intriguing glowing eyes

Table: human, villager
Able to heal broken bones/burns with a touch
Hawking superstitious wind-chimes/mobiles
About to burn/just burnt a witch
Heavily taxed, to the point of destitution
Advertising a bounty on a local deaf and toothless giant
Hoping to marry off eligible bachelors
All whistling the same, terribly infectious tune
Hysterically laughing at a dead horse
Anxiously awaiting rainfall, last one was a doozy
Need a wizard to banish town's imaginary curse
Asking you to repeat everything. Everyone hard of hearing?
Infertile and desperate, bargaining with local fey
Assisting the priest as they bless holy water
Laying the cornerstone of a new church
Attempting to halt a runaway ox plowing the streets
Lugging buckets to fill a large boiling cauldron
Averting their eyes as you approach for at least an hour
Making a surplus of coffins and cradles
Baking delicious smelling breads and pastries
Manufacturing high-quality sand-candles
Banging pots and pans to scare away stubborn crows
Militia members, well-trained, to a one
Beating rugs, blankets and tapestries. Dust fills the air
Ministering to the wounded from a recent raid
Begging for news from other towns or the nearest city
Muttering "the prophecy" after everything said
Boarding up the windows/door to a hovel
Nervously awaiting the birth of a seventh son
Born with two teeth and tails, and proud of this
Offering free room/board for help with harvest
Brandishing lit torches, even during the day
Only speaking in questions. Why?
Burning books with a focus on religious texts
Painting evil-eye protection symbols on all doors
Carrying around the skulls of their favorite ancestor
Paying handsomely to help dye fabrics
Carting refuse to a smoldering trash pit that smells lovely
Poking a caged werewolf (sad gnoll) with sticks
Celebrating the birthday of a dead local hero
Preparing burlap-booted geese for market
Charing prayer scrolls for ashes to waft in the breeze
Pretty sure the party are faerie folk
Color-blind and dressed in tacky tatterdemalion attire
Raising the bounty on a local sheep rustler
Constantly complaining about an odor that you can't smell
Raking gravel to upgrade the roads
Constructing a giant wicker wyvern effigy
Recovering from a plague and keep a wide berth
Coping with the aftermath of a tornado
Reeling from a recent landshark ambush
Crowning an ugly, horrifyingly corpulent sow queen
Re-furrowing the zig-zag irrigation canals
Dancing wildly to a piper's poorly played tune
Re-thatching roofs and sweeping stoops
Dealing with a building that just caught fire
Returning with a catch of fish. Ones a whopper
Desperately in need of a smith to shoe their single horse
Roasting a huge dire boar for a town-wide feast
Digging a new well and swearing up a storm
Ruled by an ivory golem who speaks once weekly
Discussing a stone tower that sprouted in the field last week
Running to fetch priest from the next village over
Dragging sledges of firewood and furniture to burn
Schlepping a grain sacrifice to local lake spirit
Dredging the pond for missing child
Scrubbing/sloshing - village-wide laundry day
Each capable of casting a single st level magic-user spell
Sharpening stakes and crude spears, sullenly
Eager to exchange a pouch of platinum for copper
Shuttering windows and locking doors
Electing a new magistrate (ballot by blade)
Somberly stoking a funeral pyre
Erecting a windmill, architecturally precarious
Splashing water on everyone for a local festival
Eschewers of metal and highly worked goods
Striving to rescue someone who fell into the well
Extremely friendly to demi-humans, bordering on worship
Struggling to lever a large boulder
Far too fecund, every mother has quadruplets
Suffering from pellagra/scurvy
Flying colorful kites to ward off evil spirits
Tapping kegs/barrels for a seasonal vintage/brew
Foisting free strange-eyed kittens on every party member
Tending to a very pregnant sacred cow
Forming pleasingly uniform mudbricks in molds
Throwing stones at a travelling peddler
Genuflecting obsequiously and calling you lord/lady
Towing a large boat through town
Gesturing for silence whenever spoken to
Watching a fire breather entertaining children
Getting hoodwinked by a lumber merchant
Trying to gird necks with floral/garlic garlands
Ready to sacrifice their dozen eldest to a local wight
Very tall and broad, claim it's troll-blood
Giving away as many surplus tuber crops as they can
Wantonly smashing pottery and crockery
Hanging colorful pennants/flags for an upcoming festival
Wary from a charlatan who sold them snake-oil
Hauling loamy compost to their fallow fields
Wearing their clothing inside out and backwards

Table: octopus, giant
Adhering to the underside of a passing ship to hitch a ride
Jetting a plume of ink in the eyes of a sea troll
Altering the texture of their surface to perfectly match a reef
Juggling a wailing buccaneer from arm to arm
Angrily wresting an oar from a smuggler's dinghy
Looming as a dark blot, just below the sea surface
Attacking a group of pearl divers who disturbed their rest
Lovingly tending dangling strings of halfling-sized eggs
Battering a longship, as berserkers try to haul it ashore
Lugging a barnacle encrusted magic anchor wherever it goes
Biting an anchor chain clean in half with its powerful beak
Luring a sloop onto a sandbar for easy pickings
Breaking the surface to peer dully at a passing pirate ship
Lurking inside the bleached shell of a once enormous sea turtle
Burrowing in bone-white sands, to ambush prey
Marooned in a very large tidal pool during a hurricane
Camouflaging itself as kelp with beguiling chromatophores
Menacing a coastal community by sinking trading ships
Carefully clamping a tremendous dire urchin
Mimicking a small, rocky island among the waves
Changing direction suddenly with powerful jets of water
Moving massive boulders into an eldritch arrangement
Choking four helpless crew members simultaneously
Opening lobster pots and dining casually on the contents
Churning up massive amounts of seafoam as they surface
Outflanking the four heads of a sea hydra
Clinging to the starboard side of a schooner
Overturning a lifeboat full of starving, sea-mad sailors
Clouding a stretch of sea with tenebrous ink
Playfully grappling with a storm giant companion
Clutching a statue of a minotaur, gilt and inset with gems
Plucking tasty water termites from their maze-like nest
Coiling an arm around the mast of a makeshift raft
Pounding an intrusive pier to smithereens
Completely capsizing a storm wracked cutter
Pouring forth out of a surprisingly small crevasse in the seabed
Consuming a struggling seal
Protecting a stone-strewn shoal, where nixies dwell
Contracting after being shot with a flaming arrow
Prying open a pirate's sunken treasure chest
Cracking open the shell of a massive giant crab
Pulling on fishing lines out of curiosity
Crawling rhythmically along the sea floor
Quietly seizing single sailors as they serve a sting on watch
Crushing a clam, the size of a pony
Recoiling as a dwarf's powerful axe swing severs an arm
Decorated with vibrant blue, bioluminescent rings
Releasing their grasp on an acolyte after a magic missile strike
Devouring a mutineer, tossed overboard by vote
Restraining a tiger shark with five arms still free
Drowning a dolphin in its writhing clutches
Shooting through the brine with breakneck speed
Dwelling in an ornate shrine, sunken by ancient cataclysm
Snatching a screeching harpy out of the air
Eating constantly, barely any life remains on a barren seabed
Splintering floating wooden crates in search of an evil idol
Embracing a sunken shipwreck sullenly
Sprawling in the shallow surf, soaking in the warm seawater
Emerging from a massive undersea cavern to hunt
Squeezing and snapping the ribs of a small pilot whale
Ensnaring a sinking scow to tow toward the shore
Squirming its way around a school of frightened fish
Escaping from the jaws of a slavering sea serpent
Squirting ink ashore, barreled an enterprising alchemist
Evicting fishermen from their lagoon by tossing boats ashore
Staring balefully with an eye the size of a buckler
Extending an arm onto shore to shake fruit from a tree
Strangling a seven-foot sea snake, a mass of knots
Feeding on shield-sized scallops
Submerging suddenly after being struck by a lightning spell
Ferociously thrashing after being stung by a giant rockfish
Tearing apart a helpless sea turtle
Floating lazily in the shallows, digesting a large lunch
Throttling members of an aquatic ghoul pack
Forcing an arm through a porthole, shattering the thick glass
Toppling the timbered masts of a reef-bound boat
Gouging huge holes in a hull with their bird-like beak
Tossing a hogtied wave druid back aboard a ship
Grabbing goblins from the deck of an ill-built barque
Undulating rhythmically in response to distant whale song
Gracefully swimming among a colorful kingdom of corals
Unfurling suddenly to corral a clumped-up cod
Guarding an atoll, inhabited by a cyclops sage
Utterly enveloping a frenzied bull shark
Hauling long lost treasures from the deep to its den
Violently constricting a veteran who will sink like a stone
Heaving itself over a stone strewn skerries
Waving their arms frantically above the water
Hiding among thick corals from a hungry sea dragon
Wearing a magical coral crown that endows telepathy
Holding a magic trident in one of its arms
Worshipped by strange eelfolk and their undersea clerics
Hunting a migrating pod of orca
Wrapping their arms around a wooden bridge, tearing it asunder
Impatiently waiting for a seasonal sacrifice
Wrestling with a giant squid as awed sailors make wagers
Inadvertently summoned by a very scared sorcerer
Writhing their way ashore after a nearly drowned ogre
Inhabiting an abandoned merfolk shell keep
Yanking down the rigging of a foundering cog

Table: ogre
Abducting a prized oracular pig
Loafing on a moldering bed of hay, swatting stinging insects
Addled by the fumes of an ill-chosen firewood
Lobbing sacks of stinking manure at a group of pilgrims
Baffled by an ogre trail that leads to and from their "secret" lair
Lumbering loudly, patrolling the area
Bedeviled by blood-sucking ticks the size of silver coins
Messily eating the haunch of a moose
Being grilled by a nefarious magic-user after sleeping on watch
Netting a giant bass for breakfast
Belching boorishly after downing a large cask of vinegar
Nose to the ground, sniffing dervish tracks
Bickering with only companion - a motheaten, glassy-eyed bearskin
Nose-picking with gusto
Brawling with half a dozen brigands, and winning
Nursing a doozy of a hangover after stealing some gnomish spirits
Carrying off a starving family's cow as payment for "protection"
Obsessively repacking trusty sacks, coins trickling from holes
Catching a cold, sneezing and dribbling constantly
Offended by a lowball offer of coin for safe passage from a trader
Chasing after an albino giant rat that he's named zig
Ousting an owlbear from a decently sized den
Chewing on a massive raw onion
Outwitted by a canny bugbear - his precious sack is now full of rocks
Chucking empty amphorae down a cliff and clapping as they break
Peppered with pixie arrows, running for their lives
Clashing with a troop of white apes
Pestering a nearby village by trampling crops
Clutching a child's corn silk doll tenderly
Pigging out on a whole ox, roasting on a massive spit
Completely awestruck by a medium's paltry prestidigitations
Pitching a short-sighted plan in their churlish tongue
Confused by a pack of wily blink dogs
Prying open a locked chest with a bent short sword
Damaging a windmill by scratching his scabby back
Pursuing a rumor of elf gold buried in a churchyard
Daubing stinking mud on a rather embarrassing rash
Quaffing "magic potions" purchased from an enterprising kobold
Daydreaming about becoming a powerful wizard
Quarrelling with their tribe over who has the biggest nose
Driving a stolen herd of sheep into their cave for safe keeping
Raging in frustration after their sack went missing during a nap
Dumbfounded by a sack filled with weighty tomes
Rearranging tchotchkes and keepsakes on a rabbit pelt blanket
Enforcing for a hobgoblin tribe - they pay ten shiny coins a week
Rebuilding a barn, after stern admonishment from an acolyte
Eyeing a beehive with a red and swollen face
Rendering tallow to make stinking candles
Feuding with nearby neanderthals by poisoning their wolf-like dogs
Ridiculing their own reflection in the surface of a pool
Flinging javelins clumsily at a wooden dummy
Roaring loudly as they charge some now-frightened gnolls
Flushing out a duo of kobolds, bent on stealing his treasure
Robbing a merchant caravan, shoving ill-gotten goods into sacks
Flustered by a talking tree (hidden medium with ventriloquism)
Scarfing down armloads of mold-furred loaves of bread
Gambling with large dice - crude pictures instead of numbers
Scowling at a patrol of lizard men, armed to the teeth
Gnawing on their club due to a persistent toothache
Slurping out of cauldron, greasy stew dribbling down their chin
Gorging on a massive blackbird pie
Smashing a giant scorpion with an iron-clad club
Grappling with an enormous rock python
Snatching a dropped hare out of a fire and burning themselves
Grinning ear-to-ear as they count their coins
Sniffing a scent on the wind with large, hairy nostrils
Guzzling stolen cyclops wine from a waterskin the size of a sheep
Snooping around the outskirts of an adventuring party campsite
Heaving a large boulder into a pond to frighten nixies
Squeezing the life out of a squirming bugbear
Hiccupping uncontrollably, would do anything for it to stop
Stealing an unattended donkey cart, laden with rutabagas
Hindering hobgoblins by refusing passage without a toll
Strewing a trail of copper pieces toward a pretty obvious deadfall trap
Hopelessly bewildered and lost after following a will-o-wisp
Teasing a tied-up veteran with childish insults
Idolizing their leader - an ogre magi
Tending to a badly stubbed toe, toenail blackened and about to fall off
Inspecting a jeweled necklace with beady eyes
Throwing handfuls of dirt at a sleeping manticore
Jeopardizing a peace treaty - playing both sides of orc/goblin conflict
Trailing behind a group of mercenaries after they declined his help
Jockeying for rank in a highly competitive tribe
Tripping over a low wall/log
Kicking down a sturdy wooden door
Unleashing his primitive fury on a finely crafted mechanical music box
Kidnapping a dwarf diplomat, being lectured on how ransom works
Unloading a stuck wagon for some grateful farmers
Knitting brows in frustration after a boulder misses a warp beast
Upgrading clubs with extremely large femurs
Lapping water greedily at the edge of a pool
Usurping control of a goblin tribe after eating their king
Laughing heartily as a goblin jester performs some pratfalls
Vexed by an extremely simple riddle
Leading a local band of orc bandits, surprisingly charismatic
Wincing as a barbed elf arrow is yanked from his leg
Lighting a pile of rubbish on fire, failing to see the cask of oil
Wolfing down a bowl of steaming porridge with a ladle for a spoon
Limping after twisting their ankle in a giant ant dug hole
Yodeling simple rhymes in ogre and enjoying the echoes

Table: orc
Abandoning a lair, overrun with a rust monster infestation
Nocking quarrels in their crossbows, almost silently
Accumulating a remarkable collection of daggers and knives
Nursing horrible hangovers from potent pixie wine
Appointing a chieftain, after the other's death from old age
Obeying the sorcerer who has somehow enthralled their leader
Avenging a betrayal by former bandit allies
Offering bowls of coins to a manticore, reverently
Baking dense, un-spoiling bread in a large clay oven
Ousting a carcass crawler from beneath a sagging bed
Banishing a traitor out into the burning sun
Outsmarting a hill giant, trading copper for silver
Beaching a cave-barnacle covered coracle
Overthrowing the minotaur that usurped their chieftain
Bickering among themselves over which route to take
Pacing nervously before a shuddering stone door
Butchering a ten-point buck, arguing over the antlers
Panicking a group of satyrs with a well-timed ambush
Cauterizing a gnashing troll's severed arm with a torch
Patrolling the edge of their territory, ruefully examining tracks
Chewing on a oozing red root that encourages wakefulness
Pelting a giant bat with stones to drive it away
Confiscating a treasure chest from a group of kobolds
Placating a nearby vampire with regular prisoners
Curdling blood with the mournful keening of their horns
Poisoning a river to make a fishing expedition swifter
Cursing at a searing bright shaft of sunlight
Quarrelling so intently over a sausage, a halfling escapes
Dazzled from a medium's incantation, snarling and enraged
Raiding a nearby farmstead for livestock
Defending a magic pool that eliminates the need to eat
Ransacking the room of a cowering goblin king
Delivering an ultimatum to the lair of a rival orc clan
Rationing what little remains of their food supply
Descending a rickety ladder, into a dark pit
Rebuilding a crude defensive barricade with battered furniture
Eating lightly roasted, plump stirges on spits
Recruiting from the decimated ranks of a gnoll pack
Employing the services of a massive ogress, they call "sister"
Ridiculing another orc's extremely ostentatious helmet
Escaping from a collapsing tunnel, supports eaten by termites
Rustling cattle from a nearby werebear's herd
Exhorting the combat prowess of their leader in a toast
Savoring a odoriferous delicacy - pickled pegasus eggs
Fattening up a sounder of boar on unspeakable slop
Scattering a swarm of rats from a moldering larder
Fermenting a pungent mash in big copper vats
Scouting a well-travelled route for easy pickings
Fleeing from a ravenous ochre jelly
Seeking a relic, sacred to their clan, stolen by a gnome
Flushing out giant centipedes with addictive venom
Serving a surprisingly intelligent cyclops
Frustrating tomb robbers with devious traps and snares
Slamming metal tankards in unison, part of a drinking game
Gambling with a group of drunken lizard men
Snorting as they drag a dead troglodyte over to a crackling pyre
Gloating incessantly about a recent military victory
Stabilizing an injured comrade, bleeding from a ghoul claw
Grappling, unsuccessfully with a ravenous rhagodessa
Subduing a sun-mad acolyte with a swift blow the head
Grumbling at their meager rations of rum
Swearing numerous oaths to their ancestors
Guzzling loud sips of brackish water from their canteens
Tackling a crocodile as part of a coming of age ceremony
Harvesting slabs of shrieker fungus with wax-stuffed ears
Taming a pack of hellhounds with tasty charcoal
Hijacking a hobgoblin supply wagon
Tattooing their bravest with mystical symbols
Howling ancient ballads concerning the moon's betrayal
Taunting an adventuring party into a well-concealed trap
Hunkering down after being singed by a rutting chimera
Thronging around a shipment of arms/armor to lay claim
Ignoring a clan wizard's warning, hunting in areas off-limits
Toiling to build an unsound wizard's tower
Inhabiting an old elf crypt, using niches as bunks/storage
Toppling several large trees for lumber, angering a dryad
Investigating a distant clattering sound, cautiously
Uncorking a wine bottle and sniffing the contents warily
Jeopardizing a mutual aid agreement with gnolls by dawdling
Undermining the wall of a nearby keep with long tunnels
Knocking over several life-like bugbear statues
Unleashing their pet tuatara lizard on any interlopers
Laughing at a simpering gargoyle's off-color jokes
Unloading their ammunition on a screeching owl bear
Launching a sortie against encroaching skeletons
Unsheathing an iron blade that dampens light
Limping after a crossing an area drizzled with brutal caltrops
Urging each other across a very treacherous looking bridge
Lugging a huge, expertly carved wooden statue of a lion
Venerating the shadows that sometimes feed on them
Marching under the banner of a local human noble
Volleying eagle fletched arrows at a circling wyvern
Masterminding a plot to unseat a nearby bishop
Walling in a disappointing diplomat with bricks and mortar
Menacing a dwarf mining camp by stealing food and mules
Withdrawing into a more heavily defended redoubt
Milking large and lumpy goats, adapted for life underground
Xenografting portions of a giant crab onto their bodies
Negotiating with a brigand leader for more protection money
Yanking a rope to toll a clamorous alarm bell

Table: owl bear
Absolutely overwhelming an orc war band, all feathers & fury
Nodding and moving their rotating head in quick circles
Accidentally uprooting a tree by leaning against it to scratch
Obeying the orders of a lanky druid
Ambling confidently through noisy, skittering leaf-fall
Occupying former ogre den, old owner growing colder in the corner
Appearing only as a set of glowing, frontward facing eyes
Opening tough-skinned melons, feasting on sticky, juicy flesh
Balefully puffing up their feathered mane to appear larger
Pawing at a large, rotting log to set it rolling down a hill
Banishing cubs who are large enough to fend for themselves
Peering out of their deep and dirty burrow, groggy but wary
Barreling through the brush after a bandit
Piercing a crying cleric's breastplate with their barbed beak
Battling another over territory, with snarls and beak-snaps
Plucking dagger-sized silvertip feathers, growing too long
Charging ferociously into a formation of hobgoblins
Practicing their pounce on a massive spotted mushroom
Chasing a cougar up a tree, growling and rending the bark
Preening and puffing the flammulated plumes lining their face
Clawing open a chest containing rations with wicked talons
Preying on a halfling rancher's goat herd, lost three this week
Croaking loudly from a perch atop a precipice
Protecting juveniles from a hungry hippogriff
Crouching on hind haunches, about to pounce on a pegasus
Prowling in dappled darkness, surprisingly silent
Digging deep gouges, unearthing a giant rat burrow
Rampaging and riled - crossbow bolts buried in their shoulder
Disturbing a dervish prayer ceremony by hooting ominously
Regurgitating a pellet, in the fur and bone shines a gauntlet
Dragging a dead deer in its razor-sharp beak
Returning to a favorite ambush location, and hunkering down
Dropping a dwarf who wisely decided to play opossum
Roaming the edge of their territory, sniffing a boulder ruefully
Dwelling in an abandoned mineshaft where seams still sparkle
Rolling around on an ant nest, acid from angry ants kills parasites
Echoing distant screams and shrieks, hissing occasionally
Ruffling their tufted shoulders to appear much larger than they are
Emerging from a tangled burrow at the base of giant tree roots
Running on thunderous paws after a squealing boar
Enthralled by a very frightened, flute playing bard
Savaging several skeletons with a single swipe
Fattening up for hibernation on an unfortunate dairy cow
Settling down to finish their bugbear breakfast
Feeding slender strips of flesh to chirping her cubs
Shambling and bruised from a recent bout with a troll
Filling the air with resounding calls - mating season approaches
Shivering their shoulders for feathers to fall back into place
Following a scent, beak to the ground and snuffling
Shredding a sturdy oaken door with massive, sword-like talons
Gazing tigerishly at a group of thouls cooking their dinner
Shrieking as they lunge at a one of the circling wolves
Gingerly turning large speckled eggs over in a downy nest
Snapping their beak with hollow clacks as they sharpen claws
Gnawing on a magic saddle, no horse or rider in sight
Snarling as a giant rattler tries to slither away
Grabbing a flailing gnome in their beak to carry back to their den
Sniffing wide gouges in the rock for signs of rival males
Growling through a clenched beak as they scratch irritating fleas
Squeezing a veteran to near unconsciousness in their powerful arms
Hooting malevolently and turning the blood of listeners cold
Standing on her massive haunches - trying to reach a treed acolyte
Howling in a blood-curdling fashion, their hind leg snared in a trap
Staring down a path with yellow, unblinking, dinner-plate sized eyes
Hunting with a handicap - a large jagged chunk is missing from beak
Startling a summoner, expecting an owl familiar
Interrupting the rest of an otherwise distracted adventuring party
Surprising a party of dwarf prospectors, panning a stream
Itching between the shoulders, moaning as they scratch on trees
Swiping aside the spears of a band of brigands in formation
Jerking their head backwards as they attempt to swallow a lamb
Threatening to delay the opening of a goblin market
Jumping onto the back of an oblivious elk, raking with claws
Trailing the wounded warp beast that slew her only cub
Keeping a clutch of eggs warm with her own harvested down
Unhorsing a charging knight with a well-timed talon
Launching herself at lizard men hunters
Unleashing a piercing roar as they clobber a kobold
Listening intently to the sounds of brigands setting up camp
Vigilantly drinking from a sparkling pool of water
Looming forebodingly behind his ranger companion
Violently shaking a giant gecko, clamped in their beak
Loudly landing after falling off a perch that couldn't support weight
Visiting the kindly old witch who once removed a thorn from his paw
Lugging an ewe with brilliant gold wool along the muddy ground
Vociferously screeching, causing flocks of birds/bats to take flight
Lumbering woozily from captors, rattling chain dragging behind
Wallowing, knee-deep in mud, looking for tasty mollusks
Lunging at a sneering manticore, face pincushioned by quills
Watching two males clash with intense interest
Marauding after the death of their mate
Whistling to tell cubs to hide or climb, after sensing a predator
Mauling a medium, collecting pellets for dissection
Wounding both a warrior and a wizard with separate swipes
Mocking a trapper by disabling a deadfall
Wrestling playfully with adopted father - a werebear in human form
Moping and mud-covered after falling into a river
Yawning and stretching after leaving their bone strewn den
Nest-building, one larger piece is actually a gnarled magical staff
Zealously worshipped for their ferocity by a nearby clan of berserkers

Table: pegasus
Adorning a bower with bright blue flowers as colorful courtship
Nibbling gingerly on salty mineral deposits to expose them
Alighting on a verdant hill bearing bushes with big, ripe berries
Nudging a self-conscious acolyte toward a forgotten shrine
Ascending into a cloudbank, trailing a plume of soft white brume
Nursing two foals, one pearlescent, the other deep, oily sable
Baulking, lowering her head to challenge a chattering chipmunk
Overlooking treetops from a high perch, after smelling dragon
Bucking and bothered, tormented by a thirst of stirges
Overtaking a motley band of egg-stealing kobolds
Careening for cover, barely dodging a leafy canopy
Pampered, mane and tail meticulously braided by a lonely dryad
Carrying a timorous rider, eyes shut/head buried in the mane
Panicking a nye of pheasants by landing in their field
Charging to scatter a pack of prowling wolves
Parading with outstretched wings before disinterested mares
Chomping with satisfaction on an abandoned basket of carrots
Perching on a cliff's edge, tugging a dangling bard's cloak
Clattering with a canter down a road in desperate need of repair
Playfully chasing a pleasure of pixies through bearblossoms
Climbing abruptly, out of the range of hobgoblin arrows
Plucking fat, juicy cherries from branches, staining mouth red
Coasting to a slow stop, mere inches above the ground
Plunging in a twisting dive to outmaneuver a hungry hippogriff
Considered a sacred omen, fearlessly protected by lizard men
Prancing up to a pond to genuflect before a nixie
Crunching as they trot through deep piles of dead leaves
Preening their wings fastidiously after a recent rain shower
Descending toward a precarious and largely inaccessible nest
Pulling an ornate chariot with a broken axle, frustrating/noisy
Desperately dogfighting with two screeching griffons
Quickly divebombing a group of fearful goblins
Dramatically plummeting to show off bravely for the herd
Racing affably with a unicorn, across a sweet-smelling meadow
Drinking from a trickling, crystal-clear spring
Rallying to right a wagon with a cleric pinned beneath
Drooping and singed wings betray a chimera encounter
Rearing on hind legs at the hiss of a cockatrice
Encouraging young foals to fledge from the nest with nudges
Receiving the attentions of a tender centaur with a hoof knife
Escaping from an ogre's massive net, hooves still tangled
Resting in treant shade, branches draped with hairy moss
Fidgeting and fussing from an un-scratchable itch
Roaming from wizard to wizard, looking for another reincarnation
Fleeing at the sound of gnoll war-cries
Roosting on a half-collapsed bridge, spanning a deep ravine
Flying low over a lake, belly barely brushing cattails
Running to gain speed, before leaping into flight
Folding and refolding their wings at rest
Scouting for potential predators before bringing foals to feed
Fretting near a ruined shrine, rider went in and has not returned
Selecting sun-ripened fruit from high branches, hovering
Galloping with a herd of similarly striped zebra
Shying away from the outstretched hand of a neanderthal
Gamboling and frolicking in the beginnings of a brisk breeze
Skidding to a stop on stony gravel after a sudden landing
Gathering sturdy branches to weave together their first nest
Skimming tops of tall grasses, wings kicking up clouds of dust
Gently nipping their rider's shoulder for a few head scratches
Snorting to warn a moose, grazing too close
Giving wide berth to a temperamental gorgon grazing nearby
Soaring higher, a terrified halfling on her back
Gliding gracefully above treetops, looking for prime pasture
Springing to defense of a sacred stone circle
Grazing alongside a few grumpy titanothere
Stamping at barren ground and producing a trickle of water
Guiding an injured limping mate gently down a steep slope
Stealing a dwarf merchant's outrageous hat in jest
Harassing a crouched and growling cougar from the air
Striking a skull from the shoulders of a sword-wielding skeleton
Herding a mass of skittish deer, lightheartedly
Studying a snake haired statue, almost forlornly
Humoring an energetic foal, playing tug-of-war with a branch
Swerving to avoid the bolts of vicious harpy crossbows
Idly circling on rising thermals, flapping only occasionally
Swooping to dodge a cyclops' large lobbed boulder
Inconceivably trudging before a plow, pulling it down a furrow
Taking wing in unison, a truly breath-taking sight
Joyfully flapping their wide wings after a yawning stretch
Tamed mascot of a travelling circus not seen in centuries
Kicking both back legs, striking a troll square in the chest
Tenderly nuzzling a fair-haired knight as she laces her greaves
Landing unsteadily on a pile of bracken, stomping and shaking
Throwing back their head and shaking burrs from their mane
Lassoed and baying as bandits struggle to keep him terrestrial
Treading mercilessly on a hissing snake
Launching themselves from a tall bluff
Trotting cautiously on water-logged turf
Lining their nest with down and shed feathers
Unfurling magnificent ivory feathered wings to bask
Luring a wyvern away from their mate, incubating eggs
Vaulting over the crumbling walls of a massive open-air maze
Molting, pulling out crooked pinions with their teeth
Visiting friendly gnomes to be re-shod
Munching on a handful of oats offered by an elf
Waiting patiently by a bugbear cave for their paladin to emerge
Neighing softly to calm down a frightened foal
Wheeling to avoid the grasping talons of a wyvern
Nesting atop a dilapidated windmill, groaning in the breeze
Whinnying after catching scent of an owl bear

Table: human, pirate
Ambushing a large freighter, laden with exotic lumber
Licensed by a local lord of ill-repute (a secret devil swine)
Approaching a deadly reef, hoping to shake pursuers
Licking their wounds after a fierce fight with water termites
Attacking a fortified lighthouse, well-armed landing parties
Looting a littoral lizard man village for food and fresh water
Avoiding detection in a verdant, shielded lagoon
Lying low with the assistance of sympathetic fishermen
Battering an enemy vessel with their iron-clad prow
Mapping a treacherous route through a sargasso sea
Bellowing bawdy sea shanties at the top of their lungs
Marooning a mariner who inadvertently slew an albatross
Blackballing their cook after another abominable meal
Mutinying against their odious ogre captain
Blockading a busy bay with their mermen allies
Navigating with the uncanny aid of a blind medusa seer
Boarding a bilander, brimming with bolts of silk
Nimbly perching and balancing - all are ex-circus performers
Bullying a new member of the crew - a seasick medium
Off-loading barrel after barrel of profitable high-proof potables
Burying bountiful boxes of boodle in sandy soil
Overconfidently swaggering as shipworms eat through the hull
Capturing cargo from a completely surrendered clipper
Patching sails, perforated by a hail of hobgoblin arrows
Celebrating a successful recent raid by drinking to excess
Patrolling shark-infested waters surrounding their island haven
Chasing after an embezzling deserter, to mete out punishment
Peering through a looking glass at a distant dragon turtle
Christening a new captain, a tradition with ritual dunking
Plaguing a high-traffic trade route, most merchants pay a toll
Crewing a four-mast carrack, recently captured
Plotting to overthrow the druid that protects a coastal hamlet
Cursing loudly with wax-stuffed ears at an aerie of harpies
Plundering a shipwreck, only accessible when tides are low
Daring to raid a seaside keep for crucial supplies
Polishing boots and buckles, honing cutlasses and knives
Destined for the brine queen, according to an old salt
Praying to foreign and very vengeful sea deities
Discovering an atoll, rich in lumber, crawling with giant crab
Press-ganging capable adventurers at every opportunity
Dividing ill-gotten gains according to rank and tenure
Quick to use oil and kindling laden boats to set ships ablaze
Dragging a great white carcass behind their ship as a warning
Racing back aboard after underestimating coastal orcs
Drinking repeatedly watered grog, and desperate for alcohol
Recently returned from distant lands, hold full of exotic animals
Driving away a pod of dolphins with unlucky markings
Recording detailed accounts of their spoils in an old spell book
Drowning a naval spy, uncovered among the crew
Repairing the hull of a dinghy, bestrewn with barnacles
Dueling over naming rights for a recently stolen ship
Reputed to take no prisoners, but actually treat captives well
Ensorcelled by disgusting gull harpies, convinced of their beauty
Retiring after seizing a galleon containing a king's ransom in gems
Establishing trade with mermen for a newly founded haven
Roughing up a merchant ship captain to unlock a chest
Experiencing the first stages of scurvy, seeking citrus
Rowing out to greet the nixie that charmed them long ago
Fashioning a crude effigy of their cruel captain from rope
Sailing straight toward a colony of easily angered coral golems
Fleeing after seeing a sea serpent sprout of the starboard bow
Saluting their new/old captain - a one-eyed doppelgänger
Floating listlessly in a becalmed lifeboat, low on fresh water
Scourging a crew mate who fell asleep on watch
Flying a false flag - warning of mummy rot aboard
Seeking out their shares, following a magical map
Frantically foundering on windless waters, bailing constantly
Shipwrecked on a salt-covered island, teeming with rime wights
Freebooting with an elf frigate firmly in their savage sights
Signaling distress as a ploy to draw in victims
Frequenting a local tavern for tips on cargo shipments
Staggering, sea legs stolen by a vengeful cyclops
Gambling with a group of soldiers, someone is cheating
Storming a schooner, only to discover its crewed by ghouls
Grinning as their captain, a defrocked friar, sermonizes
Swabbing decks to prepare for a djinni visitor
Growling bellies betray ravaged food stores
Swinging from rigging into a frantic fray with complete abandon
Hauling up nets, containing cargo hidden from customs
Taunting a shark with a precariously suspended noble
Hiding their tiger shark lycanthropy rather well
Teetotalers, to a one - their former paladin captain forbids it
Hoarding fine gems and jewelry, to impress and woo on land
Trading with friendly island dwarfs, unfamiliar with magic
Impersonating famous privateers, known for a lack of mercy
Underestimating the tenacity of a giant octopus
Inspecting their ship for damage after a giant squid attack
Voting on whether they should maroon their minotaur captain
Interrupting a prisoner exchange, hoping to ransom both
Voyaging far too near a swirling vortex of water elementals
Jeopardizing crew safety by transporting a caged basilisk
Wearing antique styles of clothing and speaking old tongues
Just escaped from a local gaol, following the coastline
Weathering a howling gale, shredding sails and rigging
Keelhauling crewmembers who staged an unsuccessful mutiny
Weighing anchor after taking on oblivious passengers
Kidnapping a kobold captain of a rival fleet, after his map
Whaling a bit on the side, excellent narwhal scrimshaw
Lamenting the loss of their mascot - a dire rat named antius
Wrecking ships stranded on a submerged sandbar

Table: pixie
Advising a dour dwarf to lay down his axe
Leading a tax collector straight into an owlbear lair
Asking an apple tree for permission to pick
Lopping flowers from sunflower stems to practice swordplay
Attending a funeral for a unicorn
Loudly carousing with a hopelessly lost miller
Bandaging up an unconscious, bleeding ranger
Making umbrellas from enormous foxglove blossoms
Befriending a curmudgeonly owl familiar
Maliciously smiling as they trade magic beans for a cow
Befuddling a lama, tending to a roadside shrine
Maltreating a goblin servant
Being foiled by a traveler wearing her coat inside out
Manifesting suddenly to startle a sage
Bestowing supernatural gifts on a newborn baby
Meddling in a medium's summoning ritual
Braiding a dryad's season-matching tresses
Noisily roistering during a somber religious service
Cavorting around a ring of colorful toadstools
Nursing a beautiful berserker maiden back to health
Chastising a milkmaid for failing to leave tribute
Obeying their queen's edict - no armor allowed in the wood
Cheering as they defeat an odious ogre
Obscuring an obvious path with heavy fog and mist
Climbing about on a cromlech
Orbiting their orphan mascot on tiny, frantically beating wings
Confusing a woodsman by moving landmarks
Parading with prodigious pomp, on the way to a wedding
Cowering from distant church bells tolling
Picking only the ugliest blossoms from every flowered bed
Cutting life-size paper dolls from magical scrolls
Promenading beneath fragrant ornamental plum trees
Dancing merrily to talented cricket violinists
Punishing a greedy cobbler with cursed ever-dancing shoes
Defending an elfin barrow from interlopers
Puppeteering ogre bones invisibly - dead ringer for a skeleton
Defrocking (literally) an embarrassed friar
Quaffing wine that works like philters of love on mortals
Deterring an incursion of hobgoblins by blocking paths
Resting in caterpillar spun hammocks
Distilling dew and nectar into a potent brew
Revealing themselves to a lovelorn lycanthrope
Drinking wine, swindled from a cyclops
Reveling with several satyrs and abducted soldiers
Driving caterpillars from a friendly farmer's lettuce
Riding atop the segmented backs of giant centipedes
Dwelling within locally shunned hollow hills
Salivating as a trader displays her wares - mostly sweets/candies
Encouraging a pegasus foal to fledge
Saluting a legendary sprite champion
Extracting a thorn from the paw of a friendly blink dog
Serenading a giant toad, formally a princess
Fabricating a pair of magical shoes
Setting a tiny table for a lavish banquet
Fluttering in the face of a medium attempting to study
Sheltering from a sudden rainstorm beneath broad leaves
Following a squadron of un-spookable skeletons cautiously
Singing hoary pixie tunes that force listeners to smile for a week
Frolicking among beautifully blossomed bowers
Snarling roots to trip up a fleeing footpad
Gamboling around moss-covered dolmens
Spinning weightless and virtually transparent spider-silk shawls
Gathering gallons of amber honey from giant beehives
Stealing every left shoe they can lay their tiny hands upon
Giggling uncontrollably at a donkey walking upright
Stringing colorful garlands to festoon their arbor
Giving an acolyte and involuntary haircut
Stymieing a sneaking bugbear by placing loud twigs in his path
Gossiping with sparrows and nightingales
Surprising a stage magician by helping improve his act
Grinning ear-to-ear as a wily bandit tries to bargain for gold
Taming bats to serve as nocturnal mounts
Guzzling from empty goblets, but getting quite drunk
Tangling the hair of a haughty noblewoman
Hampering a bounty hunter from catching his quarry
Tending to a wounded lizard man
Harvesting bulbous berries from a talking bush
Terrifying a superstitious smuggler
Hiding a magic sword from a sleeping paladin
Toasting continuously to the health of their queen
Holding the change of seasons for ransom
Trimming the leaf-sails of lilliputian boats for a regatta
Humoring a grumpy treant, telling a very boring tale
Trundling tiny carts of wares to a faerie market
Imbibing magical mead from mithril thimbles
Turning up tiny noses to a tithe of soured milk
Imploring nixies to join their crusade against boredom
Unclasping any accessible buckles and straps
Inflicting terrible dreams on a sleeping adventuring party
Uncorking a bottle of wine with a spiral bladed sword
Jealously guarding a spring with incredible healing properties
Upsetting an otherwise unflappable mule
Jousting atop large frogs glamored to appear as horses
Vexing a prospecting gnome by salting every site with pyrite
Kidnapping an infant from an unattended bassinet
Visiting with local wood elfs to discuss a threat of orcs
Knotting the mane and tail of a knight's worried warhorse
Waking a grizzled veteran who has been asleep for a century
Laughing at a centaur, induced to do a jig
Waltzing wildly to the tunes of their bard hostage

Table: pterodactyl
Alighting on an ancient, moss covered lizard man statue
Migrating to warmer climes, stopping only to eat
Barreling into branches of the canopy, fleeing a predator
Peering from within verdant foliage, clucking periodically
Beating their membranous wings furiously to take off
Pitching and banking gracefully on warm thermals
Brooding over a conical, termite mound-like nest
Quietly squeaking to calm recently hatched young
Combing their bristling pycnofibers with their mouths
Regurgitating a meal for cacophonous nestlings
Croaking defiantly amidst obnoxious birdsong
Scavenging strips of rotting rib meat from a sabre cat kill
Diving suddenly after a smaller pterosaur snack
Scuttling among leaf litter with a wounded wing
Drinking awkwardly from a pool of water, vulnerable
Spreading wet wings to dry them out before taking flight
Dropping a tough-skinned fruit on the rocks to dash it open
Squawking loudly at an egg eating snake
Fanning each other to stay cool on a sunbaked bluff
Stealing a meal from a halfling adventurer's hand
Feasting on the carcass of a young stegosaurus
Taking wing suddenly after a distant explosion
Fishing on the wing - grabbing their catch with quick snaps
Tearing down a canvas tent to reach the food supplies inside
Flying low to the ground, chasing after a scurrying mammal
Unfolding painstakingly from a tightly wrapped nap
Gnawing on tree bark to clean their beak-like mouths
Waltzing in an aerial ballet as part of a courtship dance
Landing clumsily on a branch, barely big enough to support it
Wheeling in sudden turns to follow a formation leader
Altering their coloration to blend in with a tree trunk
Grabbing a holy symbol out of an acolyte's hand
Bristling with long, whisker like hairs
Hanging from the outstretched arms of a petrified priest
Chasing after a frantically hopping frog
Hissing loudly at a wounded gnome
Chirping like a baby alligator, inquisitively
Hollowing out a nook in a thick tree trunk to roost
Climbing up a distracted medium's robe
Licking nectar out of flowers the size of bucklers
Cracking open large, opal-shelled snails with sharp stones
Mimicking most sounds, rather remarkably
Dangling joyfully from a low hanging bough
Nesting in a dented, but heavily gilded helmet
Darting from tree to tree after a huge dragon fly
Snapping up large bees as they head home to their hive
Displaying vibrant eyespots on their wings to deter predation
Picking parasites off the back of a grateful triceratops
Eating slimy, over-ripe stink fruit and making a huge mess
Pouncing on a giant centipede, trying to avoid the venom
Flapping desperately in a rope-like spider web
Preening their fine proto-feathers with tiny, comb-like teeth
Flashing their bright bellies at an unimpressed female
Screeching after returning with a fish to an empty nest
Fleeing from the nets of kobold tamers
Snatching a thief's flung dagger out of the air to protect a druid
Flitting about after a thirst of groggy, blood-filled stirges
Watching a bandit's roasting boar hungrily from the trees
Foraging for wriggling grubs in a rotting log
Whistling a warning in call-and-response fashion to their flock

Table: pteranodon
Alighting on an ancient, moss covered lizard man statue
Migrating to warmer climes, stopping only to eat
Barreling into branches of the canopy, fleeing a predator
Peering from within verdant foliage, clucking periodically
Beating their membranous wings furiously to take off
Pitching and banking gracefully on warm thermals
Brooding over a conical, termite mound-like nest
Quietly squeaking to calm recently hatched young
Combing their bristling pycnofibers with their mouths
Regurgitating a meal for cacophonous nestlings
Croaking defiantly amidst obnoxious birdsong
Scavenging strips of rotting rib meat from a sabre cat kill
Diving suddenly after a smaller pterosaur snack
Scuttling among leaf litter with a wounded wing
Drinking awkwardly from a pool of water, vulnerable
Spreading wet wings to dry them out before taking flight
Dropping a tough-skinned fruit on the rocks to dash it open
Squawking loudly at an egg eating snake
Fanning each other to stay cool on a sunbaked bluff
Stealing a meal from a halfling adventurer's hand
Feasting on the carcass of a young stegosaurus
Taking wing suddenly after a distant explosion
Fishing on the wing - grabbing their catch with quick snaps
Tearing down a canvas tent to reach the food supplies inside
Flying low to the ground, chasing after a scurrying mammal
Unfolding painstakingly from a tightly wrapped nap
Gnawing on tree bark to clean their beak-like mouths
Waltzing in an aerial ballet as part of a courtship dance
Landing clumsily on a branch, barely big enough to support it
Wheeling in sudden turns to follow a formation leader
Blushing a brilliant crimson to intimidate a rival male
Laying their oblong eggs in a tiny furrow
Burrowing their beak into the carcass of a stegosaurus
Living among the crenulations of a massive ruined keep
Carrying an important scroll, tied to a hind leg
Opening their massive mouths in an unstifled yawn
Circling lazily, looking for easy prey
Perching precariously on a sagging branch
Cooling off with a quick splash on the surface of a lake
Plucking a neanderthal child from a riverbank
Crawling quickly along with its wing-claws, bleating
Preying on a shepherd's flock - reward being offered
Dazzling with a remarkably iridescent coat of fine follicles
Puffing up to try and scare away a gargoyle
Descending to investigate a terror bird kill
Roosting on impossibly tall cliff-sides, hundreds of them
Devouring a dwarf, dented armor and all
Sailing with the wind, clipping the occasional high cloud
Digging in warm soil with their sharp snout, gravid with eggs
Shifting the shade of their scales by flexing their wings
Drifting near a hungry griffon nest, full of fledging cubs
Shrieking with a blood-curdling sound, constantly
Extending a colorful dew lap to attract a mate
Skimming the surface of a stream with daring dives
Following a pack of hunting gnolls, hoping for easy pickings
Soaring just outside of elf archer range
Gliding majestically, were it not for the occasional yelp
Swooping suddenly at their hobgoblin rider's behest
Gobbling up a screaming goblin in a single bite
Waddling along a muddy beach, drilling for mollusks

Table: purple worm
Anchoring a row of massive, ogre-sized eggs to a ceiling
Impaling a giant with their horse-sized stinger
Arriving on the surface in time for a record rainstorm
Inadvertently burrowing through defenses of a dwarf enclave
Attacking a rival in their territory - a titanic struggle
Ingesting a rock living statue, going to suffer from heartburn
Bearing recent scars from a run-in with a deep dragon
Invading a minotaur's maze - now straightforward to solve
Belching forth miasmic gasses that wither plant life
Joylessly crawling across a battlefield, inhaling remains of fallen
Bisecting a corridor completely - a lumpy, violet wall of flesh
Laboriously creeping along a cathedral like lava tube
Boring up to the surface from the unseen depths below
Lethargically probing its way past an ancient ophidian temple
Breaking through the ground to swallow a herd of sheep whole
Migrating to cooler climates for reasons only known to them
Bulldozing an ancient gargoyle rookery, decimating their nests
Molting, wiry worm casts used as tough leather by troglodytes
Bursting forth from below - in the center of a magic circle
Moving a massive mound of dirt in their furrowed wake
Burying a thoroughfare under a huge amount of flung soil
Narrowly squeezing between massive, glyph carved boulders
Carrying a fabled magical spear, buried deep in its back
Noiselessly cringing as they plow a foul-tasting fungal forest
Carving strange, spiral gouges in the side of a mountain peak
Obstructing further passage as it slowly meanders past
Chewing through fossilized remains of prehistoric civilization
Only mouth breaks the surface - a trembling tooth rimmed pit
Clogging a mineshaft with its massive mauve bulk
Passing near a farmer's field and spooking livestock for miles
Coiling around the base of a wizard's tower - summoned in error
Perforating a mummy's burial chamber, now afflicted with disease
Consuming the entire blackpaw tribe of bugbear in a single gulp
Poised like a cobra, most of its bulk still buried under the ground
Contracting reflexively after being peppered by ballista fire
Poisoning a once pure pool with their odious bubbling bile
Cooling off from thermal vents by draining a lake from below
Preying on an entire herd of antelope - unable to escape its huge maw
Crushing the majestic stalagmite stronghold of the cave sprites
Reaching upwards to feast on roosting giant bats
Curling to confront a cave bear with their formidable stinger
Rearing, taller than a tower as archers turn pale with fright
Dangling from a cliffside, twitching to find suitable purchase
Retracting from whence they came called away by unseen forces
Debouching from a cramped valley to ravage an open plain
Rooting around the remains of a once thriving goblin kingdom
Destroying an ancient dam, built to protect a halfling village
Rotating as they auger through tenacious marble
Devouring a dozen crab spiders as they skitter in an attempt to flee
Rupturing from sandy soil to consume a camel
Discharging prodigious oily secretions to lubricate their digging
Scouring the sides of a tunnel smooth with their acidic coating
Distressing lizard men, fearing ancient prophecy has come to pass
Shrieking with an indescribable, terrifying wail as they mate
Dragging the bloated corpse of a rival around in its jaws
Slithering just below surface, creating sinkhole traps for herd animals
Dredging, half buried, dining on a driver ant colony
Slurping a caecilia like squirming spaghetti
Drenching a platoon of pikemen in disgusting blue ichor
Squirming in response to a sorcerer's powerful spell
Drilling through worked walls like a warm knife through butter
Stinging incautious orc hunters, trying to sneak behind it
Drugged with powerful narcotics - a wall for a hobgoblin fortress
Stinking with odor that makes the bravest dwarf tremble with fear
Eating each of the trained trees in an elf settlement
Stirring after an eon long sleep, will be ravenous on fully waking
Emitting a foul charnel stench, detectable for miles
Stretching skyward snapping at a furiously flapping griffon
Encased in a brittle shell of stone after snacking on a basilisk
Surfacing to vomit forth a particularly resilient ranger
Erupting suddenly from soil, swaying before striking a roc on wing
Swallowing a prepared sacrifice and most of the attending acolytes
Excreting a mucus, prized by alchemists for transmuting minerals
Swelling as a swallowed medium quaffs a potion granting titanic size
Extruding through an archway, cracking/crumbling the stonework
Thrashing at every stab from stubborn gnoll spearmen in its gullet
Feeding all manner of oozes/jellies with its nutrient rich ordure
Tolerated by farmers by tradition - phenomenal for fertile soils
Fiercely piercing their stinger into the ground repeatedly
Transporting deep gnome merchants w/ protective magical amulets
Flailing their stinger to shake off a very upset, still living troll
Tunneling between deep dungeon levels, on its way to the surface
Glistening with foul-smelling sweat, would make a ghoul wretch
Turning around, or attempting to, in order to bring its stinger to bear
Glowing due to flecks of gemstones, embedded in it's fibrous hide
Uncomfortably digesting a desperate, dual-dagger wielding thief
Gnawing its way slowly through a dense deposit of granite
Undulating its way underneath a noble's keep, shaking the walls
Gorging on a gnome city - refusing to listen to reason
Unwittingly channeling a new river as it snakes across countryside
Greasing entire tunnel in its wake, slippery and slick with secretions
Violently writhing as kamikaze kobolds cling and stab
Hollowing out a large cul-de-sac for impending hibernation
Weaving a gargantuan cocoon out of silk and scavenged steel
Howling thunderously, swallowing an adventuring party whole
Withdrawing into the ground after the early arrival of a giant roc
Hurling itself at a humongous hammer handed golem
Wounding a red dragon before retreating from the fiery breath
Ignoring a druid's frantic pleas and decimating a sacred grove
Wrapping around a colossal statue of a titan and slowly constricting

Table: rat
Awkwardly struggling to squeeze through a too small hole
Muffled scratching as more maneuver within the walls
Befouling an otherwise perfectly pure water source
Nesting abaft an overturned table, shoved to the side
Carrying a virulent strain of the dreaded berserker pox
Noisily rummaging through a pile of refuse
Clustering in a corner, behind a broken crate
Periodically peeking out from darkened bolt holes
Conjoined at the tail - a disgustingly fascinating rat king
Racing after a colony member, hauling a cave locust leg
Contaminating a barrel of recently winnowed grain
Riddled with disease bearing fleas
Cowering from a bandit, brandishing a bright torch
Roiling en masse from beneath a threadbare rug
Deftly swimming across a brackish pool, wet and glistening
Scurrying to-and-from their hiding places throughout the area
Eating the hems of a faded and dusty tapestry
Sniffing the air with pale twitching noses
Flensing an unfortunate fighter, already looted of arms/armor
Spoiling a hungry halfling's supper with their presence
Flicking long whiskers as they snuffle about for food
Squeaking loudly as they squabble over a stale chunk of bread
Gathering at the behest of a nearby vampire
Tenaciously chewing through an important, knotted rope
Gnawing deep gouges in the bottom of doors/furniture
Utterly famished from lack of food, eyeing each other for weakness
Investigating a dropped backpack inquisitively
Veering into corners after sensing distant footfalls
Leaping across very sturdy shelves
Writhing in a seething ball of fur and teeth
Absconding with a ring of keys as a hobgoblin jailer shouts
Infesting a chest used to store clothes, only stinky rags remain
Bruxing on the cloth wrappings of a stack of cheese wheels
Jumping onto the legs of an acolyte aghast
Burrowing into the body of a dead giant scorpion
Knocking over glasses/vials as they scurry across a shelf
Caching shiny things, including coins in their little nests
Landing on a brigand, biting/scrabbling as they jockey for position
Clambering along a high, thin ledge lining the ceiling
Lurking within a cupboard/cabinet among sawdust and droppings
Congregating around an offering bowl of runny goats' milk
Nibbling on the edges of a massive, leather bound tome
Cornered by a viciously barking, diminutive dog
Overwhelming a driver ant
Dangling from gnawed through ropes, suspended from the ceiling
Proliferating due to an abundance of forage, rancid nests everywhere
Darting beneath a discarded tower shield
Scampering from bolt hole to bolt hole
Dispersing rapidly as a lit torch falls from its sconce
Skillfully scaling a stiff chandelier chain
Erupting from a crack in the wall, ravenous
Squealing as they avoid the footfalls of a determined ogre
Feasting on a fallen bat
Swarming around a one rat who drank a potion of control humans
Fleeing from the footsteps of an orc enforcer
Teeming with ticks and fleas, scratching their patchy fur
Freezing in place as a slithering snake slides past them
Uncorking an expensive vintage of champagne with a loud pop!
Hoarding seeds, one magic - grows into tree instantly on planting
Zipping to avoid a hungry giant centipede

Table: rat, dire
Awkwardly struggling to squeeze through a too small hole
Muffled scratching as more maneuver within the walls
Befouling an otherwise perfectly pure water source
Nesting abaft an overturned table, shoved to the side
Carrying a virulent strain of the dreaded berserker pox
Noisily rummaging through a pile of refuse
Clustering in a corner, behind a broken crate
Periodically peeking out from darkened bolt holes
Conjoined at the tail - a disgustingly fascinating rat king
Racing after a colony member, hauling a cave locust leg
Contaminating a barrel of recently winnowed grain
Riddled with disease bearing fleas
Cowering from a bandit, brandishing a bright torch
Roiling en masse from beneath a threadbare rug
Deftly swimming across a brackish pool, wet and glistening
Scurrying to-and-from their hiding places throughout the area
Eating the hems of a faded and dusty tapestry
Sniffing the air with pale twitching noses
Flensing an unfortunate fighter, already looted of arms/armor
Spoiling a hungry halfling's supper with their presence
Flicking long whiskers as they snuffle about for food
Squeaking loudly as they squabble over a stale chunk of bread
Gathering at the behest of a nearby vampire
Tenaciously chewing through an important, knotted rope
Gnawing deep gouges in the bottom of doors/furniture
Utterly famished from lack of food, eyeing each other for weakness
Investigating a dropped backpack inquisitively
Veering into corners after sensing distant footfalls
Leaping across very sturdy shelves
Writhing in a seething ball of fur and teeth
Awful, yelping screams as a kobold is attacked
Injuring a carcass crawler, as others crouch in motionless rage
Biting crunching chunks out of a dead crab spider
Latching onto the leg of a lizard man, hissing in pain
Bullying the runt of the colony
Mobbing a merchant, hopelessly lost and frightened
Chasing after a distressed cat, tables having turned
Panicking a peasant armed with only a pitchfork
Conditioned to trigger a secret door if offered food
Ravaging stores, stockpiled for a brutal winter
Creeping up on a medium, studying her spellbook
Scrambling to get out of the way of a quivering ochre jelly
Defiling a once beautiful shrine with their mangy chattering
Snarling confidently at a goblin bodyguard
Devouring some sacks of moldering and stinking potatoes
Startling a thief, listening at a door
Dragging an unconscious cleric into a once grated drain
Starving a gnoll, trapped and surrounded on a tall stone plinth
Excavating a spacious den, leavings and dirt abound
Stealing supplies from nearby bugbears via a tunnel network
Feeding on florescent fungus, sprouting from nearly every surface
Tainting everything they touch with yellow mould spores
Frothing at the mouth and desperately hydrophobic
Tunneling throughout, lost count of the # of buckler-sized holes
Grinding down their menacing teeth on the base of a statue
Unravelling a thick coil of rope, cast off in a corner
Hollowing out a home inside an abandoned altar
Upsetting a pack of ravenous ghouls by snatching tasty morsels
Hosting a magical disease that makes victims speak only in goblin
Wounding a giant snake that slithered to close to fist-sized pink pups

Table: rhagodessa
Ambushing a white ape, ostracized from his pack
Luring a receptive female closer with a strange -legged dance
Attaching themselves to a struggling ogre
Lurking near the kobold enclave that feeds him occasionally
Avoiding a brightly burning blue flame
Menacing a group of merchants after their guards fled
Awkwardly flailing as they grapple an angry giant scorpion
Meticulously selecting a new lair with suitable space to nest
Barely moving when the ground suddenly starts to tremble
Molting and cautiously peeking out from a hole
Burrowing in gravel, so that only their scissor-like jaws show
Noisily gnashing its huge, sharp jaws to intimidate a rival
Capturing a squirming giant centipede and hanging on tight
Occupying an abandoned well, opening just large enough
Careening between cool, dark places for cover
Overtaking a fleeing orc, stopping when he makes a sign
Climbing to their perch, high in a shadowy corner
Painstakingly consuming the insides of a driver ant
Clinging defiantly to an angry berserker, tiring them out
Patrolling a well-traveled route for potential prey
Concealing themselves among tall, wilting toadstools
Perching defiantly in front of a closed door
Crawling in bursts of speed, stopping to survey surroundings
Picking apart what may have once been a bear
Crouching low in preparation to pounce on a shadow
Pinching off portions of a giant snake
Cutting the hair of a sleeping hill giant for their nest
Preying mostly on goats as the bones at their feet attest
Dangling precariously from a column slick in slime
Quickly catching a camel with their sticky front legs
Dashing a kobold against the ground
Rattling loudly to warn away a hungry wyvern
Defending their burrow from an inquisitive giant tuatara
Reaching surprising speeds on its swift legs
Detecting vibrations through the ground, alert and hungry
Rearing on its hind legs to try to snag a giant gecko
Dining on a dire darkling beetle
Retreating after sensing the approach of a gelatinous cube
Disappearing below a stone table, surface scorched slightly
Returning to its den after an unsuccessful hunt
Dissolving an unlucky dervish with their digestive saliva
Rolling in a writhing ball of far too many legs, down a slope
Dropping suddenly on a robber fly and rolling around
Running after a galloping warhorse...gaining
Dwelling in a tunnel, hollowed out from a huge bone pile
Rushing into a shadowy spot after a medium's light spell
Efficiently amputating a ghoul for easy transport
Scurrying down a wall, swatting away stirges
Emerging from a surprisingly tight squeeze and unfurling
Scuttling across several shallow puddles with frequent splashes
Feeding slowly on a still twitching fire beetle
Seizing a zealot with their sticky suckers
Fighting over territory, the larger one is losing
Shearing feathers from a giant hawk before feeding
Flicking a strange, whip-like tail to-and-fro
Skittering across a stony scree after a bombardier beetle
Flummoxed by a troll arm that keeps fighting back
Slicing clean-through a thoul with a single snap
Foraging among ancient roots, wider than a giant's leg
Slurping on a giant shrew, clutched tightly
Freezing suddenly after sensing something approach
Sprawling atop a large rock, flecked with sparkling ore
Gathering conveniently sized sections of giant termite
Squatting at the bottom of a pit, waiting for food to come to him
Glaring with its fused eye at a quivering ochre jelly
Startling a draco lizard, which suddenly takes wing
Grabbing a giant rat and swiftly pulling it to their mouth
Stridulating with a loud, almost metallic sound
Grooming the long, stiff hairs that sprout from its face
Struggling to drag an owl bear into a too small alcove
Guarding the peaceful trickle of a natural spring
Stubbornly clutching a valuable marble bust
Hauling a hobgoblin leg home for later
Tapping gently on a large jar, containing a scared gnome
Hiding, somewhat unsuccessfully, behind a motheaten banner
Tenaciously grasping a gasping goblin
Holding fast to a frantically fluttering giant bat
Terrifying a trader, shaking as he swings a bent sword
Hunting near a hamlet, having acquired a taste for humans
Throwing sprays of sand/gravel in the faces of gnolls
Infesting a once sacred shrine, lairing under a pile of benches
Toppling a huge termite mound
Jumping just in time to avoid a giant toad's sticky tongue
Trailing after a potential mate, intently tasting the air
Kneading the ground with each leg in sequence
Tumbling down an incline to escape a giant weasel
Laboring to build a suitable nest among shards of pottery
Unfastening themselves from a limp lizard man
Lashing fruitlessly at a guffawing gargoyle
Utterly sated atop an enormous, shattered egg
Leaping to try and catch a cave locust from its high perch
Violently pouncing on a pit fighter while brigands place bets
Lifting an overturned cart, hungry for the halflings beneath it
Waving forelegs high above its head, as if signaling something
Liquifying the insides of a dead mule
Wheeling around suddenly after being struck by an arrow
Looming in an archway, outstretched legs supporting it
Yanking a rope taught before clipping it with their jaws
Lunging at an unsuspecting bugbear lookout
Zigzagging around small pools of congealed green slime

Table: rhinoceros
Avoiding the scent of poachers on the wind
Rampaging after the death of their mate from starvation
Barreling directly toward a stranded cart
Roaming perilously close to a halfling settlement
Charging after a rival male, to drive him from their territory
Rummaging through hardy shrubs for tender shoots
Crashing through brittle undergrowth
Rushing across a flat field, kicking up clouds
Destroying a lean-to, as nomad's flee
Shunning a huge pile of bones, patrolled by skeletons
Eating their fill on tough, dry grasses
Sidling up to a large boulder for a satisfying scratch
Enraged at the sight of their own shadow
Sniffing the large tracks of a potential interloper
Furrowing the packed soil in search of tubers and roots
Stampeding to drive away a pack of slavering wolves
Grunting as they rub their sides on a sad looking tree trunk
Stumbling and sluggish after ingesting a soporific herb
Inadvertently stomping on a gnome's meager garden
Thundering down a hill toward a terrified berserker
Mother watches as squealing young fight over a branch
Toppling an enormous dead tree trunk
Nursing a noisy and inquisitive calf
Trampling a neanderthal hunting party with stone spears
Pawing at the packed ground, preparing to charge
Trotting majestically with horn(s) held high
Peering into the distance, squinting after a distant roar
Visiting a favorite watering hole, startling other drinkers
Prodding at another rhino to move them gently away
Wallowing in sticky red mud to alleviate itching
Attacking a group of net-wielding hobgoblins
Menacing a spell-component seeking medium
Besieging a brigand's bivouac, she cowers atop a boulder
Nibbling on thick dangling strands of dripping aquatic plants
Browsing low hanging branches for leaves
Peacefully grazing among a herd of wild horses
Chasing away grazing antelope from his precious patch
Playfully splashing in innumerable puddles after a recent rain
Cooling off in a pond, occasionally thrashing to frighten birds
Plucking shiny leaves with surprisingly dexterous lips
Cropping flower buds from a spikey succulent
Reaching and straining to strip the last greenery from a tree
Defending a ranger, mauled by a manticore
Scattering a troop of feisty and vocal rock baboons
Drinking deeply from a stream, eyeing crocodiles closely
Shredding long strips of bright yellow bark from a log
Flicking their bristly tails from side to side
Splintering the wooden door of a disused barn
Fording a piranha infested river with stoic confidence
Tolerating the large ivory birds, perched on its back
Galloping on a crumbling bridge, snapping beams and wood
Treeing a very terrified templar
Gorging on a haystack, flustered farmer glowering nearby
Twitching their tufted ears to swat a swarm of flies
Hauling a wagon, full of very drunken dwarfs
Unhorsing a knight, crumpled and dented in the dust
Intimidating a pack of feral hellhounds into flight
Uprooting an equally stubborn avocado tree
Lazily consuming fallen fruit that is starting to ferment
Wading through well-armed goblins, flinging them like toys

Table: rhinoceros, woolly
Avoiding the scent of poachers on the wind
Rampaging after the death of their mate from starvation
Barreling directly toward a stranded cart
Roaming perilously close to a halfling settlement
Charging after a rival male, to drive him from their territory
Rummaging through hardy shrubs for tender shoots
Crashing through brittle undergrowth
Rushing across a flat field, kicking up clouds
Destroying a lean-to, as nomad's flee
Shunning a huge pile of bones, patrolled by skeletons
Eating their fill on tough, dry grasses
Sidling up to a large boulder for a satisfying scratch
Enraged at the sight of their own shadow
Sniffing the large tracks of a potential interloper
Furrowing the packed soil in search of tubers and roots
Stampeding to drive away a pack of slavering wolves
Grunting as they rub their sides on a sad looking tree trunk
Stumbling and sluggish after ingesting a soporific herb
Inadvertently stomping on a gnome's meager garden
Thundering down a hill toward a terrified berserker
Mother watches as squealing young fight over a branch
Toppling an enormous dead tree trunk
Nursing a noisy and inquisitive calf
Trampling a neanderthal hunting party with stone spears
Pawing at the packed ground, preparing to charge
Trotting majestically with horn(s) held high
Peering into the distance, squinting after a distant roar
Visiting a favorite watering hole, startling other drinkers
Prodding at another rhino to move them gently away
Wallowing in sticky red mud to alleviate itching
Bellowing mournfully over a missing calf
Pin-cushioned by crude spears, but no worse of wear
Bracing against a frigid, sleeting wind
Plodding in snow at least as deep as a halfling is tall
Chewing on a mouthful of crunchy dry twigs
Plowing with their horn, searching for scraggly plants
Cracking a thick ice pack with their tremendous weight
Pulling a sled with a frost giant driver
Digging with their forelegs for any trace of grass
Rolling around on the ground to dislodge icy chunks
Emerging from a biting blizzard, covered in snow
Scratching at an iced over watering hole, thirsty
Gazing from atop a ridge at curling campfire smoke
Shaking off a massive amount of snow from their backs
Huddling for warmth, a mass of shaggy horns
Sheltering beneath a large granite overhang
Joining up with a herd of mammoths temporarily
Shoveling aside a drift with their horn hoping for food
Lumbering slowly, carrying nomad tent materials
Snorting and blowing out large clouds of breath-steam
Marching single file, down an avalanche prone pass
Stripping the bark from a snow-covered pine
Migrating to new lands, after a white dragon woke up
Sweeping a snowdrift with their huge horn
Munching on a patch of grass, miraculously intact
Towering above the dwarf that domesticated them
Overrunning a dire wolf, separated from their pack
Trekking past the body of a mastodon, succumbed to starvation
Peeling thick sheets of hardy lichen from icy boulders
Viciously gouging a roaring cave bear

Table: robber fly
Affixing themselves to a high corner perch
Laying a uniform line of apple-sized eggs in a corner
Alighting on a groaning chandelier
Leaping from a perch to avoid an oozing green slime
Ambushing anything ascending a spiral stair
Liquifying the organs of an orc
Annoying a rock living statue
Loudly slurping out the insides of a giant luna moth
Assassinating an unlucky driver ant
Lunging unsuccessfully at a shadow
Attempting to untangle themselves from a giant spider's web
Lurking in a prime perch - belly of a horse statue
Balancing perilously on the side of a stalactite
Meandering awkwardly across the ground with wet wings
Being swatted away by a cyclops
Negotiating an area almost completely filled with webs
Besieging a killer beehive - planted along their route home
Orbiting an ogre hauling a dead cow
Blundering into a kobold camp
Outmaneuvering a wobbling black pudding
Bombinating obstreperously with piercing resonance
Overtaking a leaping giant grasshopper
Boring into the thick carapace of a tiger beetle
Peering, with ever watchful red, grapefruit-sized compound eyes
Buzzing relentlessly at a flickering torch
Perching over doorways - an effective hunting strategy
Camping out on a corridor ceiling
Plucking a giant centipede from the floor, midflight
Carrying all manner of unusual diseases
Plunging their proboscis clean-through an elf's leather armor
Circling a deer carcass cautiously
Preening fuzzy faces with their spindly forelegs
Clasping tightly to a tattered tapestry
Punching through plate armor, worn by a hobgoblin
Climbing clumsily up a very slick surface
Resting atop a rusty iron cage
Clutching a dead snake securely in its forelegs
Rubbing its spindly forelegs together as if scheming
Darting to-and-fro frantically in search of prey
Seeking a warm, living creature in which to lay eggs
Depositing eggs in a still living fire beetle
Seizing a giant crab spider, clinging to a wall
Dissolving the insides of a dead mule
Serving as mounts for wicked, unseelie sprites
Divebombing a druid
Settling on an owlbear corpse
Drawn to an unhygienic hill giant
Shuddering slightly at the sound of a distant slam
Drifting lazily on cool wind currents
Skewering a bloated stirge
Drinking from a puddle, fed by dripping water
Skimming the surface of a cloudy pool
Droning contentedly after draining a dwarf
Skipping across the ceiling, disturbing roosting bats
Eluding the sticky tongue of a giant toad
Snatching a screaming goblin
Escaping from the pointy maw of a snuffling giant shrew
Springing upon a bombardier beetle
Exterminating a colony of giant bees with magical healing honey
Squatting in a shadowy corner, waiting to strike
Extracting the liquified insides of a cave locust
Squeezing its striped abdomen through an arrow slit
Feeding on nectar from strange carrion-scented blooms
Startling a shrieker with an inopportune landing
Flicking its segmented antennae
Stationing well out of tongue range from a giant frog
Fluttering repeatedly, attempting to find purchase to perch
Struggling with a giant scorpion
Fooling its prey as a fat-bodied giant bumblebee mimic
Surprising an extremely cautious thief
Frantically grappling with a rhagodessa
Surveying the area closely from a high position
Glaring with its large alien eyes at passersby
Swarming around a dead giant catfish
Grabbing a gnome, but struggling to carry her away
Swooping suddenly toward an unsuspecting carcass crawler
Holding a twitching giant rat gingerly as it slurps out its insides
Taking wing in unison after sensing some unseen threat
Hovering around the putrid remains of a ghoul's supper
Teetering and unsteady while trying to hang on an iron chain
Humming almost musically to attract prey
Throbbing and gravid with eggs and eager to oviposit
Ignoring a patrolling band of skeletons
Thrumming monotonously upon a thick window
Impaling a poacher with a wickedly appointed proboscis
Tightly gripping the back of a lurching zombie
Infesting the area after an exceptionally mild winter
Tussling with an angry acolyte
Injecting paralyzing enzymes into a sleeping bugbear
Twitching wings to maintain their balance as they cling
Investigating a stinking rubbish heap enthusiastically
Underestimating the agility of a hungry giant bat
Jabbing mouthparts futilely against the scaly hide of a lizard man
Unfurling their wrinkled wings for the first-time post-pupation
Jumping without warning and startling a hidden bandit
Very large specimens, occasionally ridden by kobolds
Knocking over chairs in clumsy flight as it flees a giant lizard
Waiting patiently to be fed by plague-bringer cultists
Landing delicately on a sour-smelling giant mushroom
Waylaying a medium, attempting to study ancient inscriptions

Table: roc, giant
Announcing their presence with a cry heard for miles
Guarding the prison of the last in a line of ancient, evil elfs
Ascending swiftly to conceal themselves among the clouds
Hovering above a terrified hobgoblin fortress
Blotting out the sun - shadow turning day to night
Landing with shed feather gifts for a gnome village
Carrying off a tasty titanothere
Menacing a chaotic kingdom, destroying bridges and roads
Clashing with an airborne red dragon, high overhead
Plunging from the sky to attack a t. Rex, strike shakes the earth
Crouching to peer directly into the eye of a cyclops
Presiding over a conference with representatives from all birds
Distributing much needed meat to starving neanderthals
Roosting in an abandoned cloud giant castle
Dropping enormous boulders on a fire giant stronghold
Scattering an invading army of wicked brigands to protect a town
Enforcing a brutal doctrine of peace through fury in the region
Seeking a sage to record her magnificent memoirs
Feathering a massive nest, inside a distant caldera
Shrieking with a piercing, ear-shattering scream that melts undead
Feeding strips of mastodon to their young
Snatching an evil temple from a mountaintop to fling into the sea
Fishing for whale in oceans many leagues away
Toppling a wicked lord's castle, with a quick fly-by
Glaring at the campfires of a distant battlefield
Towering over the halfling hamlet that helps preen their feathers
Gliding gracefully, dwarfing even the clouds
Unfurling wings wet with a small ponds' worth of dew to dry them
Grasping firmly onto a mountain side, gouging the stone
Utterly eclipsing the sun as they soar overhead

Table: roc, large
Allying with dervishes against invading berserkers
Liberating prisoners after defeating a cruel manticore
Avenging a mate's death by destroying a village
Nesting among the ruins of an ancient amphitheatre
Beating their wings, generating dust-devils and high winds
Overshadowing a shimmering paladin, astride her pegasus
Capturing a wily bandit to convince her to change her ways
Perching on the battlements of a trusted cleric's abbey
Circling ominously above dueling wizards
Plummeting into the ocean, diving after a delicious sea serpent
Clutching a gigantic rock python in their talons
Preying on a camel caravan, laden with temple stolen treasure
Descending to perch atop a crumbling tower
Rending road in anger as parley with stubborn dwarfs breaks down
Dogfighting with a trio of wyverns
Scanning horizon with huge, unblinking eyes and a fierce expression
Encouraging their cautious young to fledge, vigilant and protective
Screaming as they drive away goblin egg thieves
Falling after being winged by a poisoned bugbear ballista bolt
Seizing a simpering slave merchant for her chicks
Flying with an important message from a monastery in need of aid
Soaring high with their ranger companion to survey the wilderness
Gnawing on massive iron fetters, escaped from frost giants
Swooping suddenly to pluck a gnoll from their pack
Gobbling down a wild mustang with a gulping motion
Tearing through the treetops after hearing a unicorn's distress call
Hunting an orc fletcher, capable of crafting roc slaying arrows
Wantonly slaying all travelers - ensorcelled by an evil wizard
Hurtling themselves at a surfacing purple worm
Watching over a procession of pilgrims, carrying remains of a saint

Table: roc, small
Adorning their bower with bones of the unrighteous
Molting awkwardly, shed feathers are valuable to alchemists
Arriving too late to stop the assassination of a kindly noble
Overlooking the hamlet they've sworn to protect
Brooding over boulder-sized eggs, waiting for return of mate
Pecking at the scaly hide of a huge crocodile
Catching a warm updraft to glide on the current
Pouncing on a still struggling gorgon
Chasing down a druid to grant him the power of speech
Protecting a den of blink dogs from a vicious warp beast
Climbing with labored wingbeats - the warhorse is heavy
Rejoicing on sight of elf friend that long ago nursed an arrow wound
Diving into a lake and surfacing with a giant catfish
Sailing high above a volley of bandit arrows
Eating the dead acolytes of a fascinating religious sect
Savaging an ogre, carelessly starting forest fires
Flapping their wings to dry off a drenched nomad
Screeching loudly at a giant rattler found in her nest
Gorging on sheep, received as payment for ferrying letters
Skimming surface of a pristine lake playfully to entertain nixies
Grabbing a barn roof where sunlight-hating goblins hide
Startling a herd of elk into a stampede
Grazing a gargoyle's stony hide with their keen talons
Sweeping countryside for a lost child with immaculate vision
Gripping the leather wrist cuff of their cloud giant friend
Taking wing wobblily after feasting on a pack of ghouls
Harrying a herd of hippogriff away from their nest
Wheeling to try to lose a tenacious swarm of killer bees
Inhabiting precarious nest of ship masts, clinging to a cliffside
Whistling forlornly at the gravesite of a friend

Table: rock baboon
Adopting an abandoned blink dog pup
Luring a giant weasel out of its desirable den
Approaching a merchant's wagon cautiously, smelling food
Lurking near a neanderthal cave, subsisting on scraps
Attempting to intimidate an illusionist with colorful displays
Meticulously picking ripe berries from very thorny bushes
Basking atop a large rock that looks suspiciously like a face
Morosely dining on dead grasses that require a lot of chewing
Begging humbly for food scarps whenever they encounter elfs
Nosily barking to intimidate a pack of wolves hovering nearby
Blithering with each other as they try to open a large nut
Observing ominous clouds gathering with somber faces
Bounding after a wounded driver ant
Ostracizing an injured member of the flange
Burying their colorful faces in their hands, appearing to mourn
Peering with narrowed eyes at a druid offering them food
Carrying a very hairy baby neanderthal
Perching atop moss covered, dwarf-runed grave markers
Challenging each other for congressional leadership
Playfully gamboling juveniles annoy lightly napping adults
Chasing away a leopard by waving tree branches
Playing with a dented breastplate and making a huge racket
Chattering contentedly, oblivious to a nearby crocodile
Plucking succulent parasites from each others coats to snack on
Chewing on mildly toxic tubers to get tipsy
Prodding a dead troop member with a stick
Clambering over a crumbling cyclopean wall
Quietly climbing onto the back of a trader's fruit cart
Clinging to a cleric's dropped shield
Rehearsing their grimaces reflexively, or are they yawning?
Courageously leaping onto the back of a hissing owl bear
Rejoicing cacophonously after driving away a lion
Cowering from a large male, baring massive fangs
Robbing a bird's nest, holding fragile eggs close to their chests
Decorating their lair with clumps of colorful mud
Running alongside a galloping war horse in full barding
Digging for tasty buried toads with teeth-sharpened sticks
Savagely devouring a dead deer as forlorn hyaena look on
Dispersing after a distant arcane explosion
Scampering up a steep cliff face, startling some mountain goats
Drinking with cupped hands from a shallow spring
Scavenging on the corpse of a diseased ogre
Dropping large stones on a tough-skinned fruit
Scratching strange glyphs in the sand, before wiping them away
Enraged after a swooping giant hawk stole a infant
Screeching uselessly at a rhinoceros grazing nearby
Entering into an uneasy truce with a grazing elephant
Scurrying into a gigantic, hollowed out log
Fashioning long, slender sticks for termite fishing
Seizing thrashing fish from a river
Feigning an injury to distract a terror bird from their young
Sleeping in shifts to keep a watchful eye out for predators
Fixating on a glittering, scabbard embedded with glass gems
Sniffing puddles of rain before slurping up muddy water
Flashing their colorful hindquarters to display dominance
Sounding off in sequence with brief barks for an "all's well"
Fleeing after discovering a rowdy rattlesnake
Splashing gleefully in a pristine pond
Following a herd of antelope for mutual safety
Splitting open marrow rich zebra bones with big, sharp, stones
Foraging among the rocks for tenacious lichens
Squatting in a loose circle, listening intently to an elder's hoots
Gathering fallen fruits from a thunder-struck tree
Startled by a fire-gouting chimera, seeking to steal their cave
Gibbering incessantly, passing around a bleached skull
Studying a broken piece of ceramic intently
Gloating dominate male drives away weaker rivals
Swinging stripped branches wildly at a giant scorpion
Grabbing at a brigands backpack and cloak
Tamed to trust anyone wearing predominantly blue
Grinning with fang-filled mouths as they lob sharp stones
Tamping down areas of tall grass for bedding
Grooming each other, safe on the boughs of a tall tree
Teaching juveniles how to open logs to feed on grubs
Harvesting tender flower buds to bring back to the den
Theatrically screaming to threaten a veteran
Herding their young into a cave after seeing a distant roc
Thumping their chests loudly at a passing titanothere
Holding a glowing, flanged mace above their heads
Tugging on the tail of an irritated vulture, trying to feast
Hooting and tossing long leg-bones into the air
Uprooting rare and sacred herbs to toss around madly
Huddling together against a biting, sand-filled wind
Voraciously eating bright red berries, staining their fur
Hunting for honey by following the song of bee-eating birds
Warning the troop of an approaching troll
Hurling rocks at anything that trespasses in their territory
Warring between baboon factions has broken out, it's bloody
Hypnotically flushing their faces bright blue and orange
Watching a distant grassfire with apparent concern
Inhabiting a massive bronze helmet, green with age
Whipping a dead rabbit around violently
Injuring a sleeping treant by violently pruning limbs
Wielding a strange short sword, with an unnaturally keen edge
Jumping up and down, shrieking at a nervous tortoise
Wounding a harpy with a well-aimed rock
Learning how to draw water from a well through trial & error
Wrenching an unlucky nomad's shoulder out of socket
Living on wriggling, greasy robber fly larvae
Yelping and howling, being attacked by a hungry giant lizard

Table: rust monster
Accelerating the decay of a huge chain, supporting a boulder
Leashed with a length or rope, tied to a hideous statue of an orc
Annoying dungeon denizens by abrading bands on every door
Licking the iron bands of brine-filled barrels
Arriving late, but hungry, to a gnoll/bugbear battle
Lunging menacingly at an ore merchant
Attracted to a pulsing meteor chunk, fallen from the heavens
Lying in wait, after sensing a sound
Besieging bandit arms dealers, worried about their stock
Marring a delicately decorated, elf-wrought gate
Building a lumpy, calcified, almost coral-like nest of corrosion
Mewing, with occasional chirps, awaiting food from goblin keepers
Burying a partially melted battle axe, a snack for later
Molting, accompanied by a stringent ozone-like smell
Buzzing excitedly after getting a whiff of a paladin's panoply
Nesting in a pit, replete with large iron spikes to sup on
Caking a metal sculpture with flaky verdigris
Nibbling on a heavily pitted anvil
Caressing an abandoned crowbar gently with feathered antennae
Observing ghouls as they open a coffin with armored corpse inside
Chasing after a terrified living statue, forged from ferrous metal
Oxidizing an ominous iron pillar, supporting the ceiling
Clattering like coins in a pouch, crouched in a doorway
Painstakingly tunneling through a chalky wall
Clicking as they rub their forelegs together in anticipation
Pitting the breastplate adorning a skeletal bugbear
Climbing up a wall, slavering over an iron chandelier, out of reach
Plaguing a gnomish smithy, they'll pay generously for extermination
Completely consuming a cast-off crossbows' pins and plating
Prowling through purple worm tunnels, snacking on seams
Conveniently rusting weapons of some helpless animate skeletons
Purring with contentment near a now-shoeless horse
Cornering a conjurer after scenting their hob-nailed boot tracks
Pushing all their weight against an iron maiden, to knock it over
Corroding the bars of a cell, craving the delicious fetters within
Quibbling over a pot helm with a smaller specimen
Creeping along a wooden floor, pausing to partake of the odd nail
Rasping at the forked head of a discarded ranseur
Dashing down a wooden ladder with incredibly speed
Reducing a set of magical lockpicks to a pile of ochre dust
Defending their territory from a curious carcass crawler
Regurgitating a few decorative gems, sucked up by mistake
Disintegrating a dented metal helmet in the middle of a room
Retreating from a troll with an enchanted wooden club
Dissolving the buckles on a suit of leather armor, sequentially
Ridden by sprites, on a crusade to rid the world of cold iron
Dodging a lobbed hobgoblin club
Scampering from a collapsed campsite after a tent-spike banquet
Eagerly straining and stretching to scarf on sconces
Scraping slowly at a steel shield, savoring the flavor
Eating away at minecart rails and growing quite fat
Scurrying away after being scorched by an unerring magical missile
Encrusting an ornamental escutcheon
Scuttling a wagon after inhaling the wheel hubs
Feasting on a pile of iron pitons, dropped by a fleeing dwarf
Slowly cankering an iron slab, placed to prevent a wraith from rising
Feeding their writhing, insatiable larvae a shattered lantern
Sniffing a hoard of coins, occasionally devouring the debased ones
Feeling their way across a floor, blinded by a well-placed light spell
Squeezing through their narrow, labyrinthine warrens
Fighting a stubborn, treat-filled gelatinous cube
Stalking some surprisingly well-equipped goblins
Flaking away at a once formidable flail
Stinking slightly of blood, metallic, like a sweaty penny
Flicking fringed feelers to-and-fro from the safety of a small alcove
Symbiotically benefiting from a rampaging ochre jelly
Following iron filings, leading straight into a wooden kobold cage
Tangling itself in a ball of twine like a cat with catnip
Gnawing on an acolyte's dropped pernach
Tarnishing a once wondrous warhammer
Graciously devouring arrowheads from a once lethal spring trap
Taste-testing a holy symbol, still clutched in hands of a dead cleric
Grappling with a hapless golem, limping with a mostly lost leg
Threatening an ogre in over-sized chainmail
Grazing on a convenient grapple, unsuspecting thief climbs below
Transforming spears into staves, swiftly
Hibernating in an overturned wooden crate
Trundling down a slope by rolling into an astoundingly compact ball
Hiding after being pelted with halfling sling stones
Twitching their quill-like antennae as they decompose a spade-head
Hounding a particularly palatable surprise - a gorgon calf
Unfurnishing a shiny buckler
Humming constantly in a concentrated effort to attract a mate
Utterly confounded by a piece of lodestone, senses going haywire
Hunkering down to dine on the head of a hammer
Vacuuming up flakey shavings that used to be a magic mace
Hurtling down a hallway after a well-armored hobgoblin
Wagging their fin-like tails as they inhale some ingots
Imbruing a once magical blade with tawny pits
Weakening a ferrous floor grate, only thing separating it from falling
Incubating their strange dodecahedral clutch
Withdrawing after failing to defeat a rival male
Infesting the area due to plentiful and iron-rich, red soil
Withering the hilt of a dagger, embedded in the wall
Jumping into a pool after a lizard man with a stolen sword
Worrying a medium, clutching their metal bound spellbook tightly
Knocking down a wooden table after rusting its nails
Yielding ground to a gargoyle, angered at the loss of her iron crown
Lashing at a veteran's treasured longsword
Zeroing in on heroes, a trio of knights decked out in the finest plate

Table: salamander, flame
Adapting begrudgingly to slightly cooler climes
Interrupting a summoning ritual for a water elemental
Advancing in a fiery formation, a wall of wicked spears
Jabbing spears in piles of rubbish to scatter giant rats
Apprehending an acolyte, bearing a sacred torch
Jeering at a captured frost salamander
Balancing with their tails as they navigate a narrow ledge
Kneading molten tin and copper together with bare claws
Barbecuing sizzling caecilia segments for supper
Leaving scorched claw-prints and tail tracks behind them
Basking in the radiant heat from a fissure of flowing magma
Leering enviously at a medium's wand of fire
Branding their giant lizard mounts with white-hot irons
Licking their lips as a camel rotates on a large spit
Capturing giant cave crawfish for a well-seasoned boil
Living comfortably in the thermal steam of a hot spring
Carrying the charred carcass of a cow to their larder for later
Lounging on a dark, heat absorbent boulder
Cavorting around a raging campfire, stoking the flames
Luring feral hellhounds into an iron cage with goat meat
Clawing their way up a steep cliffside
Maiming a wood golem gleefully
Communing with their home plane through a swirling gate
Manufacturing crude arms and armor for hobgoblin armies
Conserving their energy, sluggish due to chilly conditions
Marveling at a strangely fireproof spellbook
Crackling and sputtering as an argument heats up
Melting a killer beehive, collecting wax for molds
Creeping on all fours through surprisingly narrow crevasses
Mocking a missive from a local goblin king
Cremating the dead, as a service to a local community
Obliterating a quivering black pudding, trapped in a pit
Dangling an unhappy carcass crawler on a lumpy chain
Operating a humongous bellows with expert timing
Decorating walls with intricate and artful smears of ash
Organizing an annual frost salamander hunt
Dipping tips of their tails in a pool of water, making it boil
Parboiling an enormous giant catfish
Dislodging a large boulder, concealing a passage
Performing a vital role in controlling a green slime infestation
Drinking jug after jug of acrid lamp oil with gusto
Piling salvaged armor and metal into a huge stack of slag
Driving away a howling pack of rock baboons
Plagued by the chill touch of a recently arrived shadow
Easily eradicating a persistent yellow mould infestation
Plundering a forgotten cache of dwarf siege machinery
Emerging from strangely beautiful baked mud cocoons
Pressing nearly liquid lead into unique artistic forms
Enkindling a stack of scrolls, just by strolling by
Quarrelling over who gets to eat a boiled pegasus egg
Fanning a flickering fire, huddled close to the heat
Rallying after a defeat at the hands of an elf warband
Feasting on a rich seam of crunchy coal
Rebelling against their fire giant overseer
Fermenting heavily spiced stews in huge cast iron cauldrons
Recruiting for their strange religion of fire and smoke
Flaring narrow nostrils angrily at a cool, refreshing breeze
Relinquishing their control of a pass to ogre mercenaries
Gambling on a hellhound/dire wolf fight
Salivating heavily, drops of sizzling spittle steam on the ground
Gently charring large grubs on long metal skewers
Scalding a trader's donkey accidentally
Glowing dully through jagged, dry cracks in their skin
Shackling a subdued hydra as a new lair guardian
Gossiping about the upcoming visit from an efreeti
Shimmering the air around them with angry heat
Gradually warming an entire cave complex with their presence
Singeing the tips of metal wrapped reeds to write with
Grilling a captive dwarf, apprehended in their territory
Smacking their lips as they drag a dead deer
Grumbling as they follow a fire giant's tracks
Smoldering a crate of extremely valuable incense
Haggling politely with dervishes who keep their distance
Spearing strange eye-less cave fish to trade to gnolls
Hammering molten metal with a musical rhythm
Stealing sheep from a sleeping cyclops shepherd
Harassing a giant spider colony, by setting webs alight
Stinking of sweat and tar-like musk, breeding season
Harnessing heat from a malfunctioning magic item
Stooping to pass through a low archway
Hijacking an anvil from a fleeing centaur clan
Taming a strong-willed chimera
Homesick and seeking a powerful wizard to send them back
Tasting the air with their brilliant blue tongues
Howling with glee as a slightly singed bugbear runs away
Taunting local lizard men with their mastery over fire
Igniting a massive pile of wood and wagon parts
Tending burgeoning fields of brilliant red and very spicy peppers
Incinerating a doppelgänger, discovered among their ranks
Thriving in a volcano, long thought extinct, but starting to smoke
Incubating gelatinous, twitching eggs in a pool of lava
Toasting barley and malt in exchange for dwarf-made ales
Indulging in fricasseed giant ferret
Twitching their tails nervously as their leader speaks
Inhabiting the plundered den of a dead red dragon
Uncontrollably shivering from a brisk northern wind
Injuring a pack of wincing and fearful trolls
Wallowing in a huge bonfire for warmth
Inspecting a group of fiercely loyal kobold lackeys
Welding the head onto a partially completed bronze golem

Table: salamander, frost
Agitating a pale haired purple worm, adapted to the cold
Laughing as a veteran's spear fails to pierce its hide
Ambling across an icy field of rubble, glaring
Leaping through deep snowdrifts, bounding on all six legs
Ambushing a herd of reindeer by rising from the snow
Levelling the tents of a hobgoblin camp
Barging into a bandit camp, dousing their fire
Lodging a frozen ogre between boulders for their next meal
Bathing in a river, ice crystals forming around them
Lurching slowly, dripping blue blood - magic arrow wounds
Battering at a stone door with four of its legs
Mauling a bellowing moose, defending a downed ranger
Bemoaning gradually warming weather, irritable
Meandering cautiously around a huge icy cavern
Biting into a frozen bugbear, slain months ago
Meditating in a twisted pose, as snowflakes coat their face
Bullying a group of timid ice trolls to do his bidding
Melding almost perfectly into a sleet storm
Burrowing into cold ground to escape a warm wind
Molting, with scales sloughing in frost like sheets
Caked with frost as they recline in a biting wind
Munching their way out from under a downed tree
Camouflaged expertly among snow covered statues
Nosing around for voles, game is scarce in these parts
Carving a passable likeness out of a block of ice
Numbing a paladin, desperately trying to defeat it
Celebrating defeat of a rival with load howls
Obscuring the entrance to a nesting site with a coating of ice
Chilling the air of their den to near freezing
Patiently ice-fishing for seal and narwhal
Clashing with two young flame salamanders, evenly matched
Patrolling their territory, on a predictable schedule
Climbing a wall of ice, using back claws like crampons
Plodding toward a suspicious wooly rhino
Cooperating ruefully with a frost giant hunter
Prudently stashing a polar bear carcass in a pit
Covering the ground with a layer of frost beneath each footfall
Quaking with rage as a flame salamander escapes
Croaking gutturally, pining for a mate
Quenching a cleric's torch and licking their lips
Descending downstairs hewn from ice by helpful gnomes
Racing up a snowy slope with impossibly sure steps
Destroying an arctic owlbear nest
Refrigerating a white-furred rock baboon
Detecting prey on the wind with rapid tongue flicks
Resting in the shade of an overhang to remain cool
Digesting a musk ox with a comically distended belly
Resurfacing, empty handed, after diving in frigid waters
Dwelling in a cool barn during the hottest part of the day
Roaring in pain at an explosive ball of flame
Encasing a caribou in ice to cache it for later
Scooping fistfuls of snow and forming them into round stacks
Enjoying a biting and bracing blizzard-like gale
Scratching deep gouges into the ice with their claws
Entombing an elf in a block of thick, translucent blue ice
Scrimshawing intricate geometric sigils and glyphs on tusks
Fattening up on a cave bear carcass
Scuttling across thick ice with nary a slip
Fawning over a sapphire tipped scepter
Sealing a larder of frozen prey by rolling a large, icy rock
Flecked with frozen blood from a recent skirmish
Shrugging off a thick blanket of snow, only to have it reform
Fogging the air with their frigid breath
Slavering at a roasting boar, cautious of the campfire
Gathering icy lichen to line their nest
Slithering deftly over ground scattered with caltrops
Glistening with condensation that quickly turns to frost
Somersaulting playfully down a slick hill in a light snow flurry
Gnawing on a dead deer, frozen completely solid
Squeezing the life from a dire wolf with a pale pelt
Grinning with too many teeth at a shivering bard
Sulking as they drag a frost giant sled
Grunting as they lug a sled, loaded with stiff, frozen furs
Surrendering to a summoner, served by fire elementals
Gulping a barrel of brined herring down greedily
Swallowing chunks of frozen giant crab meat
Hatching their strange, cubic eggs by burying them in a drift
Swiftly plowing a new den in the bank of a huge drift
Haunting an abandoned mineshaft, avoided due to cold
Swinging at a snow leopard with an uprooted tree as a club
Hissing loudly at a torch wielding warrior
Tearing through a foundered wagon in search of food
Hurtling on all six legs after a herd of reindeer
Thawing and groaning ice signals the time to head north
Ignoring a lumbering herd of wooly mammoth
Toppling a mammoth by tripping with their tail
Impeding travel through a region by causing avalanches
Tracking a hunter through the tundra by residual heat
Imprisoning an unconscious berserker in an icy cell
Trading ice covered treasures to nomads for caribou meat
Instantaneously freezing a path across a chilly pool as they walk
Uncoiling their long tail as they stretch and yawn
Journeying to an ancient portal to summon companionship
Utterly filling the humid air with stinging ice crystals
Knocking down halfling-sized icicles on a pack of frost gnolls
Wielding a pair of sharpened narwhal tusks as weapons
Knotting around a crumbling column, covered in spidery ice
Whipping around at the distant rumble of avalanche
Lashing their snake-like tail impatiently, while an orc begs
Wrestling three neanderthal to the ground at once

Table: scorpion, giant
Agitating a diligent colony of driver ants
Lifting their pincers into the air to bask in a breeze
Ambushing an orc axe-maiden from the shadows
Lurking under a massive steel shield, fit for a giant
Angrily grasping at the air and waving their sting to-and-fro
Manipulating a giant rat deftly with their claws and mandibles
Attacking a reflection in a cracked brass mirror
Menacing an oblivious giant bat, roosting out of reach
Battering down a stuck wooden door with massive, spiny claws
Munching on a gaudily dressed merchant, still wearing jewelry
Beckoning atop a boulder in a strangely mechanical fashion
Neatly coiling themselves around a warm, black boulder
Besieging a small community of dervishes
Nesting in a shallow depression of cool sand
Brandishing the contorted corpse of a ghoul in their claws
Noticing a marauding ochre jelly, just in time
Bustling back and forth around a shallow pit of bones
Overwhelming a phalanx of kobold spearmen
Cannibalizing a male, having just mated
Picking at an abandoned camp site inquisitively
Carrying cat-sized translucent young on their backs
Piercing the fuzzy hide of a foaming mad giant shrew
Catching a fleeing cutpurse by the cloak with their claw
Pinching at the bases of plants to release a sweet sap
Charging belligerently at a rival, pincers raised
Plunging their sting into a pool, and pulling up gasping fish
Clacking their pinchers rhythmically with a hollow sound
Prowling among tall termite mounds, tricky to spot
Clambering over a pile of cracked roof tiles
Prying a flat boulder onto its side with their claws
Climbing with surprising grace, over a pile of rusted armor
Quietly skulking toward some tethered warhorses
Cramming what may have been a camel in their mouthparts
Raising their sting high, moments from striking a dwarf
Crawling low to the ground, due to flying bats above
Rearing onto hindmost legs to snap at a robber fly
Crushing a buzzing cave locust's abdomen with a crunch
Releasing its hold on a furious mummy
Damaging a finely carved ring of statues, knocking them over
Repeatedly stinging a stubborn ranger with a magic periapt
Dancing a promenade à deux as part of a mate selection process
Ridden by goblins, tails propped upright with wooden forks
Dashing out from underneath a precarious overhang
Running with a loud clatter across stones, away from a roc
Devouring a giant tarantula
Scaling a mound of boulders, slipping slightly with every step
Dropping the drained husk of a hermit
Scurrying toward their druid companion
Emerging from a pebble strewn, foul-smelling burrow
Scuttling out from behind an upturned table
Entwining with a giant ferret, locked in mortal combat
Sedately creeping, slower due to a lack of food
Envenoming a veteran, stinger punching through breastplate
Seizing a rock baboon and stinging it repeatedly
Feeding on a bloated giant toad
Serving as mounts for a vicious vector of paladins of disease
Flinching from the embers of a hurled torch
Severing the arm of a whimpering troglodyte
Flogging the tip of their tail angrily against a statuesque golem
Sheltering under a beautifully carved ciborium
Flourishing their wicked pincers dramatically at any sound
Squeezing the life out of a cultist sent to deposit offerings
Fluorescing a beautiful blue in the light of glowing fungi
Stabbing a killer bee whose stinger failed to find purchase
Following patiently behind a staggering horse
Staunchly clenching a twitching troll leg
Frustratedly shaking an undying skeleton in their grasp
Storming a pen of bleating sheep
Gathering smooth stones into uniform piles
Strangling an unlucky gnoll as allies begin to titter nervously
Gesticulating wildly - victim of a djinni's polymorphic curse
Stretching to surprising lengths to cross a crevasse
Grabbing a stalagmite suddenly, gouging into the surface
Striking the shield of a sun cleric with a resounding ring
Grappling with an enormous rattlesnake
Thrashing a still squirming crab spider against a rock
Hiding in the damp beneath a large tent canvass
Trampling an elf archer, with an empty quiver
Hissing loudly as their book-lungs sputter and wheeze
Twirling & clacking claws...surrounded by hungry giant weasels
Holding fast to a frightened fighter, futilely bashing with fists
Unbalancing a precariously placed monolith by trying to climb it
Huddling compactly, ready to spring on any prey
Vacating a favorite den due to green slime
Impaling a gelatinous cube, repeatedly and to little effect
Venturing cautiously out of an enormous green glass bottle
Inching ever closer to a rambunctious litter of blink puppies
Vomiting up indigestible armor, bones, and straps
Intercepting a group of lizard man foragers
Waiting patiently to be fed by a minotaur shaman
Jabbing wickedly barbed sting into a screeching fire beetle
Walking around a moaning group of zombies
Juddering after stirring up a cloud of yellow mould
Waving their claws at an ogre menacingly
Killing a rock baboon with its tenacious squeeze
Wounding a nomad, perched in a tree with their sting
Knouting a giggling gargoyle fruitlessly with their tail
Wrenching the halberd out of the hands of a berserker
Lashing their stings side-to-side as a distant vulture croaks
Wringing the neck of a bugbear turning blue

Table: sea serpent (lesser)
Abruptly surfacing and bellowing loudly as fog begins to form
Lurking within the weedy masses of a sargasso sea
Accompanied by a shiver of sharks, happy to feast on scraps
Menacing orc pearl divers, taking an unfair cut of the spoils
Appearing alongside a sudden savage squall
Mercilessly smashing a merchant ship
Attacking a merman merchant caravan, surfaced to trade
Mesmerically swaying in a sailor's spyglass
Basking in the sun, draped over a shallow sandbar
Migrating to warmer waters to mate, easily upset
Beaching itself to dine on a rotting whale carcass
Narrowing their eyes as a desperate captain bargains with gods
Biting through the line of an anchored dhow, setting it adrift
Navigating to an ancient serpent graveyard using the stars
Boiling the seas around it into a frothing vortex
Ominously snapping its titanic jaws
Breaching majestically, creating a massive splash
Overturning a trireme as oarsmen scream
Capsizing a large cog by cracking its keel
Overwhelming a small trawler with its giant wake
Catching scent of chum being tossed by hobgoblin whalers
Pluming massive jets of water that can be seen for leagues
Cavorting sinuously through the salty spray
Plunging swiftly, only to reappear in a better position
Chasing down a pod of delicious dolphins
Possessing deadly venom, like his smaller sea snake cousins
Circling around a rocky islet, home of the harpy queen
Pursuing a school of buttery tuna
Constricting a ship, about to be set alight - all hands fleeing
Queasily spewing massive amounts of ancient, corroded coins
Consuming seals by stalking their sunning grounds
Quickly submerging to avoid a tethered bolt from a ballista
Crunching on an absolutely gargantuan giant crab
Ramming the starboard side of a schooner
Curling their coiling tail around a schooner's mast
Rearing to full height, eye-level with most crows' nests
Darting up from the deep, its wake flooding a lifeboat
Reeving through large caps in a giant net
Destroying the monthly supply ship for a nearby lighthouse
Ripping sails to absolute shreds, intentionally becalming boats
Devouring sailors, shipwrecked on a treacherous reef
Roaring in frustration as a clipper escapes
Diving after treasure, being flung overboard as a distraction
Savaging a giant octopus, biting off giant morsels of pink flesh
Dwelling within a staggeringly gaudy coral castle
Scuttling a large halfling barge, topped with an entire village
Eating most of a local fishermen's catch, straight from the net
Seeming to surround with its long, surging coils
Emerging from the wine dark depths, to survey for ships
Shimmering like a pearl, with iridescent, nacreous scales
Enraged by a cloud giant's barbed harpoon
Sinking a xebec after stranding sailors on a witch's island
Entwining, locked in mortal combat with a giant squid
Sloughing off parasites by rubbing against rough rocks
Felling the final mast of a foreign frigate
Spawning in a picturesque lagoon, worrying nearby nixies
Flabbergasting even the oldest of salts with eloquent speech
Splintering the rudder of a minotaur man-of-war
Fleeing from the sudden surfacing of a dragon turtle
Striking at a swooping sea wyvern
Followed by clingy remorafollk, tolerated for their cleaning
Struggling to unearth a hoard, half buried due to hurricane
Gliding, just beneath the waves, easy to lose track of length
Swallowing only the tastiest water termites
Glistening scales make for the finest of merman chainmail
Swamping a crucial bridge, connecting keys
Gracefully swimming in some kind of courtship dance
Tangled in massive tresses of kelp, a dryad hitchhiker
Guarding the sunken wreck in which they store their hoard
Terrifying a seaside village into regular sacrifice to appease it
Half-heartedly reaching for a lazily circling roc
Thrashing within a magnificent dwarf-forged net
Headbutting the hull of a sturdy ship wrought from treant wood
Throttling a gnoll pirate, shaking him side-to-side as crew looks on
Heaving as rippling muscles crack a timbered hull
Twisting to avoid a peculiar species of str draining shadow rays
Hissing loudly after being struck by a wave wizard's bolt
Uncoiling their grip from a galleon at a sea cleric's prayer
Impaling a captain with its long, swordfish like snout
Undulating into twisted coral passageways to rest in their lair
Indulging on a large shoal of shimmering silver fish
Unobtrusively slinking, coordinating with rough waves
Interrupting a pirate vessel's boarding attempt
Utterly devastating a local fishery by driving off the catch
Jealously seizing a gold-plated pleasure yacht for their hoard
Vanquishing six sailors in a single swipe of her tail
Jerking to try and dislodge a volley of elf arrows
Violently splashing, in the throes of giant stonefish venom
Keelhauling an unfortunate buccaneer hanging on for dear life
Worshipped by ferocious lizard men on a nearby atoll
Knotting around an orca, trying to drown it
Wounding a merfolk paladin's faithful aquatic steed
Lashing their spiked tail, spearing a great white
Wrapping itself tightly around a warship
Looming over a longship, somewhat perplexed by its prow
Writhing in warm water, heated by undersea volcanic vents
Lunging to snatch a bite-sized buccaneer from the decks
Yanking a ship by its anchor chain through calmed seas - charmed
Luring sailors with its siren like song
Zealously protecting a floating shrine to the sea goddess

Table: shadow
Accentuating an already eerie area, clotting it with gloom
Joyously debilitating a dwarf, can no longer hold his hammer
Adding to their numbers by draining an exorcist
Knavishly slinking, mirroring the movements of a merchant
Annihilating a shivering torchbearer with glee
Lengthening and distorting, filling an entire foyer
Aping a fleeing, debilitated bandit for fun and amusement
Lingering beside a dead dervish, waiting to greet a new friend
Avoiding the brilliant glow of a medium's magical illumination
Looking unnaturally skewed to any artists' eye, given the light
Beckoning with disturbingly long, refracted claws
Looming near an ornate, barely functioning fountain
Benumbing a bugbear, white as a sheet
Lurking in a pool of murkiness below a fly-infested slab of meat
Bisecting the floor, stretching from one side to the other
Materializing due to an illusionist's mishap
Blotting out the gimmer of small pile of coins
Melding/contorting into a spitting image of a medusa's shadow
Blurring usually sharp edges, like the haze above a campfire
Menacing some legend-tripping youths, far out of their depth
Brooding at the light's edge, preparing to spring
Merging with their fleeting fellows as a door swings open
Brushing a terrified tomb robbers cheek with an evil grin
Mocking a cultist for meddling in misunderstood forces
Chasing an oblivious ogre with measured, matching movements
Murmuring to a mute companion cast from a statue
Chilling the air around their favored haunt
Nefariously reappearing behind an overconfident cleric
Clinging desperately to back of a chair, as torchlight sweeps
Nickering diabolically...the only sound they seem to make
Clouding a bone-filled alcove with their impenetrable murk
Noiselessly enveloping a limp lizard man
Coalescing in the shade of a gargoyle-shaped statue's wings
Obscuring the somewhat obvious trigger to a trap
Copying the lurching gate of an empty-eyed zombie
Overpowering an owlbear to add to a -dimensional menagerie
Cowering in the charcoal dust of a disused fireplace
Perfectly pantomiming a paranoid porter
Creeping through a colony of shrieker in quiet darkness
Pooling in an inky blot to share secrets about their surroundings
Crouching behind an overstuffed alligator armchair
Projected, larger than life, clinging to a crumbling fresco
Curving around a corner, in gnarling almost agonizing twists
Prowling amid ankle-high, neatly stacked piles of bones
Dancing across ceiling to the silent music of a flickering candle
Quivering perceptibly in anticipation of their next victim
Dappling to enhance their disguise, wincing silently
Rapaciously sapping the strength from a scout
Darkening a doorway, decorated with angelic children
Receding under a door in search of prey
Deliberately blocking all exits with strategic positions
Recoiling as berserkers light a protective bonfire
Detaching from the fat, ailing friar they're following
Ruthlessly propagating after uncovering a kobold colony
Draining the vitality from a group of goblins, one at a time
Silhouetting a grinning gold idol atop an altar, an ideal ambush
Eclipsing an important clue, by shrouding it in shade
Skulking along the wall like an animate scorch mark
Encircling a censer, smoking anemically in the center
Slanting down a stone ramp away from the light
Encroaching the edge of a medium's shimmering silver circle
Slithering along the underside of big, bench-like pews
Enervating a valiant veteran, standing her ground as allies flee
Smudging slightly at the edges, briefly reminded of former lives
Engulfing a terrified gnoll in umbral misery
Sparring playfully with each other, literally boxing
Extinguishing a gnome's last lucifer with a maniacal laugh
Spreading across a cut-glass throne
Fading from view as a lantern lugging living statue shuffles past
Stealing strength from a lip-biting barbarian
Falling lightly on a small pile of purloined children's toys
Stretching to impossibly spindly shapes, to reach a stirge roost
Flickering in perfect time to a sputtering oil lamp
Superimposing on the surface of a sculpted sarcophagus
Flitting across the face of a gruesomely tusked bust
Swallowing the small shadow of a halfling, preparing to strike
Frightening a famished fighter, who thinks he's hallucinating
Tinting the surface of a silvered mirror slightly
Gathering blots of tenebrous gloom together like quicksilver
Tiptoeing behind a thoul
Generating a slight chill and rime on areas they cast
Tormenting a terrified trader
Gliding alongside a crafty, catlike cutpurse
Towering over a sinewy troll with elongated, grasping hands
Hanging onto the heels of a hobgoblin
Trailing troglodytes, waiting for their glowing fungal torches to fade
Haunting a small shrine to the deity of crepuscular dusk
Unexpectedly enshrouding even a keen-eyed elf
Hissing as a paladin draws a glowing two-handed sword
Utterly blanketing the area, amplified by terror
Hovering just outside a beam from an abandoned bullseye lantern
Veiling a vast vestibule in penumbral darkness
Impeccably mimicking a fluttering giant bat flying above
Voraciously slurping vitality from their only victim in weeks - a rat
Inching silently toward an unsuspecting orc
Waning in proportion to a wizard's glowing wand
Intruding into this reality during a summoning gone awry
Wilting a desperate dryad
Jaggedly crisscrossing the room due to a filigree girded sconce
Yearning for a true, utter night to envelop the world

Table: shark, bull
Bludgeoning each other for territorial dominance
Lashing violently on the end of a sturdy steel line
Brushing along the seabed in search of skates
Migrating to warmer waters with abundant food
Chasing away a large saltwater crocodile
Nosing and nudging a very annoyed giant crab
Congregating around a whaling ship, feeding on chum
Prowling silently through a kelp forest
Dashing swiftly through a school of jellyfish
Ramming a lifeboat, startling the sailors within
Diving after a sinking, struggling dwarf
Returning to breeding grounds, violently defending them
Dragging a sea bird underwater to dine
Scavenging on the carcass of a seal
Dwelling in comfortable caves among a colorful reef
Scenting distant blood and abruptly scattering
Feeding on the floating body of a huge sea snake
Skulking around the edges of a merfolk village
Floundering within a fisherman's net
Slamming into the starboard side of a small sailboat
Ganging up on a great white to drive her away
Snapping at an angry sea troll
Hectoring an octopus about to spray its ink
Stalking a run of salmon, all the way inland, upstream
Herding a large school of fish into shallower water
Struggling in the undulating arms of a giant octopus
Hunting as a coordinated team, outflanking their pelagic prey
Swerving suddenly to take a chunk out of a big barracuda
Infesting coastal rivers, surprisingly freshwater tolerant
Wounding a whale calf, angering the mother

Table: shark, great white
Ambushing a fishing boat from below
Marauding near a sandy beach, where nixies dwell
Battering floating flotsam angrily
Mistaking a marooned medium for a seal
Battling a bottlenose dolphin, separated from the pod
Picking off stragglers from a school of tuna
Breaching in a splashy display of awful majesty
Retreating from a large pod of killer whales
Communicating telepathically, swallowed sentient dagger
Ruthlessly attacking a shiver of smaller sharks
Cutting through the waves, with tell-tale fins
Savaging one of a sea hydra's several heads
Developing a taste for the flesh of humanoids
Seizing the shell of a struggling sea turtle
Devouring the ragged remains of a sea serpent
Slapping the water's surface with their massive tail
Festooned with a pair of patient and overprotective remora
Smelling a single drop of blood from a wounded merman
Foaming water red in a ferocious feeding frenzy
Surfacing to accept a sacrifice from superstitious pirates
Following a humpback whale creche closely
Surging above the waves to take a low flying large roc
Gliding effortlessly through choppy seas
Swarming around a shipwreck as sailors scream
Grabbing vicious hunks from the side of a sperm whale
Tearing into the fin of a fleeing giant bass
Inquisitively biting an undersea gargoyle
Terrorizing a stony skerry, home to breeding seals
Leaping from the water with huge, gaping jaws
Violently thrashing a narwhal back and forth

Table: shark, mako
Approaching a fleet of fishermen hungrily
Lunging unexpectedly at another shark in the shiver
Brutally pecking at a bloated sunfish
Lurking among the ribcage of a sunken galleon
Charging into a scintillating school of sardines
Menacing a merman trader's sea horse draft animals
Chomping on a writhing swarm of inky cuttlefish
Overtaking a galley, after a drowning rower
Churning the seas around a reef in a feeding frenzy
Patrolling their sea sorceress' coral atoll
Circling a cleric, clinging to a floating barrel
Pursuing a wreck diver, mostly out of curiosity
Clamping onto the arm of a hobgoblin buccaneer
Quickly spitting out a spiny pufferfish
Darting swiftly through seaweed in search of prey
Racing through waves with wing-like pectoral fins
Detecting and drawn to a wounded otter
Reappearing after chasing off an inquisitive dolphin
Eating a scavenged swordfish corpse
Semi-domesticated by capricious aquatic elfs
Escaping from a gnome trawlers damaged nets
Slinking sleepily along the seabed
Flocking around the entrance to a sea serpent's den
Starving due to overfishing, attacking boats
Gobbling the edges of a shoal of mackerel
Stealing a sturgeon off a long fishing line
Harpooned by a sea ogre hoping for shark-fin soup supper
Studying a school of shad, probing for weakness
Hounding a sea dragon for scattered scraps
Swimming swiftly alongside a pirate ship

Table: shrew, giant
Aggravating halfling farmers by ravaging their cabbage crop
Narcotizing a wolf that got a little too curious
Alarming a swarm of bees
Nibbling on a dead bandit
Ambling up a collapsed column
Nosing through leaf litter, in search of nutritious newts
Attacking a snail, the size of sheep
Obliterating a dropped backpack and the rations it contained
Barking a squeaky warning to unseen enemies
Ousting an owlbear from her den, just too much trouble
Biting into a massive mushroom with needle-like teeth
Outraged at the sight of another shrew
Breathing with a wheeze after exposure to yellow mould
Overpowering a driver ant, biting off legs one at a time
Brutalizing a bombardier beetle
Patrolling their patch, on the lookout for a mate
Burrowing at the base of a massive, ancient ash tree
Pawing at a barrel of pickles
Bursting forth from the earth to snatch a giant centipede
Perplexing a swarm of bats with conflicting echolocation sounds
Careening down a corridor towards you
Pouncing from above onto an unsuspecting ghoul
Catching a large cave cricket in snapping jaws
Preying almost exclusively on overpopulated carcass crawlers
Chomping on an abandoned basket of golden apples
Prowling through a clay drainpipe - echoing, splashing sounds
Clambering up a hobgoblin's torso - going for the head
Purposefully antagonizing a rock python
Climbing skillfully down from a top a plinth
Pursuing the fragrant smell of roasting mutton
Concealing tasty turnips in a cache for leaner times
Raging at a bemused and completely immune gargoyle
Co-opting a giant mole tunnel
Rending open a big wheel of burlap wrapped cheese
Defending the entrance to their burrow from a giant scorpion
Rooting around near a worried gnome stronghold
Demoralizing a party of greenhorn adventurers - fleeing
Rummaging through pungent troglodyte garbage
Detecting a wriggling giant grub beneath the soil
Scaring away a nosy giant ferret
Devouring dryad seedlings
Scooping up mouthfuls of spilt grain, barely chewing
Digging furiously after an earthworm as long as your arm
Screaming commences as it launches itself onto an acolyte
Dowsing for buried tubers with their sensitive snout
Seething with fury as lizard men manage to hold their ground
Dredging a puddle in search of tasty fat frogs
Shoveling larvae from a toppled giant wasp nest into their mouth
Driving off a massive, well-armed goblin bodyguard
Shredding a sack of sweet potatoes
Emitting an unpleasant, skunk-like musk
Smelling the muddy tracks left by a giant toad
Erupting out from a pile of rubbish and rags
Squeaking of shrewlets surrounds a proud and defensive mother
Excavating loamy soil to form a brooding den
Squinting with beady eyes at a stirge roosting out of reach
Fighting an ogre and not backing down
Stalking a medium after getting a whiff of her component pouches
Flicking their whiskers, tasting the air
Startling hardy berserkers, bivouacking for the night
Flinging a prodigious amount of dirt up as they delve
Stealing a prize-winning pumpkin, rolling it comically
Foaming at the mouth and spitting mad - kobolds cowering
Striking, lightning fast, at the neck of a coiled giant rattler
Foraging for fallen nuts and seeds
Suddenly leaping onto a rust monster
Frightening a group of veterans
Sweeping through detritus with an over-active nose
Gnashing ferociously at a terror-stricken gnoll
Tantruming after being sprayed by a giant stinkbug
Going completely berserk on a bugbear
Tearing into the carapace of a cave locust
Guarding a dead caecilia that they intend to feast on for weeks
Temporarily "blinded" by a cacophonous racket and panicked
Hunting driver ants in a rare example of cooperation
Terrifying a warhorse, bucking off her paladin rider
Hurling themselves fruitlessly at a living statue
Tracking gelatinous cube, an acquired taste
Inhaling an entire mound of termites
Tunneling into the side of an ancient barrow
Inspecting their territory for signs of interlopers
Twitching their pointy snout in anger after smelling another male
Intently sniffing a spilt vial containing a potion of growth
Undermining a monument to a brave vampire slayer
Investigating a cowardly dwarf's helmet, cast off when he fled
Vociferously snuffling through an abandoned tent
Jumping onto the back of a mountain lion - claws & teeth blazing
Voraciously eating a cyclops' most treasured vines
Listening intently to locate their slithering giant slug prey
Wading across a pool of water, barely getting wet thanks to thick fur
Live hoarding - storing prey they've paralyzed with their venom
Weaning a large litter and extra touchy
Meandering through a hedge-maze
Wearing down their teeth as they gnaw on ironcone seeds
Menacing a wine merchant and his cask-laden mule
Whisking the floor, to-and-fro as they follow a scent
Muddling about "blindly" after a shrieker begins to caterwaul
Widening the entrance to their burrow to bring in a fire beetle
Munching contentedly on a crab spider
Zig-zagging their way across a very trapped room

Table: shrieker
Advancing sluggishly toward a dead dire rat
Muffled by a mauled missionary's silencing scroll
Alerting an alchemist of laboratory intruders
Mulishly inching toward a dead donkey
Announcing the arrival of an obliviously deaf acolyte
Nurtured by wax-eared witches, for a valuable singing cheese
Annoying a kobold archer - trying to get some sleep
Obscuring a mosaic map of this dungeon level
Arranging themselves atop a decomposing driver ant
Overgrowing a fusty owl bear carcass
Attaching to circuitous treant roots
Overhanging a charnel pit, straining to reach the bones
Becoming slowly sentient after snacking on a spell book
Piercing the stony silence with an ear-splitting squeal
Billowing forth fuchsia clouds of choking, obscuring spores
Poisonous to warp beasts, if brewed in a tea
Blaring, fog-horn-like, after a bombardier beetle nibble
Possessing tubular, graduated ranks of organ-like pipes
Blotched with sickly olive music notes spots and red gills
Preventing green slime from surging through a sluice
Breaching a decaying door with decades of patience
Prized by potion stirrers to improve wakefulness
Breaking down the body of a bugbear, bedecked in green fuzz
Producing a shrill shout, confusing the bats above
Budding with pale, fleshy orbs, hollow and rattling
Proliferating rapidly on dead fish in a dried-up pool
Caking the darkened corners of a small chapel
Puffing hallucinogenic prophecy spores - snatches of future sounds
Capped with brilliant blue, horn-shaped structures
Quietly sprouting new noisy gills after rats gnawed them off
Carpeting a cave, crowding out a rare medicinal mushroom
Raising clamorous hue and cry due to haywire photoreceptors
Clinging to a corridor wall, at a crucial intersecting corner
Resembling harps with sickly, sticky mycelium filaments
Clustering around a cave locust carapace
Reverberating throughout, thanks to a vaulted ceiling
Colonizing a colorful carpet depicting a hunting scene
Rising in response to cloying carrion on the air currents
Composting a coin concealing cushion
Screaming a single word in lawful - vigilance
Creeping deliberately toward a deceased dwarf
Shedding a smelly film as they slowly traipse
Cultivated by a hobgoblin herbalist, trained in marching tunes
Shuffling into a chirping mass to exchange spores
Dancing hypnotically in a glacially slow waltz
Signaling to shadows that pickings are present
Deafening a drug dealer, searching for dreamcaps
Singing a somnolent lullaby instead of shrieking
Discordantly screeching as zombies lurch through
Sounding off in strident sequence - a cacophony of racket
Drowning out bickering bandits nearby
Spreading and devouring the priceless scrolls in a library
Dusting dungeon walls with sneeze-inducing spores
Squeaking inquisitively at a bioluminescent moth
Echoing throughout the complex, disturbed by an orc
Startling a sleeping gnoll sell-sword
Emitting high-pitched frequencies that antagonize dogs
Stinking of strong drink as they ferment old potatoes
Encircling myconid remains, almost reverently
Sullenly glowing with a sickly chartreuse effulgence
Feasting on a fighter's festering corpse
Summoning a curious basilisk, associating them with food
Filling a crate, once containing cabbages
Swelling pustules loudly wheeze when disturbed - bagpipe-y
Gathering in moist clumps near a dripping stalactite
Symbiotically associated with saffron yellow mold nearby
Germinating on a giant skeleton, near a massive sword
Tasting like a symphony, uniquely delicious before toxin takes hold
Growing on the underside of a tempting trap door
Topped with cymbal-like caps that clatter and crash
Growling a warning to a nearby crab spider colony
Triggering a rain of small rocks/stalactites with their loud cries
Heralding a troglodyte stench shaman's arrival
Trumpeting tuckets and fanfares, to greet their vivamancer
Home to an unusually chatty dryad
Turning slowly around a corner with squelching sounds
Hooting with strigine sounds at a clumsy skeleton
Undermining an invisible stalker's attempts at stealth
Housing a colony of completely earless cave sprites
Voraciously consuming the corpse of a cleric
Howling mournfully as a cave crab clips off caps
Waddling ponderously across a rickety bridge
Infesting the surface of a treasure chest
Wailing fruitlessly at a wight
Invading a goblin garbage pile, full of broken baubles
Waking up a golem from pleasant dreams of wooly sheep
Jarring to overhear - their shriek sounds of distressed damsel
Warbling with a wet yodel, underwater
Keening continuously due to a sputtering torch
Warning a wicked wizard of intruders to her sanctum
Living safely on the ceiling, but still easily startled
Weakening a wooden floor with their microscopic chewing
Looming, having ballooned to nearly the size of an ogre
Weathering frequent harvests from a thoul fungomancer
Luring locals to deal with a trespassing trap-finder
Whining softly under a trickle of water from above
Maturing rapidly, frequently fed by lizard men
Whistling every hour as part of an ingenious water clock
Moaning softly as they mulch a minotaur
Zither makers seek their woody stems for magical instruments

Table: skeleton
Adjourning to a nearby chamber after driving away a noisy owl
Mobbing a medium, who came here to study ancient inscriptions
Adorned with noisy bronze chains that foretell their arrival
Muttering paeans of thanksgiving in a long dead language
Ambling on unsteady legs, across a rock-strewn floor
Nodding at the silent gestures of their necromancer
Angrily clawing gooey chunks from a mud effigy
Obeying orders from a sweaty and nervous acolyte
Animating slowly after a graven idol is moved
Obliterating a mirror that mocks their fleshless forms
Arriving in time to assist a nearly victorious ghoul
Occupying the opposite bank of a rickety rope bridge
Astride skeletal giant lizards that can climb walls still
Overrunning their smallest - an armored dwarf skeleton
Avoiding a bone hungry black pudding
Parading with a reliquary box held aloft, it contains a tooth
Bashing rust-covered blades against dented shields
Patrolling with loaded crossbows & silver tipped ammunition
Besieging a nearby inn, only on holy days
Playing a femur flute, while others drum on hollow skulls
Blanketed with black beetles, dripping in onyx cascades
Pounding bony fists on a table in unison
Charred slightly after lamp-oil immolation
Pouring algae-laden water from a huge amphora into a font
Chiseling at a played-out seam, mechanically
Pulling the legs off a giant centipede, one at a time
Clattering across an echoey floor, glancing to-and-fro
Quarrelling over a ratty silk shawl, embroidered with dull pearls
Compelled to peacefully escort any visitors to the nearest exit
Quoting a famous jester incessantly and laughing maniacally
Crushing every single unattended skull they come across
Raising alarm by striking a bronze gong with a huge mallet
Dangling from a massive, low-slung chandelier
Rending an unlucky elf with sharpened phalanges
Deformed by bone worms, practically perforated in places
Retreating from a cleric, brandishing a golden triskelion
Draped with dangling bits of leathery, mummified flesh
Returning to their posts after slaying a giant spider
Drilling incessantly, presenting arms to an absent captain
Robotically drawing water from a well, long dry
Eradicating every living thing, down to the rats, in this room
Rowing a wrecked galley for eternity, not a drop of water in sight
Failing to brace a door as an ogre smashes through
Shoveling colorful, mineral-rich clays into gaping mouths
Faltering slightly every time they cross an inlaid silver circle
Silently brandishing spears in surprisingly good condition
Fawning over their king, a shriveled corpse, seated on a throne
Silently shadowing an unsuspecting corpse smuggler
Fending off goblin looters in a frantic fracas
Sitting cross-legged in a circle, around a flickering lamp
Festooning an arch with brittle, bird/bat bone garlands
Skulls perforated by distinctive, star-shaped trepanation holes
Genuflecting mechanically as they pass a statue of a saint
Smashing fragile clay urns with great aplomb
Gibbetted in cages littered with coins, biding their time
Sorting a large pile of coins into teetering, mismatched stacks
Glittering gold teeth adorn each jeering jaw
Stoically saluting anyone/anything that passes by their posts
Gnashing tusks betray their orcish origins
Strapping a sacrifice to a rood with wyvern leather straps
Gnawing fruitlessly on the body of a bandit
Sulking at the bottom of a spiked pit - former victims of a fall
Grasping hungrily at a beautiful painting of a pastoral cow
Tackling a zombie, animated by a rival cult
Grinning unsettlingly with gap-filled, crenelated smiles
Taunting a prisoner, confined to a cast-iron cage
Groveling at the hems of their necromancer's robe
Thawing a massive block of ice containing a manticore
Held at bay by the holy symbol of a tiring cleric
Throttling the bugbear that crept into their crypt
Hiding among the moldering bones in a family crypt
Toasting with empty leaden goblets, every few minutes
Hobbling on wobbly, mismatched legs
Trammeled by rusting manacles that groan with each step
Impaling a squealing bat with a perfectly aimed javelin toss
Tugging on a taut rope to hoist a creaking dumbwaiter
Isolating a veteran from the rest of his adventuring party
Tumbling out of a wardrobe closet in a clattering cacophony
Jamming a portcullis lever in the "down" position
Unshackling themselves from deceptive all-mounted chains
Jolting upright after sensing nearby life
Venturing, newly arisen, from their cold and silent catacombs
Knocking with ivory knuckles on a wall, listening for responses
Wading in brackish water, pelvic girdle deep
Lying about in disarticulated piles, waiting to strike
Waiting for instructions from a nearby necromancer
Leaping into the fray after berserkers desecrate a tomb
Walking with a strange gait, only stepping on every third tile
Loading moth-eaten sacks with bleached bones
Wandering without aim in large concentric circles
Locking the iron lid of an oubliette with a ring of namesake keys
Whirling around in a contagious danse macabre
Looming over an unconscious halfling
With tails and elongated maxillaries, skeletal lizard men
Marauding chaotically, even striking each other and themselves
Withering under the holy light of a powerful paladin's prayers
Materializing from choking clouds of bone-dust
Working tirelessly to fill a bottomless pit with rubble
Meting retribution on a gnoll daring to disturb their rest
Yielding spare bones to a bent and broken comrade

Table: snake, giant rattler
Angrily biting a blundering bugbear
Nesting a little to near a heavily trafficked area
Basking atop a rusting, but still ornate breastplate
Preying upon a giant bat that flew too low
Bearing already quite venomous live young
Rattling ear-splittingly as skeletons stumble by
Coiling in a defense posture, head raised and rattle-ready
Retreating to the safety of a hill giant's boot
Digesting a giant shrew, swallowed a few days ago
Rustling leaves and debris as they glide across the ground
Envenoming a veteran who should have worn taller boots
Sensing nearby vibrations and seeking concealment
Eyeing a preening mountain lion hungrily
Shaking their tail in time to a snake charmer's flute
Following the pheromone trail of a female
Snapping testily at an overconfident ogre
Gone to ground after smelling giant ferret
Squatting in the burrow of a caecilia
Hunting a gasping, slowly dying giant toad
Startling a caravan of traders, panicking their horses
Infesting every nook and cranny, gathered here to breed
Striking a dire wolf as the pack yelps and growls
Jolting all listeners with a sudden resounding rattle
Vibrantly colored with yellow-bordered black diamonds
Losing their crypsis to a giant rat after missing a strike
Warning everything of its presence with a staccato cacophony
Loudly clattering their tail-scales at a cautious mule
Weaving its way around an extremely lifelike medusa statue
Mulling over how to best to swallow a giant porcupine
Whipping around, seething at a surprised dwarf

Table: snake, pit viper
Ambushing a hawk, preening on a perch
Licking the air to taste for potential prey
Blending in with verdant surroundings
Meticulously eating eggs much larger than its head
Climbing and entwining within a decorative iron gate
Protecting their clutch with surprising maternal fury
Congregating in a warm, disused den
Racing across sands with sidewinding slithers
Crossing paths with acolytes, who collect them for rituals
Sheathed in shimmering, emerald scales - skins prized by nobles
Dangling their long, sinuous bodies off bare branches
Shedding a layer of skin, milky eyed and perturbed
Emerging from a deep crevice, preferring darkness to hunt
Slithering contently around the shoulders of a mummy
Exposing the white lining of its gaping mouth in threat display
Springing from its hiding place on an unsuspecting sheep
Following a dying rabbit using its heat sensors
Stretching out in the shade of a snake loving treant
Frightening a fleeing prisoner, crossing a creek
Tempting prey with novel, spider shaped tail-scales
Gracefully skating across the surface of a pool
Trusting their peerless golden camouflage to hide atop a hoard
Heat-sensing smaller snakes to snack on
Unhinging their wide mouth to strike
Hypnotizing a helpless halfling
Vastly bloated belly betrays a recent lavish meal
Instinctually drawn towards temples and shrines
Waiting patiently for unsuspecting birds to land nearby
Lairing in a large rotting log
Warming themselves on a sun-dappled stone

Table: snake, rock python
Ardently crushing an unfortunate antelope or deer
Scaling a large obelisk to dine on the roc eggs above
Barely tensing beneath reticulated scales
Seeking a powerful sorcerer to undo this polymorph curse
Choking a troll, wrapped like a scarf around their neck
Sheltering r in a massive, sun-bleached tortoise shell
Constricting around a marble statue, shattering the stone
Sluggishly chymifying a chimera
Cradling a giant catfish in its coils, preparing to swallow
Smiling with slit-pupil, unblinking eyes the size of dinner plates
Flicking a sword-sized, bifurcated blue tongue
Squeezing the life from a large crocodile
Flowing unstoppable, around the edges of a pit
Strangling an elephant, no mean feat
Ingesting an owlbear, beak first
Stunning a wyvern with a well-timed strike
Intertwining themselves around a profane altar
Swallowing their second warhorse as knights look on in fear
Lazing confidently in the open, an apex predator
Thawing from a chilly night/brumation
Lunging half-heartedly at an alighting griffon
Tightening thick coils around a trunk containing a treed thief
Lurching its massive bulk across a shard strewn floor
Uncurling themselves from a now-suffocated cyclops
Muscles rippling beneath shiny bronze and oily black patterns
Worshipped and well-fed by devoted lizard man zealots
Pursuing a centaur tribe, eyes on the young foals
Winding their way down corridors, barely wide-enough
Rasping their smooth scales against slate tiles
Yawning widely, one could stand in the maw and not touch the top

Table: snake, sea
Agilely gliding across the surface of the water
Injecting lethal toxins into a shipwrecked sailor
Balling around the crown of a sunken, sculptured bust
Looping lazily around an abandoned anchor
Brilliantly striped in bright, headache yellow
Masterfully sinuating across the seabed
Chasing after a frantically paddling pearl diver
Noiselessly stalking giant crab on the beach
Consuming a brilliantly "plumed" parrot fish
Orbiting a shoal of delicious daggerfish
Crawling carefully along a rocky outcrop
Plumbing holes where fish hide among the reefs
Delivering its pinprick bite to a merman diplomat
Recklessly surfacing in a sea roc's shadow
Disappearing into the darkening depths
Serving as a familiar for an aquatic medusa witch
Diving after a floundering shieldfish
Shivering from deep waters, come ashore to bask
Elegantly swimming against a backdrop of brilliant blue
Struggling to swallow a still-twitching salmon
Fleeing from an indiscriminately hungry shark
Terrestrially sunning atop an overturned lifeboat
Floating listlessly in the sun to speed digestion
Undulating underwater, antagonizing an octopus
Gorging on a school of shimmering fry
Wallowing in the warmer water of a shallow bay
Grabbing a seabird from beneath the surf
Wriggling their way up an oar towards an unsuspecting rower
Helplessly thrashing, inadvertently hooked on a line
Zig-zagging the pebbly beach, looking for a suitable nest

Table: snake, spitting cobra
Aimlessly prowling in search of rats and rodents
Peering intently at their reflections in a mirror
Barring their fangs, practically dripping with venom
Poised to strike a careless kobold
Blinding a basilisk - lucky break
Quivering as cultists sprinkle them with unholy water
Catching skittering bats on the wing
Ringing a stone font, filled with bubbling magic liquid
Curling tightly around the base of a gold idol
Sibilating softly into the ears of a troglodyte oracle
Defensively postured, as a cleric chants during approach
Spitting directly into the eyes of dervish
Dwelling within a strategically disguised pit
Sunbathing beneath a shaft of light
Ejecting their venom at an elf's face
Surprising a smuggler, searching a strongbox
Forked tongues tasting the air around a sleeping prince
Swaying rhythmically as they fix their gaze on a grave robber
Guarding a gateway that leads to an easy exit
Threatening to strike a summoner, stumbling blindly
Hissing loudly after a distant thud disturbs their rest
Uncoiling and relaxing after a hobgoblin collapses
Intruding on tomb raiders resting
Unfurling their distinctively rune-marked hoods
Knotting and twisting in a scaly agglomeration
Winding around the legs of a paralyzed pilgrim
Mobbing a swarm of scarab beetles
Wrapping themselves around the legs of a warm living statue
Molting, with translucent skins sloughing off
Wreathed around a suit of magic armor

Table: spectre
Addressing newly materialized spawn in an oddly caring voice
Limping as they drag a spectral bear trap on their ankle
Animating several skeletons simultaneously in a magic circle
Lingering until every grave in a nearby cemetery is cleaned
Avenging her death at the hands of elfs by targeting them first
Looming menacingly from behind an altar covered in bones
Balefully glaring at their portrait, painted from life
Lurking by the sputtering flame of a single, burning torch
Beckoning a greedy thief, almost seductively
Masquerading as the soul of a munificent martyr
Bleeding endless ectoplasmic gore from many open wounds
Materializing to chastise a group of quarreling wraiths
Breathing becomes difficult the longer one gazes upon them
Menacing a tribe of fearful neanderthals
Brooding forms tiny smoke skulls that swirl above their head
Mercilessly mocking an inexperienced evil acolyte
Chasing after a fleet-footed halfling with grasping hands
Murmuring as they consult a portal, pulsing with black energy
Chilling the area, so much so that a thin layer of frost forms
Muttering obscenities as they shear a braying black goat
Clad in clinking bells, that ring out a tinny funeral dirge
Noiselessly shattering like dark glass, only to swirl and reform
Clutching their blood-stained wedding dress to their chest
Ominously tapping a wickedly curved blade on a tabletop
Confronting a cleric after causing their symbol to shatter
Ordering their shady spawn to decimate a village
Convincing ghouls to raid a local settlement for prisoners
Passing a row of saluting skeletons, as if inspecting troops
Crumbling and reforming constantly in a mass of ash/embers
Pontificating vociferously to the dry carapace of a fire beetle
Cursing feebly in a tongue not spoken in centuries
Producing spectral implements of torture, floating around them
Debating with themselves, using separate voices
Profaning a humble shrine, dead attendants all around
Demoralizing a once brave dwarf warrior
Protecting an urn containing a powerful vampire's ashes
Desolating a dryad grove by poisoning the soil with their bile
Pursuing an age-old foe - an ancient but still fearsome unicorn
Dissolving as they pass through a door
Quietly sobbing to catch her prey completely off guard
Draining the soul from a swordsman, slowly to savor it
Reaching into the chest of a veteran to stop their heart
Echoing faint blasphemous litanies from every direction
Recoiling as a gnome reads a scroll of protection from undead
Ecstatically clinging to the neck of an exhausted nomad
Resembling royalty emblazoned on the old coins nearby
Emerging from the cursed adamantine idol binding them here
Rising from the cooling corpse of a crusader
Eulogizing a victim as they inhale their life-force
Robbing breath from a sleeping adventuring party
Fading and reforming, each time more horrible than the last
Rotting phantasmal strips of flesh hang from their ghostly bones
Floating above the surface of a pool of unholy water
Shattering iron bars like icicles with a sadistic grin
Forming from smoke from a brazier filled with saint's bones
Shimmering tenebrously, like a foggy cataract floating on eyes
Frequenting sites of tremendous tragedy, if locked in a pattern
Shrieking as they squeeze lifeforce from a lizard man
Frightening a family of farmers every full moon
Sinking into the ground so that only their torso is visible
Frowning with eyes and lips stitched shut with black twine
Sitting atop a tarnished silver throne depicting ice devils
Galloping their spectral steed through all obstacles
Sneering as a sorcerer cowers before them
Gibbering and chanting half-remembered prayers
Speaking in a tender, almost maternal, tone to a crying paladin
Gleaming within a swirl of red embers and dark motes
Stalking a tomb robber, hoping to destroy the things they love
Gliding inches above the ground, still staining the floor
Starving for living vitality, reduced to withering bats
Grieving over the crumbling skull of a former enemy
Swiftly desiccating an entire brigade of brigands
Grinning with a sinister smirk that seems to bisect their face
Tainting a medium's spellbook with disgraceful litanies
Guarding the tomb of a powerful anti-paladin
Toppling a circle of religiously significant statues, one at a time
Hauntingly crooning old nursery rhymes
Torturously dipping his charred fingertips in holy water
Hounded by the faint odor of sour milk and grave soil
Trapping bandits in a dead-end passage
Hovering in impatient circles above a dying minotaur
Unbearably screaming telepathically at anyone wearing red
Howling with impotent rage at a defiant bishop's crosier
Uncontrollably shivering by a bonfire of holy books
Hunting pieces of a profane artifact from the wraith wars
Vanishing in misty flickers, only to reappear
Infusing a natural magical spring with unholy corruption
Veiling furniture in ectoplasmic cobwebs
Intently watching two heroes trying to strangle each other
Walking in circles around a sword stuck in the ground
Interrupting a clandestine meeting between devil swine
Weeping meekly by the sarcophagus of their former lover
Joylessly shaping waxen effigies of holy personages
Whispering blighted phrases to counteract a cleric's turn
Keening debased hymns as they erase holy books
Wilting all plant-life in their presence, shriveling to dust
Laughing at a play, performed by clumsy zombies
Wringing a noble descendant's neck
Leading a derisive procession, draped in stained vestments
Yawning in boredom from centuries of unlife

Table: spider, giant (black widow)
Amputating the hind leg of a cave locust
Hoisting a still twitching tiger beetle into a corner for later
Brooding an egg sac, rolling it around and around
Immobilizing several struggling stirges
Cannibalizing a contorted casanova post coitus
Liquifying the organs of an orc, stiff and pale
Casting silken strands into corners to rebuild their web
Mending her damaged meshwork meticulously
Clinging menacingly on a cobwebbed ceiling
Obscuring an exit/entrance completely with webbing
Cocooning an ashen faced acolyte
Preening monstrous mouthparts repeatedly
Constructing a sturdier guideline across a chasm
Rappelling rapidly to fetch a robber fly that wriggled free
Discarding the husk of an utterly drained giant bat
Retiring to a convenient alcove as hobgoblin boots stomp by
Eating damaged webs to regain essential nutrients
Slowly descending via their spinnerets
Ensnaring several sprites with strategically placed toil
Stepping lightly over a treacherously trapped floor
Entangling a goblin bodyguard, on his way to betray the king
Strumming strands to draw a curious carcass crawler closer
Flinging bits of armor and a helm from her home with a clatter
Suspending an enveloped driver ant
Glistening black in the damp, her telltale red timer blazing
Swiveling to confront a halfling, trying to rescue a friend
Guarding her skittering spiderlings tenderly
Tugging on a silken skein to test its resiliency
Hanging, stock-still, in the center of her gossamer abode
Weaving a magnificent labyrinth of interlacing webs

Table: spider, giant (crab spider)
Ambushing a squad of kobolds, armed only with torches
Lurking above doorframes, perched and ready to pounce
Carrying horripilating spiderlings on their broad backs
Mimicking bleached bone amid a large pile of skeletal remains
Climbing down from their ceiling corner perches
Nesting cozily among gothic ceiling arches
Clutching a dead giant rat in their hairy pedipalps
Secreting pheromones, allowing them to move among driver ants
Coating the floors, walls, ceilings with fine, glistening cobwebs
Presenting a silk wrapped robber fly to a potential lover
Consuming an elf, dead by their toxic bite
Repairing a section of web, mistakenly placed in front of a door
Dashing to perceived safety underneath a defaced altar
Scaling ornately carved columns that support the ceiling
Defending pulsating egg sacs, hatching any minute now
Scuttling across echoing flagstones
Dining on a veteran, they caught sleeping on watch
Slinging innovative web "bolas" at their prey
Dismantling a fire beetle as they fight over its remains
Slurping the liquified insides of a dwarf
Envenomating fish - they skate on the surface of a pool
Spinning fine filaments that serve as tripwires to alert them of lunch
Gnashing teeth of a gnoll soon cease as their venom takes effect
Squatting silently in the shadows cast by medusa statues
Grooming bristly faces, eight shiny unblinking black eyes staring
Stalking an abandoned, heavily laden mule, misplaced by his owners
Hiding among huge mushrooms, blending in well with the caps
Swaddling a foolhardy harpy, ensnared by their webs
Injecting their venom into a struggling killer bee
Waving iridescent palps in an intriguing courtship display

Table: spider, giant (tarantella)
Attacking a pair of tangoing traders
Laying tambourine shaped eggs along the base of an ornate dais
Biting a group of jitterbugging bugbears
Leaping onto line-dancing lizard men
Catching a cleric mid-conga
Lining their lairs with fusty sheet music
Clambering over a passed-out paladin
Menacing a moshing medium
Covered in itching hairs, prized by thieves as lockpicks
Molting, it's said the skins make for marvelous banjos
Creeping rhythmically, as if to unheard music
Patrolling their territory with synchronized cadence
Crouching suddenly, about to spring on an unsuspecting skeleton
Scurrying after a sashaying smuggler
Dismembering a druid that danced himself to death
Snatching a squirming giant centipede in their fangs
Dwelling among piles of moldering books
Springing suddenly from a trapdoor onto a passing giant shrew
Feeding their young a friar, frazzled from the foxtrot
Tailing some tap-dancing troglodytes
Glaring at a tuning bard, almost expectantly
Tensing their long, piliferous legs, one at a time
Grabbing at gamboling goblins
Thrumming on hollow skulls/webbed rib-harps with their pedipalps
Hauling a horse that died from excessive dressage
Twitching with revulsion at the cry of an atonal shrieker
Hunting hurtling hobgoblins
Whistling an infectious tune through the slits in their abdomen
Jumping on an oblivious bombardier beetle
Wrapping up an unconscious apprentice as their wizard waltzes

Table: sprite
Amusing themselves with an elaborate "talking sword" prank
Gathering honey from cooperative and friendly bees
Befuddling bugbears by making loud noises with every step
Giggling uncontrollably at the sight of a hairless gnoll
Bestowing an impressive pair of antlers on an acolyte
Glamouring themselves to appear grotesque for entertainment
Bewildering a bandit by swapping their face with a nobles
Gliding softly whilst gripping propeller shaped samaras/seeds
Confounding a cleric by hiding their holy symbol in a skull
Guarding a sleeping figure, covered in cobwebs and moss
Confusing a kobold by flying around in their shoes
Haunting an abandoned barrow, responsible for many local rumors
Cursing a craftsman by with great skill, and an allergy to money
Helping a bluebird gather twigs and hair for a new nest
Disorientating a ranger by replacing tracks with his own
Humming audibly as they flit about from fern to fern
Distracting a dwarf by glamouring copper as gold
Imprisoning a villainous, bat-winged sprite after holding a trial
Embarrassing an elf by replacing their arrows with roses
Investigating an abandoned chest, but unable to pick the lock
Evaporating explorer's waterskin - replacing liquid with gold dust
Jesting with a nervous bard, who is swiftly running out of jokes
Flustering a fighter by gluing every blade into its scabbard
Keeping tabs on a child, blessed as an infant with second sight
Frustrating an ogre by instantaneously spoiling his supper
Kidnapping a bride from an involuntary wedding
Goosing a grave digger during a solemn occasion
Laughing uproariously at a donkey headed human
Hiding a hunter's hat inside a big block of un-melting ice
Liberating a grateful blink dog from a trapper's snare
Instantly swapping outfits of everyone in an adventuring party
Making faces in a silvered hand mirror - their prized possession
Leading a lizard man astray by granting him "prophetic" dreams
Meddling with a necromancer by turning bones to shortbread
Misleading a hobgoblin squadron by changing road signs
Mocking a minotaur with a dainty tea party, porcelain and all
Muddling a medium by replacing spellbook with racy literature
Nesting in a magical helmet, very protective of their home
Perplexing a priest, swapping a holy relic with a chicken bone
Nudging a nomad to steal back a stolen magical ring
Replacing a rake's blade with a droopy cattail when drawn
Objecting to the presence of a nearby vampire, seeking assistance
Scolding a scholar by removing their ability to read
Occupying an unfinished golem, able to make it walk and speak
Spontaneously inebriating an entire band of brigands
Pantomiming a perfect rendition of a famous assassination
Spraying a squire with very powerful giant ferret pheromones
Perching on the end of an enthralled knight's lance
Stealing a gnome's voice and substituting croaks of a frog/toad
Presiding over a wedding between a dryad and her thrall
Transforming a troll into a sprite a day and a night
Protecting an ancient and somewhat senile treant from termites
Tricking a greedy goblin - a pile of gold turns to acorns in an hour
Quietly fluttering along the flower tops, drinking their fragrance
Tripping a trader whenever they draw a weapon
Repairing a milkmaid's leaky bucket as trade for thimbles of milk
Unfastening all of a well-armed warriors belts and straps at once
Reveling alongside centaurs, satyrs, and a few very confused farmers
Weighing down a wizard, by making pack as heavy as an anvil
Riding colorful beetles, and girded for all-out war
Adding beautiful blossoms to barrel-sized bowers
Scheming to topple an evil sorcerer's tower
Advising a chipmunk of the best hiding places for her hoard
Scrutinizing a stoppered vial, daring each other to drink
Banqueting with a humble beggar, who can't believe his luck
Shimmering with highly sought-after magical dust
Beheading thistles with miniature swords
Singing ancient ballads alongside the birdsong
Buzzing about on translucent, dragonfly like wings
Stringing garlands from branches of a bush to celebrate its seed day
Celebrating raucously with song/dance for no discernable reason
Struggling to free a fellow from a sticky spider's web
Chasing each other, some dressed as mice others as cats
Stumping a barrelheart treant with a nonsensical riddle
Cheering up a depressed dryad with foolish pratfalls
Swinging from verdant vines and springing stems
Crowning an awakened snail as their new and rightful king
Tangling the net of a fisherman as a favor to nearby nixies
Dancing an incredibly contagious jig - tarantella like and exhausting
Teaching all the animals of the wood a few words of common
Darting to-and-fro, just out of reach of an alchemist's butterfly net
Teasing their surprisingly tender hill giant mascot, playfully
Dazzling a druid with their knowledge of magical herbs & plants
Terrifying travelers with a carefully orchestrated "ghost gag"
Drinking honeysuckle wine by the thimble - can knock a dwarf flat
Thronging around a fragrant flower that blooms only once an eon
Encouraging a ring-shaped growth of toadstools
Tinkering with an abandoned crossbow, turning it into a ride of sorts
Expecting a visit, any moment now, from seelie royalty
Underestimating the properties of a magic wand they found
Fashioning intricate garments from petals and gossamer
Utterly despondent from a child's disbelief
Fencing with needles/button bucklers, stolen from a seamstress
Vanishing within their stronghold of sleep-inducing thorny briars
Fettering a wicked witch hunter, unbreakable chains of flowers
Vexing attempts to leave a clearing - you end up walking right back in
Frightening a band of orcs by making spooky, ill-portentous sounds
Waltzing to the strident stridulating of a cricket
Frolicking among the magical fruit of an enchanted pear tree
Yammering on about nearby buried treasure (actually an old boot)

Table: squid, giant
Affixing a string of watermelon-sized eggs to the hull
Nibbling inquisitively on a bit of floating flotsam
Ambushing a pod of squealing dolphins
Obscuring sharkfolk allies with its ink cloud
Attacking the crew of a crippled carrack
Overturning a trireme, laden with treasure
Avoiding a roiling vortex on the surface of the sea
Plucking panicked pirates from the foredecks
Basking in the warm water of shallower seas
Preying on delicious dragon turtle eggs
Biolumenescing balefully beneath the waterline
Protecting a jewel-like lagoon of saltwater nixies
Breaking anchor chains/moorings to set ships adrift
Proudly bearing scars and barbed hooks all along his mantle
Capturing a barn-sized crab scuttling across the seabed
Quavering with anticipation at the sound of a ship's bell
Chasing away a shoal of shimmering daggerfish
Quitting a confrontation with a tenacious sea dragon
Clacking their beak loudly to ward off a rival
Ramming the broadside of a barque
Clamping tree-trunk like tentacles around a lighthouse
Recoiling from a sudden lightning strike from the heavens
Clouding the water for leagues with their midnight ink
Releasing its grasp on a soft-spoken sea druid
Colliding suddenly with the port side of a schooner
Rending a ship's ropes with dagger-like denticles
Completely capsizing a cutter crewed by traders
Retreating after disturbing a giant stonefish
Constricting the hobgoblin captain of the ship no quarter
Ripping a rudder to becalm a clipper
Crumbling a coral castle in search of tasty mermen
Roiling furiously, generating deck-high waves
Crushing a lifeboat callously as shipwrecked sailors scream
Running amok after the death of a mate
Deftly changing color to blend with wine dark waves
Shattering an elf galleass made of thick green glass
Deliberately dredging the sea floor to build a sandbar
Shredding sails with sharp, spiny suckers
Devouring a drowned malletnose whale
Sinking a prisoner transport, all hands screaming for help
Discharging an ink that reacts with air - creating thick blue fog
Slamming their bulk against a summoned icy wall
Disentangling itself from a sturdy steel net
Slowly flickering their gills, feigning sleep
Drenching a dinghy with its wake as it thankfully swims past
Smashing through portholes to probe for prey
Drowning the crew of a caravel, one at a time, sadistically
Snacking on succulent saltwater termites
Dwelling in the deepest reaches, only surfacing on new moons
Snapping tall masts like twigs
Encircling a pair of vessels as pirates prepare to board
Snipping a giant sea snake in two with its powerful beak
Engulfing a galley, wrenching oars from rowers hands
Splintering bobbing barrels of hard tack
Entwining a scuttled sloop, probing for prey huddled beneath decks
Spraying its ink onto a pristine, white sandy beach
Fastidiously dissecting their dinner - a smaller sea serpent
Spreading terror aboard a troop
Fatally grabbing an experienced weather wizard
Squirming to try and snatch some tricky blink dolphins
Flashing crimson chromatophores, bright on pale pink background
Stargazing with unnervingly unblinking eyes
Floating on the surface with a massive ivory harpoon protruding
Starving a small fishing village by destroying it's nets and boats
Fracturing an ogre sailors bones with a single squeeze
Studying the arcane markings on a submerged basalt obelisk closely
Glaring with sinister, otherworldly intelligence in their eyes
Submerging suddenly, pulled downward by an army of mermen
Gliding swiftly through stormy seas
Surrounding a shipwreck, as it broods on the sea bottom
Grappling with an angry storm giant
Swallowing a bull shark whole
Grinding their beak, back and forth, a cacophonous, grating sound
Swamping a seaside cemetery and shrine
Haunting a sargasso sea, waiting for easy prey
Swiftly enveloping a gnashing great white shark
Hemming in a shoal of greatfin tuna with flailing arms
Swimming in slow circles, trying to pick up a scent
Heralding the arrival of a kraken before the week is out
Tearing open a sunken strongbox to add shiny contents to her hoard
Hunting their favorite prey - other similarly sized squid
Thrashing as it battles a wraith whale
Injuring itself slightly on a massive reef of vampiric coral
Toppling the sole sail of a berserker bearing longship
Inundating the decks of a beautifully decorated dhow
Tugging a clinker-built cog of sea clerics toward shallower water
Investigating an offering left by an apocalypse-hastening cult
Undulating in the undercurrent, digesting a dire dugong
Jetting strong blasts of water to stun a soaring roc
Unfurling its arms and attacking two ships at once
Keelhauling an unfortunate swab before swallowing him whole
Upsetting established maritime trade-routes with its presence
Leaping through the air, propelling themselves with powerful jets
Watching a transfer of a ransomed prince from below
Looping their tentacles around the hull of a ghost ship
Wrecking a warship against jagged rocks
Luring deep-sea whales to the surface with false distress calls
Wrenching the ship's wheel from a captain's hands
Migrating to warmer waters to breed
Writhing in mortal combat with a giant saltwater crocodile

Table: stegosaurus
Attacking a gingko shrub with ferocious glee
Laying a clutch of infertile eggs as a decoy
Avoiding deep and hungry mud near a stagnant pool
Licking flaky mineral deposits from a wide furrow
Basking in a warm breeze, stretching like a cat
Lumbering through palisades defending a hobgoblin camp
Battering a tree to shower down fleshy green seeds
Lunging in a pointless attempt to silence a shrieker
Being groomed by parasite-peeling, bird-like theropods
Mauling a medium whose charm spell failed
Bellowing with a deep, resounding grunt every few minutes
Menacing a halfling hamlet, feasting on farmland by night
Besieging a treant grove with frequent visits to graze
Milling flour with an ingenious dino-powered wheel
Blindsiding a congress of whooping rock baboons
Munching on pine needles, proffered from a ranger's hand
Blushing their plates bright orange to discourage predators
Nudging their young to enter a slow-moving stream
Braying melodiously to try to attract a mate
Nuzzling their bone plated neck over a warm rock
Breaking open firm-skinned, spikey fruits to slurp the insides
Oozing blood from a fresh spear wound on her flank
Bristling with spines and plates in response to a sudden sound
Overrunning an overconfident ogre
Browsing fuzzy mosses, carpeting the rocky ground
Partially submerged and covered in lily pads
Building up the courage to cross a narrow bridge
Pawing at their mate, dead from poisoned blowgun darts
Champing the caps from tall, finger-like mushrooms
Peeling strips of tender bark from the bases of every trunk
Charging a worried looking ceratosaurus
Plodding with determination near a series of noisy geysers
Chewing a mouthful of flopping horsetails
Protecting a friendly dryad's grove
Chirping soothingly to calm an excited calf
Pulling down trees at the goading of their gnome keepers
Circling defensively around a clutch of tapered oval eggs
Reaching on hind legs and tripod-tail toward fuzzy leaves
Coating their sides with thick mud to drive away stirges
Refusing to back down from stone-throwing troglodytes
Combing through fallen leaves for tender, fresh shoots
Responding to a distant call with a resounding low
Congregating around a strange monolith, pulsating with heat
Ridden by strange elfs in bone and horn armor
Crashing through woody undergrowth, making a huge racket
Roaring mournfully after discovering their nest raided
Crossing a rocky ravine, sliding on the scree
Rumbling through bamboo-like thickets
Crunching barbed, seed-filled cones in their bird like beaks
Ruminating, constantly chewing tough rubbery leaves
Crushing scattered elf bones with careless steps
Rummaging at the roots of a tree for strange truffles
Defending a wounded mate from ravenous theropods
Scouring their shedding sides against a massive boulder
Denting a dwarf's shield with a powerful tail swipe
Shaking a tall tree as tiny arboreal mammals screech and chatter
Digging a crater like hollow, preparing to lay
Sinking into a pool of water to quickly cool off
Dragging a crude sledge, hut poles for a lizard man village
Slogging through dense vines and vegetation
Drinking warily from a quick-flowing creek
Squaring off with a triceratops over nesting territory
Eating conifer saplings, pulling needles off with a long tongue
Squawking a loud warning to an inquisitive egg stealer
Emerging from a marshy bayou, shaking themselves dry
Stomping on hard-shelled seeds to access the meats within
Feasting on fabulous fern fronds, taller than a man
Stripping spines from a strange succulent before biting into it
Flailing their tail at a terrifying tyrannosaur
Stumbling a bit after eating quite a bit of fermented fruit
Flashing brightly colored waddles in a threat display
Swaying their tail to signal danger to herd members
Flattening low bushes with their massive bulk
Teaching their young how to sniff out tasty tubers
Fleeing, with surprising speed, from a nearby landslide
Thagomizing a sabre toothed tiger
Flexing muscles in their back, plates undulating rhythmically
Thermoregulating by creeping into dappled shade
Floundering in thick green algae after losing their footing
Thundering at a full clip across a barren field
Foraging among plump cycads near camping neanderthals
Trampling the trapper who snared her cub
Gingerly snipping only the most tender shoots from a shrub
Traversing a hardened magma flow, searching for food
Grazing on stringy tree moss, having to rear up to reach it
Trudging along stony lake banks, stopping to sniff the air
Grunting with satisfaction as they drive away a kobolds
Trumpeting an almost bugle like call
Herding four curious hatchlings out of their nest
Uprooting a yew sapling to nibble on nutritious roots
Holding their spike lined tail high in the air above them
Wading into a lake to have scales cleaned by tiny fish
Inhabiting and defending a fungi-rich cavern
Wallowing in a dry dust pit
Joyously scratching each other's sides with beak nibbles
Warding off a swooping wyvern with a flick of its tail
Knocking over an allosaurus with a powerful tail-swipe
Wheeling around to reposition in a clash with an allosaurus
Lashing their thagomizer about violently at a white ape
Wounding an orc war band, who unwisely woke him up

Table: stirge
Alighting on a cast iron lantern hooks, high above
Jockeying for prime position on a desperately braying mule
Annoying a gargoyle, unable to pierce her stony hide
Keening from the inky darkness above, diving down periodically
Avoiding a startling smell - an approaching gelatinous cube
Keeping their newly hatched young warm in their pouches
Beating their wings dry of damp and dew
Landing on a brackish basin, drinking watchfully with long tongues
Billowing forth from a fissure in the stone
Launching from their perch at an unlucky ranger
Blundering into a hanging, bloodstained cloth with dull thuds
Lazily gliding on warm currents from steamy thermal vents
Brooding within their scab-like spittle nests
Living in a strange symbiosis with giant ghoul rats
Buzzing with ever increasing intensity during a mating flight
Menacing a medium as she waves a torch recklessly
Circling the withered corpse of a cleric
Mobbing a merchant, bodyguards bruise as they club them off
Clicking with loud stridulating sounds to claim territory
Monotonously droning with their rapidly flapping wings
Clinging to a crudely wrought iron chandelier
Nesting inside a mummified giant bat, suspended from the ceiling
Clustering on a squealing giant rat
Noisily squealing as some of them sizzle from green slime
Congregating above a pool, occasionally spearfishing for frogs
Occupying the skull of some sort of very large lizard
Cowering from a gnome testing her last dose of stirge repellant
Overtaking an outlander, smeared with blood as a rite of passage
Crawling clumsily across the floor, too swollen with cruor to fly
Perching on the upraised arms of a dryad statue
Dangling precariously from the sides of a skinny stalactite
Piercing the carcass of a deer, hanging from a hook
Darting from perch to perch to avoid a frustrated giant spider
Plaguing a platoon of hobgoblins, marching on patrol
Depositing row upon slimy row of translucent carmine eggs
Pulsating as they digest spicy dragon blood
Detaching from a dead doppelgänger, grey skin and rubbery bone
Puncturing through a canvas sack, suspended from the ceiling
Divebombing a shouting dwarf, wildly swinging his hammer
Pursuing a fleet-footed pickpocket down darkened corridors
Draining a desperate plague doctor dry
Quavering in contented warbling chirps
Drinking small straw-like sips from an unattended glass of wine
Ranging far and wide to nearby farms for their nightly sorties
Dropping down suddenly from a doorway onto the back of a bandit
Rapidly diving to avoid a snatching snake
Drying their hematic dens by fanning their wings
Ravenously swarming a group of halfling mushroom hunters
Dwelling inside a big bronze bell, still suspended on a rotting beam
Rolling around in a pile of ashes to eliminate lice
Emerging from the helm of a hollow suit of ceremonial armor
Roosting in a uniform line, all along an arched roof
Engorging on a hibernating owlbear, flightless due to bloat
Seeking the shadows after a sudden burst of magical light
Establishing a splinter colony due to overpopulation
Settling into their nests after a big meal, distended bellies drooping
Exsanguinating an explorer, as his porters scramble and flee
Shunning the acrid smoke of a special wood, burnt by neanderthals
Extracting precious little blood from a dead rat
Skimming gore off a bloody discarded axe head
Fattening for breeding season, much more aggressive than normal
Squeaking as they flock around a fighter in recently rusted chain
Feeding young by regurgitating gory mixtures
Squeezing through tiny cracks after sensing warm breath
Fencing with pointy proboscises - fighting over the right to mate
Starving, stuck in a room with several bloodless skeletons
Flanking an archway, ready to swoop on any passersby
Streaming towards an entranced lizard man shaman
Flapping furiously within a sticky mass of web
Suddenly swooping, startling a relic smuggler
Flourishing from regular sacrifices made by a creepy blood cult
Swinging playfully on a series of suspended chains, a rattling racket
Fluttering down from a chimney flue, blackened with soot
Thirsting for the blood of a noble, sleeping in a glass coffin
Flying clumsily, drunk after feeding on an intoxicated ogre
Thriving due to plentiful play - almost the size of ravens
Following the sweet scent of a bleeding elf
Transmitting weak vampirism - sunlight sensitivity/garlic allergy
Gingerly sipping from a crimson, quickly curdling puddle
Troubling a cyclops shepherd by sucking her sheep dry
Gorging on a gibbeted gnoll
Unfurling wings as they burst forth from viscous maroon cocoons
Gripping fast with tenacious legs to a screaming goblin
Upsetting the underling of an evil mage, insists on breeding them
Hanging densely along the bottom of a shelf, preening
Utterly besieging a bugbear, can't pick them off fast enough
Hovering in place, waiting for a carcass crawler to paralyze prey
Veering sharply around a corner after a whiff of fresh blood on the air
Humming in unison as a distant shrieker howls
Weaving among a throng of bats
Hunting down a wounded horse
Whistling as they shoot toward an under-armored orc
Immaculately constructing their scarlet nests of solidified spit
Whizzing around the head of an oblivious brass golem
Impaling proboscises into a taxidermized stag head, frustrated
Wriggling below a motheaten blanket atop a straw mattress
Infecting those they drink from with bloodborne pathogens
Yexing softly after drinking their fill from a friar
Jabbing through the eye-slit of a plate armored paladin's helm
Zooming away from a recently risen/utterly famished vampire

Table: thoul
Absolutely immobilizing a gnome warrior with their touch
Neglecting crucial watch duties, gambling on rat fights
Acculturating to damp air after leaving the viscous gene vats
Numbing a noble as treaty negotiations break down
Afflicting a subordinate with paralysis for speaking out of turn
Ordering an ogre mercenary to smash through a door
Assimilating into their role as shock trooper in a war band
Overseeing trench diggers, armed with a cat-o-nine-tails
Bargaining with somewhat friendly ghouls for safe passage
Overthrowing a king after discovering their doppelgänger nature
Beaching a small boat on the banks of a still river
Painting the faces of their troops with sanctified pigments
Besieging a clan of bugbears until they pay tribute to their king
Paralyzing prisoners to make them easier to transport
Blending in with a band of hobgoblin bounty hunters
Patrolling a hobgoblin held toll road after recent collection troubles
Breaking a twisted arm with a sickening crunch to reset the bone
Piercing their hands with quick-healing hook wounds
Bristling with manticore quills, poking from face as trophies
Playing dead amid a battlefield, hoping to ambush the unwise
Bullying the "regulars" they've found themselves stationed among
Plundering a chapel of sacred objects and relics
Celebrating a holy day by burning offerings of meat
Polishing the points of spears and big blades to a regimental shine
Challenging a hobgoblin to a duel over a perceived slight
Pressuring their fellow bodyguards to accept a bribe, as a loyalty test
Charging a hellhound with reckless abandon, play fighting with it
Protecting a superstitious charm, they claim gives them their powers
Claiming first choice of spoils from a successful raid
Pulling rank by cutting to the front of a line ladling out stew
Clubbing a rust monster with a gnarled cudgel
Quelling an argument between peers by cracking knuckles loudly
Commanding a goblin peon to fetch his helmet
Rallying their underlings with threats of grievous bodily harm
Confiscating a clinking coin purse from one of his cadets
Rapidly re-growing fingers severed by a blade trap
Congratulating themselves after repelling dwarf invaders
Receiving a shipment of weapons, inspecting them for quality
Conquering another at a complex board game with lead figurines
Regenerating with a slurp, crossbow bolt pushed out of shoulder
Countermanding the orders of their captain to save a friend
Reigning over their tribe after poisoning an inferior king
Defending a strategic chokepoint, watchful and wary
Reinforcing the ranks by defending archers - unafraid of friendly fire
Demanding more rations than his hobgoblin companions
Returning from a raid, driving an entire flock of stolen sheep
Desecrating a shrine in the name of the mother of battle
Revered by his tribe as an avatar of pain
Dressing down a solider for a scuffed boot
Reviving a paralyzed comrade with the back of a gauntleted hand
Drilling subalterns in proper pike formation
Roving in search of sustenance for their ravenous appetite
Drinking to excess after commandeering a wine merchant's goods
Rushing a rhagodessa, confident their healing abilities will save them
Encouraging a hellhound puppy to toast a giant rat
Scattering the ashes of fallen comrades at the site of an historic battle
Excavating an ancestral tomb, seeking explanation for their origins
Scourging themselves as penance for letting a halfling get away
Extinguishing a blazing bonfire with buckets of sand
Seasoning their blood-colored soup with pixie wings
Flinging flaming oil on an already irate troll
Seeking a desecrated spring, said to impart more powers to thouls
Foregoing a leech's ministrations after tangling with a troglodyte
Skulking after an exiled fire giant assumed leadership
Grabbing roasting fish directly off the coals of a fire
Snarling with frustration at an elf - won't succumb to her touch
Guarding a shipment of exotic spices/silks, destined for their king
Sounding an alarm after being struck by a shadow
Hijacking a horse trader's stock to outfit a new calvary
Sowing dissent among the lower ranks, eyeing a better position
Hovering at the shoulder of the medium that hired them
Spying for a nearby medusa, promised a cure for her condition
Hunting down a would-be assassin in their ranks
Stitching a still-twitching arm back onto his shoulder with twine
Incapacitating a paladin, then moving on to her squire
Stunning a gnoll knife-flinger mid-throw
Influencing their king's policy decisions out of a hatred for elfs
Surprising a sage with the banal origin myth of his people
Initiating a new pack member with temporary scarification
Surrounding a blink dog den, hoping to smoke them out
Inspiring their companions by single-handedly slaying an orc
Threatening to eat a goblin lackey for walking too slow
Jesting to improve morale - freezing their kobold porter
Toting a sack containing the teeth of worthy foes
Joining a motley band of bandits, still a little suspicious of her
Travelling on a diplomatic mission - an alliance based on marriage
Knitting a wound closed in seconds by sheer willpower
Unsheathing a dagger, concealed inside his thigh
Leading some cautious levied conscripts to certain defeat
Usurping command of a flagging squadron by paralyzing the captain
Lumbering slightly, betraying trollish heritage in their gait
Utterly starving after a week-long ceremonial fast
Lurking comfortably within an iron maiden
Vexing an axe wielding veteran with their rapid regeneration
Making invasion plans to occupy a local hamlet
Visiting a tribe to discuss a potential merging of forces
Marrying their bizarre blood & black beer as a weak healing potion
Welcoming a group of evil dwarfs into their camp
Menacing travelers on a well-known route
Wrestling with their mentor, and elder ghoul

Table: titanothere
Ambling nonchalantly as small ground rodents scurry away
Meandering, single file, up a steep slope
Attacking the tender leaves of scraggly sun bushes
Munching on verdant pond plants, dangling from mouths
Avoiding a riverbank, lined with sunbathing crocodiles
Nosing a dying member of the herd, succumbed to disease
Bearing unusually large y-shaped horns and bony frills
Nudging foals into the center of a defensive circle
Belching loudly in sequence, echoing throughout the air
Nursing their young, only a few days old and already pony-sized
Bellowing to call together the herd after exhausting pastures
Nuzzling each other to keep warm in a frigid breeze
Bogging down in marshy grasses, flanks muddy and wet
Obstinately refusing to pull an ogre's wagon
Bounding with surprising speed away from a wyvern
Ornamented with painted patterns of swirling shapes
Breaking an abandoned hut by leaning against it to scratch
Pawing the earth, preparing to charge a group of berserkers
Browsing among juicy succulents for a favorite treat
Peering suspiciously at a traipsing sabre tooth tiger
Bumping noses with each other as a friendly familial greeting
Plodding along a dry creek bed, digging for water
Calving as an ornery male stands watchful guard
Poking only their massive horns above astonishingly tall grasses
Chewing constantly, even in their sleep
Possessing knobby protrusions all over their faces
Circling around a minotaur shaman reverently
Producing a highly vicious, yellow milk prized by nomads
Clashing ferociously - two males shove for horns for dominance
Pulverizing skeletons streaming out of a disturbed barrow
Communicating with high pitched whistles/occasional nickers
Quasi-domesticated by enterprising halflings - meat is lovely
Consuming a frantic farmer's entire lettuce crop
Rampaging after ingesting a fury-inducing fern
Cropping off the budding tops of plants with dexterous mouths
Rearing on their hind legs to push down a leafy tree
Drinking deeply from a mineral rich spring
Reclining on patches of soft grass, anticipating rains
Driven by hobgoblin calvary into massive corrals
Resonating loudly through their hollow horn-like noses
Drooling prodigiously after grazing on bitter herbs
Roaming far too close for comfort for a nearby fishing village
Dwarfing the graceful antelope that graze nearby for safety
Rutting season - extremely agitated and ferocious
Eating fallen fruit noisily and with great gusto
Saddled with yokes to plow cyclops fields
Enraged by hyaenodons trying to pick off a weaker herd mate
Sauntering over to a group of bored-looking females
Excitedly snuffling at a delicious mass of mushrooms
Scrambling down a muddy bank to cross a river filled with crocs
Fattening up on highly nutritious, knobby ground nuts
Shoveling deep furrows in the soil with their spade like horns
Favoring a foreleg after a vicious dire wolf attack
Shredding bark from massive tree trunks with their prongs
Ferociously clubbing a gnoll hunter with a head-swipe
Slaughtering a griffon who mis-timed their swoop
Fighting and sparring young, watched casually by adults
Snorting plumes of thick steam from nostrils in cold air
Freezing in place after a distant roc screech
Stampeding away from a coordinated hobgoblin hunting party
Galloping together, kicking up a massive cloud of dry dust
Standing with a blustery wind at their backs
Gathering around an idyllic watering hole to rest
Staring at a humongous rock python, slithering nearby
Goring a shrieking terror bird, tried to make off with a foal
Stinking of earthy manure, creating a feast for flies of all sizes
Grazing peacefully among a field of enormous bones
Straggling behind, unaware of a hungry pack of wolves
Grinding tough twigs down to paste with massive molars
Swishing fat tasseled tails to drive off insects
Headbutting each other, jockeying for pecking order
Tamed by dwarfs as living siege weaponry
Herding around a strange shrub that never seems to lose leaves
Thrashing with their hind leg trapped in a sinkhole
Haplessly lost from their herd, braying mournfully
Throwing back their heads to snort and whinny
Inhabiting a fertile valley, studded with brilliant violet geodes
Tied with massive ropes, being used to topple a tower
Injuring a band of neanderthal hunters, desperate for food
Tolerating a small troop of white apes foraging nearby
Intriguingly adorned with a horn resembling a holy symbol
Tossing a lion with a quick flick of their horn
Jostling each other to be hand-fed by a hill giant druid
Trampling an intricate magic circle, obliterating key runes
Kicking up massive flecks of mud as they excavate roots
Trotting up to a ranger, hoping to hear news of a lost foal
Launching an orc into the air with a scoop of their horn
Trudging through thorny brambles, hard hide immune
Licking magical moss that imparts telepathy to them
Unsuccessfully dodging atlatl fire from a troop of lizard men
Loitering around a trampled gorgon - alpha male petrified
Vigorously defending themselves from a hungry tyrannosaurus
Lowing with a deep rumble that echoes for miles
Walking along the edge of an ancient, crumbling wall
Lumbering through the aftermath of a recent forest fire
Wallowing happily in bubbling hot mud
Lunging at a giant tuatara that was wandering too close
Wandering through a crucial pass, clotting and clogging it
Marring the mud with their massive tracks
Yielding prime pasture, after sensing rumblings of purple worm

Table: toad, giant
Ambushing its dinner, a disarmed dwarf
Marinating in a toxic mix of its own making, don't drink the water
Avoiding juvenile ogres, gigging for delicious legs
Moistening leathery skin with a dribbling trickle from above
Awkwardly scuttling away from some skeletons
Nabbing a nixie, screaming for help
Ballooning its prodigious throat pouch to incredible size
Noisily groping around leaf-litter to make a mulchy bed
Befouling a well's water source with hallucinogenic secretions
Overwhelming troglodyte stench reveals a recent run-in
Bleeding from a giant rat bite - its most recent meal
Paddling lazily among gigantic lily pads
Bloated and heavy with frogspawn, searching for a suitable pond
Pained grimaces/muffled yells - halfling had for lunch is poking
Bolting down a twitching driver ant
Plodding along, oblivious to lizard man hunters
Bounding out of the darkness after being stung by a centipede
Prized by shamans/assassins alike for their mind-altering toxins
Catapulting its tongue toward the ceiling at roosting giant bats
Puffing his pouch in vain to impress a female, recently petrified
Cautiously eying a slowly climbing mass of ochre jelly
Pulsating his pouch, a proud papa transporting tadpoles on back
Centuries underground have given this species pale white skin
Reeling in a rust monster, excellent for digesting stubborn swords
Challenging a distant rival male with a startling shift in volume
Resounding ribbits are used by rangers to find fresh water
Choking down a mouth-numbing meal of carcass crawler
Roused from brumation and ravenously hungry
Clambering over dry terrain, bulging eyes on the lookout for danger
Scarfing down a giant leech, an overall disgusting sight
Clumsily creeping across a shallow, stagnant puddle
Scooting across a slippery floor, tracking a giant slug
Consuming tattered pieces of its own shed skin
Scrambling away from a large crocodile
Crawling to safety in a huge clay drainage pipe
Seizing an unsuspecting thief who stopped to check for traps
Croaking suddenly, startling spiders into the corners of their webs
Serenading rapt cultists who feed him in exchange for licks
Devouring a dire dragonfly in crunchy, toothless chomps
Sickened by a recent meal - a medium laden with magic potions
Distending its jaw as it struggles to swallow an unconscious ogre
Skulking in the shadows, driven away by a stronger male
Dragging an extra pair of vestigial legs
Slowly expanding its throat before letting out a loud shriek
Drooping from the chilly air, begrudgingly burrowing in cold mud
Slurping its latest snack like spaghetti - a giant centipede
Drowning out all other sounds with full-throated grunting
Springing upon an acolyte who chose a bad spot to stop and pray
Eating an elf that wandered too close to its bubbling spring
Squeals reveal a battle with pitchfork wielding kobolds
Echoing the crepuscular calls of his smaller brethren
Startling a gear laden mule who stopped for a drink
Enlarging its vocal sac to amplify eerie calls
Stretching languidly on a mossy perch
Enlivened by a tasty robber fly
Stuffing itself with a still-twitching cave locust
Filling ears with an incessant, throaty chirping
Submerged partially in a soupy magic pool that grants telepathy
Fishing about its everted stomach to eject a suit of chain mail
Suddenly shooting a sticky tongue, snaring a bleating goat
Flinging a fleshy tongue at a shifting shadow on the wall
Suffering from the sharp short sword lodged in its gullet
Foundering as it struggles to evade the gaping gullet of a giant bass
Swallowing a cache of giant lizard eggs
Frantically bathing after coming into contact with itchy spores
Swatting away swarming hand-sized ants
Gamboling steadily to its favorite spot beneath a towering toadstool
Swelling to bursting, shouldn't have swallowed doppelgänger
Gathering around their positively massive king - ten times the size
Swimming with surprising grace in vibrant green duckweed
Getting the drop on a crunchy wolf-sized crayfish
Throaty singing has attracted a hungry troll
Grabbing a water-skin filling goblin with a sudden lunge
Tripping a fleeing veteran with a well-placed tongue strike
Groaning in satisfaction as it digests a giant spider
Trudging after a dangling grub-on-a-stick, held by a pixie rider
Gulping down a python-sized earthworm
Trying to get your attention - a polymorphed storm giant prince
Gumming a glowing fire beetle with toothless bites
Unevenly crooning in an attempt to locate a mate
Hurling itself at a door after becoming inadvertently trapped here
Vaulting out of a giant catfish's reach
Inching into tongue range after spying a killer bee
Voraciously englutting on a rival's plump tadpoles
Insatiably gobbling water termites in an inky mess
Warbling steadily atop a giant skull
Jostling for prime position on a slick, mossy boulder
Warty backs spray blinding spurts when struck
Launching its tongue at a tiger beetle
Water-proof giant toad leather makes excellent spellbook covers
Laying pomegranate-sized eggs in gelatinous strips
Wheezing after gobbling up a yellow mould infested zombie
Leaping to avoid becoming a meal to a giant snake
Wolfing down delicious oil beetle larvae
Licking milky, orb-like eyes clean
Wriggling out of a giant black widow's webs
Lightning-fast tongue flick stuns a sprite
Writhing in a noisy mating ball
Loping along the banks of a personal pool, patrolling for intruders
Yawning wide enough to reveal a glitter of gold

Table: human, trader
Acquiring deer hides from an unreliable ogre
Jumping on a medusa's offer to sell him sculpture
Announcing his wares - mostly fish and fishing gear
Known by magic users for their fine selection of exotic inks
Anticipating a run on exquisitely crafted gloves, overstocked
Learning the hard way that fire giants cannot be trusted
Appraising shattered chunks of an amber golem
Leaving money on the table with low prices on pewter
Aspiring to join a respectable merchant company
Loading tightly bound bundles of torches onto a rickety cart
Assuring an orc customer that bolts of wool are genuine
Losing most of their stock of sweets to some mischievous sprites
Avoiding the bandits that are rumored to plague this region
Meticulously counting coins, feeling shortchanged
Bankrupting a local weaver by undercutting their prices
Monopolizing the market on magical mead
Bartering with berserkers over tin - losing their tempers
Nervous after hearing a hair-raising owl bear hoot
Beating dust from several fusty furs and hole-ridden hides
Nodding to communicate with curious neanderthals
Bickering with their porter over the best way to load the mule
Now buying bones, all sizes, shapes, and types
Borrowing a sleeping buccaneer's blade
Obtaining pearls for a pittance from besotted nixies
Bustling to unload a variety of well-travelled wares
Offending an orc chieftain by overcharging for ore
Calculating rate of exchange on a strange beaded frame
Ordering around her goblin flunkies
Carrying a trunk of intricately carved ivory scrimshaw
Paying extremely outrageous prices for monster pelts
Cheating a farmer, trying to unload a cursed shovel
Peddling "priceless" holy relics, one is actually genuine
Checking that his horse's harness is firmly clasped
Playing flickering fetch with their blink guard dog
Claiming to have teas from exotic, far-off lands
Pleading with a hill giant to spare their life
Closing a deal with some dervishes over woven goods
Plodding noisily along, pots and pans clanging loudly
Collecting payment from some stingy dwarfs
Preferring to deal strictly in electrum for esoteric reasons
Complaining about being unable to obtain shrieker gills
Preparing a massive, mouth-watering meal in true halfling style
Cooking a large pot of rather flavorless gruel - cp a bowl
Promising full refunds if their magic incense fails to function
Dealing in all manner of arrows and crossbow bolts
Protesting a troll's exorbitant bridge tolls
Delivering arms to a clandestine hobgoblin contact
Purchasing a blood-stained suit of plate from a wounded medium
Demanding full payment from a penniless peasant
Quarrelling with their ranger guide over the safest route
Displaying their wares, laid out on ornate and intriguing rugs
Receiving word of a gold strike, hurrying to profit from miners
Drinking some of the cyclops wine they received as payment
Recoiling from the stench of attacking troglodytes
Earning a modest fee for carrying a noble's correspondence
Reconsidering a devil swine's offer to buy all their stock for cp
Employing extremely capable bugbear bodyguards
Refilling empty holy water vials in a babbling brook
Evaluating some elf glassware, unable to find flaws
Refusing a desperate pilgrim's request for aid
Exchanging coins for phony promissory notes
Replenishing garlic after visiting a village plagued by vampires
Expecting a high demand for their exceptional coffee beans
Riskily crossing a rickety rope bridge with a balking mule
Explaining to an apprentice - how best to haggle with gnomes
Scheming to swindle a solider out of her hard-earned pay
Exporting water-tight woven baskets
Seeking assistance retrieving his son from a nearby dungeon
Extolling the virtues of his rare herbs and plants
Selling all wares for ridiculously low prices - retiring with dryad wife
Ferrying fragile alchemical equipment across a raging river
Specializing in treasure maps and cartographic tomes
Freelancing unwisely in guild-held territory
Stocking up on crudely carved wooden lizard man figurines
Gouging a werewolf stricken village on silver weapons
Stopping to remove a stone from their horse's shoe
Grinning as centaurs clean out his supply of iron ingots
Struggling to dig out their stock after an avalanche/cave-in
Hawking patent medicines of questionable efficacy
Supplying cider to rowdy satyrs
Hesitating when asked the price of their favorite donkey
Trading rough gems to discerning dwarfs
Hiring adventurers to escort them to a distant keep
Trailblazing a new trade-route, becoming hopelessly lost
Holding on for dear life to the edge of a gnoll pit trap
Underestimating demand adventurers have for her healing potions
Honing the blade of an heirloom hand axe
Uneasily settling in to rest from their long journey
Horning in on a well-known halfling pipeweed merchant's trade
Visiting a local shrine to tithe
Importing odiferous cheeses that are proving popular
Vying to corner the market on exotic spices
Incurring additional operating costs after losing her last mule
Waiting for the arrival of a bandit contact to fence some stolen goods
Investing all their funds in a charlatan's scheme
Weighing gold dust on a small scale
Inviting all comers to try their gaudy glass jewelry on
Willing to give phenomenal bargains to capable clerics
Joining up with nomads for a trek across barren wastelands
Wishing they had never agreed to work for a dragon

Table: treant
Admonishing a gnome they found searching for syrup
Meandering cautiously away from curling black smoke on the horizon
Afflicted with withering leaf-blight, in search of a cure
Mercifully providing shade to a plague-stricken paladin
Ambling ponderously, patrolling their territory
Monotonously murmuring timeworn adages
Banishing a pesky woodpecker from their branches
Mourning a member of their grove - felled by a violent windstorm
Bashing down the walls of a sawmill
Mumbling snatches of ancient songs, sung when the moon was new
Bearing sought after fruit - eating one de-ages by a year
Naming a new spokes-tree to attend a millennial moot
Befriending a group of peaceful nomads
Nodding sagely in the breeze as a broken-hearted dryad sobs
Bemoaning the loss of a friend after stumbling on their stump
Overtopping most of the forest, a place of pilgrimage for druids
Bickering with an elf arborist about an amputation
Pelting a resting adventuring party with pinecones
Blossoming sublimely for a faerie wedding
Pleading for aid - a rogue fire elemental has entered the wood
Bombarding a band of bugbears with rotting fruit
Pondering the answer to a riddle, furious if interrupted
Budding to form their first new growth in centuries
Protecting a group of reverent neanderthals
Burying armfuls of axe heads in the earth
Proudly bearing saw scars and even a stuck axe or two
Caring for an elder, infested with tenacious termites
Providing instructions to a glowing gathering of wil-o'-wisps
Celebrating an impossibly obscure solar alignment
Pruning back an invasive plant, slowly choking the forest
Chasing after a wolf-slaying woodsman
Pummeling a troll with battering-ram like fists
Choking charcoal burners with claw-like branches
Raining down surprisingly sharp seedpods on a pack of gnolls
Confronting a local peasant collecting deadfall
Raising an orphaned dryad as their daughter - very overprotective
Conserving energy due to spent, infertile soils
Replanting a stand of trees, decimated by greedy loggers
Contemplating a morbid curiosity - a medium's spell book
Repulsing a shipwright, seeking a tall straight mast
Contributing limbs to a carpenter, tasked to build a coffin for a saint
Ripening - heavy, fragrant fruits hanging from their branches
Coppicing a stand to stimulate stronger growth
Rolling massive boulders as a favor for druids
Covered in drooping beards of moss and webs
Rotating slowly to confuse a lost veteran, navigating by moss growth
Cultivating a rare herb, said to cure blindness
Rousing several ancient oaks to help tear down an evil wizard's tower
Debating isolationist policies with a visiting druid
Rustling in stony soil, trying to comfortably plant themselves
Defending a unicorn from vile horn hunters
Sabotaging a dam that would flood their forested valley
Deliberating the fate of lost children they found asleep at their feet
Safeguarding the only remaining seedling of their species
Disfigured and scarred from lightning
Shedding broad, dry leaves in unanimous agreement
Drinking deeply at the foot of a waterfall
Sheltering inquisitive owlbear cubs until their mother returns
Driving away an orc scouting party
Showering a satyr celebration with a profusion of petals
Evicting several sprites from their boughs after a prank taken too far
Sifting through the ashes of a forest fire for precious seeds
Extremely worried - it's giant roc nest building season
Slowly recounting the fable of how dragons stole fire from the sun
Fiercely battering an ogre building a bonfire
Smashing the skull of a downed cyclops
Flourishing due to the numerous corpses buried at their roots
Smothering a campfire by shoveling damp soil over it
Forming a defensive perimeter with animate trees
Sobbing sappy tears after promised pollen didnt arrive on winds
Grafting a sacred sprig to propagate a dying prophet
Soliloquizing to a rapt congregation of squirrels
Growing sharp-thorned trees with thick bark in preparation for war
Spreading an ancient, potent religion, much to the chagrin of clerics
Harboring a host of arboreal animals, each awakened with speech
Sprouting sword-sharp thorns in defense of a wounded werebear
Harvesting rich soil from the graveyard of an ancient church
Startling a pair of young lovers, about to incise their initials
Helping a woodcutter select a suitable tree, per terms of a truce
Stubbornly concealing the entrance to a nixie oracle's grotto
Hesitating as a bandit brandishes a flaming torch
Stumped by an acolyte's philosophical query about their ability to hear
Hurling massive boulders at a hellhound
Swatting skeletal spearmen like mosquitos
Imploring an apple orchard to revolt
Testing a ranger's resolve, unsure if they should trust her
Intoning cumbrous, stilted poetry
Throttling zealots, trying to burn their witch at the stake
Keeping tabs on a burgeoning hamlet, thus far respectful
Traipsing nosily toward a cry for help in gnome
Listening intently to gossipy birdsong for news from afar
Unabashedly blooming out of season
Looking after a local centaur tribe
Uttering words of encouragement, guiding clumsy oaks to new grove
Luxuriating with sun-kissed, outstretched arms
Warding off a family of voracious beavers
Marching old-growth, two-by-two, away from a burgeoning burg
Whispering about underground gold they can taste with their roots
Mauling hobgoblins, felling timber indiscriminately for palisades
Windswept from a few centuries spent contemplating on a cliffside

Table: triceratops
Angering a troop of rock baboons, dwelling nearby
Notoriously nick-named "angry old broken horn" by locals
Attacking a garden plot of tasty turnip tops voraciously
Overwhelming a pack of hellhounds, singed a bit, but safe
Beak low to the ground, sniffing for truffles
Panting after expelling a group of explorers from their valley
Bellowing defiantly under a cruel fire giant's flaming lash
Pausing from a drink to swiftly stomp a snake
Blundering their way into a dwarf mining company's sluice
Pawing tenderly at the sun-bleached skull of an ancestor
Branded with strange, deeply scorched runes on their flanks
Plodding down a steep scree with determination
Browsing the tops of short bushes for the tenderest leaves
Plowing through a platoon of spear-bearing soldiers like grass
Bucking suddenly after being bit by a stirge
Plunging their horns into a screeching wyvern
Bumping nose horns in greeting after months apart
Preferring to not stray far from the lizard men that feed her
Catching up with lizard man handlers after straying to graze
Proclaiming victory with a resounding bray over a dead ogre
Charging with lowered horns at a neanderthal hunting party
Protecting a barrow, where buried within lies a primitive saint
Chasing after a curious calf, straying into a swampy ground
Pumping blood into their frill to make it alter in color and form
Chewing on a beak-full of soft, limp fern fronds
Puncturing wooden barrels, toppled from a cart
Conceding defeat after horn dueling with a rival male
Quietly stripping the bark from a tree
Cornering the dwarf party that attempted to abduct their calf
Ramming into a raft, drifting to close to their bathing
Covered in odd terrestrial barnacles that glow around magic
Rampaging through a village, destroying buildings and fences
Crippling a merchant's cart that looked at him the wrong way
Refusing to emerge from a neanderthal tribe's cave
Crushing clumps of valuable fungi beneath their massive feet
Retracing ancient routes for water, worn down over centuries
Debarking a tree-trunk to hone their horns
Ridden by minotaurs, with whom they have a kinship
Defeating a ravenous pack of feathered dromaeosaurids
Ripping down a halfling's laundry line
Defending their mate from a rutting rival male in musth
Roaming in their old age to a sacred burial place
Dragging a heavy iron fetter behind them on their hind leg
Roaring feebly as they succumb to a pterodactyl harpy's song
Driving away a herd of titanothere from prime pasture
Rumbling stomach from getting into cyclops wine vats
Dwelling near a magical pool that grants articulate speech
Rushing a group of bandits, dividing up treasure in a clearing
Emaciated, with visible ribs showing signs of starvation
Savaging a clump of cycads, hungry after fighting an owl bear
Emblazoned with painted symbols in no known language
Sheltering under a rock overhang in the cool shade
Enjoying a quick wallow in a muddy creek bed
Slamming into a beached boat, while adventurers swim to safety
Fatally goring a young tyrannosaurus
Smelling the distant pheromones of a female
Fighting playfully with a juvenile, teaching them valuable tactics
Sneezing violently after munching on huge puff ball mushrooms
Galloping after a group of fleeing orcs, spear stuck in her side
Snorting as they stomp the ground, seeing their shadow
Garlanded with flowers by pixies, almost looks a bit embarrassed
Squealing and trapped in a pit - a calf with mother arriving soon
Glaring at a crouched sabre toothed cat, turning to face them
Stabbing a leaping dire wolf as the pack circles
Goaded into pulling down hobgoblin palisades by angry elfs
Stewing in a deep wallow, arrows poking from her back
Grazing confidently alongside harmless miniature proto-horses
Straining to reach high boughs of fat, ripe fruit
Grunting loudly as a gnome uses a bristly brush on their hide
Struggling to escape from a weighted and barbed net
Harboring a hatred for anything walking on two-legs
Stumbling a bit, large hydra bite on her hind leg
Harnessed and girded in bronze barding, with iron horn caps
Surging forward through dense underbrush, directly at a tiger
Herding their squealing calves away from the water's edge
Tenderly prodding a hatching egg with their massive snout
Hesitating as a step starts to sink in thick black tar
Thrusting their huge beak into a termite mound snack on larvae
Hungrily bolting down large bales of hay
Thundering across a dusty wasteland, kicking up clouds
Hurling a just-speared bugbear into the air
Toppling a rickety goblin watchtower to frantic screams
Impaling a hill giant-sized white ape
Tossing huge clods of dirt behind them as they dig out a nest
Jousting juveniles, under the watchful gaze of their mother
Towering over the tiny pterodactyls that groom their scales
Keeping their distance from a noisy nest of pteranodons
Trampling a treasure hunter, still clutching his map
Knocking down an entire stand of trees in a rage
Trotting proudly, wearing a brand-new saddle
Lowing to keep tabs on distant herd members
Utterly startling a dervish mid-prayer and unarmed
Lumbering drowsily after destroying a pack of ghouls
Wearing magic rings on both of his menacingly sharp horns
Lunging suddenly and scaring the wits out of a small jackalope
Whipping their huge head around to face a sabre tooth warp beast
Mediating between two high-strung, very young bulls
Wounded after a run in with a wizard, still covered in web
Nosing around barren rocks for traces of plant-life
Wrenching over large boulders in constant frustration

Table: troglodyte
Accompanying their shaman on a holy procession
Lurking amidst several marred/broken statues of adventurers
Adorning themselves with exotic, colorful feathers
Lying in wait for their champion - a huge, ogre sized specimen
Ambushing an unsuspecting ogre
Marking edges of territory with surprisingly detailed scent signs
Barking orders to inexperienced juveniles
Mending nets, barbed with sharp teeth for ensnaring prey
Basking in warm air from a thermal vent
Meticulously repairing a snare, designed to snatch stirges
Blending their scales to match a moss-covered wall
Mixing bright (some bioluminescent) pigments to decorate faces
Blow-darting a dwarf with giant centipede venom
Mottling into fierce, angry shades upon discovering a ghoul
Boiling a soupy concoction with heated stones
Nauseating a cleric, defending a fleeing medium
Brewing refined carcass crawler toxins in cave gourds
Nervously approaching a balefully glowing glyph
Camping after a long march, arguing over watches
Offering a halfling sacrifice to their giant tuatara avatar
Carving intricate/delicate jewelry from cave mollusk shells
Organizing a bloody raid on a surface folk settlement
Chirping high-pitched warning sounds to alert the tribe
Outraging a trapped troll with fiery guano bombs
Creeping along a corridor cautiously, frills erect
Painting detailed tribal histories on cavern walls, breathtaking
Crossing a pool filled with treacherous pale piranha
Patrolling haphazardly, underpaid mercenaries for evil acolytes
Cultivating shrieker watch-shrooms in strategic locations
Protecting a clan matriarch, suffering from a black widow bite
Darkening scales reflexively after hearing a sudden sound
Pursuing a group of bandits, hoping to steal their mule
Decorating small bone-pile shrines with shiny stones/items
Puzzling over how to operate a confiscated crossbow
Defeating a colony of crab spiders for a crunchy supper
Racing away from an inadvertently disturbed wight
Defending a humid and warm nesting site, dotted with craters
Raising hue-and-cry after discovering green slime
Detaching their tails to distract a hungry owlbear
Raking their claws futilely on a bemused gargoyle
Digging into rotting wood, seeking delicious wriggling grubs
Reeking with an especially pungent odor - mating season
Drinking stolen wine and growing quite rowdy
Resetting a spring-loaded board, studded with poisoned shards
Eating roasted giant rat, plenty to go around
Resting on hammocks woven from fibrous fungus
Erecting crude palisades to keep invading kobolds at bay
Roasting enormous robber fly larvae over low coals
Establishing a foothold within territory annexed by gnomes
Scouting nesting sites with the aid of an oracular crocodile
Excavating a fossilized skeleton of one of their forgotten gods
Scrambling out of the way of a wizard's ricocheting lightning bolt
Excreting foul secretions, watering eyes of a sage's apprentice
Scurrying on all fours, with wicked knives in their jaws
Farming row upon row of massive mushrooms for food
Sharing swigs of a potent toadstool tea that grants visions
Fashioning wickedly barbed harpoons from unusual bones
Sharpening horn and antler into daggers and blades
Filling the air with their offending stench
Shifting the hue of their scales to match an ancient mosaic
Fishing for giant cave crayfish, using giant bat bait
Skinning a giant ferret with flint hand-tools
Flinging sealed ceramic pots, brimming with grey ooze
Skulking along a well-travelled path, looking for traces of passage
Following giant toad tracks intently, needing toxins for rituals
Soaking ailing feet in a mineral rich pool
Forging crude metal weapons with the aid of a captured smith
Stealing a sharp steel dagger from the corpse of a thief
Frantically clubbing a rust monster, intent on consuming their iron
Surrounding a thoul, trespassing in their territory
Gagging a group of goblins with their noxious emissions
Taming a giant tuatara to ride into battle
Gnawing on the bones of a cave bear
Tasting the air with their forked cobalt colored tongues
Guarding an entrance to a fantastically beautiful grotto
Tending to special stalagmite sculptures of spiritual significance
Hiding within carved alcoves, melding with shadows
Topping off crude clay jugs from a trickling spring
Hissing loudly in a standoff with well-armed hobgoblins
Tracking down a wounded rhagodessa
Hunting a massive rock pythons as a rite of passage
Trading their strange puffball spore grenades to kobolds for metal
Illuminating an area, crude lanterns made of fire beetle glands
Trudging up walls, strapped to their giant gecko mounts
Injuring a retching veteran with their teeth-tipped clubs
Tying up an unlucky prisoner - a wererat concealing her nature
Intently sniffing as a stench bard relates a famous legend via smells
Unfurling their dewlaps and head crests in a dazzling display
Itching and scratching fiercely at strips of shedding skin
Viciously smashing a rival tribe's egg clutches
Joining forces with lizard men to eradicate pesky warm-bloods
Wallowing in shallow pits of heated mud
Knapping astonishingly sharp obsidian shards
Waylaying a warlock in search of special lichens
Launching volleys of bone javelins with clever atlatls
Wielding swords, stolen from a band of berserkers
Licking irritants from their eyes with long blue tongues
Worshiping at a jagged altar of murky glass
Lugging caecilia segments back to a settlement - a successful hunt
Wrestling for a new ceremonial title within the tribe

Table: troll
Accusing their reflection of stealing a bauble from them
Knitting together recent wounds together with sickening sounds
Allying with a local troglodyte tribe, mingling their stenches
Knocking on a door with a skull topped stick
Attacking a stag with savage fury and impossible hunger
Laughing politely as their brutal leader relays a funny story
Bloated from gorging on indigestible oranges, acidic enough to hurt
Leering from concealment at a portly pilgrim gathering firewood
Blundering into an armed dwarf patrol, furiously lighting torches
Lugging their lunch - a mangled/gnawed moose, stolen from a cougar
Brandishing the axle of a wagon as a crude cudgel
Lumbering on patrol, armed with uncharacteristically fine tridents
Brawling with each other while a frightened, fettered bard looks on
Luring a suspicious cow into a pit trap by waving clumps of hay
Building disgusting nests out of slimy moss and rotting vegetation
Lurking within incredibly cramped cupboards/cracks
Cackling maniacally after dropping a boulder on a bunny
Menacing a local hamlet, by kidnapping their festival queen
Calcifying in the rays of the sun - lurching toward shady dens
Mushrooming in size due to some strange affliction, covered in boils
Cannibalizing the weakest of their clan after drawing lots
Nesting in a now abandoned barn, picking teeth with farmer bones
Carrying severed heads under their arms to lob at foes
Noisily trudging through thick, stinking mud
Catching mucus covered hagfish with their unkempt claws
Opening an iron bound strongbox with brute force
Charging headlong into a group of distracted elfs
Overindulging on rancid radishes near an overturned cart
Chewing sullenly on what's left of the leather on a giant's boot
Positively rippling with rage within an owl bear's painful hug
Contorting into revolting shapes to squeeze into a crevice
Pulling a fraying rope, leading down a pit, tied to a rust monsters
Cowering from a veteran wielding a flaming sword
Pursuing a callow paladin who "slew" them and left them for dead
Dancing ungracefully to unsteady, discordant drums
Puzzling over a devoured mediums' many scrolls and spellbook
Devouring the unlucky bandit prince who tried to treat with them
Quenching a searing arm, set alight by a salamander, in a foul puddle
Dismembering their young - a cruel rite to bolster regeneration
Racking their tiny brains over a footpad's extremely simple riddle
Dominating the gaggle of goblins who live nearby
Rampaging after being tricked by a talking mule
Dropping a captured illusionist as she bursts into "flames"
Reaching wiry arms into a rat den for a squeaking snack
Dwelling, as is custom, beneath an essential bridge
Recoiling from a torch bearing trader in dire straits
Eating a disgusting giant toad stew from a dented cauldron
Re-growing a leg, stupidly severed when they were starving
Enforcing for a hobgoblin tribe, undependable and paid with food
Rending a rearing horse with their jagged claws
Feigning friendliness to catch a fat friar off guard
Roaring with mirth as they overfeed a boar
Felling a dryad's tree with stolen axes, giggling with perverse glee
Scattering a clan of kobolds, to steal their roast spider supper
Fishing from a crumbling pier with surprisingly effective tackle
Scheming to topple the evil sorcerer who holds them hostage
Frightening halfling children who unwisely strayed into the wilds
Scowling as a hill giant lays claim to all the tastiest prisoners
Fully regenerating after a big battle with an angry werebear
Seeking out a powerful magic-user to undo this inconvenient curse
Fumbling with a polymorph wand, surrounded by confused frogs
Singling out one of their number for the stew pot, no prey in weeks
Gardening in their mushroom farms, shoveling dung and detritus
Sneaking into a local village every night to pilfer chickens
Glowering at an alchemist, about to fling a vial of bubbling liquid
Sneering as a rival is peppered with arrows
Gnarling and twisting to re-sprout fingers lost in a blade trap
Sniveling at the feet of a wicked general
Gobbling down a trio of truculent goats
Sprawling on mildewed sleeping rugs, swatting large mosquitos
Gorging themselves on a rotting rock python, slain several days ago
Sprouting smaller, second heads - seen as a great blessing from the lump
Grabbing a flailing gnome to carry away to their kitchens
Stepping on awfully specific flagstones as they cross a room
Grinning beneath carrot-like noses at their mangled, miss-told jokes
Stooping down to drink from a fetid puddle
Growling, ever-hungry guts can be heard from some distance away
Stretching their gangly arms to reach roosting bats
Guarding a dungeon entrance, toll can be paid in coin or rations
Tattooing each other with strange, spidery symbols
Guffawing loudly as an elderly knight wheezes a challenge
Threatening local lizard men, who are seeking help
Gulping down clay cups of exceedingly foul moonshine
Throttling a thoul who dared to speak out of turn
Hauling a swollen net, absolutely teeming with screaming sprites
Towering over the frail swamp hag that leads them
Hoarding sheep, stolen from flocks of every shepherd in the area
Unnervingly deforming to snap broken bones back into place
Hobbling about impatiently after an amputating crocodile bite
Uprooting large, pulsating grubs for sustenance
Hunching even more so than usual to squeeze through a doorway
Vanquishing a minotaur, horning in on their territory
Idolizing a captured cleric who prays daily for create food
Voraciously consuming the carcass of a catoblepa
Imprisoning a bugbear chieftain, hoping to ransom her back
Wearing cloaks made of s of rat hides, stitched together with gut
Journeying to commune with mother lump - an ancient, huge troll
Wielding scavenged swords, arrayed in ill-fitting/mismatched armor
Jumping and shrieking as their rubbery feet are pierced by caltrops
Wounding a centaur clutching an extinguished torch

Table: tyrannosaurus rex
Attacking a huge hive of killer bees in a fury of wax and honey
Preying mostly on easy sacrifices from a local lizard man tribe
Bounding, low to the ground, after swiftly fleeing deer
Protecting an elf sleeping in a cut-crystal coffin
Bristling the quill-like plumes that line his neck and back
Prowling a shoreline for easy pickings on pirates
Broadcasting pungent pheromones for miles to attract a male
Pursuing a paladin and her galloping warhorse
Charging into a battle between mastodon and neanderthal
Quitting the hunt in frustration after a wyvern escapes
Chasing after a herd of hadrosaurs
Rampaging through a neanderthal's sacred site
Crippling a roc with a big bite to the wing
Rattling a trader's cookware with each step, still out of sight
Crouching low to smell the spoor of potential prey
Rearing young with surprisingly attentive and touching care
Crunching on bones with powerful jaws, gobbling them up
Reeking after an encounter with a dire prehistoric skunk
Defending a kudzu-covered ziggurat from tomb robbers
Rending a tree to pieces to dislodge loose teeth
Defiantly glaring at a lizard man shaman's spell-weaving
Resting in a dappled clearing, completely ignoring a unicorn
Destroying the carcass of a cave bear
Retreating from several rock lobbing stone giants
Displaying, via bright blue face patches, for a group of females
Ripping off dwarf-forged iron chains that can't hold him
Dragging a giant crocodile to dry land to gorge in peace
Roaming far and wide in search of a suitable challenge
Draining all color from a veteran's face with a loud roar
Roaring triumphantly over a dead green dragon
Eating sticky pods from a humongous chocolate tree
Robbing a kill from a pack of skittish dire wolves
Excavating damp earth into a nesting mound
Running with astounding speed, ridden by a ranger
Famished from an abscessed jaw and extremely ornery
Savaging a wagon, where a terrified sage hides within
Feasting on a spear slain megacerops while hunters look on
Scavenging on a mastodon carcass, mired in mud
Fighting an equally massive, four-armed white ape
Seeking to destroy some troublesome trolls that took her den
Flicking a phalanx of kobolds aside with their muscular tail
Seizing an ogre in his jaws and tossing it like a toy
Following the shuffling tracks of a wounded triceratops
Shaking every tree as they step, sending pterodactyls screeching
Gazing at constellations, as if awaiting instructions
Shredding a gorgon by biting gory chunks
Gingerly feeding small, wolf-sized hatchlings strips of meat
Slaying a fluttering manticore
Gnawing on the many-vertebrae bones of a hydra
Snarling as she smells a rival female nearby
Greedily devouring the ropy innards of a stegosaurus
Spotting circling vultures to find a convenient kill
Growling, almost purring, as harpies preen and groom her
Stalking a band of explorers, completely oblivious
Guarding their wheezing mate, dying from poisoned arrows
Stampeding a herd of diminutive eohippus centaurs
Guzzling massive mouthfuls from a scenic waterfall
Staring intently at antelopes drinking from a watering hole
Herding horses together through conspicuous appearances
Startling all manner of wildlife with every thunderous step
Howling resoundingly to remind the territory of its queen
Stealing a pre-cooked kill from a pouting chimera
Hunting the foolish thief who stole eggs from their nest
Stepping carefully across a sheep-sized caltrop strewn field
Judiciously sniffing at dangling brontosaurus bait
Stomping in frustration at a frantically fleeing black dragon
Killing a giant catfish with a perfectly timed, splashing snap
Striding with surprising grace and speed through a dense wood
Lapping from a freshwater spring, terrifying nixies
Subduing their energetic/playful young with a growling chirp
Lashing out at their vivamancer with lobster like claws
Sunning themselves atop an overturned stone galleon
Leading young on their first hunt - starting small - humans
Swallowing a halfling whole, while an adventuring party shouts
Leaping onto the back of a partially submerged sauropod
Tamed somewhat by a troglodyte mummy in a nearby tomb
Limping from an ogre's axe wound, scabbed and festering
Tearing a chunk from the horizon with their huge silhouette
Lugging a dead rhinoceros back to their den
Tenderly turning their clutch of eggs with their snout
Lumbering through a humid, fern-drenched forest
Terrorizing dwarf prospectors, by spooking their mules to flight
Lunging half-heartedly at a diving pteranodon
Towering above an ancient stone circle, patiently listening
Lurking, nearly up to the neck, in deep swampy bayous
Tracking an obstinate ankylosaurus
Mauling a friendly hill giant mountain man
Trampling and re-trampling skeletons as they rise from graves
Menacing a peaceful gnome village with inconsiderate steps
Utterly crushing a trader's cart with a swipe of their tail
Muzzled with rapidly fading cerulean bands of eldritch power
Vanquishing another t. Rex - a rival for the crown of crowns
Nesting on the crest of a highly defensible hill
Waking a drowsy dryad by crashing into her grove
Observing distant curls of smoke on the horizon
Watching a medium study a spellbook, mouthing the words
Overpowering a smaller and weaker male, trying to steal a kill
Wooing females with a huge and highly decorated bone bower
Plunging their banana-sized teeth into writhing purple worm
Yawning as they survey carnage after battling frost salamanders

Table: unicorn
Aiding a mother bear in locating her adorable cubs
Luring a poacher deeper into more dangerous wilds
Ambling slowly, beautiful flowers blossoming in every hoofprint
Meeting with an elf sage to plan the next several springs
Appearing suddenly in the center of a crisp, dew drowned clearing
Munching on delicious offerings, left by superstitious farmers
Avoiding detection from a hobgoblin hunting party
Narrowing their eyes at the desperate lies of a medium
Balking at a crude bugbear booby trap
Neighing softly at a mule's humorous anecdote
Befuddling a bandit by freeing her prisoners
Neutralizing the burning viper venom in a ranger's leg
Being groomed by a group of giggling sprites
Nibbling cherry blossoms, perpetually blooming in her presence
Blessing an elf union by silhouetting on a hillcrest
Nodding in approval to a neanderthal truce
Bringing a branch of ripe blackberries to a blind beggar
Nuzzling the lap of a spared sacrifice
Bucking to deliver a devastating kick to a kobold
Observing an orc war band, as they move through the wood
Calming a lost child, hoping someone will return them home
Offering to show the brave to the treasure-laden lair of an evil wraith
Cantering serenely within a stand of pale paper birch trees
Officiating at a druidic ceremony to celebrate bounty
Casually sidestepping a vampire skull, overgrown with roses
Overseeing a respectful woodcutters work
Charging at a pack of slavering dire wolves
Patrolling the edge of a valley for signs of a manticore
Chasing a chimera out of their forest
Pawing the turf before charging an angry minotaur
Confusing a trapper by tripping his snares
Perking their ears at a witch's whispers on the wind
Consecrating a woodland shrine's bubbling spring
Piercing the scroll in an evil wizard's hand, ruining the spell
Conversing silently with a stag
Playing checkers with a treant, with pixies moving the pieces
Curvetting over a thick hedge of brambles
Plunging their horn into a hill giant's thigh
Defending a blink dog den from a hungry hellhound
Prancing in a pixie parade, draped in garish garlands and caparison
Destroying a nest of vile cockatrice eggs
Protecting a precious foal from persistent poachers
Deterring loggers by ransacking their camp
Purifying a muddy puddle for a dervish, dying of thirst
Dipping their horn in a pond, befouled by bathing trolls
Quieting a quarrel between squirrels
Disarming a cruelly set snare with his horn
Rearing to defend a wounded cleric from a diving wyvern
Disemboweling a wicked noble
Relentlessly hunting the malevolent mercenary that slew her mate
Drinking from a pristine pool of water, as dragonflies flit by
Reminding a ranger about a secret path through the forest
Emerging from a thick curtain of fragrant wisteria
Restoring vitality to a spectre-drained dwarf
Enchanting a hidden halfling, peering from a treetop
Ridding a rotting rune carver of their mummy-related disease
Flicking their tufted lion-like tail reflexively
Roaming far from home, to seek out an infamous seer
Formerly a paladin, inadvertently reincarnated into this role
Savagely injuring rust coated gorgon, as his fetlocks turn to alabaster
Galloping toward a distant cry for help
Scattering leaves to conceal the trail of a herd of deer from hunters
Gingerly crossing the pebbled bottom of a babbling brook
Sheltering from a recent thunderstorm in a cozy cave
Goring an odious ogre, overfishing her lake
Shimmering like a mirage, almost unreal
Grazing on perfumed grasses, chained to a pomegranate tree
Shyly watching a young maiden pick forget-me-nots
Guarding a sacred grove, dotted with mossy, glyph covered stones
Slightly singed from a recent run-in with a heinous hydra
Guiding a dryad locate rare/valuable/delicious mushrooms
Snorting dismissively at a repetitive dwarf work-song
Halting midstride, turning her head to hear a sound
Splashing in a shallow grotto to melodious nixie song
Helping a pegasus locate a suitable place to foal
Sprinting after a trader, selling roc eggs
Herding some overgrazing sheep back to their pen
Stalking a group of lizard men, unsure of intentions in her wood
Imbuing the entire wood with a palpable sense of peace/safety
Systematically stabbing a shambling horde of zombies
Impaling a drooling ghoul who wandered into her wood
Thrashing against strong spider-silk nets as goblins try to hold her
Imploring their mate to not leave the wood
Tilting against an evil knight, as a captured princess looks on
Instantly disappearing only to rematerialize two hundred feet away
Toying with a noble's hunting party, warning animals of their arrival
Judging a trophy hunter, entangled in barbed vines
Trampling a thoul archer beneath cloven hooves
Keeping their horn keen by sharpening it on a worn block of stone
Transfixing an elderly acolyte, in tears at such awe-inspiring majesty
Kicking aside a brigand bumbling with buckler and blade
Unhitching a mistreated horse while their owner naps nearby
Knocking fruit from overladen branches for hungry piglets
Urging a weretiger to give up wicked ways
Leading a hopelessly lost gnome home
Vanishing in a sudden, unforeseen rain shower
Listening intently to warnings from the waxwings
Watching their forest slowly shrink from the encroachment of man
Locating a centaur child separated from his tribe
Weeping near a stand of trees devastated by wildfire

Table: vampire
Abducting a handsome duke to keep as chattel
Laughing at the incompetence of the acolyte sent to behead him
Appearing to evaporate before your very eyes
Leading a pack of wolves on their nightly hunt
Avoiding strategically placed mirrors, powerless to remove
Lunging toward the unarmored neck of a bugbear
Awakening from hunger induced dormancy, ravenous
Lurking dramatically in a doorway
Beckoning to a minion to fetch a captured prisoner for feeding
Malevolently influencing the royal court through their proxies
Bewitching a band of berserkers
Metamorphosing into a giant bat to take wing
Biting a noble's neck and drinking deeply
Mustering a seething swarm of plague-bearing rats
Calling forth a swarm of chittering bats
Nursing their living lover after greedily drinking too much
Calmly lapping blood from the neck of an unconscious gnome
Obsessing over image, paying painters handsomely to see themselves
Causing hysteria nearby, draining key personages nightly
Overseeing the exhumation of their latest victim
Changing into a coal black wolf, pony-sized, glowing green eyes
Perpetrating an archaic custom by taking a bride every full moon
Charming and well-fed, eager for news and gossip
Profaning sacred texts with heretical marginalia
Checking on spare coffin, in a crypt of loyal ghoul guardians
Puncturing the neck of a poacher that wandered to close
Cheerfully desecrating a small shrine to the godling of sunrises
Rallying giant rats to overwhelm an exhausted adventuring party
Circling a determined but tiring cleric brandishing holy symbol
Rapidly healing a grievous sword wound with a smirk
Clouding the mind of a medium
Recoiling from a friar's holy relic
Colluding with a doppelgänger, after finding their blood distasteful
Reinforcing a casket with powerful enchantments
Convoking a coven of their vampiric spawn
Repulsed by recent flooding, forced into a corner of a room and feral
Counting scattered grains of rice in a fit of arithmomania
Researching a way to undo their curse
Cursing at a garlic-garlanded gargoyle
Resting after a lavish meal, drained ogre corpse nearby
Daring a desperate dervish to strike them down
Returning to their family crypt after a long absence
Deciding discretion is the better part of valor, fleeing a witch hunter
Secreting an extra coffin in a concealed location
Dematerializing into a foul anthracite miasma
Seducing both leaders of rival factions to spark a bloodbath
Discussing strategy with an ensorcelled elf
Seeping under an iron door in gaseous form
Disincorporating after a grievous wound from a dwarf
Seething with rage after discovering a destroyed coffin
Draining a dryad, her blood inducing honey-suckle scented hiccups
Shapeshifting into a massive bat, fingers stretching, a sickening sound
Drinking mostly from livestock, ashamed of their nature
Shrieking after being splashed with holy water
Emitting high-pitched squeaks to bat-winged brethren
Slaughtering an entire tribe of kobolds to slake his thirst
Enshrouded in palpable darkness thanks to a magic cloak
Sleeping soundly in a coffin nailed overhead on a very high ceiling
Entering through keyholes, formerly an accomplished burglar
Slowly desiccating a damsel by drinking from her wrist
Fading from view like the haze on a hot summer day
Snatching blood bloated stirges from the air as a snack
Ferociously feeding, leaving behind a trail of pale, bloodless bodies
Sowing confusion by turning a goblin bodyguards against their king
Flinching from a reflective pool of water
Stalking their descendants to protect them from harm
Gathering blindly loyal hobgoblin minions
Summoning their rodent spies to report on the progress of a scheme
Gazing into a paladins eyes, causing her to drop her sword
Swiftly evanescing to spy on a group of acolytes
Gradually transforming the populace of a local hamlet into undead
Terrifying a former acquaintance that they wish to turn
Hesitating at the banks of a babbling brook
Threatening a thoul minion with a barbed lash
Hissing inside the holy circle that binds her here
Tormenting a local priest with tempting visions
Howling alongside the children of the night
Transcribing sheet music of an ensorcelled harpy's song
Hunting down a hermit he knew while still alive
Trying to obtain an invitation into a castle, where her prey is protected
Impaling a veteran with his own spear
Turning to necromancy to create some company
In league with local lycanthropes
Unleashing frustrations on a hypnotized halfling
Indulging in a bottle of spicy fire giant blood
Vanishing from view among a writhing mass of worms
Inflicting a horrid pestilence on vital crops
Veiled in thick wrappings after leaving their lair during the day
Ingesting one of several experimental blood potions he's created
Warning a tomb robber of traps in exchange for a drink
Inspecting a new casket, carved from a dead treant
Wearing out flagstones by pacing for centuries
Instantaneously re-growing a severed finger
Whispering instructions to a foolish cult leader
Judging a dance recital, put on by minions for their master
Withered and burned after recently being caught in sunlight
Kidnapping a terrified trader
Wooing the captain of a brigand company to make war on a rival
Languidly exsanguinating a willing victim
Yawning widely, exposing ivory fangs

Table: human, veteran
Acting as an ersatz army for a local hamlet, paid in spicy ale
Lifting a paralyzed ally onto a makeshift liter after ghoul attack
Answering a declaration of war, travelling to sign back up
Limping thanks to a devious kobold leg trap
Arguing over who ate the last ration
Mapping a new trade route through a chimera's territory
Avenging a fallen comrade, slain at the hands of thouls
Marshalling for battle against a minotaur
Bandaging up an unsightly gash after a fight with zombies
Moonlighting as gravediggers, business is good
Bargaining with a gargoyle for passage
Mourning a trusty companion - blade shattered and ruined
Belting out old ballads, lamenting the life of a soldier
Mustering under a brigand's banner, unable to settle down
Bludgeoning a black pudding with sputtering torches
Neutralizing a nest of bloodthirsty stirges
Brawling over the attentions of a grinning harpy
Nominating a new captain, statue of the former nearby
Camping near dungeon entrance, robbing those who exit
Nosing around a ruined shrine to the goddess of pyrrhic victory
Castigating a torchbearer harshly for making too much noise
Obeying the sometimes-unusual commands of a nixie
Chaffing at conflicting orders, recently received from on high
Observing a local holiday tradition, no blood can be shed
Clinking in mismatched, scavenged armor
Occupying a former hobgoblin fort, awaiting reinforcements
Counterattacking a bugbear lair, after an overnight ambush
Oiling scabbards and armor, to keep gear in good order
Darning woolen socks with surprisingly dear sentimental value
Outfoxing a hungry hill giant - food for platinum pieces
Deputized by a local lord to hunt down bandits, on the take
Pacifying a surprisingly war-like clan of gnomes, unsuccessfully
Deserting their posts as a unit after a harrowing defeat
Parceling out treasure by rank and tenure
Drinking very potent gnome spirits, but somehow still glum
Pestering local elfs with clumsy and noisy patrols
Drying soggy boots and cloaks by an anemic campfire
Pitching a heavily patched tent, wordlessly and efficiently
Eking out a living escorting trade caravans, seeking a new gig
Practicing with their longbows, expert shots
Entrenched near a small settlement - suspected wererat warren
Quelling a recent revolt, started over fears of witchcraft
Eulogizing a fallen comrade, with humorous tales and tears
Quibbling over who lays claim to a sheaf of magic arrows
Experimenting with a potion of unknown purpose
Ransacking a defenseless lizard men village, rumors of gold
Feigning retreat from an ogre, luring him into a pit
Rebuilding a barn, damaged by a recent dragon strike
Fishing around in a pack for dry tinder after seeing troll tracks
Recoiling in fear from the savage frenzy of giant shrews
Flaunting shiny new armor/weapons from a wealthy patron
Retching and overcome by troglodyte stench
Foolishly partaking in a proffered pixie feast
Safeguarding important diplomatic papers, tragically illiterate
Freezing and shivering after a run-in with a frost salamander
Salivating over a sumptuous catfish supper
Gagging a goblin prisoner who wont stop screaming
Salvaging spent ammo and a serviceable helmet from berserkers
Gorging on poached venison and cyclops wine
Singing a cadence, learned back during the wizard wars
Grinning as they smash open a strongbox full of coins
Squandering the remainder of their life savings on a horse
Hacking down a sturdy wooden door with an axe
Sterilizing a bite from a giant bat, hoping for the best
Hammering out dents in a shield that has seen better days
Teaching a medium how to wield a spear, stifling giggles
Hawking several scrolls they found on a medium's body
Thwarting an orc incursion that threatened a village
Herding halfling pilgrims to safety from giant rats
Toasting with wyvern horn tankards to battles long ago
Hiking up a slope, exhausting third day of a forced march
Trimming hair and beards to regulation length out of habit
Honing their weapons, passing around a "lucky" whetstone
Tying knots in a rope to measure the depth of a yawning pit
Hurling javelins at a tree trunk, angering a dryad
Undertaking a perilous voyage to a nearby coast
Igniting a bonfire to roast a boar on a spit
Uneasily uniting with nearby nomads, against a common threat
Improvising a sling for a potentially broken arm
Venerating a former commander, almost to the point of worship
Inspecting inexperienced levied conscripts
Visiting a battlefield with almost pilgrim like reverence
Itching for a scrape, tempers high after gambling loss
Vowing not to touch another drop as they endure a horrid hangover
Jamming a door shut with iron pitons
Waging a war of attrition on a squadron of skeleton warriors
Judging an arms trader's merchandise carefully
Warming their hands and feet by a cozy campfire
Kicking an addiction to dreamspores, jumpy and unpredictable
Waxing silent bowstrings, a gift from an elf they rescued
Kidnapping a dwarf, hoping for a huge ransom
Welcoming any fellow fighters as comrades and old friends
Lancing large blisters on calloused, smelly feet
Whistling convincing birdsong as they prepare a bushwhack
Laughing heartily at unrepeatably ribald jokes
Wrecking a local economy by spending pricey plunder
Leading an expedition to claim treasure on an unreliable map
Yawning as their tag-along cleric proselytizes
Lecturing the less experienced on swordplay technique
Yielding taken turf to a vicious pack of hellhounds

Table: warp beast
Ambushing a band of easily scent-stalked troglodytes
Leaping out of the way of a medium's lightning bolt wand
Angrily examining the interrupted tracks of a blink dog
Licking their gore covered paws contentedly
Appearing to swerve and tremble as it strides
Lugging the lifeless body of a lizard man up a tree
Battering a well-crafted dwarf helmet playfully around
Lurking among several fine statues of lions and leopards
Bending in unnatural ways to traverse a narrow gap
Mangled from a recent run-in with a manticore
Biting at their second row of shoulders to dislodge fleas
Marking the edge of territory with a viscous, bubbling spray
Bounding over broken terrain with unnerving, uncanny grace
Mauling a mule, laden with mining equipment
Bristling as they snarl at a raging berserker
Mewling pathetically, somehow trapped in a deep pit
Calculating a potential pounce, shimmying their rear as cats do
Nailing a scurrying rat to the floor with a lash of their tentacle
Cambering up a toppled tree for a better vantage point
Nibbling at a paw, impaled with a painful astral thorn
Caterwauling up a storm in frightful estrus
Nuzzling a bunch of astral catnip as a satisfied sage looks on
Chasing after an unsatisfying rabbit meal
Occluding a crossbow wielding orc's aim
Clawing an overstuffed armchair with glee
Pacing impatiently, waiting to be fed by bugbear masters
Constricting a helpless halfling with their fleshy pink tentacles
Pattering down an echoing corridor, towards a terrified scream
Contorting into a perverse, non-euclidian position
Plucking a juicy giant bat from the air with a well-timed jump
Cornering a futilely snapping giant crab, toying with prey
Pouncing on a poacher checking her snares
Creeping low, in verdant undergrowth, utterly silent
Preying on penned goats, almost too easy to be satisfying
Crossing the path of a pious paladin, sent to slay her
Prowling the edge of a bandit camp, smelling a roast duck
Crouching after landing from a great leap
Pummeling a rival with their razor-sharp spurs
Curling sinuously around an ornately carved column
Purring with every stroke from a garrulous gargoyle
Deforming before your very eyes, almost causing headaches
Pursuing a potential mate - a dance that can last for months
Devouring a dead doppelgänger, messily and with gusto
Quavering and fluctuating, casting several sets of shadows
Distorting light, not unlike a mirage or shimmer over campfire
Rattling the keen bristles on their tentacles in a threat display
Diving from a concealed perch, onto the back of a dervish
Refracting sharply, appearing to occupy only a single plane
Dragging a still flailing white deer, to dine in peace
Ripping into a goblin tent, not really that worse for wear
Enraged with raised hackles, struck by a very lucky arrow
Roaring meekly as a wizard brandishes a controlling rod
Eyeing a caravan of armed merchants cautiously for stragglers
Scaling a sheer cliff face, perusing a pegasus colt
Famished due to a fey bell, attached to collar in a pixie prank
Scavenging a kill, as disappointed wolves pace fearfully
Fishing by plunging tentacles into a pool, consistently catching
Scourging a brave steed-minder, defending his mistresses' warhorse
Flickering ominously, as if due to some sort of interference
Scraping moist, fleshy tentacles along the ceiling as they strut
Flushing out giant rats from their disease-ridden den
Scratching behind their ear with one of their four hind legs
Following gnoll tracks intently, hoping for an easy meal
Screaming with indignation after triggering a tripwire
Frustrating a stone-slinging cyclops, cackling and jeering
Seizing the carotid of a caribou, bringing it down
Gouging through an elf chain shirt, to keep their claws sharp
Shrinking from a shimmering spell of detection
Grabbing a stirge snack on the wing with a quick flick of tentacle
Snarling as a spitting cobra misses their mark
Grimacing at a faded circle of binding on the floor
Snatching specially bred sheep from a gnome shepherd's flock
Grooming their sleek black coat with gentle tentacle combing
Sneering tenebrously at a terrified thoul
Growling in a defensive stance, as an ogre tries to corner them
Squeezing life from a careless kobold, wandered into her territory
Guarding the entrance to a den of writhing glyph-spotted cubs
Stalking shadows, necessary for maintaining a healthy hide
Gulping down chunks of horseflesh greedily
Stretching indolently, belly somewhat distended from a recent meal
Hissing as their blink hound quarry suddenly vanishes
Striding across a flour strewn floor, with tracks appearing adjacent
Hunting a hunter for the sheer sport of it all
Striking at a skeleton warrior, interrupting their hunt
Incessantly preening, not a single tuft of fur will be left out of place
Thrashing within a cold iron cage, being loaded onto a cart by orcs
Infuriating a fighter, swinging wildly and missing with every strike
Tremulously cowering from a much larger male
Joylessly gobbling a goblin, craving larger fare
Unfurling their barbed, squid arms with a shrill cry
Jumping atop a jagged bluff in a single powerful leap
Upgrading their den after overpowering an owlbear
Keening softly to a litter of sleeping kittens
Voraciously tearing into a suspended slab of meat, a baited trap
Languorously sprawling atop a pile of bones
Watching an illusionist with cat-like curiosity
Lapping up spilled lamp oil, a delicious delicacy
Wavering by a few feet with every graceful traipse
Lashing tail and tentacles menacingly as they skulk about
Yowling after a lucky donkey kick shatters one of six femurs

Table: water termite (freshwater)
Abrading the bottom of a barge with tentative nibbles
Overwhelming a friendly fisherman's haphazardly patched boat
Bonding together pebbles to fabricate huge hollow hives
Perforating the planks of a newly constructed pier
Capsizing a ramshackle raft, terrified dwarf rider can't swim
Pulling themselves onto the deck of a profitable ferry
Chewing through the supports of an important bridge
Puncturing a crucially placed beaver's dam
Climbing up the sides of a coracle full of frantic sailors
Rebuilding an underwater villa for their nixie allies
Damaging the hull of a longship, laden with trader's goods
Regurgitating pulp to feed translucent larvae
Dwelling near a series of treacherous rapids
Retreating from an insatiable giant bass
Erecting a waterproof spire, reaching high above the water
Scrambling down the tree trunks of shoreside shade
Flocking around a bobbing log, reducing it to dust in minutes
Serving as tasty treats for a hungry giant catfish
Foraging on the banks for sodden driftwood
Showering a brigand crew with their stunning spray
Gnashing their mandibles threateningly at a crocodile
Streaming aboard a small ship of pirates who ply the rivers
Guarding a small island, where a single treant still stands
Surging for a seasonal migration, water thick with them
Jetting foul foamy ink after being beat with a bargepole
Tenderly brooding pale, oblong eggs the size of melons
Menacingly floating towards a funereal flatboat
Utterly decimating trees inundated by flooding waters
Noisily feeding on an intricately woven fishing net
Voraciously consuming the lumber in a large log jam

Table: water termite (saltwater)
Avoiding a school of huge and hungry fish
Pestering an anemone waving giant crab
Boarding a buccaneer's ship, to chew on sails
Plaguing a pirate fleet taking a risky shortcut
Boring through the hull of a hobgoblin hulk
Reducing a sunken wreck to a pile of corroded nails
Chomping through floating flotsam as seagulls circle
Rushing to shore up hive damage from a giant octopus
Clinging to strands of swaying kelp, just below the surface
Scattering to escape the jaws of a sea serpent
Clouding the sea after an old salt pours wine overboard
Scurrying up the anchor chain of a moored vessel
Coming ashore for a clumsy duel to select a king
Splashing anesthetizing spray into a foundering lifeboat
Defending their fortified reef mound from a curious eel
Sputtering plumes of water on the surface to signal a meal
Diving deep after deflating their strange sacs
Struggling to swim, tethered to a merfolk merchants cart
Dragging a beached boat back into the water
Summoning additional soldiers to deal with a shark
Eating the ends off the oars of a bireme
Surfacing slowly among thick floating mats of seaweed
Fleeing after a sudden waft of tidal pheromones
Swarming a giant sea snake to drive it away
Ganging up on an unarmed halfling pearl diver
Teeming on a fuzzy whalefall
Gliding along the surface toward a schooner
Thrashing in a trawlers humongous net
Nearly breaching the waterline of a brigantine
Tunneling into a storm giant's undersea stronghold

Table: water termite (swamp)
Annoying local lizard men by feeding on their palisades
Hiding from hungry troglodytes who consider them a delicacy
Balling up into a writhing mass, bobbing on the surface
Infesting an abandoned dugout, floating upside down
Bubbling furiously beneath the surface, enough to sink a raft
Laying siege to a cramped ogre camp
Burrowing deep into the heartwood of a massive cypress
Loudly clicking their jaws together to frighten fish
Clasping firmly to the underside of a canoe
Mulching mostly deactivated wood golems
Constructing tempting timber walkways with cached food
Nesting beneath a sickly and burbling, moss-choked waterfall
Crawling out of a huge sun-bleached snail shell
Nibbling inquisitively on a damaged and sputtering magic staff
Crumbling an inundated cottage
Obdurately clipping cat tails and reeds
Cultivating a digestive fungus on the bark of dead wood
Piling stones strategically to flood a stand of trees
Cutting strips of fragrant bark from saplings
Ravaging the rudder of a gnome-made rowboat
Dismantling a wooden fishing weir
Repairing troll damage to their macabre towering hive
Dragging a large, rotting log to their underwater larder
Sinking a poorly made goblin gondola
Gnawing through the side of a moored trader's barge
Staining greenish water a deep shade of black with their ink
Hauling eggs, single file as they paddle to a new nest
Storing moistened branches atop a mound to ferment in the sun
Heaping water-logged lumber into a barn-sized mound
Weaving meticulous mats of long grasses into a floating nest

Table: weasel, giant
Ambling through a field of dozens of shattered statues
Peering out of the pockmarked barrow they call home
Biting into the top of a massive egg and slurping the contents
Plaguing a local halfling village by slaying every chicken
Bounding blithely across a shrub strewn field
Playing keep-away with a human skull, inset with gems
Burrowing intently after picking up the scent of a huge mole
Popping their heads out of cracks in a wall
Caching a deer kill for later inside a large hollow log
Preying on a still thrashing and enormous earthworm
Capering atop a pile of steaming rubbish
Protecting the elf archers that they are bonded to at birth
Carrying an unconscious cleric by the blood-stained cloak
Prowling through a strange mound of mismatched boots
Catching up with a clattering cart, hungry for horseflesh
Pulling a gnome's wagon home, semi-domesticated
Cautiously slinking around narrow corners
Quickly striking a giant rattlesnake
Constantly slipping on a slick cobblestone surface
Reclaiming a blink dog burrow after they wisely moved on
Cornering an extremely nervous cockatrice
Ricocheting off walls, absolutely full of energy
Creeping stealthily after an oblivious bull
Romping on a stony slope, flinging pebbles everywhere
Crossing a trickling stream, stopping only to snatch a fish
Running down an exhausted jackalope
Darting beneath a cobbled cairn, peeking out various holes
Ruthlessly rushing a rhagodessa, showing absolutely no fear
Delivering a stunned dwarf to their young to kill
Scampering after a packmate, gold necklace in her jaws
Devouring a big woven basket of apples
Scowling at a distant roaring sound
Dragging an enormous rock python by the neck
Scurrying after an injured owl bear
Drinking deeply from the neck of a nomad
Serving as very temperamental mounts for elite kobold cavalry
Dropping their mangled kill to chase after a rabbit
Shedding constantly, as new seasonal coats start coming in
Dwelling in an abandoned building, littered with bones
Shivering and wet, gnawing on a giant pike
Ear-splittingly screeching as one returns with a goat
Sinuously slithering through barbed brambles and undergrowth
Emerging from their den, squinting and sniffing the air
Sitting upright and rapt, listening to a distant singing
Ensnared by a clever cage trap, throwing themselves at bars
Snaking their way into a hole, barely big enough
Evicting an embarrassed chimera from her cave
Snarling and seething at a hobgoblin taskmaster with a whip
Feeding chunks of mule to very energetic kits
Sneaking into the back of a wagon, laden with furs
Following foul-smelling footprints of an appetizing ogre
Snickering as they squabble over a dead giant bat
Furiously digging, soil spraying everywhere
Spiriting away a tent, screaming veteran within
Gawkily clambering up a coffinwillow tree
Spooking a warhorse to the point of rearing off its rider
Grabbing a fighter's shield and dragging it across the ground
Springing on a crunchy oil beetle
Guarding a ranger's retreat, distrustful of different smells
Squinting as they scan for the source of a distant thump
Gutturally growling at a giant hawk overhead
Squirming their way into a large reptilian skull
Hauling a blood drained hellhound, slightly scorched fur
Stalking a scuttling rust monster by its metallic scent
Hiding a hobgoblin snack under a table for later
Staring down a coiled giant cobra
Hissing vociferously at a gargoyle
Starving and tethered with chains, baring sharp pin-like teeth
Hopping and bouncing down a well-travelled pathway
Stealing leg bones from marching skeletons for sport
Hunting giant gecko, they have clinging out of reach
Storing what looks like a human leg among some thick roots
Hypnotizing birds on a branch by wriggling rhythmically
Surrounding a lone centaur, out on patrol
Impishly nipping at the hills of an annoyed living statue
Swiveling suddenly to lightheartedly nip on each other
Jumping onto the back of a retreating bandit
Tenaciously latching onto a stumbling lizard man
Keenly chasing the fading trail of a troll
Thoroughly draining a pallid thoul
Killing giant rats, outfitted with fancy collars and nametags
Tracking a driver ant back to its nest to feast
Lapping up a pool of blood as a bear's corpse cools nearby
Trapping a thief in a deep pit, staring down inquisitively
Leaping into a frenzied fray of screeching giant shrews
Undulating as they meander among some mushrooms
Lugging a wounded sheep back to their boggle
Utterly destroying a chest full of wedding dresses
Menacing a medium who was hoping to find a familiar
Viciously attacking a giant toad
Mirthfully pouncing on each other with friendly snarls
Waving head side to side to pick up the scent of its prey
Noisily cavorting with several seething kits
Wolfing down a helpless farmer's cabbage crop
Obsessively combing their valuable pelts with their claws
Worrying an orc warrior, backed into a corner
Outwitting a hunter by ransacking their camp while their out
Writhing in a coiled ball of fangs and fury
Patrolling their territory, scent-marking everything/everyone
Zipping through the legs of their adopted hill giant parent

Table: whale, killer
Aggressively chasing away a pod of dolphins
Milling around a particularly prey-rich patch of water
Attempting to capsize a shipwrecked pirate's raft
Playfully antagonizing a sea turtle
Blowing bubble nets to entrap a school of sardines
Riding the wake of a gigantic galleon cutting through the waves
Clicking cordially upon reuniting a long-lost family member
Scavenging on a floating whale carcass
Devouring a sea lion straggler, unable to escape
Snorting and splashing as they slap their fins on the surface
Echolocating to uncover tasty giant crab on the seabed
Spy-hopping in the churning waters to locate prey
Entangled in fisherman's nets, digging into their flesh
Stalking a giant sturgeon, unable to defeat its armor
Escorting a fishing boat back to shore after being fed
Submerging suddenly after a distressed calf's call
Festooning their flukes with kelp/seaweed
Surrounding a whaling vessel and making the crew nervous
Gliding gracefully through glass-smooth seas
Swimming swiftly just under the surface - ominous dorsal fins
Hunting down a great white shark that killed their matriarch
Tail-slapping after forcing herring into a clumped ball
Hurling themselves into the air to take a harpy on the wing
Throwing a barking seal into the air
Joyously leaping to breach with huge splashes
Voraciously eating salmon on their way to spawn
Lovingly trained by local merfolk to serve as mounts
Wheeling around to separate a walrus from her pup
Lunging ashore to suddenly grab an unsuspecting seal
Whistling loudly to warn the pod of evil stingray folk

Table: whale, narwhal
Attacking a lifeboat, crewed by ghoul sailors
Launching out of the water to breach
Cavorting among jagged ice floes
Listening patiently to a paladin preach, stranded on ice
Churning up frigid waters as they gobble cod
Logging, still on the surface, to bask in the warming sun
Circling protectively around a newborn calf
Majestically fencing with their spiraled tusks
Conserving their energy by lazily following the currents
Migrating to less ice-bound waters
Disappearing at the base of an ominous iceberg
Piercing a bloated, barnacle encrusted sea zombie
Expelling plumes of water high into the air
Plunging to the sea bottom to hunt for skates
Feasting on halibut, thriving in these parts
Propelling themselves with their powerful tails
Fleeing from nomad whalers in search of ivory
Pulsing frantic calls after spotting killer whales in the area
Following a congealment of cuttlefish to feed upon
Quickly cruising through an open path in the ice
Foraging under the sea ice for food in lean times
Singing whale song, containing snatches of lawful words
Frantically trapped after their whale-roads froze over
Suckling their calves, alert for potential predators
Gathering to serve as judges for a cetacean tribunal
Surfacing to breathe through a hole guarded by polar bear
Gulping down delicious swarms of shrimp
Towing bits of flotsam with shipwreck survivors to shore
Inadvertently impaling a giant octopus
Undulating, synchronized as a single, family unit

Table: whale, sperm
Allowing gulls to pick parasites their sucker scarred backs
Overturning a longboat for failing to keep its distance
Avidly swamping a sailboat in their waters
Protecting a mermaid merchant's caravan
Breaching with a tremendous spray
Ramming the starboard side of an already damaged ship
Congregating to finally deal with a kraken problem
Serenading a frightened calf to semi-sleep
Consuming and entire school of fish in a single gulp
Severing a giant octopus tentacle with a powerful bite
Covered in symbiotic barnacles, forming runes
Slamming the water's surface with a huge tail-splash
Crippling a hobgoblin caravel
Splintering a whaleboat clean in half
Diving after a near-miss from a harpoon
Spouting plumes of seawater to clear their blowholes
Dragging a sea serpent to the depths to drown it
Stunning a school of fish with a reverberating sound
Engulfing a fisherman's catch, net and all
Thrashing violently, a harpoon embedded in her back
Floundering, beached on a shallow sandbar
Utterly swallowing a halfling fishing vessel
Forming a flower-shaped protective circle
Vomiting up great gobs of valuable ambergris
Grazing on a fluttering bloom of small squid
Wallowing in the warm waters of a deep lagoon
Harvesting huge mouthfuls of water termites
Wise in her years, this whale is an accomplished cleric
Lashing large flukes on the surface with loud slaps
Wrestling ferociously with a desperate giant squid

Table: wight
Anchored to this location by a huge obsidian shard
Lightly grazing the face of a dwarf, who falls lifeless to the floor
Anyone but elf ancestors are greeted with violence
Limping, one leg turned to granite by a gorgon in life
Ardently draining life from a twitching tomb robber
Lying atop a marble altar, arms across chest
Avoiding an ornate portrait of themselves alive
Mangling a mercenary with a sunken face
Balefully grimacing with tarnished copper teeth
Missing their heads (decapitated for crimes) but no less deadly
Brandishing wickedly barbed scourges
Mocking a monk with shaking hands, intoning from a scroll
Breaking down a stubborn stone door, barehanded
Muttering prophecies of imminent doom
Brushing aside a pitchfork wielding peasant
Never releasing their grasp until their prey is dead
Carrying an ancient shield of petrified wood
Noisily opening a dusty gilt coffer of coins to count them anon
Choking a lifeless, shriveled lizard man husk
Overpowering an entire orc war party in a matter of seconds
Clawing a timeworn tapestry, depicting good deeds, to shreds
Overseeing a barrow expansion by a spade-handed golem
Clutching a rune-scribed funerary tablet tightly to its chest
Patrolling in an unceasing spiral, spanning miles
Commanding several skeletal serfs, buried alive at their death
Perpetually scowling, unaware of their lifeless state
Conspicuously creaking with taut, ashen skin over dry bones
Preserving a long-lost language as the last fluent speaker
Defending stalwartly, the only entrance/exit to their crypt
Preying upon a clan of kobolds, withered bodies in their wake
Desiccating a veteran before your eyes with a single touch
Protecting an unholy relic - the barbed hand
Devouring fear from the face of a frantic friar
Recoiling from a piously presented holy symbol
Digging through meaningless funerary offerings in frustration
Repudiating the ravages of time by smashing hourglasses
Disregarding what shouldve been a telling blow from an axe
Ripping and tearing at the blessed shroud that adorns them
Dragging a stone sledge across the floor, ceaselessly
Ruthlessly suffocating a gnome
Drawn skin covered from head to toe in spidery tattoos
Scorning their progeny - a now undead adventuring party
Emitting an eerie pale purple miasma from open wounds
Scraping a stinking bear hide with stone tools
Employing an unstrung crossbow, that somehow still fires
Scratching grimy fingernails across a slate mosaic
Escorting a zombie borne litter, carrying the corpse of their mate
Securing fealty from a recently risen pack of ghouls
Eternally atoning for crimes in life, will not strike first
Seething with resentment at anything with a beating heart
Exhaling a fetid green fog with each stilted step
Seizing a thief by the neck
Exhuming a neighboring barrow to settle an old score
Severing the arm of an impertinent thoul
Fanatically squeezing the throat of a were-rat
Shaking with perpetual unrequited rage
Festering with wriggling undead maggots
Shambling zombie servants attend their every need
Flinching slightly as they pass a statue of a saint
Shielding empty eye sockets from unexpected candlelight
Flouting at an insufficiently faithful acolyte
Shrinking away from a splash of holy water
Gasping for breath, a shriveling hobgoblin shudders at their feet
Shrugging off a spear point, impaling their torso
Giving off a strangely pleasing sandalwood and cedar scent
Shuffling across rubble strewn floors, following a minor cave-in
Glaring emotionlessly into an empty offering bowl
Slitting an ogre's throat - in life they were an accomplished assassin
Glowering with glowing yellow eyes
Strangling a gnoll in search of easy pickings
Grasping with blackened, charred fingertips, bones protruding
Stumbling gait, caused by a body draped in iron chains
Grimly grinning as a wizard wanes at their touch
Sundering a dwarf's helm with a potent hammer strike
Guarding an urn containing the ashes of a berserker chieftain
Swiftly donning rusty but still serviceable mail
Guiding dervish descendants to a place of pilgrimage
Taunting their "children" cruelly
Haunting deserted hallways, footfalls have worn the stone
Terrorizing a once flourishing town on nights with a new moon
Hesitating as a paladin brandishes a glowing spear
Throttling a halfling hero, not long for this world
Hollowly howling with rage on an hourly basis
Unchaining ghoul hounds to cull the corridors
Hurtling with unnatural alacrity after a goblin miner
Unsealing the tomb of their master - a scheming spectre
Ignoring a mighty strike from a fighter's two-handed sword
Violently mauling a merchant
Inspecting alcoves where guards once stood, now only piles of dust
Wearing ceremonial paraphernalia of a long-forgotten religion
Investigating a shrill sound from startled shriekers
Wielding pitted iron blades of ancient manufacture
Knocking over a massive pyramid of skulls, out of anger
Wilting one of the few visitors to their domain - a lost rat
Lacerating love letters penned on virgin vellum
Wincing from a sudden burst of sunlight
Lashing a group of starving ghouls savagely with a whip
Withdrawing to their hastily hewn throne to brood
Lecturing bound sacrifices on their duties to come after death
Withering under the ravages of time with protruding bone

Table: wolf, dire
Alerting their goblin handlers to an intruder
Outsmarting an ogre, tripping them and stealing their club
Ambushing a warhorse, left to graze
Overwhelming a lone chamois, ripping it to utter shreds
Approaching peak pack size, will splinter off soon
Plunging dagger-like fans into the neck of a noble
Assembling to form a great moot to discuss a coming war
Preying on encamped nomads, one a night
Attacking a gnome village with sadistic glee
Pursuing a fiery quarry for sport - a lone hellhound
Baying frightfully, sends shivers up spines for miles
Raiding the home of an elderly woman
Blooding a mastodon
Ransacking an overturned butcher's cart
Bounding across a shallow stream, splashing and spraying
Reconnoitering a new route with goblin scout riders
Bristling backs as they square off, a challenge to the alpha
Rending their claws on a defenseless dryad's tree
Broadly observing the rituals of a goblin shaman
Roving unattended, their goblins killed by adventurers
Chewing on once sturdy tent-poles to file ever-growing fangs
Rushing towards a drinking rock baboon
Clawing at uncomfortable boar-leather collars
Salivating uncontrollably at the sight of a spitted boar
Consuming what may have once been some kind of camel
Savaging a centaur warrior, out on her own
Crippling a giant stag with a ferocious bite to the back leg
Scarfing down all traces of a slain goblin warrior
Darting from shadowy cover, black fur blending completely
Scolding the goblin king, who bows his head in shame
Devouring mold-ridden meat, flung by their goblin allies
Seizing a giant tuatara by the neck
Disobeying their "masters," attacking an orc envoy
Shaking the life from a flailing berserker
Dragging the carcass of a hunter back to their den
Skulking and moody, banished from their pack
Drooling from a distance at a giant crocodile kill
Slaughtering a unicorn triumphantly, but not without cost
Eating a disgusting feast - three zombies
Slavering as they gnaw on an elf skull
Eliminating a bodyguard to the king, excessive with the lash
Smelling the air for signs of easy prey
Emaciated from a lack of suitably sized game
Snarling at each other, asserting the pack's pecking order
Encircling a band of elf warriors, with fangs ablaze
Sneaking with surprising stealth for their size, silent paw-falls
Evading a determined ranger, high prices on their pelts
Sneering after being barked at by their goblin minder
Eyeing some penned swine hungrily
Snorting with derision as they lift a leg on a treant
Flushing out a forester, more for sport than food
Sprinting after a fleeing prisoner destined for their supper
Following nervous elk herds
Spying on hobgoblin troop movements
Frothing and foaming at the mouth, likely rabid
Staring from the darkness with glowing green eyes
Gnashing their teeth under a barbed goblin whip
Startling a scourge of stirges
Grabbing a fighter's spear with their teeth, disarming her
Starving after days in a deep pit trap
Grimacing as they chew on a gamey ghoul flesh
Straining against crude harnesses of a goblin merchant's cart
Guarding the entrance to an underground goblin redoubt
Strangling an elk, by clamping down on their carotid
Harrying a herd of antelope
Strolling confidently through an abandoned camp
Howling in a blood-curdling cacophony
Swallowing huge chunks of a butchered giant catfish
Infested with bloated ticks the size of copper coins
Tearing towards a town, easy pickings on their mind
Inhabiting an abandoned crypt, to shelter from the elements
Thieving a meal from a sleeping hill giant's campfire
Intimidating their goblin minders, just for grins
Threatening a goblin bodyguard with barred fangs
Invading kobold held territory, cautious of snares and traps
Toying with a giant toad
Joining forces with a local tribe of werewolves
Trailing behind their goblin trainers
Killing a ranchers cows for pleasure, not food
Treeing a frightened friar
Leaping into a battle between bandits and goblins
Trotting in time to goblin drums
Leering at a jumpy trader, selling arms to their masters
Underestimating an elephant's fury
Lunging fiercely, but held back by crude iron chains
Unleashing their fury and frustration on each other
Lurking with the ravens on a now still battlefield
Venturing into a barrow to receive orders from a profane altar
Marauding with their mounted goblin riders
Wandering dangerously close to a cockatrice's nest
Menacing a medium and his charmed lizard man guard
Waylaying a band of brigands bivouacking
Narrowing their eyes at proffered table scraps
Weaning a litter of clumsy, but ferocious pups
Ogling the same captivating she wolf
Wounding a paladin's warhorse after an ill-timed charge
Ousting a pack-member, lamed by an owlbear
Yanking along a chain of prisoners from a local settlement
Outmaneuvering a pack of gnolls hunting a moose
Yelping in pain, being tormented by invisible sprites

Table: wolf
Absconding with a halfling's roasting seventh breakfast
Journeying to rendezvous with the rest of the pack
Agitating a squirrel, safe in the treetops
Jumping at a slab of meat, hanging from a branch
Arriving at the scene of a recent cougar kill confidently
Keening with forlorn anguish at the death of an alpha
Avoiding the scent of man on strung fladry
Licking their young to clean blood from their fur
Banishing a rowdy male from the pack
Limping from a rather brutal leg wound from a tapper's snare
Barring brutal, bloodstained fangs at an interloper
Listening intently with heads cocked to a distant yowl
Bickering over the choicest organ meats of a dead deer
Loping lazily behind a wounded bear
Biting their ranger companion playfully on the shins
Marking trees and boulders to delineate territory
Bolting down a juicy frog
Mushing in tandem, pulling a nomad's sledge
Braving civilization to sift through a trash heap
Obeying courteous commands from a druid
Burrowing into a disused badger den
Occupying an abandoned shrine to a sea goddess
Burying a marrow-filled femur for later
Organizing around a small flock of nesting grouse
Cavorting among heavenly scented grasses and flowers
Outnumbering a plump trader, slavering and snarling
Chasing an exhausted antelope
Overtaking a bounding pronghorn
Circling a bleating goat
Pacing in front of their cave, an ogre's moved in
Clambering up a rocky face to survey the area
Panicking a flock of pheasants
Cornering a crimson cloaked lass
Panting with their long tongues protruding
Coursing a bounding hare
Pilfering the leg bone of a skeleton shield-bearer
Cowering in submission from a massive alpha wolf
Pouncing on a marmot
Creeping quietly upon a flock of geese
Protecting a wounded packmate from an angry stag
Crossbred with blink dogs, in ages past
Providing food for a nursing mother
Crouching in the underbrush as a merchant caravan passes
Prowling outside a roadside tavern
Crying mournfully to commemorate a beautiful moon
Raising hackles at a rival male seeking a mate
Daring each other to approach a feeding grizzly's kill
Roaming far and wide, following the herds
Denning near nomadic centaurs, habituated but still shy
Scampering away to draw a brown bear from her kill
Digging into a rotten log, after a large snake
Scavenging with the ravens on a shredded, dead ox
Echoing distant howls from fellow pack members
Scenting a familiar fragrance - their alpha, a werewolf
Eking out an existence, subsisting mostly on meager mice
Scrambling up a rocky scree to a clandestine den
Eluding a determined huntsman
Serenading all listeners with their primal chorus of howls
Emerging from a dark den, a half-dozen pups in tow
Shedding shaggy coats, still quite thick in patches
Enticed by the constant clucking from a halfling henhouse
Slinking away, tails between legs, after a stronger pack moved in
Exacerbating a local famine by surplus killing sheep
Snapping their powerful jaws at passing butterflies
Famished from sparse prey, lanky and desperate
Snatching bits of flesh from a giant hawk's kill
Fishing in a river, retrieving squirming salmon
Sniffing fresh spoor and tracks
Fleeing after inadvertently disturbing a manticore's meal
Springing on a groundhog
Furiously scratching at their fleas
Stalking a family of beaver
Gamboling in mated pairs as the weather begins to turn
Stealing a rabbit kill from an exasperated eagle
Ganging up on an emaciated moose
Tracking human quarry, having acquired a taste for man flesh
Gently encouraging weaned pups to eat a grouse
Tugging a trapped leg fruitlessly
Gnawing on the bones of a boar
Upsetting a cyclops by stealing his sheep
Gorging themselves silly after stealing a kill from a bobcat
Vanishing in dense and thorny undergrowth
Growling low at a coiled cobra
Vilified by local villagers, who have posted a bounty
Hesitating at the flick of a skunk's tail
Visiting a kindly witch that sometimes feeds them
Hobbling a horse, following its trail lazily for it to tire
Vying for position within the pack's pecking order
Hounding a hart, hoping for an uncomplicated hunt
Waiting patiently for the designated hunters to return
Howling, staggered at first, then joining together
Waking up anyone sleeping with piercing shrieks
Huffing after nosing into an anthill
Whimpering and wet, after inadvertently falling in a stream
Hunting pigs, sent to forage for acorns by local farmers
Whining as they dig at the roots of a tree
Injuring an already infirm bison
Widening a burrow, dirt flying
Isolating an individual reindeer from a bustling herd
Yielding a downed deer to an opportunistic tiger

Table: wraith
Appearing to deliberately pace into and out of a solid wall
Keening a dreadful wail, seems to grow louder longer you listen
Avenging her death by harrowing an entire family line
Leering at an oblivious lizard man whose scales won't protect
Beckoning a bugbear with an extremely long, bony finger
Limping from an injury in life and to catch prey unawares
Billowing from beneath a doorway, rising like smoke
Lingering near a neatly swept ossuary, recent offering of flowers
Blowing out candles/torches with a frigid and penetrating fog
Lurking inside a vial labeled "healing" in common
Brooding wistfully as they stare at a faded and ripped painting
Manifesting with a black, barbed crown atop a sneering skull
Chasing after a tomb robber who dared to disturb their rest
Menacing a minotaur after dying of dehydration in their mazes
Chuckling with hollow, humorless thumps
Moaning constantly about their long-lost dryad lover
Clinging to a spectral corn dolly/children's toy
Mocking a monk, trembling as he holds his holy symbol aloft
Crumbling ghostly bread, trying to feed nonexistent pigeons
Muttering blasphemous litanies that cause ears to ooze with wax
Desecrating a sun shrine by cloaking it in perpetual twilight
Noisily stumbling in a chain strewn room, briefly corporeal
Devouring sweat-soaked fear of a fighter with a silver spear
Overseeing the removal of their bones by loyal cultists
Dictating rambling and insane demands to skeleton servitors
Patrolling the outskirts of a hidden necropolis
Dimming from view as an acolyte mutters her name
Perceptibly chilling air, breath can be seen, rime lines surfaces
Dissolving into a tattered tapestry depicting their loveless marriage
Preaching hateful doctrines to zombies with rapt expressions
Draining vitality from a vagabond, just looking for a place to sleep
Prowling edges of a forgotten grave marker, faded with moss
Drifting across a deep pit, bottom lined with elf bones
Pulsing malevolently as he circles a brazier of acrid, unholy incense
Dwelling within a grinning dwarf skull when undisturbed
Pursuing a prospector who accidentally scattered his remains
Enfeebling a prisoner, here as punishment for bogus crimes
Quavering slightly as they forget they dont need to use a door
Eradicating all life within an ever-expanding radius
Reappearing like clockwork when word "gold" is spoken aloud
Facing a dusty mirror, perpetually brushing long-white hair
Repeating mundane actions undertook in life - taking tea now
Fading in/out as they rock back/forth near an empty fireplace
Reproaching one of their spawn for letting a survivor escape
Fettered to a tarnished candelabra, does not dare leave it for long
Residing in the same cauldron in which they were boiled to death
Filling the area with blood-curdling cries of agony
Revisiting their crumbling bones for the fourth time today
Flickering like a sickly candle, as they pass a statue of a saint
Rising from the corpse of a withered veteran, freshly unborn
Flitting frantically shelf to shelf, looking for a nonexistent book
Roaming a corridor lined with cells, rattling a tin cup on the bars
Floating high within a vaulted ceiling, slaying bats with morbid glee
Sapping the life from a twitching snake
Flying low, skimming the floor, startling spiders and carrion beetles
Scheming to escape, must slay a dwarf to replace him first
Frightening a bandit by turning kindly face into a horrific visage
Seated upon a crudely carved throne, pondering eternity
Frosting a silver lidded crystal jar that they have become trapped in
Seemingly covered with oozing, gruesome wounds
Galloping atop a translucent steed - ribs poking out and frothing
Seizing a shield bearer by the nape
Gibbering uncontrollably in a mixture of harpy and elf
Shimmering as if covered in powdered glass, died from drowning
Glaring at the contorted corpse of a kobold, awaiting its rise
Shrieking a macabre parody of the song sang in life - former harpy
Glimmering faintly against a backdrop of darkness
Shrinking from a sudden splash of holy water, flung by a gnome
Gloating to their "subjects" - a desiccated pile of dead rats
Shrouding surfaces they float near in a thin layer of jagged frost
Grieving near a silver urn that burns his claws with every caress
Smiling ruefully as a ranger gasps for air in their grasp
Grinning maniacally as a cleric cowers in terror
Starving for the taste of fear, spiders and scorpions will no longer do
Guarding a treasure chest containing only a cameo of their wife
Taunting a priest who tried to turn her by haunting his family crypt
Hanging on every word from the wight of a famous playwright
Terrifying a troop of troglodytes after draining their leader
Harrowing a halfling pipeweed merchant by possessing his pipe
Tormenting a bard by taking the form of their lost love
Haunting the site where an elf slayed him, especially angry at them
Torturing themselves by drifting in and out of a beam of sunlight
Hiding within nondescript canopic jars, shoved in a crypt niche
Uncontrollably shivering, fingers blackened from a frostbitten death
Horrifyingly hungry, slurping spectral marrow from own bones
Veering suddenly after hearing nearby breathing
Hovering over cooling corpse of a gnoll, craving ensuing company
Vouchsafing passage to those who show due deference in hobgoblin
Howling silently with a grimace at a paladin with a silver sword
Warning all trespassers of deadly touch/uncontrollable urge to kill
Hunting a lineage to extinction, interested in recruiting help
Wavering like a bonfire on a windy day, glowering at a statue
Inhabiting an inlaid silver circle, hollow promises to liberators
Whimpering in a soft voice, hoping to draw in unsuspecting prey
Initiating a waithspawn teaching to feed on former friends
Whispering forbidden secrets into the ear of a studying wizard
Instantly materializing as a medium rings a big bronze gong
Withering a warhorse with a single cold caress
Joining with an evil necromancer, until they smell weakness
Wringing the neck of a berserker chieftain, come to pay homage

Table: wyvern
Ascending laboriously on somewhat tattered wings
Leaping onto the back of a titanothere, stinging repeatedly
Attacking a herd of mountain goats, clinging to the cliffside
Lumbering through undergrowth after a giant snake
Basking languorously in a light rain, craning their neck
Lunging at an illusory deer, that pops like a bubble
Bowing deeply to a female a complex courtship ritual
Marauding through a local hamlet, feasting on villagers
Braving a volley of elf arrows to snatch a fleeing horse
Noisily devouring what may have once been a moose
Brooding atop a mound of unfortunately petrified eggs
Nudging their clutch gently, turning them for even heat
Catching a sudden warm updraft and taking flight
Ostentatiously hissing as they awkwardly strut on stubby legs
Chewing on a crossbow quarrel wedged in her flank
Overpowering a pteranodon, easily
Circling over a sputtering campfire, looking for easy pickings
Peering around a craggy corner at a merchant caravan
Clawing deep into thick turf to land, gouging the ground
Perching atop a crenelated castle ruin
Clumsily clambering down a slope after a bleating sheep
Picking off pilgrims in a procession to a shrine atop a peak
Consuming hair, skin, and bones from a desiccated deer
Piercing a convulsing owl bear again for good measure
Covered in painful thorn growths after angering a druid
Pinning a noble down with her massive clawed foot
Crashing through a high canopy, as their prey takes cover
Playfully chasing its own venom-dripping, tail
Cresting an enormous butte to survey their surroundings
Pouncing on a trader, a brave mule charges into action
Crouching slightly to make their way into an old bear den
Protecting their dying mate, nearly torn in twain by a roc
Derisively snorting in chains at hobgoblin table scraps
Pursuing a flock of palomino pegasi
Descending after spotting a herd of cattle
Quelling a squabble between juveniles, almost ready to fledge
Diving suddenly, craws ready to grasp a tasty centaur
Rampaging at a toll bridge, near gnomes hiding under a cart
Dogfighting males duel with their stings
Rearing back to let out a blood-curdling shriek
Dripping venom from its swaying stinger as it screams
Recoiling from a blast of lightning from a wizard's finger
Dropping boulders on a loudly cursing dwarf mining camp
Regurgitating bugbear bits to feed its chicks
Dwelling comfortably atop an abandoned keep
Rending thick tree bark to hone his claws
Eating a humongous jack rabbit, easily the size of a dog
Retreating from a mated pair of manticores
Emerging from thick stand of pines, unfurling leathery wings
Returning to her birth nest to challenge her mother for it
Emitting the foul, semi-sweet stench of rotten roses
Roaring to intimidate a knight in shiny plate
Feeding chirping nestlings strips of hobgoblin
Rolling over a boulder, relishing the crashing sounds as it falls
Flapping furiously against a sudden gale
Sailing lazily on thermals, flapping only every few minutes
Flashing pale white mouths as a territorial challenge
Screeching after discovering an egg eating giant snake
Fleeing from an impressive shadow overhead - red dragon
Scuttling gawkily on the ground with a wounded left wing
Flexing their limbs and stretching, not unlike a feline
Seizing a dangling scout as they rappel down a cliff
Flying low, scaled belly brushing against scraggly bushes
Slaying a medium with a swift stab of their stinger
Following a herd of elk, scanning for the old or infirm
Snapping at their troglodyte trainer
Furiously flinging the ghoul in their jaws at its packmates
Snarling after scenting chimera on the wind
Gnawing on an ogre's skull to help shed and sharpen teeth
Sniffing at giant tracks, hoping to poach their livestock
Gorging on a joint of mutton tossed by an orc chieftain rider
Soaring among the clouds, so as not to spook antelope below
Grabbing a goblin in his jaws, as others move in with spears
Splashing in a shallow lake, wrestling a wriggling giant fish
Grunting as a horn helmed ranger scratches her chin
Spreading wet wings to dry them in the sun
Guarding a crumbling sorcerer's tower and charmed
Stinging a hippogriff mare mid-air, she begins to plummet
Gulping down stew from a halfling camp's cauldron, all fled
Stretching their scaley skin to shake off the remains of a molt
Heading towards a massive flock of geese to dine on the wing
Struggling with the barding of a warhorse slain on a battlefield
Helping hatchlings escape their shells with careful nibbles
Stubbornly clinging to the bottom of a bridge over a ravine
Howling after flying into a carefully strung net trap
Swallowing huge gulps of brackish pond water
Hunting white apes near a washed-out wadi
Swooping as a farmer herds sheep into a barn
Impaling a snarling wolf with her sting
Threatening a hill giant with rattling scales as a warning
Ineffectively scourging a gargoyle with his tail
Tracking a bleeding rhino, landing to smell a pool of blood
Jabbing stone spears, lizard men are losing the fight
Utterly savaging a smaller rival near a bubbling mud geyser
Kidnapping a kobold king from an escort
Viciously biting a brigand's sword-arm clean off
Lashing their venomous tail to-and-fro
Violently coughing up bits of indigestible metal armor
Launching themselves with abandon from a craggy precipice
Whisking away a warrior as a gift for his witch mistress

Table: zombie
Able to self-amputate hands, which crawl along...hungry
Grasping through the iron bars of a crude, creaking cage
Attracting hungry robber flies
Groaning audibly as they lurch toward light
Bashing an oil beetle with heavy stones
Guarding a stone font filled with the bodies of birds and toads
Bearing splash scars from holy water
Hacking through all barriers with rusty axes
Belching forth putrid and rank corpse miasma
Hauling a sledge piled high with crates
Brandishing the severed arm of a berserker
Hissing loudly at a light source
Burying their terrified victims alive
Led by an emaciated child mummy, a cruel princeling tyrant
Chained together by long iron links
Limping after losing a leg to a draco lizard
Chasing an adventuring party after killing their cleric
Loitering at the edge of consecrated ground
Chewing through coffin lids
Marching lockstep under the orders of a necromancer
Circling methodically on the outskirts of a sanctified sigil
Meandering around a magnificent sarcophagus
Clad in antique chain armor - each link is heart-shaped
Moaning as their rotting flesh is devoured by green slime
Clawing at a sealed stone door in frustration
Mocking the living by holding a morbid birthday party
Climbing awkwardly out of a spiked pit
Oblivious to the bats that buffet them from above
Clumsily constructing a pile of furniture to reach a window
Oozing with vile, pungent corpse liquor
Clutching unholy symbols tightly in their fists
Pantomiming half-remembered daily routines
Compelled to prevent anything from entering a chamber
Patrolling a long stretch of sites, this is the fourth stop of ten
Concealing plate armor underneath their heavy robes
Pounding on a portcullis with shattered stubs
Confounding a carcass crawler
Protecting their master, an inexperienced magic-user
Coughing up tattered and moldy strips of cloth
Pulsating with pale, greasy maggots that periodically peak out
Cowering from a pious priest, intoning prayer
Quietly disemboweling a cow, occasional lip smacking
Crawling across the ground, legs lost to decay
Raking their claws across walls as they walk
Creaking with age as bone rubs on bone
Rasping at a wall, a frightened footpad hangs precariously
Croaking a mockery of a greeting, only words they speak
Reattaching lost limbs by dipping them in profane tar
Decaying rapidly, will soon be skeletons
Recoiling from an initiate, reading from a scroll of protection
Devouring a defenseless dervish, whose quest ends here
Rising from forbidden eternal rest after hearing a sound
Digging themselves out of shallow graves
Scooping grey matter out of a cracked skull with grimy claws
Disguised as scarecrows, have been terrorizing a village
Scrabbling at the armor of a deceased hobgoblin
Disinterring a buried body to help boost their number
Scraping last bits of organs from under their grisly fingernails
Dismembering the noisiest member, covered in bells
Scratching at a doorknob, unable to turn it
Doused thick in astringent lamp oil
Seizing a maiden, who tripped on her flowing gown
Dragging a disarmed dwarf to an altar
Setting a table with disgusting dishes of entrails
Dressed as jesters as part of some unfunny joke
Shambling randomly, bumping into things, eyes long gone
Dutifully following instructions from acolytes
Shoving each other as they try to grab a hiding halfling
Eating the leftovers cast off by a ravenous ghoul
Shuffling slowly away from the sound of maniacal laughter
Emitting a mephitic stench, would make a goblin wretch
Silently saluting as their undead general inspects his troops
Enchanted with unnatural speed and cunning
Snacking on rats, the ones to slow to escape their grasp
Engorged with rancid blood, bursting if pierced
Spitting up a milky green fluid that reeks of death
Enveloped by thick clouds of flesh-hungry gnats
Sputtering an unintelligible warning, tongues long decayed
Equipped with surprisingly shiny gear and weapons
Squabbling over the brains of a studious medium
Festering with disease - carriers of the weeping plague
Squeezing a vulture that mistook them for carrion
Filing past a black clad cultist, receiving dark communion
Stomping to the sound of muffled drums
Flailing about, one with an arm afire
Surrounding a veteran, her spear shaft just snapped
Flinging themselves futilely against a locked door
Swaying rhythmically to unhallowed hymns
Floating listless in a gelatinous cube
Throwing decorative polearms to the floor prior to charging
Following the scent of the living like hungry wolves
Traipsing round a hanging tree, hanged men begin to twitch
Genuflecting to a more powerful wight
Unusually, they are all gnomes that clamber up taller prey
Girded with a blasphemous charm that heats holy symbols
Water-logged and bloated with aquatic worms
Gnawing on a gnoll's furry leg
Wearing their church day best, the clothes they were buried in
Grappling with a grey ooze, searing their rancid flesh
Writhing under their feculent skin are nests of centipedes

Table: lycanthrope, devil swine
With atrocious table manners, gesticulating wildly with chicken leg
Wearing, peeking out from collar, a necklace looking like human teeth
With beady eyes, deep-set in a plump face but oddly compelling
Of a pot-bellied and portly build, with rheumy, bloodshot eyes
With a constantly running, turned up nose centered in a round face
With precious rings on fat fingers, squeezing and bulging
Whose corpulent belly quakes with incessant, wheezing laughter
With sharp, needle like teeth and narrow, grinning lips
With a seemingly countless number of bulging chins
With a somewhat unsettling lack of eyebrows/semi-translucent skin
Whose greasy, fine hair distracts on a rip pling chin
With spidery capillaries adorning an extremely large and wide nose
Of incredible girth, one can't help but feel sorry for belt-maker
Squealing excitedly while pouring a goblet of rich, red claret
With jowls that jiggle and dance with every word
Stinking of over-applied perfumes, barely masks bad body odor
Guffawing and chortling noisily, punctuated with loud snorts
With stubby, short limbs and unnaturally tiny, very pointy shoes
In once fine clothing, covered in questionable stains
With swollen but nimble hands at the end of bulgy, joggling arms

Table: lycanthrope, werebear
Absent-mindedly scratching themselves, groans of pleasure
With a judgmental gaze from very large, bronze-colored eyes
Of a burly and muscular build, a mop of hair matted with twigs
Whose large, jagged scar mars an otherwise kindly face
With calloused, constantly dirty hands and a slight sunburn
With massive hands, missing a pinky, ogre/giant blood?
Whose coarse hair sprouts from rather muscular arms
Whose once fine boots have seen better days, toes blown out
Whose deep, hearty belly laughs can be heard some distance away
With a persistent smell of woodsmoke and pine
Whose ears would be nondescript were they not set so high on the head
With slightly distracting, full but berry-stained lips
Whose facial hair only seems to accentuate puffy cheeks
Appearing sturdily built, with a purposefully limp handshake so as not to hurt
With grimier fingernails than youve ever seen
Whose tattered, hand-me-down clothes have seen several crude repairs
Whose handshake is slightly sticky, like spilt, dried honey
With an unsteady gait, seems almost top heavy or unbalanced
For whom hirsute would be an understatement
With very bushy eyebrows over a pronounced brow ridge

Table: lycanthrope, wereboar
Always turning to face whoever is talking
With lower canines visibly poke out, claims orc blood on mother's side
With a broad, toothy grin that almost stretches from eye to eye
With deep red wine stains down their front, a messy drinker
Seeming choleric - seems to take almost anything as a personal affront
Being more than a bit brusque and curt
With a confident swagger, always puts a slightly grim spin on things
With nostrils flaring, almost unceasingly
Distinct lack of neck, or at least a very wide and sinewy one
Whose powerful, broad shoulders make for an imposing torso
With eyes set just a tad too far apart
With a profusion of bristly whiskers, almost like a shaving brush
Habitually whittling sticks to sharpened points as they speak
Regularly stomping and shuffling their feet impatiently
Haughtily snorting and seeming to size everyone up immediately
With rich black mud caking their legs, almost up to their knees
With head constantly bowed, somehow still manages to meet your eye
Sensitive about their almost comical proportions - very short legs
Eating an entire apple, core and all in a few sloppy bites
With a slightly hunched back, thickset

Table: lycanthrope, wererat
Always furtively searching for the exit from any given area
With, if the light hits it right, a long white hair sprouting from forehead
Appearing to be itchy, longish nails leave red lines on bare arms
Incessantly fidgeting, won't/can't be still
With contagious, squealing, and nearly always inappropriate mirth
Appearing incredibly lanky and thin, with long, delicate fingers
Delicately unwrapping a pungent cheese with delectation
Seeming a little bit bowlegged, gives them a "skip" to their gait
With a dirty handkerchief wiping flecks of saliva from sides of grin
With large, surprisingly pearly and prominently gapped buckteeth
Appearing disheveled with an unruly cowlick, constantly try to smooth down
Appearing piebald, due to vitiligo
With distinctive way to eat a slice of bread, nibbling on the edges first
Molting, accompanied by a stringent ozone-like smell
With ears slightly sharp, but none of the other signs of elf-blood
Nesting in a pit, replete with large iron spikes to sup on
With a pointy face, which the long knife-like nose in the center accentuates
Nibbling on a heavily pitted anvil
With their fist ever-clasped tightly around the hilt of a dagger or knife
Observing ghouls as they open a coffin with armored corpse inside

Table: lycanthrope, weretiger
With a very regal bearing, comports themselves in a noble fashion
Whose low and deep laughs go unnoticed unless you listen carefully
With abundant dark freckles, mostly dusting the tops of cheeks
With measured, calculated movements, unerringly swatting a fly
With a bafflingly ambiguous grin, impossible to read their feelings
With the most penetrating green-eyed gaze you've ever seen
Constantly cracking their knuckles/glancing fondly at their fingers
With nostrils angled upward, giving them an arrogant seeming
With a countenance graced with enigmatic, indecipherable expression
Giving periodic, full-bodied yawns/stretches seem highly contagious
With disconcerting/unblinking/ice-blue eyes contrast warm demeanor
Appearing ever read to pounce, perpetually tense or tightly wound
Fastidiously grooming and always brushing their hair
Staring right through you, sending shivers down spines
Gently exuding an undeniable and powerful air of strength
With a striking white forelock on otherwise auburn tresses
With imposing, but with oddly silent, footfalls
Tapping impatiently with flawlessly manicured nails
Lithe and sleek, moving sinuously
Wryly smiling, even in situations most grim or serious

Table: lycanthrope, werewolf
With a sauntering, almost swaggering stride
With hands always seem clenched or in pockets
Being very apologetic, every action tinged with some sort of forlorn regret
Whose laughter comes out a bit like a moan or wail
With bloodshot eyes, appearing a little haggard as if lacking sleep
Looking in askance for whos in charge, testing their authority
Who bluntly refuses to deal in silver coins
Whose meat they're eating is woefully undercooked
With bushy, angled eyebrows meet just above bridge of their nose
With notably odd hands - index fingers much longer than the middle
Cocking their head periodically, as if hearing sounds just out of earshot
Panting slightly, almost as if out of breath or excited
Who domesticated animals certainly don't seem to like very much
Perturbed by smell of something, wrinkling nose uncontrollably
Barking orders to everyone around them
Who seems to possess a surplus of thick hair, both on their head and body
Whose fingernails have gone untrimmed for far-too long
Being surprisingly swift in movements with measured actions
Whose hairline forms a perfect widow's peak
With a suggestion of shyness, even loneliness in the way they speak
"""

# These names match wamd_data names.
ose_monsters = [
    'ape, white', 'basilisk', 'bat', 'bat, giant', 'bat, giant vampire', 'bear, black', 'bear, cave',
    'bear, grizzly', 'bear, polar', 'beetle, fire', 'beetle, oil', 'beetle, tiger', 'black pudding',
    'blink dog', 'boar', 'bugbear', 'caecilia', 'camel', 'carcass crawler', 'cat, great (lion)',
    'cat, great (mountain lion)', 'cat, great (panther)', 'cat, great (sabre-tooth tiger)',
    'cat, great (tiger)', 'cave locust', 'centaur', 'centipede, giant', 'chimera', 'cockatrice',
    'crab, giant', 'crocodile', 'crocodile, giant', 'crocodile, large', 'cyclops', 'djinni (lesser)',
    'doppelganger', 'dragon turtle', 'driver ant', 'dryad', 'dwarf', 'efreeti (lesser)',
    'elemental, air', 'elemental, earth', 'elemental, fire', 'elemental, water', 'elephant', 'elf',
    'ferret, giant', 'fish, giant (bass)', 'fish, giant (catfish)', 'fish, giant (piranha)',
    'fish, giant (rockfish)', 'fish, giant (sturgeon)', 'gargoyle', 'gelatinous cube', 'ghoul',
    'giant, cloud', 'giant, fire', 'giant, frost', 'giant, hill', 'giant, stone', 'giant, storm',
    'gnoll', 'gnome', 'goblin', 'golem, amber', 'golem, bone', 'golem, bronze', 'golem, wood', 'gorgon',
    'green slime', 'grey ooze', 'griffon', 'halfling', 'harpy', 'hawk', 'hawk, giant', 'hellhound',
    'herd animal, large', 'herd animal, medium', 'herd animal, small', 'hippogriff', 'hobgoblin',
    'horse, draft', 'horse, riding', 'horse, war', 'horse, wild', 'human, acolyte', 'human, bandit',
    'human, berserker', 'human, brigand', 'human, buccaneer', 'human, dervish', 'human, medium',
    'human, merchant', 'human, neanderthal', 'human, noble', 'human, nomad', 'human, pirate',
    'human, trader', 'human, veteran', 'human, villager', 'hydra', 'insect swarm, creeping',
    'insect swarm, creeping and flying', 'insect swarm, flying', 'invisible stalker', 'killer bee',
    'kobold', 'leech, giant', 'living statue, crystal', 'living statue, iron', 'living statue, rock',
    'lizard man', 'lizard, giant (draco)', 'lizard, giant (gecko)', 'lizard, giant (horned chameleon)',
    'lizard, giant (tuatara)', 'lycanthrope, devil swine', 'lycanthrope, werebear', 'lycanthrope, wereboar',
    'lycanthrope, wererat', 'lycanthrope, weretiger', 'lycanthrope, werewolf', 'manticore', 'mastodon',
    'medusa', 'merman', 'minotaur', 'mule', 'mummy', 'nixie', 'ochre jelly', 'octopus, giant', 'ogre',
    'orc', 'owl bear', 'pegasus', 'pixie', 'pteranodon', 'pterodactyl', 'purple worm', 'rat', 'rat, dire',
    'rhagodessa', 'rhinoceros', 'rhinoceros, woolly', 'robber fly', 'roc, giant', 'roc, large', 'roc, small',
    'rock baboon', 'rust monster', 'salamander, flame', 'salamander, frost', 'scorpion, giant',
    'sea serpent (lesser)', 'shadow', 'shark, bull', 'shark, great white', 'shark, mako', 'shrew, giant',
    'shrieker', 'skeleton', 'snake, pit viper', 'snake, giant rattler', 'snake, rock python', 'snake, sea',
    'snake, spitting cobra', 'spectre', 'spider, giant (black widow)', 'spider, giant (crab spider)',
    'spider, giant (tarantella)', 'sprite', 'squid, giant', 'stegosaurus', 'stirge', 'thoul', 'titanothere',
    'toad, giant', 'treant', 'triceratops', 'troglodyte', 'troll', 'tyrannosaurus rex', 'unicorn',
    'vampire', 'warp beast', 'water termite (freshwater)', 'water termite (saltwater)',
    'water termite (swamp)', 'weasel, giant', 'whale, killer', 'whale, narwhal', 'whale, sperm', 'wight',
    'wolf', 'wolf, dire', 'wraith', 'wyvern', 'yellow mould', 'zombie',
    ]


class Table:
    """What are monsters doing table for one monster."""

    def __init__(self, name, rows):
        assert len(name)
        assert len(rows)
        if ',' in name:
            one, two = [x.strip() for x in name.split(',')]
            name = f'{two} {one}'
        self.name = name.capitalize()
        self.rows = rows

    def __str__(self):
        row = self.roll()
        return f'{self.name} {row[:1].lower() + row[1:]}.'

    def roll(self):
        """Roll on table."""
        return random.choice(self.rows)


def parse_tables(data):
    """Create What are monster doing tables for each monster in data."""
    tables = {}
    rows = []
    name = ''
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('Table:'):
            if name:
                tables[name] = Table(name, rows)
            name = line[6:].strip()
            rows = []
        else:
            rows.append(line)
    if name:
        tables[name] = Table(name, rows)
    return tables


tables = parse_tables(wamd_data)


@click.group()
# @click.option('-r', '--roll', default=None, type=int, help='Use this d100 roll.')
@click.pass_context
def cli(ctx):
    """Roll up BX random encounters."""
    # ctx.obj['roll'] = roll
    for monster in ose_monsters:
        print(tables[monster])


if __name__ == '__main__':
    cli(obj={})
