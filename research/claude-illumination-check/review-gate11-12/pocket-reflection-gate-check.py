#!/usr/bin/env python3
"""Exact fixed polarized linear control; no geometry or discovery operations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def zero(n, m):
    return [[0] * m for _ in range(n)]

def tr(a):
    return [list(r) for r in zip(*a)]

def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]

def neg(a):
    return [[-x for x in row] for row in a]

def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def block(*blocks):
    n = sum(len(b) for b in blocks)
    out = zero(n, n)
    pos = 0
    for b in blocks:
        for i, row in enumerate(b):
            out[pos+i][pos:pos+len(b)] = row
        pos += len(b)
    return out

O = [[0, 1], [-1, 0]]
J = [[0, -1], [1, 0]]
A = [[-1, 0], [0, 1]]
omega = block(O, O, O)
r = block(J, J, neg(J))
v = block(A, A, A)
jh = block(J, J, J)
beta = tr([[0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, -1]])
c = tr([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0]])
k = tr(eye(6)[2:])
beta_rows = tr(beta)
qx = mul([beta_rows[1]], omega)[0]
qy = neg(mul([beta_rows[0]], omega))[0]
q = [qx, qy]
checks = {}

def check(name, left, right):
    assert left == right, (name, left, right)
    checks[name] = True

check('R symplectic', mul(mul(tr(r), omega), r), omega)
check('R square', mul(r, r), neg(eye(6)))
check('V antisymplectic', mul(mul(tr(v), omega), v), neg(omega))
check('V involution', mul(v, v), eye(6))
check('dihedral relation', mul(mul(v, r), v), tr(r))
check('Hodge complex structure', mul(jh, jh), neg(eye(6)))
check('Hodge positive metric identity', mul(omega, jh), eye(6))
check('R holomorphic at base', mul(r, jh), mul(jh, r))
check('V antiholomorphic at base', mul(v, jh), neg(mul(jh, v)))
check('R metric isometry', mul(tr(r), r), eye(6))
check('V metric isometry', mul(tr(v), v), eye(6))
check('neck independent explicit minor', [beta[2], beta[3]], [[1, 0], [0, 1]])
check('neck isotropic', mul(mul(tr(beta), omega), beta), zero(2, 2))
check('neck R representation', mul(r, beta), mul(beta, J))
check('neck reflection representation', mul(v, beta), mul(beta, A))
check('C symplectic', mul(mul(tr(c), omega), c), O)
check('K symplectic', mul(mul(tr(k), omega), k), block(O, O))
check('C K orthogonality', mul(mul(tr(c), omega), k), zero(2, 4))
check('C blind', mul(q, c), zero(2, 2))
check('Q nonzero explicit entry', q[0][2], -1)
check('Q rotation covariance', mul(q, r), mul(J, q))
check('Q reflection covariance', mul(q, v), mul(A, q))
check('K minus full', mul(mul(r, r), k), neg(k))
g = mul(mul(tr(k), omega), mul(r, k))
check('indefinite rotation form', g, [[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]])
check('rotation form neck zero', mul(mul(tr(beta), omega), mul(r, beta)), zero(2,2))

period = [[1,0,0,0,0,0], [0,1,0,0,0,0]]
check('neck holonomy zero', mul(period, beta), zero(2,2))
check('holonomy rotation covariance', mul(period, r), mul(J, period))
check('slide cochains primitive', mul(q, tr(period)), zero(2,2))


# Two fixed probes check the displayed pairing matrix; neither is a core.
probe = tr([[0,0,1,0,0,0]])
rprobe = mul(r, probe)
paircols = [x+y for x,y in zip(probe, rprobe)]
pairing = mul(mul(tr(beta), omega), paircols)
a, b = pairing[0][0], pairing[1][0]
check('rotation-pairing formula on fixed probe', pairing, [[a,-b],[b,a]])
assert a*a+b*b == 1
checks['pairing determinant'] = True
# Published q=3 matrices, Matheus--Yoccoz 0912.1425, Sections 3.3/3.7.
# This is a single fixed algebra replay, not a geometric construction.
p3 = [[0,-1],[1,-1]]
p3sq = mul(p3,p3)
i2 = eye(2)
z2 = zero(2,2)
def two_by_two_blocks(a,b,c,d):
    return [x+y for x,y in zip(a,b)] + [x+y for x,y in zip(c,d)]
os = two_by_two_blocks(i2,z2,p3sq,p3)
ot = two_by_two_blocks(p3sq,p3,z2,i2)
otinv = two_by_two_blocks(p3,neg(p3sq),z2,i2)
orot = mul(mul(otinv,os),otinv)
oomega = [[0,6,-4,2],[-6,0,2,-4],[4,-2,0,6],[-2,4,-6,0]]
og = mul(oomega,orot)
check('Orn P cubed',mul(p3sq,p3),i2)
check('Orn inverse T',mul(otinv,ot),eye(4))
check('Orn R composition',orot,two_by_two_blocks(z2,neg(i2),i2,z2))
check('Orn S symplectic',mul(mul(tr(os),oomega),os),oomega)
check('Orn T symplectic',mul(mul(tr(ot),oomega),ot),oomega)
check('Orn R symplectic',mul(mul(tr(orot),oomega),orot),oomega)
check('Orn R squared',mul(orot,orot),neg(eye(4)))
check('Orn rotation quadratic symmetric',og,tr(og))
# x=a+ic, y=b+id.  -v^t G v = |2x-(1+3i)y|^2-6|y|^2.
norm_change = [[2,-1,0,3],[0,-3,2,-1],[0,1,0,0],[0,0,0,1]]
norm_diag = [[1,0,0,0],[0,1,0,0],[0,0,-6,0],[0,0,0,-6]]
check('Orn rational norm identity',mul(mul(tr(norm_change),norm_diag),norm_change),neg(og))
orn_data = {'basis':['sigma0','sigma1','zeta0','zeta1'],
            'P':p3,'S':os,'T':ot,'R':orot,'Omega':oomega,'G_R':og,
            'norm_change':norm_change,'norm_diagonal':norm_diag,
            'scope':'Published fixed matrices and norm identity only; mod3 descent and geometry are hand arguments; no room counterexample.'}
# Direct-sum limitation of the rational gate.  Formal model only.
# No assertion that three copies occur as homology of a room or covering.
index_reverse = [[1,-1],[0,-1]]
ov = block(index_reverse,neg(index_reverse))
check('Orn block reflection involution',mul(ov,ov),eye(4))
check('Orn block reflection antisymplectic',mul(mul(tr(ov),oomega),ov),neg(oomega))
check('Orn block dihedral relation',mul(mul(ov,orot),ov),neg(orot))
triple_omega = block(oomega,oomega,oomega)
triple_r = block(orot,orot,orot)
triple_v = block(ov,ov,ov)
triple_beta0 = [1,2,4,0, 0,0,1,0, 0,0,2,0]
triple_beta1 = [row[0] for row in mul(triple_r,tr([triple_beta0]))]
triple_beta = tr([triple_beta0,triple_beta1])
check('Triple neck quarterturn',mul(triple_r,triple_beta),mul(triple_beta,J))
check('Triple neck reflection',mul(triple_v,triple_beta),mul(triple_beta,A))
check('Triple neck isotropy',mul(mul(tr(triple_beta),triple_omega),triple_beta),zero(2,2))
check('Triple coordinate lattice minor',[triple_beta[4],triple_beta[6]],[[0,-1],[1,0]])
triple_g = mul(triple_omega,triple_r)
triple_values = []
for part in ([1,2,4,0],[0,0,1,0],[0,0,2,0]):
    triple_values.append(mul(mul([part],og),tr([part]))[0][0])
check('Triple explicit cancellation',triple_values,[20,-4,-16])
triple_data = {'Omega':triple_omega,'R':triple_r,'V':triple_v,
               'beta_columns':triple_beta,'block_quadratic_values':triple_values,
               'scope':'Formal rational direct sum of three published blocks; no surface, geometric neck or actual event realization.'}
result = {
    'status':'PASS',
    'scope':'30 prior formal identities,9 published fixed-matrix/norm identities,8 multi-component control identities; no geometric realization or universal theorem verified',
    'check_count':len(checks), 'checks':checks,
    'omega':omega, 'R':r, 'V':v, 'J_H':jh,
    'ornithorynque_fixed_algebra':orn_data,
    'multi_component_arithmetic_control':triple_data,
    'beta_columns':beta, 'Q':q, 'G_R_on_K':g,
    'universal_pocket_detection':'OPEN',
    'independent_review':'pending live peer',
}
assert len(checks) == 47
(ROOT / 'pocket-reflection-gate-check.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'scope':result['scope']}))
