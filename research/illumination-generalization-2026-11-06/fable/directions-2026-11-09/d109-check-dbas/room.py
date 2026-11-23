"""DBas family: chambers [0,5]x[0,4] and [5+l,9+l]x[-1,5], corridor [5,5+l]x[1,2].
l=4 is DBas (d69-bbbb/decomp.py: rect(0,5,0,4)|rect(5,9,1,2)|rect(9,13,-1,5))."""
from fractions import Fraction as F


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def cells(l):
    return rect(0, 5, 0, 4) | rect(5, 5 + l, 1, 2) | rect(5 + l, 9 + l, -1, 5)


def marks(l):
    c = 2 if l % 2 == 0 else 1
    return (F(1), F(3)), (F(5 + l + c), F(3)), c


def is_corner(C, X, Y):
    o = [(X - i, Y - j) in C for i in (1, 0) for j in (1, 0)]
    k = sum(o)
    return k in (1, 3) or (k == 2 and o[0] == o[3])


def is_reflex(C, X, Y):
    return sum((X - i, Y - j) in C for i in (1, 0) for j in (1, 0)) == 3


def boundary_cycle(C):
    """Vertices of the boundary in order (assumes one simple boundary cycle)."""
    edges = {}
    for (x, y) in C:
        for (a, b, c, d), nb in [((x, y, x + 1, y), (x, y - 1)), ((x + 1, y, x + 1, y + 1), (x + 1, y)),
                                 ((x + 1, y + 1, x, y + 1), (x, y + 1)), ((x, y + 1, x, y), (x - 1, y))]:
            if nb not in C:
                edges.setdefault((a, b), []).append((c, d))
    start = min(edges)
    cyc, p, nedge = [start], start, 0
    while True:
        assert len(edges[p]) == 1, ("pinch at", p)  # strict simplicity: out-degree 1 everywhere
        p = edges[p][0]; nedge += 1
        if p == start:
            break
        cyc.append(p)
    assert nedge == sum(len(v) for v in edges.values()), "more than one boundary component"
    return [v for v in cyc if is_corner(C, *v)]
