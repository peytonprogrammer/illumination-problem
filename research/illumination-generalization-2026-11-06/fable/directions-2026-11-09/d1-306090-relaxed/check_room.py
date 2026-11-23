"""Independent exact checker for 30-60-90 (2,3,6) tiling rooms.

Shares no code with search_relaxed.py. Coordinates (x, y) are integers or
Fractions that mean the physical point (x, sqrt(3)*y). The metric is
dx^2 + 3 dy^2, so every predicate below is exact rational arithmetic.

A points: lattice L spanned by E1=(12,0), E2=(6,6) (edge length 12).
C points: (1/2)L minus L. B points: L + (6,2) and L + (12,4).

Usage: python check_room.py room.json [--bound R]
room.json has "tiles": [[[x,y],[x,y],[x,y]], ...] and optional "S", "T".
"""
import json, sys, argparse
from fractions import Fraction as F
from math import gcd

E1, E2 = (12, 0), (6, 6)


def dot(u, v): return u[0]*v[0] + 3*u[1]*v[1]
def cross(u, v): return u[0]*v[1] - u[1]*v[0]
def sub(u, v): return (u[0]-v[0], u[1]-v[1])
def add(u, v): return (u[0]+v[0], u[1]+v[1])
def scale(t, u): return (t*u[0], t*u[1])


def lattice_coords(p):
    """Return (i, j) with p = i*E1 + j*E2 (possibly non-integer Fractions)."""
    j = F(p[1]) / 6
    i = (F(p[0]) - 6*j) / 12
    return i, j


def in_L(p):
    i, j = lattice_coords(p)
    return i.denominator == 1 and j.denominator == 1


def label(p):
    if in_L(p): return 'A'
    if in_L(scale(2, p)): return 'C'
    if in_L(sub(p, (6, 2))) or in_L(sub(p, (12, 4))): return 'B'
    return None


# The 12 directions at multiples of 30 degrees, in (x, y) coordinates.
DIR12 = [(1, 0), (3, 1), (1, 1), (0, 1), (-1, 1), (-3, 1),
         (-1, 0), (-3, -1), (-1, -1), (0, -1), (1, -1), (3, -1)]


def slot(d):
    for k, D in enumerate(DIR12):
        if cross(d, D) == 0 and dot(d, D) > 0: return k
    raise ValueError(f'direction {d} is not a multiple of 30 degrees')


UNIT = {'A': 30, 'B': 60, 'C': 90}


def validate_tile(t):
    labs = sorted((label(p), p) for p in t)
    assert [l for l, _ in labs] == ['A', 'B', 'C'], f'bad labels {t}'
    (_, a), (_, b), (_, c) = labs
    ca, cb = sub(a, c), sub(b, c)
    assert dot(ca, cb) == 0, f'no right angle at C in {t}'
    assert dot(ca, ca) == 36 and dot(cb, cb) == 12, f'wrong size tile {t}'
    return a, b, c


def boundary_cycle(tiles):
    count = {}
    for t in tiles:
        for k in range(3):
            e = frozenset((t[k], t[(k+1) % 3]))
            count[e] = count.get(e, 0) + 1
    assert max(count.values()) <= 2, 'edge shared by more than two tiles'
    bnd = [tuple(e) for e, c in count.items() if c == 1]
    nbr = {}
    for a, b in bnd:
        nbr.setdefault(a, []).append(b); nbr.setdefault(b, []).append(a)
    bad = [p for p, n in nbr.items() if len(n) != 2]
    assert not bad, f'boundary vertex of degree != 2 (pinch point): {bad[:4]}'
    start = min(nbr); cyc = [start]; prev = None; cur = start
    while True:
        nxt = nbr[cur][0] if nbr[cur][0] != prev else nbr[cur][1]
        if nxt == start: break
        cyc.append(nxt); prev, cur = cur, nxt
    assert len(cyc) == len(nbr), 'boundary has more than one component (hole or disjoint piece)'
    return cyc, count


