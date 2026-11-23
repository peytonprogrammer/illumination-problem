"""Covers with blocks of size 2 over a non-pillowcase factor: where x-lit transitivity fails.

For every saved imprimitive orbit that has a block system with blocks of size 2 and a
non-pillowcase quotient N, the script prints the type of N, the map u from regular
a-points of Q to a-points of N, and the x-lit relation corner by corner in terms of u.
It reports each corner where x-lit is not transitive and classifies the failure.

Run: python3 -B blocks2.py 8 10
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


def comps(q, edges):
    par = list(range(q))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b in edges:
        par[find(a)] = find(b)
    return [find(x) for x in range(q)]


def main():
    for n in [int(a) for a in sys.argv[1:]]:
        mine = json.loads((D12 / f'mine_n{n}.json').read_text())['orbits']
        S = Counter()
        shown = Counter()
        for o in mine:
            if o['primitive']:
                continue
            t = tuple(tuple(g) for g in o['rep'])
            cid, plen = initial_pt(t[0])
            ids = sorted({c for c in cid if plen[c] == 2})
            q = len(ids)
            pos = {p: k for k, p in enumerate(ids)}
            sheets = [[i for i in range(n) if cid[i] == p] for p in ids]
            systems = [p for p in d4.all_block_systems(list(t), n) if 1 < len(p) < n]
            for part in systems:
                m = len(part)
                if n // m != 2:
                    continue
                ig = [d4.induced(g, part) for g in t]
                types = [sorted((len(c) for c in cycles(g)), reverse=True) for g in ig]
                pillow = all(max(ty) <= 2 for ty in types) and sum(ty.count(1) for ty in types) == 4
                if pillow:
                    continue
                identity = [all(x == 1 for x in types[y]) for y in (1, 2, 3)]
                where = [0] * n
                for b, blk in enumerate(part):
                    for s in blk:
                        where[s] = b
                acid = [0] * m
                alen = []
                for k, cy in enumerate(cycles(ig[0])):
                    alen.append(len(cy))
                    for b in cy:
                        acid[b] = k
                u = [acid[where[sheets[p][0]]] for p in range(q)]
                S['(orbit, size-2 block system, non-pillowcase N)'] += 1
                key = (o['order'], json.dumps(o['cts']), json.dumps(types))
                for xi in range(3):
                    edges = [(pos[p['P']], pos[p['Q']]) for p in o['pairs'] if p['lit_x'][xi]]
                    cc = comps(q, edges)
                    lit = {tuple(sorted(e)) for e in edges}
                    bad = [(i, j) for i in range(q) for j in range(i + 1, q)
                           if cc[i] == cc[j] and (i, j) not in lit]
                    if not bad:
                        S['corner relations, x-lit transitive'] += 1
                        continue
                    S['corner relations, x-lit NOT transitive'] += 1
                    kinds = Counter('same fibre of N' if u[i] == u[j] else 'different fibres' for i, j in bad)
                    S[('missing pairs', tuple(sorted(kinds.items())), 'N identity at b,c,d = %s' % identity)] += 1
                    if shown[key] < 1:
                        shown[key] += 1
                        print('  example |G|', o['order'], 'cts', o['cts'], 'plain', o['plain'])
                        print('    N types', types, 'a-point lengths of N', alen, 'u =', u, 'corner', 'bcd'[xi])
                        print('    x-lit pairs', sorted(lit), 'missing', bad)
                        print('    lit_x all corners', [(pos[p['P']], pos[p['Q']], p['lit_x']) for p in o['pairs']])
        print(n)
        for k, v in sorted(S.items(), key=str):
            print('   ', k, v)


if __name__ == '__main__':
    main()
