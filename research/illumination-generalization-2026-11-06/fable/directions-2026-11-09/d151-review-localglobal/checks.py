"""d151 referee checks for local-global.md (snapshot 2026-11-22-0250).

Named room DB55 only; no room search.
  (1) Direct billiard: S=(2,2), T=(4,4), directions (1,2j), |j|<=60. Claim: lit iff 5 does not divide j.
  (2) Structural model: the same pencil computed in a closed 5x5 box with corner stops,
      by folding the straight line (2+t, 2+bt) modulo 10. Checks the corridor is never entered.
  (3) Modulus refutation: for every N<=60 coprime to 5, p_0 and p_N agree mod 2N but differ in lit status.
  (4) Fixed-chain witness: the segment (2,2)->(10,2) and the d148 direction (3,2).
  (5) Empirical lit density of primitive directions for (S,T) in balls of radius R (illustration only).
"""
import sys, time
from math import gcd
from itertools import product
from pathlib import Path

T0 = time.process_time()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
import roomtools as rt  # noqa: E402

def rect(a, b, c, d):
    return set(product(range(a, b), range(c, d)))

CELLS = rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5)   # DB55, as in d148/d149
assert rt.is_strictly_simple(CELLS)
S, T = (2, 2), (4, 4)
kind = lambda p: rt.status(CELLS, p)

def walls_at(p):
    x, y = p
    below = ((x - 1, y - 1) in CELLS, (x, y - 1) in CELLS)
    return 'h' if below in ((True, True), (False, False)) else 'v'

def trace(P, d, maxsteps=10 ** 6):
    """Lattice points visited from P in signed direction d (non-axis), cells visited, end reason."""
    sx, sy = (1 if d[0] > 0 else -1), (1 if d[1] > 0 else -1)
    ax, ay = abs(d[0]), abs(d[1])
    start, seen, cells = (P, sx, sy), [], set()
    for _ in range(maxsteps):
        if ax == 0 or ay == 0:
            Q = (P[0] + (sx if ax else 0), P[1] + (sy if ay else 0))
        else:
            cx, cy = P[0] - (sx < 0), P[1] - (sy < 0)
            cells.add((cx, cy))
            i = j = 1
            while i < ax or j < ay:
                if j >= ay or (i < ax and i * ay < j * ax):
                    if (cx + sx, cy) in CELLS: cx += sx
                    else: sx = -sx
                    i += 1
                else:
                    if (cx, cy + sy) in CELLS: cy += sy
                    else: sy = -sy
                    j += 1
                cells.add((cx, cy))
            Q = (cx + (sx > 0), cy + (sy > 0))
        k = kind(Q)
        seen.append(Q)
        if k in ('convex', 'reflex'):
            return seen, cells, 'stop at %s' % (Q,)
        if k == 'smooth':
            if walls_at(Q) == 'h': sy = -sy
            else: sx = -sx
        P = Q
        if (P, sx, sy) == start:
            return seen, cells, 'periodic'
    raise RuntimeError('no closure')

def lit(s, t, v):
    hits = []
    for ex, ey in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        d = (ex * v[0], ey * v[1])
        if d[0] == 0 and ex < 0 or d[1] == 0 and ey < 0: continue
        seen, cells, why = trace(s, d)
        if t in seen[:-1] or (t in seen and kind(t) == 'interior'):
            hits.append((d, seen.index(t) + 1))
    return hits

out = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.append(s)

# (1) direct billiard on the pencil
log('== DB55 cells', len(CELLS), 'S', S, 'T', T)
bad, maxx_all, corridor_cells, ends = [], 0, 0, {}
for j in range(-60, 61):
    v = (1, 2 * j)
    h = lit(S, T, v)
    pred = (j % 5 != 0)
    if bool(h) != pred: bad.append((j, h))
    for ex, ey in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        d = (ex, ey * 2 * j)
        if d[1] == 0 and ey < 0: continue
        seen, cells, why = trace(S, d)
        maxx_all = max(maxx_all, max(p[0] for p in seen))
        corridor_cells += sum(1 for c in cells if c[0] >= 5)
        ends[why.split(' at')[0]] = ends.get(why.split(' at')[0], 0) + 1
        if j % 5 == 0:
            assert why.startswith('stop'), (j, d, why)
            assert all(p[1] == 2 for p in seen), (j, d, seen)
