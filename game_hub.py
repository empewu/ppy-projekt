from console import console
from utility import min_max_number
from save_menu import save_menu
from inventory import inventory_menu
from exploration import exploration_menu
from exceptions import PlayerDeadError
from trader import trader_menu
from balance import HEAL_COST_PER_HP

def game_hub(player):
    while True:
        try:
            console.print(f"\n[bold yellow]=== {player.name} ===[/bold yellow]")
            console.print(f"[green]HP: {player.healthCurrent}/{player.healthMax}[/green] | [yellow]Gold: {player.gold}[/yellow]")
            console.print("\n[bold]What do you do?[/bold]")
            console.print("1. Explore.")
            console.print("2. Trader.")
            console.print("3. Inventory & Equipment.")
            console.print(f"4. Rest & Heal. [dim]({HEAL_COST_PER_HP}g per HP)[/dim]")
            console.print("5. Save.")
            console.print("0. Quit to main menu.")

            match min_max_number("> ", min_val=0, max_val=5):
                case 1:
                    pass
                    exploration_menu(player)
                case 2:
                    trader_menu(player)
                case 3:
                    inventory_menu(player)
                case 4:
                    heal_at_hub(player)
                case 5:
                    save_menu(player)
                case 0:
                    break
        
        except PlayerDeadError:
            console.print("\n[bold red]You have died...[/bold red]")
            console.input("[dim]Press Enter to continue[/dim]")
            return


def heal_at_hub(player):
    """Restore health for gold. Healing is no longer free, so gold (and the
    free in-dungeon rest sites) become a real part of attrition."""
    missing = player.healthMax - player.healthCurrent
    if missing <= 0:
        console.print("\n[dim]You are already at full health.[/dim]")
        return

    cost_full = missing * HEAL_COST_PER_HP
    if player.gold >= cost_full:
        player.gold -= cost_full
        player.heal()
        console.print(f"\nYou rest and [green]heal[/green] to full for [yellow]{cost_full}g[/yellow].")
        return

    affordable_hp = player.gold // HEAL_COST_PER_HP
    if affordable_hp <= 0:
        console.print("\n[red]You cannot afford any healing.[/red]")
        return

    player.gold -= affordable_hp * HEAL_COST_PER_HP
    player.heal(affordable_hp)
    console.print(
        f"\nYou can only afford to recover [green]{affordable_hp} HP[/green] "
        f"for [yellow]{affordable_hp * HEAL_COST_PER_HP}g[/yellow]."
    )
