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
found=read(HERE/'result.json');raw=read(HERE/'room.json')
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for f,k in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 p=HERE/f;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==found[k]
P=fp([(0,0),('3/2',-1),(3,0),(1,'4/3'),(2,2)])
assert P==[tuple(F(*x) for x in p) for p in found['candidate']['path']]
W=[((1,-1),(3,-1)),((3,-1),(3,1)),((1,1),(1,2))]
u,z=path_requirements(P);mi=H;ma=allK-z
assert u<=H
optical('core_three',P,W,mi,ma,(6,-4),None)
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']))
assert u<=room and not z&room
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==3
assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P[::-1]])==3
# Check the larger L0123 upper without constructing another room.
upper=H|full('L')|full((-2,2))|fan('B',[1])|fan('E',[4])|fan('Tc',[5])|fan('N',[6])
assert u<=upper and not z&upper
assert z==fan('D',[2])|fan('R',[3,4])|fan('N',[7]),sorted(z)
lo,hi,d=F(3,5),F(4,5),F(2,3)
for fn,a,b in [(lambda d:1/d,1,3),(lambda d:3*d-2,-1,1),(lambda d:5*d-2,1,2)]:
 assert a<=fn(lo)<=b and a<=fn(hi)<=b and fn(lo)!=fn(hi)
assert lo<d<hi and 6*d-2==2
assert P==fp([(0,0),(1/d,-1),(3,3*d-2),(1,5*d-2),(2,6*d-2)])
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==2 and sum(angle(room,p)==180 for p in pts-A)==4
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for j,(c,e) in enumerate(zip(V,V[1:]+V[:1])):
  if i<j and j-i not in (1,len(V)-1):
   v=sub(b,a);w=sub(e,c);den=cross(v,w)
   if den:assert not (0<=F(cross(sub(c,a),w),den)<=1 and 0<=F(cross(sub(c,a),v),den)<=1)
   else:assert not any((on(c,a,b),on(e,a,b),on(a,c,e),on(b,c,e)))
old=read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json')
matches=[n for n,g in old['named_guards'].items() if decode(g['required'])==u and decode(g['forbidden'])==z]
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_CORE_THREE_AND_REMOTE2101_L012_L0123_LEFTLEAF_N6_TRANSFER_PASS','fixed_paths':records,'exact_guard_labels':{'required':'subset of H','forbidden':'D2,R3,R4,N7'},'strict_gate':['3/5','4/5'],'root':'2/3','endpoint_equation':'6d-2=2','physical':'ONE supplied32-triangle20-wall polygon, actualfirstT/reverse/sigma PASS','applications':'L012 or L0123 + remote(-2,2)5+B1+E4+Tc5+N6, D/R empty; even full L and remote fan do not meet guard','existing_guard_matches':matches,'discovery':'ONE named room, stopped31 primitivevectors; candidate was3reflections','limits':'Parent proof pending independent review; no fullremote row theorem yet.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS coreTHREE',len(u),'U',len(z),'Z, largerL andremote safe; prior exactguard matches',matches)
