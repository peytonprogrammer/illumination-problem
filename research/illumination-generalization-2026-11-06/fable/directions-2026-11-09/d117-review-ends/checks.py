"""D117 checks for component-ends.snapshot.md (cov279 control).

Exact Fraction tracer on the named one-parameter cov279 room:
  bands (y-range) -> single open run (x-range)
  (0,2): (0,2)   (2,3): (2-t,4)   (3,4): (2,5)   (4,6): (4,6)
S = (1/2, 1), T = (3, 3), p = (2, 2).

Checks:
 1. Room facts at t = 3/q: reflex count, wall gcds, mark parities, area.
 2. Translate formula shots (claim "These pairs are lit"): each lattice
    abscissa c in (2-t, 2) of 7/4 + Z/q, with i solved by a modular
    inverse, replays as a legal shot S -> T.
 3. Exact-check shots (slope 4m + 3/2 - t/3 at t = 3/(12m+4)) replay.
 4. Note's determinant argument on every replayed shot: det = 0 at t,
    formal t = 0 development gives odd det in (2x, y), error bounds hold,
    and the reflection count satisfies m+1 >= 1/sqrt(48 t).
 5. Control: the m=2 exact slope at t = 3/28 +- 1/1000 does not hit T.
No search over rooms, directions or words is performed.
"""
from fractions import Fraction as F
from math import gcd, floor
import time

T0 = time.process_time()
S = (F(1, 2), F(1))
TGT = (F(3), F(3))
P = (F(2), F(2))
LEVELS = [F(0), F(2), F(3), F(4), F(6)]


def runs(t):
    return [(F(0), F(2)), (2 - t, F(4)), (F(2), F(5)), (F(4), F(6))]


def refl(g, axis, a):
    """g o R where R reflects axis coordinate about a. g = (sx,bx,sy,by)."""
    sx, bx, sy, by = g
    if axis == 'x':
        return (-sx, 2 * a * sx + bx, sy, by)
    return (sx, bx, -sy, 2 * a * sy + by)


def app(g, pt):
    sx, bx, sy, by = g
    return (sx * pt[0] + bx, sy * pt[1] + by)


class Fail(Exception):
    pass


def trace(t, dx, dy, maxrefl=100000):
    """Trace from S with direction (dx, dy). Return word or raise Fail.
    word entries: ('x', band, side) or ('y', level_index)."""
    R = runs(t)
    x, y = S
    band = 0
    word = []
    first_cross = None  # (prefix length, crossing abscissa)
    while len(word) <= maxrefl:
        lo, hi = R[band]
        ylo, yhi = LEVELS[band], LEVELS[band + 1]
        # time to vertical wall
        tx = None
        if dx > 0:
            tx = (hi - x) / dx
        elif dx < 0:
            tx = (lo - x) / dx
        ty = (yhi - y) / dy if dy > 0 else (ylo - y) / dy
        # target on level 3 inside band 1 (top) or band 2 (bottom)
        if tx is not None and tx < ty:
            x, y = (hi if dx > 0 else lo), y + dy * tx
            if y in (ylo, yhi):
                raise Fail('corner')
            word.append(('x', band, 'R' if dx > 0 else 'L'))
            dx = -dx
            continue
        if tx is not None and tx == ty:
            raise Fail('corner (simultaneous)')
        x, y = x + dx * ty, (yhi if dy > 0 else ylo)
        if (x, y) == TGT:
            return word, first_cross
        li = band + 1 if dy > 0 else band
        nb = band + 1 if dy > 0 else band - 1
        if nb < 0 or nb >= len(R):
            word.append(('y', li))
            dy = -dy
            continue
        a, b = R[nb]
        if x in (lo, hi, a, b):
            raise Fail('corner at level')
        if a < x < b:
            if band == 0 and nb == 1 and first_cross is None:
                first_cross = (len(word), x)
            band = nb
            continue
        word.append(('y', li))
        dy = -dy
    raise Fail('too long')


def wall_x(t, band, side):
    lo, hi = runs(t)[band]
    return lo if side == 'L' else hi


def develop(t, word, upto=None):
    g = (F(1), F(0), F(1), F(0))
    for k, w in enumerate(word):
        if upto is not None and k == upto:
            break
        if w[0] == 'x':
            g = refl(g, 'x', wall_x(t, w[1], w[2]))
        else:
            g = refl(g, 'y', LEVELS[w[1]])
    return g


def det_check(t, word, fc):
    """Note's argument in (X, Y) = (2x, y)."""
    m = len(word)
    k, c = fc
    gT, gP = develop(t, word), develop(t, word, k)
    Tt, Pt = app(gT, TGT), app(gP, (c, F(2)))
    g0T, g0P = develop(F(0), word), develop(F(0), word, k)
    T0d, P0d = app(g0T, TGT), app(g0P, P)
    X = lambda q: (2 * q[0], q[1])
    s = X(S)
    a_t = (X(Pt)[0] - s[0], X(Pt)[1] - s[1])
    b_t = (X(Tt)[0] - s[0], X(Tt)[1] - s[1])
    a0 = (X(P0d)[0] - s[0], X(P0d)[1] - s[1])
    b0 = (X(T0d)[0] - s[0], X(T0d)[1] - s[1])
    dt = a_t[0] * b_t[1] - a_t[1] * b_t[0]
    d0 = a0[0] * b0[1] - a0[1] * b0[0]
    ea, eb = abs(a_t[0] - a0[0]), abs(b_t[0] - b0[0])
    assert a_t[1] == a0[1] and b_t[1] == b0[1], 'ordinates moved'
    assert d0.denominator == 1 and d0.numerator % 2 == 1, ('det0', d0)
    assert dt == 0, ('not collinear', dt)
    assert ea <= 2 * t + 4 * t * k and eb <= 4 * t * m
    assert abs(a0[1]) <= 6 * (k + 1) and abs(b0[1]) <= 6 * (m + 1)
    bound = 6 * (m + 1) * (8 * m + 2) * t
    assert 1 <= bound <= 48 * (m + 1) ** 2 * t
    assert F((m + 1) ** 2) >= 1 / (48 * t)
    return d0, ea, eb, bound


