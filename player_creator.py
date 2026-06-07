from player import Player
from console import console
from utility import min_max_number, is_valid_name
from items import ITEM_REGISTRY
from balance import STARTING_KITS, STARTING_GOLD


def create_character():
    console.print("[bold yellow]=== Character Creator ===[/bold yellow]")

    console.print("[dim]Only letters, spaces and hyphens are allowed. A name must be 2-20 characters[/dim]")

    while True:
        name = input("Enter your name: ").strip()
        if(is_valid_name(name)):
            break
        console.print("[red]Invalid name.[/red]")


    console.print("\nEach character has four attributes:")
    console.print("[red]Strength[/red] - primarly used for melee physical attacks")
    console.print("[yellow]Agility[/yellow] - primarly used for ranged phyiscal attacks")
    console.print("[blue]Intelligence[/blue] - primarly used for magical attacks")
    console.print("[green]Endurance[/green] - determines your Health Points")
    console.print("Note, the attributes also affect other things, such as whether or not you can equip an item.")
    console.print("You have 10 attribute points to distribute. Each attribute has a minimum value of 1 and a maximum value of 5.")
    Strength = 0
    Agility = 0
    Intelligence = 0
    Endurance = 0
    while(True):
        statSum = 0
        Strength = min_max_number("[red]Strength[/red]: ", min_val=1, max_val=5)
        statSum += Strength
        Agility = min_max_number("[yellow]Agility[/yellow]: ", min_val=1, max_val=5)
        statSum += Agility
        Intelligence = min_max_number("[blue]Intelligence[/blue]: ", min_val=1, max_val=5)
        statSum += Intelligence
        Endurance = min_max_number("[green]Endurance[/green]: ", min_val=1, max_val=5)
        statSum += Endurance        
        if(statSum > 10):
            console.print("\n[bold red]Attribute sum over 10, you only have 10 attribute points to distribute[/bold red]")
            continue
        break

    player = Player(name, Strength, Agility, Intelligence, Endurance)
    player.gold = STARTING_GOLD

    #lambda do sprawdzenia
    #który atrybut jest największy
    highest = max(player.statistics, key=lambda stat: player.statistics[stat])

    # Starting kit is data-driven (balance.toml [kits]); items are resolved
    # from the registry by their display name.
    for item_name in STARTING_KITS[highest]:
        player.inventory.append(ITEM_REGISTRY[item_name])

    console.print(f"Created new character: {player.name}")
    console.print("\n[dim]Each new character stands with items in their inventory based on their attributes.[/dim]")
    console.print("[dim]Make sure to equip them before exploring.[/dim]")
    console.input("[dim]Press Enter to continue[/dim]")
    return player

