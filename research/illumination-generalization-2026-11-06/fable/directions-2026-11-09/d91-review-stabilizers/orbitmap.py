"""Physical picture of H-orbits on the cross. Run: python3 -B orbitmap.py R b"""
import sys
from math import gcd
import many
from origami import (Surface, cross_cells, apply_word, to_horizontal, cylinders, shearT,
                     descend, qperm, orbits, dedupe, lcm, divisors)


def hgroup(S, R, qpts, qidx):
    gens = []
    dirs = [(p, q) for p in range(0, R + 1) for q in range(-R, R + 1)
            if gcd(p, q) == 1 and (p > 0 or q == 1)]
    for d in dirs:
        r, u = apply_word(S.r, S.u, to_horizontal(*d))
        lam = 1
        for c, h, _ in cylinders(S, r, u):
            lam = lcm(lam, c // gcd(c, h))
        for dd in divisors(lam):
            ms = [vm for phi in many.isos_marked(S, *shearT(r, u, dd), r, u)
                  for vm in [descend(S, phi)] if vm is not None]
            if ms:
                gens += [qperm(S, vm, qpts, qidx) for vm in ms]
                break
    for phi in many.isos_marked(S, S.r, S.u, S.r, S.u):
        vm = descend(S, phi)
        if vm is not None:
            gens.append(qperm(S, vm, qpts, qidx))
    return dedupe(gens), len(dirs)


R, b = int(sys.argv[1]), int(sys.argv[2])
S = Surface(cross_cells(b))
qpts = sorted({S.qpoint(v) for v in S.verts})
qidx = {v: k for k, v in enumerate(qpts)}
gens, nd = hgroup(S, R, qpts, qidx)
orb = orbits(len(qpts), gens)
print(f'cross b={b}, {nd} directions (R={R}); orbit sizes with multiplicity:',
      sorted((len(o) for o in orb), reverse=True))
size = {}
for o in orb:
    for k in o:
        p = qpts[k][0]
        size[p] = max(size.get(p, 0), len(o))
for y in range(b, -b - 1, -1):
    row = ''
    for x in range(-b, b + 1):
        row += f'{size[(x, y)]:4d}' if (x, y) in size else '    '
    print(row)
