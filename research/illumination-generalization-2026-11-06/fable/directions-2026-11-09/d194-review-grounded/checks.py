# d194 referee checks: exact rationals, note parameters only, no room/ray searches.
from fractions import Fraction as F
from math import gcd, pi, ceil
import itertools, time
T0 = time.process_time(); FAIL = []
def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok: FAIL.append(msg)

# (b) (1) integral => T | P*C_b*S_b, over small exact tuples
cnt = 0; ok = True
for m in range(1, 9):
  for n in range(1, 7):
    if gcd(m, n) != 1: continue
    H = F(m, n)
    for hs in [(0, 1), (0, 2), (1, 2), (0, 1, 3), (1, 2, 3)]:
      for b in hs:
        for u in (1, 2, 3):
          for P in (2, 4, 6):
            for ws in itertools.product(range(1, 5), repeat=len(hs)):
              for ps in itertools.product((-1, 1, 2), repeat=len(hs)):
                s = sum(F(p * P * w, 2 * u) / (H + j) for p, w, j in zip(ps, ws, hs))
                if s.denominator != 1: continue
                T = m + b * n
                Cb = 1
                for j in hs:
                  if j != b: Cb *= (j - b)
                Sb = ps[hs.index(b)] * ws[hs.index(b)]
                cnt += 1; ok &= (P * Cb * Sb) % T == 0
check(ok and cnt > 0, f'(2): T | P C_b S_b on {cnt} integral instances of (1)')

# (b) conversion: T | P C_b S_b with w=iD+ju => T | P C_b p (jB0 - iAb)
ok = True; cnt = 0
for m in range(1, 13):
  for n in range(1, 9):
    if gcd(m, n) != 1: continue
    for A in range(1, 5):
      for B0 in range(1, 5):
        if gcd(A, B0) != 1: continue
        g = gcd(A * m, B0 * n); D, u = A * m // g, B0 * n // g
        if gcd(D, u) != 1: continue
        for b in (1, 2, 3):
          T = m + b * n
          for i in range(-2, 3):
            for j in range(-3, 4):
              w = i * D + j * u
              cnt += 1
              # residue identity behind the step
              ok &= (g * w - n * (j * B0 - i * A * b)) % T == 0
              if 0 < w < D: ok &= (j * B0 - i * A * b) != 0
check(ok, f'g*w == n(jB0-iAb) mod T, and Delta!=0 for 0<w<D, on {cnt} tuples')

# area chain: D<=Am, u<=B0 n, n<=T/b, m<=T
ok = True
for m in range(1, 30):
  for n in range(1, 30):
    if gcd(m, n) != 1: continue
    for A, B0 in [(1, 1), (2, 3), (5, 2)]:
      g = gcd(A * m, B0 * n); D, u = A * m // g, B0 * n // g
      for b in (1, 2, 4):
        T = m + b * n
        ok &= D <= A * m and u <= B0 * n and b * n <= T and m <= T
        ok &= F(D, u) / F(m, n) == F(A, B0)
check(ok, 'area conversion D<=Am, u<=B0 n, n<=T/b, m<=T')

# (c) step 2 algebra: contact y, y+Z; folded heights sum to Z
def fold(y, Z):
    y = y % (2 * Z); return y if y <= Z else 2 * Z - y
ok = True; cnt = 0
for Z in (F(3), F(5, 2), F(7, 3)):
  C = 2 * Z
  for e, s, B, j, l, v in itertools.product((F(1,3), F(2)), (F(0), F(5,7)), (F(1), F(3,2)),
                                             (F(1), F(2)), (F(1,2),), (F(1,5), F(3,11))):
    rhs = e - s - (B + 2 * j - l) * v
    for z in (rhs / 2, rhs / 2 + Z):   # the two solutions of 2z = rhs mod C
      y = s + (j - l) * v + z          # left-side contact phase
      ret = y + j * v + z - z          # placeholder
      final = s + (2 * j - l) * v + 2 * z
      ok &= (final - (e - B * v)) % C == 0
      ok &= (y - (e + s - (B + l) * v) / 2) % Z == 0
    y0 = (e + s - (B + l) * v) / 2
    ok &= fold(y0, Z) + fold(y0 + Z, Z) == Z
    cnt += 1
check(ok, f'step 2: exit eqn, contact formula y, y+Z and fold sum Z on {cnt} cases')

# (c) step 3: zero total advance mod 2H => far-wall height is y or H-y
ok = True
for H in (F(1), F(4, 3)):
  for y in (F(1, 5), F(2, 3)):
    for k in range(-3, 4):
      far = fold(y + k * H, H)   # half of a multiple of 2H is a multiple of H
      ok &= far in (fold(y, H), H - fold(y, H))
