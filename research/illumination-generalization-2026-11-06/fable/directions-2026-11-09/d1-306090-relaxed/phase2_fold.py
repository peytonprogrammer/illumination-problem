"""Phase 2 task 1: fold family.

Base B: simple C-clean polyform (every C point of B has 1 or 3 tiles of B).
S' = (0,0) is flat on B's boundary along mirror line l1 (exactly its 6 tiles on one
side): l1 = x-axis ('edge' type, lattice edge) or y-axis ('alt' type, altitude).
Mode F3: T' is a second A point, flat on B's boundary along a mirror line l2
  (exactly 6 tiles on one side of one of its 6 mirror lines). Q = B u s1 B u s2 B.
Mode F2: T' is an interior A point of B. Q = B u s1 B.
W(Q) >= 3 w_B - 8 (F3) or 2 w_B - 4 (F2), since only seam endpoints merge.
Step 1: minimise w_B. Step 2: enumerate all bases with w_B <= cap, build Q exactly,
keep strictly simple Q with S, T interior and copies glued only along their seams,
and record W(Q).
"""
import argparse, itertools, json, time
from fractions import Fraction as F
from pathlib import Path
from ortools.sat.python import cp_model
from search_relaxed import tiles_of, wedge
from check_room import analyze, label

HERE = Path(__file__).parent


def refl(p, a, d):
    """Reflect point p across the line through a with direction d (metric diag(1,3))."""
    w = (p[0]-a[0], p[1]-a[1]); dd = d[0]*d[0] + 3*d[1]*d[1]; lam = F(2*(w[0]*d[0] + 3*w[1]*d[1]), dd)
    r = (a[0] + lam*d[0] - w[0], a[1] + lam*d[1] - w[1]); assert all(c.denominator == 1 for c in r)
    return (int(r[0]), int(r[1]))


LINES = [(1, 0), (1, 1), (-1, 1), (0, 1), (3, 1), (-3, 1)]  # 3 lattice-edge + 3 altitude directions


def side(t, a, d):
    c = (sum(q[0] for q in t) - 3*a[0], sum(q[1] for q in t) - 3*a[1]); s = d[0]*c[1] - d[1]*c[0]
    assert s != 0; return s > 0


def build(radius, l1, mode):
    ts, lab = tiles_of('hex', radius); idx = {tuple(sorted(t)): i for i, t in enumerate(ts)}
    m = cp_model.CpModel(); b = [m.new_bool_var('') for _ in ts]
    at, owners = {}, {}
    for i, t in enumerate(ts):
        for p in t: at.setdefault(p, []).append(i)
        for p, q in itertools.combinations(t, 2): owners.setdefault(frozenset((p, q)), []).append(i)
    costs, turns, full = [], [], {}
    for p, ids in at.items():
        wd = [wedge(ts[i], p) for i in ids]; rows = []
        for bits in itertools.product((0, 1), repeat=len(ids)):
            occ = set().union(*[w for w, x in zip(wd, bits) if x]) if any(bits) else set(); u = len(occ)
            if u == 0: rows.append(list(bits) + [0, 0, 0]); continue
            if u == 12:
                if lab[p] == 'C': continue
                rows.append(list(bits) + [0, 0, int(lab[p] == 'A')]); continue
            if sum(1 for s in occ if (s-1) % 12 not in occ) != 1: continue
            if lab[p] == 'C' and u not in (3, 9): continue
            rows.append(list(bits) + [int(u != 6), 6-u, 0])
        c = m.new_bool_var(''); tr = m.new_int_var(-6, 6, ''); f = m.new_bool_var('')
        m.add_allowed_assignments([b[i] for i in ids] + [c, tr, f], rows); costs.append(c); turns.append(tr); full[p] = f
    m.add(sum(turns) == 12)
    d1 = (1, 0) if l1 == 'edge' else (0, 1)
    for i in at[(0, 0)]: m.add(b[i] == int(side(ts[i], (0, 0), d1)))
    sel = {}
    for p, ids in at.items():
        if lab[p] != 'A' or p == (0, 0) or len(ids) != 12: continue
        if mode == 'F2':
            sel[(p, None)] = full[p]
        else:
            for d in LINES:
                for sgn in (True, False):
                    v = m.new_bool_var(''); sel[(p, d, sgn)] = v
                    for i in ids: m.add(b[i] == int(side(ts[i], p, d) == sgn)).only_enforce_if(v)
    m.add(sum(sel.values()) == 1) if mode == 'F3' else m.add(sum(sel.values()) >= 1)
    for i, t in enumerate(ts):  # B and s1 B are disjoint
        j = idx.get(tuple(sorted(refl(q, (0, 0), d1) for q in t)))
        if j is not None and j > i: m.add(b[i] + b[j] <= 1)
    uv, ue = [], []
    for p, ids in at.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [b[i] for i in ids]); uv.append(u)
    for e, os in owners.items():
        u = m.new_bool_var(''); m.add_max_equality(u, [b[i] for i in os]); ue.append(u)
    m.add(sum(uv) - sum(ue) + sum(b) == 1)
    root = next(i for i in at[(0, 0)] if side(ts[i], (0, 0), d1))
    rank = [m.new_int_var(0, len(ts), '') for _ in ts]; m.add(rank[root] == 0); par = [[] for _ in ts]
    for e, os in owners.items():
        if len(os) != 2: continue
        for u, v in (os, os[::-1]):
            z = m.new_bool_var(''); m.add(z <= b[u]); m.add(z <= b[v]); par[v].append(z)
            m.add(rank[v] >= rank[u] + 1).only_enforce_if(z)
    for i in range(len(ts)):
        if i != root: m.add(sum(par[i]) == b[i])
    return m, ts, b, sel, sum(costs), d1, idx


