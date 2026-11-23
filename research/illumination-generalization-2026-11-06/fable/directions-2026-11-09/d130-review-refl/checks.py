"""D130 checks for reflection-complexity.2026-11-21-2110.md.

Exact Fraction slab tracer on the two named band rooms only:
  cov279 stretch q = 12j+4: bands y (0,2):(0,2q) (2,3):(2q-3,4q) (3,4):(2q,5q) (4,6):(4q,6q)
     S = (q/2, 1), T = (3q, 3), door p = (2q, 2).
  st279 end-square stretch m = 144k^2: bands y (0,m):(0,m) (m,m+1):(m-1,m+2)
     (m+1,m+2):(m,m+3) (m+2,2m+2):(m+2,2m+2); S, T from the note's rounding rule.

Checks
 A. Room facts (reflex count, wall gcds, largest inscribed square tau).
 B. Thin witnesses: two-band translate shots S -> T built by CRT, replayed
    exactly; reflection count vs sqrt(q)/12; formal t=0 determinant odd;
    band passages counted.
 C. Thin completeness: every developed image of T under <= L wall
    reflections (complete for paths with <= L reflections) is traced.
 D. Fat witnesses: note's construction replayed; parities, depth,
    reflections, band passages; limit determinant = 2 mod 4.
 E. Fat explicit constant: smallest R allowed by 1/8 <= 12(R+1)d + 2d^2
    with the actual endpoint errors; then completeness check C for small L.
No search over rooms. Word searches are only over images in the named rooms.
"""
from fractions import Fraction as F
from math import gcd, isqrt, sqrt
import time

CPU0 = time.process_time()


class Fail(Exception):
    pass


class Room:
    def __init__(self, bands):
        # bands: list of (ylo, yhi, xlo, xhi), bottom to top, one run per band
        self.b = [tuple(F(v) for v in bd) for bd in bands]

    def band_of(self, y):
        for i, (ylo, yhi, _, _) in enumerate(self.b):
            if ylo < y < yhi:
                return i
        raise ValueError

    def trace(self, P, d, T, maxrefl):
        """Trace from interior P along d; return (word, events) if T reached
        with <= maxrefl reflections, else raise Fail."""
        x, y = F(P[0]), F(P[1])
        dx, dy = F(d[0]), F(d[1])
        if dy == 0:
            raise Fail('horizontal')
        band = self.band_of(y) if (y not in [bd[0] for bd in self.b]) else None
        if band is None:
            raise Fail('start on level')
        word, events = [], []
        nb = len(self.b)
        while True:
            ylo, yhi, lo, hi = self.b[band]
            ty = ((yhi - y) / dy) if dy > 0 else ((ylo - y) / dy)
            tx = None
            if dx > 0:
                tx = (hi - x) / dx
            elif dx < 0:
                tx = (lo - x) / dx
            tn = ty if tx is None else min(tx, ty)
            # target on this segment (closed at far end)?
            if dx != 0:
                lt = (T[0] - x) / dx
                hitT = 0 < lt <= tn and y + lt * dy == T[1]
            else:
                lt = (T[1] - y) / dy
                hitT = x == T[0] and 0 < lt <= tn
            if hitT:
                return word, events
            if len(word) > maxrefl:
                raise Fail('too many')
            if tx is not None and tx == ty:
                raise Fail('corner')
            if tx is not None and tx < ty:
                x = hi if dx > 0 else lo
                y = y + dy * tx
                word.append(('x', x))
                dx = -dx
                continue
            x = x + dx * ty
            y = yhi if dy > 0 else ylo
            nxt = band + (1 if dy > 0 else -1)
            if nxt < 0 or nxt >= nb:
                word.append(('y', y))
                dy = -dy
                continue
            olo, ohi = self.b[nxt][2], self.b[nxt][3]
            if x in (lo, hi, olo, ohi):
                raise Fail('vertex')
            if max(lo, olo) < x < min(hi, ohi):
                events.append((len(word), y, x, band, nxt))
                band = nxt
            else:
                word.append(('y', y))
                dy = -dy

    def lines(self):
        xs, ys = set(), set()
        for ylo, yhi, lo, hi in self.b:
            xs |= {lo, hi}
            ys |= {ylo, yhi}
        return sorted(xs), sorted(ys)

    def facts(self):
        """reflex count, gcd of horizontal / vertical wall lengths, tau."""
        hor = []
        b = self.b
        hor.append(b[0][3] - b[0][2])
        hor.append(b[-1][3] - b[-1][2])
        reflex = 0
        for i in range(len(b) - 1):
            l1, h1, l2, h2 = b[i][2], b[i][3], b[i + 1][2], b[i + 1][3]
            assert max(l1, l2) < min(h1, h2)
            hor += [abs(l1 - l2), abs(h1 - h2)]
            reflex += (l1 != l2) + (h1 != h2)
        ver = [bd[1] - bd[0] for bd in b] * 2
        g = lambda L: __import__('functools').reduce(gcd, [int(v) for v in L if v])
        # tau: largest square = max over x-intervals of min(width, contiguous height)
        xs, _ = self.lines()
        tau = 0
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                a, c = xs[i], xs[j]
                best = run = F(0)
                for ylo, yhi, lo, hi in b:
                    if lo <= a and c <= hi:
                        run += yhi - ylo
                    else:
                        run = F(0)
                    best = max(best, run)
                tau = max(tau, min(c - a, best))
        return reflex, g(hor), g(ver), tau


