from utility import roll_loot, min_max_number
from console import console
from exceptions import PlayerDeadError

def start_combat(player, enemy):
    console.print(f"\n[bold red]A {enemy.name} appears![/bold red]")

    while player.is_alive() and enemy.health > 0:
        console.print(f"\n[green]Your HP: {player.healthCurrent}/{player.healthMax}[/green]")
        console.print(f"[red]{enemy.name} HP: {enemy.health}[/red]")
        console.print("1. Attack")
        console.print("2. Flee")

        match min_max_number("> ", min_val=1, max_val=2):
            case 1:
                attack(player, enemy)
            case 2:
                console.print("[yellow]You flee![/yellow]")
                return "flee"

    if not player.is_alive():
        raise PlayerDeadError("Player has died in combat.")

    console.print(f"[bold green]You defeated the {enemy.name}![/bold green]")
    give_loot(player, enemy)
    return "victory"

def attack(player, enemy):
    damage_dealt = (get_total_damage(player) * (100 / 100 + enemy.defence))
    enemy.health -= damage_dealt
    console.print(f"You deal [red]{damage_dealt}[/red] damage to {enemy.name}.")

    if enemy.health <= 0:
        return

    damage_taken = (enemy.damage * (100 / 100 + get_total_defence(player)))
    player.healthCurrent -= damage_taken
    console.print(f"{enemy.name} deals [red]{damage_taken}[/red] damage to you.")

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

def give_loot(player, enemy):
    dropped = roll_loot(enemy.loot_table)
    if not dropped:
        console.print("[dim]The enemy dropped nothing.[/dim]")
        return

    console.print("\n[bold yellow]=== Loot ===[/bold yellow]")
    for item in dropped:
        player.inventory.append(item)
        console.print(f"[green]+ {item.name}[/green] - {item.description}")
