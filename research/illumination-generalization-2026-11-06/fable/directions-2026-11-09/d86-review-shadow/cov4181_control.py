"""Independent exact check of the cov4181 control in shadow-budget.snapshot.md.

Uses only the cell list of cov4181 (copied from qclass-closure/bbbb/shortest.py).
1. Ordinary visibility of m=(4,2) from S=(2,3) and from T=(4,3) by straight chords.
2. Bounded exact enumeration of legal billiard paths S->T (unfolded displacement
   |D| <= L) and the parity / location of their midpoints.  This is a sanity
   check of D66's class-d verdict up to length L, not a proof.
Run: python3 -B cov4181_control.py
"""
from fractions import Fraction as F
from math import floor, gcd

cells = {(x, y) for x, ys in enumerate([range(6), (2, 3), (2, 3), range(6), range(6), (2, 3), (2,), range(3)]) for y in ys}
S, T, m = (2, 3), (4, 3), (4, 2)
assert len(cells) == 28


def status(p):
    x, y = p
    return sum((x - i, y - j) in cells for i in (0, 1) for j in (0, 1))


def vedge_open(X, y0):   # vertical edge x=X, y0<y<y0+1 is interior (not a wall)
    return (X - 1, y0) in cells and (X, y0) in cells


def hedge_open(x0, Y):
    return (x0, Y - 1) in cells and (x0, Y) in cells


def trace(D):
    """Trace from S with unfolded displacement D for unit time.
    Return (legal, endpoint, midpoint).  Illegal: hits a convex/reflex corner
    or runs along a wall.  Exact rational arithmetic."""
    px, py = F(S[0]), F(S[1])
    vx, vy = D
    t = F(0)
    mid = None
    while True:
        # next grid-line hits
        cand = [F(1) - t]
        tx = ty = None
        if vx:
            nx = floor(px) + 1 if vx > 0 else (px - 1 if px == int(px) else F(floor(px)))
            tx = (F(nx) - px) / vx
            cand.append(tx)
        if vy:
            ny = floor(py) + 1 if vy > 0 else (py - 1 if py == int(py) else F(floor(py)))
            ty = (F(ny) - py) / vy
            cand.append(ty)
        dt = min(cand)
        # axial travel along a grid line: check that the traversed edge is interior
        if vx == 0 and px == int(px):
            y0 = min(py, py + vy * dt)
            if not vedge_open(int(px), floor(y0)):
                return False, None, None
        if vy == 0 and py == int(py):
            x0 = min(px, px + vx * dt)
            if not hedge_open(floor(x0), int(py)):
                return False, None, None
        if mid is None and t + dt >= F(1, 2):
            h = F(1, 2) - t
            mid = (px + vx * h, py + vy * h)
            if mid[0] == int(mid[0]) and mid[1] == int(mid[1]) and status((int(mid[0]), int(mid[1]))) in (1, 3):
                return False, None, None
        px, py, t = px + vx * dt, py + vy * dt, t + dt
        if t == 1:
            return True, (px, py), mid
        onx = vx != 0 and tx == dt
        ony = vy != 0 and ty == dt
        if (vx == 0 and px == int(px)) or (vy == 0 and py == int(py)):
            if (onx or ony) and px == int(px) and py == int(py):
                st = status((int(px), int(py)))
                if st in (1, 3):
                    return False, None, None
                if st == 2:   # axial path meets a perpendicular wall at a lattice point
                    vx, vy = -vx, -vy
            continue
        if onx and ony:   # lattice point
            p = (int(px), int(py))
            st = status(p)
            if st in (1, 3):
                return False, None, None
            # st 4: interior, pass straight.  st 2: smooth wall, reflect normal component
            if st == 2:
                # determine wall orientation: vertical wall if both cells on one x-side
                left = sum((p[0] - 1, p[1] - j) in cells for j in (0, 1))
                if left in (0, 2):
                    vx = -vx
                else:
                    vy = -vy
        elif onx:
            X = int(px)
            y0 = floor(py)
            if not vedge_open(X, y0):
                vx = -vx
        elif ony:
            Y = int(py)
            x0 = floor(px)
            if not hedge_open(x0, Y):
                vy = -vy


# 1. Ordinary visibility of m
print("status S,T,m:", status(S), status(T), status(m), " (4=interior)")
for src in (S, T):
    D = (m[0] - src[0], m[1] - src[1])
    g = gcd(abs(D[0]), abs(D[1]))
    # straight chord: legal iff tracing from src never reflects; use a local tracer
    # by reusing trace with S temporarily replaced
    S_saved = S
    globals()['S'] = src
    ok, end, _ = trace(D)
    globals()['S'] = S_saved
    print(f"chord {src}->{m}: D={D}, gcd={g}, legal={ok}, end={end}, |D|^2={D[0]**2+D[1]**2}")

# 2. Bounded enumeration of legal paths S->T
L = 40
byclass = {}
mids_d = set()
for dx in range(-L, L + 1):
    for dy in range(-L, L + 1):
        if (dx, dy) == (0, 0) or dx * dx + dy * dy > L * L or dx % 2 or dy % 2:
            continue
        ok, end, mid = trace((dx, dy))
        if not ok or end != (F(T[0]), F(T[1])):
            continue
        par = ((S[0] + dx // 2) % 2, (S[1] + dy // 2) % 2)
        byclass.setdefault(par, []).append((dx, dy))
        if par == (0, 0):
            mids_d.add(mid)
print(f"legal S->T paths with |D|<={L}, by absolute midpoint parity:",
      {k: len(v) for k, v in sorted(byclass.items())})
print("shortest per class:", {k: min(v, key=lambda d: d[0]**2 + d[1]**2) for k, v in sorted(byclass.items())})
print("class (0,0) midpoints found:", sorted(mids_d))
