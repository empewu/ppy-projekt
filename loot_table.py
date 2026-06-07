import items.loot as loot
import items.helmet as helmet
import items.mainhand as mainhand
import items.offhand as offhand

LOCATION_LOOT = {
    "Dark Forest": [
        (loot.coinPouch, 0.3),
        (loot.monsterParts, 0.2),
        (mainhand.IronSword, 0.1),
        (mainhand.IronCrossbow, 0.1),
        (mainhand.RunedStaff, 0.1),
    ],
    "Ancient Ruins": [
        (loot.coinPouch, 0.3),
        (loot.valuableGem, 0.1),
        (loot.monsterPartsRare, 0.1),
        (helmet.IronHelmet, 0.1),
        (offhand.SpikedTowerShield, 0.1),
    ],
    "Dark Cave": [
        (loot.coinPouch, 0.2),
        (loot.valuableGem, 0.2),
        (loot.goldBar, 0.1),
    ],
    "Misty Swamp": [
        (loot.coinPouch, 0.3),
        (loot.monsterPartsMagical, 0.1),
        (offhand.WardingTalisman, 0.1),
        (offhand.MagicalTalisman, 0.1),
    ],
}

LOCATION_REST_LOOT = {
    "Dark Forest": [
        (loot.coinPouch, 0.3),
        (loot.monsterParts, 0.1),
    ],
    "Ancient Ruins": [
        (loot.valuableGem, 0.2),
        (loot.coinPouch, 0.3),
    ],
    "Dark Cave": [
        (loot.valuableGem, 0.2),
        (loot.goldBar, 0.1),
    ],
    "Misty Swamp": [
        (loot.monsterParts, 0.3),
        (loot.monsterPartsRare, 0.2),
        (loot.monsterPartsMagical, 0.1),
    ],
}
