"""Differential test: production verify_plane.c vs independent tracer.py.

For random strictly simple rooms (area 6..11, from rooms.py) plus the 22-wall
control, random interior source, random primitive direction, random m, ask
verify_plane about every interior target and compare with the tracer.
Cells are shifted by +1 as shoot.c does (verify_plane is translation-blind).
"""
import random, subprocess, json, math, sys
from collections import Counter
from rooms import rooms
from tracer import Room
random.seed(20261123)
pool = [p for n, p, w, m in rooms(11) if len(m) >= 2]
control = [(0,2),(0,3),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,4),(2,5),(3,4),(3,5),(4,3),(4,4),(5,3)]
pool += [tuple(control)] * 200
dirs = [(p, q) for s in range(1, 9) for p in range(s + 1) for q in [s - p] if math.gcd(p, q) == 1]
queries, expect = [], []
stats = Counter()
for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 4000):
    cells = random.choice(pool); R = Room(cells)
    src = random.choice(sorted(R.marks))
    p, q = random.choice(dirs); d = (p * random.choice((1, -1)), q * random.choice((1, -1)))
    m = random.randint(1, int(sys.argv[2]) if len(sys.argv) > 2 else 30)
    ok, _, end = R.trace(src, d, m)
    stats['tracer_ok' if ok else 'tracer_corner'] += 1
    if not ok:
        # where the unfolded ray would land ignoring the corner (plain mirror fold)
        stats['corner_rays'] += 1
    for t in sorted(R.marks):
        if t == src: continue
        q_ = [len(cells)] + [c + 1 for xy in cells for c in xy] + [src[0]+1, src[1]+1, d[0], d[1], m, t[0]+1, t[1]+1]
        queries.append(' '.join(map(str, q_))); expect.append(int(ok and end == t))
out = subprocess.run(['./vp_harness'], input='\n'.join(queries) + '\n', capture_output=True, text=True, check=True).stdout.split()
got = list(map(int, out))
mism = [(queries[i], expect[i], got[i]) for i in range(len(got)) if got[i] != expect[i]]
print(json.dumps({'queries': len(got), 'positives': sum(expect), 'rays': dict(stats), 'mismatches': len(mism), 'examples': mism[:3]}))
