from console import console
from exceptions import PlayerDeadError
from balance import (
    STAT_DAMAGE_SCALING,
    ENDURANCE_DEFENCE,
    WEAKNESS_MULT,
    RESISTANCE_MULT,
    NEUTRAL_MULT,
    type_matches,
)
import random
import re

STAT_COLOURS = {
    "Strength": "red",
    "Agility": "yellow",
    "Intelligence": "blue",
    "Endurance": "green",
}

def min_max_number(prompt, min_val=None, max_val=None):
    """Used for inputting a number and checking if its between min_val and max_val."""
    while True:
        try:
            number = int(console.input(prompt))

            if min_val is not None and number < min_val:
                console.print(f"[red]Must be at least {min_val}[/red]")
                continue

            if max_val is not None and number > max_val:
                console.print(f"[red]Cannot be greater than {max_val}[/red]")
                continue

            return number

        except ValueError:
            console.print("[red]Please enter a number.[/red]")

def encounter_generator(location):
    """Yields one encounter at a time until the location is cleared."""
    encounters = location["encounters"]
    random.shuffle(encounters)
    
    for encounter in encounters:
        yield encounter

def roll_loot(loot_table):
    """Rolls through a loot table and returns items."""
    loot = []
    for item, chance in loot_table:
        if random.random() < chance:
            loot.append(item)
    return loot

#regex
def is_valid_name(name):
    return bool(re.match(r"^[a-zA-Z\s\-]{2,20}$", name))

#dekorator
#troche na siłe wsadzony
def require_alive(func):
    def wrapper(player, *args, **kwargs):
        if not player.is_alive():
            console.print("[bold red]You are dead![/bold red]")
            raise PlayerDeadError("Player is dead!")
        return func(player, *args, **kwargs)
    return wrapper

def apply_ring(player, ring):
    if ring.attribute_gained is not None:
        player.statistics[ring.attribute_gained] += ring.attribute_value
        player.recompute_max_health()

def remove_ring(player, ring):
    if ring.attribute_gained is not None:
        player.statistics[ring.attribute_gained] -= ring.attribute_value
        player.recompute_max_health()

def get_total_defence(player):
    """Defence from equipped gear plus the mitigation granted by Endurance."""
    total = 0
    for item in player.equipment.values():
        if item and hasattr(item, "defence"):
            total += item.defence
    total += player.statistics["Endurance"] * ENDURANCE_DEFENCE
    return total

def weapon_power(player, weapon):
    """Raw attack power of one equipped weapon, before any enemy is involved.

    A weapon's base damage is increased by its governing stat (if it has one);
    flat weapons such as talismans do not scale.
    """
    if not weapon or not hasattr(weapon, "damage") or weapon.damage <= 0:
        return 0
    power = weapon.damage
    stat = getattr(weapon, "governing_stat", None)
    if stat:
        power += player.statistics[stat] * STAT_DAMAGE_SCALING
    return power

def get_total_damage(player):
    """Total raw attack power across equipped weapons (neutral, no enemy).

    Used for the inventory's at-a-glance damage readout. Actual combat damage
    additionally applies type matchups and the enemy's defence.
    """
    total = 0
    for item in player.equipment.values():
        total += weapon_power(player, item)
    return total

def type_multiplier(damage_type, enemy):
    """Damage multiplier for an attack of ``damage_type`` against ``enemy``,
    based on the enemy's weakness/resistance (both optional)."""
    if type_matches(damage_type, getattr(enemy, "weakness", None)):
        return WEAKNESS_MULT
    if type_matches(damage_type, getattr(enemy, "resistance", None)):
        return RESISTANCE_MULT
    return NEUTRAL_MULT

def compute_attack_damage(player, enemy):
    """Damage the player deals to ``enemy`` this turn: each equipped weapon's
    power, adjusted for type matchup, summed, then reduced by enemy defence."""
    total = 0.0
    for item in player.equipment.values():
        power = weapon_power(player, item)
        if power:
            total += power * type_multiplier(getattr(item, "damage_type", None), enemy)
    return int(total * (100 / (100 + enemy.defence)))
