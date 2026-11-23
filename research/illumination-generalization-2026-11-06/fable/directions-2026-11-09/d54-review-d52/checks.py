"""d54 referee checks on every disc cover produced by d52's arc model at r <= 8.

For each cover P (genus 0, transitive, r <= 8) of each admissible K and delta:
  A. B_y (closure under all of W, d52) equals the closure under the rotations g_x only
     (d10's definition), as partitions, for all four classes.
  B. An independent separation test (own code: W+ congruence, lifts as g_a 2-cycles, images as
     g_a-orbits of blocks) agrees with fold.positives on every in-scope P.
  C. For every in-scope P and every class y with delta_y >= 3 and d_y >= 2: K_y (normalised to
     y = (0,0)) is in d52's full genus-0 list K_z2_d12 (127 shapes), and its admissibility
     verdict is recorded. Also d36.4 (d <= 4z+1, 4z if even), delta*z <= r, and the F* fibre
     count sum_c floor(rho_c / delta) >= z are checked on the actual room.
  D. F* passes(rho, n, r) (d44 filter_rate.py, re-typed) for in-scope P with 5 <= r <= 8 and
     21 <= n <= 5r that have some delta >= 3 class with d >= 2; and the set of areas seen.
Usage: python3 -B checks.py
"""
import json
import resource
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fold import *  # noqa
import enum_P  # noqa
from analyze_K import deltas, admissible  # noqa

resource.setrlimit(resource.RLIMIT_CPU, (600, resource.getrlimit(resource.RLIMIT_CPU)[1]))


# ---- independent code (no fold.congruence / separation_table / positives) ----
def rot(G, cls):
    i, j = cls
    return [G[i][G[2 + j][u]] for u in range(len(G[0]))]


def uf_blocks(n, gens, pairs):
    par = list(range(n))

    def f(x):
        while par[x] != x:
            x = par[x]
        return x
    todo = list(pairs)
    while todo:
        u, v = todo.pop()
        a, b = f(u), f(v)
        if a == b:
            continue
        par[a] = b
        for g in gens:
            todo.append((g[u], g[v]))
    return [f(u) for u in range(n)]


def cycles(perm):
    seen, out = set(), []
    for s in range(len(perm)):
        if s in seen:
            continue
        c = [s]
        seen.add(s)
        u = perm[s]
        while u != s:
            c.append(u)
            seen.add(u)
            u = perm[u]
        out.append(c)
    return out


def indep_positive(G):
    n = len(G[0])
    gs = {c: rot(G, c) for c in CLASSES}
    gens = list(gs.values())
    blocks = {}
    for y in CLASSES:
        pairs = [(c[0], c[1]) for c in cycles(gs[y]) if len(c) == 2]
        blocks[y] = uf_blocks(n, gens, pairs)
    found = []
    for a in CLASSES:
        two = [c for c in cycles(gs[a]) if len(c) == 2]
        # interior point = two 2-cycles of g_a exchanged by the reflections around it
        i, j = a
        pts = []
        used = set()
        for c in two:
            if c[0] in used:
                continue
            o = G[i][c[0]]
            if o in c:      # smooth wall point: reflection maps the 2-cycle to itself
                continue
            other = [cc for cc in two if o in cc][0]
            used.update(c)
            used.update(other)
            pts.append((c[0], other[0]))
        for s in range(len(pts)):
            for t in range(s + 1, len(pts)):
                ok = True
                for y in CLASSES:
                    if y == a:
                        continue
                    bl = blocks[y]
                    ga = gs[a]
                    # image of lift through cell u in N_y = g_a-orbit of block(u)
                    bmap = {}
                    for u in range(n):
                        bmap[bl[u]] = bl[ga[u]]

                    def orb(b0):
                        o, b = {b0}, bmap[b0]
                        while b not in o:
                            o.add(b)
                            b = bmap[b]
                        return frozenset(o)
                    S = {orb(bl[u]) for u in pts[s]}
                    T = {orb(bl[u]) for u in pts[t]}
                    if S & T:
                        ok = False
                        break
                if ok:
                    found.append((a, s, t))
    return found


def same_partition(p, q):
    m = {}
    for a, b in zip(p, q):
        if m.setdefault(a, b) != b:
            return False
    return len(set(p)) == len(set(q))


