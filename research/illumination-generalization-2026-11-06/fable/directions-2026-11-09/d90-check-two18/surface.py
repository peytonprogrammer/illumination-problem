"""Independent square-tiled surface model for a unit-cell room (D90 referee).

Written from the two18 README definitions. Does not import the author's code.

Surface: four copies g=(ex,ey) of the room; physical (x,y) in copy g has surface
chart (ex*x, ey*y). A square is (cell index, ex, ey). Surface right/top neighbours
cross to the physical neighbour cell, or flip the copy at a wall.

Direction (p,q), p,q>0 coprime. In a square with local chart (x,y) in [0,1]^2,
u = q*x - p*y in [-p,q]. Strip piece k is {k<u<k+1}, k=-p..q-1. Interior line m
is {u=m}, m=-p+1..q-1. Only m=0 and m=q-p touch square corners.
"""
from math import gcd, lcm


class Room:
    def __init__(self, cells):
        self.cells = list(cells)
        self.idx = {c: i for i, c in enumerate(self.cells)}
        self.squares = [(c, ex, ey) for c in range(len(self.cells)) for ex in (1, -1) for ey in (1, -1)]
        self._cyl = {}

    def occ(self, x, y):
        return sum((x - i, y - j) in self.idx for i in (0, 1) for j in (0, 1))

    def is_corner(self, X, Y):
        """Polygon vertex: occupancy 1 or 3, or a diagonal pair."""
        k = self.occ(X, Y)
        if k in (1, 3):
            return True
        if k == 2:
            a = (X - 1, Y - 1) in self.idx
            d = (X, Y) in self.idx
            return a == d  # diagonal pattern
        return False

    def R(self, s):
        c, ex, ey = s
        a, b = self.cells[c]
        n = self.idx.get((a + ex, b))
        return (n, ex, ey) if n is not None else (c, -ex, ey)

    def T(self, s):
        c, ex, ey = s
        a, b = self.cells[c]
        n = self.idx.get((a, b + ey))
        return (n, ex, ey) if n is not None else (c, ex, -ey)

    def corner11(self, s):
        """Physical grid point at the surface top-right corner of square s."""
        c, ex, ey = s
        a, b = self.cells[c]
        return (a + (1 if ex > 0 else 0), b + (1 if ey > 0 else 0))

    def row(self, s):
        out = [s]
        t = self.R(s)
        while t != s:
            out.append(t)
            t = self.R(t)
        return out

    def period(self):
        return lcm(*(len(self.row(s)) for s in self.squares))

    def cylinders(self, p, q):
        key = (p, q)
        if key in self._cyl:
            return self._cyl[key]
        assert p > 0 and q > 0 and gcd(p, q) == 1
        # Line criticality, by following each closed leaf.
        crit = {}
        for s in self.squares:
            for m in range(-p + 1, q):
                if (s, m) in crit:
                    continue
                leaf = []
                seen = set()
                marked = False
                cur = (s, m)
                while True:
                    leaf.append(cur)
                    seen.add(cur)
                    sq, mm = cur
                    if q - p < mm:
                        nxt = (self.R(sq), mm - q)
                    elif mm < q - p:
                        nxt = (self.T(sq), mm + p)
                    else:  # passes through the top-right corner of sq
                        X, Y = self.corner11(sq)
                        if self.is_corner(X, Y):
                            marked = True
                        d1, d2 = self.T(self.R(sq)), self.R(self.T(sq))
                        if d1 != d2:
                            assert self.is_corner(X, Y)  # cone point must be marked
                        nxt = (d1, 0)
                    if nxt == (s, m):
                        break
                    assert nxt not in seen
                    cur = nxt
                for z in leaf:
                    crit[z] = marked
        # Union-find over strip pieces.
        parent = {}

        def find(z):
            while parent[z] != z:
                parent[z] = parent[parent[z]]
                z = parent[z]
            return z

        def union(a, b):
            a, b = find(a), find(b)
            if a != b:
                parent[a] = b

        for s in self.squares:
            for k in range(-p, q):
                parent[(s, k)] = (s, k)
        adj = {}
        for s in self.squares:
            for k in range(-p, q):
                if k <= q - p - 1:
                    n, off = (self.T(s), k + p), (0, 1)
                else:
                    n, off = (self.R(s), k - q), (1, 0)
                union((s, k), n)
                adj.setdefault((s, k), []).append((n, off))
                adj.setdefault(n, []).append(((s, k), (-off[0], -off[1])))
            for m in range(-p + 1, q):
                if not crit[(s, m)]:
                    union((s, m - 1), (s, m))
                    adj[(s, m - 1)].append(((s, m), (0, 0)))
                    adj[(s, m)].append(((s, m - 1), (0, 0)))
        lab = {z: find(z) for z in parent}
        names = {r: i for i, r in enumerate(sorted(set(lab.values()), key=repr))}
        lab = {z: names[r] for z, r in lab.items()}
        # Half-turn: square (c,ex,ey) -> (c,-ex,-ey), local (x,y)->(1-x,1-y), k -> q-p-1-k.
        H = {}
        for (s, k), l in lab.items():
            c, ex, ey = s
            img = lab[((c, -ex, -ey), q - p - 1 - k)]
            assert H.setdefault(l, img) == img
        assert all(H[H[l]] == l for l in H)
        res = dict(lab=lab, crit=crit, H=H, adj=adj, p=p, q=q)
        self._cyl[key] = res
        return res
