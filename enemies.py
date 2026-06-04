from enemy import Enemy
from items.loot import *

Goblin = Enemy(
    name = "Goblin",
    health = 15,
    damage = 5,
    defence = 0,
    loot_table=[
        (coinPouch, 0.2),
        (monsterParts,  0.3),
    ]
)

Spider = Enemy(
    name = "Spider",
    health = 20,
    damage = 10,
    defence = 5,
    loot_table=[
        (monsterParts,  0.5),
        (monsterPartsRare, 0.4),
    ]
)

Wolf = Enemy(
    name = "Wolf",
    health = 25,
    damage = 15,
    defence = 5,
    loot_table=[
        (monsterParts,  0.7),
    ]
)

Wraith = Enemy(
    name = "Wraith",
    health = 10,
    damage = 15,
    defence = 100,
    loot_table=[
        (valuableGem, 0.2),
        (monsterPartsMagical,  0.3),
    ]
)

Ghoul = Enemy(
    name = "Ghoul",
    health = 40,
    damage = 20,
    defence = 10,
    loot_table=[
        (coinPouch, 0.4),
        (monsterPartsMagical,  0.3),
    ]
)

Slime = Enemy(
    name = "Slime",
    health = 60,
    damage = 15,
    defence = 0,
    loot_table=[
        (monsterParts, 0.3),
        (monsterPartsRare, 0.3),
        (monsterPartsMagical,  0.3),
    ]
)

Skeleton = Enemy(
    name = "Skeleton",
    health = 40,
    damage = 15,
    defence = 20,
    loot_table=[
        (coinPouch, 0.2),
        (monsterParts,  0.3),
        (monsterPartsMagical,  0.3),
    ]
)

Golem = Enemy(
    name = "Golem",
    health = 100,
    damage = 30,
    defence = 30,
    loot_table=[
        (monsterPartsMagical,  1),
        (goldBar, 0.3)
    ]
)
