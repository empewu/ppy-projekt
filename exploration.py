from console import console
from utility import min_max_number, encounter_generator, roll_loot, require_alive
from locations import LOCATIONS
from loot_table import LOCATION_REST_LOOT
from combat import start_combat

def exploration_menu(player):
    console.print("\n[bold yellow]=== Explore ===[/bold yellow]")
    for key, loc in LOCATIONS.items():
        console.print(f"{key}. {loc['name']} - {loc['description']}")
    console.print("0. Back")

    choice = min_max_number("> ", min_val=0, max_val=len(LOCATIONS))
    if choice == 0:
        return

    location = LOCATIONS[choice]

    #set comprehension
    enemy_types = {encounter["enemy"].name for encounter in location["encounters"] if encounter["type"] == "combat"}
    console.print(f"[dim]You might encounter: {', '.join(enemy_types)}[/dim]")
    console.input("[dim]Press Enter to continue[/dim]")

    run_location(player, location)

    # Travelling refreshes what the trader has on offer next time.
    player.trader_stock = None

@require_alive
def run_location(player, location):
    console.print(f"\n[bold]You enter the {location['name']}...[/bold]")
    
    gen = encounter_generator(location)

    for encounter in gen:
        if not player.is_alive():
            break

        console.print("\n[dim]You press deeper...[/dim]")
        console.input("[dim]Press Enter to continue[/dim]")

        match encounter["type"]:
            case "combat":
                result = start_combat(player, encounter["enemy"])
                if result == "flee":
                    console.print("[yellow]You retreat from the location.[/yellow]")
                    return

            case "treasure":
                console.print("You encounter a site of interest.")
                loot = roll_loot(encounter["loot"])
                if loot:
                    for item in loot:
                        player.inventory.append(item)
                        console.print(f"[green]You found: {item.name}![/green]")
                else:
                    console.print("[dim]You find nothing of note.[/dim]")

            case "rest":
                console.print("You encounter a campsite. Choose whether to [green]rest[/green] or [yellow]scavenge[/yellow] for valuables.")
                console.print("1. Rest")
                console.print("2. Scavenge")

                match min_max_number("> ", min_val=1, max_val=2):
                    case 1:
                        healing = player.healthMax // 3
                        player.heal(healing)
                        console.print(f"[green]You rest and recover {healing} HP.[/green]")
                    case 2:
                        loot = roll_loot(LOCATION_REST_LOOT[location["name"]])
                        if loot:
                            for item in loot:
                                player.inventory.append(item)
                                console.print(f"[green]You found: {item.name}![/green]")
                        else:
                            console.print("[dim]You find nothing of note.[/dim]")

    if player.is_alive():
        console.print(f"\n[bold green]You cleared {location['name']}![/bold green]")
