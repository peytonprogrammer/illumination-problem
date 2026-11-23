"""d74: pole test (Proposition O / O' of d13 theory) for named rooms.  Usage: python3 -B poles.py ROOMFILE INDEX B
For convex corner c: D(c) = label of every band of c's cell whose closure contains c (checked equal).
For flat boundary point f: A(f) = labels of bands of f's two cells whose closure contains f.
Reports pole pairs that share no cylinder for every direction (p, q), 1 <= p, q <= B."""
import sys
from fractions import Fraction as F
from geom import Direction, read_rooms, pt_kind, dirs


def touching(D, c, pt):
    x, y = pt
    out = set()
    for fam in (0, 1):
        k = D.tval(fam, x, y)
        lo, hi = D.rng(c, fam)
        for K in (k - 1, k):
            if lo <= K < hi:
                out.add(D.label[(c, fam, 2 * K + 1)])
    return out


def poles(cs):
    pts = {(i + dx, j + dy) for (i, j) in cs for dx in (0, 1) for dy in (0, 1)}
    cv = sorted(p for p in pts if pt_kind(cs, *p) == 'cvx')
    fl = sorted(p for p in pts if pt_kind(cs, *p) == 'flat')
    return cv, fl


def cells_at(cs, p):
    x, y = p
    return [c for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cs]


if __name__ == '__main__':
    cs = read_rooms(sys.argv[1])[int(sys.argv[2])]
    B = int(sys.argv[3])
    cv, fl = poles(cs)
    shared = {}
    for (p, q) in dirs(B):
        D = Direction(cs, p, q)
        lab = {}
        for c in cv:
            s = set()
            for cell in cells_at(cs, c):
                s |= touching(D, cell, c)
            assert len(s) == 1, ('pole not single cylinder', c, p, q, s)
            lab[c] = s
        for f in fl:
            s = set()
            for cell in cells_at(cs, f):
                s |= touching(D, cell, f)
            lab[f] = s
        allp = cv + fl
        for i, a in enumerate(allp):
            for b in allp[i + 1:]:
                if a in fl and b in fl:
                    continue
                if lab[a] & lab[b]:
                    shared.setdefault((a, b), (p, q))
    allp = cv + fl
    bad = [(a, b) for i, a in enumerate(allp) for b in allp[i + 1:]
           if not (a in fl and b in fl) and (a, b) not in shared]
    print('convex', cv)
    print('flat', fl)
    print('pole pairs with no common cylinder for p,q <= %d: %d' % (B, len(bad)))
    for a, b in bad:
        print('  ', a, b)
