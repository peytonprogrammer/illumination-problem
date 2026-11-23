"""Count candidate non-Galois targets N for design B from the d6 Hurwitz census.

A target is a genus-0 pillowcase cover tuple (cycle lengths <= 3, up to conjugation).
Keep degree d and zero count z with z in {1, 2} and d <= 4z+1 (d <= 4z if d even),
singular points in >= 3 corner classes, and some corner with a 2-cycle (a regular point,
needed over A for the marks).  Counts are tuples, not braid orbits.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
tot = 0
for d in range(3, 10):
    data = json.load(open(HERE.parent / 'd6-hurwitz-census' / ('census_n%d.json' % d)))
    by_z = {}
    for c in data['summary']['nielsen']:
        cts = c['cts']
        z = sum(ct.count(3) for ct in cts)
        sing = sum(1 for ct in cts if any(L != 2 for L in ct))
        if z not in (1, 2) or sing < 3:
            continue
        if d > (4 * z if d % 2 == 0 else 4 * z + 1):
            continue
        if not any(2 in ct for ct in cts):
            continue
        by_z[z] = by_z.get(z, 0) + c['tuples']
    tot += sum(by_z.values())
    print('d %d targets by z %s' % (d, by_z))
print('total candidate target tuples', tot)
