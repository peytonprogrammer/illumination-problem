"""d59 first test: axis-twist orbits of cylinder certificates (named rooms only).

For a lattice room P (unit cells), DP is its double.  Points: regular lattice points of DP
of one parity class (interior lattice points have 2 lifts, wall points 1).  The horizontal
multitwist tau_h (derivative [[1,k],[0,1]], k even) and the vertical one tau_v are affine
automorphisms of DP fixing every corner, so the lit relation on DP points is invariant
under H = <tau_h, tau_v>.  A lift pair is cylinder-certified when both points lie in the
closure of one horizontal or vertical cylinder and are not on the same boundary circle
(d35.7).  A room pair is AT-certified when one of its lift pairs lies in the H-orbit of a
certified lift pair.  AT-certified implies lit.  No ray, direction or word search.
Run: python3 -B axis_twist.py
"""
import sys, json, time, resource
from math import gcd
from pathlib import Path
from itertools import combinations
pass
HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd10-mechanisms'))
from roomtools import cells_from_vertices, is_strictly_simple  # noqa: E402


def lcm(a, b):
    return a * b // gcd(a, b)


def status(cells, p):
    x, y = p
    return sum(1 for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cells)


def cylinders(cells, axis):
    """axis 0: horizontal cylinders. Returns list of (u0, u1, v0, v1) in (along, across)
    coordinates: along-extent [u0,u1], across-extent [v0,v1]."""
    tr = (lambda c: c) if axis == 0 else (lambda c: (c[1], c[0]))
    tc = {tr(c) for c in cells}
    rows = {}
    for (i, j) in tc:
        rows.setdefault(j, set()).add(i)
    runs = {}  # (j, i) -> (u0, u1)
    for j, xs in rows.items():
        for i in sorted(xs):
            if i - 1 in xs:
                runs[(j, i)] = runs[(j, i - 1)]
            else:
                u1 = i
                while u1 in xs:
                    u1 += 1
                runs[(j, i)] = (i, u1)
    cyl = {}  # (j, u0, u1) -> cylinder id ; merge with row below when same extent
    cyls = []
    for j in sorted(rows):
        for ext in sorted({runs[(j, i)] for i in rows[j]}):
            below = cyl.get((j - 1, ext[0], ext[1]))
            if below is not None:
                u0, u1, v0, v1 = cyls[below]
                cyls[below] = (u0, u1, v0, j + 1)
                cyl[(j, ext[0], ext[1])] = below
            else:
                cyls.append((ext[0], ext[1], j, j + 1))
                cyl[(j, ext[0], ext[1])] = len(cyls) - 1
    return cyls, cyl, runs


