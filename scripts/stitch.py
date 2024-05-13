import json
import os
from PIL import Image, ImageFilter
import os.path
import errno
import glob
import numpy as np
from collections import defaultdict

version = "../out/mapgen/versions/2024-04-10_a"

with open("%s/worldMapDefinitions.json" % version) as f:
	defs = json.load(f)

defs += [
  {
    "name": "Abandoned Mine - Level 1",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 150,
        "xHigh": 53,
        "xLow": 53,
        "yLow": 150
      }
    ],
    "fileId": 10000
  },
  {
    "name": "Abandoned Mine - Level 2",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 71,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 71
      }
    ],
    "fileId": 10001
  },
  {
    "name": "Abandoned Mine - Level 3",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 70,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 70
      }
    ],
    "fileId": 10002
  },
  {
    "name": "Abandoned Mine - Level 4",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 70,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 70
      }
    ],
    "fileId": 10003
  },
  {
    "name": "Abandoned Mine - Level 5",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 69,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 69
      }
    ],
    "fileId": 10004
  },
  {
    "name": "Abandoned Mine - Level 6",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 69,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 69
      }
    ],
    "fileId": 10005
  },
  {
    "name": "Abyss",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 75
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 46,
        "xLow": 46,
        "yLow": 75
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 48,
        "xLow": 48,
        "yLow": 75
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 46,
        "xLow": 46,
        "yLow": 74
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 74
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 48,
        "xLow": 48,
        "yLow": 74
      }
    ],
    "fileId": 10006
  },
  {
    "name": "Abyssal Area",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 76,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 76
      }
    ],
    "fileId": 10007
  },
  {
    "name": "Ah Za Rhoon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 146,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 146
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 145,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 145
      }
    ],
    "fileId": 10008
  },
  {
    "name": "Air altar",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 75
      }
    ],
    "fileId": 10009
  },
  {
    "name": "Airship platform",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 1,
        "yHigh": 84,
        "xHigh": 32,
        "xLow": 32,
        "yLow": 84
      }
    ],
    "fileId": 10010
  },
  {
    "name": "Ancient Cavern (unlit)",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 83,
        "xHigh": 25,
        "xLow": 25,
        "yLow": 83
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 82,
        "xHigh": 25,
        "xLow": 25,
        "yLow": 82
      }
    ],
    "fileId": 10011
  },
  {
    "name": "Ancient Cavern lighting area",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 76,
        "xHigh": 24,
        "xLow": 24,
        "yLow": 76
      }
    ],
    "fileId": 10012
  },
  {
    "name": "Another Slice of H.A.M. Sigmund fight area",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 86,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 86
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 87,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 87
      }
    ],
    "fileId": 10013
  },
  {
    "name": "Ape Atoll Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 142,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 142
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 142,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 142
      }
    ],
    "fileId": 10014
  },
  {
    "name": "Ardougne (Song of the Elves)",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 92,
        "xHigh": 52,
        "xLow": 52,
        "yLow": 92
      }
    ],
    "fileId": 10015
  },
  {
    "name": "Ardougne Sewer (Plague City)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 152,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 152
      }
    ],
    "fileId": 10016
  },
  {
    "name": "Baba Yaga's house",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 72,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 72
      }
    ],
    "fileId": 10017
  },
  {
    "name": "Banana plantation (Ape Atoll)",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 143
      }
    ],
    "fileId": 10018
  },
  {
    "name": "Barbarian Assault",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 85,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 85
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 84,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 84
      }
    ],
    "fileId": 10019
  },
  {
    "name": "Barbarian Assault lobby",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 82,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 82
      }
    ],
    "fileId": 10020
  },
  {
    "name": "Barrows crypts",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 151,
        "xHigh": 55,
        "xLow": 55,
        "yLow": 151
      }
    ],
    "fileId": 10021
  },
  {
    "name": "Blast Furnace",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 77
      }
    ],
    "fileId": 10022
  },
  {
    "name": "Boots of lightness areas",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 152,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 152
      }
    ],
    "fileId": 10023
  },
  {
    "name": "Bouncer's Cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 73,
        "xHigh": 27,
        "xLow": 27,
        "yLow": 73
      }
    ],
    "fileId": 10024
  },
  {
    "name": "Brimhaven Agility Arena",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 149,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 149
      }
    ],
    "fileId": 10025
  },
  {
    "name": "Brine Rat Cavern",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 158,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 158
      }
    ],
    "fileId": 10026
  },
  {
    "name": "Bryophyta's lair",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 155,
        "xHigh": 50,
        "xLow": 50,
        "yLow": 155
      }
    ],
    "fileId": 10027
  },
  {
    "name": "Burthorpe Games Room",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 34,
        "xLow": 34,
        "yLow": 77
      }
    ],
    "fileId": 10028
  },
  {
    "name": "Cabin Fever boats",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 28,
        "xLow": 28,
        "yLow": 75
      }
    ],
    "fileId": 10029
  },
  {
    "name": "Cerberus's Lair",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 19,
        "xHigh": 21,
        "xLow": 21,
        "yLow": 19
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 20,
        "xHigh": 20,
        "xLow": 20,
        "yLow": 20
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 19,
        "xHigh": 19,
        "xLow": 19,
        "yLow": 19
      }
    ],
    "fileId": 10030
  },
  {
    "name": "Corporeal Beast's lair",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 66,
        "xHigh": 46,
        "xLow": 46,
        "yLow": 66
      }
    ],
    "fileId": 10031
  },
  {
    "name": "Cosmic altar",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 33,
        "xLow": 33,
        "yLow": 75
      }
    ],
    "fileId": 10032
  },
  {
    "name": "Cosmic entity's plane",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 32,
        "xLow": 32,
        "yLow": 75
      }
    ],
    "fileId": 10033
  },
  {
    "name": "Courtroom",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 66,
        "xHigh": 28,
        "xLow": 28,
        "yLow": 66
      }
    ],
    "fileId": 10034
  },
  {
    "name": "Crandor Lab",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 151,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 151
      }
    ],
    "fileId": 10035
  },
  {
    "name": "Crash Site Cavern",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 88,
        "xHigh": 32,
        "xLow": 32,
        "yLow": 88
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 88,
        "xHigh": 33,
        "xLow": 33,
        "yLow": 88
      }
    ],
    "fileId": 10036
  },
  {
    "name": "Creature Creation",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 68,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 68
      }
    ],
    "fileId": 10037
  },
  {
    "name": "Daeyalt Essence mine",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 152,
        "xHigh": 57,
        "xLow": 57,
        "yLow": 152
      }
    ],
    "fileId": 10038
  },
  {
    "name": "Death altar",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 34,
        "xLow": 34,
        "yLow": 75
      }
    ],
    "fileId": 10039
  },
  {
    "name": "Desert Eagle Lair",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 149,
        "xHigh": 53,
        "xLow": 53,
        "yLow": 149
      }
    ],
    "fileId": 10040
  },
  {
    "name": "Desert Mining Camp dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 147,
        "xHigh": 51,
        "xLow": 51,
        "yLow": 147
      }
    ],
    "fileId": 10041
  },
  {
    "name": "Digsite Dungeon (rocks blown up)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 152,
        "xHigh": 52,
        "xLow": 52,
        "yLow": 152
      }
    ],
    "fileId": 10042
  },
  {
    "name": "Digsite Dungeon (rocks intact)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 52,
        "xLow": 52,
        "yLow": 153
      }
    ],
    "fileId": 10043
  },
  {
    "name": "Dondakan's mine (during quest)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 77
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 77
      }
    ],
    "fileId": 10044
  },
  {
    "name": "Dorgesh-Kaan South Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 81,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 81
      }
    ],
    "fileId": 10045
  },
  {
    "name": "Dragon Slayer boats",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 86,
        "xHigh": 32,
        "xLow": 32,
        "yLow": 86
      }
    ],
    "fileId": 10046
  },
  {
    "name": "Dream World - challenges",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 79,
        "xHigh": 27,
        "xLow": 27,
        "yLow": 79
      }
    ],
    "fileId": 10047
  },
  {
    "name": "Dream World - Dream Mentor",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 80,
        "xHigh": 28,
        "xLow": 28,
        "yLow": 80
      }
    ],
    "fileId": 10048
  },
  {
    "name": "Dream World - Me",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 79,
        "xHigh": 28,
        "xLow": 28,
        "yLow": 79
      }
    ],
    "fileId": 10049
  },
  {
    "name": "Drill Demon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 49,
        "xLow": 49,
        "yLow": 75
      }
    ],
    "fileId": 10050
  },
  {
    "name": "Eadgar's cave",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 157,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 157
      }
    ],
    "fileId": 10051
  },
  {
    "name": "Eagles' Peak Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 3,
        "yHigh": 77,
        "xHigh": 31,
        "xLow": 31,
        "yLow": 77
      }
    ],
    "fileId": 10052
  },
  {
    "name": "Elemental Workshop",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 154
      }
    ],
    "fileId": 10053
  },
  {
    "name": "Enakhra's Temple",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 145,
        "xHigh": 48,
        "xLow": 48,
        "yLow": 145
      }
    ],
    "fileId": 10054
  },
  {
    "name": "Enchanted Valley",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 70,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 70
      }
    ],
    "fileId": 10055
  },
  {
    "name": "Enlightened Journey crash areas",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 76,
        "xHigh": 28,
        "xLow": 28,
        "yLow": 76
      }
    ],
    "fileId": 10056
  },
  {
    "name": "Evil Bob's Island",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 74
      }
    ],
    "fileId": 10057
  },
  {
    "name": "Evil Chicken's Lair",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 68,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 68
      }
    ],
    "fileId": 10058
  },
  {
    "name": "Evil Twin",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 80,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 80
      }
    ],
    "fileId": 10059
  },
  {
    "name": "Eyes of Glouphrie war cutscene",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 33,
        "xLow": 33,
        "yLow": 77
      }
    ],
    "fileId": 10060
  },
  {
    "name": "Fairy Resistance Hideout",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 69,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 69
      }
    ],
    "fileId": 10061
  },
  {
    "name": "Fisher Realm (diseased)",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 73,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 73
      }
    ],
    "fileId": 10062
  },
  {
    "name": "Fisher Realm (healthy)",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 73,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 73
      }
    ],
    "fileId": 10063
  },
  {
    "name": "Fishing Trawler",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 75
      }
    ],
    "fileId": 10064
  },
  {
    "name": "Fishing Trawler",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 75
      }
    ],
    "fileId": 10065
  },
  {
    "name": "Fishing Trawler",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 31,
        "xLow": 31,
        "yLow": 75
      }
    ],
    "fileId": 10066
  },
  {
    "name": "Fossil Island boat",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 28,
        "xLow": 28,
        "yLow": 74
      }
    ],
    "fileId": 10067
  },
  {
    "name": "Fragment of Seren fight",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 92,
        "xHigh": 51,
        "xLow": 51,
        "yLow": 92
      }
    ],
    "fileId": 10068
  },
  {
    "name": "Freaky Forester",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 74
      }
    ],
    "fileId": 10069
  },
  {
    "name": "Genie cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 145,
        "xHigh": 52,
        "xLow": 52,
        "yLow": 145
      }
    ],
    "fileId": 10070
  },
  {
    "name": "Glarial's Tomb",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 153
      }
    ],
    "fileId": 10071
  },
  {
    "name": "Goblin cook",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 46,
        "xLow": 46,
        "yLow": 154
      }
    ],
    "fileId": 10072
  },
  {
    "name": "Gorak Plane",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 83,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 83
      }
    ],
    "fileId": 10073
  },
  {
    "name": "H.A.M. Store room",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 81,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 81
      }
    ],
    "fileId": 10074
  },
  {
    "name": "Hallowed Sepulchre - Level 1",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 93,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 93
      },
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 94,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 94
      },
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 93,
        "xHigh": 34,
        "xLow": 34,
        "yLow": 93
      },
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 92,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 92
      },
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 93,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 93
      }
    ],
    "fileId": 10075
  },
  {
    "name": "Hallowed Sepulchre starting area",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 93,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 93
      }
    ],
    "fileId": 10076
  },
  {
    "name": "Harmony Island lower level",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 144,
        "xHigh": 59,
        "xLow": 59,
        "yLow": 144
      }
    ],
    "fileId": 10077
  },
  {
    "name": "Isafdar (Song of the Elves)",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 95,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 95
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 96,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 96
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 96,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 96
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 96,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 96
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 95,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 95
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 95,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 95
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 94,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 94
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 94,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 94
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 94,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 94
      }
    ],
    "fileId": 10078
  },
  {
    "name": "Jaldraocht Pyramid - Level 1",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 3,
        "yHigh": 77,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 77
      }
    ],
    "fileId": 10079
  },
  {
    "name": "Jaldraocht Pyramid - Level 2",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 77,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 77
      }
    ],
    "fileId": 10080
  },
  {
    "name": "Jaldraocht Pyramid - Level 3",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 77,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 77
      }
    ],
    "fileId": 10081
  },
  {
    "name": "Jaldraocht Pyramid - Level 4",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 145,
        "xHigh": 50,
        "xLow": 50,
        "yLow": 145
      }
    ],
    "fileId": 10082
  },
  {
    "name": "Jatizso mine",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 159,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 159
      }
    ],
    "fileId": 10083
  },
  {
    "name": "Jiggig Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 147,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 147
      },
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 146,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 146
      }
    ],
    "fileId": 10084
  },
  {
    "name": "Jungle Eagle lair/Red chinchompa hunting ground",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 145,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 145
      }
    ],
    "fileId": 10085
  },
  {
    "name": "Karamjan Temple",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 144,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 144
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 145,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 145
      }
    ],
    "fileId": 10086
  },
  {
    "name": "Keep Le Faye (instance)",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 66,
        "xHigh": 26,
        "xLow": 26,
        "yLow": 66
      }
    ],
    "fileId": 10087
  },
  {
    "name": "Keldagrim Rat Pits",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 73,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 73
      }
    ],
    "fileId": 10088
  },
  {
    "name": "Killerwatt Plane",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 81,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 81
      }
    ],
    "fileId": 10089
  },
  {
    "name": "King's Ransom dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 66,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 66
      }
    ],
    "fileId": 10090
  },
  {
    "name": "Kiss the frog",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 74
      }
    ],
    "fileId": 10091
  },
  {
    "name": "Klenter's Pyramid",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 51,
        "xLow": 51,
        "yLow": 143
      }
    ],
    "fileId": 10092
  },
  {
    "name": "Kruk's Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 141,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 141
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 144,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 144
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 144,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 144
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 143
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 143
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 143
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 142,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 142
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 144,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 144
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 143
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 142,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 142
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 141,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 141
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 141,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 141
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 142,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 142
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 143
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 144,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 144
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 141,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 141
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 142,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 142
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 143
      },
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 144,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 144
      }
    ],
    "fileId": 10093
  },
  {
    "name": "Lady Trahaern hideout",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 149,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 149
      }
    ],
    "fileId": 10094
  },
  {
    "name": "Library Historical Archive",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 159,
        "xHigh": 24,
        "xLow": 24,
        "yLow": 159
      }
    ],
    "fileId": 10095
  },
  {
    "name": "Lighthouse cutscene",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 71,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 71
      }
    ],
    "fileId": 10096
  },
  {
    "name": "Lighthouse Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 156,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 156
      }
    ],
    "fileId": 10097
  },
  {
    "name": "Lighthouse Dungeon (cutscene)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 72,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 72
      }
    ],
    "fileId": 10098
  },
  {
    "name": "Lithkren Vault",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 79,
        "xHigh": 24,
        "xLow": 24,
        "yLow": 79
      }
    ],
    "fileId": 10099
  },
  {
    "name": "Lithkren Vault entrance (during quest)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 162,
        "xHigh": 55,
        "xLow": 55,
        "yLow": 162
      }
    ],
    "fileId": 10100
  },
  {
    "name": "Lithkren Vault entrance (post-quest)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 163,
        "xHigh": 55,
        "xLow": 55,
        "yLow": 163
      }
    ],
    "fileId": 10101
  },
  {
    "name": "Lizardman Temple",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 157,
        "xHigh": 20,
        "xLow": 20,
        "yLow": 157
      }
    ],
    "fileId": 10102
  },
  {
    "name": "Lumbridge Castle (Recipe for Disaster)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 83,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 83
      }
    ],
    "fileId": 10103
  },
  {
    "name": "Mage Training Arena rooms",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 150,
        "xHigh": 52,
        "xLow": 52,
        "yLow": 150
      },
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 151,
        "xHigh": 52,
        "xLow": 52,
        "yLow": 151
      }
    ],
    "fileId": 10104
  },
  {
    "name": "Maniacal monkey hunter area",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 142,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 142
      }
    ],
    "fileId": 10105
  },
  {
    "name": "Meiyerditch Laboratories",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 152,
        "xHigh": 56,
        "xLow": 56,
        "yLow": 152
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 55,
        "xLow": 55,
        "yLow": 153
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 152,
        "xHigh": 55,
        "xLow": 55,
        "yLow": 152
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 151,
        "xHigh": 56,
        "xLow": 56,
        "yLow": 151
      }
    ],
    "fileId": 10106
  },
  {
    "name": "Meiyerditch Mine",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 72,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 72
      }
    ],
    "fileId": 10107
  },
  {
    "name": "Mime",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 31,
        "xLow": 31,
        "yLow": 74
      }
    ],
    "fileId": 10108
  },
  {
    "name": "Misthalin Mystery",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 25,
        "xLow": 25,
        "yLow": 75
      },
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 26,
        "xLow": 26,
        "yLow": 75
      }
    ],
    "fileId": 10109
  },
  {
    "name": "Mogre Camp",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 148,
        "xHigh": 46,
        "xLow": 46,
        "yLow": 148
      }
    ],
    "fileId": 10110
  },
  {
    "name": "Monkey Madness hangar (post-quest)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 70,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 70
      }
    ],
    "fileId": 10111
  },
  {
    "name": "Monkey Madness hangar and Bonzara",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 154
      }
    ],
    "fileId": 10112
  },
  {
    "name": "Mourner Tunnels",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 72,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 72
      },
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 72,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 72
      },
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 72,
        "xHigh": 31,
        "xLow": 31,
        "yLow": 72
      }
    ],
    "fileId": 10113
  },
  {
    "name": "Mouse hole",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 86,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 86
      }
    ],
    "fileId": 10114
  },
  {
    "name": "My Arm's Big Adventure boat cutscene",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 76,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 76
      }
    ],
    "fileId": 10115
  },
  {
    "name": "Myreque Hideout (Burgh de Rott)",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 150,
        "xHigh": 54,
        "xLow": 54,
        "yLow": 150
      }
    ],
    "fileId": 10116
  },
  {
    "name": "Myreque Hideout (Canifis)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 54,
        "xLow": 54,
        "yLow": 153
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 53,
        "xLow": 53,
        "yLow": 153
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 54,
        "xLow": 54,
        "yLow": 154
      }
    ],
    "fileId": 10117
  },
  {
    "name": "Myreque Hideout (Meiyerditch)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 150,
        "xHigh": 56,
        "xLow": 56,
        "yLow": 150
      }
    ],
    "fileId": 10118
  },
  {
    "name": "Nature altar",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 75
      }
    ],
    "fileId": 10119
  },
  {
    "name": "Nightmare of Ashihama",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 3,
        "yHigh": 155,
        "xHigh": 60,
        "xLow": 60,
        "yLow": 155
      }
    ],
    "fileId": 10120
  },
  {
    "name": "North-east Karamja cutscene",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 71,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 71
      }
    ],
    "fileId": 10121
  },
  {
    "name": "Observatory Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 146,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 146
      }
    ],
    "fileId": 10122
  },
  {
    "name": "Ogre Enclave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 147,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 147
      }
    ],
    "fileId": 10123
  },
  {
    "name": "Old School Museum",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 155,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 155
      }
    ],
    "fileId": 10124
  },
  {
    "name": "Paterdomus Temple underground",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 53,
        "xLow": 53,
        "yLow": 154
      }
    ],
    "fileId": 10125
  },
  {
    "name": "Polar Eagle lair",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 159,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 159
      }
    ],
    "fileId": 10126
  },
  {
    "name": "Prison Pete",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 69,
        "xHigh": 32,
        "xLow": 32,
        "yLow": 69
      }
    ],
    "fileId": 10127
  },
  {
    "name": "Puro-Puro",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 67,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 67
      }
    ],
    "fileId": 10128
  },
  {
    "name": "Pyramid Plunder",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 69,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 69
      }
    ],
    "fileId": 10129
  },
  {
    "name": "Quidamortem Cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 155,
        "xHigh": 18,
        "xLow": 18,
        "yLow": 155
      }
    ],
    "fileId": 10130
  },
  {
    "name": "Quiz Master",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 74,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 74
      }
    ],
    "fileId": 10131
  },
  {
    "name": "Rantz's cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 146,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 146
      }
    ],
    "fileId": 10132
  },
  {
    "name": "Rashiliyia's Tomb",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 148,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 148
      }
    ],
    "fileId": 10133
  },
  {
    "name": "Ratcatchers Mansion",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 79,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 79
      }
    ],
    "fileId": 10134
  },
  {
    "name": "Recipe for Disaster Ape Atoll Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 85,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 85
      }
    ],
    "fileId": 10135
  },
  {
    "name": "Recruitment Drive",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 77
      }
    ],
    "fileId": 10136
  },
  {
    "name": "Rogues' Den",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 77,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 77
      },
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 79,
        "xHigh": 46,
        "xLow": 46,
        "yLow": 79
      },
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 78,
        "xHigh": 46,
        "xLow": 46,
        "yLow": 78
      },
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 78,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 78
      },
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 79,
        "xHigh": 47,
        "xLow": 47,
        "yLow": 79
      }
    ],
    "fileId": 10137
  },
  {
    "name": "Saba's cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 74,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 74
      }
    ],
    "fileId": 10138
  },
  {
    "name": "Shadow Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 79,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 79
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 79,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 79
      }
    ],
    "fileId": 10139
  },
  {
    "name": "Skavid caves",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 147,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 147
      }
    ],
    "fileId": 10140
  },
  {
    "name": "Smoke Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 146,
        "xHigh": 50,
        "xLow": 50,
        "yLow": 146
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 146,
        "xHigh": 51,
        "xLow": 51,
        "yLow": 146
      }
    ],
    "fileId": 10141
  },
  {
    "name": "Sophanem bank",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 80,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 80
      }
    ],
    "fileId": 10142
  },
  {
    "name": "Sophanem Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 67,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 67
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 66,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 66
      },
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 68,
        "xHigh": 33,
        "xLow": 33,
        "yLow": 68
      }
    ],
    "fileId": 10143
  },
  {
    "name": "Sorceress's Garden",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 85,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 85
      }
    ],
    "fileId": 10144
  },
  {
    "name": "Surprise Exam",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 78,
        "xHigh": 29,
        "xLow": 29,
        "yLow": 78
      }
    ],
    "fileId": 10145
  },
  {
    "name": "Tears of Guthix cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 148,
        "xHigh": 50,
        "xLow": 50,
        "yLow": 148
      }
    ],
    "fileId": 10146
  },
  {
    "name": "Temple of Ikov",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 154
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 41,
        "xLow": 41,
        "yLow": 153
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 153
      }
    ],
    "fileId": 10147
  },
  {
    "name": "Temple of Marimbo Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 143,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 143
      }
    ],
    "fileId": 10148
  },
  {
    "name": "Temple Trekking",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 78,
        "xHigh": 32,
        "xLow": 32,
        "yLow": 78
      }
    ],
    "fileId": 10149
  },
  {
    "name": "Thammaron's throne room",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 2,
        "yHigh": 76,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 76
      }
    ],
    "fileId": 10150
  },
  {
    "name": "The Grand Tree - Monkey Madness II",
    "regionList": [
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 86,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 86
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 86,
        "xHigh": 31,
        "xLow": 31,
        "yLow": 86
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 87,
        "xHigh": 31,
        "xLow": 31,
        "yLow": 87
      },
      {
        "numberOfPlanes": 4,
        "plane": 0,
        "yHigh": 87,
        "xHigh": 30,
        "xLow": 30,
        "yLow": 87
      }
    ],
    "fileId": 10151
  },
  {
    "name": "The Kendal's cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 157,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 157
      }
    ],
    "fileId": 10152
  },
  {
    "name": "Train station",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 86,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 86
      }
    ],
    "fileId": 10153
  },
  {
    "name": "Tree Gnome Village dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 149,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 149
      }
    ],
    "fileId": 10154
  },
  {
    "name": "Tree Gnome Village dungeon (instance)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 69,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 69
      }
    ],
    "fileId": 10155
  },
  {
    "name": "Troll arena - Trollheim tunnel",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 156,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 156
      }
    ],
    "fileId": 10156
  },
  {
    "name": "Trollweiss Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 159,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 159
      }
    ],
    "fileId": 10157
  },
  {
    "name": "Tunnel of Chaos",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 81,
        "xHigh": 49,
        "xLow": 49,
        "yLow": 81
      }
    ],
    "fileId": 10158
  },
  {
    "name": "Tutorial Island dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 148,
        "xHigh": 48,
        "xLow": 48,
        "yLow": 148
      }
    ],
    "fileId": 10159
  },
  {
    "name": "Tyras Camp cutscene",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 71,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 71
      }
    ],
    "fileId": 10160
  },
  {
    "name": "Underground Pass - bottom level",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 154
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 153,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 153
      }
    ],
    "fileId": 10161
  },
  {
    "name": "Underground Pass - bottom level (Song of the Elves instance)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 96,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 96
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 95,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 95
      }
    ],
    "fileId": 10162
  },
  {
    "name": "Underground Pass - first level",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 151,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 151
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 151,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 151
      }
    ],
    "fileId": 10163
  },
  {
    "name": "Underground Pass - Iban's Temple (post-quest)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 73,
        "xHigh": 31,
        "xLow": 31,
        "yLow": 73
      }
    ],
    "fileId": 10164
  },
  {
    "name": "Underground Pass - platforms",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 73,
        "xHigh": 33,
        "xLow": 33,
        "yLow": 73
      },
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 71,
        "xHigh": 33,
        "xLow": 33,
        "yLow": 71
      },
      {
        "numberOfPlanes": 1,
        "plane": 1,
        "yHigh": 72,
        "xHigh": 33,
        "xLow": 33,
        "yLow": 72
      }
    ],
    "fileId": 10165
  },
  {
    "name": "Underground Pass - second level",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 150,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 150
      },
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 149,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 149
      }
    ],
    "fileId": 10166
  },
  {
    "name": "Underground Pass - swamp fail and final area",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 150,
        "xHigh": 38,
        "xLow": 38,
        "yLow": 150
      }
    ],
    "fileId": 10167
  },
  {
    "name": "Ungael Laboratory",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 163,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 163
      }
    ],
    "fileId": 10168
  },
  {
    "name": "Uzer Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 76,
        "xHigh": 42,
        "xLow": 42,
        "yLow": 76
      }
    ],
    "fileId": 10169
  },
  {
    "name": "Varrock Museum basement (higher)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 27,
        "xLow": 27,
        "yLow": 77
      }
    ],
    "fileId": 10170
  },
  {
    "name": "Varrock Museum basement (lower)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 77,
        "xHigh": 25,
        "xLow": 25,
        "yLow": 77
      }
    ],
    "fileId": 10171
  },
  {
    "name": "Varrock Rat Pits",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 79,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 79
      }
    ],
    "fileId": 10172
  },
  {
    "name": "Viyeldi caves (lower level)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 73,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 73
      }
    ],
    "fileId": 10173
  },
  {
    "name": "Viyeldi caves (upper level)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 145,
        "xHigh": 43,
        "xLow": 43,
        "yLow": 145
      }
    ],
    "fileId": 10174
  },
  {
    "name": "Water Ravine Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 149,
        "xHigh": 52,
        "xLow": 52,
        "yLow": 149
      }
    ],
    "fileId": 10175
  },
  {
    "name": "Waterfall Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 40,
        "xLow": 40,
        "yLow": 154
      }
    ],
    "fileId": 10176
  },
  {
    "name": "Waterfall Dungeon (water)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 154,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 154
      }
    ],
    "fileId": 10177
  },
  {
    "name": "Wilderness Wars",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 72,
        "xHigh": 51,
        "xLow": 51,
        "yLow": 72
      }
    ],
    "fileId": 10178
  },
  {
    "name": "Witchaven Dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 79,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 79
      }
    ],
    "fileId": 10179
  },
  {
    "name": "Wrath altar",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 0,
        "yHigh": 75,
        "xHigh": 36,
        "xLow": 36,
        "yLow": 75
      }
    ],
    "fileId": 10180
  },
  {
    "name": "Yanille cutscene",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 73,
        "xHigh": 45,
        "xLow": 45,
        "yLow": 73
      }
    ],
    "fileId": 10181
  },
  {
    "name": "Tutorial Island v2 dungeon",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 195,
        "xHigh": 26,
        "xLow": 26,
        "yLow": 195
      }
    ],
    "fileId": 10182
  },
  {
    "name": "Prifddinas Grand Library (post-quest)",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 195,
        "xHigh": 50,
        "xLow": 50,
        "yLow": 195
      }
    ],
    "fileId": 10183
  },
  {
    "name": "Temple Trekking",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 71,
        "xHigh": 44,
        "xLow": 44,
        "yLow": 71
      }
    ],
    "fileId": 10184
  },
  {
    "name": "Prifddinas rabbit cave",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 196,
        "xHigh": 51,
        "xLow": 51,
        "yLow": 196
      }
    ],
    "fileId": 10185
  },
  {
    "name": "Hallowed Sepulchre - Level 5",
    "regionList": [
      {
        "numberOfPlanes": 3,
        "plane": 0,
        "yHigh": 91,
        "xHigh": 35,
        "xLow": 35,
        "yLow": 91
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 3,
        "chunk_xHigh": 7,
        "plane": 0,
        "chunk_yLow": 0,
        "yHigh": 92,
        "xHigh": 35,
        "xLow": 35,
        "chunk_yHigh": 1,
        "yLow": 92
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 3,
        "chunk_xHigh": 1,
        "plane": 0,
        "chunk_yLow": 0,
        "yHigh": 91,
        "xHigh": 36,
        "xLow": 36,
        "chunk_yHigh": 7,
        "yLow": 91
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 3,
        "chunk_xHigh": 7,
        "plane": 0,
        "chunk_yLow": 6,
        "yHigh": 90,
        "xHigh": 35,
        "xLow": 35,
        "chunk_yHigh": 7,
        "yLow": 90
      },
      {
        "chunk_xLow": 6,
        "numberOfPlanes": 3,
        "chunk_xHigh": 7,
        "plane": 0,
        "chunk_yLow": 0,
        "yHigh": 91,
        "xHigh": 34,
        "xLow": 34,
        "chunk_yHigh": 7,
        "yLow": 91
      }
    ],
    "fileId": 10186
  },
  {
    "name": "Hallowed Sepulchre - Level 2",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 93,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 93
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 94,
        "xHigh": 39,
        "xLow": 39,
        "chunk_yHigh": 1,
        "yLow": 94
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 1,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 93,
        "xHigh": 40,
        "xLow": 40,
        "chunk_yHigh": 7,
        "yLow": 93
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 6,
        "yHigh": 92,
        "xHigh": 39,
        "xLow": 39,
        "chunk_yHigh": 7,
        "yLow": 92
      },
      {
        "chunk_xLow": 6,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 93,
        "xHigh": 38,
        "xLow": 38,
        "chunk_yHigh": 7,
        "yLow": 93
      }
    ],
    "fileId": 10187
  },
  {
    "name": "Hallowed Sepulchre - Level 4",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 91,
        "xHigh": 39,
        "xLow": 39,
        "yLow": 91
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 92,
        "xHigh": 39,
        "xLow": 39,
        "chunk_yHigh": 1,
        "yLow": 92
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 1,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 91,
        "xHigh": 40,
        "xLow": 40,
        "chunk_yHigh": 7,
        "yLow": 91
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 6,
        "yHigh": 90,
        "xHigh": 39,
        "xLow": 39,
        "chunk_yHigh": 7,
        "yLow": 90
      },
      {
        "chunk_xLow": 6,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 91,
        "xHigh": 38,
        "xLow": 38,
        "chunk_yHigh": 7,
        "yLow": 91
      }
    ],
    "fileId": 10188
  },
  {
    "name": "Hallowed Sepulchre - Level 3",
    "regionList": [
      {
        "numberOfPlanes": 2,
        "plane": 1,
        "yHigh": 91,
        "xHigh": 37,
        "xLow": 37,
        "yLow": 91
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 90,
        "xHigh": 37,
        "xLow": 37,
        "chunk_yHigh": 1,
        "yLow": 90
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 1,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 91,
        "xHigh": 38,
        "xLow": 38,
        "chunk_yHigh": 7,
        "yLow": 91
      },
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 6,
        "yHigh": 90,
        "xHigh": 37,
        "xLow": 37,
        "chunk_yHigh": 7,
        "yLow": 90
      },
      {
        "chunk_xLow": 6,
        "numberOfPlanes": 2,
        "chunk_xHigh": 7,
        "plane": 1,
        "chunk_yLow": 0,
        "yHigh": 91,
        "xHigh": 36,
        "xLow": 36,
        "chunk_yHigh": 7,
        "yLow": 91
      }
    ],
    "fileId": 10189
  },
  {
    "name": "Ardougne Prison",
    "regionList": [
      {
        "chunk_xLow": 0,
        "numberOfPlanes": 1,
        "chunk_xHigh": 3,
        "plane": 0,
        "chunk_yLow": 4,
        "yHigh": 151,
        "xHigh": 40,
        "xLow": 40,
        "chunk_yHigh": 7,
        "yLow": 151
      }
    ],
    "fileId": 10190
  },
  {
    "name": "Dragon Slayer II boat",
    "regionList": [
      {
        "numberOfPlanes": 1,
        "plane": 0,
        "yHigh": 87,
        "xHigh": 25,
        "xLow": 25,
        "yLow": 87
      }
    ],
    "fileId": 10191
  }
]

