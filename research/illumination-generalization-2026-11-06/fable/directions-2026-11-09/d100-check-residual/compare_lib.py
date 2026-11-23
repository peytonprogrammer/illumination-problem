"""d100 shared parsing: cert2 PROD lines, census REG lines, exact point-in-convex-polygon."""
from fractions import Fraction as F


def pts(txt):
    a = list(map(int, txt.split()))
    assert a and len(a) % 3 == 0
    return [(F(x, d), F(y, d)) for x, y, d in zip(a[::3], a[1::3], a[2::3])]


def in_cell(p, c):
    return c[0] <= p[0] <= c[0] + 1 and c[1] <= p[1] <= c[1] + 1


def load(files, rooms):
    """cert2 output -> products [(r, a, b, src, P, W)], designated points {(r,a,b,cell): grid point}.

    The designated point of an end is the unique corner of its cell within 1/17 of every vertex of
    every polygon at that end; ends without a unique such corner are returned under key None.
    """
    mine, cand = [], {}
    for r, fn in enumerate(files):
        for line in open(fn):
            if not line.startswith('PROD '):
                continue
            h, u, v = line.split('|')
            a, b, src = map(int, h.split()[1:])
            P, W = pts(u), pts(v)
            mine.append((r, a, b, src, P, W))
            tgt = b if src == a else a
            for cell, poly in ((src, P), (tgt, W)):
                c = rooms[r][cell]
                assert all(in_cell(p, c) for p in poly), 'polygon outside its closed cell'
                ok = {(c[0] + i, c[1] + j) for i in (0, 1) for j in (0, 1)
                      if all(17 * max(abs(x - c[0] - i), abs(y - c[1] - j)) <= 1 for x, y in poly)}
                key = (r, a, b, cell)
                cand[key] = cand[key] & ok if key in cand else ok
    centers = {k: next(iter(v)) for k, v in cand.items() if len(v) == 1}
    centers[None] = sorted(k for k, v in cand.items() if len(v) != 1)
    return mine, centers


def load_census(fn):
    theirs, tcenters, n = {}, {}, 0
    for line in open(fn):
        if not line.startswith('REG '):
            continue
        h, u, v = line.split('|')
        r, i, j, src = map(int, h.split()[1:])
        r -= 1
        tgt = j if src == i else i
        P, W = pts(u), pts(v)
        theirs.setdefault((r, src, tgt), []).append((P, W))
        for cell, poly in ((src, P), (tgt, W)):
            tcenters[(r, i, j, cell)] = (round(poly[0][0]), round(poly[0][1]))
        n += 1
    return theirs, tcenters, n


def inside(p, poly):
    """p in the closed convex hull of poly (convex vertex list of dimension 0, 1 or 2)."""
    n = len(poly)
    if n == 1:
        return p == poly[0]
    if n == 2:
        (x0, y0), (x1, y1) = poly
        cr = (x1 - x0) * (p[1] - y0) - (y1 - y0) * (p[0] - x0)
        return cr == 0 and min(x0, x1) <= p[0] <= max(x0, x1) and min(y0, y1) <= p[1] <= max(y0, y1)
    s = set()
    for k in range(n):
        (x0, y0), (x1, y1) = poly[k], poly[(k + 1) % n]
        cr = (x1 - x0) * (p[1] - y0) - (y1 - y0) * (p[0] - x0)
        if cr:
            s.add(cr > 0)
    return len(s) <= 1


def in_census(theirs, r, src, tgt, S, T):
    return any(inside(S, p) and inside(T, w) for p, w in theirs.get((r, src, tgt), [])) or \
        any(inside(T, p) and inside(S, w) for p, w in theirs.get((r, tgt, src), []))
