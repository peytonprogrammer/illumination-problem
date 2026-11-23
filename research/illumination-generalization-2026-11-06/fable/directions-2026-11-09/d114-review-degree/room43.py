"""D114 claims 2-4 on the note's 20-wall room (DBay) and its stretches L = 4 + 66k.
python3 -B room43.py > room43.log"""
import sys, time
from fractions import Fraction as Fr
from math import floor
from tracer import Room, rect, Corner, path_points, crossings, cross_x, reach, reflex

s0 = Fr(43, 33)


def dbay(k):
    L = 4 + 66 * k
    C = (rect(0, 5, 0, 4) | rect(1, 3, 4, 48) | rect(1, 3, -3, 0) | rect(5, 5 + L, 1, 2)
         | rect(5 + L, 9 + L, -1, 5))
    return Room(C), L, (2, 47), (10 + 66 * k, 3)


def direction(s, sx, sy):
    return (sx * s.denominator, sy * s.numerator)


def lit(room, S, T, s, sy, maxev=400000):
    try:
        res = path_points(room, S, direction(s, 1, sy), T, maxev)
    except Corner as c:
        return f'corner {tuple(map(str, c.args[0]))}', None
    if res is None:
        return 'no reach', None
    pts, _ = res
    return 'REACH', pts


def contact_split(pts, L):
    src = sum(1 for q in pts[1:-1] if q[0] <= 5 and not (q[0] == 5 and 1 < q[1] < 2))
    cor = sum(1 for q in pts[1:-1] if 5 < q[0] < 5 + L)
    tgt = sum(1 for q in pts[1:-1] if q[0] >= 5 + L)
    return src, cor, tgt


def mismatch_j(room, L, S, T, s, sy, j, back=(-1, -1)):
    """Source launched right with vertical sign sy, followed to its (j+1)-th eastward crossing of x=5
    (the last forward exit after j round trips); target traced backward with launch signs `back`
    to its first westward crossing of x=5+L. d113 sign convention f = (vertical sign)(y-1)."""
    yA, gA, _ = room.shoot(S, direction(s, 1, sy), cross_x(5, 1, j + 1))[0]
    yB, gB, _ = room.shoot(T, direction(s, *back), cross_x(5 + L, -1, 1))[0]
    return L * s + gA * (yA - 1) + gB * (yB - 1), (yA, gA), (yB, gB)


def section(t):
    print('\n== ' + t + ' ==')


