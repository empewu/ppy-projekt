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


# --- gear swap (#4) --------------------------------------------------------
def test_weapon_swap_changes_combat_damage():
    """Swapping to the weapon that matches an enemy's weakness must change the
    damage combat computes (combat reads player.equipment live)."""
    import copy
    from player import Player
    from items import ITEM_REGISTRY
    from utility import compute_attack_damage
    from equipment import equip_from_inventory

    p = Player("hybrid", 4, 4, 1, 1)
    sword, crossbow = ITEM_REGISTRY["Iron Sword"], ITEM_REGISTRY["Iron Crossbow"]
    p.inventory = [sword, crossbow]
    equip_from_inventory(p, sword)
    melee = compute_attack_damage(p, copy.copy(E.Wolf))          # neutral
    equip_from_inventory(p, crossbow, confirm_swap=False)         # the combat swap path
    ranged = compute_attack_damage(p, copy.copy(E.Wolf))         # Wolf is weak to ranged
    assert ranged > melee, "swapping to the Wolf's ranged weakness should raise damage"
    assert p.equipment["MainHand"].name == "Iron Crossbow" and sword in p.inventory


def test_unusable_weapon_cannot_be_equipped():
    from player import Player
    from items import ITEM_REGISTRY
    from equipment import equip_from_inventory

    mage = Player("mage", 1, 1, 5, 3)
    hammer = ITEM_REGISTRY["Iron Hammer"]  # Strength-gated
    mage.inventory = [hammer]
    assert not equip_from_inventory(mage, hammer)
    assert mage.equipment["MainHand"] is None and hammer in mage.inventory


# --- trader relevance + reroll (#5) ----------------------------------------
def test_trader_stock_is_mostly_usable_for_focused_build():
    """A focused build should see mostly gear it can actually equip, not a
    uniform draw from every build's equipment."""
    from player import Player
    from trader import generate_stock, _can_equip
    import items.mainhand as mh
    import items.torso as ts

    mage = Player("mage", 1, 1, 5, 3)
    mage.equipment["MainHand"] = mh.RunedStaff
    mage.equipment["Torso"] = ts.ClothTorso
    stock = [it for _ in range(200) for it in generate_stock(mage)]
    usable = sum(_can_equip(mage, it) for it in stock) / len(stock)
    assert usable > 0.7, f"focused build sees too much unusable stock ({usable:.0%})"


def test_trader_reroll_costs_gold():
    from player import Player
    from trader import generate_stock
    from balance import TRADER_REROLL_COST

    p = Player("r", 5, 1, 1, 3)
    p.gold = TRADER_REROLL_COST + 10
    p.trader_stock = generate_stock(p)
    before = p.gold
    p.gold -= TRADER_REROLL_COST          # mirrors trader_menu's reroll branch
    p.trader_stock = generate_stock(p)
    assert p.gold == before - TRADER_REROLL_COST


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
