"""Relaxed 30-60-90 dark-room search (CP-SAT).

Room: finite union of (2,3,6) tiles forming one simple polygon.
Constraints:
  * every C point in the room has exactly 1 or 3 tiles (genuine corner);
  * S = A point (0,0) is interior (12 tiles), plus at least one more interior A;
  * --strict additionally forces every B point to be a corner (old model).
Objective: number of walls (corner points of the polygon).

Coordinates (x, y) mean physical (x, sqrt(3) y); A lattice = <(12,0),(6,6)>.
Writes search-<out>.json with the status, bound, and best room.
"""
import argparse, json, time, itertools, sys
from pathlib import Path
from ortools.sat.python import cp_model

HERE = Path(__file__).parent


def lattice(i, j): return (12*i + 6*j, 6*j)


def triangles(kind, r):
    if kind == 'para':  # identical to illumination_306090.patch(radius)
        for i in range(-r, r):
            for j in range(-r, r):
                a, b, c, d = lattice(i, j), lattice(i+1, j), lattice(i, j+1), lattice(i+1, j+1)
                yield (a, b, c); yield (b, c, d)
    else:  # hex: every vertex within hex distance r of the origin
        hd = lambda i, j: max(abs(i), abs(j), abs(i+j))
        for i in range(-r-1, r+1):
            for j in range(-r-1, r+1):
                for tri in (((i, j), (i+1, j), (i, j+1)), ((i+1, j), (i, j+1), (i+1, j+1))):
                    if all(hd(*p) <= r for p in tri): yield tuple(lattice(*p) for p in tri)


