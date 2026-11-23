"""Classify uncovered position-type pairs by the link distance k: the least
number of rectangles R1..Rk inside the room with S in R1, T in Rk and
consecutive rectangles sharing a cell.  Usage: classify_gap.py r"""
import sys, json, collections
from lemmas import OT
def max_rects(ot):
    R = []
    for i0 in range(ot.nx):
        for i1 in range(i0 + 1, ot.nx + 1):
            for j0 in range(ot.ny):
                for j1 in range(j0 + 1, ot.ny + 1):
                    if ot.rect(i0, i1, j0, j1): R.append((i0, i1, j0, j1))
    def inside(a, b): return b[0] <= a[0] and a[1] <= b[1] and b[2] <= a[2] and a[3] <= b[3]
    return [a for a in R if not any(a != b and inside(a, b) for b in R)]
def contains(rc, P):
    return 2 * rc[0] <= P[0] <= 2 * rc[1] and 2 * rc[2] <= P[1] <= 2 * rc[3]
def meet(a, b):
    return max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3])
def link(ot, R, S, T):
    cur = {i for i, rc in enumerate(R) if contains(rc, S)}
    seen = set(cur); k = 1
    while cur:
        if any(contains(R[i], T) for i in cur): return k
        cur = {j for j in range(len(R)) if j not in seen and any(meet(R[i], R[j]) for i in cur)}
        seen |= cur; k += 1
    return 99
r = sys.argv[1]
rows = json.load(open(f"cert_r{r}.json"))
hist = collections.Counter(); ex = {}
for row in rows:
    ot = OT.from_mask(row['nx'], row['ny'], row['mask']); R = max_rects(ot)
    for S, T in row['uncovered']:
        k = link(ot, R, tuple(S), tuple(T)); hist[k] += 1
        ex.setdefault(k, (row['shape'], S, T))
print("r", r, "uncovered by link distance", dict(sorted(hist.items())))
for k, e in sorted(ex.items()): print("  example k =", k, e)
