"""d69: the midpoint lemma on data.  For a same-class pair, every lighting path passes a lattice
point at its midpoint.  An x-monotone path crosses x = (s1 + t1)/2 once, at a lattice point that
is interior or a smooth point of a horizontal wall.  If the line x = m0 has no such point, the
family X is empty (midline obstruction).  This script counts, over all pairs where X fails
(decomp.py verdicts), how many the obstruction explains, and checks that the obstruction never
fires on a pair that X lights (soundness).  Same for Y.
Usage: python3 -B midline.py
"""
import json
import sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
import decomp  # noqa: E402
from decomp import status  # noqa: E402


def blocked(cells, S, T, axis):
    if axis == 0:
        cells = {(j, i) for i, j in cells}
        S, T = (S[1], S[0]), (T[1], T[0])
    if S[0] == T[0]:
        return None
    m0 = (S[0] + T[0]) // 2
    ys = {c[1] for c in cells if c[0] in (m0 - 1, m0)}
    for y in range(min(ys), max(ys) + 2):
        st = status(cells, (m0, y))
        if st == 'interior':
            return False
        if st == 'smooth' and (((m0 - 1, y) in cells and (m0, y) in cells) or
                               ((m0 - 1, y - 1) in cells and (m0, y - 1) in cells)):
            return False
    return True


if __name__ == '__main__':
    named = decomp.cells_of(None)
    hb = decomp.handbuilt()
    cov = [r for r in json.load(open(decomp.D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
           if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))
    rooms = list(named.items()) + list(hb.items()) + [('cov%d' % i, set(map(tuple, r['cells'])))
                                                      for i, r in enumerate(cov)]
    c = Counter()
    for name, cells in rooms:
        for S, T in decomp.same_class_pairs(cells):
            if decomp.visible(cells, S, T):
                continue
            for axis, lab in ((1, 'X'), (0, 'Y')):
                b = blocked(cells, S, T, axis)
                if b is None:
                    continue
                lit = decomp.monotone(cells, S, T, axis, 3000)
                c[(lab, 'lit' if lit else 'fails', 'midline-blocked' if b else 'not-blocked')] += 1
                if b and lit:
                    print('SOUNDNESS FAILURE', name, S, T, lab)
    for k, v in sorted(c.items()):
        print(k, v)
