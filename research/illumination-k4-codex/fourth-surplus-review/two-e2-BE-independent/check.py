from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,runpy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
source=ROOT/'surplus-four-local/two-e2-BE-check.json'
r=json.loads(source.read_text())
tri=lambda t:tuple(sorted(map(tuple,t)))
T=lambda ts:{tri(t) for t in ts}
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
sigma=lambda p:(2-p[1],2-p[0])
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(c,st,m):
 return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
P=[tuple(map(F,p)) for p in r['path']]
def polygon(ts):
 edges=set()
 for a,b,c in ts:
  if cross(sub(b,a),sub(c,a))<0:b,c=c,b
  for u,v in [(a,b),(b,c),(c,a)]:
   if (v,u) in edges:edges.remove((v,u))
   else:edges.add((u,v))
 nxt=dict(edges);assert len(nxt)==len(edges)==len(set(nxt.values()))
 start=min(nxt);p=nxt[start];cyc=[start]
 while p!=start:
  assert p not in cyc;cyc.append(p);p=nxt[p]
 assert len(cyc)==len(edges)
 return [p for i,p in enumerate(cyc) if cross(sub(p,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],p))]

def angle(t,p):
 return (1 if p[0]%2==p[1]%2 else 2) if p in t else 0

def ledger(ts):
 at=defaultdict(list);groups=defaultdict(list)
 for t in ts:
  a=next(p for p in t if p[0]%2==p[1]%2==0);groups[a].append(t)
  for p in t:at[p].append(t)
 fullA={a for a,parts in groups.items() if len(parts)==8}
 assert fullA=={(0,0),(2,0),(2,2)}
 Q=sum(3 if len(parts)==4 else len(parts) for a,parts in groups.items() if a not in fullA)
 J=sN=0
 for p,parts in at.items():
  if p[0]%2==p[1]%2==0:continue
  total=sum(angle(t,p) for t in parts);J+=total==8;sN+=total==4
 V=polygon(ts)
 return dict(W=len(V),Q=Q,J=J,sN=sN,k=J+sN,Delta=Q+sN-8)

def physical(P,V):
 walls=list(zip(V,V[1:]+V[:1]))
 def inside(p):
  value=False
  for a,b in walls:
   e,v=sub(b,a),sub(p,a)
   assert cross(e,v) or not(min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]))
   if (a[1]>p[1])!=(b[1]>p[1]):
    x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
    if p[0]<x:value=not value
  return value
 assert inside(P[0]) and inside(P[-1])
 for prev,p,nxt in zip(P,P[1:],P[2:]):
  hit=[(a,b) for a,b in walls if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
  assert len(hit)==1,('contact',p)
  a,b=hit[0];e=sub(b,a);v=sub(p,prev);w=sub(nxt,p)
  reflected=tuple(2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
  assert cross(reflected,w)==0 and dot(reflected,w)>0
 for p,q in zip(P,P[1:]):
  assert inside(tuple((p[k]+q[k])/2 for k in [0,1]))
  v=sub(q,p)
  for a,b in walls:
   w,ap=sub(b,a),sub(a,p);den=cross(v,w)
   if den:
    t,s=cross(ap,w)/den,cross(ap,v)/den
    assert not(0<t<1 and 0<=s<=1),('early boundary',p,q,a,b)
   elif cross(ap,v)==0:
    aa,bb=dot(ap,v)/dot(v,v),dot(sub(b,p),v)/dot(v,v)
    assert max(min(aa,bb),F(0))>=min(max(aa,bb),F(1))



fixed=H|fan((0,-2),1,3)|fan((4,2),2,3)
possible=H|fan((0,-2),0,4)|fan((4,2),2,4)|set(caps.values())
U,Z=g['path_requirements'](P)
assert U<=fixed and not Z&possible
assert fixed==T(r['fixed_minimum']) and possible==T(r['possible_envelope'])
assert U==T(r['required']) and Z==T(r['forbidden']) and len(U)==18 and len(Z)==4
Us,Zs=g['path_requirements']([sigma(p) for p in reversed(P)])
transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
assert Us==transform(U) and Zs==transform(Z)
d=F(12,13)
formulas=[(0,0),(-1,-1/d),(2*d-2,-2),(4,6/d-4),(10-7*d,3),(-1,10-11/d),(12*d-12,-2),(17*d-12,3),(4,20-16/d),(20-22*d,-2),(-1,21/d-24),(2,24/d-24)]
assert P==formulas and len(P)-2==10
ys=[p[1]+(1-p[0])*(q[1]-p[1])/(q[0]-p[0]) for p,q in zip(P,P[1:]) if min(p[0],q[0])<1<max(p[0],q[0])]
assert ys==[F(-3,4),F(1,4),F(1,12),F(-7,12),F(11,12)]
controls={}
for n,row in r['controls'].items():
 room=T(row['triangles']);V=[tuple(map(F,p)) for p in row['vertices']]
 ll=ledger(room);assert ll==row['ledger']
 assert set(polygon(room))==set(V)
 physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in reversed(P)],[sigma(p) for p in V])
 assert U<=room and not Z&room
 controls[n]={'status':'PASS','ledger':ll,'actual_boundary_forward_reverse_sigma':'PASS'}
(HERE/'check.json').write_text(json.dumps({'status':'INDEPENDENT_WHOLE_FAMILY_ACCEPT','reflections':10,'U_count':len(U),'Z_count':len(Z),'whole_envelope':'PASS','hand_contact_formula_exact_match':'PASS','x1_crossing_heights':[str(y) for y in ys],'controls':controls,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'limits':'Independent physical replay; shared canonical guard and geometry dependencies. No whole parameter interval recertified or required.'},indent=2)+'\n')
print('PASS: BE10wholefamily fullguards/formulas/4budgetledgers andactualforwardreverse/sigma')
