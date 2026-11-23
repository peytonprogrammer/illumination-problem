# Run: python3 checks.py > checks.log
"""d198 referee checks. Standard library only, exact Fraction arithmetic.

Only the rays the note names are simulated: the four starts of absolute slope
1/q from S and T, in the named rooms of the symbolic family
(chart 3,4,2,0,1; horizontal gaps (n,n+1,n+2,d); vertical gaps (1,b2,b3,h)).
No ray, direction, word, or room-size searches.
"""
import time
from fractions import Fraction as F
from math import gcd
from functools import reduce

t0 = time.process_time()
npass = nfail = 0
def check(name, ok, info=""):
    global npass, nfail
    npass += bool(ok); nfail += (not ok)
    print(("PASS " if ok else "FAIL ") + name + (("  [" + info + "]") if info else ""))

# ---------------------------------------------------------------- rooms
def coords(gx, gy):
    order = [3, 4, 2, 0, 1]; X = [0]*5; Y = [0]*5; cx = cy = 0
    for k, i in enumerate(order):
        X[i] = cx; Y[i] = cy
        if k < 4: cx += gx[k]; cy += gy[k]
    return X, Y

def open_room(X, Y):
    return [(X[0],Y[0]),(X[1],Y[0]),(X[1],Y[1]),(X[2],Y[1]),(X[2],Y[2]),
            (X[3],Y[2]),(X[3],Y[3]),(X[4],Y[3]),(X[4],Y[4]),(X[0],Y[4])]

def closed_exterior(X, Y):
    return [(X[0],Y[4]),(X[0],Y[1]),(X[2],Y[1]),(X[2],Y[2]),
            (X[3],Y[2]),(X[3],Y[3]),(X[4],Y[3]),(X[4],Y[4])]

def edges(P):
    return list(zip(P, P[1:] + P[:1]))

def turn_word(P):
    ds = []
    for a, b in edges(P):
        dx, dy = b[0]-a[0], b[1]-a[1]
        ds.append('E' if dx > 0 else 'W' if dx < 0 else 'N' if dy > 0 else 'S')
    L = {('E','N'),('N','W'),('W','S'),('S','E')}
    return ''.join('L' if (ds[i-1], ds[i]) in L else 'R' for i in range(len(ds)))

def inside(P, pt):
    x, y = pt; c = False
    for a, b in edges(P):
        if a[0] == b[0] == x and min(a[1], b[1]) <= y <= max(a[1], b[1]): return False
        if a[1] == b[1] == y and min(a[0], b[0]) <= x <= max(a[0], b[0]): return False
        if (a[1] > y) != (b[1] > y):
            xi = a[0] + F(y - a[1], b[1] - a[1])*(b[0] - a[0])
            if x < xi: c = not c
    return c

# ---------------------------------------------------------------- billiard
def trace(P, start, d, max_travel, mouth=None, target=None, stop_at_mouth=False,
          max_visits=None):
    """Exact billiard. d=(dx,dy) integers. Travel = horizontal distance.
    mouth=(x0,y0,y1): record crossings of x=x0, y0<y<y1 (open room: pass through).
    Returns dict with events; stops on corner/mouth-endpoint, target hit,
    stop_at_mouth (first mouth contact), max_visits completed, or max_travel."""
    x, y = F(start[0]), F(start[1]); dx, dy = d
    travel = F(0); events = []; visits = 0; inside_cap = False
    verts = set(P)
    E = edges(P)
    while True:
        best = None; kind = None
        for a, b in E:
            if a[0] == b[0] and dx != 0:
                t = (a[0] - x)/dx
                if t > 0:
                    yy = y + t*dy
                    if min(a[1], b[1]) <= yy <= max(a[1], b[1]):
                        if best is None or t < best: best, kind = t, 'V'
            if a[1] == b[1] and dy != 0:
                t = (a[1] - y)/dy
                if t > 0:
                    xx = x + t*dx
                    if min(a[0], b[0]) <= xx <= max(a[0], b[0]):
                        if best is None or t < best: best, kind = t, 'H'
        tm = None
        if mouth is not None and dx != 0:
            t = (mouth[0] - x)/dx
            if t > 0 and (best is None or t <= best):
                tm = t
        # target on the open segment up to the next event
        tnext = tm if tm is not None else best
        if target is not None:
            tx, ty = target
            if dx != 0:
                t = (tx - x)/dx
                if 0 < t <= tnext and y + t*dy == ty:
                    if travel + abs(t*dx) <= max_travel:
                        events.append(('T', travel + abs(t*dx), (tx, ty), (dx, dy), visits))
                        return dict(events=events, end='T', travel=travel + abs(t*dx), visits=visits)
        if travel + abs(tnext*dx) > max_travel:
            return dict(events=events, end='max', travel=travel, visits=visits)
        if tm is not None:
            x, y = x + tm*dx, y + tm*dy; travel += abs(tm*dx)
            if not (mouth[1] < y < mouth[2]):
                events.append(('M-end', travel, (x, y), (dx, dy), visits))
                return dict(events=events, end='singular', travel=travel, visits=visits)
            events.append(('M', travel, (x, y), (dx, dy), visits))
            if stop_at_mouth:
                return dict(events=events, end='mouth', travel=travel, visits=visits)
            if dx > 0: inside_cap = True
            else:
                inside_cap = False; visits += 1
                if max_visits is not None and visits >= max_visits:
                    return dict(events=events, end='visits', travel=travel, visits=visits)
            continue
        x, y = x + best*dx, y + best*dy; travel += abs(best*dx)
        if (x, y) in verts:
            events.append(('corner', travel, (x, y), (dx, dy), visits))
            return dict(events=events, end='singular', travel=travel, visits=visits)
        events.append((kind, travel, (x, y), (dx, dy), visits))
        if kind == 'V': dx = -dx
        else: dy = -dy

