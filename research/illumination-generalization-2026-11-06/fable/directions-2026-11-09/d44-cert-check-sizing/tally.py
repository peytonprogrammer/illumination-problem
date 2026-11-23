"""Tally d44 room counts in the check range from count_rooms logs; apply the d36 area filter."""
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent

def allowed(n, r, deltas=None):
    """n = delta*d with d <= 4z+1 (d <= 4z if d even), delta*z <= r, z >= 1 (d36);
    d >= 3 when delta >= 2 (a zero needs d >= 3)."""
    for delta in range(1, r + 1):
        if deltas and delta not in deltas:
            continue
        if n % delta:
            continue
        d = n // delta
        z = r // delta
        if z < 1:
            continue
        if delta >= 2 and d < 3:
            continue
        if d <= (4 * z if d % 2 == 0 else 4 * z + 1):
            return True
    return False

def load(path, key):
    out = {}
    for line in open(path):
        m = re.match(r'\s+W (\d+) area (\d+) %s ([0-9.e+]+)' % key, line)
        if m:
            out[(int(m.group(1)), int(m.group(2)))] = float(m.group(3))
    return out

exact14 = load(HERE / 'cnt_14_25.log', 'fixed')
tot = totf = totS = 0.0
for W in (14, 16, 18, 20):
    r = (W - 4) // 2
    est = exact14 if W == 14 else load(HERE / ('est_W%d.log' % W), 'est_fixed')
    rng = range(21, 5 * r + 1)
    a = sum(est.get((W, n), 0) for n in rng)
    f = sum(est.get((W, n), 0) for n in rng if allowed(n, r))
    s3 = sum(est.get((W, n), 0) for n in rng if allowed(n, r, deltas=set(range(3, 9))))
    ex = sum(exact14.get((W, n), 0) for n in rng) if W == 14 else None
    tot += a; totf += f; totS += s3
    print('W %d r %d areas 21..%d: est fixed %.3g%s | after d36 area filter %.3g (areas %s) | delta>=3 areas only %.3g (areas %s)'
          % (W, r, 5 * r, a, ' (exact %d)' % ex if ex else '', f, [n for n in rng if not allowed(n, r)] and
             'dropped %s' % [n for n in rng if not allowed(n, r)] or 'none dropped', s3,
             [n for n in rng if allowed(n, r, set(range(3, 9)))]))
print('total fixed %.3g, free ~ %.3g; after area filter fixed %.3g free ~ %.3g; delta>=3-only areas free ~ %.3g'
      % (tot, tot / 8, totf, totf / 8, totS / 8))
