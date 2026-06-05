from console import console
from utility import min_max_number
from save_menu import save_menu
from inventory import inventory_menu
from exploration import exploration_menu
from exceptions import PlayerDeadError
from trader import trader_menu

def game_hub(player):
    while True:
        try:
            console.print(f"\n[bold yellow]=== {player.name} ===[/bold yellow]")
            console.print(f"[green]HP: {player.healthCurrent}/{player.healthMax}[/green] | [yellow]Gold: {player.gold}[/yellow]")
            console.print("\n[bold]What do you do?[/bold]")
            console.print("1. Explore.")
            console.print("2. Trader.")
            console.print("3. Inventory & Equipment.")
            console.print("4. Rest & Heal.")
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
                    console.print("\nYou use the time to rest and [green]heal[/green] your wounds.")
                    player.heal()
                    console.print("[dim]Health has been restored to max.[/dim]")
                case 5:
                    save_menu(player)
                case 0:
                    break
        
        except PlayerDeadError:
            console.print("\n[bold red]You have died...[/bold red]")
            console.input("[dim]Press Enter to continue[/dim]")
            return
