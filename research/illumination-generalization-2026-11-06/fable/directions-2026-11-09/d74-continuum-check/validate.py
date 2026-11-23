"""d74 validation of the label/cylinder computation against the independent exact room tracer.
For random rational S (denominator 97) and directions with p, q <= 5, pick a label D in Lambda(S)
and a random rational T in a closed band of D (T interior, T != S).  Lemma A' says S lights T;
we search an explicit billiard path with geom.lit_pair (images up to radius R), first restricted to
images whose displacement is nearly parallel to +-theta, then all images.  Usage: validate.py ROOMFILE N R SEED"""
import random
import sys
import time
from fractions import Fraction as F
from geom import Direction, read_rooms, trace, interior_point, images

path, N, R, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
ONLINE = len(sys.argv) > 5
rooms = read_rooms(path)
rnd = random.Random(seed)
t0 = time.process_time()
ok = fail = 0
for trial in range(N):
    cs = rnd.choice(rooms)
    cells = sorted(cs)
    p, q = rnd.randint(1, 5), rnd.randint(1, 5)
    from math import gcd
    if gcd(p, q) != 1:
        continue
    D = Direction(cs, p, q)
    c = rnd.choice(cells)
    S = (c[0] + F(rnd.randint(1, 96), 97), c[1] + F(rnd.randint(1, 96), 97))
    if ONLINE:   # put S on an integer line of a random family (regular or singular)
        fam = rnd.randint(0, 1)
        lo, hi = D.rng(c, fam)
        k = rnd.randint(lo + 1, hi - 1)
        x = S[0]
        y = (q * x - k) / p if fam == 0 else (k - q * x) / p
        if not interior_point(cs, x, y):
            continue
        S = (x, y)
    lam = D.labels_at(*S)
    if not lam:
        continue
    lab = rnd.choice(sorted(lam, key=str))
    bands = [b for b, l in D.label.items() if l == lab]
    for _ in range(100):
        (bc, fam, K2) = rnd.choice(bands)
        k = F(K2 - 1, 2) + F(rnd.randint(0, 89), 89)      # closed band value
        x = bc[0] + F(rnd.randint(0, 83), 83)
        y = (q * x - k) / p if fam == 0 else (k - q * x) / p
        if bc[1] <= y <= bc[1] + 1 and interior_point(cs, x, y) and (x, y) != S:
            T = (x, y)
            break
    else:
        continue
    ims = set(images(T, R))
    th = (p, q)
    def score(im):
        v = (im[0] - S[0], im[1] - S[1])
        return (v[0] * v[0] + v[1] * v[1])
    found = None
    for im in sorted(ims, key=score):
        v = (im[0] - S[0], im[1] - S[1])
        if v[0] == 0 or v[1] == 0:
            continue
        if trace(cs, S, v) == T:
            found = v
            break
    if found:
        ok += 1
    else:
        fail += 1
        print('NO PATH FOUND', sorted(cs), (p, q), S, T)
print('validated', ok, 'no-path', fail, 'cpu %.1f' % (time.process_time() - t0))
