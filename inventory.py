# inventory.py
from console import console
from utility import min_max_number, apply_ring, remove_ring, get_total_damage, get_total_defence, STAT_COLOURS
from items.base import Equipment

def inventory_menu(player):
    while True:
        console.print("\n[bold yellow]=== Inventory & Equipment ===[/bold yellow]")
        console.print("1. View Inventory")
        console.print("2. View Equipment")
        console.print("3. Equip Item")
        console.print("4. Show Statistics")
        console.print("0. Back")

        match min_max_number("> ", min_val=0, max_val=4):
            case 0:
                return
            case 1:
                show_inventory(player)
            case 2:
                show_equipment(player)
            case 3:
                equip_item(player)
            case 4:
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
    if not player.inventory:
        console.print("\n[dim]You have nothing to equip.[/dim]")
        return
    
    #list comprehension
    equippable_items = [item for item in player.inventory if isinstance(item, Equipment)]
    
    if not equippable_items:
        console.print("\n[dim]You have no equippable items.[/dim]")
        return

    console.print("\nEquip which item? (0 to cancel)")
    for i, item in enumerate(equippable_items, 1):
        console.print(f"{i}. {item.name}")
    choice = min_max_number("> ", min_val=0, max_val=len(equippable_items))
    if choice == 0:
        return
    item_equip = equippable_items[choice - 1]
    if hasattr(item_equip, "attribute_required"):
        if item_equip.attribute_required is not None:
            if player.statistics[item_equip.attribute_required] < item_equip.attribute_amount:
                console.print("[red]You do not have the necessary attributes to equip this item.[/red]")
                console.print(f"You require {item_equip.attribute_amount} in {item_equip.attribute_required}")
                return
    
    if item_equip.slot == "Ring":
        if player.equipment["Ring1"] is None:
            player.inventory.remove(item_equip)
            player.equipment["Ring1"] = item_equip
            apply_ring(player, item_equip)

        elif player.equipment["Ring2"] is None:
            player.inventory.remove(item_equip)
            player.equipment["Ring2"] = item_equip
            apply_ring(player, item_equip)
        
        else:
            console.print("Both ring slots are occupied.")
            console.print(f"Ring1: {player.equipment['Ring1'].name}")
            console.print(f"Ring2: {player.equipment['Ring2'].name}")
            console.print("Which slot to replace? (0 to cancel)")
            match min_max_number("> ", min_val=0, max_val=2):
                case 0:
                    return
                case 1:
                    remove_ring(player, player.equipment["Ring1"])
                    player.inventory.append(player.equipment["Ring1"])
                    player.inventory.remove(item_equip)
                    player.equipment["Ring1"] = item_equip
                    apply_ring(player, item_equip)

                case 2:
                    remove_ring(player, player.equipment["Ring2"])
                    player.inventory.append(player.equipment["Ring2"])
                    player.inventory.remove(item_equip)
                    player.equipment["Ring2"] = item_equip
                    apply_ring(player, item_equip)

    else:
        if player.equipment[item_equip.slot] is not None:
            console.print("There is already an item equipped, do you want to swap the items? (0 to cancel, 1 to continue)")
            match min_max_number("> ", min_val=0, max_val=2):
                case 0:
                    return
            player.inventory.append(player.equipment[item_equip.slot])
            player.inventory.remove(item_equip)
            player.equipment[item_equip.slot] = item_equip
        else:
            player.inventory.remove(item_equip)
            player.equipment[item_equip.slot] = item_equip

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
