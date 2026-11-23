"""d179 checks for l1-swap-pole-averaging.md (snapshot d95-review-queue/snapshots/1650).

Named room only: DB55 stretch at p = 53 (d178).  Named primitive directions
only: (1,0), (0,1), (1,1), (1,2), (2,1), (1,-1), (-1,2), (3,2).  Named marks
S=(2,2), T=(10,2) and S=(2,2), T=(12,4).  Named straightening instances.
No room, ray, direction or word search.

Model (d146): front sheets are room-double squares (x,y,c) with x+y+c even.
In the developed unit grid, crossing the vertical line x=X applies
tau('V', X%2); crossing y=Y applies tau('H', Y%2).  A developed square (k,l)
lies over the pillowcase front square iff k+l is even.  A Q-square at a
corner of parity (i,j) is converted to the front sheet of the same Q-point by
tau('V', i) when it is a back square; the Q-points over site (i,j) are the
cycles of g_ij on front sheets.
"""
from collections import Counter
from fractions import Fraction as Fr
from itertools import combinations
from math import comb, gcd
from pathlib import Path
import time

t0 = time.process_time()
HERE = Path(__file__).resolve().parent
src = (HERE.parent / 'd146-review-exdescent' / 'checks.py').read_text()
defs = src.split('# ' + '=' * 66 + ' 1')[0]
ns = {'__file__': str(HERE.parent / 'd146-review-exdescent' / 'checks.py')}
exec(compile(defs, 'd146-checks-defs', 'exec'), ns)
Double, rect, ctype = ns['Double'], ns['rect'], ns['ctype']


def hdr(s):
    print('=' * 78); print(s); print('=' * 78)


p = 53; L = p - 50
cells = rect(0, 5, 0, 5) | rect(5, 5 + L, 2, 3) | rect(5 + L, 10 + L, 0, 5)
D = Double(cells)
n = D.n; N = comb(n, 2)
front = D.front; idx = D.idx


def to_front(s, corner_par_x):
    return s if (s[0] + s[1] + s[2]) % 2 == 0 else D.tau('V', corner_par_x, s)


def from_front(f, sq_parity, corner_par_x):
    return f if sq_parity == 0 else D.tau('V', corner_par_x, f)


