"""D227 independent review of l1-pinned-pairs (note-snapshot.md).

Own exact tracer for orthogonal polygons (Fractions). Pattern taken from d226 checks.py
(boundary-edge tracer, first-hit search) but generalized to any vertex list.
Every traced direction is hand-chosen and listed below; there is no sweep.
Run: nice -n 10 python3 -B checks.py
"""
import time
from fractions import Fraction as F
from math import gcd

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


# ------------------------------------------------------------------ polygon utilities
def edges(P):
    return list(zip(P, P[1:] + P[:1]))


def orthogonal(P):
    return all((a[0] == b[0]) != (a[1] == b[1]) for a, b in edges(P)) and \
        all((e[0][0] == e[1][0]) != (f[0][0] == f[1][0]) for e, f in zip(edges(P), edges(P)[1:] + edges(P)[:1]))


def seg_touch(e, f):
    """closed axis-parallel segments e, f intersect?"""
    (a, b), (c, d) = e, f
    x1, x2 = sorted((a[0], b[0])); y1, y2 = sorted((a[1], b[1]))
    x3, x4 = sorted((c[0], d[0])); y3, y4 = sorted((c[1], d[1]))
    return max(x1, x3) <= min(x2, x4) and max(y1, y3) <= min(y2, y4)


def strictly_simple(P):
    E = edges(P)
    n = len(E)
    if len(set(P)) != n:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                # adjacent: must meet only at the shared vertex (orthogonality guarantees this)
                continue
            if seg_touch(E[i], E[j]):
                return False
    return True


def area2(P):
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in edges(P))


def reflex_count(P):
    s = 1 if area2(P) > 0 else -1
    c = 0
    n = len(P)
    for i in range(n):
        a, b, d = P[i - 1], P[i], P[(i + 1) % n]
        cr = (b[0] - a[0]) * (d[1] - b[1]) - (b[1] - a[1]) * (d[0] - b[0])
        if cr * s < 0:
            c += 1
    return c


def inside(P, q):
    """strict interior test (ray casting; q assumed off boundary)."""
    x, y = q
    for a, b in edges(P):
        if seg_touch((a, b), (q, q)):
            return False
    c = False
    for (ax, ay), (bx, by) in edges(P):
        if ax == bx and min(ay, by) <= y < max(ay, by) and ax > x:
            c = not c
    return c


def square_free(P, p, r):
    """open sup-norm square of radius r about p misses every boundary edge and p is interior."""
    x, y = p
    for (a, b) in edges(P):
        x1, x2 = sorted((a[0], b[0])); y1, y2 = sorted((a[1], b[1]))
        if x1 == x2 and x - r < x1 < x + r and y1 < y + r and y2 > y - r:
            return False
        if y1 == y2 and y - r < y1 < y + r and x1 < x + r and x2 > x - r:
            return False
    return inside(P, p)


def refined_gap(P, marks):
    xs = sorted({v[0] for v in P} | {m[0] for m in marks})
    ys = sorted({v[1] for v in P} | {m[1] for m in marks})
    return xs, ys


def delta_p(xs, ys, p):
    i, j = xs.index(p[0]), ys.index(p[1])
    return min(xs[i] - xs[i - 1], xs[i + 1] - xs[i], ys[j] - ys[j - 1], ys[j + 1] - ys[j])


def quadrants(P, p, eps):
    x, y = p
    return [inside(P, (x + sx * eps, y + sy * eps)) for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]