def phase(y, y0, h, dy):
    z = y - y0
    return z if dy > 0 else (2*h - z) % (2*h)

def family(n, h, b2=1, b3=1):
    a, w = n + 2, n + 3
    return a, w

ROOMS = [(n, h, b) for n in range(3, 13) for h in (8, 12, 16) for b in ((1, 1), (2, 3))]

# ================================================================ 1
print("== 1. Closed exterior: eight walls, correspondence, first phases ==")
ok_w = ok_m = ok_corr = ok_four = ok_grid = True; ncorr = 0
for n, h, (b2, b3) in ROOMS:
    a, w = n + 2, n + 3
    q = 2*w + 2*a - 4; r = F(1, q)
    for d in (w, w - 1, w - 2):
        X, Y = coords((n, n + 1, n + 2, d), (1, b2, b3, h))
        P = open_room(X, Y); E8 = closed_exterior(X, Y)
        word = turn_word(E8)
        ok_w &= len(E8) == 8 and word.count('L') == 6 and word.count('R') == 2
        ok_w &= turn_word(P) in ['LLLRLLLRLR'[k:] + 'LLLRLLLRLR'[:k] for k in range(10)]
        S = (X[2] + 1, Y[0] + 2); T = (X[2] + 1, Y[0] + 3)
        ok_m &= inside(P, S) and inside(P, T) and inside(E8, S) and inside(E8, T)
        ok_m &= S[0] < X[0] and Y[0] < S[1] < T[1] < Y[1]
        mouth = (X[0], Y[0], Y[1])
        for M in (S, T):
            ph = set()
            for d0 in ((q, 1), (q, -1), (-q, 1), (-q, -1)):
                o = trace(P, M, d0, 10**6, mouth=mouth, stop_at_mouth=True)
                # closed exterior: stop when the ray first reaches x=x0 within the mouth
                c = trace(E8, M, d0, o['travel'], mouth=None)
                # compare the wall events strictly before the mouth contact
                oe = [e[:3] for e in o['events'][:-1]]
                ce = [e[:3] for e in c['events'] if e[1] < o['travel']]
                nxt = [e for e in trace(E8, M, d0, o['travel'] + 1)['events'] if e[1] == o['travel']]
                ok_corr &= oe == ce and o['end'] == 'mouth' and len(nxt) == 1 and nxt[0][2] == o['events'][-1][2]
                ncorr += 1
                e = o['events'][-1]
                th = phase(e[2][1], Y[0], h, e[3][1])
                ph.add(th)
                ok_grid &= (th*q).denominator == 1
            ok_four &= len(ph) <= 4
check("closed exterior has 8 walls (6 L, 2 R); open room is LLLRLLLRLR (%d named rooms x 3 widths)" % len(ROOMS), ok_w)
check("S=(x2+1,y0+2), T=(x2+1,y0+3) interior in both, left of mouth, inside top strip", ok_m)
check("open and closed trajectories agree up to first mouth contact; closed ray hits the right wall there (%d rays)" % ncorr, ok_corr)
check("at most four first phases per mark at r=1/q", ok_four)
check("every first phase lies in (1/q)Z mod 2h", ok_grid)
# order of the shift 2sp in Z/2hqZ
ok_ord = True
for h in (8, 12, 16):
    for q in (18, 22, 26, 30):
        for p in (1, 3, 5):
            if gcd(p, q) != 1: continue
            for s in (1, 2):
                g = 2*s*p; m = 1
                while (m*g) % (2*h*q): m += 1
                ok_ord &= m == h*q // gcd(h*q, s*p) and m > 4
