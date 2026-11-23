"""One fixed polygon: the pinwheel octomino (2 x 2 block with four cells attached in a
pinwheel).  Computes the monodromy group of its double over the unit pillowcase.

This is not a room search.  It tests one guess: that this room has a primitive group that
does not contain A_n.  The guess is false.  The output is |G| = 96 and "primitive: False".
So this room is not an example for the range n <= N_0 of the companion reduction.

Run: python3 -B pinwheel.py
"""
from itertools import product

CELLS = [(0, 0), (-1, 0), (0, -1), (-1, -1), (1, 0), (-1, 1), (-2, -1), (0, -2)]
IDX = {c: k for k, c in enumerate(CELLS)}


def g(px, py):
    """rotation by pi about the lattice points of parity class (px, py), as a map on cells"""
    out = []
    for (i, j) in CELLS:
        cx = i if i % 2 == px else i + 1          # the corner of the cell in the class
        cy = j if j % 2 == py else j + 1
        # cross the vertical edge at the corner, then the horizontal edge at the corner
        i2 = 2 * cx - 1 - i
        c = (i2, j) if (i2, j) in IDX else (i, j)
        j2 = 2 * cy - 1 - c[1]
        c = (c[0], j2) if (c[0], j2) in IDX else c
        out.append(IDX[c])
    return tuple(out)


def cyc(p):
    seen, t = set(), []
    for s in range(len(p)):
        if s not in seen:
            L, x = 0, s
            while x not in seen:
                seen.add(x)
                x = p[x]
                L += 1
            t.append(L)
    return sorted(t, reverse=True)


gens = {name: g(px, py) for name, (px, py) in
        dict(a=(0, 0), b=(1, 0), c=(0, 1), d=(1, 1)).items()}
for name, p in gens.items():
    print(name, cyc(p), p)
e = tuple(range(8))
G = {e}
fr = [e]
while fr:
    nf = []
    for x in fr:
        for p in gens.values():
            y = tuple(p[i] for i in x)
            if y not in G:
                G.add(y)
                nf.append(y)
    fr = nf
print('|G| =', len(G), ' all even:', all(sum(L - 1 for L in cyc(x)) % 2 == 0 for x in G))
# primitivity: no nontrivial block containing 0
prim = True
for j in range(1, 8):
    par = list(range(8))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    par[find(j)] = find(0)
    ch = True
    while ch:
        ch = False
        for p in gens.values():
            for u, v in product(range(8), repeat=2):
                if find(u) == find(v) and find(p[u]) != find(p[v]):
                    par[find(p[u])] = find(p[v])
                    ch = True
    if len({find(x) for x in range(8)}) > 1:
        prim = False
print('primitive:', prim)
