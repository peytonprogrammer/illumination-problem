#!/usr/bin/env python3
"""Compare cover.c's DP-cylinder labels (Section 4.1) with d74's independently
written geom.Direction (room-level billiard-flow union-find), direction by
direction: the partition of {(cell, family, strip)} into labels must agree,
and the set of singular integer lines must agree.

usage: python3 -B labels_cmp.py B
"""
import subprocess
import sys

HERE = sys.path[0]
sys.path.insert(0, HERE + "/../d74-continuum-check")
from geom import Direction  # noqa: E402

B = int(sys.argv[1])
bad = 0
for line in open(HERE + "/rooms.txt"):
    tok = line.split()
    nums = list(map(int, tok[1:]))
    cells = [(nums[2 + 2 * i], nums[3 + 2 * i]) for i in range(nums[0])]
    out = subprocess.run([HERE + "/harness", str(B), "dump"], input=" ".join(tok[1:]) + "\n",
                         capture_output=True, text=True, check=True).stdout
    rows = {}
    for r in out.split("\n"):
        if not r:
            continue
        w = r.split()
        p, q, a, b = int(w[1]), int(w[2]), int(w[4]), int(w[5])
        i1, i2, i3 = w.index("PL"), w.index("M"), w.index("ML")
        rows.setdefault((p, q), {})[(a, b)] = (list(map(int, w[7:i1])), list(map(int, w[i1 + 1:i2])),
                                                list(map(int, w[i2 + 1:i3])), list(map(int, w[i3 + 1:])))
    nd = nseg = 0
    for (p, q), percell in rows.items():
        Dd = Direction(frozenset(cells), p, q)
        m1, m2 = {}, {}   # cover label -> d74 label, and back
        ok = True
        for (a, b), (P, PL, M, ML) in percell.items():
            k0, m0 = q * a - p * b, q * a + p * b
            for fam, lab, lines, base in ((0, P, PL, k0 - p), (1, M, ML, m0)):
                for idx, l in enumerate(lab):
                    K = base + idx
                    g = Dd.label[((a, b), fam, 2 * K + 1)]
                    nseg += 1
                    if m1.setdefault(l, g) != g or m2.setdefault(g, l) != l:
                        ok = False
                for idx, l in enumerate(lines):
                    K = base + idx + 1
                    sing74 = ((a, b), fam, 2 * K) in Dd.singular
                    if (l == -1) != sing74:
                        ok = False
        nd += 1
        if not ok:
            bad += 1
            print("MISMATCH", tok[0], p, q)
    print(tok[0], "directions", nd, "strip labels compared", nseg, "mismatched directions so far", bad)
print("TOTAL mismatched directions", bad)
