"""d100: large-K pairs drawn from inside the d100 residual, traced along the certificate path.

Usage: python3 -B sample_k.py RES_R0 RES_R1 CENSUS_REGIONS N

A product f x W qualifies when closure(f) contains its designated grid point e and W contains
the other end's point e'. Then S = e + l1 (X - e) and T = e' + l2 (Y - e'), with X, Y random
relative-interior points and 0 < l1, l2 <= 1, lie in relint f and in W by convexity. The scale
is set so that A (largest displacement) gives a target K = ceil(1/(8 L A)) in [2, 60].
Tracing reuses d90 check.py (leaf walk, cylinder development, pull-back by the shear power)
and the D87 exact tracer.
"""
import random
import sys
from fractions import Fraction as F
from math import ceil
from pathlib import Path

HERE = Path(__file__).resolve().parent
res0, res1, census, N = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(HERE.parent / 'd90-check-two18'))
sys.argv = ['check.py', census, '0', '0']
import check  # noqa: E402  (replays the 144 trees, then exposes trace_pair)
from compare_lib import load, load_census, inside, in_census  # noqa: E402

mine, centers = load([res0, res1], check.ROOMS)
assert not centers.pop(None)
theirs = load_census(census)[0]
assert all(check.centers[(r, a, b)][cell] == g for (r, a, b, cell), g in centers.items())
quali = []
for r, a, b, src, P, W in mine:
    tgt = b if src == a else a
    e, e2 = centers[(r, a, b, src)], centers[(r, a, b, tgt)]
    if inside(e, P) and inside(e2, W) and len(P) >= 2 and len(W) >= 3:
        quali.append((r, src, tgt, P, W, e, e2))
print(f'products whose closures reach both designated points: {len(quali)} of {len(mine)}')
rng = random.Random(1000)


def relint(poly):
    w = [rng.randint(1, 1000) for _ in poly]
    t = sum(w)
    return (sum(F(c, t) * x for c, (x, _) in zip(w, poly)), sum(F(c, t) * y for c, (_, y) in zip(w, poly)))


fails = done = 0
Ks = []
census_hit = 0
while done < N:
    r, src, tgt, P, W, e, e2 = quali[rng.randrange(len(quali))]
    X, Y = relint(P), relint(W)
    dX = max(abs(X[0] - e[0]), abs(X[1] - e[1]))
    dY = max(abs(Y[0] - e2[0]), abs(Y[1] - e2[1]))
    Kt = rng.randint(2, 60)
    A = F(1, 8 * 8 * Kt) * F(rng.randint(500, 1000), 1000)    # L = 8 scale; L = 12, 16 give larger K
    l1 = min(F(1), A / dX * F(rng.randint(1, 1000), 1000) if rng.random() < .5 else A / dX)
    l2 = min(F(1), A / dY) if l1 * dX < A else min(F(1), A / dY * F(rng.randint(1, 1000), 1000))
    S = (e[0] + l1 * (X[0] - e[0]), e[1] + l1 * (X[1] - e[1]))
    T = (e2[0] + l2 * (Y[0] - e2[0]), e2[1] + l2 * (Y[1] - e2[1]))
    cells = set(check.ROOMS[r])
    if not (check.interior(cells, *S) and check.interior(cells, *T)):
        continue
    assert inside(S, P) and inside(T, W)
    ok, tag, K, ln = check.trace_pair(r, {src: S, tgt: T}, cells)
    if K < 2:
        continue
    done += 1
    census_hit += in_census(theirs, r, src, tgt, S, T)
    fails += not ok
    Ks.append(K)
    print(f'room {r} cells {src}->{tgt} tag {tag} K {K} |V|1 {float(ln):.0f} {"ok" if ok else "FAIL"}', flush=True)
Ks.sort()
print(f'large-K residual samples: {done} traced, {fails} failures; K min {Ks[0]} median {Ks[len(Ks)//2]} max {Ks[-1]}; '
      f'K>=10: {sum(k >= 10 for k in Ks)}, K>=40: {sum(k >= 40 for k in Ks)}; inside a census product closure: {census_hit}')
assert fails == 0
