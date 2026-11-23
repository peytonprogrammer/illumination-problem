"""d66: pair-level test on named rooms and on the saved d64 room list (reading only).

For every room: n, r, W, normalization (edge gcds), and the type of each canonical factor
N_x = DP / B_x for the four absolute classes x: 'B' (one block), 'Q' (discrete), or its degree.
R* = normalized rooms in which every class has type B or Q (the residual case after d64).

For every corner class a and every pair S != T of interior lattice points of class a, and every
lift pair (S~, T~), the exact pure-braid orbit verdict (d63 realize walk, d61 dp_joined) is
taken at every target x != a whose B_x is not discrete (discrete B_x: no regular x-point, so
x-dark by R3 with Par). Reported:
  pair      lit when some lift pair is x-lit for some x (the room verdict);
  per-x     room pair x-dark: all four lift pairs x-dark (RL-room per target);
  per-row   lift pair x-dark at an N_x = B target (RL-B per lift pair);
  rigRy     Rig(x) over DP / R_y for y outside {a, x} (d62 G3), on dark rows;
  delta     dark rows that are delta-pairs for a deck involution, with the classes of the
            delta-fixed points (Lemma M), and whether the pair is lit at that class (relay).
Usage: python3 -B pair_level.py [max_states]      (writes pair_level.json, prints the log)
"""
import json
import resource
import sys
import time
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd64-finite-case'))
sys.path.insert(0, str(D / 'd65-nx-equals-b'))
import rl_test  # noqa: E402  (path setup; sets RLIMIT_CPU 4000)
from rl_test import R_y, orbit_lit_capped  # noqa: E402
from realize import U, cycles, room_tuple, lattice_points, rooms as named_rooms  # noqa: E402
from roomtools import class_congruence, status  # noqa: E402
from rl_room import centraliser  # noqa: E402
import notch12 as NZ  # noqa: E402

resource.setrlimit(resource.RLIMIT_CPU, (560, 560))
LAB = {1: (1, 0), 2: (1, 1), 3: (0, 1)}          # b, c, d relative to a (roomtools)


def edge_gcds(cells):
    """d64 covers.edge_gcds, copied: gcd of maximal horizontal and vertical wall runs."""
    cs = set(cells)
    hx, vy = {}, {}
    for (i, j) in cs:
        for jj, out in ((j, (i, j - 1)), (j + 1, (i, j + 1))):
            if out not in cs:
                hx.setdefault((jj, out[1] > j), set()).add(i)
        for ii, out in ((i, (i - 1, j)), (i + 1, (i + 1, j))):
            if out not in cs:
                vy.setdefault((ii, out[0] > i), set()).add(j)
    gh = gv = 0
    for s in hx.values():
        for L in runs(sorted(s)):
            gh = gcd(gh, L)
    for s in vy.values():
        for L in runs(sorted(s)):
            gv = gcd(gv, L)
    return gh, gv


def runs(xs):
    out, start, prev = [], xs[0], xs[0]
    for x in xs[1:]:
        if x != prev + 1:
            out.append(prev + 1 - start)
            start = x
        prev = x
    out.append(prev + 1 - start)
    return out


def room_data(cells):
    pts = lattice_points(cells)
    st = {p: status(cells, p) for p in pts}
    r = sum(v == 'reflex' for v in st.values())
    origins, types = {}, {}
    for off in ((0, 0), (1, 0), (1, 1), (0, 1)):
        o = next((p for p in pts if (p[0] % 2, p[1] % 2) == off), None)
        origins[off] = o
    for off, o in origins.items():
        room, t = room_tuple(cells, o)
        n = len(t[0])
        for x in (1, 2, 3):
            m = len(class_congruence(t, [x]))
            cls = ((off[0] + LAB[x][0]) % 2, (off[1] + LAB[x][1]) % 2)
            ty = 'B' if m == 1 else ('Q' if m == n else m)
            assert types.setdefault(cls, ty) == ty, 'B_x type depends on origin'
    gh, gv = edge_gcds(cells)
    return dict(n=len(cells), r=r, W=2 * r + 4, normalized=(gh == 1 and gv == 1), types=types,
                origins=origins, st=st)


