from items.base import LegsArmour

CopperBoots = LegsArmour(
    "Copper Greaves",
    "A pair of basic copper greaves.",
    value = 20,
    defence = 5,
    attribute_required = "Strength",
    attribute_amount = 2
    )

IronBoots = LegsArmour(
    "Iron Greaves",
    "A pair of sturdy iron greaves.",
    value = 40,
    defence = 10,
    attribute_required = "Strength",
    attribute_amount = 4
    )

ClothBoots = LegsArmour(
    "Cloth Wrappings",
    "A pair of basic cloth wrappings.",
    value = 10,
    defence = 1
    )

LeatherBoots = LegsArmour(
    "Leather Boots",
    "A pair of sturdy leather boots.",
    value = 10,
    defence = 5,
    attribute_required = "Agility",
    attribute_amount = 2
)
