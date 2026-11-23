"""d72: common-cylinder candidate (CC) on existing rooms.

Surface X: the translation surface of a lattice room P, 4 reflected copies of P, tiled by
4n unit squares (origami).  Square (cell, (ex, ey)); r = right neighbour, u = upper neighbour.
Every lattice point of X is the lower-left (LL) corner of >= 1 square.  Marked points: lifts
of polygon vertices (convex corners are regular points of X but forbidden to billiards;
reflex corners are 6 pi cone points).

Direction v = (p, q) primitive: M in SL2(Z) (word in T = [[1,1],[0,1]], V = [[1,0],[1,1]])
with M v = (+-1, 0).  The SL2(Z) action on origamis keeps every square's LL corner:
  T: u' = u o r^-1     T^-1: u' = u o r     V: r' = r o u^-1     V^-1: r' = r o u
Horizontal cylinders of M.X are the v-cylinders of X.  Rows are r-cycles; a row is regular
when no square in it has a marked LL corner (its bottom leaf avoids marked points); a regular
row is glued to the row below it.  A lattice point lift Z (LL corner of square z) lies in the
OPEN interior of a cylinder iff row(z) is regular.
CC(S~, T~, v): row(s), row(t) regular and in one cylinder.
LIT(S~, T~, v): walking r (or r^-1) from s reaches t before a marked LL corner.

Usage: python3 -B cyl.py H [validate]       exact integer arithmetic only.
"""
import json
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations, product
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd69-bbbb'))
sys.path.insert(0, str(D / 'd66-pair-level'))
import decomp  # noqa: E402
import pair_level as PL  # noqa: E402


def incid(cells, pt):
    x, y = pt
    return sum((x + dx, y + dy) in cells for dx, dy in product((-1, 0), repeat=2))


class Origami:
    def __init__(self, cells):
        cells = set(map(tuple, cells))
        self.cells = cells
        sq = [(c, s) for c in sorted(cells) for s in product((1, -1), repeat=2)]
        idx = {k: i for i, k in enumerate(sq)}
        self.sq, self.idx = sq, idx
        N = len(sq)
        r, u = [0] * N, [0] * N
        for i, ((cx, cy), (ex, ey)) in enumerate(sq):
            nb = (cx + ex, cy)
            r[i] = idx[(nb, (ex, ey))] if nb in cells else idx[((cx, cy), (-ex, ey))]
            nb = (cx, cy + ey)
            u[i] = idx[(nb, (ex, ey))] if nb in cells else idx[((cx, cy), (ex, -ey))]
        self.r, self.u = r, u
        self.ll = [(cx + (ex < 0), cy + (ey < 0)) for (cx, cy), (ex, ey) in sq]
        self.marked = [incid(cells, p) in (1, 3) for p in self.ll]
        # sanity: commutator cycles = points; length 3 exactly at reflex corners
        ri, ui = inv(r), inv(u)
        com = [r[u[ri[ui[i]]]] for i in range(N)]
        for cyc in cycles(com):
            pts = {(self.ll[i], ) for i in cyc}
            assert len(pts) == 1, 'commutator cycle mixes P-points'
            k = incid(cells, self.ll[cyc[0]])
            assert len(cyc) == (3 if k == 3 else 1), (cyc, k)

    def lift(self, P, sheet):
        ex, ey = sheet
        return self.idx[((P[0] - (ex < 0), P[1] - (ey < 0)), sheet)]


def inv(a):
    b = [0] * len(a)
    for i, x in enumerate(a):
        b[x] = i
    return b


def cycles(a):
    seen, out = [False] * len(a), []
    for i in range(len(a)):
        if not seen[i]:
            c, j = [], i
            while not seen[j]:
                seen[j] = True
                c.append(j)
                j = a[j]
            out.append(c)
    return out


