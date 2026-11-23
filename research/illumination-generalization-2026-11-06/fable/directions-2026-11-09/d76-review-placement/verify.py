"""D76 independent referee check of qclass-closure/bbbb/placement.md.

Reads room geometry from the D58 builder only (resonant(..., 'double')).
Everything else is own code: column extraction, lattice basis by integer
row reduction with tracked coefficients, counting, the k >= 16 rounding
construction, and a cell-walking exact billiard tracer.
Usage: python3 -B verify.py > verify.log
"""
import os, sys, time, resource
from fractions import Fraction as F
from math import gcd, floor

resource.setrlimit(resource.RLIMIT_CPU, (480, 480))
HERE = os.path.dirname(os.path.abspath(__file__))
D58 = os.path.join(HERE, '..', 'd58-corridor-limit')
os.chdir(D58); sys.path.insert(0, D58)
from tests_lib import resonant          # builder only
from door_geom import DOOR

T0 = time.process_time()


def lcm_den(vals):
    d = 1
    for v in vals: d = d * v.denominator // gcd(d, v.denominator)
    return d


# ---------------------------------------------------------------- geometry
def build(item, k):
    try: r, g, info = resonant(*item, k, 'double')
    except AssertionError: return None
    return r, g, info


def columns(r, S, T):
    """Columns crossed by a path monotone in x from S to T; each is
    (x0, x1, bottom, top). Asserts the column is one contiguous vertical run."""
    xs = [S[0]] + [x for x in r.xs if S[0] < x < T[0]] + [T[0]]
    out = []
    for x0, x1 in zip(xs, xs[1:]):
        ci = max(i for i in range(len(r.xs) - 1) if r.xs[i] <= x0)
        assert r.xs[ci + 1] >= x1
        rows = sorted(j for (i, j) in r.cells if i == ci)
        assert rows == list(range(rows[0], rows[-1] + 1)), ('not full', ci, rows)
        out.append((x0, x1, r.ys[rows[0]], r.ys[rows[-1] + 1], ci))
    assert out[0][2] < S[1] < out[0][3] and out[-1][2] < T[1] < out[-1][3]
    return out


def lattice(cols, S, T):
    """Seam heights y = c + sum m_j G_j (positive-orientation sheet)."""
    d = [x1 - x0 for x0, x1, *_ in cols]; X = sum(d)
    P = [2 * (t - b) for _, _, b, t, _ in cols]
    r = len(cols) - 1
    cum = [sum(d[:i + 1]) for i in range(r)]
    c = [S[1] + cum[i] / X * (T[1] - S[1]) for i in range(r)]
    G = [[P[j] * (cum[i] / X - (1 if j <= i else 0)) for i in range(r)] for j in range(len(cols))]
    box = [(max(cols[i][2], cols[i + 1][2]), min(cols[i][3], cols[i + 1][3])) for i in range(r)]
    return c, G, box, P, d, X


def heights(S, T, d, P, m):
    """Own forward formula: slope and physical seam heights for indices m."""
    X = sum(d)
    s = (T[1] - S[1] + sum(p * mm for p, mm in zip(P, m))) / X
    y, out = S[1], []
    for j in range(len(d) - 1):
        y = y + d[j] * s - P[j] * m[j]
        out.append(y)
    return s, out


# ------------------------------------------------------- lattice and count
def reduce_rows(rows, coef, col):
    """Euclid on column col among rows (with coefficient vectors). Returns
    (pivot_row, pivot_coef, remaining rows/coefs with zero in col)."""
    rows = [list(x) for x in rows]; coef = [list(x) for x in coef]
    while True:
        nz = [i for i in range(len(rows)) if rows[i][col] != 0]
        if len(nz) <= 1: break
        i = min(nz, key=lambda t: abs(rows[t][col]))
        for jdx in nz:
            if jdx == i: continue
            q = rows[jdx][col] // rows[i][col]
            rows[jdx] = [a - q * b for a, b in zip(rows[jdx], rows[i])]
            coef[jdx] = [a - q * b for a, b in zip(coef[jdx], coef[i])]
    nz = [i for i in range(len(rows)) if rows[i][col] != 0]
    i = nz[0]
    if rows[i][col] < 0: rows[i] = [-a for a in rows[i]]; coef[i] = [-a for a in coef[i]]
    rest = [(rows[t], coef[t]) for t in range(len(rows)) if t != i]
    return rows[i], coef[i], [x for x, _ in rest], [y for _, y in rest]


