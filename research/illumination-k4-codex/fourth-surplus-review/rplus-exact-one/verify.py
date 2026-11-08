"""Independent replay of ONE returned Rplus witness; no discovery."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,runpy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
tri=lambda t:tuple(sorted(map(tuple,t)))
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
 target=P[-1]
 for i,(a,b) in enumerate(zip(P,P[1:])):
  if i==len(P)-2:break
  v=sub(b,a);w=sub(target,a)
  assert cross(v,w)!=0 or not(0<dot(w,v)<=dot(v,v)),('earlier target',i)
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



r=json.loads((HERE/'result.json').read_text());room=json.loads((HERE/'geometry.json').read_text())
assert r['status']=='LIT_PATH_AWAITING_INDEPENDENT_REPLAY'
P=[tuple(map(F,p)) for p in r['path']];V=[tuple(map(F,p)) for p in room['vertices']];ts={tri(t) for t in room['triangles']}
assert P[0]==(0,0) and P[-1]==(2,2) and len(P)-2==19
assert cross(sub(P[1],P[0]),(-10,3))==0 and dot(sub(P[1],P[0]),(-10,3))>0
assert ledger(ts)==room['ledger'] and set(polygon(ts))==set(V)
physical(P,V);physical(P[::-1],V)
sigma=lambda p:(2-p[1],2-p[0])
physical([sigma(p) for p in reversed(P)],[sigma(p) for p in V])
g=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
U,Z=g['path_requirements'](P);assert U<=ts and not Z&ts
Us,Zs=g['path_requirements']([sigma(p) for p in reversed(P)]);tr=lambda ts:{tri(sigma(p) for p in t) for t in ts}
assert Us==tr(U) and Zs==tr(Z)
# Independently unfold target across the ACTUAL contacted walls.
walls=[];contacts=[]
for i,p in enumerate(P[1:-1],1):
 hits=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if cross(sub(b,a),sub(p,a))==0 and 0<dot(sub(p,a),sub(b,a))<dot(sub(b,a),sub(b,a))]
 assert len(hits)==1
 a,b=hits[0];walls.append((a,b));e=sub(b,a)
 contacts.append({'index':i,'point':[str(c) for c in p],'wall':[[str(c) for c in q] for q in [a,b]],'strict_wall_parameter':str(dot(sub(p,a),e)/dot(e,e))})
q=P[-1]
for a,b in reversed(walls):
 e=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in [0,1])
assert cross(q,(-10,3))==0 and dot(q,(-10,3))>0
# Verify all non-adjacent boundary segments are disjoint.
E=list(zip(V,V[1:]+V[:1]))
for i,(a,b) in enumerate(E):
 for j,(c,d) in enumerate(E):
  if j<=i+1 or (i==0 and j==len(E)-1):continue
  v,w,ac=sub(b,a),sub(d,c),sub(c,a);den=cross(v,w)
  if den:
   t,u=cross(ac,w)/den,cross(ac,v)/den
   assert not(0<=t<=1 and 0<=u<=1),(i,j)
  elif cross(ac,v)==0:
   t,u=dot(ac,v)/dot(v,v),dot(sub(d,a),v)/dot(v,v)
   assert max(0,min(t,u))>min(1,max(t,u)),(i,j)
out={'status':'EXACT_ACTUAL_ST_FIRSTARRIVAL_PASS','reflections':19,'direction':[-10,3],'physical_forward_reverse_sigma':'PASS','ledger':ledger(ts),'unfolded_target':[str(c) for c in q],'contacts':contacts,'required':sorted(U),'forbidden':sorted(Z),'smooth_integer_contacts':{},'input_hashes':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in ['geometry.json','result.json']},'limits':'One frozen room; discovery provenance explicit; no arbitrary-completion theorem.'}
for p in P[1:-1]:
 if all(c.denominator==1 for c in p):
  a=sum(angle(t,p) for t in ts);assert a==4 and p not in V
  out['smooth_integer_contacts'][str(tuple(p))]=45*a
(HERE/'verify.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'reflections':19,'unfolded_target':out['unfolded_target'],'smooth_integer_contacts':out['smooth_integer_contacts']}))
