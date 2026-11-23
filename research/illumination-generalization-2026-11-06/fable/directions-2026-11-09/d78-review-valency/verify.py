"""d78: independent recomputation of marked valency d for the D72 BBBB rooms.

Only the cell sets (via cyl.rooms) and the saved pair list (cyl_H40.json) are read.
The four branch permutations are rebuilt here from cells, without pair_level or cyl
code paths. No search over rooms, rays, directions or reflection words.
Run: python3 -B verify.py
"""
import json
import sys
from collections import Counter
from itertools import product
from math import gcd
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D / 'd72-cylinder-test'))
import cyl  # noqa: E402  (used only for cell data)


def incid(cells, p):
    return sum((p[0] + dx, p[1] + dy) in cells for dx, dy in product((-1, 0), repeat=2))


def branch_perms(cells):
    """g_x for x in Z^2/2Z^2. Sheets = cells; sheet square of cell (i,j) is front if
    i+j even, back otherwise. g_x = two 90-degree steps about the class-x corner,
    counterclockwise on the front face and clockwise (in plane coordinates) on the back."""
    cl = sorted(cells)
    idx = {c: i for i, c in enumerate(cl)}

    def step(c, side, p):
        # rotate cell c about corner p by +90 (front) or -90 (back)
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
            s = (c, side)
            s = step(*s, p)
            s = step(*s, p)
            assert (s[0][0] + s[0][1]) % 2 == s[1]
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


def check_structure(cells, cl, idx, perms):
    n = len(cl)
    # each cycle of g_x is the star of one lattice point; length = 1,2,3 per incidence
    pts = {(c[0] + dx, c[1] + dy) for c in cells for dx, dy in product((0, 1), repeat=2)}
    r = sum(incid(cells, p) == 3 for p in pts)
    for x, g in perms.items():
        for cyc in cycles(g):
            corners = set.intersection(*[{(cl[i][0] + dx, cl[i][1] + dy)
                                          for dx, dy in product((0, 1), repeat=2)} for i in cyc])
            corners = [p for p in corners if (p[0] % 2, p[1] % 2) == x]
            assert len(corners) == 1, cyc
            k = incid(cells, corners[0])
            assert len(cyc) == {1: 1, 2: 2, 3: 3, 4: 2}[k]
    # genus 0 by Riemann-Hurwitz: sum(n - #cycles) = 2n - 2
    assert sum(n - len(cycles(g)) for g in perms.values()) == 2 * n - 2
    # transitivity
    seen, todo = {0}, [0]
    while todo:
        i = todo.pop()
        for g in perms.values():
            if g[i] not in seen:
                seen.add(g[i]); todo.append(g[i])
    assert len(seen) == n
    return r


def normalized(cells):
    """gcd of maximal horizontal wall lengths and of vertical wall lengths."""
    h, v = [], []
    hor = Counter()  # unit horizontal boundary edges (x, y)
    ver = Counter()
    for (i, j) in cells:
        for e in (((i, j), 'h'), ((i, j + 1), 'h'), ((i, j), 'v'), ((i + 1, j), 'v')):
            (hor if e[1] == 'h' else ver)[e[0]] += 1
    hb = {e for e, k in hor.items() if k == 1}
    vb = {e for e, k in ver.items() if k == 1}

    def runs(es, axis):
        out, es = [], set(es)
        while es:
            e = min(es)
            L = 0
            while e in es:
                es.discard(e); L += 1
                e = (e[0] + 1, e[1]) if axis == 0 else (e[0], e[1] + 1)
            out.append(L)
        return out
    # a run can only be split by a corner where the perpendicular wall meets; for a
    # strictly simple room collinear boundary edges are contiguous iff no corner between,
    # so splitting into maximal runs of collinear contiguous edges gives the walls.
    gh = gv = 0
    for L in runs(hb, 0):
        gh = gcd(gh, L)
    for L in runs(vb, 1):
        gv = gcd(gv, L)
    return gh == 1 and gv == 1


def orbitals(perms, n):
    gens = list(perms.values())
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


