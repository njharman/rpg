gem_names = [
  // 10 GP Gems
    [
    "Agate: Translucent circles of gray, white, brown, blue and/or green",
    "Hematite: Gray-black",
    "Tiger Eye: Translucent rich brown with golden center under-hue",
    "Turquoise: Light blue-green"
    ],
  // 50 GP Gems
    [
    "Bloodstone: Dark gray with red flecks",
    "Carnelian: Orange to reddish brown",
    "Jasper: Blue, black to brown",
    "Moonstone: Translucent white with pale blue glow"
    ],
  // 100 GP Gems
    [
    "Amber: Transparent watery gold to rich gold",
    "Amethyst: Transparent deep purple",
    "Coral: Pinkish",
    "Jade: Translucent light green, deep green, green and white, white"
    ],
  // 500 GP Gems
    [
    "Aquamarine: Transparent pale blue green",
    "Garnet: Translucent red, brown-green, or violet",
    "Pearl: Lustrous white, yellowish, pinkish, to pure black",
    "Topaz: Transparent golden yellow"
    ],
  // 1000 GP Gems
    [
    "Diamond: Transparent clear blue-white",
    "Emerald: Transparent deep bright green",
    "Ruby: Transparent clear red to deep crimson",
    "Sapphire: Transparent clear to medium blue",
    ]
  ]

gem_sizes = ["small", "large", "huge", "enormous", "legendary"]
gem_values = [ 10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000 ]
gem_table = [ 10, 25, 75, 90, 100 ]


function treasure_gems(count, roll) {
  // say count gems of same type
  if(!roll) roll = d100;
  say("DM", count + " " + roll_gem(roll));
  }

function treasure_jewelry(roll) {
  if(!roll) roll = d100;
  var gp;
  if(roll <= 20) {
    gp = 3d6 * 100;
  } else if(roll <= 80) {
    gp = d6 * 1000;
  } else {
    gp = d10 * 1000;
    }
  say("DM", gp + "gp jewelry");
  }

function roll_gem(roll) {
  var stone = table_roll(roll, gem_table);
  var size = 0;
  while(d6 == 1) size += 1;
  size = Math.min(size, gem_sizes.length-1);
  return gem_sizes[size] + " " + gem_names[stone][d4];
  }


function table_roll(roll, table) {
  // return index of roll in table
  for(i=0;i<table.length;i++) {
    if(roll <= table[i]) return i;
    }
  }
