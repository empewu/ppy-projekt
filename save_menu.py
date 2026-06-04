from saves import save_game, load_game, get_save_info, delete_save
from console import console
from utility import min_max_number

MAX_SLOTS = 3

def show_slots():
    console.print("\n[bold yellow]=== Save Slots ===[/bold yellow]")
    for slot in range(1, MAX_SLOTS + 1):
        info = get_save_info(slot)
        if info:
            console.print(f"[{slot}] {info['name']}")
        else:
            console.print(f"[{slot}] Empty")

def save_menu(player):
    show_slots()
    console.print("\n[bold]Save to which slot? (0 to cancel)[/bold]")
    slot = min_max_number("> ", min_val=0, max_val=MAX_SLOTS)

    if slot == 0:
        console.print("[red]Cancelled.[/red]")
        return

    save_game(player, slot)

def load_menu():
    show_slots()
    console.print("\n[bold]Load which slot? (0 to cancel)[/bold]")
    slot = min_max_number("> ", min_val=0, max_val=MAX_SLOTS)

    if slot == 0:
        console.print("[red]Cancelled.[/red]")
        return

    return load_game(slot)

def delete_menu():
    show_slots()
    console.print("\n[bold]Delete which slot? (0 to cancel)[/bold]")
    slot = min_max_number("> ", min_val=0, max_val=MAX_SLOTS)

    if slot == 0:
        console.print("[red]Cancelled.[/red]")
        return

    delete_save(slot)