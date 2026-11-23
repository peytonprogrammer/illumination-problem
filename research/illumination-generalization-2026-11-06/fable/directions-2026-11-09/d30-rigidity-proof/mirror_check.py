"""Exact checks for the mirror-double rooms of rigidity.md (no search over rooms).

Builds rooms from reflected copies of the five-square staircase Q, verifies
strict simplicity, wall count, the run, the fold map to Q, and traces every
lattice chain from S with |q|,|p| <= B (bounded witness check; the proof of
darkness is the fold argument, not this trace).
"""
import sys
from fractions import Fraction as Fr
from math import gcd

Q = [(0,0),(1,0),(1,1),(2,1),(2,2)]          # cells [i,i+1]x[j,j+1]
rx = lambda a: (lambda c: (2*a-1-c[0], c[1]))  # reflect cells in line x=a
ry = lambda b: (lambda c: (c[0], 2*b-1-c[1]))  # reflect cells in line y=b
px = lambda a: (lambda P: (2*a-P[0], P[1]))    # same for points
py = lambda b: (lambda P: (P[0], 2*b-P[1]))

def room(copies):
    """copies: list of (cell map, point map). Returns cells and fold map point->Q point."""
    cells, fold = set(), {}
    for cm, pm in copies:
        for c in Q:
            d = cm(c); assert d not in cells, "overlap"; cells.add(d)
        for x in range(0,4):
            for y in range(0,4):
                if any((x-a,y-b) in Q for a in (0,1) for b in (0,1)):
                    Pt = pm((x,y))
                    assert fold.get(Pt,(x,y)) == (x,y), "fold map inconsistent"
                    fold[Pt] = (x,y)
    return cells, fold

def quad(cells, P):
    x,y = P
    return {(sx,sy): ((x + (0 if sx>0 else -1), y + (0 if sy>0 else -1)) in cells)
            for sx in (1,-1) for sy in (1,-1)}

def ptype(cells, P):
    q = quad(cells,P); n = sum(q.values())
    if n == 0: return 'out'
    if n == 4: return 'int'
    if n == 1: return 'convex'
    if n == 3: return 'reflex'
    if q[(1,1)] and q[(-1,-1)] or q[(1,-1)] and q[(-1,1)]: return 'PINCH'
    return 'flat'

def stats(cells):
    pts = {(x+a,y+b) for (x,y) in cells for a in (0,1) for b in (0,1)}
    t = {P: ptype(cells,P) for P in pts}
    assert 'PINCH' not in t.values()
    # connectivity
    seen, st = set(), [next(iter(cells))]
    while st:
        c = st.pop()
        if c in seen: continue
        seen.add(c)
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            n = (c[0]+d[0], c[1]+d[1])
            if n in cells: st.append(n)
    assert seen == cells
    cv = sum(v=='convex' for v in t.values()); rf = sum(v=='reflex' for v in t.values())
    assert cv - rf == 4, "not simply connected"
    return t, cv+rf, rf

def trace(cells, t, S, T, d, maxsteps=100000):
    """Billiard from lattice point S in direction d; True if T reached before a corner."""
    x, y = Fr(S[0]), Fr(S[1]); dx, dy = d
    start = (S, d); first = True
    for _ in range(maxsteps):
        onx, ony = x.denominator == 1, y.denominator == 1
        if onx and ony:
            Pt = (int(x), int(y))
            if not first:
                if Pt == T: return True
                if (Pt,(dx,dy)) == start: return False
            ty = t.get(Pt,'out')
            if ty in ('convex','reflex'): return False
            sx = (dx>0)-(dx<0); sy = (dy>0)-(dy<0)
            if sx == 0 or sy == 0:      # axis-parallel
                q = quad(cells,Pt)
                ahead = [q[(a,b)] for a in (1,-1) for b in (1,-1)
                         if (sx==0 or a==sx) and (sy==0 or b==sy)]
                if all(ahead): pass
                elif not any(ahead): dx, dy = -dx, -dy
                else: return False       # slides along a wall: treat as blocked
            elif ty == 'flat':
                q = quad(cells,Pt)
                if not q[(sx,sy)]:
                    if q[(sx,-sy)]: dy = -dy
                    elif q[(-sx,sy)]: dx = -dx
                    else: return False
        elif onx and dx != 0:
            cx = int(x) if dx > 0 else int(x)-1
            cy = y.numerator // y.denominator
            if (cx,cy) not in cells: dx = -dx
        elif ony and dy != 0:
            cy = int(y) if dy > 0 else int(y)-1
            cx = x.numerator // x.denominator
            if (cx,cy) not in cells: dy = -dy
        first = False
        # advance to next grid line
        ts = []
        if dx: 
            nx = (x.numerator//x.denominator + 1) if dx>0 else -((-x).numerator//(-x).denominator + 1)
            ts.append((nx - x)/dx)
        if dy:
            ny = (y.numerator//y.denominator + 1) if dy>0 else -((-y).numerator//(-y).denominator + 1)
            ts.append((ny - y)/dy)
        tt = min(ts); x += tt*dx; y += tt*dy
    raise RuntimeError("step bound")

def lit(cells, t, S, T, B):
    for q in range(0,B+1):
        for p in range(0,B+1):
            if gcd(q,p) != 1: continue
            for sx in (1,-1):
                for sy in (1,-1):
                    if (q==0 and sx<0) or (p==0 and sy<0): continue
                    if trace(cells,t,S,T,(sx*q,sy*p)): return (sx*q,sy*p)
    return None

def stretch_y(cells, row, g):
    """Replace cell row `row` by g copies (g>=0); returns cells."""
    out = set()
    for (x,y) in cells:
        if y < row: out.add((x,y))
        elif y == row: out.update((x,row+k) for k in range(g))
        else: out.add((x,y+g-1))
    return out

ident = (lambda c: c, lambda P: P)
Q1 = (ry(0), py(0))
B = int(sys.argv[1]) if len(sys.argv) > 1 else 30

# P6: Q0, Q1 = mirror in y=0, Q5 = mirror of Q1 in x=3, Q0' = mirror of Q0 in y=3
P6 = [ident, Q1, (lambda c: rx(3)(ry(0)(c)), lambda P: px(3)(py(0)(P))), (ry(3), py(3))]
cells, fold = room(P6)
t, W, r = stats(cells)
S, T = (1,0), (3,-2)
print("P6 cells", len(cells), "W", W, "r", r, "S", t[S], fold[S], "T", t[T], fold[T])
rows = lambda c, y: sorted(x for (x,yy) in c if yy == y)
print(" rows y=2,3:", rows(cells,2), rows(cells,3), "points on y=3:", {P:v for P,v in t.items() if P[1]==3})
print(" transparent:", sorted((P,v,fold[P]) for P,v in t.items() if v in ('flat','int')))
print(" witness with |q|,|p| <=", B, ":", lit(cells,t,S,T,B))
# the gap line: rows 2 and 3 form the run; total run height g (g=2 is P6)
for g in (0,1,3,4,5,6):
    c1 = stretch_y(stretch_y(cells,3,0),2,g) if g != 2 else cells
    try:
        t1, W1, r1 = stats(c1)
    except AssertionError as e:
        print(" g =", g, "not a strictly simple room"); continue
    print(" g =", g, "W", W1, "witness:", lit(c1,t1,S,T,B))
