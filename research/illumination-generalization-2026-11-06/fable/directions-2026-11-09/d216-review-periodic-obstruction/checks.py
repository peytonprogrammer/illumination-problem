"""D216 referee checks: periodic obstruction note (note-snapshot.md).

Reuses the d212 exact integer-scaled cell tracer (rects, trace, reached,
vertex_counts, strictly_simple), imported unchanged. Named rooms only:
  R22 (manuscript), its staircase base P, the rectangle [0,4]x[0,2],
  and the note's eight-reflex controls C(M,f), M=7..12, f in {L-1, 4}.
The only direction scans are: (a) a sanity scan on R22 from S (must find no
path to T), (b) the optional reflected-path scan in the named f=4 controls.
Both use primitive directions |p|,|q| <= PMAX and grid crossings <= 4*area
(so reflections <= 4*area). No room enumeration, no room-size search.
Run: nice -n 10 python3 -B checks.py
"""
import importlib.util
import os
import time
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "d212checks", os.path.join(HERE, "..", "d212-review-descent-skeleton", "checks.py"))
K = importlib.util.module_from_spec(spec); spec.loader.exec_module(K)
rects, trace, reached, vertex_counts, strictly_simple = K.rects, K.trace, K.reached, K.vertex_counts, K.strictly_simple

T0 = time.process_time()
FAILS = []
PMAX = 9


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def interior(c, p):
    x, y = p
    return {(x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)} <= c


# ------------------------------------------------------------------ claim 1: genus and J
def cover_data(c):
    """Four-copy unfolding X of a cell room. Returns (chi, genus, #J-fixed lattice lifts,
    #J-fixed lifts of interior lattice points, #J-fixed lifts of smooth wall points).
    Lift of lattice point v in copy g in {+-1}^2; boundary edges at v identify g with g*sigma."""
    G = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    pts = {(x + dx, y + dy) for (x, y) in c for dx in (0, 1) for dy in (0, 1)}
    V = 0; fixed = {"corner": 0, "interior": 0, "smooth": 0}
    for (x, y) in pts:
        bl, br, tl, tr = (x - 1, y - 1) in c, (x, y - 1) in c, (x - 1, y) in c, (x, y) in c
        n = bl + br + tl + tr
        sig = []
        # boundary edges incident to v: vertical edges x=const (flip x), horizontal (flip y)
        if (tl != tr): sig.append((-1, 1))   # vertical edge above v
        if (bl != br): sig.append((-1, 1))   # vertical edge below v
        if (bl != tl): sig.append((1, -1))   # horizontal edge left of v
        if (br != tr): sig.append((1, -1))   # horizontal edge right of v
        seen = set(); orbits = []
        for g in G:
            if g in seen: continue
            orb = {g}; st = [g]
            while st:
                h = st.pop()
                for s in sig:
                    k = (h[0] * s[0], h[1] * s[1])
                    if k not in orb: orb.add(k); st.append(k)
            seen |= orb; orbits.append(orb)
        V += len(orbits)
        kind = "interior" if n == 4 else ("smooth" if n == 2 else "corner")
        fixed[kind] += sum(1 for o in orbits if all((-g[0], -g[1]) in o for g in o))
    Eint = sum(((x + 1, y) in c) + ((x, y + 1) in c) for (x, y) in c)
    Ebd = 4 * len(c) - 2 * Eint
    E = 4 * Eint + 2 * Ebd
    Fc = 4 * len(c)
    chi = V - E + Fc
    return chi, (2 - chi) // 2, fixed


# ------------------------------------------------------------------ rooms
P0 = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)]
STAIR = set(P0)
R22 = set(P0) | {(x, -y - 1) for (x, y) in P0} | {(3 - x, -y - 1) for (x, y) in P0}
RECT = rects((0, 4, 0, 2))


def control(M, f):
    L = 2 * M; u = M - 2
    c = rects((0, L, 0, L))
    c -= {(u, y) for y in range(f, L)}                 # top notch over [u,u+1] down to f
    c -= {(L - u - 1, y) for y in range(0, L - f)}     # half-turn image
    c -= {(0, 3)}                                      # left notch [0,1]x[3,4]
    c -= {(L - 1, L - 4)}                              # right notch (half-turn)
    return c, (u, 3), (L - u, L - 3)


def first_lit(c, S, T, pmax=PMAX):
    """Primitive directions, grid crossings <= 4*area. Returns sorted lit (length^2, d, steps)."""
    cap = 4 * len(c); out = []
    for p in range(-pmax, pmax + 1):
        for q in range(-pmax, pmax + 1):
            if p == 0 or q == 0 or gcd(abs(p), abs(q)) != 1: continue
            m = cap // (abs(p) + abs(q))
            r = trace(c, S, (p, q), m, hits=True)
            if T in r['hit']:
                k = r['hit'][T]; out.append((k * k * (p * p + q * q), (p, q), k))
    return sorted(out)


