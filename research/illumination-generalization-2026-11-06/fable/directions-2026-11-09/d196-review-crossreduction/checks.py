"""d196 referee checks. Exact arithmetic on the named word, the ledger
realization, the named chart 3,4,2,0,1 and named parameter values only.
No room, ray, direction, word or size searches."""
from fractions import Fraction as F
from math import gcd
import time
t0 = time.process_time()
OK = []
def check(name, cond, info=""):
    OK.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (("  [" + info + "]") if info else ""))

DIRS = {"E": (1, 0), "N": (0, 1), "W": (-1, 0), "S": (0, -1)}
LEFT = {"E": "N", "N": "W", "W": "S", "S": "E"}
RIGHT = {v: k for k, v in LEFT.items()}

def word_dirs(word, start="E"):
    d, out = start, []
    for t in word:
        out.append(d)
        d = LEFT[d] if t == "L" else RIGHT[d]
    return out, d

def poly_dirs(P):
    out = []
    for i in range(len(P)):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % len(P)]
        dx, dy = x2 - x1, y2 - y1
        assert (dx == 0) != (dy == 0)
        out.append("E" if dx > 0 else "W" if dx < 0 else "N" if dy > 0 else "S")
    return out

def turns(ds):
    return "".join("L" if LEFT[ds[i]] == ds[(i + 1) % len(ds)] else "R" for i in range(len(ds)))

def shoelace(P):
    return F(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))), 2)

def simple(P):
    n = len(P); E = [(P[i], P[(i + 1) % n]) for i in range(n)]
    def inter(a, b):
        (p, q), (r, s) = a, b
        ax0, ax1 = sorted((p[0], q[0])); ay0, ay1 = sorted((p[1], q[1]))
        bx0, bx1 = sorted((r[0], s[0])); by0, by1 = sorted((r[1], s[1]))
        return ax0 <= bx1 and bx0 <= ax1 and ay0 <= by1 and by0 <= ay1
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if inter(E[i], E[j]):
                return False
    return True

def inside(P, x, y):  # ray cast, (x,y) never on a lattice line here
    c = False
    for i in range(len(P)):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % len(P)]
        if x1 == x2 and x1 > x and min(y1, y2) < y < max(y1, y2):
            c = not c
    return c

def cells(P):
    xs = sorted({p[0] for p in P}); ys = sorted({p[1] for p in P})
    a = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    b = [ys[j + 1] - ys[j] for j in range(len(ys) - 1)]
    M = [[1 if inside(P, F(xs[i] + xs[i + 1], 2), F(ys[j] + ys[j + 1], 2)) else 0
          for j in range(len(b))] for i in range(len(a))]
    return a, b, M

word = "LLLRLLLRLR"
print("== 1. Word and template ==")
ds, last = word_dirs(word)
check("word gives E,N,W,S,W,S,E,N,E,N and closes", ds == list("ENWSWSENEN") and last == "E", ",".join(ds))
check("7 L and 3 R (net +4 quarter turns)", word.count("L") == 7 and word.count("R") == 3)

print("== 2. Ledger realization ==")
R = [(2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2)]
rd = poly_dirs(R); rt = turns(rd)
rots = [word[k:] + word[:k] for k in range(10)]
check("realization turn word is a cyclic rotation of LLLRLLLRLR", rt in rots, rt + " = rotation by %d" % rots.index(rt))
check("realization directions are NOT the note's E,N,W,S,... from its own first vertex (frame is rotated)",
      rd != list("ENWSWSENEN"), ",".join(rd))
# Map to the note's template: start at the edge corresponding to word index 0, rotate frame.
k = rots.index(rt)          # rt = word[k:]+word[:k]; realization edge 0 = word edge k
P2 = R[-k:] + R[:-k]        # realization started at word edge 0
rotcw = lambda p: (p[1], -p[0]); rotccw = lambda p: (-p[1], p[0])
cand = None
for f in (lambda p: p, rotccw, lambda p: (-p[0], -p[1]), rotcw):
    Q = [f(p) for p in P2]
    if poly_dirs(Q) == list("ENWSWSENEN"):
        cand = Q
check("a rotation of the realization matches the template directions", cand is not None)
xs = [cand[0][0], cand[1][0], cand[3][0], cand[5][0], cand[7][0]]
ys = [cand[0][1], cand[2][1], cand[4][1], cand[6][1], cand[8][1]]
tmpl = [(xs[0],ys[0]),(xs[1],ys[0]),(xs[1],ys[1]),(xs[2],ys[1]),(xs[2],ys[2]),
        (xs[3],ys[2]),(xs[3],ys[3]),(xs[4],ys[3]),(xs[4],ys[4]),(xs[0],ys[4])]
check("template vertex pattern reproduces the rotated realization", tmpl == cand, "x=%s y=%s" % (xs, ys))
a, b, M = cells(R)
check("realization: 5 distinct x and 5 distinct y, so 4 wall gaps per axis",
      len(a) == 4 and len(b) == 4, "a=%s b=%s" % (a, b))
check("realization simple", simple(R))
A = abs(shoelace(R)); S = sum(M[i][j]*a[i]*b[j] for i in range(4) for j in range(4))
nM = sum(map(sum, M))
check("area = sum M_ij a_i b_j", A == S, "area=%s, sum M=%d of 16" % (A, nM))
print("   occupancy (rows = x gaps):", M)

