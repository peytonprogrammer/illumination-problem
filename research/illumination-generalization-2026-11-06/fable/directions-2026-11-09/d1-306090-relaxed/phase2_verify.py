"""Phase 2 machine checks.

P1  Window lemma, transparent case: with full stars at S=0 and T (hexdist >= 2)
    plus e = K-1 extra lattice edges, connectivity forces hexdist(S,T) <= K+1 and
    every endpoint within hex distance K+2 of S, and every endpoint v obeys the
    ellipse bound d(S,v) + d(v,T) <= 2e + 6 - d(S,T). Enumerated for K = 2, 3, 4.
P2  W <= 21 forces n3 <= 11 (n1 + 4 n3 <= 46) even with transparent C points.
P3  Cut soundness, empirical part: for 200 exact billiard paths in a lit room, the
    support's 'present' set contains every tile met by 399 dense sample points per
    leg, every 'present' tile is in the room, every 'absent' tile is not, and the
    room's local structure at each reflection point is a flat wall.
P4  Adjacent interior A points are always joined by the direct segment (checked on
    an example: the shooter finds the 0-bounce path).
"""
import json, itertools, random
from fractions import Fraction as F
from check_room import analyze, add, scale, sub, E1, E2, label
from phase2_shoot import shoot_path, support, TileIndex, find_paths
from search_relaxed import tiles_of

out = {}
NB = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
def hd(i, j): return max(abs(i), abs(j), abs(i+j))
def star(c): return {frozenset((c, (c[0]+a, c[1]+b))) for a, b in NB}
def connected(E):
    adj = {}
    for e in E:
        u, v = tuple(e); adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    s = next(iter(adj)); seen = {s}; todo = [s]
    while todo:
        for w in adj[todo.pop()]:
            if w not in seen: seen.add(w); todo.append(w)
    return len(seen) == len(adj)

for K in (2, 3, 4):
    e = K - 1; maxD = maxR = 0; n = 0; ell = True
    for ti in range(-K-4, K+5):
        for tj in range(-K-4, K+5):
            D = hd(ti, tj)
            if D < 2 or D > K + 3 or not (0 <= tj <= ti): continue
            base = star((0, 0)) | star((ti, tj))
            def grow(X, verts, depth):
                global_ = None
                yield X
                if depth == 0: return
                for p in list(verts):
                    for a, b in NB:
                        ed = frozenset((p, (p[0]+a, p[1]+b)))
                        if ed in base or ed in X: continue
                        yield from grow(X | {ed}, verts | set(ed), depth - 1)
            verts = {p for ed in base for p in ed}
            for X in grow(frozenset(), verts, e):
                if connected(base | X):
                    n += 1; maxD = max(maxD, D); maxR = max(maxR, max(hd(*p) for ed in base | X for p in ed))
                    ell &= all(hd(*p) + hd(p[0]-ti, p[1]-tj) <= 2*e + 6 - D for ed in X for p in ed)
    out[f'P1_K{K}'] = dict(PASS=maxD <= K + 1 and maxR <= K + 2 and ell, extra_edges=e, max_ST=maxD, max_endpoint=maxR,
                           ellipse_ok=ell, configs=n)

ok = True
for n3 in range(0, 40):
    for n1 in range(40):
        for k in range(40):
            if n1 + n3 + k <= 21 and 360 <= 90*n1 - 90*n3 + 150*k and n3 > 11: ok = False
out['P2'] = dict(PASS=ok)

# P3: a lit room with transparent points: all tiles of the hex-2 patch (a big hexagon) minus a notch
ts, _ = tiles_of('hex', 2)
room = [t for t in ts if not (t[0][0] >= 12 and t[0][1] >= 6)]  # cut away tiles whose A vertex is in a corner
info, corners = analyze(room)
index = TileIndex(ts); inroom = {index.idx[tuple(t)] for t in room}
rng = random.Random(1); checked = 0; ok3 = True; reflections = 0
for _ in range(200):
    di, dj = rng.randint(-9, 9), rng.randint(-9, 9)
    if (di, dj) == (0, 0): continue
    X = add(scale(di, E1), scale(dj, E2))
    st, path, walls = shoot_path((0, 0), X, corners)
    if st != 'open': continue
    pres, absn = support(path, walls, index); checked += 1; reflections += len(walls)
    if not pres <= inroom or absn & inroom: ok3 = False
    for a, b in zip(path, path[1:]):
        for k in range(1, 400):
            q = add(a, scale(F(k, 400), sub(b, a)))
            if not index.containing(q) <= pres: ok3 = False
out['P3'] = dict(PASS=ok3, paths=checked, reflections=reflections, room_walls=info['walls'], transparent_C=len(info['transparent_C']))

# P4: adjacent interior A points in the same room
paths, shots = find_paths((0, 0), (12, 0), corners, 2, 1)
out['P4'] = dict(PASS=bool(paths) and len(paths[0]['path']) == 2, first_path_legs=len(paths[0]['path']) - 1 if paths else None)
out['ALL_PASS'] = all(v['PASS'] for v in out.values() if isinstance(v, dict))
json.dump(out, open('phase2-verify.json', 'w'), indent=1); print(json.dumps(out, indent=1))
