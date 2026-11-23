"""Check of the room lemmas of proof.md (Lemma L2 and the count of Lemma L3) on a short
fixed list of polygons.  This is not a room search: the shapes are written out by hand, and
each one is tested in the four parity positions of the lattice.

For each polygon (a set of unit cells) and each choice of the class a, the script builds
g_a, g_b, g_c, g_d by dictionary D0 (rotation by pi about the points of one class) and checks:

  L2   for every lattice segment [A1, A2] of length 2 on a line through class-a points, with
       class-a endpoints, contained in the polygon and containing no vertex, the midpoint F
       carries a 2-cycle of g_x whose two cells lie in two distinct 2-cycles of g_a (a link);
  L3   (number of segments as in L2, vertex or not) >= n/8 - (r+1)/2, and
       (number of those that contain a vertex) <= 2 p_a + 4 z_a + z_b + z_c <= 6r + 8;
  ray  for every interior a-point S and axis direction e, a link at S+e exists unless
       S+e is reflex, or S+e is interior and S+2e is reflex.

Run: python3 -B roomlink.py
"""
from fractions import Fraction


def rect(w, h, x0=0, y0=0):
    return {(x0 + i, y0 + j) for i in range(w) for j in range(h)}


SHAPES = {
    'rectangle 4x6': rect(4, 6),
    'rectangle 5x5': rect(5, 5),
    'rectangle 2x9': rect(2, 9),
    'L 6x6 minus 3x3': rect(6, 6) - rect(3, 3, 3, 3),
    'cross 3 arms of width 2': rect(2, 8, 3, 0) | rect(8, 2, 0, 3),
    'staircase': rect(6, 2) | rect(4, 2, 0, 2) | rect(2, 2, 0, 4),
    'pinwheel octomino': {(0, 0), (-1, 0), (0, -1), (-1, -1), (1, 0), (-1, 1), (-2, -1), (0, -2)},
    'pinwheel with arms of length 5': rect(2, 2, -1, -1) | rect(5, 1, 1, 0) | rect(1, 5, -1, 1)
                                      | rect(5, 1, -6, -1) | rect(1, 5, 0, -6),
    'U shape': rect(7, 2) | rect(2, 5, 0, 2) | rect(2, 5, 5, 2),
    'comb': rect(9, 2) | rect(1, 4, 0, 2) | rect(1, 4, 3, 2) | rect(1, 4, 6, 2),
}


def star(cells, p):
    x, y = p
    return [c for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cells]


def kind(cells, p):
    s = star(cells, p)
    if len(s) == 0:
        return 'out'
    if len(s) == 1:
        return 'convex'
    if len(s) == 3:
        return 'reflex'
    if len(s) == 4:
        return 'interior'
    (a, b), (c, d) = s
    assert a == c or b == d, 'not strictly simple'
    return 'flat'


def rotation(cells, order, px, py):
    """rotation by pi about the lattice points with parity (px, py), as a map on cells"""
    out = {}
    for (i, j) in order:
        cx = i if i % 2 == px else i + 1
        cy = j if j % 2 == py else j + 1
        i2 = 2 * cx - 1 - i
        c = (i2, j) if (i2, j) in cells else (i, j)
        j2 = 2 * cy - 1 - c[1]
        c = (c[0], j2) if (c[0], j2) in cells else c
        out[(i, j)] = c
    return out


def cycle_of(g, c):
    cyc, x = [c], g[c]
    while x != c:
        cyc.append(x)
        x = g[x]
    return frozenset(cyc)


def in_poly(cells, p, q):
    """the unit lattice segment [p, q] lies in the closed polygon"""
    (x, y), (u, v) = min(p, q), max(p, q)
    if y == v:
        return (x, y) in cells or (x, y - 1) in cells
    return (x, y) in cells or (x - 1, y) in cells


def main():
    checked = links = 0
    for name, cells0 in SHAPES.items():
        for dx in (0, 1):
            for dy in (0, 1):
                cells = {(i + dx, j + dy) for (i, j) in cells0}
                order = sorted(cells)
                n = len(cells)
                pts = {(x + a, y + b) for (x, y) in cells for a in (0, 1) for b in (0, 1)}
                K = {p: kind(cells, p) for p in pts}
                r = sum(1 for p in pts if K[p] == 'reflex')
                assert sum(1 for p in pts if K[p] == 'convex') == r + 4
                ga = rotation(cells, order, 0, 0)

                def cls(p):
                    return (p[0] % 2, p[1] % 2)

                def link_at(F):
                    gx = rotation(cells, order, *cls(F))
                    for c in star(cells, F):
                        d = gx[c]
                        if d != c and gx[d] == c:
                            A, B = cycle_of(ga, c), cycle_of(ga, d)
                            if len(A) == 2 and len(B) == 2 and A != B:
                                return True
                    return False

                cand = blocked = 0
                for A in pts:
                    if cls(A) != (0, 0):
                        continue
                    for e in ((1, 0), (0, 1)):
                        F = (A[0] + e[0], A[1] + e[1])
                        B = (A[0] + 2 * e[0], A[1] + 2 * e[1])
                        if F not in pts or B not in pts:
                            continue
                        if not (in_poly(cells, A, F) and in_poly(cells, F, B)):
                            continue
                        cand += 1
                        if any(K[p] in ('convex', 'reflex') for p in (A, F, B)):
                            blocked += 1
                            continue
                        assert link_at(F), ('L2 fails', name, dx, dy, A, e)
                        links += 1
                pa = sum(1 for p in pts if K[p] == 'convex' and cls(p) == (0, 0))
                za = sum(1 for p in pts if K[p] == 'reflex' and cls(p) == (0, 0))
                zb = sum(1 for p in pts if K[p] == 'reflex' and cls(p) in ((1, 0), (0, 1)))
                assert cand >= Fraction(n, 8) - Fraction(r + 1, 2), ('L3 count', name, dx, dy)
                assert blocked <= 2 * pa + 4 * za + zb <= 6 * r + 8, ('L3 blocked', name, dx, dy)
                for S in pts:
                    if cls(S) != (0, 0) or K[S] != 'interior':
                        continue
                    for e in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        F = (S[0] + e[0], S[1] + e[1])
                        B = (S[0] + 2 * e[0], S[1] + 2 * e[1])
                        stop = K[F] == 'reflex' or (K[F] == 'interior' and K[B] == 'reflex')
                        assert K[F] != 'convex'
                        if not stop:
                            assert link_at(F), ('ray lemma fails', name, dx, dy, S, e)
                        checked += 1
                print(f'{name:32s} shift ({dx},{dy})  n {n:3d}  r {r}  segments {cand:3d}'
                      f'  with a vertex {blocked:3d}  bound n/8-(r+1)/2 = {float(Fraction(n, 8) - Fraction(r + 1, 2)):.2f}')
    print('L2 instances checked:', links, ' ray instances checked:', checked, ' no assertion failed')


if __name__ == '__main__':
    main()
