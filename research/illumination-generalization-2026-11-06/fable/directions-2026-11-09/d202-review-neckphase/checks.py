"""d202 referee checks: neck phase map and the aligned 3x4 middle-chamber family.

Standard library only, exact Fraction arithmetic. Named rooms only. For each
room the ray that snapshot.md prescribes is computed from the note's formulas
(at most one floor operation or one modular inverse) and that single ray is
traced. No ray, direction, word or room-size search.

Part A: the 3x4 family. Ends [0,3]x[0,3] and [P,P+3]x[0,3], middle
         [D1,D1+3]x[0,4], unit necks at 1<y<2, D1=X+3, D2=Y+3, 1<=X,Y<=25.
         All 91 interior lattice pairs.
Part B: the gcd condition of the H0/H paragraph in six named room shapes.
Part C: the explicit families of the neck-map sections (displaced mouths,
         reflected stubs, adjacent mouths).
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from math import gcd, floor
import time

T0 = time.process_time()


# ---------------------------------------------------------------------------
# Geometry helpers

def turn_word(V):
    n = len(V)
    out = []
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        assert cr != 0
        out.append('L' if cr > 0 else 'R')
    return ''.join(out)


def canon(w):
    cands = []
    for s in (w, w[::-1]):
        cands += [s[i:] + s[:i] for i in range(len(s))]
    return min(cands)


def check_simple(V):
    """Orthogonal, counterclockwise, no two non-adjacent edges meet."""
    n = len(V)
    E = [(V[i], V[(i + 1) % n]) for i in range(n)]
    for a, b in E:
        assert (a[0] == b[0]) != (a[1] == b[1]), (a, b)
    area2 = sum(V[i][0] * V[(i + 1) % n][1] - V[(i + 1) % n][0] * V[i][1]
                for i in range(n))
    assert area2 > 0

    def meet(e, f):
        (a, b), (c, d) = e, f
        return (max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0])) and
                max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1])))
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            assert not meet(E[i], E[j]), (E[i], E[j])
    return F(area2, 2)


def inside(V, p):
    x, y = p
    c = False
    for i in range(len(V)):
        (x0, y0), (x1, y1) = V[i], V[(i + 1) % len(V)]
        if x0 == x1 and min(y0, y1) < y <= max(y0, y1) and x0 > x:
            c = not c
    return c


def on_boundary(V, p):
    x, y = p
    for i in range(len(V)):
        (x0, y0), (x1, y1) = V[i], V[(i + 1) % len(V)]
        if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1):
            return True
    return False


def interior(V, p):
    return inside(V, p) and not on_boundary(V, p)


def trace(V, p, d, target, max_bounces=2000):
    """Billiard ray p + t d. Returns ('hit'|'corner'|'over', bounce list)."""
    verts = {(F(a), F(b)) for a, b in V}
    edges = [(V[i], V[(i + 1) % len(V)]) for i in range(len(V))]
    px, py = F(p[0]), F(p[1])
    dx, dy = F(d[0]), F(d[1])
    assert dx != 0 or dy != 0
    tx, ty = F(target[0]), F(target[1])
    bounces = []
    while True:
        best = None
        for (a, b) in edges:
            if a[0] == b[0]:
                if dx == 0:
                    continue
                t = (a[0] - px) / dx
                if t <= 0:
                    continue
                y = py + t * dy
                if min(a[1], b[1]) <= y <= max(a[1], b[1]):
                    if best is None or t < best[0]:
                        best = (t, 'v', (F(a[0]), y))
            else:
                if dy == 0:
                    continue
                t = (a[1] - py) / dy
                if t <= 0:
                    continue
                x = px + t * dx
                if min(a[0], b[0]) <= x <= max(a[0], b[0]):
                    if best is None or t < best[0]:
                        best = (t, 'h', (x, F(a[1])))
        assert best is not None, "ray escaped"
        t, kind, q = best
        tt = (tx - px) / dx if dx != 0 else (ty - py) / dy
        if 0 < tt < t and px + tt * dx == tx and py + tt * dy == ty:
            return 'hit', bounces
        if q in verts:
            return 'corner', bounces + [(kind, q)]
        bounces.append((kind, q))
        if len(bounces) > max_bounces:
            return 'over', bounces
        px, py = q
        if kind == 'v':
            dx = -dx
        else:
            dy = -dy


def first_above(a0, spacing, lo):
    """First member of a0 + spacing*Z strictly above lo (one floor)."""
    return a0 + spacing * (floor((lo - a0) / spacing) + 1)


OPP_KEY = 'LLLLRRLLRRLLLLRRLLRR'
ADJ_KEY = 'LLLLRRLLLRRLLLLRRLRR'

# ---------------------------------------------------------------------------
# Part A: the 3x4 family

HM = 4   # middle height


def room34(D1, D2):
    P = D1 + D2
    return [(0, 0), (3, 0), (3, 1), (D1, 1), (D1, 0), (D1 + 3, 0), (D1 + 3, 1),
            (P, 1), (P, 0), (P + 3, 0), (P + 3, 3), (P, 3), (P, 2),
            (D1 + 3, 2), (D1 + 3, HM), (D1, HM), (D1, 2), (3, 2), (3, 3), (0, 3)]


def marks34(D1, D2):
    P = D1 + D2
    out = []
    for ci, s, rows in ((0, 0, (1, 2)), (1, D1, (1, 2, 3)), (2, P, (1, 2))):
        for u in (1, 2):
            for y in rows:
                out.append((ci, (s + u, y)))
    return out


STATS = Counter()


def build_left(D1, D2, p, q):
    """p in the left end chamber, q in the middle or right end chamber.
    Returns (dir, label)."""
    P, Dl = D1 + D2, D2 - D1
    u, yp = p
    qx, yq = q
    if yp != yq and yq in (1, 2):
        return (qx - u, yq - yp), 'different-rows'
    s = 1 if yp == 1 else -1          # vertical sign toward the far band edge
    if yq == 3:                       # middle target above the band
        v = qx - D1
        if yp == 1:
            U = u - D1
            for sg in (1, -1):
                a = F(sg * v + U, 2) % 3   # (1+t)a == sg*v + tU (mod 6), t=1
                if a != 0:
                    break
            assert 0 < a < 3
            STATS['row1->row3 sign %+d' % sg] += 1
            return (a - U, 1), 'row1-to-row3 pocket base'
        B = qx - u
        m = F(2, v)
        k = 6 * m - F(1, B)
        assert 1 + 6 * m * v == 13
        return (F(1), k), 'row2-to-row3 fast slope m=%s' % m
    if qx < P:                        # adjacent: left end and middle
        v = qx - D1
        D = D1
        if D > max(6 - u - v, u + v):
            m = F(D + u + v, 2)
            assert 3 < m < D
            return (m - u, s), 'adjacent-bounce'
        assert D == 4 and u == v
        U, V = -u, 4 + u
        M = U + V
        lo, hi = max(F(0), M - 3, F(U)), min(F(3), F(M))
        a = first_above(F(M + 2 * U, 4), F(3, 2), lo)   # h=g=1 end pocket
        assert lo < a < hi and a == F(5 - u, 2)
        return (-(a + u), s), 'adjacent-repair (end pocket)'
    # outer pair
    v = qx - P
    if Dl + v - u < 0:
        m = F(P + v - u, 2)
        assert 3 < m < D1
        return (-(m + u), s), 'outer-left-wall'
    if Dl + u - v > 0:
        m = F(P + 6 + u - v, 2)
        assert D1 + 3 < m < P
        return (m - u, s), 'outer-right-wall'
    U, V = u - D1, D2 + v
    M = U + V
    assert M in (2, 3, 4)
    lo, hi = max(F(0), M - 3, F(U)), min(F(3), F(M))
    h = 2 if yp == 1 else 1           # upper pocket (2,4) or lower pocket (0,1)
    coef = 2 + 2 * h
    spacing = F(6, coef)
    a = first_above(F(M + 2 * h * U, coef), spacing, lo)
    assert lo < a < hi, (lo, a, hi)
    assert hi - lo >= 2 > spacing
    STATS['pocket h=%d M=%d' % (h, M)] += 1
    return (a - U, s), 'outer-middle-pocket h=%d' % h


def construct(D1, D2, ci, p, cj, q):
    P = D1 + D2
    if ci == cj:
        return p, (q[0] - p[0], q[1] - p[1]), q, 'same-chamber'
    if ci == 1:                       # put the end-chamber mark first
        ci, p, cj, q = cj, q, ci, p
    if ci == 0:
        d, lab = build_left(D1, D2, p, q)
        return p, d, q, lab
    # source in right end: reverse x (room (D2,D1) is the same family)
    mp = (P + 3 - p[0], p[1])
    mq = (P + 3 - q[0], q[1])
    d, lab = build_left(D2, D1, mp, mq)
    return p, (-d[0], d[1]), q, lab


def part_a(NMAX=25):
    print("Part A: 3x4 middle chamber, X,Y in 1..%d (D = X+3)" % NMAX)
    V = room34(4, 4)
    area = check_simple(V)
    w = turn_word(V)
    print("  room X=Y=1: area %s, W=%d, canonical word %s, key match %s"
          % (area, len(V), canon(w), canon(w) == OPP_KEY))
    tot = Counter()
    fails = []
    maxb = 0
    rooms = 0
    for X in range(1, NMAX + 1):
        for Y in range(1, NMAX + 1):
            D1, D2 = X + 3, Y + 3
            V = room34(D1, D2)
            check_simple(V)
            assert canon(turn_word(V)) == OPP_KEY
            mk = marks34(D1, D2)
            assert len(mk) == 14
            for _, p in mk:
                assert interior(V, p)
            # every interior lattice point is a mark
            lattice = [(x, y) for x in range(1, D1 + D2 + 3) for y in range(1, HM)
                       if interior(V, (x, y))]
            assert sorted(lattice) == sorted(p for _, p in mk)
            rooms += 1
            npairs = 0
            for (ci, p), (cj, q) in combinations(mk, 2):
                s, d, t, lab = construct(D1, D2, ci, p, cj, q)
                res, b = trace(V, s, d, t)
                npairs += 1
                tot[lab] += 1
                maxb = max(maxb, len(b))
                if res != 'hit':
                    fails.append((X, Y, p, q, lab, res, b[-1:] if b else b))
            assert npairs == 91
    print("  rooms %d, pairs %d" % (rooms, sum(tot.values())))
    for k in sorted(tot):
        print("    %-36s %6d" % (k, tot[k]))
    print("  sub-statistics:", dict(sorted(STATS.items())))
    print("  max bounces on a prescribed ray: %d" % maxb)
    print("  failures (corner or miss): %d" % len(fails))
    for f in fails[:20]:
        print("   ", f)

    print("  controls (expected failures):")
    # d201's h=1 entry value used in the 4-tall chamber
    D1 = D2 = 7
    V = room34(D1, D2)
    u = v = 1
    U, Vv = u - D1, D2 + v
    M = U + Vv
    lo = max(F(0), M - 3, F(U))
    a_old = first_above(F(M + 2 * U, 4), F(3, 2), lo)
    print("    X=Y=4 (1,1)->(15,1) with d201 h=1 entry a=%s in the h=2 pocket:" % a_old,
          trace(V, (1, 1), (a_old - U, 1), (15, 1))[0])
    a_new = first_above(F(M + 4 * U, 6), F(1), lo)
    print("    same pair with the note's h=2 entry a=%s:" % a_new,
          trace(V, (1, 1), (a_new - U, 1), (15, 1))[0])
    # row2->row3 with m not solving 6vm == +-y-1 (mod 8)
    D1 = D2 = 5
    V = room34(D1, D2)
    B = D1 + 1 - 1
    for m in (1, 3):
        r = trace(V, (1, 2), (1, 6 * m - F(1, B)), (D1 + 1, 3))
        print("    X=2 (1,2)->(%d,3) slope 6m-1/B with m=%d (unfolded 1+6m=%d):" % (D1 + 1, m, 1 + 6 * m),
              r[0])


# ---------------------------------------------------------------------------
# Part B: gcd condition for an end chamber of height H0 (floor Fl) and a
# middle chamber of height H (floor 0), width w, unit band (1,2).

def room_gen(D1, D2, H0, Fl, H, w):
    P = D1 + D2
    E = Fl + H0
    return [(0, Fl), (3, Fl), (3, 1), (D1, 1), (D1, 0), (D1 + w, 0), (D1 + w, 1),
            (P, 1), (P, Fl), (P + 3, Fl), (P + 3, E), (P, E), (P, 2),
            (D1 + w, 2), (D1 + w, H), (D1, H), (D1, 2), (3, 2), (3, E), (0, E)]


def solve_m(A, b, n):
    """Least positive m with A*m == b (mod n), or None. One modular inverse."""
    g = gcd(A, n)
    if b % g:
        return None
    A2, b2, n2 = A // g, b // g, n // g
    m = (b2 * pow(A2, -1, n2)) % n2 if n2 > 1 else 0
    return m if m > 0 else n2


def part_b():
    print("\nPart B: row-2 source, slope 2*H0*m - 1/B, target (D1+v, y) in the middle")
    shapes = [(3, 0, 4, 3), (3, 0, 5, 3), (3, 0, 6, 3), (4, 0, 5, 4), (5, -1, 6, 3), (4, -1, 7, 5)]
    for (H0, Fl, H, w) in shapes:
        hits = fails = nocond = 0
        uncovered = set()
        for X, Y in ((1, 1), (1, 4), (3, 2), (7, 5), (12, 12)):
            D1 = X + 3
            D2 = Y + w
            V = room_gen(D1, D2, H0, Fl, H, w)
            check_simple(V)
            assert canon(turn_word(V)) == OPP_KEY
            for u in (1, 2):
                S = (u, 2)
                assert interior(V, S)
                for v in range(1, w):
                    for y in range(1, H):
                        T = (D1 + v, y)
                        assert interior(V, T)
                        cond = any((sg * y - 1) % gcd(2 * H0 * v, 2 * H) == 0 for sg in (1, -1))
                        m = None
                        for sg in (1, -1):
                            m = solve_m(2 * H0 * v, sg * y - 1, 2 * H)
                            if m is not None:
                                break
                        assert (m is not None) == cond
                        if m is None:
                            nocond += 1
                            uncovered.add((v, y))
                            continue
                        B = T[0] - S[0]
                        res, b = trace(V, S, (1, 2 * H0 * m - F(1, B)), T)
                        if res == 'hit':
                            hits += 1
                        else:
                            fails += 1
                            print("    FAIL", (H0, Fl, H, w), X, Y, S, T, m, res, b[-1:])
        print("  H0=%d floor=%d H=%d w=%d: condition holds %d, traced hits %d, failures %d;"
              " (v,y) without condition: %s" % (H0, Fl, H, w, hits + fails, hits, fails,
                                                sorted(uncovered) or 'none'))


# ---------------------------------------------------------------------------
# Part C: explicit neck-phase families

def room_disp(L, R, w, delta, h, left, right):
    """Left chamber [xl0,-L]x[lf,lr], neck (0,1) on -L<x<0, middle
    [0,w]x[-1,delta+2+h], neck (delta+1,delta+2) on w<x<w+R, right chamber
    [w+R, w+R+Wr]x[rf,rr]."""
    xl0, lf, lr = left
    Wr, rf, rr = right
    mr = delta + 2 + h
    return [(xl0, lf), (-L, lf), (-L, 0), (0, 0), (0, -1), (w, -1), (w, delta + 1),
            (w + R, delta + 1), (w + R, rf), (w + R + Wr, rf), (w + R + Wr, rr),
            (w + R, rr), (w + R, delta + 2), (w, delta + 2), (w, mr), (0, mr),
            (0, 1), (-L, 1), (-L, lr), (xl0, lr)]


def run_family(name, cases):
    hits = 0
    fails = []
    maxb = 0
    for V, S, d, T, tag in cases:
        check_simple(V)
        assert interior(V, S) and interior(V, T)
        res, b = trace(V, S, d, T)
        maxb = max(maxb, len(b))
        if res == 'hit':
            hits += 1
        else:
            fails.append((tag, res, b[-1:]))
    print("  %s: rooms %d, hits %d, failures %d, max bounces %d"
          % (name, len(cases), hits, len(fails), maxb))
    for f in fails[:10]:
        print("    FAIL", f)


def part_c():
    print("\nPart C: neck-phase families (one prescribed ray per named room)")
    words = set()
    # (1) strip family: e=f=1, r=1/2, w=2, delta even, L,R multiples of 4
    cases = []
    for delta in (2, 4, 6, 10):
        for L in (4, 8, 12, 40):
            for R in (4, 8, 20, 100):
                w = 2
                V = room_disp(L, R, w, delta, 1, (-L - 3, -1, 2), (3, delta, delta + 3))
                words.add(canon(turn_word(V)))
                cases.append((V, (-L - 1, 0), (2, 1), (w + R + 1, delta + 2), (delta, L, R)))
    run_family("strip family w=2, delta even, L,R = 0 mod 4", cases)
    # (2) roof-pocket family
    cases = []
    for delta in range(1, 7):
        w, h = 2 * delta + 8, delta + 5
        for L in (4, 8, 16):
            for R in (2, 6, 10, 30):
                V = room_disp(L, R, w, delta, h, (-L - 3, -1, 2), (3, delta, delta + 3))
                words.add(canon(turn_word(V)))
                # prediction: a = 2delta+3, b = 2delta+7, roof contact a+h/r
                a, b = 2 * delta + 3, 2 * delta + 7
                assert (a + 4 * h - b) % (2 * w) == 0 and (a + 2 * h) % w != 0
                cases.append((V, (-L - 1, 0), (2, 1), (w + R + 1, delta + 2), (delta, L, R)))
    run_family("roof family w=2d+8, h=d+5, L=0, R=2 mod 4", cases)
    # (3) reflected-stub family in the K=2A residual, r=1/4
    cases = []
    big = 0
    for H0 in (3, 4):
        for H1 in (3, 5):
            for i in (1, 2):
                for j in (1, 2):
                    for L in (8, 16, 64):
                        for w in (5, 9):
                            for n in (1, 2):
                                e, f = 8 * H0 * i + 1, 8 * H1 * j + 1
                                A = e + L
                                R = 2 * A - f
                                if R <= 0:
                                    continue
                                delta = ((4 * n + 1) * w - 5) // 4
                                assert 4 * delta == (4 * n + 1) * w - 5 and delta > 0
                                K = f + R
                                assert K == 2 * A
                                big += (e >= 3 * w and f >= 3 * w)
                                V = room_disp(L, R, w, delta, 2,
                                              (-L - e - 2, -1, H0 - 1),
                                              (f + 2, delta, delta + H1))
                                words.add(canon(turn_word(V)))
                                cases.append((V, (-L - e, 0), (4, 1), (w + R + f, delta + 2),
                                              (H0, H1, i, j, L, w, n)))
    run_family("reflected-stub K=2A family, r=1/4 (%d with e,f >= 3w)" % big, cases)
    print("  displaced-mouth rooms: canonical words %s (opposite key: %s)"
          % (sorted(words), words == {OPP_KEY}))
    # (4) adjacent mouths, r=2/3
    cases = []
    words = set()
    for l in (1, 2):
        for HL in (3, 5, 7):
            H = l + HL
            t = 3 * (HL - 1) // 2
            for w in (t + 2, t + 5):
                for L in (3, 6, 9):
                    for R in (4, 8, 12):
                        V = [(-L - 3, l - 1), (-L, l - 1), (-L, l), (0, l), (0, 0), (w, 0),
                             (w, H), (t + 1, H), (t + 1, H + R), (t + 3, H + R),
                             (t + 3, H + R + 2), (t - 1, H + R + 2), (t - 1, H + R),
                             (t, H + R), (t, H), (0, H), (0, l + 1), (-L, l + 1),
                             (-L, l + 2), (-L - 3, l + 2)]
                        words.add(canon(turn_word(V)))
                        cases.append((V, (-L - 1, l), (3, 2), (t + 2, H + R + 1), (l, H, w, L, R)))
    run_family("adjacent-mouth family r=2/3", cases)
    print("  adjacent rooms: canonical words %s (adjacent key: %s)"
          % (sorted(words), words == {ADJ_KEY}))


def part_d():
    print("\nPart D: structural check of the 'first outstanding area' claim (no rays)")
    # aligned chain: chambers of width wi and height 3 (floor 0), unit necks at 1<y<2
    for (w0, w1, w2, X, Y) in ((3, 1, 3, 1, 1), (2, 2, 2, 1, 2), (3, 3, 3, 1, 1)):
        s1 = w0 + X
        s2 = s1 + w1 + Y
        E = s2 + w2
        V = [(0, 0), (w0, 0), (w0, 1), (s1, 1), (s1, 0), (s1 + w1, 0), (s1 + w1, 1),
             (s2, 1), (s2, 0), (E, 0), (E, 3), (s2, 3), (s2, 2), (s1 + w1, 2),
             (s1 + w1, 3), (s1, 3), (s1, 2), (w0, 2), (w0, 3), (0, 3)]
        area = check_simple(V)
        marks = [(x, y) for x in range(1, E) for y in (1, 2) if interior(V, (x, y))]
        print("  chambers %dx3, %dx3, %dx3, necks %d,%d: area %s, word key %s, lattice marks %d"
              % (w0, w1, w2, X, Y, area, canon(turn_word(V)) == OPP_KEY, len(marks)))


if __name__ == '__main__':
    part_a()
    part_b()
    part_c()
    part_d()
    print("\nCPU seconds: %.1f" % (time.process_time() - T0))
