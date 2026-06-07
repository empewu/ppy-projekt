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


# --- scalar parameters -------------------------------------------------------
HP_BASE = _DATA["health"]["base"]
HP_PER_ENDURANCE = _DATA["health"]["per_endurance"]

TRADER_BUY_RATE = _DATA["economy"]["trader_buy_rate"]
TRADER_SELL_RATE = _DATA["economy"]["trader_sell_rate"]
TRADER_STOCK_SIZE = _DATA["economy"]["trader_stock_size"]

RING_BONUS = _DATA["progression"]["ring_bonus"]


# --- entity stat tables (name -> dict of fields) -----------------------------
WEAPONS = _DATA["weapons"]
ARMOUR = _DATA["armour"]
RINGS = _DATA["rings"]
ENEMIES = _DATA["enemies"]


# --- construction helpers ----------------------------------------------------
# These turn a stat-table entry into the keyword arguments the item/enemy
# constructors expect, filling defaults for omitted optional keys.

def weapon_kwargs(name):
    s = WEAPONS[name]
    return dict(
        value=s["value"],
        damage=s["damage"],
        defence=s["defence"],
        attribute_required=s.get("req_stat"),
        attribute_amount=s.get("req_amount", 0),
    )


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
    )


# --- validation --------------------------------------------------------------
# Fail loudly at startup on a malformed balance.toml rather than silently
# breaking something mid-game.
_VALID_STATS = {"Strength", "Agility", "Intelligence", "Endurance"}


def _validate():
    for name, s in WEAPONS.items():
        for key in ("damage", "defence", "value"):
            if key not in s:
                raise ValueError(f"balance.toml: weapon {name!r} missing '{key}'")
        if "req_stat" in s and s["req_stat"] not in _VALID_STATS:
            raise ValueError(f"balance.toml: weapon {name!r} has invalid req_stat {s['req_stat']!r}")

    for name, s in ARMOUR.items():
        for key in ("defence", "value"):
            if key not in s:
                raise ValueError(f"balance.toml: armour {name!r} missing '{key}'")
        if "req_stat" in s and s["req_stat"] not in _VALID_STATS:
            raise ValueError(f"balance.toml: armour {name!r} has invalid req_stat {s['req_stat']!r}")

    for name, s in RINGS.items():
        if s.get("attribute") not in _VALID_STATS:
            raise ValueError(f"balance.toml: ring {name!r} has invalid attribute {s.get('attribute')!r}")

    for name, s in ENEMIES.items():
        for key in ("health", "damage", "defence"):
            if key not in s:
                raise ValueError(f"balance.toml: enemy {name!r} missing '{key}'")


_validate()