with open("%s/minimapIcons.json" % version) as f:
	icons = json.load(f)

iconSprites = {}
for file in glob.glob("%s/icons/*.png" % version):
	print(file)
	spriteId = int(file.split("/")[-1][:-4])
	iconSprites[spriteId] = Image.open(file)

overallXLow = 999
overallXHigh = 0
overallYLow = 999
overallYHigh = 0
for file in glob.glob("%s/tiles/base/*.png" % version):
	filename = file.split("/")[-1]
	filename = filename.replace(".png", "")
	plane, x, y = map(int, filename.split("_"))
	overallYHigh = max(y, overallYHigh)
	overallYLow = min(y, overallYLow)
	overallXHigh = max(x, overallXHigh)
	overallXLow = min(x, overallXLow)

defs.append({"name": "debug", "mapId": -1, "regionList": [{"xLowerLeft": overallXLow, "yUpperRight": overallYHigh, "yLowerRight": overallYLow, "yLowerLeft": overallYLow, "numberOfPlanes": 4, "xUpperLeft": overallXLow, "xUpperRight": overallXHigh, "yUpperLeft": overallYHigh, "plane": 0, "xLowerRight": overallXHigh}]})

def mkdir_p(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc:
        pass

def getBounds(regionList):
	lowX, lowY, highX, highY = 9999, 9999, 0, 0
	planes = 0
	for region in regionList:
		if 'xLowerLeft' in region: #typeA
			lowX = min(lowX, region['xUpperLeft'])
			highX = max(highX, region['xUpperRight'])
			lowY = min(lowY, region['yLowerLeft'])
			highY = max(highY, region['yUpperLeft'])
			planes = max(planes, region['numberOfPlanes'])
		elif 'newX' in region:
			lowX = min(lowX, region['newX'])
			highX = max(highX, region['newX'])
			lowY = min(lowY, region['newY'])
			highY = max(highY, region['newY'])
			planes = max(planes, region['numberOfPlanes'])
		elif 'xLow' in region:
			lowX = min(lowX, region['xLow'])
			highX = max(highX, region['xHigh'])
			lowY = min(lowY, region['yLow'])
			highY = max(highY, region['yHigh'])
			planes = max(planes, region['numberOfPlanes'])	
		else:
			raise ValueError(region)
	return lowX, highX, lowY, highY, planes

def pointInsideBox(position, plane, lowX, highX, lowY, highY, chunk_lowX, chunk_highX, chunk_lowY, chunk_highY, allPlanes):
	x = position['x']
	y = position['y']
	z = position['z']
	lowX = lowX * 64 + chunk_lowX * 8
	lowY = lowY * 64 + chunk_lowY * 8
	highX = highX * 64 + chunk_highX * 8 + 7
	highY = highY * 64 + chunk_highY * 8 + 7
	return ((plane == 0) or (plane == z)) and x >= lowX and x <= highX and y >= lowY and y <= highY

def getIconsInsideArea(plane, lowX, highX, lowY, highY, chunk_lowX=0, chunk_highX=7, chunk_lowY=0, chunk_highY=7, dx=0, dy=0, dz=0, allPlanes=False):
	valid = []
	for icon in icons:
		if pointInsideBox(icon['position'], plane, lowX, highX, lowY, highY, chunk_lowX, chunk_highX, chunk_lowY, chunk_highY, allPlanes):
			pos = icon['position']
			icon = [pos['x'] + dx, pos['y'] + dy, icon['spriteId']]
			valid.append(icon)
	return valid
def allBlack(im):
	data = np.asarray(im.convert('RGBA'))
	return np.count_nonzero(data[:,:,:3]) == 0

PADDING = 64
baseMaps = []
px_per_square = 4
for defn in defs:
	mapId = -1
	if 'mapId' in defn:
		mapId = defn['mapId']
	elif 'fileId' in defn:
		mapId = defn['fileId']
	lowX, highX, lowY, highY, planes = getBounds(defn['regionList'])
	bounds = [[lowX * 64 - PADDING, lowY * 64 - PADDING], [(highX + 1) * 64 + PADDING, (highY + 1) * 64 + PADDING]]
	# bounds = [[0, 0], [12800, 12800]]
	if mapId < 1:
		center = [2496, 3328]
	elif 'position' in defn:
		center = [defn['position']['x'], defn['position']['y']]
	else:
		print('cent')
		center = [(lowX + highX + 1) * 32, (lowY + highY + 1) * 32]
	baseMaps.append({'mapId': mapId, 'name': defn['name'], 'bounds': bounds, 'center': center})
	overallHeight = (highY - lowY + 1) * px_per_square * 64
	overallWidth = (highX - lowX + 1) * px_per_square * 64
	
	plane0Map = None
	for plane in range(planes):
		print(mapId, plane)
		validIcons = []
		im = Image.new("RGB", (overallWidth + 512, overallHeight + 512))
		for region in defn['regionList']:
			if 'xLowerLeft' in region:
				oldLowX = region['xLowerLeft']
				oldHighX = region['xLowerRight']
				oldLowY = region['yLowerLeft']
				oldHighY = region['yUpperLeft']
				newLowX = region['xUpperLeft']
				newHighX = region['xUpperRight']
				newLowY = region['yLowerRight']
				newHighY = region['yUpperRight']
				print(oldLowX == newLowX, oldLowY == newLowY, oldHighX == newHighX, oldHighY == newHighY)
				validIcons.extend(getIconsInsideArea(region['plane'] + plane, oldLowX, oldHighX, oldLowY, oldHighY, allPlanes=plane==0))
				for x in range(oldLowX, oldHighX + 1):
					for y in range(oldLowY, oldHighY + 1):
						filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, x, y)
						if os.path.exists(filename):
							square = Image.open(filename)
							imX = (x-lowX+newLowX-oldLowX) * px_per_square * 64
							imY = (highY-y) * px_per_square * 64
							im.paste(square, box=(imX+256, imY+256))
			elif 'chunk_oldXLow' in region:
				filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['oldPlane'] + plane, region['oldX'], region['oldY'])
				dx = region['newX'] * 64 + region['chunk_newXLow'] * 8 - region['oldX'] * 64 - region['chunk_oldXLow'] * 8
				dy = region['newY'] * 64 + region['chunk_newYLow'] * 8 - region['oldY'] * 64 - region['chunk_oldYLow'] * 8
				dz = 0 - region['oldPlane']
				validIcons.extend(getIconsInsideArea(region['oldPlane'] + plane, region['oldX'], region['oldX'], region['oldY'], region['oldY'], region['chunk_oldXLow'], region['chunk_oldXHigh'], region['chunk_oldYLow'], region['chunk_oldYHigh'], dx, dy, dz, allPlanes=plane==0))
				if os.path.exists(filename):
					square = Image.open(filename)
					cropped = square.crop((region['chunk_oldXLow'] * px_per_square * 8,
					 (8-region['chunk_oldYHigh'] - 1) * px_per_square * 8,
					 (region['chunk_oldXHigh'] + 1) * px_per_square * 8,
					 (8-region['chunk_oldYLow']) * px_per_square * 8))
					imX = (region['newX']-lowX) * px_per_square * 64 + region['chunk_newXLow'] * px_per_square * 8
					imY = (highY-region['newY']) * px_per_square * 64 + (7-region['chunk_newYHigh']) * px_per_square * 8
					im.paste(cropped, box=(imX+256, imY+256))
			elif 'chunk_xLow' in region:
				validIcons.extend(getIconsInsideArea(region['plane'] + plane, region['xLow'], region['xHigh'], region['yLow'], region['yHigh'], region['chunk_xLow'], region['chunk_xHigh'], region['chunk_yLow'], region['chunk_yHigh'], allPlanes=plane==0))
				filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, region['xLow'], region['yLow'])
				if os.path.exists(filename):
					square = Image.open(filename)
					cropped = square.crop((region['chunk_xLow'] * px_per_square * 8,
					 (8-region['chunk_yHigh'] - 1) * px_per_square * 8,
					 (region['chunk_xHigh'] + 1) * px_per_square * 8,
					 (8-region['chunk_yLow']) * px_per_square * 8))
					imX = (region['xLow']-lowX) * px_per_square * 64 + region['chunk_xLow'] * px_per_square * 8
					imY = (highY-region['yLow']) * px_per_square * 64 + (7-region['chunk_yHigh']) * px_per_square * 8
					im.paste(cropped, box=(imX+256, imY+256))
			elif 'xLow' in region:
				validIcons.extend(getIconsInsideArea(region['plane'] + plane, region['xLow'], region['xHigh'], region['yLow'], region['yHigh'], allPlanes=plane==0))
				for x in range(region['xLow'], region['xHigh'] + 1):
					for y in range(region['yLow'], region['yHigh'] + 1):
						filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, x, y)
						if os.path.exists(filename):
							square = Image.open(filename)
							imX = (x-lowX) * px_per_square * 64
							imY = (highY-y) * px_per_square * 64
							im.paste(square, box=(imX+256, imY+256))
			else:
				raise ValueError(region)
		if plane == 0:
			data = np.asarray(im.convert('RGB')).copy()
			data[(data == (255, 0, 255)).all(axis = -1)] = (0, 0, 0)
			im = Image.fromarray(data, mode='RGB')
			if planes > 1:
				plane0Map = im.convert('LA').filter(ImageFilter.GaussianBlur(radius=5))
		elif plane > 0:
			data = np.asarray(im.convert('RGBA')).copy()
			data[:,:,3] = 255*(data[:,:,:3] != (255, 0, 255)).all(axis = -1)
			mask = Image.fromarray(data, mode='RGBA')
			im = plane0Map.convert("RGBA")
			im.paste(mask, (0, 0), mask)

		for zoom in range(-3, 4):
			scalingFactor = 2.0**zoom/2.0**2
			zoomedWidth = int(round(scalingFactor * im.width))
			zoomedHeight = int(round(scalingFactor * im.height))
			resample = Image.BILINEAR if zoom <= 1 else Image.NEAREST
			zoomed = im.resize((zoomedWidth, zoomedHeight), resample=resample)
			if zoom >= 0:
				for x, y, spriteId in validIcons:
					sprite = iconSprites[spriteId]
					width, height = sprite.size
					imX = int(round((x - lowX * 64) * px_per_square * scalingFactor)) - width // 2 - 2
					imY = int(round(((highY + 1) * 64 - y) * px_per_square * scalingFactor)) - height // 2 - 2
					zoomed.paste(sprite, (imX+int(round(256*scalingFactor)), int(round(imY+256 * scalingFactor))), sprite)
			
			lowZoomedX = int((lowX - 1) * scalingFactor + 0.01)
			highZoomedX = int((highX + 0.9 + 1) * scalingFactor + 0.01)
			lowZoomedY = int((lowY - 1) * scalingFactor + 0.01)
			highZoomedY = int((highY + 0.9 + 1) * scalingFactor + 0.01)
			for x in range(lowZoomedX, highZoomedX + 1):
				for y in range(lowZoomedY, highZoomedY + 1):
					coordX = int((x - (lowX - 1) * scalingFactor) * 256)
					coordY = int((y - (lowY - 1) * scalingFactor) * 256)
					cropped = zoomed.crop((coordX, zoomed.size[1] - coordY - 256, coordX + 256, zoomed.size[1] - coordY))
					if not allBlack(cropped):
						outfilename = "%s/tiles/rendered/%s/%s/%s_%s_%s.png" % (version, mapId, zoom, plane, x, y)
						mkdir_p(outfilename)
						cropped.save(outfilename)
			# outfilename = "%s/tiles/rendered/%s/%s_%s_full.png" % (version, mapId, plane, zoom)
			# mkdir_p(outfilename)
			# zoomed.save(outfilename)
with open("%s/basemaps.json" % version, 'w') as f:
	json.dump(baseMaps, f)