"""One named retained nine-path against a fixed remote-roof envelope; no discovery."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
source=ROOT/'surplus-four-local/left-return-check.json'
capsfile=ROOT/'zero-surplus-L/guard-incidence-check.json'
guardfile=ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'
g=runpy.run_path(str(guardfile))
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
def physical(path,V):
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
 assert inside(path[0]) and inside(path[-1])
 for prev,p,nxt in zip(path,path[1:],path[2:]):
  hits=[(a,b) for a,b in walls if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
  assert len(hits)==1,('nonstrict',p)
  a,b=hits[0];e,v,out=sub(b,a),sub(p,prev),sub(nxt,p)
  reflected=tuple(2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
  assert cross(reflected,out)==0 and dot(reflected,out)>0
 for p,q in zip(path,path[1:]):
  assert inside(tuple((p[k]+q[k])/2 for k in [0,1]))
  v=sub(q,p)
  for a,b in walls:
   w,ap=sub(b,a),sub(a,p);den=cross(v,w)
   if den:
    t,s=cross(ap,w)/den,cross(ap,v)/den
    assert not(0<t<1 and 0<=s<=1),('earlier boundary',p,q,a,b)
   elif cross(ap,v)==0:
    aa,bb=dot(ap,v)/dot(v,v),dot(sub(b,p),v)/dot(v,v)
    assert max(min(aa,bb),F(0))>=min(max(aa,bb),F(1))



tri=lambda t:tuple(sorted(map(tuple,t)))
raw=json.loads(source.read_text())['paths']['trapezoid_Ncap']
P=[tuple(map(F,p)) for p in raw['path']]
U,Z=g['path_requirements'](P)
H=set().union(*(g['incident'](tuple(map(F,p))) for p in [(0,0),(2,0),(2,2)]))
D=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(c,sectors):
 return {tri((c,(c[0]+D[i][0],c[1]+D[i][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in sectors}
caps={n:tri(t) for n,t in json.loads(capsfile.read_text())['cap_options'].items()}
fixed=H|fan((-2,0),[7,0,1,2])|fan((-2,2),[6])|fan((2,4),[5,6])|{caps[n] for n in ['B+','E-','Nr-']}
allowed=fixed|{caps[n] for n in ['D+','D-','R+','R-']}
missing=U-fixed;conflicts=Z&allowed
assert not missing and not conflicts,(missing,conflicts)
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


fixture=json.loads((HERE/'geometry.json').read_text())
V=[tuple(map(F,p)) for p in fixture['vertices']]
room={tri(t) for t in fixture['triangles']}
assert U<=room and not Z&room
roomledger=ledger(room)
assert roomledger==dict(W=20,Q=10,J=4,sN=2,k=6,Delta=4),roomledger
assert set(V)==set(polygon(room))
physical(P,V);physical(P[::-1],V)
sigma=lambda p:(2-p[1],2-p[0])
physical([sigma(p) for p in reversed(P)],[sigma(p) for p in V])
assert U=={tri(t) for t in raw['required']} and Z=={tri(t) for t in raw['forbidden']}
(HERE/'check.json').write_text(json.dumps({'status':'PASS','scope':'Whole fixed remote/centered-roof subfamily with ordinary Nr- present, B+/E-; D/R ordinary arbitrary','reflections':len(P)-2,'prescribed_control_actual_forward_reverse_sigma':'PASS','control_ledger':roomledger,'path':raw['path'],'required':sorted(U),'forbidden':sorted(Z),'required_missing':sorted(missing),'forbidden_allowed_conflicts':sorted(conflicts),'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,capsfile,guardfile]}},indent=2)+'\n')
print('PASS: known nine-reflection path covers whole Nr-minus-present remote-centered-roof subfamily')
