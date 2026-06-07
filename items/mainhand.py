from items.base import MainHand
from balance import weapon_kwargs

# Stats (damage, defence, value, requirements) live in balance.toml.
# Here we keep only the identity: name + description.

def _mainhand(name, description):
    return MainHand(name, description, **weapon_kwargs(name))

CopperSword = _mainhand("Copper Sword", "A basic copper sword.")

IronSword = _mainhand("Iron Sword", "A sturdy iron sword.")

IronHammer = _mainhand("Iron Hammer", "A sturdy iron hammer. Impossible to defend with.")

WoodenStaff = _mainhand("Wooden Staff", "A basic wooden staff. Barely better than a stick.")

WoodenBow = _mainhand("Wooden Bow", "A basic wooden bow.")

IronCrossbow = _mainhand("Iron Crossbow", "A sturdy crossbow with an iron mechanism.")
