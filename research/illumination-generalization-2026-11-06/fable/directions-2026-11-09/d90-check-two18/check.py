"""D90 independent check of qclass-closure/two18 (shear certificates).

Usage: python3 -B check.py REGIONS_TXT [NSAMPLES]

1. Residual audit: parse the census residual products (regions.txt), derive the
   designated grid point of each endpoint, and check the 1/17 bound.
2. Leaf check: replay every proof tree in cert00/01/10/11.txt with exact
   Fractions against this directory's own cylinder model (surface.py).
3. Spot check: random concrete endpoint pairs from the residual; build the
   actual path from the certificate's leaf and trace it with the D87 tracer.
"""
import random
import sys
from ast import literal_eval
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path

from surface import Room

HERE = Path(__file__).resolve().parent
CTX = HERE.parents[3]
TWO18 = CTX / 'qclass-closure' / 'two18'
sys.path.insert(0, str(HERE.parent / 'd87-review-cross-corners'))
import billiard  # noqa: E402  (oracle tracer, used only in step 3)

UNIT = 65536
RAD = 3856
EXPECTED_PERIOD = {'00': 8, '01': 16, '10': 8, '11': 12}

# ------------------------------------------------------------------ rooms
audit = [l for l in (CTX / 'qclass-closure/offgrid/results/eighteen-audit.txt').read_text().splitlines()
         if l.startswith('cells ')]
assert len(audit) == 2
ROOMS, PAIRS = [], []
for l in audit:
    coords, pairs = l[6:].split(' open tile pairs ')
    xy = list(map(int, coords.split()))
    ROOMS.append(list(zip(xy[::2], xy[1::2])))
    PAIRS.append(set(literal_eval(pairs)))
roomfile = [list(map(int, l.split())) for l in (TWO18 / 'rooms').read_text().splitlines()]
for r in range(2):
    assert roomfile[r][:2] == [18, 18] and list(zip(roomfile[r][2::2], roomfile[r][3::2])) == ROOMS[r]
    assert len(ROOMS[r]) == 18 and len(PAIRS[r]) == 18


def tr(v, swap):
    return (v[1], v[0]) if swap else v


ROOMOBJ = {}
for r in range(2):
    for s in range(2):
        ROOMOBJ[f'{r}{s}'] = Room([tr(c, s) for c in ROOMS[r]])
for tag, R in ROOMOBJ.items():
    assert R.period() == EXPECTED_PERIOD[tag], (tag, R.period())
print('periods', {t: R.period() for t, R in ROOMOBJ.items()})

# ------------------------------------------------------------------ 1. residual
regions = Path(sys.argv[1])
centers = {}          # (r, i, j) -> {cell: grid point}
products = []         # (r, cell_a, poly_a, cell_b, poly_b)
maxdev = F(0)
for line in regions.open():
    if not line.startswith('REG '):
        continue
    h, u, v = line.split('|')
    r, i, j, src = map(int, h.split()[1:])
    r -= 1
    assert i < j and src in (i, j)
    other = j if src == i else i
    polys = []
    for cell, txt in ((src, u), (other, v)):
        a = list(map(int, txt.split()))
        assert a and len(a) % 3 == 0
        pts = [(F(x, d), F(y, d)) for x, y, d in zip(a[::3], a[1::3], a[2::3])]
        cx, cy = round(pts[0][0]), round(pts[0][1])
        ca, cb = ROOMS[r][cell]
        assert cx in (ca, ca + 1) and cy in (cb, cb + 1)
        for x, y in pts:
            dev = max(abs(x - cx), abs(y - cy))
            assert 17 * dev <= 1
            maxdev = max(maxdev, dev)
            assert ca <= x <= ca + 1 and cb <= y <= cb + 1  # in the closed cell
        d = centers.setdefault((r, i, j), {})
        assert d.setdefault(cell, (cx, cy)) == (cx, cy)
        polys.append((cell, pts))
    products.append((r, polys[0][0], polys[0][1], polys[1][0], polys[1][1]))
for r in range(2):
    assert {(i, j) for (rr, i, j) in centers if rr == r} == PAIRS[r]
for (r, i, j), d in centers.items():
    assert set(d) == {i, j}
    for cell, (X, Y) in d.items():
        k = sum((X - u, Y - v) in set(ROOMS[r]) for u in (0, 1) for v in (0, 1))
        assert k < 4, 'designated point must be on the physical boundary'
print(f'residual: {len(products)} polygon products, {len(centers)} tile pairs, max displacement {maxdev}')
assert maxdev <= F(1, 17)

# ------------------------------------------------------------------ 2. leaves