def build_Q(base, d1, Tsel, mode):
    """Return (Q tiles, info) or (None, reason)."""
    S = (0, 0)
    copies = [[tuple(t) for t in base], [tuple(refl(q, S, d1) for q in t) for t in base]]
    seams = {(0, 1): d1}
    if mode == 'F3':
        T, d2 = Tsel[0], Tsel[1]
        copies.append([tuple(refl(q, T, d2) for q in t) for t in base]); seams[(0, 2)] = d2
    owner = {}
    for k, cp in enumerate(copies):
        for t in cp:
            key = frozenset(t)
            if key in owner: return None, 'copies overlap'
            owner[key] = k
    # copies may share an edge only along their designated seam line
    edges = {}
    for key, k in owner.items():
        for e in itertools.combinations(sorted(key), 2): edges.setdefault(e, set()).add(k)
    for e, ks in edges.items():
        if len(ks) < 2: continue
        pair = tuple(sorted(ks))
        if pair not in seams: return None, f'copies {pair} adjacent off-seam'
        a = (0, 0) if pair == (0, 1) else Tsel[0]; d = seams[pair]
        if any((q[0]-a[0])*d[1] - (q[1]-a[1])*d[0] != 0 for q in e): return None, 'adjacent off seam line'
    Q = [tuple(t) for t in owner]
    try:
        info, corners = analyze(Q)
    except AssertionError as ex:
        return None, f'not simple: {ex}'
    T = Tsel[0]
    if [0, 0] not in info['interior_A'] or list(T) not in info['interior_A']: return None, 'S or T not interior'
    return Q, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--radius', type=int, default=4); ap.add_argument('--l1', choices=['edge', 'alt'], required=True)
    ap.add_argument('--mode', choices=['F2', 'F3'], required=True)
    ap.add_argument('--seconds', type=float, default=1700); ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args(); t0 = time.monotonic(); tag = f'{a.mode}-{a.l1}-hex{a.radius}'
    m, ts, b, sel, wB, d1, idx = build(a.radius, a.l1, a.mode)
    m.minimize(wB); copies = 2 if a.mode == 'F2' else 3; merge = 4 if a.mode == 'F2' else 8
    best = None; rooms = []; rej = {}; it = 0; status = None; first_min = None; lb = None
    while True:
        left = a.seconds - (time.monotonic() - t0)
        if left < 5: status = 'BUDGET'; break
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = left; s.parameters.num_search_workers = a.workers
        st = s.solve(m); it += 1
        if st == cp_model.INFEASIBLE: status = 'EXHAUSTED'; break
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): status = s.status_name(st); break
        w = round(s.objective_value); lb = w if st == cp_model.OPTIMAL else s.best_objective_bound
        if first_min is None: first_min = w
        if best is not None and copies * lb - merge >= best['WQ']: status = 'CERTIFIED_MIN'; break
        on = {i for i in range(len(ts)) if s.value(b[i])}; base = [ts[i] for i in sorted(on)]
        key = next(k for k, v in sel.items() if s.value(v))
        Q, info = build_Q(base, d1, key, a.mode)
        if Q is None:
            rej[info[:30]] = rej.get(info[:30], 0) + 1
            if info == 'copies overlap' and a.mode == 'F3':
                T, d2 = key[0], key[1]; img2 = {}
                for i in on:
                    j = idx.get(tuple(sorted(refl(q, T, d2) for q in ts[i])))
                    if j in on: m.add_bool_or([sel[key].Not(), b[i].Not(), b[j].Not()])
                    img2[tuple(sorted(refl(q, T, d2) for q in ts[i]))] = i
                for i in on:
                    k2 = img2.get(tuple(sorted(refl(q, (0, 0), d1) for q in ts[i])))
                    if k2 is not None: m.add_bool_or([sel[key].Not(), b[i].Not(), b[k2].Not()])
        else:
            rec = dict(wB=w, WQ=info['walls'], T=list(key[0]), l2=list(key[1]) if key[1] else None,
                       transparent_C=info['transparent_C'], base=[[list(p) for p in t] for t in base],
                       Q=[[list(p) for p in t] for t in Q])
            rooms.append(rec)
            if best is None or rec['WQ'] < best['WQ']: best = rec
            print(json.dumps(dict(event='room', it=it, wB=w, WQ=rec['WQ'], transparent=len(rec['transparent_C']))), flush=True)
        m.add_bool_or([b[i].Not() if i in on else b[i] for i in range(len(ts))] + [sel[key].Not()])
    res = dict(family=a.mode, l1=a.l1, window=dict(kind='hex', radius=a.radius, tiles=len(ts)), status=status,
               iterations=it, min_wB=first_min, last_wB_bound=lb, min_WQ=best['WQ'] if best else None,
               rejections=rej, valid_rooms=len(rooms), best=best, others=sorted(rooms, key=lambda r: r['WQ'])[1:6],
               seconds=round(time.monotonic() - t0, 1))
    (HERE / f'phase2-fold-{tag}.json').write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k not in ('best', 'others')}))


if __name__ == '__main__':
    main()
