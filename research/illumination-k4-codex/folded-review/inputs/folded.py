"""Enumerate folded parity rooms: m reflected copies of a parity base glued along full walls.
Geometry on quarter-triangles (unit squares cut by both diagonals), exact integer arithmetic (coords x4)."""
import sys, itertools, os
LIM = int(os.environ.get("LIM", 21))
from fractions import Fraction as F

def cls(x, y): return (x & 1) + (y & 1)  # 0 = A

def parse(line):
    t = line.split(); W = int(t[0])
    return W, [tuple(map(int, p.split(','))) for p in t[2:]]

def quarters_of_poly(V):
    xs = [p[0] for p in V]; ys = [p[1] for p in V]
    Q = set()
    for x in range(min(xs), max(xs)):
        for y in range(min(ys), max(ys)):
            for q in range(4):  # 0 bottom,1 right,2 top,3 left
                cx, cy = [(F(1,2),F(1,4)),(F(3,4),F(1,2)),(F(1,2),F(3,4)),(F(1,4),F(1,2))][q]
                if inside(V, x+cx, y+cy): Q.add((x, y, q))
    return Q

def inside(V, px, py):
    c = False; n = len(V)
    for i in range(n):
        (ax, ay), (bx, by) = V[i], V[(i+1) % n]
        if (ay > py) != (by > py):
            xi = ax + F(py-ay)*(bx-ax)/(by-ay)
            if px < xi: c = not c
    return c

# affine maps on Z^2: (M, v) with M a signed permutation / diagonal reflection matrix
def apply(g, p): (a,b,c,d),(e,f) = g; return (a*p[0]+b*p[1]+e, c*p[0]+d*p[1]+f)
def compose(h, g):  # h after g
    (a,b,c,d),(e,f) = h; (A,B,C,D),(E,Fv) = g
    return ((a*A+b*C, a*B+b*D, c*A+d*C, c*B+d*D), (a*E+b*Fv+e, c*E+d*Fv+f))
def refl(p, q):  # reflection across line through lattice points p,q (axis or diagonal)
    dx, dy = q[0]-p[0], q[1]-p[1]
    if dx == 0: return ((-1,0,0,1),(2*p[0],0))
    if dy == 0: return ((1,0,0,-1),(0,2*p[1]))
    if dx*dy > 0: k = p[1]-p[0]; return ((0,1,1,0),(-k,k))      # y = x + k
    k = p[1]+p[0]; return ((0,-1,-1,0),(k,k))                    # y = -x + k
ID = ((1,0,0,1),(0,0))

