"""d200 referee checks: the three-chamber lighting snapshot.

Standard library only, exact Fraction arithmetic. Named rooms only: d152's
20-wall three-chamber room with X = Y = 3k+1, D = 3k+4, for k = 6..40.
Only the rays that snapshot.md prescribes are traced, from the stated start
toward the stated target. No ray, direction, word or room-size search.
"""
from fractions import Fraction as F
from itertools import combinations
import time

T0 = time.process_time()


def room(D):
    """Vertices of the 20-wall room, counterclockwise."""
    return [(0, 0), (3, 0), (3, 1), (D, 1), (D, 0), (D + 3, 0), (D + 3, 1),
            (2 * D, 1), (2 * D, 0), (2 * D + 3, 0), (2 * D + 3, 3), (2 * D, 3),
            (2 * D, 2), (D + 3, 2), (D + 3, 3), (D, 3), (D, 2), (3, 2), (3, 3),
            (0, 3)]


def area2(V):
    return sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1]
               for i in range(len(V)))


def inside(V, p):
    """Strict interior test by ray casting (p not on boundary assumed)."""
    x, y = p
    c = False
    n = len(V)
    for i in range(n):
        (x0, y0), (x1, y1) = V[i], V[(i + 1) % n]
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


def trace(V, p, d, target, max_bounces):
    """Trace the billiard ray p + t d. Return (status, bounce list).

    status: 'hit' if target is reached on an open segment, 'corner' if the ray
    meets a vertex, 'over' if more than max_bounces wall hits occur first.
    """
    verts = set(V)
    edges = [(V[i], V[(i + 1) % len(V)]) for i in range(len(V))]
    px, py = F(p[0]), F(p[1])
    dx, dy = F(d[0]), F(d[1])
    tx, ty = F(target[0]), F(target[1])
    bounces = []
    while True:
        best = None
        for (a, b) in edges:
            if a[0] == b[0]:  # vertical edge
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
        # target on the open segment p -> q?
        if dx != 0:
            tt = (tx - px) / dx
        else:
            tt = (ty - py) / dy
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
# Prescribed constructions. Each returns (start, direction, target,
# predicted bounce list or None, label). Row y=1 versions; row 2 by reflection.

def pocket(D, k, u):
    """Part 2: equal offsets, slope 1/L, L = D - 1/2."""
    L = F(D) - F(1, 2)
    a = F(u) - F(1, 2)
    # predicted bounces: side hits at unfolded local abscissas 3j in (a, a+2L),
    # roof hit at a+L. Fold local unfolded abscissa s into [0,3].
    def fold3(s):
        r = s % 6
        return r if r <= 3 else 6 - r
    pred = []
    for j in range(1, 10 ** 6):
        s = F(3 * j)
        if s >= a + 2 * L:
            break
        pred.append((s, 'v'))
    pred.append((a + L, 'h'))
    pred.sort()
    out = []
    for s, kind in pred:
        h = 2 + (s - a) / L if s <= a + L else 3 - (s - a - L) / L
        out.append((kind, (D + fold3(s), h if kind == 'v' else F(3))))
    assert len([o for o in out if o[0] == 'v']) == 2 * k + 2
    return (u, 1), (L, 1), (2 * D + u, 1), out, 'pocket'


def distinct(D, u, v):
    """Part 4: f(t) = 1 + 3t + t/H, H = 2D + v - u, x = u + t."""
    H = 2 * D + v - u
    assert H % 2 == 1
    s = 3 + F(1, H)
    seams = [3, D, D + 3, 2 * D]
    in_chamber = lambda x: x < 3 or D < x < D + 3 or x > 2 * D
    pred = []
    top = 1 + 3 * H + 1
    for c in range(2, top + 1):  # f crosses integer c at t=(c-1)/s
        t = (F(c) - 1) / s
        if not (0 < t < H):
            continue
        x = u + t
        assert x not in seams, "integral crossing at a seam"
        if in_chamber(x):
            if c % 3:
                continue
            r = c % 6
            y = F(0) if r == 0 else F(3)
        else:
            y = F(1) if c % 2 else F(2)
        pred.append(('h', (x, y)))
    # seam checks: integral t, z in (1,2), folds agree
    for xs in seams:
        t = xs - u
        z = 1 + F(t, H)
        assert 1 < z < 2
        fy = 1 + 3 * t + F(t, H)
        r6 = fy % 6
        ch = r6 if r6 <= 3 else 6 - r6
        r2 = (fy - 1) % 2
        co = 1 + (r2 if r2 <= 1 else 2 - r2)
        assert ch == co == (z if t % 2 == 0 else 3 - z)
    return (u, 1), (1, s), (2 * D + v, 1), pred, 'distinct'


def adjacent(D, i, u, v):
    """Part 3: one bounce at y=2, horizontal midpoint."""
    x0, x1 = i * D + u, (i + 1) * D + v
    m = F(x0 + x1, 2)
    assert i * D + 3 < m < (i + 1) * D
    return (x0, 1), (m - x0, 1), (x1, 1), [('h', (m, F(2)))], 'adjacent'


def straight(p, q, label):
    return p, (q[0] - p[0], q[1] - p[1]), q, [], label


def one_reversal_21(D):
    """Part 4 remark: (u,v)=(2,1), source unfolded to -2, bounce at (D-1/2, 2)."""
    src, tgt = (2, 1), (2 * D + 1, 1)
    # unfolded from (-2,1) to (D-1/2,2): direction (D+3/2, 1); actual start goes left
    d = (-(F(D) + F(3, 2)), 1)
    y0 = 1 + F(2) / (F(D) + F(3, 2))
    return src, d, tgt, [('v', (F(0), y0)), ('h', (F(D) - F(1, 2), F(2)))], 'one-rev(2,1)'


