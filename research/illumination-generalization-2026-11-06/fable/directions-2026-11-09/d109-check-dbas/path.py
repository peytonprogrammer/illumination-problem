"""Exact (Fraction) event tracer on the polygon edges, plus replay with d103's unfolded tracer.
Usage: python3 -B path.py            (DBas shot + family scan over prime n <= NMAX)"""
import sys
from fractions import Fraction as F
from pathlib import Path
from room import cells, marks, boundary_cycle, is_corner
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd103-twenty-check'))
import tracer as T103


def edges(C):
    v = boundary_cycle(C)
    return v, [(v[i], v[(i + 1) % len(v)]) for i in range(len(v))]


def shoot(C, s, d, t, maxev=10000):
    """Return list of events (kind, point) from s in direction d until t is reached, or raise."""
    verts, E = edges(C)
    V = set(verts)
    p, ev = s, []
    for _ in range(maxev):
        # target on current ray?
        best = None
        for (a, b) in E:
            if a[0] == b[0]:  # vertical edge x=a0
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
        # target strictly before the wall?
        if d[0] != 0:
            ttT = (t[0] - p[0]) / d[0]
        else:
            ttT = (t[1] - p[1]) / d[1]
        if 0 < ttT < tt and p[0] + ttT * d[0] == t[0] and p[1] + ttT * d[1] == t[1]:
            ev.append(('reach', t)); return ev
        if q in V or any(q == (F(x), F(y)) for (x, y) in V):
            raise RuntimeError(f"corner hit at {q}")
        # simultaneous hit of two edges at a non-vertex point cannot happen for a simple polygon
        ev.append(('reflect-' + ('vertical wall' if kind == 'x' else 'horizontal wall'), q))
        d = (-d[0], d[1]) if kind == 'x' else (d[0], -d[1])
        p = q
    raise RuntimeError("no arrival")


def doors(l, s, d, ev):
    """Heights where the polyline crosses x=5 and x=5+l (door abscissae)."""
    pts = [s] + [q for _, q in ev]
    out = []
    for a, b in zip(pts, pts[1:]):
        for X in (5, 5 + l):
            if (a[0] - X) * (b[0] - X) < 0:
                out.append((X, a[1] + (X - a[0]) * (b[1] - a[1]) / (b[0] - a[0])))
    return out


def fmt(p):
    return '(' + ','.join(str(z) for z in p) + ')'


def construct(l):
    """Return (b, list of admissible slopes m=2k/(l+4+b)) from the note's criterion."""
    _, _, c = marks(l)
    b = 8 - c
    Lh = l + 4 + b
    ks = [k for k in range(1, Lh) if F(1, 4) < F(2 * k, Lh) < F(2, b)]
    return b, [F(2 * k, Lh) for k in ks]


def check(l, m, verbose=False):
    C = cells(l); S, T, c = marks(l)
    d = (m.denominator, -m.numerator)
    ev = shoot(C, S, (F(d[0]), F(d[1])), T)
    dr = doors(l, S, d, ev)
    b = 8 - c
    v = (F(l + 4 + b), -m * (l + 4 + b))
    end103 = T103.trace(C, S, v)
    hreversals = sum(1 for k, _ in ev if k == 'reflect-vertical wall')
    ok = end103 == T and all(1 < y < 2 for _, y in dr) and hreversals == 1
    if verbose:
        print(f"l={l} n={len(C)} S={fmt(S)} T={fmt(T)} m={m} dir={d}")
        for k, q in ev:
            print(f"   {k:28s} {fmt(q)}")
        print(f"   door crossings {[(X, str(y)) for X, y in dr]}")
        print(f"   d103 unfolded trace v={fmt(v)} -> {fmt(end103) if end103 else None}; vertical-wall reflections {hreversals}; OK={ok}")
    return ok


def isprime(n):
    return n > 1 and all(n % p for p in range(2, int(n ** .5) + 1))


if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    print("== DBas (l=4), velocity (7,-2) ==")
    check(4, F(2, 7), verbose=True)
    for l in (53, 57):
        b, ms = construct(l)
        print(f"== family l={l}: b={b}, admissible m from criterion: {[str(m) for m in ms]}")
        check(l, ms[0], verbose=True)
    print("== scan prime n=44+l, 47<=n<=%d ==" % NMAX)
    for n in range(45, NMAX + 1):
        if not isprime(n): continue
        l = n - 44
        b, ms = construct(l)
        oks = [check(l, m) for m in ms]
        print(f"n={n} l={l} b={b} criterion slopes={len(ms)} traced OK={sum(oks)}"
              + ("" if ms else "  (no one-reversal slope of this form)"))
        assert all(oks)
        if n > 89: assert ms, n
