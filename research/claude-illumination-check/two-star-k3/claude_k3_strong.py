"""Claude's strengthened model for I=2 full A stars with exactly three B/C exceptions.

Every added constraint is a necessary condition Claude derived or checked:
- per-vertex single-sector tables with corner / interior-exception / smooth-exception
  flags and A charge (k for a nonsmooth boundary A, 3 for a smooth A);
- W = 2 + 6*I_A + Q - (2J + s_N), walls <= 23, J + s_N = 3, N <= 36;
- m = absent mandatory cells, P + m <= 10, and Q + m >= the cell-path minimum
  (claude_path_bound.py, D >= 3 only);
- used outside cells form a set of size <= 2 that keeps R grid-connected;
- tile connectivity through shared edges (single-commodity flow);
- Euler characteristic 1 and verified positive-ray cuts.
Usage: claude_k3_strong.py X Y [--fixed room.json] [--no-cuts]
"""
import json
import os
import sys
from itertools import combinations
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent/'three-star'))
from ortools.sat.python import cp_model
from claude_ray_guard_check import cell_tiles, label
from claude_relaxed_replay import incident, around
from claude_three_star_reduction import neighbors
from claude_two_star_k3_geometry import support
from claude_path_bound import minimum as path_minimum
from claude_k3_closed_replay import guards

NB = ((1, 0), (-1, 0), (0, 1), (0, -1))


def table(v, ring):
    n, rows = len(ring), []
    unit = 2 if label(v) == 'C' else 1
    for mask in range(1 << n):
        bits = [mask >> k & 1 for k in range(n)]
        k = sum(bits)
        isA = label(v) == 'A'
        if k == 0:
            rows.append(bits + [0, 0, 0, 0]); continue
        if k == n:
            rows.append(bits + [0, int(not isA), 0, 0]); continue
        if sum(1 for i in range(n) if bits[i] and not bits[i-1]) != 1:
            continue
        units = k*unit
        if units == 4:
            rows.append(bits + [0, 0, int(not isA), 3 if isA else 0])
        else:
            rows.append(bits + [1, 0, 0, k if isA else 0])
    return rows


def connected_outside_sets(R, outside, budget):
    sets = []
    for n in range(budget+1):
        for add in combinations(outside, n):
            cells = R | set(add)
            start = next(iter(cells)); seen = {start}; todo = [start]
            for p in todo:
                for dx, dy in NB:
                    q = (p[0]+dx, p[1]+dy)
                    if q in cells and q not in seen:
                        seen.add(q); todo.append(q)
            if seen == cells:
                sets.append(set(add))
    return sets