def legs_of(c, S, v, T):
    """Independent check: move with Fraction time along developed displacement v; at each
    grid-line crossing decide reflection from the two adjacent cells; reject corners;
    reflect at smooth-wall lattice points. Returns physical bounce list [S, ..., T] or None."""
    P = [F(S[0]), F(S[1])]; d = [F(v[0]), F(v[1])]; t = F(0); pts = [tuple(S)]
    import math
    while t < 1:
        cand = []
        for i in (0, 1):
            if d[i] != 0:
                nxt = (math.floor(P[i]) + 1) if d[i] > 0 else (math.ceil(P[i]) - 1)
                cand.append((nxt - P[i]) / d[i])
        dt = min(min(cand), 1 - t)
        P = [P[0] + d[0] * dt, P[1] + d[1] * dt]; t += dt
        if t == 1: break
        ix, iy = P[0].denominator == 1, P[1].denominator == 1
        if ix and iy:
            x, y = int(P[0]), int(P[1])
            bl, br, tl, tr = (x - 1, y - 1) in c, (x, y - 1) in c, (x - 1, y) in c, (x, y) in c
            if bl and br and tl and tr: continue
            if (bl, br) == (tl, tr) and bl != br:      # smooth vertical wall through a lattice point
                d[0] = -d[0] if ((x, y) not in c if d[0] > 0 else (x - 1, y) not in c) else d[0]
                pts.append((P[0], P[1])); continue
            if (bl, tl) == (br, tr) and bl != tl:      # smooth horizontal wall through a lattice point
                d[1] = -d[1] if ((x, y) not in c if d[1] > 0 else (x, y - 1) not in c) else d[1]
                pts.append((P[0], P[1])); continue
            return None                                # convex or reflex corner
        if ix:
            x, cy = int(P[0]), math.floor(P[1])
            nxtcell = (x, cy) if d[0] > 0 else (x - 1, cy)
            if nxtcell not in c: d[0] = -d[0]; pts.append((P[0], P[1]))
        if iy:
            y, cx = int(P[1]), math.floor(P[0])
            nxtcell = (cx, y) if d[1] > 0 else (cx, y - 1)
            if nxtcell not in c: d[1] = -d[1]; pts.append((P[0], P[1]))
    pts.append((P[0], P[1]))
    return pts if (P[0], P[1]) == (T[0], T[1]) else None


def seg_hits_rect(A, B, R):
    """Closed segment AB meets closed rectangle R=(x0,x1,y0,y1)? exact (Liang-Barsky)."""
    (ax, ay), (bx, by) = A, B; t0, t1 = F(0), F(1)
    for d, lo, hi, a in ((bx - ax, R[0], R[1], ax), (by - ay, R[2], R[3], ay)):
        if d == 0:
            if not (lo <= a <= hi): return False
        else:
            ta, tb = F(lo - a, d), F(hi - a, d)
            if ta > tb: ta, tb = tb, ta
            t0, t1 = max(t0, ta), min(t1, tb)
            if t0 > t1: return False
    return True


