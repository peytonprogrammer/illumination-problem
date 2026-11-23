"""The 22-wall room: every check of run_census.py on one fixed polygon.

Usage: python3 -B room22.py   -> prints a report and writes room22.json
"""
import json
import sys
import time

sys.dont_write_bytecode = True
import d0lib as L
import hurwitz as hz
import run_census as rc

V = [(0, 2), (0, 4), (1, 4), (1, 5), (2, 5), (2, 6), (4, 6), (4, 5), (5, 5), (5, 4), (6, 4), (6, 3),
     (4, 3), (4, 4), (2, 4), (2, 2), (3, 2), (3, 0), (2, 0), (2, 1), (1, 1), (1, 2)]
S, T = (1, 3), (3, 5)
cells = L.cells_from_vertices(V)
rep = dict(area=len(cells), strictly_simple=L.strictly_simple(cells),
           regular_points=[(p, L.status(cells, p)) for p in L.regular_points(cells)])

# 1. the slope signs: which sign pairs pass the state-level check on this room
rep['sign_pairs_that_pass'] = L.calibrate(cells, S)

# 2. the tuple built here equals the tuple of d10-mechanisms/roomtools.py
sys.path.insert(0, str(L.HERE.parent / 'd10-mechanisms'))
import roomtools as rt
room, t_rt = rt.room_tuple(cells, S)
sheets, t = L.room_tuple(cells, S)
keys = [room.tiles[room.faces[f][0]]['key'] for f in room.sheets]
perm = [sheets.index((i + S[0], j + S[1])) for (i, j) in keys]
rep['own_tuple_equals_roomtools_tuple'] = all(
    tuple(perm[g[k]] for k in range(len(perm))) == tuple(h[perm[k]] for k in range(len(perm)))
    for g, h in zip(t_rt, t))
rep['cycle_types'] = [hz.cycle_type(g) for g in t]

# 3. class of S: tuple orbit, state-level check, hurwitz.marked_orbit, room orbit
t0 = time.time()
chk, bad, skip, res = L.state_check(cells, S, rc.EPS)
ident = res['ident']
name = {v: k for k, v in ident.items()}
ref = hz.marked_orbit(t)
ro = L.room_orbit(cells)
a_pts = set(ident)
tup_lit = {frozenset(name[i] for i in pr) for pr in res['lit']}
room_lit = {pr for pr in ro['lit'] if pr <= a_pts}
rep['class_of_S'] = dict(
    tuple_states=res['states'], state_arc_checks=chk, mismatches=bad, skipped_large_slope=skip,
    marked_orbit_states=ref['states'], marked_orbit_same_lit=ref['lit'] == res['lit'],
    room_states=ro['states'], room_complete=ro['complete'],
    tuple_lit=sorted(sorted(pr) for pr in tup_lit), room_lit=sorted(sorted(pr) for pr in room_lit),
    equal=tup_lit == room_lit)
rep['lift_pairs'] = [dict(S_face=fs, T_face=ft,
                          tuple_LIT=frozenset(((S, fs), (T, ft))) in tup_lit,
                          room_lit=frozenset(((S, fs), (T, ft))) in room_lit)
                     for fs in (1, -1) for ft in (1, -1)]

# 4. all four classes and d8's C decider
rc.PYCAP = 10 ** 7
r = rc.do_room(cells)
rep['all_classes'] = {k: r[k] for k in ('inst', 'dp_pairs', 'dp_lit_T', 'dp_lit_R', 'dp_disagree',
                                        'room_pairs', 'room_pairs_lit_T', 'room_pairs_lit_C',
                                        'room_disagree', 'c_disagree', 'checks', 'mismatch', 'skipped',
                                        't_states', 'r_states', 'slide_only', 'iota_bad', 'replay_fail')}
rep['seconds'] = round(time.time() - t0, 1)
print(json.dumps(rep, indent=1, default=list))
with open(L.HERE / 'room22.json', 'w') as f:
    json.dump(rep, f, indent=1, default=list)
