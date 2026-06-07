"""Loader for balance.toml -- the single source of truth for tunable numbers.

This module is the *only* place that reads balance.toml. It parses the file
once at import, validates it, and re-exports plain Python values so the rest of
the codebase can simply ``from balance import WEAPONS, RING_BONUS`` and never
has to know a TOML file exists.

Optional per-item keys (such as a weapon's attribute requirement) are expressed
in TOML by omission; the ``*_kwargs`` helpers below fill in the defaults.
"""

import os
import tomllib

_PATH = os.path.join(os.path.dirname(__file__), "balance.toml")

with open(_PATH, "rb") as _f:
    _DATA = tomllib.load(_f)


# --- damage types ------------------------------------------------------------
MELEE = "melee"
RANGED = "ranged"
MAGIC = "magic"
PHYSICAL = "physical"  # shorthand for "melee and ranged" in weakness/resistance
_PHYSICAL_TYPES = {MELEE, RANGED}


# --- scalar parameters -------------------------------------------------------
STAT_DAMAGE_SCALING = _DATA["combat"]["stat_damage_scaling"]
ENDURANCE_DEFENCE = _DATA["combat"]["endurance_defence"]
WEAKNESS_MULT = _DATA["combat"]["multipliers"]["weakness"]
RESISTANCE_MULT = _DATA["combat"]["multipliers"]["resistance"]
NEUTRAL_MULT = _DATA["combat"]["multipliers"]["neutral"]

HP_BASE = _DATA["health"]["base"]
HP_PER_ENDURANCE = _DATA["health"]["per_endurance"]

TRADER_BUY_RATE = _DATA["economy"]["trader_buy_rate"]
TRADER_SELL_RATE = _DATA["economy"]["trader_sell_rate"]
TRADER_STOCK_SIZE = _DATA["economy"]["trader_stock_size"]
HEAL_COST_PER_HP = _DATA["economy"]["heal_cost_per_hp"]

RING_BONUS = _DATA["progression"]["ring_bonus"]

STARTING_GOLD = _DATA["creation"]["starting_gold"]
SAVE_VERSION = _DATA["save"]["version"]
STARTING_KITS = _DATA["kits"]


# --- entity stat tables (name -> dict of fields) -----------------------------
WEAPONS = _DATA["weapons"]
ARMOUR = _DATA["armour"]
RINGS = _DATA["rings"]
ENEMIES = _DATA["enemies"]
POTIONS = _DATA.get("potions", {})
RECIPES = _DATA.get("recipes", {})


# --- construction helpers ----------------------------------------------------
# These turn a stat-table entry into the keyword arguments the item/enemy
# constructors expect, filling defaults for omitted optional keys.

def weapon_kwargs(name):
    s = WEAPONS[name]
    return dict(
        value=s["value"],
        damage=s["damage"],
        defence=s["defence"],
        damage_type=s.get("type"),
        governing_stat=s.get("stat"),
        attribute_required=s.get("req_stat"),
        attribute_amount=s.get("req_amount", 0),
    )


def type_matches(damage_type, category):
    """True if an attack's ``damage_type`` falls under a weakness/resistance
    ``category`` (which may be a specific type or the "physical" shorthand)."""
    if category is None or damage_type is None:
        return False
    if category == PHYSICAL:
        return damage_type in _PHYSICAL_TYPES
    return damage_type == category


def armour_kwargs(name):
    s = ARMOUR[name]
    return dict(
        value=s["value"],
        defence=s["defence"],
        attribute_required=s.get("req_stat"),
        attribute_amount=s.get("req_amount", 0),
    )


def ring_kwargs(name):
    s = RINGS[name]
    return dict(
        value=s["value"],
        attribute_gained=s["attribute"],
        attribute_value=RING_BONUS,
    )


def enemy_kwargs(name):
    s = ENEMIES[name]
    return dict(
        health=s["health"],
        damage=s["damage"],
        defence=s["defence"],
        weakness=s.get("weakness"),
        resistance=s.get("resistance"),
    )


def potion_kwargs(name):
    s = POTIONS[name]
    return dict(
        description=s["description"],
        value=s["value"],
        effect=s["effect"],
        amount=s["amount"],
    )


# --- validation --------------------------------------------------------------
# Fail loudly at startup on a malformed balance.toml rather than silently
# breaking something mid-game.
_VALID_STATS = {"Strength", "Agility", "Intelligence", "Endurance"}
_VALID_TYPES = {MELEE, RANGED, MAGIC}
_VALID_EFFECTS = {"heal", "damage_buff", "defence_buff"}


def _validate():
    for name, s in WEAPONS.items():
        for key in ("damage", "defence", "value"):
            if key not in s:
                raise ValueError(f"balance.toml: weapon {name!r} missing '{key}'")
        if "req_stat" in s and s["req_stat"] not in _VALID_STATS:
            raise ValueError(f"balance.toml: weapon {name!r} has invalid req_stat {s['req_stat']!r}")
        if "type" in s and s["type"] not in _VALID_TYPES:
            raise ValueError(f"balance.toml: weapon {name!r} has invalid type {s['type']!r}")
        if "stat" in s and s["stat"] not in _VALID_STATS:
            raise ValueError(f"balance.toml: weapon {name!r} has invalid stat {s['stat']!r}")

    for name, s in ARMOUR.items():
        for key in ("defence", "value"):
            if key not in s:
                raise ValueError(f"balance.toml: armour {name!r} missing '{key}'")
        if "req_stat" in s and s["req_stat"] not in _VALID_STATS:
            raise ValueError(f"balance.toml: armour {name!r} has invalid req_stat {s['req_stat']!r}")

    for name, s in RINGS.items():
        if s.get("attribute") not in _VALID_STATS:
            raise ValueError(f"balance.toml: ring {name!r} has invalid attribute {s.get('attribute')!r}")

    for stat, names in STARTING_KITS.items():
        if stat not in _VALID_STATS:
            raise ValueError(f"balance.toml: kit key {stat!r} is not a valid attribute")
        if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
            raise ValueError(f"balance.toml: kit {stat!r} must be a list of item names")

    valid_matchups = _VALID_TYPES | {PHYSICAL}
    for name, s in ENEMIES.items():
        for key in ("health", "damage", "defence"):
            if key not in s:
                raise ValueError(f"balance.toml: enemy {name!r} missing '{key}'")
        for key in ("weakness", "resistance"):
            if key in s and s[key] not in valid_matchups:
                raise ValueError(f"balance.toml: enemy {name!r} has invalid {key} {s[key]!r}")

    for name, s in POTIONS.items():
        for key in ("description", "value", "effect", "amount"):
            if key not in s:
                raise ValueError(f"balance.toml: potion {name!r} missing '{key}'")
        if s["effect"] not in _VALID_EFFECTS:
            raise ValueError(f"balance.toml: potion {name!r} has invalid effect {s['effect']!r}")

    for name, r in RECIPES.items():
        if name not in POTIONS:
            raise ValueError(f"balance.toml: recipe {name!r} has no matching potion")
        ingredients = r.get("ingredients")
        if not ingredients or not all(isinstance(c, int) and c > 0 for c in ingredients.values()):
            raise ValueError(f"balance.toml: recipe {name!r} needs positive integer ingredient counts")


_validate()
