# Exact integer check of the Section 11 (Matheus--Yoccoz q=3) H_b matrices as
# quoted in pocket-reflection-gate.md lines 437-438 and 467-470. No search.
def mul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A): return [list(r) for r in zip(*A)]
def eye(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def blk(a, b, c, d): return [a[i]+b[i] for i in range(2)] + [c[i]+d[i] for i in range(2)]
def pw(A, n):
    M = eye(len(A))
    for _ in range(n): M = mul(M, A)
    return M
def rank(A):
    from fractions import Fraction
    M = [[Fraction(x) for x in r] for r in A]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
    return r

P = [[-1, -1], [1, 0]]            # i -> i+1 on sum-zero vectors, coords (x0, x1)
I2, O2 = eye(2), [[0, 0], [0, 0]]
negI2 = [[-1, 0], [0, -1]]
S = blk(I2, O2, mul(P, P), P)
T = blk(mul(P, P), P, O2, I2)
Tinv = pw(T, 2)                    # T has order 3 if P^3 = I and T^3 = I; verified below
Om = [[0, 6, -4, 2], [-6, 0, 2, -4], [4, -2, 0, 6], [-2, 4, -6, 0]]

print("P^3 == I:", pw(P, 3) == I2)
print("T^3 == I (so T^-1 = T^2):", pw(T, 3) == eye(4))
print("R = T^-1 S T^-1 == [[0,-I],[I,0]]:", mul(mul(Tinv, S), Tinv) == blk(O2, negI2, I2, O2))
print("S symplectic:", mul(mul(tr(S), Om), S) == Om)
print("T symplectic:", mul(mul(tr(T), Om), T) == Om)
T2 = pw(T, 2)
print("T^2 on H_b:", T2)
print("T^2 == I:", T2 == eye(4))
D = [[T2[i][j] - (i == j) for j in range(4)] for i in range(4)]
print("dim fixed space of T^2 on H_b:", 4 - rank(D))

print("--- row-vector convention v -> v M, invariance M Om M^t == Om ---")
print("S row-symplectic:", mul(mul(S, Om), tr(S)) == Om)
print("T row-symplectic:", mul(mul(T, Om), tr(T)) == Om)
R = mul(mul(Tinv, S), Tinv)
print("R col-symplectic:", mul(mul(tr(R), Om), R) == Om, " R row-symplectic:", mul(mul(R, Om), tr(R)) == Om)

print("--- dual (cohomology) convention: invariant form Om^-1 ---")
from fractions import Fraction
def inv(A):
    n = len(A); M = [[Fraction(x) for x in r] + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(A)]
    for c in range(n):
        p = next(i for i in range(c, n) if M[i][c] != 0); M[c], M[p] = M[p], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for i in range(n):
            if i != c: f = M[i][c]; M[i] = [a - f*b for a, b in zip(M[i], M[c])]
    return [r[n:] for r in M]
Oi = inv(Om)
for name, M in (("S", S), ("T", T)):
    print(name, "col Om^-1:", mul(mul(tr(M), Oi), M) == Oi, " row Om^-1:", mul(mul(M, Oi), tr(M)) == Oi)
print("--- does any of S,T preserve Om up to transpose of P blocks? check Om under P -> P^t ---")
Pt = tr(P)
S2 = blk(I2, O2, mul(Pt, Pt), Pt); T2b = blk(mul(Pt, Pt), Pt, O2, I2)
for name, M in (("S'", S2), ("T'", T2b)):
    print(name, "col:", mul(mul(tr(M), Om), M) == Om, " row:", mul(mul(M, Om), tr(M)) == Om)

print("--- all four orientations of P (shift on coords vs on basis, forward/back) ---")
cands = {"P": P, "P^2": mul(P, P), "P^t": tr(P), "(P^t)^2": mul(tr(P), tr(P))}
for nm, Q in cands.items():
    Sx = blk(I2, O2, mul(Q, Q), Q); Tx = blk(mul(Q, Q), Q, O2, I2)
    Rx = mul(mul(pw(Tx, 2), Sx), pw(Tx, 2))
    ok = lambda M: (mul(mul(tr(M), Om), M) == Om, mul(mul(M, Om), tr(M)) == Om)
    print(f"{nm:8s} S(col,row)={ok(Sx)} T(col,row)={ok(Tx)} R=[[0,-I],[I,0]]:{Rx == blk(O2, negI2, I2, O2)}")

print("=== consistent reading: P_b = [[0,-1],[1,-1]] (basis shift sigma_i -> sigma_(i+1)) ===")
Pb = [[0, -1], [1, -1]]
Sb = blk(I2, O2, mul(Pb, Pb), Pb); Tb = blk(mul(Pb, Pb), Pb, O2, I2)
print("P_b^3 == I:", pw(Pb, 3) == I2)
print("S_b, T_b preserve Om (col):", mul(mul(tr(Sb), Om), Sb) == Om, mul(mul(tr(Tb), Om), Tb) == Om)
ordT = next(n for n in range(1, 50) if pw(Tb, n) == eye(4))
print("order of T_b on H_b:", ordT)
T2b = pw(Tb, 2)
print("T_b^2:", T2b, " == I:", T2b == eye(4))
D = [[T2b[i][j] - (i == j) for j in range(4)] for i in range(4)]
print("dim fixed space of T_b^2 on H_b:", 4 - rank(D))
print("T_b^(ord) == I so a kappa-power with ord | kappa acts trivially:", pw(Tb, ordT) == eye(4))
