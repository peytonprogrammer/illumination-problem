"""Minimum wall count of simple Tokarsky-lemma rooms for reflection triangles pi/n.

Wolecki (arXiv:1905.09358, Lemma 3.1), extending Tokarsky: in a triangle ABC with angle
pi/n at A and m*pi/n at B (n even, m < n-1), no billiard path runs from A back to A. So if a
polygon Q is tiled by reflected copies of ABC, every image of B and C is a corner of Q, and
two distinct interior points fold to A, those two points don't illuminate each other.
No ray search is needed: darkness follows from the lemma.

Only Coxeter triangles tile the plane by reflection, so this covers
  n=4: the 45-45-90 tiling (A at even-even points, angle units of 45 degrees);
  n=6: the 30-60-90 kisrhombille tiling (A = triangular-lattice points, 30-degree units).
Model: every used vertex has one sector; images of B and C are corners (never interior,
never a straight angle); A images are interior full stars or boundary points, a corner
unless straight. Walls = corners. Simple polygon = edge-connected + Euler characteristic 1
+ one sector per vertex. Two marks are full A stars. Minimize walls.
Usage: claude_tokarsky_min.py n radius [seconds]
"""
import json
import math
import os
import sys
from itertools import combinations
from ortools.sat.python import cp_model


def tiling(n, R):
    """Tiles as triples of integer points, with each vertex's role and angle in units of pi/n."""
    tiles, role = set(), {}
    if n == 4:
        # Canonical 45-degree tiling: split each unit square along the diagonal joining its
        # even-even corner (A) and odd-odd corner (B); the other two corners are C.
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
        unit = {'A': 1, 'B': 1, 'C': 2}
        xy = lambda p: (float(p[0]), float(p[1]))
    elif n == 6:
        # Skew coordinates p = a*u + b*v, u=(1,0), v=(1/2, sqrt3/2), scaled by 6.
        for i in range(-R, R+1):
            for j in range(-R, R+1):
                for tri in (((6*i, 6*j), (6*i+6, 6*j), (6*i, 6*j+6)),
                            ((6*i+6, 6*j), (6*i, 6*j+6), (6*i+6, 6*j+6))):
                    g = (sum(p[0] for p in tri)//3, sum(p[1] for p in tri)//3)
                    for p, q in combinations(tri, 2):
                        mid = ((p[0]+q[0])//2, (p[1]+q[1])//2)
                        for a in (p, q):
                            tiles.add(tuple(sorted([a, mid, g])))
                            role[a], role[mid], role[g] = 'A', 'C', 'B'
        unit = {'A': 1, 'B': 2, 'C': 3}
        xy = lambda p: (p[0] + p[1]/2, p[1]*math.sqrt(3)/2)
    return sorted(tiles), role, unit, xy


def solve(n, R, seconds, marks, min_full=None):
    tiles, role, unit, xy = tiling(n, R)
    straight, full = n, 2*n
    m = cp_model.CpModel()
    x = {t: m.new_bool_var('') for t in tiles}
    inc = {}
    for t in tiles:
        for p in t:
            inc.setdefault(p, []).append(t)
    for p in marks:
        assert role[p] == 'A' and len(inc[p]) == 2*n, (p, len(inc.get(p, [])))
        for t in inc[p]:
            m.add(x[t] == 1)
    corners, vused, fullA = [], [], []
    for p, ts in inc.items():
        cx, cy = xy(p)
        ring = sorted(ts, key=lambda t: math.atan2(sum(xy(q)[1] for q in t)/3 - cy, sum(xy(q)[0] for q in t)/3 - cx))
        k = len(ring); u = unit[role[p]]
        complete = k*u == full
        rows = []
        for mask in range(1 << k):
            bits = [mask >> i & 1 for i in range(k)]; s = sum(bits)
            if s == 0:
                rows.append(bits + [0]); continue
            if s == k and complete:
                if role[p] == 'A':
                    rows.append(bits + [0])
                continue
            if complete and sum(1 for i in range(k) if bits[i] and not bits[i-1]) != 1:
                continue
            if not complete:  # vertex on the window edge: keep only contiguous runs
                runs = sum(1 for i in range(k) if bits[i] and (i == 0 or not bits[i-1]))
                if runs != 1:
                    continue
            angle = s*u
            if role[p] != 'A' and angle == straight:
                continue  # an image of B or C must be a corner
            rows.append(bits + [int(angle != straight)])
        c = m.new_bool_var('')
        m.add_allowed_assignments([x[t] for t in ring] + [c], rows)
        u_ = m.new_bool_var(''); m.add_max_equality(u_, [x[t] for t in ring])
        corners.append(c); vused.append(u_)
        if role[p] == 'A' and complete:
            f = m.new_bool_var(''); m.add_min_equality(f, [x[t] for t in ring]); fullA.append(f)
        if not complete:  # keep rooms away from the window edge
            for t in ring:
                m.add(x[t] == 0)
    edges = {}
    for t in tiles:
        for e in combinations(t, 2):
            edges.setdefault(e, []).append(t)
    eused = []
    for owners in edges.values():
        u_ = m.new_bool_var(''); m.add_max_equality(u_, [x[t] for t in owners]); eused.append(u_)
    N = sum(x.values())
    m.add(sum(vused) - sum(eused) + N == 1)
    root = inc[marks[0]][0]; big = len(tiles)
    flow_in = {t: [] for t in tiles}; flow_out = {t: [] for t in tiles}
    for owners in edges.values():
        if len(owners) == 2:
            a, b = owners
            for s, d in ((a, b), (b, a)):
                f = m.new_int_var(0, big, ''); m.add(f <= big*x[s]); m.add(f <= big*x[d])
                flow_out[s].append(f); flow_in[d].append(f)
    for t in tiles:
        if t == root:
            m.add(sum(flow_out[t]) - sum(flow_in[t]) == N - 1)
        else:
            m.add(sum(flow_in[t]) - sum(flow_out[t]) == x[t])
    if min_full is not None:  # free placement: at least this many interior A points anywhere
        m.add(sum(fullA) >= min_full)
    W = sum(corners)
    m.minimize(W)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = seconds
    s.parameters.num_search_workers = int(os.environ.get('CLAUDE_WORKERS', 6))
    st = s.solve(m)
    res = dict(n=n, R=R, marks=marks, status=s.status_name(st), seconds=round(s.wall_time, 1))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        res.update(walls=int(s.objective_value), bound=int(s.best_objective_bound), tiles=int(s.value(N)),
                   room=[[list(p) for p in t] for t in tiles if s.value(x[t])])
    return res


if __name__ == '__main__':
    n, R = int(sys.argv[1]), int(sys.argv[2]); seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 300
    step = 2 if n == 4 else 6
    if n == 4:
        cands = [(2*a, 2*b) for a in range(0, 4) for b in range(0, a+1) if (a, b) != (0, 0)]
    else:  # triangular lattice, up to symmetry: a >= b >= 0 in skew coordinates covers a 30-degree wedge
        cands = [(6*a, 6*b) for a in range(0, 4) for b in range(0, a+1) if (a, b) != (0, 0)]
    best = None
    for q in cands:
        r = solve(n, R, seconds, [(0, 0), q])
        print(json.dumps({k: v for k, v in r.items() if k != 'room'}), flush=True)
        if 'walls' in r and (best is None or r['walls'] < best['walls']):
            best = r
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'tokarsky-min-n{n}-R{R}.json'), 'w') as f:
        json.dump(best, f)
    print('best', json.dumps({k: v for k, v in (best or {}).items() if k != 'room'}))
