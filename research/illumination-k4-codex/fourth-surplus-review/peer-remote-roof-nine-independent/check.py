"""Independent fixed eights, one supplied polygon, whole-support transfers.
No peer execution/import, new room, direction/word discovery or archive scan.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import replay,on,sub,cross,dot
import illumination_geometry as geo
reads=[]
def read(p):reads.append(p);return json.loads(p.read_text())
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+R[i%8][j] for j in (0,1)),tuple(a[j]+R[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
allK=H|set().union(*(full(k) for k in C))
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
def fp(xs):return [tuple(F(x) for x in p) for p in xs]
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p];n+=90 if dot(a,b)==0 else 45
 return n
def provenance(receipt,path):
 for rel,digest in receipt['source_sha256'].items():
  p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,rel
 p=path.parent/'verify.py';reads.append(p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['checker_sha256']
records={}
def optical(name,P,walls,mi,ma,image,parent):
 u,z=path_requirements(P)
 assert u<=mi and not z&ma,(name,u-mi,z&ma)
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
 for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
  assert on(p,c,e) and p not in (c,e),(name,p)
  v=sub(p,a);w=sub(e,c)
  ref=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
  assert cross(ref,sub(b,p))==0 and dot(ref,sub(b,p))>0
 assert len(walls)==len(P)-2
 a,b=path_requirements(P[::-1]);assert (a,b)==(u,z)
 a,b=path_requirements([sigma(p) for p in P[::-1]]);assert (a,b)==(tr(u),tr(z))
 q=P[-1]
 for a,b in walls[::-1]:
  w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert q==image,(name,q,image)
 if parent is not None:
  assert u==decode(parent['required']) and z==decode(parent['forbidden'])
  assert mi==decode(parent['minimum']) and ma==decode(parent['maximum'])
 records[name]={'path':[[str(x) for x in p] for p in P],'reflections':len(P)-2,'U':len(u),'Z':len(z),'unfold':list(map(str,q)),'required':sorted(u),'forbidden':sorted(z),'minimum':sorted(mi),'maximum':sorted(ma)}
 return u,z
parentdir=ROOT/'surplus-four-remote2110/roof-control-search'
receipt=read(parentdir/'verification.json');raw=read(parentdir/'room.json');candidate=read(parentdir/'result.json')
for rel,h in receipt['source_sha256'].items():
 p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
for n in ('argument.txt','coverage.txt','verify.py'):reads.append(parentdir/n)
P=fp([(0,0),('-1/4',1),('-3/4',-1),('-4/3','4/3'),(-2,'3/2'),('-8/5','8/5'),(-2,0),('10/3','4/3'),('7/2',2),('18/5','8/5'),(2,2)])
assert P==fp(receipt['path'])==[tuple(F(*x) for x in p) for p in candidate['candidate']['path']]
W=[((-1,1),(1,1)),((-1,-1),(0,-1)),((-2,2),(-1,1)),((-2,1),(-2,2)),((-2,2),(-1,1)),((-3,1),(-1,-1)),((3,1),(4,2)),((3,2),(4,2)),((3,1),(4,2))]
mi=H|fan('L',[7,0,1,2])|fan((-2,2),[6])|fan('E',[4]);u,z=path_requirements(P)
ma=(allK|fan((-2,2),[6]))-z
optical('remote_roof_nine',P,W,mi,ma,(-4,16),receipt)
assert z==fan('L',[3,4,5,6])|fan('B',[2])|fan('E',[3,5])|fan('N',[5])|fan((-2,2),[5,7])
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']))
assert len(room)==35 and len(V)==20 and mi<=room<=ma
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==9
assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P[::-1]])==9
# Independently reconstruct the sole boundary from canceled atomic edges.
owned=geo.owners_of(sorted(room));adj=defaultdict(list);edges={e for e,owners in owned.items() if len(owners)==1}
for a,b in edges:adj[a].append(b);adj[b].append(a)
assert all(len(v)==2 for v in adj.values());cycle=[min(adj)];prev=None;p=cycle[0]
while True:
 q=next(x for x in adj[p] if x!=prev)
 if q==cycle[0]:break
 assert q not in cycle;cycle.append(q);prev,p=p,q
assert len(cycle)==len(edges)
vertices=[p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
assert set(vertices)==set(V)
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for j,(c,e) in enumerate(zip(V,V[1:]+V[:1])):
  if i<j and j-i not in (1,len(V)-1):
   v=sub(b,a);w=sub(e,c);den=cross(v,w)
   if den:assert not (0<=F(cross(sub(c,a),w),den)<=1 and 0<=F(cross(sub(c,a),v),den)<=1)
   else:assert not any((on(c,a,b),on(e,a,b),on(a,c,e),on(b,c,e)))
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==4 and sum(angle(room,p)==180 for p in pts-A)==2
assert angle(mi,(-2,0))==180 and (-2,0) not in V
assert incident((F(-1),F(0)))<=mi and incident((F(2),F(1)))<=H
# Independent parametric endpoint and strict finite-mirror inequalities.
def param(d):
 a=4*d/(1-d);b=8*d/(1+d);c=10*d/(1+d);j=10*d/(1-d);k=18*d/(1+d)
 return fp([(0,0),(-d,1),(-3*d,-1),(-a,a),(-2,6*d),(-b,b),(-c,c-2),(j,j-2),(14*d,2),(k,k-2),(2,16*d-2)])
lo,hi,d=F(3,13),F(4,15),F(1,4)
assert lo<d<hi and param(d)==P and 16*d-2==2
for fn,a,b in [(lambda d:-d,-1,0),(lambda d:-3*d,-1,0),(lambda d:-4*d/(1-d),-2,-1),(lambda d:6*d,1,2),(lambda d:-8*d/(1+d),-2,-1),(lambda d:-10*d/(1+d),-3,-1),(lambda d:10*d/(1-d),3,4),(lambda d:14*d,3,4),(lambda d:18*d/(1+d),3,4),(lambda d:1/d-4,-1,1),(lambda d:9*d-2,-1,1),(lambda d:3/d-10,1,3),(lambda d:15*d-2,1,2)]:
 assert a<=fn(lo)<=b and a<=fn(hi)<=b and fn(lo)!=fn(hi)
for n in [[],[0],[6],[7]]:
 lower=mi|fan('Tc',[5,6])|fan('B',[1])|fan('N',n)
 upper=lower|full('D')|full('R')|full('Tc')
 assert u<=lower and not z&upper
# Also h0 L7012 remote6 has E4,B1,Tc5 forced and ordinary N!=5.
lower=mi|fan('B',[1])|fan('Tc',[5]);upper=lower|full('D')|full('R')|fan('N',[0,6,7])
assert u<=lower and not z&upper
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_ACCEPT_REMOTE_ROOF_NINE_WHOLE_LEMMA','fixed_paths':records,'strict_gate':['3/13','4/15'],'actual_root':'1/4','endpoint_equation':'16d-2=2','physical':'ONE supplied35tile20wall polygon; finitefirstwalls/reverse/sigma PASS','smooth_A_L':'180 and strictly inside maximal wall','applications':'Whole parent minimum H+L7012+remote6+E4 and Z as stated; FULL D/R/Tc and ordinary N0/6/7 safe; h0 row also covered','limits':'Optical lemma accepted only; no exhaustive2110 classification or fullsurplus theorem.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('ACCEPT remote roofNINE',len(u),'U',len(z),'Z, fullD/R/Tc andN5absence wholelemma')
