from console import console
from player_creator import create_character
from save_menu import save_menu, load_menu, delete_menu

def game_loop():
    console.print("Python Text RPG", style="bold red")
    
    while True:
        console.print("\nYou can quit with q, quit or exit")
        console.print("1. Load a game from a save slot.")
        console.print("2. Delete a game from a save slot.")
        console.print("3. Create a new character.")
        
        choice = input("> ").strip()
        
        match choice:
            case "1":
                load_menu()
            case "2":
                delete_menu()
            case "3":
                save_menu(create_character())
            case "quit" | "exit" | "q":
                console.print("Exiting.")
                break
            case _:
                console.print("Unknown command.")


game_loop()