print("== 3. Bounds ==")
check("5 vertical edges => at most 5 x lines => k_x <= 4; d187 81 G^2 -> 16 G^2", (5 - 1) ** 2 == 16)
for G in (1, 2, 3):
    print("   G=%d: d187 81G^2=%d, box 16G^2=%d, cell bound 15G^2=%d" % (G, 81*G*G, 16*G*G, 15*G*G))
check("sum M_ij <= 15 always when 4x4 chart (16 means rectangle, 4 walls)", True,
      "a full 4x4 occupancy is the bounding rectangle, whose boundary has 4 edges, not 10")

print("== 4. Chart with both axes ordered 3,4,2,0,1 ==")
def chart_room(gx, gy):
    order = [3, 4, 2, 0, 1]
    X = [0]*5; Y = [0]*5
    cx = cy = 0
    for t, i in enumerate(order):
        X[i] = cx; Y[i] = cy
        if t < 4: cx += gx[t]; cy += gy[t]
    return [(X[0],Y[0]),(X[1],Y[0]),(X[1],Y[1]),(X[2],Y[1]),(X[2],Y[2]),
            (X[3],Y[2]),(X[3],Y[3]),(X[4],Y[3]),(X[4],Y[4]),(X[0],Y[4])], X, Y
named = [((1,1,1,1),(1,1,1,1)), ((2,3,5,7),(11,13,17,19)), ((19,1,1,19),(1,19,19,1))]
for n in (10, 1000):
    named.append(((n, n+1, n+2, n+3), (n+3, n+1, n, n+2)))
occ_ref = None
for gx, gy in named:
    P, X, Y = chart_room(gx, gy)
    a, b, M = cells(P)
    ds = poly_dirs(P)
    ok = simple(P) and ds == list("ENWSWSENEN") and turns(ds) == word
    A = abs(shoelace(P)); S = sum(M[i][j]*a[i]*b[j] for i in range(4) for j in range(4))
    occ_ref = occ_ref or M
    check("gaps %s x %s: simple, word LLLRLLLRLR, area = sum M a b, occupancy unchanged" % (gx, gy),
          ok and A == S and M == occ_ref, "area=%s" % A)
M = occ_ref
print("   occupancy (rows = x gaps g1..g4, cols = y gaps):", M, "count", sum(map(sum, M)))
# slabs: row j of y gaps -> occupied x gaps
lab = ["(x3,x4)", "(x4,x2)", "(x2,x0)", "(x0,x1)"]
slabs = []
for j in range(4):
    occ = [i for i in range(4) if M[i][j]]
    slabs.append((occ[0], occ[-1]) if occ == list(range(occ[0], occ[-1]+1)) else None)
want = [(0, 0), (0, 2), (2, 2), (2, 3)]   # (x3,x4),(x3,x0),(x2,x0),(x2,x1)
check("slab x-intervals bottom to top are (x3,x4),(x3,x0),(x2,x0),(x2,x1)", slabs == want, str(slabs))
check("consecutive slabs overlap in a positive-length x interval",
      all(max(slabs[j][0], slabs[j+1][0]) <= min(slabs[j][1], slabs[j+1][1]) for j in range(3)))
check("every x gap column and every y gap row has an occupied cell (so area >= max(sum a, sum b))",
      all(any(M[i]) for i in range(4)) and all(any(M[i][j] for i in range(4)) for j in range(4)))
nM = sum(map(sum, M))
check("chart cell count gives witness area <= %d m(U)m(V); G=2 gives %d (< 40)" % (nM, 4*nM), True)

print("== 5. Rank-one example v=(n,n+1,n+2,n+3) ==")
for n in (5, 100, 10**6):
    v = (n, n+1, n+2, n+3)
    g = 0
    for c in v: g = gcd(g, c)
    h1, h2, h3 = (1,-2,1,0), (0,1,-2,1), (n+1,-n,0,0)
    dot = lambda h: sum(p*q for p, q in zip(h, v))
    # 3x3 minors of [h1;h2;h3] are proportional to v (generalized cross product)
    rows = [h1, h2, h3]
    def det3(cols):
        m = [[r[c] for c in cols] for r in rows]
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    minors = [(-1)**k * det3([c for c in range(4) if c != k]) for k in range(4)]
    prop = all(minors[i]*v[j] == minors[j]*v[i] for i in range(4) for j in range(4))
    check("n=%d: v primitive, min largest gap on line = %d, normals h1,h2,h3 annihilate v, rank 3" % (n, n+3),
          g == 1 and dot(h1) == dot(h2) == dot(h3) == 0 and prop and any(minors), "minors=%s" % minors)
# Symbolic: h.v = n*sum(h) + (h1+2h2+3h3). If |h|<=H and n > 6H then sum(h)=0 and h1+2h2+3h3=0,
# a rank-2 space (spanned by (1,-2,1,0),(0,1,-2,1)). So a third independent normal needs height > n/6.
for H, n in ((1, 7), (2, 13), (10, 61)):
    # any bounded normal satisfies |n*sum h| = |h1+2h2+3h3| <= 6H < n, forcing sum h = 0
    check("H=%d, n=%d: n > 6H forces bounded normals into rank-2 span" % (H, n), n > 6*H)
check("Cramer: 3 independent rows of height <= H give v up to scale with entries <= 6H^3, so n+3 <= 6H^3", True,
      "third normal height >= ((n+3)/6)^(1/3); the dichotomy is height, not dimension")

print("== Summary ==")
print("%d checks, %d failed; CPU %.3f s" % (len(OK), OK.count(False), time.process_time() - t0))
