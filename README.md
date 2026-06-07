# Projekt PPY — Konsolowa Gra RPG

Tekstowe RPG działające w terminalu. Tworzysz postać, eksplorujesz lokacje,
walczysz z potworami w turowym systemie walki, zbierasz łup, handlujesz,
warzysz mikstury i rozwijasz ekwipunek. Interfejs jest po polsku, kod po
angielsku.

## Zamysł

Gra polega na przechodzeniu przez lokacje, pokonywaniu potworów i zbieraniu
łupu. Zaczyna się od stworzenia postaci — w zależności od rozdanych atrybutów
dostaje się inny zestaw startowy i gra się zupełnie inaczej. Sztywnego końca nie
ma: gra się, dopóki gracz nie ulegnie potworom albo się nie znudzi. Są cztery
lokacje, każda z innymi przeciwnikami i innymi szansami na łup. Rolę bossa pełni
**Golem** w Starożytnych Ruinach — neutralny na wszystkie typy obrażeń, więc jest
realnym sprawdzianem dla każdego builda.

Pierwotnie każda lokacja miała mieć własnego bossa; ostatecznie zostało przy
jednym, mocnym przeciwniku, bo to wystarcza, a system słabości/odporności i tak
daje walce wymaganą głębię.

### Inspiracje

Różne gry, w które grałem — głównie cRPG-i i tytuły z rozbudowanym ekwipunkiem
oraz konkretnymi slotami na przedmioty (jak większość MMORPG: WoW, SWTOR).

## Co oferuje gra

### Tworzenie postaci i buildy
Rozdajesz **10 punktów** na cztery atrybuty (każdy 1–5):

| Atrybut | Rola |
| --- | --- |
| **Strength** (Siła) | obrażenia broni do walki wręcz (*melee*) |
| **Agility** (Zręczność) | obrażenia broni dystansowej (*ranged*) |
| **Intelligence** (Inteligencja) | obrażenia magiczne (*magic*) |
| **Endurance** (Wytrzymałość) | punkty zdrowia oraz redukcja otrzymywanych obrażeń |

Atrybut dominujący wyznacza zestaw startowy, a wszystkie cztery prowadzą do
sensownych, grywalnych buildów (wojownik, łucznik, mag, „tank”).

### Walka
Turowy system z trzema akcjami: **Atak / Użyj przedmiotu / Ucieczka**.

- Obrażenia broni rosną wraz z jej atrybutem przewodnim (np. miecz skaluje się
  Siłą), a następnie są modyfikowane przez **typ obrażeń** i obronę przeciwnika.
- Każdy przeciwnik może mieć **słabość** (×1.3 obrażeń) i/lub **odporność**
  (×0.7) na dany typ. Gdy potwór się pojawia, gra wyświetla czytelną podpowiedź
  zależną od **aktualnie założonej broni** — np. „*Pająk jest podatny na Twoje
  ataki melee!*” albo „*Slime jest odporny na Twoje ataki melee.*”. Przy
  neutralnym starciu nie ma żadnej podpowiedzi.
- Obrona jest procentowa (`100 / (100 + obrona)`) i pochodzi z pancerza oraz z
  Wytrzymałości.

### Alchemia i mikstury
Części potworów wypadające z przeciwników to składniki — w hubie znajdziesz
menu **Alchemia**, w którym warzysz mikstury:

| Mikstura | Działanie | Składniki |
| --- | --- | --- |
| Health Potion | leczy 20 HP | 1× Monster Parts |
| Greater Health Potion | leczy 45 HP | 2× Rare Monster Parts |
| Elixir of Power | +12 obrażeń do końca walki | 1× Magical Monster Parts |
| Stoneskin Draught | −4 do każdego otrzymanego ciosu do końca walki | 1× Rare + 1× Monster Parts |

Użycie przedmiotu w walce **kosztuje turę** (przeciwnik i tak uderza), więc
leczenie i wzmocnienia to decyzja taktyczna, a nie darmowy reset. Wzmocnienia
działają tylko do końca danej walki.

### Eksploracja, handel i zapisy
- **Cztery lokacje** (Mroczny Las, Starożytne Ruiny, Mroczna Jaskinia, Mglista
  Topiel) z napotkaniami: walki, skarby oraz obozowiska (odpoczynek = leczenie
  albo przeszukanie = łup).
- **Handlarz** kupuje i sprzedaje ekwipunek; jego oferta odświeża się po każdej
  eksploracji (nie da się jej darmowo „przerollować”).
