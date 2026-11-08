"""Second-star placements q that a room with at most NMAX tiles can contain.

A room is edge-connected, so it contains a chain of tiles from the star at (0,0) to the star
at q. The chain's intermediate tiles are outside both stars, so their number, at least the
dual-graph distance between the stars minus one, is at most NMAX - 16. Up to the D4 symmetry
fixing (0,0) and the swap of the two marks, q can be taken with 0 <= qy <= qx.
Usage: claude_placements.py NMAX
"""
import json, sys
from collections import deque
from itertools import combinations
NMAX = int(sys.argv[1]); R = 30
tiles = set()
for i in range(-R, R):
    for j in range(-R, R):
        sq = [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]
        a = next(q for q in sq if q[0] % 2 == 0 and q[1] % 2 == 0)
        b = next(q for q in sq if q[0] % 2 and q[1] % 2)
        for c in sq:
            if c not in (a, b):
                tiles.add(tuple(sorted([a, b, c])))
owners = {}
for t in tiles:
    for e in combinations(t, 2):
        owners.setdefault(e, []).append(t)
adj = {t: [] for t in tiles}
for o in owners.values():
    if len(o) == 2:
        adj[o[0]].append(o[1]); adj[o[1]].append(o[0])
star = lambda p: {t for t in tiles if p in t}
s0 = star((0, 0)); dist = {t: 0 for t in s0}; dq = deque(s0)
while dq:
    t = dq.popleft()
    for u in adj[t]:
        if u not in dist:
            dist[u] = dist[t]+1; dq.append(u)
out = []
for qx in range(2, R-1, 2):
    for qy in range(0, qx+1, 2):
        d = min(dist.get(t, 10**9) for t in star((qx, qy)))
        if max(d-1, 0) <= NMAX-16:
            out.append([qx, qy])
print(json.dumps(dict(NMAX=NMAX, count=len(out), max_qx=max(q[0] for q in out), placements=out)))
