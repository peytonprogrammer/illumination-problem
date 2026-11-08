"""Incremental rewrite of claude_k_enumerate.py: same rules, same pruning, same output.

Instead of copying the state and rescanning every vertex at each node, it keeps per-vertex
known/value bit masks, running totals, and an undo trail. Per-vertex option lists are
memoized on (known, value). Every pruning test is a valid lower bound regardless of branch
order, so the set of rooms found equals the original's; node counts can differ.
Usage: claude_k_enum_fast.py K WMAX NMAX IMAX
"""
import json
import math
import sys
from itertools import combinations
from pathlib import Path
sys.setrecursionlimit(100000)
HERE = Path(__file__).resolve().parent


def tiling(n, R):
    """n=4 branch of tokarsky-n/claude_tokarsky_min.tiling, copied so PyPy needs no OR-Tools."""
    tiles, role = set(), {}
    for i in range(-2*R, 2*R):
        for j in range(-2*R, 2*R):
            sq = [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]
            a = next(q for q in sq if q[0] % 2 == 0 and q[1] % 2 == 0)
            b = next(q for q in sq if q[0] % 2 and q[1] % 2)
            for c in sq:
                if c not in (a, b):
                    tiles.add(tuple(sorted([a, b, c])))
    for t in tiles:
        for p in t:
            role[p] = 'A' if p[0] % 2 == 0 and p[1] % 2 == 0 else ('B' if p[0] % 2 and p[1] % 2 else 'C')
    return sorted(tiles), role, {'A': 1, 'B': 1, 'C': 2}, None

K, WMAX, NMAX, IMAX = map(int, sys.argv[1:5])
TAG = sys.argv[5] if len(sys.argv) > 5 else 'fast'
SEED2 = tuple(map(int, sys.argv[6].split(','))) if len(sys.argv) > 6 else None  # optional second full star
tiles, role, unit, xy = tiling(4, 12)
tid = {t: i for i, t in enumerate(tiles)}
verts = sorted({p for t in tiles for p in t})
vid = {p: i for i, p in enumerate(verts)}
NV = len(verts)
ring, pos = [], []  # ring[v]: tile ids in angular order; pos[v]: tile id -> bit
ring_tmp = {}
for t in tiles:
    for p in t:
        ring_tmp.setdefault(p, []).append(t)
complete = [False]*NV
for p in verts:
    r = sorted(ring_tmp[p], key=lambda t: math.atan2(sum(q[1] for q in t)/3-p[1], sum(q[0] for q in t)/3-p[0]))
    ring.append([tid[t] for t in r]); pos.append({tid[t]: i for i, t in enumerate(r)})
    complete[vid[p]] = len(r)*unit[role[p]] == 8
tverts = [[vid[p] for p in t] for t in tiles]
isA = [role[p] == 'A' for p in verts]
isBC = [not a for a in isA]
CORNER = {'B': {1, 2, 3, 5, 6, 7}, 'C': {1, 3}}
EXCEPT = {'B': {4, 8}, 'C': {2, 4}}


def patterns(v):
    k = len(ring[v]); out = {}
    rl = role[verts[v]]
    for mask in range(1, 1 << k):
        b = [mask >> i & 1 for i in range(k)]; s = sum(b)
        if s < k and sum(1 for i in range(k) if b[i] and not b[i-1]) != 1:
            continue
        if rl != 'A' and s not in CORNER[rl] | EXCEPT[rl]:
            continue
        if rl == 'A':
            kd = (int(s not in (4, 8)), 0, int(s == 8))
        else:
            kd = (int(s in CORNER[rl]), int(s in EXCEPT[rl]), 0)
        out[mask] = kd
    return out


PAT = [patterns(v) if complete[v] else {} for v in range(NV)]
OPT = [dict() for _ in range(NV)]


def options(v, known, val):
    d = OPT[v]; key = (known, val)
    o = d.get(key)
    if o is None:
        o = d[key] = [m for m in PAT[v] if m & known == val]
    return o


# Lighting certificates (claude_lit_certs.py): prune once some certificate is satisfied.
watch = {}
rem, sat = [], [0]
if SEED2:
    from claude_lit_certs import certificates
    cache = HERE/f'certs-{SEED2[0]}_{SEED2[1]}.json'
    if not cache.exists():
        cache.write_text(json.dumps([[sorted(map(list, map(lambda t: list(map(list, t)), U))),
                                      sorted(map(lambda t: list(map(list, t)), Z))] for U, Z, _ in certificates(SEED2)]))
    paths = HERE/f'certs-paths-{SEED2[0]}_{SEED2[1]}.json'
    if not paths.exists():  # replay audit: each precomputed (U, Z) with its exact path
        fr = lambda c: [c.numerator, c.denominator]
        paths.write_text(json.dumps([dict(U=sorted(map(sorted, U)), Z=sorted(map(sorted, Z)), path=[[fr(x), fr(y)] for x, y in P])
                                     for U, Z, P in certificates(SEED2)]))
    for ci, (U, Z) in enumerate(json.loads(cache.read_text())):
        need = [(tid[tuple(map(tuple, t))], 1) for t in U] + [(tid[tuple(map(tuple, t))], 0) for t in Z]
        rem.append(len(need))
        for t, x in need:
            watch.setdefault((t, x), []).append(ci)
assign = [-1]*len(tiles)
known = [0]*NV; value = [0]*NV; nused = [0]*NV
FULL = [(1 << len(ring[v]))-1 for v in range(NV)]
tot = dict(walls=0, exc=0, full=0, und_bc=0, n=0)
active = set()  # active (used) and undecided vertices
stats = dict(nodes=0, closed=0, rooms=0, hit_window=0, not_simple=0, lit_pruned=0, learned=0, candidates=0)
LEARN = bool(SEED2) and __import__('os').environ.get('CLAUDE_LEARN', '1') == '1'
if LEARN:
    from claude_learn import light


