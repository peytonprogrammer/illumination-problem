"""d52 step 3: enumerate all degree-delta W-set covers P -> K of each admissible K, and test each
P for a positive (same-class interior marks separated by B_y for all three y != a).

Model (memo section 3): over K minus its convex corners (and minus a slit from the cone to a
reflex vertex, if K has a cone) the cover is trivialised. It is then given by one involution
rho_A in S_delta per boundary arc A of K (arcs = maximal boundary chains between convex
corners; rho_A = id when A contains a reflex corner, since P has no interior zero) and, if K
has a cone, a fixed-point-free involution c (P is flat at interior points).
Constraint at each convex corner between arcs A, B: <rho_A, rho_B>-orbits are cvx, smooth,
rfx or int. Everything else is checked on the built P directly (local types, genus 0, r).
Usage: python3 -B enum_P.py K.json RMAX out.json [index list]
"""
import json
import resource
import sys
import time
from collections import Counter, deque
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fold import *  # noqa
from analyze_K import deltas  # noqa

resource.setrlimit(resource.RLIMIT_CPU, (3000, resource.getrlimit(resource.RLIMIT_CPU)[1]))
CLS_OF_GEN = {0: [(0, 0), (0, 1)], 1: [(1, 0), (1, 1)], 2: [(0, 0), (1, 0)], 3: [(0, 1), (1, 1)]}
P_TYPES = {'cvx', 'smooth', 'rfx', 'int'}


def K_structure(K):
    d = len(K[0])
    par = {}

    def find(s):
        while par[s] != s:
            par[s] = par[par[s]]
            s = par[s]
        return s
    for g in range(4):
        for u in range(d):
            if K[g][u] == u:
                par[(u, g)] = (u, g)
    corners, forced = [], set()
    orb_of = {}
    verts = {}
    for cls in CLASSES:
        a, b = cg(cls)
        for oi, (cells, kind, t) in enumerate(orbits(K, cls)):
            verts[(cls, oi)] = t
            for u in cells:
                orb_of[(cls, u)] = oi
            ends = [(u, g) for u in cells for g in (a, b) if K[g][u] == u]
            if t in ('smooth', 'rfx'):
                assert len(ends) == 2
                par[find(ends[0])] = find(ends[1])
                if t == 'rfx':
                    forced.add(ends[0])
            elif t == 'cvx':
                assert len(ends) == 2
                corners.append(tuple(ends))
            else:
                assert not ends
    arc_root = {s: find(s) for s in par}
    forced_roots = {arc_root[s] for s in forced}
    roots = sorted(set(arc_root.values()))
    free = [rt for rt in roots if rt not in forced_roots]
    gen_of_root = {rt: i for i, rt in enumerate(free)}
    corner_pairs = []
    for s1, s2 in corners:
        r1, r2 = arc_root[s1], arc_root[s2]
        assert r1 != r2
        if r1 in gen_of_root and r2 in gen_of_root:
            corner_pairs.append((gen_of_root[r1], gen_of_root[r2]))
    slot_gen = {s: gen_of_root.get(arc_root[s]) for s in par}   # None = identity
    # cone slit: BFS in the primal graph along interior edges from the cone to a reflex vertex
    slit = set()
    cones = [v for v, t in verts.items() if t == 'cone']
    if cones:
        start = cones[0]
        prev = {start: None}
        dq = deque([start])
        target = None
        while dq and target is None:
            v = dq.popleft()
            cls, oi = v
            a, b = cg(cls)
            for u in range(d):
                if orb_of[(cls, u)] != oi:
                    continue
                for g in (a, b):
                    w = K[g][u]
                    if w == u:
                        continue
                    other = [c2 for c2 in CLS_OF_GEN[g] if c2 != cls][0]
                    v2 = (other, orb_of[(other, u)])
                    if v2 not in prev:
                        prev[v2] = (v, frozenset([(u, g), (w, g)]))
                        if verts[v2] == 'rfx':
                            target = v2
                            break
                        if verts[v2] == 'int':
                            dq.append(v2)
                if target:
                    break
        assert target is not None
        v = target
        while prev[v] is not None:
            v, e = prev[v]
            slit |= e
    return dict(nfree=len(free), corner_pairs=corner_pairs, slot_gen=slot_gen, slit=slit,
                cone=bool(cones), narcs=len(roots), ncorners=len(corners))


def canon_perms(R):
    n = len(R[0])
    best = None
    for s in range(n):
        lab = {s: 0}
        order = [s]
        k = 0
        while k < len(order):
            u = order[k]
            k += 1
            for p in R:
                v = p[u]
                if v not in lab:
                    lab[v] = len(order)
                    order.append(v)
        form = tuple(tuple(lab[p[u]] for u in order) for p in R)
        if best is None or form < best:
            best = form
    return best


