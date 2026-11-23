"""D127 referee checks for thin-room.md (cov279 stretch, all same-parity pairs).

Exact arithmetic only (int and Fraction). Own room builder and own tracer.
Certificates are built from the note's formulas. No search over directions
or reflection words. Section E samples first-door acceptance only to test a
negative claim, not to find certificates.

Run: python3 -B checks.py > checks.log
"""
import subprocess
import sys
import time
from fractions import Fraction as Fr
from math import gcd
from itertools import combinations

T0 = time.process_time()


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- room

def cov279_polygon(q):
    """Vertex list (counterclockwise) of the normalized cov279 stretch."""
    return [(0, 0), (2*q, 0), (2*q, 2), (4*q, 2), (4*q, 3), (5*q, 3),
            (5*q, 4), (6*q, 4), (6*q, 6), (4*q, 6), (4*q, 4), (2*q, 4),
            (2*q, 3), (2*q-3, 3), (2*q-3, 2), (0, 2)]


class Room:
    """Orthogonal polygon with slab data derived from its edges only."""

    def __init__(self, verts):
        self.v = verts
        n = len(verts)
        self.vset = set(verts)
        self.edges = [(verts[i], verts[(i+1) % n]) for i in range(n)]
        self.hedges = [(min(a[0], b[0]), max(a[0], b[0]), a[1])
                       for a, b in self.edges if a[1] == b[1]]
        self.vedges = [(a[0], min(a[1], b[1]), max(a[1], b[1]))
                       for a, b in self.edges if a[0] == b[0]]
        ys = sorted({p[1] for p in verts})
        self.levels = ys
        self.slabs = []          # (ylo, yhi, [intervals])
        for ylo, yhi in zip(ys, ys[1:]):
            xs = sorted(x for x, a, b in self.vedges if a <= ylo and yhi <= b)
            ivs = [(xs[i], xs[i+1]) for i in range(0, len(xs), 2)]
            self.slabs.append((ylo, yhi, ivs))

    def area2(self):
        s = 0
        for (x1, y1), (x2, y2) in self.edges:
            s += x1*y2 - x2*y1
        return s

    def reflex(self):
        n = len(self.v)
        out = []
        for i in range(n):
            a, b, c = self.v[i-1], self.v[i], self.v[(i+1) % n]
            cr = (b[0]-a[0])*(c[1]-b[1]) - (b[1]-a[1])*(c[0]-b[0])
            if cr < 0:
                out.append(b)
        return out

    def slab_of(self, y, up):
        """Open slab entered from height y moving up (or down)."""
        for k, (lo, hi, ivs) in enumerate(self.slabs):
            if (lo <= y < hi) if up else (lo < y <= hi):
                return k
        return None

    def on_hedge(self, x, y):
        return any(a < x < b and yy == y for a, b, yy in self.hedges)

    def interior(self, x, y):
        """Strict interior test for a point (exact)."""
        if (x, y) in self.vset or self.on_hedge(x, y):
            return False
        if any(xx == x and a <= y <= b for xx, a, b in self.vedges):
            return False
        for lo, hi, ivs in self.slabs:
            if lo < y < hi:
                return any(a < x < b for a, b in ivs)
        # y is a level: inside iff inside slab above and below
        below = [iv for lo, hi, iv in self.slabs if hi == y]
        above = [iv for lo, hi, iv in self.slabs if lo == y]
        if not below or not above:
            return False
        return (any(a < x < b for a, b in below[0])
                and any(a < x < b for a, b in above[0]))

    def lattice_interior(self):
        xs = [p[0] for p in self.v]
        ys = [p[1] for p in self.v]
        return [(x, y) for y in range(min(ys), max(ys)+1)
                for x in range(min(xs), max(xs)+1) if self.interior(x, y)]


class Illegal(Exception):
    pass


def fold(z, lo, hi):
    """Fold z into [lo,hi]; return (x, sign of horizontal velocity factor)."""
    w = hi - lo
    u = (z - lo) % (2*w)
    if u <= w:
        return lo + u, 1
    return lo + 2*w - u, -1