# ------------------------------------------------------------------ tracer
def trace(P, S, d, T, maxref=400):
    """Shoot from S in direction d. Returns ('T', path) / ('corner', pt, path) / ('cap', path)."""
    E = edges(P)
    V = set(P)
    px, py = S
    dx, dy = F(d[0]), F(d[1])
    path = [(px, py)]
    for _ in range(maxref):
        best = None
        for (ax, ay), (bx, by) in E:
            if ax == bx and dx != 0:
                s = (ax - px) / dx
                yy = py + s * dy
                if s > 0 and min(ay, by) <= yy <= max(ay, by) and (best is None or s < best[0]):
                    best = (s, 'v')
            elif ay == by and dy != 0:
                s = (ay - py) / dy
                xx = px + s * dx
                if s > 0 and min(ax, bx) <= xx <= max(ax, bx) and (best is None or s < best[0]):
                    best = (s, 'h')
        s, kind = best
        # target on the open segment?
        st = (T[0] - px) / dx if dx else (T[1] - py) / dy
        if 0 < st < s and px + st * dx == T[0] and py + st * dy == T[1]:
            path.append(T)
            return ('T', None, path)
        nx, ny = px + s * dx, py + s * dy
        path.append((nx, ny))
        if (nx, ny) in V:
            return ('corner', (nx, ny), path)
        px, py = nx, ny
        if kind == 'v':
            dx = -dx
        else:
            dy = -dy
    return ('cap', None, path)


def fmt(pt):
    return "(%s,%s)" % (pt[0], pt[1]) if pt else "-"


# ------------------------------------------------------------------ R22
R22 = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3), (2, -3), (2, -1), (1, -1), (1, 1), (3, 1), (3, 0), (5, 0),
       (5, 1), (4, 1), (4, 2), (3, 2), (3, 3), (1, 3), (1, 2), (0, 2), (0, 1), (-1, 1)]
R22 = [(F(a), F(b)) for a, b in R22]


def r22_deformed(t, lift=2):
    t = F(t)

    def phi(y):
        y = t * y
        return y if y <= t else y + lift
    return [(t * x, phi(y)) for x, y in R22]


def claim1():
    say("\n=== Claim 1: local freedom at interior pins; quadrant types")
    for name, P, S, T in (("R22", R22, (F(0), F(0)), (F(2), F(2))),
                          ("R22 deformed t=2", r22_deformed(2), (F(0), F(0)), (F(4), F(6))),
                          ("six-reflex m=1", six(1), (F(0), F(0)), (F(44), F(44)))):
        xs, ys = refined_gap(P, [S, T])
        for p in (S, T):
            pinned = p[0] in {v[0] for v in P} and p[1] in {v[1] for v in P}
            dp = delta_p(xs, ys, p)
            ok = pinned and square_free(P, p, dp) and quadrants(P, p, dp / 2) == [True] * 4
            # sharpness: the square of radius slightly larger than dp fails somewhere for at least one pin? not claimed
            check(ok, f"{name}: pin {fmt(p)} has both coordinates on wall levels, free open square of radius "
                      f"delta_p={dp}, four occupied quadrants")
    # quadrant types at every grid vertex of R22: occupancy patterns realized
    xs = sorted({v[0] for v in R22}); ys = sorted({v[1] for v in R22})
    pats = {}
    Vset = set(R22)
    bad = []
    for x in xs:
        for y in ys:
            q = quadrants(R22, (x, y), F(1, 2))
            k = sum(q)
            opp = k == 2 and q[0] == q[2]
            typ = 'pinch' if opp else {0: 'ext', 1: 'convex', 2: 'smooth', 3: 'reflex', 4: 'interior'}[k]
            pats[typ] = pats.get(typ, 0) + 1
            if (typ in ('convex', 'reflex')) != ((x, y) in Vset) or typ == 'pinch':
                bad.append((x, y, typ))
    check(not bad and pats.get('convex') == 13 and pats.get('reflex') == 9,
          f"R22 grid points: types {pats}; convex/reflex exactly at the 13+9 vertices, no pinch")


