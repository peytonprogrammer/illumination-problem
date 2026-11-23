"""Review checks for d15-small-r Theorem 3 (r = 3, W = 10).

Reads (never writes) ../d15-small-r (lemmas.py, types_r3.txt, cert_r3.json),
../d15-review (rv.py, enum_check.py), ../d163-pattern-ledger/ledger.json.

Sections
 1. Independent enumeration of r = 3 order types by closed lattice walks,
    with the boundary word of each type.
 2. The 8 ledger words and their realizations, mapped to order types.
 3. Re-run of lemmas.certify_type on the 70 types; compare with cert_r3.json.
 4. Cross-check of every certificate against rv.py (review code written from
    the lemma statements), on unit-gap rooms, with an exact trace of the
    certificate's prescribed paths. Uncovered pairs: rv.py must find no
    metric-free instance either.
 5. Per word, 4 explicit lattice realizations (the ledger room plus 3 more),
    every certified pair traced exactly, plus Lemma D degenerate pairs
    (S + T = 2V and one-coordinate mirror pairs).
 6. The Ferrers word LLLLLRLRLR: the d168 claim.

Usage: python3 -B checks.py > checks.log
"""
import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction as Fr

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
D15 = os.path.join(HERE, "..", "d15-small-r")
REV = os.path.join(HERE, "..", "d15-review")
LEDGER = os.path.join(HERE, "..", "d163-pattern-ledger", "ledger.json")
sys.path.insert(0, D15)
sys.path.insert(0, REV)
import lemmas as AL        # noqa: E402  author's code, read only
import rv                  # noqa: E402  d15 review code
import enum_check as EC    # noqa: E402  d15 review code (helpers only)

Q = rv.field(2)
NPASS = NFAIL = 0
T0 = time.process_time()


def check(ok, msg):
    global NPASS, NFAIL
    if ok:
        NPASS += 1
    else:
        NFAIL += 1
    print(("PASS " if ok else "FAIL ") + msg)


def show(ot):
    return "/".join("".join("#" if ot.ins(i, j) else "." for i in range(ot.nx)) for j in reversed(range(ot.ny)))


def canon_word(w):
    best = None
    for s in (w, w[::-1]):
        for i in range(len(s)):
            c = s[i:] + s[:i]
            if best is None or c < best:
                best = c
    return best