def trace(room, S, vx, vy, D):
    """Exact billiard from S with horizontal speed vx per unit vertical
    travel, vertical sign vy = +-1, for total vertical travel D.
    Returns (endpoint, events). Raises Illegal on a corner or exit.
    Within an open slab the side walls are full-height polygon edges, so
    every side hit strictly inside the slab is a smooth reflection."""
    x, y = Fr(S[0]), Fr(S[1])
    vx = Fr(vx)
    left = Fr(D)
    events = []
    while left > 0:
        k = room.slab_of(y, vy > 0)
        if k is None:
            raise Illegal('left room at', (x, y))
        lo, hi, ivs = room.slabs[k]
        iv = [(a, b) for a, b in ivs if a <= x <= b]
        if len(iv) != 1:
            raise Illegal('no interval', (x, y))
        a, b = iv[0]
        if not (a < x < b):
            raise Illegal('starts on side wall', (x, y))
        yb = hi if vy > 0 else lo
        d = min(abs(yb - y), left)
        z = x + vx*d
        nx, sg = fold(z, a, b)
        if d == abs(yb - y) and (nx == a or nx == b):
            raise Illegal('corner at slab boundary', (nx, yb))
        if d < abs(yb - y) and (nx == a or nx == b):
            # stopping on a side wall: only possible if target on wall
            raise Illegal('ends on wall', (nx, y + vy*d))
        vx = vx*sg
        x = nx
        y = y + vy*d
        left -= d
        if left == 0:
            break
        # at a level: classify the point
        if (x, y) in room.vset:
            raise Illegal('vertex', (x, y))
        if room.on_hedge(x, y):
            vy = -vy
            events.append(('H', x, y))
        elif room.interior(x, y):
            events.append(('X', x, y))
        else:
            raise Illegal('outside at level', (x, y))
    return (x, y), events


def brute_trace(room, S, vx, vy, D):
    """Edge-by-edge exact tracer (no slab shortcut), for validation."""
    x, y = Fr(S[0]), Fr(S[1])
    dx, dy = Fr(vx), Fr(vy)
    left = Fr(D)
    while True:
        best = None
        for (p, r) in room.edges:
            if p[0] == r[0]:          # vertical edge
                if dx == 0:
                    continue
                t = (p[0] - x)/dx
                if t <= 0:
                    continue
                yy = y + dy*t
                if min(p[1], r[1]) <= yy <= max(p[1], r[1]):
                    if best is None or t < best[0]:
                        best = (t, 'V', p[0], yy)
            else:
                if dy == 0:
                    continue
                t = (p[1] - y)/dy
                if t <= 0:
                    continue
                xx = x + dx*t
                if min(p[0], r[0]) <= xx <= max(p[0], r[0]):
                    if best is None or t < best[0]:
                        best = (t, 'H', xx, p[1])
        t, kind, hx, hy = best
        # time t of vertical travel t*|dy| = t
        if t >= left:
            return (x + dx*left, y + dy*left)
        if (hx, hy) in room.vset:
            raise Illegal('vertex', (hx, hy))
        x, y = Fr(hx), Fr(hy)
        left -= t
        if kind == 'V':
            dx = -dx
        else:
            dy = -dy


# --------------------------------------------------- certificates (note)

