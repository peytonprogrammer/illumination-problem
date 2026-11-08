"""Exact lighting certificates for marks s=(0,0) and q in the canonical 45-degree tiling.

A certificate is (U, Z): tile sets such that any room using every tile of U and no tile of
Z contains a billiard path from s to q. Paths have 0, 1 or 2 reflections off lines of the
tiling arrangement (x = c, y = c, x - y = 2c, x + y = 2c).
- Every open segment point must be interior to the room. Inside a tile, that tile is used.
  On an edge, both tiles of the edge are used. At a vertex, every tile around it is used.
- Each reflection point lies inside an edge on the mirror line, never at a vertex. The tile
  on the incoming side is used and the tile across is unused, so that edge is a wall.
Nothing depends on the rest of the room, so a satisfied certificate stays satisfied in
every completion. Exact Fractions throughout.
"""
from fractions import Fraction as F
from itertools import product


def tile_at(x, y):
    """The canonical tile whose interior contains (x, y), given (x, y) is not on any tiling line."""
    i, j = x.numerator//x.denominator, y.numerator//y.denominator
    sq = [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]
    a = next(p for p in sq if p[0] % 2 == 0 and p[1] % 2 == 0)
    b = next(p for p in sq if p[0] % 2 and p[1] % 2)
    # the diagonal a-b splits the square; pick the C corner on the same side as (x, y)
    side = lambda p: (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
    s = side((x, y))
    c = next(p for p in sq if p not in (a, b) and (side(p) > 0) == (s > 0))
    return tuple(sorted([a, b, c]))


def on_lines(x, y):
    return x.denominator == 1 or y.denominator == 1 or ((x-y)/2).denominator == 1 or ((x+y)/2).denominator == 1


PROBES = [(5, 1), (3, 2), (2, 3), (1, 5), (-1, 5), (-2, 3), (-3, 2), (-5, 1),
          (-5, -1), (-3, -2), (-2, -3), (-1, -5), (1, -5), (2, -3), (3, -2), (5, -1)]


def around(x, y, eps=F(1, 1000)):
    """Tiles whose closure contains (x, y): probe two directions inside every 45-degree sector."""
    out = set()
    for u, v in PROBES:
        px, py = x+u*eps, y+v*eps
        assert not on_lines(px, py)
        out.add(tile_at(px, py))
    return out


def crossings(a, b):
    """Parameters in (0, 1) where segment a-b meets a tiling line."""
    ts = set()
    (ax, ay), (bx, by) = a, b
    dx, dy = bx-ax, by-ay
    lo, hi = int(min(ax, bx, ay, by, ax-ay, bx-by, ax+ay, bx+by))-2, int(max(ax, bx, ay, by, ax-ay, bx-by, ax+ay, bx+by))+2
    for c in range(lo, hi+1):
        for num, den in ((c-ax, dx), (c-ay, dy)):
            if den:
                ts.add(F(num)/den)
        for num, den in ((c-(ax-ay), dx-dy), (c-(ax+ay), dx+dy)):
            if den and c % 2 == 0:
                ts.add(F(num)/den)
    return sorted(t for t in ts if 0 < t < 1)


def segment_tiles(a, b):
    """Tiles that must be used for the open segment a-b to lie in the room's interior."""
    need = set()
    cuts = [F(0)] + crossings(a, b) + [F(1)]
    pt = lambda t: (a[0]+t*(b[0]-a[0]), a[1]+t*(b[1]-a[1]))
    for t in cuts[1:-1]:
        need |= around(*pt(t))
    for t0, t1 in zip(cuts, cuts[1:]):
        m = pt((t0+t1)/2)
        need |= {tile_at(*m)} if not on_lines(*m) else around(*m)
    return need


def reflect(p, line):
    kind, c = line
    x, y = p
    return {'x': (2*c-x, y), 'y': (x, 2*c-y), 'd': (y+c, x-c), 's': (c-y, c-x)}[kind]


def hit(a, b, line):
    """Parameter where segment a-b meets the line, or None."""
    kind, c = line
    (ax, ay), (bx, by) = a, b
    f = {'x': lambda x, y: x-c, 'y': lambda x, y: y-c, 'd': lambda x, y: x-y-c, 's': lambda x, y: x+y-c}[kind]
    fa, fb = f(ax, ay), f(bx, by)
    if fa == fb:
        return None
    t = F(fa)/(fa-fb)
    return t if 0 < t < 1 else None


def wall(p, line, came_from):
    """(used, unused) tiles making p an interior wall point on line, or None if p is a vertex."""
    if p[0].denominator == 1 and p[1].denominator == 1:
        return None
    tiles = around(*p)
    if len(tiles) != 2:
        return None
    kind, c = line
    f = {'x': lambda x, y: x-c, 'y': lambda x, y: y-c, 'd': lambda x, y: x-y-c, 's': lambda x, y: x+y-c}[kind]
    side = f(*came_from) > 0
    t1, t2 = sorted(tiles)
    cen = lambda t: (F(sum(v[0] for v in t), 3), F(sum(v[1] for v in t), 3))
    used = t1 if (f(*cen(t1)) > 0) == side else t2
    return used, (t2 if used == t1 else t1)


def lines(R):
    out = [('x', c) for c in range(-R, R+1)] + [('y', c) for c in range(-R, R+1)]
    out += [('d', c) for c in range(-2*R, 2*R+1, 2)] + [('s', c) for c in range(-2*R, 2*R+1, 2)]
    return out


def certificates(q, R=10, max_refl=2):
    s = (F(0), F(0)); t = (F(q[0]), F(q[1]))
    certs = [(frozenset(segment_tiles(s, t)), frozenset(), (s, t))]
    L = lines(R)
    if max_refl >= 1:
        for l1 in L:
            t1 = reflect(t, l1)
            u = hit(s, t1, l1)
            if u is None:
                continue
            p = (s[0]+u*(t1[0]-s[0]), s[1]+u*(t1[1]-s[1]))
            w = wall(p, l1, s)
            if w is None:
                continue
            U = segment_tiles(s, p) | segment_tiles(p, t) | {w[0]}
            if w[1] not in U:
                certs.append((frozenset(U), frozenset([w[1]]), (s, p, t)))
    if max_refl >= 2:
        for l1 in L:
            for l2 in L:
                if l1 == l2:
                    continue
                t2 = reflect(t, l2); t1 = reflect(t2, l1)
                u = hit(s, t1, l1)
                if u is None:
                    continue
                p1 = (s[0]+u*(t1[0]-s[0]), s[1]+u*(t1[1]-s[1]))
                v = hit(p1, t2, l2)
                if v is None:
                    continue
                p2 = (p1[0]+v*(t2[0]-p1[0]), p1[1]+v*(t2[1]-p1[1]))
                w1, w2 = wall(p1, l1, s), wall(p2, l2, p1)
                if w1 is None or w2 is None:
                    continue
                U = segment_tiles(s, p1) | segment_tiles(p1, p2) | segment_tiles(p2, t) | {w1[0], w2[0]}
                Z = {w1[1], w2[1]}
                if not U & Z:
                    certs.append((frozenset(U), frozenset(Z), (s, p1, p2, t)))
    # keep only minimal certificates (drop any implied by a smaller one)
    certs = sorted({c[:2]: c for c in certs}.values(), key=lambda c: len(c[0])+len(c[1]))
    keep = []
    for c in certs:
        if not any(k[0] <= c[0] and k[1] <= c[1] for k in keep):
            keep.append(c)
    return keep
