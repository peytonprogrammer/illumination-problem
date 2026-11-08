"""Independent fixed N70 four and N0 six, one polygon, whole-support transfers.
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
file=ROOT/'surplus-four-local/mixed-O3-N70-search/verification.json'
parent=read(file);provenance(parent,file)
P4=fp([(0,0),(3,'9/4'),(2,3),('2/7','12/7'),('5/4',3),(2,2)])
P6=P4[:3]+fp([('2/3',2),('2/7','16/7'),('1/2',2)])+P4[4:]
W4=[((3,2),(3,3)),((1,3),(3,3)),((0,2),(1,1)),((1,3),(2,3))]
W6=W4[:2]+[((0,2),(1,2)),((0,2),(1,3)),((0,2),(1,2))]+W4[-1:]
z4=fan('E',(3,))|fan('Tc',(5,6))|fan('N',(6,))
z6=fan('E',(3,))|fan('Tc',(5,6))|fan('N',(1,7))
mi4=H|fan('N',(7,0));mi6=H|fan('N',(0,))
u4,Z4=optical('N70_four',P4,W4,mi4,allK-z4,(8,6),parent['four'])
u6,Z6=optical('N0_six',P6,W6,mi6,allK-z6,(8,6),parent['six'])
assert (len(u4),len(Z4),len(u6),len(Z6))==(12,4,11,5)
assert Z4==z4 and Z6==z6
for label,P,W,mi,z in [('four',P4,W4,mi4,z4),('six',P6,W6,mi6,z6)]:
 assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
 PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
 q=PS[-1]
 for a,b in WS[::-1]:
  w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 optical('sigma_'+label,PS,WS,tr(mi),tr(allK-z),q,None)
 # Every separately forbidden triangle invalidates the necessary support condition.
 for t in z: assert not ((allK-z)|{t}).isdisjoint(z)
lo,hi=F(5,7),F(4,5)
tests=[('T_right',lambda d:3*d,2,3),('first_roof',lambda d:6-3/d,1,3),('N_portal',lambda d:6-5*d,2,3),('N_diagonal',lambda d:(6*d-4)/(1+d),0,1),('return_portal',lambda d:5/d-4,2,3),('last_roof',lambda d:7*d-4,1,2),('N0_first_bottom',lambda d:6-4/d,0,1),('N0_last_bottom',lambda d:6*d-4,0,1)]
for name,fn,a,b in tests:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(name,x,y)
d=F(3,4);a=(6*d-4)/(1+d);f=6-3/d
assert lo<d<hi and 8*d-4==2
assert P4==fp([(0,0),(3,3*d),(f,3),(a,2-a),(7*d-4,3),(8*d-4,2)])
assert P6==P4[:3]+fp([(6-4/d,2),(a,a+2),(6*d-4,2)])+P4[4:]
# Identity of outgoing affine lines holds symbolically: a*(1+d)=6*d-4.
# N70: a-d*(2-a)=4*d-4. N0 triple: (6*d-4)-2*d=4*d-4.
assert a-d*(2-a)==P6[5][0]-d*P6[5][1]==4*d-4
assert sub(P4[4],P4[3])[0]/sub(P4[4],P4[3])[1]==d
assert sub(P6[6],P6[5])[0]/sub(P6[6],P6[5])[1]==d
base=H|fan('B',(6,7,0,1))|fan('D',(3,4))|fan('L',(0,))|fan('E',(4,))|fan('R',(3,))
applications=[]
for name,u,z,upper,n in [('N70_O3_O4_R3_both_D_leaves',u4,z4,base|fan('N',(7,0)),4),('L70_N0_R3_O3_O4_both_D_leaves',u6,z6,base|fan('L',(7,))|fan('N',(0,)),6)]:
 assert u<=upper and not z&upper
 applications.append({'name':name,'reflections':n,'U_contained_Z_absent':True})
# ONLY the supplied N70 four-path room is reconstructed.
raw=read(file.parent/'room.json');found=read(file.parent/'result.json')
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 q=file.parent/name;reads.append(q);assert hashlib.sha256(q.read_bytes()).hexdigest()==found[key]
room=decode(raw['triangles']);assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items())) and len(room)==33
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
assert replay(V,(0,0),(2,2),P4)==replay(V,(2,2),(0,0),P4[::-1])==4
assert replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P4[::-1]])==4
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
assert angle(room,(2,3))==180 and (2,3) not in V
roof=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on((2,3),a,b)]
assert len(roof)==1 and set(roof[0])=={(1,3),(3,3)}
# Complete join is inherited from the already independently accepted necessary table.
# Pin all reviews carrying the earlier complements and new E4 six transfers.
for rel in ('fourth-surplus-review/peer-mixed-singleleaf-short-independent/review.txt','fourth-surplus-review/peer-B12-R3-four-independent/review.txt','fourth-surplus-review/peer-E4-six-independent/review.txt','fourth-surplus-review/mixed-e2-e1/argument.txt','surplus-four-local/mixed-O3-N70-search/findings.txt','surplus-four-local/mixed-O3-N70-search/verify.py','surplus-four-local/mixed-O3-N70-search/coverage.txt'):
 reads.append(ROOT/rel)
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_N70_FOUR_N0_SIX_AND_ROOT_SINGLELEAF_COVER_ACCEPT','fixed_paths':records,'strict_gate':['5/7','4/5'],'whole_support_applications':applications,'supplied_polygon':{'tiles':33,'W':20,'J':3,'s_N':3,'Q':9,'k':6,'Delta':4,'actual_S_T_firstwall_reverse_sigma':'PASS','roof_2_3_smooth_180':'PASS'},'whole_original_independent_unit_family_bounds':{'L70':12,'E34':8,'E45':5,'R34':7,'R23':7,'N70':4,'earlier_other_unit_cases':7},'whole_stated_e2ROOT_single_e1LEAF_bound':12,'not_closed':['mixed_all_roots','West_D1','remaining_four_unit','remote','full_Delta4'],'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT N70four12U4Z/N0six11U5Z, both whole-support transfers; complete stated root/single-leaf branch <=12, other partitions remain open.')
