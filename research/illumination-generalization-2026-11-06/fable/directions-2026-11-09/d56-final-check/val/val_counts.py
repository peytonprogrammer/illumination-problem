"""Reconcile room counts from check SUMMARY outputs ('# rooms_WA W<w>_A<a>:rooms/reduced/c3') with
d9 census_totals.md (rooms per (W, area), W <= 22) and partA-totals.json (rooms, reduced, c3).
usage: python3 -B val_counts.py MODE FILE...   MODE = rooms (census rooms) or c3 (Part A reduced, c3)"""
import sys, json, re
from pathlib import Path
D9 = Path(__file__).resolve().parent.parent.parent / 'd9-census-w22'
mode = sys.argv[1]
got = {}
for fn in sys.argv[2:]:
    for line in open(fn):
        if line.startswith('# rooms_WA'):
            for w, a, r, red, c3 in re.findall(r'W(\d+)_A(\d+):(\d+)/(\d+)/(\d+)', line):
                k = (int(w), int(a)); o = got.setdefault(k, [0, 0, 0])
                o[0] += int(r); o[1] += int(red); o[2] += int(c3)
bad = 0
if mode == 'rooms':
    ref = {}
    for line in open(D9 / 'census_totals.md'):
        f = [x.strip().replace(',', '') for x in line.split('|')[1:4]]
        if len(f) == 3 and f[0].isdigit():
            ref[(int(f[0]), int(f[1]))] = int(f[2])
    for k in sorted(got):
        if k[0] > 22: continue
        ok = ref.get(k) == got[k][0]; bad += not ok
        print('W %2d area %2d rooms %10d census %10s %s' % (k[0], k[1], got[k][0], ref.get(k), 'OK' if ok else 'MISMATCH'))
else:
    rows = json.load(open(D9 / 'partA-totals.json'))['rows']
    for k in sorted(got):
        r = rows.get('%d,%d' % k, {})
        ok = (r.get('rooms'), r.get('reduced'), r.get('c3')) == tuple(got[k]); bad += not ok
        print('W %2d area %2d rooms %8d reduced %5d c3 %7d | partA %s %s %s %s' % (k + tuple(got[k]) + (r.get('rooms'), r.get('reduced'), r.get('c3'), 'OK' if ok else 'MISMATCH')))
print('cells', len(got), 'mismatches', bad)
