from player import Player
from console import console
from utility import min_max_number

def create_character():
    console.print("[bold yellow]=== Character Creator ===[/bold yellow]")

    name = input("Enter your name: ").strip()

    console.print("\nEach character has four attributes:")
    console.print("[red]Strength[/red] - primarly used for physical attacks")
    console.print("[yellow]Agility[/yellow] - primarly used for ranged attacks")
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

    console.print(f"Created new character: {player.name}")
    return player