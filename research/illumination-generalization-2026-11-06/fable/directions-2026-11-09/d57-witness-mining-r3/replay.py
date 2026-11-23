"""Independent exact replay. Builds the walls from the cell set with d15's
raycast.wall_segments (unit edges in index space, not the maximal walls of
wm.py), maps index coordinates to real grid coordinates, and follows the
billiard path from S with velocity T* - S for unit time with Fractions.
A path is accepted iff it touches no vertex and ends exactly at T."""
import sys, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
from raycast import wall_segments


def follow(cells, xs, ys, S, V):
    H, Vw, verts = wall_segments(cells)
    H = [(ys[y], xs[a], xs[b]) for (y, a, b) in H]
    Vw = [(xs[x], ys[a], ys[b]) for (x, a, b) in Vw]
    verts = [(xs[i], ys[j]) for (i, j) in verts]
    x, y = Fr(S[0]), Fr(S[1]); vx, vy = Fr(V[0]), Fr(V[1]); left = Fr(1); nref = 0
    while left > 0:
        best = left; hit = None
        for (wy, x0, x1) in H:
            if vy != 0:
                t = (wy - y) / vy
                if 0 < t <= best and x0 <= x + t * vx <= x1 and (t < best or hit is None): best, hit = t, 'h'
        for (wx, y0, y1) in Vw:
            if vx != 0:
                t = (wx - x) / vx
                if 0 < t <= best and y0 <= y + t * vy <= y1 and (t < best or hit is None): best, hit = t, 'v'
        for (px, py) in verts:
            dx, dy = px - x, py - y
            if dx * vy == dy * vx:
                t = dx / vx if vx != 0 else (dy / vy if vy != 0 else None)
                if t is not None and 0 < t <= best: return None, False, nref
        x += best * vx; y += best * vy; left -= best
        if left == 0: break
        if hit == 'h': vy = -vy; nref += 1
        elif hit == 'v': vx = -vx; nref += 1
    return (x, y), True, nref


def lit_by(cells, xs, ys, S, T, Tstar):
    V = (Tstar[0] - S[0], Tstar[1] - S[1])
    end, ok, n = follow(cells, xs, ys, S, V)
    return ok and end == (Fr(T[0]), Fr(T[1])), n


def replay_cover(C, nvert=8, nint=2, seed=7):
    """Independent re-check of every certified box of a bb.Cover: exact replay
    at up to nvert random vertices and nint random interior dyadic points.
    Returns (points checked, failures)."""
    import random, wm
    rng = random.Random(seed)
    par, ot = C.par, C.par.ot
    SC = 1 << 24
    n = bad = 0
    for box, it in C.cert:
        B = wm.build(par, it)
        pts = []
        for _ in range(nvert):
            pts.append([l if (l == h or rng.random() < .5) else h for (l, h) in box])
        for _ in range(nint):
            pts.append([l if l == h else rng.randrange(l, h + 1) for (l, h) in box])
        for v in pts:
            vals = {k: Fr(x, SC) for k, x in enumerate(v)}
            ev = lambda f: sum(c * vals[k] for k, c in f)
            xs = [ev(f) for f in par.xf]; ys = [ev(f) for f in par.yf]
            S = (ev(par.Sf[0]), ev(par.Sf[1])); T = (ev(par.Tf[0]), ev(par.Tf[1]))
            okreg = all(xs[i] < xs[i + 1] for i in range(len(xs) - 1)) and \
                all(ys[i] < ys[i + 1] for i in range(len(ys) - 1))
            for P, Pt in ((S, par.S), (T, par.T)):
                for a, g in ((0, xs), (1, ys)):
                    i = Pt[a] // 2
                    okreg &= (P[a] == g[i]) if Pt[a] % 2 == 0 else (g[i] < P[a] < g[i + 1])
            ok, _ = lit_by(ot.cells, xs, ys, S, T, (ev(B['Tstar'][0]), ev(B['Tstar'][1])))
            n += 1; bad += not (ok and okreg)
    return n, bad
