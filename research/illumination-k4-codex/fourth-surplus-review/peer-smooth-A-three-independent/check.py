"""Independent frozen smooth-A path / family proof. No peer execution/search."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
PEER=ROOT/'surplus-four-local/R23-top6-search'
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as geo
from guard_checker import path_requirements,incident
from boundary_replay import replay,on,sub,cross,dot
raw=json.loads((PEER/'room.json').read_text());found=json.loads((PEER/'result.json').read_text());r=json.loads((PEER/'verification.json').read_text())
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
assert hashlib.sha256((PEER/'room.json').read_bytes()).hexdigest()==found['room_sha256']
assert hashlib.sha256((PEER/'search.py').read_bytes()).hexdigest()==found['search_source_sha256']
P=[(F(0),F(0)),(F(-1),F(-1,2)),(F(1),F(-3,2)),(F(0),F(-2)),(F(2),F(2))]
assert P==[tuple(F(*x) for x in p) for p in found['candidate']['path']]
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']}
# Reconstruct ONLY the supplied frozen polygon from atomic boundary edges.
edges=[e for e,owners in geo.owners_of(sorted(room)).items() if len(owners)==1]
adj=defaultdict(list)
for a,b in edges:adj[a].append(b);adj[b].append(a)
assert all(len(v)==2 for v in adj.values())
cycle=[min(adj)];prev=None;cur=cycle[0]
while True:
 nxt=next(q for q in adj[cur] if q!=prev)
 if nxt==cycle[0]:break
 assert nxt not in cycle;cycle.append(nxt);prev,cur=cur,nxt
assert len(cycle)==len(edges)
V=[p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
assert replay(V,(0,0),(2,2),P)==3 and replay(V,(2,2),(0,0),P[::-1])==3
sigma=lambda p:(2-p[1],2-p[0])
assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P[::-1]])==3
assert (0,-2) not in V
mirror=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on((0,-2),a,b)]
assert len(mirror)==1 and set(mirror[0])=={(-1,-1),(1,-3)}
R=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,(a[0]+R[i%8][0],a[1]+R[i%8][1]),(a[0]+R[(i+1)%8][0],a[1]+R[(i+1)%8][1])))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
mi=H|fan('B',[7,0,1,2]);ma=mi|(full('L')-fan('L',[7]))|(full('D')-fan('D',[3]))|set().union(*(full(k) for k in ['R','E','Tc','N']))
u,z=path_requirements(P)
assert len(u)==13 and len(z)==6 and u<=mi and not z&ma
assert z==fan('L',[7])|fan('D',[3])|fan('B',[3,4,5,6])
decode=lambda ts:{tuple(sorted(map(tuple,t))) for t in ts}
assert u==decode(r['whole_support']['required']) and z==decode(r['whole_support']['forbidden'])
assert mi==decode(r['whole_support']['minimum']) and ma==decode(r['whole_support']['maximum'])
assert incident((F(0),F(-1)))<=mi and on((0,-1),P[1],P[2])
assert incident((F(1),F(0)))<=H and on((1,0),P[3],P[4])
assert mi<=room<=ma
ur,zr=path_requirements(P[::-1]);assert ur==u and zr==z
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
us,zs=path_requirements([sigma(p) for p in P[::-1]]);assert us==tr(u) and zs==tr(z)
# First two strict finite contacts; third lies on one combined maximal line.
walls=[((-1,-1),(-1,0)),((1,-2),(1,-1)),((-1,-1),(1,-3))]
q=P[-1]
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert q==(-8,-4)
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p];n+=90 if dot(a,b)==0 else 45
 return n
assert angle(room,(0,-2))==180
pts={p for t in room for p in t}
assert {p for p in pts if p[0]%2==p[1]%2==0 and angle(room,p)==360}=={(0,0),(2,0),(2,2)}
nonA={p for p in pts if not p[0]%2==p[1]%2==0}
assert sum(angle(room,p)==360 for p in nonA)==3
assert sum(angle(room,p)==180 for p in nonA)==3
# Hand equation at fixed root, and strict portal/wall gates.
d=F(1,2);assert F(3,7)<d<F(5,8)
c=((4*d-2)/(1+d),-6*d/(1+d))
assert P==[(F(0),F(0)),(F(-1),-d),(F(1),-3*d),c,(8*d-2,F(2))]
assert -1<-d<0 and -2<-3*d<-1 and -1<c[0]<1 and 1<7*d-2<3
# b1 H4 exhaustive active second-root types; no complete room assignments.
partners={'L':[[7,0],[0,1]],'D':[[0,1],[1,2],[2,3]],'E':[[3,4],[4,5]],'R':[[2,3],[3,4],[4,5]],'Tc':[[4,5],[5,6],[6,7]],'N':[[4,5],[5,6],[6,7],[7,0],[0,1]]}
dispatch={}
for site,forms in partners.items():
 for ss in forms:
  key=site+''.join(map(str,ss))
  if site=='L' and ss==[7,0]:
   assert angle(mi|fan(site,ss),(1,-2))==180 and angle(mi|fan(site,ss),(-1,-1))==180
   # ordinary D1/2 cannot heal east C; other K sites cannot heal lower-left B.
   assert not any((1,-2) in t for t in fan('D',[1,2]))
   assert not any((-1,-1) in t for k in ['D','R','E','Tc','N'] for t in full(k))
   dispatch[key]='TWO_EXTRA_SMOOTH_POINTS_B1_IMPOSSIBLE'
  elif site=='D' and ss==[2,3]:dispatch[key]='PRIOR_ACCEPTED_4_6_ORDINARY_TC_SPLIT'
  else:
   assert mi|fan(site,ss)<=ma and u<=mi|fan(site,ss) and not z&ma
   dispatch[key]='NEW_THREE_SUPPORT_PASS'
# OWN b0 mixed root/single-D4-leaf application. The other unit is awayD/B.
# Forced L0 restricts any L unit to70/01; H4/LC70 has forbidden b0 smoothB.
assert angle(mi|fan('D',[4])|fan('L',[7,0]),(-1,-1))==180
assert not any((-1,-1) in t for k in ['D','R','E','Tc','N'] for t in full(k))
leaf_dispatch={}
for site in ['L','E','R','Tc','N']:
 for ss in partners[site]:
  if site=='L' and ss==[7,0]:leaf_dispatch['L70']='B0_UNHEALABLE_SMOOTH_B_IMPOSSIBLE';continue
  minimum=mi|fan('D',[4])|fan(site,ss)
  assert minimum<=ma and u<=minimum and not z&ma
  leaf_dispatch[site+''.join(map(str,ss))]='H4_D4_WHOLE_SUPPORT_PASS'
# D3 genuinely removes a used mirror, so there is no entire single-leaf claim.
assert z&fan('D',[3])
inputs=[PEER/k for k in ['findings.txt','room.json','result.json','verify.py','verification.json','coverage.txt']]+[ROOT/'surplus-four-local/e2-e1-b1/critical-B.txt',ROOT/'fourth-surplus-review/mixed-e2-e1/argument.txt',ROOT/'surplus-four-local/joined-six-review/review.txt',Path(__file__),ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']
out={'status':'INDEPENDENT_SMOOTH_A_THREE_AND_H4_TRANSFERS_PASS','path':[[str(x) for x in p] for p in P],'reflections':3,'whole_support':{'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z)},'physical_frozen_room':{'walls':20,'J':3,'sN':3,'smooth_A_angle':180,'maximal_mirror':mirror,'actual_firstT_reverse_sigma':'PASS'},'actual_unfolded_target':list(map(str,q)),'H4_b1_partner_dispatch':dispatch,'own_H4_single_D4_dispatch':leaf_dispatch,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'limits':'Own geometry/guard primitives, NO peer execution/import. Frozen supplied polygon only. Local fan/angle assertions and whole-envelope implications, not assembled room/cap census. Class/forcing and prior 4/6 accepted dependencies. No new discovery/archive/worker; not fullDelta4.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: smoothA inside maximal wall, frozen20wall/J3/sN3, actual3 firstT/reverse/sigma,13U6Z fullmax, entireH4b1 partner split and ownH4+D4singleleaf wholetransfer.')