def main():
    t_start = time.process_time()
    room, L, S, T = dbay(0)
    section('room DBay, L = 4')
    print('W =', room.W, ' r =', room.r, ' reflex =', reflex(room.V))

    section('claim 2: four central-slope launches from S at 43/33')
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        try:
            room.shoot(S, direction(s0, sx, sy), reach(T), 4000)
            print(f'  ({sx:+d},{sy:+d}): no corner (unexpected)')
        except Corner as c:
            print(f'  ({sx:+d},{sy:+d}): stops at vertex {tuple(map(int, c.args[0]))}')

    section('claim 4: s = 31/23, source launched right and UP, k = 0')
    s = Fr(31, 23)
    print('  first top hit y=48 at x =', 2 + Fr(1) / s, '; unfolded image height 2*48-47 = 49')
    print('  49 - 33 s =', 49 - 33 * s, '(> 4:', 49 - 33 * s > 4, ')')
    (yA, gA, tA), _, _ = room.shoot(S, direction(s, 1, 1), cross_x(5, 1, 1))
    (yB, gB, tB), _, _ = room.shoot(T, direction(s, -1, -1), cross_x(5 + L, -1, 1))
    print(f'  source door: y = {yA}, vertical sign {gA:+d}, developed x-travel {tA * s.denominator}')
    print(f'  57 - 41 s = {57 - 41 * s};  target backward door: y = {yB}, sign {gB:+d}, 3 - s = {3 - s}')
    Fv = L * s + gA * (yA - 1) + gB * (yB - 1)
    print(f'  F = 4s + fA + fB = {L * s} + ({gA * (yA - 1)}) + ({gB * (yB - 1)}) = {Fv};  46s-58 = {46 * s - 58};'
          f' lower-branch continuation 46s-56 = {46 * s - 56}')
    st, pts = lit(room, S, T, s, 1)
    src, cor, tgt = contact_split(pts, L)
    dx = sum(abs(b[0] - a[0]) for a, b in zip(pts, pts[1:])); dy = sum(abs(b[1] - a[1]) for a, b in zip(pts, pts[1:]))
    print(f'  full trace: {st}, {len(pts) - 2} reflections = {src} source chamber + {cor} corridor + {tgt} target chamber;'
          f' crossings of x=5: {crossings(pts, 5)}; developed |dx|,|dy| = {dx}, {dy}')
    st2, _ = lit(room, S, T, s, -1)
    print('  same slope launched DOWN:', st2)

    section('claim 4: L = 4 + 66k, corrected upper root s_k = (54+86k)/(40+66k) for F = 6+86k')
    print('  s_k - 43/33 = 62/(33(40+66k)) > 0 and decreasing; check k=0..5:',
          all(Fr(54 + 86 * k, 40 + 66 * k) - s0 == Fr(62, 33 * (40 + 66 * k)) for k in range(6)))
    print('  s_2 =', Fr(54 + 172, 40 + 132), '; 113/86 < 46/35:', Fr(113, 86) < Fr(46, 35),
          '; 46/35 - 113/86 =', Fr(46, 35) - Fr(113, 86), '; 43/33 < s < 46/35 gives 47-31s>4:', Fr(43, 31) > Fr(46, 35),
          ', 47-33s<4: True, 1<47-35s<2:', Fr(45, 35) < s0)
    print('  s_0, s_1 window test (need s < 46/35):', [(str(Fr(54 + 86 * k, 40 + 66 * k)), Fr(54 + 86 * k, 40 + 66 * k) < Fr(46, 35)) for k in (0, 1)])
    print('  d113 upper numerator 56+86k gives F =', [str((40 + 66 * k) * Fr(56 + 86 * k, 40 + 66 * k) - 48) for k in (1, 3, 10)],
          'for k = 1,3,10, i.e. 8+86k; required 4+86k =', [4 + 86 * k for k in (1, 3, 10)])
    rows = [(0, Fr(31, 23), 1, 'up-launch chart 46s-58 = 4'), (1, Fr(71, 53), -1, 'd113 k=1 path')]
    rows += [(k, Fr(54 + 86 * k, 40 + 66 * k), -1, 'corrected upper root 6+86k') for k in (2, 3, 10, 100, 1000)]
    rows += [(3, Fr(56 + 86 * k, 40 + 66 * k), -1, "d113's 8+86k root") for k in (3,)]
    for k, s, sy, name in rows:
        room, L, S, T = dbay(k)
        t = time.process_time()
        Fv = None
        try:
            Fv = mismatch_j(room, L, S, T, s, sy, 0)[0]
        except Corner:
            pass
        st, pts = lit(room, S, T, s, sy, maxev=400000)
        extra = ''
        if pts:
            dx = sum(abs(b[0] - a[0]) for a, b in zip(pts, pts[1:]))
            extra = f'{len(pts) - 2} reflections, x=5 crossings {crossings(pts, 5)}, developed |dx| {dx}'
        print(f'  k={k:<4d} L={L:<6d} W={room.W} r={room.r} s={s} launch {"up" if sy > 0 else "down"} ({name}):'
              f' first-door F={Fv} -> {st} {extra} [{time.process_time() - t:.1f}s]')

    section('claim 3: derivative of the (2j+1)-traversal mismatch equals the total horizontal travel')
    eps = Fr(1, 10 ** 9)
    for k, s, sy in ((0, Fr(13, 10), -1), (0, Fr(27, 20), 1), (0, Fr(5, 4), 1), (1, Fr(71, 53), -1)):
        room, L, S, T = dbay(k)
        st, pts = lit(room, S, T, s, sy)
        n = crossings(pts, 5); j = (n - 1) // 2
        X = sum(abs(b[0] - a[0]) for a, b in zip(pts, pts[1:]))
        a_, b_ = pts[-2], pts[-1]
        back = (1 if a_[0] > b_[0] else -1, 1 if a_[1] > b_[1] else -1)   # reversed arrival direction
        F0 = mismatch_j(room, L, S, T, s, sy, j, back)
        Fm = mismatch_j(room, L, S, T, s - eps, sy, j, back)[0]; Fp = mismatch_j(room, L, S, T, s + eps, sy, j, back)[0]
        print(f'  k={k} s={s} launch {"up" if sy > 0 else "down"}, backward target launch {back}: {st}, crossings {n} (j={j}); F_j(s)={F0[0]}'
              f' (even: {F0[0] % 2 == 0}); dF/ds left {(F0[0] - Fm) / eps}, right {(Fp - F0[0]) / eps};'
              f' total |dx| = {X} = (2j+1)L + chamber travels with (2j+1)L = {(2 * j + 1) * L}')

    section('claim 3: counting identity across the 43/33 graze (first traversal, down launch, theta = 0)')
    room, L, S, T = dbay(0)
    a, b = s0 - Fr(30, 3300), s0 + Fr(30, 3300)
    H = lambda u: floor(u / 2)
    Fa = mismatch_j(room, L, S, T, a, -1, 0)[0]; Fb = mismatch_j(room, L, S, T, b, -1, 0)[0]
    Fm = 46 * s0 - 56; Fp = 40 * s0 - 48
    hits = (H(Fm) - H(Fa)) + (H(Fb) - H(Fp))
    print(f'  F(a)={Fa} F(s0-)={Fm} F(s0+)={Fp} F(b)={Fb}; piece hits {hits};'
          f' endpoint change {H(Fb) - H(Fa)} minus jump {H(Fp) - H(Fm)} = {H(Fb) - H(Fa) - (H(Fp) - H(Fm))}')
    for e in (Fr(29, 3300), Fr(1, 3300)):
        print(f'   check branch formulas at s0-{e}: {mismatch_j(room, L, S, T, s0 - e, -1, 0)[0] == 46 * (s0 - e) - 56},'
              f' s0+{e}: {mismatch_j(room, L, S, T, s0 + e, -1, 0)[0] == 40 * (s0 + e) - 48}')

    section("claim 2 data: exit phases (units 1/33, mod 66) at successive eastward x=5 crossings, offset start +-1/132")
    room, L, S, T = dbay(0)
    for side in (-1, 1):
        for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            seq = []
            def coll(p, q, d, t0):
                if (p[0] - 5) * (q[0] - 5) < 0 and d[0] > 0:
                    y = p[1] + (5 - p[0]) * d[1] / d[0]
                    ph = (1 if d[1] > 0 else -1) * (y - 1) % 2
                    seq.append(round(33 * ph) % 66)
                    if len(seq) == 40:
                        return True
                return None
            start = (Fr(S[0]), S[1] + sy * Fr(side, 132))
            room.shoot(start, direction(s0, sx, sy), coll, 200000)
            per = next(p for p in range(1, 40) if seq[p:] == seq[:40 - p])
            first = seq.index(49) if 49 in seq else None
            print(f'  side {side:+d} launch ({sx:+d},{sy:+d}): first phase {seq[0]}, period {per}, first index of 49: {first}, '
                  f'multiplicity of 49 over 935 = {935 // per if first is not None else 0}; cycle {seq[:per]}')
    tp = []
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        y, g, _ = room.shoot(T, direction(s0, sx, sy), cross_x(9, -1, 1))[0]
        tp.append(round(33 * (g * (y - 1) % 2)) % 66)
    print('  backward target first-hit phases (++,+-,-+,--):', tp, '; required source phase for -- target:', (-172 - tp[3]) % 66)
    print(f'\nCPU {time.process_time() - t_start:.1f}s')


if __name__ == '__main__':
    main()
