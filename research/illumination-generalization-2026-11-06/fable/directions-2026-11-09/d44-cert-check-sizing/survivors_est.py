"""Estimated rooms passing the proved filter F*: count(W, n) x sampled pass rate(r, n).
High side: pass count p < 3 replaced by 3 (about the 95% upper bound) where F* allows the area."""
import re
from pathlib import Path
import sys; sys.argv = sys.argv[:1]
HERE = Path(__file__).resolve().parent

def cases(n, r):
    return [(n // d, z) for d in range(3, 10) if n % d == 0 for z in (1, 2)
            if n // d >= 3 and (n // d) * z <= r and d <= (4 * z if d % 2 == 0 else 4 * z + 1)]
rate = {}
for line in open(HERE / 'filter_rate.log'):
    r, n, s, p = map(int, re.findall(r'(\d+) area (\d+) sampled (\d+) pass (\d+)', line)[0])
    rate[(r, n)] = (s, p)
def load(path, key):
    out = {}
    for line in open(path):
        m = re.match(r'\s+W (\d+) area (\d+) %s ([0-9.e+]+)' % key, line)
        if m:
            out[(int(m.group(1)), int(m.group(2)))] = float(m.group(3))
    return out
lo_t = hi_t = 0.0
for W in (14, 16, 18, 20):
    r = (W - 4) // 2
    cnt = load(HERE / 'cnt_14_25.log', 'fixed') if W == 14 else load(HERE / ('est_W%d.log' % W), 'est_fixed')
    lo = hi = 0.0
    for n in range(21, 5 * r + 1):
        s, p = rate[(r, n)]
        c = cnt.get((W, n), 0) / 8          # free rooms, approx
        lo += c * p / s
        hi += c * max(p, 3) / s if cases(n, r) else 0.0
    lo_t += lo; hi_t += hi
    print('W %d: free rooms passing F* ~ %.3g (point) .. %.3g (with 3/S upper bound where pass < 3)' % (W, lo, hi))
print('total ~ %.3g .. %.3g free rooms' % (lo_t, hi_t))
