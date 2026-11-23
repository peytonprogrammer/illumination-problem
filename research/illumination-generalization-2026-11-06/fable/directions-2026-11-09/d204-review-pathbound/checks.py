"""d204 review checks: exact rational billiard traces in the named one-neck family.

Room (word LLLLRRLLLLRR), for integers m >= 2, u >= 1:
  left chamber [-u-1, 0] x [-m-1, 3], neck [0, m] x [0, 2],
  right chamber [m, m+2] x [-1, 3].  S = (-u, -m), T = (m+1, 1).

Check A: the straight segment S->T is legal with zero reflections iff u > m(m+1).
Check B: the snapshot's prescribed slope-r ray reaches T legally with <= 2m+4
reflections, for every admissible odd target phase in the prescribed interval.

Only these prescribed rays in these named rooms are traced. Standard library only.
"""
from fractions import Fraction as Fr
import sys
import time


def room(m, u):
    v = [(-u - 1, -m - 1), (0, -m - 1), (0, 0), (m, 0), (m, -1), (m + 2, -1),
         (m + 2, 3), (m, 3), (m, 2), (0, 2), (0, 3), (-u - 1, 3)]
    edges = [(v[i], v[(i + 1) % len(v)]) for i in range(len(v))]
    return v, edges


def turn_word(v):
    w = []
    n = len(v)
    for i in range(n):
        a, b, c = v[i - 1], v[i], v[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        w.append('L' if cr > 0 else 'R')
    return ''.join(w)


def trace(v, edges, p, d, target, max_refl):
    """Trace from p in direction d. Return (status, reflections, stop_point).

    status: 'reached' (T hit strictly before any wall), 'vertex' (ray meets a
    polygon corner: illegal), 'limit'.
    """
    verts = set((Fr(x), Fr(y)) for x, y in v)
    px, py = Fr(p[0]), Fr(p[1])
    dx, dy = Fr(d[0]), Fr(d[1])
    tx, ty = Fr(target[0]), Fr(target[1])
    refl = 0
    while True:
        best = None
        for (a, b) in edges:
            if a[0] == b[0]:  # vertical edge x = c
                if dx == 0:
                    continue
                t = (a[0] - px) / dx
                if t <= 0:
                    continue
                y = py + t * dy
                lo, hi = min(a[1], b[1]), max(a[1], b[1])
                if lo <= y <= hi and (best is None or t < best[0]):
                    best = (t, 'v')
            else:  # horizontal edge y = c
                if dy == 0:
                    continue
                t = (a[1] - py) / dy
                if t <= 0:
                    continue
                x = px + t * dx
                lo, hi = min(a[0], b[0]), max(a[0], b[0])
                if lo <= x <= hi and (best is None or t < best[0]):
                    best = (t, 'h')
        t, kind = best
        # does the target lie on the open segment before the hit?
        if dx != 0:
            tt = (tx - px) / dx
        else:
            tt = (ty - py) / dy
        if 0 < tt < t and px + tt * dx == tx and py + tt * dy == ty:
            return 'reached', refl, (tx, ty)
        hx, hy = px + t * dx, py + t * dy
        if (hx, hy) in verts:
            return 'vertex', refl, (hx, hy)
        refl += 1
        if refl > max_refl:
            return 'limit', refl, (hx, hy)
        px, py = hx, hy
        if kind == 'v':
            dx = -dx
        else:
            dy = -dy


def main():
    t0 = time.process_time()
    M = range(2, 31)
    U = range(1, 1001)
    out = []
    v, _ = room(2, 1)
    out.append('turn word (CCW from (-u-1,-m-1)), cyclic: %s' % turn_word(v))

    # Check A
    mismatch_a = 0
    eq_vertex = 0
    for m in M:
        for u in U:
            v, e = room(m, u)
            S, T = (-u, -m), (m + 1, 1)
            st, r, pt = trace(v, e, S, (T[0] - S[0], T[1] - S[1]), T, 0)
            legal = (st == 'reached' and r == 0)
            if legal != (u > m * (m + 1)):
                mismatch_a += 1
                out.append('A MISMATCH m=%d u=%d status=%s' % (m, u, st))
            if u == m * (m + 1):
                if st == 'vertex' and pt == (0, 0):
                    eq_vertex += 1
                # mouth ordinate formula
            y0 = Fr(u - m * (m + 1), u + m + 1)
            yline = Fr(-m) + Fr(u) * Fr(m + 1, u + m + 1)
            if y0 != yline:
                out.append('A ordinate formula mismatch m=%d u=%d' % (m, u))
    out.append('Check A: %d (m,u) pairs, legality != [u > m(m+1)] in %d cases' %
               (len(M) * len(U), mismatch_a))
    out.append('Check A: at u = m(m+1) the segment stops at reflex corner (0,0) '
               'in %d of %d cases' % (eq_vertex, len(M)))

    # Check B
    fail_b = 0
    rays = 0
    worst = (-1, None)
    maxratio = Fr(0)
    k_bound_fail = 0
    chamber_fail = 0
    for m in M:
        for u in U:
            v, e = room(m, u)
            S, T = (-u, -m), (m + 1, 1)
            w = u + 1
            k = 0
            while u + 2 * k * w < m + 2:
                k += 1
            d = u + 2 * k * w
            D = d + m + 1
            if 2 * k > m + 3:
                k_bound_fail += 1
            if k > 0 and not (d <= w * (m + 2)):
                chamber_fail += 1
            lo, hi = Fr(m, d), Fr(m + 2, d)
            # admissible integers n = -m + rD, n odd, r in (lo, hi)
            n = (lo * D).__floor__() - m - 1
            cands = []
            while Fr(n + m, D) < hi:
                if n % 2 != 0 and lo < Fr(n + m, D):
                    cands.append(n)
                n += 1
            if not cands:
                fail_b += 1
                out.append('B NO ADMISSIBLE r m=%d u=%d' % (m, u))
                continue
            for n in cands:
                r = Fr(n + m, D)
                assert 0 < r < 1
                rays += 1
                st, nr, pt = trace(v, e, S, (1, r), T, 2 * m + 4)
                if st != 'reached' or nr > 2 * m + 4:
                    fail_b += 1
                    out.append('B FAIL m=%d u=%d r=%s status=%s refl=%d at %s' %
                               (m, u, r, st, nr, pt))
                    continue
                if nr > worst[0]:
                    worst = (nr, (m, u, r))
                ratio = Fr(nr, 2 * m + 4)
                if ratio > maxratio:
                    maxratio = ratio
    out.append('Check B: %d prescribed rays traced, %d failures' % (rays, fail_b))
    out.append('Check B: 2k <= m+3 violated in %d cases; d <= w(m+2) (k>0) '
               'violated in %d cases' % (k_bound_fail, chamber_fail))
    out.append('Check B: max reflections %d at (m,u,r)=%s; max refl/(2m+4) = %s' %
               (worst[0], worst[1], maxratio))
    out.append('CPU seconds: %.1f' % (time.process_time() - t0))
    print('\n'.join(out))


if __name__ == '__main__':
    main()
