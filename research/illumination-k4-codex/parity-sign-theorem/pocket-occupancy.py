"""Prescribed symbolic algebra only; no geometric directions or paths generated."""
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import json

BASE=Path(__file__).resolve().parent
# Sparse polynomials in formal coefficients n,K,L,j,alpha,beta.
NV=6
ZERO={}
def constant(c):return {(0,)*NV:F(c)} if c else {}
def variable(i):
 e=[0]*NV;e[i]=1;return {tuple(e):F(1)}
def add(*polys):
 out={}
 for p in polys:
  for e,c in p.items():out[e]=out.get(e,F(0))+c
 return {e:c for e,c in out.items() if c}
def neg(p):return {e:-c for e,c in p.items()}
def mul(p,q):
 out={}
 for e,c in p.items():
  for f,d in q.items():
   k=tuple(x+y for x,y in zip(e,f));out[k]=out.get(k,F(0))+c*d
 return {e:c for e,c in out.items() if c}
def mm(a,b):return [[add(*(mul(x,y) for x,y in zip(row,col))) for col in zip(*b)] for row in a]
def det(a):return add(mul(a[0][0],a[1][1]),neg(mul(a[0][1],a[1][0])))
one=constant(1)
n,K,L,j,alpha,beta=[variable(i) for i in range(NV)]
nK=mul(n,K);Lj=mul(L,j)
Aw=[[one,nK],[ZERO,one]]
AwInv=[[one,neg(nK)],[ZERO,one]]
Aj=[[add(one,neg(Lj)),mul(L,mul(j,j))],[neg(L),add(one,Lj)]]
assert det(Aw)==det(Aj)==one
conjugate=mm(mm(Aw,Aj),AwInv)
assert conjugate[0][0]==add(one,neg(Lj),neg(mul(nK,L)))
assert conjugate[1][0]==neg(L)
# Conjugating sends the formal cylinder coefficient pair (j,1) to(j+nK,1).
assert mm(Aw,[[j],[one]])==[[add(j,nK)],[one]]
# A wall-line determinant is affine in n. If beta=0, it is -alpha*L.
wall_det=add(mul(alpha,conjugate[1][0]),neg(mul(beta,conjugate[0][0])))
assert all(e[0]<=1 for e in wall_det)
assert add(*( {e:c} for e,c in wall_det.items() if e[5]==0))==neg(mul(alpha,L))

# Abstract homology control: eta=e0, z=e1, Nw z=e2; no surface claimed.
I3=[[one if r==c else ZERO for c in range(3)] for r in range(3)]
Nw=[[ZERO,ZERO,ZERO],[ZERO,ZERO,ZERO],[ZERO,one,ZERO]]
Nj=[[ZERO,ZERO,ZERO],[one,ZERO,ZERO],[ZERO,ZERO,ZERO]]
plus=[[add(I3[r][c],mul(n,Nw[r][c])) for c in range(3)] for r in range(3)]
minus=[[add(I3[r][c],neg(mul(n,Nw[r][c]))) for c in range(3)] for r in range(3)]
tau=[[add(I3[r][c],Nj[r][c]) for c in range(3)] for r in range(3)]
assert mm(Nw,Nw)==[[ZERO]*3 for _ in range(3)]
assert mm(mm(mm(plus,tau),minus),[[one],[ZERO],[ZERO]])==[[one],[one],[n]]

# Occupancy coefficients, not cylinder measurements from a room.
rs=[(F(1),F(2)),(F(3),F(-1))]
ls=[F(3,4),F(1,4)];lt=[F(1,4),F(3,4)]
assert sum(ls)==sum(lt)==1
weighted=tuple(sum(rs[i][k]*(lt[i]-ls[i]) for i in range(2)) for k in range(2))
assert weighted==(F(1),F(-3,2))
# Grouping several marked strips with the same maximal-cylinder ratio.
strip_weights=[F(-1,4),F(-1,4),F(1,2)]
strip_ratios=[rs[0],rs[0],rs[1]]
assert tuple(sum(strip_ratios[i][k]*strip_weights[i] for i in range(3)) for k in range(2))==weighted
# Unimodular halves each have occupancy1 in one cylinder.
assert tuple(rs[1][k]-rs[0][k] for k in range(2))==(F(2),F(-3))
# Only a count is checked; no image directions or integer powers are selected.
wall_lines=4;possible_zero_defects=1;excluded_bound=wall_lines+possible_zero_defects
assert excluded_bound==5 and excluded_bound+1==6

# Fixed annulus-cover degree arithmetic, not a surface decomposition.
cover_degrees=(2,3,4)
degree=sum(cover_degrees)
level=lcm(*range(1,degree+1))
assert degree==9 and level==2520
assert all(level % width == 0 for width in cover_degrees)

out={
 'status':'PRESCRIBED_OCCUPANCY_AND_RESIDUE_ALGEBRA_PASS',
 'symbolic_variables':['n','K','L','j','alpha','beta'],
 'controls':[
  'formal_parabolic_determinants',
  'formal_Bezout_residue_conjugacy',
  'formal_image_half_vector_coefficients',
  'wall_line_determinant_affine_in_n',
  'abstract_relative_nilpotent_conjugation',
  'weighted_occupancy_and_strip_grouping',
  'unit_occupancy_flux_contrast',
  'six_images_exceed_five_possible_exclusions',
  'fixed_annulus_degree_common_level_arithmetic'],
 'formulas':{'increment':'z_j+n N_w z_j','defect':'b_j+n d_j','image_half_vector':'(1-n K L_j)w-L_j v_j'},
 'scope':'Formal coefficient polynomials, one abstract3dimensional nilpotent representation and prescribed rational occupancy weights only. No geometric direction, cylinder, room, event, word or orbit was discovered or traced.',
 'degree_control':{'component_cover_degrees':cover_degrees,'total_degree':degree,'common_level':level},
 'geometric_hypotheses':'Actual seed still required. Marked refinement, torus-lift pure parabolics, occupancy and finite-residue proofs accepted by two tools-disabled reviews; this checker verifies only prescribed algebra, not actual path existence.',
 'independent_review':'TWO_TOOLS_DISABLED_OPUS_REVIEWS_ACCEPTED_EXIT0; corrections to pairing/sign/pure-scope and chart-derivative wording incorporated; no independent code execution claimed','goal_complete':False,'discovery_runs':0}
(BASE/'pocket-occupancy.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
