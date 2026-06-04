from console import console
from utility import min_max_number, encounter_generator, roll_loot
from locations import LOCATIONS
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
    run_location(player, location)

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
                loot = roll_loot(encounter["loot"])
                if loot:
                    for item in loot:
                        player.inventory.append(item)
                        console.print(f"[green]You found: {item.name}![/green]")
                else:
                    console.print("[dim]You find nothing of note.[/dim]")

            case "rest":
                heal = player.healthMax // 3
                player.healthCurrent = min(player.healthMax, player.healthCurrent + heal)
                console.print(f"[green]You rest and recover {heal} HP.[/green]")

    if player.is_alive():
        console.print(f"\n[bold green]You cleared {location['name']}![/bold green]")