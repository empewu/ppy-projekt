import random
from console import console
from utility import min_max_number
from items.base import Equipment

import items.helmet as helmet
import items.arms as arms
import items.legs as legs
import items.torso as torso
import items.mainhand as mainhand
import items.offhand as offhand
import items.rings as rings

BUY_RATE  = 1.1
SELL_RATE = 0.9

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

def generate_stock(size = 5):
    """Picks a random assortment of items from the pool."""
    return random.sample(TRADER_POOL, min(size, len(TRADER_POOL)))

def trader_menu(player):
    stock = generate_stock()

    while True:
        console.print(f"[bold yellow]=== Trader ===[/bold yellow]")
        console.print(f"\n[yellow]Gold: {player.gold}g[/yellow]")
        console.print("1. Buy")
        console.print("2. Sell")
        console.print("0. Leave")

        match min_max_number("> ", min_val=0, max_val=2):
            case 0:
                console.print("[dim]You leave the trader.[/dim]")
                return
            case 1:
                buy_menu(player, stock)
            case 2:
                sell_menu(player)

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
