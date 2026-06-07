#!/usr/bin/env python3
"""Drive the text RPG (``main.py``) programmatically over pipes.

The game is a synchronous, menu-driven console app. Running it as a child
process with piped stdin/stdout lets us script it reliably -- far more robust
than poking a detached background process through a FIFO.

:class:`GameDriver` provides the low-level primitives (send a menu choice, wait
for a prompt, read the current menu); the module-level helpers build
task-level actions (load a save, shop the trader, equip an item) on top of it.

Run directly for a small demo that loads a save and prints its character sheet::

    python3 driver.py [slot]   # slot defaults to 1
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import threading
import time

GAME_DIR = os.path.dirname(os.path.abspath(__file__))


class GameDriver:
    """Spawn ``main.py`` and talk to it over stdin/stdout.

    Usable as a context manager so the child process is always cleaned up::

        with GameDriver() as game:
            load_game(game, slot=1)
            ...
    """

    def __init__(self, cwd: str = GAME_DIR):
        self._proc = subprocess.Popen(
            ["python3", "-u", "main.py"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, bufsize=1, cwd=cwd,
        )
        self._buf = ""
        self._lock = threading.Lock()
        threading.Thread(target=self._pump, daemon=True).start()

    # -- context manager ------------------------------------------------
    def __enter__(self) -> "GameDriver":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        try:
            self._proc.terminate()
            self._proc.wait(timeout=3)
        except Exception:
            self._proc.kill()

    # -- low-level I/O --------------------------------------------------
    def _pump(self) -> None:
        """Background thread: accumulate the game's output as it arrives."""
        for ch in iter(lambda: self._proc.stdout.read(1), ""):
            with self._lock:
                self._buf += ch

    def snapshot(self) -> str:
        """Return everything the game has printed since the last :meth:`clear`."""
        with self._lock:
            return self._buf

    def clear(self) -> None:
        with self._lock:
            self._buf = ""

    def send(self, choice: str) -> None:
        self._proc.stdin.write(f"{choice}\n")
        self._proc.stdin.flush()

    def expect(self, marker: str, timeout: float = 15) -> bool:
        """Block until ``marker`` appears in the output, or the game exits."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if marker in self.snapshot():
                return True
            if self._proc.poll() is not None:
                return False
            time.sleep(0.03)
        return False

    def act(self, choice: str, wait: str, timeout: float = 15) -> bool:
        """Clear the buffer, send a menu ``choice``, wait for the next prompt.

        This is the workhorse for menu navigation: clearing first means
        :meth:`expect` only sees output produced by *this* choice.
        """
        self.clear()
        self.send(choice)
        return self.expect(wait, timeout)

    def option_index(self, name: str, anchor: str | None = None) -> str | None:
        """Return the number of the menu entry for ``name`` (e.g. ``"3"``).

        Numbered menus look like ``"3. Iron Sword - 40g | ..."`` or simply
        ``"1. Iron Sword"``. If ``anchor`` is given, only the text after its
        last occurrence is searched -- handy when the same word appears earlier
        in the scrollback.
        """
        text = self.snapshot()
        if anchor:
            text = text[text.rfind(anchor):]
        match = re.search(rf"^\s*(\d+)\.\s+{re.escape(name)}\b", text, re.M)
        return match.group(1) if match else None


# ---------------------------------------------------------------------------
# Task-level helpers, built on the GameDriver primitives.
# ---------------------------------------------------------------------------

def load_game(game: GameDriver, slot: int = 1) -> bool:
    """From the main menu, load the save in ``slot``. Returns success."""
    if not game.expect("Quit the game"):
        return False
    game.act("1", "Load which slot")        # 1. Load a game
    return game.act(str(slot), "What do you do?")


def buy_items(game: GameDriver, wanted, max_rolls: int = 60) -> dict:
    """Re-roll the trader until every name in ``wanted`` has been bought.

    The trader restocks each visit, so we leave and re-enter to refresh the
    shelves. Returns ``{item_name: roll_number}`` for everything purchased.
    """
    wanted = list(wanted)
    bought: dict = {}
    game.act("2", "1. Buy")                 # enter Trader
    game.act("1", "0. Back")                # open Buy
    for roll in range(1, max_rolls + 1):
        for name in wanted:
            if name in bought:
                continue
            idx = game.option_index(name, anchor="=== Buy ===")
            if idx:
                game.clear()
                game.send(idx)
                if game.expect("Bought"):
                    bought[name] = roll
                    game.expect("0. Back")  # buy menu reprints
        if len(bought) == len(wanted):
            break
        # leave and re-enter to reroll the stock
        game.act("0", "1. Buy")             # Buy -> Trader menu
        game.act("0", "What do you do?")    # Trader -> hub
        game.act("2", "1. Buy")             # hub -> Trader
        game.act("1", "0. Back")            # Trader -> Buy (fresh stock)
    game.act("0", "1. Buy")                 # leave the trader
    game.act("0", "What do you do?")
    return bought


def equip_item(game: GameDriver, name: str) -> bool:
    """Equip ``name`` from the inventory, confirming any swap/replace prompt."""
    if not game.act("3", "Equip Item"):     # hub -> Inventory & Equipment
        return False
    if not game.act("3", "Equip which item"):  # -> Equip list
        return False
    idx = game.option_index(name, anchor="Equip which item")
    if idx is None:
        game.act("0", "What do you do?")
        return False
    game.clear()
    game.send(idx)
    if game.expect("swap the items", timeout=2):        # armor slot occupied
        game.send("1")
    elif game.expect("Which slot to replace", timeout=2):  # both rings occupied
        game.send("1")
    game.expect("Equipped")
    game.act("0", "What do you do?")         # back to hub
    return True


def character_sheet(game: GameDriver) -> str:
    """Return the raw text of the stats screen (from the hub)."""
    game.act("3", "Equip Item")             # Inventory & Equipment
    game.act("4", "Total Defence")          # Statistics
    sheet = game.snapshot()
    game.act("0", "What do you do?")
    return sheet


def save_game(game: GameDriver, slot: int = 1) -> bool:
    game.act("5", "Save to which slot")
    return game.act(str(slot), "saved to slot")


def quit_game(game: GameDriver) -> None:
    """Return to the main menu and quit the game cleanly."""
    if game.expect("What do you do?", timeout=2):
        game.act("0", "Quit the game")      # hub -> main menu
    game.send("0")                          # main menu -> quit


def main(argv) -> int:
    slot = int(argv[1]) if len(argv) > 1 else 1
    with GameDriver() as game:
        if not load_game(game, slot):
            print(f"Could not load slot {slot}.", file=sys.stderr)
            return 1
        sheet = character_sheet(game)
        quit_game(game)

    keys = ("Strength", "Agility", "Intelligence", "Endurance",
            "Total Damage", "Total Defence")
    print(f"=== Character sheet (slot {slot}) ===")
    for line in sheet.splitlines():
        if any(k in line for k in keys):
            print(line.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
