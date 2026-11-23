"""Refine the d6 involution flag: split "interior cone point or overlap" into its two cases.

Saved data only (d6 summary.json, n <= 10).  For each counterexample family, each tuple of
its plain braid orbit and each lift iota of the seam reflection:

  rp2            iota has no fixed point;
  interior_cone  a pole or zero of Q is not fixed by iota, so Q / iota is not a polygon;
  immersed       every pole and zero is on the fixed circle, so Q / iota is a flat disc with
                 all corners on its boundary, but its development overlaps (not embedded);
  planar         an embedded lattice polygon.

An "immersed" hit would be an orthogonal room that overlaps itself: it would show that
embeddedness is the only planar hypothesis that excludes the mechanism.
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
sys.path.insert(0, str(D6))
from hurwitz import cycles, decode, plain_orbit          # noqa: E402
import involution_flag as F                              # noqa: E402


def classify(t, phi):
    """Back tiles carry the label of the front tile across the bottom edge (d6 convention).
    The back tiles around a point over a or b are B_i, i in its cycle C; over c or d they
    are B_T(i).  The point is fixed by iota iff phi maps that back set onto C."""
    status, cells = F.develop(t, phi)
    if status == 'no_fixed_points_RP2':
        return 'rp2'
    T = F.edge_maps(t)['top']
    cone = False
    for y, g in enumerate(t):
        for c in cycles(g):
            back = c if y < 2 else [T[i] for i in c]
            if len(c) != 2 and sorted(phi[j] for j in back) != sorted(c):
                cone = True
    if cone:
        return 'interior_cone'
    # no interior cone point: the development of the disc is well defined
    assert status != 'interior_cone_point_or_overlap', status
    return 'planar' if status in ('planar_polygon', 'planar_with_slits') else 'immersed'


def main():
    summary = json.loads((D6 / 'summary.json').read_text())
    total = Counter()
    for n, fams in summary['counterexample_families'].items():
        for f in fams:
            t = tuple(tuple(g) for g in f['representative']['rep'])
            c = Counter()
            for enc in sorted(plain_orbit(t)):
                tt, _ = decode(enc, int(n), False)
                refl = F.reflections(tt)
                if not refl:
                    c['no reflection lift'] += 1
                for phi in refl:
                    c[classify(tt, phi)] += 1
            total.update(c)
            print(n, f['nielsen_class_up_to_bcd'], '|', f['mechanism'][:40], '|', dict(c))
    print('total', dict(total))


if __name__ == '__main__':
    main()
