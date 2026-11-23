"""d121: does every P1/P2 braid family at z >= 2 have a node lit on room 0?

Reuses d22.small() unchanged: same covers (d22.brute), same rooms (SMALL[z][0]),
same tracer call (X.visible(a, 8)). The only addition is grouping the saved node
set into braid-orbit families, so that a verdict on rooms 1 and 2 is never needed.
No new rooms, directions, or tracer depths.
"""
import sys, json, itertools
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'replay' / 'd22-structured'))
import d22
hz, bp = d22.hz, d22.bp


def key(t, d, node):
    enc, labs = bp.canon(t, d)
    return enc, min(tuple(sorted((p, frozenset((lab[a], lab[b])) and tuple(sorted((lab[a], lab[b])))) for p, a, b in node))
                    for lab in labs)


def move(t, node, i):
    k = hz.inv(t[i])
    t2 = list(t); t2[i], t2[i + 1] = hz.conj_by(t[i + 1], k), t[i]
    out = []
    for p, a, b in node:
        if p == i + 1: p, a, b = i, k[a], k[b]
        elif p == i: p = i + 1
        assert (a, b) in {(c[0], c[1]) for c in hz.cycles(t2[p]) if len(c) == 2} or \
               (b, a) in {(c[0], c[1]) for c in hz.cycles(t2[p]) if len(c) == 2}
        out.append((p, a, b))
    return tuple(t2), out


rows = []
for z, d in ((2, 2), (2, 3), (2, 4), (3, 2), (4, 2)):
    R0, y0 = d22.Room(d22.SMALL[z][0][0]), d22.SMALL[z][0][1]
    covers = d22.brute(z + 4, d, 8 - d * z)
    for kind in ('P1', 'P2'):
        lit, par = {}, {}
        def find(u):
            while par[u] != u: par[u] = par[par[u]]; u = par[u]
            return u
        todo = []
        for h in covers.values():
            nodes = d22.nodes_of(h, d)[0 if kind == 'P1' else 1]
            if not nodes: continue
            X = d22.Cx(R0, h); vis = {}
            for nd in nodes:
                a, b = X.vpole(nd[0][0], nd[0][1]), X.vpole(nd[1][0], nd[1][1])
                if a not in vis: vis[a] = X.visible(a, 8)
                u = key(h, d, nd); par.setdefault(u, u)
                lit[u] = lit.get(u, False) or (b in vis[a])
                todo.append((h, list(nd)))
        for h, nd in todo:
            u = key(h, d, nd)
            for i in range(z + 3):
                t2, nd2 = move(h, nd, i)
                v = key(t2, d, nd2)
                assert v in par, 'braid image not in enumerated node set'
                par[find(u)] = find(v)
        fams = {}
        for u in par: fams.setdefault(find(u), []).append(lit[u])
        rows.append(dict(z=z, delta=d, kind=kind, node_classes=len(par), families=len(fams),
                         families_without_room0_lit_node=sum(1 for v in fams.values() if not any(v)),
                         family_sizes=sorted(len(v) for v in fams.values())))
        print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open(HERE / 'family_check_small.json', 'w'), indent=1)
