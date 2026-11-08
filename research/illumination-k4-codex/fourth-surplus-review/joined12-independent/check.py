"""Independent physical replay of one supplied path in seven frozen rooms."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
core=ROOT/'fourth-surplus-review/rplus-exact-one/verify.py'
text=core.read_text();marker="r=json.loads((HERE/'result.json').read_text())"
assert text.count(marker)==1
ns={'__file__':str(core),'__name__':'retained_physical_helpers'}
exec(compile(text.split(marker)[0],str(core),'exec'),ns)
physical,polygon,ledger,angle=[ns[n] for n in ['physical','polygon','ledger','angle']]
sub,cross,dot,tri=[ns[n] for n in ['sub','cross','dot','tri']]
source=ROOT/'surplus-four-local/two-e2-check.json'
result=ROOT/'surplus-four-local/two-e2-joined-exact-one/result.json'
fixtures=json.loads(source.read_text())['hand_prescribed_fixtures']
r=json.loads(result.read_text());P=[tuple(map(F,p)) for p in r['path']]
assert P==[(F(0),F(0)),(F(-3,4),F(1)),(F(-3,2),F(0)),(F(-12,7),F(2,7)),(F(-4,3),F(0)),(F(0),F(1)),(F(20,7),F(-8,7)),(F(1,2),F(2)),(F(2,7),F(12,7)),(F(2,3),F(2)),(F(10,3),F(0)),(F(26,7),F(2,7)),(F(7,2),F(0)),(F(2),F(2))]
assert r['direction']==[-3,4] and r['reflections']==12
names=['Bouter3_Dhalf3_Rplus_Tempty','Bouter4_Dhalf3_Rplus_Tempty','Bouter3_Dfullwest4_Rplus_Tminus','Bouter3_Dfullwest4_Rplus_Tplus','Bouter4_Dfullwest4_Rplus_Tminus','Bouter4_Dfullwest4_Rplus_Tplus','BHeast4_Dhalf3_Rplus_Tplus']
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
U,Z=g['path_requirements'](P)
sigma=lambda p:(2-p[1],2-p[0]);tr=lambda ts:{tri(sigma(p) for p in t) for t in ts}
Ps=[sigma(p) for p in P[::-1]];Us,Zs=g['path_requirements'](Ps)
assert Us==tr(U) and Zs==tr(Z)
intersection=None;union=set();rows={}
def simple(V):
 edges=list(zip(V,V[1:]+V[:1]))
 for i,(a,b) in enumerate(edges):
  for j,(c,d) in enumerate(edges):
   if j<=i+1 or (i==0 and j==len(edges)-1):continue
   v,w,ac=sub(b,a),sub(d,c),sub(c,a);den=cross(v,w)
   if den:
    t,u=cross(ac,w)/den,cross(ac,v)/den
    assert not(0<=t<=1 and 0<=u<=1),(i,j)
   elif cross(ac,v)==0:
    t,u=dot(ac,v)/dot(v,v),dot(sub(d,a),v)/dot(v,v)
    assert max(0,min(t,u))>min(1,max(t,u)),(i,j)
def cyclic_equal(a,b):
 return any(a==b[i:]+b[:i] for i in range(len(b))) or any(a==b[::-1][i:]+b[::-1][:i] for i in range(len(b)))
for name in names:
 room=fixtures[name];ts={tri(t) for t in room['triangles']};V=[tuple(map(F,p)) for p in room['vertices']]
 assert cyclic_equal(polygon(ts),V)
 simple(V);ld=ledger(ts)
 assert ld==room['ledger'] and ld['W']==20 and ld['k']==6 and ld['Delta']==4
 physical(P,V);physical(P[::-1],V);physical(Ps,[sigma(p) for p in V])
 assert U<=ts and not Z&ts
 intersection=ts if intersection is None else intersection&ts;union|=ts
 assert sum(angle(t,(0,1)) for t in ts)==4 and (0,1) not in V
 walls=[];contacts=[]
 for p in P[1:-1]:
  found=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
  assert len(found)==1;a,b=found[0];walls.append((a,b));e=sub(b,a)
  contacts.append({'point':[str(x) for x in p],'wall':[[str(x) for x in a],[str(x) for x in b]],'strict_parameter':str(dot(sub(p,a),e)/dot(e,e))})
 q=P[-1]
 for a,b in walls[::-1]:
  e=sub(b,a);v=sub(q,a)
  q=tuple(a[k]+2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
 assert q==(-12,16)
 negative={}
 for label,bad in [('earlier_target',P+[P[0],P[-1]]),('off_wall',P[:5]+[(F(0),F(11,10))]+P[6:])]:
  try:physical(bad,V)
  except AssertionError:negative[label]='REJECTED'
  else:raise AssertionError(('negative control accepted',label))
 rows[name]={'status':'PASS','ledger':ld,'first_target_forward_reverse_sigma':'PASS','simple_boundary_and_tile_equality':'PASS','unfolded_actual_target':[str(x) for x in q],'smooth_0_1_degrees':180,'contacts':contacts,'negative_controls':negative}
assert U<=intersection and not Z&union
# Check every formula stated in the post-discovery hand explanation at the witness.
d=F(3,4);xd=(8-4*d)/(1+d);xr=(14-10*d)/(1+d);h=8-10*d
hand=[(-d,1),(-2*d,0),(-4*d/(1+d),2*(1-d)/(1+d)),(2/d-4,0),(3/d-4,1),(xd,xd-4),(h,2),(h/(1+d),2-h/(1+d)),(8/d-10,2),(10/d-10,0),(xr,4-xr),(14-14*d,0)]
assert hand==P[1:-1] and 12/d-14==2
out={'status':'ACCEPT_FIXED_WITNESS_AND_ALL_SEVEN_INHERITANCE','reflections':12,'direction':[-3,4],'rooms':rows,'intersection_union':'PASS','required':sorted(U),'forbidden':sorted(Z),'hand_formulas_at_exact_parameter':'PASS','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,result,core]},'limits':'Own retained physical implementation, shared historical helper/guard origins. No peer checker executed, discovery run, extra room or new path. Finite witness only; not a full interval proof or formal verification.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT: same12 path, ALL SEVEN original rooms, firstT/reverse/sigma/U-Z/simple geometry/unfold/negative controls')
