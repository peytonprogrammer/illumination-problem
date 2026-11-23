"""Task 5: structural facts behind the block systems.

1. 22-wall room, square framework: G versus (S3 wr A5) cap A15; kernel versus the sign-product subgroup.
2. Ramification of DP -> N for every proper block system of the 22-wall room (both frameworks):
   which points of DP ramify, their lattice coordinates, angles upstairs and downstairs.
3. Which blocks carry the S and T lifts.
4. Symmetry test: does an isometry of the tiling map the room to itself and swap S and T?
   Applied to the 22-wall room, the staircase, and the 11 imprimitive lit 45-degree rooms of task 3.

Run: python3 -B task5_structure.py   -> writes task5_structure.json (needs task3_lit_controls.json)
"""
import json
from fractions import Fraction as Fr
from pathlib import Path

from monodromy import (Room, analyse_room, all_block_systems, cycles, induced, is_even, schreier_sims, tris_of_squares)
from task1_room22 import P_SQ, P1_SQ, P2_SQ, S, T, a, b
from task3_lit_controls import tri_records

HERE = Path(__file__).resolve().parent
D4 = [((1, 0), (0, 1)), ((-1, 0), (0, -1)), ((0, -1), (1, 0)), ((0, 1), (-1, 0)),
      ((-1, 0), (0, 1)), ((1, 0), (0, -1)), ((0, 1), (1, 0)), ((0, -1), (-1, 0))]


def apply(L, p):
    return (L[0][0] * p[0] + L[0][1] * p[1], L[1][0] * p[0] + L[1][1] * p[1])


def swapping_symmetries(room):
    """Lattice isometries x -> Lx + t with t integer that preserve the tile set and swap the marks."""
    s, t = room.marks
    tiles = {frozenset(tl['verts']) for tl in room.tiles}
    out = []
    for L in D4:
        Ls = apply(L, s)
        tr = (t[0] - Ls[0], t[1] - Ls[1])
        Lt = apply(L, t)
        if (Lt[0] + tr[0], Lt[1] + tr[1]) != s:
            continue
        img = {frozenset((apply(L, p)[0] + tr[0], apply(L, p)[1] + tr[1]) for p in tl) for tl in tiles}
        if img == tiles:
            out.append(dict(linear=L, translation=tr))
    return out


def vertex_points(room):
    """Map (corner, frozenset(sheet cycle)) -> lattice vertex for every point of DP."""
    where = {}
    verts = {p for tl in room.tiles for p in tl['verts']}
    for p in verts:
        c, pts = room.points_at(p)
        for cy in pts:
            where[(c, frozenset(cy))] = p
    return where


def ramification(room, part):
    vp = vertex_points(room)
    ig = {c: induced(g, part) for c, g in room.gen.items()}
    out = []
    for c, g in room.gen.items():
        down = {}
        for z in cycles(ig[c]):
            for blk in z:
                down[blk] = len(z)
        bl = {x: k for k, B in enumerate(part) for x in B}
        for cy in cycles(g):
            L = down[bl[cy[0]]]
            e = len(cy) // L
            assert len(cy) % L == 0
            if e > 1:
                out.append(dict(vertex=list(vp[(c, frozenset(cy))]), corner=room.cname[c],
                                angle_DP=str(len(cy) * room.base_angle[c]), angle_N=str(L * room.base_angle[c]), e=e))
    return sorted(out, key=lambda d: d['vertex'])


def mark_blocks(room, part):
    bl = {x: k for k, B in enumerate(part) for x in B}
    res = {}
    for m in room.marks:
        c, pts = room.points_at(m)
        res[str(list(m))] = [sorted({bl[x] for x in cy}) for cy in pts]
    return res


def main():
    out = {}
    Q_SQ = sorted(P_SQ + P1_SQ + P2_SQ)
    Q = Room('room22', 'square', Q_SQ, [S, T])
    gens = Q.gens_list()
    order = schreier_sims(gens, Q.degree)[2]
    systems = all_block_systems(gens, Q.degree)
    part = next(p for p in systems if len(p[0]) == 3)
    kernel_gens = None
    wreath = 6 ** 5 * 60
    out['room22_square_group'] = dict(
        order=order, all_generators_even=all(is_even(g) for g in gens),
        order_S3_wr_A5=wreath, order_S3_wr_A5_cap_A15=wreath // 2,
        G_equals_S3_wr_A5_cap_A15=all(is_even(g) for g in gens) and order == wreath // 2,
        block_group_order=schreier_sims([induced(g, part) for g in gens], 5)[2],
        note='G <= G_B^B wr G^Sigma = S3 wr A5 (orders from task1); G <= A15 since all generators are even; '
             'equal orders then give G = (S3 wr A5) cap A15 and kernel = {(s_1..s_5) in S3^5 : prod sgn s_i = 1}.')
    out['room22_square_ramification_size3'] = ramification(Q, part)
    out['room22_square_mark_blocks_size3'] = mark_blocks(Q, part)
    Qt = Room('room22_tri', 'tri', tris_of_squares(Q_SQ), [S, T])
    out['room22_tri'] = []
    for p in all_block_systems(Qt.gens_list(), Qt.degree):
        if 1 < len(p[0]) < Qt.degree:
            out['room22_tri'].append(dict(block_size=len(p[0]), ramification=ramification(Qt, p),
                                          mark_blocks=mark_blocks(Qt, p)))
    out['symmetries_swapping_marks'] = {
        'room22_tri': swapping_symmetries(Qt),
        'staircase5_tri': swapping_symmetries(Room('st', 'tri', tris_of_squares(P_SQ), [a, b])),
    }
    # imprimitive lit rooms of task 3
    lit = json.loads((HERE / 'task3_lit_controls.json').read_text())
    names = {r['name'] for g, v in lit['groups'].items() if g in ('screen', 'global', 'learned')
             for r in v['rows'] if r['proper_block_sizes']}
    found = {}
    for src, name, tris, marks, path in tri_records():
        if name in names:
            room = Room(name, 'tri', [tuple(map(tuple, t)) for t in tris], marks)
            systems = all_block_systems(room.gens_list(), room.degree)
            ar = analyse_room(room)
            prop = [x for x in ar['block_systems'] if x['trivial'] == 'proper']
            found[name] = dict(swapping_symmetries=swapping_symmetries(room), order=ar['order'],
                               wreath_bound_over_order=[x['wreath_bound_order'] // ar['order'] for x in prop],
                               proper=[dict(block_size=len(p[0]), ramification=ramification(room, p),
                                            mark_blocks=mark_blocks(room, p))
                                       for p in systems if 1 < len(p[0]) < room.degree])
    assert set(found) == names
    out['imprimitive_lit_rooms'] = found
    (HERE / 'task5_structure.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'imprimitive_lit_rooms'}, indent=1, default=str))
    for k, v in found.items():
        print(k, 'wreath/|G|', v['wreath_bound_over_order'], 'swap symmetries', v['swapping_symmetries'], 'ramification sizes',
              [len(p['ramification']) for p in v['proper']])


if __name__ == '__main__':
    main()
