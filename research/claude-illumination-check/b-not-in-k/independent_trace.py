"""Second tracer for core_loads.py: ray against the 25 wall segments, not the triangle grid.

Shares only the 28-triangle room list with core_loads.py. Checks every saved core:
closure, corner avoidance, inside-room segments, D/H hit counts, and Q.
"""
import json
import sys
from fractions import Fraction as F
from collections import Counter
import importlib.util

spec = importlib.util.spec_from_file_location("cl", "core_loads.py")
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)

E = Counter()
for t in cl.TRIANGLES:
    for i in range(3):
        E[tuple(sorted((t[i], t[(i + 1) % 3])))] += 1
WALLS = [e for e, n in E.items() if n == 1]
CORNERS = {p for e in WALLS for p in e}


def inside(pt):
    """Closed-triangle test; chord midpoints can lie on shared interior edges."""
    x, y = pt
    for a, b, c in cl.TRIANGLES:
        d1 = (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0])
        d2 = (c[0] - b[0]) * (y - b[1]) - (c[1] - b[1]) * (x - b[0])
        d3 = (a[0] - c[0]) * (y - c[1]) - (a[1] - c[1]) * (x - c[0])
        if (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0):
            return True
    return False


def hit(z, v, seg):
    (ax, ay), (bx, by) = seg
    ex, ey = bx - ax, by - ay
    den = v[0] * ey - v[1] * ex
    if den == 0:
        return None
    t = F((ax - z[0]) * ey - (ay - z[1]) * ex) / den
    s = F((ax - z[0]) * v[1] - (ay - z[1]) * v[0]) / den
    if t <= 0 or s < 0 or s > 1:
        return None
    assert 0 < s < 1, "path meets a wall endpoint"
    return t, seg


def reflect(v, seg):
    (ax, ay), (bx, by) = seg
    ex, ey = bx - ax, by - ay
    k = F(2 * (v[0] * ex + v[1] * ey), ex * ex + ey * ey)
    return (k * ex - v[0], k * ey - v[1])


DSEG = ((1, 1), (2, 0))
HSEG = ((1, 0), (2, 0))


def lin_of(seg):
    (ax, ay), (bx, by) = seg
    ex, ey = bx - ax, by - ay
    n2 = ex * ex + ey * ey
    return ((F(ex * ex - ey * ey, n2), F(2 * ex * ey, n2)), (F(2 * ex * ey, n2), F(ey * ey - ex * ex, n2)))


def core(z0, v0, theta):
    L0 = cl.frame_to(theta, v0)
    L = tuple(tuple(F(x) for x in r) for r in L0)
    z, v = z0, v0
    Q = [F(0), F(0)]
    nD = nH = hits = 0
    while True:
        best = min((h for h in (hit(z, v, w) for w in WALLS) if h), key=lambda h: h[0])
        t, seg = best
        p = (z[0] + t * v[0], z[1] + t * v[1])
        assert inside(((z[0] + p[0]) / 2, (z[1] + p[1]) / 2)), "segment leaves the room"
        assert p not in CORNERS
        hits += 1
        if seg in (DSEG, HSEG):
            a = (1, 1) if seg == DSEG else (0, 2)
            Q[0] += L[0][0] * a[0] + L[0][1] * a[1]
            Q[1] += L[1][0] * a[0] + L[1][1] * a[1]
            nD += seg == DSEG
            nH += seg == HSEG
        L = cl.matmul(L, lin_of(seg))
        v = reflect(v, seg)
        z = p
        if z == z0 and v == v0 and L == L0:
            return hits, nD, nH, [int(Q[0]), int(Q[1])]


J = json.load(open(sys.argv[1]))
assert sorted(map(tuple, (tuple(sorted(e)) for e in WALLS))) and len(WALLS) == 26
bad = 0
for d in J["directions"]:
    th = tuple(d["theta"])
    for c in d["cores"]:
        x0 = F(c["start_x_on_D"])
        got = core((x0, 2 - x0), tuple(c["start_velocity"]), th)
        want = (c["wall_hits"], c["D_hits"], c["H_hits"], c["Q"])
        ok = got == want
        bad += not ok
        print(th, c["start_x_on_D"], c["start_velocity"], "OK" if ok else f"MISMATCH {got} vs {want}")
print("mismatches", bad)
sys.exit(1 if bad else 0)