# ---- F* (d44 filter_rate.py lines 12-30, re-typed) ----
def fcases(n, r):
    out = []
    for d in range(3, n + 1):
        if n % d:
            continue
        delta = n // d
        if delta < 3:
            continue
        zmin = max(1, (d + 2) // 4 if d % 2 else (d + 3) // 4)
        if zmin <= r // delta:
            out.append((delta, d, zmin))
    return out


def fpasses(rho, n, r):
    return any(sum(x // dl for x in rho) >= zmin for dl, d, zmin in fcases(n, r))


def normalise(G, x):
    i, j = x
    return [G[i], G[1 - i], G[2 + j], G[3 - j]]


if __name__ == '__main__':
    t0 = time.process_time()
    adm = json.load(open(HERE / 'data/K_adm_r8.json'))
    full = json.load(open(HERE / 'data/K_z2_d12.json'))
    full_idx = {tuple(tuple(r) for r in k['canon']): k for k in full}
    adm_set = {tuple(tuple(r) for r in k['canon']) for k in adm}
    rooms = {}
    for i, k in enumerate(adm):
        K = [list(r) for r in k['canon']]
        for dl in deltas(k, 8):
            coll = set()
            enum_P.covers(K, k['z'], dl, 8, collect=coll)
            for c in coll:
                rooms.setdefault(c, []).append((i, dl))
    print('distinct disc covers (canonical W-sets) over all cases:', len(rooms), flush=True)
    st = Counter()
    areas = defaultdict(set)
    kverdict = Counter()
    for c, src in rooms.items():
        P = [list(r) for r in c]
        n = len(P[0])
        prof = profile(P)
        s = summary(prof)
        r = s['z']
        ncls = len([cl for cl, ts in prof.items() if 'cvx' in ts or 'rfx' in ts])
        # A
        for y in CLASSES:
            if not same_partition(B(P, y), congruence_G(P, two_cycle_pairs(P, y))):
                st['A_mismatch'] += 1
        if ncls < 3:
            st['out_of_scope'] += 1
            continue
        st['in_scope'] += 1
        # B
        p1 = sorted(positives(P)[0])
        p2 = sorted(indep_positive(P))
        st['B_agree' if len(p1) == len(p2) else 'B_MISMATCH'] += 1
        st['positives'] += len(p2)
        # C
        rho = Counter()
        for cl, ts in prof.items():
            rho[cl] = ts.count('rfx')
        rhov = [rho[cl] for cl in CLASSES]
        has_big = False
        for y in CLASSES:
            blk = B(P, y)
            d = max(blk) + 1
            dl = n // d
            if dl < 3 or d < 2:
                continue
            has_big = True
            Pn = normalise(P, y)
            K = quotient(Pn, B(Pn, (0, 0)))
            kc = canon(K)
            ks = summary(profile(K))
            z = ks['z']
            if kc not in full_idx:
                st['C_K_NOT_IN_127'] += 1
                print('  K_y missing from enumerated list: n=%d r=%d y=%s d=%d z=%d' % (n, r, y, d, z))
                continue
            st['C_K_in_127'] += 1
            if kc in adm_set:
                kverdict['admissible'] += 1
            else:
                kverdict[tuple(admissible(full_idx[kc], 8))] += 1
            bound = 4 * z + 1 if d % 2 else 4 * z
            st['C_d36.4_ok' if d <= bound else 'C_d36.4_FAIL'] += 1
            st['C_dz_ok' if dl * z <= r else 'C_dz_FAIL'] += 1
            st['C_fibre_ok' if sum(x // dl for x in rhov) >= z else 'C_fibre_FAIL'] += 1
        # D
        if has_big and 5 <= r <= 8 and 21 <= n:
            areas[r].add(n)
            st['D_pass' if (n <= 5 * r and fpasses(rhov, n, r)) else 'D_FSTAR_REJECTS'] += 1
        if 5 <= r <= 8 and n >= 21:
            areas[('any', r)].add(n)
    print(dict(st))
    print('admissibility of K_y for delta>=3, d>=2 classes of in-scope covers:', dict(kverdict))
    for key in sorted(areas, key=str):
        print('areas', key, sorted(areas[key]))
    print('CPU s %.1f' % (time.process_time() - t0))
