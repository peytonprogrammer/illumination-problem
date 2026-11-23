"""Window families in the canonical Lemma H frame, exact.

geo = (a, b, p, q, d, S, T): channel [a, b], door (p, q) on y = d, viewer S
(s2 < d), corridor point T (t2 > d). A family is (hh, DD, sy):
  hh = height of the T-image above d (h for H, 2 ell - h for E),
  DD = depth of the S-image below d (D, or D + 2 (s2 - c) for a back wall at y = c),
  sy = initial vertical direction at S (+1 toward the door, -1 toward the back wall).
Candidates: s' = a + e1 (s1 - a) + 2 L k, X = p + e2 tau + 2 w m, crossing
xi = (hh s' + DD X)/(DD + hh) in (p, q). The tracer decides validity."""
from fractions import Fraction as Fr
from math import floor
from exact import frgcd, ext_gcd, trace


def candidates(geo, hh, DD, e1, e2, nwin=6, nker=4):
    a, b, p, q, d, S, T = geo
    L, w, tau = b - a, q - p, T[0] - p
    A, B = 2 * L * hh, 2 * w * DD
    g = frgcd(A, B)
    c = hh * (a + e1 * (S[0] - a)) + DD * (p + e2 * tau)
    lo, hi = p * (DD + hh), q * (DD + hh)
    den = A.denominator * B.denominator
    Ai, Bi, gi = int(A * den), int(B * den), int(g * den)
    _, x0, y0 = ext_gcd(Ai, Bi)
    kx, ky = Bi // gi, -(Ai // gi)
    N = floor((lo - c) / g) + 1
    out = []
    while c + g * N < hi and len(out) < nwin * (2 * nker + 1):
        Nn = int(round((c + g * N - c) / g))
        k0, m0 = x0 * Nn, y0 * Nn
        t0 = -round(Fr(k0, kx)) if kx else 0
        for t in sorted(range(-nker, nker + 1), key=abs):
            out.append((c + g * N, k0 + (t0 + t) * kx, m0 + (t0 + t) * ky))
        N += 1
    return out


def vector(geo, hh, DD, sy, e1, e2, k, m):
    a, b, p, q, d, S, T = geo
    L, w, tau = b - a, q - p, T[0] - p
    sp = a + e1 * (S[0] - a) + 2 * L * k
    X = p + e2 * tau + 2 * w * m
    return (e1 * (X - sp), sy * (DD + hh))


def window_exists(geo, hh, DD):
    """Exact: does some sign pair have a window value? (complete enumeration)"""
    return any(candidates(geo, hh, DD, e1, e2, nwin=1, nker=0) for e1 in (1, -1) for e2 in (1, -1))


def small_candidates(geo, hh, DD, K=8, M=4):
    """All window candidates with |k| <= K, up to M per (e1, e2, k), shortest first."""
    a, b, p, q, d, S, T = geo
    L, w, tau = b - a, q - p, T[0] - p
    out = []
    for e1 in (1, -1):
        for e2 in (1, -1):
            for k in range(-K, K + 1):
                sp = a + e1 * (S[0] - a) + 2 * L * k
                # p (DD+hh) < hh sp + DD X < q (DD+hh)
                Xlo = (p * (DD + hh) - hh * sp) / DD
                Xhi = (q * (DD + hh) - hh * sp) / DD
                X0 = p + e2 * tau
                m = floor((Xlo - X0) / (2 * w)) + 1
                c = 0
                while X0 + 2 * w * m < Xhi and c < M:
                    out.append((abs(X0 + 2 * w * m - sp), e1, e2, k, m)); m += 1; c += 1
    out.sort()
    return [(e1, e2, k, m) for _, e1, e2, k, m in out]


def light(room, geo, fam, maxtries=60):
    """Shortest traced-valid candidate of family fam = (hh, DD, sy) among small ones.
    Returns (status, reflections, vector, tried)."""
    hh, DD, sy = fam
    a, b, p, q, d, S, T = geo
    tried = 0
    for e1, e2, k, m in small_candidates(geo, hh, DD):
        vec = vector(geo, hh, DD, sy, e1, e2, k, m)
        ok, nref, why = trace(room, S, vec, T)
        tried += 1
        if ok: return ('valid', nref, vec, tried)
        if tried >= maxtries: break
    return ('none-window' if tried == 0 else 'all-invalid', None, None, tried)


def h_fail_formula(geo, h):
    """Phase criterion for Lemma H failure (memo, Lemma P / Corollary R).
    Returns True iff the criterion predicts no window candidate."""
    a, b, p, q, d, S, T = geo
    L, w, tau, D = b - a, q - p, T[0] - p, d - S[1]
    n = L * h / (w * D)
    if n.denominator != 1 or D <= h: return False
    kap, beta, u, pi = h / D, tau / w, S[0] - a, p - a
    for e1 in (1, -1):
        for e2 in (1, -1):
            val = (n / L * (e1 * u - pi) + e2 * beta) % 2
            if not (val == 0 or val >= 1 + kap): return False
    return True
