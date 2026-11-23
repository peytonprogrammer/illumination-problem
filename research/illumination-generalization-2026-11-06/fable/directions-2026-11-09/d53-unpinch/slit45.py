"""Rooms with optional slits on the canonical45 tiling: origami, corners, plane tracer.

A room is (tiles, slit_edges): tiles of d11's canonical45 tiling and a set of
unit tile edges that are walls although tiles lie on both sides (a slit).

- build(tiles, slit): 8-fold unfolding X as an origami (port of shoot45's
  construction, with slit edges treated as walls).  Lattice points get a type
  from a sector analysis: the tiles around the point are split into runs by
  the walls through it.  Interior = no wall at the point.  Flat = one run of
  angle pi.  Every other point on a wall is a corner (trajectories die there):
  this includes the slit tip (one run of angle 2 pi) and the slit foot.
- trace(...): independent exact tracer in the room plane, with walls given as
  segments (polygon cycle plus slit) and corners as points.  Uses Fractions.
"""
from fractions import Fraction as Fr
from collections import defaultdict
import rooms45 as R

GM = [(1, 0, 0, 1), (0, -1, 1, 0), (-1, 0, 0, -1), (0, 1, -1, 0), (1, 0, 0, -1), (-1, 0, 0, 1), (0, 1, 1, 0), (0, -1, -1, 0)]


def _gfind(m):
    return GM.index(tuple(m))


def gmul(g, h):
    A, B = GM[g], GM[h]
    return _gfind((A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3], A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3]))


def ginv(g):
    return [h for h in range(8) if gmul(g, h) == 0][0]


def gapply(g, v):
    a, b, c, d = GM[g]
    return (a * v[0] + b * v[1], c * v[0] + d * v[1])


RHO = {0: 4, 1: 5, 2: 6, 3: 7}   # edge type H, V, D+, D-  -> reflection in GM


def etype(p, q):
    if p[1] == q[1]:
        return 0
    if p[0] == q[0]:
        return 1
    return 2 if (q[0] - p[0]) * (q[1] - p[1]) > 0 else 3


def ekey(p, q):
    return (p, q) if p < q else (q, p)


def tile_angle_units(t, p):
    """Angle of tile t at its vertex p, in units of pi/4 (C point: 2, A/B point: 1)."""
    return 2 if (p[0] + p[1]) % 2 else 1


def build(tiles, slit=()):
    tiles = [tuple(t) for t in tiles]
    n = len(tiles)
    V = [R.tile_verts(*t) for t in tiles]
    slit = {ekey(*e) for e in slit}
    own = defaultdict(list)
    for a in range(n):
        for k in range(3):
            own[ekey(V[a][k], V[a][(k + 1) % 3])].append(a)
    assert all(len(o) <= 2 for o in own.values())
    for e in slit:
        assert len(own[e]) == 2, ('slit edge must be interior', e)
    nb = [[None] * 3 for _ in range(n)]
    et = [[None] * 3 for _ in range(n)]
    wall = set()
    for a in range(n):
        for k in range(3):
            e = ekey(V[a][k], V[a][(k + 1) % 3])
            et[a][k] = etype(*e)
            o = own[e]
            if len(o) == 1 or e in slit:
                nb[a][k] = -1
                wall.add(e)
            else:
                nb[a][k] = o[0] if o[1] == a else o[1]
    # lattice points and sector analysis
    pts = sorted({p for v in V for p in v})
    pid = {p: i for i, p in enumerate(pts)}
    inc = defaultdict(list)   # point -> tiles
    for a in range(n):
        for p in V[a]:
            inc[p].append(a)
    ptype = {}
    wall_at = defaultdict(list)
    for e in wall:
        wall_at[e[0]].append(e)
        wall_at[e[1]].append(e)
    for p in pts:
        ts = inc[p]
        walls_at = wall_at[p]
        # union tiles around p across non-wall edges containing p
        par = {a: a for a in ts}

        def f(x):
            while par[x] != x:
                x = par[x]
            return x
        for a in ts:
            for k in range(3):
                e = ekey(V[a][k], V[a][(k + 1) % 3])
                if p in e and nb[a][k] >= 0:
                    par[f(a)] = f(nb[a][k])
        runs = defaultdict(int)
        for a in ts:
            runs[f(a)] += tile_angle_units(a, p)
        if not walls_at:
            assert len(runs) == 1 and list(runs.values())[0] == 8, p
            ptype[p] = 'I'
        elif len(runs) == 1 and list(runs.values())[0] == 4:
            ptype[p] = 'F'
        else:
            ptype[p] = 'C'
    # origami (faces (a, g) = 8a+g)
    glue = [[None] * 3 for _ in range(8 * n)]
    for a in range(n):
        for g in range(8):
            for k in range(3):
                glue[8 * a + g][k] = 8 * nb[a][k] + g if nb[a][k] >= 0 else 8 * a + gmul(g, RHO[et[a][k]])
    sq = [-1] * (8 * n)
    nsq = 0
    for f in range(8 * n):
        a = f // 8
        hk = [k for k in range(3) if et[a][k] >= 2][0]
        p = glue[f][hk]
        b = p // 8
        hk2 = [k for k in range(3) if et[b][k] >= 2][0]
        assert glue[p][hk2] == f
        if sq[f] < 0:
            sq[f] = sq[p] = nsq
            nsq += 1
    assert nsq == 4 * n
    H = [-1] * nsq
    Vv = [-1] * nsq
    lab = [-1] * nsq
    sqg = [-1] * nsq
    for f in range(8 * n):
        a, g = divmod(f, 8)
        d = [gapply(g, p) for p in V[a]]
        bx = min(x for x, _ in d)
        by = min(y for _, y in d)
        s = sq[f]
        for k in range(3):
            if d[k] == (bx, by):
                q = pid[V[a][k]]
                assert lab[s] in (-1, q)
                lab[s] = q
                if sqg[s] < 0:
                    sqg[s] = g
        for k in range(3):
            k2 = (k + 1) % 3
            if d[k][0] == bx + 1 and d[k2][0] == bx + 1:
                assert H[s] < 0
                H[s] = sq[glue[f][k]]
            if d[k][1] == by + 1 and d[k2][1] == by + 1:
                assert Vv[s] < 0
                Vv[s] = sq[glue[f][k]]
    assert min(H) >= 0 and min(Vv) >= 0 and min(lab) >= 0
    assert sorted(H) == list(range(nsq)) and sorted(Vv) == list(range(nsq))
    cnt = defaultdict(int)
    for s in range(nsq):
        cnt[lab[s]] += 1
    for p in pts:
        if ptype[p] == 'I':
            assert cnt[pid[p]] == 8, (p, cnt[pid[p]])
    return dict(tiles=tiles, pts=pts, pid=pid, ptype=ptype, H=H, V=Vv, lab=lab, sqg=sqg, nsq=nsq, wall=wall)


