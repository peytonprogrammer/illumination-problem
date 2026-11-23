"""D84: independent check of qclass-closure/bbbb/adjacent-cylinders.md and convex-cylinder.md.

Own code, exact Fractions. Does not use cyl.py's SL2 action, tau propagation or tracer.
The rim of the room-double cylinder is read by tracing an offset billiard ray (offset eta
toward the adjacent lattice leaf) and recording, at integer and half-integer times, the
nearest lattice / half-lattice point of Q. Paths are checked with an own billiard tracer.
Only named rooms, the named U2 stretch family and saved data are used.
"""
from fractions import Fraction as F
from math import floor, ceil, gcd
from itertools import product, combinations
from pathlib import Path
import io, runpy, sys, time
from contextlib import redirect_stdout

ETA = F(1, 1000003)


def incid(cells, p):
    return sum((p[0] + a, p[1] + b) in cells for a, b in product((-1, 0), repeat=2))


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def U2(k=0):
    base = rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7)
    return {(x + (4 * k if x >= 4 else 0), y) for x, y in base} | rect(4, 4 + 4 * k, 0, 2)


# ---------------------------------------------------------------- room checks
def room_facts(cells):
    pts = {(x + a, y + b) for x, y in cells for a, b in product((0, 1), repeat=2)}
    # strictly simple: cells connected, no holes, no pinch (diagonal incid-2) points
    def comps(S, nb):
        S = set(S); n = 0
        while S:
            n += 1; todo = [S.pop()]
            while todo:
                c = todo.pop()
                for d in nb:
                    e = (c[0] + d[0], c[1] + d[1])
                    if e in S: S.remove(e); todo.append(e)
        return n
    four = ((1, 0), (-1, 0), (0, 1), (0, -1))
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    box = rect(min(xs) - 1, max(xs) + 2, min(ys) - 1, max(ys) + 2)
    pinch = [p for p in pts if incid(cells, p) == 2 and
             ((p[0] - 1, p[1] - 1) in cells) == ((p[0], p[1]) in cells)]
    simple = comps(cells, four) == 1 and comps(box - cells, four) == 1 and not pinch
    corners = [p for p in pts if incid(cells, p) in (1, 3)]
    reflex = sorted(p for p in corners if incid(cells, p) == 3)
    # wall lengths: maximal boundary segments between corners
    hor, ver = [], []
    for p in corners:
        for d, out in (((1, 0), hor), ((0, 1), ver)):
            q, L = p, 0
            def edge(q):  # unit boundary edge from q in direction d
                if d == (1, 0):
                    return ((q[0], q[1] - 1) in cells) != ((q[0], q[1]) in cells)
                return ((q[0] - 1, q[1]) in cells) != ((q[0], q[1]) in cells)
            while edge(q):
                q = (q[0] + d[0], q[1] + d[1]); L += 1
                if incid(cells, q) in (1, 3): break
            if L: out.append(L)
    g = lambda a: __import__('functools').reduce(gcd, a)
    interior = [p for p in pts if incid(cells, p) == 4]
    smooth = [p for p in pts if incid(cells, p) == 2]
    classes = {(p[0] % 2, p[1] % 2) for p in interior + smooth}
    return dict(simple=simple, walls=len(corners), r=len(reflex), reflex=reflex, area=len(cells),
                normalized=(g(hor) == 1 and g(ver) == 1), hor=sorted(hor), ver=sorted(ver),
                all4=len(classes) == 4, interior=interior)


def on_boundary(cells, p):
    x, y = p
    if x.denominator == 1 and y.denominator == 1:
        return incid(cells, (int(x), int(y))) != 4
    if x.denominator == 1:
        cy = floor(y); return ((int(x) - 1, cy) in cells) != ((int(x), cy) in cells)
    if y.denominator == 1:
        cx = floor(x); return ((cx, int(y) - 1) in cells) != ((cx, int(y)) in cells)
    return False


# ---------------------------------------------------------------- billiard tracer
class Corner(Exception):
    pass


