"""Coordinator cross-check for d237: decide every 1500th production disc, and the dark disc,
with the validator's independent unfolding and decider (validator/validate_w26.py).
Prediction, written first: same verdict on every sampled pair (P = 0.95)."""
import sys, time
from collections import Counter
sys.path.insert(0, 'validator'); import validate_w26 as V
lines = [l for l in open('astra/production/jobs.txt').read().split('\n') if l]
def parse(line):
    f = line.split(); n = list(map(int, f[3:]))
    cells = [n[i:i + 6] for i in range(0, len(n), 6)]
    assert len(cells) == int(f[0])
    return int(f[0]), int(f[1]), f[2], [c[2:6] for c in cells]
import json
_c = json.loads(open('astra/dark.tsv').read().split('\n')[1].split('\t')[3])
dark_line = ' '.join(map(str, [15, 22, 'EMBEDDED'] + [x for c in _c for x in c]))  # exact line; a prefix match picked another disc
assert lines.count(dark_line) == 1
t = time.process_time(); tot = lit = 0; by = Counter(); notlit = []
for l in lines[::1500] + [dark_line]:
    a, w, b, nb = parse(l)
    comp, info = V.links(nb); (ls, ns, complete), srcs = V.light(nb, comp, info)
    k = len(srcs); p = k * (k - 1) // 2; tot += p; lit += len(ls); by[b] += 1
    if len(ls) != p: notlit.append((a, w, b, p - len(ls), ns, complete))
print(f"sample discs {sum(by.values())} {dict(by)}, pairs {tot}, lit {lit}, not lit {tot - lit}: {notlit}, cpu {time.process_time() - t:.1f}s")
