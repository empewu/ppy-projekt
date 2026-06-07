import random
from console import console
from utility import min_max_number
from items.base import Equipment
from balance import (
    TRADER_BUY_RATE as BUY_RATE,
    TRADER_SELL_RATE as SELL_RATE,
    TRADER_STOCK_SIZE,
    TRADER_REROLL_COST,
)

import items.helmet as helmet
import items.arms as arms
import items.legs as legs
import items.torso as torso
import items.mainhand as mainhand
import items.offhand as offhand
import items.rings as rings

def get_all_items_from_module(module):
    return [
        obj for obj in vars(module).values()
        if isinstance(obj, Equipment) and obj is not None
    ]

TRADER_POOL = (
    get_all_items_from_module(helmet) +
    get_all_items_from_module(arms) +
    get_all_items_from_module(legs) +
    get_all_items_from_module(torso) +
    get_all_items_from_module(mainhand) +
    get_all_items_from_module(offhand) +
    get_all_items_from_module(rings)
)

def _dominant_stats(player):
    """The attribute(s) the character is built around (ties included)."""
    best = max(player.statistics.values())
    return {stat for stat, value in player.statistics.items() if value == best}


def _player_tier(player):
    """Average value of equipped gear -- a proxy for how far the character has
    progressed. Used to bias stock toward upgrades over outgrown junk."""
    values = [it.value for it in player.equipment.values() if it]
    return sum(values) / len(values) if values else 0.0


def _item_stat(item):
    """The attribute an item is 'about': a weapon's governing stat, a ring's
    granted attribute, or an armour piece's requirement."""
    return (getattr(item, "governing_stat", None)
            or getattr(item, "attribute_gained", None)
            or getattr(item, "attribute_required", None))


def _can_equip(player, item):
    req = getattr(item, "attribute_required", None)
    return req is None or player.statistics[req] >= item.attribute_amount


def _stock_weight(player, item, tier, dominant):
    """Relative likelihood of an item appearing in stock. Combines relevance
    (can you use it / does it match your build) with tiering (is it near your
    current power, or outgrown junk / a touch aspirational)."""
    weight = 3.0 if _can_equip(player, item) else 0.3   # usable gear dominates
    if _item_stat(item) in dominant:
        weight *= 2.0                                    # matches the build's focus
    if tier > 0:
        ratio = item.value / tier
        if ratio < 0.4:
            weight *= 0.15                               # well below tier -- outgrown junk
        elif ratio < 0.7:
            weight *= 0.5                                # a bit below your level
        elif ratio > 2.5:
            weight *= 0.6                                # far ahead -- rare, hunt via reroll
    return weight


def generate_stock(player, size=TRADER_STOCK_SIZE):
    """A weighted assortment biased toward gear this character can use and that
    fits their current power tier. Weighted sampling without replacement via the
    Efraimidis-Spirakis (A-Res) key ``random() ** (1/weight)``."""
    dominant = _dominant_stats(player)
    tier = _player_tier(player)
    ranked = sorted(
        TRADER_POOL,
        key=lambda it: random.random() ** (1.0 / _stock_weight(player, it, tier, dominant)),
        reverse=True,
    )
    return ranked[:min(size, len(TRADER_POOL))]

def trader_menu(player):
    # Reuse the player's standing stock; only generate a fresh assortment when
    # there is none (a new game, or after the last exploration cleared it).
    if player.trader_stock is None:
        player.trader_stock = generate_stock(player)

    while True:
        console.print(f"[bold yellow]=== Trader ===[/bold yellow]")
        console.print(f"\n[yellow]Gold: {player.gold}g[/yellow]")
        console.print("1. Buy")
        console.print("2. Sell")
        console.print(f"3. Reroll stock ([yellow]{TRADER_REROLL_COST}g[/yellow])")
        console.print("0. Leave")

        match min_max_number("> ", min_val=0, max_val=3):
            case 0:
                console.print("[dim]You leave the trader.[/dim]")
                return
            case 1:
                buy_menu(player, player.trader_stock)
            case 2:
                sell_menu(player)
            case 3:
                if player.gold < TRADER_REROLL_COST:
                    console.print("[red]Not enough gold to reroll.[/red]")
                else:
                    player.gold -= TRADER_REROLL_COST
                    player.trader_stock = generate_stock(player)
                    console.print("[green]The trader clears the table and lays out fresh wares.[/green]")

def buy_menu(player, stock):
    stock.sort(key=lambda item: item.value)
    while True:

        console.print(f"\n[bold]=== Buy ===[/bold]")
        console.print(f"[yellow]Gold: {player.gold}g[/yellow]")

        for i, item in enumerate(stock, 1):
            console.print(f"{i}. {item.name} - [yellow]{int(item.value * BUY_RATE)}g[/yellow] | {item.description}")
        console.print("0. Back")

        choice = min_max_number("> ", min_val=0, max_val=len(stock))
        if choice == 0:
            return

        item = stock[choice - 1]
        if player.gold < int(item.value * BUY_RATE):
            console.print("[red]Not enough gold![/red]")
        else:
            player.gold -= int(item.value * BUY_RATE)
            player.inventory.append(item)
            console.print(f"Bought {item.name} for [yellow]{int(item.value * BUY_RATE)}g[/yellow]!")

def sell_menu(player):
    player.inventory.sort(key=lambda item: item.value)
    while True:
        if not player.inventory:
            console.print("[dim]Your inventory is empty.[/dim]")
            return


        console.print(f"\n[bold yellow]=== Sell ===[/bold yellow]")
        console.print(f"[yellow]Gold: {player.gold}g[/yellow]")
        for i, item in enumerate(player.inventory, 1):
            console.print(f"{i}. {item.name} - [yellow]{int(item.value * SELL_RATE)}g[/yellow] | {item.description}")
        console.print("0. Back")

        choice = min_max_number("> ", min_val=0, max_val=len(player.inventory))
        if choice == 0:
            return

        item = player.inventory[choice - 1]
        earned = int(item.value * SELL_RATE)
        player.gold += earned
        player.inventory.remove(item)
        console.print(f"Sold {item.name} for [yellow]{earned}g[/yellow]!")
