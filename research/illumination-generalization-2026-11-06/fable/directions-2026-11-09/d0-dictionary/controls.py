"""Negative controls for the conventions of dictionary.md.

Family: every fixed polyomino of area <= NMAX (default 6) and the 22-wall room.
Each control breaks one convention and counts what fails.

  signs     the three other sign choices for the matrices of s_0^2 and s_1^2
  faces     front lift = {NW, SE} instead of {NE, SW}
  inverses  the tuple (r_00, r_10, r_11, r_01), without inverses: is the product 1?
  one_arc   read position 1 only in every state: LIT pairs that are lost
  mixed     allow a walk to change corner inside one state: DARK pairs that turn "lit"

Usage: python3 -B controls.py [NMAX]   -> prints and writes controls.json
"""
import json
import sys
from collections import Counter

sys.dont_write_bytecode = True
import d0lib as L
import hurwitz as hz

EPS = (1, -1)
ORIGINS = ((0, 0), (1, 0), (1, 1), (0, 1))
V22 = [(0, 2), (0, 4), (1, 4), (1, 5), (2, 5), (2, 6), (4, 6), (4, 5), (5, 5), (5, 4), (6, 4), (6, 3),
       (4, 3), (4, 4), (2, 4), (2, 2), (3, 2), (3, 0), (2, 0), (2, 1), (1, 1), (1, 2)]

real_a_lifts = L.a_lifts


def swapped_a_lifts(cells, origin):
    out = {}
    for (p, f), c in real_a_lifts(cells, origin).items():
        x, y = p
        out[(p, f)] = c if f == 0 else ((x - 1, y) if f == 1 else (x, y))
    return out


def run(family, name):
    c = Counter()
    for cells in family:
        for o in ORIGINS:
            if len(real_a_lifts(cells, o)) < 2:
                continue
            c['instances'] += 1
            chk, bad, skip, res = L.state_check(cells, o, EPS)
            c['checks'] += chk
            c['mismatch_correct_conventions'] += bad
            for eps in ((1, 1), (-1, 1), (-1, -1)):
                _, bad2, _, _ = L.state_check(cells, o, eps)
                c[f'mismatch_signs_{eps[0]}_{eps[1]}'] += bad2
                c[f'instances_failing_signs_{eps[0]}_{eps[1]}'] += bad2 > 0
            L.a_lifts = swapped_a_lifts
            _, bad3, _, _ = L.state_check(cells, o, EPS)
            L.a_lifts = real_a_lifts
            c['mismatch_faces_swapped'] += bad3
            c['instances_failing_faces_swapped'] += bad3 > 0
            sheets, t = L.room_tuple(cells, o)
            noinv = (t[0], hz.inv(t[1]), t[2], hz.inv(t[3]))
            prod = hz.mul(hz.mul(hz.mul(noinv[0], noinv[1]), noinv[2]), noinv[3])
            c['product_not_1_without_inverses'] += prod != hz.ident(len(sheets))
            # one arc only, and walks that mix corners
            plen = res['plen']
            one, mixed = set(), set()

            def on_state(t_, pt_, word, M):
                for comp in hz.arc_components(t_[0], pt_, plen, t_[1]):
                    cl = sorted(comp)
                    one.update(frozenset((cl[x], cl[y])) for x in range(len(cl)) for y in range(x))
                parent = {}

                def find(u):
                    while parent.setdefault(u, u) != u:
                        parent[u] = parent[parent[u]]
                        u = parent[u]
                    return u

                for j in (1, 2, 3):
                    cid, lens = hz.cycle_index(t_[j])
                    for i in range(len(pt_)):
                        if pt_[i] >= 0 and lens[cid[i]] == 2:
                            parent[find(('a', pt_[i]))] = find((j, cid[i]))
                comp = {}
                for u in list(parent):
                    if u[0] == 'a':
                        comp.setdefault(find(u), []).append(u[1])
                for cl in comp.values():
                    mixed.update(frozenset((cl[x], cl[y])) for x in range(len(cl)) for y in range(x))

            L.tuple_orbit(t, EPS, on_state=on_state)
            lit = res['lit']
            assert one <= lit <= mixed
            q = sum(1 for x in plen if x == 2)
            c['pairs'] += q * (q - 1) // 2
            c['LIT'] += len(lit)
            c['LIT_lost_with_one_arc'] += len(lit - one)
            c['DARK_turned_lit_by_mixed_walks'] += len(mixed - lit)
    print(name, json.dumps(dict(c), indent=1), flush=True)
    return dict(c)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    polys = L.fixed_polyominoes(nmax)
    fam = [p for n in range(1, nmax + 1) for p in polys[n] if L.strictly_simple(p)]
    out = {f'fixed_polyominoes_area_le_{nmax}': run(fam, 'polyominoes'),
           'room22': run([L.cells_from_vertices(V22)], 'room22')}
    with open(L.HERE / 'controls.json', 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
