"""D87: are all same-parity interior lattice pairs of the b=7 cross lit within |D| <= L?"""
from fractions import Fraction as F
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from billiard import run, incid
from replay_cross import cross

b = int(sys.argv[1]) if len(sys.argv) > 1 else 7
L = int(sys.argv[2]) if len(sys.argv) > 2 else 30
c = cross(b)
pts = sorted({(x + i, y + j) for x, y in c for i in (0, 1) for j in (0, 1) if incid(c, (x + i, y + j)) == 4})
t0 = time.process_time()
unlit = []
pairs = 0
seen = set()
for S in pts:
    reached = set()
    for dx in range(-L, L + 1, 2):
        for dy in range(-L, L + 1, 2):
            if (dx, dy) == (0, 0) or dx * dx + dy * dy > L * L or dx == 0 or dy == 0:
                continue
            try:
                r = run(c, S, (dx, dy), 1)
            except RuntimeError:
                continue
            if r['ok']:
                e = r['end']
                if e[0].denominator == 1 and e[1].denominator == 1:
                    reached.add((int(e[0]), int(e[1])))
    for T in pts:
        if T != S and (T[0] - S[0]) % 2 == 0 and (T[1] - S[1]) % 2 == 0:
            key = frozenset((S, T))
            if key in seen:
                continue
            seen.add(key)
            pairs += 1
            if T not in reached:
                unlit.append((S, T))
print(f'cross b={b}: {len(pts)} interior lattice points, {pairs} unordered same-parity pairs, '
      f'nonaxial |D|<={L}; unlit by this search: {len(unlit)} {unlit[:10]}')
print(f'cpu {time.process_time() - t0:.1f}s')
