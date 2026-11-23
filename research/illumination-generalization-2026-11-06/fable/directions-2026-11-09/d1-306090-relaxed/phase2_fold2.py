"""Phase 2 task 1, direct model of the F3 fold family for fixed (T, l2).

Q = B u s1 B u s2 B with s1 the reflection in l1 = x-axis through S=(0,0) and s2 the
reflection in l2 through T. Hard constraints:
  * the three copies are disjoint; copies share edges only along their seam line
    (B|s1B on l1, B|s2B on l2, never s1B|s2B);
  * B is C-clean (every C point has 0, 1 or 3 tiles of B);
  * B has exactly the 6 tiles above l1 at S and the 6 tiles on one side of l2 at T;
  * Q is a simple polygon (contiguous fans, Euler characteristic 1, connected);
Objective: walls of Q. Transparent C points of Q are unconstrained.
Usage: phase2_fold2.py --T i j --l2 dx dy --side 0|1 [--radius R]
"""
import argparse, itertools, json, time
from pathlib import Path
from ortools.sat.python import cp_model
from search_relaxed import tiles_of, wedge
from phase2_fold import refl, side
from phase2_cegar import rows_for

HERE = Path(__file__).parent


def on_line(e, a, d):
    return all((q[0]-a[0])*d[1] - (q[1]-a[1])*d[0] == 0 for q in e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--T', type=int, nargs=2, required=True); ap.add_argument('--l2', type=int, nargs=2, required=True)
    ap.add_argument('--side', type=int, choices=[0, 1], required=True); ap.add_argument('--radius', type=int, default=5)
    ap.add_argument('--seconds', type=float, default=600); ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--wmax', type=int); ap.add_argument('--out', required=True)
    a = ap.parse_args(); t0 = time.monotonic()
    S = (0, 0); T = (12*a.T[0] + 6*a.T[1], 6*a.T[1]); d1 = (1, 0); d2 = tuple(a.l2)
    ts, lab = tiles_of('hex', a.radius); key = lambda t: tuple(sorted(t)); idx = {key(t): i for i, t in enumerate(ts)}
    s1 = [idx.get(key([refl(q, S, d1) for q in t])) for t in ts]
    s2 = [idx.get(key([refl(q, T, d2) for q in t])) for t in ts]
    m = cp_model.CpModel(); b = [m.new_bool_var('') for _ in ts]
    for i in range(len(ts)):
        if s1[i] is None or s2[i] is None: m.add(b[i] == 0)
    # copy membership of window tile i: c0 = b[i], c1 = b[s1[i]], c2 = b[s2[i]]
    def cp(k, i):
        j = i if k == 0 else (s1[i] if k == 1 else s2[i]); return None if j is None else b[j]
    x = []
    for i in range(len(ts)):
        lits = [l for l in (cp(0, i), cp(1, i), cp(2, i)) if l is not None]
        m.add(sum(lits) <= 1); xi = m.new_bool_var(''); m.add(xi == sum(lits)); x.append(xi)
    at, owners = {}, {}
    for i, t in enumerate(ts):
        for p in t: at.setdefault(p, []).append(i)
        for p, q in itertools.combinations(t, 2): owners.setdefault(frozenset((p, q)), []).append(i)
    for e, os in owners.items():
        if len(os) != 2: continue
        u, v = os
        for (k1, k2) in itertools.permutations(range(3), 2):
            ok = (sorted((k1, k2)) == [0, 1] and on_line(e, S, d1)) or (sorted((k1, k2)) == [0, 2] and on_line(e, T, d2))
            if ok: continue
            l1_, l2_ = cp(k1, u), cp(k2, v)
            if l1_ is not None and l2_ is not None: m.add_bool_or([l1_.Not(), l2_.Not()])
    # B C-clean
    for p, ids in at.items():
        if lab[p] != 'C': continue
        n = m.new_int_var(0, 4, ''); m.add(n == sum(b[i] for i in ids))
        m.add_allowed_assignments([n], [[0], [1], [3]])
    for i in at[S]: m.add(b[i] == int(side(ts[i], S, d1)))
    for i in at[T]: m.add(b[i] == int(side(ts[i], T, d2) == bool(a.side)))
    # Q simple polygon with S, T interior
    costs, turns = [], []
    for p, ids in at.items():
        rows = rows_for(ids, [wedge(ts[i], p) for i in ids], lab[p])
        c = m.new_bool_var(''); tr = m.new_int_var(-6, 6, ''); f = m.new_bool_var(''); z = m.new_bool_var('')
        m.add_allowed_assignments([x[i] for i in ids] + [c, tr, f, z], rows); costs.append(c); turns.append(tr)
        if p in (S, T): m.add(f == 1)
    m.add(sum(turns) == 12)
    uv, ue = [], []
    for p, ids in at.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [x[i] for i in ids]); uv.append(u)
    for e, os in owners.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [x[i] for i in os]); ue.append(u)
    m.add(sum(uv) - sum(ue) + sum(x) == 1)
    root = at[S][0]; rank = [m.new_int_var(0, len(ts), '') for _ in ts]; m.add(rank[root] == 0); par = [[] for _ in ts]
    for e, os in owners.items():
        if len(os) != 2: continue
        for u, v in (os, os[::-1]):
            z = m.new_bool_var(''); m.add(z <= x[u]); m.add(z <= x[v]); par[v].append(z)
            m.add(rank[v] >= rank[u] + 1).only_enforce_if(z)
    for i in range(len(ts)):
        if i != root: m.add(sum(par[i]) == x[i])
    W = sum(costs)
    if a.wmax: m.add(W <= a.wmax)
    m.minimize(W)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = a.seconds; s.parameters.num_search_workers = a.workers
    st = s.solve(m); ok = st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    res = dict(T=list(a.T), l2=list(d2), side=a.side, radius=a.radius, status=s.status_name(st),
               WQ=round(s.objective_value) if ok else None, bound=s.best_objective_bound, seconds=round(time.monotonic() - t0, 1))
    if ok:
        res['rec'] = dict(T=list(T), l2=list(d2), base=[[list(p) for p in ts[i]] for i in range(len(ts)) if s.value(b[i])],
                          Q=[[list(p) for p in ts[i]] for i in range(len(ts)) if s.value(x[i])])
    (HERE / f'phase2-fold2-{a.out}.json').write_text(json.dumps(res))
    print(json.dumps({k: v for k, v in res.items() if k != 'rec'}), flush=True)


if __name__ == '__main__':
    main()