def run(cells, p, v, T, samples=()):
    """Billiard flow from p with velocity v for time T. Returns (p, v, side, recs).
    recs[t] = (point, velocity, side) at each sample time t. Raises Corner on a corner."""
    x, y = F(p[0]), F(p[1]); vx, vy = F(v[0]), F(v[1]); side = 1
    t = F(0); recs = {}; samples = sorted(set(map(F, samples)))
    # starting cell: the one entered along v (p may lie on grid lines)
    def cell():
        cx = floor(x) if not (x.denominator == 1 and vx < 0) else int(x) - 1
        cy = floor(y) if not (y.denominator == 1 and vy < 0) else int(y) - 1
        return cx, cy
    if vx == 0 or vy == 0:
        return run_axial(cells, p, v, T, samples)
    c = cell(); assert c in cells, ('start leaves room', p, v)
    si = 0
    while True:
        nx = floor(x) + 1 if vx > 0 else ceil(x) - 1
        ny = floor(y) + 1 if vy > 0 else ceil(y) - 1
        tx, ty = (nx - x) / vx, (ny - y) / vy
        dt = min(tx, ty)
        while si < len(samples) and samples[si] <= t + dt and samples[si] <= T:
            s = samples[si]; recs[s] = ((x + vx * (s - t), y + vy * (s - t)), (vx, vy), side); si += 1
        if t + dt >= T:
            x += vx * (T - t); y += vy * (T - t)
            return (x, y), (vx, vy), side, recs
        x += vx * dt; y += vy * dt; t += dt
        sx, sy = (1 if vx > 0 else -1), (1 if vy > 0 else -1)
        if tx == ty:  # lattice point
            k = incid(cells, (int(x), int(y)))
            if k in (1, 3): raise Corner((x, y))
            a, b, d = (c[0] + sx, c[1]) in cells, (c[0], c[1] + sy) in cells, (c[0] + sx, c[1] + sy) in cells
            if k == 4: c = (c[0] + sx, c[1] + sy)
            elif a and not b and not d: vy = -vy; side = -side; c = (c[0] + sx, c[1])
            elif b and not a and not d: vx = -vx; side = -side; c = (c[0], c[1] + sy)
            else: raise AssertionError('pinch')
        elif tx < ty:
            if (c[0] + sx, c[1]) in cells: c = (c[0] + sx, c[1])
            else: vx = -vx; side = -side
        else:
            if (c[0], c[1] + sy) in cells: c = (c[0], c[1] + sy)
            else: vy = -vy; side = -side


def run_axial(cells, p, v, T, samples):
    """Axis-parallel path from a lattice point along a grid line (unit lattice steps).
    Fails (Corner) on a corner or if it would run along a wall."""
    sw = v[0] == 0  # moving vertically
    a, b = (p[1], p[0]) if sw else (p[0], p[1])     # a: moving coordinate, b: fixed
    va = v[1] if sw else v[0]
    assert all(F(z).denominator == 1 for z in p) and F(va).denominator == 1
    pt = lambda A: ((F(b), F(A)) if sw else (F(A), F(b)))
    inc = lambda A: incid(cells, (int(b), int(A)) if sw else (int(A), int(b)))
    def seg_ok(A, s):  # unit segment from A in direction s: both side cells in room
        lo = A if s > 0 else A - 1
        cs = [(b - 1, lo), (b, lo)] if sw else [(lo, b - 1), (lo, b)]
        k = sum(c in cells for c in cs)
        if k == 1: raise Corner(('along wall', pt(A)))
        return k == 2
    side = 1; s = 1 if va > 0 else -1; A = int(a); steps = abs(int(va)); recs = {}
    for q in range(steps + 1):
        tq = F(q, steps)
        for smp in samples:
            if smp == tq: recs[smp] = (pt(A), (0, s) if sw else (s, 0), side)
        if q == steps: break
        if q > 0 and inc(A) in (1, 3): raise Corner(pt(A))
        if not seg_ok(A, s):
            s = -s; side = -side
            if not seg_ok(A, s): raise AssertionError('stuck')
        A += s
    for smp in samples:
        assert smp in recs or smp.denominator != 1 and (smp * steps).denominator != 1, 'non-lattice sample on axial path'
    return pt(A), ((0, s) if sw else (s, 0)), side, recs


