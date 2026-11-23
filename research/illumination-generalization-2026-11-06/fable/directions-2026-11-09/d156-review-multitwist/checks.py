"""d156 checks for multitwist-first-shot (snapshot 2026-11-22 03:55).

Named room only: the d129/d155 12-wall dumbbell at a = 10, 20, 60.
Exact integer arithmetic throughout. No room searches, no network.
Run: python3 -B checks.py > checks.log
"""
from math import gcd
import time

T0 = time.process_time()


def lcm(*xs):
    out = 1
    for x in xs:
        out = out * x // gcd(out, x)
    return out


def dumbbell(a):
    U = 2 * a
    P = [(0, 0), (U, 0), (U, 2), (U + 2, 2), (U + 2, 0), (2 * U + 3, 0), (2 * U + 3, 5),
         (U + 2, 5), (U + 2, 3), (U, 3), (U, 5), (0, 5)]
    return P, (a, 2), (3 * a + 2, 2)


# ------------------------------------------------------------ cylinders
def horizontal_cylinders(P):
    """Corner-cut horizontal cylinders of the 4-copy unfolding.

    Each open band between consecutive corner ordinates splits into rectangles.
    A leaf in a rectangle of length L is a round trip, so each rectangle gives two
    cylinders (one per vertical-sign class of copies) of circumference 2L.
    Returns list of (circumference, height, x0, x1, y0, y1).
    """
    n = len(P)
    ys = sorted({v[1] for v in P})
    vwalls = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    out = []
    for y0, y1 in zip(ys, ys[1:]):
        ym2 = y0 + y1
        xs = sorted(a[0] for a, b in vwalls if 2 * min(a[1], b[1]) < ym2 < 2 * max(a[1], b[1]))
        for x0, x1 in zip(xs[0::2], xs[1::2]):
            out.append((2 * (x1 - x0), y1 - y0, x0, x1, y0, y1))
    return out


def vertical_cylinders(P):
    Q = [(y, x) for x, y in P]
    return [(C, h, y0, y1, x0, x1) for C, h, x0, x1, y0, y1 in horizontal_cylinders(Q)]


# ------------------------------------------------------------ exact tracer
def trace_scaled(V, start, s, target=None, maxsteps=10 ** 6):
    """45-degree billiard in an integer orthogonal polygon V (already scaled).

    Stops at a vertex ('corner'), at target ('target'), or on return to start with
    the launch direction ('closed'). Returns (event, point, reflections, path length in
    scaled |dX| units).
    """
    n = len(V)
    hw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][1] == V[(i + 1) % n][1]]
    vw = [(V[i], V[(i + 1) % n]) for i in range(n) if V[i][0] == V[(i + 1) % n][0]]
    vset = set(V)
    X, Y = start
    sx, sy = s
    run = 0
    for step in range(maxsteps):
        best = None
        for (a, b) in vw:
            t = (a[0] - X) * sx
            if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + sy * t <= max(a[1], b[1]):
                best = (t, 'v')
        for (a, b) in hw:
            t = (a[1] - Y) * sy
            if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + sx * t <= max(a[0], b[0]):
                best = (t, 'h')
        t, kind = best
        for tag, Z in (('target', target), ('closed', start)):
            if Z is None or (tag == 'closed' and (sx, sy) != s):
                continue
            tz = (Z[0] - X) * sx
            if 0 < tz <= t and (Z[1] - Y) * sy == tz:
                return tag, Z, step, run + tz
        X, Y = X + sx * t, Y + sy * t
        run += t
        if (X, Y) in vset:
            return 'corner', (X, Y), step, run
        if kind == 'v':
            sx = -sx
        else:
            sy = -sy
    return 'limit', (X, Y), maxsteps, run


def shoot(P, S, d, T, maxsteps=10 ** 6):
    """Physical shot from S in primitive direction d=(p,q), p,q != 0.

    Scale X = |q| x, Y = |p| y so the direction becomes (+-1,+-1).
    Returns (event, physical point, reflections, total |dx|, total |dy|).
    """
    p, q = d
    kx, ky = abs(q), abs(p)
    V = [(kx * x, ky * y) for x, y in P]
    ev, pt, st, run = trace_scaled(V, (kx * S[0], ky * S[1]), (1 if p > 0 else -1, 1 if q > 0 else -1),
                                   (kx * T[0], ky * T[1]), maxsteps)
    from fractions import Fraction as Fr
    return ev, (Fr(pt[0], kx), Fr(pt[1], ky)), st, Fr(run, kx), Fr(run, ky)


