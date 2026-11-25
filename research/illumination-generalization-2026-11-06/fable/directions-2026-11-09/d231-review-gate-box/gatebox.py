"""D231: exact checks of the d230 gate-box lemmas (Angle 1).

Named rooms only: seven-cell room, parabola family (5 points), six-reflex
locked-gate family (3 points). For every itinerary up to a fixed number of
events, every side-reflection parity pattern, and every winding vector in a
small range, compare
  A = "the coset point u(k) lies in the open box of event intervals"
  B = "the exact polygon billiard with the induced slope is legal, follows the
       itinerary, and ends at T".
Then compute the dual lattice two ways (direct inverse transpose; Lemma 1),
the minimal flatness width, and exact hollowness of every parity coset.
"""
import itertools, math, sys, time
from fractions import Fraction as F

FLT2 = 1 + 2 / math.sqrt(3)  # Hurkens 1990

# ---------------------------------------------------------------- geometry
def room_from_tiers(tiers):
    """tiers: list of (y0,y1,a,b) bottom to top. Returns CCW vertex list."""
    right, left = [], []
    for k, (y0, y1, a, b) in enumerate(tiers):
        right += [(b, y0), (b, y1)]
        left += [(a, y0), (a, y1)]
    pts = [(tiers[0][2], tiers[0][0])] + right + left[::-1][:-1]
    # drop duplicates and collinear points
    out = []
    for p in pts:
        if not out or out[-1] != p:
            out.append(p)
    if out[0] == out[-1]:
        out.pop()
    changed = True
    while changed:
        changed = False
        n = len(out)
        for i in range(n):
            a, b, c = out[i - 1], out[i], out[(i + 1) % n]
            if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]) or a == b:
                out.pop(i); changed = True; break
    return out

def edges(V):
    return [(V[i], V[(i + 1) % len(V)]) for i in range(len(V))]

def check_room(V):
    """orthogonal, simple (no edge touches a non-adjacent edge), reflex count."""
    E = edges(V)
    for (p, q) in E:
        assert p[0] == q[0] or p[1] == q[1]
    def seg_meet(e, f):
        (p, q), (r, s) = e, f
        x0, x1 = sorted([p[0], q[0]]); y0, y1 = sorted([p[1], q[1]])
        X0, X1 = sorted([r[0], s[0]]); Y0, Y1 = sorted([r[1], s[1]])
        return max(x0, X0) <= min(x1, X1) and max(y0, Y0) <= min(y1, Y1)
    n = len(E)
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            assert not seg_meet(E[i], E[j]), ("not strictly simple", E[i], E[j])
    area2 = sum(V[i][0] * V[(i + 1) % n][1] - V[(i + 1) % n][0] * V[i][1] for i in range(n))
    sgn = 1 if area2 > 0 else -1
    refl = 0
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if cr * sgn < 0:
            refl += 1
    return refl, abs(area2) / 2

def slabs(V):
    ys = sorted(set(p[1] for p in V))
    E = edges(V)
    S = []  # (k, y0, y1, a, b)
    for k in range(len(ys) - 1):
        y0, y1 = ys[k], ys[k + 1]; ym = (y0 + y1) / 2
        xs = sorted(p[0] for (p, q) in E if p[0] == q[0] and min(p[1], q[1]) < ym < max(p[1], q[1]))
        for i in range(0, len(xs), 2):
            S.append((k, y0, y1, xs[i], xs[i + 1]))
    return ys, S

def ceiling_pieces(sl, S, up):
    """open pieces of the top (up) or bottom face: list of (J, kind, next slab)."""
    k, y0, y1, a, b = sl
    nk = k + 1 if up else k - 1
    gates = []
    for t in S:
        if t[0] == nk:
            lo, hi = max(a, t[3]), min(b, t[4])
            if lo < hi:
                gates.append(((lo, hi), 'T', t))
    gates.sort()
    walls, x = [], a
    for (lo, hi), _, _ in gates:
        if x < lo:
            walls.append(((x, lo), 'R', sl))
        x = hi
    if x < b:
        walls.append(((x, b), 'R', sl))
    return gates + walls

def interior(V, P):
    """strict interior test (ray casting, P not on boundary)."""
    E = edges(V); x, y = P; inside = False
    for (p, q) in E:
        if p[0] == q[0] and min(p[1], q[1]) <= y <= max(p[1], q[1]) and p[0] == x:
            return False
        if p[1] == q[1] and min(p[0], q[0]) <= x <= max(p[0], q[0]) and p[1] == y:
            return False
        if p[0] == q[0] and p[0] > x and min(p[1], q[1]) <= y < max(p[1], q[1]):
            inside = not inside
    return inside

