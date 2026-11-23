"""Independent re-run of the d22 slice z = 1, delta = 4 (no code shared with d21/d22).

Cover of D(L(A,B)): edge permutations g[E] (front sheet k -> back sheet g[E][k]).
Edges in boundary order from the reflex corner: E0..E5, g[E0] = g[E5] = id.
Pole i (1..5) sits between E(i-1) and E(i); h_i = g[Ei]^-1 g[E(i-1)].
"""
import sys
from itertools import permutations, product, combinations
from math import gcd

D = 4
ID = tuple(range(D))
PERMS = list(permutations(range(D)))
def mul(a, b): return tuple(a[b[k]] for k in range(D))          # a after b
def inv(a):
    r = [0] * D
    for i, x in enumerate(a): r[x] = i
    return tuple(r)
def cycles(a):
    seen, out = set(), []
    for i in range(D):
        if i not in seen:
            c, j = [], i
            while j not in seen: seen.add(j); c.append(j); j = a[j]
            out.append(tuple(c))
    return out
def ctype(a): return tuple(sorted(len(c) for c in cycles(a)))
def transitive(hs):
    comp = {0}; stack = [0]
    while stack:
        k = stack.pop()
        for h in hs:
            if h[k] not in comp: comp.add(h[k]); stack.append(h[k])
    return len(comp) == D
def canon(a):   # a: tuple of perms, up to simultaneous conjugation
    return min(tuple(mul(mul(c, x), inv(c)) for x in a) for c in PERMS)
def canon_pair(a, pr):
    return min((tuple(mul(mul(c, x), inv(c)) for x in a), tuple(sorted(c[k] for k in pr))) for c in PERMS)

def hs_of(g):   # g = (g0..g5); returns h_1..h_5
    return tuple(mul(inv(g[i]), g[i - 1]) for i in range(1, 6))

# ---- enumeration
covers = {}
for g1, g2, g3, g4 in product(PERMS, repeat=4):
    g = (ID, g1, g2, g3, g4, ID)
    hs = hs_of(g)
    ts = [ctype(h) for h in hs]
    if any(max(t) > 3 for t in ts): continue
    if sum(D - len(t) for t in ts) != 2 * D - 2: continue
    if sum(t.count(3) for t in ts) > 8 - D: continue
    if not transitive(hs): continue
    a = tuple(reversed(hs))               # a_1..a_5 = h_5..h_1, product a_1...a_5 = 1
    covers.setdefault(canon(a), g)
print("covers", len(covers))

def braid(a, i):
    a = list(a); x, y = a[i], a[i + 1]
    a[i], a[i + 1] = mul(mul(x, y), inv(x)), x
    return tuple(a)
def orbits(nodes, moves):
    nodes = set(nodes); n = 0; sizes = []
    while nodes:
        s = nodes.pop(); n += 1; stack = [s]; sz = 1
        while stack:
            u = stack.pop()
            for v in moves(u):
                if v in nodes: nodes.discard(v); stack.append(v); sz += 1
        sizes.append(sz)
    return n, sorted(sizes)
print("braid orbits", orbits(covers, lambda a: [canon(braid(a, i)) for i in range(4)]))

# P1 nodes: (cover, position j whose type is 2+2)
p1 = [(a, j) for a in covers for j in range(5) if ctype(a[j]) == (2, 2)]
def p1moves(u):
    a, j = u; out = []
    for i in range(4):
        nj = i if j == i + 1 else i + 1 if j == i else j
        out.append((canon(braid(a, i)), nj))
    return out
print("P1 nodes", len(p1), "families", orbits(p1, p1moves))
# P3 nodes: (cover, sheet pair), per cover without quotient by automorphisms, as d22 counts
print("P3 nodes (6 per cover)", 6 * len(covers))
p3 = {canon_pair(a, pr) for a in covers for pr in combinations(range(D), 2)}
def p3moves(u):
    a, pr = u; out = [canon_pair(braid(a, i), pr) for i in range(4)]
    out += [canon_pair(a, tuple(x[k] for k in pr)) for x in a]
    return out
print("P3 nodes mod conj", len(p3), "families", orbits(p3, p3moves))

# ---- geometry on L(A,B)
class Room:
    def __init__(s, A, B):
        s.A, s.B = A, B
        s.cells = {(i, 0) for i in range(A)} | {(0, j) for j in range(B)}
        s.poles = {(1, B): 1, (0, B): 2, (0, 0): 3, (A, 0): 4, (A, 1): 5}
    def wall(s, cell, axis, sgn):          # edge index of the wall left through
        i, j = cell
        if axis == 0: return 2 if sgn < 0 else (4 if j == 0 else 0)
        return 3 if sgn < 0 else (5 if j == 0 else 1)
    def edge_at(s, pt):                     # edge through a non-corner boundary lattice point
        x, y = pt
        if y == 0: return 3, 1
        if x == 0: return 2, 0
        if y == 1 and x > 1: return 5, 1
        if x == 1 and y > 1: return 0, 0
        raise ValueError(pt)