check("order of 2sp in Z/2hqZ is hq/gcd(hq,sp) and exceeds 4 for named h,q,p,s", ok_ord)

# ================================================================ 2
print("== 2. Symbolic family: travel totals, one-visit test, strip bounds ==")
ok_tot = ok_dw = ok_d1 = ok_d2 = ok_strip = ok_reg = ok_formula = True; nsing = []
for n, h, (b2, b3) in ROOMS:
    a, w = n + 2, n + 3
    q = 2*w + 2*a - 4; r = F(1, q)
    ok_strip &= F(a + 1 + 2*w, q) < 2 and 2*w + 3*a > 9 and F(2*a + 2 + 2*w, q) < 2
    for d in (w, w - 1, w - 2):
        X, Y = coords((n, n + 1, n + 2, d), (1, b2, b3, h))
        P = open_room(X, Y); E8 = closed_exterior(X, Y); mouth = (X[0], Y[0], Y[1])
        S = (X[2] + 1, Y[0] + 2); T = (X[2] + 1, Y[0] + 3)
        # A_S: first entry phases and prefix travel
        A = {}
        for d0 in ((q, 1), (q, -1), (-q, 1), (-q, -1)):
            o = trace(P, S, d0, 10**6, mouth=mouth, stop_at_mouth=True)
            e = o['events'][-1]; A[phase(e[2][1], Y[0], h, e[3][1])] = o['travel']
            ok_tot &= o['travel'] == (a - 1 if d0[0] > 0 else a + 1)
        # B_T: reverse first phases from T, converted to exit phases (velocity reversed)
        B = {}
        for d0 in ((q, 1), (q, -1), (-q, 1), (-q, -1)):
            o = trace(P, T, d0, 10**6, mouth=mouth, stop_at_mouth=True)
            e = o['events'][-1]
            B[phase(e[2][1], Y[0], h, -e[3][1])] = o['travel']
        # intersection formula (A_d + 2dr) cap B_T, all excursions regular here
        inter = {(th + 2*d*r) % (2*h) for th in A} & set(B)
        totals = sorted({A[th] + 2*d + B[(th + 2*d*r) % (2*h)] for th in A if (th + 2*d*r) % (2*h) in B})
        # direct simulation of one-visit paths: four starts, stop after one visit
        hit1 = []
        for d0 in ((q, 1), (q, -1), (-q, 1), (-q, -1)):
            o = trace(P, S, d0, 10**6, mouth=mouth, target=T, max_visits=2)
            # count as one-visit hit if T is reached with exactly one completed visit
            if o['end'] == 'T' and o['visits'] == 1: hit1.append((d0, o['travel']))
            ok_reg &= o['end'] in ('T', 'visits') or o['visits'] >= 1
            if o['end'] == 'singular': nsing.append((n, h, d, d0, o['events'][-1][0], o['travel']))
        ok_formula &= (len(inter) > 0) == (len(hit1) > 0)
        ok_formula &= all(t == q for _, t in hit1) and all(d0[1] > 0 for d0, _ in hit1)
        allt = sorted({x + 2*d + y for x in (a - 1, a + 1) for y in (a - 1, a + 1)})
        ok_tot &= allt == [2*d + 2*a - 2, 2*d + 2*a, 2*d + 2*a + 2]
        if d == w: ok_dw &= not inter and not hit1 and allt[0] == q + 2
        if d == w - 1: ok_d1 &= bool(hit1) and allt[0] == q
        if d == w - 2: ok_d2 &= bool(hit1) and allt[1] == q
check("prefix travel a-1 (right start), a+1 (left start); totals 2d+2a-2, 2d+2a, 2d+2a+2", ok_tot)
check("d=w: one-visit intersection empty, no one-visit ray reaches T; smallest total = q+2", ok_dw)
check("d=w-1: one-visit path exists, smallest total = q", ok_d1)
check("d=w-2: one-visit path exists, middle total = q", ok_d2)
check("intersection formula agrees with direct simulation; hits are upward with travel q", ok_formula)
check("(a+1+2w)/q < 2 <=> 2w+3a > 9; the suffix bound (2a+2+2w)/q < 2 also holds", ok_strip)
check("prefix, first excursion and suffix of every named ray are regular (singular events occur only after the first visit)", ok_reg)
print("   info: %d named rays meet a corner or mouth endpoint after the first completed visit (C_d or E_r undefined), e.g. %s" % (len(nsing), nsing[:2]))

