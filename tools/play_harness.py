"""Deterministic play harness — drive the turn-based game one input at a time.

A terminal RPG normally needs an interactive TTY. This harness makes it
scriptable: each call appends the new input line(s) for this turn, replays the
*entire* session from the start under a fixed RNG seed, and prints only the
newly revealed screen. Because the seed is fixed, replays are reproducible, so
it doubles as a manual-testing and demo driver.

    python tools/play_harness.py --reset          # start a fresh session
    python tools/play_harness.py 3 Hero 5 1 1 3    # feed several inputs
    python tools/play_harness.py 1                 # feed one more input
    python tools/play_harness.py --pop 2           # rewind the last 2 inputs

State lives in two scratch files in the working directory (_inputs.txt records
the full input log; _prevlen.txt remembers how much output was already shown).
Both are gitignored. Delete them, or pass --reset, to start over.
"""
import sys
import os
import subprocess

INPUTS = "_inputs.txt"
PREVLEN = "_prevlen.txt"
SEED = 1234
LAUNCHER = f"import random; random.seed({SEED}); import main"
ENV = {**os.environ, "COLUMNS": "98", "PYTHONHASHSEED": "0"}


def _replay(record_len=True):
    inp = open(INPUTS).read() if os.path.exists(INPUTS) else ""
    res = subprocess.run(
        [sys.executable, "-c", LAUNCHER],
        input=inp, capture_output=True, text=True, env=ENV,
    )
    if record_len:
        with open(PREVLEN, "w") as f:
            f.write(str(len(res.stdout)))
    return res.stdout


def main(argv):
    if argv and argv[0] == "--reset":
        for f in (INPUTS, PREVLEN):
            if os.path.exists(f):
                os.remove(f)
        argv = argv[1:]

    # Rewind: drop the last N inputs and silently re-sync the game state.
    if argv and argv[0] == "--pop":
        n = int(argv[1])
        lines = open(INPUTS).read().splitlines() if os.path.exists(INPUTS) else []
        kept = lines[:-n] if n else lines
        with open(INPUTS, "w") as f:
            f.write("\n".join(kept) + ("\n" if kept else ""))
        _replay()
        return

    if argv:  # append this turn's input lines
        with open(INPUTS, "a") as f:
            for line in argv:
                f.write(line + "\n")

    prevlen = int(open(PREVLEN).read() or "0") if os.path.exists(PREVLEN) else 0
    out = _replay()
    # Fresh screen -> show everything; otherwise only the newly revealed suffix.
    sys.stdout.write(out if prevlen == 0 else out[prevlen:])


if __name__ == "__main__":
    main(sys.argv[1:])