# ---------------------------------------------------------------- itineraries
def itineraries(V, S0, T, gmax):
    ys, S = slabs(V)
    def containing(P, strict):
        out = []
        for s in S:
            k, y0, y1, a, b = s
            if a < P[0] < b and ((y0 < P[1] < y1) if strict else (y0 <= P[1] <= y1)):
                out.append(s)
        return out
    starts = []
    for s in containing(S0, False):
        k, y0, y1, a, b = s
        if y0 < S0[1] < y1:
            starts += [(s, True), (s, False)]
        elif S0[1] == y0:
            starts.append((s, True))
        elif S0[1] == y1:
            starts.append((s, False))
    res = []
    def dfs(sl, up, ypos, visits, events):
        k, y0, y1, a, b = sl
        # end at T inside this visit?
        if a < T[0] < b:
            if (up and ypos <= T[1] <= y1 and T[1] != ypos) or ((not up) and y0 <= T[1] <= ypos and T[1] != ypos):
                if not (T[1] in (y0, y1)) or T[1] == (y1 if up else y0):
                    res.append((visits + [(sl, abs(T[1] - ypos))], events))
        if len(events) >= gmax:
            return
        ylev = y1 if up else y0
        h = abs(ylev - ypos)
        for J, kind, nsl in ceiling_pieces(sl, S, up):
            if kind == 'T':
                dfs(nsl, up, ylev, visits + [(sl, h)], events + [(ylev, J, 'T')])
            else:
                dfs(sl, not up, ylev, visits + [(sl, h)], events + [(ylev, J, 'R')])
    for s, up in starts:
        dfs(s, up, S0[1], [], [])
    return res

# ---------------------------------------------------------------- formula side
def coset_point(itin, S0, T, eps, k):
    """my own derivation: returns (p, [x_i physical], [u_i folded], sigma list)."""
    visits, events = itin
    g = len(events)
    h = [vh for (_, vh) in visits]
    Y = [sum(h[:i]) for i in range(g + 2)]
    H = Y[g + 1]
    sig = [1]
    cs = []
    for j in range(g + 1):
        a = visits[j][0][3]
        cs.append(0 if eps[j] == 0 else 2 * sig[j] * a)
        sig.append(sig[j] * (1 if eps[j] == 0 else -1))
    w = [visits[j][0][4] - visits[j][0][3] for j in range(g + 1)]
    tot = sum(cs[j] + 2 * w[j] * k[j] for j in range(g + 1))
    p = F(sig[g + 1] * T[0] - S0[0] + tot) / H
    u = []
    for i in range(1, g + 1):
        u.append(S0[0] + p * Y[i] - sum(cs[j] + 2 * w[j] * k[j] for j in range(i)))
    x = [sig[i] * u[i - 1] for i in range(1, g + 1)]
    return p, x, u, sig

def in_open_box(itin, x):
    return all(J[0] < xi < J[1] for xi, (_, J, _) in zip(x, itin[1]))

def phi_matrix(itin):
    visits, events = itin
    g = len(events)
    h = [vh for (_, vh) in visits]
    Y = [sum(h[:i]) for i in range(g + 2)]
    H = Y[g + 1]
    w = [visits[j][0][4] - visits[j][0][3] for j in range(g + 1)]
    return [[2 * w[j] * (F(Y[i], 1) / H - (1 if j < i else 0)) for j in range(g + 1)] for i in range(1, g + 1)], w, h, Y, H

