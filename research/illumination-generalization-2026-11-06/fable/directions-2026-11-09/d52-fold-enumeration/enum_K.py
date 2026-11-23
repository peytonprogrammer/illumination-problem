"""d52 step 2: enumerate candidate class quotients N_x = DP / B_x as W-sets K (the fold target
K = N_x / iota, d cells), with the target class fixed to x = (0, 0) by the square symmetries.

Constraints imposed during the search (see memo section 1):
  * every <V_i, H_j>-orbit is cvx, smooth, rfx, cone or int (Fact L; zeros on the seam);
  * class x has no regular point: its orbits are cvx, rfx or cone only (Par(x));
  * at most zmax zeros (rfx), at most one cone, at most zmax + 4 poles;
  * d <= dmax.
At the leaf: transitive (by construction), genus 0 (p = z + 4).
Usage: python3 -B enum_K.py zmax dmax out.json
"""
import json
import resource
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fold import *  # noqa

resource.setrlimit(resource.RLIMIT_CPU, (900, 900))
X = (0, 0)
ALL = {'cvx', 'smooth', 'rfx', 'cone', 'int'}
ALLOWED = {cls: ({'cvx', 'rfx', 'cone'} if cls == X else ALL) for cls in CLASSES}
CLS_OF_GEN = {0: [(0, 0), (0, 1)], 1: [(1, 0), (1, 1)], 2: [(0, 0), (1, 0)], 3: [(0, 1), (1, 1)]}


def counts_ok(G, n, zmax):
    z = cone = cvx = 0
    for cls in CLASSES:
        a, b = cg(cls)
        seen = set()
        for c in range(n):
            if c in seen:
                continue
            cells, kind = trace(G, a, b, c)
            seen.update(cells)
            t = orbit_type(cells, kind)
            if t == 'rfx':
                z += 1
            elif t == 'cone':
                cone += 1
            elif t == 'cvx':
                cvx += 1
    return z <= zmax and cone <= 1 and cvx + 2 * cone <= zmax + 4


def local_ok(G, cells_touched, g):
    for cls in CLS_OF_GEN[g]:
        a, b = cg(cls)
        for c in cells_touched:
            cl, kind = trace(G, a, b, c)
            if not partial_ok(cl, kind, ALLOWED[cls]):
                return False
    return True


def enumerate_K(zmax, dmax):
    G = [[-1] * dmax for _ in range(4)]
    found = {}
    nodes = [0]

    def rec(n, ptr):
        nodes[0] += 1
        # next undefined slot
        while ptr < 4 * n and G[ptr % 4][ptr // 4] != -1:
            ptr += 1
        if ptr == 4 * n:
            K = [row[:n] for row in G]
            prof = profile(K)
            if prof is None:
                return
            s = summary(prof)
            if not s['genus0']:
                return
            key = canon(K)
            if key not in found:
                found[key] = dict(d=n, z=s['z'], cone=s['cone'], p=s['p'],
                                  sing=[list(c) for c in s['sing']],
                                  types={'%d%d' % c: sorted(t) for c, t in prof.items()})
            return
        c, g = ptr // 4, ptr % 4
        # option 1: wall (fixed)
        G[g][c] = c
        if local_ok(G, [c], g) and counts_ok(G, n, zmax):
            rec(n, ptr + 1)
        G[g][c] = -1
        # option 2: glue to an existing cell with free g-slot
        for c2 in range(c + 1, n):
            if G[g][c2] == -1:
                G[g][c] = c2
                G[g][c2] = c
                if local_ok(G, [c, c2], g) and counts_ok(G, n, zmax):
                    rec(n, ptr + 1)
                G[g][c] = -1
                G[g][c2] = -1
        # option 3: new cell
        if n < dmax:
            G[g][c] = n
            G[g][n] = c
            if local_ok(G, [c, n], g) and counts_ok(G, n + 1, zmax):
                rec(n + 1, ptr + 1)
            G[g][c] = -1
            G[g][n] = -1

    rec(1, 0)
    return found, nodes[0]


if __name__ == '__main__':
    zmax, dmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    t0 = time.process_time()
    found, nodes = enumerate_K(zmax, dmax)
    recs = [dict(canon=k, **v) for k, v in sorted(found.items(), key=lambda kv: (kv[1]['d'], kv[0]))]
    json.dump(recs, open(out, 'w'))
    print('zmax', zmax, 'dmax', dmax, 'genus-0 K (x = (0,0) has no regular point):', len(recs),
          'search nodes', nodes, 'CPU s', round(time.process_time() - t0, 1))
