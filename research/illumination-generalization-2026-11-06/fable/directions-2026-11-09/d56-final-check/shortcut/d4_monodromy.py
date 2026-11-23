"""Exact monodromy of the fold cover DP -> base orbifold, and its block systems.

Two tile frameworks, both with lattice vertices Z^2 and parity classes
A = (even, even), B = (odd, odd), C = mixed:

* 'square': P is a union of unit squares. Base = pillowcase D([0,1]^2),
  folded by the triangle wave in each coordinate. Corners of the base are the
  four parity classes (0,0)=A, (1,1)=B, (1,0)=C1, (0,1)=C2, each of angle pi.
* 'tri': P is a union of half unit squares cut along their A-B diagonal (the
  project's canonical45 tiles). Base = double of the triangle A,B,C with
  angles pi/4, pi/4, pi/2, so the base sphere has cone angles pi/2 (A),
  pi/2 (B), pi (C).

Sheets are the faces (tile, copy) of DP lying over the top face of the base.
The corner generator g_c is the product of the two edge-gluing involutions of
the edges meeting at corner c; a cycle of g_c of length k is a point of DP of
cone angle k * (base angle at c).

Permutations are tuples; mul(p, q) applies p first, then q.
All arithmetic is exact (integers and Fractions).
"""
from fractions import Fraction as Fr
from itertools import combinations
from math import factorial, pi


# ---------------------------------------------------------------- permutations

def mul(p, q):
    return tuple(q[i] for i in p)


def inv(p):
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return tuple(r)


def ident(n):
    return tuple(range(n))


def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen:
            continue
        c, j = [], i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = p[j]
        out.append(c)
    return out


def cycle_type(p):
    return sorted((len(c) for c in cycles(p)), reverse=True)


def schreier_sims(gens, n):
    """Deterministic Schreier-Sims. Returns (base, transversal sizes, order)."""
    e = ident(n)
    gens = [g for g in gens if g != e]
    if not gens:
        return [], [], 1
    base, S = [], []

    def moved(g):
        return next(i for i in range(n) if g[i] != i)

    for g in gens:
        if all(g[b] == b for b in base):
            base.append(moved(g))
    for i in range(len(base)):
        S.append([g for g in gens if all(g[b] == b for b in base[:i])])

    def orbit(i):
        T = {base[i]: e}
        queue = [base[i]]
        for x in queue:
            for s in S[i]:
                y = s[x]
                if y not in T:
                    T[y] = mul(T[x], s)
                    queue.append(y)
        return T

    T = [orbit(i) for i in range(len(base))]

    def strip(h, start):
        for l in range(start, len(base)):
            x = h[base[l]]
            if x not in T[l]:
                return h, l
            h = mul(h, inv(T[l][x]))
        return h, len(base)

    i = len(base) - 1
    while i >= 0:
        restart = False
        for x in list(T[i]):
            for s in S[i]:
                h = mul(mul(T[i][x], s), inv(T[i][s[x]]))
                if h == e:
                    continue
                y, j = strip(h, i + 1)
                if j < len(base) or y != e:
                    if j == len(base):
                        base.append(moved(y))
                        S.append([])
                        T.append({})
                    for l in range(i + 1, j + 1):
                        S[l].append(y)
                        T[l] = orbit(l)
                    i = j
                    restart = True
                    break
            if restart:
                break
        if not restart:
            i -= 1
    sizes = [len(t) for t in T]
    order = 1
    for s in sizes:
        order *= s
    return base, sizes, order


def is_even(p):
    return sum(len(c) - 1 for c in cycles(p)) % 2 == 0


def is_prime(p):
    return p >= 2 and all(p % d for d in range(2, int(p ** 0.5) + 1))


def jordan_witness(gens, n):
    """An element some power of which is a p-cycle, p prime, p <= n-3, among words of length <= 3."""
    words = list(gens)
    words += [mul(a, b) for a in gens for b in gens]
    words += [mul(mul(a, b), c) for a in gens for b in gens for c in gens]
    for w in words:
        lengths = [len(c) for c in cycles(w)]
        for p in set(lengths):
            if is_prime(p) and p <= n - 3 and lengths.count(p) == 1 and all(L % p for L in lengths if L != p):
                return w, p
    return None


