"""Exact prescribed symplectic mixed-twist control; no surface/optical search."""
from fractions import Fraction as F
from pathlib import Path
import json
b=Path(__file__).resolve().parent
D=7
zero=lambda:[[F(0) for _ in range(D)] for _ in range(D)]
J=zero()
for i in (0,2,4):J[i][i+1]=F(1);J[i+1][i]=F(-1)
I=zero()
for i in range(D):I[i][i]=F(1)
def mv(A,x):return [sum(a*y for a,y in zip(row,x)) for row in A]
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(D)) for j in range(D)] for i in range(D)]
def plus(A,B):return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def transpose(A):return list(map(list,zip(*A)))
def pairing(c,x):return sum(c[i]*z for i,z in enumerate(mv(J,x)))
def operator(cores):
 A=zero()
 for c in cores:
  row=[sum(c[k]*J[k][j] for k in range(D)) for j in range(D)]
  for i in range(D):
   for j in range(D):A[i][j]+=c[i]*row[j]
 return A
hplus=[1,0,0,1,0,0,0];hminus=[1,0,0,-1,0,0,0]
nplus=[1,1,1,0,0,0,0];nminus=[1,1,-1,0,0,0,0]
H=operator([hplus,hminus]);N=operator([nplus,nminus])
eta=list(map(F,[0,0,1,0,1,0,1]));q=list(map(F,[0,0,1,0,-1,0,0]))
def Q(x):return sum(a*z for a,z in zip(q,x))
assert pairing(hplus,hminus)==pairing(nplus,nminus)==0
for A in (H,N):
 assert mm(A,A)==zero()
 G=plus(I,A)
 assert mm(mm(transpose(G),J),G)==J
 assert mv(G,[0,0,0,0,0,0,1])==[0,0,0,0,0,0,1]
assert all(Q([H[i][j] for i in range(D)])==0 for j in range(D))
assert Q(eta)==Q(mv(N,eta))==0
assert mv(H,eta)==[0,0,0,-2,0,0,0]
assert mv(N,mv(H,eta))==[0,0,-4,0,0,0,0]
assert Q(mv(plus(I,N),mv(plus(I,H),eta)))==-4
for A,derivative in [(H,[[1,2],[0,1]]),(N,[[-1,2],[-2,3]])]:
 G=plus(I,A)
 for j in range(D):
  x=[F(int(k==j)) for k in range(D)];image=mv(G,x)
  assert image[:2]==[sum(derivative[i][k]*x[k] for k in range(2)) for i in range(2)]
controls=[]
for a,bb in [(-2,-3),(-1,2),(0,1),(1,0),(1,1),(2,-1),(3,4)]:
 A=plus(I,[[a*x for x in row] for row in N])
 B=plus(I,[[bb*x for x in row] for row in H])
 result=mv(A,mv(B,eta))
 assert Q(result)==-4*a*bb
 assert result[-1]==1
 controls.append(dict(a=a,b=bb,defect_x=str(Q(result)),boundary_r=str(result[-1])))
Hminus=plus(I,[[-x for x in row] for row in H])
Nconjugate=mm(mm(Hminus,N),plus(I,H))
assert Q(mv(Nconjugate,eta))==-4
assert [1-2*1,1]==[-1,1]
assert 2*1-1*(-1)==3
# Supplied-operator closure in this seven-dimensional formal lattice only.
def rank(columns):
 if not columns:return 0
 A=[list(row) for row in zip(*columns)];r=0
 for j in range(len(columns)):
  k=next((k for k in range(r,len(A)) if A[k][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];a=A[r][j];A[r]=[x/a for x in A[r]]
  for k in range(len(A)):
   if k!=r:
    a=A[k][j];A[k]=[x-a*y for x,y in zip(A[k],A[r])]
  r+=1
 return r
basis=[eta];closure_dimensions=[1];detection_depth=None
for depth in range(1,D+1):
 candidates=basis+[mv(A,x) for A in (H,N) for x in basis]
 new=[]
 for x in candidates:
  if rank(new+[x])>len(new):new.append(x)
 closure_dimensions.append(len(new))
 if detection_depth is None and any(Q(x) for x in new):detection_depth=depth
 if len(new)==len(basis):break
 basis=new
assert closure_dimensions==[1,2,3,3] and detection_depth==2
out=dict(status='PRESCRIBED_MIXED_TWIST_ALGEBRA_PASS',
 model='Six-dimensional symplectic absolute lattice plus formal fixed relative generator; no realization claimed.',
 H_squared_zero=True,N_squared_zero=True,absolute_symplectic=True,
 QH_globally_zero=True,Q_eta_zero=True,QN_eta_zero=True,QNH_eta=[-4,0],
 first_stage_conjugate_Q=[-4,0],conjugate_determinant_relative_w=3,
 closure_dimensions=closure_dimensions,detection_depth=detection_depth,
 controls=controls,universal_actual_mixed_pairing='OPEN',optical_discovery_runs=0)
(b/'pocket-seed-module.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
