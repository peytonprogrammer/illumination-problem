"""Count z = 4 shapes whose >= 3 singular classes need the cone (README step 4 argues from
corners, i.e. cvx/rfx orbits only; shapes.py also counts a cone class as singular).
Usage: python3 -B strict_sing.py skel_output.txt ..."""
import sys
from collections import Counter
CLS = [(0, 2), (1, 2), (0, 3), (1, 3)]  # (V_i, H_j) generator indices, rows V0 V1 H0 H1


def orbit_types(G, a, b, n):
    seen, out = set(), []
    for c in range(n):
        if c in seen:
            continue
        comp, ends, cyc = {c}, 0, False
        for first in (a, b):
            cur, g = c, first
            while True:
                nx = G[g][cur]
                if nx == cur:
                    ends += 1
                    break
                if nx == c:
                    cyc = True
                    break
                comp.add(nx)
                cur, g = nx, (b if g == a else a)
            if cyc:
                break
        seen |= comp
        L = len(comp)
        out.append({2: 'cone', 4: 'int'}[L] if cyc else {1: 'cvx', 2: 'smooth', 3: 'rfx'}[L])
    return out


diff = Counter()
for path in sys.argv[1:]:
    for line in open(path):
        head, form = line.split('|')
        d, z, cone, sing = map(int, head.split())
        if z != 4 or sing < 3:
            continue
        f = list(map(int, form.split()))
        G = [[f[4 * i + g] for i in range(d)] for g in range(4)]
        strict = sum(any(t in ('cvx', 'rfx') for t in orbit_types(G, a, b, d)) for a, b in CLS)
        if strict < 3:
            diff[d] += 1
print('admissible z=4 shapes with < 3 corner (cvx/rfx) classes, by d:', sorted(diff.items()),
      'total', sum(diff.values()))
