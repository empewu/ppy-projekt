from items import HeadArmour

CopperHelmet = HeadArmour(
    "Copper Helmet",
    "A basic copper helmet.",
    value = 20,
    defence = 5,
    attribute_required = "Strength",
    attribute_amount = 2
    )

IronHelmet = HeadArmour(
    "Iron Helmet",
    "A sturdy iron helmet.",
    value = 40,
    defence = 10,
    attribute_required = "Strength",
    attribute_amount = 4
    )

ClothHood = HeadArmour(
    "Cloth Hood",
    "A basic cloth hood.",
    value = 10,
    defence = 0
    )

LeatherHood = HeadArmour(
    "Leather Hood",
    "A sturdy leather hood.",
    value = 10,
    defence = 5,
    attribute_required = "Agility",
    attribute_amount = 2
)
