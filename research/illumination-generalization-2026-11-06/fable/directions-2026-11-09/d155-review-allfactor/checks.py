"""d155 checks for all-factor-first-shot (snapshot 2026-11-22 03:45).

Exact integer / Fraction arithmetic. Named rooms only. No searches over rooms.
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as Fr
from math import gcd
from itertools import product

# ---------------------------------------------------------------- geometry
def area2(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1]
               for i in range(len(P)))

def ccw(P):
    return P if area2(P) > 0 else P[::-1]

def angles(P):
    """interior angle of each vertex in units of pi/4 (P ccw)."""
    import math
    out = []
    n = len(P)
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        u = (a[0] - b[0], a[1] - b[1]); v = (c[0] - b[0], c[1] - b[1])
        # angle from v to u counterclockwise = interior angle for ccw polygon
        t = math.atan2(u[1], u[0]) - math.atan2(v[1], v[0])
        t %= 2 * math.pi
        k = round(t / (math.pi / 4)); assert abs(t - k * math.pi / 4) < 1e-9
        out.append(k)
    return out

def on_seg(p, a, b):
    cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    if cr != 0: return False
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def locate(p, P):
    """'v' vertex, 'b' boundary, 'i' interior, 'o' outside."""
    n = len(P)
    for v in P:
        if v[0] == p[0] and v[1] == p[1]: return 'v'
    for i in range(n):
        if on_seg(p, P[i], P[(i + 1) % n]): return 'b'
    x, y = p; ins = False
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + Fr(y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x: ins = not ins
    return 'i' if ins else 'o'

def content(P):
    g = 0
    for v in P:
        g = gcd(g, gcd(v[0] - P[0][0], v[1] - P[0][1]))
    return g

# ---------------------------------------------------------------- lattices
def hnf(vecs):
    """HNF basis [[a,b],[0,d]] (rows (a,b),(0,d)) of integer span in Z^2."""
    rows = [list(v) for v in vecs if v != (0, 0)]
    # column 0 gcd via Euclid
    a_row = None
    rest = []
    for r in rows:
        if a_row is None:
            a_row = r; continue
        while r[0] != 0:
            q = a_row[0] // r[0]
            a_row = [a_row[0] - q * r[0], a_row[1] - q * r[1]]
            a_row, r = r, a_row
        rest.append(r)
    if a_row[0] < 0: a_row = [-a_row[0], -a_row[1]]
    d = 0
    for r in rest: d = gcd(d, r[1])
    d = abs(d)
    return (a_row[0], a_row[1] % d if d else a_row[1], d)

def covol(L): return L[0] * L[2]

def in_lat(v, L):
    a, b, d = L
    if v[0] % a: return False
    k = v[0] // a
    return (v[1] - k * b) % d == 0

def superlattices(L):
    """all integer lattices containing L (finite)."""
    out = set()
    a, b, d = L
    for a2 in range(1, a + 1):
        if a % a2: continue
        for d2 in range(1, d + 1):
            if d % d2: continue
            for b2 in range(d2):
                G = (a2, b2, d2)
                if in_lat((a, b), G) and in_lat((0, d), G): out.add(G)
    return sorted(out, key=covol)

# ---------------------------------------------------------------- unfolding
D4 = [((1, 0), (0, 1)), ((-1, 0), (0, -1)), ((1, 0), (0, -1)), ((-1, 0), (0, 1)),
      ((0, 1), (1, 0)), ((0, -1), (-1, 0)), ((0, -1), (1, 0)), ((0, 1), (-1, 0))]

def mm(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def mv(A, v): return (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])

def refl(e):
    dx, dy = e
    if dy == 0: return ((1, 0), (0, -1))
    if dx == 0: return ((-1, 0), (0, 1))
    if dx == dy: return ((0, 1), (1, 0))
    if dx == -dy: return ((0, -1), (-1, 0))
    raise ValueError

def unfold(P):
    n = len(P)
    walls = []
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        R = refl((b[0] - a[0], b[1] - a[1]))
        Ra = mv(R, a)
        walls.append((R, (a[0] - Ra[0], a[1] - Ra[1])))
    I = ((1, 0), (0, 1))
    t = {I: (0, 0)}; queue = [I]
    lam = []
    while queue:
        h = queue.pop(0)
        for R, s in walls:
            h2 = mm(h, R); hs = mv(h, s)
            tv = (hs[0] + t[h][0], hs[1] + t[h][1])
            if h2 not in t:
                t[h2] = tv; queue.append(h2)
            else:
                lam.append((tv[0] - t[h2][0], tv[1] - t[h2][1]))
    Labs = hnf(lam)
    dev = {(h, i): (mv(h, P[i])[0] + t[h][0], mv(h, P[i])[1] + t[h][1]) for h in t for i in range(n)}
    base = dev[(I, 0)]
    Lrel = hnf(lam + [(p[0] - base[0], p[1] - base[1]) for p in dev.values()])
    return t, Labs, Lrel

def coset_points(P, h, t, x, G):
    """points p in closed P with h p + t = x mod G (x may be Fraction)."""
    hinv = tuple(tuple(h[j][i] for j in range(2)) for i in range(2))  # orthogonal
    xs = [v[0] for v in P]; ys = [v[1] for v in P]
    a, b, d = G
    # lattice h^{-1} G generated by h^{-1}(a,b), h^{-1}(0,d); point base = h^{-1}(x - t)
    g1 = mv(hinv, (a, b)); g2 = mv(hinv, (0, d))
    base = mv(hinv, (x[0] - t[0], x[1] - t[1]))
    R = max(max(xs) - min(xs), max(ys) - min(ys)) + 2 * (a + d + abs(b)) + 2
    out = []
    N = R + 2
    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            p = (base[0] + i * g1[0] + j * g2[0], base[1] + i * g1[1] + j * g2[1])
            if min(xs) <= p[0] <= max(xs) and min(ys) <= p[1] <= max(ys):
                loc = locate(p, P)
                if loc != 'o': out.append((p, loc))
    return out

def site_analysis(P, G, t):
    n = len(P); ang = angles(P); W = n
    A = Fr(area2(P), 2)
    V = covol(G)
    deg = 8 * A / V
    # generic degree count
    gx = (Fr(1, 7), Fr(2, 13))
    cnt = sum(1 for h in t for (_, loc) in coset_points(P, h, t[h], gx, G) if loc == 'i')
    def red(v):
        a, b, d = G
        k = v[0] // a if isinstance(v[0], int) else None
        x0 = v[0] % a; k = (v[0] - x0) // a
        y = (v[1] - k * b) % d
        return (x0, y)
    cand = set()
    for h in t:
        for i in range(n):
            p = mv(h, P[i]); cand.add(red((p[0] + t[h][0], p[1] + t[h][1])))
    clean = []
    for x in sorted(cand):
        ok = True; Dx = Fr(0)
        for h in t:
            for p, loc in coset_points(P, h, t[h], x, G):
                if loc != 'v': ok = False; break
                Dx += Fr(ang[P.index(p)], 8)
            if not ok: break
        if ok:
            clean.append((x, Dx))
    return A, V, deg, cnt, clean

# ---------------------------------------------------------------- rooms
rooms = {
    'B (V-notch)': [(0, 0), (4, 0), (4, 4), (2, 2), (0, 4)],
    'B/2': [(0, 0), (2, 0), (2, 2), (1, 1), (0, 2)],
    'F^-1(B/2)': [(0, 0), (1, -1), (2, 0), (1, 0), (1, 1)],
    'M (d138)': [(0, 0), (3, 0), (4, 1), (4, 2), (2, 4), (0, 4)],
    'A (d135)': [(0, 0), (2, 0), (2, 1), (1, 2), (0, 2)],
    'C (d135)': [(0, 0), (4, 0), (4, 2), (3, 2), (2, 3), (2, 4), (0, 4)],
    'D (d135)': [(0, 0), (4, 0), (4, 4), (3, 4), (2, 3), (2, 4), (0, 4)],
    'R2 (d139)': [(1, 0), (4, 0), (4, 2), (2, 2), (1, 3), (1, 4), (0, 4), (0, 1)],
    'R3 (d139)': [(0, 0), (2, 0), (2, 1), (3, 1), (4, 2), (4, 4), (1, 4), (0, 3)],
    'C1 (d139)': [(0, 0), (3, 0), (3, 1), (2, 2), (0, 2)],
    'C2 (d139)': [(0, 0), (2, 0), (2, 2), (1, 3), (0, 2)],
    'hexagon (d138)': [(0, 0), (2, 0), (3, 1), (2, 2), (0, 2), (-1, 1)],
}

print("# 1. Clean-site area bound on named mixed rooms")
print("Bound under test: d*|J| <= 4(W-2), i.e. area <= V(W-2)/(2|J|); and V <= 8 when content = 1.")
print("For each room, every lattice Gamma between Lambda_abs and Z^2 is tested (finite list).")
for name, P in rooms.items():
    P = ccw(P)
    W = len(P); ang = angles(P)
    assert sum(ang) == 4 * (W - 2)
    t, Labs, Lrel = unfold(P)
    assert len(t) == 8
    c = content(P)
    # half-turn lemma: 2 Lrel in Labs
    a, b, d = Lrel
    ht = in_lat((2 * a, 2 * b), Labs) and in_lat((0, 2 * d), Labs)
    print(f"\n## {name}: W={W}, angles(pi/4)={ang}, content={c}, area={Fr(area2(P), 2)}")
    print(f"   Lambda_abs HNF={Labs} covol={covol(Labs)}; Lambda_rel HNF={Lrel} covol={covol(Lrel)}; 2*Lrel in Labs: {ht}")
    for G in superlattices(Labs):
        A, V, deg, cnt, clean = site_analysis(P, G, t)
        J = len(clean)
        okdeg = (deg == cnt)
        okD = all(Dx == deg for _, Dx in clean)
        bound = Fr(V * (W - 2), 2 * J) if J else None
        flag = ''
        if J:
            assert deg * J <= 4 * (W - 2), (name, G)
            flag = ' EQUALITY' if deg * J == 4 * (W - 2) else ''
        print(f"   Gamma={G} V={V} deg={deg} (generic count {cnt}, match {okdeg}) clean sites J={J}"
              + (f" at {[x for x, _ in clean]}, D_x=deg for all: {okD}, area {A} <= bound {bound}{flag}" if J else ""))
        assert okdeg

print("\n# 2. Axis span <= area + 1")
def span(P):
    xs = [v[0] for v in P]; ys = [v[1] for v in P]
    return max(xs) - min(xs), max(ys) - min(ys)
for name, P in rooms.items():
    A = Fr(area2(ccw(P)), 2); sx, sy = span(P)
    print(f"   {name}: spans ({sx},{sy}), area {A}, max span - area = {max(sx, sy) - A}, holds: {max(sx, sy) <= A + 1}")
for L in (3, 10, 40):
    P = [(0, 0), (1, 0), (L, L - 1), (L, L)]
    A = Fr(area2(P), 2); ang = angles(ccw(P))
    print(f"   diagonal strip L={L} {P}: angles {ang}, area {A}, span {L}, span-area = {L - A} (bound allows 1)")
W = 20
print(f"   W=20, J=1, V<=8: area <= {Fr(8 * (W - 2), 2)}, span <= {1 + 8 * (W - 2) // 2}")
print(f"   W=20, J=1, V<=4 (c=1 normalization after F^-1): area <= {Fr(4 * (W - 2), 2)}, span <= {1 + 4 * (W - 2) // 2}")
print(f"   higher-genus line: floor((3W-8)/2)*4(W-2) = {((3 * W - 8) // 2) * 4 * (W - 2)}")

# ---------------------------------------------------------------- dumbbell
print("\n# 3. Dumbbell: bounded-|p| directions all stop at the lower doorway lip (U,2)")
def lcm(a, b): return a * b // gcd(a, b)

def trace(P, S, d, T, maxsteps):
    """exact billiard in orthogonal polygon; returns (event, point, steps)."""
    n = len(P)
    p = (Fr(S[0]), Fr(S[1])); dx, dy = Fr(d[0]), Fr(d[1])
    for step in range(maxsteps):
        best = None
        for i in range(n):
            a, b = P[i], P[(i + 1) % n]
            if a[1] == b[1]:  # horizontal wall
                if dy == 0: continue
                s = (a[1] - p[1]) / dy
                if s <= 0: continue
                x = p[0] + s * dx
                if min(a[0], b[0]) <= x <= max(a[0], b[0]):
                    if best is None or s < best[0]: best = (s, 'h', (x, Fr(a[1])))
            else:
                if dx == 0: continue
                s = (a[0] - p[0]) / dx
                if s <= 0: continue
                y = p[1] + s * dy
                if min(a[1], b[1]) <= y <= max(a[1], b[1]):
                    if best is None or s < best[0]: best = (s, 'v', (Fr(a[0]), y))
        s, kind, q = best
        # target on the open segment?
        if dx != 0:
            st = (T[0] - p[0]) / dx
        else:
            st = (T[1] - p[1]) / dy
        if 0 < st <= s and p[0] + st * dx == T[0] and p[1] + st * dy == T[1]:
            return ('target', (T[0], T[1]), step)
        if any(q[0] == v[0] and q[1] == v[1] for v in P):
            return ('corner', q, step)
        # a horizontal and vertical wall at the same parameter means a corner; handled above
        if kind == 'h': dy = -dy
        else: dx = -dx
        p = q
    return ('limit', p, maxsteps)

for Bb in (1, 2, 3):
    M = 1
    for k in range(1, Bb + 1): M = lcm(M, k)
    a = 10 * M; U = 2 * a
    P = [(0, 0), (U, 0), (U, 2), (U + 2, 2), (U + 2, 0), (2 * U + 3, 0), (2 * U + 3, 5),
         (U + 2, 5), (U + 2, 3), (U, 3), (U, 5), (0, 5)]
    A = Fr(area2(P), 2)
    S = (U - a, 2); T = (U + 2 + a, 2)
    refl_count = sum(1 for k in angles(ccw(P)) if k > 4)
    hg = 0; vg = 0
    for i in range(len(P)):
        e = (P[(i + 1) % 12][0] - P[i][0], P[(i + 1) % 12][1] - P[i][1])
        hg = gcd(hg, e[0]); vg = gcd(vg, e[1])
    print(f"\n## b={Bb}: a={a}, U={U}, W={len(P)}, area={A} (20a+7={20 * a + 7}), reflexes={refl_count}, "
          f"axis gcds=({hg},{vg}), S={S} {locate(S, P)}, T={T} {locate(T, P)}")
    tested = 0; bad = []
    Q = 40
    dirs = [(p, q) for p in range(-Bb, Bb + 1) for q in range(-Q, Q + 1) if p != 0 and gcd(abs(p), abs(q)) == 1]
    for d in dirs:
        ev, pt, st = trace(P, S, d, T, 20000)
        tested += 1
        if not (ev == 'corner' and pt == (U, 2)): bad.append((d, ev, pt))
    print(f"   {tested} primitive directions with 1<=|p|<={Bb}, |q|<={Q}: all stop at (U,2): {not bad} {bad[:3]}")
    for d in [(0, 1), (0, -1)]:
        ev, pt, st = trace(P, S, d, T, 50)
        print(f"   vertical {d}: {ev} at {pt}")
    ev, pt, st = trace(P, S, (a + 1, 1), T, 50)
    print(f"   witness (a+1,1)=({a + 1},1): {ev} after {st} reflections")

print("\nDone.")
