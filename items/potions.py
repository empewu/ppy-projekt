from items.base import Consumable
from balance import potion_kwargs

# Stats (effect, amount, value) live in balance.toml; only name + the
# construction call live here. Potions are crafted via the Alchemy menu.

def _potion(name):
    return Consumable(name, **potion_kwargs(name))

HealthPotion = _potion("Health Potion")

GreaterHealthPotion = _potion("Greater Health Potion")

ElixirOfPower = _potion("Elixir of Power")

StoneskinDraught = _potion("Stoneskin Draught")
