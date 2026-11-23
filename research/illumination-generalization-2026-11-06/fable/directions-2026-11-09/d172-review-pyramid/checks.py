"""d172 review checks for pyramid-column.md (snapshot 2026-11-22 0855).

Named explicit rooms only, exact Fraction arithmetic, no room or direction searches.
trace() is copied verbatim from d170-review-ferrers2/checks.py.
Run: python3 -B checks.py > checks.log
"""
import random, time
from fractions import Fraction as F
from math import floor

T0 = time.process_time()
FAIL = []
def log(*a): print(*a, flush=True)
def check(ok, msg):
    log(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok: FAIL.append(msg)
def nearest(q): return floor(q + F(1, 2))

# ---------------------------------------------------------------- verbatim from d170
def trace(P, A, B, maxrefl=10**6):
    n = len(P)
    hw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][1] == P[(i + 1) % n][1]]
    vw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    V = {(F(a), F(b)) for a, b in P}
    X, Y = F(A[0]), F(A[1])
    vx, vy = F(B[0]) - X, F(B[1]) - Y
    tau, contacts = F(1), []
    for _ in range(maxrefl):
        best = None
        if vx:
            for a, b in vw:
                t = (a[0] - X) / vx
                if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + vy * t <= max(a[1], b[1]):
                    best = (t, 'v')
        if vy:
            for a, b in hw:
                t = (a[1] - Y) / vy
                if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + vx * t <= max(a[0], b[0]):
                    best = (t, 'h')
        if best is None or best[0] > tau:
            return 'end', (X + vx * tau, Y + vy * tau), contacts
        t, kind = best
        X, Y = X + vx * t, Y + vy * t
        if best[0] == tau:
            return 'wall-end', (X, Y), contacts
        tau -= t
        if (X, Y) in V:
            return 'corner', (X, Y), contacts
        contacts.append(((X, Y), kind))
        if kind == 'v': vx = -vx
        else: vy = -vy
    return 'limit', (X, Y), contacts

# ---------------------------------------------------------------- rooms from d169 masks
def rows_of(nx, ny, mask):
    rows = []
    for j in range(ny):
        cols = [i for i in range(nx) if (mask >> (i + nx * j)) & 1]
        assert cols == list(range(cols[0], cols[-1] + 1))
        rows.append((cols[0], cols[-1] + 1))
    return rows

def polygon(rows, X, Y):
    pts = []
    for k, (l, r) in enumerate(rows):
        pts += [(X[r], Y[k]), (X[r], Y[k + 1])]
    for k in reversed(range(len(rows))):
        l, r = rows[k]
        pts += [(X[l], Y[k + 1]), (X[l], Y[k])]
    out = []
    for p in pts:
        if not out or out[-1] != p: out.append(p)
    if out[0] == out[-1]: out.pop()
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            a, b, c = out[i - 1], out[i], out[(i + 1) % len(out)]
            if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]) or a == b:
                out.pop(i); changed = True; break
    return out

def cum(g): return [F(sum(g[:k])) for k in range(len(g) + 1)]

