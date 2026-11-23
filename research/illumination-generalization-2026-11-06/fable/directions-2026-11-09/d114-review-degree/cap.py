"""D114 claim 1: cap doubling on the odd crosses P_7 and P_9, plus the notched-square remark.
Arm = east arm [2,b]x[-2,2] (w = 4, length l = b-2), cap x = b. Double = P_b union its mirror in x = b.
Slopes are roots of the note's phase equation on a fixed short list of base slopes; no direction search.
python3 -B cap.py > cap.log"""
import time
from fractions import Fraction as Fr
from math import floor, ceil
from tracer import Room, rect, Corner, cross_x, reach, reflex

BASE = [Fr(37, 53), Fr(61, 47), Fr(89, 71), Fr(29, 97), Fr(113, 41), Fr(13, 59), Fr(151, 67), Fr(5, 43)]
SIGNS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
EPS = Fr(1, 10 ** 12)


def cross(b):
    return rect(-b, b, -2, 2) | rect(-2, 2, -b, b)


def mirror_cells(C, b):
    return {(2 * b - 1 - x, y) for x, y in C}


def mir(P, b):
    return (2 * b - Fr(P[0]), Fr(P[1]))


def d_of(s, sx, sy):
    return (sx * s.denominator, sy * s.numerator)


def edge_of(room, q):
    for x, lo, hi in room.vert:
        if q[0] == x and lo <= q[1] <= hi:
            return ('v', x, lo, hi)
    for y, lo, hi in room.horz:
        if q[1] == y and lo <= q[0] <= hi:
            return ('h', y, lo, hi)


def leg(room, P, s, signs, X, sense):
    """First crossing of x=X with horizontal sense; returns (y, vertical sign, time, wall-edge itinerary)."""
    bounces = []
    f = cross_x(X, sense)
    def g(p, q, d, t0):
        r = f(p, q, d, t0)
        if r is None:
            bounces.append(edge_of(room, q))
        return r
    r, nb, _ = room.shoot(P, d_of(s, *signs), g, 20000)
    if r is None:
        raise Corner('no portal crossing', 0)
    y, g_, t = r
    return y, g_, t, tuple(bounces)


def phase(y, sign):
    return (y + 2) if sign > 0 else -(y + 2)          # height above corridor floor y=-2, signed


def solve(Fs, s0, X, period=8):
    out = []
    for n in (floor(Fs / period), ceil(Fs / period), floor(Fs / period) - 1, ceil(Fs / period) + 1):
        out.append(s0 + (n * period - Fs) / X)
    return out


def F_and_X(D, b, S, Tp, s, sg, tg, strip, tsign):
    """Note's phase mismatch at slope s on the current itineraries, and its exact derivative."""
    vals = []
    for ss in (s, s + EPS):
        yA, gA, _, itA = leg(D, S, ss, sg, 2, 1)
        if strip:
            h = Fr(Tp[0]) - 2
            vals.append((phase(yA, gA) + h * ss - tsign * (Fr(Tp[1]) + 2), itA))
        else:
            yB, gB, _, itB = leg(D, Tp, ss, tg, 2 * b - 2, -1)
            vals.append((phase(yA, gA) + (2 * b - 4) * ss - phase(yB, -gB), (itA, itB)))
    if vals[0][1] != vals[1][1]:
        raise Corner('itinerary changes', 0)
    return vals[0][0], (vals[1][0] - vals[0][0]) / EPS


