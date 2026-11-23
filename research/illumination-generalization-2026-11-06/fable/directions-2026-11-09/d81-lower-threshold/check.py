"""d81: saved-data check of the weak valency target d >= 2n/3.

Reads only cell sets: cyl.rooms() (the named rooms plus the normalized rooms saved in
d64-finite-case/data/covers.json) and the 9 BBBB room names in d72 cyl_H40.json.
For every room with area n >= 21 and r <= 8 it computes, for every distinct same-parity
pair of interior lattice marks, the marked valency d (d78 definition). Every pair with
3d < 2n gets an exact direct-visibility test (rational arithmetic). It also records the
block structure used in README.md. No search over rooms, rays, directions or words.
Permutation code is copied from d78-review-valency/verify.py (that file runs main() on
import).
Run: python3 -B check.py > check.log
"""
import json
import sys
import time
from collections import Counter
from fractions import Fraction as Fr
from itertools import permutations, product
from math import gcd, floor
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D / 'd72-cylinder-test'))
import cyl  # noqa: E402  (cell data only)

QUAD = list(product((-1, 0), repeat=2))


def incid(cells, p):
    return sum((p[0] + dx, p[1] + dy) in cells for dx, dy in QUAD)


# ---- copied from d78 verify.py -------------------------------------------------------
def branch_perms(cells):
    cl = sorted(cells)
    idx = {c: i for i, c in enumerate(cl)}

    def step(c, side, p):
        cx, cy = c[0] + 0.5 - p[0], c[1] + 0.5 - p[1]
        nx, ny = (-cy, cx) if side == 0 else (cy, -cx)
        c2 = (round(p[0] + nx - 0.5), round(p[1] + ny - 0.5))
        return (c2, side) if c2 in cells else (c, 1 - side)

    perms = {}
    for x in product((0, 1), repeat=2):
        g = [0] * len(cl)
        for c in cl:
            side = (c[0] + c[1]) % 2
            p = next((c[0] + dx, c[1] + dy) for dx, dy in product((0, 1), repeat=2)
                     if ((c[0] + dx) % 2, (c[1] + dy) % 2) == x)
            s = step(c, side, p)
            s = step(*s, p)
            g[idx[c]] = idx[s[0]]
        perms[x] = g
    return cl, idx, perms


def cycles(g):
    seen, out = set(), []
    for i in range(len(g)):
        if i not in seen:
            c, j = [], i
            while j not in seen:
                seen.add(j); c.append(j); j = g[j]
            out.append(c)
    return out


def normalized(cells):
    hor, ver = Counter(), Counter()
    for (i, j) in cells:
        hor[(i, j)] += 1; hor[(i, j + 1)] += 1
        ver[(i, j)] += 1; ver[(i + 1, j)] += 1
    hb = {e for e, k in hor.items() if k == 1}
    vb = {e for e, k in ver.items() if k == 1}

    def runs(es, axis):
        out, es = [], set(es)
        while es:
            e = min(es); L = 0
            while e in es:
                es.discard(e); L += 1
                e = (e[0] + 1, e[1]) if axis == 0 else (e[0], e[1] + 1)
            out.append(L)
        return out
    gh = gv = 0
    for L in runs(hb, 0):
        gh = gcd(gh, L)
    for L in runs(vb, 1):
        gv = gcd(gv, L)
    return gh == 1 and gv == 1


def orbitals(gens, n):
    orb, val = {}, {}
    for i in range(n):
        for j in range(n):
            if i == j or (i, j) in orb:
                continue
            key = (i, j); orb[key] = key; todo = [key]; size = 0
            while todo:
                a, b = todo.pop(); size += 1
                for g in gens:
                    z = (g[a], g[b])
                    if z not in orb:
                        orb[z] = key; todo.append(z)
            assert size % n == 0
            val[key] = size // n
    return orb, val
# ---------------------------------------------------------------------------------------


