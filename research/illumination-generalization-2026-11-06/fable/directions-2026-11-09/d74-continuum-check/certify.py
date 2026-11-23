"""d74 continuum certifier.  Usage: python3 -B certify.py ROOMFILE INDEX B [maxpieces]

State: a partition of int P into relatively open convex pieces f (dim 0, 1, 2), each with a list
Q(f) of closed 2-dim convex polygons (each inside one closed cell) such that
    (I1)  U(S) := int P minus Ill(S)  is contained in  union Q(f)   for every S in f,
where Ill(S) is the union over processed directions theta and labels D in Lambda_theta(S) of K_D.
A piece with Q(f) empty is dead: S lights every T != S (Lemma A').
Pairs: (S, T) can be dark only if S in f, T in g, both live, T in U(S), S in U(T); we test
closure(g) ∩ union Q(f) and closure(f) ∩ union Q(g) (over-approximation).  A piece with no mutual
partner is dropped (all its pairs are lit).
"""
import sys
import time
from fractions import Fraction as F

from geom import (Direction, read_rooms, square, clip, area2, dirs, bbox, convex_intersect,
                  pt_kind, interior_point)


class Piece:
    __slots__ = ('dim', 'verts', 'home', 'Q', 'bb')

    def __init__(self, dim, verts, home, Q):
        self.dim, self.verts, self.home, self.Q = dim, verts, home, Q
        self.bb = bbox(verts)

    def rep(self):
        n = len(self.verts)
        if n == 1:
            return self.verts[0]
        if n == 2:
            (a, b), (c, d) = self.verts
            return ((a + c) / 2, (b + d) / 2)
        # centroid of three vertices of a convex polygon with nonzero area: interior point
        v = self.verts
        for i in range(1, n - 1):
            if area2([v[0], v[i], v[i + 1]]) != 0:
                return ((v[0][0] + v[i][0] + v[i + 1][0]) / 3, (v[0][1] + v[i][1] + v[i + 1][1]) / 3)
        raise AssertionError


def initial_pieces(cs):
    Q0 = tuple((c, tuple(square(c))) for c in sorted(cs))
    out = []
    for c in sorted(cs):
        out.append(Piece(2, square(c), c, Q0))
        a, b = c
        if (a + 1, b) in cs:      # open vertical edge x = a+1
            out.append(Piece(1, [(F(a + 1), F(b)), (F(a + 1), F(b + 1))], c, Q0))
        if (a, b + 1) in cs:
            out.append(Piece(1, [(F(a), F(b + 1)), (F(a + 1), F(b + 1))], c, Q0))
    pts = {(i + dx, j + dy) for (i, j) in cs for dx in (0, 1) for dy in (0, 1)}
    for (x, y) in sorted(pts):
        if pt_kind(cs, x, y) == 'int':
            out.append(Piece(0, [(F(x), F(y))], (x - 1, y - 1), Q0))
    return out


def split(piece, line):
    """Split a relatively open piece by a line a x + b y = c crossing its relative interior."""
    a, b, c = line
    vals = [a * x + b * y - c for (x, y) in piece.verts]
    if not (min(vals) < 0 < max(vals)):
        return None
    if piece.dim == 2:
        L = clip(piece.verts, a, b, c, 1)
        R = clip(piece.verts, a, b, c, -1)
        chord = [v for v, s in zip(piece.verts, vals) if s == 0]
        n = len(piece.verts)
        for i in range(n):
            vp, vq = vals[i], vals[(i + 1) % n]
            if (vp < 0 < vq) or (vq < 0 < vp):
                P, Qp = piece.verts[i], piece.verts[(i + 1) % n]
                t = vp / (vp - vq)
                chord.append((P[0] + t * (Qp[0] - P[0]), P[1] + t * (Qp[1] - P[1])))
        chord = sorted(set(chord))
        assert len(chord) == 2
        return [Piece(2, L, piece.home, piece.Q), Piece(2, R, piece.home, piece.Q),
                Piece(1, chord, piece.home, piece.Q)]
    # dim 1
    (P, Qp) = piece.verts
    vp, vq = vals
    t = vp / (vp - vq)
    M = (P[0] + t * (Qp[0] - P[0]), P[1] + t * (Qp[1] - P[1]))
    return [Piece(1, [P, M], piece.home, piece.Q), Piece(1, [M, Qp], piece.home, piece.Q),
            Piece(0, [M], piece.home, piece.Q)]