def reflect(c):
    """Vertical reflection y -> 3 - y of a construction."""
    p, d, q, pred, lab = c
    p2 = (p[0], 3 - p[1])
    q2 = (q[0], 3 - q[1])
    d2 = (d[0], -d[1])
    pred2 = None if pred is None else [(kd, (pt[0], 3 - pt[1])) for kd, pt in pred]
    return p2, d2, q2, pred2, lab + '/refl'


def prescribe(D, k, P, Q):
    """Choose the note's construction for the unordered pair {P, Q}."""
    (ip, up, vp), (iq, uq, vq) = P, Q
    pt = lambda i, u, v: (i * D + u, v)
    if ip == iq:
        return straight(pt(*P), pt(*Q), 'same-chamber')
    if vp != vq:
        return straight(pt(*P), pt(*Q), 'diff-row')
    if ip > iq:
        P, Q = Q, P
        (ip, up, vp), (iq, uq, vq) = P, Q
    if iq - ip == 1:
        c = adjacent(D, ip, up, uq)
    elif up == uq:
        c = pocket(D, k, up)
    else:
        c = distinct(D, up, uq)
    return c if vp == 1 else reflect(c)


def run(V, c):
    p, d, q, pred, lab = c
    maxb = (len(pred) if pred is not None else 0) + 1
    status, b = trace(V, p, d, q, maxb)
    issues = []
    if status != 'hit':
        issues.append(status)
    elif pred is not None and [(kd, (F(x), F(y))) for kd, (x, y) in pred] != b:
        issues.append('bounce sequence differs from prediction')
    if pred is not None:
        # straight segments must stay in open band 1<y<2 between chambers:
        # implied by no corner hit + reaching target; nothing more to check.
        pass
    return status, b, issues


print("d200 checks: three-chamber room X=Y=3k+1, D=3k+4, k=6..40")
print()
total_pairs = 0
bad = []
for k in range(6, 41):
    D = 3 * k + 4
    X = D - 3
    V = room(D)
    A = area2(V) // 2
    W = len(V)
    # family identification
    reflex = 0
    n = len(V)
    for i in range(n):
        a, b, c = V[i - 1], V[i], V[(i + 1) % n]
        cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        reflex += cross < 0
    assert A == 27 + 2 * X == 29 + 6 * k and W == 20 and reflex == 8
    assert len(set(V)) == 20
    # interior lattice points
    pts = [(x, y) for x in range(0, 2 * D + 4) for y in range(0, 4)
           if not on_boundary(V, (x, y)) and inside(V, (x, y))]
    marks = [(i, u, v) for i in range(3) for u in (1, 2) for v in (1, 2)]
    assert sorted(pts) == sorted((i * D + u, v) for i, u, v in marks)

    # Part 1 arithmetic: unfolded midpoint abscissas are the middle mouths
    for u in (1, 2):
        assert (-u + 2 * D + u) == 2 * D             # left reversal midpoint D
        assert (u + 2 * (2 * D + 3) - (2 * D + u)) == 2 * (D + 3)
        assert (u + 2 * D + u) == 2 * (D + u)        # zero reversal midpoint D+u
    # Part 2 arithmetic
    L = F(D) - F(1, 2)
    for u in (1, 2):
        a = F(u) - F(1, 2)
        assert (a + L) % 3 == u % 3 and (a + 2 * L) % 6 == a + 1
        assert D + u - F(1, 2) > D and F(D) + u + F(1, 2) + L == 2 * D + u

    labels = {}
    for P, Q in combinations(marks, 2):
        c = prescribe(D, k, P, Q)
        status, b, issues = run(V, c)
        # also trace the reversed construction for straight/one-bounce cases
        labels[c[4]] = labels.get(c[4], 0) + 1
        total_pairs += 1
        if issues:
            bad.append((k, P, Q, c[4], issues, b[-1:] if b else b))
    c = one_reversal_21(D)
    status, b, issues = run(V, c)
    if issues:
        bad.append((k, 'one-rev', '', c[4], issues, b[-1:]))
    if k in (6, 7, 20, 40):
        nb = len(trace(V, *distinct(D, 1, 2)[:3], 10 ** 6)[1])
        print("  k=%d D=%d X=Y=%d area=%d W=%d reflex=%d marks=12 pairs=66 %s; "
              "pocket bounces=%d (2k+3=%d), distinct(1,2) bounces=%d"
              % (k, D, X, A, W, reflex, dict(sorted(labels.items())),
                 len(trace(V, *pocket(D, k, 1)[:3], 10 ** 6)[1]), 2 * k + 3, nb))

print()
print("pairs traced:", total_pairs, "(66 unordered pairs x 35 rooms)")
print("one-reversal (2,1) remark traced for each k")
print("failures (corner hit, wall miss, target miss, prediction mismatch):", len(bad))
for row in bad[:20]:
    print("  ", row)

# Scope note: the adjacent construction at k=0 (D=4), recorded analytically.
D0 = 4
m = F(1 + D0 + 1, 2)
print()
print("scope: k=0 (D=4) adjacent u=v=1 bounce abscissa =", m,
      "= corridor end x=3, a corner; the note needs k>=1 for this step")
# Tracer controls: two named rays that must fail.
st, b = trace(room(22), (1, 1), (1, 0), (45, 1), 5)
print("control 1 (k=6, horizontal ray from (1,1) along y=1):", st, b[-1:])
st0, b0 = trace(room(4), (1, 1), (2, 1), (5, 1), 5)
print("control 2 (k=0, adjacent u=v=1 ray toward (3,2)):", st0, b0[-1:])
print("CPU seconds: %.2f" % (time.process_time() - T0))
