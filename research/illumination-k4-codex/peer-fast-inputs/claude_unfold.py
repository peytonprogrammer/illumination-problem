"""Independent unfolding audit of the three control rooms (no Codex helpers, no rays).

Surface X = room x D4 / ~: copy (t, g) develops to g(t). Across a shared, unslit room edge,
(t, g) meets (t', g). Across a wall or slit side with linear reflection s, (t, g) meets
(t, g s). Vertices are union-find classes of (t, g, corner), glued only through edges, so a
boundary contact point splits correctly. Checks: cone data, genus, marks, the half-turn
rho(t, g) = (t, -g), its fixed set, translation automorphisms, and the absolute period lattice.
"""
import json
import sys
from collections import Counter, deque
from fractions import Fraction
from functools import reduce
from itertools import combinations, product
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
CTX = HERE.parents[1]
G = [((a, b), (c, d)) for a, b, c, d in product((-1, 0, 1), repeat=4)
     if abs(a*d-b*c) == 1 and (a*a+c*c, b*b+d*d, a*b+c*d) == (1, 1, 0)]
assert len(G) == 8
mul = lambda g, h: tuple(tuple(sum(g[i][k]*h[k][j] for k in range(2)) for j in range(2)) for i in range(2))
app = lambda g, p: (g[0][0]*p[0]+g[0][1]*p[1], g[1][0]*p[0]+g[1][1]*p[1])
NEG = ((-1, 0), (0, -1))


def refl(e):
    (x0, y0), (x1, y1) = e
    dx, dy = x1-x0, y1-y0
    n = dx*dx+dy*dy  # reflection fixing direction (dx, dy): 2 v v^T / |v|^2 - I
    return ((Fraction(dx*dx-dy*dy, n), Fraction(2*dx*dy, n)), (Fraction(2*dx*dy, n), Fraction(dy*dy-dx*dx, n)))


def angle(t, p):
    """Interior angle at corner p in 45-degree units."""
    a, b = [q for q in t if q != p]
    u, v = (a[0]-p[0], a[1]-p[1]), (b[0]-p[0], b[1]-p[1])
    return 2 if u[0]*v[0]+u[1]*v[1] == 0 else 1


