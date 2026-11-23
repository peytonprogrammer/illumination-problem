"""d52: the positive covers of P6's quotient (delta = 4, r = 12), identified up to lattice isometry."""
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fold import *  # noqa
import enum_P  # noqa
from named import ROOMS  # noqa
from sanity import full_canon, normalise, named  # noqa

G6, _ = from_cells(ROOMS['P6'])
Gn = normalise(G6, (0, 0))
K = quotient(Gn, B(Gn, (0, 0)))
res, stats, st = enum_P.covers(K, 3, 4, 12)
seen = {}
for r in res:
    fc = full_canon(r['P'])
    if fc in seen:
        continue
    pos, ok, emb = develop(r['P'])
    cells = sorted(pos.values())
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    seen[fc] = cells
    print('room: n=%d r=%d embedded=%s true room=%s is P6=%s bbox %dx%d pairs=%s' % (
        r['n'], r['r'], emb, is_room(r['P']), fc == named['P6'],
        max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, r['pos']))
    for Y in range(max(ys), min(ys) - 1, -1):
        print('   ' + ''.join('#' if (X, Y) in set(cells) else '.' for X in range(min(xs), max(xs) + 1)))
d31 = json.load(open(HERE.parent / 'd31-run-dark-min' / 'found.json'))
print('d31 found.json entries:', len(d31))
for e in d31:
    c = {tuple(x) for x in e['cells']}
    print('  d31 entry n=%d matches:' % len(c), [i for i, fc in enumerate(seen) if fc == full_canon(from_cells(c)[0])])
