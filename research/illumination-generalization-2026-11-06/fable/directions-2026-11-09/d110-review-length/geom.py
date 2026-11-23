"""D110: exact dumbbell geometry and an exact event tracer on polygon edges (own code).

A dumbbell: left chamber [0,d1]x[b1,b1+h1], corridor [d1,d1+L]x[p,p+w],
right chamber [d1+L,d1+L+d2]x[b2,b2+h2]. All data integral.
"""
from fractions import Fraction as F


def dumbbell(d1, b1, h1, d2, b2, h2, p, w, L):
    assert b1 < p and p + w < b1 + h1 and b2 < p and p + w < b2 + h2
    x2 = d1 + L
    V = [(0, b1), (d1, b1), (d1, p), (x2, p), (x2, b2), (x2 + d2, b2), (x2 + d2, b2 + h2),
         (x2, b2 + h2), (x2, p + w), (d1, p + w), (d1, b1 + h1), (0, b1 + h1)]
    return dict(d1=d1, b1=b1, h1=h1, d2=d2, b2=b2, h2=h2, p=p, w=w, L=L, V=V)


ROOMS = {  # d69-bbbb/decomp.py base rooms; the corridor length L is free
    'DBas': (5, 0, 4, 4, -1, 6, 1, 1),
    'DB55': (5, 0, 5, 5, 0, 5, 2, 1),
    'DBw2': (5, 0, 5, 5, 0, 6, 1, 2),
}


def room(name, L):
    return dumbbell(*ROOMS[name], L)


def shoot(V, s, d, t, maxev=10 ** 6):
    """Exact billiard from s in direction d. Returns (events, list of (x,y) wall hits) on
    reaching t; raises on any vertex hit. Edges are closed segments of the polygon V."""
    E = [(V[i], V[(i + 1) % len(V)]) for i in range(len(V))]
    Vs = set((F(a), F(b)) for a, b in V)
    p = (F(s[0]), F(s[1])); d = (F(d[0]), F(d[1])); t = (F(t[0]), F(t[1]))
    hits = []
    for _ in range(maxev):
        best = None
        for (a, b) in E:
            if a[0] == b[0]:
                if d[0] == 0: continue
                tt = (a[0] - p[0]) / d[0]
                if tt <= 0: continue
                y = p[1] + tt * d[1]
                if min(a[1], b[1]) <= y <= max(a[1], b[1]) and (best is None or tt < best[0]):
                    best = (tt, 'x', (F(a[0]), y))
            else:
                if d[1] == 0: continue
                tt = (a[1] - p[1]) / d[1]
                if tt <= 0: continue
                x = p[0] + tt * d[0]
                if min(a[0], b[0]) <= x <= max(a[0], b[0]) and (best is None or tt < best[0]):
                    best = (tt, 'y', (x, F(a[1])))
        tt, kind, q = best
        # target on the open segment (p, q)?
        u = (t[0] - p[0], t[1] - p[1])
        if u[0] * d[1] == u[1] * d[0]:
            tt_t = u[0] / d[0] if d[0] != 0 else u[1] / d[1]
            if 0 < tt_t < tt:
                return hits
        if q in Vs:
            raise RuntimeError(f"vertex hit at {q}")
        hits.append((kind, q))
        d = (-d[0], d[1]) if kind == 'x' else (d[0], -d[1])
        p = q
    raise RuntimeError("no arrival within maxev")
