"""Prescribed C4 pocket topology and cup-form controls, not a surface search."""
from fractions import Fraction as F
from pathlib import Path
import json
b=Path(__file__).resolve().parent
D=5
I=[[F(int(i==j)) for j in range(D)] for i in range(D)]
R=[[F(x) for x in row] for row in [[0,-1,0,0,0],[1,0,0,0,0],
    [0,0,0,0,-1],[0,0,1,0,-1],[0,0,0,1,-1]]]
J=[[F(0) for _ in range(D)] for _ in range(D)];J[0][1]=1;J[1][0]=-1
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(D)) for j in range(D)] for i in range(D)]
def mv(A,x):return [sum(a*y for a,y in zip(row,x)) for row in A]
def tr(A):return list(map(list,zip(*A)))
R2=mm(R,R);assert mm(R2,R2)==I
assert mm(mm(tr(R),J),R)==J
assert mm(J,R)==[[F(int(i==j and i<2)) for j in range(D)] for i in range(D)]
beta0=list(map(F,[0,0,1,0,-1]));beta1=list(map(F,[0,0,1,2,1]))
assert mv(R,beta0)==beta1 and mv(R,beta1)==[-x for x in beta0]
assert mv(J,beta0)==mv(J,beta1)==[0]*D
# Exact RH and quotient topology for this ONE prescribed branch triple.
chi_U=4-3-3-2;boundaries_U=4;genus_U=(2-boundaries_U-chi_U)//2
chi_half=2-1-1;boundaries_half=2;genus_half=(2-boundaries_half-chi_half)//2
assert (chi_U,boundaries_U,genus_U)==(-4,4,1)
assert (chi_half,boundaries_half,genus_half)==(0,2,0)
# The handle isotropy identity is the matrix JR=diag(1,1,0,0,0),
# so <a,Ra>=a_handle_1^2+a_handle_2^2; no sample extrapolation.
out=dict(status='PRESCRIBED_POCKET_NECK_TOPOLOGY_CUP_PASS',
 branch_exponents=[1,1,2],U=dict(chi=chi_U,boundaries=boundaries_U,genus=genus_U),
 halfturn_quotient=dict(chi=chi_half,boundaries=boundaries_half,genus=genus_half),
 R_order_four=True,R_squared_minus_identity_on_handle=True,
 exact_handle_quadratic_form=[1,1,0,0,0],antisymmetric_boundary_generators=[list(map(int,beta0)),list(map(int,beta1))],
 scope='Prescribed topology and representation only. Material slide localization and absolute PD deduction require hand proof; actual event pairing remains open.',
 optical_discovery_runs=0)
(b/'pocket-neck.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
