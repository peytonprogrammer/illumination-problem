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
raw=read(HERE/'room.json');candidate=read(HERE/'result.json')
for f,k in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 q=HERE/f;reads.append(q);assert hashlib.sha256(q.read_bytes()).hexdigest()==candidate[k]
P=fp([(0,0),('1/4',1),('4/5','-6/5'),(-1,'-3/4'),('18/5','2/5'),('7/2',0),('10/3','2/3'),('2/3','4/3'),('1/2',2),('2/5','8/5'),(2,2)])
assert P==[tuple(F(*x)for x in p)for p in candidate['candidate']['path']]
W=[((-1,1),(1,1)),((0,-2),(1,-1)),((-1,-1),(-1,0)),((3,1),(4,0)),((3,0),(4,0)),((3,1),(4,0)),((0,2),(1,1)),((0,2),(1,2)),((0,2),(1,1))]
u,z=path_requirements(P);mi=H|fan('B',[1,2])|fan('R',[3])|fan('N',[7]);ma=(allK|full((-2,-2)))-z
assert z==fan('L',[7])|fan('B',[0])|fan('R',[2,4])|fan('N',[0,6])
optical('Bcenter_R3_N7_nine',P,W,mi,ma,(4,16),None)
room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']));assert len(room)==33 and len(V)==20 and mi<=room<=ma
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==9
assert replay([sigma(p)for p in V],(0,0),(2,2),[sigma(p)for p in P[::-1]])==9
assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
def param(d):
 a=4*d/(1+d);b=6*(1-d)/(1+d);c=(6-14*d)/(1-d);e=(4-14*d)/(1-d);f=(4-14*d)/(1+d)
 return fp([(0,0),(d,1),(a,a-2),(-1,5*d-2),(b,4-b),(6-10*d,0),(c,4-c),(e,2-e),(4-14*d,2),(f,2-f),(2,16*d-2)])
lo,hi,d=F(3,13),F(4,15),F(1,4)
assert lo<d<hi and param(d)==P and 16*d-2==2
for fn,a,b in [(lambda d:d,0,1),(lambda d:4*d/(1+d),0,1),(lambda d:5*d-2,-1,0),(lambda d:6*(1-d)/(1+d),3,4),(lambda d:6-10*d,3,4),(lambda d:(6-14*d)/(1-d),3,4),(lambda d:(4-14*d)/(1-d),0,1),(lambda d:4-14*d,0,1),(lambda d:(4-14*d)/(1+d),0,1),(lambda d:9*d-2,0,1),(lambda d:15*d-2,1,2)]:
 assert a<=fn(lo)<=b and a<=fn(hi)<=b and fn(lo)!=fn(hi)
apps=[]
for B in [[1,2,3],[1,2,3,4]]:
 for leaf in ([0],) if B==[1,2,3] else ([0],[7]):
  lower=H|fan('B',B)|fan((-2,-2),leaf)|fan('L',[0])|fan('E',[4])|fan('R',[3])|fan('N',[7])
  upper=lower|full('D')|full('Tc')
  assert u<=lower and not z&upper;apps.append({'B':B,'leaf':leaf,'fullD_Tc_safe':True})
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_BCENTER_R3_N7_NINE_THREE_REMOTE_APPLICATIONS_PASS','fixed_paths':records,'strict_gate':['3/13','4/15'],'actual_root':'1/4','endpoint_equation':'16d-2=2','whole_support_lemma':'minimum H+B12+R3+N7; Z L7,B0,R2,R4,N0,N6; fullD/E/Tc andremoteentirefan safe','applications':apps,'physical':'ONE33tile20wallpolygon, finitefirstwalls/reverse/sigma andSUT/J3sN3 PASS','limits':'Parenthandproofpendingindependentreview. ConditionalR3/N7cover only, no entireBfamily orremote theorem.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS actualNINE',len(u),'U',len(z),'Z, R3N7conditionalBfamilies')
