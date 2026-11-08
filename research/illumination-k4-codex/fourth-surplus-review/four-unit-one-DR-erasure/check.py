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
# This reads ONLY the148 already independently accepted stored guard clauses,
# not a path archive, reflection words or any new completed rooms.
old=read(ROOT/'fourth-surplus-review/three-unit-b1-independent/check.json')
assert old['bound']==13
Dstar=full('D');Rstar=full('R');dependent=[]
for name,g in old['named_guards'].items():
 U,Z=decode(g['required']),decode(g['forbidden'])
 assert not U&(Dstar|Rstar),name
 hit=Z&(Dstar|Rstar)
 if hit:dependent.append((name,hit,g))
assert len(old['named_guards'])==148 and {k for k,_,_ in dependent}=={'three_CL_CE_BO_1','three_sigma_CL_CE_BO_1'}
for name,Z,g in dependent:
 minimum=decode(g['minimum'])
 if name=='three_CL_CE_BO_1':
  assert Z==fan('D',(3,)) and fan('B',(0,1))<=minimum
 else:assert Z==fan('R',(2,)) and fan('E',(4,5))<=minimum
# The ONLY unitD root containing3 is23. It meets B01 in unhealed180
# outsideC, so precisely that potentially blocking branch is impossibleb0.
assert [ss for ss in ((0,1),(1,2),(2,3)) if fan('D',ss)&fan('D',(3,))]==[(2,3)]
assert [ss for ss in ((2,3),(3,4),(4,5)) if fan('R',ss)&fan('R',(2,))]==[(2,3)]
for a,ss,b,tt,p in [('D',(2,3),'B',(0,1),(1,-2)),('R',(2,3),'E',(4,5),(4,1))]:
 base=H|fan(a,ss)|fan(b,tt)
 high=base|set().union(*(full(k) for k in C if k not in (a,b)))
 assert angle(base,p)==angle(high,p)==180
# Local bound on NEW extra smooth non-A points after deleting the soleDunit.
# Only non-A vertices of the deleted fan can change status. NorthC=(2,-1)
# is a baseline uncovered-H C, excluded fromb. Other candidates below.
# OtherRsite is ordinary (empty,3or4), never aunit in this subcase.
Bchoices=[(),(1,),(2,),(0,1),(1,2),(2,3)]
Rchoices=[(),(3,),(4,)]
# Independently record single-site angle ranges, never products ofcaps/rooms.
Bcontrib={p:sorted({angle(fan('B',ss),p) for ss in Bchoices}) for p in ((1,-1),(1,-2),(3,-1),(3,-2))}
Rcontrib={p:sorted({angle(fan('R',ss),p) for ss in Rchoices}) for p in ((1,-1),(1,-2),(3,-1),(3,-2))}
assert Bcontrib[(1,-1)]==[0,45,90] and Rcontrib[(1,-1)]==[0]
assert Bcontrib[(1,-2)]==[0,90] and Rcontrib[(1,-2)]==[0]
assert Bcontrib[(3,-1)]==[0] and Rcontrib[(3,-1)]==[0,45]
assert Bcontrib[(3,-2)]==Rcontrib[(3,-2)]==[0]
assert angle(H,(1,-1))==180 and angle(H,(3,-1))==90
assert angle(H,(1,-2))==angle(H,(3,-2))==0
for ss in ((0,1),(1,2),(2,3)):
 vertices={p for t in fan('D',ss) for p in t}
 nonA={p for p in vertices if any(x%2 for x in p)}
 assert nonA<= {(1,-1),(1,-2),(2,-1),(3,-1),(3,-2)}
# Thus afterdeletion ONLY(1,-1) can newly have extra smooth180;
# Cnorth smooth180 is baselineM; no otherchangedpoint contributes tob.
assert angle(H,(2,-1))==180
# Exactsource hashes pinned; underlying old theorem is accepted, not rerun.
reads += [ROOT/'surplus-four-local/three-unit-b1/argument.txt',ROOT/'fourth-surplus-review/three-unit-b1-independent/review.txt',ROOT/'fourth-surplus-review/four-unit-DR-erasure/argument.txt',ROOT/'fourth-surplus-review/four-unit-DR-erasure/check.json',ROOT/'surplus-four-local/two-unit.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'PARENT_FOUR_UNIT_AT_LEAST_ONE_DR_THIRTEEN','stored_three_unit_guard_count':148,'only_DR_dependent_clauses':[{'name':name,'forbidden':sorted(Z)} for name,Z,_ in dependent],'auxiliary_b_bound':1,'changed_vertex_single_site_coefficients':{'B':{str(k):v for k,v in Bcontrib.items()},'Rordinary':{str(k):v for k,v in Rcontrib.items()}},'parent_claim':'BothDRcase uses separatejointdeletion proof. ExactlyoneDunit deleteslegally to3unitROOTauxwithb0or1; accepted3unitcoverextendsb<=1 andall148clausesavoidD/R exceptretained9D3 andsigmaretained9R2. A blockingD23requiresB01 branch, makingunhealedC180forbiddenoriginalb0; sigmaR23/E45same. SelectedlegalactualSTpathsurvives<=13. Onlyno-positiveD/Rfourunitcasesremain.','limits':'Parenttheorypendingindependenthandreview. No completedroom, capproduct, path/ray/direction/word discovery, archive orworker. Only148storedacceptedguards andlocalanglecoefficients checked; topology/coverextension proof inargument.txt, existingopticallegalityinherited.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: auxiliary newb<=1 localcoefficients; onlyTWO D/R-sensitive acceptedguards, exactlyblockedbyoriginalb0junctions; parentatleastoneD/R<=13 pendinghandreview.')