def audit(name):
    d = json.loads((CTX/name).read_text())
    tiles = [tuple(sorted(map(tuple, t))) for t in d['triangles']]
    slits = {tuple(sorted(map(tuple, s))) for s in d.get('slits', [])}
    owners = {}
    for i, t in enumerate(tiles):
        for e in combinations(t, 2):
            owners.setdefault(e, []).append(i)
    cells = [(i, g) for i in range(len(tiles)) for g in G]
    cid = {c: k for k, c in enumerate(cells)}
    par = {}
    find = lambda x: x if par.setdefault(x, x) == x else (par.__setitem__(x, find(par[x])) or par[x])
    union = lambda a, b: par.__setitem__(find(a), find(b))
    nbr = {}  # (cell, edge) -> cell
    for e, own in owners.items():
        for i in own:
            for g in G:
                if len(own) == 2 and e not in slits:
                    j = own[0] if own[1] == i else own[1]; h = g
                else:
                    j = i; s = refl(e); h = mul(g, tuple(tuple(int(v) for v in r) for r in s))
                nbr[(i, g), e] = (j, h)
                for p in e:
                    union((i, g, p), (j, h, p))
    classes = {}
    for i, g in cells:
        for p in tiles[i]:
            classes.setdefault(find((i, g, p)), []).append((i, g, p))
    ang = {r: sum(angle(tiles[i], p) for i, g, p in m) for r, m in classes.items()}
    assert all(a % 8 == 0 for a in ang.values())
    m = {r: a//8 for r, a in ang.items()}
    V, E, Fc = len(classes), len(cells)*3//2, len(cells)
    chi = V-E+Fc; genus = (2-chi)//2
    marks = [tuple(p) for p in d['marked']]
    mark_lifts = [{r for r, mm in classes.items() if mm[0][2] == q} for q in marks]
    # half-turn rho: (t, g) -> (t, -g); vertex class map
    rho = {r: find((mm[0][0], mul(NEG, mm[0][1]), mm[0][2])) for r, mm in classes.items()}
    fixed = {r for r in classes if rho[r] == r}
    regular = {r for r in classes if m[r] == 1}
    # developed positions: BFS placing cell (i, g) at g(t_i) + offset
    dev = lambda c: [app(c[1], p) for p in tiles[c[0]]]
    off = {cells[0]: (0, 0)}; q = deque([cells[0]]); periods = set()
    for c in cells:
        pass
    while q:
        c = q.popleft()
        for e in combinations(tiles[c[0]], 2):
            c2 = nbr[c, e]
            # the shared edge e of t develops to c[1](e)+off[c] and c2[1](e)+off[c2]; must match as sets
            a = sorted((app(c[1], p)[0]+off[c][0], app(c[1], p)[1]+off[c][1]) for p in e)
            b0 = sorted(app(c2[1], p) for p in e)
            o2 = (a[0][0]-b0[0][0], a[0][1]-b0[0][1])
            assert sorted((x+o2[0], y+o2[1]) for x, y in b0) == a
            if c2 not in off:
                off[c2] = o2; q.append(c2)
            else:
                periods.add((off[c2][0]-o2[0], off[c2][1]-o2[1]))
    periods.discard((0, 0))
    lat = reduce(gcd, (abs(a*d_-b*c_) for (a, b), (c_, d_) in combinations(periods, 2)), 0)
    pos = lambda r: (lambda i, g, p: (app(g, p)[0]+off[(i, g)][0], app(g, p)[1]+off[(i, g)][1]))(*classes[r][0])
    res2 = lambda r: tuple(v % 2 for v in pos(r))
    # translation automorphisms: map cell 0 to any cell whose developed triangle is a translate
    base = cells[0]; bshape = sorted(dev(base)); ntr = 0
    for c in cells:
        sh = sorted(dev(c)); v = (sh[0][0]-bshape[0][0], sh[0][1]-bshape[0][1])
        if sorted((x+v[0], y+v[1]) for x, y in bshape) != sh:
            continue
        f = {base: c}; q = deque([base]); ok = True
        while q and ok:
            a = q.popleft()
            for e in combinations(tiles[a[0]], 2):
                a2 = nbr[a, e]
                ea = sorted(app(a[1], p) for p in e)
                # find the edge of f[a] whose development is ea translated by the same local vector
                fa = f[a]; da = sorted(dev(a)); dfa = sorted(dev(fa)); w = (dfa[0][0]-da[0][0], dfa[0][1]-da[0][1])
                tgt = sorted((x+w[0], y+w[1]) for x, y in ea)
                e2 = next(ee for ee in combinations(tiles[fa[0]], 2) if sorted(app(fa[1], p) for p in ee) == tgt)
                b2 = nbr[fa, e2]
                if a2 in f:
                    ok = f[a2] == b2
                else:
                    f[a2] = b2; q.append(a2)
        if ok and len(set(f.values())) == len(cells):
            ntr += 1
    src, tgt = mark_lifts
    out = dict(input=name, tiles=len(tiles), squares=len(cells)//2, genus=genus,
               cones=dict(sorted(Counter(v for v in m.values() if v > 1).items())),
               regular=len(regular), source_lifts=len(src), target_lifts=len(tgt),
               translation_automorphisms=ntr, rho_fixed=len(fixed),
               rho_fixed_cone_data=dict(sorted(Counter(m[r] for r in fixed).items())),
               rho_fixed_mass=sum(m[r] for r in fixed), W_from_mass=str(2+Fraction(sum(m[r] for r in fixed), 4)),
               all_cones_fixed=all(r in fixed for r in classes if m[r] > 1),
               regular_nonfixed=len(regular-fixed), regular_nonfixed_is_marks=(regular-fixed) == (src | tgt),
               period_lattice_index=lat, periods_all_even=all(a % 2 == 0 and b % 2 == 0 for a, b in periods),
               mark_residues=sorted({res2(r) for r in src | tgt}),
               cone_residues=dict(Counter(f"m{m[r]}@{res2(r)}" for r in classes if m[r] > 1)),
               fixed_regular_residues=dict(Counter(str(res2(r)) for r in fixed & regular)))
    return out


if __name__ == '__main__':
    rows = [audit(n) for n in ('illumination-20.json', 'illumination-22.json', 'illumination-search-simple-unrestricted.json')]
    for r in rows:
        print(json.dumps(r))
    (HERE/'claude-unfold.json').write_text(json.dumps(rows, indent=1)+'\n')
