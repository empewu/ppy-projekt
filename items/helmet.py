from items.base import HeadArmour
from balance import armour_kwargs

# Stats live in balance.toml; only name + description are kept here.

def _helmet(name, description):
    return HeadArmour(name, description, **armour_kwargs(name))

CopperHelmet = _helmet("Copper Helmet", "A basic copper helmet.")

IronHelmet = _helmet("Iron Helmet", "A sturdy iron helmet.")

ClothHood = _helmet("Cloth Hood", "A basic cloth hood.")

LeatherHood = _helmet("Leather Hood", "A sturdy leather hood.")
