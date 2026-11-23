"""d165: independent checks of the d163 pattern ledger.

Combinatorial only. No ray, direction or room-size search. Shares no code with ledger.py.
Run: python3 -B checks.py > checks.log
"""
import json
import random
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
LED = json.load(open(D / 'd163-pattern-ledger' / 'ledger.json'))
T0 = time.process_time()
FAIL = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        say('FAIL', msg)


# ------------------------------------------------------------ 1. words as bitmasks
def bits_to_word(b, n):
    return ''.join('R' if b >> i & 1 else 'L' for i in range(n))


def canon_bits(b, n):
    """Least integer over the 2n rotations and reflections of the bitmask."""
    full = (1 << n) - 1
    rev = 0
    for i in range(n):
        if b >> i & 1:
            rev |= 1 << (n - 1 - i)
    best = None
    for x in (b, rev):
        for k in range(n):
            y = ((x >> k) | (x << (n - k))) & full
            if best is None or y < best:
                best = y
    return best


def canon_rot_bits(b, n):
    full = (1 << n) - 1
    return min(((b >> k) | (b << (n - k))) & full for k in range(n))


def word_bits(w):
    return sum(1 << i for i, c in enumerate(w) if c == 'R')


say('# d165 checks')
say('## 1. Enumeration by bitmask orbits (rotation + reversal), independent of ledger.py')
EXPECT = {4: 1, 6: 1, 8: 4, 10: 8, 12: 29, 14: 79, 16: 280, 18: 912, 20: 3260}
mine = {}
for W in range(4, 21, 2):
    m = (W - 4) // 2
    br, nk = set(), set()
    for pos in combinations(range(W), m):
        b = sum(1 << p for p in pos)
        br.add(canon_bits(b, W))
        nk.add(canon_rot_bits(b, W))
    mine[W] = br
    say(f'W={W:2d}: bracelets {len(br)} (expected {EXPECT[W]}), necklaces {len(nk)}, '
        f'chiral pairs merged {len(nk) - len(br)}')
    check(len(br) == EXPECT[W], f'count W={W}')
led_words = LED['words']
for W in mine:
    lw = {canon_bits(word_bits(w), W) for w, r in led_words.items() if r['W'] == W}
    check(lw == mine[W], f'ledger word set differs at W={W}')
    check(len([1 for r in led_words.values() if r['W'] == W]) == len(lw), f'duplicate classes W={W}')
check(all(w.count('L') - w.count('R') == 4 for w in led_words), 'L-R != 4')
say('ledger word set equals bitmask orbit set at every W:', not FAIL)


