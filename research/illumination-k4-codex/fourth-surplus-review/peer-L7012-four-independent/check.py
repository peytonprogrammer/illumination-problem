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
file=ROOT/'surplus-four-local/L7012-D23-search/verification.json';parent=read(file);provenance(parent,file)
P=fp([(0,0),('-4/3',1),('-16/7','2/7'),('-7/4',1),('-1/4',-1),(2,2)])
W=[((-3,1),(-1,1)),((-3,1),(-2,0)),((-3,1),(-1,1)),((-1,-1),(0,-1))]
mi=H|fan('L',(7,0,1,2));remote=fan((-2,2),(6,))
zexp=fan('L',(3,))|fan('B',(2,))|remote
ma=allK-zexp
u,z=optical('L7012_four',P,W,mi,ma,(-8,6),parent)
assert len(u)==13 and z==zexp and not remote&allK
assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
assert on((-1,0),P[3],P[4]) and incident((F(-1),F(0)))<=mi and angle(mi,(-1,0))==360
# Explicit actual firstT and finite smooth contacts in the entire gate.
lo,hi=F(5,7),F(4,5)
tests=[('first_top',lambda d:-1/d,-2,-1),('diagonal_x',lambda d:-4/(1+d),-3,-2),('second_top',lambda d:-4+3*d,-2,-1),('source_floor',lambda d:-4+5*d,-1,0),('L_portal',lambda d:4-3/d,-1,1),('U_T_portal',lambda d:-4+7*d,1,3)]
for key,fn,a,b in tests:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(key,x,y)
d=F(3,4);c=-4/(1+d)
assert lo<d<hi and -4+8*d==2
assert P==fp([(0,0),(-1/d,1),(c,-c-2),(-4+3*d,1),(-4+5*d,-1),(-4+8*d,2)])
# All non-centeredB partner rows fit ONE universal upper.
upper=mi|fan('B',(0,1))|set().union(*(full(k) for k in ('D','R','E','Tc','N')))
assert u<=mi<=upper<=ma and not z&upper
BCmin=mi|fan('B',(1,2));BCmax=BCmin|set().union(*(full(k) for k in ('D','R','E','Tc','N')))
for p in ((-2,1),(-1,-1)):
 assert angle(BCmin,p)==angle(BCmax,p)==180
# Both distinct points are unhealed smooth non-A boundary points, exceeding b1.
assert (-2,1)!=(-1,-1) and any(v%2 for v in (-2,1)) and any(v%2 for v in (-1,-1))
refs=fan('B',(1,))|fan('Tc',(5,))
case_extras=[('EO_D2',fan('E',(4,5))|fan('N',(5,))|fan('D',(2,))),('EO_R3',fan('E',(4,5))|fan('N',(5,))|fan('R',(3,))),('EC_D2_R4',fan('E',(3,4))|fan('N',(5,))|fan('D',(2,))|fan('R',(4,))),('DC_R3',fan('D',(1,2))|fan('E',(4,))|fan('N',(5,))|fan('R',(3,))),('DQ23',fan('D',(2,3))|fan('E',(4,))|fan('N',(5,))),('RQ23',fan('R',(2,3))|fan('E',(4,))|fan('N',(5,))),('NSW_D2',fan('N',(4,5))|fan('E',(4,))|fan('D',(2,))),('NSW_R3',fan('N',(4,5))|fan('E',(4,))|fan('R',(3,)))]
for name,extra in case_extras:assert u<=mi|refs|extra<=upper and not z&(mi|refs|extra),name
# No sigma inference from arbitrary marked lattice images: transform actual path,
# mirrors, required and absent sets. The full endpoint identity is checked.
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]]
q=PS[-1]
for a,b in WS[::-1]:
 v=sub(q,a);w=sub(b,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
optical('sigma_Tc_four',PS,WS,tr(mi),tr(ma),q,None)
# Reconstruct ONLY ONE supplied frozen polygon; no other room.
raw=read(file.parent/'room.json');found=read(file.parent/'result.json')
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
 f=file.parent/name;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==found[key]
room=decode(raw['triangles']);assert room==mi|refs|fan('D',(2,3))|fan('E',(4,))|fan('N',(5,)) and len(room)==34
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
for p in (P[1],P[3]):
 walls=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(p,a,b)]
 assert len(walls)==1 and set(walls[0])=={(-3,1),(-1,1)}
