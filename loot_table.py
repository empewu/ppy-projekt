import items.loot as loot
import items.helmet as helmet
import items.mainhand as mainhand
import items.offhand as offhand

LOCATION_LOOT = {
    "Dark Forest": [
        (loot.coinPouch, 0.8),
        (loot.monsterParts, 0.5),
        (mainhand.IronSword, 0.2),
        (mainhand.IronCrossbow, 0.1),
    ],
    "Ancient Ruins": [
        (loot.coinPouch, 0.6),
        (loot.valuableGem, 0.15),
        (loot.monsterPartsRare, 0.2),
        (helmet.IronHelmet, 0.15),
    ],
    "Dark Cave": [
        (loot.coinPouch, 0.2),
        (loot.valuableGem, 0.2),
        (loot.goldBar, 0.1),
    ],
    "Misty Swamp": [
        (loot.coinPouch, 0.5),
        (loot.monsterPartsMagical, 0.3),
        (offhand.WoodenShield, 0.2),
        (offhand.MagicalTalisman, 0.2),
    ],
}

