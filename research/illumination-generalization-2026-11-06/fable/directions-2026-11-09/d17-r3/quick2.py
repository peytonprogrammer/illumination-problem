from rooms import Room, shoot
from newlemmas import *
def show(R, S, T):
    g = Geo(R.cells, R.W, R.H)
    print(R.shape(), R.gx, R.gy, S, T, "types", R.ptype(S), R.ptype(T))
    for sym in SYMS:
        for (A, B) in ((S, T), (T, S)):
            o = g.tr(sym); a, b = g.tp(sym, A), g.tp(sym, B)
            for cfg in H_configs(o, a, b): print("  H", sym, cfg, H_solve(cfg, a, b), "resonant", H_resonant(cfg, a, b))
            for cfg in Cperp_configs(o, a, b): print("  perp", sym, cfg, Cperp_solve(o, cfg, a, b))
            for cfg in Cpar_configs(o, a, b): print("  par", sym, cfg)
show(Room(3, 3, 122, [2, 2, 2], [2, 2, 2]), (1, 3), (3, 1))
show(Room(3, 3, 122, [4, 2, 6], [2, 6, 2]), (1, 3), (5, 1))
show(Room(4, 4, 4991, [3, 4, 2, 3], [3, 4, 2, 3]), (1, 11), (11, 1))
show(Room(4, 4, 4991, [3, 2, 4, 3], [3, 2, 4, 3]), (1, 11), (11, 1))
