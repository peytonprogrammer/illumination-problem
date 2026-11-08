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
# Independent literal transcriptions of two supplied new paths.
P2=fp([(0,0),(-1,'-1/4'),('14/5','-6/5'),(2,2)])
W2=[((-1,-1),(-1,0)),((2,-2),(3,-1))]
mi2=H|fan('D',(1,2));z2e=fan('L',(7,))|fan('D',(0,));ma2=allK-z2e
f2=ROOT/'surplus-four-local/outside-L0123-D12-search/verification.json';v2=read(f2);provenance(v2,f2)
u2,z2=optical('D12_two',P2,W2,mi2,ma2,(-8,-2),v2)
assert len(u2)==13 and z2==z2e
assert incident((F(2),F(-1)))<=mi2 and on((2,-1),P2[1],P2[2])
assert not incident((F(2),F(-1)))<=H|fan('D',(1,))
assert not incident((F(2),F(-1)))<=H|fan('D',(2,))
P3=fp([(0,0),('2/3',1),(2,-1),(3,'1/2'),(2,2)])
W3=[((0,1),(1,1)),((1,-1),(3,-1)),((3,0),(3,1))]
z3e=fan('D',(1,2))|fan('R',(3,))|fan('N',(6,));ma3=allK-z3e
f3=ROOT/'surplus-four-local/outside-L0123-N45-search/verification.json';v3=read(f3);provenance(v3,f3)
u3,z3=optical('core_three',P3,W3,H,ma3,(4,6),v3)
assert len(u3)==10 and z3==z3e
assert angle(H,(2,-1))==180
# Sigma and time reversal preserve ordered ACTUAL S/T; actual target image
# derived from transformed physical walls, not another lattice point.
for name,P,W,mi,ma,parent in [('R34_sigma_two',P2,W2,mi2,ma2,v2['sigma_two']),('sigma_core_three',P3,W3,H,ma3,v3['sigma_three'])]:
 ps=[sigma(p) for p in P[::-1]];ws=[(sigma(a),sigma(b)) for a,b in W[::-1]]
 q=ps[-1]
 for a,b in ws[::-1]:
  v=sub(q,a);w=sub(b,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 optical(name,ps,ws,tr(mi),tr(ma),q,parent)
 assert all(not on((0,0),a,b) for a,b in zip(ps[1:],ps[2:]))
assert tr(mi2)==H|fan('R',(3,4)) and tr(z2)==fan('R',(5,))|fan('Tc',(6,))
assert tr(z3)==fan('D',(2,))|fan('R',(3,4))|fan('N',(7,))
# Monotone rational finite-contact inequalities on the whole strict interval.
gates=[]
def gate(name,lo,hi,tests):
 for key,fn,a,b in tests:
  x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(name,key,x,y)
 gates.append({'name':name,'interval':[str(lo),str(hi)],'tests':[x[0] for x in tests]})
gate('two',F(1,5),F(1,3),[('left_y',lambda d:-d,-1,0),('D_inlet',lambda d:1/d-2,1,3),('D_diagonal_x',lambda d:(4-2*d)/(1+d),2,3)])
d=F(1,4);c=(4-2*d)/(1+d);assert P2==fp([(0,0),(-1,-d),(c,c-4),(4-8*d,2)]) and 4-8*d==2
gate('three',F(3,5),F(3,4),[('source_ceiling',lambda d:d,0,1),('floor_x',lambda d:3*d,1,3),('U_right_y',lambda d:3/d-4,0,1),('final_portal',lambda d:6-5*d,1,3)])
d=F(2,3);assert P3==fp([(0,0),(d,1),(3*d,-1),(3,3/d-4),(6-6*d,2)]) and 6-6*d==2
# Only the TWO given frozen polygons, never another room.
def intersects(a,b,c,d):
 v=sub(b,a);w=sub(d,c);den=cross(v,w)
 if den:return 0<=cross(sub(c,a),w)/den<=1 and 0<=cross(sub(c,a),v)/den<=1
 return any((on(c,a,b),on(d,a,b),on(a,c,d),on(b,c,d)))
def frozen(file,P,spec,count,J,sn,smooth=False):
 raw=read(file.parent/'room.json');found=read(file.parent/'result.json')
 for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
  f=file.parent/name;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==found[key]
 room=decode(raw['triangles']);assert room==spec and len(room)==count
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
 for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
  for j,(c,d) in enumerate(zip(V,V[1:]+V[:1])):
   if i<j and j-i not in (1,len(V)-1):assert not intersects(a,b,c,d)
 ps=[sigma(p) for p in P[::-1]]
 assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==replay([sigma(p) for p in V],(0,0),(2,2),ps)==len(P)-2
 assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
 pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
 assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
 assert sum(angle(room,p)==360 for p in pts-A)==J and sum(angle(room,p)==180 for p in pts-A)==sn
 if smooth:
  assert (2,-1) not in V and angle(room,(2,-1))==180
  walls=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on((2,-1),a,b)]
  assert len(walls)==1 and set(walls[0])=={(1,-1),(3,-1)}
 else:assert angle(room,(2,-1))==360 and (2,-1) not in V
 Q=20-2-18+2*J+sn;assert Q+sn-8==4 and J+sn==6
 return {'W':20,'tiles':count,'J':J,'s_N':sn,'Q':Q,'k':6,'Delta':4,'fullA':'SUT','simple_actual_firstwall_firstT_reverse_sigma':'PASS','D_portal_or_smooth_floor':360 if not smooth else 180}
