from enemies import *
from loot_table import LOCATION_LOOT

LOCATIONS = {
    1: {
        "name": "Dark Forest",
        "description": "A dense, eerie forest.",
        "encounters": [
            {"type": "combat", "enemy": Slime},
            {"type": "combat", "enemy": Wolf},
            {"type": "treasure", "loot": LOCATION_LOOT["Dark Forest"]},
            {"type": "rest"},
            {"type": "combat", "enemy": Spider},
            {"type": "combat", "enemy": Goblin},
        ]
    },
    2: {
        "name": "Ancient Ruins",
        "description": "Ancient ruins full of danger.",
        "encounters": [
            {"type": "combat", "enemy": Skeleton},
            {"type": "combat", "enemy": Wraith},
            {"type": "rest"},
            {"type": "treasure", "loot": LOCATION_LOOT["Ancient Ruins"]},
            {"type": "combat", "enemy": Golem},
        ]
    },
    3: {
        "name": "Dark Cave",
        "description": "A damp, dark cave.",
        "encounters": [
            {"type": "combat", "enemy": Slime},
            {"type": "rest"},
            {"type": "treasure", "loot": LOCATION_LOOT["Dark Cave"]},
            {"type": "combat", "enemy": Spider},
            {"type": "combat", "enemy": Goblin},
        ]
    },
    4: {
        "name": "Misty Swamp",
        "description": "A murky swamp shrouded in mist.",
        "encounters": [
            {"type": "combat", "enemy": Wraith},
            {"type": "treasure", "loot": LOCATION_LOOT["Misty Swamp"]},
            {"type": "combat", "enemy": Ghoul},
        ]
    },
}