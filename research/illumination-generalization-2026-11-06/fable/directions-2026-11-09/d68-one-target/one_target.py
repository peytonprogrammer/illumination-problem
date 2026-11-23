"""d68: the one-B-target sub-case (OL1) of d66's lemma OL, checked on existing data only.

Reads d64-finite-case/data/covers.json (all 4,776 rooms) and d66-pair-level/pair_level.json.
No search. For every room and every class y (absolute parity class of lattice points):
  star counts  cvx_y, smooth_y, pinch_y, rfx_y, int_y  (cells around a point: 1, 2 adj, 2 diag, 3, 4)
  identity     n == cvx_y + 2 smooth_y + 3 rfx_y + 4 int_y + 2 pinch_y   (each cell has one y-corner)
  geometric Q  no interior and no smooth point of class y (d66 section 1 criterion)
Checks:
  (1) the identity for all 4 classes of all rooms;
  (2) geometric Q agrees with the block-system type 'Q' in pair_level.json (where present);
  (3) every room with two or more Q classes has n <= (3 r_Q + v_Q) / 2 <= 2 r + 2;
  (4) OL1 pairs (class a of type B, exactly one B among the other three classes): area,
      W, d66 pair verdict, and whether the straight segment S T is a direct light path.
Usage: python3 -B one_target.py      (prints the log)
"""
import json
import time
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from pathlib import Path

D = Path(__file__).resolve().parent.parent


def star(cs, p):
    i, j = p
    q = [(i - 1, j - 1) in cs, (i, j - 1) in cs, (i, j) in cs, (i - 1, j) in cs]   # cyclic order
    k = sum(q)
    if k == 2:
        return 'pinch' if q[0] == q[2] else 'smooth'
    return {0: 'out', 1: 'cvx', 3: 'rfx', 4: 'int'}[k]


def classify(cs):
    pts = {(i + di, j + dj) for (i, j) in cs for di in (0, 1) for dj in (0, 1)}
    st = {p: star(cs, p) for p in pts}
    cnt = {y: Counter() for y in ((0, 0), (0, 1), (1, 0), (1, 1))}
    for p, s in st.items():
        cnt[(p[0] % 2, p[1] % 2)][s] += 1
    return st, cnt


