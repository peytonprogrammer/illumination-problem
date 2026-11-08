"""Function-only frozen excerpt; no library reads, random sampling or CLI execution."""
import json, random, sys
from fractions import Fraction as F

def cr(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def where(T, p):
    s = [cr(T[i], T[(i + 1) % 3], p) for i in range(3)]
    if all((x > 0 for x in s)) or all((x < 0 for x in s)):
        return 'in'
    if all((x >= 0 for x in s)) or all((x <= 0 for x in s)):
        return 'vertex' if p in T else 'edge'
    return 'out'

def status(p, U, Z):
    """'int' if p is interior to the union of U (every triangle touching p is in U, and p is covered),
       'wall' if touching triangles are in U on one side of a line and Z on the other (straight wall), else 'bad'."""
    touch = [(T, 'U') for T in U if where(T, p) != 'out'] + [(T, 'Z') for T in Z if where(T, p) != 'out']
    return touch

def tiles_at(p):
    import math
    out = []
    for x in range(math.floor(p[0]) - 1, math.floor(p[0]) + 2):
        for y in range(math.floor(p[1]) - 1, math.floor(p[1]) + 2):
            c = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
            k = [i for i in range(4) if c[i][0] % 2 == 0 and c[i][1] % 2 == 0][0]
            a, b = (c[k], c[(k + 2) % 4])
            for o in (c[(k + 1) % 4], c[(k + 3) % 4]):
                T = (a, b, o)
                if where(T, p) != 'out':
                    out.append(frozenset(T))
    return set(out)

def check(g):
    U = {frozenset((tuple(v) for v in T)) for T in g['U']}
    Z = {frozenset((tuple(v) for v in T)) for T in g['Z']}
    P = [(F(x[0], x[1]), F(y[0], y[1])) for x, y in g['path']]
    if P[0] != (0, 0) or P[-1] != (g['q'][0], g['q'][1]):
        return 'endpoints'
    if U & Z:
        return 'U∩Z'
    for a, b in zip(P, P[1:]):
        ts = {F(0), F(1)}
        for T in [tuple(T) for T in U | Z]:
            for i in range(3):
                p, q = (T[i], T[(i + 1) % 3])
                d = (b[0] - a[0], b[1] - a[1])
                e = (q[0] - p[0], q[1] - p[1])
                den = d[0] * e[1] - d[1] * e[0]
                if den == 0:
                    continue
                w = (p[0] - a[0], p[1] - a[1])
                t = F(w[0] * e[1] - w[1] * e[0], 1) / den
                if 0 < t < 1:
                    ts.add(t)
        ts = sorted(ts)
        pts = [(a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])) for t in ts]
        mids = [((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) for p, q in zip(pts, pts[1:])]
        for m in mids + pts[1:-1]:
            if not tiles_at(m) <= U:
                return 'segment leaves U-interior at %s' % (m,)
    for a, p, b in zip(P, P[1:], P[2:]):
        T = tiles_at(p)
        if not T <= U | Z:
            return 'bounce tiles undetermined at %s' % (p,)
        inU = {t for t in T if t in U}
        inZ = T - inU
        if not inU or not inZ:
            return 'bounce not on wall at %s' % (p,)
        lines = [(1, 0), (0, 1), (1, 1), (1, -1)]
        ok = None
        for n in lines:

            def side(t):
                c = (sum((F(v[0]) for v in t)) / 3, sum((F(v[1]) for v in t)) / 3)
                return (c[0] - p[0]) * n[0] + (c[1] - p[1]) * n[1]
            on = any((where((t[i], t[(i + 1) % 3], t[i]), p) != 'out' and (t[(i + 1) % 3][0] - t[i][0]) * n[0] + (t[(i + 1) % 3][1] - t[i][1]) * n[1] == 0 and (cr(t[i], t[(i + 1) % 3], p) == 0) and (min(t[i][0], t[(i + 1) % 3][0]) <= p[0] <= max(t[i][0], t[(i + 1) % 3][0])) and (min(t[i][1], t[(i + 1) % 3][1]) <= p[1] <= max(t[i][1], t[(i + 1) % 3][1])) for t in [tuple(t) for t in T] for i in range(3)))
            if not on:
                continue
            if all((side(t) > 0 for t in inU)) and all((side(t) < 0 for t in inZ)) or (all((side(t) < 0 for t in inU)) and all((side(t) > 0 for t in inZ))):
                if ok is not None and ok != n:
                    return 'ambiguous wall at %s' % (p,)
                ok = n
        if ok is None:
            return 'bounce not straight wall at %s' % (p,)
        n = ok
        din = (p[0] - a[0], p[1] - a[1])
        dout = (b[0] - p[0], b[1] - p[1])
        nn = n[0] * n[0] + n[1] * n[1]
        k = 2 * (din[0] * n[0] + din[1] * n[1]) / nn
        r = (din[0] - k * n[0], din[1] - k * n[1])
        if r[0] * dout[1] - r[1] * dout[0] != 0 or r[0] * dout[0] + r[1] * dout[1] <= 0:
            return 'reflection law at %s' % (p,)
    return 'ok'
from collections import Counter
