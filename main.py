from console import console
from player_creator import create_character

def game_loop():
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
                create_character()
            case "quit" | "exit" | "q":
                console.print("Exiting.")
                break
            case _:
                console.print("Unknown command.")


game_loop()