def direct(cs, S, T):
    """Open segment S T lies in the room interior: every piece between grid crossings has its
    midpoint in a cell, and every crossing is an interior lattice point or an edge point with
    both adjacent cells present. Axis-parallel segments: both cells along each unit step."""
    dx, dy = T[0] - S[0], T[1] - S[1]
    if dx == 0 or dy == 0:
        ux, uy = (dx > 0) - (dx < 0), (dy > 0) - (dy < 0)
        L = abs(dx) + abs(dy)
        for k in range(L):
            x, y = S[0] + k * ux, S[1] + k * uy
            if k and star(cs, (x, y)) != 'int':
                return False
            if dx:
                a = min(x, x + ux)
                if (a, y) not in cs or (a, y - 1) not in cs:
                    return False
            else:
                b = min(y, y + uy)
                if (x, b) not in cs or (x - 1, b) not in cs:
                    return False
        return True
    ts = sorted({F(k, abs(dx)) for k in range(abs(dx) + 1)} | {F(k, abs(dy)) for k in range(abs(dy) + 1)})
    for t0, t1 in zip(ts, ts[1:]):
        m = (t0 + t1) / 2
        x, y = S[0] + m * dx, S[1] + m * dy
        if (int(x // 1), int(y // 1)) not in cs:
            return False
    for t in ts[1:-1]:
        x, y = S[0] + t * dx, S[1] + t * dy
        if x.denominator == 1 and y.denominator == 1:
            if star(cs, (int(x), int(y))) != 'int':
                return False
        elif x.denominator == 1:                       # crossing a vertical line
            if (int(x) - 1, int(y // 1)) not in cs or (int(x), int(y // 1)) not in cs:
                return False
        else:
            if (int(x // 1), int(y) - 1) not in cs or (int(x // 1), int(y)) not in cs:
                return False
    return True


def main():
    t0 = time.process_time()
    allrooms = json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
    norm = sorted((r for r in allrooms if r['normalized']), key=lambda r: (r['n'], r['cells']))
    pl = {R['name']: R for R in json.load(open(D / 'd66-pair-level' / 'pair_level.json'))['rooms']}
    ident_bad = 0
    qtype_agree = qtype_dis = 0
    twoQ = []
    ol1 = []
    for idx, r in enumerate(norm):
        cs = set(map(tuple, r['cells']))
        n = len(cs)
        st, cnt = classify(cs)
        rr = sum(c['rfx'] for c in cnt.values())
        vv = sum(c['cvx'] for c in cnt.values())
        assert vv == rr + 4
        for y, c in cnt.items():
            if n != c['cvx'] + 2 * c['smooth'] + 3 * c['rfx'] + 4 * c['int'] + 2 * c['pinch']:
                ident_bad += 1
        Q = [y for y, c in cnt.items() if c['int'] == 0 and c['smooth'] == 0]
        name = 'cov%d' % idx
        if name in pl:
            for y in cnt:
                key = '%d%d' % y
                isq = pl[name]['types'][key] == 'Q'
                if isq == (y in Q):
                    qtype_agree += 1
                else:
                    qtype_dis += 1
        if len(Q) >= 2:
            rq = sum(cnt[y]['rfx'] for y in Q[:2])
            vq = sum(cnt[y]['cvx'] for y in Q[:2])
            assert 2 * n == 3 * rq + vq, (name, n, rq, vq)
            assert n <= 2 * rr + 2
            diffs = tuple(sorted(((Q[0][0] - Q[1][0]) % 2, (Q[0][1] - Q[1][1]) % 2) for _ in [0]))
            twoQ.append((name, n, rr, len(Q), diffs[0], name in pl and pl[name]['Rstar']))
        if name in pl and pl[name]['Rstar']:
            ty = pl[name]['types']
            for a in cnt:
                if ty['%d%d' % a] != 'B':
                    continue
                others = [y for y in cnt if y != a]
                if sum(ty['%d%d' % y] == 'B' for y in others) != 1:
                    continue
                ints = sorted(p for p, s in st.items() if s == 'int' and (p[0] % 2, p[1] % 2) == a)
                xB = [y for y in others if ty['%d%d' % y] == 'B'][0]
                for S, T in combinations(ints, 2):
                    ol1.append((name, n, rr, a, xB, S, T, direct(cs, S, T), pl[name]['counts']))
    print('rooms read:', len(allrooms), 'normalized:', len(norm))
    print('(1) star identity failures over all classes:', ident_bad)
    print('(2) geometric Q vs block type Q (pair_level rooms): agree', qtype_agree, 'disagree', qtype_dis)
    print('(3) normalized rooms with >= 2 Q classes:', len(twoQ),
          ' max n', max(t[1] for t in twoQ), ' max (n - 2r - 2)', max(t[1] - 2 * t[2] - 2 for t in twoQ))
    print('    by #Q:', dict(Counter(t[3] for t in twoQ)), ' Q-pair difference:', dict(Counter(t[4] for t in twoQ)),
          ' R*:', sum(t[5] for t in twoQ))
    print('    area histogram:', dict(sorted(Counter(t[1] for t in twoQ).items())))
    print('    in R*, area histogram:', dict(sorted(Counter(t[1] for t in twoQ if t[5]).items())))
    # all (not only normalized) rooms for the bound
    worst = 0
    for r in allrooms:
        cs = set(map(tuple, r['cells']))
        st, cnt = classify(cs)
        Q = [y for y, c in cnt.items() if c['int'] == 0 and c['smooth'] == 0]
        if len(Q) >= 2:
            rr = sum(c['rfx'] for c in cnt.values())
            worst = max(worst, len(cs) - 2 * rr - 2)
    print('    all 4,776 rooms: max (n - 2r - 2) over rooms with >= 2 Q classes:', worst)
    print('(4) OL1 pairs:', len(ol1), 'in', len({o[0] for o in ol1}), 'rooms;',
          'max area', max(o[1] for o in ol1), '; area >= 21:', sum(o[1] >= 21 for o in ol1))
    for o in ol1:
        name, n, rr, a, xB, S, T, dl, c = o
        print('   ', name, 'n', n, 'r', rr, 'a', a, 'x', xB, 'S', S, 'T', T, 'direct', dl,
              'room pairs lit', c.get('pair_lit'), '/', c.get('pairs'))
    print('    direct segment lights:', sum(o[7] for o in ol1), 'of', len(ol1))
    print('CPU %.2f s' % (time.process_time() - t0))


if __name__ == '__main__':
    main()
