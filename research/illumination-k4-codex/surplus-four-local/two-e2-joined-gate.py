"""Reject two hand-declared joined-room words at their first actual corner."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
from boundary_replay import replay,dot,sub,cross,on
from guard_checker import path_requirements
tri=lambda t:tuple(sorted(map(tuple,t)))
D=((1,-1),4);N=((1,1),2);R=((1,1),4);L=((1,-1),-2);E=((1,-1),2)
x=lambda a:((1,0),a)
y=lambda a:((0,1),a)
rooms=json.loads((HERE/'two-e2-check.json').read_text())['hand_prescribed_fixtures']
prefix=[D,y(2),N,y(3),x(3),N,y(2)]
full=prefix+[D,L,y(-1),y(3),E]
replacement=[R,y(0),R,L,y(0),L,E,y(2),E,N,y(2),N,E,y(2),E]
def construct(d,word,velocity,terminal_x):
 p=(F(0),F(0));v=velocity;P=[p]
 for n,k in word:
  t=(k-dot(n,p))/dot(n,v);assert t>0,(p,v,n,k,t)
  p=tuple(p[j]+t*v[j] for j in (0,1));P.append(p)
  q=2*dot(n,v)/dot(n,n);v=tuple(v[j]-q*n[j] for j in (0,1))
 t=(terminal_x-p[0])/v[0];assert t>0
 P.append(tuple(p[j]+t*v[j] for j in (0,1)))
 return P,v
names=['Bouter3_Dhalf3_Rplus_Tempty','Bouter4_Dhalf3_Rplus_Tempty','Bouter3_Dfullwest4_Rplus_Tminus','Bouter4_Dfullwest4_Rplus_Tminus']

def first_obstruction(V,P):
 # Inspect only the declared finite segments; never continue the ray.
 for i,(a,b) in enumerate(zip(P,P[1:])):
  v=sub(b,a);hits=[]
  for c,e in zip(V,V[1:]+V[:1]):
   w=sub(e,c);den=cross(v,w)
   if not den:continue
   t=cross(sub(c,a),w)/den;u=cross(sub(c,a),v)/den
   if 0<t<=1 and 0<=u<=1:hits.append((t,c,e))
  if not hits:continue
  t=min(h[0] for h in hits)
  point=tuple(a[k]+t*v[k] for k in (0,1))
  edges=[(c,e) for tt,c,e in hits if tt==t]
  if t<1 or len(edges)!=1 or point in V:
   # Independently establish every preceding reflection and open flight.
   mid=tuple((a[k]+point[k])/2 for k in (0,1))
   assert replay(V,(0,0),mid,P[:i+1]+[mid])==i
   return i+1,point,edges
 raise AssertionError('no obstruction on declared word')

attempts={}
for label,d,word,velocity,expected,angle,hits,equation in [
 ('Rplus_replacement',F(1,13),replacement,(F(1),F(1,13)),(1,1),315,6,'26*d=2'),
 ('D_Nr_circuit',F(7,4),full,(F(7,4),F(-1)),(1,2),270,3,'28/d-14=2')]:
 P,_=construct(d,word,velocity,F(2));assert P[-1]==(2,2)
 controls={}
 for name in names:
  row=rooms[name];V=[tuple(map(F,q)) for q in row['vertices']]
  flight,point,edges=first_obstruction(V,P)
  assert point==expected and flight==hits+1
  ts=list(map(tri,row['triangles']));owners=g.owners_of(ts)
  opens={e for e,ls in owners.items() if len(ls)==2}
  angles,interior=g.check_fan_angles(ts,point,owners,opens)
  assert angles==[angle//45] and not interior
  try:replay(V,(0,0),(2,2),P)
  except AssertionError:pass
  else:raise AssertionError('invalid full word accepted')
  controls[name]={'status':'REJECTED_FIRST_ACTUAL_CORNER',
   'first_obstructed_flight':flight,'prior_reflections_verified':hits,
   'first_obstruction':[str(q) for q in point],'angle_degrees':angle,
   'incident_boundary_edges':[[[str(q) for q in p] for p in edge] for edge in edges]}
  print(label,name,'REJECTED',point,'after',hits,'reflections')
 attempts[label]={'target_equation_in_infinite_mirror_model':equation,
  'root':str(d),'declared_path':[[str(q) for q in p] for p in P],
  'controls':controls}

P,v=construct(F(7,4),prefix,(F(7,4),F(-1)),F(1))
assert P[-1]==(1,F(7,4)) and v==(1,F(-7,4))
try:path_requirements(P)
except AssertionError as ex:assert str(ex)=='path constraints contradictory'
else:raise AssertionError('invalid seven-prefix guards accepted')
# Hand formula: after D, first Nr roof and hypotenuse, the upward ray
# crosses y=2 at x=4*d-6. Portal-first exit requires x>1, hence d>7/4.
assert 4*F(7,4)-6==1
out={'status':'TWO_BOUNDED_ATTEMPTS_REJECTED_NO_JOINED_CLOSURE',
 'attempts':attempts,
 'seven_prefix':{'status':'INVALID_AT_TARGET_ROOT',
  'earliest_obstruction':['1','2'],'prior_reflections_verified':3,
  'guard_failure':'path constraints contradictory',
  'next_roof_crossing_x_formula':'4*d-6',
  'necessary_portal_exit_condition':'d>7/4',
  'correction':'No valid seven-reflection transport is established. The later floor corner is only an algebraic feature of an already invalid itinerary.'},
 'remaining_joined_cases':7,'remaining_two_e2_cases':8,
 'scope':'Only two predeclared words at their analytic target roots, four original fixtures; exact actual-wall checks. No discovery scan, archive, solver, worker or whole-interval claim.'}
(HERE/'two-e2-joined-gate.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
