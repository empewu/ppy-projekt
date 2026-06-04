import json
import os
from console import console
from player import Player

SAVE_DIR = "saves"

def get_save_path(slot):
    return os.path.join(SAVE_DIR, f"save_slot{slot}.json")

def save_game(player, slot):
    os.makedirs(SAVE_DIR, exist_ok=True)#
    with open(get_save_path(slot), "w") as f:
        json.dump(player.to_dict(), f, indent=4)
    console.print(f"Player named {player.name} saved to slot {slot}!")

def load_game(slot):
    path = get_save_path(slot)
    if not os.path.exists(path):
        console.print(f"No save found in slot {slot}.")
        return None
    with open(path, "r") as f:
        data = json.load(f)
    console.print(f"Succesfully loaded save file from slot {slot}.")
    return Player.from_save(data)


def get_save_info(slot):
    path = get_save_path(slot)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    return data

def delete_save(slot):
    path = get_save_path(slot)
    if os.path.exists(path):
        os.remove(path)
        print(f"Slot {slot} deleted.")
    else:
        print(f"No save in slot {slot}.")
