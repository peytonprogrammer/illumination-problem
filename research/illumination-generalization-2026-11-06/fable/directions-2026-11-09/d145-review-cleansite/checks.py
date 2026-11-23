"""d145 checks for clean-site-cost.md (snapshot 2026-11-22 02:15).

Named rooms only: R22 (d144 cell list, cross-checked against d8 R22-base),
cov4181 (d144 cell list, cross-checked against d64 covers.json index 4181),
the 3-cell L-room, and the V-notch B (angle arithmetic only). No searches.
Exact integer / Fraction arithmetic. The billiard tracer below is written
here, independently of d8's tracer, so the six archived routes are replayed
by a second implementation.
"""
from collections import Counter
from fractions import Fraction as Fr
from itertools import combinations
from math import floor, ceil, gcd
from pathlib import Path
import json
import time

t0 = time.process_time()
HERE = Path(__file__).resolve().parent
DIRS = HERE.parent
QC = DIRS.parents[2] / 'qclass-closure' / 'bbbb'


def hdr(s):
    print('=' * 78); print(s); print('=' * 78)


# ---------------------------------------------------------------- rooms
def r22():
    P = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)]
    Q = set(P) | {(x, -y - 1) for x, y in P} | {(3 - x, -y - 1) for x, y in P}
    assert len(Q) == 15
    return Q


def cov4181():
    cov = set()
    for x, ys in enumerate([range(6), (2, 3), (2, 3), range(6), range(6), (2, 3), (2,), range(3)]):
        for y in ys:
            cov.add((x, y))
    assert len(cov) == 28
    return cov


LROOM = {(0, 0), (1, 0), (0, 1)}


def counts(cells):
    return Counter((x + i, y + j) for x, y in cells for i in (0, 1) for j in (0, 1))


def wall_lengths(cells):
    """Maximal horizontal and vertical wall lengths, from unit boundary edges."""
    hs = set(); vs = set()
    for x, y in cells:
        for dy, side in ((-1, 'b'), (1, 't')):
            if (x, y + dy) not in cells:
                hs.add((y + (dy > 0), x, side))
        for dx, side in ((-1, 'l'), (1, 'r')):
            if (x + dx, y) not in cells:
                vs.add((x + (dx > 0), y, side))
    def maximal(units):
        lens = []
        units = set(units)
        for (line, a, side) in sorted(units):
            if (line, a - 1, side) in units:
                continue
            L = 1
            while (line, a + L, side) in units:
                L += 1
            lens.append(L)
        return lens
    return maximal(hs), maximal(vs)


def parity_table(cells):
    c = counts(cells)
    tab = {}
    for x in ((0, 0), (1, 0), (0, 1), (1, 1)):
        pts = [p for p, k in c.items() if (p[0] % 2, p[1] % 2) == x]
        i = sum(c[p] == 4 for p in pts); b = sum(c[p] == 2 for p in pts)
        f = sum(c[p] == 1 for p in pts); r = sum(c[p] == 3 for p in pts)
        tab[x] = dict(i=i, b=b, f=f, r=r, fiber=4 * i + 2 * b + f + 3 * r,
                      q=2 * i + b, regular=sorted(p for p in pts if c[p] in (2, 4)),
                      reflex=sorted(p for p in pts if c[p] == 3))
    return tab