def qkey(cells, pt, side):
    return (pt, 0) if on_boundary(cells, pt) else (pt, side)


def half_round(z):
    return F(round(2 * z), 2)


# ---------------------------------------------------------------- rim walk on Q
def rim(cells, L, v, w, sign, n):
    """Offset ray from L + sign*eta*w with velocity v. Returns the rim walk of the lattice
    tree through L as seen from the band toward L + sign*w."""
    start = (L[0] + sign * ETA * w[0], L[1] + sign * ETA * w[1])
    N = 4 * n + 4  # longer than any rim
    _, _, _, recs = run(cells, start, v, N, [F(k, 2) for k in range(2 * N + 1)])
    v0 = (F(v[0]), F(v[1]))
    keys, vel = [], []
    for k in range(2 * N + 1):
        (x, y), vv, side = recs[F(k, 2)]
        if k % 2 == 0:
            pt = (F(round(x)), F(round(y)))
        else:
            pt = (half_round(x), half_round(y))
        assert max(abs(pt[0] - x), abs(pt[1] - y)) <= ETA * (abs(w[0]) + abs(w[1]))
        keys.append(qkey(cells, pt, side)); vel.append(vv)
    C = next(c for c in range(1, N) if keys[2 * c] == keys[0] and vel[2 * c + 1] == vel[1] and keys[2 * c + 1] == keys[1])
    lat = [keys[2 * t] for t in range(C)]
    mid = [keys[2 * t + 1] for t in range(C)]
    # band frame on the unit (t, t+1): velocity at the half time (no wall event there)
    R = [(vel[2 * t + 1][0] / v0[0], vel[2 * t + 1][1] / v0[1]) for t in range(C)]
    return C, lat, mid, R


def tree_edges(cells, C, lat, mid):
    occ = {}
    for t, K in enumerate(mid): occ.setdefault(K, []).append(t)
    assert all(len(o) == 2 for o in occ.values()), 'unit segment not traversed exactly twice'
    pair = {}
    for a, b in occ.values():
        assert lat[a] == lat[(b + 1) % C] and lat[(a + 1) % C] == lat[b], 'not reversed'
        pair[a], pair[b] = b, a
    V = set(lat); E = len(occ)
    is_tree = (E == len(V) - 1)
    corner = [incid(cells, (int(p[0]), int(p[1]))) in (1, 3) for p, _ in lat]
    verts = [t for t in range(C) if corner[t]]
    edges = []
    for i, j in zip(verts, verts[1:] + [verts[0] + C]):
        m = pair[i % C] + 1
        for t in range(i, j):
            assert (pair[t % C] + 1) % C == (m - (t - i)) % C, 'edge occurrence not paired as a whole'
        leaf = any(incid(cells, (int(lat[q % C][0][0]), int(lat[q % C][0][1]))) == 1 for q in (i, j))
        edges.append((i, j, m, leaf))
    nref = sum(incid(cells, (int(p[0]), int(p[1]))) == 3 for p, _ in set(lat))
    nconv = sum(incid(cells, (int(p[0]), int(p[1]))) == 1 for p, _ in set(lat))
    return edges, pair, is_tree, nref, nconv


def covers(C, edges):
    """Union of open arcs (i-m, i-m+2(j-i)) mod C must contain (0, C). Exact interval merge."""
    pieces = []
    for i, j, m, _ in edges:
        a, L = (i - m) % C, 2 * (j - i)
        if L > C: return True  # an open arc longer than the circle covers it
        pieces.append((a, min(a + L, C)))
        if a + L > C: pieces.append((0, a + L - C))
    pieces.sort()
    reach = 0  # (0, reach) is covered; the difference 0 is not required
    for lo, hi in pieces:
        if lo < reach or lo == 0:
            reach = max(reach, hi)
        else:
            return False  # the point `reach` (or more) is uncovered
    return reach >= C


