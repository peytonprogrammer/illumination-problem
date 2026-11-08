"""Fixed-room ray check of the 15-wall pi/6 room R (Daniel approved 2026-11-02: "yes go ahead").

Fixed in advance. Room R and marks S=(-2,0), T=(2,0) from creative-reset/pi6-boundary-test.txt.
Coordinates (x, Y) with y = sqrt(3)*Y, so every quantity is rational; the metric is x^2 + 3Y^2.
Directions from S toward primitive A-lattice vectors u = (2a+b, b) with |u|^2 <= 1200 (any path S->T
unfolds to a segment between A points, so only these directions can reach T). Each ray is traced for
at most 200 reflections and stops at a corner, at T, or at the limit. Arrivals at O=(0,0) are recorded.
Every S->T path found is re-checked by verify(), which uses a separate containment test.
"""
import json
from fractions import Fraction as F
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
h, h2 = F(1, 3), F(2, 3)
V = [(-3, -h), (-2, -h2), (-1, -h), (-1, 0), (1, 0), (1, -h), (2, -h2), (3, -h), (3, h), (2, h2),
     (1, h), (0, h2), (-1, h), (-2, h2), (-3, h)]
V = [(F(x), F(y)) for x, y in V]
WALLS = list(zip(V, V[1:] + V[:1]))
S, T, O = (F(-2), F(0)), (F(2), F(0)), (F(0), F(0))


def dot(a, b):
    return a[0] * b[0] + 3 * a[1] * b[1]


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def reflect(d, w):
    k = 2 * dot(d, w) / dot(w, w)
    return (k * w[0] - d[0], k * w[1] - d[1])


def on_open_segment(q, p, d, tmax):
    r = sub(q, p)
    if cross(r, d) != 0:
        return False
    lam = r[0] / d[0] if d[0] else r[1] / d[1]
    return 0 < lam < tmax


def trace(d, max_ref=200):
    p, pts, hit_o = S, [S], False
    for _ in range(max_ref + 1):
        best = None
        for i, (a, b) in enumerate(WALLS):
            e = sub(b, a)
            den = cross(d, e)
            if den == 0:
                continue
            ap = sub(a, p)
            t, s = cross(ap, e) / den, cross(ap, d) / den
            if t > 0 and 0 <= s <= 1 and (best is None or t < best[0]):
                best = (t, s, i)
        t, s, i = best
        if on_open_segment(T, p, d, t):
            return "T", pts + [T], hit_o
        q = (p[0] + t * d[0], p[1] + t * d[1])
        if s in (0, 1):
            return "corner", pts + [q], hit_o
        hit_o |= q == O
        pts.append(q)
        a, b = WALLS[i]
        p, d = q, reflect(d, sub(b, a))
    return "limit", pts, hit_o


def inside(q):
    """Even-odd test for a point not on the boundary (separate from the tracer)."""
    c = False
    for a, b in WALLS:
        if (a[1] > q[1]) != (b[1] > q[1]):
            x = a[0] + (q[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            c ^= q[0] < x
    return c


def on_wall(q):
    for a, b in WALLS:
        if cross(sub(q, a), sub(b, a)) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) \
                and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return (a, b)
    return None


def verify(pts):
    assert pts[0] == S and pts[-1] == T and inside(S) and inside(T)
    for p, q in zip(pts, pts[1:]):
        for a, b in WALLS:  # no proper crossing of any wall, and no corner on the open segment
            d1, d2 = cross(sub(a, p), sub(q, p)), cross(sub(b, p), sub(q, p))
            d3, d4 = cross(sub(p, a), sub(b, a)), cross(sub(q, a), sub(b, a))
            assert not (d1 * d2 < 0 and d3 * d4 < 0), "segment crosses a wall"
        for v in V:
            r = sub(v, p)
            assert not (cross(r, sub(q, p)) == 0 and 0 < dot(r, sub(q, p)) < dot(sub(q, p), sub(q, p))), "corner on path"
        assert inside(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)), "segment leaves the room"
    for p, q, r in zip(pts, pts[1:], pts[2:]):
        w = on_wall(q)
        assert w and q not in V, "bounce is not on a wall interior"
        e = sub(w[1], w[0])
        din, dout = sub(q, p), sub(r, q)
        assert cross(dout, reflect(din, e)) == 0 and dot(dout, reflect(din, e)) > 0, "reflection law"
    return True


def main():
    dirs = sorted({(2 * a + b, b) for a in range(-40, 41) for b in range(-40, 41)
                   if (a, b) != (0, 0) and gcd(a, b) == 1 and (2 * a + b) ** 2 + 3 * b * b <= 1200},
                  key=lambda u: (u[0] ** 2 + 3 * u[1] ** 2, u))
    out, tally = [], {"T": 0, "corner": 0, "limit": 0, "O": 0}
    for u in dirs:
        res, pts, hit_o = trace((F(u[0]), F(u[1])))
        tally[res] += 1
        tally["O"] += hit_o
        row = {"u": u, "norm2": u[0] ** 2 + 3 * u[1] ** 2, "result": res, "reflections": len(pts) - 2 if res != "limit" else len(pts) - 1,
               "hits_O": hit_o}
        if res == "T":
            row["verified"] = verify(pts)
            row["path"] = [[str(c) for c in q] for q in pts]
        out.append(row)
    lit = [r for r in out if r["result"] == "T"]
    print("directions", len(dirs), tally, flush=True)
    for r in lit[:10]:
        print("LIT u=%s |u|^2=%d reflections=%d hits_O=%s path=%s" % (r["u"], r["norm2"], r["reflections"], r["hits_O"], r["path"]))
    json.dump({"directions": len(dirs), "tally": tally, "lit": lit, "rows": out}, open(HERE / "ray_check.json", "w"), indent=1)


if __name__ == "__main__":
    main()
