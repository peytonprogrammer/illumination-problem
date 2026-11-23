"""D77 referee checks for chain-criteria.md and reversal.md.

Own code. Exact Fraction arithmetic throughout. Reads only covers.json (cov2929 cells) and
cyl_H40.json (saved directions). No search over rooms, rays, directions or reflection words:
every path below is built by the construction stated in the reviewed proofs, then traced.
Run: python3 -B verify.py > verify.log
"""
import json
import sys
import time
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, floor, ceil
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
T0 = time.process_time()


# ------------------------------------------------------------------ polygon tracer
class Room:
    """Rectilinear polygon given by maximal walls (axis-aligned segments) and corners."""

    def __init__(self, walls):
        self.walls = walls  # list of ('v', x, y0, y1) or ('h', y, x0, x1)
        self.corners = set()
        for o, c, a, b in walls:
            for e in (a, b):
                self.corners.add((c, e) if o == 'v' else (e, c))

    @classmethod
    def from_vertices(cls, vs):
        vs = [(F(x), F(y)) for x, y in vs]
        walls = []
        for (x0, y0), (x1, y1) in zip(vs, vs[1:] + vs[:1]):
            if x0 == x1:
                walls.append(('v', x0, min(y0, y1), max(y0, y1)))
            else:
                assert y0 == y1
                walls.append(('h', y0, min(x0, x1), max(x0, x1)))
        return cls(walls)

    @classmethod
    def from_cells(cls, cells):
        """Merge unit boundary edges into maximal walls; merge only across smooth points."""
        unit = {}
        for (cx, cy) in cells:
            for o, c, a, side, nb in (('v', cx, cy, +1, (cx - 1, cy)), ('v', cx + 1, cy, -1, (cx + 1, cy)),
                                      ('h', cy, cx, +1, (cx, cy - 1)), ('h', cy + 1, cx, -1, (cx, cy + 1))):
                if nb not in cells:
                    unit[(o, c, a)] = side
        walls = []
        for (o, c, a), side in sorted(unit.items()):
            if (o, c, a - 1) in unit and unit[(o, c, a - 1)] == side:
                continue  # not a run start
            b = a
            while (o, c, b + 1) in unit and unit[(o, c, b + 1)] == side:
                b += 1
            walls.append((o, F(c), F(a), F(b + 1)))
        return cls(walls)

    def trace(self, P, V, T, cap=200000):
        """Trace from P with velocity V until T. Returns (ok, contacts, reason)."""
        px, py = F(P[0]), F(P[1])
        vx, vy = F(V[0]), F(V[1])
        tx, ty = F(T[0]), F(T[1])
        contacts = []
        for _ in range(cap):
            best, hit = None, None
            for o, c, a, b in self.walls:
                if o == 'v' and vx:
                    t = (c - px) / vx
                    if t > 0:
                        y = py + t * vy
                        if a <= y <= b and (best is None or t < best):
                            best, hit = t, (o, c, y, a, b)
                elif o == 'h' and vy:
                    t = (c - py) / vy
                    if t > 0:
                        x = px + t * vx
                        if a <= x <= b and (best is None or t < best):
                            best, hit = t, (o, c, x, a, b)
            if best is None:
                return False, contacts, 'escaped'
            # target on the open segment before the hit?
            dx, dy = tx - px, ty - py
            if dx * vy == dy * vx:
                t = dx / vx if vx else dy / vy
                if 0 < t <= best:
                    if t == best:
                        return False, contacts, 'target on wall'
                    return True, contacts, 'hit T'
            o, c, e, a, b = hit
            if e == a or e == b:
                return False, contacts, 'corner %s' % ((c, e) if o == 'v' else (e, c),)
            # a hit on a wall line exactly at a corner of another wall is caught above via its endpoint
            if o == 'v':
                px, py = c, e
                vx = -vx
                contacts.append(('v', px, py))
            else:
                px, py = e, c
                vy = -vy
                contacts.append(('h', px, py))
        return False, contacts, 'cap'


def interior_points(cells):
    pts = set()
    for (cx, cy) in cells:
        for dx, dy in product((0, 1), repeat=2):
            p = (cx + dx, cy + dy)
            if all((p[0] + ex, p[1] + ey) in cells for ex, ey in product((-1, 0), repeat=2)):
                pts.add(p)
    return sorted(pts)


