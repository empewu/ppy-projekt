from enemy import Enemy
from balance import enemy_kwargs
from items.loot import *

# Enemy stats (health, damage, defence) live in balance.toml.
# Loot tables reference item objects, so they stay here as the enemy's identity.

_LOOT = {
    "Goblin": [
        (coinPouch, 0.2),
        (monsterParts, 0.3),
    ],
    "Spider": [
        (monsterParts, 0.5),
        (monsterPartsRare, 0.4),
    ],
    "Wolf": [
        (monsterParts, 0.7),
    ],
    "Wraith": [
        (valuableGem, 0.2),
        (monsterPartsMagical, 0.3),
    ],
    "Ghoul": [
        (coinPouch, 0.4),
        (monsterPartsMagical, 0.3),
    ],
    "Slime": [
        (monsterParts, 0.3),
        (monsterPartsRare, 0.3),
        (monsterPartsMagical, 0.3),
    ],
    "Skeleton": [
        (coinPouch, 0.2),
        (monsterParts, 0.3),
        (monsterPartsMagical, 0.3),
    ],
    "Golem": [
        (monsterPartsMagical, 1),
        (goldBar, 0.3),
    ],
}

def _enemy(name):
    return Enemy(name, loot_table=_LOOT[name], **enemy_kwargs(name))

Goblin = _enemy("Goblin")
Spider = _enemy("Spider")
Wolf = _enemy("Wolf")
Wraith = _enemy("Wraith")
Ghoul = _enemy("Ghoul")
Slime = _enemy("Slime")
Skeleton = _enemy("Skeleton")
Golem = _enemy("Golem")