def qverts(t):
    x, y, q = t; c = (F(2*x+1,2), F(2*y+1,2))
    corners = [(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
    return c, corners[q], corners[(q+1) % 4]
def qmap(g, t):
    c, a, b = qverts(t); c2 = apply(g, c)
    x, y = int(c2[0] - F(1,2)), int(c2[1] - F(1,2))
    a2 = apply(g, a); mid = (F(a2[0]+apply(g,b)[0],2), F(a2[1]+apply(g,b)[1],2))
    dx, dy = mid[0]-c2[0], mid[1]-c2[1]
    q = {(0,-1):0,(1,0):1,(0,1):2,(-1,0):3}[(int(2*dx), int(2*dy))]
    return (x, y, q)

def boundary(Qs):
    """Return directed boundary edges (half-unit outer edges + diagonal halves) of a quarter set."""
    E = {}
    for t in Qs:
        c, a, b = qverts(t)
        for (u, v) in ((a, b), (b, c), (c, a)):   # CCW triangle edges
            key = (min(u,v), max(u,v))
            E[key] = None if key in E else (u, v)
    return [e for e in E.values() if e is not None]

def polygon(Qs):
    """Trace boundary; return CCW corner list or None if not one strictly simple cycle."""
    edges = boundary(Qs); nxt = {}
    for u, v in edges:
        if u in nxt: return None   # vertex with two outgoing edges: pinch
        nxt[u] = v
    start = edges[0][0]; cyc = [start]; u = nxt[start]
    while u != start: cyc.append(u); u = nxt[u]
    if len(cyc) != len(edges): return None   # more than one cycle (hole or disconnected)
    n = len(cyc); out = []
    for i in range(n):
        p, q, r = cyc[i-1], cyc[i], cyc[(i+1) % n]
        if (q[0]-p[0])*(r[1]-q[1]) - (q[1]-p[1])*(r[0]-q[0]) != 0: out.append(q)
    return out

def around(p):  # quarters incident to lattice point p
    x, y = p
    return {(x,y,0),(x,y,3),(x-1,y,0),(x-1,y,1),(x-1,y-1,1),(x-1,y-1,2),(x,y-1,2),(x,y-1,3)}

def run(line, mmax_rule):
    W, V = parse(line)
    marks = []
    P0 = quarters_of_poly(V)
    pts = {(x, y) for (x, y, q) in P0} | {(x+1, y+1) for (x, y, q) in P0}
    xs = range(min(p[0] for p in V), max(p[0] for p in V)+1); ys = range(min(p[1] for p in V), max(p[1] for p in V)+1)
    Vs = set(V)
    for x in xs:
        for y in ys:
            if cls(x, y) == 0 and (x, y) not in Vs and (around((x, y)) & P0): marks.append((x, y))
    walls = [(V[i], V[(i+1) % len(V)]) for i in range(len(V))]
    res = []
    M = max(m for m in (1, 2, 3, 4, 5, 6) if m*(W-4)+4 <= LIM) if W > 4 else 6
    seen = set()
    def key(gs): return frozenset(gs)
    def grow(gs, cells):
        k = key(gs)
        if k in seen: return
        seen.add(k)
        if len(gs) >= 2: evaluate(gs, cells)
        if len(gs) == M: return
        for g in list(gs):
            for (p, q) in walls:
                h = compose(refl(apply(g, p), apply(g, q)), g)
                if h in gs: continue
                C = {qmap(h, t) for t in P0}
                if C & cells: continue
                grow(gs + [h], cells | C)
    def evaluate(gs, cells):
        poly = polygon(cells)
        if poly is None: return
        # fold consistency: every edge shared by two copies must be a mirror seam
        owner = {}
        for i, g in enumerate(gs):
            for t in P0: owner[qmap(g, t)] = i
        bad = False
        Es = {}
        for t, i in owner.items():
            c, a, b = qverts(t)
            for (u, v) in ((a, b), (b, c), (c, a)):
                Es.setdefault((min(u,v), max(u,v)), []).append(i)
        for (u, v), own in Es.items():
            if len(own) == 2 and own[0] != own[1]:
                i, j = own; r = refl(u, v) if u[0]==v[0] or u[1]==v[1] or abs(u[0]-v[0])==abs(u[1]-v[1]) else None
                if r is None or compose(r, gs[i]) != gs[j]: bad = True; break
        if bad: return
        Wq = len(poly)
        lifts = {}
        for i, g in enumerate(gs):
            for mk in marks:
                p = apply(g, mk)
                if around(p) <= cells: lifts.setdefault(mk, set()).add(p)
        ok = [(a, b) for a, b in itertools.permutations(marks, 2) if a in lifts and b in lifts]
        if ok and Wq <= LIM:
            res.append((Wq, len(gs), poly, ok, lifts))
    grow([ID], set(P0))
    return W, V, res

if __name__ == '__main__':
    for line in open(sys.argv[1]):
        W, V, res = run(line, None)
        for Wq, m, poly, ok, lifts in res:
            print('HIT', W, V, 'm', m, 'Wq', Wq, 'poly', poly, 'pairs', ok, 'lifts', {k: sorted(v) for k, v in lifts.items()})
        print('base', W, len(res), file=sys.stderr)
