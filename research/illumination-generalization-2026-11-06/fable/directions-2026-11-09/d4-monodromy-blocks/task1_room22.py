"""Task 1: monodromy and block systems of the 22-wall room (manuscript construction).

Run: python3 -B task1_room22.py   -> writes task1_room22.json
"""
import json
from fractions import Fraction as Fr
from pathlib import Path

from monodromy import (Room, analyse_room, all_block_systems, induced, cycles, schreier_sims,
                       squares_from_polygon, tris_of_squares, mul, inv, ident)

HERE = Path(__file__).resolve().parent

# Manuscript eq. (squares), (copies), (vertices).
P_SQ = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)]
P1_SQ = [(x, -y - 1) for x, y in P_SQ]             # (x,y) -> (x,-y)
P2_SQ = [(4 - x - 1, -y - 1) for x, y in P_SQ]     # (x,y) -> (4-x,-y)
Q_VERTS = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3), (2, -3), (2, -1), (1, -1), (1, 1), (3, 1), (3, 0), (5, 0),
           (5, 1), (4, 1), (4, 2), (3, 2), (3, 3), (1, 3), (1, 2), (0, 2), (0, 1), (-1, 1)]
S, T = (0, 0), (2, 2)
a, b = (0, 0), (2, -2)


def fold_square(sq):
    """Square of Q -> (square of P, orientation reversing?)."""
    if sq in P_SQ:
        return sq, False
    if sq in P1_SQ:
        x, y = sq
        return (x, -y - 1), True
    x, y = sq
    return (4 - x - 1, -y - 1), False   # (x,y)->(4-x,-y) is a half-turn: orientation preserving


def main():
    Q_SQ = sorted(P_SQ + P1_SQ + P2_SQ)
    assert len(set(Q_SQ)) == 15
    assert sorted(squares_from_polygon(Q_VERTS)) == Q_SQ, 'vertex cycle and union description disagree'
    Q = Room('room22', 'square', Q_SQ, [S, T])
    P = Room('staircase5', 'square', P_SQ, [a, b])
    led = Q.ledger()
    assert led['walls'] == 22 and len(led['reflex']) == 9 and led['area'] == 15
    assert sorted(led['transparent_nonA']) == sorted([(-1, 0), (1, 0), (2, 1), (2, 3)])
    assert set(led['interior_lattice']) == {S, T}
    out = {'room22_square': analyse_room(Q), 'staircase5_square': analyse_room(P)}

    # The fold f: DQ -> DP as a map on sheets; its fibres must be one of the block systems.
    pidx = {t['key']: k for k, t in enumerate(P.tiles)}
    fib = {}
    for j, f in enumerate(Q.sheets):
        k, cp = Q.faces[f]
        sq, rev = fold_square(Q.tiles[k]['key'])
        pf = P.fid[(pidx[sq], cp ^ int(rev))]
        assert P.topface[pf], 'fold does not preserve the top face'
        fib.setdefault(P.sheet_index[pf], []).append(j)
    fold_part = [sorted(fib[i]) for i in range(P.degree)]
    systems = all_block_systems(Q.gens_list(), Q.degree)
    canon = [sorted(map(sorted, s)) for s in systems]
    assert sorted(map(sorted, fold_part)) in canon
    # N for the fold system equals D(staircase) generator by generator under the fold.
    same = all(induced(Q.gen[c], fold_part) == P.gen[c] for c in Q.gen)
    out['fold_check'] = dict(fold_fibres_are_a_block_system=True, fold_block_size=len(fold_part[0]),
                             induced_generators_equal_staircase_generators=same,
                             fold_partition=fold_part)
    # Mark points of DQ, with copy and cone angle (units of pi)
    out['mark_points_DQ'] = {}
    for m in (S, T):
        c, pts = Q.points_at(m)
        out['mark_points_DQ'][str(m)] = [dict(sheets=list(cy), angle=len(cy)) for cy in pts]
    # Triangle (canonical45) framework for the same room, for comparison with the 45-degree rooms.
    Qt = Room('room22_tri', 'tri', tris_of_squares(Q_SQ), [S, T])
    Pt = Room('staircase5_tri', 'tri', tris_of_squares(P_SQ), [a, b])
    out['room22_tri'] = analyse_room(Qt)
    out['staircase5_tri'] = analyse_room(Pt)
    (HERE / 'task1_room22.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
    for key in ('room22_square', 'staircase5_square', 'room22_tri', 'staircase5_tri'):
        r = out[key]
        print(key, 'deg', r['degree'], '|G|', r['order'], 'sym', r['is_symmetric'], 'alt', r['is_alternating'],
              'primitive', r['primitive'], 'gens', r['generator_cycle_types'], 'ledger', r['ledger'])
        for bs in r['block_systems']:
            print('   ', {k: v for k, v in bs.items() if k != 'partition'})
    print('fold', {k: v for k, v in out['fold_check'].items() if k != 'fold_partition'})


if __name__ == '__main__':
    main()
