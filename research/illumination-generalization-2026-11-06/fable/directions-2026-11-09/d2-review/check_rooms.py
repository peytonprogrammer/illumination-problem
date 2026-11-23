"""Independent exact check of the factor bookkeeping on explicit rooms.

Reviewer script. It shares no code with d2-factor-audit. It builds the four
corner permutations of DP -> pillowcase by rotating about lattice points of
the room, enumerates ALL block systems by two brute-force methods plus a
union-find method, and tests on every factor:

  C1   r = delta * z_N + t,  s + 2t = 2 delta - 2,  fibre sums of e equal delta
  GB   p_N - z_N = 4 (this is NOT imposed; it is a real test here)
  C2   Z' = p_A + (3/2) R_A + 2 z_A - 1 and z_N = d - 1 - R_A/2 on parity factors
  C3   every parity factor other than the pillowcase has z_N >= 2
  BMIN a factor has the parity property iff its partition contains B_min
  K    k_wall + 2 k_interior <= s on parity factors

Rooms: every fixed strictly simple polyomino of area <= AMAX (default 8), in
all four choices of the A class, plus rooms written by hand below.
No room search for dark pairs is run.
"""
import itertools
import sys
from collections import Counter
from fractions import Fraction

sys.dont_write_bytecode = True
CLASSES = ("A", "C1", "B", "C2")
PAR = {(0, 0): "A", (1, 0): "C1", (1, 1): "B", (0, 1): "C2"}

# ------------------------------------------------------------- rooms


def fixed_polyominoes(nmax):
    """All fixed polyominoes with 1..nmax cells, as frozensets (translated)."""
    def norm(cells):
        mx = min(x for x, _ in cells)
        my = min(y for _, y in cells)
        return frozenset((x - mx, y - my) for x, y in cells)
    level = {frozenset([(0, 0)])}
    out = {1: level}
    for n in range(2, nmax + 1):
        nxt = set()
        for p in level:
            for (x, y) in p:
                for c in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if c not in p:
                        nxt.add(norm(p | {c}))
        out[n] = nxt
        level = nxt
    return out


def strictly_simple(cells):
    """No pinch vertex and no hole."""
    xs = [x for x, _ in cells]
    ys = [y for _, y in cells]
    for x in range(min(xs), max(xs) + 2):
        for y in range(min(ys), max(ys) + 2):
            a, b = (x - 1, y - 1) in cells, (x, y - 1) in cells
            c, d = (x - 1, y) in cells, (x, y) in cells
            if (a and d and not b and not c) or (b and c and not a and not d):
                return False
    lo_x, hi_x, lo_y, hi_y = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    seen = {(lo_x, lo_y)}
    stack = [(lo_x, lo_y)]
    while stack:
        x, y = stack.pop()
        for c in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if lo_x <= c[0] <= hi_x and lo_y <= c[1] <= hi_y and c not in cells and c not in seen:
                seen.add(c)
                stack.append(c)
    total = (hi_x - lo_x + 1) * (hi_y - lo_y + 1)
    return len(seen) + len(cells) == total


def around(cells, v):
    x, y = v
    return [c for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cells]


def lattice_points(cells):
    pts = set()
    for (i, j) in cells:
        pts |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    return sorted(pts)


def cls(v, origin):
    return PAR[((v[0] - origin[0]) % 2, (v[1] - origin[1]) % 2)]


# ------------------------------------------------------------- monodromy


def corner_perms(cells, origin):
    """g_X on cells: rotate the pillow front face of each cell about its X corner.

    Sheet of a cell c: the top copy if c is even, the bottom copy if c is odd.
    A rotation about lattice point v crosses the two lines through v in turn.
    Crossing a line moves to the neighbour cell, or flips the copy at a wall.
    """
    order = sorted(cells)
    idx = {c: k for k, c in enumerate(order)}
    ox, oy = origin

    def front(c):
        return (c[0] - ox + c[1] - oy) % 2

    perms = {}
    for X in CLASSES:
        g = []
        for c in order:
            i, j = c
            px, py = next(k for k, name in PAR.items() if name == X)
            vx = i if (i - ox) % 2 == px else i + 1
            vy = j if (j - oy) % 2 == py else j + 1
            assert cls((vx, vy), origin) == X
            s = front(c)
            dx = 1 if i == vx else -1
            dy = 1 if j == vy else -1
            vertical_first = (dx * dy > 0) == (s == 0)
            for step in (0, 1):
                vertical = vertical_first if step == 0 else not vertical_first
                nb = (2 * vx - 1 - i, j) if vertical else (i, 2 * vy - 1 - j)
                if nb in cells:
                    i, j = nb
                else:
                    s = 1 - s
            assert s == front((i, j))
            g.append(idx[(i, j)])
        assert sorted(g) == list(range(len(order)))
        perms[X] = tuple(g)
    return order, idx, perms