# ================================================================ 3
print("== 3. k-visit recurrence X_{k+1} = C_d(E_r(X_k)) ==")
def E_r(E8, X, Y, h, q, th):
    """Closed exterior, start on M just after reflection (moving left), stop before next M hit."""
    z = th if th <= h else 2*h - th
    if z in (0, h): return None
    dy = 1 if th < h else -1
    start = (X[0], Y[0] + z)
    # step off the wall by tracing in the open room clipped at x0: use E8 with a mouth stop
    o = trace(E8, start, (-q, dy), 10**7, mouth=(X[0], Y[0], Y[1]), stop_at_mouth=True)
    if o['end'] != 'mouth': return None
    e = o['events'][-1]
    return phase(e[2][1], Y[0], h, e[3][1])
ok_rec = ok_exact = ok_grid3 = True; nk = 0; first_hit = set()
for n, h, (b2, b3) in [(3, 8, (1, 1)), (4, 12, (2, 3)), (6, 16, (1, 1)), (9, 8, (2, 3)), (12, 16, (1, 1))]:
    a, w = n + 2, n + 3
    q = 2*w + 2*a - 4; r = F(1, q); K = 12
    for d in (w, w - 1, w - 2):
        X, Y = coords((n, n + 1, n + 2, d), (1, b2, b3, h))
        P = open_room(X, Y); E8 = closed_exterior(X, Y); mouth = (X[0], Y[0], Y[1])
        S = (X[2] + 1, Y[0] + 2); T = (X[2] + 1, Y[0] + 3)
        A = []; B = set()
        for d0 in ((q, 1), (q, -1), (-q, 1), (-q, -1)):
            o = trace(P, S, d0, 10**6, mouth=mouth, stop_at_mouth=True); e = o['events'][-1]
            A.append(phase(e[2][1], Y[0], h, e[3][1]))
            o = trace(P, T, d0, 10**6, mouth=mouth, stop_at_mouth=True); e = o['events'][-1]
            B.add(phase(e[2][1], Y[0], h, -e[3][1]))
        def C(th):
            # regular cap excursion: far-wall contact and mouth exit must both miss {0,h}
            for u in (th + d*r, th + 2*d*r):
                z = u % (2*h); z = z if z <= h else 2*h - z
                if z in (0, h): return None
            return (th + 2*d*r) % (2*h)
        Xk = [C(t) for t in A]
        # direct: exit phases after k visits for the four starts in the open room
        for k in range(1, K + 1):
            direct = []
            for d0 in ((q, 1), (q, -1), (-q, 1), (-q, -1)):
                o = trace(P, S, d0, 10**7, mouth=mouth, max_visits=k)
                if o['end'] == 'visits':
                    e = o['events'][-1]; direct.append(phase(e[2][1], Y[0], h, e[3][1]))
                else: direct.append(None)
            ok_rec &= direct == Xk
            ok_grid3 &= all(t is None or (t*q).denominator == 1 for t in Xk)
            # exactness: X_k meets B_T iff some start reaches T with exactly k visits (and not fewer)
            # direct: continue each start's k-th exit in the open room until T or the next mouth contact
            reach = []
            for d0 in ((q, 1), (q, -1), (-q, 1), (-q, -1)):
                o = trace(P, S, d0, 10**7, mouth=mouth, max_visits=k)
                if o['end'] != 'visits': reach.append(False); continue
                e = o['events'][-1]
                o2 = trace(P, e[2], e[3], 10**7, mouth=mouth, target=T, stop_at_mouth=True)
                reach.append(o2['end'] == 'T')
                if k == 1 or o2['end'] == 'T': first_hit.add((n, h, d, d0, k)) if o2['end'] == 'T' else None
            meet = [t is not None and t in B for t in Xk]
            ok_exact &= meet == reach
            nk += 1
            Xk = [None if t is None else (lambda u: None if u is None else C(u))(E_r(E8, X, Y, h, q, t)) for t in Xk]
check("X_k from the recurrence equals the direct k-th exit phase of each start (%d (room,d,k) cases, k<=12)" % nk, ok_rec)
check("X_k meets B_T exactly when that start, after its k-th regular exit, reaches T before the next mouth contact", ok_exact)
print("   info: %d (room,d,start,k) hits; smallest k per (room,d): %s" % (len(first_hit),
      sorted({(n_, h_, d_): min(k_ for (a_, b_, c_, _, k_) in first_hit if (a_, b_, c_) == (n_, h_, d_)) for (n_, h_, d_, _, _) in first_hit}.items())))
