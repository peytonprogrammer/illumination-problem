"""Smallest rooms of order type 122 (`#../###/.#.`) where Lemma H is resonant
and no sign pair has a candidate. Pair types (1, 3) and (3, 1). Rooms: gaps
with sum at most 12 on x and at most 8 on y (not a sampled population)."""
import itertools, time
from rooms import Room, shoot
import newlemmas as nl
from newlemmas import Geo, SYMS
t0 = time.time(); rooms = found = inst = 0; first = None; undec = 0
for gx in itertools.product(range(1, 11), repeat=3):
    if sum(gx) > 12: continue
    for gy in itertools.product(range(1, 7), repeat=3):
        if sum(gy) > 8: continue
        R = Room(3, 3, 122, gx, gy); g = Geo(R.cells, R.W, R.H); rooms += 1
        pts = R.interior_points()
        Ss = [P for P in pts if R.ptype(P) == (1, 3)]; Ts = [P for P in pts if R.ptype(P) == (3, 1)]
        o = g.tr((0, 0, 1))                      # flip y: T above S
        for S in Ss:
            for T in Ts:
                inst += 1
                A, B = g.tp((0, 0, 1), S), g.tp((0, 0, 1), T)
                cfgs = list(nl.H_configs(o, A, B))
                assert len(cfgs) == 1
                if not any(nl.H_solve(cfgs[0], A, B)):
                    found += 1
                    sh = shoot(R, S, T, 80)
                    if sh is None: undec += 1
                    if first is None: first = (gx, gy, S, T, cfgs[0], sh[:3] if sh else None, len(sh[3]) if sh else None)
print("rooms", rooms, "instances", inst, "H has no candidate", found, "of which not lit at bound 80", undec, "seconds", round(time.time() - t0, 1))
print("first", first)
