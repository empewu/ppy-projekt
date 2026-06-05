from console import console
from exceptions import PlayerDeadError
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

def remove_ring(player, ring):
    if ring.attribute_gained is not None:
        player.statistics[ring.attribute_gained] -= ring.attribute_value

def get_total_defence(player):
    """Adds up defence from all equipped items."""
    total = 0
    for item in player.equipment.values():
        if item and hasattr(item, "defence"):
            total += item.defence
    return total

def get_total_damage(player):
    """Adds up damage from all equipped items."""
    total = 0
    for item in player.equipment.values():
        if item and hasattr(item, "damage"):
            total += item.damage
    return total
