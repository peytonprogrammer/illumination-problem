# Hand checks, not a population test: d15 T-shape example and the 4-step staircase.
from rooms import Room, shoot
from newlemmas import *
# T-shape: bar [0,31]x[0,10], tab [20,30]x[10,12], S=(5,1), T=(21,11)
R = Room(3, 2, 0b010111, [20, 10, 1], [10, 2])
g = Geo(R.cells, R.W, R.H)
S, T = (5, 1), (21, 11)
for cfg in H_configs(g, S, T):
    sol = H_solve(cfg, S, T)
    print("T-shape cfg", cfg, sol, [trace(g, S, T, x[2], x[3]) for x in sol if x])
# staircase mask 4991, V2 on the chord (all gaps equal) and below the chord
for gx, gy in (([3, 3, 3, 3], [3, 3, 3, 3]), ([3, 5, 1, 3], [3, 1, 5, 3]), ([3, 1, 5, 3], [3, 5, 1, 3])):
    R = Room(4, 4, 4991, gx, gy)
    g = Geo(R.cells, R.W, R.H)
    S, T = (1, R.H - 1), (R.W - 1, 1)
    print(R.shape(), gx, gy, "shoot", shoot(R, S, T, 40)[:3])
    for sym in SYMS:
        for (A, B) in ((S, T), (T, S)):
            o = g.tr(sym); a, b = g.tp(sym, A), g.tp(sym, B)
            for cfg in Cperp_configs(o, a, b):
                print("  perp", sym, cfg, Cperp_solve(o, cfg, a, b))
            for cfg in Cpar_configs(o, a, b):
                print("  par", sym, cfg, Cpar_solve(o, cfg, a, b))
