"""Solver-free check of the 45-degree zero-exception bound: no locally valid closed
configuration containing a full A star and a second full A star has fewer than WMAX+1 walls.

Rules per vertex: one sector; B (45 deg) holds 1-3 or 5-7 tiles; C (90 deg) holds 1 or 3;
A unrestricted. Walls = corners: every used B and C, plus each A whose tile count isn't 4
(straight) or 8 (interior). Pruning: used B/C points + decided A corners >= the final wall
count, because B and C are always corners. Simple rooms satisfy these rules, so a negative
result at WMAX = 23 means no simple 45-degree Tokarsky room has fewer than 24 walls.
Usage: claude_n4_bound.py WMAX
"""
import json, math, sys
from pathlib import Path
sys.setrecursionlimit(100000)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from claude_tokarsky_min import tiling

WMAX = int(sys.argv[1])
tiles, role, unit, xy = tiling(4, 10)
inc = {}
for t in tiles:
    for p in t:
        inc.setdefault(p, []).append(t)
ring = {p: sorted(ts, key=lambda t: math.atan2(sum(q[1] for q in t)/3-p[1], sum(q[0] for q in t)/3-p[0])) for p, ts in inc.items()}
ALLOWED = {'A': None, 'B': {1, 2, 3, 5, 6, 7}, 'C': {1, 3}}
PAT = {}


def patterns(p):
    k = len(ring[p]); out = []
    for mask in range(1, 1 << k):
        b = [mask >> i & 1 for i in range(k)]; s = sum(b)
        if s < k and sum(1 for i in range(k) if b[i] and not b[i-1]) != 1:
            continue
        if ALLOWED[role[p]] is not None and s not in ALLOWED[role[p]]:
            continue
        out.append(b)
    return out


def corner(p, b):
    s = sum(b)
    return role[p] != 'A' or s not in (4, 8)


stats = dict(nodes=0, closed=0, two_star=0, hit_window=0, min_walls_two_star=None)
found = []


def search(state):
    stats['nodes'] += 1
    if stats['nodes'] % 1000000 == 0:
        print(json.dumps(stats), flush=True)
    used = [t for t, v in state.items() if v]
    pts = {q for t in used for q in t}
    walls, todo = 0, []
    for p in pts:
        r = ring[p]
        if len(r)*unit[role[p]] != 8:
            stats['hit_window'] += 1; return
        if p not in PAT:
            PAT[p] = patterns(p)
        if all(t in state for t in r):
            b = [state[t] for t in r]
            if b not in PAT[p]:
                return
            walls += corner(p, b)
            continue
        if role[p] != 'A':
            walls += 1
        opts = [b for b in PAT[p] if all(state.get(t, b[i]) == b[i] for i, t in enumerate(r))]
        todo.append((len(opts), p, opts))
    if walls > WMAX:
        return
    if not todo:
        stats['closed'] += 1
        full = [p for p in pts if role[p] == 'A' and all(state.get(t) for t in ring[p])]
        if len(full) >= 2:
            stats['two_star'] += 1
            if stats['min_walls_two_star'] is None or walls < stats['min_walls_two_star']:
                stats['min_walls_two_star'] = walls
            if len(found) < 5:
                found.append(dict(walls=walls, full=sorted(full), room=[[list(q) for q in t] for t in sorted(used)]))
        return
    todo.sort(key=lambda z: z[0])
    _, p, opts = todo[0]
    for b in opts:
        nxt = dict(state)
        for i, t in enumerate(ring[p]):
            nxt[t] = b[i]
        search(nxt)


search({t: 1 for t in ring[(0, 0)]})
print(json.dumps(stats), flush=True)
(HERE/f'claude-n4-bound-{WMAX}.json').write_text(json.dumps(dict(stats=stats, examples=found))+'\n')