check(ok, 'step 3: far-wall height is entrance height or its complement')

# (c) step 4/5: f, g formulas and divisibility T | p q0 P j B0 m n; p=0 => m | q q0 P j B0
ok = True; cnt = 0
for m in range(1, 16):
  for n in range(1, 10):
    if gcd(m, n) != 1: continue
    H = F(m, n)
    for b in (1, 2, 3):
      Z = H + b; T = m + b * n
      for A, B0 in [(3, 1), (5, 2), (7, 3)]:
        X = F(A, B0) * H
        for j in (1, 2):
          if not j < X: continue
          for q0, P in [(1, 2), (2, 2), (3, 4)]:
            f = F(q0 * P * j, 2) / Z; g = q0 * P * (X - j) / H
            ok &= f == F(q0 * P * j * n, 2 * T) and g == q0 * P * (F(A, B0) - F(j * n, m))
            for p in range(-3, 4):
              for q in range(-3, 4):
                if (p, q) == (0, 0): continue
                if (p * f + q * g).denominator != 1: continue
                cnt += 1
                if p != 0:
                  ok &= (p * q0 * P * j * B0 * m * n) % T == 0
                  ok &= T <= b * abs(p) * q0 * P * j * B0
                else:
                  ok &= (q * q0 * P * j * B0) % m == 0
                  ok &= T <= (1 + b / H) * abs(q) * q0 * P * j * B0
check(ok and cnt > 0, f'steps 4-5: f,g and both divisor bounds on {cnt} relations')

# K for s=2: tail 2s/(pi^2 K rho^(s+1)) < 1/2 with K = 1+ceil(8/(pi^2 rho^3))
ok = all(4 / (pi**2 * (1 + ceil(8 / (pi**2 * r**3))) * r**3) < 0.5 for r in (0.1, 0.05, 0.01))
check(ok, 'K = 1+ceil(8/(pi^2 rho^3)) makes the s=2 omitted mass < 1/2 (< constant term 1)')

# triangle-bump Fourier coefficient bound used for tails
ok = all((F(1) if k == 0 else None) is not None or True for k in range(1))
ok = True
for r in (0.1, 0.03):
  for k in range(1, 400):
    c = (__import__('math').sin(pi * k * r) / (pi * k * r))**2
    ok &= c <= 1 / (pi**2 * k**2 * r**2) + 1e-15
check(ok, 'triangle bump coefficients <= 1/(pi^2 k^2 rho^2)')

# (d) d193 family: w=u=m(2m+1), D=(m+1)(2m+1), c=m, (p,q)=(1,2), H=(m+1)/m, beta=1, P=2
ok = True
for m in range(2, 80):
  H = F(m + 1, m); be = 1; P = 2; u = m * (2 * m + 1); D = (m + 1) * (2 * m + 1); w = u; c = m
  lhs = F(P * 1 * (D - w - c)) / (2 * u * H) + F(P * 2 * w) / (2 * u * (H + be))
  T = (m + 1) + be * m
  ok &= lhs == 1 and gcd(D, u) == 2 * m + 1 == T and 0 < c < D - w and F(D, u) / H == 1
check(ok, 'd193 family (1,2) identity, gcd(D,u)=T=2m+1 for m=2..79')

# (d) Delta=0 with 0<w<D impossible for integral rows (exhaustive small)
ok = True
for A in range(1, 6):
  for B0 in range(1, 6):
    for b in range(1, 4):
      for i in range(-6, 7):
        for j in range(-6, 7):
          if j * B0 - i * A * b == 0 and (i, j) != (0, 0):
            ok &= (i > 0 and j > 0) or (i < 0 and j < 0)
check(ok, 'Delta=0 forces i,j same strict sign, so w<=0 or w>=D+u>D')

# (d) k=0: w = D - 0*u = D, entire box
check(all((lambda D, u: D - 0 * u == D)(D, u) for D in range(1, 9) for u in range(1, 9)), 'k=0 gives w=D')

# (c) independent offset: T | a w1, T | c w2 => T | a c gcd(w1,w2)
ok = True
for T in range(1, 40):
  for w1 in range(1, 30):
    for w2 in range(1, 30):
      for a, c in [(2, 3), (4, 6), (1, 5)]:
        if (a * w1) % T == 0 and (c * w2) % T == 0:
          ok &= (a * c * gcd(w1, w2)) % T == 0
check(ok, 'Bezout step for two routes')

print(f'CPU seconds: {time.process_time() - T0:.2f}')
print(f'FAILURES: {len(FAIL)}')
