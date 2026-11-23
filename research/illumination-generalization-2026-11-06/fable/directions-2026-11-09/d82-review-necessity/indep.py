"""d82: independent recomputation for the review of midpoint-necessity.md and d81.

Reads only cell sets of named rooms (d72 cyl.rooms()). Builds the four pole monodromies
from scratch by walking quadrants around each lattice point of the room double (not the
d78 step() code), then:
  A. R22 dark pair (0,0),(2,2): marked union, d, and the diagonal budget 2d = R + J split
     by pole class relative to S, with the location of every regular coincidence.
  B. Marked valency d for every same-parity interior pair in cov2493, cov3397, st279,
     compared with d81 check.py's own functions; block structure of cov2493.
No search over rooms, rays, directions or reflection words.
Run: python3 -B indep.py
"""
import sys
import time
from itertools import product
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D / 'd72-cylinder-test'))
import cyl  # noqa: E402  (cell data only)


def par(c):
    return (c[0] + c[1]) % 2


def arc(cells, p):
    """Cells around lattice point p in counterclockwise order, as a list starting after a
    missing quadrant (boundary point) or a 4-cycle flag (interior point)."""
    ring = [(p[0], p[1]), (p[0] - 1, p[1]), (p[0] - 1, p[1] - 1), (p[0], p[1] - 1)]
    have = [c in cells for c in ring]
    if all(have):
        return ring, True
    k = next(i for i in range(4) if not have[i] and have[(i + 1) % 4])
    rot = ring[k + 1:] + ring[:k + 1]
    hv = [c in cells for c in rot]
    out = [c for c, h in zip(rot, hv) if h]
    # strictly simple: present cells are contiguous
    j = len(out)
    assert hv[:j] == [True] * j and not any(hv[j:]), (p, rot, hv)
    return out, False


def monodromy(cells):
    cl = sorted(cells)
    idx = {c: i for i, c in enumerate(cl)}
    pts = {(c[0] + a, c[1] + b) for c in cells for a, b in product((0, 1), repeat=2)}
    g = {x: [None] * len(cl) for x in product((0, 1), repeat=2)}
    local = []   # (pole class, point, kind, list of sheet cycles)
    for p in sorted(pts):
        x = (p[0] % 2, p[1] % 2)
        cs, interior = arc(cells, p)
        if interior:
            # side 0 ccw and side 1 cw are separate 4-cycles of quadrants; +2 = opposite cell
            cyc = [[idx[cs[0]], idx[cs[2]]], [idx[cs[1]], idx[cs[3]]]]
            kind = 'interior'
        else:
            seq = [(c, 0) for c in cs] + [(c, 1) for c in reversed(cs)]
            L = len(seq)
            front = [i for i, (c, s) in enumerate(seq) if s == par(c)]
            nxt = {}
            for i in front:
                c2, s2 = seq[(i + 2) % L]
                assert s2 == par(c2)
                nxt[idx[seq[i][0]]] = idx[c2]
            seen, cyc = set(), []
            for a in nxt:
                if a in seen:
                    continue
                cy, b = [], a
                while b not in seen:
                    seen.add(b); cy.append(b); b = nxt[b]
                cyc.append(cy)
            kind = {1: 'convex', 2: 'smooth', 3: 'reflex'}[len(cs)]
        for cy in cyc:
            for i, a in enumerate(cy):
                assert g[x][a] is None
                g[x][a] = cy[(i + 1) % len(cy)]
        local.append((x, p, kind, cyc))
    for x in g:
        assert None not in g[x]
    return cl, idx, g, local


def orbit_partition(gens, n):
    lab = {}
    sizes = {}
    for i in range(n):
        for j in range(n):
            if i == j or (i, j) in lab:
                continue
            key = (i, j); lab[key] = key; st = [key]; s = 0
            while st:
                a, b = st.pop(); s += 1
                for gg in gens:
                    z = (gg[a], gg[b])
                    if z not in lab:
                        lab[z] = key; st.append(z)
            sizes[key] = s
    return lab, sizes


def star(idx, P):
    return [idx[(P[0] + a, P[1] + b)] for a, b in product((-1, 0), repeat=2)]


def marked_union(lab, idx, S, T):
    return {lab[i, j] for i in star(idx, S) for j in star(idx, T)}