def min_block(gens, n, seed):
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    todo = [(seed[0], s) for s in seed[1:]]
    while todo:
        a, b = todo.pop()
        ra, rb = f(a), f(b)
        if ra == rb:
            continue
        par[ra] = rb
        for g in gens:
            todo.append((g[a], g[b]))
    r0 = f(seed[0])
    return frozenset(i for i in range(n) if f(i) == r0)


def all_blocks_at_0(gens, n):
    """All blocks containing sheet 0 (closure of joins of minimal ones)."""
    allb = {min_block(gens, n, [0, j]) for j in range(1, n)}
    frontier = set(allb)
    while frontier:
        new = set()
        for A in frontier:
            for B in list(allb):
                C = min_block(gens, n, sorted(A | B))
                if C not in allb:
                    new.add(C)
        allb |= new
        frontier = new
    return allb


def block_system(gens, n, B):
    blocks, seen, k = [B], set(B), 0
    while k < len(blocks):
        for g in gens:
            img = frozenset(g[i] for i in blocks[k])
            if not img & seen:
                blocks.append(img); seen |= img
        k += 1
    assert len(seen) == n
    return blocks


def structure(perms, n):
    """('prim', None) or ('k', k, m, zeros per pole of the maximal-block quotient)."""
    gens = list(perms.values())
    proper = [b for b in all_blocks_at_0(gens, n) if 1 < len(b) < n]
    if not proper:
        return {'type': 'primitive'}
    B = max(proper, key=len)
    blocks = block_system(gens, n, B)
    where = {i: bi for bi, b in enumerate(blocks) for i in b}
    zeros = {}
    for x, g in perms.items():
        q = [where[g[next(iter(b))]] for b in blocks]
        zeros[x] = sum(len(c) == 3 for c in cycles(q))
    return {'type': 'imprimitive', 'k': len(B), 'm': len(blocks), 'zeros': zeros,
            'where': where}


def point_open(cells, p):
    """Exact: is the rational point p in the open room (union of closed unit cells)?"""
    xs = [p[0] - 1, p[0]] if p[0].denominator == 1 else [floor(p[0])]
    ys = [p[1] - 1, p[1]] if p[1].denominator == 1 else [floor(p[1])]
    return all((int(x), int(y)) in cells for x in xs for y in ys)


def visible(cells, S, T):
    """Exact: is the closed segment ST contained in the open room?
    Breakpoints are the grid-line crossings; between two consecutive breakpoints the
    segment lies in one open cell or along one open unit edge, so checking every
    breakpoint and the midpoint of every gap is exact."""
    dx, dy = T[0] - S[0], T[1] - S[1]
    ts = {Fr(0), Fr(1)}
    for a, da in ((S[0], dx), (S[1], dy)):
        if da:
            lo, hi = sorted((a, a + da))
            ts |= {Fr(v - a, da) for v in range(lo, hi + 1)}
    ts = sorted(ts)
    samples = ts + [(u + v) / 2 for u, v in zip(ts, ts[1:])]
    return all(point_open(cells, (S[0] + t * dx, S[1] + t * dy)) for t in samples)