assert angle(room,(-2,1))==180 and (-2,1) not in V
assert angle(room,(-1,0))==360 and (-1,0) not in V
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
# Retain exact established joins, not a new classification.
inward=read(ROOT/'fourth-surplus-review/peer-BO-five-independent/check.json')
outside=read(ROOT/'fourth-surplus-review/peer-outside-two-three-independent/check.json')
assert len(inward['original_thirteen_inward_join'])==13 and inward['original13_reflection_bound']==9
assert outside['whole_L0123_accepted_bound']==8 and len(outside['h0_outside_dispatch'])==24
# Conservative whole branch bound uses only already accepted oldL012<=15.
shape_bounds={'L670':14,'L701':14,'L6701':14,'L5670':6,'L012':15,'L0123':8,'L7012':4}
# Proposed refinement uses the separate NEW L012<=8 join, pending peer acceptance.
new_bounds={**shape_bounds,'L012':8}
assert max(shape_bounds.values())==15 and max(new_bounds.values())==14
# Peer independently accepted the NEWL0128 extension. Verify its frozen
# twelve clauses equal our already checked L012 half of the24-clause join.
peerjoin=read(ROOT/'surplus-four-local/critical-L-final-join/check.json')
assert peerjoin['L012_independent_verdict'].startswith('ACCEPT')
for rel,digest in peerjoin['source_sha256'].items():
 f=ROOT/rel;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==digest,rel
def signature(low,high,n):return (tuple(sorted(decode(low))),tuple(sorted(decode(high))),n)
ours={signature(c['minimum'],c['upper'],c['reflections']) for c in outside['h0_outside_dispatch'] if c['L']==[0,1,2]}
theirs={signature(c['minimum'],c['maximum'],c['reflections']) for c in peerjoin['L012_clauses']}
assert len(ours)==len(theirs)==12 and ours==theirs
assert {'L'+k:v for k,v in peerjoin['seven_shapes_conditional_bounds'].items()}==new_bounds
assert peerjoin['parent_critical_L_T_bound']==max(new_bounds.values())==14
reads += [ROOT/'surplus-four-local/critical-L-final-join'/f for f in ('argument.txt','check.py','coverage.txt')]
reads += [ROOT/'surplus-four-local'/f for f in ('L7012-D23-search/findings.txt','L7012-D23-search/coverage.txt','outside-C-frontier.txt','e2-e1-b1/critical-L.txt')]
reads += [ROOT/'fourth-surplus-review'/f for f in ('peer-critical-L-classification-independent/review.txt','peer-critical-L-optical-independent/review.txt','peer-BO-five-independent/review.txt','peer-outside-two-three-independent/review.txt')]
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_L7012_FOUR_WHOLE_TABLE_AND_CRITICAL_L_T_JOIN_PASS','fixed_paths':records,'strict_gate':['5/7','4/5'],'whole_table_upper':sorted(upper),'eight_previous_residues':[k for k,_ in case_extras],'centered_B_exclusion':'TWO distinct unhealed nonA smooth180 points (-2,1),(-1,-1), hence impossibleb1','remote_limit':'(-2,2)sector6 genuinely forbidden, absent ONLY bylocalK','frozen_polygon':{'tiles':34,'W':20,'J':3,'s_N':3,'Q':9,'k':6,'Delta':4,'fullA':'SUT','simple_firstwalls_firstT_reverse_sigma':'PASS'},'accepted_conservative_seven_shape_bounds':shape_bounds,'accepted_conservative_whole_critical_L_T_bound':15,'accepted_current_seven_shape_bounds':new_bounds,'accepted_current_whole_critical_L_T_bound':14,'L012_independent_extension_verdict':'Peer ACCEPT fully read; all12 clauses equal ownverifiedjoin and allpinnedhashescurrent','scope':'L7012four and whole table, all8previousresidues ACCEPT. All7Lwindows join<=14 with existing prerequisites; newownL0128 independentlyacceptedbypeer, finalwholejoinindependentlyACCEPTEDhere. LocalTWOroot e2+e1+b1 only, not fullDelta4 or universalminimum.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: L7012four13U3Z, remote-top restriction/portal/maxwall, wholeL7012table; ENTIREcriticalL/T<=14, including independent peer acceptance of L0128 and checked final7shapejoin.')
