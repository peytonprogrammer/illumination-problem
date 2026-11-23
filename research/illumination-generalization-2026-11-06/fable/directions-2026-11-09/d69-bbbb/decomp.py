"""d69: test the rectangle/door decomposition families on same-class interior lattice pairs.

Families (each is an explicit, proof-derived construction, not a search for witnesses):
  V   visible: the segment ST lies in the open room (no reflection).
  X   x-monotone: a billiard path that reflects only off horizontal walls.  Exact decision:
      the unfolded T-images are (t1, Y) with Y = t2 mod 2; validity is periodic in the slope
      with period 2 L_col (L_col = lcm of the heights of all column runs), so one period of Y
      is checked (section 3 of README).
  Y   y-monotone: the transpose of X.
A pair in none of V, X, Y is a residual pair: every path that lights it reflects off walls
of both orientations (it turns a corner).
Rooms: named rooms, all normalized rooms in d64 covers.json, and hand-built stretches.
Usage: python3 -B decomp.py [max_period]      (prints the log; writes decomp.json)
"""
import json
import resource
import sys
import time
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd10-mechanisms'))
from roomtools import status, lattice_points  # noqa: E402



def lcm(a, b):
    return a * b // gcd(a, b)


def quad(v, sx, sy):
    return (v[0] + (0 if sx > 0 else -1), v[1] + (0 if sy > 0 else -1))


def trace(cells, S, T, p, q, sx, sy, nsteps, forbid, bad=None):
    """Follow the billiard path from S in direction (sx p, sy q), p, q >= 0 coprime, for nsteps
    lattice steps.  forbid: set of flips not allowed ('x' = reflect off a vertical wall,
    'y' = off a horizontal wall).  True when the path reaches T at a lattice step before a
    vertex and before a forbidden flip.  Adapted from d66 g1_check.shoot."""
    v = S
    for _ in range(nsteps):
        if p and q:
            if quad(v, sx, sy) not in cells:          # at a smooth wall point: reflect
                if quad(v, sx, -sy) in cells:
                    if 'y' in forbid:
                        return False
                    sy = -sy
                elif quad(v, -sx, sy) in cells:
                    if 'x' in forbid:
                        return False
                    sx = -sx
                else:
                    return False
            cell = quad(v, sx, sy)
            k = m = 1
            while k < p or m < q:
                if m >= q or (k < p and k * q < m * p):
                    nb = (cell[0] + sx, cell[1])
                    if nb in cells:
                        cell = nb
                    else:
                        if 'x' in forbid:
                            return False
                        sx = -sx
                    k += 1
                else:
                    nb = (cell[0], cell[1] + sy)
                    if nb in cells:
                        cell = nb
                    else:
                        if 'y' in forbid:
                            return False
                        sy = -sy
                    m += 1
            v = (cell[0] + (1 if sx > 0 else 0), cell[1] + (1 if sy > 0 else 0))
        else:                                          # along a grid line
            moved = False
            for _ in range(2):
                if p:
                    adj = [(v[0] + (0 if sx > 0 else -1), v[1] + dy) for dy in (0, -1)]
                    if any(a in cells for a in adj):
                        v = (v[0] + sx, v[1]); moved = True; break
                    if 'x' in forbid:
                        return False
                    sx = -sx
                else:
                    adj = [(v[0] + dx, v[1] + (0 if sy > 0 else -1)) for dx in (0, -1)]
                    if any(a in cells for a in adj):
                        v = (v[0], v[1] + sy); moved = True; break
                    if 'y' in forbid:
                        return False
                    sy = -sy
            if not moved:
                return False
        if v == T:
            return True
        if (bad(v) if bad else status(cells, v) not in ('interior', 'smooth')):
            return False
    return False


def visible(cells, S, T):
    dx, dy = T[0] - S[0], T[1] - S[1]
    g = gcd(abs(dx), abs(dy))
    return trace(cells, S, T, abs(dx) // g, abs(dy) // g, 1 if dx >= 0 else -1,
                 1 if dy >= 0 else -1, g, {'x', 'y'})


