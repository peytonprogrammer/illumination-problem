"""Replay sampled witnesses with tracer.py and with own room checks."""
import sys, json, math, random
from collections import Counter
from tracer import check_witness
from rooms import has_hole, has_pinch, walls, marks
res = Counter(); bad = []
per_file = Counter()
for path in sys.argv[1:]:
    for line in open(path):
        ok, first, m, endok, R = check_witness(line)
        cells = tuple(R.s)
        assert not has_hole(cells) and not has_pinch(R.s) and walls(R.s) <= 20 and len(cells) == 21
        good = ok and endok and first == m
        res['ok' if good else 'FAIL'] += 1
        per_file[path] += 1
        if not good: bad.append(line.strip())
print(json.dumps({'checked': sum(res.values()), 'result': dict(res), 'per_file': dict(per_file), 'bad': bad[:5]}))