def room_facts(q):
    t = F(3, q)
    R = [(lo * q, hi * q) for lo, hi in runs(t)]
    reflex = 0
    for (a, b), (c, d) in zip(R, R[1:]):
        reflex += 2 if (c > a and d > b) else 0  # both ends step right
    hor = [R[0][1] - R[0][0], R[-1][1] - R[-1][0]]
    for (a, b), (c, d) in zip(R, R[1:]):
        hor += [abs(c - a), abs(d - b)]
    hg = 0
    for h in hor:
        hg = gcd(hg, int(h))
    area = sum((b - a) * (LEVELS[i + 1] - LEVELS[i]) for i, (a, b) in enumerate(R))
    Sx, Tx = S[0] * q, TGT[0] * q
    return dict(reflex=reflex, walls=2 * reflex + 4, hgcd=hg, area=area,
                area_formula=13 * q + 3,
                S=(Sx, S[1]), T=(Tx, TGT[1]),
                par=(Sx % 2, int(S[1]) % 2, Tx % 2, int(TGT[1]) % 2))


def translate_shots(q):
    """c in (2-t,2) on 7/4 + Z/q; solve 4q i = -(2cq - 7q/2) mod (4q+6)."""
    t = F(3, q)
    out = []
    n_lo = (2 - t - F(7, 4)) * q
    n_hi = (F(2) - F(7, 4)) * q
    n = floor(n_lo) + 1
    cs = []
    while F(7, 4) + F(n, q) < 2:
        cs.append(F(7, 4) + F(n, q))
        n += 1
    for c in cs:
        # need (2c - 7/2 + 4i) / (4 + 2t) integer -> scaled by q
        A = 4 * q
        M = 4 * q + 6
        B = -(2 * c * q - F(7, 2) * q)
        assert B.denominator == 1
        B = int(B)
        g = gcd(A, M)
        if B % g:
            out.append((c, None, 'no solution'))
            continue
        i0 = (B // g) * pow(A // g, -1, M // g) % (M // g)
        # smallest i >= i0 - k*(M/g) with D > 0
        i = i0
        while c - F(1, 2) + 4 * (i - M // g) > 0:
            i -= M // g
        D = c - F(1, 2) + 4 * i
        out.append((c, D, None))
    return t, out


def main():
    lines = []
    pr = lambda *a: (lines.append(' '.join(str(x) for x in a)), print(*a))
    pr('# D117 checks (exact Fraction arithmetic)')
    pr('## 1. Room facts at t = 3/q, q = 12j+4')
    for j in range(1, 6):
        q = 12 * j + 4
        f = room_facts(q)
        pr(f'j={j} q={q}', f)
        assert f['reflex'] == 6 and f['walls'] == 16 and f['hgcd'] == 1
        assert f['area'] == f['area_formula'] and f['par'] == (0, 1, 0, 1)
    pr('## 2. Translate-formula shots and 4. determinant argument')
    for j in range(1, 6):
        q = 12 * j + 4
        t, shots = translate_shots(q)
        for c, D, err in shots:
            if err:
                pr(f'q={q} c={c}: {err}')
                continue
            word, fc = trace(t, D, F(1))
            d0, ea, eb, bd = det_check(t, word, fc)
            pr(f'q={q} t={t} c={c} D={D} refl={len(word)} first_cross={fc[1]} '
               f'det0={d0} ea={ea} eb={eb} bound={float(bd):.3f} '
               f'lowerbound(m+1)>={1/(48*float(t))**0.5:.3f}')
            assert fc[1] == c
    pr('## 3. Exact-check shots, slope 4m + 3/2 - t/3, t = 3/(12m+4)')
    for m in range(1, 9):
        t = F(3, 12 * m + 4)
        sA = 4 * m + F(3, 2) - t / 3
        sB = 4 * m + 1 + t / 3 + 2 * t * m
        assert sA == sB, (m, sA, sB)
        word, fc = trace(t, sA, F(1))
        d0, ea, eb, bd = det_check(t, word, fc)
        nv = sum(1 for w in word if w[0] == 'x')
        pr(f'm={m} t={t} slope={sA} c={fc[1]} (2-t/3={2 - t/3}) refl={len(word)} '
           f'vertical={nv} det0={d0} bound={float(bd):.3f} '
           f'need m+1>={1/(48*float(t))**0.5:.3f}')
        assert fc[1] == 2 - t / 3
    pr('## 5. Same slopes off the parameter: m=2 slope at t=3/28 +- 1/1000 miss T')
    m = 2
    for t in (F(3, 28) + F(1, 1000), F(3, 28) - F(1, 1000)):
        sA = 4 * m + F(3, 2) - t / 3
        try:
            word, fc = trace(t, sA, F(1), maxrefl=200)
            pr(f't={t}: unexpectedly hit T, refl={len(word)}')
        except Fail as e:
            pr(f't={t}: no hit within 200 reflections ({e})')
    pr(f'CPU seconds: {time.process_time() - T0:.2f}')
    open(__file__.replace('checks.py', 'checks.log'), 'w').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
