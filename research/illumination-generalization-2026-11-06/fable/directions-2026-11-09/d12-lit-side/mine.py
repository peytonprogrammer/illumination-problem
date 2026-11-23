"""Witness mining on the saved d6 census (no enumeration of new covers).

For every saved pure-braid orbit with at least two 2-cycles in g_a, rebuild the fully
marked orbit graph (states = (tuple, IDs of the regular points over a) up to conjugation,
edges = s0^2, s0^-2, s1^2, s1^-2) and record, per pair of regular points over a:

  * per corner x: is the pair joined by a chain in some state (x-lit), minimal chain length
    (number of 2-cycles of g_x traversed), and the same for cylinder witnesses;
  * the distance (pure-braid word length in the four generators) from every state of the
    orbit to the nearest state with a connecting chain: maximum and histogram;
  * the same with witnesses restricted to chain length 1;
  * static data in the saved basis: fibres of the canonical factor Q / B_x, and the
    certificates Par / Rig / Cut of d10 per corner (imported from unified_test.py);
  * the group M induced on the regular points over a by the stabiliser of the plain tuple.

Cylinder witnesses (abstract Lemma A / A'), per state and arc a -> x with complementary arc:
  Gamma = orbits of <g_a, g_x>, T = orbits of the two other loops, annuli = cycles of the
  core monodromy; a component is a regular closed leaf when all its vertices are 2-cycles.
  Maximal cylinders are chains of annuli glued across regular leaves.
  CylA: one mark on a regular closed leaf inside a cylinder whose closure contains the other.
  CylB: the marks lie on the two different boundary components of one cylinder.

Run: python3 -B mine.py N [workers] [max_marked_states]   -> mine_nN.json
"""
import json
import sys
import time
from array import array
from collections import deque, Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
D10 = HERE.parent / 'd10-mechanisms'
sys.path.insert(0, str(D6))
sys.path.insert(0, str(D10))
import d4_monodromy as d4                                   # noqa: E402
from hurwitz import (mul, move, pure_move, canon_marked, canon_plain, initial_pt,
                     PURE_GENS)                              # noqa: E402
import unified_test as UT                                   # noqa: E402

LABELS = ('a', 'b', 'c', 'd')


def cyc_info(p):
    n = len(p)
    cid = [-1] * n
    lens = []
    for i in range(n):
        if cid[i] < 0:
            k = len(lens)
            j = i
            L = 0
            while cid[j] < 0:
                cid[j] = k
                j = p[j]
                L += 1
            lens.append(L)
    return cid, lens


def orbits2(p, q):
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


def chains(pt, tx):
    """{(P, Q): number of 2-cycles of g_x on the chain from P to Q} for P < Q."""
    adj = {}
    for i, j in enumerate(tx):
        if i < j and tx[j] == i:
            P, Q = pt[i], pt[j]
            if P >= 0 and Q >= 0 and P != Q:
                adj.setdefault(P, []).append(Q)
                adj.setdefault(Q, []).append(P)
    res = {}
    for P in adj:
        dist = {P: 0}
        dq = [P]
        for u in dq:
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    dq.append(v)
        for Q, dv in dist.items():
            if Q > P:
                res[(P, Q)] = dv
    return res


def cyl_pairs(q, r, s, p, pt):
    """Arc between the punctures of loops q, r (adjacent, product q r s p = 1).
    Returns {(P, Q): 'A' or 'B'} for regular a-points P < Q (a is q or r; pt gives IDs)."""
    n = len(q)
    cq, lq = cyc_info(q)
    cr, lr = cyc_info(r)
    cs, ls = cyc_info(s)
    cp, lp = cyc_info(p)
    G, nG = orbits2(q, r)
    T, nT = orbits2(s, p)
    A, lA = cyc_info(mul(q, r))
    nA = len(lA)
    assert nG + nT - nA == 1, 'cylinder graph is not a tree: convention error'
    regG = [True] * nG
    regT = [True] * nT
    for i in range(n):
        if lq[cq[i]] != 2 or lr[cr[i]] != 2:
            regG[G[i]] = False
        if ls[cs[i]] != 2 or lp[cp[i]] != 2:
            regT[T[i]] = False
    par = list(range(nA))

    def find(u):
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        return u

    firstG = [-1] * nG
    firstT = [-1] * nT
    for i in range(n):
        g = G[i]
        if regG[g]:
            if firstG[g] < 0:
                firstG[g] = A[i]
            else:
                ru, rv = find(firstG[g]), find(A[i])
                if ru != rv:
                    par[ru] = rv
        h = T[i]
        if regT[h]:
            if firstT[h] < 0:
                firstT[h] = A[i]
            else:
                ru, rv = find(firstT[h]), find(A[i])
                if ru != rv:
                    par[ru] = rv
    info = {}
    for i in range(n):
        P = pt[i]
        if P >= 0:
            e = info.get(P)
            if e is None:
                e = info[P] = [set(), regG[G[i]], G[i]]
            e[0].add(find(A[i]))
    out = {}
    ids = sorted(info)
    for x in range(len(ids)):
        cP, iP, nP = info[ids[x]]
        for y in range(x + 1, len(ids)):
            cQ, iQ, nQ = info[ids[y]]
            if cP & cQ:
                if iP or iQ:
                    out[(ids[x], ids[y])] = 'A'
                elif nP != nQ:
                    out[(ids[x], ids[y])] = 'B'
    return out


