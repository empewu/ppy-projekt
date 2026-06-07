# inventory.py
from console import console
from utility import min_max_number, get_total_damage, get_total_defence, STAT_COLOURS
from consumables import use_item_menu
from equipment import equip_menu

def inventory_menu(player):
    while True:
        console.print("\n[bold yellow]=== Inventory & Equipment ===[/bold yellow]")
        console.print("1. View Inventory")
        console.print("2. View Equipment")
        console.print("3. Equip Item")
        console.print("4. Use Item")
        console.print("5. Show Statistics")
        console.print("0. Back")

        match min_max_number("> ", min_val=0, max_val=5):
            case 0:
                return
            case 1:
                show_inventory(player)
            case 2:
                show_equipment(player)
            case 3:
                equip_item(player)
            case 4:
                use_item_menu(player, in_combat=False)
            case 5:
                show_stats(player)

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
    equip_menu(player)

def show_stats(player):
    #dict comprehension
    stats_display = {stat: value for stat, value in player.statistics.items()}
    for stat, value in stats_display.items():
        colour = STAT_COLOURS.get(stat, "white")
        console.print(f"[{colour}]{stat}[/{colour}]: {value}")
    
    console.print("[dim]Attributes affect whether or not you can equip an item. Certain items increase attributes.[/dim]")

    console.print(f"\nTotal Damage: {get_total_damage(player)}")
    console.print(f"Total Defence: {get_total_defence(player)}")
    console.print("[dim]Defence is percentile damage reduction to damage taken. Enemies also have defence.[/dim]")
