"""Exact billiard tracing in a validated Room.

A candidate path from S to T with reflections at walls w1..wk unfolds to the
segment S -> rho_w1 ... rho_wk (T). For each candidate image T' the tracer
follows the line S + lam (T' - S) inside the room, reflecting both line
points at each wall, and accepts only if it reaches T at lam = 1 without
touching a corner. Every predicate is an exact sign in Z[zeta].
"""
from geom import reflect_point


class Tracer:
    def __init__(self, room):
        self.room = room
        self.tri = room.tri
        self.F = F = room.tri.F
        self.walls = room.walls()
        self.corners = list(room.corners)
        self.iz = F.z(self.tri.n // 2)  # i

    # real numbers as real elements of Z[zeta]
    def two_cross(self, x, y):
        F = self.F
        w = F.mul(F.conj(x), y)
        return F.neg(F.mul(self.iz, F.sub(w, F.conj(w))))  # 2 Im(conj(x) y)

    def two_dot(self, x, y):
        F = self.F
        w = F.mul(F.conj(x), y)
        return F.add(w, F.conj(w))

    def less(self, f1, f2):
        """f = (num, den) real with den != 0; return sign(f1 - f2)."""
        F = self.F
        n1, d1 = f1
        n2, d2 = f2
        diff = F.sub(F.mul(n1, d2), F.mul(n2, d1))
        s = F.sign_re(diff) * F.sign_re(d1) * F.sign_re(d2)
        return s

    def trace(self, S, Tp, T, max_steps=200):
        """Return (ok, wall_sequence, info)."""
        F = self.F
        a, b = S, Tp
        cur = None  # current lambda as fraction; None means 0
        seq = []
        for _ in range(max_steps):
            d = F.sub(b, a)
            best = None
            bestw = None
            for wi, (P, Q, j) in enumerate(self.walls):
                s1 = F.sign_re(self.two_cross(d, F.sub(P, a)))
                s2 = F.sign_re(self.two_cross(d, F.sub(Q, a)))
                if s1 == 0 or s2 == 0 or s1 == s2:
                    continue
                wv = F.sub(Q, P)
                lam = (self.two_cross(F.sub(P, a), wv), self.two_cross(d, wv))
                if cur is not None and self.less(lam, cur) <= 0:
                    continue
                if cur is None and F.sign_re(lam[0]) * F.sign_re(lam[1]) <= 0:
                    continue
                if best is None or self.less(lam, best) < 0:
                    best, bestw = lam, wi
            # end of segment at lam = 1
            one = (F.one, F.one)
            end_first = best is None or self.less(one, best) < 0
            limit = one if end_first else best
            # corners on the open stretch (cur, limit]
            dd = self.two_dot(d, d)
            for c in self.corners:
                if F.sign_re(self.two_cross(d, F.sub(c, a))) != 0:
                    continue
                lc = (self.two_dot(d, F.sub(c, a)), dd)
                lo = self.less(lc, cur) > 0 if cur is not None else F.sign_re(lc[0]) > 0
                if lo and self.less(lc, limit) <= 0:
                    return False, seq, "corner"
            if end_first:
                return (b == T), seq, ("arrive" if b == T else "wrong endpoint")
            P, Q, j = self.walls[bestw]
            a = reflect_point(F, a, P, j)
            b = reflect_point(F, b, P, j)
            cur = best
            seq.append(bestw)
        return False, seq, "too many steps"

    def images(self, T, depth, limit=None):
        """Images of T under words of length <= depth in the wall reflections,
        deduplicated, with their words, sorted by float distance."""
        F = self.F
        seen = {T: ()}
        frontier = [(T, ())]
        for _ in range(depth):
            nf = []
            for p, w in frontier:
                for wi, (P, Q, j) in enumerate(self.walls):
                    if w and w[0] == wi:
                        continue
                    q = reflect_point(F, p, P, j)
                    if q not in seen:
                        seen[q] = (wi,) + w
                        nf.append((q, (wi,) + w))
            frontier = nf
            if limit and len(seen) > limit:
                break
        return seen

    def find_path(self, S, T, depth, limit=None, maxdist=None):
        F = self.F
        imgs = self.images(T, depth, limit)
        S0 = F.cval(S)
        cand = sorted(imgs, key=lambda q: abs(F.cval(q) - S0))
        tried = 0
        for q in cand:
            if q == S:
                continue
            if maxdist is not None and abs(F.cval(q) - S0) > maxdist:
                break
            tried += 1
            ok, seq, info = self.trace(S, q, T)
            if ok:
                return {"found": True, "image": q, "walls_hit": seq, "tried": tried}
        return {"found": False, "tried": tried, "images": len(imgs)}


def find_path_mid(tr, S, T, mids, depth):
    """Midpoint-targeted search. By the proof of Theorem 1, every path from S
    to T unfolds to a segment S -> T' whose midpoint is an image g(X) of a
    transparent E point X, with g a word of about half the path's reflections.
    Try T' = 2 g(X) - S for all images g(X) with |g| <= depth."""
    F = tr.F
    tried = 0
    seen = set()
    for X in mids:
        for Xp in tr.images(X, depth):
            Tp = F.sub(F.smul(2, Xp), S)
            if Tp in seen or Tp == S:
                continue
            seen.add(Tp)
            tried += 1
            ok, seq, info = tr.trace(S, Tp, T)
            if ok:
                return {"found": True, "image": Tp, "walls_hit": seq, "tried": tried, "mid": X}
    return {"found": False, "tried": tried}
