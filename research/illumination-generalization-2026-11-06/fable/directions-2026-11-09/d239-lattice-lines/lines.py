"""Lattice lines in an orthogonal lattice room given as a set of unit cells (x, y) = [x,x+1] x [y,y+1].
From an interior lattice point, follow a primitive direction one primitive step at a time.
Stop at a corner. Reflect at a wall point. Record interior lattice points reached, with the step count."""
from math import gcd

def kind(cells, x, y):
    c = [(x - 1, y - 1) in cells, (x, y - 1) in cells, (x - 1, y) in cells, (x, y) in cells]  # SW SE NW NE
    n = sum(c)
    if n == 4: return 'I'
    if n == 2:
        if c[0] and c[2] or c[1] and c[3]: return 'V'   # both west or both east: vertical wall
        if c[0] and c[1] or c[2] and c[3]: return 'H'
    return 'C'

def step(cells, x, y, sx, sy, P, Q):
    """One primitive step from lattice point (x, y), velocity (sx*P, sy*Q). Returns the end point and signs."""
    if Q == 0: return x + sx, y, sx, sy
    if P == 0: return x, y + sy, sx, sy
    cx, cy = x - (sx < 0), y - (sy < 0)
    assert (cx, cy) in cells
    i = j = 0
    while not (i == P - 1 and j == Q - 1):
        if (i + 1) * Q < (j + 1) * P:
            i += 1
            if (cx + sx, cy) in cells: cx += sx
            else: sx = -sx
        else:
            j += 1
            if (cx, cy + sy) in cells: cy += sy
            else: sy = -sy
    return cx + (sx > 0), cy + (sy > 0), sx, sy

def lit_from(cells, S, B, K):
    """min step count k for each interior lattice point reached from S."""
    best = {}
    for P in range(0, B + 1):
        for Q in range(0, B + 1):
            if gcd(P, Q) != 1: continue
            for sx in ((1, -1) if P else (1,)):
                for sy in ((1, -1) if Q else (1,)):
                    x, y, a, b = S[0], S[1], sx, sy
                    for k in range(1, K + 1):
                        x, y, a, b = step(cells, x, y, a, b, P, Q)
                        t = kind(cells, x, y)
                        if t == 'C': break
                        if t == 'V': a = -a
                        elif t == 'H': b = -b
                        elif (x, y) != S and best.get((x, y), 99) > k: best[(x, y)] = k
    return best

def interior(cells):
    return sorted({(x, y) for (x, y) in cells if kind(cells, x, y) == 'I'})

def report(name, cells, B, K, sources=None):
    pts = interior(cells); tally = {}; bad = []
    for S in (sources or pts):
        best = lit_from(cells, S, B, K)
        for T in pts:
            if T == S: continue
            same = (T[0] - S[0]) % 2 == 0 and (T[1] - S[1]) % 2 == 0
            k = best.get(T)
            tally[(same, k)] = tally.get((same, k), 0) + 1
            if k is None: bad.append((S, T))
    print(name, 'area', len(cells), 'interior points', len(pts), 'B', B, 'K', K)
    for key in sorted(tally, key=lambda t: (t[0], t[1] or 99)):
        print('   same class' if key[0] else '   diff class', 'k =', key[1], ':', tally[key])
    print('   not reached:', bad[:8], '...' if len(bad) > 8 else '')

def pyramid(w, u, V, q, h, d, f):
    return ({(x, y) for x in range(0, w) for y in range(-q, h + d + f)} |
            {(x, y) for x in range(w, u) for y in range(0, h + d)} |
            {(x, y) for x in range(u, V) for y in range(0, h)})

if __name__ == '__main__':
    import json, time
    row = open('../d237-dark-examples-w22-26/astra/dark.tsv').read().split('\n')[1].split('\t')
    dark = {(c[0], c[1]) for c in json.loads(row[3])}
    t = time.time(); report('22-wall dark room', dark, 60, 6); print('   %.0fs' % (time.time() - t))
    t = time.time(); report('pyramid (4,5,12;3,4,1,2)', pyramid(4, 5, 12, 3, 4, 1, 2), 40, 6); print('   %.0fs' % (time.time() - t))
    t = time.time(); report('gap room (4,5,60;8,4,1,2), 3 sources', pyramid(4, 5, 60, 8, 4, 1, 2), 60, 6, [(1, 6), (15, 1), (40, 2)]); print('   %.0fs' % (time.time() - t))
