from items import TorsoArmour

CopperPlate = TorsoArmour(
    "Copper Plate",
    "A basic copper plate.",
    value = 20,
    defence = 15,
    attribute_required = "Strength",
    attribute_amount = 3
    )

IronPlate = TorsoArmour(
    "Iron Plate",
    "A sturdy iron plate.",
    value = 40,
    defence = 20,
    attribute_required = "Strength",
    attribute_amount = 5
    )

ClothHood = TorsoArmour(
    "Cloth Vest",
    "A basic cloth vest.",
    value = 10,
    defence = 0
    )

LeatherHood = TorsoArmour(
    "Leather Vest",
    "A sturdy leather vest.",
    value = 10,
    defence = 10,
    attribute_required = "Agility",
    attribute_amount = 3
)
