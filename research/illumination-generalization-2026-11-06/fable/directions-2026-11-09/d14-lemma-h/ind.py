"""Imprimitive covers: point monodromy on the fibres of a factor (task 4).

Reads cusp_nN.json (generators of M_t) and ../d12-lit-side/mine_nN.json (verdicts).
For every imprimitive orbit with q >= 2 and every proper nontrivial block system Pi
(N = Q / Pi), the script computes

  u(p)    : the a-point of N under the regular a-point p of Q;
  FH(Pi)  : "fibre homogeneity": the M_t-orbits on unordered pairs of regular a-points are
            exactly the classes predicted by N, i.e. two pairs lie in one M_t-orbit iff
            their images {u, u'} (or their common image u) lie in one orbit of the group
            induced by M_t on the a-points of N;
  uniform : the LIT/DARK verdict is constant on each predicted class.

Run: python3 -B ind.py 6 7 8 9 10   -> ind_summary.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
D12 = HERE.parent / 'd12-lit-side'
sys.path.insert(0, str(D6))
import d4_monodromy as d4                      # noqa: E402
from hurwitz import cycles, initial_pt         # noqa: E402
from cusp import closure                       # noqa: E402


def analyse(o, verdict):
    n = o['n']
    t = tuple(tuple(g) for g in o['rep'])
    cid, plen = initial_pt(t[0])
    ids = sorted({c for c in cid if plen[c] == 2})
    q = len(ids)
    sheets = [[i for i in range(n) if cid[i] == p] for p in ids]
    M = closure([tuple(g) for g in o['gensM']], q)
    pairs = [(i, j) for i in range(q) for j in range(i + 1, q)]
    # M-orbits on pairs
    orb = {}
    for pr in pairs:
        orb[pr] = min(tuple(sorted((g[pr[0]], g[pr[1]]))) for g in M)
    lit = {(i, j): verdict[(ids[i], ids[j])] for (i, j) in pairs}
    systems = [p for p in d4.all_block_systems(list(t), n) if 1 < len(p) < n]
    blocks0 = [frozenset(next(b for b in p if 0 in b)) for p in systems]
    out = []
    any_identity = False
    any_pillow = False
    recs = []
    for part, b0 in zip(systems, blocks0):
        m = len(part)
        where = [0] * n
        for b, blk in enumerate(part):
            for s in blk:
                where[s] = b
        ig = [d4.induced(g, part) for g in t]
        types = [sorted((len(c) for c in cycles(g)), reverse=True) for g in ig]
        identity_corner = any(all(x == 1 for x in types[y]) for y in (1, 2, 3))
        pillow = all(max(ty) <= 2 for ty in types) and sum(ty.count(1) for ty in types) == 4
        any_identity = any_identity or identity_corner
        any_pillow = any_pillow or (pillow and m > 1)
        acid = [0] * m
        alen = []
        for k, cy in enumerate(cycles(ig[0])):
            alen.append(len(cy))
            for b in cy:
                acid[b] = k
        u = [acid[where[sheets[p][0]]] for p in range(q)]
        assert all(acid[where[sheets[p][1]]] == u[p] for p in range(q))
        # M_Pi: the elements of M_t that preserve the fibres over N (the return conjugation
        # of a loop can move one block system to another, so M_Pi can be a proper subgroup)
        def preserves(g):
            im = {}
            return all(im.setdefault(u[p], u[g[p]]) == u[g[p]] for p in range(q))
        MP = [g for g in M if preserves(g)]
        orbP = {pr: min(tuple(sorted((g[pr[0]], g[pr[1]]))) for g in MP) for pr in pairs}
        def key(pr):
            i, j = pr
            if u[i] == u[j]:
                return ('F', min(u[g[i]] for g in MP))
            return ('S', min(tuple(sorted((u[g[i]], u[g[j]]))) for g in MP))
        classes = {}
        for pr in pairs:
            classes.setdefault(key(pr), []).append(pr)
        fh = all(len({orbP[pr] for pr in cl}) == 1 for cl in classes.values())
        uniform = all(len({lit[pr] for pr in cl}) == 1 for cl in classes.values())
        maximal = not any(b1 < b0 for b1 in blocks0)
        cls = []
        for k, cl in sorted(classes.items()):
            reg = sorted({alen[u[i]] for pr in cl for i in pr})
            cls.append(dict(kind=k[0], pairs=len(cl), M_orbits=len({orbP[pr] for pr in cl}),
                            lit=sum(lit[pr] for pr in cl), n_point_lengths=reg))
        recs.append(dict(block_size=n // m, degree_N=m, types_N=types, maximal=maximal,
                         index_M_Pi=len(M) // len(MP),
                         identity_corner=identity_corner, pillowcase=pillow, FH=fh,
                         uniform=uniform, classes=cls))
    return dict(n=n, cts=o['cts'], order=o['order'], q=q, deck_order=o['deck_order'],
                Q_identity=any(len(c) == n for c in o['cts'][1:]),
                plain=o['plain'], M_order=len(M), any_identity=any_identity,
                any_pillow=any_pillow, factors=recs)


def main():
    res = []
    for n in [int(a) for a in sys.argv[1:]]:
        cus = json.loads((HERE / f'cusp_n{n}.json').read_text())['orbits']
        mine = json.loads((D12 / f'mine_n{n}.json').read_text())['orbits']
        ver = {json.dumps(o['rep']): {(p['P'], p['Q']): bool(p['lit']) for p in o['pairs']} for o in mine}
        S = Counter()
        for o in cus:
            if o['primitive']:
                continue
            r = analyse(o, ver[json.dumps(o['rep'])])
            res.append(r)
            S['imprimitive orbits'] += 1
            mx = [f for f in r['factors'] if f['maximal']]
            S['(orbit, maximal factor) incidences'] += len(mx)
            for f in mx:
                rigid = r['any_identity'] or r['Q_identity']
                tag = ('rigid factor' if rigid else 'no rigid factor') + (', pillowcase factor' if r['any_pillow'] else '') + (', deck' if r['deck_order'] > 1 else '')
                S[('FH holds' if f['FH'] else 'FH fails', tag)] += 1
                S[('verdict uniform on N-classes' if f['uniform'] else 'verdict NOT uniform on N-classes', tag)] += 1
                for c in f['classes']:
                    if c['kind'] == 'S':
                        S[('S-classes', 'all LIT' if c['lit'] == c['pairs'] else 'all DARK' if c['lit'] == 0 else 'mixed')] += 1
                    else:
                        S[('F-classes', 'all LIT' if c['lit'] == c['pairs'] else 'all DARK' if c['lit'] == 0 else 'mixed')] += 1
            S['orbits: FH holds for every maximal factor'] += all(f['FH'] for f in mx)
            S['orbits: FH holds for every factor'] += all(f['FH'] for f in r['factors'])
        print(n)
        for k, v in sorted(S.items(), key=str):
            print('   ', k, v)
    (HERE / 'ind_summary.json').write_text(json.dumps(res, separators=(',', ':')) + '\n')


if __name__ == '__main__':
    main()
