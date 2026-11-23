"""d43 referee check: the 12-wall cross and its scalings by 2 and 3 only. No search.

For each presentation: n, r, corner classes, B_x and R_y block counts, induced cycle
types, and whether B_x / R_y separate each of the four endpoint lift pairs.
"""
import sys, time, resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from roomtools import *  # noqa

def rigid(t, y):
    seeds = [(c[0], s) for c in cycles(t[y]) for s in c[1:]]
    return closure_partition(len(t[0]), t, seeds)

def types(t, part):
    return [sorted((len(c) for c in cycles(induced(g, part))), reverse=True) for g in t]

def join(t, parts):
    n = len(t[0]); seeds = []
    for p in parts:
        for blk in p:
            seeds += [(blk[0], s) for s in blk[1:]]
    return closure_partition(n, t, seeds)

def report(label, k):
    t0 = time.process_time()
    cross = {(i, j) for i in range(4) for j in range(1, 3)} | {(i, j) for i in range(1, 3) for j in range(4)}
    cells = {(k * i + u, k * j + v) for (i, j) in cross for u in range(k) for v in range(k)}
    S, T = (k * 1, k * 2), (k * 3, k * 2)
    led = ledger(cells, S)
    room, t = room_tuple(cells, S)
    n = len(t[0])
    cls = sorted({'abcd'[OFFS[((x - S[0]) % 2, (y - S[1]) % 2)]] for (x, y) in led['reflex'] + led['convex']})
    print('==', label, 'n', n, 'r', led['r'], 'corner classes', cls, 'strictly simple', is_strictly_simple(cells))
    print('  base types', [cycle_type(g) for g in t])
    LS, LT = lifts(room, t, S, S), lifts(room, t, T, S)
    Bs = {}
    for name, x in (('b', 1), ('c', 2), ('d', 3)):
        B = class_congruence(t, [x]); R = rigid(t, x); Bs[name] = B
        sepB = [a_image(t, B, s[0])[0] != a_image(t, B, u[0])[0] for s in LS for u in LT]
        sepR = [a_image(t, R, s[0])[0] != a_image(t, R, u[0])[0] for s in LS for u in LT]
        print('  B_%s blocks %d types %s separates %s | R_%s blocks %d types %s separates %s'
              % (name, len(B), types(t, B), sepB, name, len(R), types(t, R), sepR))
    J = join(t, list(Bs.values()))
    print('  B_* blocks', len(J), '| R_y == B_y:', [rigid(t, x) == class_congruence(t, [x]) for x in (1, 2, 3)])
    print('  CPU', round(time.process_time() - t0, 4))

for k in (1, 2, 3):
    report('cross scaled by %d' % k, k)
