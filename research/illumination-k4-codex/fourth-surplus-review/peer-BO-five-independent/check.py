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
file=ROOT/'surplus-four-local/L670-BO-D2-search/verification.json';parent=read(file);provenance(parent,file)
P=fp([(0,0),(1,'-4/3'),('1/2',-2),(0,'-4/3'),(3,'8/3'),('11/4',3),(2,2)])
W=[((1,-2),(1,-1)),((0,-2),(1,-2)),((0,-2),(0,-1)),((3,2),(3,3)),((2,3),(3,3))]
mi=H|fan('B',(0,1));Z=fan('B',(2,7))|fan('D',(3,))|fan('E',(3,))|fan('Tc',(6,));ma=allK-Z
u,z=optical('BO_five',P,W,mi,ma,(6,-8),parent)
assert len(u)==13 and z==Z
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
assert incident((F(1),F(0)))<=H and on((1,0),P[3],P[4])
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
q=PS[-1]
for a,b in WS[::-1]:
 v=sub(q,a);w=sub(b,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
optical('EO_sigma_five',PS,WS,tr(mi),tr(ma),q,parent['sigma_five'])
assert tr(Z)==fan('E',(3,6))|fan('R',(2,))|fan('B',(2,))|fan('L',(7,))
# All named strict inequalities hold throughout this open interval by monotonicity.
lo,hi=F(5,7),F(5,6)
tests=[('B_right',lambda d:-1/d,-2,-1),('B_bottom',lambda d:2-2*d,0,1),('B_left',lambda d:2/d-4,-2,-1),('B_exit',lambda d:3*d-2,0,1),('U_T_portal',lambda d:5*d-2,1,3),('T_right',lambda d:5/d-4,2,3),('T_roof',lambda d:8-7*d,2,3)]
for name,fn,a,b in tests:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(name,x,y)
d=F(3,4);assert lo<d<hi and 8-8*d==2
assert P==fp([(0,0),(1,-1/d),(2-2*d,-2),(0,2/d-4),(3,5/d-4),(8-7*d,3),(8-8*d,2)])
applications=[]
def inclusion(name,low,high,U,Z):
 assert low<=high and U<=low and not Z&high
 applications.append({'name':name,'lower':sorted(low),'upper':sorted(high)})
common=mi|fan('L',(6,7,0))|fan('E',(4,))|fan('Tc',(5,))|fan('N',(6,))
upper=common|fan('D',(1,2))|fan('R',(3,4))
inclusion('FOUR_inward_BO_descriptions',common,upper,u,z)
assert upper<=ma
blow=mi|fan('E',(4,))|fan('Tc',(5,))|fan('N',(5,))
bhigh=blow|full('L')|fan('D',(1,2))|fan('R',(3,4))
inclusion('ALL_THREE_outside_BO_rows',blow,bhigh,u,z)
su,sz=path_requirements(PS)
elow=tr(mi)|fan('B',(1,))|fan('Tc',(5,))|fan('N',(5,))
ehigh=elow|fan('L',(0,1,2,3))|fan('D',(1,2))|fan('R',(3,4))
inclusion('TWO_outside_EO_rows_L012_L0123',elow,ehigh,su,sz)
assert sz&fan('L',(7,))
# Only ONE supplied frozen physical polygon is reconstructed.
dir=file.parent;raw=read(dir/'room.json');found=read(dir/'result.json')
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 f=dir/name;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==found[key]
room=decode(raw['triangles']);assert room==common|fan('D',(2,)) and len(room)==33
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
def intersect(a,b,c,d):
 v=sub(b,a);w=sub(d,c);den=cross(v,w)
 if den:return 0<=cross(sub(c,a),w)/den<=1 and 0<=cross(sub(c,a),v)/den<=1
 return any((on(c,a,b),on(d,a,b),on(a,c,d),on(b,c,d)))
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for j,(c,d) in enumerate(zip(V,V[1:]+V[:1])):
  if i<j and j-i not in (1,len(V)-1):assert not intersect(a,b,c,d)
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==replay([sigma(p) for p in V],(0,0),(2,2),PS)==5
pts={p for t in room for p in t};aa={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in aa if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-aa)==3 and sum(angle(room,p)==180 for p in pts-aa)==3
# Join EXACT original THIRTEEN NECESSARY DESCRIPTIONS to accepted fixed paths.
# These are support-inclusion tests, not assembled room validity checks.
eights=read(ROOT/'fourth-surplus-review/peer-critical-L-eights-independent/check.json')['fixed_paths']
old9=read(ROOT/'fourth-surplus-review/single-room-search/verification.json')
N9=fp(old9['path']);u9,z9=path_requirements(N9)
assert len(N9)-2==9
join=[]
def match(name,support,P):
 U,Z=path_requirements(P);assert U<=support and not Z&support,name
 join.append({'original_description':name,'reflections':len(P)-2})
b6=fp(eights['B_D2_complement_six']['path']);e6=fp(eights['E_R3_complement_six']['path'])
b8=fp(eights['B_center_eight']['path']);l8=fp(eights['lower_L_square_E_eight']['path'])
base=H|fan('L',(6,7,0))|fan('B',(1,2))|fan('E',(4,))|fan('Tc',(5,))|fan('N',(5,))
match('L670_BC_N5_D2_R4',base|fan('D',(2,))|fan('R',(4,)),b6)
match('L670_BC_N5_D2_R3',base|fan('D',(2,))|fan('R',(3,)),b6)
match('L670_BC_N5_D1_R3',base|fan('D',(1,))|fan('R',(3,)),b8)
for k,ss in [('D',(2,)),('D',(1,)),('R',(4,)),('R',(3,))]:match('L670_BO_N6_'+k+str(ss),common|fan(k,ss),P)
base=H|fan('L',(6,7,0,1))|fan('E',(3,4))|fan('B',(1,))|fan('Tc',(5,))|fan('N',(5,))|fan('D',(2,))
match('L6701_EC_N5_D2_R4',base|fan('R',(4,)),l8)
match('L6701_EC_N5_D2_R3',base|fan('R',(3,)),e6)
base=H|fan('L',(7,0,1))|fan('E',(3,4))|fan('B',(1,))|fan('Tc',(5,))|fan('N',(6,))|fan('D',(2,))
match('L701_EC_N6_D2_R4',base|fan('R',(4,)),N9)
match('L701_EC_N6_D2_R3',base|fan('R',(3,)),e6)
prior9=read(ROOT/'fourth-surplus-review/peer-O3-complete-independent/check.json')['fixed_paths']['L70_nine']
np=fp(prior9['path'])
base=H|fan('L',(7,0,1))|fan('E',(3,4))|fan('B',(1,))|fan('Tc',(5,))|fan('N',(7,))|fan('R',(3,))
for dcap in (2,1):match('L701_EC_N7_R3_D'+str(dcap),base|fan('D',(dcap,)),np)
assert len(join)==13 and max(r['reflections'] for r in join)==9
reads += [ROOT/'surplus-four-local/L670-BO-D2-search'/f for f in ('findings.txt','coverage.txt')]
reads += [ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt',ROOT/'fourth-surplus-review/peer-critical-L-classification-independent/review.txt',ROOT/'fourth-surplus-review/peer-critical-L-optical-independent/review.txt',ROOT/'fourth-surplus-review/peer-Bunit-six-independent/review.txt',ROOT/'fourth-surplus-review/peer-Ecenter-six-independent/review.txt',ROOT/'surplus-four-local/nine-seven-review/review.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_BO_FIVE_AND_ORIGINAL_THIRTEEN_INWARD_JOIN_PASS','fixed_paths':records,'strict_interval':['5/7','5/6'],'applications':applications,'original_thirteen_inward_join':join,'original13_reflection_bound':9,'frozen_geometry':{'W':20,'triangles':33,'J':3,'s_N':3,'Q':9,'k':6,'Delta':4,'strict_simple_firstT_forward_reverse_sigma':'PASS'},'scope':'Newfive/fullFOURBOinward and BO/EO outside transfers independently ACCEPTED. Original13 necessary inward table completely covered<=9, with accepted earlier classification/optical prerequisites retained. Not a census or fullcriticalL/Delta4/universal closure.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: BO five, 13U5Z, one frozen polygon, fullFOURinward/fiveoutside rows; EXACT original13join <=9.')