def rect(x0, x1, y0, y1):
    return {(i, j) for i in range(x0, x1) for j in range(y0, y1)}


# ------------------------------------------------------------------ DBw2 family
def dbw2(l):
    vs = [(0, 0), (5, 0), (5, 1), (5 + l, 1), (5 + l, 0), (10 + l, 0), (10 + l, 6), (5 + l, 6),
          (5 + l, 3), (5, 3), (5, 5), (0, 5)]
    return Room.from_vertices(vs)


def frac_dist_to_multiple(z, g):
    r = z - g * floor(z / g)
    return min(r, g - r)


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    q, r = divmod(a, b)
    g, x, y = egcd(b, r)
    return g, y, x - q * y


def lr_path(S, T, l, use_g=True):
    """Constructive three-column proof (chain-criteria section 'Three columns').
    Returns slope s or (None, reason). Left P=10, corridor Q=4 (bottom 1), right R=12."""
    P, Q, R = 10, 4, 12
    u = v = F(2)
    ci = cj = F(2)
    a = 5 - S[0]
    b = T[0] - (5 + l)
    Sy, Ty = F(S[1]), F(T[1])
    g = gcd(b * P, a * R)
    target = b * ci + a * cj - b * Sy - a * Ty
    k = round(target / g)
    N0 = b * Sy + a * Ty + g * k            # nearest lattice value of b x + a y
    e = abs(target - g * k)
    assert e == frac_dist_to_multiple(target, g)
    twoE = F(g) if use_g else 2 * e
    delta = min(u / a, v / b, (b * u + a * v - twoE) / (2 * a * b))
    if delta <= 0:
        return None, 'incompatible', delta
    if (a + l + b) * delta <= Q:
        return None, 'length test fails', delta
    # pick delta' just below delta with (a+l+b) delta' > Q
    dp = (delta + F(Q, a + l + b)) / 2
    assert 0 < dp < delta and (a + l + b) * dp > Q
    # eroded windows: x in (ci - (u - a dp)/2, ci + ...), y similarly; need b x + a y = N0
    hx, hy = (u - a * dp) / 2, (v - b * dp) / 2
    D0 = N0 - b * ci - a * cj
    assert abs(D0) < b * hx + a * hy
    th = (b * hx) / (b * hx + a * hy)
    x = ci + D0 * th / b
    y = cj + D0 * (1 - th) / a
    assert abs(x - ci) < hx and abs(y - cj) < hy and b * x + a * y == N0
    # integers m, n with b P m + a R n = N0 - b S - a T = g k
    gg, p0, q0 = egcd(b * P, a * R)
    m, n = -p0 * k, q0 * k
    # shift m to keep |s| small (lattice direction (aR/g, -bP/g))
    step = a * R // g
    # x = S + a s - P m, y = T - b s + R n  =>  b x + a y = bS + aT - bPm + aRn
    sc = lambda mm: (x - Sy + P * mm) / a
    m = m - step * round(sc(m) * a / (P * step))
    n = (N0 - b * Sy - a * Ty + b * P * m) // (a * R)
    assert -b * P * m + a * R * n == N0 - b * Sy - a * Ty
    s_c = sc(m)
    assert (Sy + a * s_c - x) % P == 0 and (Ty - b * s_c - y) % R == 0
    # mismatch F(s) = x(s) + l s - y(s), slope a+l+b; nearest multiple of Q
    Fc = x + l * s_c - y
    jj = round(Fc / Q)
    s = s_c + (Q * jj - Fc) / (a + l + b)
    assert abs(s - s_c) <= dp / 2
    return s, 'ok', delta


def mouth_path(S, c, side, l):
    """Chamber mark S to corridor target at depth c>0 from its mouth (chain-criteria last para)."""
    if side == 'L':
        a = 5 - S[0]
        mx = 5
    else:
        a = S[0] - (5 + l)
        mx = 5 + l
    ys = F(S[1])
    # crossing height of segment from S to image (., 2+2k): ys + (2+2k-ys) a/(a+c); pick k nearest 2
    k = round(((2 - ys) * (a + c) / a + ys - 2) / 2)
    cross = ys + (2 + 2 * k - ys) * F(a, a + c)
    for dk in (0, 1, -1):
        cr = ys + (2 + 2 * (k + dk) - ys) * F(a, a + c)
        if 1 < cr < 3:
            k, cross = k + dk, cr
            break
    else:
        return None
    dy = 2 + 2 * k - ys
    return ((a + c) if side == 'L' else -(a + c), dy)


