from utility import roll_loot, min_max_number, require_alive, compute_attack_damage, get_total_defence, describe_matchup
from consumables import use_item_menu
from equipment import equip_menu
from console import console
from exceptions import PlayerDeadError
import copy

@require_alive
def start_combat(player, enemy):
    enemy = copy.copy(enemy)
    console.print(f"\n[bold red]A {enemy.name} appears![/bold red]")

    matchup = describe_matchup(player, enemy)
    if matchup:
        console.print(matchup)

    # Buffs from potions last only the current fight.
    damage_bonus = 0       # Elixir of Power: flat bonus to damage dealt
    damage_reduction = 0   # Stoneskin Draught: flat reduction to damage taken

    while player.is_alive() and enemy.health > 0:
        console.print(f"\n[green]Your HP: {player.healthCurrent}/{player.healthMax}[/green]")
        console.print(f"[red]{enemy.name} HP: {enemy.health}[/red]")
        console.print("1. Attack")
        console.print("2. Use Item")
        console.print("3. Swap Weapon")
        console.print("4. Flee")

        match min_max_number("> ", min_val=1, max_val=4):
            case 1:
                player_strike(player, enemy, damage_bonus)
                if enemy.health <= 0:
                    break
                enemy_strike(player, enemy, damage_reduction)
            case 2:
                used = use_item_menu(player, in_combat=True)
                if used is None:
                    continue  # nothing used -> the turn is not spent
                kind, amount = used
                if kind == "damage_buff":
                    damage_bonus += amount
                elif kind == "defence_buff":
                    damage_reduction += amount
                # Using an item costs your turn: the enemy still strikes.
                if enemy.health > 0:
                    enemy_strike(player, enemy, damage_reduction)
            case 3:
                if not equip_menu(player, weapons_only=True, confirm_swap=False):
                    continue  # no swap -> the turn is not spent
                # Show how the new weapon fares, then pay the turn.
                matchup = describe_matchup(player, enemy)
                if matchup:
                    console.print(matchup)
                if enemy.health > 0:
                    enemy_strike(player, enemy, damage_reduction)
            case 4:
                console.print("[yellow]You flee![/yellow]")
                return "flee"

    if not player.is_alive():
        raise PlayerDeadError("Player has died in combat.")

    console.print(f"[bold green]You defeated the {enemy.name}![/bold green]")
    give_loot(player, enemy)
    return "victory"

def player_strike(player, enemy, damage_bonus=0):
    damage_dealt = compute_attack_damage(player, enemy) + damage_bonus
    enemy.health -= damage_dealt
    console.print(f"You deal [red]{damage_dealt}[/red] damage to {enemy.name}.")

def enemy_strike(player, enemy, damage_reduction=0):
    damage_taken = int(enemy.damage * (100 / (100 + get_total_defence(player))))
    # Stoneskin Draught reduces each hit by a flat amount (always leaves a chip).
    damage_taken = max(1, damage_taken - damage_reduction)
    player.healthCurrent -= damage_taken
    console.print(f"{enemy.name} deals [red]{damage_taken}[/red] damage to you.")

def give_loot(player, enemy):
    dropped = roll_loot(enemy.loot_table)
    if not dropped:
        console.print("[dim]The enemy dropped nothing.[/dim]")
        return

    console.print("\n[bold yellow]=== Loot ===[/bold yellow]")
    for item in dropped:
        player.inventory.append(item)
        console.print(f"[green]+ {item.name}[/green] - {item.description}")