def group_order(gens, n, primitive):
    """|G|. Jordan's theorem (primitive + p-cycle, p <= n-3 => G >= A_n) when it applies, else Schreier-Sims."""
    if primitive and n >= 8 and jordan_witness(gens, n):
        even = all(is_even(g) for g in gens)
        return (factorial(n) // 2 if even else factorial(n)), 'jordan'
    return schreier_sims(gens, n)[2], 'schreier_sims'


def orbit_of(x, gens):
    seen = {x}
    queue = [x]
    for y in queue:
        for g in gens:
            z = g[y]
            if z not in seen:
                seen.add(z)
                queue.append(z)
    return seen


def min_block_partition(points, gens, n):
    """Finest G-invariant partition with all `points` in one part (Atkinson)."""
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    queue = []
    p0 = points[0]
    for q in points[1:]:
        a, b = find(p0), find(q)
        if a != b:
            parent[b] = a
            queue.append((p0, q))
    while queue:
        a, b = queue.pop()
        for g in gens:
            ra, rb = find(g[a]), find(g[b])
            if ra != rb:
                parent[rb] = ra
                queue.append((g[a], g[b]))
    parts = {}
    for i in range(n):
        parts.setdefault(find(i), []).append(i)
    return sorted(sorted(p) for p in parts.values())


def all_block_systems(gens, n):
    """Every block system of a transitive group, as sorted lists of blocks."""
    assert len(orbit_of(0, gens)) == n
    found = {}

    def add(partition):
        blk = next(frozenset(b) for b in partition if 0 in b)
        if blk not in found:
            found[blk] = partition
            return True
        return False

    add([[i] for i in range(n)])
    frontier = []
    for x in range(1, n):
        part = min_block_partition([0, x], gens, n)
        if add(part):
            frontier.append(part)
    while frontier:
        part = frontier.pop()
        blk = next(b for b in part if 0 in b)
        for x in range(n):
            if x in blk:
                continue
            new = min_block_partition(list(blk) + [x], gens, n)
            if add(new):
                frontier.append(new)
    systems = sorted(found.values(), key=lambda p: (len(p[0]), p))
    for part in systems:
        assert is_block_system(part, gens)
    return systems


def is_block_system(part, gens):
    where = {}
    for k, b in enumerate(part):
        for x in b:
            where[x] = k
    for g in gens:
        for b in part:
            if len({where[g[x]] for x in b}) != 1:
                return False
    return True


def induced(g, part):
    where = {}
    for k, b in enumerate(part):
        for x in b:
            where[x] = k
    return tuple(where[g[b[0]]] for b in part)


# ---------------------------------------------------------------- geometry

def pclass(p):
    return (p[0] % 2, p[1] % 2)


def tri_class(p):
    a, b = pclass(p)
    return 'A' if (a, b) == (0, 0) else 'B' if (a, b) == (1, 1) else 'C'


SQ_CORNER_NAME = {(0, 0): 'A', (1, 1): 'B', (1, 0): 'C1', (0, 1): 'C2'}


def ekey(a, b):
    return tuple(sorted((tuple(a), tuple(b))))


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def point_in_polygon(pt, poly):
    """Strict interior test, exact; pt must not lie on the boundary."""
    x, y = pt
    inside = False
    m = len(poly)
    for i in range(m):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % m]
        if (y1 > y) != (y2 > y):
            xc = Fr(x1) + Fr(y - y1) * Fr(x2 - x1, y2 - y1)
            if xc > x:
                inside = not inside
    return inside