def double_path(D, b, S, Tp, strip):
    """Root of the phase equation F(s) in 8Z, by Newton steps on the current itinerary from each base
    slope (F is increasing and piecewise affine). Returns (direction, time to T', roots tried, s, signs)."""
    attempts = 0
    for s0 in BASE:
        for sg in SIGNS:
            for tg in ([None] if strip else [g for g in SIGNS if g[0] < 0]):
                for tsign in ((1, -1) if strip else (1,)):
                    try:
                        F0, X = F_and_X(D, b, S, Tp, s0, sg, tg, strip, tsign)
                    except Corner:
                        continue
                    for n in (floor(F0 / 8), ceil(F0 / 8)):
                        s = s0
                        for _ in range(8):
                            try:
                                Fs, X = F_and_X(D, b, S, Tp, s, sg, tg, strip, tsign)
                            except Corner:
                                break
                            if Fs == 8 * n:
                                attempts += 1
                                r = full(D, S, s, sg, Tp)
                                if r:
                                    return r + (attempts, s, sg)
                                break
                            s = s + (8 * n - Fs) / X
                            if s <= 0:
                                break
                            s = Fr(s).limit_denominator(10 ** 6) if s.denominator > 10 ** 6 else s
    return None


def full(D, S, s, sg, Tp):
    caps = [0]
    try:
        def g(p, q, d, t0):
            r = reach(Tp)(p, q, d, t0)
            if r:
                return r
            return None
        (st, t), nb, _ = D.shoot(S, d_of(s, *sg), g, 20000)
    except Corner:
        return None
    return (d_of(s, *sg), t)


def count_cap_crossings(D, S, d, t_end, b):
    n = [0]
    def g(p, q, dd, t0):
        if t0 >= t_end:
            return True
        lam = min(Fr(1), (t_end - t0) / ((q[0] - p[0]) / dd[0] if dd[0] else (q[1] - p[1]) / dd[1]))
        x2 = p[0] + lam * (q[0] - p[0])
        if (p[0] - b) * (x2 - b) < 0:
            n[0] += 1
        return None
    D.shoot(S, d, g, 20000)
    return n[0]


def project(P, S, T, d, tD):
    """Projection lemma check in the original room. Returns description."""
    try:
        (st, t), nb, _ = P.shoot(S, d, reach(T), 20000)
        if t == tD:
            return f'fold legal, reaches T at time {t} = double time', True
        try:
            P.shoot(S, d, lambda *a: None, 20000)
            a = None
        except Corner as c:
            a = c.args[1]
        return (f'T is reached on the incoming leg at time {t} before the cap corner at time {a}; '
                f'2a - D = {None if a is None else 2 * a - tD}: {a is not None and t == 2 * a - tD}'), a is not None and t == 2 * a - tD
    except Corner as c:
        v, a = c.args
        if 2 * a > tD:
            try:
                (st, t), _, _ = P.shoot(S, d, reach(T), 20000)
            except Corner as c2:
                return f'corner {v} at {a}; T should precede it but trace hits {c2.args[0]}', False
        rev = (-d[0], -d[1])
        try:
            (st, t), _, _ = P.shoot(S, rev, reach(T), 20000)
            ok = t == tD - 2 * a
            return (f'fold hits cap corner {tuple(map(str, v))} at time {a} < D-a; reversed ray from S reaches T at '
                    f'time {t} = D - 2a: {ok}'), ok
        except Corner as c2:
            return f'fold hits {tuple(map(str, v))} at {a}; reversed ray hits {c2.args[0]}', False