def word_of(vs):
    n = len(vs)
    a2 = sum(vs[i - 1][0] * vs[i][1] - vs[i][0] * vs[i - 1][1] for i in range(n))
    if a2 < 0:
        vs = vs[::-1]
    out = []
    for i in range(n):
        a, b, c = vs[i - 1], vs[i], vs[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        out.append('L' if cr > 0 else 'R')
    return canon_word(''.join(out))


def type_key(vs):
    xs = sorted({v[0] for v in vs})
    ys = sorted({v[1] for v in vs})
    rk = [(xs.index(x), ys.index(y)) for x, y in vs]
    nx, ny = len(xs) - 1, len(ys) - 1
    cells = EC.inside_cells(rk, nx, ny)
    return EC.canon(nx, ny, cells), (nx, ny, cells)


# ------------------------------------------------------------------ 1
def walks_lexmin(W, N):
    """Closed alternating walks on {0..N}^2 that start at their lexicographically
    least vertex with a horizontal edge. One walk per polygon."""
    out = []

    def rec(vs):
        k = len(vs)
        if k == W:
            if vs[-1][0] == vs[0][0] and vs[-1][1] != vs[0][1]:
                out.append(tuple(vs))
            return
        x, y = vs[-1]
        if k % 2 == 1:
            nxt = [(a, y) for a in range(N + 1) if a != x]
        else:
            nxt = [(x, b) for b in range(N + 1) if b != y]
        for v in nxt:
            if v < vs[0] or v in vs:
                continue
            rec(vs + [v])

    for x0 in range(N + 1):
        for y0 in range(N + 1):
            for x1 in range(x0 + 1, N + 1):
                rec([(x0, y0), (x1, y0)])
    return out


print("== 1. Order types for r = 3 by closed walks on {0..4}^2")
types = {}
nwalk = 0
for vs in walks_lexmin(10, 4):
    if not EC.simple(list(vs)):
        continue
    nwalk += 1
    key, _ = type_key(list(vs))
    types.setdefault(key, set()).add(word_of(list(vs)))
auth = {}
for line in open(os.path.join(D15, "types_r3.txt")):
    nx, ny, W, mask = map(int, line.split())
    cells = frozenset((i, j) for j in range(ny) for i in range(nx) if (mask >> (i + nx * j)) & 1)
    auth[EC.canon(nx, ny, cells)] = (nx, ny, mask)
print(f"   simple walks {nwalk}, order types {len(types)}, author's {len(auth)}")
check(set(types) == set(auth), "walk enumeration gives exactly the 70 types of types_r3.txt")
check(all(len(v) == 1 for v in types.values()), "each order type has one boundary word")
TYPE_WORD = {auth[k]: next(iter(v)) for k, v in types.items()}
words = sorted(set(TYPE_WORD.values()))
print("   words:", len(words), words)

# ------------------------------------------------------------------ 2
print("\n== 2. Ledger words W = 10")
led = json.load(open(LEDGER))['words']
lw = {k: v for k, v in led.items() if v['W'] == 10}
check(sorted(lw) == words, "the 8 ledger words equal the 8 words of the 70 types")
LED_TYPE = {}
for k, v in sorted(lw.items()):
    vs = [tuple(p) for p in v['realization']]
    check(word_of(vs) == k, f"ledger realization of {k} has word {k}")
    key, _ = type_key(vs)
    LED_TYPE[k] = auth[key]
    print(f"   {k}: {v['subfamily']}, ledger room has type {auth[key]}")

# ------------------------------------------------------------------ 3
print("\n== 3. Re-run of lemmas.certify_type on the 70 types")
cert = json.load(open(os.path.join(D15, "cert_r3.json")))
CERT = {}
UNC = {}
tot = Counter()
for row in cert:
    ot = AL.OT.from_mask(row['nx'], row['ny'], row['mask'])
    certs, unc = AL.certify_type(ot)
    c = Counter(v['lem'] + ('-' + v['form'] if 'form' in v else '') for v in certs.values())
    same = dict(c) == row['counts'] and [list(map(list, p)) for p in unc] == row['uncovered']
    if not same:
        check(False, f"rerun differs from cert_r3.json for {row['shape']}")
    key = (row['nx'], row['ny'], row['mask'])
    CERT[key], UNC[key] = certs, unc
    tot.update(c)
    tot['pairs'] += len(certs) + len(unc)
    tot['unc'] += len(unc)
check(tot['pairs'] == 13608 and tot['unc'] == 578, f"pairs {tot['pairs']}, uncovered {tot['unc']}, certified {tot['pairs'] - tot['unc']}")
full = [row['shape'] for row in cert if not row['uncovered']]
check(sorted(full) == sorted(['.#./###/##.', '.#./##./###/.##', '##../####/.###/.##.']), f"fully certified types {full}")
print("   certificates by lemma:", {k: v for k, v in sorted(tot.items()) if k not in ('pairs', 'unc')})

# link distance (author's classify_gap functions, re-implemented call)


def max_rects(ot):
    R = [(i0, i1, j0, j1) for i0 in range(ot.nx) for i1 in range(i0 + 1, ot.nx + 1)
         for j0 in range(ot.ny) for j1 in range(j0 + 1, ot.ny + 1) if ot.rect(i0, i1, j0, j1)]
    return R


def contains(rc, P):
    return 2 * rc[0] <= P[0] <= 2 * rc[1] and 2 * rc[2] <= P[1] <= 2 * rc[3]


def meet(a, b):
    return max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3])