refs=fan('B',(1,))|fan('E',(4,))|fan('Tc',(5,))|fan('N',(5,))
geo2=frozen(f2,P2,H|fan('L',(0,1,2,3))|fan('D',(1,2))|refs,34,3,3)
geo3=frozen(f3,P3,H|fan('L',(0,1,2,3))|fan('N',(4,5))|fan('B',(1,))|fan('E',(4,))|fan('Tc',(5,)),33,2,4,True)
applications=[]
def inclusion(name,low,high,U,Z,reflections):
 assert low<=high and U<=low and not Z&high,name
 applications.append({'name':name,'lower':sorted(low),'upper':sorted(high),'reflections':reflections})
inclusion('L0123_D12_Rempty',mi2|fan('L',(0,1,2,3))|refs,mi2|fan('L',(0,1,2,3))|refs,u2,z2,2)
us2,zs2=path_requirements(fp(records['R34_sigma_two']['path']))
for shape,extra in [((0,1,2,3),set()),((7,0,1,2),fan('D',(2,)))]:
 low=H|fan('R',(3,4))|fan('L',shape)|refs|extra
 inclusion('R34_withL'+str(shape),low,low,us2,zs2,2)
low=H|fan('L',(0,1,2,3))|fan('N',(4,5))|fan('B',(1,))|fan('E',(4,))|fan('Tc',(5,))
inclusion('L0123_N45',low,low,u3,z3,3)
us3,zs3=path_requirements(fp(records['sigma_core_three']['path']))
for site,ss in [('N',(4,5)),('E',(4,5))]:
 base=H|fan('L',(7,0,1,2))|fan('B',(1,))|fan('Tc',(5,))|fan('E',(4,))|fan('N',(5,))|fan(site,ss)
 inclusion('L7012_'+site+'outer_R4',base|fan('R',(4,)),base|fan('R',(4,)),u3,z3,3)
 inclusion('L7012_'+site+'outer_D1',base|fan('D',(1,)),base|fan('D',(1,)),us3,zs3,3)
# Exhaustive h0 OUTSIDE table dispatch from exact previously accepted paths.
eights=read(ROOT/'fourth-surplus-review/peer-critical-L-eights-independent/check.json')['fixed_paths']
fives=read(ROOT/'fourth-surplus-review/peer-BO-five-independent/check.json')['fixed_paths']
old=read(ROOT/'fourth-surplus-review/peer-critical-L-optical-independent/check.json')
north=read(ROOT/'fourth-surplus-review/peer-roof-three-independent/check.json')
print('north records',list(north['three']),list(north['accepted_six_rechecked']))
# North supplied old witnesses, read only; no old checker invocation.
def available(name,P):
 P=fp(P);a,b=path_requirements(P)
 return {'name':name,'path':P,'U':a,'Z':b,'reflections':len(P)-2}
paths={k:available(k,v['path']) for k,v in eights.items()}
paths.update({k:available(k,v['path']) for k,v in fives.items()})
paths['T3']=available('T3',old['named_paths']['T3'])
paths['N3']=available('N3',north['three']['path'])
paths['N6']=available('N6',north['accepted_six_rechecked']['path'])
paths['D2new']=available('D2new',P2);paths['R2new']=available('R2new',records['R34_sigma_two']['path'])
paths['core3new']=available('core3new',P3)
joined=[]
def covers(shape,row,partner,ordinary,extra,path):
 base=H|fan('L',shape)|partner|ordinary
 rec=paths[path];assert rec['U']<=base and not rec['Z']&(base|extra),(shape,row,path)
 joined.append({'L':shape,'row':row,'path':path,'reflections':rec['reflections'],'minimum':sorted(base),'upper':sorted(base|extra)})
