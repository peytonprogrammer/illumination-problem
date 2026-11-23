"""d203 referee checks for snapshot.md (aligned three-chamber rooms).

Standard library only, exact integer/rational arithmetic. Every ray traced
here comes from a construction in the note (closed-form slope, one modular
solve, or a solution of the note's group-ring test). No ray, direction, word
or room-size search.
"""
import json
import os
import sys
import time
from fractions import Fraction as Fr
from itertools import product
from math import gcd

T0 = time.process_time()
HERE = os.path.dirname(os.path.abspath(__file__))


def lcm(*a):
    r = 1
    for x in a:
        r = r * x // gcd(r, x)
    return r


# ---------------------------------------------------------------- rooms
class Room:
    def __init__(self, verts):
        self.verts = verts
        self.vset = set(verts)
        self.v, self.h = [], []
        n = len(verts)
        for i in range(n):
            (x1, y1), (x2, y2) = verts[i], verts[(i + 1) % n]
            if x1 == x2:
                self.v.append((x1, min(y1, y2), max(y1, y2)))
            else:
                self.h.append((y1, min(x1, x2), max(x1, x2)))


def aligned(ws, bs, ts, Ls):
    """Chambers [l_i, l_i+w_i] x [-b_i, 1+t_i]; unit necks at 0<y<1."""
    w1, w2, w3 = ws
    l = [0, w1 + Ls[0], w1 + Ls[0] + w2 + Ls[1]]
    P = l[2] + w3
    b, t = bs, ts
    V = [(0, -b[0]), (w1, -b[0]), (w1, 0), (l[1], 0), (l[1], -b[1]),
         (l[1] + w2, -b[1]), (l[1] + w2, 0), (l[2], 0), (l[2], -b[2]),
         (P, -b[2]), (P, 1 + t[2]), (l[2], 1 + t[2]), (l[2], 1),
         (l[1] + w2, 1), (l[1] + w2, 1 + t[1]), (l[1], 1 + t[1]), (l[1], 1),
         (w1, 1), (w1, 1 + t[0]), (0, 1 + t[0])]
    R = Room(V)
    R.ws, R.bs, R.ts, R.Ls, R.l, R.P = list(ws), list(bs), list(ts), list(Ls), l, P
    R.seams = [w1, l[1], l[1] + w2, l[2]]
    R.necks = [(w1, l[1]), (l[1] + w2, l[2])]
    R.area = sum(w * (bb + 1 + tt) for w, bb, tt in zip(ws, bs, ts)) + sum(Ls)
    return R


def flipped(R):
    """Vertical reflection y -> 1-y (swaps floors and roofs)."""
    return aligned(R.ws, R.ts, R.bs, R.Ls)


def marks(R):
    out = []
    for i in range(3):
        for x in range(R.l[i] + 1, R.l[i] + R.ws[i]):
            for y in range(-R.bs[i] + 1, R.ts[i] + 1):
                out.append((i, x, y))
    return out


