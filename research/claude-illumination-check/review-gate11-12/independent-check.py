#!/usr/bin/env python3
"""Independent fixed-matrix recheck of pocket-reflection-gate.md Sections 11-12.

Rebuilds every matrix from the index formulas in Matheus--Yoccoz
arXiv:0912.1425v2, Sections 3.3, 3.5, 3.7, instead of reusing the Codex
checker's hand-typed blocks. Exact rational arithmetic only. No search,
scan, word enumeration, or geometric discovery.
"""
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
out = {}


def mul(a, b):
    return [[sum(x * y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def tr(a):
    return [list(r) for r in zip(*a)]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def neg(a):
    return [[-x for x in r] for r in a]


def mpow(a, k):
    r = eye(len(a))
    for _ in range(k):
        r = mul(r, a)
    return r


def inv(a):
    n = len(a)
    m = [[F(x) for x in r] + [F(int(i == j)) for j in range(n)] for i, r in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        pv = m[c][c]
        m[c] = [x / pv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [[x for x in r[n:]] for r in m]


def rank(a):
    m = [[F(x) for x in r] for r in a]
    rk, rows, cols = 0, len(m), len(m[0]) if m else 0
    for c in range(cols):
        p = next((r for r in range(rk, rows) if m[r][c] != 0), None)
        if p is None:
            continue
        m[rk], m[p] = m[p], m[rk]
        for r in range(rows):
            if r != rk and m[r][c] != 0:
                f = m[r][c] / m[rk][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[rk])]
        rk += 1
    return rk


def det(a):
    m = [[F(x) for x in r] for r in a]
    n, d = len(m), F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d


checks = {}


def check(name, cond):
    assert cond, name
    checks[name] = True


# ---------------------------------------------------------------------------
# 1. H_b from the paper's 6 generators sigma_i, zeta_i (i in Z/3), sum zero.
#    Reduced basis (s0, s1, z0, z1); s2 = -s0-s1, z2 = -z0-z1.
# ---------------------------------------------------------------------------
def vec(kind, i):
    """Coordinates of breve-sigma_i or breve-zeta_i in (s0,s1,z0,z1)."""
    i %= 3
    base = [0, 0] if kind == 's' else [2, 2]
    v = [0, 0, 0, 0]
    off = 0 if kind == 's' else 2
    if i == 2:
        v[off], v[off + 1] = -1, -1
    else:
        v[off + i] = 1
    return v


def add(*vs):
    return [sum(c) for c in zip(*vs)]


def cols(images):
    return tr(images)


# Paper 3.7 table (equivalently the q=3 table of 3.3):
#   S s_i = s_i + z_{i-1};  S z_i = z_{i+1}
#   T s_i = s_{i-1};        T z_i = z_i + s_{i+1}
S_b = cols([add(vec('s', 0), vec('z', -1)), add(vec('s', 1), vec('z', 0)),
            vec('z', 1), vec('z', 2)])
T_b = cols([vec('s', -1), vec('s', 0),
            add(vec('z', 0), vec('s', 1)), add(vec('z', 1), vec('s', 2))])

# Consistency of the table with the sum-zero relation (images of s2, z2).
check('S table respects sum relation',
      mul(S_b, [[x] for x in vec('s', 2)]) == [[x] for x in add(vec('s', 2), vec('z', 1))]
      and mul(S_b, [[x] for x in vec('z', 2)]) == [[x] for x in vec('z', 0)])
check('T table respects sum relation',
      mul(T_b, [[x] for x in vec('s', 2)]) == [[x] for x in vec('s', 1)]
      and mul(T_b, [[x] for x in vec('z', 2)]) == [[x] for x in add(vec('z', 2), vec('s', 0))])

# Paper 3.7 intersection numbers (Lemma 3.4 proof), as a 6x6 Gram matrix on
# (s0,s1,s2,z0,z1,z2), then reduced. (s_i,s_{i+1})=(z_i,z_{i+1})=6,
# (s_i,z_i)=-4, (s_i,z_{i+1})=(s_i,z_{i-1})=2.
gram6 = [[0] * 6 for _ in range(6)]
for i in range(3):
    j = (i + 1) % 3
    gram6[i][j], gram6[j][i] = 6, -6
    gram6[3 + i][3 + j], gram6[3 + j][3 + i] = 6, -6
    for k, val in ((i, -4), ((i + 1) % 3, 2), ((i - 1) % 3, 2)):
        gram6[i][3 + k], gram6[3 + k][i] = val, -val
ones_s = [1, 1, 1, 0, 0, 0]
ones_z = [0, 0, 0, 1, 1, 1]
check('paper pairings vanish on sum(s_i)', mul([ones_s], gram6) == [[0] * 6])
check('paper pairings vanish on sum(z_i)', mul([ones_z], gram6) == [[0] * 6])
lift = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
Omega_b = mul(mul(tr(lift), gram6), lift)

# Codex transcription (pocket-reflection-gate-check.py lines 97-107).
P = [[0, -1], [1, -1]]
P2 = mul(P, P)
I2, Z2 = eye(2), [[0, 0], [0, 0]]


def blk(a, b, c, d):
    return [x + y for x, y in zip(a, b)] + [x + y for x, y in zip(c, d)]


codex_S = blk(I2, Z2, P2, P)
codex_T = blk(P2, P, Z2, I2)
codex_Omega = [[0, 6, -4, 2], [-6, 0, 2, -4], [4, -2, 0, 6], [-2, 4, -6, 0]]
check('S matches Codex transcription', S_b == codex_S)
check('T matches Codex transcription', T_b == codex_T)
check('Omega_b matches Codex transcription', Omega_b == codex_Omega)

Tinv = inv(T_b)
R_b = mul(mul(Tinv, S_b), Tinv)
check('R_b = [[0,-I],[I,0]]', R_b == blk(Z2, neg(I2), I2, Z2))
check('braid relation S T^-1 S = T^-1 S T^-1', mul(mul(S_b, Tinv), S_b) == R_b)
check('R_b^4 = I', mpow(R_b, 4) == eye(4))
check('(S T^-1)^3 = R_b^2', mpow(mul(S_b, Tinv), 3) == mul(R_b, R_b))
check('Z/3 deck action preserves Omega_b',
      mul(mul(tr(blk(P, Z2, Z2, P)), Omega_b), blk(P, Z2, Z2, P)) == Omega_b)

# Uniqueness: dimension of S,T-invariant antisymmetric forms on Q^4.
basis_pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]


def antisym(coeffs):
    m = [[0] * 4 for _ in range(4)]
    for (i, j), c in zip(basis_pairs, coeffs):
        m[i][j], m[j][i] = c, -c
    return m


rows = []
for g in (S_b, T_b):
    eqcols = []
    for k in range(6):
        e = [int(t == k) for t in range(6)]
        X = antisym(e)
        D = mul(mul(tr(g), X), g)
        eqcols.append([D[i][j] - X[i][j] for i, j in basis_pairs])
    rows += tr(eqcols)
inv_dim = 6 - rank(rows)
check('S,T-invariant antisymmetric forms on H_b are one-dimensional', inv_dim == 1)

# H_tau from 3.3: S tau_i = -tau_{i+1}, T tau_i = -tau_{i-1}; basis (t0,t1).
S_tau = neg(P)
T_tau = neg(P2)
R_tau = mul(mul(inv(T_tau), S_tau), inv(T_tau))
check('R on H_tau is -I', R_tau == neg(I2))
# H_st from 3.3: S sigma = sigma+zeta, S zeta = zeta; T sigma = sigma, T zeta = zeta+sigma.
S_st = [[1, 0], [1, 1]]
T_st = [[1, 1], [0, 1]]
R_st = mul(mul(inv(T_st), S_st), inv(T_st))
check('R on T_0 is J', R_st == [[0, -1], [1, 0]])
# Fixed-space dimensions for the transfer genus formula.
R_full_blocks = [R_st, R_tau, R_b]


def fixdim(m):
    n = len(m)
    return n - rank([[m[i][j] - int(i == j) for j in range(n)] for i in range(n)])


fixR = sum(fixdim(m) for m in R_full_blocks)
fixR2 = sum(fixdim(mul(m, m)) for m in R_full_blocks)
check('genus X/<R> = 0', fixR == 0)
check('genus X/<R^2> = 1', fixR2 == 2)

# ---------------------------------------------------------------------------
# 2. Rotation form and an independent rational diagonalization.
# ---------------------------------------------------------------------------
G = mul(Omega_b, R_b)
check('G symmetric', G == tr(G))
check('G matches Section 11 display',
      G == [[-4, 2, 0, -6], [2, -4, 6, 0], [0, 6, -4, 2], [-6, 0, 2, -4]])


def ldl(a):
    """Rational diagonalization of a symmetric matrix by congruence."""
    n = len(a)
    m = [[F(x) for x in r] for r in a]
    diag = []
    for k in range(n):
        p = m[k][k]
        assert p != 0, 'zero pivot; would need a pivot swap'
        diag.append(p)
        for i in range(k + 1, n):
            f = m[i][k] / p
            for j in range(k + 1, n):
                m[i][j] -= f * m[k][j]
        for i in range(k + 1, n):
            m[i][k] = m[k][i] = F(0)
    return diag


diag_negG = ldl(neg(G))
out['diag_of_minus_G'] = [str(x) for x in diag_negG]
disc = 1
for x in diag_negG:
    disc *= x
check('det G = 576 = 24^2 (square discriminant)', det(G) == 576)


def hilbert_p(a, b, p):
    """Hilbert symbol (a,b)_p for nonzero rationals, odd prime p or p=2."""
    def split(x):
        x = F(x)
        num, den = x.numerator, x.denominator
        v = 0
        while num % p == 0:
            num //= p
            v += 1
        while den % p == 0:
            den //= p
            v -= 1
        return v, num * den  # unit part up to squares: num/den ~ num*den
    va, ua = split(a)
    vb, ub = split(b)
    if p != 2:
        def leg(u):
            r = pow(u % p, (p - 1) // 2, p)
            return -1 if r == p - 1 else 1
        s = (-1) ** ((va * vb * (p - 1) // 2) % 2)
        return s * leg(ua) ** vb * leg(ub) ** va
    eps = lambda u: ((u - 1) // 2) % 2
    omg = lambda u: ((u * u - 1) // 8) % 2
    e = eps(ua) * eps(ub) + va * omg(ub) + vb * omg(ua)
    return (-1) ** (e % 2)


def hasse(diag, p):
    h = 1
    for i in range(len(diag)):
        for j in range(i + 1, len(diag)):
            h *= hilbert_p(diag[i], diag[j], p)
    return h


# A 4-dim form with square discriminant is isotropic over Q_p iff its Hasse
# invariant equals (-1,-1)_p (equivalently it is hyperbolic there).
local = {}
for p in (2, 3, 5, 7):
    local[p] = hasse(diag_negG, p) == hilbert_p(-1, -1, p)
out['minus_G_isotropic_over_Q_p'] = {str(k): v for k, v in local.items()}
check('-G anisotropic over Q_3 (descent prime)', local[3] is False)
check('-G anisotropic over Q_2', local[2] is False)
# Same invariant as <1,1,-6,-6>, the norm form of (-1,6)_Q.
ref = [1, 1, -6, -6]
check('-G locally equivalent to <1,1,-6,-6> at 2,3',
      all(hasse(diag_negG, p) == hasse(ref, p) for p in (2, 3)))

# ---------------------------------------------------------------------------
# 3. Section 12: reflection, eigenspace, (12.1), triple cancellation.
# ---------------------------------------------------------------------------
L = [[1, -1], [0, -1]]
check('L implements i -> -i on s', [r for r in tr(L)] == [vec('s', 0)[:2], vec('s', -1)[:2]])
V_b = blk(L, Z2, Z2, neg(L))
check('V_b involution', mul(V_b, V_b) == eye(4))
check('V_b antisymplectic', mul(mul(tr(V_b), Omega_b), V_b) == neg(Omega_b))
check('V_b R V_b = R^-1', mul(mul(V_b, R_b), V_b) == inv(R_b))
neg_basis = [[1, 2, 0, 0], [0, 0, 1, 0]]  # (a,2a,c,0)
check('V_b negative eigenspace basis',
      all(mul(V_b, [[x] for x in v]) == [[-x] for x in v] for v in neg_basis)
      and rank([[V_b[i][j] + int(i == j) for j in range(4)] for i in range(4)]) == 2)
# Restriction of G to (a,c) coordinates must equal -4*[[ -3, 3],[3,-1]]... i.e.
# -4((c-3a)^2-6a^2) = -4(c^2 - 6ac + 3a^2): Gram [[-12, 12],[12, -4]].
Bn = tr(neg_basis)
Gres = mul(mul(tr(Bn), G), Bn)
check('(12.1) restricted Gram', Gres == [[-12, 12], [12, -4]])
check('(12.1) restricted form anisotropic (6 not a square)',
      hasse(ldl(Gres), 3) is not None and det(Gres) == -96)  # -96 = -6*16, not -square
# Two V-negative copies: <1,-6,1,-6> ~ <1,1,-6,-6>, anisotropic -> need 3 copies.
two = ldl([[-12, 12, 0, 0], [12, -4, 0, 0], [0, 0, -12, 12], [0, 0, 12, -4]])
check('two V-negative copies remain anisotropic at 3',
      hasse(two, 3) != hilbert_p(-1, -1, 3))


def block_diag(*ms):
    n = sum(len(m) for m in ms)
    r = [[0] * n for _ in range(n)]
    o = 0
    for m in ms:
        for i, row in enumerate(m):
            r[o + i][o:o + len(m)] = row
        o += len(m)
    return r


O3, R3, V3 = (block_diag(m, m, m) for m in (Omega_b, R_b, V_b))
b = [1, 2, 4, 0, 0, 0, 1, 0, 0, 0, 2, 0]
Rb = [r[0] for r in mul(R3, [[x] for x in b])]
check('R_3 b matches Section 12 display', Rb == [-4, 0, 1, 2, -1, 0, 0, 0, -2, 0, 0, 0])
vals = [mul(mul([b[4 * k:4 * k + 4]], G), [[x] for x in b[4 * k:4 * k + 4]])[0][0] for k in range(3)]
check('block values 20,-4,-16', vals == [20, -4, -16])
check('Omega_3(b, R_3 b) = 0', mul(mul([b], O3), [[x] for x in Rb]) == [[0]])
check('V_3 b = -b', [r[0] for r in mul(V3, [[x] for x in b])] == [-x for x in b])
check('V_3 R_3 b = R_3 b', [r[0] for r in mul(V3, [[x] for x in Rb])] == Rb)
check('saturating minor rows 4,6', [[b[4], Rb[4]], [b[6], Rb[6]]] == [[0, -1], [1, 0]]
      and det([[b[4], Rb[4]], [b[6], Rb[6]]]) == 1)
# Without the V constraint, two copies already admit an isotropic R-plane.
b2 = [1, 0, 0, 0, 1, 0, 0, -1]
O2, R2 = block_diag(Omega_b, Omega_b), block_diag(R_b, R_b)
Rb2 = [r[0] for r in mul(R2, [[x] for x in b2])]
check('two copies, no V constraint: isotropic R-plane exists',
      mul(mul([b2], O2), [[x] for x in Rb2]) == [[0]])

# ---------------------------------------------------------------------------
# 4. Neck reflection convention from 31.1, on the D4 coset labels.
# ---------------------------------------------------------------------------
# D4 as pairs (k, s): R^k V^s, with V R V = R^-1. Left action by V.
def d4mul(x, y):
    k1, s1 = x
    k2, s2 = y
    return ((k1 + (-k2 if s1 else k2)) % 4, (s1 + s2) % 2)


coset = {j: frozenset({(j, 0), d4mul((j, 0), (0, 1))}) for j in range(4)}
Vel = (0, 1)
images = {}
for j, cs in coset.items():
    img = frozenset(d4mul(Vel, g) for g in cs)
    images[j] = next(k for k, c in coset.items() if c == img)
check('left V maps annulus j to annulus -j', all(images[j] == (-j) % 4 for j in range(4)))
# V reverses orientation, so V b_j = -b_{-j}. Then on beta_0=b0-b2, beta_1=b1-b3:
Vb = {j: (-1, (-j) % 4) for j in range(4)}  # sign, target index


def apply_V(comb):
    res = [0] * 4
    for j, c in enumerate(comb):
        s, t = Vb[j]
        res[t] += s * c
    return res


check('V beta_0 = -beta_0', apply_V([1, 0, -1, 0]) == [-1, 0, 1, 0])
check('V beta_1 = beta_1', apply_V([0, 1, 0, -1]) == [0, 1, 0, -1])

out['checks'] = checks
out['check_count'] = len(checks)
out['S_b'], out['T_b'], out['Omega_b'], out['R_b'], out['G'] = S_b, T_b, Omega_b, R_b, G
out['invariant_antisymmetric_form_dim'] = inv_dim
out['scope'] = ('Fixed rational linear algebra rebuilt from arXiv:0912.1425v2 3.3/3.5/3.7 '
                'index formulas; no geometric realization, scan or search.')
(HERE / 'independent-check.json').write_text(json.dumps(out, indent=2, default=str) + '\n')
print(json.dumps({'status': 'PASS', 'check_count': len(checks),
                  'diag_minus_G': out['diag_of_minus_G'],
                  'isotropic_over_Qp': out['minus_G_isotropic_over_Q_p']}))
