"""d69: which residual pairs (not lit by V, X, Y, B in decomp.py) are swapped by a symmetry of
the room (one of the 7 non-identity maps of D4 that preserve the cell set)?
Usage: python3 -B symcheck.py      (reads decomp.json)
"""
import json
from collections import Counter
import decomp

MAPS = {'rot90': lambda x, y: (-y, x), 'rot180': lambda x, y: (-x, -y), 'rot270': lambda x, y: (y, -x),
        'mirror_x': lambda x, y: (-x, y), 'mirror_y': lambda x, y: (x, -y),
        'diag': lambda x, y: (y, x), 'antidiag': lambda x, y: (-y, -x)}


def pts(cells):
    return {(x, y) for c in cells for x in (c[0], c[0] + 1) for y in (c[1], c[1] + 1)}


def swapping(cells, S, T):
    P = pts(cells)
    out = []
    for name, f in MAPS.items():
        img = {f(*p) for p in P}
        # translate so the images coincide
        dx = min(p[0] for p in P) - min(p[0] for p in img)
        dy = min(p[1] for p in P) - min(p[1] for p in img)
        g = lambda x, y, f=f, dx=dx, dy=dy: (f(x, y)[0] + dx, f(x, y)[1] + dy)
        cimg = set()
        for (i, j) in cells:
            corners = [g(i, j), g(i + 1, j), g(i, j + 1), g(i + 1, j + 1)]
            cimg.add((min(c[0] for c in corners), min(c[1] for c in corners)))
        if cimg == cells and g(*S) == tuple(T):
            out.append(name)
    return out


if __name__ == '__main__':
    d = json.load(open(decomp.HERE / 'decomp.json'))
    named = decomp.cells_of(None)
    cov = [r for r in json.load(open(decomp.D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms']
           if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))
    c = Counter()
    for r in d['residual']:
        name = r['room']
        cells = named[name] if name in named else set(map(tuple, cov[int(name[3:])]['cells']))
        sw = swapping(cells, tuple(r['S']), tuple(r['T']))
        c[('area>=21' if r['n'] >= 21 else 'area<=20', tuple(sw) if sw else 'asymmetric')] += 1
        if not sw:
            print('asymmetric residual', name, r['n'], r['S'], r['T'])
    for k, v in sorted(c.items(), key=str):
        print(k, v)
