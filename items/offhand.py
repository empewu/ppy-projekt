from items.base import OffHand
from balance import weapon_kwargs

# Stats live in balance.toml; only name + description are kept here.

def _offhand(name, description):
    return OffHand(name, description, **weapon_kwargs(name))

MagicalTalisman = _offhand("Magical Talisman", "A talisman made of bones and wood. Enhances your attacks.")

WardingTalisman = _offhand("Warding Talisman", "A talisman made of bones and wood. Protects you from attacks.")

WoodenShield = _offhand("Wooden Shield", "A sturdy wooden shield.")

TowerShield = _offhand("Tower Shield", "A massive iron shield.")

SpikedShield = _offhand("Spiked Shield", "A shield covered with spikes, both on the inside and outside.")

SpikedTowerShield = _offhand("Spiked Tower Shield", "A massive tower shield lined with cruel spikes. Only the hardy can wield it.")