def report_room(name, cells):
    n = len(cells)
    hl, vl = wall_lengths(cells)
    W = len(hl) + len(vl)
    c = counts(cells)
    r = sum(k == 3 for k in c.values()); f = sum(k == 1 for k in c.values())
    gh = 0; gv = 0
    for L in hl: gh = gcd(gh, L)
    for L in vl: gv = gcd(gv, L)
    print(f'[{name}] area n={n}, walls W={W}, convex={f}, reflex={r}, W==2r+4: {W == 2 * r + 4}; '
          f'gcd(horizontal lengths)={gh}, gcd(vertical lengths)={gv} -> Per(X)=2Z^2: {gh == gv == 1}')
    tab = parity_table(cells)
    for x, t in tab.items():
        clean = t['i'] == 0 and t['b'] == 0
        print(f'   class {x}: interior {t["i"]}, smooth {t["b"]}, convex {t["f"]}, reflex {t["r"]}; '
              f'fiber 4i+2b+f+3r = {t["fiber"]} (= n: {t["fiber"] == n}); '
              f'{"CLEAN: n = f+3r = %d+3*%d" % (t["f"], t["r"]) if clean else "regular points " + str(t["regular"])}')
        assert t['fiber'] == n
    # angle bound d|Z| <= M(W-2)/2 with M=4, d=n
    Z = [x for x, t in tab.items() if t['i'] == t['b'] == 0]
    print(f'   clean sites {Z}; d|Z| = {n * len(Z)} <= M(W-2)/2 = {2 * (W - 2)}: {n * len(Z) <= 2 * (W - 2)}')
    return tab, W, r


# ---------------------------------------------------------------- tracer
def leg(cells, start, v, stop_at=None, max_hits=50):
    """Billiard flow from lattice point `start` with integer velocity v.
    Returns (event point, kind, lattice hits incl. event, arrival velocity, time).
    Stops at the first convex/reflex corner, or at `stop_at`."""
    x, y = Fr(start[0]), Fr(start[1]); vx, vy = v; t = Fr(0)
    hits = []
    c = counts(cells)
    # first cell entered must be a room cell
    assert (start[0] if vx > 0 else start[0] - 1, start[1] if vy > 0 else start[1] - 1) in cells
    while len(hits) < max_hits:
        tx = (((floor(x) + 1) if vx > 0 else (ceil(x) - 1)) - x) / vx
        ty = (((floor(y) + 1) if vy > 0 else (ceil(y) - 1)) - y) / vy
        dt = min(tx, ty); t += dt
        x, y = x + vx * dt, y + vy * dt
        if x.denominator == 1 and y.denominator == 1:
            p = (int(x), int(y)); k = c[p]; hits.append(p)
            if k in (1, 3):
                return p, {1: 'convex', 3: 'reflex'}[k], hits, (vx, vy), t
            if p == stop_at:
                return p, 'target', hits, (vx, vy), t
            if k == 2:
                X, Y = p
                horiz = ((X - 1, Y - 1) in cells) == ((X, Y - 1) in cells)
                if horiz: vy = -vy
                else: vx = -vx
            elif k != 4:
                raise RuntimeError('left room')
            continue
        if dt == tx and x.denominator == 1:
            col = int(x) if vx > 0 else int(x) - 1
            if (col, floor(y)) not in cells: vx = -vx
        else:
            row = int(y) if vy > 0 else int(y) - 1
            if (floor(x), row) not in cells: vy = -vy
    raise RuntimeError('no event')


# ================================================================== 1
hdr('1. R22: clean site contents, and replay of the six axial-reflex routes')
R = r22()
d8 = json.loads((DIRS / 'd8-perturbation-test' / 'rooms.json').read_text())
d8cells = {tuple(p) for p in next(r['cells'] for r in d8 if r['id'] == 'R22-base')}
print('R22 cells (d144 manuscript construction) == d8 R22-base cells:', d8cells == R)
assert d8cells == R
tabR, WR, rR = report_room('R22', R)
S, T = (0, 0), (2, 2)