def cert_four(q, X, Y):
    """Section 'The four-band crossing', steps 1-4, as written."""
    info = {}
    # step 1
    c = 2*q - 1
    if (3*Y + 2*X - 2*c) % (2*q) == 0:
        c = 2*q + 1
    assert (3*Y + 2*X - 2*c) % (2*q) != 0
    # step 2: s = (c - X + 4qi)/3, i in {0,1,2}; phase Y-4q-s mod 4q nearest 0
    def cen(z, m):
        r = z % m
        return r - m if r > m/2 else r
    best = None
    for i in range(3):
        s = Fr(c - X + 4*q*i, 3)
        p = cen(Y - 4*q - s, 4*q)
        if best is None or abs(p) < abs(best[1]):
            best = (s, p)
    s, p4 = best
    info['p4'] = p4
    assert 3*(X + s) % 2 == 1                    # bottom contact odd/3
    x2, e2 = fold(X + 3*s, 0, 2*q)
    assert x2 == 2*q - 1
    x4, e4 = fold(Y - s, 4*q, 6*q)               # backward from T
    assert 4*q < x4 < 5*q and x4 - 4*q <= Fr(2*q, 3)
    # step 3: s += 4q m, phase e4(x4-2q)-s mod 6q within q of 0
    best = None
    for m in range(3):
        sm = s + 4*q*m
        assert fold(X + 3*sm, 0, 2*q) == (x2, e2)
        assert fold(Y - sm, 4*q, 6*q) == (x4, e4)
        p = cen(e4*(x4 - 2*q) - sm, 6*q)
        if abs(p) <= q:
            best = (sm, p)
            break
    s, p3 = best
    assert p3 != 0
    x3, e3 = fold(2*q + e4*(x4 - 2*q) - s, 2*q, 5*q)
    assert 2*q < x3 <= 3*q
    # step 4: P = 12q, band (2q-3, 4q), period 4q+6
    l, M = 2*q - 3, 4*q + 6
    g = gcd(12*q, M)
    E2 = l + e2*(x2 - l)
    E3 = l + e3*(x3 - l)
    F = E3 - E2 - s
    info['g'] = g
    info['F_even'] = (F.denominator == 1 and F.numerator % 2 == 0)
    if F.denominator != 1 or F.numerator % g:
        return None, info
    Fi = F.numerator
    # solve 12q k = F mod M
    k = (Fi//g) * pow(12*q//g, -1, M//g) % (M//g)
    s = (s + 12*q*k) % (12*q*(2*q + 3))
    for sm in (s,):
        assert fold(X + 3*sm, 0, 2*q) == (x2, e2)
        assert fold(Y - sm, 4*q, 6*q) == (x4, e4)
    info.update(x2=x2, x3=x3, x4=x4)
    return s, info


def cert_two(U, V, u, v, lo, hi, l1, l2):
    """Two-band Bezout certificate. U image in lower band (period 2u, left
    wall l1), V image in upper band (period 2v). Crossing on positive seam
    sheet in (lo,hi): x = (U+V)/2 + u a + v b. Returns slope or None."""
    g = gcd(u, v)
    c = Fr(U + V, 2)
    mid = Fr(lo + hi, 2)
    n = round((mid - c)/g)
    cands = [c + g*(n + t) for t in (0, -1, 1, -2, 2)]
    cands = [x for x in cands if lo < x < hi]
    if not cands:
        return None
    x = min(cands, key=lambda z: abs(z - mid))
    N = int((x - c)/g)            # u a + v b = g N
    a = N * pow(u//g, -1, v//g) % (v//g) if v//g > 1 else 0
    b = (g*N - u*a)//v
    assert u*a + v*b == g*N
    Up = U + 2*u*a
    s = x - Up
    return s


# --------------------------------------------------- per-q driver

def run_q(q, pairs_limit=None, brute_sample=0, verbose=True):
    room = Room(cov279_polygon(q))
    pts = room.lattice_interior()
    by_y = {}
    for x, y in pts:
        by_y.setdefault(y, []).append(x)
    rows = {y: (min(xs), max(xs)) for y, xs in by_y.items()}
    counts = {}
    fails = []
    maxtravel = Fr(0)
    maxden = 1
    nbrute = 0
    twoband_none = 0
    pairs = [(S, T) for S, T in combinations(sorted(pts, key=lambda p: (p[1], p[0])), 2)
             if (S[0]-T[0]) % 2 == 0 and (S[1]-T[1]) % 2 == 0]
    if pairs_limit is not None and len(pairs) > pairs_limit:
        step = len(pairs) // pairs_limit
        pairs = pairs[::step]
    for S, T in pairs:
        (X, y1), (Y, y2) = S, T
        if y1 > y2:
            (X, y1), (Y, y2) = (Y, y2), (X, y1)
            S, T = T, S
        key = (y1, y2)
        counts[key] = counts.get(key, 0) + 1
        try:
            if y1 == y2:
                # direct chord: every point between is interior
                a, b = sorted((X, Y))
                ok = (room.interior(a, y1) and room.interior(b, y1) and
                      not any(a < e < b and lo <= y1 <= hi for e, lo, hi in room.vedges) and
                      not any(y1 == yy and not (b <= h0 or h1 <= a) for h0, h1, yy in room.hedges))
                if not ok:
                    fails.append((S, T, 'chord'))
                continue
            if key == (1, 5):
                s, info = cert_four(q, X, Y)
                if s is None:
                    fails.append((S, T, 'gcd', info['g']))
                    continue
                vx, vy, D = s, -1, 6
            elif key == (3, 5) and (X, Y) == (3*q, 5*q):
                vx, vy, D = Fr(3*q, 2), 1, 4
            else:
                # bands from the room's slabs: lower slab y1->y1+1
                k1 = room.slab_of(y1, True)
                lo1, hi1, iv1 = room.slabs[k1]
                k2 = room.slab_of(y2, False)
                lo2, hi2, iv2 = room.slabs[k2]
                assert k2 == k1 + 1 and hi1 == lo2 == y1 + 1 == y2 - 1
                (a1, b1), = iv1
                (a2, b2), = iv2
                u, v = b1 - a1, b2 - a2
                olo, ohi = max(a1, a2), min(b1, b2)
                choices = [(X, Y)]
                if key == (3, 5):
                    # note: flip source if X not multiple of q, else target
                    c0 = Fr(X + Y, 2)
                    if (c0 - olo) % gcd(u, v) == 0:
                        choices = [(2*a1 - X, Y)] if X % q else [(X, 2*a2 - Y)]
                s = cert_two(choices[0][0], choices[0][1], u, v, olo, ohi, a1, a2)
                if s is None:
                    twoband_none += 1
                    fails.append((S, T, 'two-band none'))
                    continue
                # the source image may be flipped: then launch with -s
                vx = s if choices[0][0] == X else -s
                vy, D = 1, 2
            end, ev = trace(room, S, vx, vy, D)
            if end != (Fr(T[0]), Fr(T[1])):
                fails.append((S, T, 'miss', end))
                continue
            if nbrute < brute_sample and key in ((1, 5), (1, 3), (2, 4), (3, 5)):
                if counts[key] % 7 == 1:
                    e2 = brute_trace(room, S, vx, vy, D)
                    assert e2 == end, (S, T, e2, end)
                    nbrute += 1
            maxtravel = max(maxtravel, abs(vx)*D)
            maxden = max(maxden, Fr(vx).denominator)
        except Illegal as err:
            fails.append((S, T, 'illegal', str(err)))
    return dict(room=room, counts=counts, fails=fails, total=sum(counts.values()),
                maxtravel=maxtravel, maxden=maxden, nbrute=nbrute, rows=rows)


# --------------------------------------------------- A. room facts
log('== A. Room facts (own builder) ==')
for q in (16, 28, 76, 100):
    R = Room(cov279_polygon(q))
    pts = R.lattice_interior()
    rows = {}
    for x, y in pts:
        rows.setdefault(y, []).append(x)
    log(f'q={q}: walls={len(R.v)} reflex={len(R.reflex())} area={R.area2()//2} '
        f'(13q+3={13*q+3}) slabs={[(a, b, iv) for a, b, iv in R.slabs]}')
    log('   interior rows: ' + ', '.join(f'y={y}: ({min(v)}..{max(v)}) n={len(v)}'
                                         for y, v in sorted(rows.items())))

# --------------------------------------------------- B. full replays
log('\n== B. Note certificates, own tracer: all same-parity pairs ==')
for q in (16, 28):
    r = run_q(q, brute_sample=40)
    c = r['counts']
    log(f'q={q}: pairs={r["total"]} four-band={c.get((1, 5), 0)} '
        f'by heights={dict(sorted(c.items()))}')
    log(f'   failures={len(r["fails"])} brute-tracer cross-checks={r["nbrute"]} '
        f'max horizontal travel={float(r["maxtravel"]):.0f} '
        f'(/q^2={float(r["maxtravel"])/q**2:.1f}) max slope denominator={r["maxden"]}')
    for f in r['fails'][:5]:
        log('   FAIL', f)
log(f'CPU so far {time.process_time()-T0:.1f}s')

log('\n== C. Beyond the replayed range ==')
for q in (76, 100):
    r = run_q(q)
    c = r['counts']
    log(f'q={q}: pairs={r["total"]} four-band={c.get((1, 5), 0)} failures={len(r["fails"])} '
        f'max travel/q^2={float(r["maxtravel"])/q**2:.1f} max denom={r["maxden"]}')
    for f in r['fails'][:5]:
        log('   FAIL', f)
log(f'CPU so far {time.process_time()-T0:.1f}s')

log('\n== D. Scope: other q (all same-parity pairs) ==')
for q in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 20, 22, 24, 30):
    try:
        r = run_q(q)
    except AssertionError as e:
        log(f'q={q}: construction assertion failed: {e!r}')
        continue
    kinds = {}
    for f in r['fails']:
        kinds[f[2]] = kinds.get(f[2], 0) + 1
    log(f'q={q:3d} (q mod 12={q % 12:2d}, 3|q={q % 3 == 0}): pairs={r["total"]} '
        f'failures={len(r["fails"])} {kinds}')
log(f'CPU so far {time.process_time()-T0:.1f}s')

# --------------------------------------------------- E. negative claims
log('\n== E1. First-door acceptance set at y=2 (integer a, direction (a,1)) ==')
for q in (16, 28):
    R = Room(cov279_polygon(q))
    for X in (1, q, 2*q - 1):
        acc = []
        for a in range(0, 8*q):
            try:
                (_, _), ev = trace(R, (X, 1), a, 1, Fr(3, 2))
                if ev and ev[0][0] == 'X' and ev[0][2] == 2:
                    acc.append(a)
            except Illegal:
                pass
        res = sorted({(X + a) % (4*q) for a in acc})
        accset = set(acc)
        per = next(p for p in range(1, 8*q + 1)
                   if all(((a in accset) == ((a + p) in accset)) for a in range(0, 4*q)))
        log(f'q={q} X={X}: residues of X+a mod 4q = {res} '
            f'(expect {[2*q-2, 2*q-1, 2*q+1, 2*q+2]}); least period in a = {per} (4q={4*q})')

log('\n== E2. Monotone obstruction X=2q-1 (y=1), Y=6q-1 (y=5) ==')
for q in (16, 28):
    R = Room(cov279_polygon(q))
    X, Y = 2*q - 1, 6*q - 1
    # exact acceptance window for the first door, from the folding formula
    ok_first = []
    grid = [Fr(j, 7) for j in range(-7*4*q, 7*4*q)]   # s in [-4q, 4q) step 1/7
    for s in grid:
        try:
            _, ev = trace(R, (X, 1), s, 1, Fr(3, 2))
            if ev and ev[0][0] == 'X':
                ok_first.append(s)
        except Illegal:
            pass
    near = all(min(abs(s - 4*q*k) for k in (-1, 0, 1)) < 4 for s in ok_first)
    back_far = []
    for s in ok_first:
        x4, _ = fold(Y - s, 4*q, 6*q)
        back_far.append(6*q - x4)
    log(f'q={q}: sampled s with legal first leg={len(ok_first)}, all within 4 of 0 mod 4q: {near}; '
        f'max distance of backward y=4 point from 6q = {float(max(back_far)):.3f} (<5 and q<6q-5-4q: {max(back_far) < 5})')

log('\n== E3. Odd crosses: largest contained rectangle shorter side ==')
for b in (7, 9, 11):
    cells = {(x, y) for x in range(-b, b) for y in range(-2, 2)} | \
            {(x, y) for x in range(-2, 2) for y in range(-b, b)}
    best = 0
    xs = range(-b, b)
    for x0 in xs:
        for x1 in range(x0, b):
            colsok = None
            # maximal y-run fully inside for columns x0..x1
            for y0 in range(-b, b):
                h = 0
                while (y0 + h < b and all((x, y0 + h) in cells for x in range(x0, x1 + 1))):
                    h += 1
                if h:
                    best = max(best, min(x1 - x0 + 1, h))
    log(f'b={b}: max shorter side of a contained lattice rectangle = {best}; bbox 2b={2*b}')

# --------------------------------------------------- F. author's script
log('\n== F. Author replay script, run once ==')
t = time.time()
out = subprocess.run([sys.executable, '-B', 'thin-room-replay.snapshot.py'],
                     capture_output=True, text=True, cwd=__file__.rsplit('/', 1)[0] or '.')
log(out.stdout.strip() or out.stderr.strip())
log(f'(wall {time.time()-t:.1f}s)')
log(f'\nTotal CPU (this process) {time.process_time()-T0:.1f}s')
