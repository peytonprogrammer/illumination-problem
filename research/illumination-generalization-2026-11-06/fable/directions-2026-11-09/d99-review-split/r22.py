"""d99: R22 and its 3-sheet fold (the 5-cell staircase double, images u=(0,0), v=(2,2) per d94),
plus the visible-seed lemma bookkeeping (i, b, q per class; cardinal-ray first hits) on R22 and cross b=7.
Run: python3 -B r22.py > r22.log"""
import os, sys, json, time
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '..', 'd91-review-stabilizers'))
sys.argv.append('noQ')
import importlib.util
spec = importlib.util.spec_from_file_location('aff', os.path.join(D, 'affine.py'))
from origami import Surface, sigma_squares, cross_cells

T0 = time.process_time()
src = open(os.path.join(D, 'affine.py')).read()
ns = {'__file__': os.path.join(D, 'affine.py')}
exec(src.split('# ------------------------------------------------------------------ the cross')[0], ns)
Ori, affine_group, orbit, suborbit = ns['Ori'], ns['affine_group'], ns['orbit'], ns['suborbit']


def surface(cells):
    S = Surface(cells)
    O = Ori(S.r, S.u, sigma_squares(S))
    phys = {}
    for k in range(S.N):
        phys.setdefault(O.LL[k], S.LL[k][0])
    lift = {}
    for v in range(O.V):
        lift.setdefault(phys[v], set()).add(O.qp(v))
    return S, O, {p: sorted(x) for p, x in lift.items()}


R22 = sorted(tuple(c) for c in json.load(open(os.path.join(D, '..', 'd8-perturbation-test', 'rooms.json')))[0]['cells'])
S, O, lift = surface(R22)
idx, G, naut = affine_group(O)
s, t = lift[(0, 0)][0], lift[(2, 2)]
print(f'R22: Veech index {idx}; |Aut|={naut}; lifts S {lift[(0, 0)]}, T {t}')
for si in lift[(0, 0)]:
    print(f'  s={si}: |F.s|={len(orbit(G, si))}; |F_s.t| for both T lifts {[suborbit(G, si, x) for x in t]}; '
          f'e(S)={suborbit(G, si, [y for y in lift[(0, 0)] if y != si][0])}')

stair = [(-1, 0), (0, 0), (0, 1), (1, 1), (1, 2)]
S2, O2, lift2 = surface(stair)
idx2, G2, naut2 = affine_group(O2)
u, v = lift2[(0, 0)], lift2[(2, 2)]
print(f'staircase N (k=3 fold of R22): Veech index {idx2}; |Aut|={naut2}; lattice points {len(O2.qpts)}; '
      f'poles {len(O2.poles)}, zeros {len(O2.zeros)}; lifts u {u} (wall), v {v} (wall)')
print(f'  |F_N.u|={len(orbit(G2, u[0]))}; |(F_N)_u.v|={suborbit(G2, u[0], v[0])}; '
      f'bound k*I*|F_s.t| with k=3, I<=(3!)^(z+3)=6^6 and z=3')
print(f'  cpu {time.process_time() - T0:.1f}s')


# ---------------------------------------------------------------- lemma bookkeeping
def ptype(cells, p):
    x, y = p
    k = [(c in cells) for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y))]
    n = sum(k)
    return {4: 'int', 3: 'reflex', 1: 'convex', 0: 'out'}.get(n, 'wall')


def first_hit(cells, p, d):
    x, y = p
    while True:
        # cell crossed moving from (x,y) to (x+dx,y+dy)
        dx, dy = d
        if dx:
            c1 = (x if dx > 0 else x - 1, y - 1); c2 = (x if dx > 0 else x - 1, y)
        else:
            c1 = (x - 1, y if dy > 0 else y - 1); c2 = (x, y if dy > 0 else y - 1)
        if not (c1 in cells and c2 in cells):
            return (x, y), ptype(cells, (x, y))
        x, y = x + dx, y + dy
        if ptype(cells, (x, y)) != 'int':
            return (x, y), ptype(cells, (x, y))


def lemma(name, cells):
    cells = set(cells)
    pts = {(x + a, y + b) for (x, y) in cells for a in (0, 1) for b in (0, 1)}
    r = sum(ptype(cells, p) == 'reflex' for p in pts)
    print(f'{name}: r={r}, W-2=2r+2={2*r+2}')
    for cl in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        P = [p for p in pts if (p[0] % 2, p[1] % 2) == cl]
        I = [p for p in P if ptype(cells, p) == 'int']
        B = [p for p in P if ptype(cells, p) == 'wall']
        allreflex = [p for p in I if all(first_hit(cells, p, d)[1] == 'reflex'
                                         for d in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        print(f'  class {cl}: i={len(I)} b={len(B)} q={2*len(I)+len(B)}; interior marks with all four '
              f'cardinal rays ending at reflex corners: {sorted(allreflex)} '
              f'(others have a perpendicular wall return, a lit pair {{x, ix}})')


lemma('R22', R22)
lemma('cross b=7', cross_cells(7))
print(f'cpu {time.process_time() - T0:.1f}s')
