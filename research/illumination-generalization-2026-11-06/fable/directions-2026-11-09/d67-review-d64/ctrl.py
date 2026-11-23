"""d67 controls for indep.py's billiard code.
1  Negative control: P6 (cells retyped from d52 named.py). Its known dark same-class pair must get no
   witness; the other P6 pairs (all classes, all interior points) are reported.
2  Per-target consistency on the 37 d64 point-level pairs: direction parity classes that reach T
   for max(p, q) <= H. d64 says no path of target class x exists. Target class of a direction
   (p, q) from an a-point is a + (p mod 2, q mod 2)... reported as the parity (p%2, q%2); d64's
   verify_billiard maps (1,0)->b, (1,1)->c, (0,1)->d (relative to a).
Usage: python3 -B ctrl.py H
"""
import re
import sys
import time
import json
from itertools import combinations
from indep import shoot, dirs_upto, lattice_pts, vstatus, light_from, D64

H = int(sys.argv[1])
t0 = time.process_time()
Q5 = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
P6 = Q5 | {(i, -j - 1) for i, j in Q5} | {(5 - i, -j - 1) for i, j in Q5} | {(i, 5 - j) for i, j in Q5}
ints = sorted(p for p in lattice_pts(P6) if vstatus(P6, p) == 'int')
print('P6 cells', len(P6), 'interior points', ints)
for S, T in combinations(ints, 2):
    w = light_from(P6, S, {T}, H)
    same = (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0
    print('P6 %s %s same-class=%s : %s' % (S, T, same, w.get(T, 'NO WITNESS at H<=%d' % H)))

XN = {(1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}
norm = sorted([r for r in json.load(open(D64 / 'data' / 'covers.json'))['rooms'] if r['normalized']],
              key=lambda r: (r['n'], r['cells']))
pat = re.compile(r'room (\d+) a=\((\d), (\d)\) x=(\w) S,T=\(\((\d+), (\d+)\), \((\d+), (\d+)\)\)')
bad = 0
for m in pat.finditer(open(D64 / 'logs' / 'pointlevel.log').read()):
    idx = int(m.group(1))
    S = (int(m.group(5)), int(m.group(6)))
    T = (int(m.group(7)), int(m.group(8)))
    cs = set(tuple(x) for x in norm[idx]['cells'])
    cls = set()
    for p, q in dirs_upto(H):
        for sx in ((1, -1) if p else (1,)):
            for sy in ((1, -1) if q else (1,)):
                if shoot(cs, S, p, q, sx, sy, {T}):
                    cls.add(XN[(p % 2, q % 2)])
    flag = m.group(4) in cls
    bad += flag
    print('PL room %d %s %s x=%s reached by classes %s %s' % (idx, S, T, m.group(4), sorted(cls),
                                                            'CONTRADICTS x-dark' if flag else 'ok'))
print('point-level contradictions', bad, 'CPU %.1f' % (time.process_time() - t0))
