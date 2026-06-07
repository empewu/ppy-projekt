from items.base import ArmsArmour
from balance import armour_kwargs

# Stats live in balance.toml; only name + description are kept here.

def _arms(name, description):
    return ArmsArmour(name, description, **armour_kwargs(name))

CopperGloves = _arms("Copper Gauntlets", "A pair of basic copper gauntlets.")

IronGloves = _arms("Iron Gauntlets", "A pair of sturdy iron gauntlets.")

ClothGloves = _arms("Cloth Mittens", "A pair of basic cloth mittens.")

LeatherGloves = _arms("Leather Gloves", "A pair of sturdy leather gloves.")