def build_P(K, st, R, C, delta):
    d = len(K[0])
    n = d * delta
    G = [[0] * n for _ in range(4)]
    for g in range(4):
        for u in range(d):
            v = K[g][u]
            if v == u:
                gi = st['slot_gen'][(u, g)]
                for k in range(delta):
                    G[g][u * delta + k] = u * delta + (k if gi is None else R[gi][k])
            elif (u, g) in st['slit']:
                for k in range(delta):
                    G[g][u * delta + k] = v * delta + C[k]
            else:
                for k in range(delta):
                    G[g][u * delta + k] = v * delta + k
    return G


def covers(K, z, delta, rmax, collect=None):
    st = K_structure(K)
    F = st['nfree']
    ngen = F + (1 if st['cone'] else 0)
    cidx = F if st['cone'] else None
    R = [[-1] * delta for _ in range(ngen)]
    rx_max = rmax - delta * z
    seen = set()
    out = []
    stats = Counter()

    def corners_ok(touched, gi):
        for (ga, gb) in st['corner_pairs']:
            if gi not in (ga, gb):
                continue
            for s in touched:
                cl, kind = trace(R, ga, gb, s)
                if not partial_ok(cl, kind, P_TYPES):
                    return False
        return True

    def rfx_extra():
        tot = 0
        for (ga, gb) in st['corner_pairs']:
            done = set()
            for s in range(delta):
                if s in done:
                    continue
                cl, kind = trace(R, ga, gb, s)
                done.update(cl)
                if kind == ('fixed', 'fixed') and len(cl) == 3:
                    tot += 1
        return tot

    def rec(ns, ptr):
        stats['nodes'] += 1
        while ptr < ngen * ns and R[ptr % ngen][ptr // ngen] != -1:
            ptr += 1
        if ptr == ngen * ns:
            if ns < delta:
                return
            key = canon_perms(R)
            if key in seen:
                return
            seen.add(key)
            stats['covers'] += 1
            C = R[cidx] if cidx is not None else None
            P = build_P(K, st, [R[i] for i in range(F)], C, delta)
            prof = profile(P)
            if prof is None or any('cone' in ts for ts in prof.values()):
                stats['bad_local'] += 1
                return
            s = summary(prof)
            if not s['genus0'] or not transitive(P):
                stats['not_disc'] += 1
                return
            if s['z'] > rmax:
                stats['r_too_big'] += 1
                return
            corner_cls = [c for c, ts in prof.items() if 'cvx' in ts or 'rfx' in ts]
            stats['rooms'] += 1
            if collect is not None:
                collect.add(canon(P))
            if len(corner_cls) < 3:
                stats['le2_classes'] += 1
                return
            stats['in_scope'] += 1
            pos, nb = positives(P)
            emb = is_room(P)
            stats['true_room'] += emb
            if pos:
                stats['positive'] += 1
                out.append(dict(R=[list(r) for r in R], r=s['z'], n=len(P[0]), embedded=emb, P=P,
                                blocks={'%d%d' % c: v for c, v in nb.items()},
                                pos=[[list(a), i, j] for a, i, j in pos]))
            return
        sh, gi = ptr // ngen, ptr % ngen
        if gi != cidx:
            R[gi][sh] = sh
            if corners_ok([sh], gi) and rfx_extra() <= rx_max:
                rec(ns, ptr + 1)
            R[gi][sh] = -1
        for s2 in range(sh + 1, ns):
            if R[gi][s2] == -1:
                R[gi][sh] = s2
                R[gi][s2] = sh
                if corners_ok([sh, s2], gi) and rfx_extra() <= rx_max:
                    rec(ns, ptr + 1)
                R[gi][sh] = -1
                R[gi][s2] = -1
        if ns < delta:
            R[gi][sh] = ns
            R[gi][ns] = sh
            if corners_ok([sh, ns], gi) and rfx_extra() <= rx_max:
                rec(ns + 1, ptr + 1)
            R[gi][sh] = -1
            R[gi][ns] = -1

    if ngen == 0:
        return out, stats, st
    rec(1, 0)
    return out, stats, st


def K_from_canon(cf):
    return [list(row) for row in cf]


if __name__ == '__main__':
    recs = json.load(open(sys.argv[1]))
    rmax = int(sys.argv[2])
    outp = sys.argv[3]
    sel = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else range(len(recs))
    t0 = time.process_time()
    allres = []
    tot = Counter()
    for i in sel:
        k = recs[i]
        K = K_from_canon(k['canon'])
        for dl in deltas(k, rmax):
            t1 = time.process_time()
            res, stats, st = covers(K, k['z'], dl, rmax)
            tot.update(stats)
            line = dict(K=i, d=k['d'], z=k['z'], cone=k['cone'], delta=dl, n=k['d'] * dl,
                        arcs=st['narcs'], free=st['nfree'], stats=dict(stats), positives=res,
                        cpu=round(time.process_time() - t1, 2))
            allres.append(line)
            print('K%d d=%d z=%d cone=%d delta=%d free arcs=%d: %s positives=%d cpu=%.2f' % (
                i, k['d'], k['z'], k['cone'], dl, st['nfree'], dict(stats), len(res), line['cpu']),
                flush=True)
    json.dump(allres, open(outp, 'w'))
    print('TOTAL', dict(tot), 'CPU s', round(time.process_time() - t0, 1))