def gaps(C, edges):
    """Uncovered nonzero half-integer differences (for reporting failures)."""
    out = []
    for t2 in range(1, 2 * C):
        if not any(0 < (t2 - 2 * ((i - m) % C)) % (2 * C) < 4 * (j - i) for i, j, m, _ in edges):
            out.append(F(t2, 2))
    return out


def bezout(v):
    p, q = v
    cand = [(a, b) for a, b in product(range(-abs(q) - 1, abs(q) + 2), range(-abs(p) - 1, abs(p) + 2))
            if p * b - q * a == 1]
    return min(cand, key=lambda z: (abs(z[0]) + abs(z[1]), z))


def analyse_any(cells, v):
    """Band start: first lattice point L (sorted) for which both offset rays start inside."""
    pts = sorted({(x + a, y + b) for x, y in cells for a, b in product((0, 1), repeat=2)
                  if incid(cells, (x + a, y + b)) in (2, 4)})
    for L in pts:
        try:
            return analyse(cells, v, L)
        except AssertionError:
            continue


def analyse(cells, v, L):
    """Both rims of the band between the lattice leaves through L and L+w."""
    n = len(cells); w = bezout(v)
    bot = rim(cells, L, v, w, 1, n)
    Lw = (L[0] + w[0], L[1] + w[1])
    top = rim(cells, Lw, v, w, -1, n)
    return w, bot, top


# ---------------------------------------------------------------- path construction
def build_path(top_edges, C, s, t):
    """s, t: abscissas on the bottom walk. Returns Delta = z - s for a regular top-rim z."""
    delta = (s - t) % C
    for i, j, m, _ in top_edges:
        for q in range(-4, 6):
            z = F(delta + i + m, 2) + F(q * C, 2)
            if i < z < j:
                return z - s, (i, j, m)
    return None


def point_at(cells, bot, s, v):
    """Physical point and band frame R at bottom abscissa s (Fraction)."""
    C, lat, mid, R = bot
    t0 = floor(s); lam = s - t0
    P = lat[t0 % C][0]
    if lam == 0: return P, R[t0 % C], lat[t0 % C]
    Rt = R[t0 % C]
    end, vv, side, _ = run(cells, P, (Rt[0] * v[0], Rt[1] * v[1]), lam)
    Rs = (vv[0] / v[0], vv[1] / v[1])
    return end, Rs, None


def check_pair(cells, v, w, bot, top, tedges, tpair, s, t, up=1):
    C = bot[0]
    S, Rs, _ = point_at(cells, bot, s, v)
    T, _, _ = point_at(cells, bot, t, v)
    got = build_path(tedges, C, s, t)
    assert got, ('no edge for', s, t)
    Delta, edge = got
    D = (2 * up * w[0] + 2 * Delta * v[0], 2 * up * w[1] + 2 * Delta * v[1])
    D = (Rs[0] * D[0], Rs[1] * D[1])
    end, _, _, recs = run(cells, S, D, 1, [F(1, 2)])
    assert end == T, ('wrong end', S, T, D, end)
    return S, T, D, recs[F(1, 2)][0]


