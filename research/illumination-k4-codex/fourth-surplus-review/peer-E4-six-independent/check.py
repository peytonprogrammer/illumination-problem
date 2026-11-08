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
file=ROOT/'surplus-four-local/mixed-H4-R23-search/verification.json';parent=read(file);provenance(parent,file)
P=fp([(0,0),('4/5',1),('12/5',-1),(3,'-1/4'),(1,'9/4'),('8/5',3),('28/9','10/9'),(2,2)])
W=[((0,1),(1,1)),((2,-1),(3,-1)),((3,-1),(3,0)),((1,2),(1,3)),((1,3),(2,3)),((3,1),(4,2))]
mi=H|fan('E',(4,));Z=fan('D',(1,))|fan('R',(4,))|fan('N',(0,6))|fan('Tc',(5,))|fan('E',(5,));ma=allK-Z
u,z=optical('E4_six',P,W,mi,ma,(8,10),parent)
assert len(u)==19 and z==Z and all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
assert on((2,1),P[3],P[4]) and incident((F(2),F(1)))<=H
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
q=PS[-1]
for a,b in WS[::-1]:
 v=sub(q,a);w=sub(b,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
optical('sigma_six',PS,WS,tr(mi),tr(ma),q,None)
lo,hi=F(7,9),F(5,6)
tests=[('ceiling',lambda d:d,0,1),('floor',lambda d:3*d,2,3),('lower_Uright',lambda d:3/d-4,-1,0),('upper_Tleft',lambda d:5/d-4,2,3),('left_roof',lambda d:7*d-4,1,2),('E_diagonal',lambda d:(12*d-4)/(1+d),3,4),('E_T_portal',lambda d:9*d-6,1,2)]
for name,fn,a,b in tests:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(name,x,y)
d=F(4,5);c=(12*d-4)/(1+d)
assert lo<d<hi and 10*d-6==2
assert P==fp([(0,0),(d,1),(3*d,-1),(3,3/d-4),(1,5/d-4),(7*d-4,3),(c,c-2),(2,10*d-6)])
# Three peer mixed applications, plus NEWOWNWestD2 entire-support transfer.
apps=[]
def fits(name,high):
 assert u<=high<=ma and not z&high,name
 apps.append({'name':name,'upper':sorted(high),'reflections':6})
ref=fan('L',(0,))|fan('E',(4,))|fan('N',(7,))
fits('mixed_R23_H4_bothDleaves',H|fan('B',(7,0,1,2))|fan('D',(3,4))|fan('R',(2,3))|ref)
base=H|fan('B',(6,7,0,1))|fan('D',(3,4))|fan('L',(7,0))|fan('E',(4,))|fan('R',(3,))
fits('mixed_L70_N7_bothDleaves',base|fan('N',(7,)))
fits('mixed_L70_Tc6_bothDleaves',base|fan('Tc',(6,)))
west=H|fan('B',(1,2,3,4))|fan('L',(7,0))|fan('E',(4,))|fan('Tc',(6,))|fan('R',(3,))|fan('N',(7,))|fan('D',(2,))
fits('OWN_remaining_West_Tc6_R3_N7_D2',west)
assert z&fan('D',(1,)) and not z&fan('D',(2,))
# No West room is constructed: ONLY the original supplied mixed polygon.
raw=read(file.parent/'room.json');found=read(file.parent/'result.json')
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 f=file.parent/name;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==found[key]
room=decode(raw['triangles']);assert room==H|fan('B',(7,0,1,2))|fan('D',(3,))|fan('R',(2,3))|ref and len(room)==34
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
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==replay([sigma(p) for p in V],(0,0),(2,2),PS)==6
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
# Whole ORIGINAL Rquarter family earlierN7abs complement keepsuniform7;
# new residualtable row6 is not silently promoted to wholefamily6.
rootleaf=read(ROOT/'fourth-surplus-review/mixed-e2-e1/root-leaf-check.json')
old7=rootleaf['named_implications']['ordinary_LE_Nrminus_absent'];p7=fp(old7['path']);u7,z7=path_requirements(p7)
oldcase=H|fan('B',(7,0,1))|fan('D',(3,4))|fan('R',(2,3))|fan('L',(0,))|fan('E',(4,))
assert u7<=oldcase and not z7&oldcase
reads += [ROOT/'surplus-four-local/mixed-H4-R23-search'/f for f in ('findings.txt','verify.py','coverage.txt')]
reads += [ROOT/'fourth-surplus-review/mixed-e2-e1/argument.txt',ROOT/'fourth-surplus-review/west1234-coupled/argument.txt',ROOT/'fourth-surplus-review/west1234-coupled/N7-prefix-assessment.txt',ROOT/'surplus-four-local/west1234-coupled-review/roof-review.txt',ROOT/'fourth-surplus-review/peer-L70-six-independent/review.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_E4_SIX_MIXED_TRANSFERS_ACCEPT_AND_NEW_WEST_D2_SIX','fixed_paths':records,'strict_gate':['7/9','5/6'],'whole_support_applications':apps,'frozen_polygon':{'W':20,'tiles':34,'J':3,'s_N':3,'Q':9,'k':6,'Delta':4,'fullA':'SUT','simple_firstwalls_firstT_reverse_sigma':'PASS'},'mixed_bounds':{'new_R23_necessary_residual_row':6,'whole_original_Rquarter_branch_retaining_uniform7':7,'new_L70_N7_or_Tc6_residuals':6},'OWN_West_consequence':'RemainingD2descriptioncovered<=6 bywholeU/Zinclusion. ONLYremainingWestdescription Tc6/R3/N7/D1. NewownWesttransferneedsindependentpeerreview; noWestroomconstructed.','limits':'No peercheckerexecution,newroom/capcensus/discovery/archive/worker. AlloldWestclassifications/acceptedcoversretained. FullDelta4/universalminimumOPEN.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT E4six and3mixedapplications; NEWOWN whole remainingWestD2<=6, onlyWestD1remains, pendingindependenttransferreview.')