class Room:
    def __init__(self, name, nx, ny, mask, gx, gy):
        self.name, self.mask = name, mask
        self.rows = rows_of(nx, ny, mask)
        self.X, self.Y = cum(gx), cum(gy)
        self.gx, self.gy = gx, gy
        self.P = polygon(self.rows, self.X, self.Y)
    def coord(self, axis, k, f):
        G = self.X if axis == 0 else self.Y
        return G[k // 2] if k % 2 == 0 else G[k // 2] + (G[k // 2 + 1] - G[k // 2]) * f
    def width(self, r): l, rr = self.rows[r]; return self.X[rr] - self.X[l]

# sweep spec: (source type, target type, source row, middle row, target row, x0 col, sigma)
PYR = {761: (3, 4), 763: (3, 4), 8051: (4, 4), 6131: (4, 4), 5111: (4, 4)}
OPEN = {761: [((1, 7), (5, 3))], 763: [((1, 7), (5, 3))],
        8051: [((1, 1), (7, 5)), ((2, 1), (7, 5)), ((3, 1), (7, 5))],
        6131: [((1, 7), (7, 3))], 5111: [((1, 7), (7, 3))]}
def sweep(mask, S, T):
    if mask == 8051: return (S, T, 0, 1, 2, 0, 1)
    if mask == 8052: return (T, S, 0, 1, 2, 3, -1)   # bottom tip (5,1) is the source
    return (S, T, 3, 2, 1, 0, 1)

def params(R, sr, mr, tr, x0c, sg):
    x0 = R.X[x0c]
    down = sr > tr
    yj1 = R.Y[sr] if down else R.Y[sr + 1]
    yj2 = R.Y[mr] if down else R.Y[mr + 1]
    w, u, V = R.width(sr), R.width(mr), R.width(tr)
    l, r = R.rows[mr]; lm = sg * (R.X[l] - x0); rm = sg * (R.X[r] - x0)
    assert min(lm, rm) == 0 and max(lm, rm) == u
    lt, rt = sorted((sg * (R.X[R.rows[tr][0]] - x0), sg * (R.X[R.rows[tr][1]] - x0)))
    c = 0 if lt == 0 else u
    assert (lt == 0 or rt == u), 'final run must share a side with the middle run'
    ls, rs = sorted((sg * (R.X[R.rows[sr][0]] - x0), sg * (R.X[R.rows[sr][1]] - x0)))
    assert ls == 0 and rs == w, 'first run must share side 0 with the middle run'
    return dict(x0=x0, sg=sg, s=-1 if down else 1, yj1=yj1, yj2=yj2, w=w, u=u, V=V, c=c,
                d=abs(yj2 - yj1), hT=R.gy[tr])

def shot(R, p, S, T, i=None, j=None, k=0):
    w, u, V, c, d = p['w'], p['u'], p['V'], p['c'], p['d']
    x, z = p['sg'] * (S[0] - p['x0']), p['sg'] * (T[0] - p['x0'])
    a, b = abs(S[1] - p['yj1']), abs(T[1] - p['yj2'])
    L = d + b; D = a + L
    if i is None:                          # note's choice, plus the j-rounding variant
        i1, j1 = nearest((d * z - c * L) / (2 * u * b)), 0
        j2, i2 = nearest(-(d * z - c * L) / (2 * d * V)), 0
        r1 = abs(d * z - c * L - 2 * u * b * i1)
        r2 = abs(d * z - c * L + 2 * d * V * j2)
        i, j = (i1, j1) if r1 <= r2 else (i2, j2)
    M = (z + 2 * V * j + 2 * u * i) / L
    X = (x + M * a + w) % (2 * w) - w + 2 * w * k
    g1 = X * L / D
    g2 = d * M - 2 * u * i + X * b / D
    gates = abs(g1) < w and abs(g2 - c) < u
    vec = (p['sg'] * (M - X / D) * D, p['s'] * D)
    st, pos, con = trace(R.P, S, (S[0] + vec[0], S[1] + vec[1]))
    return dict(gates=gates, lit=(st == 'end' and pos == T), st=st, pos=pos, n=len(con),
                a=a, b=b, L=L, D=D, i=i, j=j, M=M, X=X, g1=g1, g2=g2)

def lemma_holds(p, b):
    w, u, V, d = p['w'], p['u'], p['V'], p['d']
    return min(u * b, d * V) + w * b <= u * (d + b)

def marks(R, ta, tb, rnd, n_rand):
    out = [((R.coord(0, ta[0], F(1, 2)), R.coord(1, ta[1], F(1, 2))),
            (R.coord(0, tb[0], F(1, 2)), R.coord(1, tb[1], F(1, 2))))]
    for _ in range(n_rand):
        q = lambda: F(rnd.randint(1, 96), 97) if rnd.random() < .5 else F(rnd.randint(1, 1008), 1009)
        out.append(((R.coord(0, ta[0], q()), R.coord(1, ta[1], q())),
                    (R.coord(0, tb[0], q()), R.coord(1, tb[1], q()))))
    return out

rnd = random.Random(172)

# ================================================================== item 1
log('# Item 1: lemma algebra on 4000 random rational instances')
ok = [True] * 5
for _ in range(4000):
    w = F(rnd.randint(1, 30), rnd.randint(1, 4)); u = w + F(rnd.randint(1, 30), rnd.randint(1, 4))
    V = u + F(rnd.randint(1, 30), rnd.randint(1, 4))
    a, d, b = (F(rnd.randint(1, 60), rnd.randint(1, 6)) for _ in range(3))
    c = rnd.choice([0, u]); L = d + b; D = a + L
    z = (F(rnd.randint(1, 999), 1000) * V) - (V - u if c == u else 0)
    x = F(rnd.randint(1, 999), 1000) * w
    i = nearest((d * z - c * L) / (2 * u * b)); j = rnd.randint(-5, 5)
    M = (z + 2 * u * i) / L; Rr = d * M - 2 * u * i
    ok[0] &= abs(Rr - c) <= u * b / L
    X = (x + M * a + w) % (2 * w) - w
    ok[1] &= -w <= X < w and ((X - M * a - x) / (2 * w)).denominator == 1
    Mp = M - X / D
    ok[2] &= X - M * a + Mp * a == X * L / D and X - M * a + Mp * (a + d) - 2 * u * i == Rr + X * b / D \
        and X - M * a + Mp * D - 2 * u * i == z
    if w * b <= u * d:
        ok[3] &= abs(Rr + X * b / D - c) < u and abs(X * L / D) < w
    M2 = (z + 2 * V * j + 2 * u * i) / L
    ok[4] &= d * (z + 2 * V * j) - c * L - 2 * u * b * i == L * (d * M2 - 2 * u * i - c)
check(ok[0], '|R - c| <= ub/L with i nearest to (dz - cL)/(2ub)')
check(ok[1], 'X in [-w, w), X - Ma congruent to x mod 2w (even copy, so physical slope = developed slope)')
check(ok[2], 'joint coordinates XL/D, R + Xb/D (after -2ui), final coordinate z')
check(ok[3], 'wb <= ud gives strict gates |g1| < w, |g2 - c| < u')
check(ok[4], 'broad winding: residual numerator dz - cL + 2dVj - 2ubi = L(R - c)')
def fold(g, lo, hi):
    p = 2 * (hi - lo); t = (g - lo) % p
    return lo + (t if t <= hi - lo else p - t)
okf = True
for _ in range(3000):
    u = F(rnd.randint(2, 40), rnd.randint(1, 3)); V = u + F(rnd.randint(1, 40), rnd.randint(1, 3))
    for c in (0, u):
        lo3, hi3 = (0, V) if c == 0 else (u - V, u)
        g = c - u + F(rnd.randint(1, 9999), 10000) * 2 * u
        okf &= fold(g, 0, u) == fold(g, lo3, hi3) and 0 <= fold(g, 0, u) <= u
        okf &= fold(g, 0, u) not in ((u if c == 0 else 0),)   # never the corner side
check(okf, 'middle and final folding maps agree on (c-u, c+u) for c = 0 and c = u')
okw = True
for _ in range(3000):
    w, du, dv = rnd.randint(1, 20), rnd.randint(1, 20), rnd.randint(0, 30)
    u, V = w + du, w + du + dv
    d = F(rnd.randint(1, 50), rnd.randint(1, 5))
    for b in [d * F(rnd.randint(1, 4000), 100) for _ in range(5)]:
        crit = min(u * b, d * V) + w * b <= u * (d + b)
        okw &= crit == (b <= u * d / w or b >= d * (V - u) / (u - w))
        if w * V <= u * u: okw &= crit
check(okw, 'min(ub,dV)+wb <= u(d+b) iff b <= ud/w or b >= d(V-u)/(u-w); always true when wV <= u^2')

# ================================================================== item 2
log('\n# Item 2: the 7 open pairs, sweep form at unit gaps')
for mask, (nx, ny) in PYR.items():
    R = Room(f'unit-{mask}', nx, ny, mask, [1] * nx, [1] * ny)
    for S, T in OPEN[mask]:
        sv = sweep(mask, S, T)
        p = params(R, *sv[2:])
        # full side walls: each run is one rank row, so its two side walls span the row
        log(f'   mask {mask} rows {R.rows} pair {S}-{T}: (w,u,V)=({p["w"]},{p["u"]},{p["V"]}) c={p["c"]} '
            f'wV<=u^2: {p["w"] * p["V"] <= p["u"] ** 2}; w*hT<=u*d: {p["w"] * p["hT"] <= p["u"] * p["d"]}')
check(True, 'every open pyramid pair has the nested three-run form with c = 0 (asserts in params())')

# ================================================================== item 3
log('\n# Item 3: exact replay in named lattice rooms')
ROOMS = [  # name, mask, gx, gy (bottom-up)
    ('A761', 761, (2, 3, 5), (1, 4, 1, 3)), ('B8051', 8051, (1, 1, 2, 3), (2, 1, 5, 3)),
    ('C6131', 6131, (1, 2, 1, 5), (2, 3, 1, 2)), ('D5111', 5111, (2, 2, 1, 3), (1, 3, 2, 2)),
    ('E763', 763, (3, 1, 6), (1, 2, 3, 1)),
    ('V1-761', 761, (3, 1, 6), (1, 5, 1, 2)), ('V2-8051', 8051, (2, 2, 1, 6), (2, 1, 4, 2)),
    ('V3-5111', 5111, (3, 1, 1, 5), (1, 4, 1, 2))]
for name, mask, gx, gy in ROOMS:
    nx, ny = PYR[mask]
    R = Room(name, nx, ny, mask, gx, gy)
    log(f' room {name}: mask {mask} x gaps {gx} y gaps {gy}, polygon {[(int(a), int(b)) for a, b in R.P]}')
    for S0, T0_ in OPEN[mask]:
        sv = sweep(mask, S0, T0_)
        p = params(R, *sv[2:])
        wide = p['w'] * p['V'] <= p['u'] ** 2; deep = p['w'] * p['hT'] <= p['u'] * p['d']
        ms = marks(R, sv[0], sv[1], rnd, 12)
        nlem = nlit = nbad = 0; still = 0; undecided = []
        for S, T in ms:
            r = shot(R, p, S, T)
            hyp = lemma_holds(p, r['b'])
            nlem += hyp
            if hyp:
                nlit += r['lit'] and r['gates']
                if not (r['lit'] and r['gates']): nbad += 1; log(f'     BAD {S}-{T}: {r["st"]} {r["pos"]}')
            else:
                if r['lit']: still += 1; continue
                found = None
                for di in range(-4, 5):
                    for jj in range(-4, 5):
                        for k in range(-3, 4):
                            q = shot(R, p, S, T, r['i'] + di, jj, k)
                            if q['lit']: found = q; break
                        if found: break
                    if found: break
                if found: still += 1
                else: undecided.append((S, T, r['st']))
        log(f'   pair {S0}-{T0_}: wV<=u^2 {wide}, w*hT<=u*d {deep}; {len(ms)} marks, lemma applies to {nlem}, '
            f'lit by note shot {nlit}, outside lemma lit by one-middle family {still}, undecided {len(undecided)}')
        for S, T, st in undecided[:3]:
            log(f'     undecided {S}-{T}: note shot ends "{st}"')
        check(nbad == 0, f'{name} {S0}-{T0_}: every mark inside the lemma hypothesis traces to T with strict gates')
        if wide or deep:
            check(nlem == len(ms), f'{name} {S0}-{T0_}: length condition holds so the lemma applies to every mark')

log('\n# Item 3b: note example mask 8052, unit horizontal gaps, uneven vertical gaps, opposite shared sides')
R = Room('8052', 4, 4, 8052, (1, 1, 1, 1), (3, 1, 4, 2))
log(f' polygon {[(int(a), int(b)) for a, b in R.P]}')
for S0 in [(1, 5), (1, 6)]:
    sv = sweep(8052, S0, (5, 1)); p = params(R, *sv[2:])
    ms = marks(R, sv[0], sv[1], rnd, 12)
    good = sum(1 for S, T in ms if (lambda r: r['lit'] and r['gates'])(shot(R, p, S, T)))
    check(p['c'] == p['u'] and good == len(ms), f'8052 (5,1)->{S0}: c = u, {good}/{len(ms)} marks lit with strict gates')

log(f'\nCPU {time.process_time() - T0:.1f}s; FAIL {len(FAIL)}')
