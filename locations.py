from enemies import *

LOCATIONS = {
    1: {
        "name": "Dark Forest",
        "description": "A dense, eerie forest.",
        "encounters": [
            {"type": "combat", "enemy": Slime},
            {"type": "combat", "enemy": Wolf},
            {"type": "treasure", "loot": "Dark Forest"},
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
            {"type": "combat", "enemy": Skeleton},
            {"type": "treasure", "loot": "Ancient Ruin"},
            {"type": "combat", "enemy": Golem},
        ]
    },
    3: {
        "name": "Dark Cave",
        "description": "A damp, dark cave.",
        "encounters": [
            {"type": "combat", "enemy": Slime},
            {"type": "rest"},
            {"type": "combat", "enemy": Spider},
            {"type": "combat", "enemy": Goblin},
        ]
    },
    4: {
        "name": "Misty Swamp",
        "description": "A murky swamp shrouded in mist.",
        "encounters": [
            {"type": "combat", "enemy": Wraith},
            {"type": "treasure", "loot": "Haunted Swamp"},
            {"type": "combat", "enemy": Ghoul},
            {"type": "combat", "enemy": Slime},
        ]
    },
}