def part_A(rooms):
    cells = set(map(tuple, rooms['R22']))
    S, T = (0, 0), (2, 2)
    cl, idx, g, local = monodromy(cells)
    n = len(cl)
    gens = list(g.values())
    lab, sizes = orbit_partition(gens, n)
    keys = marked_union(lab, idx, S, T)
    d = sum(sizes[k] for k in keys) // n
    r = sum(k == 'reflex' for _, _, k, _ in local)
    rel = lambda x: ((x[0] - S[0]) % 2, (x[1] - S[1]) % 2)
    R, J, where = {}, {}, []
    for x, p, kind, cyc in local:
        for cy in cyc:
            if len(cy) == 2:
                if lab[cy[0], cy[1]] in keys:
                    R[rel(x)] = R.get(rel(x), 0) + 1; where.append((p, kind))
            elif len(cy) == 3:
                for s in (1, 2):
                    if lab[cy[0], cy[s]] in keys:
                        J[rel(x)] = J.get(rel(x), 0) + 1
    print('A. R22 n=%d r=%d marked orbits=%d d=%d 2d=%d' % (n, r, len(keys), d, 2 * d))
    print('   regular coincidences by relative class:', dict(sorted(R.items())), 'total', sum(R.values()))
    print('   reflex branches by relative class:     ', dict(sorted(J.items())), 'total', sum(J.values()))
    print('   regular coincidence locations:', sorted(where))
    print('   reflex corners carrying both branches in the union:',
          sum(1 for x, p, k, cyc in local if k == 'reflex'
              and all(lab[cyc[0][0], cyc[0][s]] in keys for s in (1, 2))), 'of', r)
    assert 2 * d == sum(R.values()) + sum(J.values())
    # full off-diagonal budget: every room has total 2n-2 = (#regular points) + 2r
    regs = sum(len(cy) == 2 for _, _, _, cyc in local for cy in cyc)
    print('   all-orbit budget: regular points %d + 2r %d = %d = 2n-2 %d' % (regs, 2 * r, regs + 2 * r, 2 * n - 2))
    floor_half = n // 2
    print('   capacity check: R_a=%d <= floor(n/2)=%d' % (R.get((0, 0), 0), floor_half))


def load_d81():
    src = (D / 'd81-lower-threshold' / 'check.py').read_text()
    src = src.rsplit('\nmain()', 1)[0]
    ns = {'__file__': str(D / 'd81-lower-threshold' / 'check.py'), '__name__': 'd81'}
    exec(compile(src, 'd81check', 'exec'), ns)
    return ns


def my_blocks(gens, n):
    """All blocks containing sheet 0, by brute closure from minimal blocks (own code)."""
    def minblock(seed):
        comp = {i: {i} for i in range(n)}
        rep = list(range(n))

        def find(a):
            while rep[a] != a:
                a = rep[a]
            return a
        stack = [(seed[0], s) for s in seed[1:]]
        while stack:
            a, b = stack.pop()
            ra, rb = find(a), find(b)
            if ra == rb:
                continue
            if len(comp[ra]) < len(comp[rb]):
                ra, rb = rb, ra
            rep[rb] = ra; comp[ra] |= comp.pop(rb)
            for gg in gens:
                stack.append((gg[a], gg[b]))
        return frozenset(comp[find(seed[0])])
    blocks = {minblock([0, j]) for j in range(1, n)}
    grew = True
    while grew:
        grew = False
        for A in list(blocks):
            for B in list(blocks):
                C = minblock(sorted(A | B))
                if C not in blocks:
                    blocks.add(C); grew = True
    return blocks


def part_B(rooms, ns):
    for name in ('cov2493', 'cov3397', 'st279'):
        cells = set(map(tuple, rooms[name]))
        cl, idx, g, local = monodromy(cells)
        n = len(cl)
        r = sum(k == 'reflex' for _, _, k, _ in local)
        gens = list(g.values())
        lab, sizes = orbit_partition(gens, n)
        # d81's own code on the same room
        _, idx2, perms2 = ns['branch_perms'](cells)
        orb2, val2 = ns['orbitals'](list(perms2.values()), n)
        assert idx2 == idx
        pts = {(c[0] + a, c[1] + b) for c in cells for a, b in product((0, 1), repeat=2)}
        marks = sorted(p for p in pts if ns['incid'](cells, p) == 4)
        mism, ds = 0, []
        for S in marks:
            for T in marks:
                if not (S < T and (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0):
                    continue
                d = sum(sizes[k] for k in marked_union(lab, idx, S, T)) // n
                keys2 = {orb2[i, j] for i in ns['sheets_fn'](idx2, S) for j in ns['sheets_fn'](idx2, T)}
                d2 = sum(val2[k] for k in keys2)
                mism += d != d2
                ds.append(d)
        prop = [b for b in my_blocks(gens, n) if 1 < len(b) < n]
        k = max(map(len, prop)) if prop else None
        # cycle-type comparison of the two constructions
        ct = lambda gg: sorted(len(c) for c in ns['cycles'](gg))
        same_ct = all(ct(g[x]) == ct(perms2[x]) for x in g)
        same_perm = all(g[x] == perms2[x] or g[x] == [perms2[x].index(i) for i in range(n)] for x in g)
        print('B. %-8s n=%d r=%d pairs=%d min d=%d (2n/3=%.2f) d-mismatches vs d81=%d '
              'maximal block size=%s m=%s cycle types equal=%s perms equal up to inverse=%s'
              % (name, n, r, len(ds), min(ds), 2 * n / 3, mism, k, n // k if k else None,
                 same_ct, same_perm))


def main():
    t0 = time.process_time()
    rooms = dict(cyl.rooms())
    part_A(rooms)
    ns = load_d81()
    ns['sheets_fn'] = lambda idx, P: [idx[(P[0] + a, P[1] + b)] for a, b in ns['QUAD']]
    part_B(rooms, ns)
    print('CPU seconds: %.1f' % (time.process_time() - t0))


main()
