from console import console
import random

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
