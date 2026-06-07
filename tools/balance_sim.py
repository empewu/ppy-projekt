"""Balance simulation for the RPG.

Reads the live game balance (``balance.toml`` via the game's own modules) and
reports, for representative character builds:

  * per-enemy combat outcomes (turns to kill, HP lost, win/lose),
  * the boss fight with and without a realistic potion supply,
  * the drop-gated potion economy a player reaches the boss with.

Run it after editing ``balance.toml`` to check that every build stays viable,
that no single enemy is a wall, and that the boss is winnable but not trivial.

    python tools/balance_sim.py

Nothing here is imported by the game; it only *reads* the game's modules, so it
always reflects the current balance numbers.
"""
import copy
import os
import sys

# Allow running from anywhere: put the repo root on the path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from player import Player
from utility import compute_attack_damage, get_total_defence
from balance import RECIPES, POTIONS
from locations import LOCATIONS
from loot_table import LOCATION_REST_LOOT
import enemies as E
import items.mainhand as mh
import items.offhand as oh
import items.helmet as hl
import items.torso as ts
import items.arms as ar
import items.legs as lg

# --- builds ----------------------------------------------------------------
# Each build is (stats, [equipped items]) at a "boss-ready" gear tier. Stats are
# (Strength, Agility, Intelligence, Endurance).
def _make(stats, items):
    p = Player("sim", *stats)
    for it in items:
        slot = "Ring1" if it.slot == "Ring" else it.slot
        p.equipment[slot] = it
    return p

BUILDS = {
    "Strength": _make((5, 1, 1, 3),
        [mh.IronSword, hl.IronHelmet, ts.IronTorso, ar.IronGloves, lg.IronBoots]),
    "Agility": _make((1, 5, 1, 3),
        [mh.IronCrossbow, hl.LeatherHood, ts.LeatherTorso, ar.LeatherGloves, lg.LeatherBoots]),
    "Intelligence": _make((1, 1, 5, 3),
        [mh.RunedStaff, oh.MagicalTalisman, hl.ClothHood, ts.ClothTorso, ar.ClothGloves, lg.ClothBoots]),
    "Tank": _make((2, 1, 2, 5),
        [mh.SpikedClub, oh.SpikedShield, hl.WardenHelm, ts.WardenPlate, ar.WardenGauntlets, lg.WardenGreaves]),
}

ALL_ENEMIES = [E.Goblin, E.Spider, E.Wolf, E.Slime, E.Skeleton, E.Wraith, E.Ghoul, E.Golem]


# --- core combat model -----------------------------------------------------
def simulate_fight(player, enemy, hp=None, damage_bonus=0, damage_reduction=0):
    """Resolve a fight with the game's real damage formulas. Returns
    (won, turns, hp_end). Mirrors combat.py: player strikes first each round,
    a slain enemy does not counterattack."""
    e = copy.copy(enemy)
    hp = player.healthMax if hp is None else hp
    dealt = compute_attack_damage(player, e) + damage_bonus
    taken = max(1, int(e.damage * (100 / (100 + get_total_defence(player)))) - damage_reduction)
    turns = 0
    while e.health > 0 and hp > 0:
        e.health -= dealt
        turns += 1
        if e.health <= 0:
            break
        hp -= taken
    return hp > 0, turns, max(hp, 0)


# --- potion economy --------------------------------------------------------
_PART_TIER = {"Monster Parts": "common", "Rare Monster Parts": "rare", "Magical Monster Parts": "magical"}

def expected_parts():
    """Expected monster parts after clearing the three non-boss zones."""
    exp = {"common": 0.0, "rare": 0.0, "magical": 0.0}
    def add(table):
        for item, chance in table:
            if item.name in _PART_TIER:
                exp[_PART_TIER[item.name]] += chance
    for loc_id in (1, 3, 4):  # Dark Forest, Dark Cave, Misty Swamp
        loc = LOCATIONS[loc_id]
        for enc in loc["encounters"]:
            if enc["type"] == "combat":
                add(enc["enemy"].loot_table)
            elif enc["type"] == "treasure":
                add(enc["loot"])
        add(LOCATION_REST_LOOT[loc["name"]])
    return exp

