from items.base import LegsArmour
from balance import armour_kwargs

# Stats live in balance.toml; only name + description are kept here.

def _legs(name, description):
    return LegsArmour(name, description, **armour_kwargs(name))

CopperBoots = _legs("Copper Greaves", "A pair of basic copper greaves.")

IronBoots = _legs("Iron Greaves", "A pair of sturdy iron greaves.")

ClothBoots = _legs("Cloth Wrappings", "A pair of basic cloth wrappings.")

LeatherBoots = _legs("Leather Boots", "A pair of sturdy leather boots.")

WardenGreaves = _legs("Warden Greaves", "A pair of heavy plated greaves that only the tough can bear.")