def update_Q(Q, D, lam):
    """New Q after direction D with labels lam (I1 preserved; only 2-dim pieces kept)."""
    if not lam:
        return Q
    out = []
    p, q = D.p, D.q
    for (c, W) in Q:
        runs_t, runs_s = D.kept_runs(c, lam)
        lo_t, hi_t = D.rng(c, 0)
        lo_s, hi_s = D.rng(c, 1)
        if runs_t == [(lo_t, hi_t)] and runs_s == [(lo_s, hi_s)]:
            out.append((c, W))
            continue
        for (i1, i2) in runs_t:
            W1 = clip(list(W), q, -p, i1, -1)        # q x - p y >= i1
            W1 = clip(W1, q, -p, i2, 1)              # q x - p y <= i2
            if len(W1) < 3:
                continue
            for (j1, j2) in runs_s:
                W2 = clip(W1, q, p, j1, -1)
                W2 = clip(W2, q, p, j2, 1)
                if len(W2) >= 3 and area2(W2) != 0:
                    out.append((c, tuple(W2)))
    return tuple(out)


def qarea(Q):
    return sum(abs(area2(W)) for (_, W) in Q) / 2


def apply_direction(cs, pieces, D, stats):
    out = []
    for f in pieces:
        lines = D.singular_lines(f.home) if f.dim > 0 else []
        parts = [f]
        for ln in lines:
            nxt = []
            for g in parts:
                s = split(g, ln)
                if s is None:
                    nxt.append(g)
                else:
                    nxt.extend(s)
            parts = nxt
        newQ = []
        changed = False
        for g in parts:
            x, y = g.rep()
            lam = D.labels_at(x, y)
            Q2 = update_Q(g.Q, D, lam)
            if Q2 is not g.Q and qarea(Q2) < qarea(g.Q):
                changed = True
            newQ.append(Q2)
        if not changed:
            out.append(f)          # forgo this direction for f (sound: Ill only shrinks)
            continue
        stats['split'] += len(parts) - 1
        for g, Q2 in zip(parts, newQ):
            if Q2:
                g.Q = Q2
                out.append(g)
    return out


def cells_touched(verts):
    """Cells whose closure may contain a point of the closed convex set with these vertices."""
    x0, x1, y0, y1 = bbox(verts)
    return {(i, j) for i in range(x0.__ceil__() - 1, x1.__floor__() + 1)
            for j in range(y0.__ceil__() - 1, y1.__floor__() + 1)}


def hits(Q, g, gcells):
    for (c, W) in Q:
        if c in gcells and convex_intersect(g.verts, list(W)):
            return True
    return False


def prune(pieces, rounds=3):
    """Drop pieces with no mutual partner; repeat (dropping can only remove partners)."""
    for _ in range(rounds):
        cells = [cells_touched(f.verts) for f in pieces]
        idx = {}
        for k, cc in enumerate(cells):
            for c in cc:
                idx.setdefault(c, []).append(k)
        hitcache = {}

        def H(a, b):     # closure(piece b) meets union Q(piece a)
            key = (a, b)
            if key not in hitcache:
                hitcache[key] = hits(pieces[a].Q, pieces[b], cells[b])
            return hitcache[key]
        keep = []
        for a, f in enumerate(pieces):
            qcells = {c for (c, _) in f.Q}
            cand = set()
            for c in qcells:
                cand.update(idx.get(c, ()))
            ok = False
            for b in cand:
                if b == a and f.dim == 0:
                    continue
                if H(a, b) and H(b, a):
                    ok = True
                    break
            if ok:
                keep.append(f)
        if len(keep) == len(pieces):
            return keep
        pieces = keep
    return pieces


def partners(pieces, f):
    out = []
    fc = cells_touched(f.verts)
    for g in pieces:
        if g is f and f.dim == 0:
            continue
        if hits(f.Q, g, cells_touched(g.verts)) and hits(g.Q, f, fc):
            out.append(g)
    return out


def run(cs, B, maxpieces=20000, log=print, prune_every=10**9):
    t0 = time.process_time()
    pieces = initial_pieces(cs)
    stats = {'split': 0}
    used = []
    for k, (p, q) in enumerate(dirs(B)):
        D = Direction(cs, p, q)
        pieces = apply_direction(cs, pieces, D, stats)
        used.append((p, q))
        if k % prune_every == prune_every - 1:
            pieces = prune(pieces)
        dims = [sum(f.dim == d for f in pieces) for d in (0, 1, 2)]
        log('dir (%d,%d) cyl %d live %d dims %s area %s cpu %.1f' % (
            p, q, D.ncyl, len(pieces), dims, sum(len(f.Q) for f in pieces),
            time.process_time() - t0))
        if not pieces or len(pieces) > maxpieces:
            break
    pieces = prune(pieces)
    return pieces, used


def describe(pieces):
    out = []
    for f in pieces:
        out.append((f, partners(pieces, f)))
    return out


if __name__ == '__main__':
    path, idx, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    mp = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
    cs = read_rooms(path)[idx]
    print('room', sorted(cs))
    pieces, used = run(cs, B, mp)
    print('FINAL live pieces', len(pieces))
    for f, ps in describe(pieces)[:60]:
        print(' dim', f.dim, [(str(x), str(y)) for x, y in f.verts], 'partners',
              [[(str(x), str(y)) for x, y in g.verts] for g in ps][:6])