certs = [  # from corner-support.py (archived)
    ((0, -1), (-8, 11), (8, -11), 1, 3),
    ((0, 1), (-2, 1), (-2, -1), 1, 1),
    ((1, -2), (7, -4), (-7, -4), 1, 1),
    ((1, -1), (9, -5), (-9, 5), 1, 1),
    ((1, 1), (1, 1), (-1, -1), 1, 1),
    ((1, 2), (3, 2), (3, 2), 1, 1),
    ((3, 1), (9, 5), (9, 5), 1, 1),
    ((3, 2), (9, 2), (9, 2), 1, 1),
    ((4, 1), (4, 7), (4, -7), 1, 1),
]
reflexes = {p for p, k in counts(R).items() if k == 3}
assert reflexes == {c[0] for c in certs}
oddodd = {p for p in reflexes if p[0] % 2 and p[1] % 2}
print('odd-odd reflexes (permanently stopped):', sorted(oddodd))
cells_used = Counter()
supports = []
for C, vs, vt, i, j in certs:
    pA, kA, hA, uA, tA = leg(R, S, vs, stop_at=T)
    pB, kB, hB, uB, tB = leg(R, T, vt, stop_at=S)
    assert pA == C and pB == C and kA == kB == 'reflex'
    assert len(hA) == i and len(hB) == j
    straight = uA == tuple(-u for u in uB)
    # route lattice points in order from S
    route = hA + list(reversed(hB[:-1])) + [T]
    corners_on_route = [p for p in route[:-1] if counts(R)[p] in (1, 3)]
    others_ok = all(counts(R)[p] in (2, 4) for p in route[:-1] if p != C)
    D = tuple((i + j) * a for a in vs)          # developed displacement S -> T lift
    arrive = tuple(-a for a in vt)               # physical velocity on arrival at T
    g = tuple(arrive[k] // vs[k] for k in (0, 1))   # sheet: diag(g)
    assert all(abs(arrive[k]) == abs(vs[k]) for k in (0, 1))
    lift_ok = all((D[k] - g[k] * T[k]) % 2 == 0 for k in (0, 1))
    w4 = (D[0] % 4, D[1] % 4)
    mid = (Fr(D[0], 2), Fr(D[1], 2))
    mid_site = (int(mid[0]) % 2, int(mid[1]) % 2)
    mid_phys = route[(i + j) // 2 - 1] if (i + j) % 2 == 0 else None
    blocked_by_site = w4 == (2, 2)
    tag = 'odd-odd' if C in oddodd else 'axial'
    print(f'  C={C} [{tag}] steps {i}+{j}; lattice points from S: {route}; corners met {corners_on_route}; '
          f'other points smooth/interior: {others_ok}; straight join: {straight}')
    print(f'      developed D={D}, target sheet diag{g}, lift consistent: {lift_ok}, '
          f'holonomy class D mod 4Z^2={w4}; midpoint site {mid_site} at physical {mid_phys}; '
          f'in clean-site class (2,2): {blocked_by_site}')
    assert corners_on_route == [C] and others_ok and straight and lift_ok
    assert blocked_by_site == (C in oddodd)
    if C not in oddodd:
        assert mid_site != (1, 1)
        # the route avoids the three permanent stops
        assert not (set(route) & oddodd)
        cells_used[(g, w4)] += 1
    supports.append(set(route[:-1]) & reflexes)
print('  supports are singletons:', all(len(s) == 1 for s in supports))
print('  residual (sheet, class) cells hit by the six axial routes:', dict(cells_used),
      f'-> {len(cells_used)} of 12 residual cells carry a certificate')
nax = len(reflexes - oddodd)
print(f'  axial reflexes available in R22: {nax}. Lower bound from singleton routes: {nax}; '
      f'upper bound (all stopped = original room, dark per manuscript): {nax}. "Exactly six" = "all of them".')

# ================================================================== 2
hdr('2. n = f_x + 3 r_x at a clean parity (torus fiber count); cov4181, R22, L-room')
covs = json.loads((DIRS / 'd64-finite-case' / 'data' / 'covers.json').read_text())['rooms']
ctrl = sorted((r for r in covs if r['normalized']), key=lambda r: (r['n'], r['cells']))[4181]
cc = {tuple(p) for p in ctrl['cells']}
C4 = cov4181()
mn = (min(x for x, _ in cc), min(y for _, y in cc))
print('cov4181 (d144 list) == d64 normalized index 4181 (up to translation):',
      {(x - mn[0], y - mn[1]) for x, y in cc} == C4, '; translation', mn)
report_room('cov4181', C4)
report_room('L-room', LROOM)
print('  Pick check (all rooms): sum over classes of fibers = 4n holds by the asserts above.')

# ================================================================== 3
hdr('3. Fold budget  sum_{x in J} (q_x + 2 (r_x mod k)) <= 2k-2  on R22')
off = [(1, 0), (0, 1), (1, 1)]
for x in off:
    print(f'  class {x}: (q_x, r_x) = ({tabR[x]["q"]}, {tabR[x]["r"]}), convex f_x = {tabR[x]["f"]}')
for k in (2, 3, 5):
    if 15 % k:
        print(f'  k={k}: k does not divide n=15, so no fold of inner degree {k} exists; inequality shown anyway:')
    for m in range(1, 4):
        for J in combinations(off, m):
            cost = sum(tabR[x]['q'] + 2 * (tabR[x]['r'] % k) for x in J)
            print(f'  k={k} J={J}: cost {cost} vs budget {2 * k - 2}: {"allowed" if cost <= 2 * k - 2 else "EXCLUDED"}')
# reconstruct the forced degree-3 fiber data and check Riemann-Hurwitz / Gauss-Bonnet
k = 3; m = 15 // k
print('  forced k=3 structure (J = three off-source classes, budget tight):')
poles = zeros = 0; R_total = 0
for x in off:
    t = tabR[x]; z = t['r'] // k; b3 = t['r'] % k; b2 = t['q']
    rest = m - 3 * z                       # N-degree left for poles (regular N points excluded over J)
    npoles = rest
    b1 = npoles * k - 2 * b2 - 3 * b3      # sum over poles of b1+2b2+3b3 = k per pole
    print(f'    {x}: zeros {z}, poles {npoles}, (b1,b2,b3)=({b1},{b2},{b3}); b1 == f_x: {b1 == t["f"]}')
    assert b1 == t['f']
    poles += npoles; zeros += z; R_total += b2 + 2 * b3
t = tabR[(0, 0)]
# over the source class nothing ramifies: regular Q points come in k-tuples over regular N points
assert t['q'] % k == 0 and t['f'] % k == 0 and t['r'] == 0
p00 = t['f'] // k; reg00 = t['q'] // k
print(f'    (0,0): poles {p00}, regular N points {reg00}, N-degree {p00 + 2 * reg00} (= {m}: {p00 + 2 * reg00 == m})')
poles += p00
print(f'    ramification used {R_total} = 2k-2 = {2 * k - 2}; N: poles {poles}, simple zeros {zeros}, '
      f'poles - zeros = {poles - zeros} (sphere needs 4)')
# canonical double of N: each simple zero gives one point of angle 6pi (Euler contribution -2); poles become regular
g_tilde = (2 + 2 * zeros) // 2
print(f'    canonical double of N: 2 - 2g = -2*{zeros} -> genus {g_tilde}; area {4 * m} unit squares'
      f' d143 lists one genus-4, 20-square quotient of X: genus match {g_tilde == 4}')
print('  d143 block systems of R22 X (60 squares): genus>=2 quotients of degree 1, 3; genus-1 of 1,2,2,2,4 squares.')
print('  A degree-2 fold Q->N would give a degree-2 (30-square) translation quotient of X: none exists.')

# ================================================================== 4 (arithmetic only)
hdr('4. V-notch B: angle bound d|Z| <= M(W-2)/2 (M = 8)')
angles = {(0, 0): Fr(1, 4), (4, 0): Fr(1, 4), (4, 4): Fr(1, 8), (2, 2): Fr(3, 4), (0, 4): Fr(1, 8)}  # in units of 2pi
M = 8
tot = sum(M * a for a in angles.values())
print(f'  sum_C M*theta/2pi = {tot}; M(W-2)/2 = {M * 3 // 2}; d|Z| = 3*4 = 12 -> equality: {tot == 12}')
print(f'  lifts: (0,0),(4,0): 2 each of degree 1; (4,4),(0,4): 1 each of degree 1; (2,2): 2 of degree 3')

print(f'Total CPU {time.process_time() - t0:.2f}s')
