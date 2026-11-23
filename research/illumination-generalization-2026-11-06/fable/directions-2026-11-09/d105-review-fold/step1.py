"""Exact star count and parity-darkness check for R34-base (d8 rooms.json)."""
import json, sys
from math import gcd
from pathlib import Path
rooms = json.load(open(Path(__file__).resolve().parent.parent / 'd8-perturbation-test/rooms.json'))
name = sys.argv[1] if len(sys.argv) > 1 else 'R34-base'
room = next(r for r in rooms if r['id'] == name)
cells = {tuple(c) for c in room['cells']}   # cell (i,j) = [i,i+1]x[j,j+1]
print(name, 'cells', len(cells), 'marks', room['marks'])
pts = {(i + dx, j + dy) for i, j in cells for dx in (0, 1) for dy in (0, 1)}
def star(p):
    x, y = p
    return [c for c in ((x, y), (x - 1, y), (x - 1, y - 1), (x, y - 1)) if c in cells]
kind = {1: 'convex', 2: 'smooth', 3: 'reflex', 4: 'interior'}
cnt = {}; pinch = []; byk = {}
for p in sorted(pts):
    s = star(p); k = len(s)
    if k == 2 and s[0][0] != s[1][0] and s[0][1] != s[1][1]:
        pinch.append(p); continue
    byk.setdefault(kind[k], []).append(p)
for k in kind.values():
    print(k, len(byk.get(k, [])), byk[k] if k in ('smooth', 'interior') else '')
print('pinches', pinch)
reg = byk['smooth'] + byk['interior']
print('regular-site parities', sorted({(x % 2, y % 2) for x, y in reg}))
r = len(byk['reflex']); print('r =', r, 'W = 2r+4 =', 2 * r + 4)
# connectivity and holes: Euler check V - E + F = 1 for a simply connected union
edges = set()
for i, j in cells:
    edges |= {((i, j), (i + 1, j)), ((i, j + 1), (i + 1, j + 1)), ((i, j), (i, j + 1)), ((i + 1, j), (i + 1, j + 1))}
print('Euler V-E+F =', len(pts) - len(edges) + len(cells))
# Monodromy of the double over the pillowcase, block systems by closure
cl = sorted(cells); idx = {c: n for n, c in enumerate(cl)}
def inv(axis, par):
    out = []
    for (i, j) in cl:
        if axis == 'x':   # cross vertical edge at x = line with line % 2 == par
            line = i if i % 2 == par else i + 1
            nb = (2 * line - i - 1, j)
        else:
            line = j if j % 2 == par else j + 1
            nb = (i, 2 * line - j - 1)
        out.append(idx.get(nb, idx[(i, j)]))
    return out
gens = [inv(a, p) for a in 'xy' for p in (0, 1)]
n = len(cl)
def closure(a, b):
    parent = list(range(n))
    def f(u):
        while parent[u] != u: parent[u] = parent[parent[u]]; u = parent[u]
        return u
    todo = [(a, b)]
    while todo:
        u, v = todo.pop(); ru, rv = f(u), f(v)
        if ru == rv: continue
        parent[ru] = rv
        for g in gens: todo.append((g[u], g[v]))
    return len({f(u) for u in range(n)})
print('degree n =', n, '; minimal block systems from pair {0,j}: block counts', sorted({closure(0, j) for j in range(1, n)}))
# Parity darkness: any unfolded displacement is even-even; first primitive lattice step has an odd coordinate
S, T = room['marks'] if room['marks'] else byk['interior'][:2]
seen = {cl[0]}; stack = [cl[0]]
while stack:
    i, j = stack.pop()
    for nb in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
        if nb in cells and nb not in seen: seen.add(nb); stack.append(nb)
print('edge-connected cells', len(seen), 'of', n)
# Parity argument, checked arithmetically on every even displacement in a box:
# the first lattice point on S->S+D is strictly before the end and is not even-even.
bad = 0
for u in range(-40, 41):
    for v in range(-40, 41):
        if (u, v) == (0, 0): continue
        D = (2 * u, 2 * v); g = gcd(*map(abs, D)); step = (D[0] // g, D[1] // g)
        if g < 2 or (step[0] % 2 == 0 and step[1] % 2 == 0): bad += 1
print('even displacements violating the parity step:', bad)
