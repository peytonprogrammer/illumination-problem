"""D113 own geometry + exact polygon tracer (Fractions). No shared code with d109/d112."""
from fractions import Fraction as F
from math import gcd
from functools import reduce


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def occ(C, X, Y):
    return [(X - 1, Y - 1) in C, (X - 1, Y) in C, (X, Y - 1) in C, (X, Y) in C]


def kind(C, X, Y):
    o = occ(C, X, Y); k = sum(o)
    if k == 0: return 'out'
    if k == 4: return 'interior'
    if k == 3: return 'reflex'
    if k == 1: return 'convex'
    if o[0] == o[3]: return 'pinch'
    return 'smooth'


def polygon(C):
    """Boundary cycle (ccw, interior on the left); asserts a single simple cycle (no pinch)."""
    nxt = {}
    for (x, y) in C:
        for a, b, nb in [((x, y), (x + 1, y), (x, y - 1)), ((x + 1, y), (x + 1, y + 1), (x + 1, y)),
                         ((x + 1, y + 1), (x, y + 1), (x, y + 1)), ((x, y + 1), (x, y), (x - 1, y))]:
            if nb not in C:
                assert a not in nxt, ('pinch', a)
                nxt[a] = b
    start = min(nxt); cyc = [start]; p = nxt[start]
    while p != start:
        cyc.append(p); p = nxt[p]
    assert len(cyc) == len(nxt), 'more than one boundary component'
    V = [v for v in cyc if kind(C, *v) in ('reflex', 'convex')]
    return V


def summary(C):
    V = polygon(C)
    E = list(zip(V, V[1:] + V[:1]))
    refl = [v for v in V if kind(C, *v) == 'reflex']
    hl = [abs(b[0] - a[0]) for a, b in E if a[1] == b[1]]
    vl = [abs(b[1] - a[1]) for a, b in E if a[0] == b[0]]
    xs = [x for x, _ in C] ; ys = [y for _, y in C]
    cls = {}
    for X in range(min(xs), max(xs) + 2):
        for Y in range(min(ys), max(ys) + 2):
            k = kind(C, X, Y)
            if k == 'out': continue
            cls.setdefault((X % 2, Y % 2), {}).setdefault(k, 0)
            cls[(X % 2, Y % 2)][k] += 1
    qfree = all(c.get('interior', 0) + c.get('smooth', 0) > 0 for c in cls.values()) and len(cls) == 4
    return dict(W=len(V), r=len(refl), area=len(C), gcd_h=reduce(gcd, hl), gcd_v=reduce(gcd, vl),
                reflex=refl, classes=cls, no_corner_only_class=qfree, V=V)


class Corner(Exception):
    pass


def shoot(V, p, d, stop, maxev=20000):
    """Trace from p in direction d. stop(a,b) -> value or None, called on every straight segment.
    Raises Corner on a vertex hit."""
    V = [(F(x), F(y)) for x, y in V]
    E = list(zip(V, V[1:] + V[:1])); Vs = set(V)
    p = (F(p[0]), F(p[1])); d = (F(d[0]), F(d[1])); ev = []
    for _ in range(maxev):
        best = None
        for a, b in E:
            if a[0] == b[0]:
                if d[0] == 0: continue
                t = (a[0] - p[0]) / d[0]
                if t <= 0: continue
                y = p[1] + t * d[1]
                if min(a[1], b[1]) <= y <= max(a[1], b[1]) and (best is None or t < best[0]):
                    best = (t, 'v', (a[0], y))
            else:
                if d[1] == 0: continue
                t = (a[1] - p[1]) / d[1]
                if t <= 0: continue
                x = p[0] + t * d[0]
                if min(a[0], b[0]) <= x <= max(a[0], b[0]) and (best is None or t < best[0]):
                    best = (t, 'h', (x, a[1]))
        t, k, q = best
        r = stop(p, q, d)
        if r is not None:
            return r, ev
        if q in Vs:
            raise Corner(q)
        ev.append((k, q))
        d = (-d[0], d[1]) if k == 'v' else (d[0], -d[1])
        p = q
    return None, ev


def first_cross(X):
    """stop at the first crossing of the vertical line x=X; return (y, vertical direction sign)."""
    def f(a, b, d):
        if (a[0] - X) * (b[0] - X) < 0 or (b[0] == X and False):
            y = a[1] + (X - a[0]) * (b[1] - a[1]) / (b[0] - a[0])
            return (y, 1 if d[1] > 0 else -1)
        return None
    return f


def reach(T):
    T = (F(T[0]), F(T[1]))
    def f(a, b, d):
        # T strictly inside segment (a,b]?
        if (T[0] - a[0]) * d[1] == (T[1] - a[1]) * d[0]:
            lam = (T[0] - a[0]) / d[0] if d[0] else (T[1] - a[1]) / d[1]
            lb = (b[0] - a[0]) / d[0] if d[0] else (b[1] - a[1]) / d[1]
            if 0 < lam <= lb:
                return 'reach'
        return None
    return f