def shoelace2(poly):
    return sum(cross(poly[k], poly[(k+1) % len(poly)]) for k in range(len(poly)))


def tile_connected(tiles, count):
    adj = {}
    for i, t in enumerate(tiles):
        for k in range(3):
            adj.setdefault(frozenset((t[k], t[(k+1) % 3])), []).append(i)
    seen = {0}; todo = [0]
    while todo:
        i = todo.pop(); t = tiles[i]
        for k in range(3):
            for j in adj[frozenset((t[k], t[(k+1) % 3]))]:
                if j not in seen: seen.add(j); todo.append(j)
    return len(seen) == len(tiles)


def point_in_polygon_strict(p, poly):
    """True if p is strictly inside; raises if p is on the boundary."""
    n = len(poly); inside = False
    for k in range(n):
        a, b = poly[k], poly[(k+1) % n]
        if cross(sub(b, a), sub(p, a)) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
            raise ValueError('point on boundary')
        if (a[1] > p[1]) != (b[1] > p[1]):
            xint = a[0] + F(p[1]-a[1]) * (b[0]-a[0]) / (b[1]-a[1])
            if p[0] < xint: inside = not inside
    return inside


def analyze(tiles):
    tiles = [tuple(tuple(map(int, p)) for p in t) for t in tiles]
    assert len(set(map(frozenset, tiles))) == len(tiles), 'duplicate tile'
    for t in tiles: validate_tile(t)
    assert tile_connected(tiles, None), 'tiles not edge-connected'
    cyc, count = boundary_cycle(tiles)
    if shoelace2(cyc) < 0: cyc = cyc[::-1]
    area_tiles = sum(abs(shoelace2(list(t))) for t in tiles)
    assert shoelace2(cyc) == area_tiles, 'boundary area != tile area'
    # interior angles at every boundary vertex, from the polygon alone
    n = len(cyc); angle = {}
    for k in range(n):
        p, prv, nxt = cyc[k], cyc[k-1], cyc[(k+1) % n]
        a = (slot(sub(prv, p)) - slot(sub(nxt, p))) % 12
        angle[p] = 30 * (a if a else 12)
    corners = [p for p in cyc if angle[p] != 180]
    assert sum(180 - angle[p] for p in corners) == 360, 'turning sum != 360'
    # tile counts and cross-check with polygon angles
    tc = {}
    for t in tiles:
        for p in t: tc[p] = tc.get(p, 0) + 1
    on_bnd = set(cyc)
    for p, c in tc.items():
        a = c * UNIT[label(p)]
        if p in on_bnd: assert a == angle[p], f'angle mismatch at {p}: tiles {a}, polygon {angle[p]}'
        else: assert a == 360, f'non-boundary point {p} not surrounded: {a}'
    interior_A = sorted(p for p, c in tc.items() if label(p) == 'A' and c == 12)
    for p in interior_A: assert point_in_polygon_strict(p, cyc)
    cpts = {p: c for p, c in tc.items() if label(p) == 'C'}
    transparent_C = sorted(p for p, c in cpts.items() if c not in (1, 3))
    return dict(tiles=len(tiles), walls=len(corners),
                corners=[dict(p=list(p), label=label(p), angle=angle[p]) for p in corners],
                interior_A=[list(p) for p in interior_A],
                C_tile_counts=sorted(set(cpts.values())), C_points=len(cpts),
                transparent_C=[list(p) for p in transparent_C],
                flat_B=sum(1 for p in on_bnd if label(p) == 'B' and angle[p] == 180),
                interior_B=sum(1 for p, c in tc.items() if label(p) == 'B' and c == 6),
                angle_histogram={str(a): sum(1 for p in corners if angle[p] == a) for a in sorted({angle[p] for p in corners})}), corners


