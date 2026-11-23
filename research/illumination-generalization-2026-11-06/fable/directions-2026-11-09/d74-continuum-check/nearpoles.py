"""d74: evidence only (not a proof).  For each residual corner pair (a, b) of the two 18-cell rooms,
sample rational S, T within 1/20 of a, b inside the room and search an explicit billiard path
(geom.lit_pair, images up to radius R).  Usage: nearpoles.py IDX R NSAMP SEED"""
import random, sys, time
from fractions import Fraction as F
from geom import read_rooms, lit_pair, interior_point
PAIRS = {0: [((0,1),(1,0)),((0,1),(1,8)),((0,1),(3,0)),((0,3),(3,4)),((0,3),(1,4)),((0,5),(3,4)),((0,5),(1,4)),
             ((0,7),(1,0)),((0,7),(1,8)),((0,7),(3,0)),((1,0),(4,1)),((1,8),(4,1)),((3,0),(4,1)),((3,4),(4,3)),((4,3),(1,4))],
         1: [((0,0),(2,7)),((0,0),(2,1)),((0,8),(2,7)),((0,8),(2,1)),((2,7),(4,0)),((4,0),(2,1)),
             ((0,3),(2,4)),((0,5),(2,4)),((4,3),(2,4))]}
idx, R, N, seed = map(int, sys.argv[1:5])
cs = read_rooms('../../../../qclass-closure/two18/rooms')[idx]
rnd = random.Random(seed)
t0 = time.process_time()
def near(pt):
    while True:
        x = pt[0] + F(rnd.randint(-50, 50), 1000); y = pt[1] + F(rnd.randint(-50, 50), 1000)
        if interior_point(cs, x, y):
            return (x, y)
tot = got = 0
for a, b in PAIRS[idx]:
    res = []
    for _ in range(N):
        S, T = near(a), near(b)
        v = lit_pair(cs, S, T, R)
        tot += 1; got += v is not None
        res.append('lit' if v else 'none')
    print(a, b, res)
print('room', idx, 'sampled', tot, 'explicit path found', got, 'cpu %.1f' % (time.process_time() - t0))