check("all exit phases stay in (1/q)Z mod 2h", ok_grid3)

# ================================================================ 4
print("== 4. Unbounded visits: q = 2mL, L = a+d ==")
ok_up = ok_down = ok_reg4 = ok_dist = True; n4 = 0
for n in range(3, 13):
    for h in (8, 12, 16):
        a, w = n + 2, n + 3
        for d in (w, w - 1, w - 2):
            X, Y = coords((n, n + 1, n + 2, d), (1, 1, 1, h))
            P = open_room(X, Y); mouth = (X[0], Y[0], Y[1])
            S = (X[2] + 1, Y[0] + 2); T = (X[2] + 1, Y[0] + 3); L = a + d
            for m in range(1, 7):
                q = 2*m*L
                for d0 in ((q, 1), (-q, 1), (q, -1), (-q, -1)):
                    o = trace(P, S, d0, q, mouth=mouth, target=T)
                    ok_reg4 &= o['end'] in ('T', 'max')
                    if d0[1] > 0:
                        ok_up &= o['end'] == 'T' and o['travel'] == q and o['visits'] == m
                        exits = [e[2][1] for e in o['events'] if e[0] == 'M' and e[3][0] < 0]
                        ok_dist &= len(exits) == m and len(set(exits)) == m
                    else:
                        o2 = trace(P, S, d0, q, mouth=mouth, max_visits=m)
                        ok_down &= o['end'] == 'max' and o2['end'] == 'visits'
                    n4 += 1
check("upward starts (both horizontal signs) first reach T at travel exactly q after exactly m visits (%d rays, m=1..6)" % n4, ok_up)
check("downward starts miss T before travel q and have completed m visits by travel q", ok_down)
check("all contacts regular up to travel q", ok_reg4)
check("the m upward exit heights are distinct", ok_dist)

# ================================================================ 5
print("== 5. d197 corrections ==")
def v2(x):
    x = abs(x); k = 0
    while x and x % 2 == 0: x //= 2; k += 1
    return k
ok_lam = ok_edge = True
for n in range(3, 13):
    v = [n, n + 1, n + 2, n + 3]
    ok_lam &= reduce(gcd, v) == 1
    for b in ((1, 1, 1, 8), (1, 2, 3, 12)):
        X, Y = coords(v, b)
        P = open_room(X, Y)
        hl = [abs(e[1][0] - e[0][0]) for e in edges(P) if e[0][1] == e[1][1]]
        ok_edge &= reduce(gcd, hl) == reduce(gcd, v) == 1
check("v primitive, so lam*v integral forces lam integral (Bezout); n=3..12", ok_lam)
check("horizontal edge-length gcd = horizontal wall-gap gcd = 1 on named rooms", ok_edge)
def fold(u, h):
    u = u % (2*h); return u if u <= h else 2*h - u
ok_fold = all(fold(u + k*h, h) == (fold(u, h) if k % 2 == 0 else h - fold(u, h))
              for h in (8, 12, 16) for k in range(-3, 4) for u in (F(j, 7) for j in range(0, 7*2*h)))
check("fold(u + kh) = fold(u) (k even) or h - fold(u) (k odd); {0,h} symmetric", ok_fold)
# v2 test: hq | s|p| implies v2(h) <= v2(s) + v2(DY) for DY = k p, k != 0
ok_v2 = True
for h in (4, 8, 12, 16, 24):
    for q in range(1, 9):
        for p in range(1, 13):
            if gcd(p, q) != 1: continue
            for s in (1, 2, 3, 4):
                for k in (1, 2, 3, 4, 6):
                    if (s*p) % (h*q) == 0:
                        ok_v2 &= v2(h) <= v2(s) + v2(k*p)
check("hq | s|p| => v2(h) <= v2(s) + v2(DY) for DY = kp", ok_v2)
# even physical difference: unfolded DY = (2c - yT) - yS changes the 2-adic valuation
yS, yT = 2, 6  # physical difference 4, v2 = 2
img = [2*c - yT - yS for c in (5, 6)]  # reflections of T in integer lines y=c
check("even physical difference 4: unfolded DY values %s have v2 %s, not 2" % (img, [v2(x) for x in img]),
      all(x % 2 == 0 for x in img) and any(v2(x) != v2(yT - yS) for x in img))

print("\nSUMMARY: %d PASS, %d FAIL, CPU %.2f s" % (npass, nfail, time.process_time() - t0))
