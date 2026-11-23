"""D112 claims 1 and 3: the gluing equation, the gcd/translate test, and resonance.

Sealed legs come from chamber.leg (own tracer); full-room checks use
chamber.shoot_room on d110's dumbbell polygons. Python 3 -B, exact Fractions.
"""
import sys, random
from fractions import Fraction as F
from math import floor
from pathlib import Path
from chamber import leg, shoot_room, slab_period, gcd_rat, lcm_rat, Irregular, next_hit, edges
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd110-review-length'))
from geom import room


def sealed(R):
    d1, L = R['d1'], R['L']; p, w = R['p'], R['w']
    A = [(0, R['b1']), (d1, R['b1']), (d1, p), (d1, p + w), (d1, R['b1'] + R['h1']), (0, R['b1'] + R['h1'])]
    x2 = d1 + L
    B = [(x2, R['b2']), (x2 + R['d2'], R['b2']), (x2 + R['d2'], R['b2'] + R['h2']), (x2, R['b2'] + R['h2']),
         (x2, p + w), (x2, p)]
    return A, (d1, p, p + w), B, (x2, p, p + w)


def Fval(R, S, T, s, dA, dB):
    A, mA, B, mB = sealed(R)
    vx = lambda V: sorted(set(x for x, _ in V))
    la = leg(A, mA, vx(A) + [S[0]], S, s, *dA)
    lb = leg(B, mB, vx(B) + [T[0]], T, s, *dB)
    p = F(R['p'])
    phiA = la['exit'][2] * (la['exit'][0] - p)
    phiB = -lb['exit'][2] * (lb['exit'][0] - p)           # forward sign at B entry
    return R['L'] * s + phiA - phiB, la, lb


def single_traversal_hit(R, S, d, T, maxev=4000):
    """Trace in the full room; True if T is reached before a second corridor entry."""
    V = [(F(x), F(y)) for x, y in R['V']]
    E = edges(V); Vs = set(V)
    p = (F(S[0]), F(S[1])); d = (F(d[0]), F(d[1])); T = (F(T[0]), F(T[1]))
    xa, xb = F(R['d1']), F(R['d1'] + R['L'])
    entries = 0
    for _ in range(maxev):
        t, kind, q, e = next_hit(E, Vs, p, d)
        u = (T[0] - p[0], T[1] - p[1])
        if u[0] * d[1] == u[1] * d[0]:
            tt = u[0] / d[0]
            if 0 < tt < t:
                return entries <= 1  # T lies in B; the arriving segment may itself be the entry
        if q in Vs:
            return False
        if (p[0] < xa < q[0]) or (q[0] < xb < p[0]):  # entry into the corridor from either end
            entries += 1
        if entries > 1:
            return False
        d = (-d[0], d[1]) if kind == 'v' else (d[0], -d[1])
        p = q
    return False


DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def iff_test(name, L, pairs, slopes):
    R = room(name, L)
    w = F(R['w'])
    pos = neg = agree = 0
    for S, T in pairs:
        for s in slopes:
            for dA in DIRS:
                glued = []
                for dB in DIRS:
                    try:
                        Fv, la, lb = Fval(R, S, T, s, dA, dB)
                    except Irregular:
                        continue
                    glued.append((Fv / (2 * w)).denominator == 1)
                hit = single_traversal_hit(R, S, (dA[0], dA[1] * s), T)
                pos += hit; neg += not hit
                agree += hit == any(glued)
    return pos, neg, agree


def solved_slopes(name, L, S, T, n, rnd):
    """Slopes with F in 2wZ on a fixed chart (verified), for the 'if' direction."""
    R = room(name, L); w = F(R['w'])
    out = []
    tries = 0
    while len(out) < n and tries < 50 * n:
        tries += 1
        s0 = F(rnd.randrange(1, 4000), 997)
        dA, dB = rnd.choice(DIRS), rnd.choice(DIRS)
        try:
            F0, la, lb = Fval(R, S, T, s0, dA, dB)
        except Irregular:
            continue
        slope = L + la['a'] + lb['a']
        m = round(F0 / (2 * w))
        s = s0 + (2 * w * m - F0) / slope
        if s <= 0:
            continue
        try:
            F1, la1, lb1 = Fval(R, S, T, s, dA, dB)
        except Irregular:
            continue
        if la1['a'] == la['a'] and lb1['a'] == lb['a'] and la1['nh'] == la['nh'] and lb1['nh'] == lb['nh']:
            assert (F1 / (2 * w)).denominator == 1
            out.append((s, dA, dB))
    return out


