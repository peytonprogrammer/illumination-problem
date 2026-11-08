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
P=fp([(0,0),('3/4',1),('9/4',-1),(3,0),(1,'8/3'),('5/4',3),(2,2)])
assert P==[tuple(F(*x)for x in p)for p in candidate['candidate']['path']]
W=[((0,1),(1,1)),((2,-1),(3,-1)),((3,-1),(3,1)),((1,2),(1,3)),((1,3),(2,3))]
u,z=path_requirements(P);mi=H;ma=(allK|full((-2,-2)))-z
assert z==fan('D',[1])|fan('R',[3,4])|fan('Tc',[5])|fan('N',[0,6])
optical('core_five',P,W,mi,ma,(6,8),None)
room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']));assert len(room)==34 and len(V)==20 and mi<=room<=ma
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==5
assert replay([sigma(p)for p in V],(0,0),(2,2),[sigma(p)for p in P[::-1]])==5
assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
assert angle(mi,(3,0))==180 and (3,0)not in V
# Parametricactualfive: firstsmoothC3,0 isstrictinsideverticalmaxwall.
def param(d):return fp([(0,0),(d,1),(3*d,-1),(3,3/d-4),(1,5/d-4),(7*d-4,3),(8*d-4,2)])
lo,hi,d=F(5,7),F(5,6),F(3,4)
assert lo<d<hi and param(d)==P and 8*d-4==2
for fn,a,b in [(lambda d:d,0,1),(lambda d:3*d,2,3),(lambda d:3/d-4,-1,1),(lambda d:5/d-4,2,3),(lambda d:7*d-4,1,2)]:
 assert a<=fn(lo)<=b and a<=fn(hi)<=b and fn(lo)!=fn(hi)
# ExactlastupperfixtureandWHOLEsupportguard, noadditionalroomconstructed.
upper=H|fan('B',[1,2,3,4])|fan((-2,-2),[0])|fan('L',[0])|fan('E',[4])|fan('D',[2])|fan('N',[5])|fan('Tc',[6])
assert upper==room and u<=upper and not z&upper
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_CORE_FIVE_AND_FINAL_UPPER2101_RESIDUE_PASS','fixed_paths':records,'strict_gate':['5/7','5/6'],'actual_root':'3/4','endpoint_equation':'8d-4=2','whole_support_lemma':'minimum H; blockers D1,R3,R4,Tc5,N0,N6; allL/B/E/remote safe, D2/N5/N7/Tc6 safe','application':'FinalupperB1234leaf0+L0E4D2N5Tc6,Rempty','smooth_C_contact':'(3,0)180strictlyinsidemaxverticalmirror','physical':'ONE34tile20wallpolygon, finitefirstT/noSrevisit/reverse/sigma PASS','limits':'Parentwholelemma awaitingindependentreview; lowerB1234leaf7+D2R4Tc6 remainsopen.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS coreFIVE',len(u),'U',len(z),'Z; FINALupper2101residue')
