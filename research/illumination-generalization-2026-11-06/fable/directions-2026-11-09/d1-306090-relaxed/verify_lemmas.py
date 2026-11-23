"""Machine checks for the window argument in README.md ("Why hex radius 6 is enough").

L1  W <= 26 and n3 >= 12 force n1 + 4*n3 <= 59, hence n3 <= 14 (at most 2 extra triples).
L2  Edge-adjacent tiles with different C vertices share their A vertex (shared edge is AB).
L3  At every C point, any 3 of its 4 tiles carry both lattice-edge endpoints as A vertices;
    every tile at a C point has an endpoint of that point's lattice edge as A vertex.
L4  Lattice-edge connectivity: with stars at S=0 and T, plus at most 2 extra lattice
    edges, the union is connected only if hexdist(S,T) <= 4, and then every endpoint
    is within hex distance 5 of S.
L5  Every tile whose A vertex is within hex distance 5 of S lies in the hex-6 window.
Exact integer arithmetic only. Uses check_room.label for the vertex classes.
"""
import itertools, json
from check_room import label

def lat(i, j): return (12*i + 6*j, 6*j)
def hd(i, j): return max(abs(i), abs(j), abs(i+j))
NB = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
out = {}

# L1: enumerate all (n1, n3, k) with the turning inequality 360 <= 90 n1 - 90 n3 + 150 k
ok = True; worst = 0
for n3 in range(12, 40):
    for n1 in range(0, 40):
        for k in range(0, 40):
            W = n1 + n3 + k
            if W <= 26 and 360 <= 90*n1 - 90*n3 + 150*k:
                worst = max(worst, n3)
                if n1 + 4*n3 > 59: ok = False
out['L1'] = dict(PASS=ok and worst <= 14, max_n3_when_W_le_26=worst,
                 min_W_two_stars=min(n1+n3+k for n3 in range(12, 40) for n1 in range(40) for k in range(40) if 360 <= 90*n1-90*n3+150*k))

# tiles of a patch (independent re-derivation from lattice triangles)
tiles = []
for i in range(-4, 4):
    for j in range(-4, 4):
        for tri in (((i, j), (i+1, j), (i, j+1)), ((i+1, j), (i, j+1), (i+1, j+1))):
            v = [lat(*p) for p in tri]; g = (sum(p[0] for p in v)//3, sum(p[1] for p in v)//3)
            for p, q in itertools.combinations(v, 2):
                m = ((p[0]+q[0])//2, (p[1]+q[1])//2)
                tiles += [(p, m, g), (q, m, g)]
def parts(t): return {label(p): p for p in t}
ok2 = True; pairs = 0; edges = {}
for idx, t in enumerate(tiles):
    for e in itertools.combinations(sorted(t), 2): edges.setdefault(e, []).append(idx)
for e, ids in edges.items():
    assert len(ids) <= 2
    if len(ids) == 2:
        a, b = parts(tiles[ids[0]]), parts(tiles[ids[1]]); pairs += 1
        if a['C'] != b['C'] and (a['A'] != b['A'] or {label(p) for p in e} != {'A', 'B'}): ok2 = False
out['L2'] = dict(PASS=ok2, shared_edges_checked=pairs)

atC = {}
for t in tiles: atC.setdefault(parts(t)['C'], []).append(parts(t)['A'])
ok3 = True; full = 0
for c, As in atC.items():
    if len(As) != 4: continue
    full += 1; ends = set(As)
    if len(ends) != 2 or 2*c[0] != sum(p[0] for p in ends) or 2*c[1] != sum(p[1] for p in ends): ok3 = False
    for trip in itertools.combinations(As, 3):
        if set(trip) != ends: ok3 = False
out['L3'] = dict(PASS=ok3, C_points_checked=full)

# L4: grow at most 2 extra lattice edges from the two stars.
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
S = (0, 0); maxD = 0; maxR = 0; configs = 0
for ti in range(-8, 9):
    for tj in range(-8, 9):
        D = hd(ti, tj)
        if D < 2 or D > 8: continue
        base = star(S) | star((ti, tj))
        verts = {p for e in base for p in e}
        cand1 = {frozenset((p, (p[0]+a, p[1]+b))) for p in verts for a, b in NB} - base
        configs_here = [set()] + [{e} for e in cand1]
        for e1 in cand1:
            v1 = verts | set(e1)
            for p in v1:
                for a, b in NB:
                    e2 = frozenset((p, (p[0]+a, p[1]+b)))
                    if e2 not in base and e2 != e1: configs_here.append({e1, e2})
        for X in configs_here:
            if connected(base | X):
                configs += 1; maxD = max(maxD, D)
                maxR = max(maxR, max(hd(*p) for e in base | X for p in e))
out['L4'] = dict(PASS=maxD <= 4 and maxR <= 5, max_ST_distance=maxD, max_endpoint_distance=maxR, connected_configs=configs)

# L5: hex-6 window = all triangles with every vertex within hex distance 6
ok5 = True; n = 0
for i in range(-6, 7):
    for j in range(-6, 7):
        if hd(i, j) > 5: continue
        for a, b in NB:
            for c, d in NB:
                # triangle (v, v+n1, v+n2) with n1, n2 adjacent neighbor directions
                if hd(a - c, b - d) != 1: continue
                for p in ((i+a, j+b), (i+c, j+d)):
                    n += 1
                    if hd(*p) > 6: ok5 = False
out['L5'] = dict(PASS=ok5, triangle_vertices_checked=n)
out['ALL_PASS'] = all(v['PASS'] for v in out.values() if isinstance(v, dict))
json.dump(out, open('verify-lemmas.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
