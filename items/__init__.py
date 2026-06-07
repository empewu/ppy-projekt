from items.base import *
from items.helmet import *
from items.arms import *
from items.legs import *
from items.torso import *
from items.mainhand import *
from items.offhand import *
from items.rings import *
from items.loot import *
from items.potions import *

import items.helmet as helmet
import items.arms as arms
import items.legs as legs
import items.torso as torso
import items.mainhand as mainhand
import items.offhand as offhand
import items.rings as rings
import items.loot as loot
import items.potions as potions
from items.base import Item

def _build_registry():
    modules = [helmet, arms, legs, torso, mainhand, offhand, rings, loot, potions]
    return {
        obj.name: obj
        for module in modules
        for obj in vars(module).values()
        if isinstance(obj, Item)
    }

ITEM_REGISTRY = _build_registry()

def _validate_recipes():
    """Cross-check crafting recipes against the registry (done here rather than
    in balance.py, which must not import the item modules)."""
    from balance import RECIPES
    for potion_name, recipe in RECIPES.items():
        if potion_name not in ITEM_REGISTRY:
            raise ValueError(f"recipe for unknown potion {potion_name!r}")
        for ingredient in recipe["ingredients"]:
            if ingredient not in ITEM_REGISTRY:
                raise ValueError(f"recipe {potion_name!r} uses unknown ingredient {ingredient!r}")

_validate_recipes()
