# Run: uv run --with sympy python checks.py > checks.log
"""d197 referee checks: exact arithmetic only. No ray, direction, word, or room-size searches."""
import time
from fractions import Fraction as F
from math import gcd
from functools import reduce
import sympy as sp

t0 = time.process_time()
npass = nfail = 0
def check(name, ok, info=""):
    global npass, nfail
    npass += bool(ok); nfail += (not ok)
    print(("PASS " if ok else "FAIL ") + name + (("  [" + info + "]") if info else ""))

# ---------- 1. Admissible horizontal moves ----------
print("== 1. Admissible moves on v=(n,n+1,n+2,n+3) ==")
ok_pos = ok_gcd3 = ok_gcdall = True
for n in range(3, 51):
    v = [n, n+1, n+2, n+3]
    for j in range(4):
        for s in (1, 2):
            w = v[:]; w[j] -= s
            ok_pos &= min(w) >= 1
            rest = [v[i] for i in range(4) if i != j]
            ok_gcd3 &= reduce(gcd, rest) == 1
            ok_gcdall &= reduce(gcd, w) == 1
check("n=3..50, j=1..4, s=1,2: all gaps stay positive", ok_pos)
check("n=3..50: the three unchanged gaps have gcd 1 (two consecutive integers)", ok_gcd3)
check("n=3..50: successor horizontal gap vector is normalized (gcd 1)", ok_gcdall)
# consecutive pair claim, symbolic over j
cons = all(any(b - a == 1 for a, b in zip(r, r[1:])) for r in
           ([k for k in range(4) if k != j] for j in range(4)))
check("removing any one index of 0..3 leaves two consecutive indices", cons)

# ---------- 2. Leaving the line ----------
print("== 2. v - s e_j leaves span(v) ==")
def parallel(a, b):
    return all(a[i]*b[k] - a[k]*b[i] == 0 for i in range(4) for k in range(4))
ok = all(not parallel([n, n+1, n+2, n+3], [n+(i) - (s if i == j else 0) for i in range(4)])
         for n in range(3, 51) for j in range(4) for s in (1, 2))
check("n=3..50: v - s e_j not parallel to v (s=1,2, all j)", ok)
# general symbolic statement: v - s e_j = lam v with an unchanged positive coordinate => lam=1 => s=0
lam, s_, vi, vj = sp.symbols('lam s v_i v_j', positive=True)
sol = sp.solve([sp.Eq(vi, lam*vi), sp.Eq(vj - s_, lam*vj)], [lam, s_], dict=True)
check("symbolic: v_i = lam v_i, v_j - s = lam v_j has no solution with s > 0 (lam=1 forces s=0)", sol == [], str(sol))
sol0 = sp.solve([sp.Eq(vi, lam*vi), sp.Eq(vj - sp.Symbol('s0'), lam*vj)], [lam, sp.Symbol('s0')], dict=True)
check("without the sign restriction the only solution is lam=1, s=0", sol0 == [{lam: 1, sp.Symbol('s0'): 0}], str(sol0))
okv = all(not parallel(b, [b[i] - (s if i == j else 0) for i in range(4)])
          for b in ([1, b2, b3, 4*k] for b2 in (1, 2, 5) for b3 in (1, 3, 7) for k in (1, 2, 3))
          for j in range(4) for s in (1, 2) if b[j] > s)
check("vertical analog, named b=(1,b2,b3,4k): positive-gap shrinks leave span(b)", okv)

# ---------- 3. Affine side test and averaging identity ----------
print("== 3. Affine side test, averaging identity ==")
t = sp.symbols('t')
c = sp.symbols('c0:4', integer=True); al = sp.symbols('a0:4')  # wall line x = c_i + a_i t
X, Y, Sx, Sy, Cx0, Cy, Ca = sp.symbols('X Y Sx Sy Cx0 Cy Ca')
x = X
for i in range(4):
    x = 2*(c[i] + al[i]*t) - x          # reflection in a vertical line moving affinely
Tstar = (x, Y)
Cpt = (Cx0 + Ca*t, Cy)
det = (Tstar[0] - Sx)*(Cpt[1] - Sy) - (Tstar[1] - Sy)*(Cpt[0] - Sx)
check("det(T*-S, C-S) is affine in t after 4 moving reflections", sp.diff(det, t, 2) == 0)
Sxt = Sx + sp.symbols('sa')*t
det2 = (Tstar[0] - Sxt)*(Cpt[1] - Sy) - (Tstar[1] - Sy)*(Cpt[0] - Sxt)
check("still affine when S itself moves (S right of the strip)", sp.expand(sp.diff(det2, t, 2)) == 0)
F0, B, s = sp.symbols('F0 B s', real=True)
# strict sign on [0,s] for affine F: F0>0, B<0 => need F0 + s B > 0 <=> F0 > s|B|
check("F0>0, B<0: F(s)>0 <=> F0 > s|B| (affine endpoint test)",
      sp.simplify((F0 + s*B) - (F0 - s*sp.Abs(B))).subs(B, -sp.Symbol('b', positive=True)) == 0)