def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i not in seen:
            c, j = [], i
            while j not in seen:
                seen.add(j)
                c.append(j)
                j = p[j]
            out.append(tuple(c))
    return out


def check_geometry(cells, origin, order, perms):
    """Cycles of g_X must be exactly the points of DP over corner X."""
    for X in CLASSES:
        want = []
        for v in lattice_points(cells):
            if cls(v, origin) != X:
                continue
            cs = around(cells, v)
            if len(cs) == 4:
                ev = frozenset(c for c in cs if (c[0] + c[1] - origin[0] - origin[1]) % 2 == 0)
                want += [ev, frozenset(cs) - ev]
            else:
                want.append(frozenset(cs))
        got = [frozenset(order[i] for i in cyc) for cyc in cycles(perms[X])]
        assert sorted(map(sorted, want)) == sorted(map(sorted, got)), (X, origin)


# ------------------------------------------------------------- block systems


def invariant(part_of, gens):
    n = len(part_of)
    for g in gens:
        img = {}
        for a in range(n):
            if img.setdefault(part_of[a], part_of[g[a]]) != part_of[g[a]]:
                return False
    return True


def equal_partitions(n, m):
    """All partitions of range(n) into blocks of size m."""
    def rec(rest):
        if not rest:
            yield []
            return
        first = rest[0]
        for others in itertools.combinations(rest[1:], m - 1):
            blk = (first,) + others
            left = [x for x in rest if x not in blk]
            for tail in rec(left):
                yield [blk] + tail
    return rec(list(range(n)))


def systems_brute_partitions(n, gens):
    out = set()
    for m in range(1, n + 1):
        if n % m:
            continue
        for part in equal_partitions(n, m):
            part_of = [None] * n
            for k, blk in enumerate(part):
                for a in blk:
                    part_of[a] = k
            if invariant(part_of, gens):
                out.add(frozenset(frozenset(b) for b in part))
    return out


def systems_brute_blocks(n, gens):
    """A block system of a transitive group is the orbit of the block through 0."""
    out = set()
    for m in range(1, n + 1):
        if n % m:
            continue
        for others in itertools.combinations(range(1, n), m - 1):
            blk = frozenset((0,) + others)
            orbit = {blk}
            stack = [blk]
            ok = True
            while stack and ok:
                b = stack.pop()
                for g in gens:
                    nb = frozenset(g[a] for a in b)
                    if nb not in orbit:
                        if len(orbit) >= n // m:
                            ok = False
                            break
                        orbit.add(nb)
                        stack.append(nb)
            if ok and len(orbit) == n // m and len(frozenset().union(*orbit)) == n:
                out.add(frozenset(orbit))
    return out


def closure(n, gens, seeds):
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    todo = list(seeds)
    while todo:
        a, b = todo.pop()
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb
            for g in gens:
                todo.append((g[a], g[b]))
    blocks = {}
    for a in range(n):
        blocks.setdefault(find(a), set()).add(a)
    return frozenset(frozenset(b) for b in blocks.values())


def systems_join_closure(n, gens):
    base = {closure(n, gens, [(0, b)]) for b in range(1, n)}
    out = set(base) | {frozenset(frozenset([a]) for a in range(n))}
    grew = True
    while grew:
        grew = False
        for p in list(out):
            for q in base:
                seeds = [(min(b), x) for b in list(p) + list(q) for x in b]
                j = closure(n, gens, seeds)
                if j not in out:
                    out.add(j)
                    grew = True
    return out


# ------------------------------------------------------------- factor tests

STATS = Counter()
CASES = Counter()


