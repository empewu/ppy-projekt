# Projekt PPY - Konsolowa Gra RPG
1. Zamysł
2. Jak Uruchomić
3. Kod

## Zamysł

Gra polega na utworzeniu postaci, w zależności od atrybutów dostaje się różne startowe przedmioty.
Końca gry nie ma, gra się aż się komuś znudzi, 
Są cztery lokalizacje, każda ma różnych przeciwników oraz różne szanse na zdobywany łup.
Oryginalnie gra miała posiadać końcowego bossa w każdej lokalizacji, 

### Inspiracje

Różne gry w które grałem, ale głównie. CRPGi i podobne, gry posiadające ekwipunek i specyficzne sloty na ekwipunek.
Np. większość gier MMORPG (WoW, SWtOR) coś takiego ma.

## Jak Uruchomić

Gra wymaga biblioteki [**Rich**](https://github.com/textualize/rich)
Oraz wersji **Python 3.10** lub nowszej.

Oczywiście można zainstalować poprzez:
```bash
pip install rich
```

Aby uruchomić grę, należy znajdować się w folderze projektu i uruchomić plik main.py, np. poprzez:
```bash
python main.py
```

## Kod

Porozmieszczałem komentarze tam gdzie uważałem, że będą przydatne przy np. ocenianiu projektu.
Do chwalenia się tutaj zbytnio nie ma, chyba, ale napewno pochwaliłbym się plikiem ```utility.py``` gdzie znajduję się kilka przydotnych metod używanych wszędzie w projekcie, w tym głównie używaną funkcją ```min_max_number```:

```python
def min_max_number(prompt, min_val=None, max_val=None):
    """Used for inputting a number and checking if its between min_val and max_val."""
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
```