def claim3():
    say("\n=== Claim 3: R22 deformation (0,0)->(2t,2t+2)")
    S = (F(0), F(0))
    for t in (1, 2, 5):
        P = r22_deformed(t)
        T = (F(2 * t), F(2 * t + 2))
        simple = orthogonal(P) and strictly_simple(P)
        check(simple and len(P) == 22 and reflex_count(P) == 9,
              f"t={t}: deformed room orthogonal, strictly simple, 22 walls, 9 reflex")
        # chart: same vertex order type in x and y as dilated R22
        D = [(F(t) * x, F(t) * y) for x, y in R22]
        rank = lambda L, i: [sorted({v[i] for v in L}).index(v[i]) for v in L]
        check(rank(P, 0) == rank(D, 0) and rank(P, 1) == rank(D, 1),
              f"t={t}: marked chart preserved (vertex rank vectors in x and y agree with the dilation)")
        xs, ys = refined_gap(P, [S, T])
        g = min(min(b - a for a, b in zip(xs, xs[1:])), min(b - a for a, b in zip(ys, ys[1:])))
        pinned = all(p[0] in {v[0] for v in P} and p[1] in {v[1] for v in P} for p in (S, T))
        check(g == t and pinned and inside(P, S) and inside(P, T) and T[0] % 2 == 0 and T[1] % 2 == 0,
              f"t={t}: least refined gap {g}, both marks pinned and interior, T={fmt(T)} keeps even parity")
        st, info, path = trace(P, S, T, T)
        x1 = path[1][0] if len(path) > 1 else None
        check(st == 'T' and len(path) == 2, f"t={t}: direct segment S->T is legal (no reflection); "
              f"predicted interface abscissa t^2/(t+1)={F(t * t, t + 1)}")
        # crossing of y=t
        xc = F(2 * t) * F(t) / F(2 * t + 2)
        check(xc == F(t * t, t + 1) and 0 < xc < t, f"t={t}: crossing at y=t is {xc} in (0,t)")
        # undeformed: direct chord hits the reflex corner (t,t)
        st2, info2, _ = trace(D, S, (2 * t, 2 * t), (F(2 * t), F(2 * t)))
        check(st2 == 'corner' and info2 == (F(t), F(t)), f"t={t}: dilated R22 direct chord hits corner {fmt(info2)}")
        # determinant test: det(tv+w, tc+e) with v=(2,2), w=(0,2), c=(1,1), e=0
        det = 2 * t * t - (2 * t + 2) * t
        check(det == -2 * t, f"t={t}: det((2t,2t+2),(t,t)) = {det} = -2t (corner to the right of the ray)")


def claim4():
    say("\n=== Claim 4: graze determinant expansion")
    ok = True
    for v, w, c, e in (((2, 2), (0, 2), (1, 1), (0, 0)), ((3, 1), (1, -2), (6, 2), (2, 5)),
                       ((1, 4), (-3, 2), (2, 8), (-1, 1))):
        dt = lambda a, b: a[0] * b[1] - a[1] * b[0]
        assert dt(v, c) == 0
        for t in (1, 2, 7, 50):
            lhs = dt((t * v[0] + w[0], t * v[1] + w[1]), (t * c[0] + e[0], t * c[1] + e[1]))
            ok &= lhs == t * (dt(v, e) + dt(w, c)) + dt(w, e)
    check(ok, "det(tv+w,tc+e) = t[det(v,e)+det(w,c)] + det(w,e) when det(v,c)=0 (3 cases x 4 t)")


def claim5():
    say("\n=== Claim 5: sign-pattern identity and attainable patterns")
    ok = True
    for K, D, a, b in ((F(4), F(8), F(2), F(0)), (F(9), F(13), F(1), F(3)), (F(44), F(44), F(2), F(2))):
        for al in (F(1, 7), F(1, 4), F(1, 2), F(5, 6)):
            ok &= K * (D * al + a) / (D + a + b) - K * al == K * (a * (1 - al) - b * al) / (D + a + b)
    check(ok, "crossing displacement K[(D alpha+a)/(D+a+b) - alpha] = K[a(1-alpha)-b alpha]/(D+a+b)")
    # q(alpha) = a(1-alpha) - b alpha is affine nonincreasing for a,b >= 0, so (-,+) is impossible.
    pats = set()
    d0, d3 = F(1), F(1)
    for e in range(0, 4):
        for f in range(0, 4):
            a, b = 2 * e * d0, 2 * f * d3
            q = [a * (1 - al) - b * al for al in (F(1, 4), F(3, 4))]
            pats.add(tuple((x > 0) - (x < 0) for x in q))
    check((-1, 1) not in pats, f"e,f in 0..3, d0=d3: sign patterns at (1/4,3/4) = {sorted(pats)}; (-,+) absent")
    # repeated bounces move the switch point: theta = e d0/(e d0 + f d3)
    th = sorted({F(e, e + f) for e in range(1, 4) for f in range(1, 4)})
    check(len(th) > 1, f"repeated end bounces (e,f in 1..3, d0=d3) give switch points {[str(x) for x in th]}, "
                       f"not only d0/(d0+d3)")
    # a transverse endpoint shift (Delta0 at source, Delta3 at target) moves gate i by (1-alpha)Delta0+alpha Delta3:
    q = [(1 - al) * (-2) + al * 2 for al in (F(1, 4), F(3, 4))]
    check(q[0] < 0 < q[1], "transverse endpoint images shifted by -2 and +2 produce a (-,+) pattern "
                           "(outside the note's longitudinal end-bounce model)")


