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
# Independent literal transcription. No parent program is executed or imported.
P=fp([(0,0),('2/5',1),('6/5',-1),('14/5',3),(3,'5/2'),('8/5',-1),('4/5',1),('-2/7','-12/7'),('2/3','-4/3'),(2,2)])
W=[((0,1),(1,1)),((1,-1),(2,-1)),((2,3),(3,3)),((3,2),(3,3)),((1,-1),(2,-1)),((0,1),(1,1)),((-1,-1),(0,-2)),((0,-2),(1,-1))]
mi=H|fan('B',(1,2));zexp=fan('B',(0,3))|fan('D',(2,))|fan('E',(3,))|fan('Tc',(6,))|fan('N',(6,))
ma=allK-zexp
bfile=ROOT/'surplus-four-local/L670-B12-D1-search/verification.json';bparent=read(bfile);provenance(bparent,bfile)
u,z=optical('B_center_eight',P,W,mi,ma,(8,20),bparent)
assert len(u)==20 and z==zexp
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
for p in ((2,1),(0,-1)):
 assert incident(tuple(map(F,p)))<=mi and any(on(p,a,b) for a,b in zip(P,P[1:]))
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
us,zs=path_requirements(PS)
# Compute the actual reflected target image directly from transformed mirrors.
q=PS[-1]
for a,b in WS[::-1]:
 v=sub(q,a);w=sub(b,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
optical('E_center_sigma_eight',PS,WS,tr(mi),tr(ma),q,bparent['sigma_eight'])
assert zs==fan('E',(2,5))|fan('R',(3,))|fan('B',(2,))|fan('L',(7,))|fan('N',(7,))
# Both previously accepted SIX complements, from their fixed supplied data.
six=read(ROOT/'fourth-surplus-review/peer-Bunit-six-independent/check.json')
p6=fp(six['fixed_six']['path']);w6=[tuple(map(tuple,w)) for w in six['fixed_six']['finite_mirrors']]
mi6=mi|fan('D',(2,));ma6=mi6|set().union(*(full(k) for k in ('L','E','Tc','R')))|fan('N',(0,1,2,3,4,5,7))
optical('B_D2_complement_six',p6,w6,mi6,ma6,(-2,-12),six['fixed_six'])
p6s=[sigma(p) for p in p6[::-1]];w6s=[(sigma(a),sigma(b)) for a,b in w6[::-1]]
optical('E_R3_complement_six',p6s,w6s,tr(mi6),tr(ma6),(12,2),None)
# Whole support implications, not construction or enumeration of rooms.
applications=[]
def covers(name,low,high,rec):
 assert low<=high and decode(rec['required'])<=low<=high<=decode(rec['maximum'])
 assert not decode(rec['forbidden'])&high
 applications.append({'name':name,'minimum':sorted(low),'maximum':sorted(high),'reflections':rec['reflections']})
ordinary=fan('E',(4,))|fan('Tc',(5,))|fan('N',(5,))
inward=mi|fan('L',(6,7,0))|ordinary|fan('D',(1,))|fan('R',(3,))
covers('inward_L670_B12_D1_R3',inward,inward,records['B_center_eight'])
for shape in ((0,1,2),(0,1,2,3)):
 low=mi|fan('L',shape)|ordinary
 covers('outside_B_noD2_'+str(shape),low,low|fan('D',(1,))|fan('R',(3,4)),records['B_center_eight'])
 low=mi6|fan('L',shape)|ordinary
 covers('outside_B_D2_'+str(shape),low,low,records['B_D2_complement_six'])
 low=tr(mi)|fan('L',shape)|fan('B',(1,))|fan('Tc',(5,))|fan('N',(5,))
 covers('outside_E_noR3_'+str(shape),low,low|fan('D',(1,2))|fan('R',(4,)),records['E_center_sigma_eight'])
 low=tr(mi6)|fan('L',shape)|fan('B',(1,))|fan('Tc',(5,))|fan('N',(5,))
 covers('outside_E_R3_'+str(shape),low,low,records['E_R3_complement_six'])
# Lower-L square fixed eight, independent transcription.
PL=fp([(0,0),('22/7','8/7'),('18/5','12/5'),(1,'16/11'),(3,'8/11'),('-7/4',-1),(-2,'-10/11'),(3,'10/11'),(1,'18/11'),(2,2)])
WL=[((3,1),(4,2)),((3,3),(4,2)),((1,1),(1,2)),((3,0),(3,1)),((-2,-1),(0,-1)),((-2,-1),(-2,0)),((3,0),(3,1)),((1,1),(1,2))]
remote=fan((-2,-2),(1,));zl=fan('L',(5,))|fan('E',(2,5))|fan('R',(3,))|fan('N',(7,))|remote
mil=H|fan('L',(6,7))|fan('E',(3,4))
mal=mil|fan('L',(0,1,2,3,4))|set().union(*(full(k) for k in ('B','D','Tc')))|fan('R',(0,1,2,4,5,6,7))|fan('N',(0,1,2,3,4,5,6))
lfile=ROOT/'surplus-four-local/Llower-square-Ecenter-hand/check.json';lp=read(lfile)
for rel,digest in lp['source_sha256'].items():
 f=ROOT/rel;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==digest,rel
lchecker=lfile.parent/'check.py';reads.append(lchecker);assert hashlib.sha256(lchecker.read_bytes()).hexdigest()==lp['checker_sha256']
ul,zlactual=optical('lower_L_square_E_eight',PL,WL,mil,mal,(22,8),lp)
assert len(ul)==19 and zlactual==zl and not remote&allK
assert all(not on((0,0),a,b) for a,b in zip(PL[1:],PL[2:]))
low=H|fan('L',(6,7,0,1))|fan('E',(3,4))|fan('B',(1,))|fan('Tc',(5,))|fan('N',(5,))|fan('D',(2,))|fan('R',(4,))
covers('inward_L6701_E34_D2_R4',low,low,records['lower_L_square_E_eight'])
# Explicitly show why the remote extension is excluded.
assert remote<=zlactual and remote&(mal|remote)
# The declared strict intervals: finite-contact inequalities are linear or
# linear-fractional with nonvanishing denominator and monotone on interval.
# Checking closed endpoints with differing values proves strict inequalities
# throughout the open interval. This is an interval proof, not parameter search.
gates=[]
def gate(label,lo,hi,tests):
 for name,fn,a,b in tests:
  x,y=fn(lo),fn(hi)
  assert a<=x<=b and a<=y<=b and x!=y,(label,name,x,y,a,b)
 gates.append({'name':label,'interval':list(map(str,(lo,hi))),'finite_gate_tests':[t[0] for t in tests]})
gate('B_eight',F(5,13),F(7,17),[
 ('ceiling1',lambda d:d,0,1),('floor1',lambda d:3*d,1,2),('roof',lambda d:7*d,2,3),('right',lambda d:10-3/d,2,3),
 ('floor2',lambda d:6-11*d,1,2),('ceiling2',lambda d:6-13*d,0,1),('B_left',lambda d:(6-16*d)/(1+d),-1,0),
 ('B_right',lambda d:(16*d-6)/(1-d),0,1),('first_U_T',lambda d:5*d,1,3),
 ('B_inlet',lambda d:6-15*d,-1,1),('B_outlet',lambda d:17*d-6,-1,1),('last_U_T',lambda d:19*d-6,1,3)])
d=F(2,5);assert F(5,13)<d<F(7,17) and 20*d-6==2
c=(6-16*d)/(1+d);r=(16*d-6)/(1-d)
assert P==fp([(0,0),(d,1),(3*d,-1),(7*d,3),(3,10-3/d),(6-11*d,-1),(6-13*d,1),(c,-c-2),(r,r-2),(20*d-6,2)])
gate('lower_L_E_eight',F(5,14),F(7,19),[
 ('E_lower_x',lambda d:2/(1-d),3,4),('E_lower_y',lambda d:2*d/(1-d),1,2),('E_upper_x',lambda d:(2+8*d)/(1+d),3,4),
 ('T_left1',lambda d:4-7*d,1,2),('U_right1',lambda d:4-9*d,0,1),('L_inlet',lambda d:4-13*d,-1,0),
 ('L_floor',lambda d:12-5/d,-2,-1),('L_west',lambda d:14*d-6,-1,0),('L_outlet',lambda d:15*d-6,-1,0),
 ('U_right2',lambda d:19*d-6,0,1),('T_left2',lambda d:21*d-6,1,2)])
d=F(4,11);assert F(5,14)<d<F(7,19) and 22*d-6==2
assert PL==fp([(0,0),(2/(1-d),2*d/(1-d)),((2+8*d)/(1+d),6-(2+8*d)/(1+d)),(1,4-7*d),(3,4-9*d),(12-5/d,-1),(-2,14*d-6),(3,19*d-6),(1,21*d-6),(2,22*d-6)])
# Reconstruct ONLY the supplied frozen B-center room. No second room.
dir=bfile.parent;raw=read(dir/'room.json');found=read(dir/'result.json')
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 f=dir/name;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==found[key]
room=decode(raw['triangles']);assert room==inward and len(room)==34
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
# Exact nonadjacent wall intersection including collinear overlap.
def intersect(a,b,c,d):
 v=sub(b,a);w=sub(d,c);den=cross(v,w)
 if den:
  t=cross(sub(c,a),w)/den;s=cross(sub(c,a),v)/den
  return 0<=t<=1 and 0<=s<=1
 return any((on(c,a,b),on(d,a,b),on(a,c,d),on(b,c,d)))
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for j,(c,d) in enumerate(zip(V,V[1:]+V[:1])):
  if i<j and j-i not in (1,len(V)-1):assert not intersect(a,b,c,d)
for verts,path,start,end in [(V,P,(0,0),(2,2)),(V,P[::-1],(2,2),(0,0)),([sigma(v) for v in V],PS,(0,0),(2,2))]:assert replay(verts,start,end,path)==8
pts={p for t in room for p in t};aa={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in aa if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-aa);sn=sum(angle(room,p)==180 for p in pts-aa)
assert (J,sn)==(4,2)
Q=20-2-6*3+2*J+sn;assert Q==10 and Q+sn-8==4 and J+sn==6
# Original necessary table is checked only for the transfer rows being used.
table=ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt';reads.append(table)
s=table.read_text();assert 'B center12       E-,T-,Nb-                     One DR' in s and 'E center34       B+,T-,Nb-                     One DR' in s
for rel in ['surplus-four-local/L670-B12-D1-search/findings.txt','surplus-four-local/L670-B12-D1-search/coverage.txt','surplus-four-local/Llower-square-Ecenter-hand/argument.txt','surplus-four-local/Llower-square-Ecenter-hand/coverage.txt','surplus-four-local/source-suffix-four-review/review.txt','fourth-surplus-review/peer-Bunit-six-independent/review.txt']:
 reads.append(ROOT/rel)
reads += [ROOT/'triangle-composition/inputs'/k for k in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_CRITICAL_L_TWO_EIGHTS_AND_FOUR_OUTSIDE_ROWS_PASS','fixed_paths':records,'whole_support_applications':applications,'strict_intervals':gates,'frozen_room':{'triangles':34,'walls':20,'J':J,'s_N':sn,'Q':Q,'Delta':4,'k':6,'strict_simple_actual_first_T_reverse_sigma':'PASS'},'scope':'Two additional original inward descriptions and four complete L012/L0123 centered B/E outside rows <=8; accepted six complements rechecked. Four historical BO inward descriptions remain; no room census. Remote lower-L floor mate expressly excluded by local K. Full surplus4 remains open.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: both eights, sigma, both six complements, ten support inclusions, strict interval gates and ONE frozen room.')
