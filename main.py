from console import console
from player_creator import create_character
from save_menu import load_menu, delete_menu
from game_hub import game_hub

def game_loop():
    console.print("\nKonsolowa Gra RPG", style="bold red")
    
    while True:
        console.print("\n[bold yellow]=== Main Menu ===[/bold yellow]")
        console.print("1. Load a game from a save slot.")
        console.print("2. Delete a game from a save slot.")
        console.print("3. Create a new character. This will also start the game.")
        console.print("0. Quit the game.")
        
        choice = input("> ").strip()
        
        match choice:
            case "1":
                player = load_menu()
                if player is None:
                    continue
                game_hub(player)
            case "2":
                delete_menu()
            case "3":
                game_hub(create_character())
            case "0" | "quit" | "exit" | "q":
                console.print("[dim]Exiting...[/dim]")
                break
            case _:
                console.print("Unknown command.")

game_loop()
