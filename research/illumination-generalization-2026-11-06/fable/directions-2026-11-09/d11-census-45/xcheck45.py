"""Cross-check of star-growth enumeration against plain enumeration.

Plain mode lists every free strictly simple room with W <= WMAX and an eligible
class.  This script recomputes, in Python, the interior points of each plain
room, splits the rooms into "has an A/B pair" and "has a C pair", and compares
those sets with the union of the star-mode (A/B) and cstar-mode (C) outputs.

usage: python3 -B xcheck45.py NMIN NMAX plain_files... -- star_files... -- cstar_files...
"""
import sys
from collections import Counter

import rooms45 as R


def read(files, nmin, nmax):
    out = set()
    for f in files:
        for line in open(f):
            p = line.split()
            if p and nmin <= int(p[0]) <= nmax:
                out.add(' '.join(p))
    return out


def classes(line):
    p = list(map(int, line.split()))
    tiles = [tuple(p[2 + 3 * a:5 + 3 * a]) for a in range(p[0])]
    cnt = Counter(v for t in tiles for v in R.tile_verts(*t))
    c = Counter()
    for (x, y), m in cnt.items():
        cl = 2 if (x + y) % 2 else (x % 2)
        if m == (4 if cl == 2 else 8):
            c[cl] += 1
    return c


def main():
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    rest = ' '.join(sys.argv[3:]).split(' -- ')
    plain = read(rest[0].split(), nmin, nmax)
    star = read(rest[1].split(), nmin, nmax)
    cstar = read(rest[2].split(), nmin, nmax)
    ab, cc = set(), set()
    for line in plain:
        c = classes(line)
        if c[0] >= 2 or c[1] >= 2:
            ab.add(line)
        if c[2] >= 2:
            cc.add(line)
    print('N range %d..%d' % (nmin, nmax))
    print('plain rooms %d, with A/B pair %d, with C pair %d' % (len(plain), len(ab), len(cc)))
    print('star rooms %d, cstar rooms %d' % (len(star), len(cstar)))
    print('A/B: plain-only %d, star-only %d' % (len(ab - star), len(star - ab)))
    print('C:   plain-only %d, cstar-only %d' % (len(cc - cstar), len(cstar - cc)))
    print('per N (plain A/B, star, plain C, cstar):')
    for n in range(nmin, nmax + 1):
        f = lambda s: sum(1 for x in s if int(x.split()[0]) == n)  # noqa
        print('  N %2d  %8d %8d  %8d %8d' % (n, f(ab), f(star), f(cc), f(cstar)))
    ok = ab == star and cc == cstar
    print('MATCH' if ok else 'MISMATCH')


if __name__ == '__main__':
    main()