def claim6():
    say("\n=== Claim 6: X'_i = X_i + sigma' q_i")
    ok = True
    for K, D, a, b in ((F(44), F(44), F(2), F(2)), (F(7), F(19), F(4), F(0)), (F(3), F(5), F(0), F(6))):
        Dp = D + a + b
        for al in (F(1, 4), F(3, 4), F(2, 5)):
            ok &= K * (D * al + a) / Dp == K * al + (K / Dp) * (a * (1 - al) - b * al)
    check(ok, "interpolation identity at 9 (K,D,a,b,alpha) points")


# ------------------------------------------------------------------ six-reflex room
def six(m):
    m = F(m)
    t = 10 * m + 1
    tiers = [((-m, F(0)), (-2 * t - 1, t)), ((F(0), t), (-t, t)), ((t, 3 * t), (F(0), 4 * t)),
             ((3 * t, 4 * t), (3 * t, 6 * t)), ((4 * t, 4 * t + m), (3 * t, 7 * t))]
    # right side going up, then left side going down
    R = []
    for (y0, y1), (l, r) in tiers:
        R += [(r, y0), (r, y1)]
    L = []
    for (y0, y1), (l, r) in reversed(tiers):
        L += [(l, y1), (l, y0)]
    P = R + L
    # merge collinear / duplicate points
    out = []
    for p in P:
        if out and out[-1] == p:
            continue
        out.append(p)
    if out[0] == out[-1]:
        out.pop()
    changed = True
    while changed:
        changed = False
        n = len(out)
        for i in range(n):
            a, b, c = out[i - 1], out[i], out[(i + 1) % n]
            if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]):
                out.pop(i)
                changed = True
                break
    return out


def claim7():
    say("\n=== Claim 7: six-reflex room, t=10m+1")
    for m in (1, 2, 3):
        t = 10 * m + 1
        P = six(m)
        S, T = (F(0), F(0)), (F(4 * t), F(4 * t))
        check(orthogonal(P) and strictly_simple(P) and reflex_count(P) == 6 and len(P) == 16,
              f"m={m}: orthogonal, strictly simple, 16 walls, 6 reflex")
        xs = sorted({v[0] for v in P}); ys = sorted({v[1] for v in P})
        gx = [b - a for a, b in zip(xs, xs[1:])]; gy = [b - a for a, b in zip(ys, ys[1:])]
        gg = lambda L: __import__('functools').reduce(gcd, [int(v) for v in L])
        check(inside(P, S) and inside(P, T) and S[0] in xs and S[1] in ys and T[0] in xs and T[1] in ys
              and min(gx + gy) == m and gg(gx) == 1 and gg(gy) == 1,
              f"m={m}: S, T interior and pinned; x gaps {[str(v) for v in gx]}, y gaps {[str(v) for v in gy]}; "
              f"min gap m, gcds 1")
        # unbounced chord and the three end-bounce chords
        cases = [("unbounced", (4 * t, 4 * t)), ("floor", (4 * t, 4 * t + 2 * m)),
                 ("roof", (4 * t, 4 * t + 2 * m)), ("both", (4 * t, 4 * t + 4 * m))]
        res = []
        for lab, d in cases:
            # floor bounce: developed source (0,-2m), so the ray leaves S downward
            dd = (d[0], -d[1]) if lab in ("floor", "both") else d
            st, info, path = trace(P, S, dd, T, maxref=6)
            res.append((lab, st, info, [fmt(p) for p in path[:5]]))
        say("   " + "; ".join(f"{l}: {s} {fmt(i)}" for l, s, i, _ in res))
        check(res[0][1] == 'corner' and res[0][2] == (F(t), F(t)),
              f"m={m}: unbounced chord grazes and dies at reflex (t,t)=({t},{t}) [alpha=1/4 needs minus]")
        mid = lambda p: p[1] not in (F(-m), F(4 * t + m))
        check(all(r[1] != 'T' for r in res[1:]) and
              all(any(mid(q) for q in trace(P, S, (cd[0], -cd[1]) if l in ("floor", "both") else cd, T, 6)[2][1:3])
                  for l, cd in cases[1:]),
              f"m={m}: floor, roof and both-bounce chords fail on the first pass: each reflects off a "
              f"middle-tier wall within 6 reflections (paths: " +
              " | ".join(f"{l} {p}" for l, s, i, p in res[1:]) + ")")


