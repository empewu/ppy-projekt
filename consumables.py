from console import console
from utility import min_max_number
from items.base import Consumable

def grouped_consumables(player):
    """Distinct consumables in the inventory with their counts, preserving order."""
    counts = {}
    order = []
    for item in player.inventory:
        if isinstance(item, Consumable):
            if item.name not in counts:
                counts[item.name] = [item, 0]
                order.append(item.name)
            counts[item.name][1] += 1
    return [(counts[name][0], counts[name][1]) for name in order]

def apply_consumable(player, item, in_combat=False):
    """Apply a consumable's effect.

    Returns (consumed, kind, amount, message):
      * consumed  - whether the item should be removed from the inventory
      * kind       - "heal" / "damage_buff" / "defence_buff" (for combat to act on)
      * amount     - the effect magnitude actually applied
    Healing works anywhere; combat buffs do nothing (and are not consumed)
    outside of combat.
    """
    if item.effect == "heal":
        before = player.healthCurrent
        player.heal(item.amount)
        gained = player.healthCurrent - before
        return (True, "heal", gained, f"[green]You drink the {item.name} and recover {gained} HP.[/green]")

    if item.effect in ("damage_buff", "defence_buff"):
        if not in_combat:
            return (False, None, 0, f"[dim]The {item.name} only has an effect in combat.[/dim]")
        if item.effect == "damage_buff":
            blurb = f"+{item.amount} damage"
        else:
            blurb = f"-{item.amount} damage taken"
        return (True, item.effect, item.amount,
                f"[green]You drink the {item.name}: {blurb} for this fight![/green]")

    return (False, None, 0, f"[dim]The {item.name} does nothing.[/dim]")

def use_item_menu(player, in_combat=False):
    """Let the player use a consumable. Returns (kind, amount) describing what
    was used (so combat can apply buffs), or None if nothing was used."""
    items = grouped_consumables(player)
    if not items:
        console.print("[dim]You have no usable items.[/dim]")
        return None

    console.print("\n[bold]Use which item?[/bold] (0 to cancel)")
    for i, (item, count) in enumerate(items, 1):
        console.print(f"{i}. {item.name} (x{count}) - {item.description}")

    choice = min_max_number("> ", min_val=0, max_val=len(items))
    if choice == 0:
        return None

    item, _ = items[choice - 1]
    consumed, kind, amount, message = apply_consumable(player, item, in_combat)
    console.print(message)
    if consumed:
        player.inventory.remove(item)
        return (kind, amount)
    return None