def floor_sum(n, m, a, b):
    """sum_{i=0}^{n-1} floor((a i + b)/m), m > 0 (ACL-style)."""
    ans = 0
    while True:
        if a >= m or a < 0: q = a // m; ans += q * n * (n - 1) // 2; a -= q * m
        if b >= m or b < 0: q = b // m; ans += q * n; b -= q * m
        y = a * n + b
        if y < m: return ans
        n, b, m, a = y // m, y % m, a, m


def count_and_point(c, G, box):
    Q = lcm_den([x for row in G for x in row] + c + [v for bx in box for v in bx])
    Gi = [[int(x * Q) for x in row] for row in G]
    ci = [int(x * Q) for x in c]
    bi = [(int(l * Q), int(u * Q)) for l, u in box]
    n = len(Gi)
    eye = [[int(i == j) for j in range(n)] for i in range(n)]
    v1, m1, rest, rc = reduce_rows(Gi, eye, 0)
    g = v1[0]
    (L1, U1) = bi[0]
    i0 = (L1 - ci[0]) // g + 1; i1 = -((ci[0] - U1) // g) - 1      # c+g i in (L1,U1)
    if len(c) == 1:
        cnt = max(0, i1 - i0 + 1)
        if cnt == 0: return 0, None
        i = (i0 + i1) // 2
        return cnt, [i * a for a in m1]
    v2, m2, _, _ = reduce_rows(rest, rc, 1)
    H, t = v2[1], v1[1] % v2[1]
    shift = (v1[1] - t) // H
    m1 = [a - shift * b for a, b in zip(m1, m2)]          # now v1 = (g, t)
    L2, U2 = bi[1]
    N = i1 - i0 + 1
    if N <= 0: return 0, None
    # count l with L2 < c2 + t i + H l < U2  ->  floor((U2-1-c2-t i)/H) - floor((L2-c2-t i)/H)
    if N <= 400000:
        cnt = 0
        for i in range(i0, i1 + 1):
            base = ci[1] + t * i
            cnt += (U2 - 1 - base) // H - (L2 - base) // H
    else:
        A = -t; B1 = U2 - 1 - ci[1] - t * i0; B2 = L2 - ci[1] - t * i0
        cnt = floor_sum(N, H, A, B1) - floor_sum(N, H, A, B2)
    # one explicit point: middle first coordinate, middle admissible l
    i = (i0 + i1) // 2
    while True:
        base = ci[1] + t * i
        lo, hi = (L2 - base) // H + 1, (U2 - 1 - base) // H
        if lo <= hi: break
        i += 1
    l = (lo + hi) // 2
    return cnt, [i * a + l * b for a, b in zip(m1, m2)]


