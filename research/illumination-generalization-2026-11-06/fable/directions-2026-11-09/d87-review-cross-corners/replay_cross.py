"""D87: independent checks for every-direction.md.

1. Parity counts mu(e) and level sums for the cross and for positive controls.
2. Half-offset leaf census on the four-sheet unfolding M in sampled directions:
   a single cylinder (H=2) or two exchanged cylinders (H=1) both force exactly two
   half-offset closed leaves, swapped by tau. The lemma says the cross never has that.
3. The (6,0) -> (0,6) path for many b.
4. Optional: all same-parity interior lattice pairs of the b=7 cross.
"""
from fractions import Fraction as F
from math import floor, ceil, gcd, hypot
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from billiard import run, incid


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def cross(b):
    return rect(-b, b, -2, 2) | rect(-2, 2, -b, b)


def corners(cells):
    pts = {(x + i, y + j) for x, y in cells for i in (0, 1) for j in (0, 1)}
    return ({p for p in pts if incid(cells, p) == 1}, {p for p in pts if incid(cells, p) == 3})


CLASSES = [(0, 0), (1, 0), (0, 1), (1, 1)]


def mu(cells):
    cv, rf = corners(cells)
    m = {e: 0 for e in CLASSES}
    for p in cv:
        m[(p[0] % 2, p[1] % 2)] += 1
    for p in rf:
        m[(p[0] % 2, p[1] % 2)] -= 1
    return [m[e] for e in CLASSES]


def level_sums(m):
    """For L = y, x, x+y (directions (1,0),(0,1),(1,1) mod 2): sums on L=0 and L=1."""
    out = {}
    for name, L in (('L=y', lambda e: e[1]), ('L=x', lambda e: e[0]), ('L=x+y', lambda e: (e[0] + e[1]) % 2)):
        s = [0, 0]
        for e, v in zip(CLASSES, m):
            s[L(e)] += v
        out[name] = tuple(s)
    return out


def leaf_census(cells, p, q):
    """Count half-offset closed leaves on M in primitive direction (p, q), p != 0.

    States are (X, y, vx, vy) at vertical grid-line events, velocity after the event.
    Returns (N, swapped_pairs, self_tau)."""
    assert p != 0
    ap = abs(p)
    vsegs = set()
    for x, y in cells:
        vsegs.add((x, y))
        vsegs.add((x + 1, y))
    states = []
    for X, n in vsegs:
        left, right = (X - 1, n) in cells, (X, n) in cells
        for j in range(ap):
            y = n + F(2 * j + 1, 2 * ap)
            for sx in ((1, -1) if left and right else ((1,) if right else (-1,))):
                for sy in (1, -1):
                    states.append((X, y, sx * ap, sy * q))
    index = {}
    orbits = 0

    def step(X, y, vx, vy):
        x = F(X)
        while True:
            nx = floor(x) + 1 if vx > 0 else ceil(x) - 1
            tx = (nx - x) / vx
            ty = None
            if vy:
                ny = floor(y) + 1 if vy > 0 else ceil(y) - 1
                ty = (ny - y) / vy
            if ty is not None and ty < tx:
                x, y = x + vx * ty, y + vy * ty
                row = int(y) if vy > 0 else int(y) - 1
                if (floor(x), row) not in cells:
                    vy = -vy
                continue
            assert ty is None or ty != tx
            x, y = x + vx * tx, y + vy * tx
            col = int(x) if vx > 0 else int(x) - 1
            if (col, floor(y)) not in cells:
                vx = -vx
            return (int(x), y, vx, vy)

    for s in states:
        if s in index:
            continue
        cur = s
        while True:
            index[cur] = orbits
            cur = step(*cur)
            if cur == s:
                break
            assert cur not in index
        orbits += 1

    def tau(st):
        X, y, vx, vy = st
        n = floor(y)
        if ((X - 1, n) in cells) and ((X, n) in cells):
            return (X, y, -vx, -vy)
        return (X, y, vx, -vy)

    image = {}
    for st, o in index.items():
        image.setdefault(o, set()).add(index[tau(st)])
    assert all(len(v) == 1 for v in image.values())
    fixed = sum(1 for o, v in image.items() if v == {o})
    return orbits, (orbits - fixed) // 2, fixed


def dirs(R):
    out = []
    for p in range(1, R + 1):
        for q in range(-R, R + 1):
            if gcd(p, q) == 1:
                out.append((p, q))
    return out


def transpose(cells):
    return {(y, x) for x, y in cells}


if __name__ == '__main__':
    t0 = time.process_time()
    R22 = {(x, y) for y, xs in {2: [1, 2], 1: [0, 1, 2, 3], 0: [-1, 0, 3, 4], -1: [-1, 0], -2: [0, 1], -3: [1]}.items() for x in xs}
    DBas = rect(0, 5, 0, 4) | rect(5, 9, 1, 2) | rect(9, 13, -1, 5)
    U2 = rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7)

    print('== parity counts mu in order (00,10,01,11), level sums (L=0, L=1)')
    for name, c in [('R22', R22), ('DBas', DBas), ('U2', U2)] + [(f'cross b={b}', cross(b)) for b in (3, 5, 7, 9, 11, 21)]:
        cv, rf = corners(c)
        m = mu(c)
        print(f'{name}: walls {len(cv)+len(rf)} r {len(rf)} mu {m} sum {sum(m)} levels {level_sums(m)}')

    print('\n== controls: half-offset leaf census (N, tau-swapped pairs, tau-fixed leaves)')
    for name, c, d in [('R22', R22, (4, 7)), ('R22', R22, (7, 4)), ('DBas', DBas, (-4, 1)), ('U2', U2, (-1, 1))]:
        p, q = d
        if p < 0:
            p, q = -p, -q
        print(f'{name} {d}: {leaf_census(c, p, q)}')

    print('\n== cross sweep: directions p in 1..R, |q| <= R, plus axis (0,1) via transpose')
    for b, R in ((7, 10), (9, 8)):
        c = cross(b)
        hist = {}
        bad = []
        for p, q in dirs(R) + [('T', None)]:
            if p == 'T':
                res = leaf_census(transpose(c), 1, 0)
                key = '(0,1)'
            else:
                res = leaf_census(c, p, q)
                key = (p, q)
            N, sw, fx = res
            hist[N] = hist.get(N, 0) + 1
            if N == 2 and sw == 1:
                bad.append(key)
            if N <= 2:
                print(f'  b={b} {key}: N={N} swapped={sw} fixed={fx}')
        print(f'  b={b}: {len(dirs(R)) + 1} directions; N histogram {dict(sorted(hist.items()))}; '
              f'directions with N=2 swapped: {bad}')

    print('\n== path (6,0) -> (4,-2) -> (-2,4) -> (0,6)')
    for b in range(7, 41, 2):
        c = cross(b)
        r = run(c, (0, 0) if False else (6, 0), (-1, -1), 10)
        h = run(c, (6, 0), (-1, -1), 5)
        ok = r['ok'] and r['end'] == (F(0), F(6))
        mid = h['end']
        assert ok and mid == (F(1), F(1)) and incid(c, (1, 1)) == 4, (b, r, h)
        assert [p for _, p, _ in r['contacts']] == [(4, -2), (-2, 4)]
    print('  legal for b = 7..39 odd; contacts (4,-2), (-2,4); midpoint (1,1), interior, class (1,1)')
    print('  (3,3) inside room:', any((3 - i, 3 - j) in cross(7) for i in (0, 1) for j in (0, 1)))
    print(f'cpu {time.process_time() - t0:.1f}s')
