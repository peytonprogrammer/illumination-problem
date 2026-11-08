"""Prescribed low-r all-witness resonance control. No parameter search or author import."""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
R=Path(__file__).resolve().parent
helpers=R/'geometric-reduction-ear-monotonicity-check.py';ns={'F':F}
module=ast.parse(helpers.read_text())
exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef)],type_ignores=[]),str(helpers),'exec'),ns)
S=(F(2),F(2));T=(F(4),F(6))
Q=[(0,0),(8,0),(8,8),(0,8)]
D=[(0,0),(8,0),(8,8),(4,8),(4,12),(0,12)]
def validate(p,r):
 a2=sum(a[0]*b[1]-a[1]*b[0] for a,b in ns['edges'](p));assert a2>0
 ts=[ns['cross'](p[i-1],p[i],p[(i+1)%len(p)]) for i in range(len(p))]
 assert all(ts) and sum(t<0 for t in ts)==r
 for i,(a,b) in enumerate(ns['edges'](p)):
  assert a!=b and (a[0]==b[0] or a[1]==b[1])
  for j,(c,d) in enumerate(ns['edges'](p)):
   if j<=i or j in ((i-1)%len(p),(i+1)%len(p)):continue
   assert not ns['intersects'](a,b,c,d)
 assert ns['classify'](p,S)==ns['classify'](p,T)=='interior'
 return dict(vertices=p,reflex=r,walls=len(p),area=F(a2,2))
# Exact segments intersect only designated contact points; no collinear wall overlap.
def intersections(a,b,p):
 out=[];u=(b[0]-a[0],b[1]-a[1])
 for idx,(c,d) in enumerate(ns['edges'](p)):
  v=(d[0]-c[0],d[1]-c[1]);z=(c[0]-a[0],c[1]-a[1]);cross=lambda x,y:x[0]*y[1]-x[1]*y[0]
  det=cross(u,v)
  if det:
   t=F(cross(z,v),det);s=F(cross(z,u),det)
   if 0<=t<=1 and 0<=s<=1:out.append((idx,(a[0]+t*u[0],a[1]+t*u[1])))
  else:assert not ns['intersects'](a,b,c,d)
 return out

def checkpath(p,points,wall_indices):
 for i,(a,b) in enumerate(zip(points,points[1:])):
  hits=intersections(a,b,p);expected=[]
  if i>0:expected.append((wall_indices[i-1],a))
  if i<len(points)-2:expected.append((wall_indices[i],b))
  assert sorted(hits)==sorted(expected),(i,hits,expected)
  assert ns['classify'](p,((a[0]+b[0])/2,(a[1]+b[1])/2))=='interior'
 for i,wall in enumerate(wall_indices,1):
  a,b=ns['edges'](p)[wall];contact=points[i]
  assert contact!=a and contact!=b and ns['on'](contact,a,b)
  vin=(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]);out=(points[i+1][0]-points[i][0],points[i+1][1]-points[i][1])
  reflected=(-vin[0],vin[1]) if a[0]==b[0] else (vin[0],-vin[1])
  assert reflected[0]*out[1]-reflected[1]*out[0]==0
  assert sum(reflected[j]*out[j] for j in (0,1))>0

q=validate(Q,0);d=validate(D,1)
checkpath(Q,[S,T],[]);checkpath(D,[S,T],[])
H=(F(7,2),F(8));qpath=[S,H,T]
checkpath(Q,qpath,[2])
exit=(F(5,2),F(8));prefix=[S,(F(4),F(10)),(F(7,2),F(12)),exit]
checkpath(D,prefix,[3,4])
assert ns['classify'](D,H)==ns['classify'](D,exit)=='interior'
assert F(4)*F(1,4)/4==F(1,4)
x_unfold=F(7,2)+2*4*F(1,4);assert x_unfold==F(11,2) and 8-x_unfold==F(5,2)
# Symbolic universal residues: the free integer multiples16n/16m vanish modulo4.
assert all((eps*4-2)%4==2 for eps in (-1,1))
assert all((eps*6-2)%4==0 for eps in (-1,1))
assert 4%16!=0 and (-8)%16!=0 # neither form4+16m or-8+16m can vanish
output={'status':'PASS_EXACT_LOW_REFLEX_RESONANCE_CONTROL','Q':q,'D':d,'actual_S':S,'actual_T':T,'direct_actual_path_both_rooms':[S,T],'Q_one_bounce_actual_path':qpath,'D_same_launch_excursion_prefix':prefix,'ear':dict(x0=0,x1=4,y0=8,y1=12,width=4,depth=4),'universal_hand_congruence':{'all_images':'(eps_x*4+16n,eps_y*6+16m), signs±1, n/m arbitraryintegers','Delta_x_mod4':2,'Delta_y_mod4':0,'Delta_y_nonzero':'4+16m or-8+16m never0','integer_ratio_possible':False,'all_Q_target_witnesses_square_ear_resonant':False},'method_scope':'No resonant Q witness exists; D nevertheless has direct actual path. Only resonance-retuning sublemma rejected.','geometry_helpers_sha256':hashlib.sha256(helpers.read_bytes()).hexdigest(),'new_discovery_or_search':False,'whole_goal_complete':False}
def jsonify(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,tuple):return [jsonify(v) for v in x]
 if isinstance(x,list):return [jsonify(v) for v in x]
 if isinstance(x,dict):return {k:jsonify(v) for k,v in x.items()}
 return x
(R/'geometric-reduction-resonance-gap.json').write_text(json.dumps(jsonify(output),indent=2)+'\n')
print(json.dumps({k:output[k] for k in ['status','universal_hand_congruence','method_scope']},indent=2))