def shorten(m, G):
    """Add the integer kernel vector to reduce |m| (pure rounding)."""
    if len(m) != 3: return m
    Q = lcm_den([x for row in G for x in row])
    Gi = [[int(x * Q) for x in row] for row in G]
    # kernel of 3 vectors in Z^2: cross products of columns
    kx = [Gi[1][0] * Gi[2][1] - Gi[2][0] * Gi[1][1],
          Gi[2][0] * Gi[0][1] - Gi[0][0] * Gi[2][1],
          Gi[0][0] * Gi[1][1] - Gi[1][0] * Gi[0][1]]
    gk = gcd(gcd(kx[0], kx[1]), kx[2]); kx = [a // gk for a in kx]
    j = max(range(3), key=lambda t: abs(kx[t]))
    q = round(F(-m[j], kx[j]))
    return [a + q * b for a, b in zip(m, kx)]


# ---------------------------------------------------------------- tracer
def trace(r, S, vec, T, cap=400000):
    """Cell-walking billiard tracer. Fails on any pass through a grid point
    unless all four cells around it are in the room. Returns (ok, nref, why)."""
    xs, ys, cells = r.xs, r.ys, r.cells
    x, y = S; dx, dy = vec; rem = F(1)
    ci = max(i for i in range(len(xs) - 1) if xs[i] < x)
    cj = max(j for j in range(len(ys) - 1) if ys[j] < y or (ys[j] == y and dy > 0))
    assert (ci, cj) in cells and xs[ci] < x < xs[ci + 1] and ys[cj] <= y < ys[cj + 1] or y == ys[cj + 1]
    if y in ys: assert (ci, cj - (1 if y == ys[cj] else -1)) in cells, 'start on wall'
    nref = 0
    while True:
        tx = ((xs[ci + 1] if dx > 0 else xs[ci]) - x) / dx
        ty = ((ys[cj + 1] if dy > 0 else ys[cj]) - y) / dy
        t = min(tx, ty)
        if t >= rem:
            x, y = x + rem * dx, y + rem * dy
            return (x, y) == T, nref, ('end' if (x, y) == T else f'miss {float(x)},{float(y)}')
        x, y = x + t * dx, y + t * dy; rem -= t
        sx = 1 if dx > 0 else -1; sy = 1 if dy > 0 else -1
        if tx == ty:
            gx_, gy_ = (ci + (1 if sx > 0 else 0)), (cj + (1 if sy > 0 else 0))
            around = [(gx_ - 1, gy_ - 1), (gx_, gy_ - 1), (gx_ - 1, gy_), (gx_, gy_)]
            if not all(a in cells for a in around): return False, nref, f'grid point {x},{y}'
            ci += sx; cj += sy; continue
        if tx < ty:
            if (ci + sx, cj) in cells: ci += sx
            else: dx = -dx; nref += 1
        else:
            if (ci, cj + sy) in cells: cj += sy
            else: dy = -dy; nref += 1
        if nref > cap: return False, nref, 'cap'


def check_path(r, S, T, cols, m, box):
    d = [x1 - x0 for x0, x1, *_ in cols]; P = [2 * (t - b) for _, _, b, t, _ in cols]
    s, ys_ = heights(S, T, d, P, m)
    inside = all(l < v < u for v, (l, u) in zip(ys_, box))
    vec = (T[0] - S[0], s * sum(d))
    ok, nref, why = trace(r, S, vec, T)
    return inside, ok, nref, why, s


# ---------------------------------------------------------------- main
CLAIM = {}
for line in open(os.path.join(HERE, '..', '..', '..', '..', 'qclass-closure', 'bbbb', 'placement.txt')):
    head, tail = line.rsplit(')', 1)
    CLAIM[head + ')'] = tail.split()

print('# Part A: k = 2..15 own counts vs placement.txt; explicit traced path per instance')
mism = 0; traced = 0; tr_ok = 0
for item in DOOR:
    key = str(item); row = []
    for k in range(2, 16):
        b = build(item, k)
        if b is None: row.append('-'); continue
        r, g, info = b
        S, T = g[5], g[6]
        if 2 * (T[1] - g[4]) != info['ell']: row.append('outside'); continue
        cols = columns(r, S, T)
        c, G, box, P, d, X = lattice(cols, S, T)
        cnt, m = count_and_point(c, G, box)
        row.append(str(cnt))
        m = shorten(m, G) if cnt > 0 else None
        if cnt > 0 and k in (2, 3, 6, 7, 9, 12, 15) and sum(abs(p_ * x) for p_, x in zip(P, m)) / min(P) < 150000:
            inside, ok, nref, why, s = check_path(r, S, T, cols, m, box)
            traced += 1; tr_ok += inside and ok
            print(f'  trace {key} k={k} m={m} inside={inside} ok={ok} refl={nref} {why}')
    same = row == CLAIM[key]
    mism += not same
    print(key, ' '.join(row), 'MATCH' if same else f'DIFF claim={CLAIM[key]}')
print(f'Part A: {mism} rows differ; traced {tr_ok}/{traced} valid')

print('\n# Part B: k >= 16 argument, exact arithmetic')
for k in (16, 17, 20, 30, 41):
    n = 2 ** (k - 2)
    j = round(F(n, 6) - F(7, 80)); i = round(F(j, 2) + F(1, 160))
    assert n % 12 in (4, 8) and j % 2 == 1 and i == (j + 1) // 2
    for item in DOOR:
        b = build(item, k)
        if b is None: print(k, item, 'BUILDER FAILS'); continue
        r, g, info = b
        S, T = g[5], g[6]
        if 2 * (T[1] - g[4]) != info['ell']: print(k, item, 'outside'); continue
        w = F(1, 2 ** k)
        p, u = g[2], S[0]
        assert p == (F(14, 5) + 32 * j) * w and u == (F(6, 5) + 32 * i) * w, 'p,u formula'
        cols = columns(r, S, T)
        c, G, box, P, d, X = lattice(cols, S, T)
        cc = d[-1]; assert cc == w / 20
        assert X / cc == 33 + 320 * (j - 1) and X / cc > 800000
        widths = [u_ - l_ for l_, u_ in box]; assert min(widths) >= 2
        ctr = [(l_ + u_) / 2 for l_, u_ in box]
        if len(cols) == 2:
            m1 = round((c[0] - ctr[0]) / (P[0] * cc / X)); m = [m1, 0]
            s, ys_ = heights(S, T, d, P, m)
            err = [abs(ys_[0] - ctr[0])]; bound_ok = err[0] <= P[0] * cc / (2 * X)
            per = (P[0],)
        else:
            a_, b_ = d[0], d[1]
            assert b_ == p / 16 and a_ == 15 * p / 16 - u and a_ == 7 * b_ - 316 * cc
            assert 8 * a_ - 7 * X == -323 * cc
            P1, P2 = P[0], P[1]
            # least positive common multiple of P1, P2
            M = next(F(t) * P1 for t in range(1, 1000) if (F(t) * P1 / P2).denominator == 1)
            assert M <= 150 and P1 <= F(17, 2)
            Lf = lambda ys_: 8 * ys_[0] - 323 * ys_[1]
            Lstar = 8 * ctr[0] - 323 * ctr[1]
            _, y0 = heights(S, T, d, P, [0, 0, 0])
            _, y1_ = heights(S, T, d, P, [1, 0, 0])
            assert Lf(y1_) - Lf(y0) == -P1
            m1 = round((Lf(y0) - Lstar) / P1)
            step = [7 * M / P1, M / P2, 0]; assert all(F(v).denominator == 1 for v in step)
            step = [int(v) for v in step]
            _, ya = heights(S, T, d, P, [m1, 0, 0])
            _, yb = heights(S, T, d, P, [m1 + step[0], step[1], 0])
            assert yb[0] - ya[0] == -323 * M * cc / X and Lf(yb) == Lf(ya)
            tt = round((ya[0] - ctr[0]) / (323 * M * cc / X))
            m = [m1 + tt * step[0], tt * step[1], 0]
            s, ys_ = heights(S, T, d, P, m)
            err = [abs(ys_[0] - ctr[0]), abs(ys_[1] - ctr[1])]
            bound_ok = err[0] <= 323 * M * cc / (2 * X) and err[1] <= (P1 / 2 + 8 * 323 * M * cc / (2 * X)) / 323
            per = (P1, P2, M)
        inside = all(l_ < v < u_ for v, (l_, u_) in zip(ys_, box))
        msg = f'{k} {item} cols={len(cols)} per={tuple(map(str, per))} widths={[str(x) for x in widths]} err={[round(float(e), 5) for e in err]} bounds={bound_ok} inside={inside} m={m}'
        if k in (16, 17, 20):
            ok, nref, why = trace(r, S, (T[0] - S[0], s * X), T)
            msg += f' traced={ok} refl={nref} {why}'
        print(msg)
print('cpu', round(time.process_time() - T0, 1))
