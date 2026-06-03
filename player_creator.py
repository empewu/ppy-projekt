from player import Player
from console import console


def create_character():
    console.print("[bold yellow]Character Creator[/bold yellow]")

    name = input("Enter your name: ").strip()

    console.print("\nEach character has four attributes, :")
    console.print("[red]Strength[/red] - primarly used for physical attacks")
    console.print("[yellow]Agility[/yellow] - primarly used for ranged attacks")
    console.print("[blue]Intelligence[/blue] - primarly used for magical attacks")
    console.print("[green]Endurance[/green] - determines your Health Points")
    console.print("Note, the attributes also affect other things, such as whether or not you can equip an item.")
    Strength = 0
    Agility = 0
    Intelligence = 0
    Endurance = 0
    while(True):
        statSum = 0
        
        if(statSum > 20):
            console.print("\n[bold red]Attribute sum over 20, you only have 20 attribute points to distribute[/bold red]")
            continue
        break

    player = Player(name)

    console.print(f"\Created new character: {player.name}")
    return player