for shape in ((0,1,2),(0,1,2,3)):
 other=fan('D',(1,2))|fan('R',(3,4))
 covers(shape,'BO',fan('B',(0,1)),fan('E',(4,))|fan('Tc',(5,))|fan('N',(5,)),set(),'BO_five')
 ordinary=fan('E',(4,))|fan('Tc',(5,))|fan('N',(5,))
 covers(shape,'BC D2abs',fan('B',(1,2)),ordinary,fan('D',(1,))|fan('R',(3,4)),'B_center_eight')
 covers(shape,'BC D2present',fan('B',(1,2))|fan('D',(2,)),ordinary,set(),'B_D2_complement_six')
 ordinary=fan('B',(1,))|fan('Tc',(5,))|fan('N',(5,))
 covers(shape,'EO',fan('E',(4,5)),ordinary,set(),'EO_sigma_five')
 covers(shape,'EC R3abs',fan('E',(3,4)),ordinary,fan('D',(1,2))|fan('R',(4,)),'E_center_sigma_eight')
 covers(shape,'EC R3present',fan('E',(3,4))|fan('R',(3,)),ordinary,set(),'E_R3_complement_six')
 covers(shape,'Tc center',fan('Tc',(5,6)),fan('B',(1,))|fan('E',(4,))|fan('N',(5,)),other,'T3')
 covers(shape,'D center',fan('D',(1,2)),refs,set(),'D2new')
 covers(shape,'R center',fan('R',(3,4)),refs,set(),'R2new')
 ordinary=fan('B',(1,))|fan('E',(4,))|fan('Tc',(5,))
 covers(shape,'N center D2abs',fan('N',(5,6)),ordinary,fan('D',(1,))|fan('R',(3,4)),'N3')
 covers(shape,'N center D2present',fan('N',(5,6))|fan('D',(2,)),ordinary,set(),'N6')
 covers(shape,'N southwest',fan('N',(4,5)),ordinary,set(),'core3new')
assert max(r['reflections'] for r in joined)==8
# Parent static frontier and all pinned sources are current.
front=read(ROOT/'surplus-four-local/outside-C-frontier.json')
for rel,digest in front['source_sha256'].items():
 f=ROOT/rel;reads.append(f);assert hashlib.sha256(f.read_bytes()).hexdigest()==digest,rel
assert len(front['remaining_L7012_necessary_descriptions'])==8
# Necessary h1 remaining list, after retaining exactly the published dispatch.
remaining=['E45/N5/D2','E45/N5/R3','E34/N5/D2/R4','D12/E4/N5/R3','D23/E4/N5/Rempty','R23/E4/N5/Dempty','N45/E4/D2','N45/E4/R3']
assert remaining==front['remaining_L7012_necessary_descriptions']
reads += [ROOT/'surplus-four-local'/f for f in ('outside-L0123-D12-search/findings.txt','outside-L0123-N45-search/findings.txt','outside-L0123-D12-search/coverage.txt','outside-L0123-N45-search/coverage.txt','outside-C-frontier.txt','mixed-Eouter-dispatch-review/review.txt')]
reads += [ROOT/'fourth-surplus-review/peer-roof-three-independent/review.txt',ROOT/'surplus-four-local/e2-e1-b1/critical-L-continuation.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_OUTSIDE_TWO_THREE_AND_L0123_JOIN_PASS_WITH_NEW_L012_EIGHT_EXTENSION','new_paths':records,'strict_gates':gates,'two_frozen_polygons':{'D12':geo2,'N45':geo3},'eight_named_transfers':applications,'h0_outside_dispatch':joined,'whole_L0123_accepted_bound':8,'NEW_whole_L012_bound_pending_peer_review':8,'previous_L012_bound':15,'remaining_L7012_necessary_descriptions':remaining,'scope':'Two and three and reflected witnesses plus eight parent inclusions ACCEPT. Whole L0123<=8 independently checked with all nine table rows and complements. Same exact join newly proves L012<=8 pending independent peer challenge; original conservative<=15 remainsvalid. Eight h1 residues are necessary descriptions, not certified rooms/darkness. Upstream local/forcing/classification prerequisites retained; fullDelta4/universal minimum OPEN.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: TWO/THREE finite optical proofs, eight transfers, two frozen polygons; ALL9table rows for BOTH L0123 and L012 <=8; newL012 extension pending peer.')
