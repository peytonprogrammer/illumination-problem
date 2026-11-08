"""Independent three fixed paths, two supplied polygons, O3 join and L transfer.
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
def frozen(dirname,P,J,sn,count,smooth,wallends):
 directory=ROOT/'surplus-four-local'/dirname
 raw=read(directory/'room.json');result=read(directory/'result.json')
 assert hashlib.sha256((directory/'room.json').read_bytes()).hexdigest()==result['room_sha256']
 assert hashlib.sha256((directory/'search.py').read_bytes()).hexdigest()==result['search_source_sha256']
 reads.append(directory/'search.py') # read bytes for provenance only, never executed
 room=decode(raw['triangles']);assert len(room)==count and H<=room<=allK
 edges=[e for e,owners in geo.owners_of(sorted(room)).items() if len(owners)==1]
 adj=defaultdict(list)
 for a,b in edges:adj[a].append(b);adj[b].append(a)
 assert all(len(v)==2 for v in adj.values())
 cycle=[min(adj)];previous=None;cur=cycle[0]
 while True:
  nxt=next(p for p in adj[cur] if p!=previous)
  if nxt==cycle[0]:break
  assert nxt not in cycle;cycle.append(nxt);previous,cur=cur,nxt
 assert len(cycle)==len(edges)
 V=[p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
 assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
 assert replay(V,(0,0),(2,2),P)==len(P)-2
 def first_arrival(path,target):
  for i,(a,b) in enumerate(zip(path,path[1:])):
   if on(target,a,b):return path[:i+1]+[tuple(map(F,target))]
  raise AssertionError('target absent')
 reverse=first_arrival(P[::-1],(0,0))
 sigma_path=first_arrival([sigma(p) for p in P[::-1]],(2,2))
 assert replay(V,(2,2),(0,0),reverse)==len(reverse)-2
 assert replay([sigma(p) for p in V],(0,0),(2,2),sigma_path)==len(sigma_path)-2
 pts={p for t in room for p in t}
 assert {p for p in pts if all(v%2==0 for v in p) and angle(room,p)==360}=={(0,0),(2,0),(2,2)}
 nonA={p for p in pts if not all(v%2==0 for v in p)}
 assert sum(angle(room,p)==360 for p in nonA)==J
 assert sum(angle(room,p)==180 for p in nonA)==sn
 assert smooth not in V and angle(room,smooth)==180
 candidates=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(smooth,a,b)]
 assert len(candidates)==1 and set(candidates[0])==set(wallends)
 return {'walls':20,'triangles':count,'J':J,'sN':sn,'smooth_point':smooth,'maximal_wall':candidates,'actual_firstT_reverse_sigma':'PASS; reverse/sigma stopped at FIRST target visit','reverse_first_arrival_reflections':len(reverse)-2}
# New O3 five, transcribed independently from hand proof.
P5=fp([(0,0),(-1,'-2/5'),(1,'-6/5'),(0,'-8/5'),(1,-2),('2/7','-16/7'),(2,2)])
w5=[((-1,-1),(-1,0)),((1,-2),(1,-1)),((0,-2),(0,-1)),((1,-3),(1,-1)),((0,-2),(1,-3))]
file5=ROOT/'surplus-four-local/O3-R23-search/verification.json';v5=read(file5);provenance(v5,file5)
mi5=H|fan('B',(7,0,1));ma5=mi5|fan('L',(0,1,2,3,4,5,6))|fan('D',(0,1,2,5,6,7))|set().union(*(full(k) for k in ('R','E','Tc','N')))
u5,z5=optical('O3_five',P5,w5,mi5,ma5,(-10,-4),v5['whole_support'])
assert len(u5)==11 and z5==fan('L',(7,))|fan('D',(3,4))|fan('B',(2,6))
assert angle(mi5,(1,-2))==180 and incident((F(1),F(-2)))<=u5|z5
physical5=frozen('O3-R23-search',P5,2,4,32,(1,-2),((1,-3),(1,-1)))
d=F(2,5);assert F(1,3)<d<F(3,7)
assert P5==[(F(0),F(0)),(F(-1),-d),(F(1),-3*d),(F(0),-4*d),(F(1),-5*d),((6*d-2)/(1+d),-8*d/(1+d)),(10*d-2,F(2))]
# New L70 eleven and nine. Only the given eleven frozen room is replayed.
P11=fp([(0,0),('-1/4',-1),('-3/4',1),('-6/5','-4/5'),(3,'1/4'),(0,1),('-4/3','2/3'),('-8/5','-2/5'),(3,'3/4'),('2/3','4/3'),('1/2',2),('2/5','8/5'),(2,2)])
P9=fp([(0,0),('-1/4',-1),('-3/4',1),('-6/5','-4/5'),('18/5','2/5'),('7/2',0),('10/3','2/3'),('2/3','4/3'),('1/2',2),('2/5','8/5'),(2,2)])
w11=[((-1,-1),(0,-1)),((-1,1),(0,1)),((-2,0),(-1,-1)),((3,0),(3,1)),((-1,1),(1,1)),((-2,0),(-1,1)),((-2,0),(-1,-1)),((3,0),(3,1)),((0,2),(1,1)),((0,2),(1,2)),((0,2),(1,1))]
w9=w11[:3]+[((3,1),(4,0)),((3,0),(4,0)),((3,1),(4,0))]+w11[-3:]
fileN=ROOT/'surplus-four-local/L70-N7-search/verification.json';vN=read(fileN);provenance(vN,fileN)
mi11=H|fan('L',(7,0))|fan('N',(7,))
ma11=mi11|fan('B',(0,1,3,4,5,6,7))|set().union(*(full(k) for k in ('D','E','Tc')))|fan('R',(0,1,2,4,5,6,7))|fan('N',(1,2,3,4))
u11,z11=optical('L70_eleven',P11,w11,mi11,ma11,(-6,-24),vN['eleven'])
mi9=mi11|fan('R',(3,))
ma9=mi9|fan('B',(0,1,3,4,5,6,7))|set().union(*(full(k) for k in ('D','E','Tc')))|fan('R',(0,1,5,6,7))|fan('L',(1,2,3,4,5))|fan('N',(1,2,3,4))
u9,z9=optical('L70_nine',P9,w9,mi9,ma9,(-4,-16),vN['nine'])
assert len(u11)==22 and z11==fan('L',(1,6))|fan('B',(2,))|fan('R',(3,))|fan('N',(0,5,6))
assert len(u9)==21 and z9==fan('L',(6,))|fan('B',(2,))|fan('R',(2,4))|fan('N',(0,5,6))
for P in (P11,P9):assert on((-1,0),P[2],P[3]) and incident((F(-1),F(0)))<=mi11
assert angle(mi11,(0,1))==180 and incident((F(0),F(1)))<=u11|z11
physical11=frozen('L70-N7-search',P11,3,3,33,(0,1),((-1,1),(1,1)))
# NEW own suffix after the last actual S visit; no new direction or word chosen.
assert on((0,0),P11[7],P11[8])
P4=[(F(0),F(0))]+P11[8:]
mi4=H|fan('N',(7,))
ma4=mi4|set().union(*(full(k) for k in ('L','B','D','E','Tc')))|fan('R',(0,1,2,4,5,6,7))|fan('N',(1,2,3,4,5))
u4,z4=optical('OWN_source_suffix_four',P4,w11[7:],mi4,ma4,(8,2),None)
assert z4==fan('R',(3,))|fan('N',(0,6))
assert physical11['reverse_first_arrival_reflections']==4
d=F(1,4);assert F(5,21)<d<F(6,23) and F(3,13)<d<F(4,15)
assert 24*d-4==16*d-2==2 and 4-1/d==0
assert 0<9*d-2<1 and 0<19*d-4<1 and 1<21*d-4<23*d-4<2
assert 0<9*d-2<11*d-2<1 and 1<13*d-2<15*d-2<2
# Earlier accepted short-forcing and D23 exceptions, checked at whole supports.
old=read(ROOT/'fourth-surplus-review/peer-critical-B-b1-independent/check.json')
clauses={c['name']:c for c in old['whole_envelopes']}
assert set(('force_E4','force_L0_Eordinary','force_L0_Ecenter','force_L0_Eouter'))<=clauses.keys()
assert allK-fan('E',(4,))==decode(clauses['force_E4']['maximum'])
joined=read(ROOT/'fourth-surplus-review/mixed-e2-e1/joined-four-check.json')
for name,rec,tc in [('four',joined,(0,1,2,3,4,6,7)),('six',joined['six_path_complement'],(5,))]:
 P=fp(rec['path']);u,z=path_requirements(P)
 ma=mi5|fan('D',(2,3))|set().union(*(full(k) for k in ('L','E','R','N')))|fan('Tc',tc)
 minimum=mi5|fan('D',(2,3))|(fan('Tc',(5,)) if name=='six' else set())
 assert u<=minimum and not z&ma
# L70 dispatch is by ordinary R and N, not a cap product.
six=read(ROOT/'fourth-surplus-review/peer-L70-six-independent/check.json')
assert six['status']=='INDEPENDENT_L70_E4_SIX_AND_WEST_TRANSFER_PASS'
assert decode(six['whole_support']['minimum'])<=H|fan('B',(7,0,1))|fan('L',(7,0))|fan('E',(4,))
for k in ('D','R','Tc'):assert full(k)<=decode(six['whole_support']['maximum'])
assert fan('N',(0,6))<=decode(six['whole_support']['maximum'])
assert mi11|fan('B',(7,0,1))|fan('R',(4,))<=ma11
assert mi9|fan('B',(7,0,1))<=ma9
assert mi11|fan('B',(7,0,1))|fan('R',(4,))<=ma4
# Conditional mixed single-leaf Eouter residual: Rempty for O3/O4, N7 present.
eouter_residual=H|fan('B',(6,7,0,1))|fan('B',(2,))|full('D')|fan('E',(4,5))|full('L')|full('Tc')|fan('N',(7,))
assert eouter_residual<=ma4 and u4<=H|fan('N',(7,))
# New L701/E34/B1/Tc5/N7/R3 common lower and FULLD upper inclusion.
critical=H|fan('L',(7,0,1))|fan('E',(3,4))|fan('B',(1,))|fan('Tc',(5,))|fan('N',(7,))|fan('R',(3,))
assert u9<=critical and critical|full('D')<=ma9 and not z9&(critical|full('D'))
table=ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt';reads.append(table)
assert 'TWO:   L701 +EC+B+/T-/Nr- +R+ and D- or D+.' in table.read_text()
transfer=read(ROOT/'surplus-four-local/nine-critical-L-transfer/check.json')
assert decode(transfer['common_minimum'])==critical and decode(transfer['maximum_with_full_D'])==critical|full('D')
for rel,digest in transfer['source_sha256'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,rel
# West's B2 prevents nine/eleven transfer; no accidental West closure.
assert fan('B',(2,))&z9 and fan('B',(2,))&z11
reads += [ROOT/'surplus-four-local'/k for k in ('O3-R23-search/findings.txt','O3-R23-search/verify.py','L70-N7-search/findings.txt','L70-N7-search/verify.py','nine-critical-L-transfer/argument.txt','nine-critical-L-transfer/check.py','O3-L70-hand/argument.txt')]
reads += [ROOT/'triangle-composition/inputs'/k for k in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_O3_COMPLETE_AND_CRITICAL_L_TWO_TRANSFER_PASS','fixed_paths':records,'frozen_physical_checks':{'five':physical5,'eleven':physical11},'dispatch':'O3 outsideL70 NEW5 except D23accepted4/6; shortforcing<=4. L70 N7absaccepted6; N7R3new9; N7noR3new11. EntirelocalO3two-rootb1<=11.','OWN_short_suffix_consequence':'Four derived from source revisit has9U3Z, minH+N7, maxfullL/B/D/E/Tc+Rexcept3+Nexcept0/6; improves wholeO3 parentbound11->9 pending independent review of ownfour. Conditional mixedEouter O3/O4 N7residual Rempty also fits.',
'critical_L_transfer':'One lower support plus FULLD fits nine maximum; both original L701/E34/N7/R3 D1/D2 named descriptions close<=9. Relative historical8->6 only, no fullcriticalL classification.','West_limit':'B2 intersects both new9/11 forbidden sets; no transfer to remainingWestTc6R3N7D1or2.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)},'limits':'Own historical exact helpers and supplied frozen polygons ONLY; no peer code execution/import, search rerun, newroom/cap/direction/word discovery or workers. Hand verdict in review.txt; independent AI review, not formal/expert verification.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: independent O3five/L70nine-eleven +wholeO3<=11 +two criticalL transfers; ownsource-suffix FOUR9U3Z improves O3parentbound<=9 pending peer review.')
