"""d153: independent checks of parity-shortening.2026-11-22-0320.md.

Own room builder and own exact tracer (Fractions, continuous ray, no import of cyl.py).
Named rooms only: the three-chamber row R(X,Y, m) at the listed lengths. No searches.
Run: python3 -B checks.py
"""
from fractions import Fraction as F
from itertools import product
from math import gcd


def room(X, Y, m=1):
    """Cells of the m-dilated three-chamber row: 3x3 chambers at x=0, 3+X, 6+X+Y,
    unit corridors over 1<y<2."""
    cells = set()
    for a in (0, 3 + X, 6 + X + Y):
        cells |= {(x, y) for x in range(a, a + 3) for y in range(3)}
    cells |= {(x, 1) for x in range(9 + X + Y)}
    return {(m * x + i, m * y + j) for x, y in cells for i in range(m) for j in range(m)}


def incid(cells, p):
    x, y = p
    return sum((x + dx, y + dy) in cells for dx, dy in product((-1, 0), repeat=2))


def walls(cells):
    """Trace the boundary; return (#boundary components, #vertices, strictly simple?)."""
    pts = {(x + dx, y + dy) for x, y in cells for dx, dy in product((0, 1), repeat=2)}
    pinch = [p for p in pts if incid(cells, p) == 2 and
             ((p[0] - 1, p[1] - 1) in cells) == ((p[0], p[1]) in cells)]
    # directed boundary unit edges with the room on the left
    E = {}
    for x, y in cells:
        if (x, y - 1) not in cells: E[(x, y)] = (x + 1, y)
        if (x + 1, y) not in cells: E[(x + 1, y)] = (x + 1, y + 1)
        if (x, y + 1) not in cells: E[(x + 1, y + 1)] = (x, y + 1)
        if (x - 1, y) not in cells: E[(x, y + 1)] = (x, y)
    comps, seen, verts = 0, set(), 0
    for s in E:
        if s in seen: continue
        comps += 1
        p = s
        while p not in seen:
            seen.add(p); p = E[p]
    verts = sum(incid(cells, p) in (1, 3) for p in pts)
    return comps, verts, not pinch