def strip_label(R, cyl, c, sg, k):
    row = R.row((c, 1, sg))
    q = cyl['q']
    i = k // q
    return cyl['lab'][(row[i % len(row)], k - q * i)]


def line_info(R, cyl, c, sg, n):
    """(open label or None, closure labels) for a point on row line u=n."""
    row = R.row((c, 1, sg))
    q = cyl['q']
    i = n // q
    sq, m = row[i % len(row)], n - q * i
    a, b = cyl['lab'][(sq, m - 1)], cyl['lab'][(sq, m)]
    if cyl['crit'][(sq, m)]:
        return None, {a, b}
    assert a == b
    return a, {a}


def guaranteed(R, cyl, c, sg, lo, hi):
    """Half-turn orbits {l, H l} whose open cylinders (O) / closures (C) contain every u in [lo,hi].

    Orbits suffice: if s is in open l and t is in the closure of l or of H l, then t or
    its half-turn lift H t is in the closure of l.
    """
    H = cyl['H']
    O = C = None
    ks = range(floor(lo), ceil(hi)) if lo < hi else ([floor(lo)] if lo.denominator > 1 else [])
    for k in ks:
        l = strip_label(R, cyl, c, sg, k)
        l = min(l, H[l])
        O = {l} if O is None else O & {l}
        C = {l} if C is None else C & {l}
    for n in range(ceil(lo), floor(hi) + 1):
        op, cl = line_info(R, cyl, c, sg, n)
        o = {min(op, H[op])} if op is not None else set()
        cl = {min(l, H[l]) for l in cl}
        O = o if O is None else O & o
        C = cl if C is None else C & cl
    return O, C


def u_interval(p, q, j, end, sg, box, e):
    c, (cx, cy), (a, b) = end
    sx = 1 if cx == a else -1
    sy = 1 if cy == b else -1
    Yb = (cy - b) if sg == 1 else 1 - (cy - b)
    base = F(q * (cx - a) - p * Yb)
    lo = hi = base
    for coef, (l, h) in ((q * sx, box[2 * e]), (-p * sg * sy, box[2 * e + 1]), (-sg * q * j * sy, box[4 + e])):
        v1, v2 = coef * F(l, UNIT), coef * F(h, UNIT)
        lo += min(v1, v2)
        hi += max(v1, v2)
    return lo, hi


def witness_ok(R, ends, box, j, p, q):
    cyl = R.cylinders(p, q)
    sets = [[guaranteed(R, cyl, ends[e][0], sg, *u_interval(p, q, j, ends[e], sg, box, e)) for sg in (1, -1)]
            for e in (0, 1)]
    for e in (0, 1):
        for so in range(2):
            O = sets[e][so][0]
            for sc in range(2):
                C = sets[1 - e][sc][1]
                if O & C:
                    return True
    return False


TREES = {}   # (tag, c0, c1, main) -> list of (box, kind, data)


