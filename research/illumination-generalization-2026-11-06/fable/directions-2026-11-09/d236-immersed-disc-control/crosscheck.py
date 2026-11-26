"""Coordinator cross-check: decide a hand-specified sample of Astra's production discs
with the validator's independent unfolding and decider (validator/validate.py).
Sample: every 2000th line of astra/production/jobs.txt, plus the 20 OVERLAP lines with the most cells among the first 100 OVERLAP lines of area 16.
Prediction, written first: every sampled pair is lit by the validator too (P = 0.95).
"""
import sys, time
sys.path.insert(0, 'validator')
import validate as V
assert V.DX[:2] == [(1, 0), (0, 1)] or tuple(V.DX[:2]) == ((1, 0), (0, 1)), V.DX
def parse(line):
    a, *n = map(int, line.split())
    cells = [n[i:i + 6] for i in range(0, len(n), 6)]
    return a, [c[2:6] for c in cells], len({(c[0], c[1]) for c in cells}) < a
lines = open('astra/production/jobs.txt').read().split('\n')
lines = [l for l in lines if l]
sample = lines[::2000]
ov16 = [l for l in lines if l.startswith('16 ') and parse(l)[2]][:100]
sample += ov16[:20]
t = time.process_time(); tot = lit = 0; discs = 0; ov = 0; bad = []
for l in sample:
    a, nb, overlap = parse(l)
    comp, info = V.links(nb)
    res, srcs = V.light(nb, comp, info)
    k = len(srcs); pairs = k * (k - 1) // 2
    discs += 1; ov += overlap; tot += pairs
    litset, nstates, complete = res  # validator's decider returns the lit pairs
    lit += len(litset)
    if len(litset) != pairs: bad.append((l, len(litset), pairs, nstates, complete))
print(f"sample discs {discs} (overlap {ov}), pairs {tot}, lit {lit}, not lit {tot - lit}, cpu {time.process_time() - t:.1f}s")
for b in bad[:5]: print("NOT LIT:", b)