def write_origami(o, fn, eligible, S=None, T=None):
    """File for shootall: nsq, H, V, lab, sqg, then npt and per point: corner flag, eligible index (-1)."""
    pts = o['pts']
    el = {p: i for i, p in enumerate(eligible)}
    with open(fn, 'w') as fh:
        fh.write('%d\n' % o['nsq'])
        for arr in (o['H'], o['V'], o['lab'], o['sqg']):
            fh.write(' '.join(map(str, arr)) + '\n')
        fh.write('%d %d\n' % (len(pts), len(eligible)))
        fh.write(' '.join('%d %d' % (1 if o['ptype'][p] == 'C' else 0, el.get(p, -1)) for p in pts) + '\n')
        fh.write('%d %d\n' % (el[S] if S is not None else -1, el[T] if T is not None else -1))


def orbit_line(o, S, T):
    """orbit45 input line: dec 0 = S lift, 1 = T lift, -1 corner, -2 free."""
    pid = o['pid']
    dec = []
    for s in range(o['nsq']):
        p = o['pts'][o['lab'][s]]
        dec.append(0 if p == S else 1 if p == T else -1 if o['ptype'][p] == 'C' else -2)
    return '%d %s %s %s' % (o['nsq'], ' '.join(map(str, o['H'])), ' '.join(map(str, o['V'])), ' '.join(map(str, dec)))


# ------------------------------------------------------------------ plane tracer (independent)

def _cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def reflect(d, w):
    """Reflect vector d in the line with direction w (w axis-parallel or diagonal)."""
    if w[1] == 0:
        return (d[0], -d[1])
    if w[0] == 0:
        return (-d[0], d[1])
    if w[0] * w[1] > 0:
        return (d[1], d[0])
    return (-d[1], -d[0])


def trace(segs, corners, S, d, m, T, record=False):
    """Follow the billiard path from S in direction d for parameter m (position S + t d).

    segs: wall segments ((x1,y1),(x2,y2)), integer.  corners: set of points where paths die.
    Returns (ok, nrefl, hits) where ok means the path reaches T at t = m, meets no corner
    for 0 < t <= m before that, and T is not met earlier.  hits lists reflection points with
    the wall segment index."""
    P = (Fr(S[0]), Fr(S[1]))
    D = (Fr(d[0]), Fr(d[1]))
    left = Fr(m)
    nrefl = 0
    hits = []
    corners = {(Fr(c[0]), Fr(c[1])) for c in corners}
    Tq = (Fr(T[0]), Fr(T[1]))
    for _ in range(100000):
        # nearest wall hit
        best = None
        for i, (a, b) in enumerate(segs):
            e = (b[0] - a[0], b[1] - a[1])
            den = _cross(D, e)
            if den == 0:
                continue
            w = (a[0] - P[0], a[1] - P[1])
            t = _cross(w, e) / den
            u = _cross(w, D) / den
            if t > 0 and 0 <= u <= 1 and (best is None or t < best[0]):
                best = (t, i)
        assert best is not None, 'ray escapes'
        t, i = best
        # corner or target strictly before the hit, within budget
        for c in corners:
            w = (c[0] - P[0], c[1] - P[1])
            if _cross(w, D) == 0:
                tc = (w[0] / D[0]) if D[0] != 0 else (w[1] / D[1])
                if 0 < tc <= min(t, left):
                    return False, nrefl, hits
        w = (Tq[0] - P[0], Tq[1] - P[1])
        if _cross(w, D) == 0:
            tc = (w[0] / D[0]) if D[0] != 0 else (w[1] / D[1])
            if 0 < tc <= min(t, left):
                return tc == left, nrefl, hits
        if left <= t:
            return False, nrefl, hits
        left -= t
        P = (P[0] + t * D[0], P[1] + t * D[1])
        a, b = segs[i]
        D = reflect(D, (b[0] - a[0], b[1] - a[1]))
        nrefl += 1
        if record:
            hits.append((P, i))
    raise RuntimeError('too many reflections')