- **Sloty ekwipunku**: głowa, tors, ręce, nogi, broń główna, broń pomocnicza i
  dwa pierścienie.
- **Zapis/wczytywanie** do slotów (pliki JSON) z wersjonowaniem zapisów.

## Jak uruchomić

Gra wymaga **Pythona 3.11 lub nowszego** (loader korzysta z modułu `tomllib` z
biblioteki standardowej) oraz biblioteki [**Rich**](https://github.com/textualize/rich):

```bash
pip install rich
```

Następnie, będąc w katalogu projektu:

```bash
python main.py
```

Sterowanie odbywa się przez wpisywanie numerów opcji z menu i zatwierdzanie
Enterem.

## Architektura

Główna idea: **wszystkie strojone liczby znajdują się w `balance.toml`**, a
Python czyta je przez jeden loader i nigdzie nie zaszywa wartości na sztywno.

```
balance.toml   ->  jedyne źródło prawdy dla wszystkich liczb
balance.py     ->  wczytuje i WALIDUJE toml; udostępnia stałe i pomocnicze
                   funkcje *_kwargs(name) (weapon_kwargs, enemy_kwargs, ...)
items/*.py     ->  budują obiekty przedmiotów na podstawie balance
items/__init__ ->  tworzy ITEM_REGISTRY {nazwa: obiekt} i sprawdza receptury
enemies.py     ->  tożsamości przeciwników + tabele łupów
```

Na tej warstwie danych stoją moduły rozgrywki: `player.py`, `utility.py`
(matematyka walki), `combat.py`, `consumables.py`, `alchemy.py`, `game_hub.py`
oraz menu (`exploration.py`, `trader.py`, `inventory.py`, `save_menu.py`).
Renderowanie idzie przez wspólny obiekt `console` (Rich).

Dodanie zawartości sprowadza się zwykle do wpisu w `balance.toml` plus jednej
linijki konstruktora w odpowiednim module. Szczegóły i pełen opis warstw są w
[`CLAUDE.md`](CLAUDE.md), a uzasadnienia decyzji projektowych i wnioski
balansowe — w [`DESIGN_NOTES.md`](DESIGN_NOTES.md).

## Struktura projektu

```
main.py             punkt wejścia (menu główne)
balance.toml        wszystkie strojone liczby
balance.py          loader + walidacja balance.toml
player.py           klasa Player (statystyki, HP, ekwipunek, zapisy)
utility.py          matematyka walki, łup, dekoratory, pomocnicze
combat.py           turowa pętla walki
consumables.py      używanie mikstur (walka i ekwipunek)
alchemy.py          menu warzenia mikstur
game_hub.py         główne menu huba
exploration.py      eksploracja lokacji
trader.py           handlarz
inventory.py        ekwipunek i statystyki
save_menu.py        zapis/wczytywanie/usuwanie
saves.py            serializacja zapisów
enemy.py/enemies.py przeciwnicy i ich łup
locations.py        lokacje i napotkania
loot_table.py       tabele łupów lokacji
items/              definicje przedmiotów (wg slotów) + rejestr
tools/              narzędzia deweloperskie (poniżej)
tests/              testy regresyjne (poniżej)
```

## Narzędzia deweloperskie

```bash
python tools/balance_sim.py        # raport balansu (czyta żywy balance.toml)
python tests/test_playthrough.py   # testy regresyjne (działają też pod pytest)
```

- `tools/balance_sim.py` — symuluje walki dla reprezentatywnych buildów i
  raportuje, czy każdy build daje radę każdemu przeciwnikowi oraz jak wygląda
  walka z bossem (z miksturami i bez). Uruchamiaj po każdej zmianie
  `balance.toml`.
- `tests/test_playthrough.py` — deterministyczne testy logiki (każdy build
  pokonuje każdego przeciwnika; boss jest do pokonania, ale nie trywialny) plus
  „dymny” test wejścia/wyjścia uruchamiający `main` ze skryptowanym wejściem.
- `tools/play_harness.py` — deterministyczny, zaseedowany sterownik do
  prowadzenia gry po jednym wejściu (testy ręczne / demonstracje).

## Kod

Komentarze są tam, gdzie uznałem je za przydatne. Najchętniej pochwaliłbym się
plikiem `utility.py` — zbiera metody używane w całym projekcie, w tym główną
funkcję walidującą wejście, `min_max_number`:

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
