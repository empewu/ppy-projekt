"""Regression tests for the RPG.

Two layers:

  * Logic tests (deterministic, fast): use the game's real combat formulas to
    assert every representative build clears every enemy and that the boss stays
    winnable-but-not-trivial. These guard against a bad ``balance.toml`` edit.
  * I/O smoke test: drive ``main`` through a scripted stdin session under a
    fixed RNG seed and assert it starts, creates a character, and exits cleanly
    with no traceback. This guards against menu-flow / interface breakage.

Runs standalone (``python tests/test_playthrough.py``) and under pytest.
"""
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from tools.balance_sim import (
    BUILDS, ALL_ENEMIES, simulate_fight, expected_parts,
    potions_from_parts, boss_with_potions,
)
import enemies as E


# --- logic regressions -----------------------------------------------------
def test_all_builds_clear_all_enemies():
    """No build should lose a 1-on-1 to any enemy at full health."""
    for name, player in BUILDS.items():
        for enemy in ALL_ENEMIES:
            won, turns, _ = simulate_fight(player, enemy)
            assert won, f"{name} build LOSES to {enemy.name}"
            assert turns <= 8, f"{name} vs {enemy.name} drags on for {turns} turns"


def test_boss_is_winnable_without_potions():
    """Every build must beat the Golem unaided, but pay a real HP cost for it."""
    for name, player in BUILDS.items():
        won, turns, hp_end = simulate_fight(player, E.Golem)
        assert won, f"{name} cannot beat the boss"
        # 'real cost': the boss should take several turns and leave a dent.
        assert turns >= 3, f"{name} one-shots the boss in {turns} turns (too easy)"
        assert hp_end < player.healthMax, f"{name} beats the boss untouched"


def test_potions_help_but_do_not_trivialize_boss():
    """With the natural drop-gated supply, potions should improve the boss
    outcome without making it a walkover (still a multi-turn fight)."""
    pots = potions_from_parts(**expected_parts())
    for name, player in BUILDS.items():
        _, _, hp_no = simulate_fight(player, E.Golem)
        won, turns, hp_yes, _ = boss_with_potions(player, pots)
        assert won, f"{name} loses the boss even with potions"
        assert hp_yes >= hp_no, f"potions hurt {name} at the boss"
        assert turns >= 3, f"potions trivialize the boss for {name}"


def test_potion_supply_is_scarce():
    """The fight-long buffs must stay rate-limited by drops: a player should
    reach the boss with only a couple of Elixirs/Stoneskins, not a stack."""
    pots = potions_from_parts(**expected_parts())
    assert pots["Elixir"] <= 2, f"too many Elixirs available: {pots['Elixir']}"
    assert pots["Stoneskin"] <= 2, f"too many Stoneskins available: {pots['Stoneskin']}"


# --- I/O smoke test --------------------------------------------------------
def _run_game(stdin_lines, seed=1234):
    """Launch main with a scripted stdin under a fixed seed; return CompletedProcess."""
    launcher = f"import random; random.seed({seed}); import main"
    return subprocess.run(
        [sys.executable, "-c", launcher],
        input="\n".join(stdin_lines) + "\n",
        capture_output=True, text=True, cwd=REPO,
        env={**os.environ, "COLUMNS": "98", "PYTHONHASHSEED": "0"},
        timeout=60,
    )


def test_create_character_and_quit_cleanly():
    """A full create -> hub -> quit session must run without crashing."""
    # 3=new char, name, four stats, Enter past the intro, 0=quit hub, 0=quit game.
    res = _run_game(["3", "Tester", "5", "1", "1", "3", "", "0", "0"])
    assert res.returncode == 0, f"non-zero exit:\n{res.stderr}"
    assert "Traceback" not in res.stdout + res.stderr, f"crash:\n{res.stderr}"
    assert "Created new character: Tester" in res.stdout
    assert "=== Main Menu ===" in res.stdout


def test_launch_and_quit_immediately():
    """The bare main menu must render and exit on '0' with no input left over."""
    res = _run_game(["0"])
    assert res.returncode == 0, f"non-zero exit:\n{res.stderr}"
    assert "Traceback" not in res.stdout + res.stderr
    assert "Main Menu" in res.stdout


# --- standalone runner -----------------------------------------------------
def _main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
        except Exception as e:  # noqa: BLE001 - surface any unexpected error
            failed += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_main())
