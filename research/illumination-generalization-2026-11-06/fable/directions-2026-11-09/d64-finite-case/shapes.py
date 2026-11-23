"""d64 step 1: admissible quotient shapes K_x (x = (0,0)) for RL-fin at r <= RMAX.

Input: enum_K.c output (all genus-0 shapes, z <= zmax, d <= dmax).
Admissible (README section 2): z >= 1; singular orbits in >= 3 classes; some delta >= 2 with
delta * z <= RMAX (delta even if K has a cone). Asserts d <= 4z + 2 on every admissible shape
(so the d <= 18 search bound is not binding).
Usage: python3 -B shapes.py K.txt RMAX out.json
"""
import json
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd52-fold-enumeration'))
from fold import profile, summary  # noqa: E402
from kload import load_txt  # noqa: E402


def deltas(z, cone, rmax):
    return [dl for dl in range(2, rmax + 1) if dl * z <= rmax and (cone == 0 or dl % 2 == 0)]


if __name__ == '__main__':
    forms = load_txt(sys.argv[1])
    rmax = int(sys.argv[2])
    keep, rej = [], Counter()
    for f in forms:
        K = [list(r) for r in f]
        prof = profile(K)
        s = summary(prof)
        assert s['genus0']
        dl = deltas(s['z'], s['cone'], rmax)
        why = []
        if s['z'] < 1:
            why.append('z0')
        if len(s['sing']) < 3:
            why.append('sing<3')
        if not dl:
            why.append('no_delta')
        if why:
            rej[tuple(why)] += 1
            continue
        assert len(K[0]) <= 4 * s['z'] + 2, f
        keep.append(dict(canon=[list(r) for r in f], d=len(K[0]), z=s['z'], cone=s['cone'],
                         deltas=dl, types={'%d%d' % c: sorted(t) for c, t in prof.items()}))
    keep.sort(key=lambda k: (k['z'], k['d'], k['canon']))
    print('shapes read', len(forms), 'rejected', dict(rej), 'admissible', len(keep))
    print('admissible by (z, cone):', sorted(Counter((k['z'], k['cone']) for k in keep).items()))
    print('admissible by (z, d):', sorted(Counter((k['z'], k['d']) for k in keep).items()))
    cases = Counter((k['z'], dl) for k in keep for dl in k['deltas'])
    print('(K, delta) cases by (z, delta):', sorted(cases.items()), 'total', sum(cases.values()))
    json.dump(keep, open(sys.argv[3], 'w'))