def develop(word, pt, subst=lambda a, v: v):
    """Image rho_1 ... rho_k (pt) for word w_1..w_k (w_1 hit first)."""
    x, y = F(pt[0]), F(pt[1])
    for ax, v in reversed(word):
        v = subst(ax, v)
        if ax == 'x':
            x = 2 * v - x
        else:
            y = 2 * v - y
    return x, y


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def images(room, T, L):
    xs, ys = room.lines()
    lev = {(F(T[0]), F(T[1]))}
    allimg = {0: set(lev)}
    seen = set(lev)
    for k in range(1, L + 1):
        new = set()
        for (x, y) in lev:
            for v in xs:
                new.add((2 * v - x, y))
            for v in ys:
                new.add((x, 2 * v - y))
        new -= seen
        seen |= new
        allimg[k] = new
        lev = new
    return allimg


def complete_check(room, S, T, L):
    """Return min reflections among paths with <= L reflections, or None."""
    imgs = images(room, T, L)
    best = None
    ntr = 0
    for k in range(L + 1):
        for P in imgs[k]:
            d = (P[0] - S[0], P[1] - S[1])
            if d[1] == 0:
                continue
            ntr += 1
            try:
                w, _ = room.trace(S, d, T, L)
                if len(w) <= L and (best is None or len(w) < best):
                    best = len(w)
            except Fail:
                pass
    return best, ntr