def main():
    t0 = time.process_time()
    bbbb = {k for k, v in json.loads((D / 'd72-cylinder-test/cyl_H40.json').read_text()).items()
            if v.get('group') == 'BBBB'}
    rooms = cyl.rooms()
    r22 = set(map(tuple, dict(rooms)['R22']))
    print('self-test: R22 dark pair (0,0),(2,2) visible =', visible(r22, (0, 0), (2, 2)))
    tally = Counter()           # (n-range, structure label) -> rooms
    low_rows, nrooms, npairs, nlow = [], 0, 0, 0
    min_ratio = None
    min_ratio8 = None
    struct_of = {}
    for name, cells in rooms:
        cells = set(map(tuple, cells))
        n = len(cells)
        pts = {(c[0] + dx, c[1] + dy) for c in cells for dx, dy in product((0, 1), repeat=2)}
        r = sum(incid(cells, p) == 3 for p in pts)
        if n < 21 or r > 8:
            continue
        assert normalized(cells), name
        cl, idx, perms = branch_perms(cells)
        gens = list(perms.values())
        assert sum(n - len(cycles(g)) for g in gens) == 2 * n - 2      # genus 0
        z = {x: sum(len(c) == 3 for c in cycles(g)) for x, g in perms.items()}
        assert sum(z.values()) == r
        nrooms += 1
        rel = Counter()
        for order in permutations(perms):
            for inv in product((False, True), repeat=4):
                acc = list(range(n))
                for x, iv in zip(order, inv):
                    g = perms[x]
                    if iv:
                        gi = [0] * n
                        for a, b in enumerate(g):
                            gi[b] = a
                        g = gi
                    acc = [g[a] for a in acc]
                if acc == list(range(n)):
                    rel[True] += 1
        assert rel[True], name                       # a product relation holds
        st = structure(perms, n)
        if st['type'] == 'imprimitive':
            assert st['k'] * sum(st['zeros'].values()) <= r   # Fact L charging
            assert st['k'] <= r
        orb, val = orbitals(gens, n)
        twotrans = len(val) == 1
        if st['type'] == 'primitive':
            label = 'primitive, ' + ('2-transitive' if twotrans else 'rank>2')
        else:
            zl = sorted(v for v in st['zeros'].values() if v)
            label = 'k=%d m=%d quotient zeros %s' % (st['k'], st['m'], zl)
        struct_of[name] = label
        tally[label] += 1
        marks = sorted(p for p in pts if incid(cells, p) == 4)

        def sheets(P):
            return [idx[(P[0] + a, P[1] + b)] for a, b in QUAD]
        for S in marks:
            for T in marks:
                if not (S < T and (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0):
                    continue
                npairs += 1
                keys = {orb[i, j] for i in sheets(S) for j in sheets(T)}
                d = sum(val[k] for k in keys)
                ratio = Fr(d, n)
                if min_ratio is None or ratio < min_ratio[0]:
                    min_ratio = (ratio, name, n, r, S, T, d)
                if st['type'] == 'imprimitive' and len({st['where'][i] for i in sheets(S) + sheets(T)}) == 1:
                    pass
                elif min_ratio8 is None or ratio < min_ratio8[0]:
                    min_ratio8 = (ratio, name, n, r, S, T, d, label)
                if 3 * d < 2 * n:
                    nlow += 1
                    vis = visible(cells, S, T)
                    allin1 = (st['type'] == 'imprimitive' and
                              len({st['where'][i] for i in sheets(S) + sheets(T)}) == 1)
                    low_rows.append((name, n, r, S, T, d, vis, allin1, label,
                                     'BBBB' if name in bbbb else ''))
    print('rooms with n>=21 and r<=8:', nrooms, '; same-parity interior pairs:', npairs)
    print('D72 BBBB rooms in range (dumb12 has n=20):', sorted(bbbb & set(struct_of)))
    print()
    print('structure of the maximal block system (rooms):')
    for lab, c in sorted(tally.items()):
        print('  %5d  %s' % (c, lab))
    print()
    print('pairs with 3d < 2n:', nlow)
    nonvis = [row for row in low_rows if not row[6]]
    print('  of which not directly visible:', len(nonvis))
    print('  of which all 8 marked sheets lie in one maximal block:', sum(r[7] for r in low_rows))
    by = Counter((row[1], row[8], row[6]) for row in low_rows)
    for key, c in sorted(by.items()):
        print('   n=%d  %-40s visible=%s  pairs=%d' % (key[0], key[1], key[2], c))
    print()
    print('low pairs (name, n, r, S, T, d, visible, all-8-in-one-block, structure):')
    for row in low_rows:
        print('  ', row)
    print()
    print('minimum d/n over all pairs:', min_ratio)
    print('minimum d/n over pairs whose 8 marked sheets are not in one maximal block:', min_ratio8)
    print('BBBB rooms:', {k: struct_of[k] for k in sorted(bbbb & set(struct_of))})
    print('CPU seconds: %.1f' % (time.process_time() - t0))


main()
