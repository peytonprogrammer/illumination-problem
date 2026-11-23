"""Phase 2 CEGAR: simple (2,3,6) rooms with W <= Wmax, S=(0,0) and a selected T both
interior A points, and at most K transparent C points (2 or 4 tiles).

Loop: CP-SAT proposes (room, T). phase2_shoot looks for a legal S->T path. Each path
found gives a sound cut: NOT(T selected AND every tile of its support present AND
every tile it reflects off absent). Any room satisfying the support has that same
path legal, so the cut removes only lit (room, T) pairs. A proposal with no path
up to the shooter bound is saved as a dark candidate and excluded by an exact
no-good on (room, T), so the search continues.

Window: hex radius K+3 (see README, phase 2 window lemma). T is restricted to hex
distance 2..K+1 from S (adjacent pairs are always lit; the lemma bounds the rest).
"""
import argparse, json, time, itertools
from fractions import Fraction as F
from pathlib import Path
from ortools.sat.python import cp_model
from search_relaxed import tiles_of, wedge
from check_room import analyze
from phase2_shoot import find_paths, mirror_exact, support, TileIndex

HERE = Path(__file__).parent


def hexd(p):
    j = p[1] // 6; i = (p[0] - 6*j) // 12
    return max(abs(i), abs(j), abs(i+j))


def rows_for(ids, wedges, lab):
    rows = []
    for bits in itertools.product((0, 1), repeat=len(ids)):
        occ = set().union(*[w for w, b in zip(wedges, bits) if b]) if any(bits) else set()
        u = len(occ)
        if u == 0: rows.append(list(bits) + [0, 0, 0, 0]); continue
        if u == 12: rows.append(list(bits) + [0, 0, int(lab == 'A'), int(lab == 'C')]); continue
        if sum(1 for s in occ if (s - 1) % 12 not in occ) != 1: continue
        rows.append(list(bits) + [int(u != 6), 6 - u, 0, int(lab == 'C' and u == 6)])
    return rows


def wedge30(p):
    """T = i e1 + j e2 with 0 <= j <= i: direction between 0 and 30 degrees (D6 fundamental domain)."""
    j = p[1] // 6; i = (p[0] - 6*j) // 12
    return 0 <= j <= i


def hexd2(p, q):
    return hexd((p[0]-q[0], p[1]-q[1]))


