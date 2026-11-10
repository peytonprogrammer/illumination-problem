#!/usr/bin/env python3
"""Finite strip certificates for the two directions in manuscript.tex.

Standard-library Python only. Square order: sorted cell, then SHEETS order.
Slot q*i+j is the bottom-edge interval (j/q,(j+1)/q) in square i.
The output contains every permutation cycle, so it can be checked separately.
This verifies the finite inputs; the manuscript proves their implication for
all distinct real interior points.
"""
import json
from pathlib import Path

SHEETS = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
BASE = {(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)}


def certificate():
    cells = BASE | {(a, -b - 1) for a, b in BASE} | {(3-a, -b-1) for a, b in BASE}
    squares = [(c, e) for c in sorted(cells) for e in SHEETS]
    index = {s: i for i, s in enumerate(squares)}
    right, up = [], []
    for (a, b), (ex, ey) in squares:
        right.append(index[((a+ex, b), (ex, ey))] if (a+ex, b) in cells
                     else index[((a, b), (-ex, ey))])
        up.append(index[((a, b+ey), (ex, ey))] if (a, b+ey) in cells
                  else index[((a, b), (ex, -ey))])
    assert len(cells) == 15 and len(squares) == 60
    assert sorted(right) == sorted(up) == list(range(60))
    lattice = {(x, y) for a, b in cells for x in (a, a+1) for y in (b, b+1)}
    interior = sorted((x, y) for x, y in lattice
                      if all((a, b) in cells for a in (x-1, x) for b in (y-1, y)))
    assert interior == [(0, 0), (2, 2)]
    directions = []
    for p, q in [(4, 7), (7, 4)]:
        perm = []
        for i in range(60):
            for j in range(q):
                k = i
                for _ in range((j+p)//q):
                    k = right[k]
                perm.append(q*up[k] + (j+p) % q)
        assert sorted(perm) == list(range(60*q))
        unseen = set(range(60*q))
        cycles = []
        while unseen:
            first = min(unseen)
            cycle, cur = [], first
            while cur in unseen:
                unseen.remove(cur)
                cycle.append(cur)
                cur = perm[cur]
            assert cur == first
            cycles.append(cycle)
        assert len(cycles) == 2
        # First return to residue j=0: exactly q steps because gcd(p,q)=1.
        return_map = []
        for i in range(60):
            cur = q*i
            for _ in range(q):
                cur = perm[cur]
            assert cur % q == 0
            return_map.append(cur // q)
        return_cycles = []
        unseen_return = set(range(60))
        while unseen_return:
            first = min(unseen_return)
            cycle, cur = [], first
            while cur in unseen_return:
                unseen_return.remove(cur)
                cycle.append(cur)
                cur = return_map[cur]
            assert cur == first
            return_cycles.append(cycle)
        assert [len(c) for c in return_cycles] == [30, 30]
        directions.append({'p': p, 'q': q, 'slots': 60*q,
                           'cycle_lengths': [len(c) for c in cycles], 'cycles': cycles,
                           'return_map': return_map, 'return_cycles': return_cycles})
    return {'cells': sorted(cells), 'sheets': SHEETS, 'right': right, 'up': up,
            'interior_lattice_points': interior, 'directions': directions}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare with included certificate.json')
    args = parser.parse_args()
    result = certificate()
    if args.check:
        normalized = json.loads(json.dumps(result))
        assert normalized == json.loads(Path(__file__).with_name('certificate.json').read_text())
        print('PASS: two strip cycles in each direction; interior lattice points (0,0), (2,2).')
    else:
        print(json.dumps(result, indent=2))
