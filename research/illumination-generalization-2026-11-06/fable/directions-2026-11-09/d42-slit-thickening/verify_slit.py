"""Darkness checks for Monteil's slit room (k = 1).

1. Origami shooting (shootall) to direction bound BOUND1.
2. Independent plane tracer: from S, every primitive direction (dx, dy) with
   |dx| + |dy| <= BOUND2, followed for up to MAXREFL reflections or until it
   dies at a corner; reports any direction that reaches T.
3. Fold (Tokarsky) condition: every lattice point of class B (odd, odd) or
   C (mixed parity) in the closed room is a corner (polygon vertex, slit foot
   or slit tip); the marks are A points (even, even).
usage: python3 -B verify_slit.py BOUND1 BOUND2 MAXREFL
"""
import subprocess
import sys
from fractions import Fraction as Fr
from math import gcd

import rooms42 as Q
import slit45 as S

b1, b2, maxr = map(int, sys.argv[1:4])
room = Q.make_room(1)
o = S.build(room['tiles'], room['slit'])
Sm, Tm = room['marks']
elig = [p for p in o['pts'] if o['ptype'][p] == 'I']
S.write_origami(o, 'work/slit_k1.origami', elig, Sm, Tm)
print('1. shootall', b1, subprocess.run(['./shootall', str(b1), 'work/slit_k1.origami'], capture_output=True, text=True).stdout.strip().replace('\n', ' | '))

poly = Q.clean(Q.P0)
segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))] + [Q.SLIT0]
corners = set(poly) | set(Q.SLIT0)
print('   polygon corners', len(poly), 'slit', Q.SLIT0, 'total corner points', len(corners))


def run(d):
    """Follow from S in direction d; return ('T', nrefl) / ('corner', nrefl) / ('max', nrefl)."""
    P = (Fr(Sm[0]), Fr(Sm[1]))
    D = d
    for nrefl in range(maxr + 1):
        best = None
        for i, (a, b) in enumerate(segs):
            e = (b[0] - a[0], b[1] - a[1])
            den = D[0] * e[1] - D[1] * e[0]
            if den == 0:
                continue
            w = (a[0] - P[0], a[1] - P[1])
            t = Fr(w[0] * e[1] - w[1] * e[0], den)
            u = Fr(w[0] * D[1] - w[1] * D[0], den)
            if t > 0 and 0 <= u <= 1 and (best is None or t < best[0]):
                best = (t, i)
        t, i = best
        for c, tag in [(Tm, 'T')] + [(c, 'corner') for c in corners]:
            w = (c[0] - P[0], c[1] - P[1])
            if w[0] * D[1] - w[1] * D[0] == 0:
                tc = w[0] / D[0] if D[0] else w[1] / D[1]
                if 0 < tc <= t:
                    return tag, nrefl
        P = (P[0] + t * D[0], P[1] + t * D[1])
        a, b = segs[i]
        D = S.reflect(D, (b[0] - a[0], b[1] - a[1]))
    return 'max', maxr


from collections import Counter
cnt = Counter()
hitsT = []
for dx in range(-b2, b2 + 1):
    for dy in range(-b2, b2 + 1):
        if abs(dx) + abs(dy) > b2 or gcd(dx, dy) != 1:
            continue
        tag, n = run((dx, dy))
        cnt[tag] += 1
        if tag == 'T':
            hitsT.append(((dx, dy), n))
print('2. plane tracer: directions', sum(cnt.values()), dict(cnt), 'reaching T:', hitsT)

bad = []
xs = [p[0] for p in poly]
ys = [p[1] for p in poly]
for x in range(min(xs), max(xs) + 1):
    for y in range(min(ys), max(ys) + 1):
        if (x, y) not in o['ptype']:
            continue      # outside the closed room
        cls = 'A' if x % 2 == 0 and y % 2 == 0 else 'B' if x % 2 and y % 2 else 'C'
        if cls != 'A' and (x, y) not in corners:
            bad.append((x, y))
        if cls == 'A' and o['ptype'][(x, y)] == 'I':
            print('   interior A point', (x, y))
print('3. fold condition: B/C points of the closed room that are not corners:', bad)