# ---------------------------------------------------------------- billiard tracer
def trace(V, S0, T, vx, vy, Htot, levels):
    """Exact billiard in polygon V from S0 with velocity (vx,vy), |vy|=1, for
    absolute vertical travel Htot. Returns (status, events, endpoint).
    events: list of (level, x, kind, onwall) at times in (0,end)."""
    E = edges(V)
    Vset = set(V)
    P = (F(S0[0]), F(S0[1])); vx = F(vx); vy = F(vy)
    rem = F(Htot); ev = []; steps = 0
    while True:
        steps += 1
        if steps > 100000:
            return 'loop', ev, P
        hits = []
        for (p, q) in E:
            if p[0] == q[0] and vx != 0:
                t = (p[0] - P[0]) / vx
                if t > 0 and min(p[1], q[1]) <= P[1] + vy * t <= max(p[1], q[1]):
                    hits.append((t, 'V'))
            if p[1] == q[1]:
                t = (p[1] - P[1]) / vy
                if t > 0 and min(p[0], q[0]) <= P[0] + vx * t <= max(p[0], q[0]):
                    hits.append((t, 'H'))
        t_hit = min(h[0] for h in hits)
        kinds = set(h[1] for h in hits if h[0] == t_hit)
        t_stop = min(t_hit, rem)
        cross = sorted(((L - P[1]) / vy, L) for L in levels if 0 < (L - P[1]) / vy < t_stop)
        for t, L in cross:
            ev.append((L, P[0] + vx * t, 'T', False))
        if rem < t_hit:
            return 'ok', ev, (P[0] + vx * rem, P[1] + vy * rem)
        Q = (P[0] + vx * t_hit, P[1] + vy * t_hit)
        if Q in Vset or len(kinds) > 1:
            return 'corner', ev, Q
        if rem == t_hit:
            return 'wallend', ev, Q
        if 'H' in kinds:
            ev.append((Q[1], Q[0], 'R', False)); vy = -vy
        else:
            if Q[1] in levels:
                ev.append((Q[1], Q[0], 'T', True))  # smooth side hit exactly on a level
            vx = -vx
        rem -= t_hit; P = Q

def follows(itin, ev):
    events = itin[1]
    if len(ev) != len(events):
        return False, False
    onb = False
    for (L, x, kd, onwall), (L2, J, kd2) in zip(ev, events):
        if L != L2 or kd != kd2:
            return False, False
        if not (J[0] <= x <= J[1]):
            return False, False
        if x in J:
            onb = True
    return True, onb

# ---------------------------------------------------------------- lattices
def hnf_cols(M):
    """integer column lattice basis (as list of column vectors) via row-style HNF on transpose."""
    rows = [list(c) for c in zip(*M)]  # generators as rows
    m = len(rows[0]); basis = []
    rows = [r[:] for r in rows]
    col = 0; r0 = 0
    while col < m and rows:
        nz = [r for r in rows if r[col] != 0]
        z = [r for r in rows if r[col] == 0]
        while len(nz) > 1:
            nz.sort(key=lambda r: abs(r[col]))
            piv = nz[0]
            new = [piv]
            for r in nz[1:]:
                q = r[col] // piv[col]
                rr = [a - q * b for a, b in zip(r, piv)]
                (new if rr[col] != 0 else z).append(rr)
            nz = new
        if nz:
            basis.append(nz[0])
        rows = [r for r in z if any(r)]
        col += 1
    return basis