def analyse_factor(cells, origin, order, perms, part, bmin, kw, ki, r):
    n = len(order)
    blocks = list(part)
    sizes = {len(b) for b in blocks}
    assert len(sizes) == 1
    delta = sizes.pop()
    d = n // delta
    bid = {}
    for k, b in enumerate(blocks):
        for a in b:
            bid[a] = k
    q = {}
    for X in CLASSES:
        qq = [None] * d
        for a in range(n):
            assert qq[bid[a]] in (None, bid[perms[X][a]])
            qq[bid[a]] = bid[perms[X][a]]
        q[X] = tuple(qq)
    cnt = {X: Counter(len(c) for c in cycles(q[X])) for X in CLASSES}
    for X in CLASSES:
        assert set(cnt[X]) <= {1, 2, 3}, ("cone angle above 3 pi in N", cnt)
    p_N = sum(cnt[X][1] for X in CLASSES)
    z_N = sum(cnt[X][3] for X in CLASSES)
    assert p_N - z_N == 4, ("Gauss-Bonnet fails", cnt)

    # ramification of phi, point by point
    s = t = 0
    for X in CLASSES:
        npt = {}
        for cyc in cycles(q[X]):
            for b in cyc:
                npt[b] = (min(cyc), len(cyc))
        fibre = Counter()
        for cyc in cycles(perms[X]):
            L = len(cyc)
            images = {npt[bid[a]] for a in cyc}
            assert len(images) == 1
            pt, m = images.pop()
            assert L % m == 0
            e = L // m
            fibre[pt] += e
            if e == 2:
                assert (L, m) == (2, 1)
                s += 1
            elif e == 3:
                assert (L, m) == (3, 1)
                t += 1
            else:
                assert e == 1
        assert all(v == delta for v in fibre.values()), "fibre sum of e differs from delta"
        assert len(fibre) == len(cycles(q[X]))
    assert r == delta * z_N + t, ("claim 1 fails", r, delta, z_N, t)
    assert s + 2 * t == 2 * delta - 2, ("Riemann-Hurwitz fails", s, t, delta)
    assert 0 <= t <= delta - 1
    if delta == 2:
        assert t == 0
    STATS["factors"] += 1
    if 1 < delta < n:
        STATS["proper factors"] += 1
    if t:
        STATS["factors with t > 0"] += 1
        if 1 < delta < n:
            STATS["proper factors with t > 0"] += 1
    if s and 1 < delta < n:
        STATS["proper factors with s > 0"] += 1

    parity = all(cnt[X][2] == 0 for X in ("C1", "B", "C2"))
    contains_bmin = all(any(b <= blk for blk in blocks) for b in bmin)
    assert parity == contains_bmin, "B_min characterisation fails"
    if parity:
        pA, RA, zA = cnt["A"][1], cnt["A"][2], cnt["A"][3]
        Zp = z_N - zA
        assert Fraction(Zp) == pA + Fraction(3, 2) * RA + 2 * zA - 1, "claim 2 fails"
        assert RA % 2 == 0 and z_N == d - 1 - RA // 2
        assert kw + 2 * ki <= s, ("budget fails", kw, ki, s)
        STATS["parity factors"] += 1
        if d > 1:
            assert z_N >= 2, "claim 3 lemma fails: parity factor with z_N <= 1"
            STATS["parity factors other than PC"] += 1
            CASES[(delta, z_N, t, (pA, RA, zA))] += 1
            if t:
                STATS["parity factors other than PC with t > 0"] += 1
            if 1 < delta:
                STATS["proper parity factors other than PC"] += 1
    else:
        # the Z' formula must fail exactly by R'/2 (audit section 1.4)
        pA, RA, zA = cnt["A"][1], cnt["A"][2], cnt["A"][3]
        Rp = sum(cnt[X][2] for X in ("C1", "B", "C2"))
        Zp = z_N - zA
        assert Fraction(Zp) == pA + Fraction(3, 2) * RA + 2 * zA - 1 - Fraction(Rp, 2)
        STATS["non-parity factors"] += 1
    return delta, d, cnt, parity, bid, q