def claim7_lit():
    say("\n=== Claim 7 (m=1): is (0,0),(44,44) lit? 20 hand-chosen directions, <=400 reflections each")
    P = six(1)
    S, T = (F(0), F(0)), (F(44), F(44))
    # direction (dx,dy) and the itinerary idea that motivated it
    cands = [
        ((1, 1), "unbounced winding (pin)"),
        ((22, 23), "roof bounce"),
        ((22, -23), "floor bounce"),
        ((11, -12), "floor+roof bounce"),
        ((1, 2), "E2 roof y=3t then E2 floor y=t, monotone transverse"),
        ((1, 3), "E2 roof/floor twice"),
        ((3, 2), "bounce off E1/E2 walls x=t, x=0"),
        ((5, 2), "two transverse folds"),
        ((-1, 1), "start left, E1 wall x=-t"),
        ((-1, 2), "start left, then E2"),
        ((-1, -1), "end-tier floor and ceiling over (-2t-1,-t)"),
        ((3, 1), "shallow right"),
        ((2, 3), ""),
        ((3, 4), ""),
        ((1, 4), "E2 three vertical traversals"),
        ((1, -2), "floor bounce, then (1,2) pattern"),
        ((2, 1), "shallow"),
        ((-3, 2), "left winding"),
        ((5, 4), ""),
        ((3, 5), ""),
    ]
    lit = []
    for d, why in cands:
        st, info, path = trace(P, S, d, T)
        nref = len(path) - 2 if st == 'T' else len(path) - 1
        say(f"   d={d}: {st} {fmt(info)} after {nref} reflections  [{why}]")
        if st == 'T':
            lit.append((d, path))
    check(len(cands) <= 30, f"{len(cands)} candidate directions (budget 30)")
    check(any(d == (1, 2) for d, _ in lit), "direction (1,2) reaches T")
    for d, path in lit:
        say(f"   LIT d={d}: path " + " -> ".join(fmt(p) for p in path))
    # exact witness geometry for general m: (0,0)->(t/2,t)->(3t/2,3t)R->(5t/2,t)R->(7t/2,3t)->(4t,4t)
    for m in (1, 2, 3, 7):
        t = 10 * m + 1
        st, info, path = trace(six(m), S, (1, 2), (F(4 * t), F(4 * t)))
        exp = [(F(0), F(0)), (F(t, 2), F(t)), (F(3 * t, 2), F(3 * t)), (F(5 * t, 2), F(t)), (F(7 * t, 2), F(3 * t)),
               (F(4 * t), F(4 * t))]
        # the tracer records only reflection points; gate crossings are not vertices of the path
        check(st == 'T' and path == [exp[0], exp[2], exp[3], exp[5]],
              f"m={m}: (1,2) witness reflects at {fmt(exp[2])} (E2 roof) and {fmt(exp[3])} (E2 floor), "
              f"gate crossings {fmt(exp[1])}, {fmt(exp[4])}")