# ---------------------------------------------------------------- main
def main():
    t0 = time.process_time()
    out = []
    pr = lambda *a: (print(*a), out.append(' '.join(map(str, a))))
    v = (-1, 1)
    # tracer negative controls: hitting reflex (2,2) and convex (0,0) of U2 must raise
    for S0, D0 in (((1, 1), (2, 2)), ((1, 1), (-2, -2)), ((3, 1), (-4, 4))):
        try:
            run(U2(0), S0, D0, 1); raise SystemExit('tracer missed a corner')
        except Corner:
            pass
    pr('tracer negative controls (corner hits detected): ok')
    pr('== U2 stretches, direction', v)
    for k in range(0, 7):
        cells = U2(k); f = room_facts(cells); n = len(cells)
        L = next(p for p in sorted(f['interior']) if (p[0] + p[1]) % 2 == 0)
        w, bot, top = analyse(cells, v, L)
        res = []
        for walk in (bot, top):
            C, lat, mid, R = walk
            edges, pair, is_tree, nref, nconv = tree_edges(cells, C, lat, mid)
            res.append((C, edges, pair, is_tree, nref, nconv))
        (Cb, eb, pb, tb, rb, cb), (Ct, et, pt_, tt, rt, ct) = res
        ok = [covers(Cb, eb), covers(Ct, et)]
        assert ok == [not gaps(Cb, eb), not gaps(Ct, et)]
        lens = [sorted(j - i for i, j, _, _ in e) for e in (eb, et)]
        leafmax = [max(j - i for i, j, _, lf in e if lf) for e in (eb, et)]
        pr(f'k={k} area={f["area"]} walls={f["walls"]} r={f["r"]} reflex={f["reflex"]} simple={f["simple"]} '
           f'normalized={f["normalized"]} all4classes={f["all4"]} 2n={2*n} C=({Cb},{Ct}) '
           f'trees={tb and tt} reflex/convex per side={(rb,cb),(rt,ct)} '
           f'occurrences={len(eb)},{len(et)} pass={ok} leafmax={leafmax} lens={lens}')
        assert Cb == Ct == 2 * n and tb and tt and all(ok)
        assert len(eb) // 2 + len(et) // 2 == 2 * f['r'] + 2
        # Every same-parity interior lattice pair, via the constructed path and the tracer.
        if k in (0, 1, 3):
            nb = 0; bad = []
            for walk, other, oedges, opair, up in ((bot, top, et, pt_, 1), (top, bot, eb, pb, -1)):
                C, lat, mid, R = walk
                first = {}
                for t, (p, side) in enumerate(lat):
                    if incid(cells, (int(p[0]), int(p[1]))) == 4: first.setdefault((p, side), t)
                # representatives: one abscissa per Q-lift; pair every two distinct physical points
                reps = {}
                for (p, side), t in first.items(): reps.setdefault(p, t)
                for P, Q in combinations(sorted(reps), 2):
                    if (P[0] - Q[0]) % 2 or (P[1] - Q[1]) % 2: continue
                    S, T, D, M = check_pair(cells, v, w, walk, other, oedges, opair, F(reps[P]), F(reps[Q]), up)
                    off = M[0].denominator == M[1].denominator == 1 and ((M[0] - S[0]) % 2 or (M[1] - S[1]) % 2)
                    nb += 1
                    if not off or incid(cells, (int(M[0]), int(M[1]))) in (1, 3): bad.append((S, T, D, M))
            pr(f'   k={k}: same-parity interior lattice pairs traced via rim path: {nb}, failures {len(bad)}')
            assert not bad
            # Real (non-lattice) points on the critical graph: abscissas s+1/3, t+2/3 (fixed choice).
            C, lat, mid, R = bot
            ss = [F(3 * q + 1, 3) for q in range(0, C, 7)]
            cnt = 0
            for a, b in combinations(ss, 2):
                S, _, _ = point_at(cells, bot, a, v); T, _, _ = point_at(cells, bot, b, v)
                if S == T or on_boundary(cells, S) or on_boundary(cells, T): continue
                check_pair(cells, v, w, bot, top, et, pt_, a, b); cnt += 1
            pr(f'   k={k}: real pairs on bottom rim (abscissa = integer + 1/3) traced: {cnt}, all reach T legally')

    # Formula check of rim-trees.txt against the k-linear data, origin-free:
    # multiset of (i-m mod C, length) is invariant under shifting the origin.
    pr('== interval multisets vs rim-trees.txt formulas')
    claimed0 = [(0, 2, 0, 0, 0, 0), (2, 17, 32, 0, 4, 8), (17, 32, 17, 4, 8, 4), (32, 57, 90, 8, 12, 16),
                (57, 59, 61, 12, 12, 12), (59, 61, 59, 12, 12, 12), (61, 63, 65, 12, 12, 12),
                (63, 65, 63, 12, 12, 12), (65, 90, 57, 12, 16, 12), (90, 92, 2, 16, 16, 0)]
    claimed1 = [(5, 7, 9, 4, 4, 4), (7, 9, 7, 4, 4, 4), (9, 38, 67, 4, 8, 12), (38, 67, 38, 8, 12, 8),
                (67, 82, 5, 12, 16, 4), (82, 97, 82, 16, 20, 16)]
    for k in (0, 1, 2, 3, 5):
        cells = U2(k); C = 92 + 16 * k
        L = next(p for p in sorted(room_facts(cells)['interior']) if (p[0] + p[1]) % 2 == 0)
        w, bot, top = analyse(cells, v, L)
        mine = []
        for walk in (bot, top):
            e = tree_edges(cells, walk[0], walk[1], walk[2])[0]
            mine.append(sorted(((i - m) % C, j - i) for i, j, m, _ in e))
        theirs = []
        for cl in (claimed0, claimed1):
            ed = [(i + a * k, j + b * k, m + c * k) for i, j, m, a, b, c in cl]
            theirs.append(sorted(((i - m) % C, j - i) for i, j, m in ed))
        neg = lambda S: sorted(((-a - 2 * L) % C, L) for a, L in S)
        match = all(any(x == y for y in (t, neg(t))) for x, t in zip(sorted(mine), sorted(theirs))) or \
            all(any(x == y for y in (t, neg(t))) for x, t in zip(mine, theirs[::-1]))
        pr(f'k={k}: own rim intervals equal the stated linear formulas (up to orientation/side order): {match}')
        assert match

    # ------------------------------------------------ named rooms through saved code data
    base = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(base / 'd72-cylinder-test'))
    bbbb = base.parents[2] / 'qclass-closure' / 'bbbb'
    with redirect_stdout(io.StringIO()):
        ns = runpy.run_path(str(bbbb / 'adjacent-cylinders.py'))
    prev = ns['prev']; rooms = prev['rooms']; cylmod = prev['cyl']
    pr('== R22 controls (own rim walk)')
    R22 = set(rooms['R22'])
    fR = room_facts(R22)
    pr('R22 facts', {k: fR[k] for k in ('area', 'walls', 'r', 'simple', 'normalized')})
    for vv in ((4, 7), (7, 4)):
        w, bot, top = analyse_any(R22, vv)
        line = []
        for walk in (bot, top):
            edges, pair, is_tree, nref, nconv = tree_edges(R22, walk[0], walk[1], walk[2])
            g = gaps(walk[0], edges)
            line.append((walk[0], is_tree, nref, nconv, covers(walk[0], edges), len(g), [str(x) for x in g[:6]]))
        pr('R22', vv, 'w', w, '(C, tree, reflex, convex, pass, #gaps, first gaps):', line)

    pr('== DBas single-cylinder claim (own rim walk, Q-height 1 bands)')
    for name, cells in (('DBas', set(rooms['DBas'])),
                        ('DBas+bays(2,3)', set(rooms['DBas']) | {(x, y) for x in (1, 2) for y in (-3, -2, -1, 4, 5)})):
        f = room_facts(cells); vv = (-4, 1)
        res = []
        for _ in [0]:
            w, bot, top = analyse_any(cells, vv)
            for walk in (bot, top):
                edges, pair, is_tree, nref, nconv = tree_edges(cells, walk[0], walk[1], walk[2])
                res.append((walk[0], is_tree, nref, nconv, len(edges)))
        pr(name, {k: f[k] for k in ('area', 'walls', 'r', 'simple', 'normalized')}, '2n=', 2 * len(cells),
           'rims (C, tree, reflex, convex, edge occurrences):', res)

    # ------------------------------------------------ the 23 newly closed saved pairs
    pr('== 23 newly closed pairs: own tracer on the saved/derived displacements')
    chart_graph, solve = ns['chart_graph'], ns['solve']
    from functools import lru_cache
    ok = 0; rows = []
    for name in ('DBw2', 'st279'):
        report = prev['data'][name]
        O = cylmod.Origami(rooms[name]); cells = set(rooms[name])
        graph = lru_cache(None)(lambda vv: chart_graph(O, vv))
        for pair in report['pairs']:
            S, T = tuple(pair['S']), tuple(pair['T'])
            vs = [tuple(pair[l][0]) for l in ('cc', 'lit')]
            if prev['old_test'](O, S, T, pair) or any(prev['on_saved_leaf'](O, S, T, vv) or
                    any(prev['midpoint_witness'](c, S, T) for c in graph(vv)[0]) for vv in vs):
                continue
            vec = None
            for vv in vs:
                x = solve(graph(vv), S, T)
                if x: vec = prev['orig'](x, vv); break
            if vec is None:
                # md's three explicit residual paths (signs tried below in both directions)
                vec = {((2, 2), (6, 2)): (4, 14), ((8, 2), (12, 2)): (4, 10), ((8, 2), (12, 4)): (4, 2)}[(S, T)]
            good = []
            for ex, ey in product((1, -1), repeat=2):
                D = (ex * vec[0], ey * vec[1])
                for A, B in ((S, T), (T, S)):
                    try:
                        end, _, _, recs = run(cells, A, D, 1, [F(1, 2)])
                    except Corner:
                        continue
                    if end == (F(B[0]), F(B[1])):
                        M = recs[F(1, 2)][0]
                        integral = M[0].denominator == M[1].denominator == 1
                        off = integral and ((M[0] - A[0]) % 2 or (M[1] - A[1]) % 2)
                        reg = integral and incid(cells, (int(M[0]), int(M[1]))) in (2, 4)
                        good.append((A, D, (int(M[0]), int(M[1])) if integral else M, bool(off and reg)))
            certified = any(g[3] for g in good)
            ok += certified
            rows.append((name, S, T, vec, certified, good[:1]))
    for r in rows: pr(*r)
    pr(f'newly closed pairs re-traced: {len(rows)}, certified by own tracer: {ok}')

    # ------------------------------------------------ the 37 pairs newly covered by convex-cylinder.md
    pr('== convex-cylinder.md: 37 newly covered pairs, own tracer')
    n37 = ok37 = 0; total = 0
    for name, report in prev['data'].items():
        if report['group'] != 'BBBB': continue
        O = cylmod.Origami(rooms[name]); cells = set(rooms[name])
        cache = lru_cache(None)(lambda vv: prev['charts'](O, vv))
        for pair in report['pairs']:
            total += 1
            S, T = tuple(pair['S']), tuple(pair['T'])
            if prev['old_test'](O, S, T, pair): continue
            vecs = []
            for label in ('cc', 'lit'):
                vv = tuple(pair[label][0])
                for chart in cache(vv):
                    x = prev['midpoint_witness'](chart, S, T)
                    if x: vecs.append(prev['orig'](x, vv)); break
                lf = prev['on_saved_leaf'](O, S, T, vv)
                if lf: vecs.append(lf)
            if not vecs: continue
            n37 += 1; good = False
            for vec in vecs:
                for ex, ey in product((1, -1), repeat=2):
                    D = (ex * vec[0], ey * vec[1])
                    try:
                        end, _, _, recs = run(cells, S, D, 1, [F(1, 2)])
                    except Corner:
                        continue
                    M = recs[F(1, 2)][0]
                    if end == (F(T[0]), F(T[1])) and M[0].denominator == M[1].denominator == 1 and \
                            ((M[0] - S[0]) % 2 or (M[1] - S[1]) % 2) and incid(cells, (int(M[0]), int(M[1]))) in (2, 4):
                        good = True
            ok37 += good
    pr(f'pairs in BBBB rooms: {total}; not covered by the old audit but covered by chart/leaf tests: {n37}; '
       f'certified by own tracer: {ok37}')
    pr(f'CPU {time.process_time() - t0:.1f} s')


if __name__ == '__main__':
    main()
