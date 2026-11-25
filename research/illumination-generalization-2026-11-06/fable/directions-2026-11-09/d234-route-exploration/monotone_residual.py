"""Exact horizontal (x-monotone) list on the gate-box residual chart.

Chart from bbbb/l1-two-gate-chart.md: transverse supports
0, N-1, N, 2N, 2N+1, 5N/2, 3N, 4N; tiers (0,5N/2),(0,N),(N-1,2N+1),(2N,3N),(2N,4N)
on axial slabs [y0,y1],...,[y4,y5]; S = (N-1, y1), T = (5N/2, y4).

An x-monotone ray from S to T crosses four columns once each:
  c1 x in [N-1, N]     interval [y0, y3]
  c2 x in [N, 2N]      interval [y2, y3]
  c3 x in [2N, 2N+1]   interval [y2, y5]
  c4 x in [2N+1, 5N/2] interval [y3, y5]
Open transmissions: x=N and x=2N need y in (y2, y3); x=2N+1 needs (y3, y5).
Endpoint hits on horizontal walls exactly at a transition are rejected
(conservative). Integer vertical travel V gives slope V/X, X = 3N/2 + 1.
Legality is periodic in V with period X * lcm(2h_i); the scan is complete
(it stops early after 5 hits).
"""
import sys
from fractions import Fraction as F
from math import lcm


def run(N, levels):
    y0, y1, y2, y3, y4, y5 = levels
    X = 3 * N // 2 + 1
    cols = [(1, y0, y3), (N, y2, y3), (1, y2, y5), (N // 2 - 1, y3, y5)]
    gates = [(y2, y3), (y2, y3), (y3, y5)]
    P = X * lcm(*[2 * (b - a) for _, a, b in cols])
    hits = []
    for V in range(1, P + 1):
        s = F(V, X)
        for d0 in (1, -1):
            y, d, ok = F(y1), d0, True
            nbounce = 0
            for i, (w, a, b) in enumerate(cols):
                h = b - a
                t = y - a
                phi = t if d == 1 else 2 * h - t
                z = phi + s * w
                nbounce += int(z // h) if z > 0 else 0
                phi2 = z % (2 * h)
                if phi2 == 0 or phi2 == h:
                    ok = False
                    break
                if phi2 < h:
                    y, d = a + phi2, 1
                else:
                    y, d = a + 2 * h - phi2, -1
                if i < 3:
                    lo, hi = gates[i]
                    if not (lo < y < hi):
                        ok = False
                        break
            if ok and y == y4:
                hits.append((V, d0, nbounce))
        if len(hits) >= 5:
            break
    return X, P, hits


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "d233":  # validation: known (1,2) witness, V = 2X
        N = int(sys.argv[2]); B = 2 * N + 2
        X, P, hits = run(N, (-1, 0, 1, 1 + B, 2 + B, 3 + B))
    else:
        m = int(sys.argv[2]); N = 64 * m * m
        X, P, hits = run(N, (-(m + 2), 0, 1, 1 + m, 2 + m, 3 + 2 * m))
    print(f"{mode} {sys.argv[2]}: X={X} period={P} hits={len(hits)}")
    for V, d0, nb in hits[:8]:
        print(f"  V={V} slope={F(V, X)} start_dir={d0} horizontal_bounces={nb}")