def state_arcs(t):
    """(corner index j, tx, (q, r, s, p)) for the three tail arcs from a."""
    t0, t1, t2, t3 = t
    tb, _, _ = move(t, LABELS, None, 0, +1)          # (a b a^-1, a, c, d): frees the arc a-c
    return ((1, t1, (t0, t1, t2, t3)),
            (2, t2, (t0, t2, t3, tb[0])),
            (3, t3, (t3, t0, t1, t2)))


def congruence(t, pairs):
    """Finest G-invariant partition merging the given pairs of sheets."""
    n = len(t[0])
    par = list(range(n))

    def find(u):
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        return u

    stack = list(pairs)
    while stack:
        u, v = stack.pop()
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        par[ru] = rv
        for g in t:
            stack.append((g[u], g[v]))
    return [find(i) for i in range(n)]


def static_data(t, n, pair_sheets):
    """Per pair and corner: same fibre of Q/B_x, and certificate kinds over B."""
    factors = [UT.Factor(t, part) for part in d4.all_block_systems(list(t), n)]
    proper = [F for F in factors if F.m > 1]
    Bx = {}
    for x in (1, 2, 3):
        prs = [(i, t[x][i]) for i in range(n) if t[x][t[x][i]] == i and t[x][i] > i]
        Bx[x] = congruence(t, prs)
    out = {}
    for key, (sP, sQ) in pair_sheets.items():
        rec = {}
        for x in (1, 2, 3):
            blk = Bx[x]
            fP = {blk[i] for i in sP}
            fQ = {blk[i] for i in sQ}
            same = bool(fP & fQ)
            kinds = ''
            for F in proper:
                if 'P' not in kinds and UT.par(F, x, sP[0], sQ[0]):
                    kinds += 'P'
                if 'R' not in kinds and UT.rig(F, x, sP[0], sQ[0]):
                    kinds += 'R'
                if 'C' not in kinds and UT.cut(F, t, x, sP[0], sQ[0]):
                    kinds += 'C'
            rec[x] = (same, kinds)
        out[key] = rec
    return out


