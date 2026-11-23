"""Independent computation of the point monodromy M_t and tests of the d12 lemmas.

Method (differs from d12-lit-side/mine.py, which enumerates the fully marked orbit):
  * Walk the PLAIN pure-braid orbit only, keeping one literal marked representative
    (t_v, labels_v) per plain state, reached along a spanning tree.
  * Every non-tree edge u -> v, and every conjugator from the moved tuple to t_v, gives a
    Schreier generator: a permutation of the regular a-point IDs. M is the group they
    generate, together with the deck group of the base tuple.
  * Per-corner lit sets are rebuilt as the M-closure of the pairs joined in the
    representatives. This is Proposition R used as a computation. The result is compared
    with the census verdicts, which come from a direct search of the marked orbit.

Per state the script also tests:
  * Lemma 1: components(a, x) + components(y', z') - cycles(h_x) = 1 for the three arcs.
  * Lemma T: every k = h_x^m that commutes with g_a and g_x induces an element of M.
    For the first few cases per orbit and arc, the braid word is applied literally.
  * Lemma F / Corollary T1: at a one-mirror pinch the cycle of h_x has length 4, and the
    transposition lies in M when no other cycle length is divisible by 4.

Run: python3 -B check_m.py N [workers] [max_plain]      -> m_nN.json.gz
"""
import json
import sys
import time
from itertools import combinations
from multiprocessing import Pool

from lib import (HERE, save_out, mul, inv, cyc, cyc_id, conj_fn, half_move, pure_move, GENS,
                 initial_labels, canon, conjugators, census_orbits)


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
    return c


def joined_pairs(pt, gx):
    """Pairs of regular a-points joined by a chain through 2-cycles of gx."""
    adj = {}
    for i, j in enumerate(gx):
        if i < j and gx[j] == i:
            P, Q = pt[i], pt[j]
            if P >= 0 and Q >= 0 and P != Q:
                adj.setdefault(P, set()).add(Q)
                adj.setdefault(Q, set()).add(P)
    out = set()
    seen = set()
    for P in adj:
        if P in seen:
            continue
        comp = [P]
        seen.add(P)
        for u in comp:
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    comp.append(v)
        for a, b in combinations(sorted(comp), 2):
            out.add((a, b))
    return out


def id_perm(pt, k, ids):
    """The permutation P -> (a-point containing k(sheet of P)), as a tuple over ids."""
    pos = {P: i for i, P in enumerate(ids)}
    r = [None] * len(ids)
    for s, P in enumerate(pt):
        if P >= 0:
            img = pt[k[s]]
            assert img >= 0
            assert r[pos[P]] in (None, pos[img])
            r[pos[P]] = pos[img]
    return tuple(r)


def literal_twist(t, pt, x, m, k):
    """Apply the pure braid word of Lemma T for arc x, m full twists. Returns True when
    the tuple returns literally and the labels move by k or by k^-1."""
    n = len(k)
    ki = inv(k)
    want = (tuple(pt[k[s]] for s in range(n)), tuple(pt[ki[s]] for s in range(n)))
    if x == 1:
        u, pu = t, pt
        for _ in range(m):
            u, pu = pure_move(u, pu, 0, +1)
        return u == t and pu in want
    if x == 2:
        u, ap, pu = half_move(t, 0, pt, 0, +1)
        for _ in range(2 * m):
            u, ap, pu = half_move(u, ap, pu, 1, +1)
        u, ap, pu = half_move(u, ap, pu, 0, -1)
        return ap == 0 and u == t and pu in want
    u, pu = t, pt
    for _ in range(m):
        u, pu = pure_move(u, pu, 1, +1)
    assert pu == pt                      # s1 never moves the loop of a
    for c in (k, ki):
        if tuple(conj_fn(g, c) for g in u) == t:
            # sheet s of u becomes sheet c(s): the new label of c(s) is pt[s]
            ci = inv(c)
            if tuple(pt[ci[s]] for s in range(n)) in want:
                return True
    return False


def generate(gens, q):
    e = tuple(range(q))
    seen = {e}
    fr = [e]
    while fr:
        nf = []
        for g in fr:
            for s in gens:
                x = tuple(s[g[i]] for i in range(q))
                if x not in seen:
                    seen.add(x)
                    nf.append(x)
        fr = nf
    return seen


