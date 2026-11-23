"""Combinatorial certificates for Lemmas A, A2, B, C on an order type.

An order type is a cell set on an nx x ny index grid. Grid lines have integer
indices; a position type is a point (X, Y) in doubled coordinates: an even
coordinate 2i lies on grid line i, an odd coordinate 2i+1 lies in the open gap
between lines i and i+1. Every test below compares a point with grid objects
only, never the two points with each other, so a certificate holds for every
metric realization of the order type and every pair of points of those
position types (see theorems.md, section 6).

A certificate is a "recipe" in the original frame:
  lem   : 'A', 'A2', 'B', 'C'
  swap  : 0/1. If 1, point 1 of the recipe is T and point 2 is S.
  p1    : None or (axis, c, e): images of point 1 along `axis`:
          coord[c] + eps*(v - coord[c]) + 2*w*k, w = |coord[e] - coord[c]|
  p2    : same for point 2
  r2    : None or (axis, i): point 2 is first reflected in grid line i of `axis`
  cons  : list of (axis, i, j, c, e): the unfolded segment crosses the line
          {coordinate[axis] = 2*coord[i] - coord[j]} and there its other
          coordinate lies strictly inside (coord[c] - w, coord[c] + w).
"""
from itertools import product

TRANSFORMS = [(tr, fx, fy) for tr in (0, 1) for fx in (0, 1) for fy in (0, 1)]


