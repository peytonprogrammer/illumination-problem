"""d59: exact lattice-step billiard tracer for ONE named lattice room (no room search).

From a lattice point S, direction (p, q) with p, q nonzero and coprime, the path visits a
lattice point after each unfolded step (p, q).  Wall crossings between lattice points are at
non-lattice points, so they are handled by cell moves and reflections.  The path dies at a
convex or reflex corner and is lit when it reaches T.  Integer arithmetic only.
Usage: python3 -B lattice_trace.py
"""
import sys, json, resource
from math import gcd
from pathlib import Path
pass
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from axis_twist import load, status, cells_from_vertices, D  # noqa: E402


def trace(cells, S, T, p, q, maxsteps=100000):
    sp, sq = (1 if p > 0 else -1), (1 if q > 0 else -1)
    ap, aq = abs(p), abs(q)
    ex = ey = 1
    cx = S[0] + (0 if sp > 0 else -1)
    cy = S[1] + (0 if sq > 0 else -1)
    if (cx, cy) not in cells:
        return None
    ev = sorted([(i * aq, 'x') for i in range(1, ap)] + [(j * ap, 'y') for j in range(1, aq)])
    seen = set()
    for step in range(1, maxsteps + 1):
        for _, kind in ev:
            if kind == 'x':
                d = ex * sp
                if (cx + d, cy) in cells:
                    cx += d
                else:
                    ex = -ex
            else:
                d = ey * sq
                if (cx, cy + d) in cells:
                    cy += d
                else:
                    ey = -ey
        dx, dy = ex * sp, ey * sq
        L = (cx + (1 if dx > 0 else 0), cy + (1 if dy > 0 else 0))
        if L == tuple(T):
            return step
        k = status(cells, L)
        if k in (1, 3):
            return -step  # blocked at a corner
        key = (cx, cy, ex, ey)
        if key in seen:
            return 0  # periodic, never reaches T
        seen.add(key)
        # pass through the regular lattice point: both crossings
        for kind in ('x', 'y'):
            if kind == 'x':
                d = ex * sp
                if (cx + d, cy) in cells:
                    cx += d
                else:
                    ex = -ex
            else:
                d = ey * sq
                if (cx, cy + d) in cells:
                    cy += d
                else:
                    ey = -ey
    return 0


def axis_lit(cells, S, T):
    """Straight horizontal or vertical chord through S containing T with no corner between."""
    for a in (0, 1):
        if S[1 - a] != T[1 - a]:
            continue
        lo, hi = sorted((S[a], T[a]))
        ok = True
        for u in range(lo + 1, hi):
            P = (u, S[1]) if a == 0 else (S[0], u)
            if status(cells, P) != 4:
                ok = False
        if ok and status(cells, S) == 4 and status(cells, T) == 4:
            return True
    return False


def lighting(cells, S, T, H):
    out = []
    for p in range(-H, H + 1):
        for q in range(-H, H + 1):
            if p == 0 or q == 0 or gcd(abs(p), abs(q)) != 1:
                continue
            r = trace(cells, S, T, p, q)
            if r and r > 0:
                out.append((abs(p) + abs(q), p, q, r))
    return sorted(out)


if __name__ == '__main__':
    R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1),
           (5, 1), (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2),
           (0, -2), (0, -1)]
    rooms = D / 'd41-two-param-cover' / 'rooms'
    cases = [('R22 dark control', cells_from_vertices(R22), (0, 0), (2, 2)),
             ('r20a W=20', load(rooms / 'r20a.txt'), (1, 3), (3, 5)),
             ('dumb12', load(rooms / 'dumb12.txt'), (2, 2), (6, 2)),
             ('dumb12', load(rooms / 'dumb12.txt'), (1, 2), (7, 2)),
             ('dumb12', load(rooms / 'dumb12.txt'), (1, 1), (7, 1))]
    H = 15
    res = []
    for name, cells, S, T in cases:
        L = lighting(cells, S, T, H)
        Lr = lighting(cells, T, S, H)
        rec = dict(room=name, S=S, T=T, H=H, axis=axis_lit(cells, S, T),
                   n_lighting_dirs=len(L), first=L[:12], n_reverse=len(Lr))
        print(json.dumps(rec))
        res.append(rec)
    json.dump(res, open(HERE / 'lattice_trace.json', 'w'), indent=1)