def fmt(r):
    ev, pt, st, hx, hy = r
    return f"{ev} at ({pt[0]},{pt[1]}) after {st} reflections, |dx|={hx}, |dy|={hy}"


print("# 0. Tracer sanity (independent of the d155 tracer)")
P, S, T = dumbbell(10)
for d in [(11, 1), (1, 1), (1, 7), (-1, 3), (2, 5), (-2, -9)]:
    print(f"   a=10 d={d}: {fmt(shoot(P, S, d, T))}")
print("   expected: (11,1) reaches T with |dx|=22, |dy|=2; the others stop at (20,2) (d155 table).")

summary = []
for a in (10, 20, 60):
    P, S, T = dumbbell(a)
    U = 2 * a
    print(f"\n# a={a} (2a={U}), S={S}, T={T}, W={len(P)}")
    # ------------------------------------------------------------ 1. cylinders and c
    cyl = horizontal_cylinders(P)
    print("## 1. Horizontal corner-cut cylinders (4-copy unfolding; each band rectangle gives two)")
    for C, h, x0, x1, y0, y1 in cyl:
        print(f"   y in ({y0},{y1}), x in ({x0},{x1}): circumference {C}, height {h}, C/gcd(C,h)={C // gcd(C, h)}")
    c = lcm(*[C // gcd(C, h) for C, h, *_ in cyl])
    c_note = lcm(2 * a, 2 * a + 1, 8 * a + 6)
    print(f"   least pointwise rim-fixing shear c = {c}; note's lcm(2a,2a+1,8a+6) = {c_note}; equal: {c == c_note}")
    rims = sorted({v[1] for v in P})
    print(f"   rim ordinates {rims}; S and T on rims: {S[1] in rims and T[1] in rims}")
    # set-preserving twist: do not cut at the all-convex leaves y=0, y=5; mirror bands merge (height 4)
    c2 = lcm(*([C // gcd(C, 2 * h) for C, h, x0, x1, y0, y1 in cyl if y0 == 0 or y1 == 5]
               + [C // gcd(C, h) for C, h, x0, x1, y0, y1 in cyl if not (y0 == 0 or y1 == 5)]))
    print(f"   corner-SET-preserving variant (y=0, y=5 leaves uncut, bands merged to height 4): c' = {c2}, c/c' = {c // c2}")
    for C, h, x0, x1, y0, y1 in cyl:
        if y0 == 0 or y1 == 5:
            print(f"     merged C={C}: rim shift {c2 * 2 * h % C}, convex mid-leaf shift {c2 * h % C} "
                  f"(its corner lifts sit at 0 and {C // 2}, so the set is preserved)")

    # ------------------------------------------------------------ 1b. residues
    print("## 1b. Direction family (p,1), exact traces")
    print("   p=0: vertical ray keeps x=a (not a corner abscissa), closes after |dy|=10, T.x != a: MISS")
    rows = []
    for k in (1, -1, 2):
        r = shoot(P, S, (k * c, 1), T, maxsteps=3 * 10 ** 6)
        rows.append(('0', k, r[0]))
        print(f"   p={k}c={k * c}: {fmt(r)}  [expect closed, |dy|=10]")
    for k in (1, -1, 2, -2):
        p = a + 1 + k * c
        r = shoot(P, S, (p, 1), T, maxsteps=3 * 10 ** 6)
        rows.append(('a+1', k, r[0]))
        print(f"   p=a+1+{k}c={p}: {fmt(r)}  [expect target, |dy|=2]")
    for k in (1, -1):
        r = shoot(P, S, (a + 1 + k * c2, 1), T, maxsteps=3 * 10 ** 6)
        print(f"   p=a+1+{k}c'={a + 1 + k * c2}: {fmt(r)}")
        r = shoot(P, S, (k * c2, 1), T, maxsteps=3 * 10 ** 6)
        print(f"   p={k}c'={k * c2}: {fmt(r)}")
    if a == 10:
        hits = [p for p in range(-150, 151) if p != 0 and shoot(P, S, (p, 1), T)[0] == 'target']
        print(f"   all p in [-150,150] with (p,1) reaching T: {hits}")

    # ------------------------------------------------------------ 2. stabilizer obstruction ingredients
    print("## 2. Stabilizer obstruction ingredients")
    circ = sorted({C for C, *_ in cyl})
    print(f"   distinct circumferences {circ}; cylinders per circumference in the unfolding: "
          f"{ {C: 2 * sum(1 for D, *_ in cyl if D == C) for C in circ} }")
    for name, Z in (('S', S), ('T', T)):
        touch = [(C, (x0, x1), (y0, y1)) for C, h, x0, x1, y0, y1 in cyl if x0 <= Z[0] <= x1 and y0 <= Z[1] <= y1]
        print(f"   cylinder closures containing {name}: {touch}")
    for Cv in (4 * a, 4 * a + 2):
        xr = [(x0, x1) for C, h, x0, x1, *_ in cyl if C == Cv]
        print(f"   x-projection of circumference-{Cv} closures: [{min(x for x, _ in xr)}, {max(x for _, x in xr)}]")
    bad = []
    for qq in range(-60, 61):
        for pp in (1, -1):
            if qq == 0:
                continue
            r = shoot(P, S, (pp, qq), T)
            if not (r[0] == 'corner' and r[1] == (U, 2)):
                bad.append(((pp, qq), r[0]))
    print(f"   transposed pencil (+-1,m), 1<=|m|<=60: all stop at lower lip ({U},2): {not bad} {bad[:3]}")

    # ------------------------------------------------------------ 2b. full affine orbit probe
    print("## 2b. Probe beyond the horizontal stabilizer: holonomy multiplicities in direction (a+1,1)")
    vm = sorted({C for C, *_ in vertical_cylinders(P)})
    print(f"   vertical corner-cut cylinders have holonomy (0,m) with m in {vm}")
    p, q = a + 1, 1
    kx, ky = 2 * q, 2 * p  # doubled scaling: start at X odd, Y even, so X+-Y is odd and no vertex is ever met
    V = [(kx * x, ky * y) for x, y in P]
    ms = {}
    xs = sorted(set(list(range(0, U, max(1, U // 5))) + [U] + list(range(U + 2, 2 * U + 3, max(1, U // 5)))))
    for xx in xs:
        for yy2 in range(1, 10, 2):  # physical y = yy2/2 + 1/(2p) style offsets via Y = yy2*p + 2
            X0, Y0 = kx * xx + 1, yy2 * p + 2 - ((yy2 * p) % 2)
            xph, yph = X0 / kx, Y0 / ky
            ok = (0 < xph < U and 0 < yph < 5) or (U + 2 < xph < 2 * U + 3 and 0 < yph < 5) or \
                 (U <= xph <= U + 2 and 2 < yph < 3)
            if not ok:
                continue
            ev, pt, st, run = trace_scaled(V, (X0, Y0), (1, 1), None, 10 ** 6)
            assert ev == 'closed', ev
            from fractions import Fraction as Fr
            m = Fr(run, ky) / q
            ms[m] = ms.get(m, 0) + 1
    print(f"   sampled closed orbits in direction {(p, q)}: holonomy multiplicities m -> count {dict(sorted(ms.items()))}")
    print(f"   any m outside {vm}: {any(m not in vm for m in ms)}")
    if a == 10:
        from fractions import Fraction as Fr
        out = {}
        for pp in hits:
            kx, ky = 2, 2 * abs(pp)
            V = [(kx * x, ky * y) for x, y in P]
            mm = set()
            for X0, Y0 in ((kx * 3 + 1, 2 * abs(pp) + 2), (kx * 30 + 1, 2 * abs(pp) + 2),
                           (kx * 21 + 1, 5 * abs(pp) + 2 - (5 * abs(pp)) % 2)):
                ev, pt, st, run = trace_scaled(V, (X0, Y0), (1 if pp > 0 else -1, 1), None, 10 ** 6)
                assert ev == 'closed'
                mm.add(Fr(run, ky))
            out[pp] = sorted(mm)
        inorbit = [pp for pp, mm in out.items() if all(m in vm for m in mm)]
        print(f"   successful p in [-150,150]: sampled multiplicities all in {vm} (necessary for being an "
              f"affine image of vertical) for p = {inorbit}")
        print(f"   sample: { {pp: out[pp] for pp in hits[:6]} }")
    summary.append((a, c, all(ev == 'closed' for t, k, ev in rows if t == '0'),
                    all(ev == 'target' for t, k, ev in rows if t == 'a+1')))

print("\n# Summary (a, c, p=0 mod c all closed-miss, p=a+1 mod c all hit)")
for row in summary:
    print("  ", row)
print("\nCPU seconds:", round(time.process_time() - T0, 2))