v = sp.symbols('v1:5', positive=True); L = sum(v)
E = [sp.Matrix([1 if i == j else 0 for i in range(4)]) for j in range(4)]
V = sp.Matrix(v)
lhs = sum(((v[j]/L)*(V - E[j]) for j in range(4)), sp.zeros(4, 1))
check("sum_j (v_j/L)(v - e_j) = (1 - 1/L) v", sp.simplify(lhs - (1 - 1/L)*V) == sp.zeros(4, 1))
lhs2 = sum(((v[j]/L)*(V - 2*E[j]) for j in range(4)), sp.zeros(4, 1))
check("two-unit version: sum_j (v_j/L)(v - 2e_j) = (1 - 2/L) v", sp.simplify(lhs2 - (1 - 2/L)*V) == sp.zeros(4, 1))
# a linear form positive on all four shrinks is positive at v
g = sp.symbols('g1:5')
f = sum(gi*vi_ for gi, vi_ in zip(g, v))
check("linear f: sum (v_j/L) f(v-e_j) = (1-1/L) f(v)",
      sp.simplify(sum((v[j]/L)*f.subs(v[j], v[j]) - (v[j]/L)*g[j] for j in range(4)) - (1 - 1/L)*f) == 0)

# ---------- 4. Terminal-rectangle transfer criterion ----------
print("== 4. Terminal rectangle: s r in hZ ==")
def phase(u, h):  # phase mod 2h, exact
    return u % (2*h)
def fold(u, h):
    u = u % (2*h); return u if u <= h else 2*h - u
ok_iff = ok_corner = True
cnt = 0
for h in range(1, 9):
    for w in range(3, 8):
        for s in (1, 2):
            if s >= w: continue
            for q in range(1, 7):
                for p in range(-7, 8):
                    if p == 0 or gcd(abs(p), q) != 1: continue
                    r = F(p, q)
                    for z in (F(1, 3), F(1, 2), F(5, 7)):
                        z = z*h
                        old = phase(z + 2*(w - s)*r, h); new = phase(z + 2*w*r, h)
                        crit = (s*r) % h == 0
                        ok_iff &= ((old == new) == crit)
                        if crit:
                            fo, fn = fold(z + (w - s)*r, h), fold(z + w*r, h)
                            ok_corner &= ((fo in (0, h)) == (fn in (0, h)))
                        cnt += 1
check("exit phase mod 2h unchanged <=> s r in hZ (exact, %d named cases h<=8, w<=7, |p|<=7, q<=6)" % cnt, ok_iff)
check("under s r in hZ, restored far-wall contact is a corner iff old one is", ok_corner)
# symbolic: phase shift on restoring is 2 s r; far wall shift is s r
z_, w_, r_ = sp.symbols('z w r')
check("restored minus old: exit 2sr, far wall sr",
      sp.expand((z_ + 2*w_*r_) - (z_ + 2*(w_ - s_)*r_)) == 2*s_*r_ and sp.expand((z_ + w_*r_) - (z_ + (w_ - s_)*r_)) == s_*r_)

# ---------- 5. Parity obstruction ----------
print("== 5. Parity ==")
okr = all((2*cc - xx - xx) % 2 == 0 for cc in range(-6, 7) for xx in range(-9, 10))
check("reflection x -> 2c - x preserves x mod 2 for integer c", okr)
okd = True
for dx in range(-15, 16):
    for dy in range(-15, 16, 2):  # dy odd
        if dy % 2 == 0: continue
        if dx == 0: continue
        gg = gcd(abs(dx), abs(dy)); p = dy // gg
        okd &= (p % 2 != 0)
