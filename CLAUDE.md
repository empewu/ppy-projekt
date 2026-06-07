# CLAUDE.md

Guidance for working in this repository.

## What this is

A turn-based console RPG in Python (the UI strings are Polish; the code is
English). The player creates a character, explores locations, fights enemies in
a simple turn loop, manages an inventory/equipment, trades, crafts potions, and
saves/loads. Rendering uses [`rich`](https://github.com/Textualize/rich) via the
shared `console` object (`console.py`).

## Running and testing

```bash
python main.py                  # play the game
python tools/balance_sim.py     # balance report (reads live balance.toml)
python tests/test_playthrough.py    # regression tests (also pytest-compatible)
```

`main.py` calls `game_loop()` at import time, so importing it *starts the game*.
Tests and the sim therefore launch it in a subprocess, never by importing it.

## Architecture

The big idea: **all tunable numbers live in `balance.toml`**; Python reads them
through one loader and never hardcodes stats.

```
balance.toml   <- single source of truth for every number
   |
balance.py     <- loads + VALIDATES the toml; exposes constants and
   |               *_kwargs(name) helpers (weapon_kwargs, enemy_kwargs,
   |               potion_kwargs, ...). Fails loudly at startup on bad data.
   |
items/*.py     <- construct item objects from balance via the loader. Each
   |               module (mainhand, torso, rings, loot, potions, ...) holds
   |               item *identities*; their stats come from the toml.
items/__init__ <- builds ITEM_REGISTRY {name: object} from all item modules,
   |               and cross-checks crafting recipes against it.
enemies.py     <- enemy identities + loot tables (loot references item objects,
                   so it lives in code; stats come from balance via enemy_kwargs).
```

Gameplay modules sit on top of that data layer:

- `player.py` — `Player` (stats, HP, gold, inventory, equipment dict). Saves are
  by item *name* (`to_dict` / `from_save`), resolved through `ITEM_REGISTRY`.
  `SAVE_VERSION` gates a migration warning for pre-rebalance saves.
- `utility.py` — the **combat maths**: `compute_attack_damage` (weapon power +
  stat scaling, then type matchup, then enemy-defence mitigation),
  `get_total_defence` (gear + Endurance), `describe_matchup` (the weakness/
  resistance hint), `roll_loot`, the `require_alive` decorator, ring apply/remove.
- `combat.py` — the fight loop: Attack / Use Item / Swap Weapon / Flee. Using an
  item or swapping a weapon costs the turn (the enemy still strikes). Fight-scoped
  buffs (`damage_bonus`, `damage_reduction`) reset when the fight ends. Damage is
  recomputed from `player.equipment` each turn, so a mid-fight swap takes effect
  immediately.
- `consumables.py` — shared `grouped_consumables` / `apply_consumable` /
  `use_item_menu`, used by both combat and the inventory menu.
- `equipment.py` — shared `equip_from_inventory` / `equip_menu` (attribute check,
  ring slots, swap-back). Used by the hub inventory menu, the between-encounter
  step in `exploration.py`, and the in-combat weapon swap.
- `alchemy.py` — the hub crafting menu (consumes monster parts per `RECIPES`).
- `game_hub.py` — the main hub menu (Explore / Trader / Inventory / Rest /
  Alchemy / Save). `exploration.py`, `trader.py`, `inventory.py`, `save_menu.py`
  are the sub-menus. `locations.py` + `loot_table.py` define zones/encounters.
  The trader (`trader.py`) weights its stock toward gear the player can use and
  that fits their power tier, and offers a paid reroll (`trader_reroll_cost`).
- `driver.py` — `GameDriver` helper used by the menus for input loops.

## Combat model (so balance edits make sense)

- Damage dealt = sum over equipped weapons of `(base + governing_stat * scaling)`
  * type matchup (weakness ×, resistance ×, else neutral) * `100/(100+enemy.def)`.
- Damage taken = `enemy.damage * 100/(100 + get_total_defence(player))`, then
  consumable flat reductions, floored at 1. Defence is **percentile**, so flat
  per-hit reductions (e.g. Stoneskin) matter more than +defence at low enemy
  damage — keep that in mind when tuning defensive effects.
- Enemies have optional `weakness`/`resistance` damage types (melee/ranged/magic).

## How to add content

- **Item**: add a `[weapons."X"]` / `[armour."X"]` / etc. block to `balance.toml`,
  then one constructor line in the matching `items/<slot>.py`. The registry and
  saves pick it up automatically by name.
- **Potion**: add `[potions."X"]` (effect = `heal` / `damage_buff` /
  `defence_buff`) and `[recipes."X".ingredients]` in `balance.toml`, plus a line
  in `items/potions.py`. The loader validates the effect and recipe.
- **Enemy**: add `[enemies."X"]` to `balance.toml` and an entry + loot table in
  `enemies.py`.

After any balance edit, run `tools/balance_sim.py` and `tests/test_playthrough.py`.

## Conventions

- Never hardcode a stat in Python — put it in `balance.toml` and read it via the
  loader. The loader's `_validate()` is the safety net; extend it when you add a
  new data shape.
- `_*.py`, `_inputs.txt`, `_prevlen.txt` are local scratch (gitignored). The
  maintained dev tools are `tools/` and `tests/`.
- See `DESIGN_NOTES.md` for design rationale, balance findings, and the roadmap.
