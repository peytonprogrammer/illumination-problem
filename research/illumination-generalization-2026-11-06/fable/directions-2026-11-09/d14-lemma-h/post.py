"""Post-processing of cusp_nN.json: tests of the intermediate claims of the Lemma H plan.

For every saved orbit with q >= 2 the script rebuilds M_t and the normal closure Nbar of
the cusp elements in M_t, and tests each claim on three nested families:
  ALL   every saved orbit,
  PRIM  the PRIM hypotheses (G primitive, no identity corner among b, c, d, some 2-cycle
        at b, c or d),
  AN    PRIM and G contains A_n.
It prints the count of orbits that satisfy each claim and the first failure (smallest n,
then smallest plain orbit).

Run: python3 -B post.py 4 5 6 7 8 9 10   -> post_summary.json
"""
import json
import sys
from collections import Counter
from math import factorial
from pathlib import Path

from cusp import closure, orbit_counts

HERE = Path(__file__).resolve().parent


def mul(a, b):
    """apply a, then b"""
    return tuple(b[i] for i in a)


def inv(a):
    r = [0] * len(a)
    for i, x in enumerate(a):
        r[x] = i
    return tuple(r)


def normal_closure(gensN, M, q):
    conj = {mul(mul(inv(m), g), m) for g in gensN for m in M}
    return closure(conj, q)


def moved(g):
    return sum(1 for i, x in enumerate(g) if x != i)


def is_primitive(group, q):
    """transitive and no nontrivial block (q <= 5 here, brute force over pair-generated blocks)"""
    if orbit_counts(group, q)[0] != 1:
        return False
    for j in range(1, q):
        par = list(range(q))

        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x
        par[find(j)] = find(0)
        changed = True
        while changed:
            changed = False
            for g in group:
                for a in range(q):
                    for b in range(a + 1, q):
                        if find(a) == find(b) and find(g[a]) != find(g[b]):
                            par[find(g[a])] = find(g[b])
                            changed = True
        if len({find(x) for x in range(q)}) > 1:
            return False
    return True


def transposition_graph_connected(group, q):
    par = list(range(q))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for g in group:
        if moved(g) == 2:
            a, b = [i for i in range(q) if g[i] != i]
            par[find(a)] = find(b)
    return len({find(x) for x in range(q)}) == 1


CLAIMS = [
    ('C1 some cusp element is nontrivial (Nbar != 1)', lambda r: r['Nbar'] > 1),
    ('C2 a single cusp loop is a transposition or a 3-cycle', lambda r: r['single']),
    ('C3 Nbar contains a transposition or a 3-cycle', lambda r: r['Nbar_small']),
    ('C4 M_t contains a transposition or a 3-cycle (q >= 3)', lambda r: r['M_small'] or r['q'] < 3),
    ('C5 M_t is transitive', lambda r: r['M_orb'][0] == 1),
    ('C6 M_t is primitive', lambda r: r['M_prim']),
    ('C7 M_t is 2-homogeneous (Lemma H)', lambda r: r['M_orb'][1] == 1),
    ('C8 M_t = S_q', lambda r: r['M'] == factorial(r['q'])),
    ('C9 Nbar is transitive', lambda r: r['Nbar_orb'][0] == 1),
    ('C10 Nbar is 2-homogeneous', lambda r: r['Nbar_orb'][1] == 1),
    ('C11 Nbar = M_t', lambda r: r['Nbar'] == r['M']),
    ('C12 the transpositions of Nbar connect all points (then M_t = S_q)', lambda r: r['tgraph']),
    ('E1 some state has a link', lambda r: r['link_any'] > 0),
    ('E2 the base state has a link', lambda r: r['base_link']),
    ('E3 every state has a link', lambda r: r['link_any'] == r['plain']),
]


def main():
    out = {}
    for n in [int(a) for a in sys.argv[1:]]:
        recs = []
        for o in json.loads((HERE / f'cusp_n{n}.json').read_text())['orbits']:
            q = o['q']
            cts = o['cts']
            M = closure([tuple(g) for g in o['gensM']], q)
            gN = [tuple(g) for gs in o['gensN'] for g in gs]
            Nb = normal_closure(gN, M, q) if gN else {tuple(range(q))}
            assert Nb <= M
            hyp = all(len(c) < n for c in cts[1:]) and any(2 in c for c in cts[1:])
            fam = ['ALL']
            if o['primitive'] and hyp:
                fam.append('PRIM')
                if o['contains_An']:
                    fam.append('AN')
            recs.append(dict(
                n=n, cts=cts, plain=o['plain'], order=o['order'], q=q, fam=fam,
                genus=o['hurwitz_genus'], deck=o['deck_order'],
                M=len(M), M_orb=orbit_counts(M, q), M_prim=is_primitive(M, q),
                M_small=any(moved(g) in (2, 3) for g in M),
                Nbar=len(Nb), Nbar_orb=orbit_counts(Nb, q),
                Nbar_small=any(moved(g) in (2, 3) for g in Nb),
                single=o['single_cusp_transposition'] or o['single_cusp_3cycle'],
                tgraph=transposition_graph_connected(Nb, q),
                link_any=o['link_states'][3], base_link=any(o['base_link'])))
        recs.sort(key=lambda r: r['plain'])
        out[n] = recs
        print(f'n = {n}')
        for fam in ('AN', 'PRIM', 'ALL'):
            rs = [r for r in recs if fam in r['fam']]
            print(f'  family {fam}: {len(rs)} orbits; q distribution',
                  dict(sorted(Counter(r["q"] for r in rs).items())))
            for name, f in CLAIMS:
                bad = [r for r in rs if not f(r)]
                line = f'    {name}: {len(rs) - len(bad)} of {len(rs)}'
                if bad:
                    b = bad[0]
                    line += (f'; first failure cts {b["cts"]} plain {b["plain"]} |G| {b["order"]}'
                             f' q {b["q"]} |M| {b["M"]} |Nbar| {b["Nbar"]} genus {b["genus"]}')
                print(line)
            g0 = [r for r in rs if r['genus'] == 0 and r['deck'] == 1]
            print(f'    Hurwitz genus 0 and no deck map: {len(g0)} orbits; Nbar = M_t in',
                  sum(r['Nbar'] == r['M'] for r in g0))
            ct = [r for r in rs if r['Nbar'] == 1]
            print(f'    cusp-trivial orbits (Nbar = 1): {len(ct)}; genus',
                  sorted(Counter(r['genus'] for r in ct).items()),
                  '; (q, |M|)', sorted(Counter((r['q'], r['M']) for r in ct).items()))
            if rs:
                fr = [r['link_any'] / r['plain'] for r in rs]
                print(f'    share of states with a link: min {min(fr):.3f}, mean {sum(fr) / len(fr):.3f}')
    (HERE / 'post_summary.json').write_text(json.dumps(out, separators=(',', ':')) + '\n')


if __name__ == '__main__':
    main()
