"""D110 claim 1: implement the note's period-one tail construction literally and trace it exactly.
Usage: python3 -B tail.py            (DBas, DB55, DBw2 at L = K and K+1, sample real marks)"""
import sys, random
from fractions import Fraction as F
from math import ceil, floor
from geom import room, shoot, ROOMS


def constants(R):
    d1, h1, d2, h2, w = R['d1'], R['h1'], R['d2'], R['h2'], R['w']
    d, h = max(d1, d2), max(h1, h2)
    eta = F(w, 8 * d)
    X = (2 * h + w) / eta + 2 * d
    N = (ceil(X / d1) + ceil(X / d2) + 4) * (ceil(2 * eta * X) + 2)
    K = ceil(4 * w * (N + 1) / eta)
    return eta, X, N, K


def leg(x0, y0, dd, hh, prel, w, X, s):
    """Sealed rectangle of depth dd, height hh; start at distance x0 from portal wall, height y0
    above the chamber floor, moving toward the portal wall and upward with slope s.
    Return (a, k, copy, branch, phase) at the first door hit, phase = signed height in (-w,w)."""
    k = 0
    while True:
        x = x0 + k * dd
        assert x <= X, "door not reached within X"
        u = y0 + s * x
        assert u.denominator != 1 or False, "integral visit (excluded slope)"
        if k % 2 == 0:
            m, r = divmod(u, 2 * hh)
            if r < hh and prel < r < prel + w:
                return x, k, m, '+', r - prel
            if r > hh and prel < 2 * hh - r < prel + w:
                return x, k, m, '-', -(2 * hh - r - prel)
        k += 1


def excluded(x0, y0, dd, X, eta):
    out = set()
    k = 0
    while x0 + k * dd <= X:
        x = x0 + k * dd
        if x > 0:
            for n in range(floor(y0 + eta * x), ceil(y0 + 2 * eta * x) + 1):
                s = (n - y0) / x
                if eta <= s <= 2 * eta:
                    out.add(s)
        k += 1
    return out


def run(name, L, S, T, consts, do_trace=True):
    R = room(name, L)
    eta, X, N, K = consts
    w, p = R['w'], R['p']
    # left leg: from S rightward-up; right leg: from T backward, leftward-up
    l1 = (R['d1'] - S[0], S[1] - R['b1'], R['d1'], R['h1'], p - R['b1'])
    l2 = (T[0] - (R['d1'] + L), T[1] - R['b2'], R['d2'], R['h2'], p - R['b2'])
    ex = excluded(*l1[:2], l1[2], X, eta) | excluded(*l2[:2], l2[2], X, eta)
    assert len(ex) <= N, (len(ex), N)
    pts = sorted(ex | {eta, 2 * eta})
    gaps = [(b - a, a, b) for a, b in zip(pts, pts[1:])]
    g, a, b = max(gaps)
    assert g >= eta / (N + 1)
    delta = eta / (2 * (N + 1))      # the note's interval length, not the larger gap
    mid = (a + b) / 2
    s0, s1 = mid - delta / 2, mid + delta / 2
    A0 = leg(*l1[:3], l1[3], l1[4], w, X, s0); A1 = leg(*l1[:3], l1[3], l1[4], w, X, s1)
    B0 = leg(*l2[:3], l2[3], l2[4], w, X, s0); B1 = leg(*l2[:3], l2[3], l2[4], w, X, s1)
    assert A0[:4] == A1[:4] and B0[:4] == B1[:4], "itinerary changed on the interval"
    a_, b_ = A0[0], B0[0]
    Fs = lambda s, A, B: L * s + A[4] + B[4]          # backward phase of right leg = -eps2*y2
    F0, F1 = Fs(s0, A0, B0), Fs(s1, A1, B1)
    slope = (F1 - F0) / (s1 - s0)
    assert slope == L + a_ + b_, (slope, L + a_ + b_)
    assert F1 - F0 >= 2 * w
    kk = ceil(F0 / (2 * w))
    assert 2 * w * kk <= F1
    sstar = s0 + (2 * w * kk - F0) / slope
    As, Bs = leg(*l1[:3], l1[3], l1[4], w, X, sstar), leg(*l2[:3], l2[3], l2[4], w, X, sstar)
    assert Fs(sstar, As, Bs) == 2 * w * kk
    res = f"{name} L={L} S={tuple(map(str,S))} T={tuple(map(str,T))} excl={len(ex)} gap={float(g):.3e} " \
          f"delta={float(delta):.3e} a={a_} b={b_} range={float(F1-F0):.4f} k={kk} s*={sstar}"
    if do_trace:
        hits = shoot(R['V'], S, (sstar.denominator, sstar.numerator), T)
        cross = [q for kd, q in hits]
        res += f" | traced OK, {len(hits)} wall hits"
    return res


def interior_samples(R, L, rng, n):
    """Rational interior marks: lattice, near-corner, and random."""
    out = []
    for side in (1, 2):
        if side == 1:
            x0, x1, y0, y1 = 0, R['d1'], R['b1'], R['b1'] + R['h1']
        else:
            x0, x1, y0, y1 = R['d1'] + L, R['d1'] + L + R['d2'], R['b2'], R['b2'] + R['h2']
        pts = [(F(x0 + 1), F(y0 + 1)), (F(x1) - F(1, 1009), F(R['p']) - F(1, 997)),
               (F(x1 if side == 1 else x0) + (F(-1, 1013) if side == 1 else F(1, 1013)), F(R['p']) + F(1, 2))]
        while len(pts) < n:
            pts.append((F(x0) + F(rng.randrange(1, 1000 * (x1 - x0)), 1000), F(y0) + F(rng.randrange(1, 1000 * (y1 - y0)), 1000)))
        out.append(pts)
    return out


if __name__ == "__main__":
    rng = random.Random(110)
    for name in ROOMS:
        R0 = room(name, 1)
        c = constants(R0)
        eta, X, N, K = c
        print(f"== {name}: chambers {R0['d1']}x{R0['h1']}, {R0['d2']}x{R0['h2']}, w={R0['w']}: "
              f"eta={eta} X={X} N={N} K={K}")
        for L in (K, K + 1):
            R = room(name, L)
            left, right = interior_samples(R, L, rng, 4)
            pairs = [(left[i], right[j]) for i in range(4) for j in range(4)]
            for i, (S, T) in enumerate(pairs):
                print("  ", run(name, L, S, T, c, do_trace=True))
            sys.stdout.flush()
