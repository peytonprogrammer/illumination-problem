"""d69: soundness check of family B.  For every pair that decomp.py lights by B (hand-built rooms
and d64 rooms), fold the B witness back to the room and trace it with no restriction on flips
(decomp.trace, cross-checked against d66 shoot in crosscheck.py).  Mover T: from S with the same
direction.  Mover S: from S with the initial direction mirrored in the glued line.
Usage: python3 -B verify_b.py
"""
import json
import decomp

d = json.load(open(decomp.HERE / 'decomp.json'))
hb = decomp.handbuilt()
cov = [r for r in json.load(open(decomp.D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
       if r['normalized']]
cov.sort(key=lambda r: (r['n'], r['cells']))
ok = bad = 0
for name, cells in list(hb.items()) + [('cov%d' % i, set(map(tuple, r['cells']))) for i, r in enumerate(cov)]:
    for S, T in decomp.same_class_pairs(cells):
        if decomp.visible(cells, S, T) or decomp.monotone(cells, S, T, 1, 3000) or \
                decomp.monotone(cells, S, T, 0, 3000):
            continue
        w = []
        if not decomp.backwall(cells, S, T, 3000, w):
            continue
        axis, mover, (p, q, sx, sy, g) = w[0]
        if mover == 'S':
            sx = -sx                       # mirror the initial direction in the glued line
        if axis == 0:
            p, q, sx, sy = q, p, sy, sx
        lim = 8 * len(decomp.lattice_points(cells)) + 8
        good = decomp.trace(cells, S, T, p, q, sx, sy, lim, set())
        ok += good
        bad += not good
        if not good:
            print('B witness FAILS', name, S, T, w)
print('B witnesses verified', ok, 'failed', bad)
