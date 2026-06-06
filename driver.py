#!/usr/bin/env python3
"""Self-contained controller: spawns the RPG, loads slot 1, hunts the trader for
defensive gear, equips it, saves, and exits. Synchronous over pipes -> robust."""
import subprocess, threading, time, re, sys

CWD = "/home/user/ppy-projekt"
proc = subprocess.Popen(["python3", "-u", "main.py"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, bufsize=1, cwd=CWD)
buf = ""
lock = threading.Lock()

def _reader():
    global buf
    for ch in iter(lambda: proc.stdout.read(1), ""):
        with lock:
            buf += ch
threading.Thread(target=_reader, daemon=True).start()

def snap():
    with lock:
        return buf

def clear():
    global buf
    with lock:
        buf = ""

def wait_for(sub, timeout=15):
    end = time.time() + timeout
    while time.time() < end:
        if sub in snap():
            return True
        if proc.poll() is not None:
            return False
        time.sleep(0.03)
    return False

def send(x):
    proc.stdin.write(x + "\n")
    proc.stdin.flush()

def last_buy_block():
    s = snap()
    i = s.rfind("=== Buy ===")
    return s[i:] if i >= 0 else ""

def stock_index(block, name):
    m = re.search(r"^(\d+)\.\s+" + re.escape(name) + r"\s+-\s", block, re.M)
    return m.group(1) if m else None

TARGETS = ["Copper Plate", "Iron Gauntlets", "Iron Greaves"]
got = {t: False for t in TARGETS}
log = []

# --- main menu -> load slot 1 ---
if not wait_for("Quit the game"):
    print("ERR: no main menu"); sys.exit(1)
clear(); send("1")                      # Load a game
wait_for("Load which slot")
clear(); send("1")                      # slot 1
if not wait_for("What do you do?"):
    print("ERR: load failed:\n", snap()[-400:]); sys.exit(1)
log.append("Loaded slot 1.")

# --- enter trader buy ---
clear(); send("2"); wait_for("1. Buy")
clear(); send("1"); wait_for("0. Back")

ROLLS = 60
for r in range(1, ROLLS + 1):
    blk = last_buy_block()
    for name in TARGETS:
        if got[name]:
            continue
        idx = stock_index(blk, name)
        if idx:
            clear(); send(idx)
            if wait_for("Bought"):
                got[name] = True
                log.append(f"Bought {name} (roll {r}).")
                wait_for("0. Back")     # buy menu reprints
                blk = last_buy_block()
    if all(got.values()):
        break
    # re-roll: buy -> back -> leave -> hub -> trader -> buy
    clear(); send("0"); wait_for("1. Buy")        # trader menu
    clear(); send("0"); wait_for("What do you do?")  # hub
    clear(); send("2"); wait_for("1. Buy")        # trader
    clear(); send("1"); wait_for("0. Back")       # buy (new stock)

# leave trader -> hub
clear(); send("0"); wait_for("1. Buy")
clear(); send("0"); wait_for("What do you do?")

# --- equip the acquired pieces (by name; swap-confirm where needed) ---
def equip_by_name(name):
    clear(); send("3"); wait_for("Equip Item")        # inventory menu
    clear(); send("3"); wait_for("Equip which item")  # equip list
    blk = snap()[snap().rfind("Equip which item"):]
    m = re.search(r"^(\d+)\.\s+" + re.escape(name) + r"\s*$", blk, re.M)
    if not m:
        log.append(f"Could not find {name} to equip."); return
    clear(); send(m.group(1))
    # may prompt to swap
    if wait_for("swap the items", timeout=3):
        clear(); send("1")
    wait_for("Equipped")
    log.append(f"Equipped {name}.")
    clear(); send("0"); wait_for("What do you do?")   # back to hub

# enter inventory menu fresh each time via hub
for name in TARGETS:
    if got[name]:
        # open inventory&equipment from hub
        clear(); send("3"); wait_for("Equip Item")
        clear(); send("3"); wait_for("Equip which item")
        blk = snap()[snap().rfind("Equip which item"):]
        m = re.search(r"^(\d+)\.\s+" + re.escape(name) + r"\s*$", blk, re.M)
        if not m:
            log.append(f"Could not find {name} in equip list.");
            clear(); send("0"); wait_for("What do you do?"); continue
        clear(); send(m.group(1))
        if wait_for("swap the items", timeout=3):
            clear(); send("1")
        wait_for("Equipped")
        log.append(f"Equipped {name}.")
        clear(); send("0"); wait_for("What do you do?")

# --- show stats ---
clear(); send("3"); wait_for("Equip Item")
clear(); send("4"); wait_for("Total Defence")
stats = snap()
clear(); send("0"); wait_for("What do you do?")

# --- save to slot 1 ---
clear(); send("5"); wait_for("Save to which slot")
clear(); send("1"); wait_for("saved to slot 1")

# --- quit cleanly ---
clear(); send("0"); wait_for("Quit the game")
send("0")
time.sleep(0.5)
proc.terminate()

print("==== ACTION LOG ====")
print("\n".join(log))
print("\n==== FINAL STATS ====")
for line in stats.splitlines():
    if any(k in line for k in ("Strength","Agility","Intelligence","Endurance","Total Damage","Total Defence")):
        print(line.strip())