def potions_from_parts(common, rare, magical):
    """Greedy craft split: magical -> Elixirs, rare+common -> Stoneskins,
    leftovers -> Health potions."""
    elixirs = int(magical)
    stoneskins = min(int(rare), int(common))
    return {
        "Elixir": elixirs,
        "Stoneskin": stoneskins,
        "Health": int(common) - stoneskins,
    }

def _amount(effect):
    for s in POTIONS.values():
        if s["effect"] == effect:
            return s["amount"]
    return 0


# --- boss fight with potions -----------------------------------------------
def boss_with_potions(player, stock):
    """Boss fight using a reasonable opening: one Stoneskin, up to two Elixirs,
    then attack (each potion costs a turn -> one boss hit)."""
    e = copy.copy(E.Golem)
    hp = player.healthMax
    taken_base = int(e.damage * (100 / (100 + get_total_defence(player))))
    dmg_bonus = 0
    reduction = 0
    turns = 0
    used = []
    if stock.get("Stoneskin", 0) > 0 and taken_base > 1:
        reduction += _amount("defence_buff"); used.append("Stoneskin")
        hp -= max(1, taken_base - reduction); turns += 1
    for _ in range(min(2, stock.get("Elixir", 0))):
        dmg_bonus += _amount("damage_buff"); used.append("Elixir")
        hp -= max(1, taken_base - reduction); turns += 1
    won, t, hp_end = simulate_fight(player, E.Golem, hp=hp,
                                    damage_bonus=dmg_bonus, damage_reduction=reduction)
    return won, turns + t, hp_end, used


# --- report ----------------------------------------------------------------
def main():
    print("=" * 74)
    print("BALANCE SIMULATION  (reads live balance.toml)")
    print("=" * 74)

    for name, p in BUILDS.items():
        print(f"\n## {name}  (HP {p.healthMax}, defence {get_total_defence(p)})")
        print(f"   {'enemy':10} {'dmg/turn':>9} {'taken/turn':>11} {'turns':>6} {'HP left':>8}  result")
        for enemy in ALL_ENEMIES:
            dealt = compute_attack_damage(p, enemy)
            taken = max(1, int(enemy.damage * (100 / (100 + get_total_defence(p)))))
            won, turns, hp_end = simulate_fight(p, enemy)
            flag = "ok" if won else "*** LOSS ***"
            print(f"   {enemy.name:10} {dealt:>9} {taken:>11} {turns:>6} "
                  f"{hp_end:>4}/{p.healthMax:<3} {flag}")

    # potion economy + boss comparison
    exp = expected_parts()
    pots = potions_from_parts(exp["common"], exp["rare"], exp["magical"])
    print("\n" + "=" * 74)
    print("POTION ECONOMY  (expected supply at the boss)")
    print("=" * 74)
    print(f"  expected parts: common {exp['common']:.1f}, rare {exp['rare']:.1f}, "
          f"magical {exp['magical']:.1f}")
    print(f"  craftable: {pots['Elixir']} Elixir, {pots['Stoneskin']} Stoneskin, "
          f"{pots['Health']} Health\n")
    print(f"  {'build':12} {'boss no potions':>18} {'boss w/ potions':>18}   used")
    for name, p in BUILDS.items():
        _, t0, h0 = simulate_fight(p, E.Golem)
        w1, t1, h1, used = boss_with_potions(p, pots)
        print(f"  {name:12} {f'{t0}t  {h0}/{p.healthMax} HP':>18} "
              f"{f'{t1}t  {h1}/{p.healthMax} HP':>18}   {'+'.join(used) or '-'}")

    print("\n" + "=" * 74)
    print("Sanity checks: every 'result' above should read 'ok' (all builds clear")
    print("every enemy), and the boss should be won in both columns but with a")
    print("real HP cost -- potions should soften it, not trivialize it.")
    print("=" * 74)


if __name__ == "__main__":
    main()