def dbw2_check(l, out):
    cells = rect(0, 5, 0, 5) | rect(5, 5 + l, 1, 3) | rect(5 + l, 10 + l, 0, 6)
    room = dbw2(l)
    pts = interior_points(cells)
    left = [p for p in pts if p[0] < 5]
    right = [p for p in pts if p[0] > 5 + l]
    corr = [p for p in pts if 5 <= p[0] <= 5 + l]
    assert len(left) == 16 and len(right) == 20 and len(corr) == l + 1
    assert all(p[1] == 2 for p in corr)
    stats = {'L-R': 0, 'chamber-corridor': 0, 'direct': 0, 'fail': [], 'max_refl': 0}

    def zone(p):
        return 'L' if p[0] < 5 else ('R' if p[0] > 5 + l else 'C')
    for S, T in combinations(pts, 2):
        zs, zt = zone(S), zone(T)
        if {zs, zt} == {'L', 'R'}:
            A, B = (S, T) if zs == 'L' else (T, S)
            s, why, _ = lr_path(A, B, l)
            if s is None:
                stats['fail'].append((S, T, why))
                continue
            ok, con, r = room.trace(A, (1, s), B)
            kind = 'L-R'
            P0, P1 = A, B
        elif zs == zt or (zs == 'C' and zt == 'C'):
            ok, con, r = room.trace(S, (T[0] - S[0], T[1] - S[1]), T)
            kind = 'direct'
        else:
            M, C = (S, T) if zt == 'C' else (T, S)
            side = zone(M)
            depth = C[0] - 5 if side == 'L' else 5 + l - C[0]
            if depth == 0:
                ok, con, r = room.trace(M, (C[0] - M[0], C[1] - M[1]), C)
                kind = 'direct'
            else:
                V = mouth_path(M, depth, side, l)
                if V is None:
                    stats['fail'].append((S, T, 'no k'))
                    continue
                ok, con, r = room.trace(M, V, C)
                kind = 'chamber-corridor'
        if ok:
            stats[kind] += 1
            stats['max_refl'] = max(stats['max_refl'], len(con))
        else:
            stats['fail'].append((S, T, r))
    npairs = len(pts) * (len(pts) - 1) // 2
    # same-class count for the original length (sanity against D72's 190)
    same = sum(1 for S, T in combinations(pts, 2) if (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0)
    print('DBw2 l=%d: %d interior points (16 L, 20 R, %d on y=2), %d pairs, same-class %d; '
          'L-R traced %d, chamber-corridor traced %d, direct %d, failures %d, max reflections %d'
          % (l, len(pts), len(corr), npairs, same, stats['L-R'], stats['chamber-corridor'],
             stats['direct'], len(stats['fail']), stats['max_refl']))
    for f in stats['fail'][:10]:
        print('   FAIL', f)
    out['DBw2_%d' % l] = {'points': len(pts), 'pairs': npairs, 'failures': len(stats['fail'])}
    return len(stats['fail'])


def dbw2_table():
    print('\nDBw2 delta lower bounds with g = gcd(10b,12a) (rows a, cols b); 4/delta - a - b:')
    worst = (None, None)
    for a in range(1, 5):
        row = []
        for b in range(1, 5):
            g = gcd(10 * b, 12 * a)
            d = min(F(2, a), F(2, b), F(2 * a + 2 * b - g, 2 * a * b))
            row.append('%s(%s)' % (d, 4 / d - a - b))
            if worst[0] is None or 4 / d - a - b > worst[0]:
                worst = (4 / d - a - b, (a, b))
        print('  a=%d: %s' % (a, '  '.join(row)))
    print('  max 4/delta-a-b = %s at (a,b)=%s' % worst)


def short_lengths():
    print('\nDBw2 proof coverage at short lengths (L-R pairs, positive sheets):')
    for l in range(4, 12):
        fg, fe = [], []
        for sx, sy, tx, ty in product(range(1, 5), range(1, 5), range(1, 5), range(1, 6)):
            S, T = (sx, sy), (5 + l + tx, ty)
            if lr_path(S, T, l, True)[0] is None:
                fg.append((5 - sx, tx))
            if lr_path(S, T, l, False)[0] is None:
                fe.append((S, T))
        print('  l=%2d: g-test (endpoint-free) fails for %3d/320 pairs, (a,b) %s; exact-e test fails for %3d/320'
              % (l, len(fg), sorted(set(fg)), len(fe)))
        if fe and l >= 9:
            print('        e-test failures e.g.', fe[:4])


# ------------------------------------------------------------------ (a) lattice index check
def hnf_index_check():
    """Check h_i/(D h_{i-1}) against direct kernel spacing for one 3-column DBw2 instance."""
    from fractions import Fraction as Fr
    print('\n(a) index formula: one DBw2 instance l=11, S=(1,1), T=(19,3); travels 4, 11, 3')
    d = [4, 11, 3]
    Pp = [10, 4, 12]
    X = sum(d)
    A = [d[0], d[0] + d[1]]
    G = [[Fr(Pp[j]) * (Fr(A[i], X) - (1 if j <= i else 0)) for j in range(3)] for i in range(2)]
    Dn = 1
    for r in G:
        for z in r:
            Dn = Dn * z.denominator // gcd(Dn, z.denominator)
    M = [[int(z * Dn) for z in r] for r in G]
    h1 = 0
    for z in M[0]:
        h1 = gcd(h1, abs(z))
    h2 = 0
    for j, k in combinations(range(3), 2):
        h2 = gcd(h2, abs(M[0][j] * M[1][k] - M[0][k] * M[1][j]))
    # direct: second coordinates of lattice vectors with first coordinate 0, small box
    ker = 0
    rng = range(-40, 41)
    for m in product(rng, repeat=3):
        if sum(M[0][j] * m[j] for j in range(3)) == 0:
            ker = gcd(ker, abs(sum(M[1][j] * m[j] for j in range(3))))
    first = 0
    for m in product(range(-3, 4), repeat=3):
        first = gcd(first, abs(sum(M[0][j] * m[j] for j in range(3))))
    print('  D=%d, h1=%d (direct first-coordinate gcd %d), h2=%d, h2/h1=%s, direct kernel step %d (box |m|<=40)'
          % (Dn, h1, first, h2, F(h2, h1), ker))
    print('  spacings: seam1 %s, seam2 %s; both windows have width 2'
          % (F(h1, Dn), F(h2, h1 * Dn)))


# ------------------------------------------------------------------ DB55 reversal
def db55(l):
    vs = [(0, 0), (5, 0), (5, 2), (5 + l, 2), (5 + l, 0), (10 + l, 0), (10 + l, 5), (5 + l, 5),
          (5 + l, 3), (5, 3), (5, 5), (0, 5)]
    return Room.from_vertices(vs)


def db55_check(out):
    print('\nDB55 reversal: interval for t from x_left=5/2+4t, y_right=21/8-9t in (2,3)')
    lo = max(F(-1, 8), F(-1, 24))   # 4t in (-1/2,1/2); -9t in (-5/8,3/8)
    hi = min(F(1, 8), F(5, 72))
    print('  t in (%s, %s), width %s; mirror height 39/2-4t in [%s, %s]' % (lo, hi, hi - lo,
          F(39, 2) - 4 * hi, F(39, 2) - 4 * lo))
    # symbolic re-derivation at general l: developed heights from (1,1) with slope s
    s0 = F(-37, 8)
    xl = 1 + 4 * s0
    print('  1+4s0 = %s -> mod 10 = %s; target image backward 9: 1-9s0 = %s -> mod 10 = %s'
          % (xl, xl % 10, 1 - 9 * s0, (1 - 9 * s0) % 10))
    print('  l=3 placement at t=0: x_left + 3 s0 - y_right = %s' % (F(5, 2) + 3 * s0 - F(21, 8)))
    print('  threshold: (13+l)/9 > 2 iff l > 5')
    res = {}
    for l in [F(3), F(11, 2), F(6), F(63, 10), F(7), F(20), F(5), F(51, 10)]:
        room = db55(l)
        c0 = F(5, 2) + l * s0 - F(21, 8)
        slope = 13 + l
        # open image (c0 + slope*lo, c0 + slope*hi): choose even integer inside, nearest middle
        a, b = c0 + slope * lo, c0 + slope * hi
        evens = [2 * k for k in range(ceil(a / 2), floor(b / 2) + 1) if a < 2 * k < b]
        if not evens:
            print('  l=%s: open phase image (%s, %s) has no even integer: no path from this branch'
                  % (l, a, b))
            res[str(l)] = 'no even integer'
            continue
        mid = (a + b) / 2
        E = min(evens, key=lambda z: abs(z - mid))
        t = (E - c0) / slope
        s = s0 + t
        T = (6 + l, 1)
        ok, con, r = room.trace((1, 1), (1, s), T)
        vert = [c for c in con if c[0] == 'v']
        nh = len(con) - len(vert)
        vinfo = ', '.join('x=%s y=%s' % (c[1], c[2]) for c in vert)
        inside = all(0 < c[2] < 5 and c[1] == 10 + l for c in vert)
        print('  l=%s: t=%s, s=%s; traced: %s (%s); %d horizontal contacts, vertical: %s; strictly inside right wall: %s'
              % (l, t, s, ok, r, nh, vinfo, inside))
        res[str(l)] = ok and len(vert) == 1 and inside
    # contact list at l=3, t=0 (the reconstructed D69 witness)
    ok, con, r = db55(3).trace((1, 1), (1, s0), (9, 1))
    seg = {'left': [c for c in con if c[1] < 5 and c[0] == 'h'],
           'corr': [c for c in con if c[0] == 'h' and 5 < c[1] < 8]}
    v = [c for c in con if c[0] == 'v'][0]
    iv = con.index(v)
    before = [c for c in con[:iv] if c[1] > 8]
    after = con[iv + 1:]
    print('  l=3 witness s=-37/8: %s; left %d contacts (y=%s), corridor %d (first y=%s), right before %d (first y=%s), '
          'mirror at y=%s, right after %d (y=%s); total horizontal %d'
          % (ok, len(seg['left']), [str(c[2]) for c in seg['left']], len(seg['corr']), seg['corr'][0][2],
             len(before), before[0][2], v[2], len(after), [str(c[2]) for c in after], len(con) - 1))
    # corridor exit height
    lastc = seg['corr'][-1]
    exit_y = lastc[2] + (8 - lastc[1]) * (-1 if lastc[2] == 3 else 1) * F(37, 8)
    print('  corridor exit height at x=8: %s' % exit_y)
    out['DB55'] = res


# ------------------------------------------------------------------ cov2929
def cov2929_check(out):
    cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms'] if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))
    cells = set(map(tuple, cov[2929]['cells']))
    pic = {(x, y) for y, row in enumerate(['#.##....', '####....', '..####..', '..####..', '....####', '....##.#'])
           for x, ch in enumerate(row) if ch == '#'}
    print('\ncov2929: %d cells; matches D69 diagram: %s' % (len(cells), cells == pic))
    room = Room.from_cells(cells)
    print('  walls %d, corners %d' % (len(room.walls), len(room.corners)))
    saved = json.load(open(D / 'd72-cylinder-test' / 'cyl_H40.json'))['cov2929']['pairs']
    for S, T, V in [((3, 1), (5, 3), (-2, 3)), ((3, 3), (5, 5), (2, 3))]:
        rec = [p for p in saved if tuple(p['S']) == S and tuple(p['T']) == T][0]
        ok, con, r = room.trace(S, V, T)
        desc = []
        for o, x, y in con:
            note = ''
            if o == 'v':
                # wall piece containing the contact, strict interior?
                w = [w for w in room.walls if w[0] == 'v' and w[1] == x and w[2] <= y <= w[3]][0]
                note = ' [vertical wall x=%s, y in (%s,%s), strict %s]' % (x, w[2], w[3], w[2] < y < w[3])
            desc.append('(%s,%s)%s' % (x, y, note))
        print('  %s->%s V=%s (saved lit dir %s): %s %s; contacts %s' % (S, T, V, rec['lit'][0], ok, r, ', '.join(desc)))
        out['cov2929_%s_%s' % (S, T)] = ok


def main():
    out = {}
    hnf_index_check()
    dbw2_table()
    short_lengths()
    print()
    print('Sanity at the original length 4 (proof not claimed there; its L-R failures are expected):')
    dbw2_check(4, out)
    fails = 0
    for l in (11, 12, 13, 17, 25):
        fails += dbw2_check(l, out)
    db55_check(out)
    cov2929_check(out)
    print('\nDBw2 total failures over l = 11, 12, 13, 17, 25: %d' % fails)
    print('CPU %.1f s' % (time.process_time() - T0))


if __name__ == '__main__':
    main()