def interior_bounce():
    say("\n=== Extra: an interior roof-floor double bounce realizes (-,+)")
    # inserting 2L of longitudinal travel at a slab strictly between the gates (developed target
    # moves from D to D+2L) shifts a gate below the slab by -K a 2L/(D+2L), a gate above by +K(1-a)2L/(D+2L)
    ok = True
    for K, D, L in ((F(44), F(44), F(22)), (F(5), F(9), F(2)), (F(7), F(20), F(11))):
        for a in (F(1, 8), F(1, 4), F(3, 4)):
            ok &= K * a * D / (D + 2 * L) - K * a == -K * a * 2 * L / (D + 2 * L)
            ok &= K * (a * D + 2 * L) / (D + 2 * L) - K * a == K * (1 - a) * 2 * L / (D + 2 * L)
    check(ok, "gate below the bounced slab moves by -K alpha 2L/(D+2L) < 0; gate above by +K(1-alpha)2L/(D+2L) > 0")
    t = F(11)
    check((4 * t * t / (8 * t) - t, 4 * t * 7 * t / (8 * t) - 3 * t) == (-t / 2, t / 2),
          "six-reflex m=1, L=2t: displacements at the two pins are (-t/2, +t/2), the demanded (-,+)")


def claim8():
    say("\n=== Claim 8: interval-chain test; R22 multiple components at y=1")

    def slabs(P, y):
        """open x-intervals of the slab just above (+1) / below (-1) height y."""
        xs = sorted({v[0] for v in P})
        res = {}
        for sgn in (1, -1):
            yy = y + sgn * F(1, 1000)
            ivs = []
            for a, b in zip(xs, xs[1:]):
                if inside(P, ((a + b) / 2, yy)):
                    if ivs and ivs[-1][1] == a:
                        ivs[-1] = (ivs[-1][0], b)
                    else:
                        ivs.append((a, b))
            res[sgn] = ivs
        return res

    s = slabs(R22, F(1))
    up, dn = s[1], s[-1]
    ov = [(max(a, c), min(b, d)) for a, b in dn for c, d in up if max(a, c) < min(b, d)]
    check(up == [(0, 4)] and dn == [(-1, 1), (3, 5)] and ov == [(0, 1), (3, 4)],
          f"R22 y=1: below {dn}, above {up}, openings {ov}")
    # direct ray (0,0)->(2,2) crosses y=1 at x=1, the right end of the opening of its own component
    check(F(1) == ov[0][1], "R22 direct ray crosses y=1 at x=1, endpoint of the opening (0,1)")
    # chain test agrees with the tracer on the deformed R22 and the six-reflex chords
    def chain(P, S, T):
        lv = sorted({v[1] for v in P if S[1] < v[1] < T[1]})
        dx = (T[0] - S[0]) / (T[1] - S[1])
        comp = None
        for y in [S[1]] + lv:
            ivs = slabs(P, y)[1]
            x = S[0] + (y - S[1]) * dx
            # component above y containing the crossing
            c = [iv for iv in ivs if iv[0] < x < iv[1]]
            if not c:
                return False
            if comp is not None and not (comp[0] < x < comp[1]):
                return False
            comp = c[0]
        return comp[0] < T[0] < comp[1]
    for t in (1, 2, 5):
        P = r22_deformed(t)
        check(chain(P, (F(0), F(0)), (F(2 * t), F(2 * t + 2))) and
              not chain([(F(t) * x, F(t) * y) for x, y in R22], (F(0), F(0)), (F(2 * t), F(2 * t))),
              f"t={t}: chain test passes the deformed direct chord and rejects the dilated one (tracer agrees)")
    P = six(1)
    check(not chain(P, (F(0), F(0)), (F(44), F(44))), "six-reflex m=1: chain test rejects the unbounced chord")


if __name__ == '__main__':
    claim1()
    claim3()
    claim4()
    claim5()
    claim6()
    claim7()
    claim7_lit()
    interior_bounce()
    claim8()
    say(f"\ncpu {time.process_time() - T0:.2f}s")
    say(f"FAILURES: {len(FAILS)}" + (f" ({FAILS})" if FAILS else ""))