def main():
    rnd = random.Random(1120)
    print("== claim 1: F in 2wZ  <=>  single-traversal hit (both directions) ==")
    for name, L in (('DBas', 4), ('DB55', 7), ('DBw2', 6)):
        R = room(name, L)
        x2 = R['d1'] + L
        pairs = [((1, 3), (x2 + 2, 3)), ((2, 1), (x2 + 1, 4)), ((F(7, 2), F(1, 1013) + 1), (x2 + F(3, 2), 2))]
        pairs = [(a, b) for a, b in pairs if R['b2'] < b[1] < R['b2'] + R['h2']]
        tot_s = 0; ok = 0
        for S, T in pairs:
            sl = solved_slopes(name, L, S, T, 15, rnd)
            for s, dA, dB in sl:
                tot_s += 1
                ok += single_traversal_hit(R, S, (dA[0], dA[1] * s), T)
        rs = [F(rnd.randrange(1, 3000), 1009) for _ in range(25)]
        pos, neg, agree = iff_test(name, L, pairs, rs)
        print(f"{name} L={L}: solved F=2wm slopes traced: {ok}/{tot_s} reach T in one traversal; "
              f"random slopes: {pos} hits, {neg} non-hits, criterion agrees in {agree}/{pos+neg}")
    # d109 witness: DBas (1,3) -> (11,3), v = (7,-2), slope 2/7
    R = room('DBas', 4)
    Fv, la, lb = Fval(R, (1, 3), (11, 3), F(2, 7), (1, -1), (1, -1))
    print("d109 witness DBas (1,3)->(11,3) v=(7,-2): F =", Fv, " (2w =", 2 * R['w'], ")")

    print("\n== claim 3: translates and the gcd ==")
    # integral data: is LK always in 2wZ for lattice marks at integer L?
    for name in ('DBas', 'DB55', 'DBw2'):
        res = set()
        for L in range(1, 41):
            R = room(name, L); A, mA, B, mB = sealed(R)
            for xs in range(1, R['d1']):
                for xt in range(1, R['d2']):
                    vx = sorted(set(x for x, _ in A) | {xs}) + sorted(set(x for x, _ in B) | {R['d1'] + L + xt})
                    K, _ = slab_period(A + B, [])  if False else (None, None)
                    KA, _ = slab_period(A, sorted(set(x for x, _ in A) | {xs}))
                    KB, _ = slab_period(B, sorted(set(x for x, _ in B) | {R['d1'] + L + xt}))
                    K = lcm_rat(KA, KB)
                    res.add(gcd_rat(L * K, F(2 * R['w'])) == 2 * R['w'])
        print(f"{name}: integer L in 1..40, lattice mark abscissas: g = 2w in every case: {res == {True}}")
    # rational corridor length where g < 2w: DB55 with L = 21/10
    L = F(21, 10)
    R = room('DB55', L)
    S, T = (F(1), F(1)), (F(5) + L + 4, F(1))
    A, mA, B, mB = sealed(R)
    KA, _ = slab_period(A, [0, 1, 5]); KB, _ = slab_period(B, [5 + L, 5 + L + 4, 10 + L])
    K = lcm_rat(KA, KB); g = gcd_rat(L * K, F(2)); q = 2 / g
    print(f"DB55 at L=21/10, S={S}, T={T}: K={K}, LK={L*K}, g={g}, q={q}")
    found = 0
    for s0 in [F(k, 113) for k in range(5, 300, 7)]:
        for dA in DIRS:
            for dB in DIRS:
                try:
                    F0, la, lb = Fval(R, S, T, s0, dA, dB)
                except Irregular:
                    continue
                slope = L + la['a'] + lb['a']
                m = floor(F0 / g) + 1
                if (m * g / 2).denominator == 1:
                    continue      # want a hit in gZ \ 2wZ (translation needed)
                s1 = s0 + (m * g - F0) / slope
                try:
                    F1, la1, lb1 = Fval(R, S, T, s1, dA, dB)
                except Irregular:
                    continue
                if (la1['a'], la1['nh'], lb1['a'], lb1['nh']) != (la['a'], la['nh'], lb['a'], lb['nh']):
                    continue
                k = next(k for k in range(int(q)) if ((F1 + k * L * K) / 2).denominator == 1)
                s2 = s1 + k * K
                F2, _, _ = Fval(R, S, T, s2, dA, dB)
                direct = single_traversal_hit(R, S, (dA[0], dA[1] * s1), T)
                trans = single_traversal_hit(R, S, (dA[0], dA[1] * s2), T)
                congr = ((F2 - F1 - k * L * K) / 2).denominator == 1
                found += 1
                if found <= 6:
                    print(f"  s1={s1} F(s1)={F1} (in gZ, not 2Z; s1 glues: {direct}); k={k}, s2=s1+kK: "
                          f"F(s2)={F2}, F(s2)=F(s1)+kLK mod 2: {congr}, s2 glues and traces to T: {trans}")
                assert congr and trans and not direct
    print(f"  {found} translated witnesses, all exact")


if __name__ == '__main__':
    main()