def int_kernel(row):
    """Z-basis of {n in Z^m : row.n = 0}, row integer."""
    m = len(row)
    # unimodular U with row*U = (g,0,...,0) by column ops
    U = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    r = row[:]
    for j in range(1, m):
        # combine columns 0 and j
        a, b = r[0], r[j]
        if b == 0:
            continue
        # ext gcd
        def eg(a, b):
            if b == 0:
                return (a, 1, 0)
            g, x, y = eg(b, a % b)
            return (g, y, x - (a // b) * y)
        g, x, y = eg(a, b)
        # new col0 = x*c0 + y*cj, new colj = (-b/g)*c0 + (a/g)*cj
        c0 = [U[i][0] for i in range(m)]; cj = [U[i][j] for i in range(m)]
        for i in range(m):
            U[i][0] = x * c0[i] + y * cj[i]
            U[i][j] = (-b // g) * c0[i] + (a // g) * cj[i]
        r[0], r[j] = g, 0
    return [[U[i][j] for i in range(m)] for j in range(1, m)]

def det(M):
    M = [row[:] for row in M]; n = len(M); d = F(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return F(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return d

def inv(M):
    n = len(M)
    A = [list(map(F, row)) + [F(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]; A[c] = [a / pv for a in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]; A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]

def lattice_data(itin):
    Phi, w, h, Y, H = phi_matrix(itin)
    g = len(Phi)
    D = 1
    for row in Phi:
        for e in row:
            D = D * e.denominator // math.gcd(D, e.denominator)
    M = [[int(e * D) for e in row] for row in Phi]
    B = hnf_cols(M)  # rows = basis vectors (scaled by D)
    assert len(B) == g, "lattice not full rank"
    Bv = [[F(x, D) for x in b] for b in B]  # basis vectors of Lambda
    # dual basis: rows of (Bmat^{-1})^T where Bmat has basis vectors as columns
    Bmat = [[Bv[j][i] for j in range(g)] for i in range(g)]
    Bi = inv(Bmat)
    dual = [[Bi[j][i] for i in range(g)] for j in range(g)]  # rows: dual vectors = rows of Bi
    # Lemma 1
    mu = [F(h[j], 2 * w[j]) for j in range(g + 1)]
    Lm = 1
    for e in mu:
        Lm = Lm * e.denominator // math.gcd(Lm, e.denominator)
    rowint = [int(e * Lm) for e in mu]
    K = int_kernel(rowint)
    ell = [[F(n[i - 1], 2 * w[i - 1]) - F(n[i], 2 * w[i]) for i in range(1, g + 1)] for n in K]
    # check: each ell in Lambda* and same covolume
    ok_in = all(all((sum(l[i] * Phi[i][j] for i in range(g))).denominator == 1 for j in range(g + 1)) for l in ell)
    ok_cov = abs(det(ell)) == abs(det(dual))
    return dict(Phi=Phi, w=w, h=h, Y=Y, H=H, basis=Bv, dual=dual, mu=mu, K=K, ell=ell,
                lemma1_in=ok_in, lemma1_cov=ok_cov, covol=abs(det(Bmat)))

def lll(B, delta=F(3, 4)):
    B = [list(b) for b in B]; n = len(B)
    def dot(a, b): return sum(x * y for x, y in zip(a, b))
    def gs(B):
        Bs = []; mu = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            v = B[i][:]
            for j in range(i):
                mu[i][j] = dot(B[i], Bs[j]) / dot(Bs[j], Bs[j])
                v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
            Bs.append(v)
        return Bs, mu
    k = 1
    while k < n:
        Bs, mu = gs(B)
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * b for a, b in zip(B[k], B[j])]
                Bs, mu = gs(B)
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]; k = max(k - 1, 1)
    return B

def min_width(itin, dual, R=4):
    Jl = [J[1] - J[0] for (_, J, _) in itin[1]]
    D = lll(dual)
    best = None
    for c in itertools.product(range(-R, R + 1), repeat=len(D)):
        if not any(c):
            continue
        l = [sum(ci * D[t][i] for t, ci in enumerate(c)) for i in range(len(Jl))]
        wd = sum(abs(li) * Ji for li, Ji in zip(l, Jl))
        if best is None or wd < best[0]:
            best = (wd, l)
    return best

def coset_hollow(itin, S0, T, eps, Ld):
    """exact: does v+Lambda meet the open box (physical x_i in J_i)? Returns a hit or None."""
    g = len(itin[1])
    p, x0, u0, sig = coset_point(itin, S0, T, eps, [0] * (g + 1))
    # box in u coordinates
    lo, hi = [], []
    for i, (_, J, _) in enumerate(itin[1]):
        s = sig[i + 1]
        a, b = (J[0], J[1]) if s == 1 else (-J[1], -J[0])
        lo.append(a); hi.append(b)
    Bv = Ld['basis']
    Bmat = [[Bv[j][i] for j in range(g)] for i in range(g)]
    Bi = inv(Bmat)
    # bounding box for c: c = Bi (u - u0)
    corners = list(itertools.product(*[(lo[i], hi[i]) for i in range(g)]))
    cr = []
    for t in range(g):
        vals = [sum(Bi[t][i] * (cn[i] - u0[i]) for i in range(g)) for cn in corners]
        cr.append(range(math.floor(min(vals)), math.ceil(max(vals)) + 1))
    n = 0
    for c in itertools.product(*cr):
        n += 1
        uu = [u0[i] + sum(c[t] * Bv[t][i] for t in range(g)) for i in range(g)]
        if all(lo[i] < uu[i] < hi[i] for i in range(g)):
            return uu
    return None

# ---------------------------------------------------------------- driver
def run_room(name, V, S0, T, gmax, Kr, log, trace_gmax=99, keep=None):
    t0 = time.process_time()
    refl, area = check_room(V)
    ys, S = slabs(V)
    assert interior(V, S0) and interior(V, T)
    its = itineraries(V, S0, T, gmax)
    log(f"\n## {name}: {len(V)} walls, {refl} reflexes, area {area}, S={S0}, T={T}, levels {ys}")
    log(f"itineraries with g<={gmax}: {len(its)}")
    tot = dict(A=0, B=0, AnotB=0, BnotA_boundary=0, BnotA_dup=0, BnotA_bad=0, deriv_bad=0,
               lemma1_bad=0, flat_bad=0, hollow=0, certified=0, univ=0, univ_long=0)
    summaries = []
    for it in its:
        visits, events = it
        g = len(events)
        # direction: if S strictly inside, which way? infer from first event level or T
        if g > 0:
            vy = 1 if events[0][0] > S0[1] else -1
        else:
            vy = 1 if T[1] > S0[1] else -1
        H = sum(vh for _, vh in visits)
        if H == 0:
            continue
        if keep is not None and g > trace_gmax and not keep(events):
            continue
        Apts, Bpts, Bbd, Bx = set(), set(), set(), {}
        rng = range(-Kr[g], Kr[g] + 1) if g in Kr else range(-1, 2)
        Phi = phi_matrix(it)[0] if g else []
        for eps in itertools.product((0, 1), repeat=g + 1):
            for k in itertools.product(rng, repeat=g + 1):
                p, x, u, sig = coset_point(it, S0, T, eps, list(k))
                A = in_open_box(it, x)
                # derivative check against the note's formula, once per eps at k=0
                if g and not any(k):
                    for j in range(g + 1):
                        kk = [0] * (g + 1); kk[j] = 1
                        _, _, u1, _ = coset_point(it, S0, T, eps, kk)
                        for i in range(g):
                            if u1[i] - u[i] != Phi[i][j]:
                                tot['deriv_bad'] += 1
                st, ev, Q = trace(V, S0, T, p, vy, H, ys)
                fo, onb = follows(it, ev) if st == 'ok' else (False, False)
                B = st == 'ok' and fo and Q == (T[0], T[1])
                if A:
                    tot['A'] += 1; Apts.add(p)
                    if not B:
                        tot['AnotB'] += 1
                        log(f"  SOUNDNESS FAIL {events} eps={eps} k={k} p={p} st={st}")
                if B:
                    tot['B'] += 1
                    if onb:
                        Bbd.add(p)
                    else:
                        Bpts.add(p); Bx[p] = [e[1] for e in ev]
        def wide_hit(p):
            # recover windings from the traced event abscissas: k_j must be integral
            xs = [F(S0[0])] + Bx[p]
            for eps in itertools.product((0, 1), repeat=g + 1):
                sig = [1]
                for e in eps:
                    sig.append(sig[-1] * (1 if e == 0 else -1))
                us = [sig[i] * xs[i] for i in range(g + 1)] + [sig[g + 1] * T[0]]
                k = []
                for j in range(g + 1):
                    sl = visits[j][0]; wj = sl[4] - sl[3]
                    cj = 0 if eps[j] == 0 else 2 * sig[j] * sl[3]
                    kj = (us[j] + p * visits[j][1] - cj - us[j + 1]) / (2 * wj)
                    if kj.denominator != 1:
                        break
                    k.append(int(kj))
                else:
                    pp, x, _, _ = coset_point(it, S0, T, eps, k)
                    if pp == p and in_open_box(it, x):
                        return True
            return False
        for p in Bpts - Apts:
            if wide_hit(p):
                tot['BnotA_dup'] += 1
                continue
            tot['BnotA_bad'] += 1
            log(f"  MISSED (not boundary) itinerary {[(e[0], e[2]) for e in events]} p={p}")
        tot['BnotA_boundary'] += len(Bbd - Apts)
        for p in sorted(Bbd - Apts)[:2]:
            log(f"  boundary-smooth legal chord missed by open box: events {[(e[0], e[1], e[2]) for e in events]} p={p}")
        if g == 0:
            continue
        Ld = lattice_data(it)
        if not (Ld['lemma1_in'] and Ld['lemma1_cov']):
            tot['lemma1_bad'] += 1
            log(f"  LEMMA 1 MISMATCH {events}")
        mw = min_width(it, Ld['dual'])
        hol = []
        for eps in itertools.product((0, 1), repeat=g + 1):
            hit = coset_hollow(it, S0, T, eps, Ld)
            hol.append(hit is None)
        allhollow = all(hol)
        flt = 1.0 if g == 1 else (FLT2 if g == 2 else float(g))  # g>=3: lower bound g only
        if any(hol):
            tot['hollow'] += 1
            if float(mw[0]) > flt and g <= 2:
                tot['flat_bad'] += 1
                log(f"  LEMMA 2 VIOLATION {events} minwidth={mw[0]}")
        if g <= 2 and float(mw[0]) > flt:
            tot['certified'] += 1
        # universal relations: repeated full-height visits
        for j1 in range(g + 1):
            for j2 in range(j1 + 1, g + 1):
                if visits[j1][0] == visits[j2][0] and visits[j1][1] == visits[j2][1]:
                    n = [0] * (g + 1); n[j1] = 1; n[j2] = -1
                    w = Ld['w']
                    l = [F(n[i - 1], 2 * w[i - 1]) - F(n[i], 2 * w[i]) for i in range(1, g + 1)]
                    wd = sum(abs(li) * (J[1] - J[0]) for li, (_, J, _) in zip(l, events))
                    tot['univ'] += 1
                    if wd > 2:
                        tot['univ_long'] += 1
        summaries.append((events, g, Ld, mw, hol, len(Apts), len(Bbd - Apts)))
    tot['cpu'] = round(time.process_time() - t0, 2)
    log("totals: " + ", ".join(f"{k}={v}" for k, v in tot.items()))
    return summaries, tot

def fmt_it(events):
    return " ".join(f"{e[2]}@{e[0]}{tuple(e[1])}" for e in events)

if __name__ == "__main__":
    out = []
    def log(s):
        print(s); out.append(s)
    T0 = time.process_time()
    grand = {}
    # seven-cell room
    V7 = [(1, 0), (3, 0), (3, 2), (2, 2), (2, 3), (0, 3), (0, 1), (1, 1)]
    s7, t7 = run_room("seven-cell room", V7, (1, 2), (2, 1), 4, {1: 3, 2: 2, 3: 1, 4: 1}, log)
    for ev, g, Ld, mw, hol, nA, nbd in s7:
        log(f"  g={g} {fmt_it(ev)} | mu={[str(m) for m in Ld['mu']]} covol={Ld['covol']} minwidth={mw[0]} "
            f"(l={[str(x) for x in mw[1]]}) hollow-cosets={sum(hol)}/{len(hol)} chords(k-range)={nA}")
    # parabola family
    for (m, u) in [(3, 5), (3, 12), (4, 7), (6, 20), (10, 30)]:
        tiers = [(-1, 0, -2, 1), (0, m, -1, 1), (m, u - 1, 0, m), (u - 1, u, 0, m + 2), (u, u + 1, 0, m + 3)]
        V = room_from_tiers(tiers)
        roofp = lambda ev, m=m, u=u: [e[0] for e in ev] == [m, u - 1, u, u + 1]
        sp, tp = run_room(f"parabola m={m} u={u}", V, (0, 0), (m, u), 4, {1: 2, 2: 2, 3: 1, 4: 1}, log, 2, roofp)
        for ev, g, Ld, mw, hol, nA, nbd in sp:
            if ev[0][2] == 'T' and ev[0][0] == m and all(e[2] == 'T' for e in ev) or (len(ev) == 4 and ev[0][0] == m and ev[-1][2] == 'R'):
                log(f"  g={g} {fmt_it(ev)} | mu={[str(x) for x in Ld['mu']]} minwidth={float(mw[0]):.4f} "
                    f"l={[str(x) for x in mw[1]]} hollow-cosets={sum(hol)}/{len(hol)} chords(k-range)={nA}")
    # six-reflex locked gate
    for (a, t, Bq) in [(1, 1, 1), (1, 1, 18), (1, 2, 3)]:
        b = a + Bq; D = b + a
        tiers = [(-a, 0, 0, 20 * t), (0, a, 0, 8 * t), (a, b, 7 * t, 17 * t), (b, D, 16 * t, 24 * t), (D, D + 3 * a, 16 * t, 25 * t)]
        V = room_from_tiers(tiers)
        roofs = lambda ev, a=a, b=b, D=D: [e[0] for e in ev] == [a, b, D, D + 3 * a]
        ss, ts = run_room(f"six-reflex a={a} t={t} B={Bq}", V, (7 * t, 0), (20 * t, D), 4, {1: 1, 2: 2, 3: 1, 4: 1}, log, 2, roofs)
        for ev, g, Ld, mw, hol, nA, nbd in ss:
            mono = [e[0] for e in ev] == [a, b] and all(e[2] == 'T' for e in ev)
            roof = [e[0] for e in ev] == [a, b, D, D + 3 * a]
            if mono or roof:
                log(f"  g={g} {fmt_it(ev)} | mu={[str(x) for x in Ld['mu']]} minwidth={float(mw[0]):.4f} "
                    f"l={[str(x) for x in mw[1]]} hollow-cosets={sum(hol)}/{len(hol)} chords(k-range)={nA}")
    log(f"\nTOTAL CPU {time.process_time() - T0:.1f}s")
    open(__file__.replace('gatebox.py', 'gatebox.log'), 'w').write("\n".join(out) + "\n")