def link(R, S, T):
    cur = {i for i, rc in enumerate(R) if contains(rc, S)}
    seen, k = set(cur), 1
    while cur:
        if any(contains(R[i], T) for i in cur):
            return k
        cur = {j for j in range(len(R)) if j not in seen and any(meet(R[i], R[j]) for i in cur)}
        seen |= cur
        k += 1
    return 99


print("\n   Per word: types, pairs, uncovered, link distance of uncovered pairs")
WORD_TYPES = defaultdict(list)
for row in cert:
    WORD_TYPES[TYPE_WORD[(row['nx'], row['ny'], row['mask'])]].append(row)
for w in words:
    rows = WORD_TYPES[w]
    npairs = sum(sum(r_['counts'].values()) + len(r_['uncovered']) for r_ in rows)
    nunc = sum(len(r_['uncovered']) for r_ in rows)
    hist = Counter()
    for r_ in rows:
        ot = AL.OT.from_mask(r_['nx'], r_['ny'], r_['mask'])
        R = max_rects(ot)
        for S, T in r_['uncovered']:
            hist[link(R, tuple(S), tuple(T))] += 1
    nfull = sum(1 for r_ in rows if not r_['uncovered'])
    print(f"   {w} [{lw[w]['subfamily']}]: {len(rows)} types ({nfull} fully certified), "
          f"{npairs} pairs, {npairs - nunc} certified, {nunc} uncovered, by k {dict(sorted(hist.items()))}")
    for r_ in rows:
        print(f"      {r_['nx']}x{r_['ny']} mask {r_['mask']:5d} {r_['shape']:22s} uncovered {len(r_['uncovered']):3d} "
              f"{[tuple(map(tuple, p)) for p in r_['uncovered']]}")

# ------------------------------------------------------------------ 4
print("\n== 4. Cross-check of certificates with rv.py on unit-gap rooms")


def auth_key(c, R):
    co = R.coord
    lem = c['lem']
    if lem in ('A', 'D'):
        return (lem,)
    if lem == 'A2':
        ax, i = c['r2']
        return ('A2', ax, co[ax][i])
    if lem == 'B':
        ax, ci, ei = c['p2']
        ay, d = c['cons'][0][0], c['cons'][0][1]
        return ('B', c['swap'], ax, co[ax][ci], co[ax][ei], co[ay][d])
    if lem == 'B2':
        al, F, E = c['p2']
        perp, opp = c['r2']
        dp = c['cons'][0][2]
        return ('B2', c['swap'], al, co[al][F], co[al][E], co[perp][opp], co[perp][dp])
    if lem == 'C':
        al1, F1, E1 = c['p1']
        al2, F2, E2 = c['p2']
        c1, c2 = c['cons']
        d1 = co[c1[0]][c1[1]]
        if c['form'] == 'same':
            perp, opp = c['r2']
            d2, oppv = co[c2[0]][c2[2]], co[perp][opp]
        else:
            d2, oppv = co[c2[0]][c2[1]], None
        return ('C', c['form'], (al1, co[al1][F1], co[al1][E1], d1), (al2, co[al2][F2], co[al2][E2], d2), oppv)
    raise ValueError(lem)


def ikey(inst):
    k = inst['key']
    return ('D',) if k[0] == 'D' else k


def val(coord, X, frac):
    i = X // 2
    if X % 2 == 0:
        return coord[i]
    return coord[i] + (coord[i + 1] - coord[i]) * frac


