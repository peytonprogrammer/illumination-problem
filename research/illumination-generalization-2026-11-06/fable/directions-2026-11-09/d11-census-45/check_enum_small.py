"""Independent brute-force check of enum45 (plain mode) at small sizes.

Shares no code with enum45.c.  A tile is a frozenset of its 3 vertices.  The
neighbour across an edge is the mirror image of the tile in that edge (the
canonical45 tiling is a reflection tiling).  Animals are grown level by level
as sets, normalised by the translation group L = {(a,b): a+b even}.  Strict
simplicity and W come from a boundary-cycle walk.

usage: python3 check_enum_small.py NMAX enum45_counts_file
"""
import sys
from collections import Counter


def reflect(p, a, b):
    """Mirror image of lattice point p in the line through a, b (exact)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    px, py = p[0] - a[0], p[1] - a[1]
    dd = dx * dx + dy * dy
    t2 = 2 * (px * dx + py * dy)
    assert t2 % dd == 0
    k = t2 // dd
    return (a[0] + k * dx - px, a[1] + k * dy - py)


def neighbours(t):
    v = sorted(t)
    out = []
    for i in range(3):
        a, b, c = v[i], v[(i + 1) % 3], v[(i + 2) % 3]
        out.append(frozenset((a, b, reflect(c, a, b))))
    return out


def norm(S):
    vs = [p for t in S for p in t]
    mx = min(vs, key=lambda p: (p[1], p[0]))
    dx, dy = -mx[0], -mx[1]
    if (dx + dy) % 2:
        dx += 1
    return frozenset(frozenset((x + dx, y + dy) for x, y in t) for t in S)


MATS = [(1, 0, 0, 1), (0, -1, 1, 0), (-1, 0, 0, -1), (0, 1, -1, 0),
        (1, 0, 0, -1), (-1, 0, 0, 1), (0, 1, 1, 0), (0, -1, -1, 0)]


def key(S):
    return tuple(sorted(tuple(sorted(t)) for t in S))


def canon(S):
    best = None
    for a, b, c, d in MATS:
        img = norm(frozenset(frozenset((a * x + b * y, c * x + d * y) for x, y in t) for t in S))
        k = key(img)
        if best is None or k < best:
            best = k
    return best


def boundary_info(S):
    """(strictly_simple, W, interior points)."""
    ec = Counter()
    for t in S:
        v = sorted(t)
        for i in range(3):
            ec[frozenset((v[i], v[(i + 1) % 3]))] += 1
    bnd = [e for e, c in ec.items() if c == 1]
    inc = {}
    for e in bnd:
        for p in e:
            inc.setdefault(p, []).append(e)
    verts = {p for t in S for p in t}
    interior = sorted(p for p in verts if p not in inc)
    if any(len(es) != 2 for es in inc.values()):
        return False, None, interior
    # single cycle?
    start = next(iter(inc))
    prev, cur, steps = None, start, 0
    e = inc[start][0]
    while True:
        nxt = next(p for p in e if p != cur)
        steps += 1
        cur = nxt
        if cur == start:
            break
        e = inc[cur][0] if inc[cur][1] == e else inc[cur][1]
    if steps != len(bnd):
        return False, None, interior
    W = 0
    for p, (e1, e2) in inc.items():
        q1 = next(q for q in e1 if q != p)
        q2 = next(q for q in e2 if q != p)
        if (q1[0] - p[0]) * (q2[1] - p[1]) - (q1[1] - p[1]) * (q2[0] - p[0]) != 0:
            W += 1
    return True, W, interior


def cls(p):
    return 'A' if p[0] % 2 == 0 and p[1] % 2 == 0 else 'B' if p[0] % 2 and p[1] % 2 else 'C'


def main():
    nmax = int(sys.argv[1])
    t0 = frozenset(((0, 0), (1, 0), (1, 1)))
    # the four L-orbits of tiles: start from all four to get every animal
    starts = {norm(frozenset([t])) for t in [t0] + neighbours(t0) + [n2 for n1 in neighbours(t0) for n2 in neighbours(n1)]}
    level = set(starts)
    fixed, free, rooms, elig = Counter(), Counter(), Counter(), Counter()
    for n in range(1, nmax + 1):
        if n > 1:
            nxt = set()
            for S in level:
                for t in S:
                    for u in neighbours(t):
                        if u not in S:
                            nxt.add(norm(S | {u}))
            level = nxt
        fixed[n] = len(level)
        cs = {}
        for S in level:
            cs.setdefault(canon(S), S)
        free[n] = len(cs)
        for S in cs.values():
            ok, W, inter = boundary_info(S)
            if ok:
                rooms[(n, W)] += 1
                c = Counter(cls(p) for p in inter)
                if max(c.values(), default=0) >= 2:
                    elig[(n, W)] += 1
        print('n', n, 'fixed', fixed[n], 'free', free[n], flush=True)
    # compare with enum45 counts
    cf, cfree, cr, ce = Counter(), Counter(), Counter(), Counter()
    for line in open(sys.argv[2]):
        p = line.split()
        if p[0] == 'fixed':
            cf[int(p[1])] = int(p[2]); cfree[int(p[1])] = int(p[4])
        elif p[0] == 'rooms':
            cr[(int(p[1]), int(p[2]))] = int(p[3]); ce[(int(p[1]), int(p[2]))] = int(p[5])
    ce = Counter({k: v for k, v in ce.items() if v})
    print('fixed match', all(cf[n] == fixed[n] for n in range(1, nmax + 1)))
    print('free match', all(cfree[n] == free[n] for n in range(1, nmax + 1)))
    print('rooms per (n,W) match', {k: v for k, v in cr.items() if k[0] <= nmax} == dict(rooms))
    print('eligible per (n,W) match', {k: v for k, v in ce.items() if k[0] <= nmax} == dict(elig))
    print('free counts', [free[n] for n in range(1, nmax + 1)])
    print('strictly simple rooms', [sum(v for k, v in rooms.items() if k[0] == n) for n in range(1, nmax + 1)])


if __name__ == '__main__':
    main()
