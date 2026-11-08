"""Exact algebraic gates for changing a billiard's mirror action.
No new action on an actual room surface, quotient, or dark room is asserted.
"""
import json
from pathlib import Path
from itertools import product
from fractions import Fraction as F
ROOT=Path(__file__).parent
I=(1,0,0,1); R=(0,-1,1,0); J=(1,0,0,-1)
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def tr(a):return(a[0],a[2],a[1],a[3])
def det(a):return a[0]*a[3]-a[1]*a[2]
def inv(a):
 d=det(a);assert d
 return tuple(F(v,d) for v in (a[3],-a[1],-a[2],a[0]))
def group(r,j):
 g={I};todo=[I]
 for a in todo:
  for b in(r,j):
   c=mul(a,b)
   if c not in g:g.add(c);todo.append(c)
 return sorted(g)
def rank(rows):
 a=[list(map(F,r)) for r in rows];k=0
 for col in range(3):
  piv=next((i for i in range(k,len(a)) if a[i][col]),None)
  if piv is None:continue
  a[k],a[piv]=a[piv],a[k];v=a[k][col];a[k]=[x/v for x in a[k]]
  for i in range(len(a)):
   if i!=k:
    v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
  k+=1
 return k
basis=[(1,0,0,0),(0,1,1,0),(0,0,0,1)]
def constraints(g):
 rows=[]
 for a in g:
  transformed=[tuple(x-y for x,y in zip(mul(mul(tr(a),b),a),b)) for b in basis]
  rows.extend([[b[i] for b in transformed] for i in (0,1,3)])
 return rows
G=group(R,J);assert len(G)==8
assert rank(constraints(G))==2
assert rank(constraints(group(mul(R,R),J)))==1
reflections=[]
for a in product(range(-6,7),repeat=4):
 if det(a)==-1 and mul(a,a)==I and mul(mul(a,R),a)==inv(R):reflections.append(a)
assert len(reflections)==4
assert set(reflections)=={(1,0,0,-1),(-1,0,0,1),(0,1,1,0),(0,-1,-1,0)}
# Exhaustive integer conclusion follows from a=[[u,v],[v,-u]], u^2+v^2=1;
# the bounded enumeration is a cross-check, not a proof outside its range.
conjugates=[]
for M in ((1,1,0,1),(1,2,0,1),(2,1,1,1)):
 H=[mul(mul(M,g),inv(M)) for g in G]
 Q=tuple(sum(mul(tr(h),h)[i] for h in H) for i in range(4))
 assert Q[0]>0 and det(Q)>0
 assert all(mul(mul(tr(h),Q),h)==Q for h in H)
 B=mul(tr(inv(M)),inv(M));scale=F(Q[0],B[0])
 assert Q==tuple(scale*x for x in B)
 conjugates.append(dict(M=M,averaged_metric=Q,metric_is_conjugated_original=True))
# Test the claimed slit-axis flow conjugacy at an interior slit tip.
# In a symmetric square with slit {(0,y):0<=y<=1}, p=(0,0) is absorbing.
# Folding to the left half makes p a smooth point of the vertical wall.
S=(F(-1,2),F(-1,2));p=(F(0),F(0));T=(F(-1,2),F(1,2))
incoming=tuple(p[i]-S[i] for i in (0,1));outgoing=tuple(T[i]-p[i] for i in (0,1))
assert outgoing==(-incoming[0],incoming[1])
slit_tip_gate=dict(original_tip_absorbing=True,folded_tip_is_smooth=True,
 reflected_path_in_half_room=[S,p,T],same_path_invalid_in_original=True,
 scope='Counterexample to the proposed exact local flow conjugacy, not a counterexample to its global darkness equivalence.')
result=dict(status='PASS_ALGEBRAIC_GATES_ONLY',slit_tip_conjugacy_gate=slit_tip_gate,D4_invariant_symmetric_metric_dimension=1,D2_invariant_symmetric_metric_dimension=2,reflections_compatible_with_fixed_standard_quarter_turn=reflections,free_orbit_orders_dividing_eight=[d for d in(2,4,6,8,12) if 8%d==0],conjugate_group_checks=conjugates,scope='Algebraic necessary conditions; no enumeration of affine actions on the actual room, no alternative planar quotient found.')
(ROOT/'reset-probe.json').write_text(json.dumps(result,indent=2,default=str)+'\n');print(json.dumps(result,default=str))