def step(R, g, pt, sx, sy, p, q, face, k):
    """Unit-time flight from lattice point pt, direction (sx*p, sy*q). Returns arrival."""
    cell = (pt[0] - (sx < 0), pt[1] - (sy < 0))
    if cell not in R.cells: return None
    ev = sorted([(a * q, 0) for a in range(1, p)] + [(b * p, 1) for b in range(1, q)])
    for _, axis in ev:
        sgn = sx if axis == 0 else sy
        nc = (cell[0] + sgn, cell[1]) if axis == 0 else (cell[0], cell[1] + sgn)
        if nc in R.cells: cell = nc
        else:
            E = R.wall(cell, axis, sgn)
            k = g[E][k] if face == 0 else inv(g[E])[k]
            face ^= 1
            if axis == 0: sx = -sx
            else: sy = -sy
    return (cell[0] + (sx > 0), cell[1] + (sy > 0)), sx, sy, face, k

def point_at_pole(g, hs, i, face, k):
    """Cycle (as frozenset of front labels) of the X-point over pole i."""
    f = k if face == 0 else inv(g[i])[k]
    c = [f]; j = hs[i - 1][f]
    while j != f: c.append(j); j = hs[i - 1][j]
    return frozenset(c)

def fly(R, g, hs, pt, sx, sy, p, q, face, k, target):
    """target = ('pole', i, cycle) or ('wall', pt, frontlabel). True if the ray reaches it."""
    seen = set()
    while True:
        r = step(R, g, pt, sx, sy, p, q, face, k)
        if r is None: return False
        pt, sx, sy, face, k = r
        if pt == (1, 1): return False
        if pt in R.poles:
            i = R.poles[pt]; c = point_at_pole(g, hs, i, face, k)
            if target[0] == 'pole' and target[1] == i and c == target[2]: return True
            if len(c) != 2: return False
            f = k if face == 0 else inv(g[i])[k]
            f2 = hs[i - 1][f]
            k = f2 if face == 0 else g[i][f2]
            sx, sy = -sx, -sy
        else:
            E, axis = R.edge_at(pt)
            f = k if face == 0 else inv(g[E])[k]
            if target[0] == 'wall' and target[1] == pt and f == target[2]: return True
            k = g[E][k] if face == 0 else inv(g[E])[k]
            face ^= 1
            if axis == 0: sx = -sx
            else: sy = -sy
        st = (pt, sx, sy, face, k)
        if st in seen: return False
        seen.add(st)

DIRS = lambda N: [(p, q) for p in range(1, N) for q in range(1, N - p + 1) if gcd(p, q) == 1]
INTO = lambda R: {(1, R.B): (-1, -1), (0, R.B): (1, -1), (0, 0): (1, 1), (R.A, 0): (-1, 1), (R.A, 1): (-1, -1)}

def edge_walk(R, g, hs, i, E, f, target):
    """Walk along wall E from pole i with front label f; bounce at 2-cycles."""
    ends = {0: (None, 1), 1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, None)}[E]
    seen = set()
    while True:
        j = ends[1] if ends[0] == i else ends[0]
        if j is None: return False                      # reflex corner
        c = point_at_pole(g, hs, j, 0, f)
        if target[0] == 'pole' and target[1] == j and c == target[2]: return True
        if len(c) != 2: return False
        f = hs[j - 1][f]; i = j
        if (i, f) in seen: return False
        seen.add((i, f))

def p1_lit(R, g, i, N):
    hs = hs_of(g)
    cyc = [frozenset(c) for c in cycles(hs[i - 1]) if len(c) == 2]
    S, T = cyc
    pt = [P for P, n in R.poles.items() if n == i][0]
    sx, sy = INTO(R)[pt]
    tgt = ('pole', i, T)
    for a in S:
        for E in (i - 1, i):
            if edge_walk(R, g, hs, i, E, a, tgt): return ('edge', E)
        for (p, q) in DIRS(N):
            for face, k in ((0, a), (1, g[i][a])):
                if fly(R, g, hs, pt, sx, sy, p, q, face, k, tgt): return (p, q)
    return None

def p3_lit(R, g, pr, N):
    hs = hs_of(g)
    walls = [(x, 0) for x in range(1, R.A)] + [(0, y) for y in range(1, R.B)]
    for W in walls:
        E, axis = R.edge_at(W)
        for k1, k2 in (pr, pr[::-1]):
            tgt = ('wall', W, k2)
            for (p, q) in DIRS(N):
                for s in (1, -1):
                    sx, sy = (s, 1) if axis == 1 else (1, s)
                    for face, k in ((0, k1), (1, g[E][k1])):
                        if fly(R, g, hs, W, sx, sy, p, q, face, k, tgt): return (W, p, q)
    return None

rooms = [Room(2, 2), Room(3, 2), Room(2, 3)]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
dark1 = []
for a, j in p1:
    g = covers[a]; i = 5 - j                      # a_{j+1} = h_{5-j}
    if not any(p1_lit(R, g, i, N) for R in rooms): dark1.append((a, j))
print("P1 nodes with no segment (p+q <= %d, three bases):" % N, len(dark1))
one_pole = [(a, j) for a, j in p1 if sum(1 for x in a if 2 in ctype(x)) == 1]
print("P1 nodes whose cover has 2-cycles over one pole only (Lemma A):", len(one_pole),
      "equal to unlit set:", set(one_pole) == set(dark1))
print("type multisets of unlit:", sorted({tuple(sorted(ctype(x) for x in a)) for a, _ in dark1}))
dark3 = 0
for a, g in covers.items():
    for pr in combinations(range(D), 2):
        if not any(p3_lit(R, g, pr, N) for R in rooms): dark3 += 1
print("P3 nodes with no segment (wall-lattice y, p+q <= %d, three bases):" % N, dark3, "of", 6 * len(covers))