def run_room(ot, R, rng, fracsets, tag, stats, problems, uncovered_probe=False):
    pts = ot.interior_types()
    cache = {P: AL.arm_objects(ot, P) for P in pts}
    for a in range(len(pts)):
        for b in range(a, len(pts)):
            St, Tt = pts[a], pts[b]
            if St == Tt and St[0] % 2 == 0 and St[1] % 2 == 0:
                continue
            c = dict(lem='A', swap=0) if St == Tt else AL.certify_pair(ot, St, Tt, cache)
            for fs in fracsets:
                S = (val(R.xs, St[0], fs[0]), val(R.ys, St[1], fs[1]))
                T = (val(R.xs, Tt[0], fs[2]), val(R.ys, Tt[1], fs[3]))
                if S == T:
                    continue
                assert R.pt(S)[2:] == St and R.pt(T)[2:] == Tt and R.interior(S) and R.interior(T)
                if c is None:
                    if uncovered_probe:
                        insts = rv.all_instances(R, S, T, rng, which=('A', 'A2', 'B', 'B2', 'C', 'D'))
                        stats['uncovered probed'] += 1
                        if insts:
                            problems.append((tag, St, Tt, 'rv finds a metric-free instance', sorted({i['lem'] for i in insts})))
                        bp = rv.all_instances(R, S, T, rng, which=("B'",))
                        if bp:
                            stats["uncovered with a B' instance (metric, not a certificate)"] += 1
                    continue
                name = c['lem'] + ('-' + c['form'] if 'form' in c else '')
                insts = rv.all_instances(R, S, T, rng, which=(c['lem'],))
                ak = auth_key(c, R)
                match = [i for i in insts if ikey(i) == ak]
                if not match:
                    problems.append((tag, St, Tt, 'certificate not confirmed by rv', ak))
                    continue
                stats['cert ' + name] += 1
                for inst in match[:1] if c['lem'] != 'D' else match:
                    v, det = rv.evaluate(R, inst, rng)
                    stats['trace ' + v] += 1
                    if v not in ('ok', 'skip'):
                        problems.append((tag, St, Tt, 'path failure', inst['key'], v, det))
                    if v == 'skip':
                        stats['skip ' + name] += 1


rng = random.Random(20261122)
stats, problems = Counter(), []
t1 = time.process_time()
for row in cert:
    ot = AL.OT.from_mask(row['nx'], row['ny'], row['mask'])
    R = rv.Room(ot.nx, ot.ny, ot.cells, [Q(i) for i in range(ot.nx + 1)], [Q(j) for j in range(ot.ny + 1)])
    assert len(R.vertices()) == 10
    run_room(ot, R, rng, [(Fr(1, 3), Fr(2, 5), Fr(3, 7), Fr(5, 11))], row['shape'], stats, problems, uncovered_probe=True)
print("   stats:", dict(sorted(stats.items())))
print(f"   CPU {time.process_time() - t1:.1f} s")
for p in problems[:30]:
    print("   PROBLEM", p)
check(not problems, f"unit-gap cross-check: {len(problems)} problems")
check(stats['uncovered probed'] == 578, f"uncovered pairs probed {stats['uncovered probed']}")

# Lemma C same form with one corridor as both arms (d15-review gap)
bad = totc = 0
for key, certs in CERT.items():
    for (S, T), c in certs.items():
        if c.get('form') == 'same':
            totc += 1
            (_, F1, E1), (_, F2, E2) = c['p1'], c['p2']
            if (F1, E1) == (E2, F2) and c['cons'][0][1] == c['cons'][1][2]:
                bad += 1
check(bad == 0, f"C-same certificates using one corridor as both arms: {bad} of {totc}")

# ------------------------------------------------------------------ 5
print("\n== 5. Four explicit lattice realizations per word")
GAPS = [(3, 1, 2, 5, 1), (1, 4, 1, 1, 6), (2, 7, 3, 1, 2), (5, 2, 1, 3, 4)]


def from_ledger(k):
    vs = [tuple(p) for p in lw[k]['realization']]
    xs = sorted({v[0] for v in vs})
    ys = sorted({v[1] for v in vs})
    rk = [(xs.index(x), ys.index(y)) for x, y in vs]
    nx, ny = len(xs) - 1, len(ys) - 1
    cells = EC.inside_cells(rk, nx, ny)
    return nx, ny, cells, xs, ys


