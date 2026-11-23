"""d201 referee checks: pocket lemma and unequal-length three-chamber theorem.

Standard library only, exact Fraction arithmetic. Named rooms only: the
20-wall aligned three-chamber room with chambers at 0, D1, D1+D2 and unit
corridors at 1<y<2, for 4 <= D1, D2 <= 30. For every pair of interior lattice
points, the path that snapshot.md prescribes is built (entry a from the
criterion, by one floor operation) and that single ray is traced. No ray,
direction, word or room-size search. Also a structural check of the named R22
base room (odd-odd fiber, integral full-mouth pockets) and a ledger lookup.
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
import math
import time

T0 = time.process_time()
HERE = Path(__file__).resolve().parent
ARCH = HERE.parent
W, H, G = 3, 1, 1                      # pocket width, pocket height, band height
SPACING = F(W * G, G + H)              # wg/(g+h) = 3/2


def room(D1, D2):
    P = D1 + D2
    return [(0, 0), (3, 0), (3, 1), (D1, 1), (D1, 0), (D1 + 3, 0), (D1 + 3, 1),
            (P, 1), (P, 0), (P + 3, 0), (P + 3, 3), (P, 3), (P, 2),
            (D1 + 3, 2), (D1 + 3, 3), (D1, 3), (D1, 2), (3, 2), (3, 3), (0, 3)]


def inside(V, p):
    x, y = p
    c = False
    for i in range(len(V)):
        (x0, y0), (x1, y1) = V[i], V[(i + 1) % len(V)]
        if x0 == x1 and min(y0, y1) < y <= max(y0, y1) and x0 > x:
            c = not c
    return c


def on_boundary(V, p):
    x, y = p
    for i in range(len(V)):
        (x0, y0), (x1, y1) = V[i], V[(i + 1) % len(V)]
        if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1):
            return True
    return False


def trace(V, p, d, target, max_bounces=400):
    """Billiard ray p + t d. Returns ('hit'|'corner'|'over', bounce list)."""
    verts = {(F(a), F(b)) for a, b in V}
    edges = [(V[i], V[(i + 1) % len(V)]) for i in range(len(V))]
    px, py = F(p[0]), F(p[1])
    dx, dy = F(d[0]), F(d[1])
    tx, ty = F(target[0]), F(target[1])
    bounces = []
    while True:
        best = None
        for (a, b) in edges:
            if a[0] == b[0]:
                if dx == 0:
                    continue
                t = (a[0] - px) / dx
                if t <= 0:
                    continue
                y = py + t * dy
                if min(a[1], b[1]) <= y <= max(a[1], b[1]):
                    if best is None or t < best[0]:
                        best = (t, 'v', (F(a[0]), y))
            else:
                if dy == 0:
                    continue
                t = (a[1] - py) / dy
                if t <= 0:
                    continue
                x = px + t * dx
                if min(a[0], b[0]) <= x <= max(a[0], b[0]):
                    if best is None or t < best[0]:
                        best = (t, 'h', (x, F(a[1])))
        assert best is not None, "ray escaped"
        t, kind, q = best
        tt = (tx - px) / dx if dx != 0 else (ty - py) / dy
        if 0 < tt < t and px + tt * dx == tx and py + tt * dy == ty:
            return 'hit', bounces
        if q in verts:
            return 'corner', bounces + [(kind, q)]
        bounces.append((kind, q))
        if len(bounces) > max_bounces:
            return 'over', bounces
        px, py = q
        if kind == 'v':
            dx = -dx
        else:
            dy = -dy


# ---------------------------------------------------------------------------
# Part 1/2: the pocket lemma as stated in the note.

def fold(s, w=W):
    r = s % (2 * w)
    return r if r <= w else 2 * w - r


def pocket_bounces(xl, a, c):
    """Predicted wall hits of the pocket (xl, xl+3) x (2, 3), mouth y=2,
    entered at local a moving right with dx/dy = c. Side hits at unfolded
    multiples of w in (a, a+2hc), roof hit at a+hc."""
    pts = []
    j = math.floor(a / W) + 1
    while W * j < a + 2 * H * c:
        s = F(W * j)
        y = 2 + (s - a) / c if s < a + H * c else 3 - (s - a - H * c) / c
        pts.append((s, ('v', (xl + fold(s), y))))
        j += 1
    pts.append((a + H * c, ('h', (xl + fold(a + H * c), F(3)))))
    pts.sort(key=lambda z: z[0])
    return [b for _, b in pts]


def solve_entry(U, V):
    """Criterion: max(0,M-w,U) < a < min(w,M), (2+2h/g) a == M+(2h/g)U mod 2w.
    Returns the first progression value strictly above the lower endpoint."""
    M = U + V
    lo, hi = max(F(0), M - W, F(U)), min(F(W), F(M))
    coef = 2 + F(2 * H, G)
    a0 = (M + F(2 * H, G) * U) / coef          # one solution of the congruence
    a = a0 + SPACING * (math.floor((lo - a0) / SPACING) + 1)
    assert lo < a <= lo + SPACING
    return a, lo, hi, M


def criterion_holds(a, U, V):
    """Independent check of entry/return/roof/exit conditions (lemma part 1)."""
    M = U + V
    c = (F(a) - U) / G
    b = M - a
    ok = c > 0 and 0 < a < W and 0 < b < W
    ret = a + 2 * H * c                        # unfolded return phase
    ok = ok and (ret - b) % (2 * W) == 0       # folds to b, rightward
    ok = ok and (a + H * c) % W != 0 and ret % W != 0
    return ok, c, b


# ---------------------------------------------------------------------------
# Prescribed constructions (row 1). Each returns start, dir, target, predicted.

def reflect_y(c):
    p, d, q, pred, lab = c
    return ((p[0], 3 - p[1]), (d[0], -d[1]), (q[0], 3 - q[1]),
            [(k, (pt[0], 3 - pt[1])) for k, pt in pred], lab)


def reflect_x(c, L):
    p, d, q, pred, lab = c
    return ((L - p[0], p[1]), (-d[0], d[1]), (L - q[0], q[1]),
            [(k, (L - pt[0], pt[1])) for k, pt in pred], lab)


STATS = Counter()


def adjacent(x0, D, u, v):
    """Source (x0+u,1), target (x0+D+v,1)."""
    m = F(2 * x0 + D + u + v, 2)
    assert x0 + 3 < m < x0 + D
    return ((x0 + u, 1), (m - x0 - u, 1), (x0 + D + v, 1),
            [('h', (m, F(2)))], 'adjacent-bounce')


def adjacent_repair(D, u):
    """D=4, u=v, pair in first two chambers. Source unfolded to -u."""
    assert D == 4
    U, V = -u, 4 + u
    a, lo, hi, M = solve_entry(U, V)
    assert (lo, hi, M) == (1, 3, 4)
    assert a == F(5 - u, 2), "item 1 formula a=(5-u)/2"
    ok, c, b = criterion_holds(a, U, V)
    assert ok
    assert b == 4 - a and a + 2 * c - b == 6 and a + H * c == 5
    y0 = 1 + F(u) / (a + u)
    pred = [('v', (F(0), y0))] + pocket_bounces(0, a, c)
    STATS['repair a=%s u=%d' % (a, u)] += 1
    return (u, 1), (-(a + u), 1), (D + u, 1), pred, 'adjacent-repair'


def outer(D1, D2, u, v):
    P, Dl = D1 + D2, D2 - D1
    if Dl + v - u < 0:                       # bounce in first corridor
        m = F(P + v - u, 2)
        assert 3 < m < D1
        y0 = 1 + F(u) / (m + u)
        return ((u, 1), (-(m + u), 1), (P + v, 1),
                [('v', (F(0), y0)), ('h', (m, F(2)))], 'outer-left-wall')
    if Dl + u - v > 0:                       # bounce in second corridor
        m = F(P + 6 + u - v, 2)
        assert D1 + 3 < m < P
        img = P + 6 - v
        y1 = 2 - (F(P + 3) - m) / (img - m)
        return ((u, 1), (m - u, 1), (P + v, 1),
                [('h', (m, F(2))), ('v', (F(P + 3), y1))], 'outer-right-wall')
    # residual: middle pocket
    assert (u == v and Dl == 0) or ((u, v) == (1, 2) and abs(Dl) <= 1)
    U, V = u - D1, D2 + v
    a, lo, hi, M = solve_entry(U, V)
    assert M in (2, 3, 4) and hi - lo == min(M, 6 - M) and hi - lo > SPACING
    assert a < hi
    ok, c, b = criterion_holds(a, U, V)
    assert ok
    if Dl == 0:   # item 2's congruence 4a == u+v+2(u-D1) mod 6
        assert (4 * a - (u + v + 2 * (u - D1))) % 6 == 0
    STATS['pocket M=%d' % M] += 1
    return ((u, 1), (D1 + a - u, 1), (P + v, 1),
            pocket_bounces(D1, a, c), 'outer-pocket')


def construct(D1, D2, p, q):
    starts = [0, D1, D1 + D2]
    P = D1 + D2
    ci = lambda z: max(i for i in range(3) if starts[i] < z[0])
    if ci(p) > ci(q):
        p, q = q, p
    i, j = ci(p), ci(q)
    if i == j or p[1] != q[1]:
        return (p, (q[0] - p[0], q[1] - p[1]), q, [],
                'same-chamber' if i == j else 'different-rows')
    row2 = p[1] == 2
    u, v = p[0] - starts[i], q[0] - starts[j]
    if j - i == 1:
        D = starts[j] - starts[i]
        if D > max(6 - u - v, u + v):
            c = adjacent(starts[i], D, u, v)
        else:
            assert D == 4 and u == v
            if i == 0:
                c = adjacent_repair(D, u)
            else:   # reverse the room: x -> P+3-x puts the pair first
                c = reflect_x(adjacent_repair(D, 3 - u), P + 3)
    else:
        c = outer(D1, D2, u, v)
    return reflect_y(c) if row2 else c


def run_room(D1, D2):
    V = room(D1, D2)
    P = D1 + D2
    pts = [(s + u, y) for s in (0, D1, P) for u in (1, 2) for y in (1, 2)]
    for z in pts:
        assert inside(V, z) and not on_boundary(V, z)
    # no other interior lattice points
    cnt = sum(1 for x in range(P + 4) for y in range(4)
              if inside(V, (x, y)) and not on_boundary(V, (x, y)))
    assert cnt == 12
    labels = Counter()
    for p, q in combinations(pts, 2):
        s, d, t, pred, lab = construct(D1, D2, p, q)
        assert {s, t} == {p, q}
        st, bounces = trace(V, s, d, t)
        if st != 'hit':
            raise AssertionError((D1, D2, p, q, lab, st, bounces[-3:]))
        bounces = [(k, (F(x), F(y))) for k, (x, y) in bounces]
        predf = [(k, (F(x), F(y))) for k, (x, y) in pred]
        if bounces != predf:
            raise AssertionError(('bounce mismatch', D1, D2, p, q, lab,
                                  bounces, predf))
        labels[lab] += 1
        STATS['bounces max'] = max(STATS['bounces max'], len(bounces))
    return labels


def word_of(V):
    n = len(V)
    out = []
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        out.append('L' if cr > 0 else 'R')
    return ''.join(out)


def canon(w):
    cands = []
    for s in (w, w[::-1]):
        cands += [s[i:] + s[:i] for i in range(len(s))]
    return min(cands)


def main():
    print("d201 checks. Pocket w=3, h=g=1, spacing wg/(g+h) =", SPACING)
    totals = Counter()
    rooms = 0
    for D1 in range(4, 31):
        for D2 in range(4, 31):
            lab = run_room(D1, D2)
            assert sum(lab.values()) == 66
            totals.update(lab)
            rooms += 1
            if (D1, D2) in [(4, 4), (4, 5), (5, 4), (4, 30), (7, 7), (13, 14), (30, 30)]:
                print("  room D1=%2d D2=%2d: %s" % (D1, D2, dict(sorted(lab.items()))))
    print("rooms traced: %d; pairs per room: 66; all prescribed rays reach their"
          " targets, no corner hits, bounce lists equal the predicted ones" % rooms)
    print("pair totals by construction:", dict(sorted(totals.items())))
    print("residual pocket / repair stats:", dict(sorted(STATS.items())))

    # Controls: the naive one-bounce paths fail exactly where the note says.
    print("\nControls (expected failures of the plain bounce):")
    for D1, D2, p, q, d in [(4, 4, (1, 1), (5, 1), (2, 1)),
                            (4, 4, (2, 1), (6, 1), (2, 1)),
                            # outer equal offsets, Delta=0: left-wall bounce at (7,2)
                            (7, 7, (1, 1), (15, 1), (-8, 1)),
                            # (u,v)=(1,2), Delta=1: left-wall midpoint lies in
                            # the middle chamber, so there is no bounce at y=2
                            (6, 7, (1, 1), (15, 1), (-8, 1))]:
        st, b = trace(room(D1, D2), p, d, q)
        print("  D=(%d,%d) %s->%s plain bounce: %s at %s" % (D1, D2, p, q, st, b[-1][1] if b else None))
    # Wrong-congruence control: a just off the progression misses the target.
    D1 = D2 = 6
    U, V = 1 - D1, D2 + 1
    a, *_ = solve_entry(U, V)
    for aa in (a, a + F(1, 4)):
        c = aa - U
        st, b = trace(room(D1, D2), (1, 1), (c, 1), (2 * D1 + 1, 1))
        print("  D=(6,6) (1,1)->(13,1) pocket entry a=%s: %s" % (aa, st))

    # Item 1 / item 2 explicit values.
    print("\nItem 1 (D=4): a = (5-u)/2 is the first criterion value above 1 for u=1,2;"
          " roof contact 2a+u = 5; a+2c-b = 6 (asserted).")
    print("Item 2 (D1=D2): 4a == u+v+2(u-D1) mod 6 holds for every chosen a (asserted).")

    # Equal-length agreement with d200's pocket ray for D == 1 mod 3.
    agree = 0
    for D in range(7, 31, 3):
        for u in (1, 2):
            a, *_ = solve_entry(u - D, D + u)
            if a == u - F(1, 2):
                agree += 1
    print("d200 cross-check: for D = 3k+1 in 7..28, the criterion's first value "
          "equals d200's a = u - 1/2 in %d of 16 cases" % agree)

    # R22 control.
    print("\nR22 control (d8 rooms.json, R22-base):")
    rooms_json = json.load(open(ARCH / "d8-perturbation-test" / "rooms.json"))
    cells = {tuple(c) for r in rooms_json if r["id"] == "R22-base" for c in r["cells"]}
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    x0, x1, y0, y1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1
    print("  cells:", len(cells), "bbox", (x0, y0, x1, y1))
    kinds = Counter()
    for X in range(x0, x1 + 1):
        for Y in range(y0, y1 + 1):
            inc = [(X - 1, Y - 1), (X, Y - 1), (X - 1, Y), (X, Y)]
            k = sum(c in cells for c in inc)
            if k == 0:
                continue
            if k == 4:
                t = 'interior'
            elif k == 2:
                diag = ((X - 1, Y - 1) in cells) == ((X, Y) in cells)
                t = 'pinch' if diag else 'smooth'
            else:
                t = 'corner'
            kinds[(X % 2, Y % 2, t)] += 1
    for cls in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        print("  class", cls, {t: kinds[(cls[0], cls[1], t)] for t in
                               ('interior', 'smooth', 'corner', 'pinch')})
    # Integral full-mouth pockets: rectangle of cells, solid roof and flanks,
    # mouth row fully inside. Four orientations via coordinate maps.
    maps = [lambda x, y: (x, y), lambda x, y: (x, -y - 1),
            lambda x, y: (y, x), lambda x, y: (-y - 1, x)]
    found = []
    for mi, m in enumerate(maps):
        C = {m(*c) for c in cells}
        cx = [c[0] for c in C]
        cy = [c[1] for c in C]
        for a0 in range(min(cx), max(cx) + 1):
            for w in range(3, max(cx) - a0 + 2):
                for b0 in range(min(cy), max(cy) + 1):
                    for h in range(1, max(cy) - b0 + 2):
                        body = all((a0 + i, b0 + j) in C for i in range(w) for j in range(h))
                        if not body:
                            continue
                        roof = all((a0 + i, b0 + h) not in C for i in range(w))
                        flanks = all((a0 - 1, b0 + j) not in C and (a0 + w, b0 + j) not in C
                                     for j in range(h))
                        mouth = all((a0 + i, b0 - 1) in C for i in range(w))
                        if roof and flanks and mouth:
                            found.append((mi, a0, b0, w, h))
    print("  integral full-mouth pockets with width>=3, height>=1:", len(found), found[:5])

    # Ledger lookup for the three-chamber word.
    w = canon(word_of(room(7, 7)))
    led = json.load(open(ARCH / "d163-pattern-ledger" / "ledger.json"))["words"]
    e = led.get(w)
    print("\nLedger: three-chamber word", w, "W=%d" % len(w),
          "status", None if e is None else (e.get('status'), e.get('by'), e.get('family')))
    print("\nCPU seconds: %.1f" % (time.process_time() - T0))


if __name__ == "__main__":
    main()
