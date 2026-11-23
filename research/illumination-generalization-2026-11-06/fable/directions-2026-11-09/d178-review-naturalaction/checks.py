"""d178 checks for l1-natural-four-sites.md and l1-natural-marked-poles.md
(snapshot d95-review-queue/snapshots/1632).

Named rooms only: DB55 stretch at p = 53, 59, 61; Ferrers grid widths
5,3,2,1^11 (N_x=5, N_y=14); c4181s (d146 constructor).  No room, ray,
direction or word searches.  The monodromy model is d146's checks.py, loaded
by exec of its function definitions only (sections before '# ===...== 1').
"""
from collections import Counter
from math import comb, gcd
from pathlib import Path
import time

t0 = time.process_time()
HERE = Path(__file__).resolve().parent
src = (HERE.parent / 'd146-review-exdescent' / 'checks.py').read_text()
defs = src.split('# ' + '=' * 66 + ' 1')[0]
ns = {'__file__': str(HERE.parent / 'd146-review-exdescent' / 'checks.py')}
exec(compile(defs, 'd146-checks-defs', 'exec'), ns)
Double, closure, ctype, counts, wall_gcds, rect, stretch, cov4181 = (
    ns[k] for k in ('Double', 'closure', 'ctype', 'counts', 'wall_gcds', 'rect', 'stretch', 'cov4181'))
print('loaded d146 definitions:', sorted(k for k in ns if not k.startswith('_'))[:12], '...')


def hdr(s):
    print('=' * 78); print(s); print('=' * 78)


def inv(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return out


def compose(*ps):  # leftmost applied last
    n = len(ps[0]); out = list(range(n))
    for p in reversed(ps):
        out = [p[i] for i in out]
    return out


def strictly_simple(cells):
    """4-connected, no holes, no diagonal pinch lattice points."""
    cells = set(cells)
    start = next(iter(cells)); seen = {start}; st = [start]
    while st:
        x, y = st.pop()
        for nb in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nb in cells and nb not in seen:
                seen.add(nb); st.append(nb)
    conn = seen == cells
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    X0, X1, Y0, Y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    out = {(x, y) for x in range(X0, X1 + 1) for y in range(Y0, Y1 + 1)} - cells
    s = (X0, Y0); seen = {s}; st = [s]
    while st:
        x, y = st.pop()
        for nb in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nb in out and nb not in seen:
                seen.add(nb); st.append(nb)
    noholes = seen == out
    pinch = 0
    for (X, Y) in counts(cells):
        q = [(X - 1, Y - 1) in cells, (X, Y - 1) in cells, (X - 1, Y) in cells, (X, Y) in cells]
        if q == [True, False, False, True] or q == [False, True, True, False]:
            pinch += 1
    return conn and noholes and pinch == 0


def sign(p):
    return (-1) ** sum(L - 1 for L in ctype(p))


def primitive(D):
    gens = list(D.g.values())
    return all(len(closure(D.n, gens, [(0, j)])) == 1 for j in range(1, D.n))


def transitive(D):
    gens = list(D.g.values())
    seen = {0}; st = [0]
    while st:
        i = st.pop()
        for g in gens:
            if g[i] not in seen:
                seen.add(g[i]); st.append(g[i])
    return len(seen) == D.n


def tstr(p):
    c = Counter(ctype(p))
    return ' '.join(f'{L}^{c[L]}' for L in sorted(c))


ORDER = [(0, 0), (1, 0), (1, 1), (0, 1)]


def analyse(name, cells):
    D = Double(cells)
    W, gh, gv = wall_gcds(cells)
    cnt = counts(cells)
    r = sum(k == 3 for k in cnt.values())
    conv = sum(k == 1 for k in cnt.values())
    ss = strictly_simple(cells)
    g = D.g
    rel = compose(g[(0, 0)], inv(g[(1, 0)]), g[(1, 1)], inv(g[(0, 1)])) == list(range(D.n))
    print(f'[{name}] n={D.n} W={W} r={r} convex={conv} gcd(h)={gh} gcd(v)={gv} strictly_simple={ss}')
    print(f'   product g00 g10^-1 g11 g01^-1 = id: {rel}')
    for x in ORDER:
        sq = compose(g[x], g[x])
        sqt = Counter(ctype(sq))
        print(f'   site {x}: type {tstr(g[x])}  sign {sign(g[x]):+d}  square is a single 3-cycle: '
              f'{sqt[3] == 1 and sqt[1] == D.n - 3}')
    tr, pr = transitive(D), primitive(D)
    canon = {}
    for x in ORDER:
        pairs = [c for c in D.cycles(g[x]) if len(c) == 2]
        canon[x] = None if not pairs else len(closure(D.n, list(g.values()), pairs))
    print(f'   transitive {tr}; primitive (closure of (0,j) universal for all j) {pr}; '
          f'canonical B_x block counts {canon}')
    # interior lattice points by parity
    inter = Counter((P[0] % 2, P[1] % 2) for P, k in cnt.items() if k == 4)
    print(f'   interior lattice points by parity: {dict(sorted(inter.items()))}')
    return D, r


def poles(D, r, name):
    """Note 2 counts on the unordered-pair cover, computed by orbit enumeration."""
    n = D.n
    tot_swap = tot_fix2 = tot_fq = tot_reg_bad = 0
    fs = []
    rh = 0
    for x in ORDER:
        g = D.g[x]
        cyc = D.cycles(g)
        f = sum(len(c) == 1 for c in cyc); q = sum(len(c) == 2 for c in cyc); z = sum(len(c) == 3 for c in cyc)
        fs.append(f)
        rh += q + 2 * z
        clen = {i: len(c) for c in cyc for i in c}
        swap = fix2 = regbad = 0
        seen = set()
        for a in range(n):
            for b in range(a + 1, n):
                P = frozenset((a, b))
                if P in seen:
                    continue
                orb = [P]; seen.add(P)
                Q_ = frozenset((g[a], g[b]))
                while Q_ != P:
                    orb.append(Q_); seen.add(Q_)
                    u, v = tuple(Q_); Q_ = frozenset((g[u], g[v]))
                if len(orb) == 1:
                    if g[a] == b: swap += 1
                    else: fix2 += 1
                if len(orb) == 2 and 1 in (clen[a], clen[b]):
                    regbad += 1
        assert swap == q and fix2 == comb(f, 2) and regbad == f * q
        tot_swap += swap; tot_fix2 += fix2; tot_fq += regbad
    print(f'   [{name}] f_x={fs} sum f={sum(fs)} (r+4={r + 4}); sum(q+2z)={rh} (2n-2={2 * n - 2})')
    print(f'   swap poles={tot_swap} (2n-2-2r={2 * n - 2 - 2 * r}); fixed-2-set poles={tot_fix2}; '
          f'binom(r+4,2)={comb(r + 4, 2)}; regular Y-points with a convex-corner leg={tot_fq}')
    assert rh == 2 * n - 2 and sum(fs) == r + 4 and tot_swap == 2 * n - 2 - 2 * r
    assert tot_fix2 <= comb(sum(fs), 2)
    return tot_swap, tot_fix2, tot_fq


hdr('Note 1a: DB55 stretch rooms, l = p - 50')
db = {}
for p in (53, 59, 61):
    L = p - 50
    cells = rect(0, 5, 0, 5) | rect(5, 5 + L, 2, 3) | rect(5 + L, 10 + L, 0, 5)
    D, r = analyse(f'DB55 p={p} l={L}', cells)
    types = {tstr(D.g[x]) for x in ORDER}
    exp = f'1^2 2^{(p - 5) // 2} 3^1'
    signs = {sign(D.g[x]) for x in ORDER}
    print(f'   all four sites {exp}: {types == {exp}}; p mod 4 = {p % 4}; common sign {signs} '
          f'-> G = {"A_p" if signs == {1} else "S_p"} (given primitive + 3-cycle)')
    db[p] = (D, r)
# reproduce d146 p=53 data
D53 = db[53][0]
d146_53 = rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5)
print('p=53 cell set equals d146 DB55:', D53.cells == d146_53)

