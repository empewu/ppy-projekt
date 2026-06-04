from items import OffHand

MagicalTalisman = OffHand(
    "Magical Talisman",
    "A talisman made of bones and wood. Enhances your attacks.",
    value = 100,
    damage = 15,
    defence = 0,
    attribute_required = "Intelligence",
    attribute_amount = 4
    )

WardingTalisman = OffHand(
    "Warding Talisman",
    "A talisman made of bones and wood. Protects you from attacks.",
    value = 100,
    damage = 0,
    defence = 25,
    attribute_required = "Intelligence",
    attribute_amount = 4
    )

WoodenShield = OffHand(
    "Wooden Shield",
    "A sturdy wooden shield.",
    value = 50,
    damage = 0,
    defence = 15
    )

TowerShield = OffHand(
    "Tower Shield",
    "A massive iron shield.",
    value = 100,
    damage = 0,
    defence = 35,
    attribute_required = "Strength",
    attribute_amount = 6
    )

SpikedShield = OffHand(
    "Spiked Shield",
    "A shield covered with spikes, both on the inside and outside.",
    value = 75,
    damage = 10,
    defence = 15,
    attribute_required = "Endurance",
    attribute_amount = 4
    )