def d_degenerate(ot, R, rng, tag, stats, problems):
    """Lemma D pairs with S + T = 2V, or one coordinate mirrored in V."""
    pts = ot.interior_types()
    refl = [(R.xs[i], R.ys[j]) for i in range(ot.nx + 1) for j in range(ot.ny + 1) if ot.npt(i, j) == 3]
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            St, Tt = pts[a], pts[b]
            c = AL.certify_pair(ot, St, Tt)
            if not c or c['lem'] != 'D':
                continue
            for fs in ((Fr(1, 3), Fr(2, 5)), (Fr(1, 2), Fr(1, 2)), (Fr(4, 5), Fr(1, 7))):
                S = (val(R.xs, St[0], fs[0]), val(R.ys, St[1], fs[1]))
                for (vx, vy) in refl:
                    tg = (val(R.xs, Tt[0], Fr(3, 7)), val(R.ys, Tt[1], Fr(5, 11)))
                    for T, lab in (((2 * vx - S[0], 2 * vy - S[1]), 'S+T=2V'),
                                   ((2 * vx - S[0], tg[1]), 'x mirrored'),
                                   ((tg[0], 2 * vy - S[1]), 'y mirrored')):
                        if R.pt(T)[2:] != Tt or not R.interior(T):
                            continue
                        insts = [i for i in rv.inst_D(R, S, T)]
                        if not insts:
                            problems.append((tag, St, Tt, lab, 'no D instance in rv'))
                            continue
                        stats['D degenerate ' + lab] += 1
                        for inst in insts:
                            stats['D case ' + inst['case']] += 1
                            v, det = rv.evaluate(R, inst, rng)
                            stats['D degenerate trace ' + v] += 1
                            if v not in ('ok', 'skip'):
                                problems.append((tag, St, Tt, lab, v, det))


stats5, problems5 = Counter(), []
t1 = time.process_time()
FR_SETS = [(Fr(1, 3), Fr(2, 5), Fr(3, 7), Fr(5, 11)), (Fr(1, 2), Fr(1, 2), Fr(1, 2), Fr(1, 2))]
for w in words:
    rooms = []
    nx, ny, cells, xs, ys = from_ledger(w)
    rooms.append(('ledger', nx, ny, cells, xs, ys))
    rows = sorted(WORD_TYPES[w], key=lambda r_: -len(r_['uncovered']))
    for t in range(3):
        r_ = rows[t % len(rows)]
        g = GAPS[(t + 1 + words.index(w)) % 4]
        gy = GAPS[(t + 2 + words.index(w)) % 4][::-1]
        ot = AL.OT.from_mask(r_['nx'], r_['ny'], r_['mask'])
        xs = [sum(g[:i]) for i in range(ot.nx + 1)]
        ys = [sum(gy[:j]) for j in range(ot.ny + 1)]
        rooms.append((f"mask {r_['mask']} gaps x{tuple(g[:ot.nx])} y{tuple(gy[:ot.ny])}", ot.nx, ot.ny, ot.cells, xs, ys))
    for (lab, nx, ny, cells, xs, ys) in rooms:
        ot = AL.OT(nx, ny, cells)
        R = rv.Room(nx, ny, cells, [Q(x) for x in xs], [Q(y) for y in ys])
        vs = R.vertices()
        assert len(vs) == 10 and all(v[0].b == 0 and v[0].a.denominator == 1 for v in vs)
        before = sum(v for k_, v in stats5.items() if k_.startswith('trace'))
        run_room(ot, R, rng, FR_SETS, f"{w} {lab}", stats5, problems5)
        d_degenerate(ot, R, rng, f"{w} {lab}", stats5, problems5)
        after = sum(v for k_, v in stats5.items() if k_.startswith('trace'))
        print(f"   {w} {lab:40s} xs {xs} ys {ys}: traced {after - before} certificate instances")
print("   stats:", dict(sorted(stats5.items())))
print(f"   CPU {time.process_time() - t1:.1f} s")
for p in problems5[:30]:
    print("   PROBLEM", p)
check(not problems5, f"lattice realizations: {len(problems5)} problems")