# ------------------------------------------------------------ geometry helpers (own code)
def turn_word(P):
    n = len(P)
    out = []
    for i in range(n):
        ax, ay = P[i - 1]; bx, by = P[i]; cx, cy = P[(i + 1) % n]
        u = (bx - ax, by - ay); v = (cx - bx, cy - by)
        if (u[0] == 0) == (u[1] == 0) or (v[0] == 0) == (v[1] == 0):
            return None  # not axis parallel or zero length
        if u[0] * v[0] + u[1] * v[1] != 0:
            return None  # collinear or backtracking
        out.append('L' if u[0] * v[1] - u[1] * v[0] > 0 else 'R')
    return ''.join(out)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_seg(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def seg_touch(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return ((o1 == 0 and on_seg(a, b, c)) or (o2 == 0 and on_seg(a, b, d))
            or (o3 == 0 and on_seg(c, d, a)) or (o4 == 0 and on_seg(c, d, b)))


def strictly_simple(P):
    n = len(P)
    if len(set(P)) != n:
        return False
    E = [(P[i], P[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            adj = (j == i + 1) or (i == 0 and j == n - 1)
            if adj:
                # adjacent perpendicular edges: only the shared vertex may be common
                shared = set(E[i]) & set(E[j])
                if len(shared) != 1:
                    return False
                continue
            if seg_touch(*E[i], *E[j]):
                return False
    return True


def area2(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))


def raster(P):
    """Cells by horizontal crossing parity at cell centers (own version: rays to -x)."""
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    n = len(P)
    V = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    S = set()
    for j in range(min(ys), max(ys)):
        for i in range(min(xs), max(xs)):
            k = sum(1 for a, b in V if a[0] <= i and min(a[1], b[1]) <= j < max(a[1], b[1]))
            if k % 2:
                S.add((i, j))
    return S


HEAD = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def walk_cells(cells):
    """Left-hand boundary walk on a cell set. Returns (turn word, vertex list) or raises on pinch."""
    cells = set(cells)
    j0 = min(c[1] for c in cells)
    i0 = min(c[0] for c in cells if c[1] == j0)
    p, h = (i0, j0), 3  # arrive at the lowest-leftmost corner heading south; first move is east
    start = (p, h)
    turns, verts = [], []
    steps = 0
    while True:
        dx, dy = HEAD[h]; nx, ny = -dy, dx
        # doubled coordinates of the two cells ahead of p
        al = ((2 * p[0] + dx + nx) // 2, (2 * p[1] + dy + ny) // 2)
        ar = ((2 * p[0] + dx - nx) // 2, (2 * p[1] + dy - ny) // 2)
        a_l, a_r = al in cells, ar in cells
        if not a_l and a_r:
            raise ValueError('pinch at %s' % (p,))
        if not a_l:
            turns.append('L'); verts.append(p); h = (h + 1) % 4
        elif a_r:
            turns.append('R'); verts.append(p); h = (h - 1) % 4
        dx, dy = HEAD[h]
        p = (p[0] + dx, p[1] + dy)
        steps += 1
        if (p, h) == start or steps > 4 * len(cells) + 8:
            break
    # the start point may have been a vertex visited at the very beginning; walk is cyclic
    boundary_len = steps
    per = sum(4 for _ in cells) - 2 * sum(1 for (x, y) in cells for d in ((1, 0), (0, 1))
                                          if (x + d[0], y + d[1]) in cells)
    if boundary_len != per:
        raise ValueError('boundary has more than one component')
    return ''.join(turns), verts


def same_class(a, b):
    n = len(a)
    return len(a) == len(b) and canon_bits(word_bits(a), n) == canon_bits(word_bits(b), n)


# ------------------------------------------------------------ 1b. mirror convention
say('## 1b. Mirror convention')
bad_rev = bad_swap = 0
for w, r in led_words.items():
    P = [tuple(p) for p in r['realization']]
    M = [(-x, y) for x, y in P][::-1]  # reflect, then traverse CCW again
    wm = turn_word(M)
    check(area2(M) > 0, 'mirror not CCW')
    ok_rev = canon_bits(word_bits(wm), len(w)) == canon_bits(word_bits(w[::-1]), len(w))
    bad_rev += not ok_rev
    swapped = w[::-1].translate(str.maketrans('LR', 'RL'))
    bad_swap += swapped.count('L') - swapped.count('R') == -4
chir = sum(1 for w in led_words if canon_rot_bits(word_bits(w), len(w)) != canon_rot_bits(word_bits(w[::-1]), len(w)))
say(f'mirror image (reflect + re-orient CCW) has the reversed word: {len(led_words) - bad_rev}/{len(led_words)}')
say(f'reversal with L/R swap gives #L-#R = -4 on {bad_swap}/{len(led_words)} words (not an equivalence on CCW words)')
say(f'chiral words (word and its mirror differ up to rotation): {chir}')
check(bad_rev == 0, 'mirror convention')

# ------------------------------------------------------------ 2. realizations
say('## 2. Realizations (own simplicity test, own raster, own boundary walk)')
random.seed(165)
big = [w for w, r in led_words.items() if r['W'] > 12]
sample = set(random.sample(big, 200)) | {w for w, r in led_words.items() if r['W'] <= 12}
stats = {'checked': 0, 'lattice': 0, 'simple': 0, 'ccw': 0, 'word_exact': 0, 'area_match': 0, 'walk_match': 0}
allbad = []
for w, r in led_words.items():
    P = [tuple(p) for p in r['realization']]
    ok_lat = all(isinstance(c, int) for p in r['realization'] for c in p) and len(P) == len(w)
    tw = turn_word(P)
    ok_simple = strictly_simple(P)
    ok_ccw = area2(P) > 0
    ok_word = tw == w
    cells = raster(P)
    ok_area = len(cells) * 2 == area2(P) == r['area'] * 2
    try:
        ww, _ = walk_cells(cells)
        ok_walk = same_class(ww, w)
    except ValueError:
        ok_walk = False
    allok = ok_lat and ok_simple and ok_ccw and ok_word and ok_area and ok_walk
    if not allok:
        allbad.append(w)
    if w in sample:
        stats['checked'] += 1
        for k, v in (('lattice', ok_lat), ('simple', ok_simple), ('ccw', ok_ccw), ('word_exact', ok_word),
                     ('area_match', ok_area), ('walk_match', ok_walk)):
            stats[k] += v
say(f'spot sample (all W<=12 plus 200 random W>=14): {stats}')
say(f'all {len(led_words)} realizations: failures {len(allbad)} {allbad[:5]}')
check(not allbad, 'realization failures')

# ------------------------------------------------------------ word structure (own rules)
def headings(w):
    h, out = 0, []
    for c in w:  # heading of edge i (vertex i -> i+1) after the turn at vertex i
        h = (h + (1 if c == 'L' else -1)) % 4
        out.append(h)
    return out


def dent_classes(w):
    n = len(w)
    return [i % 2 for i in range(n) if w[i] == w[(i + 1) % n] == 'R']


def is_hist(w):
    """Some edge parity class has exactly one edge whose heading is opposite to all the others."""
    hs = headings(w)
    for p in (0, 1):
        cls = [hs[i] for i in range(len(w)) if i % 2 == p]
        vals = set(cls)
        if len(vals) == 2 and min(cls.count(v) for v in vals) == 1:
            return True
    return False


def corner_counts(w):
    """Dent-free word: reflex count by incoming heading (the four staircase corners)."""
    hs = headings(w)
    n = len(w)
    k = [0, 0, 0, 0]
    for i in range(n):
        if w[i] == 'R':
            k[hs[i - 1]] += 1
    return k


def my_family(w):
    n = len(w)
    dc = dent_classes(w)
    if n == 4:
        return 'rectangle'
    if not dc:
        k = corner_counts(w)
        nz = [i for i in range(4) if k[i]]
        s = sorted(k, reverse=True)
        if s == [1, 0, 0, 0]: return 'L'
        if s == [1, 1, 0, 0] and (nz[1] - nz[0]) % 2 == 1: return 'T'
        if s == [1, 1, 0, 0]: return 'Z/S'
        if s == [1, 1, 1, 1]: return 'plus'
        if len(nz) == 1: return 'staircase (Ferrers)'
        if len(nz) == 2 and (nz[1] - nz[0]) == 2: return 'staircase band'
        if len(nz) == 2: return 'pyramid'
        return 'orthoconvex 3-4 corners'
    if len(set(dc)) == 1:
        return 'stacked hall (one bank)' if is_hist(w) else 'two-bank'
    r = w.count('R')
    if r >= 3 and any((w[i:] + w[:i]) == 'L' * (r + 4) + 'R' * r for i in range(n)):
        return 'spiral'
    return 'other'


say('## 4. Families (own heading-based rules)')
mism = [(w, r['subfamily'], my_family(w)) for w, r in led_words.items() if my_family(w) != r['subfamily']]
say(f'family mismatches vs ledger: {len(mism)} {mism[:8]}')
check(not mism, 'family mismatch')
Ws = list(range(4, 21, 2))
fam = {}
for w, r in led_words.items():
    fam.setdefault(my_family(w), [0] * 9)[Ws.index(r['W'])] += 1
for k in sorted(fam):
    say(f'  {k}: {fam[k]} total {sum(fam[k])}')

# dent lemma on realizations, own raster
dl_bad = 0
for w, r in led_words.items():
    P = [tuple(p) for p in r['realization']]
    cells = raster(P)
    rows, cols = {}, {}
    for x, y in cells:
        rows.setdefault(y, []).append(x); cols.setdefault(x, []).append(y)
    rconv = all(max(v) - min(v) + 1 == len(v) for v in rows.values())
    cconv = all(max(v) - min(v) + 1 == len(v) for v in cols.values())
    n = len(P)
    hd = any(w[i] == w[(i + 1) % n] == 'R' and P[i][1] == P[(i + 1) % n][1] for i in range(n))
    vd = any(w[i] == w[(i + 1) % n] == 'R' and P[i][0] == P[(i + 1) % n][0] for i in range(n))
    dl_bad += (rconv == hd) or (cconv == vd)
say(f'dent lemma (rows intervals <=> no horizontal dent) on all realizations: mismatches {dl_bad}')

# target counts
open_ = {w for w, r in led_words.items() if r['status'] == 'OPEN'}
t1 = [w for w in open_ if len(set(dent_classes(w))) <= 1]
t1_by = [sum(1 for w in t1 if len(w) == W) for W in Ws]
t1_zero = sum(1 for w in t1 if not dent_classes(w))
say(f'target 1 (all dents parallel, OPEN): {t1_by} total {len(t1)}; of these dent-free (orthoconvex) {t1_zero}, '
    f'with >= 1 dent {len(t1) - t1_zero}')


def hv(w):
    dc = dent_classes(w)
    return sorted((dc.count(0), dc.count(1)))


t2 = [w for w in open_ if hv(w) == [1, 1]]
t2_all = [w for w in led_words if hv(w) == [1, 1]]
say(f'target 2 (exactly one dent per direction, OPEN): {[sum(1 for w in t2 if len(w) == W) for W in Ws]} '
    f'total {len(t2)}; all statuses {len(t2_all)}')
th = [w for w in open_ if is_hist(w)]
say(f'target 3 (histograms, OPEN): {[sum(1 for w in th if len(w) == W) for W in Ws]} total {len(th)}; '
    f'dent-free among them {sum(1 for w in th if not dent_classes(w))}')

# ------------------------------------------------------------ named rooms (own cell sets and walk)
say('## 4b. Named rooms (cells from source dirs, own boundary walk)')


def rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms'] if r['normalized']]
cov.sort(key=lambda r: (r['n'], r['cells']))  # d72 cyl.py convention for covN
C = lambda i: {tuple(c) for c in cov[i]['cells']}
c4181_d66 = ({(0, j) for j in range(6)} | {(1, 2), (1, 3), (2, 2), (2, 3)} | {(3, j) for j in range(6)}
             | {(4, j) for j in range(6)} | {(5, 2), (5, 3), (6, 2)} | {(7, 0), (7, 1), (7, 2)})
r1843_d64 = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3),
             (2, 4), (2, 5), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4)}
check(C(4181) == c4181_d66, 'cov4181 index convention')
check(C(1843) == r1843_d64, 'room 1843 index convention')
say(f'cov4181 index matches d66 cells: {C(4181) == c4181_d66}; room 1843 matches d64 log: {C(1843) == r1843_d64}; '
    f'sizes cov279 {len(C(279))}, cov446 {len(C(446))}, cov2929 {len(C(2929))}, cov4269 {len(C(4269))}')
U2 = rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7)  # d84 indep.py
named = {
    'L6': rect(0, 2, 0, 1) | rect(0, 1, 1, 2),
    'cross12 b=7': rect(-7, 7, -2, 2) | rect(-2, 2, -7, 7),
    'DB55': rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5),
    'DBas': rect(0, 5, 0, 4) | rect(5, 9, 1, 2) | rect(9, 13, -1, 5),
    'DBw2': rect(0, 5, 0, 5) | rect(5, 9, 1, 3) | rect(9, 14, 0, 6),
    'U2': U2,
    'room 1843': C(1843), 'cov279': C(279), 'cov446': C(446), 'cov2929': C(2929),
    'cov4181': C(4181), 'cov4269': C(4269),
}
claimed = {'L6': ('LLLLLR', 'COVERED'), 'cross12 b=7': ('LLRLLRLLRLLR', 'PARTIAL'),
           'DB55': ('LLLLRRLLLLRR', 'PARTIAL'), 'DBas': ('LLLLRRLLLLRR', 'PARTIAL'),
           'DBw2': ('LLLLRRLLLLRR', 'PARTIAL'), 'U2': ('LLLLLLLRRR', 'PARTIAL'),
           'room 1843': ('LLLRLLRLLLRR', 'OPEN'), 'cov279': ('LLLRLRLRLLLRLRLR', 'PARTIAL'),
           'cov446': ('LLRLLRLLRLRLLRLLRR', 'OPEN'), 'cov2929': ('LLLRLRLLRRLLLRLRLLRR', 'OPEN'),
           'cov4181': ('LLLLRRLLRLRLLLRRLLRR', 'OPEN'), 'cov4269': ('LLRLLRLLRRLLRLLRLLRR', 'OPEN')}
for name, cells in named.items():
    ww, V = walk_cells(cells)
    wc, st = claimed[name]
    okw = same_class(ww, wc)
    lw = [w for w in led_words if same_class(w, ww)]
    status = led_words[lw[0]]['status'] if lw else None
    say(f'  {name}: W={len(ww)} word class matches ledger table {okw}; family {my_family(lw[0])}; '
        f'dents (cls0, cls1) {tuple(sorted((dent_classes(ww).count(0), dent_classes(ww).count(1))))}; '
        f'ledger status {status} (table says {st})')
    check(okw and status == st, f'named {name}')

# ------------------------------------------------------------ 3. statuses
say('## 3. Statuses')
cnt = {}
for w, r in led_words.items():
    cnt.setdefault(r['W'], {}).setdefault(r['status'], 0)
    cnt[r['W']][r['status']] += 1
say('ledger status counts per W:', {W: cnt[W] for W in sorted(cnt)})
partial = sorted((r['W'], w, r['by']) for w, r in led_words.items() if r['status'] == 'PARTIAL')
say('PARTIAL words:', partial)

# d15: do its combinatorial types cover the r<=2 (and r=3) words?
for rr in (0, 1, 2, 3):
    got = set()
    for line in open(D / 'd15-small-r' / f'types_r{rr}.txt'):
        a = line.split()
        if len(a) < 4:
            continue
        w_, h_, W_, m_ = map(int, a[:4])
        cells = {(i % w_, i // w_) for i in range(w_ * h_) if m_ >> i & 1}
        ww, _ = walk_cells(cells)
        got.add(canon_bits(word_bits(ww), len(ww)))
    want = mine[2 * rr + 4]
    say(f'd15 types_r{rr}.txt: {sum(1 for _ in open(D / "d15-small-r" / f"types_r{rr}.txt"))} order types -> '
        f'{len(got)} words; ledger words at W={2 * rr + 4}: {len(want)}; equal {got == want}')
    check(got == want, f'd15 types r={rr}')

# ------------------------------------------------------------ d162 coverage (constructions, no lighting)
say('## 3b. d162 reach: explicit class members per word (word, simplicity, metric hypothesis checked)')


def bands_ok(P, c, A, const, banks):
    """Every horizontal-cut rectangle outside the hall satisfies const*A*h <= c*u."""
    cells = raster(P)
    ys = sorted({y for _, y in cells})
    worst = Fraction(0)
    for y in ys:
        if 0 <= y < c:
            continue
        xs = sorted(x for x, yy in cells if yy == y)
        runs, s = [], xs[0]
        for a, b in zip(xs, xs[1:] + [None]):
            if b != a + 1:
                runs.append((s, a + 1)); s = b
        for a, b in runs:
            u = b - a
            # height of the rectangle: maximal vertical extent of this exact run (conservative: whole bank height)
            h = banks
            worst = max(worst, Fraction(const * A * h, c * u))
    return worst <= 1, worst


def one_sided(w):
    """Hall [0,A]x[0,c] plus an x-monotone roof profile from the word's L^4 P rotation."""
    n = len(w)
    for s in (w, w[::-1]):
        for i in range(n):
            rw = s[i:] + s[:i]
            if not rw.startswith('LLLL'):
                continue
            Pp = rw[4:]
            if len(Pp) % 2 or any(Pp[j:j + 2] not in ('RL', 'LR') for j in range(0, len(Pp), 2)):
                continue
            k = len(Pp) // 2
            steps = [1 if Pp[2 * j:2 * j + 2] == 'RL' else -1 for j in range(k)]
            hts, t = [0], 0
            for d in steps:
                t += d; hts.append(t)
            lo, H = min(hts), max(hts) - min(hts)
            A = k + 1
            c = 8 * A * max(H, 1)
            y0 = c - lo
            # vertices in the order of rw: top-left, bottom-left, bottom-right, top-right, then P
            V = [(0, y0 + hts[-1]), (0, 0), (A, 0), (A, y0)]
            x, y = A, y0
            for j, d in enumerate(steps):
                x -= 1
                V.append((x, y)); y += d; V.append((x, y))
            return V, c, A, H
    return None


def dyck(Pp):
    if not Pp or len(Pp) % 2 or any(Pp[j:j + 2] not in ('RL', 'LR') for j in range(0, len(Pp), 2)):
        return None
    t, out = 0, []
    for j in range(0, len(Pp), 2):
        t += 1 if Pp[j:j + 2] == 'RL' else -1
        if t < 0:
            return None
        out.append(t)
    return out if t == 0 else None


def two_sided(w):
    """Hall with both banks rooted strictly inside [A/4, A/3], 16Ah <= cu (d162 second step)."""
    n = len(w)
    for s in (w, w[::-1]):
        for i in range(n):
            rw = s[i:] + s[:i]
            if not rw.startswith('LL'):
                continue
            for j in range(2, n - 1):
                if rw[j:j + 2] != 'LL':
                    continue
                P1, P2 = rw[2:j], rw[j + 2:]
                h1, h2 = dyck(P1), dyck(P2)
                if h1 is None or h2 is None:
                    continue
                k1, k2 = len(h1), len(h2)
                m = max(k1, k2)
                A = 12 * m
                H = max(h1 + h2)
                c = 16 * A * H
                # order: bottom-right (A,0), top-right (A,c), P1 westward, top-left, bottom-left, P2 eastward
                V = [(A, 0), (A, c)]
                x, y = A // 3 + 1, c
                for t in h1:
                    x -= 1
                    V.append((x, y)); y = c + t; V.append((x, y))
                V += [(0, c), (0, 0)]
                x, y = A // 4 - 1, 0
                for t in h2:
                    x += 1
                    V.append((x, y)); y = -t; V.append((x, y))
                xs1 = [p[0] for p in V[2:2 + 2 * k1]]
                xs2 = [p[0] for p in V[4 + 2 * k1:]]
                mouths = all(A / 4 <= v <= A / 3 for v in xs1 + xs2)
                return V, c, A, H, mouths
    return None


one, two = {}, {}
bad1 = bad2 = 0
for w, r in led_words.items():
    if r['W'] < 10:
        continue
    o = one_sided(w)
    if o:
        V, c, A, H = o
        ok = turn_word(V) is not None and same_class(turn_word(V), w) and strictly_simple(V) and area2(V) > 0
        okb, _ = bands_ok(V, c, A, 8, max(H, 1))
        if ok and okb:
            one[w] = r['status']
        else:
            bad1 += 1
    t = two_sided(w)
    if t:
        V, c, A, H, mouths = t
        ok = turn_word(V) is not None and same_class(turn_word(V), w) and strictly_simple(V) and area2(V) > 0
        if ok and mouths:
            two[w] = r['status']
        else:
            bad2 += 1
check(set(one) == {w for w in led_words if led_words[w]['W'] >= 10 and is_hist(w)}, 'histogram construction set')
for name, S in (('one-sided stacked hall (d162 main theorem)', one), ('two-sided, mouths in [A/4,A/3] (d162 second step)', two)):
    by = [sum(1 for w in S if len(w) == W) for W in Ws[3:]]
    st = {}
    for v in S.values():
        st[v] = st.get(v, 0) + 1
    say(f'{name}: words with an explicit member, W=10..20 {by}, total {len(S)}, ledger statuses {st}')
say(f'construction failures: one-sided {bad1}, two-sided {bad2}')
both = set(one) | set(two)
mv = [w for w in both if led_words[w]['status'] == 'OPEN']
say(f'OPEN words that d162 (sound with gaps) gives an all-pairs metric member: {len(mv)} '
    f'(per W {[sum(1 for w in mv if len(w) == W) for W in Ws[3:]]}); overlap of the two classes {len(set(one) & set(two))}')
say(f'  by ledger subfamily: { {k: sum(1 for w in mv if led_words[w]["subfamily"] == k) for k in sorted({led_words[w]["subfamily"] for w in mv})} }')
for nm in ('room 1843', 'cov446', 'cov2929', 'cov4181', 'cov4269', 'cov279', 'DB55'):
    ww, _ = walk_cells(named[nm])
    lw = [w for w in led_words if same_class(w, ww)][0]
    say(f'  {nm}: one-sided {lw in one}, two-sided {lw in two}')

# ------------------------------------------------------------ 5. M2 vs word class
say('## 5. Two-sided stacked hall (M2) vs the one-direction-convex word class')
no_band = []
for w in t1:
    if not dent_classes(w):
        continue
    P = [tuple(p) for p in led_words[w]['realization']]
    cells = raster(P)
    n = len(P)
    hd = any(w[i] == w[(i + 1) % n] == 'R' and P[i][1] == P[(i + 1) % n][1] for i in range(n))
    if hd:  # dents horizontal -> columns are intervals -> hall must be a full-width horizontal band
        xs = {x for x, _ in cells}
        full = any({x for x, yy in cells if yy == y} == xs for y in {y for _, y in cells})
    else:
        ys = {y for _, y in cells}
        full = any({y for xx, y in cells if xx == x} == ys for x in {x for x, _ in cells})
    if not full:
        no_band.append(w)
say(f'OPEN one-direction-convex words with >= 1 dent: {len([w for w in t1 if dent_classes(w)])}; '
    f'ledger realization has no spanning hall band (so not a stacked hall at those lengths): {len(no_band)}')
if no_band:
    w = min(no_band, key=len)
    say(f'  smallest: {w} W={len(w)} vertices {led_words[w]["realization"]}')

say(f'## done: {len(FAIL)} failures; CPU {time.process_time() - T0:.1f} s')
