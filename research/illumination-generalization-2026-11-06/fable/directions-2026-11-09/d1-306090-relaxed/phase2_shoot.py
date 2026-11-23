"""Phase 2 exact shooter: legal S->T paths in rooms that may have transparent C points.

Uses check_room.py (independent of the CP-SAT code) for polygon analysis. Adds:
  * find_paths: exact billiards from S toward every A point X with |X-S| <= bound,
    recording the full path; reports the ones that end exactly at T.
  * mirror_exact: the 12 directions along mirror lines, simulated until a corner
    is hit or the state (point, direction) repeats; a complete decision for them.
  * support: the tiles a path needs present / absent, for sound CEGAR cuts.
Coordinates (x, y) mean (x, sqrt(3) y); everything is Fraction arithmetic.
"""
from fractions import Fraction as F
from math import gcd
from check_room import analyze, label, dot, cross, sub, add, scale, E1, E2, DIR12, lattice_coords


def shoot_path(S, v, corners, length=F(1), max_bounces=100000):
    """Billiard from S with velocity v for parameter `length`.
    Returns (status, path, walls) where status is 'corner' or 'open'; path is the
    list of points [S, r1, ..., end]; walls[i] is the wall direction at r_{i+1}."""
    poly = corners; n = len(poly); cset = set(poly)
    p = (F(S[0]), F(S[1])); tau = F(0); path = [p]; walls = []
    for _ in range(max_bounces):
        best = None
        for k in range(n):
            a, b = poly[k], poly[(k+1) % n]; w = sub(b, a); den = cross(v, w)
            if den == 0: continue
            ap = sub(a, p); t = F(cross(ap, w), den); s = F(cross(ap, v), den)
            if t <= 0 or s < 0 or s > 1: continue
            if best is None or t < best[0]: best = (t, k, s)
        assert best is not None, 'ray escaped'
        t, k, s = best
        if tau + t > length:
            path.append(add(p, scale(length - tau, v))); return 'open', path, walls
        q = add(p, scale(t, v)); path.append(q)
        if q in cset or s in (0, 1): return 'corner', path, walls
        if tau + t == length: return 'open', path, walls
        a, b = poly[k], poly[(k+1) % n]; w = sub(b, a)
        lam = F(2 * dot(v, w), dot(w, w)); v = (lam*w[0] - v[0], lam*w[1] - v[1])
        walls.append(w); p = q; tau += t
    raise RuntimeError('too many bounces')


def lattice_targets(bound):
    out = []
    for di in range(-2*bound, 2*bound+1):
        for dj in range(-2*bound, 2*bound+1):
            n2 = di*di + di*dj + dj*dj
            if 0 < n2 <= bound*bound: out.append((n2, di, dj))
    out.sort()
    return [(di, dj) for _, di, dj in out]


def find_paths(S, T, corners, bound, max_paths=None):
    """All legal S->T paths whose unfolded length is <= bound edge lengths."""
    S = tuple(S); T = (F(T[0]), F(T[1])); found = []; shots = 0
    for di, dj in lattice_targets(bound):
        X = add(S, add(scale(di, E1), scale(dj, E2)))
        st, path, walls = shoot_path(S, sub(X, S), corners); shots += 1
        if st == 'open' and path[-1] == T:
            found.append(dict(X=(di, dj), path=path, walls=walls))
            if max_paths and len(found) >= max_paths: break
    return found, shots


def mirror_exact(S, T, corners):
    """Exact decision for the 12 mirror-line directions from S (any length)."""
    T = (F(T[0]), F(T[1])); out = []
    for d in DIR12:
        poly = corners; n = len(poly); cset = set(poly)
        p = (F(S[0]), F(S[1])); v = d; seen = set(); res = None; path = [p]
        while res is None:
            if (p, v) in seen: res = 'periodic'; break
            seen.add((p, v)); best = None
            for k in range(n):
                a, b = poly[k], poly[(k+1) % n]; w = sub(b, a); den = cross(v, w)
                if den == 0: continue
                ap = sub(a, p); t = F(cross(ap, w), den); s = F(cross(ap, v), den)
                if t <= 0 or s < 0 or s > 1: continue
                if best is None or t < best[0]: best = (t, k, s)
            t, k, s = best; q = add(p, scale(t, v))
            # does the open leg (p, q] pass through T?
            dT = sub(T, p)
            if cross(dT, v) == 0 and 0 < F(dot(dT, v), dot(v, v)) <= t: res = 'reaches T'; break
            if q in cset or s in (0, 1): res = 'corner'; break
            a, b = poly[k], poly[(k+1) % n]; w = sub(b, a)
            lam = F(2 * dot(v, w), dot(w, w)); v = (lam*w[0] - v[0], lam*w[1] - v[1]); p = q; path.append(q)
        out.append(dict(direction=d, result=res, bounces=len(path) - 1))
    return out


# ---------- support of a path (for sound cuts) ----------
FUNCS = [lambda p: p[1], lambda p: p[0], lambda p: p[0]-p[1], lambda p: p[0]+p[1], lambda p: p[0]-3*p[1], lambda p: p[0]+3*p[1]]


def in_closed_tri(p, t):
    a, b, c = t
    s1, s2, s3 = cross(sub(b, a), sub(p, a)), cross(sub(c, b), sub(p, b)), cross(sub(a, c), sub(p, c))
    return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)


class TileIndex:
    def __init__(self, tiles):
        self.tiles = [tuple(tuple(q) for q in t) for t in tiles]; self.idx = {t: i for i, t in enumerate(self.tiles)}
        self.byA = {}
        for i, t in enumerate(self.tiles):
            A = next(q for q in t if label(q) == 'A'); self.byA.setdefault(A, []).append(i)

    def containing(self, p):
        i, j = lattice_coords(p); i0, j0 = int(i // 1), int(j // 1); out = set()
        for di in range(-1, 3):
            for dj in range(-1, 3):
                A = add(scale(i0+di, E1), scale(j0+dj, E2))
                for k in self.byA.get(A, []):
                    if in_closed_tri(p, self.tiles[k]): out.add(k)
        return out


def support(path, walls, index):
    """(present, absent) tile index sets that make this exact path legal in any room."""
    present, absent = set(), set()
    for a, b in zip(path, path[1:]):
        d = sub(b, a); ts = {F(0), F(1)}
        for f in FUNCS:
            fa, fb = f(a), f(b)
            if fa == fb: continue
            lo, hi = sorted((fa, fb)); k = (lo // 6) * 6
            while k <= hi:
                t = F(k - fa, fb - fa)
                if 0 < t < 1: ts.add(t)
                k += 6
        ts = sorted(ts)
        samples = [scale(t, d) for t in ts[1:-1]] + [scale((t1 + t2) / 2, d) for t1, t2 in zip(ts, ts[1:])]
        for s in samples: present |= index.containing(add(a, s))
    for r, prev, w in zip(path[1:-1], path[:-2], walls):
        side_prev = cross(w, sub(prev, r))
        for k in index.containing(r):
            t = index.tiles[k]; c3 = (sum(q[0] for q in t), sum(q[1] for q in t))
            side = cross(w, sub(c3, scale(3, r)))
            (present if (side > 0) == (side_prev > 0) else absent).add(k)
    present |= index.containing(path[0]) | index.containing(path[-1])
    assert not present & absent
    return present, absent
