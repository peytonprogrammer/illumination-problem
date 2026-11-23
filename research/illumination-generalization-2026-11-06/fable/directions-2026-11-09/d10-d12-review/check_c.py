"""Lemma C (cylinder witnesses) of d12-lit-side/notes.md, tested from the definition.

For every plain state and arc, find the pairs of regular a-points with a CylA or CylB
witness. Close the set under M (computed as in check_m.py). Lemma C says every such pair
is LIT. The script compares with the census verdicts and with the per-corner flags in
d12-lit-side/mine_nN.json.

Run: python3 -B check_c.py N [workers]      -> prints counts
"""
import json
import sys
from collections import Counter
from multiprocessing import Pool

from lib import (D12, mul, inv, cyc_id, conj_fn, pure_move, GENS, initial_labels, canon,
                 conjugators, census_orbits)
from check_m import generate


def comps(p, q):
    n = len(p)
    comp = [-1] * n
    c = 0
    for i in range(n):
        if comp[i] < 0:
            comp[i] = c
            st = [i]
            while st:
                x = st.pop()
                for y in (p[x], q[x]):
                    if comp[y] < 0:
                        comp[y] = c
                        st.append(y)
            c += 1
    return comp, c


def all_two(g, comp, nc):
    """reg[k] is True when every cycle of g inside component k has length 2."""
    reg = [True] * nc
    for i in range(len(g)):
        if g[g[i]] != i or g[i] == i:
            reg[comp[i]] = False
    return reg


def cyl_pairs(qq, rr, ss, pp, pt):
    n = len(qq)
    G, nG = comps(qq, rr)
    T, nT = comps(ss, pp)
    A, lens = cyc_id(mul(qq, rr))
    regG = [a and b for a, b in zip(all_two(qq, G, nG), all_two(rr, G, nG))]
    regT = [a and b for a, b in zip(all_two(ss, T, nT), all_two(pp, T, nT))]
    par = list(range(len(lens)))

    def find(u):
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        return u

    first = {}
    for i in range(n):
        for key, ok in ((('G', G[i]), regG[G[i]]), (('T', T[i]), regT[T[i]])):
            if ok:
                j = first.setdefault(key, A[i])
                ru, rv = find(j), find(A[i])
                if ru != rv:
                    par[ru] = rv
    info = {}
    for i in range(n):
        P = pt[i]
        if P >= 0:
            e = info.setdefault(P, [set(), G[i]])
            e[0].add(find(A[i]))
    out = set()
    ids = sorted(info)
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            cP, gP = info[ids[a]]
            cQ, gQ = info[ids[b]]
            if not (cP & cQ):
                continue
            if regG[gP] or regG[gQ]:
                out.add((ids[a], ids[b]))            # CylA
            elif gP != gQ:
                out.add((ids[a], ids[b]))            # CylB
    return out


def analyse(job):
    n, cts, o = job
    t0 = tuple(tuple(g) for g in o['rep'])
    pt0 = initial_labels(t0[0])
    ids = sorted({P for P in pt0 if P >= 0})
    q = len(ids)
    pos = {P: i for i, P in enumerate(ids)}
    index = {canon(t0): 0}
    reps = [(t0, pt0)]
    gens = set()
    for c in conjugators(t0, t0):
        ptc = [0] * n
        for s in range(n):
            ptc[c[s]] = pt0[s]
        gens.add(tuple(pos[ptc[next(s for s in range(n) if pt0[s] == P)]] for P in ids))
    raw = {1: set(), 2: set(), 3: set()}
    cur = 0
    while cur < len(reps):
        t, pt = reps[cur]
        cur += 1
        tb = conj_fn(t[1], inv(t[0]))
        for x, arc in ((1, (t[0], t[1], t[2], t[3])), (2, (t[0], t[2], t[3], tb)),
                       (3, (t[3], t[0], t[1], t[2]))):
            raw[x] |= cyl_pairs(*arc, pt)
        for (i, s) in GENS:
            t2, pt2 = pure_move(t, pt, i, s)
            key = canon(t2)
            v = index.get(key)
            if v is None:
                index[key] = len(reps)
                reps.append((t2, pt2))
                continue
            tv, ptv = reps[v]
            for c in conjugators(t2, tv):
                pt3 = [0] * n
                for sh in range(n):
                    pt3[c[sh]] = pt2[sh]
                r = [None] * q
                for sh in range(n):
                    if ptv[sh] >= 0:
                        r[pos[ptv[sh]]] = pos[pt3[sh]]
                gens.add(tuple(r))
    M = generate(list(gens), q)
    cyl = {x: {tuple(sorted((g[pos[a]], g[pos[b]]))) for (a, b) in raw[x] for g in M} for x in (1, 2, 3)}
    res = []
    for p in o['pairs']:
        key = tuple(sorted((pos[pt0[p['sheets_P'][0]]], pos[pt0[p['sheets_Q'][0]]])))
        res.append((p['P'], p['Q'], p['lit'], [int(key in cyl[x]) for x in (1, 2, 3)]))
    return json.dumps(o['rep']), cts, o['primitive'], res


def main():
    n = int(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    assert workers <= 2
    theirs = {json.dumps(o['rep']): {(p['P'], p['Q']): p for p in o['pairs']}
              for o in json.loads((D12 / f'mine_n{n}.json').read_text())['orbits']}
    jobs = [(n, cts, o) for cts, o in census_orbits(n)]
    jobs.sort(key=lambda j: -j[2]['plain_orbit_size'])
    S = Counter()
    with Pool(workers) as pool:
        for rep, cts, prim, res in pool.imap_unordered(analyse, jobs, chunksize=1):
            prim_hyp = prim and all(len(c) < n for c in cts[1:]) and any(2 in c for c in cts[1:])
            for P, Q, lit, cx in res:
                S['pairs'] += 1
                has = any(cx)
                S['DARK pairs with a cylinder witness (Lemma C false)'] += (has and not lit)
                S['LIT pairs'] += lit
                S['LIT pairs with no cylinder witness'] += (lit and not has)
                if prim_hyp:
                    S['PRIM pairs'] += 1
                    S['PRIM pairs with a cylinder witness'] += has
                th = theirs[rep][(P, Q)]['cyl_x']
                S['pair-corner cylinder flag differs from d12'] += sum(
                    1 for a, b in zip(cx, th) if bool(a) != bool(b))
    print(n)
    for k, v in S.items():
        print('   ', k, v)


if __name__ == '__main__':
    main()
