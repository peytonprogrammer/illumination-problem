"""Explicit rooms from population G (r = 3) where the new families fail.
O1: Lemma H configuration, resonant, no sign pair has a candidate.
O2: Lemma C+ perp configuration with a vertex strictly inside K, and no valid
    window candidate for any sign pair (|k1| <= 60)."""
import json, time
from rooms import Room, shoot
import newlemmas as nl
from newlemmas import Geo, SYMS
from test_lemmas import open_lists
t0 = time.time()
opens = open_lists()
o1 = o2 = None
n1 = n2 = n2all = rooms = 0
for l in open("runs/g_rooms.txt"):
    a, b = l.split("|"); r, nx, ny, mask, *gx = map(int, a.split())
    if r != 3 or rooms >= 600: continue
    rooms += 1
    R = Room(nx, ny, mask, gx, list(map(int, b.split())))
    g = Geo(R.cells, R.W, R.H); pts = R.interior_points(); op = opens[(nx, ny, mask)]
    ty = [R.ptype(P) for P in pts]
    for sym in SYMS:
        o = g.tr(sym); tp = [g.tp(sym, P) for P in pts]
        for i, A in enumerate(tp):
            for j, B in enumerate(tp):
                if i == j or frozenset((ty[i], ty[j])) not in op: continue
                nl.CHECK_K = True
                for cfg in nl.H_configs(o, A, B):
                    if not any(nl.H_solve(cfg, A, B)):
                        n1 += 1
                        if o1 is None: o1 = (l.strip(), R.shape(), pts[i], pts[j], sym, A, B, cfg, shoot(R, pts[i], pts[j], 60)[:3])
                nl.CHECK_K = False
                for cfg in nl.Cperp_configs(o, A, B):
                    if cfg[-1]: continue
                    nl.CHECK_K = True
                    inK = any(c2[:6] == cfg[:6] for c2 in nl.Cperp_configs(o, A, B))
                    nl.CHECK_K = False
                    if inK: continue
                    n2all += 1
                    sol = nl.Cperp_solve(o, cfg, A, B, K=60)
                    if not any(sol):
                        n2 += 1
                        if o2 is None: o2 = (l.strip(), R.shape(), pts[i], pts[j], sym, A, B, cfg, shoot(R, pts[i], pts[j], 60)[:3])
print("r=3 rooms scanned", rooms, "seconds", round(time.time() - t0, 1))
print("O1 count", n1, o1)
print("O2: perp configurations with a vertex inside K", n2all, "no valid window candidate", n2, o2)
