from console import console
from utility import min_max_number
from balance import RECIPES
from items import ITEM_REGISTRY

def _inventory_counts(player):
    counts = {}
    for item in player.inventory:
        counts[item.name] = counts.get(item.name, 0) + 1
    return counts

def _format_recipe(ingredients):
    return " + ".join(f"{name} x{count}" for name, count in ingredients.items())

def alchemy_menu(player):
    recipe_names = list(RECIPES.keys())
    # Every distinct ingredient used by any recipe, for the "you have" readout.
    ingredient_names = sorted({ing for r in RECIPES.values() for ing in r["ingredients"]})

    while True:
        counts = _inventory_counts(player)

        console.print("\n[bold yellow]=== Alchemy ===[/bold yellow]")
        have = ", ".join(f"{name} x{counts.get(name, 0)}" for name in ingredient_names)
        console.print(f"[dim]Ingredients: {have or 'none'}[/dim]")

        console.print("\n[bold]Craft which potion? (0 to cancel)[/bold]")
        for i, potion_name in enumerate(recipe_names, 1):
            ingredients = RECIPES[potion_name]["ingredients"]
            craftable = all(counts.get(name, 0) >= count for name, count in ingredients.items())
            tag = "[green]craftable[/green]" if craftable else "[dim]missing ingredients[/dim]"
            potion = ITEM_REGISTRY[potion_name]
            console.print(f"{i}. {potion_name} ({_format_recipe(ingredients)}) - {tag}")
            console.print(f"   [dim]{potion.description}[/dim]")
        console.print("0. Back")

        choice = min_max_number("> ", min_val=0, max_val=len(recipe_names))
        if choice == 0:
            return
        craft(player, recipe_names[choice - 1])

def craft(player, potion_name):
    ingredients = RECIPES[potion_name]["ingredients"]
    counts = _inventory_counts(player)

    if not all(counts.get(name, 0) >= count for name, count in ingredients.items()):
        console.print("[red]You don't have the ingredients for that.[/red]")
        return

    for name, count in ingredients.items():
        removed = 0
        for item in list(player.inventory):
            if item.name == name:
                player.inventory.remove(item)
                removed += 1
                if removed == count:
                    break

    player.inventory.append(ITEM_REGISTRY[potion_name])
    console.print(f"[bold green]You brew a {potion_name}![/bold green]")
