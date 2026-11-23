"""D107: independent replay of one bin-pair (pixel_finish) room's receipts.

Usage: python3 -B pixchk.py ROOMDIR QUERIES_OUT NEAR_HARD_OUT [--mutate]

Written from qclass-closure/twenty/method.md ("The 12-square room ...") and the receipt grammar.
It doesn't import or run census code. Per bin pair `I i j u v` (bins 16 x 16, u = 16*xbin + ybin):
  S k            bisect coordinate k (x0, y0, x1, y1 in units 1/65536 of the tile)
  L sw j p q     fixed direction pulled back by shear power j; written as a label query for labchk
  V ex ey tx ty  explicit reflected path; checked here over the whole box (multilinear
                 orientation determinant at the 16 box vertices, both orders at ties with a
                 non-corner physical vertex, every branch must end at the target sheet)
  N k0 k1        both ends within 1/64 of tile corners k0, k1; needs a near/ shear box
  P sw var h0 h1 rational reference heights; derives the sign and dominance cases and the phase
                 root rectangle itself, then replays the K / E / B phase tree, writing K leaves
                 as label queries
Also checks that the I keys are distinct and equal the grid's PIX set, and that the N
neighborhoods equal near/boxes. It writes a synthetic hard directory for D103's shear_check.py.
--mutate adds 1 to j in every L and K leaf (negative control).
"""
import gzip, sys
from fractions import Fraction as Fr
from itertools import product
from math import lcm
from pathlib import Path
from collections import Counter

U = 65536
d = Path(sys.argv[1]); qout = open(sys.argv[2], 'w'); nearout = Path(sys.argv[3]); mutate = '--mutate' in sys.argv
raw = list(map(int, (d / 'room').read_text().split()))
cells = list(zip(raw[2::2], raw[3::2])); C = set(cells)
cnt = Counter()


def period(cs):
    w = []
    for x, y in cs:
        if (x - 1, y) not in cs:
            z = x + 1
            while (z, y) in cs:
                z += 1
            w.append(2 * (z - x))
    return lcm(*w)


orient = [cells, [(y, x) for x, y in cells]]
Ls = [period(set(o)) for o in orient]
for sw in (0, 1):
    print(f'ROOM {sw} {Ls[sw]} {len(cells)} ' + ' '.join(f'{x} {y}' for x, y in orient[sw]), file=qout)


def emit(ids, sw, z, j, p, q, phase=None, sgn=None, tag=''):
    """Strip coordinate u = q*x - sg*p*y' - sg*q*j*s_e*phase_e (+ base), y' = y (sg=+1) or U - y (sg=-1).
    In the fixed case the y coefficient is p + j*q*L instead and there is no phase term."""
    if mutate:
        j += 1
    out = []
    for e in (0, 1):
        x = z[2 * e + sw]; y = z[2 * e + 1 - sw]
        for sg in (1, -1):
            terms = [(q, x)]
            if phase is None:
                terms.append((-sg * (p + j * q * Ls[sw]), y))
            else:
                terms.append((-sg * p, y)); terms.append((-sg * q * j * sgn[e], phase[e]))
            base = 0 if sg == 1 else -p * U
            lo = base + sum(min(k * a, k * b) for k, (a, b) in terms)
            hi = base + sum(max(k * a, k * b) for k, (a, b) in terms)
            out += [lo, hi]
    assert max(abs(v) for v in out) < 4 * 10 ** 18
    print(f'Q {sw} {ids[0]} {ids[1]} {p} {q} ' + ' '.join(map(str, out)) + f' {tag}', file=qout)
    cnt['queries'] += 1


def occ(X, Y):
    return [(X - i, Y - j) in C for i in (0, 1) for j in (0, 1)]


def noncorner(X, Y):  # regular interior vertex, or a straight-wall vertex (two edge-adjacent cells)
    o = occ(X, Y); k = sum(o)
    if k == 4:
        return True
    if k == 2:  # o order: (X,Y),(X,Y-1),(X-1,Y),(X-1,Y-1); diagonal pairs are pinches
        return not ((o[0] and o[3]) or (o[1] and o[2]))
    return False


