"""d46 requirement 2 (enumerator level): pattern-level F* (FSTAR = 1, production) against
room-level F* recomputed from each materialised room's cells and its actual area (FSTAR = 2).
Both campaigns must have the same NJ, SPLIT, W and area range, so job j covers the same shapes.
For every job present in both, the per-(W, area) counts of rooms passing F* (and, if both ran
the check, rooms checked, pairs, and positives) must be identical.
usage: val_fstar_rooms.py PRODUCTION_DIR ROOMLEVEL_DIR
"""
import json, sys
from pathlib import Path

def cells(f):
    out = {}
    for ln in Path(f).read_text().splitlines():
        if ln.startswith('CELL'):
            v = ln.split(); out[(int(v[2]), int(v[4]))] = tuple(int(v[i]) for i in (10, 12, 14, 16))
    return out

A, B = Path(sys.argv[1]), Path(sys.argv[2])
ca, cb = json.loads((A / 'config.json').read_text()), json.loads((B / 'config.json').read_text())
assert ca['nj'] == cb['nj'] and ca['split'] == cb['split'] and ca['args'][:5] == cb['args'][:5]
assert ca['args'][5] == 1 and cb['args'][5] == 2
jobs = sorted(set(p.name for p in A.glob('job_*.out')) & set(p.name for p in B.glob('job_*.out')))
bad = 0; tot = [0, 0]
for j in jobs:
    x, y = cells(A / j), cells(B / j)
    keys = set(x) | set(y)
    for k in sorted(keys):
        px, py = x.get(k, (0, 0, 0, 0)), y.get(k, (0, 0, 0, 0))
        tot[0] += px[0]; tot[1] += py[0]
        same = px[0] == py[0] and (not (ca['args'][7] and cb['args'][7]) or px == py)
        if not same:
            bad += 1; print('MISMATCH', j, 'W %d area %d' % k, 'pattern-level', px, 'room-level', py)
print('%s vs %s: jobs compared %d, rooms passing F*: pattern-level %d room-level %d, mismatching cells %d'
      % (A.name, B.name, len(jobs), tot[0], tot[1], bad))