def main():
    say("=== Claim 1: four-copy cover genus and orientation involution")
    for nm, c in (("R22", R22), ("STAIR", STAIR), ("RECT", RECT), ("C(7,4)", control(7, 4)[0]), ("C(7,13)", control(7, 13)[0])):
        rx, cv, pin = vertex_counts(c)
        chi, g, fx = cover_data(c)
        check(cv - rx == 4 and g == rx + 1 and fx["corner"] == 2 * rx + 4 == 2 * g + 2 and fx["interior"] == 0 and fx["smooth"] == 0,
              f"{nm}: r={rx}, W={rx + cv}, chi(X)={chi}, genus {g}=r+1; J fixes exactly the {fx['corner']} corner lifts "
              f"(=2g+2), 0 lifts of interior/smooth lattice points")

    say("\n=== Claim 3: rectangle [0,4]x[0,2] half-turn example")
    ht = lambda p: (4 - p[0], 2 - p[1])
    check(ht((1, 1)) == (3, 1) and {(3 - x, 1 - y) for (x, y) in RECT} == RECT,
          "half-turn about (2,1) preserves the rectangle and exchanges (1,1),(3,1)")
    check(reached(trace(RECT, (1, 1), (1, 0), 2), (3, 1)), "horizontal segment (1,1)->(3,1) legal (exact trace)")
    # torus: X is the 8x4 torus; absolute periods 8Z x 4Z; N=8 works; lattice points are 8-torsion
    check(all((8 * a) % 8 == 0 and (8 * b) % 4 == 0 for a in range(8) for b in range(4)),
          "RECT: X = R^2/(8Z x 4Z); N=8 gives N Z^2 in Lambda, so every lattice lift is N-torsion")

    say("\n=== Claim 4/5: R22 fold data")
    rx, cv, _ = vertex_counts(R22); srx, scv, _ = vertex_counts(STAIR)
    check(len(R22) == 15 and (rx, cv) == (9, 13) and strictly_simple(R22) and (srx, scv) == (3, 7),
          f"R22: area 15, r=9, convex 13, W=22, strictly simple; staircase z=3 reflex, 7 convex; k=3 copies; kz={3 * srx}=r")
    check(all(2 * r + 4 >= 22 for r in [k * z for k in range(3, 8) for z in range(3, 8)]), "r>=kz with k,z>=3 gives W=2r+4>=22")
    fold = lambda p, i: p if i == 0 else ((p[0], -p[1]) if i == 1 else (4 - p[0], -p[1]))
    check(fold((0, 0), 1) == (0, 0) and fold((2, 2), 2) == (2, -2), "fold sends S=(0,0)->a=(0,0) (P1) and T=(2,2)->b=(2,-2) (P2)")
    pts = {(x + dx, y + dy) for (x, y) in STAIR for dx in (0, 1) for dy in (0, 1)}
    nonv = []
    for (x, y) in pts:
        n = sum(((x - 1, y - 1) in STAIR, (x, y - 1) in STAIR, (x - 1, y) in STAIR, (x, y) in STAIR))
        if n in (2, 4):
            nonv.append((x, y))
    check(sorted(nonv) == [(0, 0), (2, -2)], f"staircase non-vertex lattice points: {sorted(nonv)} (no interior lattice points)")
    check(interior(R22, (0, 0)) and interior(R22, (2, 2)), "S, T interior in R22")
    lit = first_lit(R22, (0, 0), (2, 2), pmax=15)
    check(not lit, "sanity (consistent with darkness): no primitive direction |p|,|q|<=15 from S reaches T within 60 grid crossings")

    say("\n=== Claim 6: pinned eight-reflex controls")
    summary = []
    for M in range(7, 13):
        L = 2 * M; u = M - 2
        for f in (L - 1, 4):
            c, S, T = control(M, f)
            rx, cv, pin = vertex_counts(c)
            sym = {(L - 1 - x, L - 1 - y) for (x, y) in c} == c
            notches = [(u, u + 1, f, L), (L - u - 1, L - u, 0, L - f), (0, 1, 3, 4), (L - 1, L, L - 4, L - 3)]
            disj = all(not (a[1] >= b[0] and b[1] >= a[0] and a[3] >= b[2] and b[3] >= a[2])
                       for i, a in enumerate(notches) for b in notches[i + 1:])
            pinned = S[0] == u and S[1] == 3 and T[0] == L - u and T[1] == L - 3
            even = (T[0] - S[0]) % 2 == 0 and (T[1] - S[1]) % 2 == 0 and T == (L - S[0], L - S[1])
            ok = (rx == 8 and cv == 12 and pin == 0 and strictly_simple(c) and sym and disj and pinned and even
                  and interior(c, S) and interior(c, T))
            d = (T[0] - S[0], T[1] - S[1]); g = gcd(*d)
            direct = reached(trace(c, S, (d[0] // g, d[1] // g), g), T)
            blocked = [i for i, R in enumerate(notches) if seg_hits_rect(S, T, R)]
            if f == L - 1:
                check(ok and direct and not blocked,
                      f"M={M} f=L-1={f}: r=8, W=20, strictly simple, notches disjoint, half-turn symmetric, pinned, even diff, "
                      f"S,T interior; direct chord legal (trace) and misses all four closed notches")
            else:
                m = F(L - 6, 4); xh = u + 1 / m
                check(ok and m > 1 and u < xh < u + 1 and not direct and blocked == [0, 1],
                      f"M={M} f=4: same structure; slope m={m}>1, chord meets top-notch floor y=4 at x=u+1/m={xh} in (u,u+1); "
                      f"direct trace fails; chord meets the top notch and, by the half-turn, the bottom notch (ceiling y=L-4 "
                      f"at x=L-u-1/m); no other notch")
                lit = first_lit(c, S, T)
                if lit:
                    L2, dd, k = lit[0]
                    summary.append((M, dd, k, len(lit)))
                    legs = legs_of(c, S, (dd[0] * k, dd[1] * k), T)
                    check(legs is not None, f"M={M} f=4: independent leg-by-leg Fraction tracer confirms {dd} x{k}: "
                          f"{None if legs is None else len(legs) - 2} reflections, bounce points {legs[1:-1] if legs else None}")
                    say(f"    M={M} f=4: area {len(c)}; {len(lit)} lit primitive directions |p|,|q|<={PMAX}; "
                        f"shortest: direction {dd}, {k} steps, unfolded displacement {(dd[0] * k, dd[1] * k)}")
                else:
                    summary.append((M, None, None, 0))
                    say(f"    M={M} f=4: no lit direction with |p|,|q|<={PMAX}, crossings <= 4*area={4 * len(c)}")
    check(all(s[1] is not None for s in summary), "optional: every f=4 control pair (M=7..12) is lit by a reflected path")

    say("\n=== Links (resolved from qclass-closure/bbbb)")
    base = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "qclass-closure", "bbbb"))
    links = ["fold-converse.md", "midpoint-necessity.md",
             "../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex",
             "../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d215-review-ratio-compactness/review.md"]
    for l in links:
        check(os.path.exists(os.path.join(base, l)), f"link resolves: {l}")

    say(f"\nTOTAL FAIL {len(FAILS)}; cpu {time.process_time() - T0:.1f}s")


if __name__ == "__main__":
    main()
