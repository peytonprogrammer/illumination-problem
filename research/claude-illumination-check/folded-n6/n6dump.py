"""Solver-free certificate for the 30-60-90 (n=6) Tokarsky family.

Claim: in any tile set that satisfies the local rules at every vertex it touches, the
component containing an interior (full) A star has at most MAX tiles and contains no other
full A star. Local rules, per vertex: the used tiles form one contiguous sector. B
(centroid, 60 degrees) holds 1, 2, 4, or 5 tiles; C (midpoint, 90 degrees) holds 1 or 3
tiles. So B and C are never interior and never straight. A is unrestricted.
A simple Tokarsky room satisfies these rules, so the claim implies that no simple room has
two interior A points. Connectivity, simplicity and wall counts are not used.

Exhaustive depth-first search: repeatedly take the undecided vertex of a used tile whose
ring has the fewest consistent completions, and branch over those completions.
"""
import json
import math
import sys
from itertools import combinations
from pathlib import Path
sys.setrecursionlimit(100000)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from claude_tokarsky_min import tiling

R = 12
tiles, role, unit, xy = tiling(6, R)
inc = {}
for t in tiles:
    for p in t:
        inc.setdefault(p, []).append(t)
ring = {}
for p, ts in inc.items():
    cx, cy = xy(p)
    ring[p] = sorted(ts, key=lambda t: math.atan2(sum(xy(q)[1] for q in t)/3-cy, sum(xy(q)[0] for q in t)/3-cx))
ALLOWED = {'A': None, 'B': {1, 2, 4, 5}, 'C': {1, 3}}


def patterns(p):
    k = len(ring[p]); out = []
    for mask in range(1, 1 << k):
        bits = [mask >> i & 1 for i in range(k)]; s = sum(bits)
        if s < k and sum(1 for i in range(k) if bits[i] and not bits[i-1]) != 1:
            continue
        if ALLOWED[role[p]] is not None and s not in ALLOWED[role[p]]:
            continue
        out.append(bits)
    return out


PAT = {}
stats = dict(nodes=0, leaves=0, max_tiles=0, second_full_A=0, hit_window=0)
best = None
LEAVES = []


def search(state):
    """state: dict tile -> 0/1 for decided tiles."""
    global best
    stats['nodes'] += 1
    used = [t for t, v in state.items() if v]
    todo = []
    for p in {q for t in used for q in t}:
        r = ring[p]
        if len(r) * unit[role[p]] != 12:
            stats['hit_window'] += 1; return
        if p not in PAT:
            PAT[p] = patterns(p)
        if all(t in state for t in r):  # decided as a side effect: check it is allowed
            if [state[t] for t in r] not in PAT[p]:
                return
            continue
        opts = [b for b in PAT[p] if all(state.get(t, b[i]) == b[i] for i, t in enumerate(r))]
        todo.append((len(opts), p, opts))
    if not todo:
        stats['leaves'] += 1
        n = len(used)
        full = [p for p in {q for t in used for q in t} if role[p] == 'A' and all(state.get(t) for t in ring[p])]
        if len(full) > 1:
            stats['second_full_A'] += 1
        LEAVES.append(sorted(used))
        if n > stats['max_tiles']:
            stats['max_tiles'] = n; best = sorted(used)
        return
    todo.sort(key=lambda z: z[0])
    _, p, opts = todo[0]
    for b in opts:
        nxt = dict(state)
        for i, t in enumerate(ring[p]):
            nxt[t] = b[i]
        search(nxt)


start = {t: 1 for t in ring[(0, 0)]}
search(start)
print(json.dumps(stats))
import pickle; pickle.dump((LEAVES,role,{p:xy(p) for p in role}),open('/tmp/n6leaves.pkl','wb'))
_=(json.dumps(dict(stats=stats, largest=[[list(p) for p in t] for t in best]))+'\n')
