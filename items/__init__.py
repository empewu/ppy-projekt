from items.base import *
from items.helmet import *
from items.arms import *
from items.legs import *
from items.torso import *
from items.mainhand import *
from items.offhand import *
from items.rings import *
from items.loot import *

import items.helmet as helmet
import items.arms as arms
import items.legs as legs
import items.torso as torso
import items.mainhand as mainhand
import items.offhand as offhand
import items.rings as rings
import items.loot as loot
from items.base import Item

def _build_registry():
    modules = [helmet, arms, legs, torso, mainhand, offhand, rings, loot]
    return {
        obj.name: obj
        for module in modules
        for obj in vars(module).values()
        if isinstance(obj, Item)
    }

ITEM_REGISTRY = _build_registry()