def tiles_of(kind, r):
    tiles, label = [], {}
    for eq in triangles(kind, r):
        g = tuple(sum(p[k] for p in eq)//3 for k in (0, 1)); label[g] = 'B'
        for p, q in itertools.combinations(eq, 2):
            m = tuple((p[k]+q[k])//2 for k in (0, 1)); label[m] = 'C'; label[p] = label[q] = 'A'
            tiles += [(p, m, g), (q, m, g)]
    return tiles, label


DIRS = [(1, 0), (3, 1), (1, 1), (0, 1), (-1, 1), (-3, 1), (-1, 0), (-3, -1), (-1, -1), (0, -1), (1, -1), (3, -1)]


def direction(p, q):
    d = (q[0]-p[0], q[1]-p[1])
    for k, D in enumerate(DIRS):
        if d[0]*D[1] - d[1]*D[0] == 0 and d[0]*D[0] + 3*d[1]*D[1] > 0: return k
    raise ValueError


def wedge(t, p):
    """30-degree slots covered by tile t at its vertex p."""
    a, b = [direction(p, q) for q in t if q != p]
    if (b - a) % 12 > 6: a, b = b, a
    return frozenset((a + k) % 12 for k in range((b - a) % 12))


def local_rows(ids, wedges, lab, strict):
    """Allowed (tile bits, cost, turn, full) rows at one point."""
    rows = []
    for bits in itertools.product((0, 1), repeat=len(ids)):
        occ = set().union(*[w for w, b in zip(wedges, bits) if b]) if any(bits) else set()
        u = len(occ)
        if u == 0: rows.append(list(bits) + [0, 0, 0]); continue
        if u == 12:
            if lab == 'C' or (lab == 'B' and strict): continue
            rows.append(list(bits) + [0, 0, int(lab == 'A')]); continue
        if sum(1 for s in occ if (s - 1) % 12 not in occ) != 1: continue  # pinch point
        if lab == 'C' and u not in (3, 9): continue
        if lab == 'B' and strict and u == 6: continue
        rows.append(list(bits) + [int(u != 6), 6 - u, 0])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--window', default='para', choices=['para', 'hex'])
    ap.add_argument('--radius', type=int, default=3)
    ap.add_argument('--strict', action='store_true', help='also force every B point to be a corner')
    ap.add_argument('--max-walls', type=int)
    ap.add_argument('--seconds', type=float, default=1800)
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--no-turning', action='store_true', help='drop the redundant turning-sum constraint')
    ap.add_argument('--interior', type=int, default=2, help='minimum number of interior A points (sanity runs use 1)')
    ap.add_argument('--t-max-dist', type=int, help='forbid interior A points beyond this hex distance from S (window lemma: 4 suffices for W <= 26)')
    ap.add_argument('--out', required=True)
    a = ap.parse_args(); t0 = time.monotonic()
    ts, label = tiles_of(a.window, a.radius)
    m = cp_model.CpModel(); x = [m.new_bool_var(f't{i}') for i in range(len(ts))]
    at = {}
    for i, t in enumerate(ts):
        for p in t: at.setdefault(p, []).append(i)
    owners = {}
    for i, t in enumerate(ts):
        for p, q in itertools.combinations(t, 2): owners.setdefault(frozenset((p, q)), []).append(i)
    costs, turns, full = [], [], {}
    for p, ids in at.items():
        rows = local_rows(ids, [wedge(ts[i], p) for i in ids], label[p], a.strict)
        c = m.new_bool_var(''); tr = m.new_int_var(-6, 6, ''); f = m.new_bool_var('')
        m.add_allowed_assignments([x[i] for i in ids] + [c, tr, f], rows)
        costs.append(c); turns.append(tr); full[p] = f
    m.add(full[(0, 0)] == 1)
    m.add(sum(f for p, f in full.items() if label[p] == 'A' and p != (0, 0)) >= a.interior - 1)
    if a.t_max_dist is not None:
        for p, f in full.items():
            if label[p] != 'A': continue
            j = p[1] // 6; i = (p[0] - 6*j) // 12
            if max(abs(i), abs(j), abs(i+j)) > a.t_max_dist: m.add(f == 0)
    if not a.no_turning: m.add(sum(turns) == 12)  # polygon turning = 360 degrees
    # Euler characteristic V - E + F = 1 (no holes) given connectivity and arc links
    used_v = []
    for p, ids in at.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [x[i] for i in ids]); used_v.append(u)
    used_e = []
    for e, os in owners.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [x[i] for i in os]); used_e.append(u)
    m.add(sum(used_v) - sum(used_e) + sum(x) == 1)
    # connectivity: spanning arborescence from a tile at the origin
    root = next(i for i in at[(0, 0)])
    rank = [m.new_int_var(0, len(ts), '') for _ in ts]; m.add(rank[root] == 0); par = [[] for _ in ts]
    for e, os in owners.items():
        if len(os) != 2: continue
        for u, v in (os, os[::-1]):
            b = m.new_bool_var(''); m.add(b <= x[u]); m.add(b <= x[v]); par[v].append(b)
            m.add(rank[v] >= rank[u] + 1).only_enforce_if(b)
    for i in range(len(ts)):
        if i != root: m.add(sum(par[i]) == x[i])
    W = sum(costs)
    if a.max_walls is not None: m.add(W <= a.max_walls)
    m.minimize(W)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = a.seconds; s.parameters.num_search_workers = a.workers
    build = time.monotonic() - t0
    print(json.dumps(dict(event='model', tiles=len(ts), points=len(at), build_seconds=round(build, 1), args=vars(a))), flush=True)
    found = []

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            room = [[list(p) for p in ts[i]] for i in range(len(ts)) if self.value(x[i])]
            ints = [list(p) for p, f in full.items() if label[p] == 'A' and self.value(f)]
            found.append(dict(walls=round(self.objective_value), tiles=room, interior_A=ints))
            print(json.dumps(dict(event='solution', walls=round(self.objective_value), tiles=len(room), interior_A=ints, t=round(self.wall_time, 1))), flush=True)
    st = s.solve(m, CB())
    res = dict(status=s.status_name(st), best_walls=round(s.objective_value) if found else None,
               lower_bound=s.best_objective_bound, solve_seconds=round(s.wall_time, 1), build_seconds=round(build, 1),
               window=dict(kind=a.window, radius=a.radius, tiles=len(ts)), args=vars(a),
               best_room=found[-1] if found else None, improving_walls=[f['walls'] for f in found])
    if found:
        best = found[-1]; ia = best['interior_A']; S = [0, 0]; T = next((p for p in ia if p != S), None)
        res['best_room']['S'], res['best_room']['T'] = S, T
    (HERE / f'search-{a.out}.json').write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != 'best_room'}), flush=True)


if __name__ == '__main__':
    main()
