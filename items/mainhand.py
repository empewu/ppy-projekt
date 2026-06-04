from items.base import MainHand

CopperSword = MainHand(
    "Copper Sword",
    "A basic copper sword.",
    value = 20,
    damage = 10,
    defence = 4,
    attribute_required = "Strength",
    attribute_amount = 2
    )

IronSword = MainHand(
    "Iron Sword",
    "A sturdy iron sword.",
    value = 40,
    damage = 20,
    defence = 8,
    attribute_required = "Strength",
    attribute_amount = 3
    )

IronHammer = MainHand(
    "Iron Hammer",
    "A sturdy iron hammer. Impossible to defend with.",
    value = 50,
    damage = 30,
    defence = 0,
    attribute_required = "Strength",
    attribute_amount = 5
    )

WoodenStaff = MainHand(
    "Wooden Staff",
    "A basic wooden staff. Barely better than a stick.",
    value = 10,
    damage = 5,
    defence = 2
    )

WoodenBow = MainHand(
    "Wooden Bow",
    "A basic wooden bow.",
    value = 30,
    damage = 15,
    defence = 0,
    attribute_required = "Agility",
    attribute_amount = 2
)

IronCrossbow = MainHand(
    "Iron Crossbow",
    "A sturdy crossbow with an iron mechanism.",
    value = 40,
    damage = 30,
    defence = 0,
    attribute_required = "Agility",
    attribute_amount = 4
)