log('(1) directions (1,2j), |j|<=60: 121 | lit iff 5 does not divide j: mismatches', len(bad), bad[:3])
log('    max x of any visited lattice point:', maxx_all, '| cells with x>=5 entered:', corridor_cells)
log('    ray endings over all signed rays:', ends)
log('    for 5|j every visited lattice point has y=2 and each ray stops at a corner')
for j in (0, 1, 2, 3, 4, 5, 10):
    log('    j=%d' % j, 'hits (signed dir, step):', lit(S, T, (1, 2 * j)),
        '| +x ray ends', trace(S, (1, 2 * j) if j else (1, 0))[2])

# (2) closed 5x5 box model by folding mod 10
CORN = {(0, 0), (0, 5), (5, 0), (5, 5), (5, 2), (5, 3)}
fold = lambda z: (z % 10) if z % 10 <= 5 else 10 - z % 10
def box_lit(q):
    for sgn, b in ((1, q), (-1, q), (1, -q), (-1, -q)):
        t = 0
        while True:
            t += sgn
            P = (fold(2 + t), fold(2 + b * t))
            if P == T: return True
            if P in CORN: break
            if (t % 10 == 0) and (b * t) % 10 == 0: break   # back at S with same direction: periodic
            if abs(t) > 100: raise RuntimeError
    return False
mm = [q for q in range(-120, 121) if box_lit(q) != bool(lit(S, T, (1, q)))]
log('(2) box model vs billiard for all (1,q), |q|<=120:', 241, 'directions, mismatches', len(mm), mm[:5])
log('    box model on even q=2j: lit set equals {5 does not divide j}:',
    all(box_lit(2 * j) == (j % 5 != 0) for j in range(-500, 501)), '(|j|<=500)')
log('    odd q lit in box model for |q|<=120:', sum(box_lit(q) for q in range(-119, 120, 2)), 'of 120')

# (3) modulus refutation
fails = [N for N in range(1, 61) if gcd(N, 5) == 1 and not (lit(S, T, (1, 2 * N)) and not lit(S, T, (1, 0)))]
log('(3) N in 1..60 coprime to 5 with p_0=(1,0) dark and p_N=(1,2N) lit (agree mod 2N):',
    sum(1 for N in range(1, 61) if gcd(N, 5) == 1) - len(fails), 'of', sum(1 for N in range(1, 61) if gcd(N, 5) == 1),
    '| failures', fails)
log('    2^k cases: k=1..5 ->', [bool(lit(S, T, (1, 2 ** (k + 1)))) for k in range(1, 6)], '(p_(2^k) lit, p_0 dark)')

# (4) fixed-chain witness
seg = [(x, 2) for x in range(2, 11)]
log('(4) lattice points on [(2,2),(10,2)] and their kind:', [(p, kind(p)) for p in seg if kind(p) != 'interior'])
T2 = (10, 2)
log('    direction (3,2) lights (2,2)->(10,2):', lit(S, T2, (3, 2)))

# (5) empirical density of lit primitive directions for (S,T)
dirs = [(p, q) for p in range(0, 41) for q in range(-40, 41)
        if gcd(p, q) == 1 and (p > 0 or q == 1) and p * p + q * q <= 1600]
L = {v: bool(lit(S, T, v)) for v in dirs}
for R in (5, 10, 20, 30, 40):
    sub = [v for v in dirs if v[0] ** 2 + v[1] ** 2 <= R * R]
    log('(5) R=%d: primitive directions %d, lit %d, fraction %.3f' % (R, len(sub), sum(L[v] for v in sub),
        sum(L[v] for v in sub) / len(sub)))
log('cpu total %.1fs' % (time.process_time() - T0))