def check_tag(tag):
    r, swap = int(tag[0]), int(tag[1])
    R = ROOMOBJ[tag]
    L = R.period()
    toks = iter((TWO18 / f'cert{tag}.txt').read_text().splitlines())
    ntree = nw = ne = 0
    seen = set()
    for head in toks:
        kind, c0, c1, main = head.split()
        assert kind == 'R'
        c0, c1, main = int(c0), int(c1), int(main)
        d = centers[(r, c0, c1)]
        ends = [(c, tr(d[c], swap), tr(ROOMS[r][c], swap)) for c in (c0, c1)]
        top = max(UNIT // 4, L * RAD)
        assert F(top, UNIT) >= max(F(1, 4), F(L, 17)) and F(RAD, UNIT) >= F(1, 17)
        box = [(0, RAD)] * 4 + [(0, top)] * 2
        box[4 + main] = (UNIT // 8, top)
        leaves = []
        stack = [box]
        while stack:
            z = stack.pop()
            tok = next(toks).split()
            if tok[0] == 'S':
                i = int(tok[1])
                l, h = z[i]
                mid = (l + h) // 2
                assert l < mid < h
                lo, hi = list(z), list(z)
                lo[i], hi[i] = (l, mid), (mid, h)
                stack += [hi, lo]   # preorder: lo first
            elif tok[0] == 'E':
                assert z[4 + 1 - main][0] > z[4 + main][1]
                leaves.append((z, 'E', None))
                ne += 1
            else:
                assert tok[0] == 'W' and len(tok) == 4
                j, p, q = map(int, tok[1:])
                assert witness_ok(R, ends, z, j, p, q), (tag, c0, c1, main, tok, z)
                leaves.append((z, 'W', (j, p, q)))
                nw += 1
        nwt = sum(1 for _, k, _ in leaves if k == 'W')
        assert next(toks) == f'{c0} {c1} {main} 1 {nwt}'
        TREES[(tag, c0, c1, main)] = leaves
        seen.add((c0, c1, main))
        ntree += 1
    assert seen == {(i, j, m) for (rr, i, j) in centers if rr == r for m in (0, 1)}
    print(f'{tag}: period {L}, {ntree} trees, {nw} witness leaves, {ne} empty leaves', flush=True)
    return ntree, nw, ne


tot = [0, 0, 0]
for tag in ('00', '01', '10', '11'):
    for k, v in enumerate(check_tag(tag)):
        tot[k] += v
print(f'TOTAL: {tot[0]} trees, {tot[1]} illuminated (W) boxes, {tot[2]} empty (E) boxes')

# ------------------------------------------------------------------ 3. spot check
NS = int(sys.argv[2]) if len(sys.argv) > 2 else 200
rng = random.Random(90)


def interior(cells, x, y):
    xs = [floor(x)] if x.denominator > 1 else [int(x) - 1, int(x)]
    ys = [floor(y)] if y.denominator > 1 else [int(y) - 1, int(y)]
    return all((a, b) in cells for a in xs for b in ys)


def sample(pts):
    w = [rng.randint(1, 1000) for _ in pts]
    s = sum(w)
    return (sum(F(wi, s) * x for wi, (x, _) in zip(w, pts)), sum(F(wi, s) * y for wi, (_, y) in zip(w, pts)))


def convex(pts):
    n = len(pts)
    if n < 3:
        return True
    sg = set()
    for i in range(n):
        (x0, y0), (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        cr = (x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)
        if cr:
            sg.add(cr > 0)
    return len(sg) <= 1


def point_labels(R, cyl, c, sg, u):
    if u.denominator > 1:
        l = strip_label(R, cyl, c, sg, floor(u))
        return {l}, {l}
    op, cl = line_info(R, cyl, c, sg, int(u))
    return ({op} if op is not None else set()), cl


def locate(R, cyl, c, sg, X, Y):
    row = R.row((c, 1, sg))
    i = floor(X)
    return row[i % len(row)], (X - i, Y)


def pieces_at(cyl, sq, loc, lab):
    p, q = cyl['p'], cyl['q']
    u = q * loc[0] - p * loc[1]
    ks = [floor(u)] if u.denominator > 1 else [int(u) - 1, int(u)]
    return [(sq, k) for k in ks if -p <= k < q and cyl['lab'][(sq, k)] == lab]


def develop(cyl, start, lab):
    off = {start: (0, 0)}
    todo = [start]
    while todo:
        z = todo.pop()
        for n, (dx, dy) in cyl['adj'][z]:
            if cyl['lab'][n] == lab and n not in off:
                off[n] = (off[z][0] + dx, off[z][1] + dy)
                todo.append(n)
    return off


def trace_pair(r, P, cells):
    """Trace the certificate path for concrete endpoints P={cell: point}. Returns (ok, tag, K, length)."""
    ca, cb = list(P)
    c0, c1 = min(ca, cb), max(ca, cb)
    d = centers[(r, c0, c1)]
    disp = [(abs(P[c][0] - d[c][0]), abs(P[c][1] - d[c][1])) for c in (c0, c1)]
    A = max(max(t) for t in disp)
    assert 0 < A <= F(1, 17)
    cand = [(0, e) for e in (0, 1) if disp[e][1] == A] + [(1, e) for e in (0, 1) if disp[e][0] == A]
    swap, main = cand[0]
    tag = f'{r}{swap}'
    R = ROOMOBJ[tag]
    L = R.period()
    K = ceil(1 / (8 * L * A))
    pt = [tr(P[c], swap) for c in (c0, c1)]
    ends = [(c, tr(d[c], swap), tr(ROOMS[r][c], swap)) for c in (c0, c1)]
    dxy = [(abs(pt[e][0] - ends[e][1][0]), abs(pt[e][1] - ends[e][1][1])) for e in (0, 1)]
    ph = [K * L * dxy[e][1] for e in (0, 1)]
    assert F(1, 8) <= ph[main] <= max(F(1, 4), F(L, 17)) and ph[1 - main] <= ph[main]
    z = [dxy[0][0], dxy[0][1], dxy[1][0], dxy[1][1], ph[0], ph[1]]
    leaf = [lf for lf in TREES[(tag, c0, c1, main)]
            if all(F(l, UNIT) <= zi <= F(h, UNIT) for zi, (l, h) in zip(z, lf[0]))]
    assert leaf, 'parameter point not covered'
    leaf = next(lf for lf in leaf if lf[1] == 'W')
    j, p, q = leaf[2]
    m = j * K
    cyl = R.cylinders(p, q)
    # Concrete sheared lifts in row charts.
    lifts = {}
    for e in (0, 1):
        c, (cx, cy), (a, b) = ends[e]
        x, y = pt[e]
        for sg in (1, -1):
            Y = (y - b) if sg == 1 else 1 - (y - b)
            X = (x - a) - sg * m * L * (y - cy)
            u = q * X - p * Y
            lifts[(e, sg)] = (point_labels(R, cyl, c, sg, u), locate(R, cyl, c, sg, X, Y))
    choice = None
    for e in (0, 1):
        for so in (1, -1):
            for sc in (1, -1):
                for flip in (False, True):
                    O = lifts[(e, so)][0][0]
                    C = lifts[(1 - e, sc)][0][1]
                    C = {cyl['H'][l] for l in C} if flip else C
                    if O & C and choice is None:
                        choice = (e, so, sc, flip, min(O & C))
    assert choice, ('no shared cylinder at concrete point', tag, leaf)
    e, so, sc, flip, lab = choice
    sqP, locP = lifts[(e, so)][1]
    sqQ, locQ = lifts[(1 - e, sc)][1]
    if flip:
        cc, ex, ey = sqQ
        sqQ, locQ = (cc, -ex, -ey), (1 - locQ[0], 1 - locQ[1])
    off = develop(cyl, pieces_at(cyl, sqP, locP, lab)[0], lab)
    pq = [z for z in pieces_at(cyl, sqQ, locQ, lab) if z in off]
    assert pq
    oP = off[pieces_at(cyl, sqP, locP, lab)[0]]
    oQ = off[pq[0]]
    Dx = oQ[0] + locQ[0] - oP[0] - locP[0]
    Dy = oQ[1] + locQ[1] - oP[1] - locP[1]
    Vx, Vy = Dx + m * L * Dy, Dy
    vel = (Vx, so * Vy)            # physical velocity in the (transposed) frame of copy (+1, so)
    vel = tr(vel, swap)
    start = P[(c0, c1)[e]]
    goal = P[(c0, c1)[1 - e]]
    res = billiard.run(cells, start, vel, F(1))
    ok = res['ok'] and res['end'] == goal
    if not ok:
        print('SPOT FAIL', tag, c0, c1, main, leaf[2], K, start, goal, vel, res['ok'], res['end'])
    return ok, tag, K, abs(Vx) + abs(Vy)


def run_samples(gen, n, name):
    fails = 0
    maxlen = maxK = 0
    tags = {}
    done = 0
    while done < n:
        item = gen()
        if item is None:
            continue
        ok, tag, K, ln = trace_pair(*item)
        fails += not ok
        maxlen, maxK = max(maxlen, ln), max(maxK, K)
        tags[tag] = tags.get(tag, 0) + 1
        done += 1
    print(f'{name}: {done} pairs traced, {fails} failures; per tag {dict(sorted(tags.items()))}; '
          f'max K {maxK}; max |Vx|+|Vy| {float(maxlen):.0f}', flush=True)
    return fails


def gen_residual():
    r, ca, pa, cb, pb = products[rng.randrange(len(products))]
    if not (convex(pa) and convex(pb)):
        return None
    cells = set(ROOMS[r])
    P = {ca: sample(pa), cb: sample(pb)}
    if not all(interior(cells, *P[c]) for c in P):
        return None
    return r, P, cells


def gen_small():
    # Both endpoints much closer to their designated points than the residual scale:
    # large K, large shear powers. These pairs lie in the certificate box, not
    # necessarily in the residual.
    (r, i, j), d = rng.choice(sorted(centers.items()))
    cells = set(ROOMS[r])
    P = {}
    for c in (i, j):
        (X, Y), (a, b) = d[c], ROOMS[r][c]
        s = F(1, 10 ** rng.randint(2, 4))
        rx, ry = F(rng.randint(1, 999), 1000), F(rng.randint(1, 999), 1000)
        P[c] = (X + (1 if X == a else -1) * s * rx, Y + (1 if Y == b else -1) * s * ry)
    return r, P, cells


NSMALL = int(sys.argv[3]) if len(sys.argv) > 3 else 40
fails = run_samples(gen_residual, NS, 'spot check (residual pairs)')
fails += run_samples(gen_small, NSMALL, 'spot check (small-A pairs, A <= 1/100)')
assert fails == 0
print('ALL CHECKS PASSED')
