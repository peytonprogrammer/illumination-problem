"""Independent small-area enumerator of strictly simple polyomino rooms.

Grows fixed polyominoes cell by cell (set-based, no Redelmeier), canonicalises
over the 8 symmetries by sorted-tuple minimum, then filters holes by flood fill,
pinches by diagonal-pair test, and counts walls as maximal collinear runs of
boundary unit edges (not by corner parity).
"""
from collections import Counter
import sys

SYMS = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (-x, -y),
        lambda x, y: (y, x), lambda x, y: (-y, x), lambda x, y: (y, -x), lambda x, y: (-y, -x)]

def norm(cells):
    mx = min(x for x, y in cells); my = min(y for x, y in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))

def canon(cells):
    return min(norm([f(x, y) for x, y in cells]) for f in SYMS)

def free_polyominoes(nmax):
    level = {((0, 0),)}
    out = {1: level}
    for n in range(2, nmax + 1):
        nxt = set()
        for p in level:
            s = set(p)
            for x, y in p:
                for c in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if c not in s:
                        nxt.add(canon(p + (c,)))
        level = nxt
        out[n] = level
    return out

def has_hole(cells):
    s = set(cells)
    X = max(x for x, y in s) + 2; Y = max(y for x, y in s) + 2
    seen = {(-1, -1)}; st = [(-1, -1)]
    while st:
        x, y = st.pop()
        for c in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if -1 <= c[0] <= X and -1 <= c[1] <= Y and c not in s and c not in seen:
                seen.add(c); st.append(c)
    return (X + 2) * (Y + 2) - len(seen) != len(s)

def has_pinch(s):
    pts = {(x+i, y+j) for x, y in s for i in (0, 1) for j in (0, 1)}
    for px, py in pts:
        ll, lr, ul, ur = (px-1, py-1) in s, (px, py-1) in s, (px-1, py) in s, (px, py) in s
        if ll + lr + ul + ur == 2 and ((ll and ur) or (lr and ul)):
            return True
    return False

def walls(s):
    # boundary unit edges: horizontal edge (x,y)-(x+1,y), vertical (x,y)-(x,y+1)
    hor = set()
    ver = set()
    for x, y in s:
        if (x, y-1) not in s: hor.add((x, y))
        if (x, y+1) not in s: hor.add((x, y+1))
        if (x-1, y) not in s: ver.add((x, y))
        if (x+1, y) not in s: ver.add((x+1, y))
    # maximal runs: an edge starts a run if its predecessor on the same line is absent
    return sum((x-1, y) not in hor for x, y in hor) + sum((x, y-1) not in ver for x, y in ver)

def marks(s):
    return [(x, y) for x, y in {(x+1, y+1) for x, y in s}
            if {(x-1, y-1), (x, y-1), (x-1, y), (x, y)} <= s]

def rooms(nmax):
    for n, polys in free_polyominoes(nmax).items():
        for p in polys:
            s = set(p)
            if has_hole(p) or has_pinch(s):
                continue
            yield n, p, walls(s), marks(s)

if __name__ == '__main__':
    nmax = int(sys.argv[1])
    tab = Counter(); same = Counter(); diff = Counter(); free = Counter()
    for n, polys in free_polyominoes(nmax).items():
        free[n] = len(polys)
    for n, p, w, m in rooms(nmax):
        if w > 20: continue
        tab[n, w] += 1
        for i in range(len(m)):
            for j in range(i+1, len(m)):
                d = ((m[i][0] ^ m[j][0]) | (m[i][1] ^ m[j][1])) & 1
                (diff if d else same)[n, w] += 1
    print('FREE', dict(free))
    for k in sorted(tab):
        print('ROW', k[0], k[1], tab[k], same[k], diff[k])