class Room:
    def __init__(self, cells, cls_origin):
        self.cells = set(cells)
        assert is_strictly_simple(self.cells)
        pts = set()
        for (i, j) in self.cells:
            pts |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
        ox, oy = cls_origin
        self.reg = []  # DP points of class of origin: (x, y, sheet); wall points sheet 0
        for p in sorted(pts):
            if (p[0] - ox) % 2 or (p[1] - oy) % 2:
                continue
            k = status(self.cells, p)
            if k == 4:
                self.reg += [(p[0], p[1], 0), (p[0], p[1], 1)]
            elif k == 2:
                # smooth wall point (two cells sharing an edge) or pinch; strictly simple -> wall
                self.reg.append((p[0], p[1], 0))
        self.regset = set(self.reg)
        self.data = [cylinders(self.cells, a) for a in (0, 1)]
        self.k = []
        for a in (0, 1):
            k = 2
            for (u0, u1, v0, v1) in self.data[a][0]:
                C, h = 2 * (u1 - u0), v1 - v0
                k = lcm(k, C // gcd(C, h))
            self.k.append(k)

    def locate(self, P, a):
        """Cylinder coordinates of DP point P for axis a: (cyl id, s, t, h) or None if P is
        on a boundary circle of two cylinders (returns list of (cid, t) memberships)."""
        x, y, sh = P
        u, v = (x, y) if a == 0 else (y, x)
        cyls, cyl, runs = self.data[a]
        tr = (lambda c: c) if a == 0 else (lambda c: (c[1], c[0]))
        cells_t = {tr(c) for c in self.cells}
        mem = []
        for j in (v - 1, v):  # cell rows below and above the point's level
            # a cell in row j touching the point along u: u-1 or u
            for i in (u - 1, u):
                if (i, j) in cells_t:
                    ext = runs[(j, i)]
                    cid = cyl[(j, ext[0], ext[1])]
                    u0, u1, v0, v1 = cyls[cid]
                    mem.append((cid, v - v0, v1 - v0))
                    break
        return sorted(set(mem))

    def s_coord(self, P, a, cid):
        x, y, sh = P
        u, v = (x, y) if a == 0 else (y, x)
        u0, u1, v0, v1 = self.data[a][0][cid]
        w = u1 - u0
        if u == u0:
            return 0
        if u == u1:
            return w
        return (u - u0) if sh == 0 else w + (u1 - u)

    def from_s(self, a, cid, s, t):
        u0, u1, v0, v1 = self.data[a][0][cid]
        w = u1 - u0
        s %= 2 * w
        if s == 0:
            u, sh = u0, 0
        elif s == w:
            u, sh = u1, 0
        elif s < w:
            u, sh = u0 + s, 0
        else:
            u, sh = u1 - (s - w), 1
        v = v0 + t
        x, y = (u, v) if a == 0 else (v, u)
        return (x, y, sh)

    def twist(self, a):
        k = self.k[a]
        perm = {}
        for P in self.reg:
            mem = self.locate(P, a)
            inner = [m for m in mem if 0 < m[1] < m[2]]
            if not inner:
                perm[P] = P  # on boundary circles: fixed
                continue
            cid, t, h = inner[0]
            s = self.s_coord(P, a, cid)
            Q = self.from_s(a, cid, s + k * t, t)
            perm[P] = Q
        assert sorted(perm.values()) == sorted(self.reg), 'twist is not a bijection on class points'
        return perm

    def certified(self, P, Q):
        """Cylinder certificate in the horizontal or vertical direction."""
        for a in (0, 1):
            mp, mq = self.locate(P, a), self.locate(Q, a)
            for (c1, t1, h1) in mp:
                for (c2, t2, h2) in mq:
                    if c1 != c2:
                        continue
                    bp = t1 in (0, h1)
                    bq = t2 in (0, h2)
                    if bp and bq and t1 == t2:
                        continue  # same boundary circle
                    return True
        return False


def analyse(name, cells, origin, marks=None):
    t0 = time.process_time()
    R = Room(cells, origin)
    gens = [R.twist(0), R.twist(1)]
    pts = R.reg
    room = lambda P: (P[0], P[1])
    pairs = [(P, Q) for P in pts for Q in pts if room(P) != room(Q)]
    cert = {pq for pq in pairs if R.certified(*pq)}
    # forward closure of the certified set under the generators (H finite => orbit union)
    closed = set(cert)
    stack = list(cert)
    while stack:
        P, Q = stack.pop()
        for g in gens:
            im = (g[P], g[Q])
            if im not in closed:
                closed.add(im)
                stack.append(im)
    roompts = sorted({room(P) for P in pts})
    interior = {room(P) for P in pts if (P[0], P[1], 1) in R.regset}
    rp = list(combinations(roompts, 2))
    def lifts(p):
        return [P for P in pts if room(P) == p]
    def status_pair(p, q, S):
        return any((P, Q) in S for P in lifts(p) for Q in lifts(q))
    direct = [pq for pq in rp if status_pair(*pq, cert)]
    atc = [pq for pq in rp if status_pair(*pq, closed)]
    rp_int = [pq for pq in rp if pq[0] in interior and pq[1] in interior]
    unc_int = [pq for pq in rp_int if not status_pair(*pq, closed)]
    moved = sum(1 for g in gens for P in pts if g[P] != P)
    out = dict(room=name, origin=origin, area=len(cells), k=R.k,
               ncyl=[len(R.data[0][0]), len(R.data[1][0])],
               class_points=len(roompts), interior_points=len(interior),
               dp_points=len(pts), points_moved_by_generators=moved,
               room_pairs=len(rp), interior_pairs=len(rp_int),
               direct_cylinder_certified=len(direct), AT_certified=len(atc),
               interior_pairs_not_AT=len(unc_int), sample_not_AT=unc_int[:8])
    if marks:
        p, q = tuple(marks[0]), tuple(marks[1])
        out['marks'] = [p, q]
        out['marks_direct'] = status_pair(p, q, cert)
        out['marks_AT'] = status_pair(p, q, closed)
    out['cpu'] = round(time.process_time() - t0, 3)
    print(json.dumps(out, default=str))
    return out


def load(fn):
    v = list(map(int, open(fn).read().split()))
    n = v[0]
    return {(v[1 + 2 * i], v[2 + 2 * i]) for i in range(n)}


if __name__ == '__main__':
    R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1),
           (5, 1), (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2),
           (0, -2), (0, -1)]
    res = []
    res.append(analyse('R22 (dark control)', cells_from_vertices(R22), (0, 0), [(0, 0), (2, 2)]))
    Q = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
    P6 = Q | {(i, -j - 1) for i, j in Q} | {(5 - i, -j - 1) for i, j in Q} | {(i, 5 - j) for i, j in Q}
    res.append(analyse('P6 d36 (dark control)', P6, (1, 0), [(1, 0), (3, -2)]))
    f = json.load(open(D / 'd31-run-dark-min' / 'found.json'))[0]
    c6 = {tuple(c) for c in f['cells']}
    S6, T6, _ = f['pairs'][0]
    res.append(analyse('P6 found.json[0] (dark control)', c6, tuple(S6), [S6, T6]))
    rooms = D / 'd41-two-param-cover' / 'rooms'
    r20a = load(rooms / 'r20a.txt')
    res.append(analyse('r20a W=20', r20a, (1, 3), [(1, 3), (3, 5)]))
    for org in ((0, 0), (1, 0), (0, 1), (1, 1)):
        res.append(analyse('r20a class %s' % (org,), r20a, org))
        res.append(analyse('cross12 class %s' % (org,), load(rooms / 'cross12.txt'), org))
        res.append(analyse('dumb12 class %s' % (org,), load(rooms / 'dumb12.txt'), org))
        res.append(analyse('R22 class %s' % (org,), cells_from_vertices(R22), org))
    json.dump(res, open(HERE / 'axis_twist.json', 'w'), default=str, indent=1)