def blocks_containing_0(perms, n):
    gens = list(perms.values())

    def closure(seed):
        par = list(range(n))

        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        pairs = [(seed[0], s) for s in seed[1:]]
        for a, b in pairs:
            ra, rb = f(a), f(b)
            if ra != rb:
                par[ra] = rb
        changed = True
        while changed:
            changed = False
            # fixpoint of the block relation: i ~ j implies g i ~ g j
            cls = {}
            for i in range(n):
                cls.setdefault(f(i), []).append(i)
            for g in gens:
                for c in cls.values():
                    for t in c[1:]:
                        ra, rb = f(g[c[0]]), f(g[t])
                        if ra != rb:
                            par[ra] = rb; changed = True
        return frozenset(i for i in range(n) if f(i) == f(0))
    mins = {closure([0, j]) for j in range(1, n)}
    allb = set(mins)
    frontier = set(mins)
    while frontier:
        new = set()
        for A in frontier:
            for Bk in list(allb):
                C = closure(sorted(A | Bk))
                if C not in allb:
                    new.add(C)
        allb |= new
        frontier = new
    return sorted(allb, key=len)


def system(perms, n, B):
    gens = list(perms.values())
    blocks = [B]
    seen = set(B)
    while len(seen) < n:
        for blk in list(blocks):
            for g in gens:
                img = frozenset(g[i] for i in blk)
                if not img & seen:
                    blocks.append(img); seen |= img
    return blocks


def quotient(perms, blocks):
    where = {i: bi for bi, b in enumerate(blocks) for i in b}
    return {x: [where[g[next(iter(b))]] for b in blocks] for x, g in perms.items()}


def k_transitive_count(qperms, m, k):
    """number of orbits on ordered k-tuples of distinct points"""
    from itertools import permutations
    gens = list(qperms.values())
    seen, norb = set(), 0
    for t in permutations(range(m), k):
        if t in seen:
            continue
        norb += 1; seen.add(t); todo = [t]
        while todo:
            u = todo.pop()
            for g in gens:
                w = tuple(g[i] for i in u)
                if w not in seen:
                    seen.add(w); todo.append(w)
    return norb


def main():
    data = json.loads((D / 'd72-cylinder-test/cyl_H40.json').read_text())
    rooms = dict(cyl.rooms())
    total = 0
    for name, rec in data.items():
        if rec['group'] != 'BBBB':
            continue
        cells = set(map(tuple, rooms[name]))
        cl, idx, perms = branch_perms(cells)
        n = len(cl)
        r = check_structure(cells, cl, idx, perms)
        orb, val = orbitals(perms, n)
        vals = sorted(val.values())

        def sheets(P):
            out = [idx[(P[0] + dx, P[1] + dy)] for dx, dy in product((-1, 0), repeat=2)]
            assert incid(cells, P) == 4
            return out
        counts = Counter()
        for p in rec['pairs']:
            S, T = tuple(p['S']), tuple(p['T'])
            assert (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0 and S != T
            keys = {orb[i, j] for i in sheets(S) for j in sheets(T)}
            counts[sum(val[k] for k in keys)] += 1
        total += sum(counts.values())
        bl = blocks_containing_0(perms, n)
        proper = [b for b in bl if 1 < len(b) < n]
        info = 'primitive'
        if proper:
            Bmax = max(proper, key=len)
            maxes = [b for b in proper if len(b) == len(Bmax)]
            blocks = system(perms, n, Bmax)
            q = quotient(perms, blocks)
            m = len(blocks)
            zeros = sum(len(c) == 3 for g in q.values() for c in cycles(g))
            t2 = k_transitive_count(q, m, 2)
            t3 = k_transitive_count(q, m, 3) if m <= 30 else None
            sizes = sorted({len(b) for b in proper})
            # are the incident sheets of each pair split across maximal blocks?
            where = {i: bi for bi, b in enumerate(blocks) for i in b}
            allin1 = sum(len({where[i] for i in sheets(tuple(p['S'])) + sheets(tuple(p['T']))}) == 1
                         for p in rec['pairs'])
            info = (f'block sizes {sizes}; maximal k={len(Bmax)} (#max blocks at 0: {len(maxes)}), '
                    f'm={m}, quotient zeros={zeros}, orbits on ordered 2-tuples={t2}, 3-tuples={t3}, '
                    f'pairs with all 8 sheets in one block={allin1}')
        print(f'{name} n={n} r={r} normalized={normalized(cells)} orbital valencies={vals} '
              f'd-counts={sorted(counts.items())} | {info}')
    print('pairs', total)


main()
