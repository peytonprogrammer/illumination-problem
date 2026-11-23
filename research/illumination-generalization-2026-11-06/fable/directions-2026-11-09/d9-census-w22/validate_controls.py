"""Lit controls for the complete deciders (orbitc and orbit.py).

Controls:
  - the 30 k7 models and the W18 k7 control from the record
    (d4-monodromy-blocks/inputs, copied to inputs/): lit rooms with W <= 21;
  - the 15 census pairs (area <= 15) whose shooting certificate is longest
    (largest |p| + |q|, then m), and 10 further census pairs chosen by a
    fixed stride.
Each control pair goes to orbitc with only the two endpoints as sources, so a
LIT answer comes from the orbit scan alone, without the shooting filter.
orbit.py re-decides the first 12 controls.
usage: python3 validate_controls.py shoot_output_area15
"""
import glob
import json
import subprocess
import sys

sys.path.insert(0, sys.path[0])
from orbit import decide  # noqa: E402


def opn(path):
    """Open a text file, or its gzip-compressed copy path + '.gz'."""
    import gzip
    import os
    if not os.path.exists(path) and os.path.exists(path + ".gz"):
        return gzip.open(path + ".gz", "rt")
    return open(path)


def controls(shoot_out):
    out = []
    for f in sorted(glob.glob("inputs/k7-models/model-*.json")):
        d = json.load(open(f))
        out.append((f.split("/")[-1], {tuple(c) for c in d["cells"]}, tuple(map(tuple, d["marks"]))))
    d = json.load(open("inputs/k7-controls.json"))
    for c in d["controls"]:
        if "cells" not in c:          # the other entries are SAT-encoding checks without a room
            continue
        out.append((c["control"], {tuple(x) for x in c["cells"]}, tuple(map(tuple, c["geometry"]["interior_A"]))))
    cand = []
    room = None
    for line in opn(shoot_out):
        f = line.split()
        if f and f[0] == "R":
            v = list(map(int, f[5:]))
            room = (f[1], {(v[i], v[i + 1]) for i in range(0, len(v), 2)})
        elif f and f[0] == "P" and f[5] == "L":
            dx, dy, m = int(f[7]), int(f[8]), int(f[9])
            cand.append((abs(dx) + abs(dy), m, room[0], room[1],
                         ((int(f[1]), int(f[2])), (int(f[3]), int(f[4])))))
    cand.sort(key=lambda t: (-t[0], -t[1], int(t[2])))
    for t in cand[:15]:
        out.append((f"census room {t[2]} (p+q={t[0]}, m={t[1]})", t[3], t[4]))
    stride = len(cand) // 10
    for t in cand[15::stride][:10]:
        out.append((f"census room {t[2]} (p+q={t[0]}, m={t[1]})", t[3], t[4]))
    return out


def main():
    sys.path.insert(1, sys.path[0] + "/../d2-factor-audit")
    ctr = controls(sys.argv[1])
    lines = []
    for name, cells, (S, T) in ctr:
        lines.append(f"{len(cells)} " + " ".join(f"{x} {y}" for x, y in sorted(cells))
                     + f" | 2 {S[0]} {S[1]} {T[0]} {T[1]}")
    res = subprocess.run(["./orbitc", "5000000"], input="\n".join(lines) + "\n",
                         capture_output=True, text=True, check=True).stdout.split("\n")
    verdicts = [ln.split()[-1] for ln in res if ln.startswith("  ")]
    states = [ln.split()[1] for ln in res if ln.startswith("states")]
    nlit = 0
    for i, (name, cells, (S, T)) in enumerate(ctr):
        extra = ""
        if i < 12:
            reach, ns, _ = decide(cells, [S, T], wanted={frozenset((S, T))})
            extra = f" orbit.py: {'LIT' if T in reach[S] else 'DARK'} after {ns} states"
        nlit += verdicts[i] == "LIT"
        print(f"{name}: area {len(cells)} pair {S}-{T}: orbitc {verdicts[i]} after {states[i]} states{extra}")
    print(f"controls {len(ctr)}, LIT {nlit}")


if __name__ == "__main__":
    main()
