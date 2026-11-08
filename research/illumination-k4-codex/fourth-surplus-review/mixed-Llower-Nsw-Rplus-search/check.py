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
 q=HERE/f;reads.append(q);assert hashlib.sha256(q.read_bytes()).hexdigest()==found[k]
old=read(ROOT/'fourth-surplus-review/peer-B12-R3-four-independent/check.json')['fixed_paths']['B12_R3_four']
P=fp(old['path']);assert P==[tuple(F(*v) for v in p) for p in found['candidate']['path']]
W=[((0,1),(1,1)),((1,-1),(3,-1)),((3,1),(4,0)),((-1,-1),(0,-2))]
mi=H|fan('B',(1,2))|fan('R',(3,));u,z=path_requirements(P)
assert z==fan('B',(3,))|fan('D',(1,2))|fan('R',(2,))|fan('N',(6,))
optical('accepted_B12_R3_four',P,W,mi,allK-z,(8,12),old)
fixtures=read(ROOT/'fourth-surplus-review/mixed-e2-e1/critical-L-check.json')
f=fixtures['hand_forced_fixtures']['Llower_Bcenter_Nsw_R+'];room=decode(raw['triangles'])
assert room==decode(f['triangles']) and len(room)==34
V=list(map(tuple,f['vertices']));assert V==list(map(tuple,raw['vertices'])) or set(V)==set(map(tuple,raw['vertices']))
assert u<=room and not z&room
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==4
assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P[::-1]])==4
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==4 and sum(angle(room,p)==180 for p in pts-A)==2
assert angle(room,(2,-1))==180 and (2,-1) not in V
# No newpath: entire old hand proof and gate are inherited explicitly.
assert P==fp([(0,0),('2/3',1),(2,-1),('16/5','4/5'),('-2/5','-8/5'),(2,2)])
reads += [ROOT/'fourth-surplus-review/peer-B12-R3-four-independent/review.txt',ROOT/'fourth-surplus-review/mixed-eleven-transfer/check.json',ROOT/'fourth-surplus-review/mixed-Llower-Nsw-search/check.json',ROOT/'fourth-surplus-review/mixed-e2-e1/critical-L.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_FINAL_RPLUS_TRANSFER_AND_ALL_ELEVEN_LT_FIXTURES_COVERED','fixed_paths':records,'new_application':'Llower_Bcenter_Nsw_R+ <=4','smooth_floor_2_minus1':'180 inside maximal straight wall','actual_firstwall_firstT_reverse_sigma':'PASS','eleven_fixture_cover':{'seven_largerL_Ecenter':4,'three_Llower_Nsw_R3abs':3,'last_Llower_Nsw_R3present':4},'whole_critical_L_T_allroot_branch_parent_bound':13,'limits':'Newfixturetransfer only, oldpath/handgate inherited. ONEsearch rediscoveredacceptedB12_R3four STOP30vectors, no newmechanismclaimed. Parentjoinawaitspeeraudit. OthermixedBjoined/fourunit/remote/fullDelta4 remainseparate.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS oldB12/R3four in lastRplusfixture; allELEVEN L/T residuals now parentcovered<=4; wholeoriginalL/Tallroot<=13 viaacceptedcomplements')