def shoot(S, X, corners, max_bounces=100000):
    """Billiard from S in direction X-S for the unfolded length |X-S|.
    Returns ('corner', tau, point) or ('open', endpoint)."""
    poly = corners; n = len(poly); cset = set(poly)
    p = (F(S[0]), F(S[1])); v = sub(X, S); tau = F(0); last = None
    for _ in range(max_bounces):
        best = None
        for k in range(n):
            a, b = poly[k], poly[(k+1) % n]; w = sub(b, a)
            den = cross(v, w)
            if den == 0: continue
            ap = sub(a, p)
            t = F(cross(ap, w), den); s = F(cross(ap, v), den)
            if t <= 0 or s < 0 or s > 1: continue
            if best is None or t < best[0]: best = (t, k, s)
        assert best is not None, 'ray escaped the polygon'
        t, k, s = best
        if tau + t > 1:
            return ('open', add(p, scale(1 - tau, v)))
        q = add(p, scale(t, v))
        if q in cset or s in (0, 1):
            return ('corner', tau + t, q)
        if tau + t == 1:
            return ('open', q)
        a, b = poly[k], poly[(k+1) % n]; w = sub(b, a)
        lam = F(2 * dot(v, w), dot(w, w))
        v = (lam * w[0] - v[0], lam * w[1] - v[1])
        p = q; tau += t
    raise RuntimeError('too many bounces')


def darkness(S, corners, bound):
    """Shoot from S toward every A point X != S with |X-S| <= bound edge lengths."""
    S = tuple(S); i0, j0 = map(int, lattice_coords(S))
    out = dict(directions=0, blocked=0, open=[], max_first_corner_tau=None, corner_labels={}, midpoint_rule_ok=True)
    R = bound
    for di in range(-2*R, 2*R+1):
        for dj in range(-2*R, 2*R+1):
            if (di, dj) == (0, 0): continue
            if di*di + di*dj + dj*dj > R*R: continue
            X = add(S, add(scale(di, E1), scale(dj, E2)))
            res = shoot(S, X, corners)
            out['directions'] += 1
            if res[0] == 'open':
                out['open'].append(dict(X=[di, dj], end=[str(c) for c in res[1]], end_label=label(res[1])))
            else:
                out['blocked'] += 1
                k = gcd(di, dj); lab = label(res[2])
                out['corner_labels'][lab] = out['corner_labels'].get(lab, 0) + 1
                # first primitive piece has its C midpoint at tau = 1/(2k)
                if res[1] > F(1, 2*k): out['midpoint_rule_ok'] = False
                m = out['max_first_corner_tau']
                out['max_first_corner_tau'] = res[1] if m is None or res[1] > m else m
    out['max_first_corner_tau'] = str(out['max_first_corner_tau'])
    out['open_count'] = len(out['open']); out['open'] = out['open'][:10]
    return out


def check(room, bound=30, quiet=False):
    info, corners = analyze(room['tiles'])
    marks = [tuple(room[k]) for k in ('S', 'T') if k in room] or [tuple(p) for p in info['interior_A']]
    info['dark_tests'] = {}
    for S in marks:
        assert list(S) in info['interior_A'], f'{S} is not an interior A point'
        info['dark_tests'][str(list(S))] = darkness(S, corners, bound)
    info['bound_edge_lengths'] = bound
    info['C_clean'] = not info['transparent_C']
    info['two_interior_A'] = len(info['interior_A']) >= 2
    info['all_blocked'] = all(d['open_count'] == 0 for d in info['dark_tests'].values())
    info['verdict'] = 'DARK (certified for paths of unfolded length <= bound; parity argument for all lengths)' if (
        info['C_clean'] and info['two_interior_A'] and info['all_blocked']) else 'NOT CERTIFIED DARK'
    return info


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('room'); ap.add_argument('--bound', type=int, default=30)
    a = ap.parse_args()
    room = json.load(open(a.room))
    info = check(room, a.bound)
    print(json.dumps(info, indent=1))