def squares_from_polygon(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return [(i, j) for i in range(min(xs), max(xs)) for j in range(min(ys), max(ys))
            if point_in_polygon((Fr(2 * i + 1, 2), Fr(2 * j + 1, 2)), poly)]


def tris_of_squares(squares):
    out = []
    for x, y in squares:
        c = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        a = next(p for p in c if tri_class(p) == 'A')
        b = next(p for p in c if tri_class(p) == 'B')
        for o in [p for p in c if p not in (a, b)]:
            out.append((a, b, o))
    return out


def tris_from_polygon(poly):
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        if a[0] != b[0] and a[1] != b[1]:
            assert abs(a[0] - b[0]) == abs(a[1] - b[1]) and (a[0] + a[1]) % 2 == 0, (a, b)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    out = []
    for t in tris_of_squares([(i, j) for i in range(min(xs), max(xs)) for j in range(min(ys), max(ys))]):
        cen = (Fr(sum(p[0] for p in t), 3), Fr(sum(p[1] for p in t), 3))
        if point_in_polygon(cen, poly):
            out.append(t)
    return out


class Room:
    """A lattice room as a set of tiles, with optional slit edges."""

    def __init__(self, name, framework, tiles, marks, slits=(), meta=None):
        self.name, self.fw, self.marks = name, framework, [tuple(m) for m in marks]
        self.meta = meta or {}
        self.tiles = []
        if framework == 'square':
            for (i, j) in sorted(set(map(tuple, tiles))):
                verts = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
                edges = {('V', i % 2): ekey((i, j), (i, j + 1)),
                         ('V', (i + 1) % 2): ekey((i + 1, j), (i + 1, j + 1)),
                         ('H', j % 2): ekey((i, j), (i + 1, j)),
                         ('H', (j + 1) % 2): ekey((i, j + 1), (i + 1, j + 1))}
                orient = 1 if (i + j) % 2 == 0 else -1
                self.tiles.append(dict(key=(i, j), verts=verts, edges=edges, orient=orient))
            self.corners = {c: (('V', c[0]), ('H', c[1])) for c in SQ_CORNER_NAME}
            self.base_angle = {c: Fr(1) for c in SQ_CORNER_NAME}         # in units of pi
            self.vclass = pclass
            self.cname = SQ_CORNER_NAME
            self.tile_angle = Fr(1, 2)
        else:
            for t in sorted(set(tuple(sorted(map(tuple, t))) for t in tiles)):
                a = next(p for p in t if tri_class(p) == 'A')
                b = next(p for p in t if tri_class(p) == 'B')
                c = next(p for p in t if tri_class(p) == 'C')
                assert abs(a[0] - b[0]) == 1 and abs(a[1] - b[1]) == 1
                edges = {'AB': ekey(a, b), 'BC': ekey(b, c), 'AC': ekey(a, c)}
                # base triangle A=(0,0), B=(1,1), C=(1,0) has cross(A,B,C) = -1
                orient = -1 if cross(a, b, c) > 0 else 1
                self.tiles.append(dict(key=(a, b, c), verts=[a, b, c], edges=edges, orient=orient))
            self.corners = {'A': ('AB', 'AC'), 'B': ('AB', 'BC'), 'C': ('BC', 'AC')}
            self.base_angle = {'A': Fr(1, 2), 'B': Fr(1, 2), 'C': Fr(1)}
            self.vclass = tri_class
            self.cname = {'A': 'A', 'B': 'B', 'C': 'C'}
        self.slits = {ekey(*s) for s in slits}
        self._build()

    # -- faces of DP: (tile index, copy) with copy 0 = top, 1 = bottom
    def _build(self):
        n = len(self.tiles)
        owners = {}
        for k, t in enumerate(self.tiles):
            for et, e in t['edges'].items():
                owners.setdefault(e, []).append((k, et))
        self.owners = owners
        faces = [(k, c) for k in range(n) for c in (0, 1)]
        fid = {f: i for i, f in enumerate(faces)}
        self.faces, self.fid = faces, fid
        self.topface = [self.tiles[k]['orient'] * (1 if c == 0 else -1) == 1 for k, c in faces]
        etypes = sorted({et for t in self.tiles for et in t['edges']})
        self.sigma = {}
        for et in etypes:
            s = [None] * len(faces)
            for i, (k, c) in enumerate(faces):
                e = self.tiles[k]['edges'][et]
                own = owners[e]
                if len(own) == 2 and e not in self.slits:
                    (k1, t1), (k2, t2) = own
                    assert t1 == t2 == et
                    other = k2 if k1 == k else k1
                    s[i] = fid[(other, c)]
                else:
                    assert len(own) == 1 or e in self.slits
                    s[i] = fid[(k, 1 - c)]
            assert all(self.topface[i] != self.topface[s[i]] for i in range(len(faces)))
            self.sigma[et] = tuple(s)
        self.sheets = [i for i in range(len(faces)) if self.topface[i]]
        self.sheet_index = {f: j for j, f in enumerate(self.sheets)}
        self.degree = len(self.sheets)
        self.gen = {}
        for c, (e1, e2) in self.corners.items():
            s1, s2 = self.sigma[e1], self.sigma[e2]
            self.gen[c] = tuple(self.sheet_index[s2[s1[f]]] for f in self.sheets)

    # -- geometry ledger
    def ledger(self):
        boundary = [e for e, own in self.owners.items() if len(own) == 1 or e in self.slits]
        inc = {}
        for e in boundary:
            for p in e:
                inc.setdefault(p, []).append(e)
        corners, reflex, convex = [], [], []
        tile_count = {}
        for t in self.tiles:
            for p in t['verts']:
                tile_count[p] = tile_count.get(p, 0) + 1
        for p, es in inc.items():
            assert len(es) == 2 or self.slits, (self.name, p, es)
            if len(es) != 2:
                continue
            d = [(q[0] - p[0], q[1] - p[1]) for e in es for q in e if q != p]
            if d[0][0] * d[1][1] - d[0][1] * d[1][0] != 0:
                corners.append(p)
                ang = tile_count[p] * self.angle_at(p)
                (reflex if ang > 1 else convex).append(p)
        verts = set(tile_count)
        interior = [p for p in verts if p not in inc]
        transparent = sorted(p for p in verts if tri_class(p) != 'A' and p not in corners)
        area = Fr(len(self.tiles)) if self.fw == 'square' else Fr(len(self.tiles), 2)
        return dict(area=area, walls=len(corners), reflex=sorted(reflex), convex=sorted(convex),
                    interior_lattice=sorted(interior), transparent_nonA=transparent)

    def angle_at(self, p):
        """Angle (units of pi) of one tile at lattice vertex p."""
        if self.fw == 'square':
            return Fr(1, 2)
        return Fr(1, 4) if tri_class(p) in 'AB' else Fr(1, 2)

    def corner_of(self, p):
        return pclass(p) if self.fw == 'square' else tri_class(p)

    def points_at(self, p):
        """Points of DP over lattice vertex p: list of (copy-set, cycle of g_c as sheet list)."""
        c = self.corner_of(p)
        g = self.gen[c]
        inc = [self.sheet_index[self.fid[(k, cp)]] for k, t in enumerate(self.tiles) if tuple(p) in t['verts']
               for cp in (0, 1) if self.topface[self.fid[(k, cp)]]]
        pts = []
        cyc = {x: tuple(cy) for cy in cycles(g) for x in cy}
        for x in inc:
            if cyc[x] not in pts:
                pts.append(cyc[x])
        assert sorted(x for cy in pts for x in cy) == sorted(inc), (self.name, p)
        return c, pts

    def gens_list(self):
        return [self.gen[c] for c in sorted(self.gen)]


def genus_from_gens(gen, base_angle):
    """Genus by Gauss-Bonnet: sum over cone points of (2 - angle/pi) = 2 * chi."""
    total = sum(2 - len(cy) * base_angle[c] for c, g in gen.items() for cy in cycles(g))
    assert total % 2 == 0
    return (2 - total // 2) // 2


def block_action_on_block(gens, part):
    """Generators of the setwise stabiliser of part[0], restricted to part[0] (Schreier generators)."""
    ig = [induced(g, part) for g in gens]
    T = {0: (ident(len(gens[0])), )}
    queue = [0]
    for b in queue:
        for g, h in zip(gens, ig):
            c = h[b]
            if c not in T:
                T[c] = (mul(T[b][0], g),)
                queue.append(c)
    blk = part[0]
    loc = {x: i for i, x in enumerate(blk)}
    out = set()
    for b in T:
        for g, h in zip(gens, ig):
            s = mul(mul(T[b][0], g), inv(T[h[b]][0]))
            out.add(tuple(loc[s[x]] for x in blk))
    return list(out)


# ---------------------------------------------------------------- factor analysis

def analyse_room(room, full_group=True):
    gens = room.gens_list()
    n = room.degree
    out = dict(name=room.name, framework=room.fw, degree=n, marks=[list(m) for m in room.marks])
    led = room.ledger()
    out['ledger'] = dict(area=str(led['area']), walls=led['walls'], reflex=len(led['reflex']),
                         convex=len(led['convex']), interior_lattice=[list(p) for p in led['interior_lattice']],
                         transparent_nonA=[list(p) for p in led['transparent_nonA']])
    out['generator_cycle_types'] = {room.cname[c]: cycle_type(g) for c, g in sorted(room.gen.items())}
    out['genus_DP'] = genus_from_gens(room.gen, room.base_angle)
    out['transitive'] = len(orbit_of(0, gens)) == n
    systems = all_block_systems(gens, n)
    out['primitive'] = len(systems) == 2
    out['all_generators_even'] = all(is_even(g) for g in gens)
    if full_group:
        order, method = group_order(gens, n, out['primitive'])
        out['order'] = order
        out['order_method'] = method
        out['is_symmetric'] = order == factorial(n)
        out['is_alternating'] = order * 2 == factorial(n)
    # mark lifts
    marks = {}
    for m in room.marks:
        c, pts = room.points_at(m)
        assert room.cname[c] == 'A', (room.name, m)
        marks[m] = pts
    out['mark_lift_angles'] = {str(list(m)): [str(len(cy) * room.base_angle[room.corner_of(room.marks[0])]) for cy in pts]
                               for m, pts in marks.items()}
    res = []
    for part in systems:
        m = len(part)
        ig = {c: induced(g, part) for c, g in room.gen.items()}
        where = {x: k for k, b in enumerate(part) for x in b}
        cone = {}
        regular_nonA = 0
        for c, g in sorted(ig.items()):
            angles = [len(cy) * room.base_angle[c] for cy in cycles(g)]
            cone[room.cname[c]] = {str(a): angles.count(a) for a in sorted(set(angles))}
            if room.cname[c] != 'A':
                regular_nonA += angles.count(Fr(2))
        phi = {}
        for mk, pts in marks.items():
            gA = ig[room.corner_of(mk)]
            cyc = {x: frozenset(cy) for cy in cycles(gA) for x in cy}
            phi[mk] = {cyc[where[pt[0]]] for pt in pts}
        S, T = room.marks[0], room.marks[1]
        entry = dict(block_size=len(part[0]), blocks=m, squares_or_tiles_of_N=2 * m,
                     cone_angles_over_corner=cone,
                     genus_N=genus_from_gens(ig, room.base_angle),
                     parity_property=regular_nonA == 0,
                     regular_nonA_points_of_N=regular_nonA,
                     phiS_disjoint_phiT=phi[S].isdisjoint(phi[T]),
                     phiS_angles=sorted(str(len(z) * room.base_angle[room.corner_of(room.marks[0])]) for z in phi[S]),
                     phiT_angles=sorted(str(len(z) * room.base_angle[room.corner_of(room.marks[0])]) for z in phi[T]),
                     trivial='discrete' if len(part[0]) == 1 else 'whole' if m == 1 else 'proper')
        if full_group and 1 < m < n:
            _, _, oq = schreier_sims(list(ig.values()), m)
            # action of block stabiliser on its block
            _, _, ob = schreier_sims(block_action_on_block(gens, part), len(part[0]))
            entry['order_on_blocks'] = oq
            entry['kernel_order'] = out['order'] // oq
            entry['block_stabiliser_on_block_order'] = ob
            entry['wreath_bound_order'] = ob ** m * oq
            entry['equals_full_wreath'] = ob ** m * oq == out['order']
        entry['partition'] = part
        res.append(entry)
    out['block_systems'] = res
    return out
