from items.base import TorsoArmour
from balance import armour_kwargs

# Stats live in balance.toml; only name + description are kept here.

def _torso(name, description):
    return TorsoArmour(name, description, **armour_kwargs(name))

CopperTorso = _torso("Copper Plate", "A basic copper plate.")

IronTorso = _torso("Iron Plate", "A sturdy iron plate.")

ClothTorso = _torso("Cloth Vest", "A basic cloth vest.")

LeatherTorso = _torso("Leather Vest", "A sturdy leather vest.")
