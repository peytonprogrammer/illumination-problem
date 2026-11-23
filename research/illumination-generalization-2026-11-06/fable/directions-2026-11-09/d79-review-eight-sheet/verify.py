"""d79: referee checks for qclass-closure/bbbb/eight-sheet.md.

Reads only cell sets: cyl.rooms() (named rooms plus the saved d64 covers list) and three
hand-built rooms defined below. For every same-parity pair of interior lattice marks in a
room it computes the minimal monodromy block containing the 8 incident cells. No search
over rooms, rays, directions or reflection words.
Run: python3 -B verify.py > verify.log
"""
import sys
import time
from itertools import product
from pathlib import Path

D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D / 'd72-cylinder-test'))
import cyl  # noqa: E402  (cell data only)

QUAD = list(product((-1, 0), repeat=2))


def incid(cells, p):
    return sum((p[0] + dx, p[1] + dy) in cells for dx, dy in QUAD)


def edge_involutions(cells, cl, idx):
    """V[i]: cross the vertical edge at x = i mod 2; H[j]: horizontal edge at y = j mod 2.
    Cells are lower-left corners (i,j), so the cell spans [i,i+1] x [j,j+1]."""
    V, H = {}, {}
    for p in (0, 1):
        v, h = [0] * len(cl), [0] * len(cl)
        for c in cl:
            ex = c[0] if c[0] % 2 == p else c[0] + 1          # parity-p vertical edge
            nb = (c[0] - 1, c[1]) if ex == c[0] else (c[0] + 1, c[1])
            v[idx[c]] = idx.get(nb, idx[c])
            ey = c[1] if c[1] % 2 == p else c[1] + 1
            nb = (c[0], c[1] - 1) if ey == c[1] else (c[0], c[1] + 1)
            h[idx[c]] = idx.get(nb, idx[c])
        V[p], H[p] = v, h
    return V, H


def corner_perms(cells, cl, idx):
    """d78's construction (two 90-degree steps about the class-x corner), re-implemented."""
    perms = {}
    for x in product((0, 1), repeat=2):
        g = []
        for c in cl:
            p = next((c[0] + dx, c[1] + dy) for dx, dy in product((0, 1), repeat=2)
                     if ((c[0] + dx) % 2, (c[1] + dy) % 2) == x)
            cell, side = c, (c[0] + c[1]) % 2
            for _ in range(2):
                cx, cy = cell[0] + 0.5 - p[0], cell[1] + 0.5 - p[1]
                nx, ny = (-cy, cx) if side == 0 else (cy, -cx)
                c2 = (round(p[0] + nx - 0.5), round(p[1] + ny - 0.5))
                cell, side = (c2, side) if c2 in cells else (cell, 1 - side)
            g.append(idx[cell])
        perms[x] = g
    return perms


def mul(a, b):  # apply b first, then a
    return [a[b[i]] for i in range(len(b))]


def min_block(gens, n, seed):
    par = list(range(n))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
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
    return [i for i in range(n) if f(i) == r0]


def block_system(gens, n, B):
    blocks, seen = [frozenset(B)], set(B)
    k = 0
    while k < len(blocks):
        for g in gens:
            img = frozenset(g[i] for i in blocks[k])
            if not img & seen:
                blocks.append(img)
                seen |= img
        k += 1
    assert len(seen) == n
    return blocks


def star(P):
    return [(P[0] + dx, P[1] + dy) for dx, dy in QUAD]


def shape_ok(block_cells, S, T):
    """Is the block (S+F(u,v)) u (T+F(u,v)) for one pair of positive half-integers u,v?"""
    # centers relative to S
    cen = {(c[0] + 0.5, c[1] + 0.5) for c in block_cells}
    xs = sorted({abs(x - S[0]) for x, y in cen} | {abs(x - T[0]) for x, y in cen})
    ys = sorted({abs(y - S[1]) for x, y in cen} | {abs(y - T[1]) for x, y in cen})
    for u in xs:
        for v in ys:
            want = {(P[0] + sx * u, P[1] + sy * v) for P in (S, T) for sx in (1, -1) for sy in (1, -1)}
            if want == cen:
                return (u, v)
    return None


def segment_open(cells, S, T):
    """Axis-parallel S,T: is the closed segment inside the open room?"""
    if S[1] == T[1]:
        a, b = sorted((S[0], T[0]))
        pts = [(x, S[1]) for x in range(a, b + 1)]
        unit = [((x, S[1]), (x, S[1] - 1)) for x in range(a, b)]
    else:
        a, b = sorted((S[1], T[1]))
        pts = [(S[0], y) for y in range(a, b + 1)]
        unit = [((S[0], y), (S[0] - 1, y)) for y in range(a, b)]
    return all(incid(cells, p) == 4 for p in pts) and all(c1 in cells and c2 in cells for c1, c2 in unit)


