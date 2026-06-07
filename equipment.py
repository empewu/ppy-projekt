"""Equipping items — shared by the hub inventory menu, the between-encounter
step during exploration, and the in-combat weapon swap.

Splitting this out of inventory.py lets gear be changed from anywhere that has a
player, without each caller re-implementing the attribute check, ring-slot
handling and swap-back-to-inventory logic.
"""
from console import console
from utility import min_max_number, apply_ring, remove_ring
from items.base import Equipment


def equip_from_inventory(player, item, confirm_swap=True):
    """Equip ``item`` (which must already be in ``player.inventory``) into its
    slot, moving any displaced item back to the inventory. Handles attribute
    requirements and the two ring slots. ``confirm_swap=False`` skips the
    "swap?" prompt for callers where the swap is already explicit (combat).

    Returns True if the item was equipped, False otherwise (requirement not met,
    or the player cancelled a swap prompt).
    """
    required = getattr(item, "attribute_required", None)
    if required is not None and player.statistics[required] < item.attribute_amount:
        console.print("[red]You do not have the necessary attributes to equip this item.[/red]")
        console.print(f"You require {item.attribute_amount} in {required}")
        return False

    if item.slot == "Ring":
        return _equip_ring(player, item)

    if player.equipment[item.slot] is not None:
        if confirm_swap:
            console.print("There is already an item equipped, do you want to swap the items? "
                          "(0 to cancel, 1 to continue)")
            if min_max_number("> ", min_val=0, max_val=1) == 0:
                return False
        player.inventory.append(player.equipment[item.slot])

    player.inventory.remove(item)
    player.equipment[item.slot] = item
    console.print(f"[dim]Equipped {item}.[/dim]")
    return True


def _equip_ring(player, ring):
    if player.equipment["Ring1"] is None:
        slot = "Ring1"
    elif player.equipment["Ring2"] is None:
        slot = "Ring2"
    else:
        console.print("Both ring slots are occupied.")
        console.print(f"Ring1: {player.equipment['Ring1'].name}")
        console.print(f"Ring2: {player.equipment['Ring2'].name}")
        console.print("Which slot to replace? (0 to cancel)")
        choice = min_max_number("> ", min_val=0, max_val=2)
        if choice == 0:
            return False
        slot = "Ring1" if choice == 1 else "Ring2"
        displaced = player.equipment[slot]
        remove_ring(player, displaced)
        player.inventory.append(displaced)

    player.inventory.remove(ring)
    player.equipment[slot] = ring
    apply_ring(player, ring)
    console.print(f"[dim]Equipped {ring}.[/dim]")
    return True


def _stat_hint(item):
    """A short '(14 dmg melee, 2 def)' style hint for the equip list."""
    bits = []
    if getattr(item, "damage", 0) > 0:
        dtype = getattr(item, "damage_type", None)
        bits.append(f"{item.damage} dmg{' ' + dtype if dtype else ''}")
    if getattr(item, "defence", 0) > 0:
        bits.append(f"{item.defence} def")
    return f" [dim]({', '.join(bits)})[/dim]" if bits else ""


def equip_menu(player, weapons_only=False, confirm_swap=True):
    """List equippable items and equip the chosen one. With ``weapons_only`` the
    list is limited to damage-dealing gear (used by the in-combat swap).

    Returns True if an item was actually equipped (so combat can charge the
    turn), False if there was nothing to equip or the player cancelled.
    """
    candidates = [
        it for it in player.inventory
        if isinstance(it, Equipment) and (not weapons_only or getattr(it, "damage", 0) > 0)
    ]
    if not candidates:
        console.print("[dim]You have no other weapons to equip.[/dim]" if weapons_only
                      else "[dim]You have nothing to equip.[/dim]")
        return False

    console.print("\nEquip which item? (0 to cancel)")
    for i, it in enumerate(candidates, 1):
        console.print(f"{i}. {it.name}{_stat_hint(it)}")
    choice = min_max_number("> ", min_val=0, max_val=len(candidates))
    if choice == 0:
        return False
    return equip_from_inventory(player, candidates[choice - 1], confirm_swap=confirm_swap)
