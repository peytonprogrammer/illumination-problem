"""Exact x-monotone list on the two-gate chart with a free last column width e.
Same legality rules as monotone_residual.py (which is the case e = N/2 - 1).
Columns: widths (1, N, 1, e); intervals [y0,y3], [y2,y3], [y2,y5], [y3,y5].
S = (N-1, y1), T = (2N+1+e, y4). Stops after `want` hits or after the full period.
Usage: scan_general.py N e y0 y1 y2 y3 y4 y5 [want]
"""
import sys
from fractions import Fraction as F
from math import lcm

def run(N, e, levels, want=3, cap=None):
    y0, y1, y2, y3, y4, y5 = levels
    X = N + 2 + e
    cols = [(1, y0, y3), (N, y2, y3), (1, y2, y5), (e, y3, y5)]
    gates = [(y2, y3), (y2, y3), (y3, y5)]
    P = X * lcm(*[2 * (b - a) for _, a, b in cols])
    lim = P if cap is None else min(P, cap)
    hits = []
    for V in range(1, lim + 1):
        s = F(V, X)
        for d0 in (1, -1):
            y, d, ok, nb = F(y1), d0, True, 0
            for i, (w, a, b) in enumerate(cols):
                h = b - a
                t = y - a
                phi = t if d == 1 else 2 * h - t
                z = phi + s * w
                nb += int(z // h)
                p2 = z % (2 * h)
                if p2 == 0 or p2 == h:
                    ok = False; break
                y, d = (a + p2, 1) if p2 < h else (a + 2 * h - p2, -1)
                if i < 3 and not (gates[i][0] < y < gates[i][1]):
                    ok = False; break
            if ok and y == y4:
                hits.append((V, d0, nb))
        if len(hits) >= want:
            break
    return X, P, lim, hits

if __name__ == "__main__":
    a = list(map(int, sys.argv[1:]))
    N, e, lv = a[0], a[1], tuple(a[2:8])
    want = a[8] if len(a) > 8 else 3
    X, P, lim, hits = run(N, e, lv, want)
    print(f"N={N} e={e} levels={lv}: X={X} period={P} scanned={lim if len(hits)<want else hits[-1][0]} hits={hits}")
