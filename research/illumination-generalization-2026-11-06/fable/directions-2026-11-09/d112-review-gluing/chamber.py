"""D112: own exact tracer for sealed orthogonal chambers and full dumbbell rooms.

Chambers are lists of vertices (Fractions). The mouth is one vertical edge of
the sealed chamber, given by (x, ylo, yhi). A leg is the ray from a mark at
slope magnitude s with initial signs (hx, hy), followed until its first hit of
the open mouth. Any hit at a vertex, including a mouth endpoint, raises
Irregular. The leg records the signed state at every cut crossing and every
vertical-wall contact (horizontal reflections are not recorded).
"""
from fractions import Fraction as F
from math import gcd


class Irregular(Exception):
    pass


def Fr(v):
    return v if isinstance(v, F) else F(v)


def rect_poly(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def edges(V):
    out = []
    for i in range(len(V)):
        a, b = V[i], V[(i + 1) % len(V)]
        out.append((a, b))
    return out


def next_hit(E, Vs, p, d):
    best = None
    for (a, b) in E:
        if a[0] == b[0]:
            if d[0] == 0:
                continue
            t = (a[0] - p[0]) / d[0]
            if t <= 0:
                continue
            y = p[1] + t * d[1]
            if min(a[1], b[1]) <= y <= max(a[1], b[1]) and (best is None or t < best[0]):
                best = (t, 'v', (a[0], y), (a, b))
        else:
            if d[1] == 0:
                continue
            t = (a[1] - p[1]) / d[1]
            if t <= 0:
                continue
            x = p[0] + t * d[0]
            if min(a[0], b[0]) <= x <= max(a[0], b[0]) and (best is None or t < best[0]):
                best = (t, 'h', (x, a[1]), (a, b))
    return best


def leg(V, mouth, cuts, S, s, hx, hy, maxev=100000):
    """Return dict(states, exit=(y, sx, sy), a=horizontal travel, nh, nv)."""
    V = [(Fr(x), Fr(y)) for x, y in V]
    E = edges(V)
    Vs = set(V)
    xm, ylo, yhi = (Fr(t) for t in mouth)
    cuts = sorted(set(Fr(c) for c in cuts))
    p = (Fr(S[0]), Fr(S[1]))
    d = (F(hx), F(hy) * Fr(s))
    states, a, nh, nv = [], F(0), 0, 0
    for _ in range(maxev):
        t, kind, q, e = next_hit(E, Vs, p, d)
        if q in Vs:
            raise Irregular(f"vertex {q}")
        x0, x1 = p[0], q[0]
        lo, hi = min(x0, x1), max(x0, x1)
        sy = 1 if d[1] > 0 else -1
        seg = [c for c in cuts if lo < c < hi]
        seg.sort(reverse=(d[0] < 0))
        for c in seg:
            y = p[1] + (c - x0) / d[0] * d[1]
            states.append(('cut', c, y, sy))
        a += hi - lo
        if kind == 'h':
            nh += 1
            if q[0] in cuts and q[0] != x0:  # artificial cut through a horizontal reflection
                states.append(('cut', q[0], q[1], -sy))
            d = (d[0], -d[1])
        else:
            if q[0] == xm and ylo < q[1] < yhi:
                return dict(states=states, exit=(q[1], 1 if d[0] > 0 else -1, sy), a=a, nh=nh, nv=nv)
            nv += 1
            states.append(('wall', q[0], q[1], sy))
            d = (-d[0], d[1])
        p = q
    raise Irregular("no mouth within maxev")


def slab_period(V, cuts):
    """Least K>0 with K*d/P integral for every slab rectangle; P = doubled height."""
    V = [(Fr(x), Fr(y)) for x, y in V]
    cuts = sorted(set(Fr(c) for c in cuts))
    E = edges(V)
    K = None
    rects = []
    for c0, c1 in zip(cuts, cuts[1:]):
        xm = (c0 + c1) / 2
        ys = sorted(a[1] for a, b in E if a[1] == b[1] and min(a[0], b[0]) < xm < max(a[0], b[0]))
        for y0, y1 in zip(ys[0::2], ys[1::2]):
            d, P = c1 - c0, 2 * (y1 - y0)
            rects.append((c0, c1, y0, y1))
            K = lcm_rat(K, P / d) if K is not None else P / d
    return K, rects


def lcm_rat(a, b):
    # lcm(p1/q1, p2/q2) = lcm(p1,p2)/gcd(q1,q2)
    p = a.numerator * b.numerator // gcd(a.numerator, b.numerator)
    return F(p, gcd(a.denominator, b.denominator))


def gcd_rat(a, b):
    # gcd(p1/q1, p2/q2) = gcd(p1,p2)/lcm(q1,q2)
    q = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    return F(gcd(a.numerator, b.numerator), q)


def reflex_count(V):
    """Number of reflex vertices of a CCW orthogonal polygon (collinear points ignored)."""
    V = [(Fr(x), Fr(y)) for x, y in V]
    area2 = sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1] for i in range(len(V)))
    sgn = 1 if area2 > 0 else -1
    r = walls = 0
    for i in range(len(V)):
        a, b, c = V[i - 1], V[i], V[(i + 1) % len(V)]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if cr == 0:
            continue
        walls += 1
        if cr * sgn < 0:
            r += 1
    return r, walls


def shoot_room(V, S, d, T, maxev=200000):
    """Full-room exact trace from S in direction d. Return list of wall hits before T; raise on vertex."""
    V = [(Fr(x), Fr(y)) for x, y in V]
    E = edges(V)
    Vs = set(V)
    p = (Fr(S[0]), Fr(S[1])); d = (Fr(d[0]), Fr(d[1])); T = (Fr(T[0]), Fr(T[1]))
    hits = []
    for _ in range(maxev):
        t, kind, q, e = next_hit(E, Vs, p, d)
        u = (T[0] - p[0], T[1] - p[1])
        if u[0] * d[1] == u[1] * d[0]:
            tt = u[0] / d[0] if d[0] != 0 else u[1] / d[1]
            if 0 < tt < t:
                return hits
        if q in Vs:
            raise Irregular(f"vertex {q}")
        hits.append((kind, q))
        d = (-d[0], d[1]) if kind == 'v' else (d[0], -d[1])
        p = q
    raise Irregular("no arrival")