def analyse_room(name, cells, origins=((0, 0), (1, 0), (0, 1), (1, 1)), brute=True, verbose=False):
    cells = frozenset(cells)
    n = len(cells)
    pts = lattice_points(cells)
    st = {v: len(around(cells, v)) for v in pts}
    r = sum(1 for v in pts if st[v] == 3)
    conv = sum(1 for v in pts if st[v] == 1)
    assert conv == r + 4, "not a simple orthogonal polygon"
    rows = []
    for origin in origins:
        order, idx, perms = corner_perms(cells, origin)
        check_geometry(cells, origin, order, perms)
        gens = [perms[X] for X in CLASSES]
        # product-one relation in the cyclic order A, C2, B, C1 up to orientation
        sysC = systems_join_closure(n, gens)
        if brute:
            sysB = systems_brute_blocks(n, gens)
            assert sysB == sysC, "block-orbit brute force disagrees with join closure"
            STATS["rooms x origins with brute-force block check"] += 1
            if n <= 8:
                sysA = systems_brute_partitions(n, gens)
                assert sysA == sysC, "partition brute force disagrees"
        seeds = [c for X in ("C1", "B", "C2") for c in cycles(perms[X]) if len(c) == 2]
        bmin = closure(n, gens, seeds)
        kw = sum(1 for v in pts if cls(v, origin) != "A" and st[v] == 2)
        ki = sum(1 for v in pts if cls(v, origin) != "A" and st[v] == 4)
        intA = [v for v in pts if cls(v, origin) == "A" and st[v] == 4]
        STATS["rooms x origins"] += 1
        for part in sysC:
            delta, d, cnt, parity, bid, q = analyse_factor(
                cells, origin, order, perms, part, bmin, kw, ki, r)
            sep = []
            if parity and len(intA) >= 2:
                acyc = {}
                for cyc in cycles(q["A"]):
                    for b in cyc:
                        acyc[b] = min(cyc)
                img = {}
                for v in intA:
                    cs = around(cells, v)
                    ev = [c for c in cs if (c[0] + c[1] - origin[0] - origin[1]) % 2 == 0]
                    od = [c for c in cs if c not in ev]
                    img[v] = set()
                    for lift in (ev, od):
                        im = {acyc[bid[idx[c]]] for c in lift}
                        assert len(im) == 1
                        img[v] |= im
                for a, b in itertools.combinations(intA, 2):
                    # audit 1.3: dark if one lift of a misses every lift of b
                    if any(x not in img[b] for x in img[a]) or any(x not in img[a] for x in img[b]):
                        sep.append((a, b))
                    STATS["interior A pairs x parity factors"] += 1
                if sep:
                    STATS["separating parity factors"] += 1
                    if r <= 8:
                        STATS["SEPARATING PARITY FACTOR WITH r <= 8"] += 1
            rows.append((origin, delta, d, {X: dict(cnt[X]) for X in CLASSES}, parity, sep))
        if verbose:
            print(f"  origin {origin}: k_wall={kw} k_int={ki} interior A={intA} "
                  f"B_min blocks={len(bmin)}")
            for row in rows:
                if row[0] == origin:
                    print(f"    delta={row[1]} d={row[2]} parity={row[4]} sep={row[5]} {row[3]}")
    return r, rows


def from_ascii(art):
    lines = [ln for ln in art.strip("\n").split("\n")]
    h = len(lines)
    return {(x, h - 1 - y) for y, ln in enumerate(lines) for x, ch in enumerate(ln) if ch == "#"}


STAIR = {(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)}
P1 = {(i, -1 - j) for (i, j) in STAIR}
P2 = {(3 - i, -1 - j) for (i, j) in STAIR}

HAND = {
    "five-square staircase": STAIR,
    "two staircases (P0 + P1)": STAIR | P1,
    "22-wall room (P0 + P1 + P2)": STAIR | P1 | P2,
    "3x3 square": {(i, j) for i in range(3) for j in range(3)},
    "4x3 rectangle": {(i, j) for i in range(4) for j in range(3)},
    "4x4 square": {(i, j) for i in range(4) for j in range(4)},
    "6x2 rectangle": {(i, j) for i in range(6) for j in range(2)},
    "12-wall cross": {(i, j) for i in range(4) for j in range(4)} - {(0, 0), (3, 0), (0, 3), (3, 3)},
    "20-cell cross": from_ascii("""
..##..
..##..
######
######
..##..
..##..
"""),
    "notched 4x4": from_ascii("""
####
###.
####
.###
"""),
    "two blocks with a bridge": from_ascii("""
##..##
######
"""),
    "two blocks, offset bridge": from_ascii("""
....##
##.###
####..
##....
"""),
    "L of blocks": from_ascii("""
##..
##..
####
####
"""),
    "diagonal blocks plus u, v": from_ascii("""
..##
.###
###.
##..
"""),
    "four L-trominoes about a point": from_ascii("""
.##.
####
####
.##.
"""),
    "pinwheel 12": from_ascii("""
.#..
.###
###.
..#.
"""),
    "three staircases around (-1,0)": STAIR | P1 | {(-3 - i, j) for (i, j) in STAIR},
    "four staircases around (-1,0)": STAIR | P1 | {(-3 - i, j) for (i, j) in STAIR | P1},
    "mirror room, axis off the lattice": STAIR | P1 | {(-2 - i, j) for (i, j) in STAIR | P1},
}

if __name__ == "__main__":
    amax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    polys = fixed_polyominoes(amax)
    for n in range(1, amax + 1):
        good = [p for p in polys[n] if strictly_simple(p)]
        for p in good:
            analyse_room(f"poly{n}", p)
        print(f"area {n}: {len(polys[n])} fixed polyominoes, {len(good)} strictly simple, all checks pass")
    for name, cells in HAND.items():
        assert strictly_simple(cells), name
        print(f"== {name}: area {len(cells)}")
        r, rows = analyse_room(name, cells, brute=len(cells) <= 20, verbose=True)
        print(f"   r={r} W={2 * r + 4}")
    print("== totals")
    for k in sorted(STATS):
        print(f"   {k}: {STATS[k]}")
    print("== parity factors other than PC, by (delta, z_N, t, (p_A, R_A, z_A)): count")
    for k in sorted(CASES):
        print(f"   {k}: {CASES[k]}")
