"""Compare rooms.py (independent) with d205 validation/optimized.counts and d9 Part A."""
import sys
from pathlib import Path
here = Path(__file__).resolve().parent
d205 = here.parent / 'd205-census-a21'
mine = {}
for line in (here / 'small_counts.txt').read_text().splitlines():
    v = line.split()
    if v[0] == 'ROW':
        a, w, r, s, d = map(int, v[1:]); mine[a, w] = (r, s, d)
theirs = {}; expect = {}; shot = {}
for line in (d205 / 'validation/optimized.counts').read_text().splitlines():
    v = line.split()
    if v[:2] == ['#', 'count']: theirs[int(v[3]), int(v[5])] = int(v[7])
    if v[0] == 'EXPECT': expect[int(v[1]), int(v[2])] = int(v[3])
    if v[0] == 'SHOT': shot[int(v[1]), int(v[2])] = (int(v[4]), int(v[5]), int(v[6]))
partA = {}
for line in (d205.parent / 'd9-census-w22/partA-totals.md').read_text().splitlines():
    f = [x.strip().replace(',', '') for x in line.strip('|').split('|')]
    if len(f) == 19 and f[0].isdigit():
        w, a = int(f[0]), int(f[1])
        if a <= 11 and w <= 20: partA[a, w] = (int(f[2]), int(f[9]), int(f[11]))
bad = 0
for k in sorted(set(mine) | set(theirs) | set(partA)):
    r, s, d = mine.get(k, (0, 0, 0))
    ok = (theirs.get(k, 0) == r and expect.get(k, 0) == s + d and partA.get(k, (0, 0, 0)) == (r, s, d)
          and shot.get(k, (0, 0, 0))[:2] == ((s, d) if s + d else (0, 0)))
    if not ok:
        bad += 1; print('MISMATCH', k, (r, s, d), theirs.get(k), expect.get(k), partA.get(k), shot.get(k))
print('buckets', len(mine), 'rooms', sum(v[0] for v in mine.values()), 'same', sum(v[1] for v in mine.values()),
      'diff', sum(v[2] for v in mine.values()), 'mismatches', bad)
