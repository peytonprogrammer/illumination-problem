"""Post-hoc test G6 (rigid factor) on every pair of every census orbit.

G6.  Let Pi be a block system other than the one-block system (Pi = singletons, N = Q, is
allowed), N = Q / Pi, and suppose the induced monodromy of N at some corner y in {b, c, d}
is the identity.  Then N -> B is a cover of the sphere minus {a, x, z} (the other two
corners), where every simple arc from a to x is isotopic.  So the lift pattern of every
arc a -> x in N is the pattern of the tail arc of the given basis.  Build the graph on
N-points over a and over x, with one edge per sheet s of Q whose Q-points over a and over
x are both regular (the only segments a light walk can use); the edge joins the N-points
of the block of s.  Over y, every point of N is one fixed block, so a walk through a
regular Q-point over y returns to the same N-point over a.  If sigma and tau map to
different components of the union of the graphs for x != y, the pair is DARK.

The script checks that G6 never predicts DARK for a LIT pair (soundness on the census),
and counts which DARK pairs it explains that G1 and G5 don't.

Run: python3 -B rigid_factor.py            (reads census_n*.json, writes rigid_factor.json)
"""
import json
from collections import Counter
from pathlib import Path

import d4_monodromy as d4
from hurwitz import cycles, cycle_index, initial_pt

HERE = Path(__file__).resolve().parent


def g6_dark(t, n, systems, P_sheet, Q_sheet):
    for part in systems:
        if len(part) == 1:
            continue
        ig = [d4.induced(g, part) for g in t]
        for y in (1, 2, 3):
            if any(ig[y][b] != b for b in range(len(part))):
                continue
            where = {s: b for b, blk in enumerate(part) for s in blk}
            ncid = [cycle_index(g)[0] for g in ig]
            qcid, qlen = zip(*[cycle_index(g) for g in t])
            parent = {}

            def find(u):
                while parent.setdefault(u, u) != u:
                    parent[u] = parent[parent[u]]
                    u = parent[u]
                return u

            for x in (1, 2, 3):
                if x == y:
                    continue
                for s in range(n):
                    if qlen[0][qcid[0][s]] == 2 and qlen[x][qcid[x][s]] == 2:
                        b = where[s]
                        ru, rv = find(('a', ncid[0][b])), find((x, ncid[x][b]))
                        if ru != rv:
                            parent[ru] = rv
            u = find(('a', ncid[0][where[P_sheet]]))
            v = find(('a', ncid[0][where[Q_sheet]]))
            if u != v:
                return [n // len(part), 'bcd'[y - 1]]
    return None


def main():
    out = {}
    for f in sorted(HERE.glob('census_n*.json'), key=lambda p: int(p.stem[8:])):
        d = json.loads(f.read_text())
        n = d['n']
        S = Counter()
        residual = []
        for cl in d['classes']:
            for o in cl['orbits']:
                if o['n_two_cycles_a'] < 2:
                    continue
                t = tuple(tuple(g) for g in o['rep'])
                systems = d4.all_block_systems(list(t), n)
                for p in o['pairs']:
                    w = g6_dark(t, n, systems, p['sheets_P'][0], p['sheets_Q'][0])
                    lit = p['lit']
                    if lit and w:
                        S['LIT predicted DARK by G6 (unsound)'] += 1
                    old = p['g1_predicted_dark'] or p['g5_predicted_dark']
                    if not lit:
                        S['DARK pairs'] += 1
                        S['DARK explained by parity factor'] += p['predicted_dark']
                        S['DARK explained by G1 or G5'] += old
                        S['DARK explained by G6'] += bool(w)
                        S['DARK explained by G6 only'] += bool(w) and not old
                        if not (old or w):
                            S['DARK unexplained by G1, G5, G6'] += 1
                            residual.append(dict(cts=cl['cts'], rep=o['rep'], P_sheets=p['sheets_P'],
                                                 Q_sheets=p['sheets_Q']))
        out[str(n)] = dict(counts=dict(S), residual=residual)
        print(n, dict(S))
    (HERE / 'rigid_factor.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