def learn(U, Z):
    """Add a certificate; rem counts its entries not satisfied by the current assignment."""
    need = [(tid[t], 1) for t in U] + [(tid[t], 0) for t in Z]
    ci = len(rem); r = sum(1 for t, x in need if assign[t] != x)
    rem.append(r)
    for t, x in need:
        watch.setdefault((t, x), []).append(ci)
    if r == 0:
        sat[0] += 1
OUT = HERE/f'claude-k{K}-w{WMAX}-rooms-{TAG}.jsonl'
fh = OUT.open('w')
lfh = (HERE/f'claude-k{K}-w{WMAX}-learned-{TAG}.jsonl').open('w', buffering=1)  # learned (U, Z, path, room) for replay
seen = set()


def set_tile(t, x, trail):
    """Assign tile t; return False on a local violation. Changes are recorded for undo."""
    assign[t] = x; trail.append(('t', t))
    if x:
        tot['n'] += 1
    for ci in watch.get((t, x), ()):
        rem[ci] -= 1
        if rem[ci] == 0:
            sat[0] += 1
    ok = True
    for v in tverts[t]:
        b = 1 << pos[v][t]
        known[v] |= b
        if x:
            value[v] |= b
            nused[v] += 1
            if nused[v] == 1:
                if not complete[v]:
                    stats['hit_window'] += 1; ok = False
                active.add(v); trail.append(('a', v))
                if isBC[v]:
                    tot['und_bc'] += 1
        trail.append(('v', v, b, x))
        if known[v] == FULL[v] and nused[v]:
            kd = PAT[v].get(value[v])
            if kd is None:
                ok = False
                kd = (0, 0, 0)
            tot['walls'] += kd[0]; tot['exc'] += kd[1]; tot['full'] += kd[2]
            active.discard(v); trail.append(('d', v, kd))
            if isBC[v]:
                tot['und_bc'] -= 1
    return ok


def undo(trail, mark):
    while len(trail) > mark:
        e = trail.pop()
        if e[0] == 't':
            t = e[1]
            if assign[t]:
                tot['n'] -= 1
            for ci in watch.get((t, assign[t]), ()):
                if rem[ci] == 0:
                    sat[0] -= 1
                rem[ci] += 1
            assign[t] = -1
        elif e[0] == 'v':
            _, v, b, x = e
            known[v] &= ~b
            if x:
                value[v] &= ~b; nused[v] -= 1
        elif e[0] == 'a':
            active.discard(e[1])
            if isBC[e[1]]:
                tot['und_bc'] -= 1
        else:
            _, v, kd = e
            tot['walls'] -= kd[0]; tot['exc'] -= kd[1]; tot['full'] -= kd[2]
            active.add(v)
            if isBC[v]:
                tot['und_bc'] += 1


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


def search(trail):
    stats['nodes'] += 1
    if stats['nodes'] % 1000000 == 0:
        print(json.dumps(stats), flush=True)
    if tot['n'] > NMAX or tot['exc'] > K or tot['full'] > IMAX:
        return
    if sat[0]:
        stats['lit_pruned'] += 1; return
    if tot['walls'] + max(0, tot['und_bc'] - (K - tot['exc'])) > WMAX:
        return
    best = None
    for v in active:
        o = options(v, known[v], value[v])
        if not o:
            return
        if best is None or len(o) < len(best[1]):
            best = (v, o)
            if len(o) == 1:
                break
    if best is None:
        stats['closed'] += 1
        if tot['full'] >= 2:
            used = sorted(tiles[t] for t in range(len(tiles)) if assign[t] == 1)
            if not simple(used):
                stats['not_simple'] += 1; return
            key = tuple(used)
            if SEED2 and LEARN:
                got, res = light(used, SEED2)
                if got:
                    learn(got[0], got[1]); stats['learned'] += 1
                    lfh.write(json.dumps(dict(U=sorted(map(sorted, got[0])), Z=sorted(map(sorted, got[1])), word=res['word'], room=used,
                                              path=[[[c.numerator, c.denominator] for c in pt] for pt in got[2]]))+'\n')
                    if stats['learned'] % 100 == 0:
                        print(json.dumps(stats), flush=True)
                    return
                stats['candidates'] += 1
                print('CANDIDATE', json.dumps(res), flush=True)
            if key not in seen:
                seen.add(key); stats['rooms'] += 1
                pts = {q for t in used for q in t}
                fulls = sorted(p for p in pts if isA[vid[p]] and all(assign[t] == 1 for t in ring[vid[p]]))
                fh.write(json.dumps(dict(walls=tot['walls'], exceptions=tot['exc'], tiles=len(used), full=fulls,
                                         triangles=[[list(q) for q in t] for t in key]))+'\n')
        return
    v, opts = best
    r = ring[v]; kn = known[v]
    for m in opts:
        mark = len(trail); ok = True
        for i, t in enumerate(r):
            if not kn >> i & 1:
                if not set_tile(t, m >> i & 1, trail):
                    ok = False; break
        if ok:
            search(trail)
        undo(trail, mark)


trail = []
okall = all(set_tile(t, 1, trail) for t in ring[vid[(0, 0)]] if assign[t] != 1)
if SEED2:
    okall = okall and all(set_tile(t, 1, trail) for t in ring[vid[SEED2]] if assign[t] != 1)
assert okall
search(trail)
fh.close()
print(json.dumps(stats), flush=True)
(HERE/f'claude-k{K}-w{WMAX}-stats-{TAG}.json').write_text(json.dumps(dict(K=K, WMAX=WMAX, NMAX=NMAX, IMAX=IMAX, stats=stats))+'\n')
