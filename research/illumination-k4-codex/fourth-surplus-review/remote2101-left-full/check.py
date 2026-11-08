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
assert candidate['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for f,k in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 q=HERE/f;reads.append(q);assert hashlib.sha256(q.read_bytes()).hexdigest()==candidate[k]
original=[tuple(F(*x) for x in p) for p in candidate['candidate']['path']]
assert len(original)-2==9 and on((0,0),original[5],original[6])
P=fp([(0,0),('-4/3',1),('-16/7','2/7'),('-7/4',1),('-1/4',-1),(2,2)])
assert P[1:]==original[6:]
W=[((-2,1),(-1,1)),((-3,1),(-1,-1)),((-2,1),(-1,1)),((-1,-1),(0,-1))]
u,z=path_requirements(P);mi=H|fan('L',[7,0,1,2]);ma=(allK|fan((-2,2),range(8)))-z
assert z==fan('L',[3])|fan('B',[2])|fan((-2,2),[6])
optical('L_full_left_four',P,W,mi,ma,(-8,6),None)
room=decode(raw['triangles']);V=list(map(tuple,raw['vertices']));assert len(room)==34 and len(V)==20 and mi<=room<=ma
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==4
assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P[::-1]])==4
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
def param(d):
 a=-4/(1+d)
 return fp([(0,0),(-1/d,1),(a,-a-2),(3*d-4,1),(5*d-4,-1),(8*d-4,2)])
lo,hi,d=F(5,7),F(4,5),F(3,4)
assert lo<d<hi and param(d)==P and 8*d-4==2
for fn,a,b in [(lambda d:-1/d,-2,-1),(lambda d:-4/(1+d),-3,-2),(lambda d:3*d-4,-2,-1),(lambda d:5*d-4,-1,0)]:
 assert a<=fn(lo)<=b and a<=fn(hi)<=b and fn(lo)!=fn(hi)
# Whole left remote orientation, all local other fans permitted except B2.
upper=H|fan('L',[7,0,1,2])|fan((-2,2),[5])|full('D')|full('R')|full('E')|full('Tc')|full('N')|fan('B',[1])
assert u<=upper and not z&upper
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
old=read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json');matches=[n for n,g in old['named_guards'].items() if decode(g['required'])==u and decode(g['forbidden'])==z]
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_FULL_L_LEFT_FOUR_ENTIRE_REMOTE2101_ORIENTATION_PASS','fixed_paths':records,'strict_gate':['5/7','4/5'],'actual_root':'3/4','endpoint_equation':'8d-4=2','whole_support_lemma':'minimum H+L7012, blockers L3,B2,remote(-2,2)6; full D/R/E/Tc/N and remote5 safe','applications':'All11 necessary fullL7012 remoteleft5 ordinarytwo-slot descriptions, no D/R/N budget needed for optics','physical':'ONE supplied34tile20wallpolygon; finitefirstwalls/reverse/sigma PASS','candidate_reduction':'Original9 hits S again betweencontacts5/6. Delete five-contact loop and start at actualS alongsuffix direction(-4,3); exact4 checked separately.','existing_identical_guard_matches':matches,'limits':'Parenthandproof pending independentreview. No fullremote row theorem yet.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS actualFOUR',len(u),'U',len(z),'Z, ENTIREfullLleft family, oldmatches',matches)
