"""Independent check of Codex's exception budget (k = 4, 5, 6). No rays.

b_min(n): brute force over every n-subset of a 9x9 cell window. Sets whose parts are more
than Manhattan distance 2 apart have disjoint, additive boundaries, so they never beat a
tighter set, and every tighter set of at most 4 cells fits in the window.
Tuples: W = 2+6I+Q-(2J+s_N) <= 23, Q >= b_min(I) - s_N, N = 8I+Q+s_A, 3 s_A <= Q, I >= 2.
"""
import json
from itertools import combinations
cells = [(x, y) for x in range(9) for y in range(9)]
bmin = {}
for n in range(1, 5):
    best = 99
    for S in combinations(cells, n):
        s = set(S)
        b = {(x+dx, y+dy) for x, y in s for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - s
        best = min(best, len(b))
    bmin[n] = best
out = {}
for k in (4, 5, 6):
    rows = []
    for I in range(2, 10):
        b = bmin.get(I, 4 + I)  # b >= 4 universally; I >= 5 is excluded either way
        for J in range(k+1):
            sN = k-J
            for W in range(4, 24):
                Q = W-2-6*I+2*J+sN
                if Q < 0 or Q < b-sN:
                    continue
                for sA in range(Q//3+1):
                    N = 8*I+Q+sA
                    assert 8*I+4*sA+8*J+4*sN == 4*(N-W+2)
                    rows.append((I, J, sN, W, Q, sA, N))
    out[k] = dict(I=sorted({r[0] for r in rows}), maxN=max(r[6] for r in rows), tuples=len(rows))
print(json.dumps(dict(bmin=bmin, budget=out)))
