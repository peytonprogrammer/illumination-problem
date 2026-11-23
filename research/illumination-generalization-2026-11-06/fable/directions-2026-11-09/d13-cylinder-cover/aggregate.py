#!/usr/bin/env python3
"""Aggregate cover.c and shoot.py outputs into a Markdown table by area.

usage: python3 aggregate.py RESULTS... -- SHOOTS...
  RESULTS: cover output files (ROOM lines). A later file overrides an earlier
           one for the same room (cells), for reruns of BIG rooms.
  SHOOTS:  shoot.py output files.
"""
import sys
from collections import defaultdict


def main():
    args = sys.argv[1:]
    k = args.index("--")
    res, shoots = args[:k], args[k + 1:]
    rooms = {}
    for fn in res:
        for ln in open(fn):
            if not ln.startswith("ROOM"):
                continue
            head, cells, _ = ln.split("|", 2)
            t = head.split()
            rooms[cells.strip()] = (int(t[2]), int(t[3]), t[4], int(t[7]), int(t[11]), int(t[12]))
    shot = defaultdict(lambda: [0, 0])
    for fn in shoots:
        for ln in open(fn):
            st, rest = ln.split(" ", 1)
            cells = rest.split("|")[0].strip()
            shot[cells][0] += 1
            shot[cells][1] += st == "LIT"
    tab = defaultdict(lambda: defaultdict(int))
    for cells, (A, W, st, npts, ll, nl) in rooms.items():
        r = tab[A]
        r["rooms"] += 1
        r[st] += 1
        if st == "DONE":
            r["pts"] += npts
            r["ll"] += ll
            r["nl"] += nl
            r["shot"] += shot[cells][0]
            r["lit"] += shot[cells][1]
            if shot[cells][1] == nl:
                r["closed"] += 1
    cols = ["rooms", "DONE", "closed", "OBST", "RESID", "BIG", "pts", "ll", "nl", "lit"]
    names = ["class (iii) rooms", "DONE", "DONE, all pairs closed", "OBST", "RESID", "BIG",
             "live points", "lattice pairs left", "other pairs left", "other pairs LIT"]
    print("| area | " + " | ".join(names) + " |")
    print("| --- " * (len(cols) + 1) + "|")
    tot = defaultdict(int)
    for A in sorted(tab):
        print(f"| {A} | " + " | ".join(f"{tab[A][c]:,}" for c in cols) + " |")
        for c in cols:
            tot[c] += tab[A][c]
    print("| all | " + " | ".join(f"{tot[c]:,}" for c in cols) + " |")


if __name__ == "__main__":
    main()