def ray(ids, z, ex, ey, tx, ty):
    assert ex in (1, -1) and ey in (1, -1) and tx % 2 == 0 and ty % 2 == 0
    (a, b), (c, f) = cells[ids[0]], cells[ids[1]]
    Sx = [a * U + z[0][0], a * U + z[0][1]]; Sy = [b * U + z[1][0], b * U + z[1][1]]
    Px = sorted(ex * (c * U + w) + tx * U for w in z[2]); Py = sorted(ey * (f * U + w) + ty * U for w in z[3])
    ax = ex * c + tx - (ex < 0); ay = ey * f + ty - (ey < 0)
    assert ax * U <= Px[0] and Px[1] <= (ax + 1) * U and ay * U <= Py[0] and Py[1] <= (ay + 1) * U

    def shares_int(r1, r2):
        lo, hi = max(r1[0], r2[0]), min(r1[1], r2[1])
        return lo <= hi and -(-lo // U) <= hi // U
    # a segment that could run along a grid line while crossing lines of the other family is refused
    if (ay != b and shares_int(Sx, Px)) or (ax != a and shares_int(Sy, Py)):
        return False
    dx = (ax > a) - (ax < a); dy = (ay > b) - (ay < b)
    verts = list(product(Sx, Sy, Px, Py))
    states = {(a, b, a, b, 1, 1)}  # developed cell, physical cell, orientation
    for _ in range(abs(ax - a) + abs(ay - b)):
        nxt = set()
        for x, y, h, k, fx, fy in states:
            vx, vy = x != ax, y != ay
            if vx and vy:
                X = (x + (dx > 0)) * U; Y = (y + (dy > 0)) * U
                # D = (X-Sx)(Py-Sy) - (Y-Sy)(Px-Sx); dx*dy*D < 0 iff the vertical line comes first
                vals = [dx * dy * ((X - sx) * (py - sy) - (Y - sy) * (px - sx)) for sx, sy, px, py in verts]
                vx, vy = min(vals) <= 0, max(vals) >= 0
                if vx and vy and not noncorner(h + (dx * fx > 0), k + (dy * fy > 0)):
                    return False
            if vx:
                nh = h + fx * dx
                nxt.add((x + dx, y, nh, k, fx, fy) if (nh, k) in C else (x + dx, y, h, k, -fx, fy))
            if vy:
                nk = k + fy * dy
                nxt.add((x, y + dy, h, nk, fx, fy) if (h, nk) in C else (x, y + dy, h, k, fx, -fy))
        states = nxt
    return states == {(ax, ay, c, f, ex, ey)}


needed = set(); seen = set(); vfail = []


def replay(ids, tok, tag):
    def visit(z):
        t = next(tok).split(); kind = t[0]; v = list(map(int, t[1:])); cnt[kind] += 1
        if kind == 'S':
            i, = v; l, r = z[i]; m = (l + r) // 2; assert l < m < r
            visit(z[:i] + [(l, m)] + z[i + 1:]); visit(z[:i] + [(m, r)] + z[i + 1:])
        elif kind == 'L':
            sw, j, p, q = v; emit(ids, sw, z, j, p, q, tag=tag)
        elif kind == 'V':
            if not ray(ids, z, *v):
                vfail.append((tag, z, v))
        elif kind == 'N':
            for e, k in enumerate(v):
                for ax in (0, 1):
                    l, r = z[2 * e + ax]
                    assert (l >= U - 1024) if (k >> ax) & 1 else (r <= 1024), (tag, z, v)
            needed.add((*ids, *v, 1024))
        else:
            assert kind == 'P', kind
            sw, var, n0, d0, n1, d1 = v
            h = [Fr(n0, d0), Fr(n1, d1)]
            assert var in (0, 1) and all(0 <= x <= 1 for x in h)
            if var == 0:
                assert all(x in (0, 1) for x in h)
            M = Ls[sw] * lcm(h[0].denominator, h[1].denominator)
            delta = []  # signed transverse displacement range y - h*U at each end
            for e in (0, 1):
                l, r = z[2 * e + 1 - sw]
                delta.append((l - h[e] * U, r - h[e] * U))
            # A > 0: some end's box misses its reference height, or a reference on a tile
            # side that is a physical wall (an interior point can't sit there)
            pos = any(l > 0 or r < 0 for l, r in delta)
            for e in (0, 1):
                if h[e] in (0, 1):
                    x, y = cells[ids[e]]; w = 1 if h[e] == 1 else -1
                    nb = (x + w, y) if sw else (x, y + w)
                    pos |= nb not in C
            assert pos, (tag, 'A may vanish')
            signs = list(product((1, -1), repeat=2)) if var else [tuple(1 if x == 0 else -1 for x in h)]
            for sgn in signs:
                sc = [sorted((sgn[e] * delta[e][0] * M, sgn[e] * delta[e][1] * M)) for e in (0, 1)]
                if any(hi < 0 for lo, hi in sc):
                    continue  # no point of the box has this sign at that end
                rng = [(max(0, lo), hi) for lo, hi in sc]  # possible K=1 phases M*|y-h|
                for dom in (0, 1):
                    if rng[dom][1] < rng[1 - dom][0]:
                        continue  # dom can't hold the larger displacement
                    top = max(Fr(U, 4), Fr(rng[dom][1])); assert top.denominator == 1; top = int(top)

                    def phased(t, u):
                        row = next(tok).split(); k = row[0]; cnt[k] += 1
                        if k == 'E':
                            assert u[0] > t[1]  # the other phase can't exceed the dominant one
                        elif k == 'K':
                            ph = [None, None]; ph[dom] = t; ph[1 - dom] = u
                            emit(ids, sw, z, *map(int, row[1:]), phase=ph, sgn=sgn, tag=tag)
                        else:
                            assert k == 'B'; st = int(row[1]); l, r = t if st else u; m = (l + r) // 2; assert l < m < r
                            for w in ((l, m), (m, r)):
                                phased(w if st else t, u if st else w)
                    # dominant phase K*M*A lies in [U/8, U/4] when K > 1, in [U/8, M*A] when K = 1
                    phased((U // 8, top), (0, top))
    return visit


for f in sorted((d / 'pixel').glob('receipts?.gz')):
    with gzip.open(f, 'rt') as tok:
        for l in tok:
            if l.startswith(('NEAR ', 'TOTAL ')):
                continue
            tag, i, j, u, v = l.split(); assert tag == 'I'
            key = tuple(map(int, (i, j, u, v))); assert key not in seen; seen.add(key)
            ids = key[:2]; bx = [divmod(key[2], 16), divmod(key[3], 16)]
            z = [(k * U // 16, (k + 1) * U // 16) for k in (bx[0][0], bx[0][1], bx[1][0], bx[1][1])]
            replay(ids, tok, f'{d.name}/{i}_{j}_{u}_{v}')(z)
pix = {tuple(map(int, l.split()[1:])) for l in (d / 'pixel' / 'grid').open() if l.startswith('PIX ')}
near = {tuple(map(int, l.split())) for l in (d / 'pixel' / 'near' / 'boxes').read_text().splitlines()}
print(f'{d.name}: bin pairs {len(seen)}, equal to grid PIX set {seen == pix}; near boxes {len(needed)}, '
      f'equal to near/boxes {needed == near}; explicit-path failures {len(vfail)} of {cnt["V"]}; {dict(cnt)}')
for x in vfail[:5]:
    print('  VFAIL', x)
# synthetic hard directory for D103's shear_check.py: room, boxes, tiles (BOX lines), shears/
nearout.mkdir(parents=True, exist_ok=True)
if needed:
    (nearout / 'room').write_text((d / 'room').read_text())
    (nearout / 'boxes').write_text(''.join(' '.join(map(str, b)) + '\n' for b in sorted(needed)))
    (nearout / 'tiles').write_text(''.join('BOX 0 ' + ' '.join(map(str, b)) + '\n' for b in sorted(needed)))
    sh = nearout / 'shears'
    if not sh.exists():
        sh.symlink_to((d / 'pixel' / 'near' / 'shears').resolve())