def analyse_orbit(job):
    n, cts, o = job
    t0 = time.time()
    t = tuple(tuple(g) for g in o['rep'])
    cid, plen = initial_pt(t[0])
    pt = tuple(c if plen[c] == 2 else -1 for c in cid)
    ids = sorted({c for c in cid if plen[c] == 2})
    root_id = ids[0]
    pair_keys = [(ids[x], ids[y]) for x in range(len(ids)) for y in range(x + 1, len(ids))]
    kidx = {k: i for i, k in enumerate(pair_keys)}
    npairs = len(pair_keys)

    def canon(t_, pt_):
        c = canon_marked(t_, pt_, [i for i in range(n) if pt_[i] == root_id])
        return bytes(x + 1 for x in c)

    index = {canon(t, pt): 0}
    nbr = array('i')
    queue = deque([(t, pt)])
    depth = array('i', [0])
    # per pair: per corner lit, min chain; cyl flags; witness flags per state
    lit = [[False] * 4 for _ in range(npairs)]
    minch = [[0] * 4 for _ in range(npairs)]
    cyl = [[''] * 4 for _ in range(npairs)]
    wit_any = [bytearray() for _ in range(npairs)]
    wit_one = [bytearray() for _ in range(npairs)]
    plain_sets = {}
    base_plain = None
    base_ptc = None
    cur = 0
    while queue:
        t_, pt_ = queue.popleft()
        for w in wit_any:
            w.append(0)
        for w in wit_one:
            w.append(0)
        for j, tx, qrsp in state_arcs(t_):
            for key, L in chains(pt_, tx).items():
                i = kidx[key]
                lit[i][j] = True
                if minch[i][j] == 0 or L < minch[i][j]:
                    minch[i][j] = L
                wit_any[i][cur] = 1
                if L == 1:
                    wit_one[i][cur] = 1
            for key, kind in cyl_pairs(*qrsp, pt_).items():
                i = kidx[key]
                if kind not in cyl[i][j]:
                    cyl[i][j] += kind
        # group on the regular a-points induced by the stabiliser of the plain tuple
        pc, labs = canon_plain(t_, want_map=True)
        pc = bytes(pc)
        S = plain_sets.setdefault(pc, set())
        for lab in labs:
            ptc = [0] * n
            for s in range(n):
                ptc[lab[s]] = pt_[s] + 1
            S.add(bytes(ptc))
        if cur == 0:
            base_plain = pc
            lab = labs[0]
            base_ptc = [0] * n
            for s in range(n):
                base_ptc[lab[s]] = pt_[s] + 1
        for (i, s) in PURE_GENS:
            t2, _, pt2 = pure_move(t_, LABELS, pt_, i, s)
            c = canon(t2, pt2)
            k = index.get(c)
            if k is None:
                k = index[c] = len(index)
                depth.append(depth[cur] + 1)
                queue.append((t2, pt2))
            nbr.append(k)
        cur += 1
    N = cur
    del index
    # group M
    sizes = {len(S) for S in plain_sets.values()}
    M = []
    for b in plain_sets[base_plain]:
        pi = {}
        for c in range(n):
            u, v = base_ptc[c] - 1, b[c] - 1
            assert (u < 0) == (v < 0)
            if u >= 0:
                assert pi.setdefault(u, v) == v
        M.append(pi)
    # orbits of M on unordered pairs
    comp = {k: k for k in pair_keys}

    def findp(u):
        while comp[u] != u:
            comp[u] = comp[comp[u]]
            u = comp[u]
        return u

    for pi in M:
        for (P, Q) in pair_keys:
            im = tuple(sorted((pi[P], pi[Q])))
            ru, rv = findp((P, Q)), findp(im)
            if ru != rv:
                comp[ru] = rv
    pair_orbit = {k: kidx[findp(k)] for k in pair_keys}
    pt_orbits = len({min(pi[P] for pi in M) for P in ids})

    def bfs(flags):
        dist = array('i', [-1]) * N
        dq = deque()
        for s in range(N):
            if flags[s]:
                dist[s] = 0
                dq.append(s)
        if not dq:
            return None
        while dq:
            u = dq.popleft()
            du = dist[u] + 1
            for v in nbr[4 * u:4 * u + 4]:
                if dist[v] < 0:
                    dist[v] = du
                    dq.append(v)
        return dict(Counter(dist))

    sheets = {}
    for P in ids:
        sheets[P] = [i for i in range(n) if cid[i] == P]
    stat = static_data(t, n, {k: (sheets[k[0]], sheets[k[1]]) for k in pair_keys})
    census_lit = {(p['P'], p['Q']): p['lit'] for p in o['pairs']}
    pairs = []
    for key in pair_keys:
        i = kidx[key]
        h_any = bfs(wit_any[i])
        h_one = bfs(wit_one[i])
        is_lit = any(lit[i])
        assert is_lit == census_lit[key], 'verdict differs from the census'
        pairs.append(dict(
            P=key[0], Q=key[1], lit=is_lit,
            lit_x=[int(lit[i][j]) for j in (1, 2, 3)],
            minchain_x=[minch[i][j] for j in (1, 2, 3)],
            cyl_x=[cyl[i][j] for j in (1, 2, 3)],
            dist_any=h_any, dist_one=h_one,
            same_fibre_x=[int(stat[key][x][0]) for x in (1, 2, 3)],
            cert_x=[stat[key][x][1] for x in (1, 2, 3)],
            M_pair_orbit=pair_orbit[key]))
    assert N == o['marked_orbit_size'] and len(plain_sets) == o['plain_orbit_size']
    return dict(n=n, cts=cts, rep=o['rep'], order=o['order'], primitive=o['primitive'],
                contains_An=o['contains_An'], k=o['k'], deck_order=o['deck_order'],
                plain=len(plain_sets), marked=N, q=len(ids), M_order=len(M),
                M_sizes_constant=(len(sizes) == 1), M_pair_orbits=len(set(pair_orbit.values())),
                M_point_orbits=pt_orbits, max_depth=max(depth), pairs=pairs,
                seconds=round(time.time() - t0, 2))


def main():
    n = int(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else None
    d = json.loads((D6 / f'census_n{n}.json').read_text())
    jobs = []
    skipped = 0
    for cl in d['classes']:
        for o in cl['orbits']:
            if o.get('n_two_cycles_a', 0) >= 2:
                if cap and o['marked_orbit_size'] > cap:
                    skipped += 1
                    continue
                jobs.append((n, cl['cts'], o))
    del d
    jobs.sort(key=lambda j: -j[2]['marked_orbit_size'])
    t0 = time.time()
    out = []
    with Pool(workers) as pool:
        for k, rec in enumerate(pool.imap_unordered(analyse_orbit, jobs, chunksize=1)):
            out.append(rec)
            if k % 200 == 0:
                print(n, k, len(jobs), round(time.time() - t0), flush=True)
    name = f'mine_n{n}.json' if not cap else f'mine_n{n}_cap{cap}.json'
    (HERE / name).write_text(json.dumps(dict(n=n, cap=cap, skipped_orbits=skipped, orbits=out),
                                        separators=(',', ':')) + '\n')
    print('done', n, len(out), 'orbits, skipped', skipped, round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
