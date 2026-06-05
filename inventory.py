# inventory.py
from console import console
from utility import min_max_number

def inventory_menu(player):
    while True:
        console.print("\n[bold yellow]=== Inventory & Equipment ===[/bold yellow]")
        console.print("1. View Inventory")
        console.print("2. View Equipment")
        console.print("3. Equip Item")
        console.print("0. Back")

        match min_max_number("> ", min_val=0, max_val=3):
            case 0:
                return
            case 1:
                show_inventory(player)
            case 2:
                show_equipment(player)
            case 3:
                equip_item(player)

def show_inventory(player):
    console.print("\n[bold]Inventory:[/bold]")
    #lambda aby posortować ekwipunek
    player.inventory.sort(key=lambda item: item.value)
    if not player.inventory:
        console.print("[dim]Empty[/dim]")
        return
    for i, item in enumerate(player.inventory, 1):
        console.print(f"  {i}. {item}")

def show_equipment(player):
    console.print("\n[bold]Equipment:[/bold]")
    for slot, item in player.equipment.items():
        item_name = item if item else "[dim]Empty[/dim]"
        console.print(f"  {slot}: {item_name}")

def equip_item(player):
    show_inventory(player)
    if not player.inventory:
        return
    console.print("\nEquip which item? (0 to cancel)")
    choice = min_max_number("> ", min_val=0, max_val=len(player.inventory))
    if choice == 0:
        return
    item = player.inventory[choice - 1]
    console.print(f"Equip [bold]{item}[/bold] to which slot?")
    # slot selection logic here