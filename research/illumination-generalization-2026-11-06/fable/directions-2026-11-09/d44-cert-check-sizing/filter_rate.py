"""Pass rate of the proved reflex-class filter F* on sample rooms (stdin: 'n x0 y0 ...').

F*: a full triple at r <= 8 needs a class x with a non-Galois quotient (d36.3 + d2),
so delta >= 3, z in {1, 2}, d <= 4z+1 (4z if d even), delta*z <= r, n = delta*d (d36.4).
Each zero of N has delta unramified preimages, all reflex corners of one parity class.
So the z zeros need sum over parity classes y of floor(rho_y / delta) >= z, where rho_y
counts reflex corners in class y.  At r <= 8 this forces z <= 2 and d <= 9.
"""
import sys
from collections import defaultdict

def cases(n, r):
    """(delta, d, zmin, zmax) with n = delta*d, delta >= 3, z >= 1, delta*z <= r, d <= 4z+1 (4z if d even)."""
    out = []
    for d in range(3, n + 1):
        if n % d:
            continue
        delta = n // d
        if delta < 3:
            continue
        zmin = max(1, (d + 2) // 4 if d % 2 else (d + 3) // 4)
        zmax = r // delta
        if zmin <= zmax:
            out.append((delta, d, zmin, zmax))
    return out

def passes(rho, n, r):
    """Some case with sum_y floor(rho_y / delta) >= zmin (z zeros, each with delta reflex
    preimages in one parity class)."""
    return any(sum(x // delta for x in rho) >= zmin for delta, d, zmin, zmax in cases(n, r))

stat = defaultdict(lambda: [0, 0])
for line in sys.stdin:
    v = list(map(int, line.split()))
    n = v[0]
    cells = set(zip(v[1::2], v[2::2]))
    rho = [0, 0, 0, 0]
    r = 0
    pts = {(x + u, y + w) for (x, y) in cells for u in (0, 1) for w in (0, 1)}
    for (x, y) in pts:
        k = sum((x - 1 + u, y - 1 + w) in cells for u in (0, 1) for w in (0, 1))
        if k == 3:
            r += 1
            rho[(x % 2) * 2 + (y % 2)] += 1
    s = stat[(r, n)]
    s[0] += 1
    s[1] += passes(rho, n, r)
for (r, n), (a, b) in sorted(stat.items()):
    print('r %d area %d sampled %d pass %d rate %.4f' % (r, n, a, b, b / a))
