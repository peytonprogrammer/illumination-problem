"""D177: for one tile pair of a partial cert2 residual, report which corner pair (ca, cb)
each product is nearest to (max-norm, exact) and the largest such displacement.
Usage: python3 -B nearest.py ROOMFILE RESIDUAL A B [LIMIT]"""
import sys
from fractions import Fraction as F
from collections import Counter
roomf, resf, A, Bt = sys.argv[1:5]; A, Bt = int(A), int(Bt)
lim = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
v = list(map(int, open(roomf).read().split()))
cells = [(v[2 + 2 * i], v[3 + 2 * i]) for i in range(v[0])]
def poly(t):
    t = list(map(int, t.split())); return [(t[i], t[i + 1], t[i + 2]) for i in range(0, len(t), 3)]
def disp(P, c, k):
    x, y = cells[c]; X0, Y0 = x + (k & 1), y + (k >> 1)
    return max(max(abs(F(X, d) - X0), abs(F(Y, d) - Y0)) for X, Y, d in P)
cnt = Counter(); worst = {}; n = 0
for line in open(resf):
    if not line.startswith(f'PROD {A} {Bt} '): continue
    head, fs, ws = line.split('|'); src = int(head.split()[3])
    Pa, Pb = (poly(fs), poly(ws)) if src == A else (poly(ws), poly(fs))
    da = min((disp(Pa, A, k), k) for k in range(4)); db = min((disp(Pb, Bt, k), k) for k in range(4))
    key = (da[1], db[1]); cnt[key] += 1; worst[key] = max(worst.get(key, 0), da[0], db[0])
    n += 1
    if n >= lim: break
for k, c in cnt.most_common():
    print(f'pair {A} {Bt} nearest corners {k}: {c} products, max disp {worst[k]} = {float(worst[k]) * 65536:.0f}/65536')
