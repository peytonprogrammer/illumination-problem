"""Cell permutations of an orthogonal lattice room: for each parity class c, g_c rotates a cell by a half turn
about its class-c corner, in the billiard sense. The doubled room covers the pillowcase with these as branch data."""
import lines as L

QUAD = [(0, 0), (-1, 0), (-1, -1), (0, -1)]   # NE, NW, SW, SE cell offsets from a lattice point, counterclockwise

def perms(cells):
    cells = sorted(cells); idx = {c: i for i, c in enumerate(cells)}
    g = {c: list(range(len(cells))) for c in ((0, 0), (1, 0), (1, 1), (0, 1))}
    pts = {(x + dx, y + dy) for (x, y) in cells for dx in (0, 1) for dy in (0, 1)}
    info = {}
    for (px, py) in pts:
        cls = (px % 2, py % 2)
        present = [(px + dx, py + dy) in idx for dx, dy in QUAD]
        n = sum(present); info[(px, py)] = n
        if n == 4:
            arcs = None
        else:
            start = next(i for i in range(4) if present[i] and not present[i - 1])
            arc = [(start + k) % 4 for k in range(n)]
            assert all(present[i] for i in arc), 'pinched point'
        for qi in range(4):
            if not present[qi]: continue
            cell = (px + QUAD[qi][0], py + QUAD[qi][1])
            front = (cell[0] + cell[1]) % 2 == 0
            if n == 4:
                tq = (qi + 2) % 4
            else:
                seq = [('F', q) for q in arc] + [('B', q) for q in reversed(arc)]
                pos = seq.index(('F' if front else 'B', qi))
                tq = seq[(pos + 2) % len(seq)][1]
            g[cls][idx[cell]] = idx[(px + QUAD[tq][0], py + QUAD[tq][1])]
    return cells, g, info

def cyc(p):
    seen = set(); out = {}
    for i in range(len(p)):
        if i in seen: continue
        n = 0; j = i
        while j not in seen: seen.add(j); j = p[j]; n += 1
        out[n] = out.get(n, 0) + 1
    return dict(sorted(out.items()))

def orbits(gens, n):
    par = list(range(n))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for p in gens:
        for i in range(n): par[f(i)] = f(p[i])
    return len({f(i) for i in range(n)})

def block_system(gens, n, x):
    """Smallest invariant partition merging points 0 and x. Returns the number of blocks."""
    par = list(range(n))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    stack = [(0, x)]
    while stack:
        a, b = stack.pop(); a, b = f(a), f(b)
        if a == b: continue
        par[a] = b
        for p in gens: stack.append((p[a], p[b]))
    # closure: images of merged pairs must merge; iterate to a fixed point
    changed = True
    while changed:
        changed = False
        for p in gens:
            for i in range(n):
                a, b = f(p[i]), f(p[f(i)])
                if a != b: par[a] = b; changed = True
    return len({f(i) for i in range(n)})

def report(name, cells):
    cells, g, info = perms(cells); n = len(cells); gens = list(g.values())
    assert all(sorted(p) == list(range(n)) for p in gens)
    print(name, 'cells', n)
    for c, p in g.items(): print('   class', c, 'cycle type', cyc(p))
    comp = lambda p, q: [p[q[i]] for i in range(n)]
    ids = [o for o in __import__('itertools').permutations(gens) if comp(comp(o[0], o[1]), comp(o[2], o[3])) == list(range(n))]
    print('   some ordering multiplies to the identity:', bool(ids))
    print('   transitive:', orbits(gens, n) == 1)
    sizes = {block_system(gens, n, x) for x in range(1, n)}
    print('   primitive:', sizes == {1}, '' if sizes == {1} else 'block counts %s' % sorted(sizes))

if __name__ == '__main__':
    import json
    row = open('../d237-dark-examples-w22-26/astra/dark.tsv').read().split('\n')[1].split('\t')
    report('22-wall dark room', {(c[0], c[1]) for c in json.loads(row[3])})
    report('pyramid (4,5,12;3,4,1,2)', L.pyramid(4, 5, 12, 3, 4, 1, 2))
    report('gap room (4,5,60;8,4,1,2)', L.pyramid(4, 5, 60, 8, 4, 1, 2))