def analyse(name, cells, pairs=None, verbose=False):
    cells = set(map(tuple, cells))
    cl = sorted(cells)
    idx = {c: i for i, c in enumerate(cl)}
    n = len(cl)
    V, H = edge_involutions(cells, cl, idx)
    for g in list(V.values()) + list(H.values()):
        assert all(g[g[i]] == i for i in range(n))
    g = corner_perms(cells, cl, idx)
    # check g_x is H V or V H for x = (i,j)
    form = {}
    for (i, j), gx in g.items():
        hv, vh = mul(H[j], V[i]), mul(V[i], H[j])
        assert gx in (hv, vh), (name, i, j)
        form[(i, j)] = 'HV' if gx == hv else 'VH'
    gens = list(g.values())
    pts = {(c[0] + dx, c[1] + dy) for c in cells for dx, dy in product((0, 1), repeat=2)}
    marks = sorted(p for p in pts if incid(cells, p) == 4)
    if pairs is None:
        pairs = [(S, T) for S in marks for T in marks
                 if S < T and (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0]
    out = []
    for S, T in pairs:
        seed = [idx[c] for c in star(S) + star(T)]
        B = min_block(gens, n, seed)
        rec = {'S': S, 'T': T, 'block': len(B)}
        if len(B) == 8:
            blocks = block_system(gens, n, B)
            Wgens = list(V.values()) + list(H.values())
            # W permutes the blocks
            bset = set(blocks)
            rec['W_invariant'] = all(frozenset(h[i] for i in b) in bset for h in Wgens for b in blocks)
            shapes = [shape_ok([cl[i] for i in b], S, T) for b in blocks]
            rec['all_blocks_shaped'] = all(s is not None for s in shapes)
            rec['offsets'] = sorted(shapes) if rec['all_blocks_shaped'] else None
            rec['aligned'] = S[0] == T[0] or S[1] == T[1]
            if S[1] == T[1]:
                mirror = {(c[0], 2 * S[1] - 1 - c[1]) for c in cells}
            else:
                mirror = {(2 * S[0] - 1 - c[0], c[1]) for c in cells}
            rec['mirror'] = rec['aligned'] and mirror == cells
            rec['segment_in_open_room'] = rec['aligned'] and segment_open(cells, S, T)
            rec['m'] = len(blocks)
        out.append(rec)
    return n, form, out


def bar_with_bumps():
    """24 cells: 8x2 bar [-2,6]x[-1,1], 2x1 bumps above and below at x in [-1,1] and [3,5]."""
    cells = {(x, y) for x in range(-2, 6) for y in (-1, 0)}
    cells |= {(x, y) for x in (-1, 0, 3, 4) for y in (-2, 1)}
    return cells


def transposed(cells):
    return {(y, x) for x, y in cells}


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def walls_and_reflex(cells):
    pts = {(c[0] + dx, c[1] + dy) for c in cells for dx, dy in product((0, 1), repeat=2)}
    refl = [p for p in pts if incid(cells, p) == 3]
    return sorted(refl)


def main():
    t0 = time.process_time()
    print('== Hand-built rooms ==')
    hb = [('bar24', bar_with_bumps(), [((0, 0), (4, 0))]),
          ('bar24T', transposed(bar_with_bumps()), [((0, 0), (0, 4))]),
          ('rect4x4', rect(-1, 3, -2, 2), [((0, 0), (2, 0))]),
          ('rect4x2', rect(-1, 3, -1, 1), [((0, 0), (2, 0))])]
    for name, cells, pairs in hb:
        n, form, out = analyse(name, cells, pairs)
        print(name, 'n=%d' % n, 'reflex=%s' % walls_and_reflex(cells), 'g_x forms', form)
        for rec in out:
            print('   ', rec)
        allpairs = analyse(name, cells)[2]
        print('    all same-parity pairs: block sizes', sorted({r['block'] for r in allpairs}),
              '; 8-blocks:', [(r['S'], r['T']) for r in allpairs if r['block'] == 8])
    print()
    print('== Saved rooms (cyl.rooms(): named rooms plus d64 covers.json) ==')
    rooms = cyl.rooms()
    hits, npairs, forms = [], 0, set()
    sizes = {}
    for name, cells in rooms:
        n, form, out = analyse(name, cells)
        forms.add(tuple(sorted(form.items())))
        npairs += len(out)
        for rec in out:
            if rec['block'] == 8:
                hits.append((name, n, rec))
        if name in ('R22', 'dumb12', 'CR34', 'DB55', 'DBas', 'DBw2', 'U2', 'c4181s', 'st279', 'st279b'):
            sizes[name] = (n, sorted({r['block'] for r in out}), len(out))
        if name == 'R22':
            r22 = [r for r in out if (r['S'], r['T']) == ((0, 0), (2, 2))]
    print('rooms', len(rooms), 'same-parity interior pairs', npairs)
    print('g_x factorisation patterns seen:', forms)
    for k, v in sizes.items():
        print('  %-7s n=%d minimal-block sizes over its pairs %s (%d pairs)' % (k, *v))
    print('R22 dark pair (0,0),(2,2):', r22)
    print('pairs whose 8 incident cells form a block:', len(hits))
    for name, n, rec in hits:
        print('  ', name, n, rec)
    bad = [h for h in hits if not (h[2]['W_invariant'] and h[2]['all_blocks_shaped'] and h[2]['mirror']
                                   and h[2]['segment_in_open_room'])]
    print('violations of (a)-(d) among them:', len(bad))
    print('CPU seconds: %.1f' % (time.process_time() - t0))


main()