def build(radius, K, wmax, tmax, only_T=None, ellipse=False):
    ts, label = tiles_of('hex', radius)
    if ellipse:  # phase 2 window lemma, per T: d(S,v) + d(v,T) <= 2e + 6 - D with e = K-1
        D = hexd(only_T); lim = 2*(K-1) + 6 - D
        ts = [t for t in ts if hexd(t[0]) + hexd2(t[0], only_T) <= lim]
    m = cp_model.CpModel(); x = [m.new_bool_var(f't{i}') for i in range(len(ts))]
    at, owners = {}, {}
    for i, t in enumerate(ts):
        for p in t: at.setdefault(p, []).append(i)
        for p, q in itertools.combinations(t, 2): owners.setdefault(frozenset((p, q)), []).append(i)
    costs, turns, full, trans = [], [], {}, []
    for p, ids in at.items():
        rows = rows_for(ids, [wedge(ts[i], p) for i in ids], label[p])
        c = m.new_bool_var(''); tr = m.new_int_var(-6, 6, ''); f = m.new_bool_var(''); z = m.new_bool_var('')
        m.add_allowed_assignments([x[i] for i in ids] + [c, tr, f, z], rows)
        costs.append(c); turns.append(tr); full[p] = f; trans.append(z)
    m.add(full[(0, 0)] == 1)
    m.add(sum(trans) <= K)
    m.add(sum(turns) == 12)
    tsel = {}
    for p, f in full.items():
        if label[p] == 'A' and 2 <= hexd(p) <= tmax and wedge30(p) and (only_T is None or p == only_T):
            tsel[p] = m.new_bool_var(''); m.add(tsel[p] <= f)
    m.add(sum(tsel.values()) == 1)
    uv = []
    for p, ids in at.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [x[i] for i in ids]); uv.append(u)
    ue = []
    for e, os in owners.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [x[i] for i in os]); ue.append(u)
    m.add(sum(uv) - sum(ue) + sum(x) == 1)
    root = at[(0, 0)][0]
    rank = [m.new_int_var(0, len(ts), '') for _ in ts]; m.add(rank[root] == 0); par = [[] for _ in ts]
    for e, os in owners.items():
        if len(os) != 2: continue
        for u, v in (os, os[::-1]):
            b = m.new_bool_var(''); m.add(b <= x[u]); m.add(b <= x[v]); par[v].append(b)
            m.add(rank[v] >= rank[u] + 1).only_enforce_if(b)
    for i in range(len(ts)):
        if i != root: m.add(sum(par[i]) == x[i])
    W = sum(costs); m.add(W <= wmax)
    return m, ts, x, tsel, W


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--K', type=int, required=True)
    ap.add_argument('--wmax', type=int, default=21)
    ap.add_argument('--radius', type=int, help='hex window radius (default K+3, the lemma value)')
    ap.add_argument('--bound', type=int, default=12, help='first shooter bound (edge lengths)')
    ap.add_argument('--bound2', type=int, default=40, help='escalated shooter bound for survivors')
    ap.add_argument('--paths', type=int, default=6, help='cuts added per lit proposal')
    ap.add_argument('--seconds', type=float, default=1800, help='total wall-clock budget')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--T', type=int, nargs=2, help='fix T = i e1 + j e2')
    ap.add_argument('--ellipse', action='store_true', help='per-T window from the phase 2 lemma (needs --T)')
    ap.add_argument('--out', required=True)
    a = ap.parse_args(); t0 = time.monotonic()
    radius = a.radius if a.radius is not None else a.K + 3
    onlyT = (12*a.T[0] + 6*a.T[1], 6*a.T[1]) if a.T else None
    if a.ellipse: radius = max(radius, 2*(a.K-1) + 7)  # big enough to contain the ellipse
    m, ts, x, tsel, W = build(radius, a.K, a.wmax, a.K + 1, onlyT, a.ellipse)
    index = TileIndex(ts)
    log = open(HERE / f'phase2-search-{a.out}.log', 'w')
    def emit(d):
        print(json.dumps(d), flush=True); log.write(json.dumps(d) + '\n'); log.flush()
    emit(dict(event='model', tiles=len(ts), radius=radius, args=vars(a)))
    it = cuts = 0; candidates = []; status = None; solve_time = 0
    while True:
        left = a.seconds - (time.monotonic() - t0)
        if left <= 5: status = 'BUDGET_EXHAUSTED'; break
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = left; s.parameters.num_search_workers = a.workers
        st = s.solve(m); solve_time += s.wall_time; it += 1
        if st == cp_model.INFEASIBLE: status = 'INFEASIBLE'; break
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): status = s.status_name(st); break
        room = [ts[i] for i in range(len(ts)) if s.value(x[i])]
        T = next(p for p, v in tsel.items() if s.value(v))
        info, corners = analyze(room)
        assert info['walls'] == s.value(W), (info['walls'], s.value(W))
        paths, shots = find_paths((0, 0), T, corners, a.bound, a.paths)
        if not paths:
            paths, shots = find_paths((0, 0), T, corners, a.bound2, a.paths)
        if not paths:
            mir = mirror_exact((0, 0), T, corners)
            cand = dict(T=list(T), walls=info['walls'], tiles=[[list(p) for p in t] for t in room],
                        transparent_C=info['transparent_C'], interior_A=info['interior_A'], mirror=mir, shots=shots)
            candidates.append(cand); emit(dict(event='dark_candidate', it=it, T=T, walls=info['walls'], transparent=len(info['transparent_C'])))
            ids = {i for i in range(len(ts)) if s.value(x[i])}
            m.add_bool_or([x[i].Not() if i in ids else x[i] for i in range(len(ts))] + [tsel[T].Not()])
            continue
        for pth in paths:
            pres, absn = support(pth['path'], pth['walls'], index)
            assert all(s.value(x[i]) for i in pres) and not any(s.value(x[i]) for i in absn)
            m.add_bool_or([x[i].Not() for i in pres] + [x[i] for i in absn] + [tsel[T].Not()]); cuts += 1
        if it % 25 == 0 or it <= 5:
            emit(dict(event='iter', it=it, cuts=cuts, walls=info['walls'], T=T, transparent=len(info['transparent_C']),
                      tiles=len(room), first_path_X=paths[0]['X'], legs=len(paths[0]['path']) - 1,
                      elapsed=round(time.monotonic() - t0, 1)))
    res = dict(status=status, iterations=it, cuts=cuts, candidates=len(candidates), solve_seconds=round(solve_time, 1),
               total_seconds=round(time.monotonic() - t0, 1), window=dict(kind='ellipse' if a.ellipse else 'hex', radius=radius, tiles=len(ts),
               ellipse_sum=(2*(a.K-1) + 6 - hexd(onlyT)) if a.ellipse else None),
               T_hex_distance=[2, a.K + 1], args=vars(a), dark_candidates=candidates)
    (HERE / f'phase2-search-{a.out}.json').write_text(json.dumps(res, indent=1, default=str))
    emit({k: v for k, v in res.items() if k != 'dark_candidates'})


if __name__ == '__main__':
    main()
