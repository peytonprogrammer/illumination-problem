"""Exact angular and matrix controls. No billiard rays or room search."""
from pathlib import Path
from fractions import Fraction as F
import itertools,math,json
B=Path(__file__).resolve().parent
angles=0
for alpha in [F(5,4),F(3,2),F(7,4)]:
 for j in range(33):
  phi=alpha*j/32
  probes={alpha*i/128 for i in range(1,128)}
  probes.update(x for x in [phi-1,phi+1] if 0<x<alpha)
  for psi in probes:
   direct=abs(psi-phi)<1
   images=any(abs(psi-(sign*phi+2*k*alpha))<1 for sign in [-1,1] for k in range(-2,3))
   shadow=(psi<=phi-1) if phi>1 else ((psi>=phi+1) if phi<alpha-1 else False)
   assert images==direct and shadow==(not direct)
   angles+=1
  length=phi-1 if phi>1 else (alpha-phi-1 if phi<alpha-1 else F(0))
  assert 0<=length<=alpha-1
  if 0<phi<alpha:assert length<alpha-1
# Endpoint exceptions to the strict shadow-length claim.
endpoint=[{'alpha_over_pi':str(a),'phi_over_pi':'0','shadow_length_over_pi':str(a-1),'equals_alpha_minus_pi':True} for a in [F(5,4),F(3,2),F(7,4)]]

def mul(A,C):return tuple(tuple(sum(A[i][k]*C[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
def add(A,C):return tuple(tuple(A[i][j]+C[i][j] for j in (0,1)) for i in (0,1))
def scale(n,A):return tuple(tuple(n*x for x in row) for row in A)
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def trace(A):return A[0][0]+A[1][1]
def apply(A,v):return tuple(sum(A[i][j]*v[j] for j in (0,1)) for i in (0,1))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def N(r):return ((-r[0]*r[1],r[0]*r[0]),(-r[1]*r[1],r[1]*r[0]))
I=((1,0),(0,1));O=((0,0),(0,0));vectors=[(1,0),(0,1),(1,1),(1,-1),(2,1),(-1,2)]
matrices=0
for r,s in itertools.product(vectors,repeat=2):
 D=cross(r,s)
 if not D:continue
 R,S=N(r),N(s);leading=mul(R,S)
 assert mul(R,R)==O and mul(S,S)==O
 assert trace(leading)==-D*D and apply(leading,s)==(0,0)
 for col in zip(*leading):assert cross(r,col)==0
 for n in [3,10,100]:
  A=mul(add(I,scale(n,R)),add(I,scale(n,S)))
  assert det(A)==1 and trace(A)==2-n*n*D*D and abs(trace(A))>2
  A2=mul(A,A);assert det(A2)==1 and trace(A2)>2
  assert A==add(add(I,scale(n,add(R,S))),scale(n*n,leading))
  matrices+=1
# There are 4k alternating attractive/repelling rays for the two eigenlines.
# An orientation-preserving color-preserving permutation shifts by an even number.
cone=0
for k in range(1,8):
 for shift in range(0,4*k,2):
  assert all((i+2*k*shift)%(4*k)==i for i in range(4*k))
  cone+=1
out={'status':'PASS','exact_angle_probes':angles,'shadow_formula_matches_image_union':True,'strict_length_endpoint_corrections':endpoint,'integer_parabolic_product_controls':matrices,'cone_eigenray_power_controls':cone,'scope':'Exact angle identities and elementary matrix/permutation identities only. The density theorem is a written analytic argument using finite labeled torus-cover data; no physical geodesic orbit or room was computed.'}
(B/'reflex-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
