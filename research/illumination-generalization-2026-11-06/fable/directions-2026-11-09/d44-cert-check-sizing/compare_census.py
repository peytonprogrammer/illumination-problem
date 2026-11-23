"""Compare count_rooms free counts per (W, area) with the d9 census totals."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
d = json.load(open(HERE.parent / 'd9-census-w22' / 'census_totals.json'))['per_W_area']
mine = {}
for line in open(sys.argv[1]):
    m = re.match(r'\s+W (\d+) area (\d+) fixed (\d+) free (\d+)', line)
    if m:
        W, a, fx, fr = map(int, m.groups())
        mine[(W, a)] = fr
amax = max(a for _, a in mine)
ok = bad = 0
for k, v in d.items():
    W, a = map(int, k.split(','))
    if a > amax or W > 20:
        continue
    if mine.get((W, a)) == v['rooms']:
        ok += 1
    else:
        bad += 1
        print('MISMATCH', W, a, 'census', v['rooms'], 'mine', mine.get((W, a)))
print('compared (W, area) cells with census rows:', ok + bad, 'match', ok, 'mismatch', bad)
