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
P=fp([(0,0),('-4/3',-2),('-8/5','-8/5'),(-1,-2),(3,'2/3'),(1,2),('14/5','16/5'),(2,2)])
assert P==[tuple(F(*x)for x in p)for p in candidate['candidate']['path']]
W=[((-2,-2),(0,-2)),((-2,-2),(-1,-1)),((-2,-2),(0,-2)),((3,0),(3,1)),((1,1),(1,3)),((2,4),(3,3))]
u,z=path_requirements(P);mi=H|fan('B',[1,2,3])|fan((-2,-2),[0])|fan('Tc',[6]);ma=(allK|full((-2,-2)))-z
assert z==fan('B',[4])|fan('R',[3])|fan('Tc',[7])|fan('N',[0,7])|fan((-2,-2),[1,7])
optical('B_upper_Tc6_six',P,W,mi,ma,(-8,-12),None)
room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']));assert len(room)==33 and len(V)==20 and mi<=room<=ma
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==6
assert replay([sigma(p)for p in V],(0,0),(2,2),[sigma(p)for p in P[::-1]])==6
assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
assert angle(room,(-1,-2))==180 and (-1,-2)not in V
assert angle(room,(1,2))==180 and (1,2)not in V
# Parametric exact six and finite contact/portal bounds.
def param(d):
 a=-4*d/(1+d);b=(10-8*d)/(1+d)
 return fp([(0,0),(-2*d,-2),(a,a),(2/d-4,-2),(3,7*d-4),(1,9*d-4),(b,6-b),(10-12*d,2)])
lo,hi,d=F(7,11),F(7,10),F(2,3)
assert lo<d<hi and param(d)==P and 10-12*d==2
for fn,a,b in [(lambda d:-2*d,-2,-1),(lambda d:-4*d/(1+d),-2,-1),(lambda d:2/d-4,-2,0),(lambda d:7*d-4,0,1),(lambda d:9*d-4,1,3),(lambda d:(10-8*d)/(1+d),2,3),(lambda d:7/d-8,2,3),(lambda d:10-11*d,1,3)]:
 assert a<=fn(lo)<=b and a<=fn(hi)<=b and fn(lo)!=fn(hi)
# Arbitrary ordinary D/R/N/Tc compatible with displayed guard, no room construction.
upper=mi|full('D')|fan('R',[4])|fan('N',[5,6])|fan('L',[0])|fan('E',[4])
assert u<=upper and not z&upper
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_B123_UPPERLEAF_TC6_SIX_AND_WHOLE_COMPATIBLE_SUPPORT_PASS','fixed_paths':records,'strict_gate':['7/11','7/10'],'actual_root':'2/3','endpoint_equation':'10-12d=2','whole_support_lemma':'minimum H+B123+remote(-2,-2)0+Tc6; Z B4,R3,Tc7,N0,N7,remote1,remote7; fullDsafe','smooth_C_contacts':['(-1,-2)','(1,2)'],'applications':'B123upperleaf withTc6,RemptyorR4,NemptyorN5orN6; allD safe. Necessaryb1 willfurtherexcludeN5; noB1234transfer becauseB4 blocks.','physical':'ONE33tile20wallpolygon; actualfirstT/reverse/sigma PASS','limits':'Parentconditionalfamily only, independentlyunreviewed. No fullremote theorem.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS actualSIX',len(u),'U',len(z),'Z; smoothCtwo; Tc6conditionalfamily')
