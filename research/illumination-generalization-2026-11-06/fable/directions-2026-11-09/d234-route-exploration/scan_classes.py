"""Exact x-monotone list with per-hit class data, integer arithmetic (ordinates scaled by X).
Same legality rules as scan_general.py. For each hit: K, start direction, turns per column,
direction at the third gate, and whether the last-column bounce count is odd ("flipped image").
Usage: scan_classes.py N e y0 y1 y2 y3 y4 y5 smax   (scans K/X <= smax)
"""
import sys
from collections import Counter

def run(N, e, lv, smax):
    y0, y1, y2, y3, y4, y5 = lv
    X = N + 2 + e
    cols = [(1, y0, y3), (N, y2, y3), (1, y2, y5), (e, y3, y5)]
    gates = [(y2, y3), (y2, y3), (y3, y5)]
    out = []
    for K in range(1, smax * X + 1):
        for d0 in (1, -1):
            y, d, ok, turns, d3 = y1 * X, d0, True, [], 0
            for i, (w, a, b) in enumerate(cols):
                h = (b - a) * X
                t = y - a * X
                phi = t if d == 1 else 2 * h - t
                z = phi + K * w
                turns.append(z // h)
                p2 = z % (2 * h)
                if p2 == 0 or p2 == h:
                    ok = False; break
                y, d = (a * X + p2, 1) if p2 < h else (a * X + 2 * h - p2, -1)
                if i < 3 and not (gates[i][0] * X < y < gates[i][1] * X):
                    ok = False; break
                if i == 2:
                    d3 = d
            if ok and y == y4 * X:
                out.append((K, d0, tuple(turns), d3, turns[3] % 2))
    return X, out

if __name__ == "__main__":
    a = list(map(int, sys.argv[1:]))
    X, out = run(a[0], a[1], tuple(a[2:8]), a[8])
    print(f"X={X} slopes up to {a[8]}: {len(out)} hits")
    c = Counter((h[1], h[2][0] > 0, h[2][2] > 0, h[3], h[4]) for h in out)
    print("(start dir, turn in col 1, turn in col 3, dir at gate 3, flipped image): count")
    for k, v in sorted(c.items()):
        print(" ", k, v)
    fl = [h for h in out if h[4] == 1]
    print("first flipped-image hits:", fl[:3])