def test_room(name, cells, max_states, rows_out):
    cells = set(map(tuple, cells))
    R = room_data(cells)
    types = R['types']
    R['Rstar'] = R['normalized'] and all(v in ('B', 'Q') for v in types.values())
    c = Counter()
    for off, o in R['origins'].items():
        room, t = room_tuple(cells, o)
        n = len(t[0])
        absx = {x: ((off[0] + LAB[x][0]) % 2, (off[1] + LAB[x][1]) % 2) for x in (1, 2, 3)}
        xs = [x for x in (1, 2, 3) if types[absx[x]] != 'Q']
        ipts = [p for p in sorted(R['st']) if ((p[0] - o[0]) % 2, (p[1] - o[1]) % 2) == (0, 0)
                and R['st'][p] == 'interior']
        if len(ipts) < 2:
            continue
        cen = centraliser(t)
        invs = [d for d in cen if d != tuple(range(n)) and all(d[d[i]] == i for i in range(n))]
        Ry = None
        for S, T in combinations(ipts, 2):
            c['pairs'] += 1
            LS = room.points_at((S[0] - o[0], S[1] - o[1]))[1]
            LT = room.points_at((T[0] - o[0], T[1] - o[1]))[1]
            per = {}
            pair_lit = False
            for A in LS:
                for Bq in LT:
                    A_, B_ = tuple(A), tuple(Bq)
                    if xs:
                        v, states, complete = orbit_lit_capped(t, A_, B_, xs, max_states)
                    else:
                        v, states, complete = {}, 0, True
                    c['max_states'] = max(c['max_states'], states)
                    if not complete:
                        c['unresolved_rows'] += 1
                    for x in xs:
                        per[(A_, B_, x)] = v[x][0]
                        pair_lit |= v[x][0]
            c['pair_lit' if pair_lit else 'pair_DARK'] += 1
            for x in xs:
                vals = [per[k] for k in per if k[2] == x]
                kind = types[absx[x]]
                if not any(vals):
                    c['room_pair_x_dark_at_%s' % ('B' if kind == 'B' else 'proper')] += 1
                    if pair_lit:
                        c['room_pair_x_dark_but_pair_lit_at_%s' % ('B' if kind == 'B' else 'proper')] += 1
                for (A_, B_, xx), lit in per.items():
                    if xx != x or lit:
                        continue
                    c['dark_rows_at_%s' % ('B' if kind == 'B' else 'proper')] += 1
                    if Ry is None:
                        Ry = {y: U.Factor(t, R_y(t, y)) for y in (1, 2, 3)}
                    rig = any(Ry[y].m < n and U.rig(Ry[y], x, A_[0], B_[0]) for y in (1, 2, 3) if y != x)
                    c['dark_rows_rigRy'] += rig
                    dl = next((d for d in invs if sorted(d[s] for s in A_) == sorted(B_)), None)
                    fixed = None
                    if dl is not None:
                        fixed = sorted({y for y in range(4) for cy in cycles(t[y])
                                        if sorted(dl[s] for s in cy) == sorted(cy)})
                        c['dark_rows_delta_pair'] += 1
                        fx = [y for y in fixed if y != 0]
                        if fx and x not in fixed:
                            relay = [per.get((A_, B_, y)) for y in fx]
                            c['delta_rows_relay_class_lit'] += any(relay)
                            c['delta_rows_relay_class_checked'] += 1
                    rows_out.append(dict(room=name, a=off, S=S, T=T, x='abcd'[x], Nx=kind,
                                         A=list(A_), B=list(B_), rigRy=rig, pair_lit=pair_lit,
                                         lit_targets=sorted({'abcd'[k[2]] for k, l in per.items() if l}),
                                         delta_fixed=None if fixed is None else ['abcd'[y] for y in fixed]))
            # iota check (d65): (S_f,T_f) ~ (S_b,T_b) and (S_f,T_b) ~ (S_b,T_f) per target
            if len(LS) == 2 and len(LT) == 2:
                for x in xs:
                    A0, A1 = map(tuple, LS)
                    B0, B1 = map(tuple, LT)
                    ok = per[(A0, B0, x)] == per[(A1, B1, x)] and per[(A0, B1, x)] == per[(A1, B0, x)]
                    c['iota_check_ok' if ok else 'iota_check_FAIL'] += 1
    R.pop('origins')
    R.pop('st')
    R['types'] = {'%d%d' % k: v for k, v in sorted(types.items())}
    R['counts'] = dict(c)
    R['name'] = name
    return R


def main():
    max_states = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    t0 = time.process_time()
    rooms = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
             if r['normalized']]
    rooms.sort(key=lambda r: (r['n'], r['cells']))
    named = list(named_rooms()) + [('Z12', NZ.Z12), ('S10', NZ.S10)]
    named += [('T8', {(0, 0), (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (5, 0)}),
              ('Z8', {(0, 0), (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (4, 1), (5, 1)}),
              ('R24', {(i, j) for i in range(4) for j in range(2)})]
    for k in (1843, 1490, 453):
        named.append(('room%d' % k, rooms[k]['cells']))
    rows, out = [], []
    print('== named rooms')
    for name, cells in named:
        R = test_room(name, cells, max_states, rows)
        out.append(R)
        print(name, 'n', R['n'], 'r', R['r'], 'W', R['W'], 'norm', R['normalized'], 'types', R['types'],
              'R*', R['Rstar'], R['counts'], flush=True)
    print('== d64 normalized rooms outside the d64 scope (R* candidates)')
    agg = Counter()
    nR = 0
    for i, r in enumerate(rooms):
        R = room_data(set(map(tuple, r['cells'])))
        if not all(v in ('B', 'Q') for v in R['types'].values()):
            continue
        nR += 1
        R = test_room('cov%d' % i, r['cells'], max_states, rows)
        out.append(R)
        agg.update({k: v for k, v in R['counts'].items() if k != 'max_states'})
        agg['max_states'] = max(agg['max_states'], R['counts'].get('max_states', 0))
        tyk = ''.join(sorted(str(v) for v in R['types'].values()))
        agg['type ' + tyk] += 1
        if R['counts'].get('dark_rows_at_B') or R['counts'].get('pair_DARK'):
            print('cov%d' % i, 'n', R['n'], 'r', R['r'], R['types'], R['counts'], flush=True)
    print('R* rooms in covers.json:', nR)
    print('aggregate:', dict(sorted(agg.items())))
    print('CPU %.1f s' % (time.process_time() - t0))
    json.dump(dict(rooms=out, dark_rows=rows, aggregate=dict(agg)), open(HERE / 'pair_level.json', 'w'),
              default=str)


if __name__ == '__main__':
    main()
