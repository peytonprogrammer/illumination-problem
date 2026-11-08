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
file=HERE/'result.json';found=read(file);raw=read(HERE/'room.json')
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for f,k in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 q=HERE/f;reads.append(q);assert hashlib.sha256(q.read_bytes()).hexdigest()==found[k]
P=fp([(0,0),(-1,-2),('-2/3','-8/3'),(-1,'-5/2'),(0,-2),(2,2)])
assert P==[tuple(F(*x) for x in p) for p in found['candidate']['path']]
W=[((-1,-3),(-1,-1)),((-1,-3),(1,-1)),((-1,-3),(-1,-1)),((-1,-3),(1,-1))]
mi=H|fan('B',(1,2,3,4));u,z=path_requirements(P)
ma=allK-z
optical('West_four',P,W,mi,ma,(-4,-8),None)
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
# Independent construction from boundary ownership, not discovery boundary output.
room=decode(raw['triangles']);assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
assert len(room)==35
edges=[e for e,owners in geo.owners_of(sorted(room)).items() if len(owners)==1]
adj=defaultdict(list)
for a,b in edges:adj[a].append(b);adj[b].append(a)
assert all(len(v)==2 for v in adj.values())
cycle=[min(adj)];prev=None;cur=cycle[0]
while True:
 nxt=next(v for v in adj[cur] if v!=prev)
 if nxt==cycle[0]:break
 assert nxt not in cycle;cycle.append(nxt);prev,cur=cur,nxt
assert len(cycle)==len(edges)
V=[p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
def intersects(a,b,c,d):
 v=sub(b,a);w=sub(d,c);den=cross(v,w)
 if den:return 0<=cross(sub(c,a),w)/den<=1 and 0<=cross(sub(c,a),v)/den<=1
 return any((on(c,a,b),on(d,a,b),on(a,c,d),on(b,c,d)))
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for j,(c,d) in enumerate(zip(V,V[1:]+V[:1])):
  if i<j and j-i not in (1,len(V)-1):assert not intersects(a,b,c,d)
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==4
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
assert replay([sigma(p) for p in V],(0,0),(2,2),PS)==4
q=PS[-1]
for a,b in WS[::-1]:
 w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
optical('sigma_West_four',PS,WS,tr(mi),tr(ma),q,None)
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==4 and sum(angle(room,p)==180 for p in pts-A)==2
assert angle(room,(-1,-2))==angle(room,(0,-2))==180
assert (-1,-2) not in V and (0,-2) not in V
assert u<=mi and not z&room
# Geometry-independent stronger whole-family implication.
assert not z & set().union(*(full(k) for k in C if k!='B'))
remote=z-allK
lo,hi=F(3,7),F(3,5)
tests=[('west_first',lambda d:-1/d,-3,-1),('diag_first',lambda d:2*(d-1)/(1+d),-1,1),('west_second',lambda d:3*d-4,-3,-1),('diag_second',lambda d:(4*d-2)/(1-d),-1,1),('floor_portal',lambda d:5*d-2,0,1),('target_portal',lambda d:7*d-2,1,3)]
for name,fn,a,b in tests:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(name,x,y)
d=F(1,2);a=2*(d-1)/(1+d);c=(4*d-2)/(1-d)
assert lo<d<hi and 8*d-2==2
assert P==fp([(0,0),(-1,-1/d),(a,a-2),(-1,3*d-4),(c,c-2),(8*d-2,2)])
assert angle(mi,(-1,-2))==angle(mi,(0,-2))==180
# Mandatory crossed H-only interior point on final open leg.
assert on((1,0),P[-2],P[-1]) and incident((F(1),F(0)))<=H
reads += [ROOT/'fourth-surplus-review/west1234-coupled/argument.txt',ROOT/'surplus-four-local/west1234-coupled-review/roof-review.txt',ROOT/'fourth-surplus-review/peer-E4-six-independent/review.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_WEST_FOUR_STRONGER_WHOLE_FAMILY_PASS','fixed_paths':records,'strict_gate':['3/7','3/5'],'actual_endpoint_equation':'8d-2=2','root':'1/2','remote_forbidden':sorted(remote),'local_blockers':{k:[i for i in range(8) if z&fan(k,(i,))] for k in C},'supplied_polygon':{'triangles':len(room),'W':20,'I':3,'J':4,'s_N':2,'Q':10,'k':6,'Delta':4,'smooth_contacts':[[-1,-2],[0,-2]],'actual_boundary_reverse_sigma':'PASS'},'claim':'Every strictly simple LOCAL K room between H+B1234 and H+B1234+FULL L/D/R/E/Tc/N retains this actual ST FOUR. Full L/D/R/E/Tc/N safe. Thus WHOLE stated West1234 family <=4, including remaining D1; independent hand review required.','limits':'ONE authorized search stopped11vectors0.003s, no extra room or search. Fixed proof recomputes full incidence/mirrors independently of search trace. Local K essential for remote-west mirrors; no full Delta4 or universal claim.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',len(u),'U',len(z),'Z; actual FOUR, full otherK safe. Local blockers',out['local_blockers'],'remote',len(remote))
