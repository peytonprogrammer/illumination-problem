"""D112: the polynomial bound L >= 8d(N+1) for expanding stepped approaches.

Named test: DBas with corridor stubs absorbed into the chambers, A = left chamber
+ 3 units of corridor, B = right chamber + 2 units. Both approaches expand at the
lip (run [0,5] -> [0,8], run [0,4] -> [-2,4]); run widths <= d = 8. The script
deletes the note's integrality slopes, takes the widest remaining component,
checks with the sealed-chamber tracer that both first-hit words are fixed there,
solves F = 2wm, and traces the full DBas polygon at total corridor 3 + Lmid + 2.
"""
import sys
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path
from chamber import leg, shoot_room
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd110-review-length'))
from geom import room

A_V = [(0, 0), (5, 0), (5, 1), (8, 1), (8, 2), (5, 2), (5, 4), (0, 4)]; A_M = (8, 1, 2)
w, p, d = F(1), F(1), F(8)


def B_poly(x0):  # right chamber [x0, x0+4] x [-1,5] with stub [x0-2, x0] x [1,2]
    return [(x0, -1), (x0 + 4, -1), (x0 + 4, 5), (x0, 5), (x0, 2), (x0 - 2, 2), (x0 - 2, 1), (x0, 1)], (x0 - 2, 1, 2)


def levels(y):
    """Distances to listed levels for an approach from height y (only the lip here)."""
    if y > p + w:
        return [y - (p + w)]
    if y < p:
        return [p - y]
    return []


def excluded(x, hs, sigma):
    """t in (2d/w, 4d/w) with x + sigma*h*t integral, for each listed distance h."""
    out = set()
    for h in hs:
        a, b = x + sigma * h * 2 * d / w, x + sigma * h * 4 * d / w
        for n in range(floor(min(a, b)), ceil(max(a, b)) + 1):
            t = (n - x) / (sigma * h)
            if 2 * d / w < t < 4 * d / w:
                out.add(1 / t)
    return out


def run(S, T, Lmid):
    x0 = 8 + Lmid + 2
    BV, BM = B_poly(x0)
    ys, yt = F(S[1]), F(T[1])
    hyS = -1 if ys > p + w / 2 else 1   # toward the nearer lip / door
    hyT = -1 if yt > p + w / 2 else 1
    N = sum(ceil(2 * d * h / w) for h in levels(ys) + levels(yt))
    ex = excluded(F(S[0]), levels(ys), 1) | excluded(F(T[0]), levels(yt), -1)
    assert len(ex) <= N, (len(ex), N)
    pts = sorted(ex | {w / (4 * d), w / (2 * d)})
    lo, hi = max(zip(pts, pts[1:]), key=lambda ab: ab[1] - ab[0])
    assert hi - lo >= w / (4 * d * (N + 1))
    cutsA = [0, 5, 8, S[0]]; cutsB = [x0 - 2, x0, x0 + 4, T[0]]
    def legs(s):
        a = leg(A_V, A_M, cutsA, S, s, 1, hyS)
        b = leg(BV, BM, cutsB, T, s, -1, hyT)
        return a, b
    sig = []
    for s in (lo + (hi - lo) / 1000, (lo + hi) / 2, hi - (hi - lo) / 1000):
        a, b = legs(s)
        sig.append((a['a'], a['nv'], a['nh'], b['a'], b['nv'], b['nh']))
    assert sig[0] == sig[1] == sig[2], sig
    am, bm = legs((lo + hi) / 2)
    phi = lambda r: r['exit'][2] * (r['exit'][0] - p)          # signed by own vertical velocity
    def Fv(s):
        a, b = legs(s)
        return Lmid * s + phi(a) + phi(b)                         # backward leg enters with a plus
    slope = Lmid + am['a'] + bm['a']
    Flo, Fhi = Fv(lo + (hi - lo) / 1000), Fv(hi - (hi - lo) / 1000)
    m = floor(Flo / (2 * w)) + 1
    assert 2 * w * m < Fhi, "range does not reach a multiple of 2w"
    s0 = (lo + hi) / 2
    s = s0 + (2 * w * m - Fv(s0)) / slope
    assert lo < s < hi and Fv(s) == 2 * w * m
    R = room('DBas', 3 + Lmid + 2)
    hits = shoot_room(R['V'], S, (1, hyS * s), T)
    return N, 8 * d * (N + 1), len(hits)


if __name__ == '__main__':
    for S, Ty in (((1, 3), 3), ((4, 1), 1), ((F(13, 2), F(3, 2)), 4), ((2, F(1, 3)), F(9, 2))):
        N = sum(ceil(2 * d * h / w) for h in levels(F(S[1])) + levels(F(Ty)))
        Lmid = int(8 * d * (N + 1))
        T = (F(8 + Lmid + 2 + 1), F(Ty))
        print(f"S={S} T={T} Lmid=8d(N+1)={Lmid}:", run(S, T, Lmid))
