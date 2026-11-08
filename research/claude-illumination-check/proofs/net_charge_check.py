"""Check the net-charge identity W = 2 + sum over A cells of net(cell) on saved rooms.

net(cell) = cost(cell) - sum of w(tile) over the cell's tiles, where
cost = 6 (full), 3 (smooth boundary A, 4 tiles in a half-plane), m (other nonempty, m tiles), 0 (empty);
w(tile) = 1/2 if its C vertex is an exception + 1/4 if its B vertex is an exception.
Exceptions are non-corner B/C points (interior or smooth boundary). Exact Fractions.
Usage: net_charge_check.py room.json [...]  (rooms with a 'triangles' list)
"""
import json, sys
from collections import Counter, defaultdict
from fractions import Fraction as F

def kind(p):
    return 'A' if p[0] % 2 == 0 and p[1] % 2 == 0 else 'B' if p[0] % 2 and p[1] % 2 else 'C'

def check(tiles):
    tiles = [tuple(sorted(map(tuple, t))) for t in tiles]
    ang = Counter(); edges = Counter()
    for t in tiles:
        for p in t:
            a, b = [q for q in t if q != p]
            right = (a[0]-p[0])*(b[0]-p[0]) + (a[1]-p[1])*(b[1]-p[1]) == 0
            ang[p] += 2 if right else 1          # units of 45 degrees
        for i in range(3):
            for j in range(i+1, 3):
                edges[tuple(sorted((t[i], t[j])))] += 1
    bdry = {p for e, c in edges.items() if c == 1 for p in e}
    # wall count: boundary vertices whose interior angle is not 180 degrees
    W = sum(1 for p in bdry if ang[p] != 4)
    exc = {p for p in ang if kind(p) != 'A' and (p not in bdry or ang[p] == 4)}
    E = sum(2 if p not in bdry else 1 for p in exc)
    cells = defaultdict(list)
    for t in tiles:
        cells[next(p for p in t if kind(p) == 'A')].append(t)
    total = F(0); nets = {}
    for a, ts in cells.items():
        m = len(ts)
        cost = 6 if a not in bdry else 3 if ang[a] == 4 else m
        w = sum(F(1, 2)*(next(p for p in t if kind(p) == 'C') in exc) + F(1, 4)*(next(p for p in t if kind(p) == 'B') in exc) for t in ts)
        nets[a] = cost - w; total += cost - w
    return W, E, total, nets

if __name__ == '__main__':
    for f in sys.argv[1:]:
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            W, E, total, nets = check(r['triangles'] if 'triangles' in r else r['room'])
            print(f, 'W', W, 'E', E, '2+sum net', 2+total, 'OK' if W == 2+total else 'MISMATCH', 'min net', min(nets.values()))
            if '--all' not in sys.argv:
                break
