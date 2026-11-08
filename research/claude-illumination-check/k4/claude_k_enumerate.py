"""Solver-free enumeration of locally valid 45-degree rooms with up to K transparent B/C points.

Extends tokarsky-n/claude_n4_bound.py. Rules per vertex: one sector. B (45-degree unit)
holds 1-3 or 5-7 tiles as a corner, or 4 (smooth) or 8 (interior) as a transparent
exception. C (90-degree unit) holds 1 or 3 as a corner, or 2 or 4 as an exception. A is
unrestricted. Walls = corners. Seed: a full star at (0,0), which is one mark without loss
of generality.
Pruning, all necessary:
- exceptions <= K;
- walls >= decided corners + undecided used B/C - (K - decided exceptions);
- tiles <= NMAX (Codex's exception budget, checked by claude_budget_check.py);
- interior A points <= IMAX.
Each closed configuration with at least two full A stars is kept if it's edge-connected
with Euler characteristic 1 (a simple polygon). The output is candidate rooms only; no
darkness claim.
Usage: claude_k_enumerate.py K WMAX NMAX IMAX
"""
import json
import math
import sys
from itertools import combinations
from pathlib import Path
sys.setrecursionlimit(100000)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'tokarsky-n'))
from claude_tokarsky_min import tiling

K, WMAX, NMAX, IMAX = map(int, sys.argv[1:5])
tiles, role, unit, xy = tiling(4, 12)
inc = {}
for t in tiles:
    for p in t:
        inc.setdefault(p, []).append(t)
ring = {p: sorted(ts, key=lambda t: math.atan2(sum(q[1] for q in t)/3-p[1], sum(q[0] for q in t)/3-p[0]))
        for p, ts in inc.items()}
CORNER = {'B': {1, 2, 3, 5, 6, 7}, 'C': {1, 3}}
EXCEPT = {'B': {4, 8}, 'C': {2, 4}}
PAT = {}


def patterns(p):
    k = len(ring[p]); out = []
    for mask in range(1, 1 << k):
        b = tuple(mask >> i & 1 for i in range(k)); s = sum(b)
        if s < k and sum(1 for i in range(k) if b[i] and not b[i-1]) != 1:
            continue
        if role[p] != 'A' and s not in CORNER[role[p]] | EXCEPT[role[p]]:
            continue
        out.append(b)
    return out


def kind(p, b):
    """(is_corner, is_exception)."""
    s = sum(b)
    if role[p] == 'A':
        return s not in (4, 8), False
    return s in CORNER[role[p]], s in EXCEPT[role[p]]


stats = dict(nodes=0, closed=0, rooms=0, hit_window=0, not_simple=0)
OUT = HERE/f'claude-k{K}-w{WMAX}-rooms.jsonl'
seen = set()
fh = OUT.open('w')


def simple(used):
    owners = {}
    for t in used:
        for e in combinations(t, 2):
            owners.setdefault(e, []).append(t)
    V = len({q for t in used for q in t})
    if V - len(owners) + len(used) != 1:
        return False
    adj = {t: [] for t in used}
    for o in owners.values():
        if len(o) == 2:
            adj[o[0]].append(o[1]); adj[o[1]].append(o[0])
    seen_, stack = {used[0]}, [used[0]]
    while stack:
        for u in adj[stack.pop()]:
            if u not in seen_:
                seen_.add(u); stack.append(u)
    return len(seen_) == len(used)


def search(state):
    stats['nodes'] += 1
    if stats['nodes'] % 1000000 == 0:
        print(json.dumps(stats), flush=True)
    used = [t for t, v in state.items() if v]
    if len(used) > NMAX:
        return
    pts = {q for t in used for q in t}
    walls = exc = und_bc = full = 0
    todo = []
    for p in pts:
        r = ring[p]
        if len(r)*unit[role[p]] != 8:
            stats['hit_window'] += 1; return
        if p not in PAT:
            PAT[p] = patterns(p)
        if all(t in state for t in r):
            b = tuple(state[t] for t in r)
            if b not in PAT[p]:
                return
            c, e = kind(p, b); walls += c; exc += e
            full += role[p] == 'A' and sum(b) == 8
            continue
        if role[p] != 'A':
            und_bc += 1
        opts = [b for b in PAT[p] if all(state.get(t, b[i]) == b[i] for i, t in enumerate(r))]
        if not opts:
            return
        todo.append((len(opts), p, opts))
    if exc > K or full > IMAX or walls + max(0, und_bc - (K - exc)) > WMAX:
        return
    if not todo:
        stats['closed'] += 1
        if full >= 2:
            if not simple(used):
                stats['not_simple'] += 1; return
            key = tuple(sorted(used))
            if key not in seen:
                seen.add(key); stats['rooms'] += 1
                fulls = sorted(p for p in pts if role[p] == 'A' and all(state.get(t) for t in ring[p]))
                fh.write(json.dumps(dict(walls=walls, exceptions=exc, tiles=len(used), full=fulls,
                                         triangles=[[list(q) for q in t] for t in key]))+'\n')
        return
    todo.sort(key=lambda z: z[0])
    _, p, opts = todo[0]
    for b in opts:
        nxt = dict(state)
        for i, t in enumerate(ring[p]):
            nxt[t] = b[i]
        search(nxt)


search({t: 1 for t in ring[(0, 0)]})
fh.close()
print(json.dumps(stats), flush=True)
(HERE/f'claude-k{K}-w{WMAX}-stats.json').write_text(json.dumps(dict(K=K, WMAX=WMAX, NMAX=NMAX, IMAX=IMAX, stats=stats))+'\n')
