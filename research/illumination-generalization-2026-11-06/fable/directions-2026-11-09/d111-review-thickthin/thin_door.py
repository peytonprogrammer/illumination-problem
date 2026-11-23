"""Build the note's thin-door witness (progression matching + corridor phase root)
and verify it with the independent exact tracer in Q(sqrt2).

Room: chamber 1 [0,D1]x[0,H1], door y in [c,c+w] on x=D1, corridor [D1,D1+L]x[c,c+w],
chamber 2 [D1+L,D1+L+D2]x[e,e+H2].  12 walls, strictly simple when e<c, c+w<min(H1,e+H2).
"""
import math, sys, time
from fractions import Fraction as F
from qr2 import Q2, R2
from tracer import trace


def room(D1, H1, D2, H2, L, c, e, w):
    X1, X2 = D1 + L, D1 + L + D2
    return [(Q2(0), Q2(0)), (D1, Q2(0)), (D1, c), (X1, c), (X1, e), (X2, e), (X2, e + H2),
            (X1, e + H2), (X1, c + w), (D1, c + w), (D1, H1), (Q2(0), H1)]


def witness(D1, H1, D2, H2, L, c, e, w, S, T, cap1, cap2, Kmax=200000):
    f = float
    sx, sy = S; tx, ty = T
    x = D1 - sx; z = tx - (D1 + L)
    a = 2 * D1 - x if cap1 else x
    b = 2 * D2 - z if cap2 else z
    A, B, Lf, wf = f(a), f(b), f(L), f(w)
    lo_d, hi_d = 2 * wf / (Lf + A + B), wf / max(A, B)
    assert lo_d < hi_d, "length condition L>|a-b| fails"
    delta = (lo_d + hi_d) / 2
    P, Q = 2 * f(H1) / A, 2 * f(H2) / B
    for k in range(Kmax):
        l1 = (f(c) - f(sy) + 2 * f(H1) * k) / A
        if l1 <= 0:
            continue
        h1 = l1 + wf / A
        # target windows ((ty-c-w+2H2 m)/b, (ty-c+2H2 m)/b): pick m nearest to align
        m0 = math.floor((l1 * B - (f(ty) - f(c) - wf)) / (2 * f(H2)))
        for m in (m0 - 1, m0, m0 + 1, m0 + 2):
            l2 = (f(ty) - f(c) - wf + 2 * f(H2) * m) / B
            h2 = l2 + wf / B
            lo, hi = max(l1, l2), min(h1, h2)
            if hi - lo > delta * 1.0001:
                # corridor mismatch f(s) = s(a+L+b) + sy - ty - 2H1 k - 2H2 m ; root in 2wZ
                C0 = sy - ty - 2 * H1 * k - 2 * H2 * m
                Df = a + L + b
                fl = f(C0) + lo * f(Df)
                j = math.floor(fl / (2 * wf)) + 1
                s = (2 * w * j - C0) / Df
                if lo < f(s) < lo + delta:
                    hx = -1 if cap1 else 1
                    return s, hx, k, m, j
    return None


def run(name, D1, H1, D2, H2, L, c, e, ws, pairs):
    sys.stdout.flush(); print(f"== {name}: D1={float(D1):.6f} H1={float(H1):.6f} D2={float(D2):.6f} "
          f"H2={float(H2):.6f} L={float(L):.6f}")
    for w in ws:
        P = room(D1, H1, D2, H2, L, c, e, w)
        Bspan = float(D1 + L + D2)
        for S, T in pairs:
            dlt = abs(float(S[1]) - float(T[1]))
            for cap1 in ((0, 1) if w.a >= F(1, 20) else (0,)):
                for cap2 in ((0, 1) if w.a >= F(1, 20) else (0,)):
                    t0 = time.time()
                    r = witness(D1, H1, D2, H2, L, c, e, w, S, T, cap1, cap2)
                    if r is None:
                        print(f"  w={w.a} S={S} T={T} caps={cap1}{cap2}: no witness found"); continue
                    s, hx, k, m, j = r
                    lit, nh, nv, why = trace(P, S, T, s, hx, 1)
                    # mutation control: shift slope by w/10^6
                    lit2, *_ = trace(P, S, T, s + w * F(1, 10**6), hx, 1, maxhits=2 * (nh + nv) + 10)
                    bound = dlt * float(L) / (Bspan * float(w))
                    ok = lit and not lit2 and (nh + 1) * (nv + 1) >= bound
                    print(f"  w={w.a} S=({float(S[0]):.4f},{float(S[1]):.4f}) T=({float(T[0]):.4f},{float(T[1]):.4f})"
                          f" caps={cap1}{cap2} k={k} m={m} j={j} s~{float(s):.4f} -> {why}"
                          f" nh={nh} nv={nv} (nh+1)(nv+1)={(nh+1)*(nv+1)} bound={bound:.1f}"
                          f" mutant_lit={lit2} {'OK' if ok else 'FAIL'} [{time.time()-t0:.1f}s]")
                    sys.stdout.flush()


if __name__ == "__main__":
    q = lambda v: Q2(F(v))
    ws = [Q2(F(1, 20)), Q2(F(1, 60))]
    # A: irrational aspect quotient (1 vs sqrt2), rational marks.
    run("A", q(1), q(1), q(1), R2, q(2), q(F(3, 10)), q(0), ws,
        [((q(F(1, 3)), q(F(1, 5))), (q(F(37, 10)), q(F(6, 5)))),
         ((q(F(9, 10)), q(F(9, 10))), (q(F(31, 10)), q(F(1, 10))))])
    run("A-thin", q(1), q(1), q(1), R2, q(2), q(F(3, 10)), q(0), [Q2(F(1, 150))],
        [((q(F(1, 3)), q(F(1, 5))), (q(F(37, 10)), q(F(6, 5))))])
    # B: commensurable aspects (both squares, sides 1 and 2), x/D1 irrational.
    run("B", q(1), q(1), q(2), q(2), q(4), q(F(1, 2)), q(F(-1, 2)), ws,
        [((1 - R2 / 2, q(F(1, 4))), (q(F(13, 2)), q(F(1))))])
    # C: D1=sqrt2, H1=1, D2=1, H2=1+sqrt2, L=2sqrt2; quotient 1/(2+sqrt2) irrational.
    run("C", R2, q(1), q(1), 1 + R2, 2 * R2, q(F(2, 5)), q(F(-1, 2)), ws,
        [((q(F(1, 2)), q(F(3, 4))), (3 * R2 + F(1, 2), q(F(3, 2))))])