def transport(P0, pts):
    """Polyline P0 -> pts[0] -> ... -> pts[-1] (last point a lattice point).
    Returns (terminal site, list term[i] = front index at the terminal Q-point
    for initial front label i).  Asserts no lattice point in the open interior."""
    P = [tuple(map(Fr, P0))] + [tuple(map(Fr, q)) for q in pts]
    end = P[-1]
    assert all(c.denominator == 1 for c in end)
    d0 = (P[1][0] - P[0][0], P[1][1] - P[0][1])
    axis = d0[0] == 0 or d0[1] == 0
    events = []  # (segment k, t, 'V'/'H', line parity)
    for k in range(len(P) - 1):
        A, B = P[k], P[k + 1]
        for ax, c in ((0, 'V'), (1, 'H')):
            a, b = A[ax], B[ax]
            if a == b:
                assert not axis or len(P) == 2
                continue
            lo, hi = min(a, b), max(a, b)
            X = int(lo // 1) + 1
            while X < hi:
                events.append((k, (X - a) / (b - a), c, X % 2))
                X += 1
    events.sort()
    for e1, e2 in zip(events, events[1:]):
        assert (e1[0], e1[1]) != (e2[0], e2[1]), 'segment passes through a lattice point'
    ax0, ay0 = int(P0[0]) % 2, int(P0[1]) % 2
    if axis:  # segment lies on a grid line: label = front square above/right, no crossings
        assert len(P) == 2 and not events
        sx = int(P0[0]) + (0 if d0[0] >= 0 else -1) if d0[0] else int(P0[0])
        sy = int(P0[1]) + (0 if d0[1] >= 0 else -1) if d0[1] else int(P0[1])
        par = (sx + sy) % 2
    else:
        sx = int(P0[0]) + (0 if d0[0] > 0 else -1)
        sy = int(P0[1]) + (0 if d0[1] > 0 else -1)
        par = (sx + sy) % 2
    bx, by = int(end[0]) % 2, int(end[1]) % 2
    term = []
    for f in front:
        s = from_front(f, par, ax0)
        for (_, _, c, k) in events:
            s = D.tau(c, k, s)
        endpar = (par + len(events)) % 2
        assert (s[0] + s[1] + s[2]) % 2 == endpar
        term.append(idx[to_front(s, bx)])
    assert sorted(term) == list(range(n)), 'transport not a bijection'
    return (bx, by), term


def cyc_of(g):
    cl = {}
    for c in D.cycles(g):
        for i in c:
            cl[i] = c
    return cl


hdr(f'Room DB55 p={p}: n={n}, N=binom(n,2)={N}')
for x in sorted(D.g):
    q = sum(len(c) == 2 for c in D.cycles(D.g[x]))
    print(f'   site {x}: q_x={q}; q_x/N = {q}/{N} = {q / N:.5f}; 1/(n-1) = {1 / (n - 1):.5f}; '
          f'q_x/N <= 1/(n-1): {q / N <= 1 / (n - 1)}')

hdr('Check 1: counting lemma on named primitive segments')
DIRS = [(1, 0), (0, 1), (1, 1), (1, 2), (2, 1), (1, -1), (-1, 2), (3, 2)]
STARTS = [(0, 0), (1, 0), (0, 1), (1, 1)]
res = {}
allok = True
for P0 in STARTS:
    for v in DIRS:
        assert gcd(*v) == 1
        b, term = transport(P0, [(P0[0] + v[0], P0[1] + v[1])])
        g = D.g[b]; cl = cyc_of(g)
        # brute force over all N unordered labels: Y-endpoint is a swap pole iff the
        # 2-set of terminal labels is a single g_b orbit with g swapping its letters
        succ = [(i, j) for i, j in combinations(range(n), 2)
                if g[term[i]] == term[j] and g[term[j]] == term[i] and term[i] != term[j]]
        q = sum(len(c) == 2 for c in D.cycles(g))
        letters = [x for e in succ for x in e]
        matching = len(letters) == len(set(letters))
        # pulled back transpositions
        inv = {t: i for i, t in enumerate(term)}
        pulled = sorted(tuple(sorted((inv[c[0]], inv[c[1]]))) for c in D.cycles(g) if len(c) == 2)
        ok = len(succ) == q and matching and pulled == sorted(succ)
        allok &= ok
        res[(P0, v)] = (b, term, succ)
        if P0 == (0, 0) or not ok:
            print(f'   start site {P0} -> v={v} ends at site {b}: successes {len(succ)} (q_b={q}), '
                  f'matching {matching}, equals pulled-back 2-cycles {pulled == sorted(succ)}')
print(f'   all {len(STARTS) * len(DIRS)} (start site, direction) cases satisfy the lemma: {allok}')
# reversal sanity: transport of -v from P0+v is the inverse correspondence
P0, v = (0, 0), (1, 2)
b, term = res[(P0, v)][:2]
b2, term2 = transport((1, 2), [(0, 0)])
print(f'   sanity: reverse of (0,0)->(1,2) is inverse transport: {all(term2[term[i]] == i for i in range(n))}')
P0, v = (0, 0), (3, 2)
b, term = res[(P0, v)][:2]
b2, term2 = transport((3, 2), [(0, 0)])
print(f'   sanity: reverse of (0,0)->(3,2) is inverse transport: {all(term2[term[i]] == i for i in range(n))}')

hdr('Check 2: marked set M = sheets(S) x sheets(T); cross edges among pulled-back swaps')
for S, T in (((2, 2), (10, 2)), ((2, 2), (12, 4))):
    sS = [sorted(D.qpoint(S, c)) for c in (0, 1)]
    sT = [sorted(D.qpoint(T, c)) for c in (0, 1)]
    A = set(sS[0] + sS[1]); B = set(sT[0] + sT[1])
    print(f'   S={S} sheets by copy {sS}; T={T} sheets by copy {sT}; |M|={len(A) * len(B)}')
    for v in DIRS:
        b, term, succ = res[((0, 0), v)]
        cross = [e for e in succ if (e[0] in A and e[1] in B) or (e[0] in B and e[1] in A)]
        inS = [e for e in succ if set(e) <= A]
        inT = [e for e in succ if set(e) <= B]
        print(f'      v={v}: {len(succ)} swap edges; cross S-T {len(cross)} {cross}; inside S {inS}; inside T {inT}')
# explicit zero-cross-edge illustration on letters {0..3} u {4..7}
A4, B4 = {0, 1, 2, 3}, {4, 5, 6, 7}
m1 = [(0, 1), (2, 3), (4, 5), (6, 7)]; m2 = [(0, 2), (1, 3), (4, 6), (5, 7)]
mass = Counter(); [mass.update({e: 0.5}) for e in m1 + m2]
print(f'   abstract example: average of two within-set perfect matchings, mass on cross edges = '
      f'{sum(w for e, w in mass.items() if (e[0] in A4) != (e[1] in A4))}; total mass = {sum(mass.values())} (=q=4)')

hdr('Check 3: straightening lemma on named instances (v=(2,1) and v=(3,2) from site 00)')


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def yorb(g, a, b):
    P = frozenset((a, b)); orb = {P}; Q = frozenset((g[a], g[b]))
    while Q not in orb:
        orb.add(Q); u, w = tuple(Q); Q = frozenset((g[u], g[w]))
    return frozenset(orb)


SA = set(D.qpoint((2, 2), 0)) | set(D.qpoint((2, 2), 1))
TB = set(D.qpoint((10, 2), 0)) | set(D.qpoint((10, 2), 1))


def tri_lattice(v, y):
    xs = [0, v[0], y[0]]; ys = [0, v[1], y[1]]
    out = []
    for X in range(int(min(xs)) - 1, int(max(xs)) + 2):
        for Y in range(int(min(ys)) - 1, int(max(ys)) + 2):
            u = (Fr(X), Fr(Y))
            d1, d2, d3 = det(v, u), det(u, y), det((y[0] - v[0], y[1] - v[1]), (u[0] - v[0], u[1] - v[1]))
            s = det(v, y)
            if s < 0:
                d1, d2, d3 = -d1, -d2, -d3
            if d1 >= 0 and d2 >= 0 and d3 >= 0 and (X, Y) not in ((0, 0), tuple(map(int, v))):
                out.append((X, Y))
    return out


for v, y in (((2, 1), (Fr(21, 10), Fr(23, 20))), ((2, 1), (Fr(19, 10), Fr(9, 10))),
             ((3, 2), (Fr(31, 10), Fr(197, 100))), ((2, 1), (Fr(17, 10), Fr(9, 5)))):
    v = (Fr(v[0]), Fr(v[1]))
    eps = ((y[0] - v[0]) ** 2 + (y[1] - v[1]) ** 2) ** 0.5
    vn = float((v[0] ** 2 + v[1] ** 2)) ** 0.5
    dmax = abs(det(v, (y[0] - v[0], y[1] - v[1])))
    lat = tri_lattice(v, y)
    _, direct = transport((0, 0), [v])
    try:
        b, broken = transport((0, 0), [y, v])
        g = D.g[b]; cl = cyc_of(g)
        lab = broken == direct
        qpt = all(cl[broken[i]] == cl[direct[i]] for i in range(n))
        ypt = all(yorb(g, broken[i], broken[j]) == yorb(g, direct[i], direct[j])
                  for i, j in combinations(range(n), 2))
        sw = lambda t: sum(g[t[i]] == t[j] and g[t[j]] == t[i] for i, j in combinations(range(n), 2)
                           if i in SA and j in TB or i in TB and j in SA)
        same = (f'labels {lab}, Q-point per sheet {qpt}, Y-point per pair {ypt}; '
                f'M-hits (S=(2,2),T=(10,2)) chord {sw(direct)} broken {sw(broken)}')
    except AssertionError as e:
        same = f'broken path not clean ({e})'
    print(f'   v={tuple(map(int, v))} y=({float(y[0])},{float(y[1])}): |y-v|={eps:.3f} |v||y-v|={vn * eps:.3f} '
          f'|det(v,y-v)|={float(dmax):.3f}; lattice pts in triangle besides 0,v: {lat}; '
          f'broken path vs chord: {same}')

print(f'CPU seconds: {time.process_time() - t0:.2f}')