def run_period(cells, axis):
    """lcm of the lengths of all maximal runs of cells in columns (axis 1) or rows (axis 0)."""
    L = 1
    lines = {}
    for c in cells:
        lines.setdefault(c[1 - axis], []).append(c[axis])
    for zs in lines.values():
        zs.sort()
        start = prev = zs[0]
        for z in zs[1:] + [None]:
            if z is None or z != prev + 1:
                L = lcm(L, prev + 1 - start)
                if z is not None:
                    start = z
            if z is not None:
                prev = z
    return L


def monotone(cells, S, T, axis, max_period, bad=None, wit=None):
    """axis 1: x-monotone family (reflect off horizontal walls only).  axis 0: y-monotone.
    Returns True / False, or None when the period exceeds max_period (not decided)."""
    if axis == 0:
        cells = {(j, i) for i, j in cells}
        S, T = (S[1], S[0]), (T[1], T[0])
        if bad:
            bad0 = bad
            bad = lambda v: bad0((v[1], v[0]))
    if S[0] == T[0]:
        return False                                     # only the vertical segment; that is V
    L = run_period(cells, 1)
    Dx = abs(T[0] - S[0])
    if L * Dx > max_period:
        return None
    sx = 1 if T[0] > S[0] else -1
    for k in range(-L * Dx + 1, L * Dx + 1):
        if (k - (T[1] - S[1])) % 2:
            continue
        g = gcd(Dx, abs(k))
        if trace(cells, S, T, Dx // g, abs(k) // g, sx, 1 if k >= 0 else -1, g, {'x'}, bad):
            if wit is not None:
                wit.append((Dx // g, abs(k) // g, sx, 1 if k >= 0 else -1, g))
            return True
    return False


def backwall(cells, S, T, max_period, wit=None):
    """Family B: monotone path with one bounce off an extreme wall line (x = X_max, x = X_min,
    y = Y_max or y = Y_min).  Unfold: glue the mirror image of P across that line and ask for a
    monotone path in the union; the glued line is crossed only at relative-interior wall points
    of P (a lattice point on it must be a smooth point of P).  Returns True/False/None."""
    undecided = False
    for axis in (1, 0):
        C = cells if axis == 1 else {(j, i) for i, j in cells}
        S_, T_ = (S, T) if axis == 1 else ((S[1], S[0]), (T[1], T[0]))
        xs = [c[0] for c in C]
        for X, mover in ((max(xs) + 1, 'T'), (min(xs), 'S'), (max(xs) + 1, 'S'), (min(xs), 'T')):
            U = C | {(2 * X - 1 - i, j) for i, j in C}
            A = (2 * X - S_[0], S_[1]) if mover == 'S' else S_
            B = (2 * X - T_[0], T_[1]) if mover == 'T' else T_

            def bad(v, U=U, C=C, X=X):
                if v[0] == X:
                    return status(C, v) != 'smooth'
                return status(U, v) not in ('interior', 'smooth')
            w = []
            r = monotone(U, A, B, 1, max_period, bad, w)
            if r:
                if wit is not None:
                    wit.append((axis, mover, w[0]))
                return True
            undecided |= r is None
    return None if undecided else False


def same_class_pairs(cells):
    ipts = [p for p in lattice_points(cells) if status(cells, p) == 'interior']
    return [(S, T) for S, T in combinations(ipts, 2)
            if (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0]


def classify(cells, max_period):
    out = []
    for S, T in same_class_pairs(cells):
        if visible(cells, S, T):
            out.append((S, T, 'V'))
            continue
        x = monotone(cells, S, T, 1, max_period)
        if x:
            out.append((S, T, 'X'))
            continue
        y = monotone(cells, S, T, 0, max_period)
        if y:
            out.append((S, T, 'Y'))
            continue
        b = backwall(cells, S, T, max_period)
        if b:
            out.append((S, T, 'B'))
            continue
        out.append((S, T, 'skip' if (x is None or y is None or b is None) else 'R'))
    return out


# ---------------------------------------------------------------- rooms
def rect(x0, x1, y0, y1):
    return {(i, j) for i in range(x0, x1) for j in range(y0, y1)}


def cells_of(name):
    sys.path.insert(0, str(D / 'd63-realization'))
    sys.path.insert(0, str(D / 'd65-nx-equals-b'))
    import realize
    import notch12
    rooms = dict(realize.rooms())
    rooms['Z12'], rooms['S10'] = notch12.Z12, notch12.S10
    return {k: set(map(tuple, v)) for k, v in rooms.items()}


def stretch(cells, axis, at, times):
    """Insert `times` extra copies of column (axis 0) or row (axis 1) number `at`."""
    out = set()
    for c in cells:
        z = c[axis]
        if z < at:
            out.add(c)
        elif z == at:
            for t in range(times + 1):
                out.add((c[0] + t, c[1]) if axis == 0 else (c[0], c[1] + t))
        else:
            out.add((c[0] + times, c[1]) if axis == 0 else (c[0], c[1] + times))
    return out


COV279 = {(0, 0), (1, 0), (0, 1), (1, 1), (1, 2), (2, 2), (3, 2), (2, 3), (3, 3), (4, 3),
          (4, 4), (5, 4), (4, 5), (5, 5)}


def handbuilt():
    cov4181 = {(0, j) for j in range(6)} | {(1, 2), (1, 3), (2, 2), (2, 3)} | \
        {(3, j) for j in range(6)} | {(4, j) for j in range(6)} | {(5, 2), (5, 3), (6, 2)} | \
        {(7, 0), (7, 1), (7, 2)}
    return {
        # two 5x5 squares, unit corridor of length 3 at height 2
        'DB55': rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5),
        # asymmetric dumbbell: 5x4 and 4x6, unit corridor of length 4
        'DBas': rect(0, 5, 0, 4) | rect(5, 9, 1, 2) | rect(9, 13, -1, 5),
        # dumbbell with a width-2 corridor of length 4
        'DBw2': rect(0, 5, 0, 5) | rect(5, 9, 1, 3) | rect(9, 14, 0, 6),
        # cross with arms 3 wide, 4 long
        'CR34': rect(4, 7, 0, 11) | rect(0, 11, 4, 7),
        # cov4181 (d66 per-target failure room) with column 1 and row 4 stretched
        'c4181s': stretch(stretch(cov4181, 0, 1, 2), 1, 4, 3),
        # U-shaped room with 2-wide arms and an inner step (r = 4)
        'U2': rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7),
        # d64 room cov279 (staircase, residual pair (1,1)-(5,5)) with both end blobs stretched
        'st279': stretch(stretch(stretch(stretch(COV279, 0, 0, 3), 1, 0, 3), 0, 8, 3), 1, 8, 3),
        # same, blobs stretched by 2 only (area <= 36 check of the trend)
        'st279b': stretch(stretch(COV279, 0, 0, 2), 1, 0, 2),
    }


def main():
    max_period = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    t0 = time.process_time()
    named = cells_of(None)
    resource.setrlimit(resource.RLIMIT_CPU, (500, 500))
    hb = handbuilt()
    rooms = [(k, v) for k, v in named.items()] + [(k, v) for k, v in hb.items()]
    cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
           if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))     # same order and names as d66 (cov<i>)
    rooms += [('cov%d' % i, set(map(tuple, r['cells']))) for i, r in enumerate(cov)]
    tally = Counter()
    resid = []
    per_room = {}
    for name, cells in rooms:
        res = classify(cells, max_period)
        c = Counter(k for _, _, k in res)
        per_room[name] = dict(n=len(cells), counts=dict(c))
        group = 'named' if name in named else ('hand' if name in hb else 'covers')
        for k, v in c.items():
            tally[(group, k)] += v
        for S, T, k in res:
            if k in ('R', 'skip'):
                resid.append(dict(room=name, n=len(cells), S=S, T=T, kind=k))
        if group != 'covers':
            print(name, 'n', len(cells), dict(c), flush=True)
    print('tally', sorted(tally.items()))
    print('residual pairs', sum(1 for r in resid if r['kind'] == 'R'),
          'skipped', sum(1 for r in resid if r['kind'] == 'skip'))
    for r in resid[:40]:
        print('  ', r)
    print('CPU %.1f s' % (time.process_time() - t0))
    json.dump(dict(per_room=per_room, residual=resid), open(HERE / 'decomp.json', 'w'))


if __name__ == '__main__':
    main()