def word(p, q):
    """Generators (in application order) taking (p, q) to (+-1, 0)."""
    w = []
    while q != 0:
        if p == 0:
            w += [('T', 1), ('V', -1)]
            p, q = q, 0
            break
        if abs(p) >= abs(q):
            k = -(p // q)
            w.append(('T', k))
            p += k * q
        else:
            k = -(q // p)
            w.append(('V', k))
            q += k * p
    assert abs(p) == 1 and q == 0
    return w


def act(r, u, w):
    for g, k in w:
        for _ in range(abs(k)):
            if g == 'T':
                u = [u[x] for x in (inv(r) if k > 0 else r)]
            else:
                r = [r[x] for x in (inv(u) if k > 0 else u)]
    return r, u


class Decomp:
    """Horizontal cylinders of (r, u) with marked LL corners."""
    def __init__(self, O, r, u):
        N = len(r)
        self.r = r
        self.row = [0] * N
        rows = cycles(r)
        self.reg = []
        for k, c in enumerate(rows):
            for i in c:
                self.row[i] = k
            self.reg.append(not any(O.marked[i] for i in c))
        par = list(range(len(rows)))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        ui = inv(u)
        for k, c in enumerate(rows):
            if self.reg[k]:
                a, b = find(k), find(self.row[ui[c[0]]])
                par[a] = b
        self.cyl = [find(k) for k in range(len(rows))]
        self.ri = inv(r)
        self.marked = O.marked

    def cc(self, s, t):
        a, b = self.row[s], self.row[t]
        return self.reg[a] and self.reg[b] and self.cyl[a] == self.cyl[b]

    def interior(self, s):
        return self.reg[self.row[s]]

    def lit(self, s, t):
        for step in (self.r, self.ri):
            j = step[s]
            while j != s and not self.marked[j]:
                if j == t:
                    return True
                j = step[j]
        return False


def directions(H):
    out = [(1, 0), (0, 1)]
    for p in range(1, H + 1):
        for q in range(1, H + 1):
            if gcd(p, q) == 1:
                out += [(p, q), (-p, q)]
    return out


SHEETS = list(product((1, -1), repeat=2))


def pairs_of(cells):
    pts = [p for p in PL.lattice_points(cells) if incid(cells, p) == 4]
    return [(S, T) for S, T in combinations(sorted(pts), 2) if (S[0] - T[0]) % 2 == 0 == (S[1] - T[1]) % 2]


def test_room(cells, H, keep_witness=False):
    """Per pair: first CC direction, first LIT direction (within H), over all 4x4 lift pairs.
    Lift of S fixed to sheet (1,1) is enough: the deck group Z2^2 maps v-cylinders to
    (+-p, +-q)-cylinders and both signs are enumerated."""
    O = Origami(cells)
    prs = pairs_of(O.cells)
    res = {pr: dict(cc=None, lit=None) for pr in prs}
    for v in directions(H):
        if all(x['cc'] for x in res.values()):
            break
        r, u = act(O.r, O.u, word(*v))
        Dc = Decomp(O, r, u)
        for (S, T), x in res.items():
            if x['cc'] and x['lit']:
                continue
            s = O.lift(S, (1, 1))
            for sh in SHEETS:
                t = O.lift(T, sh)
                if x['cc'] is None and Dc.cc(s, t):
                    x['cc'] = (v, sh)
                if x['lit'] is None and Dc.lit(s, t):
                    x['lit'] = (v, sh)
    return O, res


# ---------- independent check: the probe's lattice-step billiard tracer -------------------
def vertex_step(cells, point, velocity):
    """Copied from ../../../../illumination-cylinder-probe.py."""
    x, y = point
    p, q = velocity
    a, b = abs(p), abs(q)
    sx, sy = (1 if p > 0 else -1), (1 if q > 0 else -1)
    i, j = x - (sx < 0), y - (sy < 0)
    h = k = 1
    while h < a or k < b:
        if h * b < k * a:
            if (i + sx, j) in cells:
                i += sx
            else:
                sx = -sx
            h += 1
        else:
            if (i, j + sy) in cells:
                j += sy
            else:
                sy = -sy
            k += 1
    x, y = i + (sx > 0), j + (sy > 0)
    if incid(cells, (x, y)) in (1, 3):
        return None
    if (i + sx, j) not in cells:
        sx = -sx
    if (i, j + sy) not in cells:
        sy = -sy
    return (x, y), (sx * a, sy * b)


def leaf_regular_direct(cells, P, sheet, v):
    """Closed billiard orbit of (P, v on sheet) avoids vertices (probe semantics)."""
    a, b = abs(v[0]), abs(v[1])
    if a == 0 or b == 0:
        return None          # axis directions: probe tracer needs a, b >= 1
    vel = (sheet[0] * v[0], sheet[1] * v[1])
    if (P[0] - (vel[0] < 0), P[1] - (vel[1] < 0)) not in cells:
        return None          # wall point with velocity pointing out of the start cell
    init = (P, vel)
    st, seen = init, set()
    while st and st not in seen:
        seen.add(st)
        st = vertex_step(cells, *st)
    return st == init


def validate(cells, H, nsample=60):
    """Compare Decomp.interior with direct orbit tracing for every lattice-point lift."""
    O = Origami(cells)
    bad = n = 0
    for v in directions(H):
        if v[0] == 0 or v[1] == 0:
            continue
        r, u = act(O.r, O.u, word(*v))
        Dc = Decomp(O, r, u)
        for i in range(0, len(O.sq), max(1, len(O.sq) // nsample)):
            if O.marked[i]:
                continue
            P = O.ll[i]
            sheet = O.sq[i][1]
            d = leaf_regular_direct(O.cells, P, sheet, v)
            if d is None:
                continue
            n += 1
            bad += d != Dc.interior(i)
    return n, bad


def rooms():
    named = decomp.cells_of(None)
    out = [('dumb12', named['dumb12']), ('R22', named['R22'])]
    out += sorted(decomp.handbuilt().items())
    cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
           if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))
    out += [('cov%d' % i, set(map(tuple, r['cells']))) for i, r in enumerate(cov)]
    return out


def classes_transparent(cells):
    """Geometric BBBB test: every parity class has an interior or smooth-wall lattice point."""
    have = set()
    for p in PL.lattice_points(cells):
        if incid(cells, p) in (2, 4):
            have.add((p[0] % 2, p[1] % 2))
    return len(have) == 4


if __name__ == '__main__':
    H = int(sys.argv[1])
    t0 = time.process_time()
    types = {r['name']: r['types'] for r in json.load(open(D / 'd66-pair-level' / 'pair_level.json'))['rooms']}
    if 'validate' in sys.argv:
        named = decomp.cells_of(None)
        for nm in ('dumb12', 'R22'):
            print('validate', nm, 'H', H, 'lifts checked, mismatches:', validate(named[nm], H), flush=True)
        hb = decomp.handbuilt()
        print('validate DB55', validate(hb['DB55'], 8), flush=True)
        print('CPU %.1f s' % (time.process_time() - t0))
        sys.exit()
    probes = {'cov2929', 'cov4181', 'cov4269', 'R22'}
    out = {}
    tally = Counter()
    for name, cells in rooms():
        cells = set(map(tuple, cells))
        dat = PL.room_data(cells)
        geo = classes_transparent(cells)
        hb = not name.startswith('cov') and name not in ('R22',)
        if not (name in probes or hb or (geo and dat['normalized'] and dat['r'] <= 8)):
            continue
        ty = ''.join(str(dat['types'][k]) for k in ((0, 0), (0, 1), (1, 0), (1, 1)))
        O, res = test_room(cells, H)
        c = Counter()
        for (S, T), x in res.items():
            c['pairs'] += 1
            c['cc'] += bool(x['cc'])
            c['lit'] += bool(x['lit'] or x['cc'])
            c['lit_not_cc'] += bool(x['lit']) and not x['cc']
            c['neither'] += not x['lit'] and not x['cc']
        grp = 'probe' if name in probes else ('BBBB' if ty == 'BBBB' else 'geoB-proper')
        for k, v in c.items():
            tally[(grp, k)] += v
        out[name] = dict(n=len(cells), r=dat['r'], types=ty, geo=geo, group=grp, counts=dict(c),
                         pairs=[dict(S=S, T=T, cc=x['cc'], lit=x['lit']) for (S, T), x in res.items()])
        print(name, 'n', len(cells), 'r', dat['r'], 'types', ty, 'geoBBBB', geo, grp, dict(c),
              'CPU %.1f' % (time.process_time() - t0), flush=True)
        for (S, T), x in res.items():
            if not x['cc']:
                print('   no CC within H:', S, T, 'lit', x['lit'])
    print('tally', sorted(tally.items()))
    print('CPU %.1f s' % (time.process_time() - t0))
    json.dump(out, open(HERE / ('cyl_H%d.json' % H), 'w'))
