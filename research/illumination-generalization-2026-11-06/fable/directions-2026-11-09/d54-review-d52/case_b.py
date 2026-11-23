"""d54 sketch: replace d2 claim 4 inside F* by a small enumeration (the "Galois branch").

Case B: all three target classes have delta_y <= 2. Then every phi_y is Galois, d36.3 makes
B_b, B_c, B_d a chain, and the coarsest one, B_*, separates and has no regular point over any
of the three target classes, with delta_* <= 2. Put the marks' class at a = (1, 1). Then
K_* = P / B_* is a genus-0 W-set whose classes 00, 10, 01 have only cvx, rfx, cone orbits.
Summing d = cvx_j + 3 rfx_j + 2 cone_j over those three classes gives 3d <= p + 3z = 4z + 4, and
delta_* z <= r <= 8. So (delta_* = 1) z <= 8, d <= 12, P = K_*; (delta_* = 2) z <= 4, d <= 6.
This script enumerates every such K_* and every degree-1 or -2 W-set cover of it with room-local
orbit types and r <= 8, and runs the positivity test on each in-scope cover.
Usage: python3 -B case_b.py [RMAX (default 8)]
"""
import resource
import sys
import time
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fold import *  # noqa
from validate_generic import generic_covers  # noqa  (sets CPU limits on import; keep this order)
from checks import indep_positive  # noqa
import enum_K  # noqa

resource.setrlimit(resource.RLIMIT_CPU, (300, resource.getrlimit(resource.RLIMIT_CPU)[1]))
A = (1, 1)
enum_K.ALLOWED = {cls: ({'cvx', 'rfx', 'cone'} if cls != A else enum_K.ALL) for cls in CLASSES}
P_TYPES = {'cvx', 'smooth', 'rfx', 'int'}

if __name__ == '__main__':
    t0 = time.process_time()
    rmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    dmax1, z2, = (4 * rmax + 4) // 3, rmax // 2
    dmax2 = (4 * z2 + 4) // 3
    found, nodes = enum_K.enumerate_K(rmax, dmax1)
    print('rmax', rmax, 'genus-0 K_* (classes 00,10,01 without regular points), z <=', rmax,
          'd <=', dmax1, ':', len(found),
          'nodes', nodes, 'CPU %.1f' % (time.process_time() - t0), flush=True)
    st = Counter()
    for key, k in found.items():
        K = [list(r) for r in key]
        st['K_d=%d' % k['d']] += 1
        # delta_* = 1: P = K_*
        prof = profile(K)
        if all(t in P_TYPES for ts in prof.values() for t in ts):
            ncls = len([c for c, ts in prof.items() if 'cvx' in ts or 'rfx' in ts])
            st['delta1_rooms'] += 1
            if ncls >= 3:
                st['delta1_in_scope'] += 1
                st['delta1_true_room'] += is_room(K)
                st['delta1_with_A_pair'] += len(interior_points(K, A)) >= 2
                p1, p2 = positives(K)[0], indep_positive(K)
                st['delta1_positive'] += bool(p1)
                st['delta1_positive_indep'] += bool(p2)
        # delta_* = 2
        if k['z'] <= z2 and k['d'] <= dmax2:
            for P in generic_covers(K, 2, rmax).values():
                pr = profile(P)
                ncls = len([c for c, ts in pr.items() if 'cvx' in ts or 'rfx' in ts])
                st['delta2_covers'] += 1
                if ncls >= 3:
                    st['delta2_in_scope'] += 1
                    st['delta2_with_A_pair'] += len(interior_points(P, A)) >= 2
                    st['delta2_positive'] += bool(positives(P)[0])
                    st['delta2_positive_indep'] += bool(indep_positive(P))
    print(dict(sorted(st.items())))
    print('CPU s %.1f' % (time.process_time() - t0))
