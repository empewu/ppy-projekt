from rich import print
from rich.console import Console


def game_loop():
    console = Console()
    console.print("Python Text RPG", style="bold red")
    
    while True:
        console.print("\nYou can quit with q, quit or exit")
        console.print("1. Load character")
        console.print("2. Create new character")
        
        choice = input("> ").strip()
        
        match choice:
            case "1":
                console.print("Not implemented.")
            case "2":
                console.print("Not implemented.")
            case "quit" | "exit" | "q":
                console.print("Exiting.")
                break
            case _:
                console.print("Unknown command.")


game_loop()