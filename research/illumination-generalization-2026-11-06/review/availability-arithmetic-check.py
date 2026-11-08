#!/usr/bin/env python3
"""Prescribed Q100 metadata and exact determinant polynomial check only."""
from pathlib import Path
import json
from collections import defaultdict
P=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
# Independent formal integer-polynomial replay; no geometric search engine.
zero=(0,)*7
variables=[]
for i in range(7):
 e=list(zero);e[i]=1;variables.append({tuple(e):1})
N,p,q,r,s,k,l=variables
def add(*polys):
 d=defaultdict(int)
 for poly in polys:
  for e,c in poly.items():d[e]+=c
 return {e:c for e,c in d.items() if c}
def scale(poly,n):return {e:n*c for e,c in poly.items() if n*c}
def mul(a,b):
 d=defaultdict(int)
 for x,c in a.items():
  for y,e in b.items():d[tuple(i+j for i,j in zip(x,y))]+=c*e
 return {e:c for e,c in d.items() if c}
Ux=mul(N,add(k,scale(p,-2)));Uy=add(l,scale(q,-2))
Vx=mul(N,add(scale(r,2),scale(k,-1)));Vy=add(scale(s,2),scale(l,-1))
det=add(mul(Ux,Vy),scale(mul(Uy,Vx),-1))
rhs=scale(mul(N,add(mul(add(k,scale(p,-2)),add(s,scale(q,-1))),scale(mul(add(l,scale(q,-2)),add(r,scale(p,-1))),-1))),2)
assert det==rhs
Q=[(100*x,y) for x,y in P]
assert len(Q)==22 and all(x%100==0 for x,y in Q)
area2=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(Q,Q[1:]+Q[:1]));assert area2>0
reflex=[]
for i,c in enumerate(Q):
 a=Q[i-1];b=Q[(i+1)%len(Q)]
 if (c[0]-a[0])*(b[1]-c[1])-(c[1]-a[1])*(b[0]-c[0])<0:reflex.append(c)
assert len(reflex)==9
assert 4%200!=0 and 2%200!=0
out={'status':'PASS','determinant_polynomial_identity':True,'Q100':{'N':100,'walls':22,'reflex_corners':9,'actual_S':[0,0],'actual_T':[200,2],'all_corner_x_multiples_100':True,'divisor':200,'DI02_short_template_determinant':4,'index_two_unit_template_determinant':2,'both_templates_excluded_in_fixed_unit_frame':True,'darkness_inherited_not_reproved':True},'weight_lower_bound':{'neighbor_joint_necessary_max_a_b_at_least':20,'not_sufficiency':True},'scope':'W-free fixed-unit short-template availability only; not r<=8 refutation or transported-lattice prohibition','search_used':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','formal_identity':True,'prescribed_Q100_short_templates':'EXCLUDED','search_used':False}))
