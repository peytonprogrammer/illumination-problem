"""Complete one-pass chord lists for the mask-761 pyramid, exact integers.
Room: x in [0,w]: y in [-q, h+d+f]; x in [w,u]: y in [0,h+d]; x in [u,V]: y in [0,h].
S = (x, h+d+a), T = (z, h-b). Usage: onepass.py w u V q h d f x z a b"""
import sys
from math import lcm

def sweep(segs, start, target, n, den):
    """segs: (lo, hi, travel, singular set at the end gate). Slope n/den per unit travel.
    Positions are kept times den. Returns True when the chord ends on target."""
    pos, vel = start * den, n
    for lo, hi, t, sing in segs:
        W = (hi - lo) * den
        q = pos - lo * den + vel * t
        m = q % (2 * W)
        if (q // W) % 2: vel = -vel
        pos = lo * den + (m if m <= W else 2 * W - m)
        if pos in {s * den for s in sing}: return False
    return pos == target * den

def lists(w, u, V, q, h, d, f, x, z, a, b):
    D = a + d + b
    vsegs = [(0, w, a, {w}), (0, u, d, {u}), (0, V, b, set())]
    Pv = 2 * D * lcm(w, u, V)
    vh = [n for n in range(Pv) if sweep(vsegs, x, z, n, D)]
    Dh = z - x
    hsegs = [(0, h, z - u, {h}), (0, h + d, u - w, {0, h + d}), (-q, h + d + f, w - x, set())]
    Ph = 2 * Dh * lcm(h, h + d, q + h + d + f)
    hh = [n for n in range(Ph) if sweep(hsegs, h - b, h + d + a, n, Dh)]
    return (Pv, vh), (Ph, hh), (vsegs, hsegs, D, Dh)

if __name__ == '__main__':
    p = list(map(int, sys.argv[1:12]))
    (Pv, vh), (Ph, hh), _ = lists(*p)
    print('vertical   period', Pv, 'hits', len(vh), vh[:6])
    print('horizontal period', Ph, 'hits', len(hh), hh[:6])
