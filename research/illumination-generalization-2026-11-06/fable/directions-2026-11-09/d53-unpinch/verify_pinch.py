"""Darkness checks for Monteil's pinched room (slide 4), k = 1.

1. Fold (Tokarsky) condition: marks and pinch are A points; every B (odd, odd)
   and C (mixed parity) lattice point of the closed room is a corner.
2. Origami shooting (shootall, pinch Q = (4,4) is a corner: two separate runs).
3. Independent plane tracer from S and from T: every primitive direction with
   |dx| + |dy| <= BOUND2, up to MAXREFL reflections.  Two pinch conventions:
     die     -- Q is a vertex; a path that reaches Q stops.
     reflect -- Q is a flat point of the straight diagonal wall x + y = 8 that
                the hole's corner touches; the path reflects in that wall and
                passes from one wedge to the other.
   The tracer reports how many paths reach T and how many reach Q.
4. orbit45 input line written to work/pinch_k1.orbit.
usage: python3 -B verify_pinch.py BOUND1 BOUND2 MAXREFL
"""
import subprocess
import sys
from collections import Counter
from fractions import Fraction as Fr
from math import gcd

import rooms53 as Q
import slit45 as S

b1, b2, maxr = map(int, sys.argv[1:4])
tiles = sorted(Q.base_tiles(1))
o = S.build(tiles)
Sm, Tm = Q.MARKS0
print('tiles', len(tiles), 'pinch type', o['ptype'][Q.Q0])

# 1. fold condition
corners = set(Q.P0)
bad = []
for p, t in sorted(o['ptype'].items()):
    cls = 'A' if p[0] % 2 == 0 and p[1] % 2 == 0 else 'B' if p[0] % 2 and p[1] % 2 else 'C'
    if cls != 'A' and t != 'C':
        bad.append(p)
    if cls == 'A':
        print('   A point', p, 'type', t)
print('1. fold condition: B/C points that are not corners:', bad)

# 2. shootall
elig = [p for p in o['pts'] if o['ptype'][p] == 'I']
S.write_origami(o, 'work/pinch_k1.origami', elig, Sm, Tm)
print('2. shootall', b1, subprocess.run(['./shootall', str(b1), 'work/pinch_k1.origami'], capture_output=True, text=True).stdout.strip().replace('\n', ' | '))

# 3. plane tracer
P = Q.P0
segs = [(P[i], P[(i + 1) % len(P)]) for i in range(len(P))]
QQ = (Fr(4), Fr(4))


def run(src, dst, d, conv):
    Pp = (Fr(src[0]), Fr(src[1]))
    D = d
    nq = 0
    for nrefl in range(maxr + 1):
        best = None
        for i, (a, b) in enumerate(segs):
            e = (b[0] - a[0], b[1] - a[1])
            den = D[0] * e[1] - D[1] * e[0]
            if den == 0:
                continue
            w = (a[0] - Pp[0], a[1] - Pp[1])
            t = Fr(w[0] * e[1] - w[1] * e[0], den)
            u = Fr(w[0] * D[1] - w[1] * D[0], den)
            if t > 0 and 0 <= u <= 1 and (best is None or t < best[0]):
                best = (t, i)
        t, i = best
        ev = None
        for c in [dst] + sorted(corners):
            w = (c[0] - Pp[0], c[1] - Pp[1])
            if w[0] * D[1] - w[1] * D[0] == 0:
                tc = w[0] / D[0] if D[0] else w[1] / D[1]
                if 0 < tc <= t and (ev is None or tc < ev[0]):
                    ev = (tc, c)
        if ev is not None:
            tc, c = ev
            if c == dst:
                return 'T', nrefl, nq
            if c == Q.Q0:
                nq += 1
                if conv == 'die':
                    return 'Q', nrefl, nq
                Pp = QQ
                D = (-D[1], -D[0])          # reflect in the diagonal x + y = 8
                continue
            return 'corner', nrefl, nq
        Pp = (Pp[0] + t * D[0], Pp[1] + t * D[1])
        a, b = segs[i]
        D = S.reflect(D, (b[0] - a[0], b[1] - a[1]))
    return 'max', maxr, nq


for conv in ('die', 'reflect'):
    for src, dst, name in ((Sm, Tm, 'S'), (Tm, Sm, 'T')):
        cnt = Counter()
        reachT = []
        for dx in range(-b2, b2 + 1):
            for dy in range(-b2, b2 + 1):
                if abs(dx) + abs(dy) > b2 or gcd(dx, dy) != 1:
                    continue
                tag, n, nq = run(src, dst, (dx, dy), conv)
                cnt[tag] += 1
                cnt['visits Q'] += nq > 0
                if tag == 'T':
                    reachT.append(((dx, dy), n))
        print('3. plane tracer, pinch %-7s from %s: directions %d %s reaching the other mark: %s' %
              (conv, name, sum(v for k, v in cnt.items() if k != 'visits Q'), dict(cnt), reachT))

with open('work/pinch_k1.orbit', 'w') as fh:
    fh.write(S.orbit_line(o, Sm, Tm) + '  # monteil p4 pinched k=1\n')
print('4. orbit45 line written, nsq', o['nsq'])

# control: a non-lattice start that does reach Q, to show both conventions are exercised
for conv in ('die', 'reflect'):
    src = (Fr(3), Fr(9, 2))
    print('5. control from (3, 9/2) direction (2,-1), pinch %-7s:' % conv, run(src, (Fr(99), Fr(99)), (2, -1), conv))
