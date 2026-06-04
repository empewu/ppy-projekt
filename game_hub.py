from console import console
from utility import min_max_number
from save_menu import save_menu
from inventory import inventory_menu

def game_hub(player):
    while player.is_alive():
        console.print(f"\n[bold yellow]=== {player.name} ===[/bold yellow]")
        console.print(f"[green]HP: {player.healthCurrent}/{player.healthMax}[/green] | [yellow]Gold: {player.gold}[/yellow]")
        console.print("\n[bold]What do you do?[/bold]")
        console.print("1. Explore")
        console.print("2. Trader")
        console.print("3. Inventory & Equipment")
        console.print("4. Save & Quit")

        match min_max_number("> ", min_val=1, max_val=4):
            case 1:
                pass
                #explore_menu(player)
            case 2:
                pass
                #trader_menu(player)
            case 3:
                inventory_menu(player)
            case 4:
                save_menu(player)
                break