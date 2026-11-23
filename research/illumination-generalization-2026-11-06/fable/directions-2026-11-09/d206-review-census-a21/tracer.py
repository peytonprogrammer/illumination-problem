"""Independent exact-rational billiard tracer in the room plane.

Shares no code or method with shoot.c / verify_plane.c: the room is turned into
maximal wall segments, and a ray with rational position and integer velocity is
advanced wall-hit to wall-hit by segment intersection (Fractions).  Any contact
with a wall endpoint (a corner of the polygon) kills the path.  The ray is
checked to stay inside the closed room after every leg.
"""
from fractions import Fraction as F

def walls_of(cells):
    s = set(cells)
    hor, ver = set(), set()
    for x, y in s:
        if (x, y-1) not in s: hor.add((x, y))
        if (x, y+1) not in s: hor.add((x, y+1))
        if (x-1, y) not in s: ver.add((x, y))
        if (x+1, y) not in s: ver.add((x+1, y))
    H, V = [], []
    for x, y in hor:
        if (x-1, y) not in hor:
            e = x
            while (e, y) in hor: e += 1
            H.append((y, x, e))
    for x, y in ver:
        if (x, y-1) not in ver:
            e = y
            while (x, e) in ver: e += 1
            V.append((x, y, e))
    corners = {(x0, y) for y, x0, x1 in H} | {(x1, y) for y, x0, x1 in H}
    return H, V, corners

def inside(s, px, py):
    """closed-room membership of a rational point"""
    import math
    xs = {math.floor(px)} | ({int(px) - 1} if px.denominator == 1 else set())
    ys = {math.floor(py)} | ({int(py) - 1} if py.denominator == 1 else set())
    return any((x, y) in s for x in xs for y in ys)

class Room:
    def __init__(self, cells):
        self.s = set(cells)
        self.H, self.V, self.corners = walls_of(cells)
        # interior lattice points
        self.marks = {(x, y) for x, y in {(a+1, b+1) for a, b in self.s}
                      if {(x-1, y-1), (x, y-1), (x-1, y), (x, y)} <= self.s}

    def trace(self, src, vel, tmax, target=None):
        """Advance for total time tmax (velocity vel = one lattice step per unit).
        Returns (ok, first_target_time, final_point). ok=False if a corner is met
        at time <= tmax (or before the target when stop_at_target)."""
        px, py = F(src[0]), F(src[1]); vx, vy = vel
        t = F(0); first = None
        tmax = F(tmax)
        while True:
            best = None  # (dt, kind, is_corner)
            for c, y0, y1 in self.V:
                if vx:
                    dt = (c - px) / vx
                    if dt > 0:
                        y = py + vy * dt
                        if y0 <= y <= y1:
                            cand = (dt, 'V', (c, y) in self.corners)
                            if best is None or cand[0] < best[0]: best = cand
                elif px == c:
                    for e in (y0, y1):
                        dt = (e - py) / vy
                        if dt > 0 and (best is None or dt < best[0]): best = (dt, 'V', True)
            for r, x0, x1 in self.H:
                if vy:
                    dt = (r - py) / vy
                    if dt > 0:
                        x = px + vx * dt
                        if x0 <= x <= x1:
                            cand = (dt, 'H', (x, r) in self.corners)
                            if best is None or cand[0] < best[0] or (cand[0] == best[0] and cand[2]): best = cand
                elif py == r:
                    for e in (x0, x1):
                        dt = (e - px) / vx
                        if dt > 0 and (best is None or dt < best[0]): best = (dt, 'H', True)
            dt = best[0]
            leg = min(dt, tmax - t)
            if not inside(self.s, px + vx * leg / 2, py + vy * leg / 2):
                raise AssertionError('left room')
            if target is not None and first is None:
                if vx: tt = (target[0] - px) / vx
                else: tt = (target[1] - py) / vy
                if 0 < tt <= leg and px + vx * tt == target[0] and py + vy * tt == target[1]:
                    first = t + tt
            if t + dt > tmax:
                return True, first, (px + vx * leg, py + vy * leg)
            px += vx * dt; py += vy * dt; t += dt
            if best[2]:
                return False, first, (px, py)
            if best[1] == 'V': vx = -vx
            else: vy = -vy
            if t == tmax:
                return True, first, (px, py)

def check_witness(line):
    v = list(map(int, line.split()))
    n, ax, ay, bx, by, dx, dy, m = v[:8]
    cells = list(zip(v[8::2], v[9::2]))
    assert len(cells) == n
    R = Room(cells)
    assert (ax, ay) in R.marks and (bx, by) in R.marks and (ax, ay) != (bx, by)
    ok, first, end = R.trace((ax, ay), (dx, dy), m, (bx, by))
    return ok, first, m, end == (bx, by), R