# ---------------------------------------------------------------- tracer
def trace(R, S, T, slope, sx, sy, maxb=200000, record=False):
    """Trace from lattice S with |dx|:|dy| = slope.numerator... given as
    (DX, DY) positive ints, signs sx, sy. Exact integer arithmetic in
    coordinates scaled by Q = DX*DY. Returns (status, bounces, segs)."""
    DX, DY = slope
    g = gcd(DX, DY)
    DX, DY = DX // g, DY // g
    Q = DX * DY
    px, py = S[0] * Q, S[1] * Q
    tx, ty = T[0] * Q, T[1] * Q
    V = [(X * Q, a * Q, b * Q) for X, a, b in R.v]
    H = [(Y * Q, a * Q, b * Q) for Y, a, b in R.h]
    vset = {(x * Q, y * Q) for x, y in R.vset}
    segs = [] if record else None
    bounces = []
    for k in range(maxb):
        best = None  # (num, den, kind)
        for X, a, b in V:
            d = X - px
            if d * sx <= 0:
                continue
            num = abs(d)
            if best is not None and num * best[1] > best[0] * DX:
                continue
            yy = DY * num
            if yy % DX:
                raise ValueError("non-integral hit")
            yh = py + sy * (yy // DX)
            if a <= yh <= b:
                if best is not None and num * best[1] == best[0] * DX:
                    best = (num, DX, 'c')
                else:
                    best = (num, DX, 'v')
        for Y, a, b in H:
            d = Y - py
            if d * sy <= 0:
                continue
            num = abs(d)
            if best is not None and num * best[1] > best[0] * DY:
                continue
            xx = DX * num
            if xx % DY:
                raise ValueError("non-integral hit")
            xh = px + sx * (xx // DY)
            if a <= xh <= b:
                if best is not None and num * best[1] == best[0] * DY:
                    best = (num, DY, 'c')
                else:
                    best = (num, DY, 'h')
        # target on this segment?
        dtx, dty = tx - px, ty - py
        if dtx * sx > 0 and dty * sy > 0 and abs(dtx) * DY == abs(dty) * DX:
            st = abs(dtx)  # parameter num with den DX
            if st * best[1] <= best[0] * DX:
                if record:
                    segs.append(((px, py), (tx, ty)))
                return 'hit', bounces, (segs, Q)
        num, den, kind = best
        if den == DX:
            nx = px + sx * num
            ny = py + sy * (DY * num // DX)
        else:
            ny = py + sy * num
            nx = px + sx * (DX * num // DY)
        if record:
            segs.append(((px, py), (nx, ny)))
        if kind == 'c' or (nx, ny) in vset:
            return 'corner', bounces, (segs, Q)
        bounces.append((kind, Fr(nx, Q), Fr(ny, Q)))
        px, py = nx, ny
        if kind == 'v':
            sx = -sx
        else:
            sy = -sy
    return 'maxb', bounces, (segs, Q)


def slope_of(c):
    """horizontal per unit vertical c (Fraction>0) -> (DX, DY)."""
    c = Fr(c)
    return (c.numerator, c.denominator)


LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s)
    print(s)
    sys.stdout.flush()


def fold(xx, P):
    r = xx % (2 * P)
    return r if r <= P else 2 * P - r


def minpos_m(M, K, P):
    """least positive m with M m = K (mod 2P), or None."""
    N = 2 * P
    g = gcd(M, N)
    if K % g:
        return None
    m0 = ((K // g) * pow(M // g, -1, N // g)) % (N // g)
    return m0 if m0 > 0 else N // g


# ---------------------------------------------------------------- note constructions
def opp_construction(R, S, T):
    """S lower (y<=0), T upper (y>=1), different chambers. Returns c or None."""
    (i, xS, yS), (j, xT, yT) = S, T
    a, b = -yS, yT - 1
    P = R.P
    M = lcm(2 * R.ws[i], 2 * R.ws[j])
    g = gcd(M, 2 * P)
    r = (xT - xS) % g
    for d in sorted({r, r - g}, key=abs):
        eta = Fr(d, a + 1 + b)
        if R.l[i] < xS + a * eta < R.l[i] + R.ws[i] and R.l[j] < xT - b * eta < R.l[j] + R.ws[j]:
            m = minpos_m(M, xT - xS - d, P)
            c = M * m + eta
            if c > 0:
                return c, a + 1 + b
    return None


def chamber_at(R, x):
    for k in range(3):
        if R.l[k] < x < R.l[k] + R.ws[k]:
            return k
    return None


def same_construction(R, S, T):
    """both lower, opposite parity, coprime. Returns c, total vertical travel."""
    (i, xS, yS), (j, xT, yT) = S, T
    a, b = -yS, -yT
    P = R.P
    D = xT - xS
    assert D % 2
    d = 1 if D % 4 == 1 else -1
    K = (D - d) // 2
    assert K % 2 == 0
    M = 2 * lcm(*R.ws)
    z = xS + K
    mid = fold(Fr(2 * z + d, 2), P)
    k = chamber_at(R, mid)
    h = R.ts[k] if k is not None else 0
    eta = Fr(d, a + 2 + 2 * h + b)
    m = minpos_m(M, K, P)
    return M * m + eta, a + 2 + 2 * h + b, h


def zero_roots(R, xS, xT):
    P = R.P
    out = []
    for X, sx in ((xS, 1), (-xS, -1)):
        for Y in (xT, -xT):
            for z in range(2 * P):
                if (2 * z - X - Y) % (2 * P) == 0 and (z - X) % 2 == 0:
                    out.append((X, sx, Y, z))
    return out


def zero_construction(R, S, T):
    (i, xS, yS), (j, xT, yT) = S, T
    P = R.P
    bad = set(R.seams) | {0, P}
    M = 2 * lcm(*R.ws)
    for X, sx, Y, z in zero_roots(R, xS, xT):
        if fold(z, P) in bad:
            continue
        K = z - X
        m = minpos_m(M, K, P)
        if m is None:
            continue
        k = chamber_at(R, fold(z, P))
        h = R.ts[k] if k is not None else 0
        return M * m, sx, -yS + 2 + 2 * h - yT
    return None


def run_pair(R, S, T, stats, tag):
    """Apply the note's coprime-theorem constructions to one lattice pair."""
    (i, xS, yS), (j, xT, yT) = S, T
    if i == j:
        return 'same-chamber'
    RR, SS, TT = R, S, T
    if (yS <= 0) != (yT <= 0):
        if yS >= 1:
            SS, TT = T, S
        res = opp_construction(RR, SS, TT)
        cls = 'opp'
        if res is None:
            stats.setdefault('opp-none', []).append((S, T))
            return 'none'
        c, Vtrav = res
        sx = 1
    else:
        if yS >= 1:
            RR = flipped(R)
            SS, TT = (i, xS, 1 - yS), (j, xT, 1 - yT)
        if (xS - xT) % 2:
            c, Vtrav, h = same_construction(RR, SS, TT)
            sx, cls = 1, 'same-odd'
        else:
            if RR.P % 2 == 0:
                return 'not-applicable'
            res = zero_construction(RR, SS, TT)
            if res is None:
                stats.setdefault('zero-exception', []).append((S, T))
                return 'exception'
            c, sx, Vtrav = res
            cls = 'zero'
    st, bl, _ = trace(RR, SS[1:], TT[1:], slope_of(c), sx, 1)
    key = (tag, cls, st)
    stats[key] = stats.get(key, 0) + 1
    stats.setdefault('maxbounce', 0)
    stats['maxbounce'] = max(stats['maxbounce'], len(bl))
    if st != 'hit':
        stats.setdefault('fail', []).append((tag, cls, S, T, c))
    return cls + ':' + st


# ---------------------------------------------------------------- group-ring test
def solve_lin(eqs):
    """n*d = e mod N for all (d, e, N); return (n0, period) or None."""
    n0, per = 0, 1
    for d, e, N in eqs:
        # need n = n0 + per*t with (n0+per*t) d = e mod N
        A, Bv = (per * d) % N, (e - n0 * d) % N
        g = gcd(A, N)
        if Bv % g:
            return None
        if A % N == 0:
            continue
        t0 = ((Bv // g) * pow(A // g, -1, N // g)) % (N // g)
        n0 = n0 + per * t0
        per = per * (N // g)
        n0 %= per
    return n0, per


def J_enum(pieces, gates, x0, xs):
    s = len(pieces)
    D = sum(p[0] for p in pieces)
    sols = []
    ranges = [range(D * a + 1, D * b) for a, b in gates]
    for eps in product((1, -1), repeat=s + 1):
        for zs in product(*ranges):
            z = [D * x0] + list(zs) + [D * xs]
            eqs = []
            for j in range(1, s + 1):
                d, f, B = pieces[j - 1]
                E = eps[j] * (z[j] - D * f) - eps[j - 1] * (z[j - 1] - D * f)
                eqs.append((d, E, 2 * B * D))
            r = solve_lin(eqs)
            if r is not None:
                sols.append((eps, zs, r))
    return sols, D


def J_groupring(pieces, gates, x0, xs):
    """Identity coefficient of [c] prod_i [L_i g_i](1+[g_i]+...) in Z[G]."""
    s = len(pieces)
    D = sum(p[0] for p in pieces)
    Ns = [2 * B * D for _, _, B in pieces]
    dv = [p[0] for p in pieces]
    def canon(e):
        # lexicographically least element of the coset e + <d>
        e = [e[j] % Ns[j] for j in range(s)]
        step = list(dv)
        for j in range(s):
            N = Ns[j]
            dj = step[j] % N
            if dj == 0:
                continue
            g = gcd(dj, N)
            k = (((e[j] % g) - e[j]) // g * pow(dj // g, -1, N // g)) % (N // g)
            e = [(e[i] + k * step[i]) % Ns[i] for i in range(s)]
            step = [st * (N // g) for st in step]
        return tuple(e)

    total = 0
    for eps in product((1, -1), repeat=s + 1):
        c = [0] * s
        for j in range(1, s + 1):
            f = pieces[j - 1][1]
            c[j - 1] += -eps[j] * D * f + eps[j - 1] * D * f
        c[0] += -eps[0] * D * x0
        c[s - 1] += eps[s] * D * xs
        ring = {canon(c): 1}
        for i, (a, b) in enumerate(gates, start=1):
            gcol = [0] * s
            gcol[i - 1] += eps[i]
            gcol[i] -= eps[i]
            new = {}
            for el, co in ring.items():
                for zz in range(D * a + 1, D * b):
                    e2 = canon([el[j] + zz * gcol[j] for j in range(s)])
                    new[e2] = new.get(e2, 0) + co
            ring = new
        total += ring.get(tuple([0] * s), 0)
    return total


def J_witness(pieces, gates, x0, xs):
    """Group-ring evaluation that also keeps one witness (eps, zs) per element."""
    s = len(pieces)
    D = sum(p[0] for p in pieces)
    Ns = [2 * B * D for _, _, B in pieces]
    dv = [p[0] for p in pieces]

    def canon(e):
        e = [e[j] % Ns[j] for j in range(s)]
        step = list(dv)
        for j in range(s):
            N = Ns[j]
            dj = step[j] % N
            if dj == 0:
                continue
            g = gcd(dj, N)
            k = (((e[j] % g) - e[j]) // g * pow(dj // g, -1, N // g)) % (N // g)
            e = [(e[i] + k * step[i]) % Ns[i] for i in range(s)]
            step = [st * (N // g) for st in step]
        return tuple(e)

    total, wit = 0, None
    zero = tuple([0] * s)
    for eps in product((1, -1), repeat=s + 1):
        c = [0] * s
        for j in range(1, s + 1):
            f = pieces[j - 1][1]
            c[j - 1] += -eps[j] * D * f + eps[j - 1] * D * f
        c[0] += -eps[0] * D * x0
        c[s - 1] += eps[s] * D * xs
        ring = {canon(c): (1, ())}
        for i, (a, b) in enumerate(gates, start=1):
            gcol = [0] * s
            gcol[i - 1] += eps[i]
            gcol[i] -= eps[i]
            new = {}
            for el, (co, w) in ring.items():
                for zz in range(D * a + 1, D * b):
                    e2 = canon([el[j] + zz * gcol[j] for j in range(s)])
                    if e2 in new:
                        new[e2] = (new[e2][0] + co, new[e2][1])
                    else:
                        new[e2] = (co, w + (zz,))
            ring = new
        if zero in ring:
            total += ring[zero][0]
            if wit is None:
                wit = (eps, ring[zero][1])
    if wit is None:
        return 0, D, None
    eps, zs = wit
    z = [D * x0] + list(zs) + [D * xs]
    eqs = []
    for j in range(1, s + 1):
        d, f, B = pieces[j - 1]
        eqs.append((d, eps[j] * (z[j] - D * f) - eps[j - 1] * (z[j - 1] - D * f), 2 * B * D))
    return total, D, (eps, zs, solve_lin(eqs))


def pos_at(segs, Q, T_long, axis):
    """transverse coordinate (scaled by Q) at cumulative longitudinal travel."""
    cum = 0
    tgt = T_long * Q
    for (x1, y1), (x2, y2) in segs:
        L = abs((x2 - x1) if axis == 0 else (y2 - y1))
        if cum + L >= tgt:
            frac = Fr(tgt - cum, L)
            return (y1 + (y2 - y1) * frac) if axis == 0 else (x1 + (x2 - x1) * frac)
        cum += L
    return None


def J_case(name, R, pieces, gates, S, T, axis, sy_long=1, maxtrace=12):
    """axis 0: longitudinal = x (rightward); axis 1: longitudinal = y (up)."""
    x0 = S[1] if axis == 0 else S[0]
    xs = T[1] if axis == 0 else T[0]
    sols, D = J_enum(pieces, gates, x0, xs)
    Jg = J_groupring(pieces, gates, x0, xs)
    ok = Jg == len(sols)
    nt = nh = 0
    for eps, zs, (n0, per) in sols[:maxtrace]:
        n = n0 if n0 > 0 else n0 + per
        if axis == 0:
            st, bl, (segs, Q) = trace(R, S, T, (D, n), 1, eps[0], record=True)
        else:
            st, bl, (segs, Q) = trace(R, S, T, (n, D), eps[0], sy_long, record=True)
        nt += 1
        good = st == 'hit'
        if good:
            # total longitudinal travel must equal D, gates at z_i/D
            tot = sum(abs((b[0] - a[0]) if axis == 0 else (b[1] - a[1])) for a, b in segs)
            good = tot == D * Q
            cum = 0
            for i, zz in enumerate(zs):
                cum += pieces[i][0]
                p = pos_at(segs, Q, cum, axis)
                if p is None or p * D != zz * Q:
                    good = False
        nh += good
        if not good:
            log('   MISMATCH', name, eps, zs, n, st)
    log(f'  {name}: D={D} J(groupring)={Jg} J(enum)={len(sols)} agree={ok}; '
        f'traced {nt} solutions, {nh} reach T with predicted gates')
    return Jg, len(sols), nt, nh


# ======================================================================
def partA_named():
    log('== Part A: named rooms (area-21, area-23) ==')
    R21 = aligned((2, 2, 2), (1, 1, 1), (1, 1, 1), (1, 2))
    R23 = aligned((3, 1, 3), (1, 1, 1), (1, 1, 1), (1, 1))
    for name, R in (('area21', R21), ('area23', R23)):
        log(f' {name}: area={R.area} P={R.P} seams={R.seams} walls={len(R.verts)} marks={len(marks(R))}')
    return R21, R23


def direct(R, S, T):
    dx, dy = T[0] - S[0], T[1] - S[1]
    if dx == 0 or dy == 0:
        # axis-parallel: check segment interior in room (band rows / same column)
        return 'axis'
    st, _, _ = trace(R, S, T, (abs(dx), abs(dy)), 1 if dx > 0 else -1, 1 if dy > 0 else -1)
    return st


def partB_area21(R):
    log('== Part B: area-21 room, every lattice pair, note constructions ==')
    M = marks(R)
    stats = {}
    res = []
    for a in range(len(M)):
        for b in range(a + 1, len(M)):
            S, T = M[a], M[b]
            r = run_pair(R, S, T, stats, 'a21')
            if r == 'same-chamber':
                st = direct(R, S[1:], T[1:])
                r = 'direct:' + st
            res.append((S, T, r))
    for S, T, r in res:
        log(f'  {S[1:]} -> {T[1:]}: {r}')
    n_ok = sum(1 for _, _, r in res if r.endswith('hit') or r.endswith('axis'))
    log(f'  area21 pairs lit by note constructions: {n_ok}/{len(res)}')
    return n_ok == len(res)


def partC_width1(Lmax=14):
    log('== Part C: width-one middle family (3,1,3), heights 3, necks L=L ==')
    allok = True
    for L in range(1, Lmax + 1):
        R = aligned((3, 1, 3), (1, 1, 1), (1, 1, 1), (L, L))
        P = R.P
        Mk = marks(R)
        cnt = {}
        for a in range(len(Mk)):
            for b in range(a + 1, len(Mk)):
                (i, xS, yS), (j, xT, yT) = Mk[a], Mk[b]
                if i == j:
                    st = direct(R, (xS, yS), (xT, yT))
                    kind = 'same'
                elif yS != yT:
                    st = direct(R, (xS, yS), (xT, yT))
                    kind = 'rows'
                else:
                    if xS > xT:
                        xS, xT = xT, xS
                    # lower row by y -> 1-y symmetry: sy flips
                    sy = 1 if yS == 0 else -1
                    B = xT - xS
                    if B % 2:
                        st, _, _ = trace(R, (xS, yS), (xT, yT), (B, 3 * B + 1), 1, sy)
                        kind = 'oddB'
                    else:
                        off = xS  # 1 or 2
                        if off == 1:
                            Sx, Tx, sx = xS, xT, 1
                        else:  # mirror x -> P-x, reversed path
                            Sx, Tx, sx = xT, xS, -1
                        if L % 3 in (0, 1):
                            st, _, _ = trace(R, (Sx, yS), (Tx, yT), slope_of(Fr(P, 2)), sx, sy)
                            kind = 'endpocket'
                        else:
                            st, _, _ = trace(R, (Sx, yS), (Tx, yT), (3 + L, 1), -sx, sy)
                            kind = 'outer+neck'
                cnt[(kind, st)] = cnt.get((kind, st), 0) + 1
                if st not in ('hit', 'axis'):
                    allok = False
        # reviewer observation: end-pocket with n=1 also works for L = 2 mod 3
        extra = ''
        if L % 3 == 2:
            st, _, _ = trace(R, (1, 0), (5 + 2 * L, 0), slope_of(Fr(P, 2) + 2 * P), 1, 1)
            e = 2 - (P + 4 * P)
            extra = f' | endpocket n=1: 2-5P mod 6 = {e % 6}, trace {st}'
        log(f'  L={L} P={P} area={R.area}: ' + ', '.join(f'{k}/{s}:{v}' for (k, s), v in sorted(cnt.items())) + extra)
    log(f'  width-one family all pairs lit for L<= {Lmax}: {allok}')
    return allok


def partD_width2():
    log('== Part D: width-two family, L1 odd, L2 = 2 mod 4, arbitrary heights ==')
    hsets = [((1, 1, 1), (1, 1, 1)), ((2, 1, 3), (1, 3, 1)), ((3, 2, 1), (2, 1, 2)), ((1, 4, 2), (4, 1, 1))]
    allok, nrooms, npairs = True, 0, 0
    stats = {}
    for L1 in (1, 3, 5, 7, 9, 11):
        for L2 in (2, 6, 10, 14):
            for bs, ts in hsets:
                R = aligned((2, 2, 2), bs, ts, (L1, L2))
                nrooms += 1
                Mk = marks(R)
                for a in range(len(Mk)):
                    for b in range(a + 1, len(Mk)):
                        r = run_pair(R, Mk[a], Mk[b], stats, 'w2')
                        if r == 'same-chamber':
                            continue
                        npairs += 1
                        if not r.endswith('hit'):
                            allok = False
                            log('   FAIL', L1, L2, bs, ts, Mk[a], Mk[b], r)
    log(f'  rooms={nrooms} cross-chamber pairs traced={npairs} all hit={allok}')
    for k, v in sorted((k, v) for k, v in stats.items() if isinstance(k, tuple)):
        log(f'   {k}: {v}')
    log(f'   max bounces {stats.get("maxbounce")}')
    return allok


def audit_exception(R, S, T, stats):
    P = R.P
    xS, xT = S[1], T[1]
    fl = [fold(z, P) for X, sx, Y, z in zero_roots(R, xS, xT) if X == xS]
    if all(f in R.seams for f in fl):
        stats['exc-seams'] = stats.get('exc-seams', 0) + 1
    E = {s % (2 * P) for s in R.seams} | {(-s) % (2 * P) for s in R.seams}
    cand = {((a + b) % P, (a - b) % P) for a in E for b in E}
    if (xS % P, xT % P) in cand or (xS % P, (-xT) % P) in cand:
        stats['exc-bound'] = stats.get('exc-bound', 0) + 1
    stats.setdefault('exc-rooms', set()).add((tuple(R.ws), tuple(R.Ls), R.area))


def partE_coprime_grid():
    log('== Part E: coprime theorems on a parameter grid ==')
    hsets = [((1, 1, 1), (1, 1, 1)), ((2, 1, 3), (1, 3, 1)), ((1, 3, 2), (2, 1, 2))]
    stats = {}
    nrooms = 0
    exc_rooms = 0
    for ws in product((1, 2, 3, 4), repeat=3):
        for Ls in product((1, 2, 3), repeat=2):
            P = sum(ws) + sum(Ls)
            if gcd(P, lcm(*ws)) != 1:
                continue
            for bs, ts in hsets:
                R = aligned(ws, bs, ts, Ls)
                nrooms += 1
                Mk = marks(R)
                for a in range(len(Mk)):
                    for b in range(a + 1, len(Mk)):
                        r = run_pair(R, Mk[a], Mk[b], stats, 'grid')
                        if r == 'exception':
                            audit_exception(R, Mk[a], Mk[b], stats)
    log(f'  coprime rooms={nrooms}')
    for k, v in sorted(((k, v) for k, v in stats.items() if isinstance(k, tuple)), key=str):
        log(f'   {k}: {v}')
    log(f'   max bounces {stats.get("maxbounce")}; failures: {len(stats.get("fail", []))}')
    for f in stats.get('fail', [])[:10]:
        log('    ', f)
    exc = stats.get('zero-exception', [])
    log(f'   zero-drift exceptions (equal-parity same-side pairs, P odd): {len(exc)}')
    log(f'   exceptions with both roots at seams (never 0 or P): {stats.get("exc-seams", 0)}; '
        f'inside the 64-pair outer bound: {stats.get("exc-bound", 0)}; rooms: {sorted(stats.get("exc-rooms", set()))}')
    return stats


def partF_exceptional():
    log('== Part F: exceptional set arithmetic and the 4,6,4+156k example ==')
    ok = True
    for k in range(1, 7):
        ws = (4, 6, 4 + 156 * k)
        R = aligned(ws, (1, 1, 1), (1, 1, 1), (2, 1))
        P = R.P
        cop = gcd(P, lcm(*ws)) == 1
        roots = {}
        for X, sx, Y, z in zero_roots(R, 8, 16):
            roots[(X, Y)] = z
        folds = sorted({fold(z, P) for z in roots.values()})
        allseam = all(f in R.seams for f in folds)
        ok &= cop and P % 2 == 1 and allseam and R.seams == [4, 6, 12, 13]
        log(f'  k={k}: P={P} odd={P % 2 == 1} coprime={cop} seams={R.seams} roots={roots} folds={folds} all seams={allseam}')
    # 64-bound: for P odd, exceptions satisfy xS = z+ + z-, xT = z+ - z- (mod P)
    R = aligned((4, 6, 160), (1, 1, 1), (1, 1, 1), (2, 1))
    P = R.P
    E = sorted({s % (2 * P) for s in R.seams} | {(-s) % (2 * P) for s in R.seams})
    cand = set()
    for zp in E:
        for zm in E:
            cand.add(((zp + zm) % P, (zp - zm) % P))
    log(f'  k=1: |E|={len(E)}, outer-bound abscissa pairs={len(cand)} (<=64)')
    # brute arithmetic over all equal-parity abscissa pairs in distinct chambers (arithmetic only)
    exc = []
    for xS in range(1, P):
        for xT in range(1, P):
            if xS == xT or (xS - xT) % 2:
                continue
            cS, cT = chamber_at(R, xS), chamber_at(R, xT)
            if cS is None or cT is None or cS == cT:
                continue
            fl = [fold(z, P) for X, sx, Y, z in zero_roots(R, xS, xT) if X == xS]
            if all(f in R.seams for f in fl):
                exc.append((xS, xT))
                if (xS % P, xT % P) not in cand and (xS % P, (-xT) % P) not in cand:
                    ok = False
    log(f'  k=1: equal-parity cross-chamber abscissa pairs missed by zero-drift: {exc}')
    # control: trace the zero-drift ray at the seam root z=12 from (8,0) to (16,0): must hit the corner (12,1)
    M = 2 * lcm(4, 6, 160)
    m = minpos_m(M, 12 - 8, P)
    st, bl, _ = trace(R, (8, 0), (16, 0), (M * m, 1), 1, 1)
    log(f'  control: zero-drift ray through seam root z=12 (c={M * m}): {st} after {len(bl)} bounces')
    return ok


def partG_J():
    log('== Part G: group-ring test vs enumeration vs tracing ==')
    out = []
    R = aligned((2, 2, 2), (1, 1, 1), (1, 1, 1), (1, 2))  # area 21
    # horizontal itineraries through all pieces, chamber1 -> chamber3
    def hpieces(R, xS, xT):
        return [(R.ws[0] - xS, -R.bs[0], R.bs[0] + 1 + R.ts[0]), (R.Ls[0], 0, 1),
                (R.ws[1], -R.bs[1], R.bs[1] + 1 + R.ts[1]), (R.Ls[1], 0, 1),
                (xT - R.l[2], -R.bs[2], R.bs[2] + 1 + R.ts[2])], [(0, 1)] * 4
    for S, T in (((1, 0), (8, 1)), ((1, 0), (8, 0)), ((1, 1), (8, 0))):
        pc, gt = hpieces(R, S[0], T[0])
        out.append(J_case(f'area21 horizontal {S}->{T}', R, pc, gt, S, T, 0))
    # vertical: equal labels on the lower edge, (4,0)->(8,0)
    P = R.P
    for nk, (a, b) in enumerate(R.necks):
        pc = [(1, 0, P), (1, 0, P)]
        out.append(J_case(f'area21 vertical (4,0)->(8,0) neck{nk + 1} bounce', R, pc, [(a, b)], (4, 0), (8, 0), 1))
    for k in range(3):
        span = (R.l[k], R.l[k] + R.ws[k])
        pc = [(1, 0, P), (R.ts[k], R.l[k], R.ws[k]), (R.ts[k], R.l[k], R.ws[k]), (1, 0, P)]
        out.append(J_case(f'area21 vertical (4,0)->(8,0) excursion chamber{k + 1}', R, pc, [span] * 3, (4, 0), (8, 0), 1))
    # deeper room: pockets with stubs
    R2 = aligned((2, 3, 2), (2, 2, 2), (1, 1, 1), (1, 2))
    P2 = R2.P
    xT = R2.l[2] + 1
    for nk, (a, b) in enumerate(R2.necks):
        pc = [(1, R2.l[0], R2.ws[0]), (1, 0, P2), (1, 0, P2), (1, R2.l[2], R2.ws[2])]
        gt = [(R2.l[0], R2.l[0] + R2.ws[0]), (a, b), (R2.l[2], R2.l[2] + R2.ws[2])]
        out.append(J_case(f'room(2,3,2;b=2,t=1;1,2) vertical (1,-1)->({xT},-1) neck{nk + 1}', R2, pc, gt, (1, -1), (xT, -1), 1))
    # opposite labels with stubs
    pc = [(1, R2.l[0], R2.ws[0]), (1, 0, P2), (1, R2.l[2], R2.ws[2])]
    gt = [(R2.l[0], R2.l[0] + R2.ws[0]), (R2.l[2], R2.l[2] + R2.ws[2])]
    out.append(J_case(f'room(2,3,2;b=2,t=1;1,2) vertical (1,-1)->({xT},2)', R2, pc, gt, (1, -1), (xT, 2), 1))
    pc, gt = hpieces(R2, 1, xT)
    out.append(J_case(f'room(2,3,2;b=2,t=1;1,2) horizontal (1,-1)->({xT},1)', R2, pc, gt, (1, -1), (xT, 1), 0, maxtrace=8))
    agree = all(a == b for a, b, _, _ in out)
    traced_ok = all(nt == nh for _, _, nt, nh in out)
    log(f'  group-ring = enumeration in all cases: {agree}; all traced solutions reach T: {traced_ok}')
    return agree and traced_ok


def partH_height5():
    log('== Part H: d202 height-5 gap (3x3, 3x5, 3x3, necks 1,1) ==')
    R = aligned((3, 3, 3), (1, 1, 1), (1, 3, 1), (1, 1))
    P = R.P
    log(f'  P={P} coprime={gcd(P, 3) == 1}')
    # gcd lift arithmetic (note's formula): F=-1, H=5, y_T=3, z=0, M=3 (end height)
    for v in (1, 2):
        g = gcd(2 * 3 * v, 10)
        rhs = [-1 + s * (3 + 1) - 0 for s in (1, -1)]
        log(f'  gcd lift v={v}: gcd(2Mv,2H)={g}, F+-(yT-F)-z={rhs}, divisible={[r % g == 0 for r in rhs]}')
    stats = {}
    ok = True
    for xS in (1, 2):
        for xT in (5, 6):
            S, T = (0, xS, 1), (1, xT, 3)
            r = run_pair(R, S, T, stats, 'h5')
            log(f'  end ({xS},1) -> middle ({xT},3): {r}')
            ok &= r.endswith('hit')
    return ok


# ---------------------------------------------------------------- mixed construction
def fold_lin(alpha, beta, f, B, lo, hi):
    """phase alpha+beta r on (lo,hi); split where phase in B*Z.
    Returns list of (lo, hi, posA, posB, up) with pos = posA + posB r."""
    bps = {lo, hi}
    if beta != 0:
        for e in (lo, hi):
            pass
        vals = [alpha + beta * lo, alpha + beta * hi]
        kmin = int(min(vals) // B) - 1
        kmax = int(max(vals) // B) + 1
        for k in range(kmin, kmax + 1):
            r = Fr(k * B - alpha, beta)
            if lo < r < hi:
                bps.add(r)
    pts = sorted(bps)
    out = []
    for a, b in zip(pts, pts[1:]):
        mid = (a + b) / 2
        k = (alpha + beta * mid) // B
        if (alpha + beta * mid) % B == 0:
            continue
        if k % 2 == 0:
            out.append((a, b, f + alpha - k * B, beta, True))
        else:
            out.append((a, b, f + (k + 1) * B - alpha, -beta, False))
    return out


def prefix_pieces(R, side, x, y, image, up0, rmax):
    """Fold the prefix from mark (x,y) toward the middle mouth. Returns
    pieces (lo,hi,uA,uB) with mouth height u=uA+uB r, direction up."""
    if side == 0:
        X = -x if image else x
        t1 = R.ws[0] - X
        c, Ln = 0, R.Ls[0]
    else:
        X = 2 * R.P - x if image else x
        t1 = X - R.l[2]
        c, Ln = 2, R.Ls[1]
    f, B = -R.bs[c], R.bs[c] + 1 + R.ts[c]
    ph0 = (y - f) if up0 else (2 * B - (y - f))
    out = []
    for lo, hi, pA, pB, up in fold_lin(Fr(ph0), Fr(t1), f, B, Fr(0), rmax):
        # require seam position in (0,1): restrict
        lo2, hi2 = lo, hi
        for bound, sense in ((0, 1), (1, -1)):
            # sense*(pA + pB r - bound) > 0
            A_, B_ = sense * (pA - bound), sense * pB
            if B_ == 0:
                if A_ <= 0:
                    lo2, hi2 = 1, 0
            else:
                r0 = Fr(-A_, B_)
                if B_ > 0:
                    lo2 = max(lo2, r0)
                else:
                    hi2 = min(hi2, r0)
        if not lo2 < hi2:
            continue
        # neck phase: pos up -> pos, down -> 2-pos (f=0,B=1)
        a2 = pA if up else 2 - pA
        b2 = pB if up else -pB
        for lo3, hi3, uA, uB, up3 in fold_lin(a2, b2 + Ln, 0, 1, lo2, hi2):
            if up3:
                out.append((lo3, hi3, uA, uB))
    return out


def mixed_case(R, S, T, maxq=41):
    """S in chamber 0, T in chamber 2; upper-pocket branch of the middle."""
    w, Hm = R.ws[1], R.ts[1]
    rmax = Fr(2 * (1 + Hm), w)
    found = []
    for imS, upS, imT, upT in product((0, 1), repeat=4):
        Lp = prefix_pieces(R, 0, S[0], S[1], imS, upS, rmax)
        Rp = prefix_pieces(R, 2, T[0], T[1], imT, upT, rmax)
        for lo1, hi1, uA, uB in Lp:
            for lo2, hi2, vA, vB in Rp:
                lo, hi = max(lo1, lo2), min(hi1, hi2)
                for A_, B_ in ((1 - uA, -uB - w), (1 - vA, -vB - w)):
                    # 1-u < w r  <=>  A_ + B_ r < 0
                    if B_ == 0:
                        if A_ >= 0:
                            lo, hi = 1, 0
                    else:
                        r0 = Fr(-A_, B_)
                        if B_ < 0:
                            lo = max(lo, r0)
                        else:
                            hi = min(hi, r0)
                if not lo < hi:
                    continue
                A = 2 * (1 + Hm) - uA - vA
                Bc = -uB - vB
                # (A/r + B)/w odd: r = A / (q w - B)
                for q in range(1, maxq + 1, 2):
                    den = q * w - Bc
                    if den == 0:
                        continue
                    r = Fr(A, den)
                    if lo < r < hi:
                        found.append((r, imS, upS, imT, upT, q))
    res = []
    for r, imS, upS, imT, upT, q in found:
        sx = -1 if imS else 1
        sy = 1 if upS else -1
        st, bl, _ = trace(R, S, T, (r.denominator, r.numerator), sx, sy)
        res.append((r, q, imS, imT, st))
    return res


def partI_mixed():
    log('== Part I: mixed construction (folded neck legs + middle roof) ==')
    rooms = [('area21', aligned((2, 2, 2), (1, 1, 1), (1, 1, 1), (1, 2))),
             ('area23', aligned((3, 1, 3), (1, 1, 1), (1, 1, 1), (1, 1))),
             ('3x3,3x4,3x3 X=Y=2', aligned((3, 3, 3), (1, 1, 1), (1, 2, 1), (2, 2))),
             ('2x4,3x6,3x3 L=3,2', aligned((2, 3, 3), (2, 1, 1), (1, 4, 1), (3, 2)))]
    tot = hit = 0
    rooms = rooms + [(n + ' flipped', flipped(R)) for n, R in rooms]
    for name, R in rooms:
        Mk = marks(R)
        Ls = [(x, y) for c, x, y in Mk if c == 0]
        Rs = [(x, y) for c, x, y in Mk if c == 2]
        nsol = nh = 0
        pairs_with = 0
        for S in Ls:
            for T in Rs:
                res = mixed_case(R, S, T)
                if res:
                    pairs_with += 1
                for r, q, imS, imT, st in res:
                    nsol += 1
                    nh += st == 'hit'
                    if st != 'hit':
                        log('   MIXED FAIL', name, S, T, r, q, imS, imT, st)
        tot += nsol
        hit += nh
        log(f'  {name}: outer pairs={len(Ls) * len(Rs)}, pairs with a mixed solution={pairs_with}, '
            f'solutions (q<=41)={nsol}, traced hits={nh}')
    log(f'  mixed: {hit}/{tot} prescribed rays reach T')
    return hit == tot


def partJ_ledger():
    log('== Part J: ledger words ==')
    words = json.load(open(os.path.join(HERE, '..', 'd163-pattern-ledger', 'ledger.json')))['words']

    def canon(w):
        c = []
        for s in (w, w[::-1]):
            for i in range(len(s)):
                c.append(s[i:] + s[:i])
        return min(c)

    F = 'RRLLLLRR'
    for j, name in ((0, 'same side'), (1, 'adjacent'), (2, 'opposite')):
        c = canon(F + 'L' * j + F + 'L' * (4 - j))
        e = words.get(c)
        log(f'  j={j} ({name}): {c} ledger status={e["status"]} W={e["W"]}')
    c = canon(F + 'LLLL')
    log(f'  one neck: {c} ledger status={words[c]["status"]} by={words[c]["by"]}')
    log(f'  rectangle LLLL status={words["LLLL"]["status"]}')


def vertical_itins(R, S, T):
    """Note item 2, equal labels, both marks lower (y<=0): all itineraries
    the note lists (optional floor bounce at each end, neck bounce or
    one-chamber excursion between the band crossings)."""
    (i, xS, yS), (j, xT, yT) = S, T
    P = R.P
    span = lambda k: (R.l[k], R.l[k] + R.ws[k])
    out = []
    def ends(k, y, rev):
        a = -y
        opts = []
        if a > 0:
            opts.append(([(a, R.l[k], R.ws[k])], [span(k)], 'stub'))
        else:
            opts.append(([], [], 'edge'))
        # optional floor reflection first
        bb = R.bs[k]
        opts.append(([(y + bb, R.l[k], R.ws[k]), (bb, R.l[k], R.ws[k])], [span(k), span(k)], 'floor'))
        if rev:
            opts = [(pc[::-1], gt[::-1], nm) for pc, gt, nm in opts]
        return opts
    mids = [([], [nk], f'neck{n + 1}') for n, nk in enumerate(R.necks)]
    for k in range(3):
        mids.append(([(R.ts[k], R.l[k], R.ws[k])] * 2, [span(k)] * 3, f'excursion{k + 1}'))
    for pS, gS, nS in ends(i, yS, False):
        for pT, gT, nT in ends(j, yT, True):
            for pm, gm, nm in mids:
                pieces = pS + [(1, 0, P)] + pm + [(1, 0, P)] + pT
                gates = gS + gm + gT
                out.append((f'{nS}/{nm}/{nT}', pieces, gates))
    return out


def horizontal_itins(R, S, T):
    """Note item 1: horizontally monotone chamber-neck list, with optional
    end-wall images at the solid outer walls. S in chamber 0, T in chamber 2."""
    (i, xS, yS), (j, xT, yT) = S, T
    ch = lambda k: (-R.bs[k], R.bs[k] + 1 + R.ts[k])
    out = []
    for imS, imT in product((0, 1), repeat=2):
        pieces, gates = [], []
        f0, B0 = ch(0)
        if imS:
            pieces += [(xS, f0, B0), (R.ws[0], f0, B0)]
            gates += [(f0, f0 + B0)]
        else:
            pieces += [(R.ws[0] - xS, f0, B0)]
        pieces += [(R.Ls[0], 0, 1), (R.ws[1],) + ch(1), (R.Ls[1], 0, 1)]
        gates += [(0, 1)] * 4
        f2, B2 = ch(2)
        if imT:
            pieces += [(R.ws[2], f2, B2), (R.P - xT, f2, B2)]
            gates += [(f2, f2 + B2)]
        else:
            pieces += [(xT - R.l[2], f2, B2)]
        out.append((f'h imS={imS} imT={imT}', pieces, gates, imS, imT))
    return out


def partK_residuals():
    log('== Part K: note tests on named pairs outside the dimension-only statements ==')
    cases = [('area21 (3,1,2) necks (1,2) h3', aligned((3, 1, 2), (1, 1, 1), (1, 1, 1), (1, 2)), [((0, 2, 0), (2, 8, 0))]),
             ('area23 (2,1,4) necks (1,1) h3', aligned((2, 1, 4), (1, 1, 1), (1, 1, 1), (1, 1)), None),
             ('area23 (1,4,2) necks (1,1) h3', aligned((1, 4, 2), (1, 1, 1), (1, 1, 1), (1, 1)), None),
             ('area22 (2,2,2) necks (2,2) h3', aligned((2, 2, 2), (1, 1, 1), (1, 1, 1), (2, 2)), None)]
    for name, R, pairs in cases:
        if pairs is None:
            # lower-side cross-chamber pairs not covered by the coprime constructions
            Mk = [m for m in marks(R) if m[2] <= 0]
            pairs = []
            for a in range(len(Mk)):
                for b in range(a + 1, len(Mk)):
                    S, T = Mk[a], Mk[b]
                    if S[0] == T[0]:
                        continue
                    st = {}
                    r = run_pair(R, S, T, st, 'K')
                    if not r.endswith('hit'):
                        pairs.append((S, T))
        log(f' {name}: P={R.P} area={R.area} gcd(P,lcm)={gcd(R.P, lcm(*R.ws))}; uncovered lower pairs: {[(S[1:], T[1:]) for S, T in pairs]}')
        for S, T in pairs:
            pos = []
            for nm, pc, gt in vertical_itins(R, S, T):
                cnt, D, w = J_witness(pc, gt, S[1], T[1])
                if cnt:
                    pos.append((nm, cnt, pc, gt, D, w))
            if S[0] != 1 and T[0] != 1:
                SS, TT = (S, T) if S[0] == 0 else (T, S)
                for nm, pc, gt, imS, imT in horizontal_itins(R, SS, TT):
                    cnt, D, w = J_witness(pc, gt, SS[2], TT[2])
                    if cnt:
                        pos.append((nm, cnt, pc, gt, D, w))
            log(f'  pair {S[1:]}->{T[1:]}: positive itineraries: {[(p[0], p[1]) for p in pos]}')
            if pos:
                nm, cnt, pc, gt, D, (eps, zs, (n0, per)) = pos[0]
                n = n0 if n0 > 0 else n0 + per
                if nm.startswith('h'):
                    SS, TT = (S, T) if S[0] == 0 else (T, S)
                    sx = -1 if 'imS=1' in nm else 1
                    st, bl, _ = trace(R, SS[1:], TT[1:], (D, n), sx, eps[0])
                else:
                    sy = -1 if nm.startswith('floor') else 1
                    st, bl, _ = trace(R, S[1:], T[1:], (n, D), eps[0], sy)
                log(f'   traced first solution of {nm}: n/D={Fr(n, D)} -> {st} ({len(bl)} bounces)')


if __name__ == '__main__':
    R21, R23 = partA_named()
    okB = partB_area21(R21)
    okC = partC_width1(30)
    okD = partD_width2()
    partE_coprime_grid()
    okF = partF_exceptional()
    okG = partG_J()
    okH = partH_height5()
    okI = partI_mixed()
    partJ_ledger()
    partK_residuals()
    log(f'SUMMARY B={okB} C={okC} D={okD} F={okF} G={okG} H={okH} I={okI}')
    log(f'CPU seconds: {time.process_time() - T0:.1f}')
    with open(os.path.join(HERE, 'checks.log'), 'w') as fh:
        fh.write('\n'.join(LOG) + '\n')
