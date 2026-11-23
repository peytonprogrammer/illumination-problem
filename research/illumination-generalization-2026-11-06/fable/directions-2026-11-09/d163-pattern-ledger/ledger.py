"""d163 wall-turn pattern ledger for strictly simple orthogonal lattice rooms, W <= 20.

Combinatorial only. No ray, direction, reflection-word, room-size or by-area search.
A word is a cyclic sequence of vertex turns for a counterclockwise traversal:
L = convex (90 degrees), R = reflex (270 degrees), #L - #R = 4. Words are taken up to
rotation and reversal (reversal = mirror image traversed counterclockwise).

Run: python3 -B ledger.py   (writes ledger.json, ledger.log next to this file)
"""
import json
import sys
import time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
WMAX = 20
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s)
    print(s)


# ---------------------------------------------------------------- words
def canon(w):
    """Lexicographically least rotation of w or of its reversal."""
    n = len(w)
    best = None
    for s in (w, w[::-1]):
        for i in range(n):
            c = s[i:] + s[:i]
            if best is None or c < best:
                best = c
    return best


def enumerate_words(W):
    m = (W - 4) // 2
    seen = set()
    for pos in combinations(range(W), m):
        if pos and pos[0] != 0 and m > 0:
            continue  # rotate so an R sits at 0; every class has such a representative
        w = ['L'] * W
        for p in pos:
            w[p] = 'R'
        seen.add(canon(''.join(w)))
    return sorted(seen)