print("\n== 5b. Lemma D: the 3 fully certified types, 4 lattice rooms each, with degenerate pairs")
stats5b, problems5b = Counter(), []
for row in cert:
    if row['uncovered']:
        continue
    ot = AL.OT.from_mask(row['nx'], row['ny'], row['mask'])
    for t, g in enumerate([(1, 1, 1, 1, 1)] + GAPS[:3]):
        gy = GAPS[(t + 1) % 4][::-1]
        xs = [sum(g[:i]) for i in range(ot.nx + 1)]
        ys = [sum(gy[:j]) for j in range(ot.ny + 1)]
        R = rv.Room(ot.nx, ot.ny, ot.cells, [Q(x) for x in xs], [Q(y) for y in ys])
        run_room(ot, R, rng, FR_SETS, f"{row['shape']} {xs} {ys}", stats5b, problems5b)
        d_degenerate(ot, R, rng, f"{row['shape']} {xs} {ys}", stats5b, problems5b)
        print(f"   {row['shape']:22s} xs {xs} ys {ys}")
print("   stats:", dict(sorted(stats5b.items())))
for p in problems5b[:30]:
    print("   PROBLEM", p)
check(not problems5b and stats5b['cert D'] == 24 and stats5b['D degenerate S+T=2V'] > 0,
      f"Lemma D rooms: {len(problems5b)} problems, D certificates traced {stats5b['cert D']}")

print("\n== 5c. One irrational room per word (ledger type, gaps in Q(sqrt 2))")
s2 = Q(0, 1)
IG = [Q(1), s2, Q(2) - s2 / 2, Q(1) + s2, Q(3, 0) / 7 + s2]
stats5c, problems5c = Counter(), []
for w in words:
    nx, ny, cells, _, _ = from_ledger(w)
    ot = AL.OT(nx, ny, cells)
    xs = [sum(IG[:i], Q(0)) for i in range(nx + 1)]
    ys = [sum(IG[::-1][:j], Q(0)) for j in range(ny + 1)]
    R = rv.Room(nx, ny, cells, xs, ys)
    run_room(ot, R, rng, FR_SETS[:1], f"{w} irrational", stats5c, problems5c)
print("   stats:", dict(sorted(stats5c.items())))
for p in problems5c[:30]:
    print("   PROBLEM", p)
check(not problems5c, f"irrational rooms: {len(problems5c)} problems")

# ------------------------------------------------------------------ 6
print("\n== 6. Ferrers word LLLLLRLRLR (d168 claim)")
fw = 'LLLLLRLRLR'
rows = WORD_TYPES[fw]
check(len(rows) == 1 and rows[0]['mask'] == 4991 and rows[0]['shape'] == '#.../##../###./####',
      f"one order type for {fw}: {[(r_['mask'], r_['shape']) for r_ in rows]}")
r_ = rows[0]
check(r_['uncovered'] == [[[1, 7], [7, 1]]], f"uncovered list {r_['uncovered']}")
ot = AL.OT.from_mask(r_['nx'], r_['ny'], r_['mask'])
top = [c for c in ot.cells if c[1] == 3]
right = [c for c in ot.cells if c[0] == 3]
check(top == [(0, 3)] and right == [(3, 0)],
      "(1,7) is the open top cell (0,3) and (7,1) is the open bottom-right cell (3,0)")
pts = ot.interior_types()
inside_top = [P for P in pts if 0 < P[0] < 2 and 6 < P[1] <= 8]
inside_right = [P for P in pts if 6 < P[0] <= 8 and 0 < P[1] < 2]
check(inside_top == [(1, 7)] and inside_right == [(7, 1)],
      f"position types with a point strictly inside those cells: {inside_top}, {inside_right}")
c = Counter(v['lem'] + ('-' + v['form'] if 'form' in v else '') for v in CERT[(4, 4, 4991)].values())
print("   certificates for mask 4991:", dict(c), "pairs", sum(c.values()) + 1)

print(f"\nTOTAL {NPASS} PASS, {NFAIL} FAIL, CPU {time.process_time() - T0:.1f} s")