def run(b):
    print(f'\n== P_{b}: arm [2,{b}]x[-2,2], w=4, l={b - 2}; double across x={b} ==')
    P = Room(cross(b)); D = Room(cross(b) | mirror_cells(cross(b), b))
    capV = [(Fr(b), Fr(2)), (Fr(b), Fr(-2))]
    print(f'  P_{b}: W={P.W} r={P.r};  double: one boundary cycle, W={D.W} r={D.r}; '
          f'cap ends are vertices of P: {all(v in P.Vset for v in capV)}, of the double: {any(v in D.Vset for v in capV)}')
    print('  double reflex corners:', reflex(D.V))
    pairs = [('junction-junction', (-5, 1), (0, 5)), ('junction-junction', (-1, -1), (1, 1 - b)),
             ('junction-junction', (Fr(-3, 2), Fr(1, 3)), (Fr(1, 7), Fr(b - 1, 1) - Fr(1, 5))),
             ('junction-junction', (0, -b + 1), (0, b - 1)),
             ('junction-strip', (-b + 1, 1), (4, -1)), ('junction-strip', (1, b - 2), (b - 1, 1)),
             ('junction-strip', (Fr(-1, 3), Fr(-7, 5)), (Fr(b, 1) - Fr(1, 9), Fr(3, 2))),
             ('junction-mouth', (-3, 0), (2, 1)), ('junction-mouth', (1, -b + 2), (2, Fr(-3, 2)))]
    ok_all = True
    for kind, S, T in pairs:
        S = (Fr(S[0]), Fr(S[1])); T = (Fr(T[0]), Fr(T[1])); Tp = mir(T, b)
        r = double_path(D, b, S, Tp, kind != 'junction-junction')
        if r is None:
            print(f'  {kind} S={tuple(map(str, S))} T={tuple(map(str, T))}: construction found no path on the base list')
            continue
        d, tD, att, s, sg = r
        nc = count_cap_crossings(D, S, d, tD, b)
        msg, ok = project(P, S, T, d, tD)
        ok_all &= ok
        print(f'  {kind} S={tuple(map(str, S))} T={tuple(map(str, T))}: double path slope {s} signs {sg} '
              f'(root #{att}), crossings of x={b}: {nc}; {msg}')
    for S, T in (((3, 1), (b - 1, -1)), ((2, 0), (5, 1)), ((2, 1), (2, -1))):
        try:
            (st, t), nb, _ = P.shoot(S, (T[0] - S[0], T[1] - S[1]), reach(T), 1)
            print(f'  strip/mouth pair {S}-{T}: direct segment, {nb} reflections')
        except Corner as c:
            print(f'  strip/mouth pair {S}-{T}: direct segment hits {c.args[0]}'); ok_all = False
    print('  deliberate cap-endpoint cases (S=(0,1), direction (b,1) through the cap end (b,2)):')
    S = (Fr(0), Fr(1)); d = (b, 1)
    for tau in (Fr(3, 2), Fr(23, 10), Fr(37, 10)):
        pos = []
        def g(p, q, dd, t0, tau=tau):
            seg = (q[0] - p[0]) / dd[0] if dd[0] else (q[1] - p[1]) / dd[1]
            if t0 + seg >= tau:
                lam = tau - t0
                pos.append((p[0] + lam * dd[0], p[1] + lam * dd[1])); return True
            return None
        D.shoot(S, d, g, 1000)
        Tp = pos[0]; T = (2 * b - Tp[0], Tp[1]) if Tp[0] > b else Tp
        msg, ok = project(P, S, T, d, tau)
        ok_all &= ok
        print(f'    tau={tau}: T\'={tuple(map(str, Tp))} -> T={tuple(map(str, T))}: {msg}')
    print(f'  all projections legal: {ok_all}')


def notch(m):
    c = (m - 1) // 2
    C = rect(0, m, 0, m) - {(c, m - 1)}
    R = Room(C)
    cls = {}
    for X in range(m + 1):
        for Y in range(m + 1):
            o = [(X - 1, Y - 1) in C, (X - 1, Y) in C, (X, Y - 1) in C, (X, Y) in C]
            k = sum(o)
            if k in (4, 2):
                if k == 2 and o[0] == o[3]:
                    continue
                cls[(X % 2, Y % 2)] = cls.get((X % 2, Y % 2), 0) + 1
    xs = sorted({v[0] for v in R.V}); ys = sorted({v[1] for v in R.V})
    print(f'  notched square m={m}: W={R.W} r={R.r} reflex={reflex(R.V)} area={len(C)} (m^2-1={m * m - 1}); '
          f'interior-or-smooth points per class {dict(sorted(cls.items()))}; x-gaps {[b_ - a_ for a_, b_ in zip(xs, xs[1:])]}'
          f' y-gaps {[b_ - a_ for a_, b_ in zip(ys, ys[1:])]}')


if __name__ == '__main__':
    t = time.process_time()
    for b in (7, 9):
        run(b)
    print('\n== notched square (Limit-of-structural-conclusion paragraph) ==')
    for m in (5, 9, 21):
        notch(m)
    print(f'\nCPU {time.process_time() - t:.1f}s')