def burnside_count(W):
    """Independent count of binary bracelets with m = (W-4)/2 R's (dihedral Burnside)."""
    from math import comb, gcd
    n, m = W, (W - 4) // 2
    rot = 0
    for k in range(n):
        g = gcd(k, n)
        c = n // g
        if m % c == 0:
            rot += comb(g, m // c)
    if n % 2 == 1:
        refl = n * comb((n - 1) // 2, m // 2)
    else:
        # n/2 axes through two vertices, n/2 axes through two edges
        a = 0
        for fixed in range(3):  # number of the 2 fixed beads that are R
            if (m - fixed) % 2 == 0 and m - fixed >= 0:
                a += comb(2, fixed) * comb((n - 2) // 2, (m - fixed) // 2)
        b = comb(n // 2, m // 2) if m % 2 == 0 else 0
        refl = (n // 2) * a + (n // 2) * b
    return (rot + refl) // (2 * n)


# ---------------------------------------------------------------- realization
def sgn(v):
    return (v > 0) - (v < 0)


def compress(P):
    xs = {x: i for i, x in enumerate(sorted({p[0] for p in P}))}
    ys = {y: i for i, y in enumerate(sorted({p[1] for p in P}))}
    return [(xs[x], ys[y]) for x, y in P]


def realize(w):
    """Vertex list aligned with w (vertex i has turn w[i]). Inductive jog insertion."""
    n = len(w)
    if n == 4:
        return [(0, 0), (1, 0), (1, 1), (0, 1)]
    i = next(k for k in range(n) if w[k] != w[(k + 1) % n])
    r = w[(i + 2) % n:] + w[:(i + 2) % n] if (i + 2) % n else w
    Pp = [(2 * x, 2 * y) for x, y in compress(realize(r[:-2]))]
    A, B = Pp[-1], Pp[0]
    d = (sgn(B[0] - A[0]), sgn(B[1] - A[1]))
    nl = (-d[1], d[0])
    s = 1 if r[-2] == 'L' else -1
    M = (A[0] + d[0], A[1] + d[1])
    M2 = (M[0] + s * nl[0], M[1] + s * nl[1])
    B2 = (B[0] + s * nl[0], B[1] + s * nl[1])
    P = [B2] + Pp[1:] + [M, M2]
    Q = [None] * n
    for k in range(n):
        Q[(k + i + 2) % n] = P[k]
    return compress(Q)


def turns(P):
    n = len(P)
    out = []
    for i in range(n):
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        u = (b[0] - a[0], b[1] - a[1])
        v = (c[0] - b[0], c[1] - b[1])
        cr = u[0] * v[1] - u[1] * v[0]
        assert cr != 0 and u[0] * v[0] + u[1] * v[1] == 0, 'not orthogonal'
        out.append('L' if cr > 0 else 'R')
    return ''.join(out)


def signed_area2(P):
    return sum(P[i - 1][0] * P[i][1] - P[i][0] * P[i - 1][1] for i in range(len(P)))


def seg_meet(a, b, c, d):
    """Closed axis-parallel segments ab and cd intersect."""
    x1, x2 = sorted((a[0], b[0])); y1, y2 = sorted((a[1], b[1]))
    x3, x4 = sorted((c[0], d[0])); y3, y4 = sorted((c[1], d[1]))
    return x1 <= x4 and x3 <= x2 and y1 <= y4 and y3 <= y2


def strictly_simple(P):
    n = len(P)
    if len(set(P)) != n:
        return False
    E = [(P[i], P[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if seg_meet(*E[i], *E[j]):
                return False
    return True


def cells_of(P):
    """Unit cells inside an integer orthogonal polygon (crossing test at cell centers)."""
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    n = len(P)
    vert = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    out = set()
    for cx in range(min(xs), max(xs)):
        for cy in range(min(ys), max(ys)):
            k = 0
            for a, b in vert:
                if a[0] > cx and min(a[1], b[1]) <= cy < max(a[1], b[1]):
                    k += 1
            if k % 2:
                out.add((cx, cy))
    return out


def polygon_of_cells(cells):
    """CCW vertex list of a cell set without pinches."""
    E = {}
    for (x, y) in cells:
        for a, b in (((x, y), (x + 1, y)), ((x + 1, y), (x + 1, y + 1)),
                     ((x + 1, y + 1), (x, y + 1)), ((x, y + 1), (x, y))):
            if (b, a) in E:
                del E[(b, a)]
            else:
                E[(a, b)] = 1
    nxt = {}
    for a, b in E:
        assert a not in nxt, 'pinch'
        nxt[a] = b
    start = min(nxt)
    pts = [start]
    while True:
        p = nxt[pts[-1]]
        if p == start:
            break
        pts.append(p)
    assert len(pts) == len(nxt), 'more than one boundary component'
    n = len(pts)
    V = [pts[i] for i in range(n)
         if (pts[i][0] - pts[i - 1][0]) * (pts[(i + 1) % n][1] - pts[i][1])
         != (pts[i][1] - pts[i - 1][1]) * (pts[(i + 1) % n][0] - pts[i][0])]
    return V


def lattice_classes(P, cells):
    """Per parity class: (#vertices, #other lattice points) of the closed room."""
    pts = set()
    for (x, y) in cells:
        pts |= {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
    V = set(P)
    out = {}
    for c in ((0, 0), (0, 1), (1, 0), (1, 1)):
        cl = [p for p in pts if (p[0] % 2, p[1] % 2) == c]
        out[c] = (sum(p in V for p in cl), sum(p not in V for p in cl))
    return out


# ---------------------------------------------------------------- word structure
def dents(w):
    """Edges i (vertex i -> i+1) with both ends reflex; returns their index parities."""
    n = len(w)
    return [i % 2 for i in range(n) if w[i] == 'R' and w[(i + 1) % n] == 'R']


def corner_vector(w):
    """For a dent-free word: the 4 staircase depths (k1..k4), canonical up to dihedral."""
    n = len(w)
    Rs = [i for i in range(n) if w[i] == 'R']
    if not Rs:
        return (0, 0, 0, 0)
    seq = []  # cyclic sequence of 'R' and '*' (corner markers)
    for a, b in zip(Rs, Rs[1:] + [Rs[0] + n]):
        seq.append('R')
        seq.extend('*' * (b - a - 2))  # run of b-a-1 L's carries b-a-2 markers
    assert seq.count('*') == 4
    i0 = seq.index('*')
    k = [len(p) for p in ''.join(seq[i0:] + seq[:i0]).split('*')[1:]]
    cands = []
    for s in (k, k[::-1]):
        for i in range(4):
            cands.append(tuple(s[i:] + s[:i]))
    return max(cands)


def is_pairs(s):
    return len(s) % 2 == 0 and all(s[j:j + 2] in ('RL', 'LR') for j in range(0, len(s), 2))


def rotations(w):
    for s in (w, w[::-1]):
        for i in range(len(s)):
            yield s[i:] + s[:i]


def is_histogram(w):
    """One-sided stacked hall: cyclically L^4 P with P in {RL, LR}*."""
    return any(r.startswith('LLLL') and is_pairs(r[4:]) for r in rotations(w))


def is_two_bank(w):
    """Vertically convex form L P1 LL P2 L with P1, P2 in {RL, LR}*."""
    n = len(w)
    for r in rotations(w):
        if r[0] != 'L' or r[-1] != 'L':
            continue
        mid = r[1:-1]
        for j in range(0, n - 3, 2):
            if is_pairs(mid[:j]) and mid[j:j + 2] == 'LL' and is_pairs(mid[j + 2:]):
                return True
    return False


def family(w):
    W = len(w)
    r = w.count('R')
    dp = dents(w)
    if W == 4:
        return 'rectangle', 'rectangle'
    if not dp:
        k = corner_vector(w)
        name = {(1, 0, 0, 0): 'L', (1, 1, 0, 0): 'T', (1, 0, 1, 0): 'Z/S', (1, 1, 1, 1): 'plus'}.get(k)
        if name is None:
            nz = [i for i in range(4) if k[i]]
            if len(nz) == 1:
                name = 'staircase (Ferrers)'
            elif len(nz) == 2 and k[2]:
                name = 'staircase band'  # two opposite staircase corners: x- and y-monotone strip
            elif len(nz) == 2:
                name = 'pyramid'  # two adjacent staircase corners: orthoconvex histogram
            else:
                name = 'orthoconvex 3-4 corners'
        return 'orthoconvex', name
    if len(set(dp)) == 1:
        if is_histogram(w):
            return 'one-direction convex', 'stacked hall (one bank)'
        return 'one-direction convex', 'two-bank'
    if w.count('R') >= 3 and any(c == 'L' * (r + 4) + 'R' * r for c in rotations(w)):
        return 'two-direction dented', 'spiral'
    return 'two-direction dented', 'other'


# ---------------------------------------------------------------- named rooms
def rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


def named_rooms():
    cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
           if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))
    C = lambda i: {tuple(c) for c in cov[i]['cells']}
    R22 = {(-1, -1), (-1, 0), (0, -2), (0, -1), (0, 0), (0, 1), (1, -3), (1, -2), (1, 1), (1, 2),
           (2, 1), (2, 2), (3, 0), (3, 1), (4, 0)}
    rooms = {
        'L6 (6-wall L, d160/d161)': rect(0, 2, 0, 1) | rect(0, 1, 1, 2),
        'cross12 b=7 (d87/d147)': rect(-7, 7, -2, 2) | rect(-2, 2, -7, 7),
        'CR34 (d69)': rect(4, 7, 0, 11) | rect(0, 11, 4, 7),
        'DB55': rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5),
        'DBas': rect(0, 5, 0, 4) | rect(5, 9, 1, 2) | rect(9, 13, -1, 5),
        'DBw2': rect(0, 5, 0, 5) | rect(5, 9, 1, 3) | rect(9, 14, 0, 6),
        'U2': rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7),
        'S10 (d65)': {(0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1)},
        'room 1843 (d64)': C(1843),
        'cov279': C(279),
        'cov446': C(446),
        'cov2929': C(2929),
        'cov4181': C(4181),
        'cov4269': C(4269),
        'R22 (W=22, out of scope)': R22,
    }
    assert rooms['cov4181'] == ({(0, j) for j in range(6)} | {(1, 2), (1, 3), (2, 2), (2, 3)}
                                | {(3, j) for j in range(6)} | {(4, j) for j in range(6)}
                                | {(5, 2), (5, 3), (6, 2)} | {(7, 0), (7, 1), (7, 2)})
    return rooms


def cov279_stretch(q):  # d127 checks.py
    return [(0, 0), (2 * q, 0), (2 * q, 2), (4 * q, 2), (4 * q, 3), (5 * q, 3), (5 * q, 4), (6 * q, 4),
            (6 * q, 6), (4 * q, 6), (4 * q, 4), (2 * q, 4), (2 * q, 3), (2 * q - 3, 3), (2 * q - 3, 2), (0, 2)]


def dumbbell(d1, b1, h1, d2, b2, h2, p, w, L):  # d110 geom.py; strict mouths b<p, p+w<b+h
    x2 = d1 + L
    return [(0, b1), (d1, b1), (d1, p), (x2, p), (x2, b2), (x2 + d2, b2), (x2 + d2, b2 + h2),
            (x2, b2 + h2), (x2, p + w), (d1, p + w), (d1, b1 + h1), (0, b1 + h1)]


# ---------------------------------------------------------------- reviewed results
COVER_ALL = ('d15 Theorem S (reviewed d15-review): every pair of distinct real interior points lit, '
             'any real side lengths, r <= 2')

UNIVERSAL_BANDS = [
    ('C9 (d9, COMPUTED independent)', 'same-class lattice pairs, area <= 20; different-class lattice pairs '
     'area <= 16 (d9 Part A)'),
    ('Q-class closure (d102 reviewed, computer-assisted)', 'rooms with a corner-only parity class: all '
     'interior lattice pairs; such rooms have area <= 36 and wall-line gaps <= 2 (d97, d154)'),
    ('18-wall Q-class (d90/d100)', 'W = 18 rooms with a corner-only class: all real pairs'),
    ('d64/d67', 'rooms with a proper canonical factor (2,800 rooms, area <= 8r): same-class lattice pairs'),
    ('d80', 'n >= 120 cells: every pair with an irrational coordinate'),
    ('d126', 'a decomposition piece deeper than Z = 4HT^2 with one closed end: whole room lit'),
    ('d16 Theorem RR', 'lattice room: all rational pairs lit => all real pairs lit (a reduction, not a band)'),
]


def structural_partials():
    """Word -> list of (theorem, scope). Word-specific reviewed results on infinite metric subfamilies."""
    S = {}

    def add(P, thm, scope):
        w = canon(turns(P))
        S.setdefault(w, []).append((thm, scope))
        return w

    # d161: hall + four full-side arms (plus). Example cross12 b=7.
    add(polygon_of_cells(rect(-7, 7, -2, 2) | rect(-2, 2, -7, 7)), 'd161',
        'hall + 4 full-side rectangular arms (arm width = whole hall side), all real pairs')
    # d112/d111/d110/d108/d77: rectangular dumbbell, strict mouths
    add(dumbbell(5, 0, 5, 5, 0, 5, 2, 1, 3), 'd112',
        'two rectangular chambers + straight corridor, mouths strictly inside both sides, L > 4d, all real pairs')
    add(dumbbell(5, 0, 5, 5, 0, 5, 2, 1, 3), 'd111', 'same skeleton, L >= 2d, irrational aspect quotient, real pairs')
    add(dumbbell(5, 0, 5, 5, 0, 5, 2, 1, 3), 'd108', 'DB55 stretches, corridor length coprime to 5, same-class lattice pairs')
    add(dumbbell(5, 0, 5, 5, 0, 6, 1, 2, 4), 'd77', 'DBw2 stretches, integer corridor length > 10, lattice pairs')
    # d127: cov279 stretch family
    add(cov279_stretch(16), 'd127', 'cov279 stretches (height 6, width 6q), q >= 4, 3 does not divide q, '
        'same-parity lattice pairs only')
    # d84: U2 and its stretches
    add(polygon_of_cells(rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7)), 'd84',
        'U2 and its stretches (areas 46 + 8k), all real pairs (two-cylinder rim test)')
    return S


PENDING = {
    'stacked hall (one bank)': 'd162 (in review): parallel-mouth-combs.md, metric condition 8Ah <= cu per attached '
                               'rectangle; not every length assignment',
    'staircase (Ferrers)': 'terrace-induction.md (unreviewed): southwest staircase containing the triangle; '
                           'metric condition (A\'-A)H <= Ah per terrace',
    'two-bank': 'd162 second step (in review): two-sided halls with mouths in [A/4, A/3] and 16Ah <= cu; metric',
}


# ---------------------------------------------------------------- main
def main():
    t0 = time.process_time()
    words = {}
    log('# d163 pattern ledger run')
    log('## 1. Enumeration (cyclic L/R words, #L - #R = 4, up to rotation and reversal)')
    for W in range(4, WMAX + 1, 2):
        ws = enumerate_words(W)
        b = burnside_count(W)
        log(f'W={W:2d} r={(W - 4) // 2}: {len(ws)} words (Burnside {b})')
        assert len(ws) == b
        for w in ws:
            words[w] = {'W': W, 'r': (W - 4) // 2}

    log('## 2. Realization (inductive jog insertion, coordinates compressed)')
    bad = 0
    convex_mismatch = 0
    for w, rec in words.items():
        P = realize(w)
        ok = strictly_simple(P) and signed_area2(P) > 0 and turns(P) == w
        if not ok:
            bad += 1
            continue
        cells = cells_of(P)
        assert polygon_of_cells(cells) and len(polygon_of_cells(cells)) == len(w)
        # dent lemma check on this realization: dents of parity p <-> disconnected sections
        rows, cols = {}, {}
        for x, y in cells:
            rows.setdefault(y, []).append(x)
            cols.setdefault(x, []).append(y)
        hconv = all(max(v) - min(v) + 1 == len(v) for v in rows.values())
        vconv = all(max(v) - min(v) + 1 == len(v) for v in cols.values())
        n = len(P)
        hd = any(w[i] == 'R' and w[(i + 1) % n] == 'R' and P[i][1] == P[(i + 1) % n][1] for i in range(n))
        vd = any(w[i] == 'R' and w[(i + 1) % n] == 'R' and P[i][0] == P[(i + 1) % n][0] for i in range(n))
        if hconv == hd or vconv == vd:
            convex_mismatch += 1
        cls = lattice_classes(P, cells)
        rec.update(realization=P, area=len(cells),
                   bbox=[max(p[0] for p in P), max(p[1] for p in P)],
                   corner_only_class=any(o == 0 for _, o in cls.values()))
    log(f'realized {len(words) - bad}/{len(words)} words strictly simple with the exact word; '
        f'dent-lemma mismatches {convex_mismatch}')
    assert bad == 0 and convex_mismatch == 0

    log('## 3. Families')
    for w, rec in words.items():
        fam, sub = family(w)
        rec['family'], rec['subfamily'] = fam, sub
        rec['dents'] = len(dents(w))
        if fam == 'orthoconvex':
            rec['corner_vector'] = list(corner_vector(w))
        if rec['dents'] and len(set(dents(w))) == 1:
            assert is_two_bank(w), w
        elif not rec['dents']:
            assert is_two_bank(w), w
        else:
            assert not is_two_bank(w), w
        if sub == 'stacked hall (one bank)':
            assert is_histogram(w)

    log('## 4. Named rooms')
    named = {}
    for name, cells in named_rooms().items():
        P = polygon_of_cells(cells)
        assert strictly_simple(P)
        w = canon(turns(P))
        fam = family(w)
        tw = turns(P)
        n = len(P)
        h = sum(1 for i in range(n) if tw[i] == 'R' == tw[(i + 1) % n] and P[i][1] == P[(i + 1) % n][1])
        v = sum(1 for i in range(n) if tw[i] == 'R' == tw[(i + 1) % n]) - h
        named[name] = {'word': w, 'W': len(w), 'area': len(cells), 'family': fam[0], 'subfamily': fam[1],
                       'dents_hv': [h, v], 'vertices': P}
        log(f'{name}: W={len(w)} area={len(cells)} word={w} family={fam[0]} / {fam[1]} dents(h,v)=({h},{v})')
        if w in words:
            words[w].setdefault('named', []).append(name)
    P = cov279_stretch(16)
    log(f'cov279 stretch q=16 word equals cov279 word: {canon(turns(P)) == named["cov279"]["word"]}')

    log('## 5. Status')
    SP = structural_partials()
    for w, thm in SP.items():
        log(f'structural partial: W={len(w)} {w} {family(w)} <- {[t for t, _ in thm]}')
    for w, rec in words.items():
        if rec['W'] <= 8:
            rec['status'] = 'COVERED'
            rec['by'] = ['d15']
            extra = []
            if rec['subfamily'] in ('L', 'T', 'plus'):
                extra.append('d161')
            if rec['subfamily'] in ('L', 'T', 'Z/S', 'rectangle'):
                extra.append('d157 (lattice marks)')
            rec['also'] = extra
        elif w in SP:
            rec['status'] = 'PARTIAL'
            rec['by'] = [t for t, _ in SP[w]]
            rec['scope'] = [s for _, s in SP[w]]
        else:
            rec['status'] = 'OPEN'
            rec['by'] = []
        rec['strict_status'] = 'COVERED' if rec['W'] <= 8 else 'PARTIAL'
        if rec['subfamily'] in PENDING and rec['W'] >= 10:
            rec['pending'] = PENDING[rec['subfamily']]

    # tables
    Ws = list(range(4, WMAX + 1, 2))
    tab = {W: {'COVERED': 0, 'PARTIAL': 0, 'OPEN': 0, 'total': 0} for W in Ws}
    famtab = {}
    for w, rec in words.items():
        tab[rec['W']][rec['status']] += 1
        tab[rec['W']]['total'] += 1
        key = (rec['family'], rec['subfamily'])
        famtab.setdefault(key, {W: 0 for W in Ws})[rec['W']] += 1
    log('W | words | COVERED | PARTIAL | OPEN')
    for W in Ws:
        t = tab[W]
        log(f"{W} | {t['total']} | {t['COVERED']} | {t['PARTIAL']} | {t['OPEN']}")
    log('family / subfamily counts per W ' + str(Ws))
    for key in sorted(famtab):
        log(f'{key[0]} / {key[1]}: {[famtab[key][W] for W in Ws]} total {sum(famtab[key].values())}')

    # smallest OPEN words per subfamily
    log('## 5b. Band witnesses on the constructed realization (evidence only, one room per word)')
    for W in Ws:
        ws = [r for r in words.values() if r['W'] == W]
        log(f"W={W}: corner-only class {sum(r['corner_only_class'] for r in ws)}/{len(ws)}, "
            f"area<=20 {sum(r['area'] <= 20 for r in ws)}/{len(ws)}, max area {max(r['area'] for r in ws)}")

    log('## 5c. Dent profiles (horizontal dents, vertical dents), sorted, OPEN two-direction words at W=20')
    prof = {}
    for w, rec in words.items():
        n = len(w)
        P = rec['realization']
        h = sum(1 for i in range(n) if w[i] == 'R' == w[(i + 1) % n] and P[i][1] == P[(i + 1) % n][1])
        v = rec['dents'] - h
        rec['dent_profile'] = sorted((h, v))
        if rec['W'] == 20 and rec['family'] == 'two-direction dented' and rec['status'] == 'OPEN':
            key = tuple(sorted((h, v)))
            prof[key] = prof.get(key, 0) + 1
    log(str(sorted(prof.items())))

    log('## 5d. OPEN words a single all-lengths theorem would close, per W ' + str(Ws))
    targets = [
        ('T-orthoconvex: every orthoconvex room (no dents)', lambda w, r: r['dents'] == 0),
        ('T-histogram: one-bank stacked halls, all lengths', lambda w, r: is_histogram(w)),
        ('T-vconvex: all dents parallel (two-sided stacked halls / vertically convex), all lengths',
         lambda w, r: len(set(dents(w))) <= 1),
        ('T-bank-only: two-bank words that are not histograms', lambda w, r: r['subfamily'] == 'two-bank'),
        ('T-spiral', lambda w, r: r['subfamily'] == 'spiral'),
        ('T-(1,1): exactly one dent in each orientation', lambda w, r: r['dent_profile'] == [1, 1]),
        ('T-two-direction (everything else)', lambda w, r: r['family'] == 'two-direction dented'),
    ]
    tgt = {}
    for name, pred in targets:
        c = [sum(1 for w, r in words.items() if r['W'] == W and r['status'] == 'OPEN' and pred(w, r)) for W in Ws]
        tgt[name] = c
        log(f'{name}: {c} total {sum(c)}')

    log('## 6. Smallest OPEN word per subfamily (realization coordinates)')
    smallest = {}
    for w, rec in sorted(words.items(), key=lambda kv: (kv[1]['W'], kv[1]['area'], kv[0])):
        if rec['status'] != 'OPEN':
            continue
        key = rec['subfamily']
        if key not in smallest:
            smallest[key] = w
            log(f"{key}: W={rec['W']} word={w} area={rec['area']} vertices={rec['realization']}")
    w10 = [w for w, r in words.items() if r['W'] == 10]
    log('## all W=10 words')
    for w in w10:
        r = words[w]
        log(f"{w} {r['subfamily']} {r['status']} area={r['area']} corner_only={r['corner_only_class']} V={r['realization']}")

    out = {
        'convention': 'CCW traversal, L = convex, R = reflex; canonical = least rotation of word or reversal',
        'counts': {str(W): tab[W] for W in Ws},
        'families': {f'{k[0]} / {k[1]}': {str(W): v for W, v in c.items()} for k, c in sorted(famtab.items())},
        'universal_bands': UNIVERSAL_BANDS,
        'covering_theorem': COVER_ALL,
        'structural_partials': {w: SP[w] for w in SP},
        'pending': PENDING,
        'named_rooms': named,
        'smallest_open_by_subfamily': smallest,
        'targets_open_closed': tgt,
        'words': words,
    }
    (HERE / 'ledger.json').write_text(json.dumps(out, separators=(',', ':'), default=list))
    log(f'CPU {time.process_time() - t0:.1f} s')
    (HERE / 'ledger.log').write_text('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    main()
