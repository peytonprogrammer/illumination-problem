"""Exact check of sections A and B of the two-list closure note (d235 review).

For each named point: build K by the note's recipe, then
 (1) check the column model with my own fold arithmetic (strict gates, no turn
     in columns 1 and 3, endpoint folds to y4), and compare with the note's
     closed forms s, (2c+s)/3, (2c+4s)/3;
 (2) trace the chord in the real lattice room with d234's exact cell tracer.
Usage: python3 review_check.py
"""
import sys, time
from fractions import Fraction as F
from math import gcd, floor, ceil

sys.path.insert(0, "../d234-route-exploration")
from trace_check import trace  # noqa: E402


def nearest(first, step, aim):
    """Nearest member of first + step*i (i >= 0) to aim; returns i."""
    r = (aim - first) / step
    cands = {max(0, floor(r)), max(0, ceil(r))}
    return min(cands, key=lambda i: (abs(first + step * i - aim), i))


def recipe_A(m):
    N = 64 * m * m
    X = 3 * N // 2 + 1
    assert X == 96 * m * m + 1
    jstep = 2 * (m + 2)
    i = nearest(F(m, X), F(3 * m * jstep, X), F(m, 2) + 1)
    j = jstep * i
    K = 3 * m * j + m
    lv = (-(m + 2), 0, 1, 1 + m, 2 + m, 3 + 2 * m)
    return N, X, lv, j, K, m  # c = m


def recipe_B(m, N, a, t, H):
    X = 3 * N // 2 + 1
    g = gcd(m, 2 * H)
    cond = F(3 * m * H, g) < F(X, 2)
    c = m + 1 - t
    jstep = 2 * H // g
    i = nearest(F(c, X), F(3 * m * jstep, X), F(2 * m + 1, 2))
    j = jstep * i
    K = 3 * m * j + c
    lv = (-a, 0, 1, m + 1, m + 1 + t, m + 1 + H)
    return N, X, lv, j, K, c, cond


def columns(N, lv, s):
    """My own fold of an upward ray from (N-1, y1) through the four columns."""
    y0, y1, y2, y3, y4, y5 = lv
    cols = [(1, y0, y3), (N, y2, y3), (1, y2, y5), (N // 2 - 1, y3, y5)]
    gates = [(y2, y3), (y2, y3), (y3, y5)]
    y, up, out, turns = F(y1), True, [], []
    for k, (w, lo, hi) in enumerate(cols):
        h = hi - lo
        u = (y - lo) if up else (2 * h - (y - lo))  # developed position
        u += s * w
        q, r = divmod(u, 2 * h)
        if r == 0 or r == h:
            return out, turns, "corner/endpoint", None
        turns.append(int(u // h) - int(((y - lo) if up else 2 * h - (y - lo)) // h))
        y, up = (lo + r, True) if r < h else (lo + 2 * h - r, False)
        out.append((y, up))
        if k < 3 and not (gates[k][0] < y < gates[k][1] and up):
            return out, turns, f"gate {k+1} fails at {y} up={up}", None
    return out, turns, "ok", y


def check(label, N, X, lv, j, K, c, extra=""):
    s = F(K, X)
    out, turns, status, yend = columns(N, lv, s)
    closed = (s, (2 * c + s) / 3, (2 * c + 4 * s) / 3)
    match = status == "ok" and all(out[k][0] == closed[k] for k in range(3))
    t0 = time.process_time()
    steps = 4 * (X + K) + 100
    res = trace(N, lv, (N - 1, lv[1]), (5 * N // 2, lv[4]), F(X), F(K), maxsteps=steps)
    dt = time.process_time() - t0
    print(f"{label}: N={N} X={X} levels={lv} j={j} K={K} s~{float(s):.5f} {extra}")
    print(f"   columns: {status}; crossings~{[round(float(o[0]),4) for o in out[:3]]}"
          f" turns per column={turns}; end={yend} (y4={lv[4]}); closed forms match={match}")
    print(f"   room trace: {res}  [{dt:.2f} CPU-s]")
    return res[0] == "HIT"


if __name__ == "__main__":
    print("== Section A ==")
    for m in list(range(2, 11)) + [16, 20]:
        N, X, lv, j, K, c = recipe_A(m)
        s = F(K, X)
        err = abs(s - (F(m, 2) + 1))
        check(f"A m={m}", N, X, lv, j, K, c,
              extra=f"|s-(m/2+1)|={float(err):.5f} j%2(m+2)={j % (2*(m+2))}")
    print("== Section A negative control (K+1, m=2) ==")
    N, X, lv, j, K, c = recipe_A(2)
    check("A m=2 K+1", N, X, lv, j, K + 1, c)
    print("== Section B ==")
    pts = [  # (name, m, N, a, t, H)
        ("B1 roof-1, m=3", 3, 576, 5, 4, 5),
        ("B2 t=1, m=3, min N", 3, 60, 1, 1, 5),
        ("B3 c=0, m=4, min N", 4, 24, 2, 5, 6),
        ("B4 t=1, m=9, g=3, min N", 9, 144, 1, 1, 12),
        ("B5 m=5 H=m+2 t=3 min N", 5, 140, 3, 3, 7),
        ("B6 m=6 H=20 t=3 min N", 6, 240, 10, 3, 20),
        ("B7 roof-1, m=7", 7, 3136, 9, 8, 9),
        ("B8 outside: m=2 roof-1", 2, 256, 4, 3, 4),
    ]
    for name, m, N, a, t, H in pts:
        N, X, lv, j, K, c, cond = recipe_B(m, N, a, t, H)
        Nm = N - 2
        Xm = 3 * Nm // 2 + 1
        cond_prev = F(3 * m * H, gcd(m, 2 * H)) < F(Xm, 2)
        check(name, N, X, lv, j, K, c,
              extra=f"c={c} cond={cond} cond(N-2)={cond_prev}")
