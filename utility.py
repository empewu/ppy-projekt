from console import console

def min_max_number(prompt, min_val=None, max_val=None):
    while True:
        try:
            number = int(console.input(prompt))

            if min_val is not None and number < min_val:
                console.print(f"[red]Must be at least {min_val}[/red]")
                continue

            if max_val is not None and number > max_val:
                console.print(f"[red]Cannot be greater than {max_val}[/red]")
                continue

            return number

        except ValueError:
            console.print("[red]Please enter a number.[/red]")