def analyse(job):
    n, cts, o = job
    t0c = time.time()
    t0 = tuple(tuple(g) for g in o['rep'])
    e = tuple(range(n))
    assert mul(mul(mul(t0[0], t0[1]), t0[2]), t0[3]) == e
    pt0 = initial_labels(t0[0])
    ids = sorted({P for P in pt0 if P >= 0})
    q = len(ids)
    pos = {P: i for i, P in enumerate(ids)}
    index = {canon(t0): 0}
    reps = [(t0, pt0)]
    gens = set()
    for c in conjugators(t0, t0):                    # deck group of the base tuple
        ptc = [0] * n
        for s in range(n):
            ptc[c[s]] = pt0[s]
        gens.add(tuple(pos[ptc[next(s for s in range(n) if pt0[s] == P)]] for P in ids))
    deck_order = len(conjugators(t0, t0))
    raw = {1: set(), 2: set(), 3: set()}             # pairs joined in a representative
    one = {1: set(), 2: set(), 3: set()}             # joined by one mirror
    twists = set()
    pinch = set()
    stats = dict(tree_fail=0, twist_cases=0, twist_nontrivial=0, literal_ok=0, literal_fail=0,
                 pinch_cases=0, pinch_not4=0, pinch_t1=0)
    lit_budget = {1: 4, 2: 4, 3: 4}
    cur = 0
    while cur < len(reps):
        t, pt = reps[cur]
        cur += 1
        ga = t[0]
        tb = conj_fn(t[1], inv(ga))                 # g_a g_b g_a^-1 : apply g_a, g_b, g_a^-1
        arcs = ((1, (t[0], t[1], t[2], t[3])),
                (2, (t[0], t[2], t[3], tb)),
                (3, (t[3], t[0], t[1], t[2])))
        for x, (qq, rr, ss, pp) in arcs:
            gx = t[x]
            h = mul(qq, rr)
            assert mul(mul(h, ss), pp) == e
            hc, hl = cyc_id(h)
            if orbits2(qq, rr) + orbits2(ss, pp) - len(hl) != 1:
                stats['tree_fail'] += 1
            raw[x] |= joined_pairs(pt, gx)
            # one-mirror pinches
            for i, j in enumerate(gx):
                if i < j and gx[j] == i and pt[i] >= 0 and pt[j] >= 0 and pt[i] != pt[j]:
                    P, Q = sorted((pt[i], pt[j]))
                    one[x].add((P, Q))
                    oi, oj = ga[i], ga[j]
                    if gx[oi] == oi and gx[oj] == oj:
                        stats['pinch_cases'] += 1
                        if hl[hc[i]] != 4 or len({hc[i], hc[j], hc[oi], hc[oj]}) != 1:
                            stats['pinch_not4'] += 1
                        if not any(L % 4 == 0 for c, L in enumerate(hl) if c != hc[i]):
                            stats['pinch_t1'] += 1
                            r = list(range(q))
                            r[pos[P]], r[pos[Q]] = pos[Q], pos[P]
                            pinch.add(tuple(r))
            # twist elements
            k = h
            m = 1
            while k != e:
                if mul(k, ga) == mul(ga, k) and mul(k, gx) == mul(gx, k):
                    pi = id_perm(pt, k, ids)
                    stats['twist_cases'] += 1
                    if pi != tuple(range(q)):
                        stats['twist_nontrivial'] += 1
                    twists.add(pi)
                    if lit_budget[x] > 0 and m <= 60:
                        lit_budget[x] -= 1
                        if literal_twist(t, pt, x, m, k):
                            stats['literal_ok'] += 1
                        else:
                            stats['literal_fail'] += 1
                    break                            # later commuting powers are powers of this one
                k = mul(k, h)
                m += 1
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
                    a_, b_ = ptv[sh], pt3[sh]
                    assert (a_ < 0) == (b_ < 0)
                    if a_ >= 0:
                        assert r[pos[a_]] in (None, pos[b_])
                        r[pos[a_]] = pos[b_]
                gens.add(tuple(r))
    M = generate(list(gens), q)
    pairs = [(a, b) for a in range(q) for b in range(a + 1, q)]
    # orbits of M on unordered pairs
    orb = {}
    for pr in pairs:
        if pr in orb:
            continue
        O = {tuple(sorted((g[pr[0]], g[pr[1]]))) for g in M}
        for z in O:
            orb[z] = min(O)
    n_pair_orbits = len(set(orb.values()))
    lit = {}
    onel = {}
    for x in (1, 2, 3):
        lit[x] = {tuple(sorted((g[pos[a]], g[pos[b]]))) for (a, b) in raw[x] for g in M}
        onel[x] = {tuple(sorted((g[pos[a]], g[pos[b]]))) for (a, b) in one[x] for g in M}
    # comparison with the census verdicts
    mismatch = 0
    plist = []
    for p in o['pairs']:
        P, Q = pt0[p['sheets_P'][0]], pt0[p['sheets_Q'][0]]
        key = tuple(sorted((pos[P], pos[Q])))
        mine = [int(key in lit[x]) for x in (1, 2, 3)]
        if any(mine) != p['lit']:
            mismatch += 1
        plist.append(dict(P=p['P'], Q=p['Q'], lit=p['lit'], lit_x=mine,
                          one_x=[int(key in onel[x]) for x in (1, 2, 3)],
                          pair_orbit=pairs.index(orb[key])))
    twists_in_M = all(g in M for g in twists)
    pinch_in_M = all(g in M for g in pinch)
    return dict(n=n, cts=cts, rep=o['rep'], order=o['order'], primitive=o['primitive'],
                contains_An=o['contains_An'], q=q, plain=len(reps),
                plain_matches_census=(len(reps) == o['plain_orbit_size']),
                marked_census=o['marked_orbit_size'], deck=deck_order,
                M_order=len(M), M_pair_orbits=n_pair_orbits,
                M_transitive=(len({g[0] for g in M}) == q),
                verdict_mismatch=mismatch, twists_in_M=twists_in_M, pinch_in_M=pinch_in_M,
                n_twist_perms=len(twists), n_pinch=len(pinch), stats=stats, pairs=plist,
                seconds=round(time.time() - t0c, 2))


def main():
    n = int(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else None
    assert workers <= 2
    jobs = []
    skipped = 0
    for cts, o in census_orbits(n):
        special = (not o['primitive']) or (not o['contains_An'])
        if cap and o['plain_orbit_size'] > cap and not (special and o['plain_orbit_size'] <= 20 * cap):
            skipped += 1
            continue
        jobs.append((n, cts, o))
    jobs.sort(key=lambda j: -j[2]['plain_orbit_size'])
    t0 = time.time()
    out = []
    with Pool(workers) as pool:
        for k, rec in enumerate(pool.imap_unordered(analyse, jobs, chunksize=1)):
            out.append(rec)
            if k % 500 == 0:
                print(n, k, len(jobs), round(time.time() - t0), flush=True)
    name = f'm_n{n}.json'
    save_out(name, dict(n=n, cap=cap, skipped=skipped, orbits=out))
    print('done', n, len(out), 'orbits, skipped', skipped, round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
