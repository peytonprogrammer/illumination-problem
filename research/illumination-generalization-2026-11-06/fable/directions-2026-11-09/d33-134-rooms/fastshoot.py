"""Float prefilter for shoot.Tracer. Candidate images are built and traced in
floats; any candidate that the float trace does not clearly reject is rebuilt
exactly from its reflection word and checked with the exact Tracer.trace.
So every reported path is exact; the float step only chooses what to test."""
import cmath, math
from geom import reflect_point

EPS = 1e-7


class Fast:
    def __init__(self, tr):
        self.tr = tr
        F = self.F = tr.F
        self.W = [(F.cval(P), cmath.exp(1j * math.pi * j / tr.tri.n), P, j) for P, Q, j in tr.walls]
        self.Wq = [F.cval(Q) for P, Q, j in tr.walls]
        self.C = [F.cval(c) for c in tr.corners]

    @staticmethod
    def refl(z, p, u):
        return p + u * u * (z - p).conjugate()

    def images(self, X, depth):
        x = self.F.cval(X)
        seen = {(round(x.real, 9), round(x.imag, 9))}
        out = [(x, ())]
        fr = [(x, ())]
        for _ in range(depth):
            nf = []
            for z, w in fr:
                for i, (p, u, _, _) in enumerate(self.W):
                    if w and w[0] == i:
                        continue
                    q = self.refl(z, p, u)
                    key = (round(q.real, 9), round(q.imag, 9))
                    if key not in seen:
                        seen.add(key)
                        nf.append((q, (i,) + w))
            out += nf
            fr = nf
        return out

    def exact(self, X, w):
        F = self.F
        for i in reversed(w):
            _, _, P, j = self.W[i]
            X = reflect_point(F, X, P, j)
        return X

    def ftrace(self, a, b, t, max_steps=200):
        """Return 'miss' only when the float trace is clearly not a path."""
        cur = 0.0
        for _ in range(max_steps):
            d = b - a
            L = abs(d)
            best, bw = None, None
            for i, (p, u, _, _) in enumerate(self.W):
                q = self.Wq[i]
                c1 = (d.conjugate() * (p - a)).imag
                c2 = (d.conjugate() * (q - a)).imag
                if abs(c1) < EPS * L or abs(c2) < EPS * L:
                    # line passes near a wall endpoint: check that corner region below
                    pass
                if c1 * c2 >= 0:
                    continue
                wv = q - p
                den = (d.conjugate() * wv).imag
                lam = ((p - a).conjugate() * wv).imag / den
                if lam <= cur + 1e-12:
                    continue
                if best is None or lam < best:
                    best, bw = lam, i
            limit = 1.0 if best is None or best > 1.0 else best
            for c in self.C:
                lc = ((c - a) * d.conjugate()).real / (L * L)
                if cur - 1e-9 < lc <= limit + 1e-9:
                    if abs(((c - a) * d.conjugate()).imag) / L < EPS:
                        return 'amb'
            if best is None or best > 1.0:
                return 'hit' if abs(b - t) < 1e-6 else 'miss'
            if abs(best - 1.0) < 1e-9:
                return 'amb'
            p, u, _, _ = self.W[bw]
            a, b = self.refl(a, p, u), self.refl(b, p, u)
            cur = best
        return 'amb'

    def _check(self, S, Tex, z, w, base, how):
        s = self.F.cval(S)
        r = self.ftrace(s, z, self.F.cval(Tex))
        if r == 'miss':
            return None
        img = self.exact(base, w)
        if how == 'mid':
            img = self.F.sub(self.F.smul(2, img), S)
        ok, seq, info = self.tr.trace(S, img, Tex)
        return {'found': True, 'image': img, 'walls_hit': seq} if ok else None

    def find_path(self, S, T, depth):
        s = self.F.cval(S)
        imgs = [(z, w) for z, w in self.images(T, depth) if len(w) == depth]
        imgs.sort(key=lambda zw: abs(zw[0] - s))
        for z, w in imgs:
            if abs(z - s) < 1e-9:
                continue
            r = self._check(S, T, z, w, T, 'plain')
            if r:
                return r
        return {'found': False}

    def find_path_mid(self, S, T, mids, depth):
        s = self.F.cval(S)
        cand = []
        for X in mids:
            cand += [(2 * z - s, w, X) for z, w in self.images(X, depth)]
        cand.sort(key=lambda c: abs(c[0] - s))
        for z, w, X in cand:
            if abs(z - s) < 1e-9:
                continue
            r = self._check(S, T, z, w, X, 'mid')
            if r:
                r['mid'] = X
                return r
        return {'found': False}
