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
file=ROOT/'surplus-four-local/mixed-H4-D3-EO-search/verification.json';parent=read(file);provenance(parent,file)
P=fp([(0,0),('2/3',1),(2,-1),('16/5','4/5'),('-2/5','-8/5'),(2,2)])
W=[((0,1),(1,1)),((1,-1),(3,-1)),((3,1),(4,0)),((-1,-1),(0,-2))]
mi=H|fan('B',(1,2))|fan('R',(3,));Z=fan('B',(3,))|fan('D',(1,2))|fan('R',(2,))|fan('N',(6,));ma=allK-Z
u,z=optical('B12_R3_four',P,W,mi,ma,(8,12),parent)
assert len(u)==17 and z==Z
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
assert on((2,0),P[3],P[4]) and incident((F(2),F(0)))<=H
assert angle(mi,(2,-1))==180
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
q=PS[-1]
for a,b in WS[::-1]:
 v=sub(q,a);w=sub(b,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
optical('sigma_four',PS,WS,tr(mi),tr(ma),q,None)
lo,hi=F(7,11),F(5,7)
tests=[('ceiling',lambda d:d,0,1),('floor',lambda d:3*d,1,3),('R_inlet',lambda d:3/d-4,0,1),('R_diag',lambda d:8*d/(1+d),3,4),('B_inlet',lambda d:8-5/d,-1,1),('B_diag',lambda d:(8*d-6)/(1+d),-1,0),('B_exit',lambda d:9*d-6,-1,1),('final_seam',lambda d:11*d-6,1,3)]
for name,fn,a,b in tests:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(name,x,y)
d=F(2,3);r=8*d/(1+d);b=(8*d-6)/(1+d)
assert lo<d<hi and 12*d-6==2
assert P==fp([(0,0),(d,1),(3*d,-1),(r,4-r),(b,-b-2),(12*d-6,2)])
# One actual frozen polygon only.
raw=read(file.parent/'room.json');found=read(file.parent/'result.json')
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 f=file.parent/name;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==found[key]
room=decode(raw['triangles'])
base=H|fan('B',(7,0,1,2))|fan('L',(0,))|fan('E',(4,))|fan('N',(7,))|fan('R',(3,))
assert room==base|fan('D',(3,))|fan('E',(5,)) and len(room)==34
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
assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==replay([sigma(p) for p in V],(0,0),(2,2),PS)==4
assert angle(room,(2,-1))==180 and (2,-1) not in V
cw=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on((2,-1),a,b)]
assert len(cw)==1 and set(cw[0])=={(1,-1),(3,-1)}
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
# THREE requested whole implications, independent upper per named case.
apps=[]
for name,high in [('last_EO_H4_D3_R3',base|fan('D',(3,))|fan('E',(5,))),('H4_R34_Tc6_both_Dleaves',base|fan('D',(3,4))|fan('R',(4,))|fan('Tc',(6,))),('H4_N70_R3_Tc6_both_Dleaves',base|fan('D',(3,4))|fan('N',(0,))|fan('Tc',(6,)))]:
 assert u<=high<=ma and not z&high,name
 apps.append({'name':name,'upper':sorted(high),'reflections':4})
# Whole-Rcenter scope clarification: old N7abs complement can still use7.
rootleaf=read(ROOT/'fourth-surplus-review/mixed-e2-e1/root-leaf-check.json')
old7=rootleaf['named_implications']['ordinary_LE_Nrminus_absent']
P7=fp(old7['path']);u7,z7=path_requirements(P7)
assert u7==decode(old7['required']) and z7==decode(old7['forbidden'])
old_R34_case=H|fan('B',(6,7,0,1))|fan('D',(3,4))|fan('L',(0,))|fan('E',(4,))|fan('R',(3,4))|fan('Tc',(6,))
assert u7<=old_R34_case and not z7&old_R34_case
assert not u<=old_R34_case # B2 is missing; does not refute existence of another4path.
short=read(ROOT/'fourth-surplus-review/peer-mixed-singleleaf-short-independent/check.json')
assert short['bounds']['whole_E34']==8
# Row joins use the previously accepted structural table, not a room census:
# EO missingL2/N7abs5/O3O4N7present4/H4D4<=4/H4D3N7 R3new4, hencewhole5.
# R34 remainingN7row Tc6absnew2 versus H4Tc6new4, henceresidualrow4;
# initialN7abs uniform7 remains as complementary originalfamily branch.
reads += [ROOT/'surplus-four-local/mixed-H4-D3-EO-search'/f for f in ('findings.txt','verify.py','coverage.txt')]
reads += [ROOT/'fourth-surplus-review/mixed-e2-e1/argument.txt',ROOT/'fourth-surplus-review/mixed-Eouter-four-transfer/argument.txt',ROOT/'surplus-four-local/H4-D4-review/review.txt',ROOT/'surplus-four-local/mixed-Eouter-dispatch-review/review.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_B12_R3_FOUR_MIXED_EO_AND_RESIDUAL_R34_JOIN_PASS','fixed_paths':records,'strict_gate':['7/11','5/7'],'frozen_polygon':{'W':20,'tiles':34,'J':3,'s_N':3,'Q':9,'k':6,'Delta':4,'smooth_floor_firstwalls_firstT_reverse_sigma':'PASS'},'whole_support_applications':apps,'bounds':{'whole_Eouter':5,'previously_unresolved_Rcenter_table_row':4,'whole_original_Rcenter_including_N7abs_uniform7':7,'whole_Ecenter_previously_accepted':8,'H4_N70_R3_Tc6':4},'clarification':'Rcenterresidualrow<=4 accepted. WholeoriginalRcenterfamily stillhasN7abs cases usinguniform7; B2abs prevents thisfourcertificate there, soentireoriginalbound7retained. No proof ofalternate4pathnonexistence.','remaining_singleleaf_rows':'L70O3/O4R3+N0/N7/Tc6, R23H4Tcempty, N70O3/O4R3Tcempty, eitherDleaf; allothermixed/allroot/West/remote obligationsseparate.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT newfour and3applications; entireEO<=5, residualRcenter<=4 (wholeoriginal<=7), H4N70Tc6<=4.')