class OT:
    def __init__(self, nx, ny, cells):
        self.nx, self.ny = nx, ny
        self.cells = frozenset(cells)

    @staticmethod
    def from_mask(nx, ny, mask):
        return OT(nx, ny, [(i, j) for j in range(ny) for i in range(nx) if (mask >> (i + nx * j)) & 1])

    def ins(self, i, j):
        return (i, j) in self.cells

    def rect(self, i0, i1, j0, j1):
        if i0 >= i1 or j0 >= j1 or i0 < 0 or j0 < 0 or i1 > self.nx or j1 > self.ny:
            return False
        return all((i, j) in self.cells for i in range(i0, i1) for j in range(j0, j1))

    def vedge(self, i, j):      # unit edge on vertical line i between rows j, j+1 is boundary
        return self.ins(i - 1, j) != self.ins(i, j)

    def hedge(self, i, j):      # unit edge on horizontal line j between columns i, i+1
        return self.ins(i, j - 1) != self.ins(i, j)

    def vseg(self, i, j0, j1):
        return j0 < j1 and all(self.vedge(i, j) for j in range(j0, j1))

    def hseg(self, j, i0, i1):
        return i0 < i1 and all(self.hedge(i, j) for i in range(i0, i1))

    def npt(self, i, j):
        return self.ins(i - 1, j - 1) + self.ins(i, j - 1) + self.ins(i - 1, j) + self.ins(i, j)

    def vertex(self, i, j):
        return self.npt(i, j) in (1, 3)

    def interior(self, P):
        X, Y = P
        xs = [X // 2] if X % 2 else [X // 2 - 1, X // 2]
        ys = [Y // 2] if Y % 2 else [Y // 2 - 1, Y // 2]
        return all(self.ins(i, j) for i in xs for j in ys)

    def interior_types(self):
        return [(X, Y) for X in range(2 * self.nx + 1) for Y in range(2 * self.ny + 1)
                if self.interior((X, Y))]

    def walls(self):
        return sum(1 for i in range(self.nx + 1) for j in range(self.ny + 1) if self.vertex(i, j))

    # --- symmetries -------------------------------------------------------
    def transform(self, g):
        tr, fx, fy = g
        out = []
        for (i, j) in self.cells:
            a = self.nx - 1 - i if fx else i
            b = self.ny - 1 - j if fy else j
            out.append((b, a) if tr else (a, b))
        return OT(self.ny, self.nx, out) if tr else OT(self.nx, self.ny, out)

    def tpoint(self, g, P):
        tr, fx, fy = g
        X, Y = P
        if fx:
            X = 2 * self.nx - X
        if fy:
            Y = 2 * self.ny - Y
        return (Y, X) if tr else (X, Y)

    def line_back(self, g, axis, idx):
        """Grid line `idx` of `axis` in the transformed frame -> (axis, idx) in the original frame."""
        tr, fx, fy = g
        a = 1 - axis if tr else axis
        if a == 0:
            return 0, (self.nx - idx if fx else idx)
        return 1, (self.ny - idx if fy else idx)


# ---------------------------------------------------------------- Lemma A
def lemma_A(ot, S, T):
    X0, X1 = sorted((S[0], T[0]))
    Y0, Y1 = sorted((S[1], T[1]))
    if S[1] == T[1] and S[1] % 2 == 0:
        if any(ot.vertex(i, S[1] // 2) for i in range(X0 // 2 + 1, (X1 + 1) // 2) if X0 < 2 * i < X1):
            return None
    if S[0] == T[0] and S[0] % 2 == 0:
        if any(ot.vertex(S[0] // 2, j) for j in range(Y0 // 2 + 1, (Y1 + 1) // 2) if Y0 < 2 * j < Y1):
            return None
    i0, i1, j0, j1 = X0 // 2, (X1 + 1) // 2, Y0 // 2, (Y1 + 1) // 2
    xo = [(i0, i1)] if i0 < i1 else [(i0 - 1, i0), (i0, i0 + 1)]
    yo = [(j0, j1)] if j0 < j1 else [(j0 - 1, j0), (j0, j0 + 1)]
    for (a, b), (c, d) in product(xo, yo):
        if ot.rect(a, b, c, d):
            return dict(lem='A', swap=0, p1=None, p2=None, r2=None, cons=[])
    return None


# ---------------------------------------------------------------- Lemma A2
def lemma_A2(ot, S, T):
    """S, T on one grid line; V-shaped path off a wall parallel to that line."""
    for g in TRANSFORMS:
        o = ot.transform(g)
        s, t = ot.tpoint(g, S), ot.tpoint(g, T)
        if s[1] != t[1] or s[1] % 2:
            continue
        if s[0] > t[0]:
            s, t = t, s
        j = s[1] // 2
        i0, i1 = s[0] // 2, (t[0] + 1) // 2
        for jp in range(j - 1, -1, -1):          # wall below, in the transformed frame
            if not o.rect(i0, i1, jp, j):
                break
            if o.hseg(jp, i0, i1):
                ax, idx = ot.line_back(g, 1, jp)
                return dict(lem='A2', swap=0, p1=None, p2=None, r2=(ax, idx), cons=[])
    return None


# ---------------------------------------------------------------- Lemma B
def _lemma_B_canon(o, S, T):
    """Canonical frame: T in a corridor that runs upward from a door at level
    jd; the left wall (line ip) continues below the door; viewer S is below
    the door line and right of line ip. Returns (ip, iq, jd) or None."""
    XS, YS = S
    XT, YT = T
    rT = (YT + 1) // 2 - 1
    c0 = (XT - 1) // 2
    if rT < 0 or not o.ins(c0, rT):
        return None
    ip = c0
    while o.ins(ip - 1, rT):
        ip -= 1
    iq = c0 + 1
    while o.ins(iq, rT):
        iq += 1
    if not (2 * ip < XT < 2 * iq):
        return None
    jd = rT
    while jd >= 0:
        if not (o.rect(ip, iq, jd, jd + 1) and not o.ins(ip - 1, jd) and not o.ins(iq, jd)):
            break
        # door at level jd
        if YS < 2 * jd and XS > 2 * ip:
            imax = max(iq, (XS + 1) // 2)
            jlo = YS // 2
            if o.rect(ip, imax, jlo, jd) and o.vseg(ip, jlo, jd):
                return ip, iq, jd
        jd -= 1
    return None


def lemma_B(ot, S, T):
    for swap, (A, B) in enumerate(((S, T), (T, S))):   # A = viewer (point 1), B = corridor point (point 2)
        for g in TRANSFORMS:
            o = ot.transform(g)
            r = _lemma_B_canon(o, ot.tpoint(g, A), ot.tpoint(g, B))
            if r:
                ip, iq, jd = r
                ax, c = ot.line_back(g, 0, ip)
                _, e = ot.line_back(g, 0, iq)
                ay, d = ot.line_back(g, 1, jd)
                return dict(lem='B', swap=swap, p1=None, p2=(ax, c, e), r2=None,
                            cons=[(ay, d, d, c, e)])
    return None


# ---------------------------------------------------------------- Lemma C
def arm_objects(ot, P):
    """All (hub, door) objects whose arm contains P, in the original frame.
    Each object: dict(G=(g0,g1,h0,h1), side, along, perp_idx, F, E).
    `side` in 'LRBT'; `along` = axis along the door; perp_idx = index of the
    door line on the other axis; F, E = indices (on `along`) of the flat end
    and of the other end of the door."""
    out = []
    for g in TRANSFORMS:
        o = ot.transform(g)
        XS, YS = ot.tpoint(g, P)
        # canonical: door on the left side of the hub, flat end at its bottom-left corner,
        # arm runs to the left of the door.
        c0 = XS // 2
        r0 = (YS - 1) // 2
        if not o.ins(c0, r0):
            continue
        jb = r0
        while o.ins(c0, jb - 1):
            jb -= 1
        jt = r0 + 1
        while o.ins(c0, jt):
            jt += 1
        if not (2 * jb < YS < 2 * jt):
            continue
        gd = c0 + 1
        while gd <= o.nx:
            col = gd - 1
            if not (o.rect(col, col + 1, jb, jt) and o.hedge(col, jb) and o.hedge(col, jt)):
                break
            # door on line gd, rows jb..jt, flat end (gd, jb): hub floor continues
            for g1 in range(gd + 1, o.nx + 1):
                if not o.hseg(jb, gd, g1):
                    break
                for h1 in range(jt, o.ny + 1):
                    if not o.rect(gd, g1, jb, h1):
                        break
                    # map back
                    pts = []
                    for (a, b) in ((gd, jb), (g1, h1)):
                        _, ia = ot.line_back(g, 0, a)
                        _, ib = ot.line_back(g, 1, b)
                        pts.append((ia, ib) if not g[0] else (ib, ia))
                    (xa, ya), (xb, yb) = pts
                    G = (min(xa, xb), max(xa, xb), min(ya, yb), max(ya, yb))
                    al, F = ot.line_back(g, 1, jb)       # door runs along transformed y
                    _, E = ot.line_back(g, 1, jt)
                    pa, pidx = ot.line_back(g, 0, gd)
                    if pa == 0:
                        side = 'L' if pidx == G[0] else 'R'
                    else:
                        side = 'B' if pidx == G[2] else 'T'
                    out.append(dict(G=G, side=side, along=al, perp=pidx, F=F, E=E))
            gd += 1
    # dedupe
    seen, res = set(), []
    for d in out:
        k = (d['G'], d['side'], d['F'], d['E'])
        if k not in seen:
            seen.add(k)
            res.append(d)
    return res


OPP = {'L': 'R', 'R': 'L', 'B': 'T', 'T': 'B'}


def lemma_C(ot, S, T, cache=None):
    oS = cache[S] if cache is not None else arm_objects(ot, S)
    oT = cache[T] if cache is not None else arm_objects(ot, T)
    if not oS or not oT:
        return None
    byG = {}
    for d in oT:
        byG.setdefault(d['G'], []).append(d)
    for d1 in oS:
        for d2 in byG.get(d1['G'], ()):
            if (d1['side'], d1['F'], d1['E']) == (d2['side'], d2['F'], d2['E']):
                continue
            g0, g1, h0, h1 = d1['G']
            perp = 1 - d1['along']
            c1 = (perp, d1['perp'], d1['perp'], d1['F'], d1['E'])
            if d2['side'] == d1['side']:
                # same side: the opposite side of the hub must be a wall
                if d1['side'] in 'LR':
                    opp = g1 if d1['side'] == 'L' else g0
                    if not ot.vseg(opp, h0, h1):
                        continue
                else:
                    opp = h1 if d1['side'] == 'B' else h0
                    if not ot.hseg(opp, g0, g1):
                        continue
                if d1['F'] == d2['F']:
                    continue
                c2 = (perp, opp, d2['perp'], d2['F'], d2['E'])
                return dict(lem='C', form='same', swap=0, p1=(d1['along'], d1['F'], d1['E']),
                            p2=(d2['along'], d2['F'], d2['E']), r2=(perp, opp), cons=[c1, c2])
            perp2 = 1 - d2['along']
            c2 = (perp2, d2['perp'], d2['perp'], d2['F'], d2['E'])
            form = 'par' if d2['side'] == OPP[d1['side']] else 'perp'
            return dict(lem='C', form=form, swap=0, p1=(d1['along'], d1['F'], d1['E']),
                        p2=(d2['along'], d2['F'], d2['E']), r2=None, cons=[c1, c2])
    return None


def lemma_B2(ot, S, T, cache=None):
    """Viewer in the closed hub G sees the door of the other point's arm by one
    reflection in the side of G opposite to the door."""
    for swap, (A, B) in enumerate(((S, T), (T, S))):   # A = viewer, B = arm point
        objs = cache[B] if cache is not None else arm_objects(ot, B)
        for d in objs:
            g0, g1, h0, h1 = d['G']
            if not (2 * g0 <= A[0] <= 2 * g1 and 2 * h0 <= A[1] <= 2 * h1):
                continue
            perp = 1 - d['along']
            if d['side'] in 'LR':
                opp = g1 if d['side'] == 'L' else g0
                if not ot.vseg(opp, h0, h1):
                    continue
            else:
                opp = h1 if d['side'] == 'B' else h0
                if not ot.hseg(opp, g0, g1):
                    continue
            return dict(lem='B2', swap=swap, p1=None, p2=(d['along'], d['F'], d['E']),
                        r2=(perp, opp), cons=[(perp, opp, d['perp'], d['F'], d['E'])])
    return None


# ---------------------------------------------------------------- Lemma D
def _lemma_D_canon(o, S, T):
    """Canonical frame: V = grid point (iq, jd). Corridor 1 runs upward from
    the door [x_ip, x_iq] x {y_jd} and contains S. Corridor 2 runs to the right
    from the door {x_iq} x [y_jb, y_jd] and contains T. The block
    [x_ip, x_iq] x [y_jb, y_jd] lies in the room."""
    XS, YS = S
    XT, YT = T
    rS = (YS + 1) // 2 - 1
    c0 = (XS - 1) // 2
    if rS < 0 or c0 < 0 or not o.ins(c0, rS):
        return False
    ip = c0
    while o.ins(ip - 1, rS):
        ip -= 1
    iq = c0 + 1
    while o.ins(iq, rS):
        iq += 1
    if not (2 * ip < XS < 2 * iq):
        return False
    cT = (XT + 1) // 2 - 1
    if cT < iq:
        return False
    jd = rS
    while jd >= 1:
        if not (o.rect(ip, iq, jd, jd + 1) and not o.ins(ip - 1, jd) and not o.ins(iq, jd)):
            break
        # door 1 at level jd; corridor 2 lies below line jd, right of line iq
        jb = jd
        while o.ins(iq, jb - 1):
            jb -= 1
        if jb < jd and 2 * jb < YT < 2 * jd and o.rect(ip, iq, jb, jd) and all(
                o.rect(i, i + 1, jb, jd) and o.hedge(i, jb) and o.hedge(i, jd) for i in range(iq, cT + 1)):
            return True
        jd -= 1
    return False


def lemma_D(ot, S, T):
    for (A, B) in ((S, T), (T, S)):
        for g in TRANSFORMS:
            if _lemma_D_canon(ot.transform(g), ot.tpoint(g, A), ot.tpoint(g, B)):
                return dict(lem='D', swap=0, p1=None, p2=None, r2=None, cons=[])
    return None


def certify_pair(ot, S, T, cache=None):
    return (lemma_A(ot, S, T) or lemma_A2(ot, S, T) or lemma_B(ot, S, T)
            or lemma_B2(ot, S, T, cache) or lemma_C(ot, S, T, cache) or lemma_D(ot, S, T))


def certify_type(ot):
    """Returns (certs, uncovered): certs maps (S, T) with S < T to a recipe."""
    pts = ot.interior_types()
    cache = {P: arm_objects(ot, P) for P in pts}
    certs, unc = {}, []
    for a in range(len(pts)):
        for b in range(a, len(pts)):
            S, T = pts[a], pts[b]
            if S == T:
                if S[0] % 2 == 0 and S[1] % 2 == 0:
                    continue                      # a single point
                certs[(S, T)] = dict(lem='A', swap=0, p1=None, p2=None, r2=None, cons=[])
                continue
            c = certify_pair(ot, S, T, cache)
            if c:
                certs[(S, T)] = c
            else:
                unc.append((S, T))
    return certs, unc