def trace(cells, S, v, T, maxev=10**6):
    """Exact billiard from S with velocity v. Returns (outcome, #reflections).
    Outcome: 'target' if the ray passes T, 'corner' at a vertex, 'repeat' if a
    (position, velocity) state at a crossing recurs."""
    x, y = F(S[0]), F(S[1]); vx, vy = v
    seen, refl = set(), 0
    for _ in range(maxev):
        # time to next integer vertical / horizontal line
        nx = (x // 1 + 1 if vx > 0 else -((-x) // 1) - 1) if x.denominator == 1 else (x // 1 + (vx > 0))
        ny = (y // 1 + 1 if vy > 0 else -((-y) // 1) - 1) if y.denominator == 1 else (y // 1 + (vy > 0))
        tx, ty = (nx - x) / vx, (ny - y) / vy
        t = min(tx, ty)
        x, y = x + t * vx, y + t * vy
        cx = x.denominator == 1 and tx == t
        cy = y.denominator == 1 and ty == t
        # cell the ray occupies just before the crossing, and the targets beyond
        i = int(x - (vx > 0)) if cx else int(x // 1)
        j = int(y - (vy > 0)) if cy else int(y // 1)
        sx, sy = (1 if vx > 0 else -1), (1 if vy > 0 else -1)
        if cx and cy:
            p = (int(x), int(y))
            if p == T: return 'target', refl
            k = incid(cells, p)
            if k in (1, 3): return 'corner', refl
            if k == 2:
                if (i + sx, j) not in cells: vx = -vx
                if (i, j + sy) not in cells: vy = -vy
                refl += 1
        elif cx:
            if (i + sx, j) not in cells: vx = -vx; refl += 1
        else:
            if (i, j + sy) not in cells: vy = -vy; refl += 1
        st = (x, y, vx, vy)
        if st in seen: return 'repeat', refl
        seen.add(st)
    raise RuntimeError('event cap')


SIGNS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def line_outcomes(X, Y, m=1, d=(2, 1)):
    c = room(X, Y, m)
    S, T = (2 * m, 1 * m), ((4 + X) * m, 1 * m)
    return [trace(c, S, (sx * d[0], sy * d[1]), T)[0] for sx, sy in SIGNS]


def corridor_exit(L, y0, vy):
    """Exit (height, vertical sign) after a full traversal of a width-1 corridor of
    length L with |v|=(2,1), entering at height y0 in (0,1): unfolded phase on the
    doubled height circle of length 2."""
    ph = (F(y0) + vy * F(L, 2)) % 2
    return (ph, vy) if ph <= 1 else (2 - ph, -vy)


def site_counts(cells):
    pts = {(x + dx, y + dy) for x, y in cells for dx, dy in product((0, 1), repeat=2)}
    out = {}
    for s in product((0, 1), repeat=2):
        cnt = {k: 0 for k in (1, 2, 3, 4)}
        for p in pts:
            if (p[0] % 2, p[1] % 2) == s: cnt[incid(cells, p)] += 1
        n = sum(k * c for k, c in cnt.items())
        f, r = cnt[1], cnt[3]
        out[s] = dict(n=n, f=f, r=r, q=(n - f - 3 * r) // 2, e2=cnt[2], e4=cnt[4])
    return out


def main():
    print('== 1. Wall count, simplicity, gcds, area')
    for X, Y in [(4, 4), (2, 4), (28, 28), (26, 28)]:
        c = room(X, Y)
        comps, W, simple = walls(c)
        print(f'X={X} Y={Y}: components={comps} W={W} strictly_simple={simple} '
              f'area={len(c)} hgcd={gcd(gcd(3, X), Y)}')
        assert comps == 1 and W == 20 and simple

    print('== 1. Fixed line (2,1), four launch signs --, -+, +-, ++')
    want = {(4, 4): ['corner', 'repeat', 'repeat', 'corner'],
            (2, 4): ['corner', 'repeat', 'repeat', 'target'],
            (28, 28): ['corner', 'repeat', 'repeat', 'corner'],
            (26, 28): ['corner', 'repeat', 'repeat', 'target']}
    for (X, Y), w in want.items():
        o = line_outcomes(X, Y)
        print(f'X={X} Y={Y} S=(2,1) T=({4+X},1): {o}  matches note: {o == w}')
        assert o == w
    print('mark parities: S=(2,1) fixed; T x-parity (4+X)%2 at X=28,26:', (32 % 2, 30 % 2))

    print('== 2. Corridor exit height/sign vs inserted length (|v|=(2,1), w=1)')
    for y0, v in [(F(1, 2), 1), (F(1, 4), -1), (F(3, 4), 1)]:
        base = corridor_exit(10, y0, v)
        row = {d: corridor_exit(10 + d, y0, v) == base for d in (1, 2, 3, 4, 6, 8, 12)}
        print(f'entry y={y0} vy={v}: restored after insertion d -> {row}')
    print('formula T(p,q)=2w|p|/gcd(|q|,2w|p|) with p=2,q=1,w=1:', 2 * 1 * 2 // gcd(1, 4))
    print('room-level replay at period 4 and 12 (outcome tuples):')
    for X, Y in [(8, 8), (6, 8), (16, 16), (14, 16), (4, 8), (2, 8), (40, 40), (38, 40),
                 (28, 32), (26, 32)]:
        print(f'  X={X} Y={Y}: {line_outcomes(X, Y)}  hgcd={gcd(gcd(3, X), Y)}')
    print('2 is not a period: X=Y=6 (vs X=Y=4 above) ->', line_outcomes(6, 6))

    print('== 1/5. One-reflection shot of slope 2/(X+2) (direction (X/2+1, 1))')
    for X, Y in [(4, 4), (2, 4), (28, 28), (26, 28)]:
        c = room(X, Y)
        d = ((X + 2) // 2, 1)
        print(f'X={X} Y={Y} dir={d}:', trace(c, (2, 1), d, (4 + X, 1)))
        assert trace(c, (2, 1), d, (4 + X, 1)) == ('target', 1)

    print('== 3. Site counts n = f + 2q + 3r (q := e2 + 2 e4)')
    a, b = site_counts(room(28, 28)), site_counts(room(26, 28))
    for s in a:
        print(f'site {s}: long {a[s]}  short {b[s]}  dq={a[s]["q"]-b[s]["q"]} '
              f'de2={a[s]["e2"]-b[s]["e2"]} de4={a[s]["e4"]-b[s]["e4"]}')
        assert a[s]['f'] == b[s]['f'] and a[s]['r'] == b[s]['r']
        assert a[s]['q'] - b[s]['q'] == 1 and a[s]['n'] - b[s]['n'] == 2

    print('== 4. Dilation sanity: m=2 room, marks and direction scaled')
    for X, Y in [(4, 4), (2, 4)]:
        print(f'X={X} Y={Y} m=2: {line_outcomes(X, Y, m=2)}  m=1: {line_outcomes(X, Y)}')
        assert line_outcomes(X, Y, m=2) == line_outcomes(X, Y)
    print('done')


if __name__ == '__main__':
    main()
