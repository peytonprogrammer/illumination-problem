"""Own exact billiard tracer for an orthogonal polygon with Q(sqrt2) coordinates.

Independent of the note's unfolding: it follows the physical ray wall by wall.
Corner avoidance: any hit at a polygon vertex (convex or reflex) kills the ray.
Direction is (hx, hy*s) with hx, hy in {+1,-1}, s > 0 in Q(sqrt2).
"""
from qr2 import Q2


def edges(poly):
    E = []
    n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if x0 == x1:
            E.append(("v", x0, min(y0, y1), max(y0, y1)))
        else:
            assert y0 == y1
            E.append(("h", y0, min(x0, x1), max(x0, x1)))
    return E


def trace(poly, S, T, s, hx, hy, maxhits=10**7):
    """Return (lit, nh, nv, reason). nh/nv count horizontal/vertical wall hits before T."""
    E = edges(poly)
    px, py = S
    tx, ty = T
    nh = nv = 0
    sinv = s.inv()
    for _ in range(maxhits):
        best = None
        for kind, c, lo, hi in E:
            if kind == "v":
                t = (c - px) * hx  # horizontal travel
                if t.sign() <= 0:
                    continue
                y = py + s * t * hy
                if lo <= y <= hi:
                    hit = (t, kind, c, y, y == lo or y == hi)
                else:
                    continue
            else:
                dy = (c - py) * hy
                if dy.sign() <= 0:
                    continue
                t = dy * sinv
                x = px + t * hx
                if lo <= x <= hi:
                    hit = (t, kind, x, c, x == lo or x == hi)
                else:
                    continue
            if best is None or hit[0] < best[0]:
                best = hit
            elif hit[0] == best[0]:
                best = (best[0], best[1], best[2], best[3], True)  # two walls at once: a vertex
        assert best is not None, "ray escaped: polygon not closed?"
        t, kind = best[0], best[1]
        # target on the open segment before the hit?
        lam = (tx - px) * hx
        if lam.sign() > 0 and lam < t and ty == py + s * lam * hy:
            return True, nh, nv, "lit"
        if best[4]:
            return False, nh, nv, "vertex"
        if kind == "v":
            px, py = best[2], best[3]
            hx = -hx
            nv += 1
        else:
            px, py = best[2], best[3]
            hy = -hy
            nh += 1
    return False, nh, nv, "maxhits"