hdr('Note 1b: Ferrers grid widths 5,3,2,1^11 (N_x=5, N_y=14)')
widths = [5, 3, 2] + [1] * 11
fer = {(i, j) for j, w in enumerate(widths) for i in range(w)}
Df, rf = analyse('Ferrers 5,3,2,1x11', fer)
claimed = {(0, 0): '1^2 2^8 3^1', (1, 0): '1^3 2^9', (1, 1): '1^1 2^7 3^2', (0, 1): '1^1 2^10'}
print('   table matches note:', {x: tstr(Df.g[x]) == claimed[x] for x in ORDER})
inter_pts = sorted(P for P, k in counts(fer).items() if k == 4)
print('   interior lattice points:', inter_pts)

hdr('Note 1c: c4181s (d146: stretch(stretch(cov4181,0,1,2),1,4,3))')
c41 = stretch(stretch(cov4181(), 0, 1, 2), 1, 4, 3)
Dc, rc = analyse('c4181s', c41)
claimed = {(0, 0): '1^3 2^19', (1, 0): '1^4 2^8 3^7', (1, 1): '1^3 2^19', (0, 1): '1^2 2^18 3^1'}
print('   types match note (order 00,10,11,01):', {x: tstr(Dc.g[x]) == claimed[x] for x in ORDER})

hdr('Note 2a: pole counts on the unordered-pair cover Y')
for p in (53, 59, 61):
    D, r = db[p]
    s, f2, fq = poles(D, r, f'DB55 p={p}')
    print(f'      4(n-5)={4 * (D.n - 5)}: {fq == 4 * (D.n - 5)}')
poles(Df, rf, 'Ferrers21')
poles(Dc, rc, 'c4181s')

hdr('Note 2a: is binom(r+4,2) the max of sum binom(f_x,2)? (pure arithmetic, r<=8)')
for r in range(0, 9):
    best = max(sum(comb(f, 2) for f in fs) for fs in
               ((a, b, c, r + 4 - a - b - c) for a in range(r + 5) for b in range(r + 5 - a) for c in range(r + 5 - a - b)))
    print(f'   r={r}: max over 4-part compositions of r+4 = {best}; binom(r+4,2) = {comb(r + 4, 2)}; '
          f'swap-majority threshold n > {(comb(r + 4, 2) + 2 + 2 * r) // 2}')

print(f'CPU seconds: {time.process_time() - t0:.2f}')
