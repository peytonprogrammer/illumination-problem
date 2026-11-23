"""d102 negative control: corrupt saved witnesses and confirm the replay tracer rejects them.

For a random room sample, each lit witness (S, T, dx, dy, m) is corrupted three ways:
  target  -- replace T by another interior lattice point of the room;
  sign    -- negate dx (or dy when dx == 0);
  steps   -- require arrival at exactly m - 1 steps.
A corruption counts as accepted only if the tracer reaches the corrupted target at exactly the
corrupted step count. Usage: python3 -B control.py SEED NROOMS
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import replay as R  # noqa: E402

seed, N = int(sys.argv[1]), int(sys.argv[2])
random.seed(seed)
keep = set(random.sample(range(780565), N))
acc = {'target': 0, 'sign': 0, 'steps': 0}
tried = {'target': 0, 'sign': 0, 'steps': 0}
for idx, (cells, rows) in enumerate(R.rooms('witnesses.txt.gz')):
    if idx not in keep:
        continue
    cs = set(cells)
    inter = [p for p in R.I.lattice_pts(cs) if R.I.vstatus(cs, p) == 'int']
    for r in rows:
        if r[5] != 'L':
            continue
        S, T = (int(r[1]), int(r[2])), (int(r[3]), int(r[4]))
        dx, dy, m = int(r[7]), int(r[8]), int(r[9])
        assert R.trace(cs, S, T, dx, dy, m) == m
        others = [p for p in inter if p not in (S, T)]
        if others:
            T2 = random.choice(others)
            tried['target'] += 1
            acc['target'] += R.trace(cs, S, T2, dx, dy, m) == m
        ndx, ndy = (-dx, dy) if dx else (dx, -dy)
        tried['sign'] += 1
        acc['sign'] += R.trace(cs, S, T, ndx, ndy, m) == m
        if m > 1:
            tried['steps'] += 1
            acc['steps'] += R.trace(cs, S, T, dx, dy, m - 1) == m - 1
print('corruptions tried', tried)
print('corruptions accepted', acc)
