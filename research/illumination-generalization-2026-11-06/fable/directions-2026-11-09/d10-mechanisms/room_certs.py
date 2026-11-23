"""Static certificates of Theorem U for ONE given room and one pair of class-a lattice points.

No search.  The functions take a cell set, so the same code can be called on any room that
another direction produces.  Run as a script, it reports the 22-wall room.
"""
from roomtools import *
import unified_test as U


def rigid_congruence(t, y):
    """Finest block system whose quotient has identity monodromy at corner index y."""
    seeds = [(c[0], s) for c in cycles(t[y]) for s in c[1:]]
    return closure_partition(len(t[0]), t, seeds)


def room_report(cells, S, T, origin=(0, 0), decide=True, max_states=None):
    led = ledger(cells, origin)
    room, t = room_tuple(cells, origin)
    n = len(t[0])
    LS, LT = lifts(room, t, S, origin), lifts(room, t, T, origin)
    out = {'area': n, 'r': led['r'], 'W': led['W'], 'k': led['k'],
           'types': [cycle_type(g) for g in t]}
    # per-class finest parity congruences and their join
    sep = {}
    for name, cl in (('b', [1]), ('c', [2]), ('d', [3]), ('min', [1, 2, 3])):
        part = class_congruence(t, cl)
        img_S = {a_image(t, part, s[0])[0] for s in LS}
        img_T = {a_image(t, part, s[0])[0] for s in LT}
        sep[name] = (len(part), not (img_S & img_T))
    out['B_x: (blocks, separates)'] = sep
    out['second kind by Par'] = all(sep[x][1] for x in 'bcd') and not sep['min'][1]
    out['R_y blocks (finest rigid congruence at y)'] = {
        'bcd'[y - 1]: len(rigid_congruence(t, y)) for y in (1, 2, 3)}
    systems = d4.all_block_systems(list(t), n)
    out['block systems (blocks)'] = sorted(len(p) for p in systems)
    factors = [U.Factor(t, part) for part in systems]
    certs = []
    for s in LS:
        for q in LT:
            desc, _, perx, rel = U.analyse_pair(t, factors, s[0], q[0])
            certs.append((desc, {'abcd'[x]: sorted(v) for x, v in perx.items()}))
    out['certificates per lift pair'] = certs
    if decide:
        res, states, _ = decide_pairs(t, LS, LT, max_states=max_states)
        out['decider (i, j, lit)'] = res
        out['decider states'] = states
    return out


if __name__ == '__main__':
    R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
           (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
    cells = cells_from_vertices(R22)
    for k, v in room_report(cells, (0, 0), (2, 2)).items():
        print(k, ':', v)
    # the 12-wall cross: lit only through one class (theory.md, section 3.5)
    cross = cells_from_rows(['.##.', '####', '####', '.##.'], x0=0, y_top=3)
    print('12-wall cross, S = (1, 2), T = (3, 2), class origin (1, 0)')
    for k, v in room_report(cross, (1, 2), (3, 2), origin=(1, 0)).items():
        print(k, ':', v)