def out(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- thin
def cov(q):
    return Room([(0, 2, 0, 2 * q), (2, 3, 2 * q - 3, 4 * q), (3, 4, 2 * q, 5 * q), (4, 6, 4 * q, 6 * q)])


def crt(a1, n1, a2, n2):
    g = gcd(n1, n2)
    if (a2 - a1) % g:
        return None
    l = n1 // g * n2
    k = ((a2 - a1) // g * pow(n1 // g, -1, n2 // g)) % (n2 // g)
    return (a1 + k * n1) % l, l


def thin_witnesses(q):
    """Direction (h, 1) from S=(q/2,1): band0 developed x = q/2 + h folds to c
    in the door; band1 unfolded coordinate then reaches T=(3q,3)."""
    l, w = 2 * q - 3, 2 * q + 3
    res = []
    for c in range(2 * q - 2, 2 * q):
        for sig in (1, -1):
            a1 = (c - q // 2) % (4 * q) if sig == 1 else (-c - q // 2) % (4 * q)
            u0 = sig * (c - l)
            for r2 in (3 * q - l, 2 * w - (3 * q - l)):
                sol = crt(a1, 4 * q, (r2 - u0) % (2 * w), 2 * w)
                if sol:
                    h = sol[0] if sol[0] else sol[1]
                    res.append((c, sig, h))
    return res


out('== A/B. Thin cov279 stretch: witnesses and determinant ==')
for j in (1, 2, 3, 48, 300):
    q = 12 * j + 4
    R_ = cov(q)
    rf, gh, gv, tau = R_.facts()
    S, T, p = (F(q, 2), F(1)), (F(3 * q), F(3)), (F(2 * q), F(2))
    bound = sqrt(q) / 12
    wits = thin_witnesses(q)
    ok = []
    for c, sig, h in wits:
        for hh in (h, -h):  # also mirror direction is a different shot
            try:
                w, ev = R_.trace(S, (hh, 1), T, 10 ** 6)
            except Fail as e:
                continue
            k0 = ev[0][0]
            # actual collinearity with first crossing
            cpt = (ev[0][2], ev[0][1])
            Tp = develop(w, T)
            cp = develop(w[:k0], cpt)
            d_act = det((cp[0] - S[0], cp[1] - S[1]), (Tp[0] - S[0], Tp[1] - S[1]))
            sub = lambda ax, v: F(2 * q) if (ax == 'x' and v == 2 * q - 3) else v
            Tf = develop(w, T, sub)
            pf = develop(w[:k0], p, sub)
            d0 = det((pf[0] - S[0], pf[1] - S[1]), (Tf[0] - S[0], Tf[1] - S[1])) * 2 / q
            ok.append((len(w), cpt[0], len(ev), d_act, d0))
    out(f'q={q}: reflex={rf} gcdH={gh} gcdV={gv} tau={tau} bound sqrt(q)/12={bound:.3f}')
    for n, cx, ne, da, d0 in sorted(set(ok)):
        assert da == 0 and d0.denominator == 1 and d0 % 2 == 1 and n + 1 >= bound
        out(f'   lit: R={n:6d} door x={cx} band passages={ne + 1} det_actual={da} det_t0(2x/q,y)={d0}')
    assert ok

out('\n== C. Thin completeness: all developed images with <= L reflections ==')
for q, L in ((16, 8), (28, 8), (580, 8), (3604, 10)):
    best, ntr = complete_check(cov(q), (F(q, 2), F(1)), (F(3 * q), F(3)), L)
    need = sqrt(q) / 12 - 1
    out(f'q={q}: bound needs R >= {need:.3f}; traced {ntr} images; min R with <= {L} refl: {best}')
    assert best is None or best >= need

# ---------------------------------------------------------------- fat
def st(m):
    return Room([(0, m, 0, m), (m, m + 1, m - 1, m + 2), (m + 1, m + 2, m, m + 3), (m + 2, 2 * m + 2, m + 2, 2 * m + 2)])


def fold(z, m):
    r = z % (2 * m)
    return r if r <= m else 2 * m - r


def rnd(x):
    return int((2 * x + 1) // 2)


def fat_marks(k):
    m = 144 * k * k
    s = F(6 * k) + F(3, 2)
    a0, b0 = m // 2 + 1, m // 4 + 1
    zS = F(m) - F(1, 2) - a0 * s           # moves by -4s per i
    dS = (zS - F(m, 2)) % (2 * m)
    i = rnd(dS / (4 * s))
    zT = F(1, 2) + b0 * s                    # moves by +4s per j
    dT = (F(m, 2) - zT) % (2 * m)
    jj = rnd(dT / (4 * s))
    a, b = a0 + 4 * i, b0 + 4 * jj
    S = (fold(F(m) - F(1, 2) - a * s, m), F(m - a))
    T = (m + 2 + fold(F(1, 2) + b * s, m), F(m + 2 + b))
    zs = F(m) - F(1, 2) - a * s
    sgn = 1 if (zs % (2 * m)) <= m else -1   # physical horizontal sign moving up
    return m, s, a, b, S, T, (sgn * 2 * s, F(2))


out('\n== D. Fat st279 stretch: witnesses, depth, limit determinant ==')
fat_err = {}
for k in (1, 2, 4, 16, 128, 320):
    m, s, a, b, S, T, d = fat_marks(k)
    R_ = st(m)
    rf, gh, gv, tau = R_.facts()
    w, ev = R_.trace(S, d, T, 10 ** 6)
    seams = [e[2] for e in ev]
    assert seams == [m - F(1, 2), m + 1, m + F(5, 2)], seams
    par = (S[0] % 2, S[1] % 2, T[0] % 2, T[1] % 2)
    assert all(v.denominator == 1 for v in S + T) and par == (0, 1, 0, 1)
    depthS = min(S[0], m - S[0], S[1], m - S[1])
    depthT = min(T[0] - m - 2, 2 * m + 2 - T[0], T[1] - m - 2, 2 * m + 2 - T[1])
    # limit determinant in coordinates 4/m
    lim = lambda ax, v: F(0) if v == 0 else (F(m) if v <= m + 3 else F(2 * m))
    S0, T0, p0 = (F(m, 2), F(m, 2)), (F(3 * m, 2), F(5 * m, 4)), (F(m), F(m))
    k0 = ev[0][0]
    pf = develop(w[:k0], p0, lim)
    Tf = develop(w, T0, lim)
    D0 = det((pf[0] - S0[0], pf[1] - S0[1]), (Tf[0] - S0[0], Tf[1] - S0[1])) * 16 / (m * m)
    assert D0.denominator == 1 and D0 % 4 == 2
    eS = max(abs(S[0] - S0[0]), abs(S[1] - S0[1])) / m
    eT = max(abs(T[0] - T0[0]), abs(T[1] - T0[1])) / m
    fat_err[k] = (m, eS, eT)
    out(f'k={k} m={m}: reflex={rf} gcdH={gh} gcdV={gv} tau={tau} S={tuple(map(int,S))} T={tuple(map(int,T))} '
        f'a-m/2={a - m // 2} b-m/4={b - m // 4} (cap 2m/s+5={float(2*m/s+5):.1f})')
    out(f'   lit: R={len(w)}  R/sqrt(m)={len(w)/sqrt(m):.3f}  band passages={len(ev)+1}  '
        f'depth/m S={float(depthS/m):.3f} T={float(depthT/m):.3f}  limit det (4/m coords)={D0}  '
        f'eS*sqrt(m)={float(eS)*sqrt(m):.2f} eT*sqrt(m)={float(eT)*sqrt(m):.2f}')

out('\n== E. Fat explicit bound from the note inequality, then completeness ==')
for k, (m, eS, eT) in fat_err.items():
    R = 0
    while True:
        dl = float(eS) + max(1 / m, float(eT)) + 6 * R / m
        if 12 * (R + 1) * dl + 2 * dl * dl >= 1 / 8:
            break
        R += 1
    fat_err[k] = fat_err[k] + (R,)
    out(f'k={k} m={m}: note inequality forces R >= {R}  (sqrt(m)/R+1 = {sqrt(m)/(R+1):.0f})')
for k, L in ((1, 9), (128, 8), (320, 10)):
    m, s, a, b, S, T, d = fat_marks(k)
    best, ntr = complete_check(st(m), S, T, L)
    out(f'k={k}: traced {ntr} images; min R with <= {L} refl: {best}')
    assert best is None or best >= fat_err[k][3]

out(f'\nCPU seconds: {time.process_time() - CPU0:.1f}')