check("integral displacement with odd dy => primitive p is odd", okd)
okno = True; witness = None
for h in range(4, 101, 4):
    for s in (1, 2):
        for q in range(1, 3):
            if s % q: continue
            for p in range(-99, 100, 2):
                if (s // q)*p % h == 0: okno = False
check("4|h (h=4..100), s in {1,2}, q|s, p odd: h never divides (s/q)p", okno)
check("contrast: s=4, h=4, q=1, p odd satisfies the criterion (the step bound is the culprit)",
      all((4*p) % 4 == 0 for p in range(1, 20, 2)))
# general 2-adic form: obstruction whenever v2(h) > v2(s)
def v2(m):
    m = abs(m); k = 0
    while m and m % 2 == 0: m //= 2; k += 1
    return k
okg = all(not ((s//q)*p % h == 0) for h in range(2, 65) for s in range(1, 9) for q in range(1, 9)
          if s % q == 0 and v2(h) > v2(s) for p in range(1, 40, 2))
check("general: p odd and v2(h) > v2(s) => no same-exit transfer (h<=64, s<=8)", okg)

# ---------- 6. Chart and realization class ----------
print("== 6. Chart 3,4,2,0,1 with v x (1,b2,b3,4k) ==")
def chart_room(gx, gy):
    order = [3, 4, 2, 0, 1]; Xc = [0]*5; Yc = [0]*5; cx = cy = 0
    for k, i in enumerate(order):
        Xc[i] = cx; Yc[i] = cy
        if k < 4: cx += gx[k]; cy += gy[k]
    P = [(Xc[0],Yc[0]),(Xc[1],Yc[0]),(Xc[1],Yc[1]),(Xc[2],Yc[1]),(Xc[2],Yc[2]),
         (Xc[3],Yc[2]),(Xc[3],Yc[3]),(Xc[4],Yc[3]),(Xc[4],Yc[4]),(Xc[0],Yc[4])]
    return P, Xc, Yc
def dirs(P):
    out = []
    for a, b in zip(P, P[1:] + P[:1]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        out.append('E' if dx > 0 else 'W' if dx < 0 else 'N' if dy > 0 else 'S')
    return out
def turns(ds):
    L = {('E','N'),('N','W'),('W','S'),('S','E')}
    return ''.join('L' if (ds[i-1], ds[i]) in L else 'R' for i in range(len(ds)))
def inside(P, pt):
    x, y = pt; c = False
    for a, b in zip(P, P[1:] + P[:1]):
        if a[0] == b[0] and min(a[1], b[1]) <= y <= max(a[1], b[1]) and x == a[0]: return False
        if a[1] == b[1] and min(a[0], b[0]) <= x <= max(a[0], b[0]) and y == a[1]: return False
        if (a[1] > y) != (b[1] > y):
            xi = a[0] + F(y - a[1], b[1] - a[1])*(b[0] - a[0])
            if x < xi: c = not c
    return c
okc = True
for n in (3, 10):
    for gy in ((1, 1, 1, 4), (1, 2, 3, 8), (1, 5, 2, 12)):
        P, Xc, Yc = chart_room((n, n+1, n+2, n+3), gy)
        ds = dirs(P)
        word_ok = turns(ds) in ['LLLRLLLRLR'[k:] + 'LLLRLLLRLR'[:k] for k in range(10)]
        w = Xc[1] - Xc[0]; h = Yc[1] - Yc[0]
        # vertical edges on x = x0: only (x0,y4)-(x0,y0)
        vx0 = [(a, b) for a, b in zip(P, P[1:] + P[:1]) if a[0] == b[0] == Xc[0]]
        left_open = all(max(a[1], b[1]) <= Yc[0] for a, b in vx0)
        S = (Xc[0] - 1, Yc[0] + 1); T = (Xc[0] - 1, Yc[0] + 2)
        marks_ok = inside(P, S) and inside(P, T) and (T[1] - S[1]) % 2 == 1
        okc &= word_ok and w == n + 3 and h == gy[3] and h % 4 == 0 and left_open and marks_ok
        print("   n=%d gy=%s: word ok=%s, w=%d, h=%d, left side of cap open=%s, marks S=%s T=%s interior=%s"
              % (n, gy, word_ok, w, h, left_open, S, T, marks_ok))
check("named realizations: cap is (x0,x1)x(y0,y1), w=n+3, h=b4=4k, left side open, odd-difference marks exist", okc)

# ---------- 7. Follow-up snapshot2: one-visit test and additive order ----------
print("== 7. snapshot2: exit phase, disjointness, additive order ==")
def order(shift, h):   # additive order of shift in R/2hZ, shift rational
    m = 1
    while (m*shift) % (2*h) != 0: m += 1
    return m
ok_dis = ok_div = ok_ord = ok_v2 = ok_back = True; cnt = 0
for h in range(1, 13):
    for q in range(1, 7):
        for p in range(1, 12):
            if gcd(p, q) != 1: continue
            r = F(p, q)
            for s in (1, 2):
                for w in (s + 1, s + 4):
                    for th in (F(1, 5)*h, F(7, 5)*h):
                        short = (th + 2*(w - s)*r) % (2*h); long_ = (th + 2*w*r) % (2*h)
                        ok_dis &= ((short != long_) == ((2*s*r) % (2*h) != 0))
                        # entry needed in width w to reproduce the short exit
                        ok_back &= ((th - 2*s*r) + 2*w*r) % (2*h) == short
                    ok_div &= (((2*s*r) % (2*h) == 0) == ((s*p) % (h*q) == 0))
                    o = order(2*s*r, h)
                    ok_ord &= o == h*q // gcd(h*q, s*p)
                    if h % 4 == 0 and p % 2 == 1:
                        ok_v2 &= (o % 4 == 0) if s == 1 else (o % 2 == 0)
                    cnt += 1
check("same entry: short and long exits differ <=> 2sr not in 2hZ", ok_dis)
check("2sr in 2hZ <=> hq | s|p|", ok_div)
check("long entry theta - 2sr reproduces the short exit theta + 2(w-s)r", ok_back)
check("additive order of 2sr on R/2hZ equals hq/gcd(hq, s|p|) (%d exact cases, h<=12, q<=6, p<=11)" % cnt, ok_ord)
check("4|h, p odd: order is a multiple of 4 (s=1) and of 2 (s=2)", ok_v2)

print("\nSUMMARY: %d PASS, %d FAIL, CPU %.3f s" % (npass, nfail, time.process_time() - t0))