def build(target, use_cuts=True, fixed=None, extra=None):
    full, allowed, r = support(target)
    R = set(full) | neighbors(full)
    mandatory = R - set(full)
    outside = sorted(allowed - R)
    ts = sorted({t for c in allowed for t in cell_tiles(*c)})
    index = {t: i for i, t in enumerate(ts)}
    m = cp_model.CpModel()
    x = [m.new_bool_var('') for _ in ts]
    zero = m.new_constant(0)
    var = lambda t: x[index[t]] if t in index else zero
    for c in full:
        for t in cell_tiles(*c):
            m.add(var(t) == 1)
    corners, ei, es, charge, vused, fullA = [], [], [], [], [], []
    for v in sorted({p for t in ts for p in t}):
        ring = around(v, incident(v))
        c, a, b, u = (m.new_bool_var('') for _ in range(4))
        q = m.new_int_var(0, 7, '')
        m.add_allowed_assignments([var(t) for t in ring] + [c, a, b, q], table(v, ring))
        m.add_max_equality(u, [var(t) for t in ring])
        corners.append(c); ei.append(a); es.append(b); charge.append(q); vused.append(u)
        if label(v) == 'A':
            f = m.new_bool_var(''); m.add_min_equality(f, [var(t) for t in ring]); fullA.append(f)
    edges = {}
    for t in ts:
        for e in combinations(t, 2):
            edges.setdefault(e, []).append(t)
    eused = []
    for owners in edges.values():
        u = m.new_bool_var(''); m.add_max_equality(u, [var(t) for t in owners]); eused.append(u)
    W, Q, J, sN, N = sum(corners), sum(charge), sum(ei), sum(es), sum(x)
    m.add(W <= int(os.environ.get("CLAUDE_MAXW", 23)))
    m.add(J + sN == 3)
    loose = os.environ.get('CLAUDE_LOOSE') == '1'  # sanity mode: drop constraints derived from W <= 23
    if not loose:
        m.add(N <= 36)
    m.add(sum(vused) - sum(eused) + N == 1)
    m.add(W == 2 + 6*sum(fullA) + Q - 2*J - sN)
    used = {}
    for c in allowed:
        u = m.new_bool_var(''); m.add_max_equality(u, [var(t) for t in cell_tiles(*c)]); used[c] = u
    missing = sum(1 - used[c] for c in mandatory)
    P = sum(used[c] for c in allowed if c not in full)
    if not loose:
        m.add(P + missing <= 10)
    if sum(target) >= 3 and not loose:
        m.add(Q + missing >= path_minimum(target))  # equivalent to W >= 8 + minimum
    rows = [[int(c in s) for c in outside] for s in connected_outside_sets(R, outside, r)]
    if not loose:
        m.add_allowed_assignments([used[c] for c in outside], rows)
    # Single-commodity flow from a tile of the origin star.
    root = index[sorted(cell_tiles(0, 0))[0]]
    arcs = []
    for owners in edges.values():
        if len(owners) == 2 and all(t in index for t in owners):
            i, j = index[owners[0]], index[owners[1]]
            for a, b in ((i, j), (j, i)):
                f = m.new_int_var(0, 36, '')
                m.add(f <= 36*x[a]); m.add(f <= 36*x[b])
                arcs.append((a, b, f))
    inflow = {i: [] for i in range(len(ts))}; outflow = {i: [] for i in range(len(ts))}
    for a, b, f in arcs:
        outflow[a].append(f); inflow[b].append(f)
    for i in range(len(ts)):
        if i == root:
            m.add(sum(outflow[i]) - sum(inflow[i]) == N - 1)
        else:
            m.add(sum(inflow[i]) - sum(outflow[i]) == x[i])
    cuts = set()
    if use_cuts:
        for f in (HERE/__import__('os').environ.get('CLAUDE_INPUTS','inputs')).glob(f'three-*/*{target[0]}-{target[1]}*.json'):
            for g in guards(json.loads(f.read_text())):
                cuts.add(tuple(sorted(map(tuple, g['tile_facts']))))
        seeds = HERE/'claude-k3-verified-seeds.json'  # seed cuts verified by claude_k3_seed_check.py
        if seeds.exists():
            for facts in json.loads(seeds.read_text()).get(f'{target[0]}-{target[1]}', []):
                cuts.add(tuple(sorted(map(tuple, facts))))
        for c in cuts:
            m.add_bool_or([x[i].Not() if v else x[i] for i, v in c])
    if fixed is not None:
        for t in ts:
            m.add(x[index[t]] == int(t in fixed))
    if extra is not None:  # caller-supplied restriction, e.g. a fixed neck plus its own cuts
        extra(m, x, index, used, ts)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = float(os.environ.get('CLAUDE_CAP', 1500))
    s.parameters.num_search_workers = int(os.environ.get('CLAUDE_WORKERS', 4))
    st = s.solve(m)
    res = dict(target=target, cuts=len(cuts), status=s.status_name(st), seconds=round(s.wall_time, 1))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        res['walls'] = int(s.value(W)); res['Q'] = int(s.value(Q))
        res['room'] = [[list(p) for p in t] for t in ts if s.value(x[index[t]])]
    return res


if __name__ == '__main__':
    tgt = (int(sys.argv[1]), int(sys.argv[2]))
    fixed = None
    if '--fixed' in sys.argv:
        tri = json.loads(Path(sys.argv[sys.argv.index('--fixed')+1]).read_text())
        fixed = {tuple(sorted(tuple(v) for v in t)) for t in tri}
    res = build(tgt, use_cuts='--no-cuts' not in sys.argv, fixed=fixed)
    print(json.dumps({k: v for k, v in res.items() if k != 'room'}), flush=True)
    if 'room' in res and fixed is None:
        (HERE/f'strong-survivor-{tgt[0]}-{tgt[1]}.json').write_text(json.dumps(res['room'])+'\n')
