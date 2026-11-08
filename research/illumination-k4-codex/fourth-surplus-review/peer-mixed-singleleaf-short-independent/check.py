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
# Fixed paths ONLY from already independently accepted receipts.
eights=read(ROOT/'fourth-surplus-review/peer-critical-L-eights-independent/check.json')['fixed_paths']
outside=read(ROOT/'fourth-surplus-review/peer-outside-two-three-independent/check.json')['new_paths']
rootleaf=read(ROOT/'fourth-surplus-review/mixed-e2-e1/root-leaf-check.json')
parentfile=ROOT/'surplus-four-local/mixed-singleleaf-short-transfer/check.json';parent=read(parentfile)
for rel,digest in parent['source_sha256'].items():
 p=ROOT/rel;reads.append(p);assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,rel
named={'E8':eights['E_center_sigma_eight']['path'],'E6':eights['E_R3_complement_six']['path'],'R2':outside['R34_sigma_two']['path'],'C3':outside['core_three']['path'],'CS3':outside['sigma_core_three']['path'],'L12':rootleaf['named_implications']['center_L_Nrright_Tplus_absent']['path']}
guards={}
for name,P in named.items():
 P=fp(P);U,Z=path_requirements(P)
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
 su,sz=path_requirements([sigma(p) for p in P[::-1]]);assert (su,sz)==(tr(U),tr(Z))
 guards[name]={'path':[[str(x) for x in p] for p in P],'U':sorted(U),'Z':sorted(Z),'reflections':len(P)-2}
Bmax=fan('B',(6,7,0,1));Ball=fan('B',(6,7,0,1,2));Dleaves=fan('D',(3,4))
apps=[]
def fits(name,low,high,path):
 rec=guards[path];U,Z=decode(rec['U']),decode(rec['Z'])
 assert low<=high and U<=low and not Z&high,name
 apps.append({'name':name,'minimum':sorted(low),'maximum':sorted(high),'path':path,'reflections':rec['reflections']})
base=H|Bmax|full('D')|fan('L',(0,))|fan('E',(3,4))|fan('N',(0,))
fits('ENTIRE_Ecenter_R3',H|fan('E',(3,4))|fan('R',(3,)),base|fan('R',(3,)),'E6')
fits('ENTIRE_Ecenter_R4',H|fan('E',(3,4)),base|fan('R',(4,)),'E8')
base=H|Ball|full('D')|fan('L',(0,))|fan('E',(4,))|fan('N',(7,))|fan('R',(3,4))|fan('Tc',(5,))
fits('Rcenter_Tc6abs_ALL_Broot_forms',H|fan('R',(3,4)),base,'R2')
base=H|Ball|Dleaves|fan('L',(0,))|fan('E',(4,))|fan('N',(7,0))|fan('R',(4,))|fan('Tc',(5,6))
fits('N70_R3abs_ALL_Broot_forms',H,base,'C3')
base=H|Bmax|Dleaves|fan('L',(7,0))|fan('E',(4,))|fan('N',(0,7))|fan('R',(4,))|fan('Tc',(5,6))
fits('L70_N6abs_R3abs',H,base,'C3')
base=H|Bmax|Dleaves|fan('L',(7,0))|fan('E',(4,))|fan('N',(6,))|fan('Tc',(6,))
fits('L70_N6present_Tc6_Rempty',H,base,'CS3')
for theirs,ours in zip(parent['whole_support_applications'],apps):
 assert decode(theirs['minimum'])==decode(ours['minimum']) and decode(theirs['maximum'])==decode(ours['maximum']) and theirs['reflections']==ours['reflections']
# Explicit old complement. This is WHY the new3 does not establish a
# universal3 bound for every R3-absent L70 room in the original full branch.
base=H|Bmax|Dleaves|fan('L',(7,0))|fan('E',(4,))|fan('R',(3,4))|fan('N',(6,))|fan('Tc',(5,))
fits('old_L12_N6_Tc6abs_complement',H|fan('L',(7,0))|fan('E',(4,)),base,'L12')
named_old_case=H|Bmax|Dleaves|fan('L',(7,0))|fan('E',(4,))|fan('N',(6,))|fan('R',(4,))
assert decode(guards['C3']['Z'])&named_old_case
assert decode(guards['CS3']['Z'])&named_old_case
assert decode(guards['L12']['U'])<=named_old_case and not decode(guards['L12']['Z'])&named_old_case
# This is only a fixed support envelope to challenge a BOUND, not a new
# completed-room validity test or a counterexample to a3path theorem.
# Symbolic budget: centeredL/N/E/R c1, hence n=3+h; quarterR c0 n2+h.
assert {h:2+h+1 for h in (0,1)}=={0:3,1:4}
# Shared B/D junction and root h contribution, checked as local angle identities.
for ss in ((7,0,1),(6,7,0,1),(7,0,1,2)):
 for leaf in (3,4):
  assert angle(H|fan('B',ss)|fan('D',(leaf,)),(1,-2))==270
# L70 + ordinary N5 creates forbidden smoothB; the preceding table excludes it.
assert angle(H|fan('L',(7,0))|fan('N',(5,)),(-1,1))==180
# E34/Tc6 and ordinaryN0/Tc5 create the TWO separate unhealed points used
# by upstream Ecenter table to force Tcempty (within this root/leaf class).
assert angle(H|fan('E',(3,4))|fan('Tc',(6,)),(3,3))==180
assert angle(H|fan('N',(0,))|fan('Tc',(5,)),(1,3))==180
remaining={
 'L70':'O3/O4; ordinaryR3 plus N0,N7 orTc6; eitherDleaf',
 'E34':'NONE; entirefamily<=8 includingearlier<=6/forcingcovers',
 'E45':'H4/D3 withordinaryR3,Tcempty, subjecttoseparateEOproof',
 'R34':'H4/Tc6, eitherDleaf; unitcontainsR3',
 'R23':'H4/Tcempty, eitherDleaf; unitcontainsR3',
 'N70':'ordinaryR3; TcemptyforO3/O4,Tc6forH4; eitherDleaf'}
reads += [ROOT/'surplus-four-local/mixed-singleleaf-short-transfer'/f for f in ('argument.txt','check.py','coverage.txt')]
reads += [ROOT/'fourth-surplus-review/mixed-e2-e1/argument.txt',ROOT/'fourth-surplus-review/mixed-Eouter-four-transfer/argument.txt',ROOT/'surplus-four-local/mixed-Eouter-dispatch-review/review.txt']
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'INDEPENDENT_MIXED_SINGLELEAF_SHORT_DISPATCH_ACCEPT_WITH_L70_BOUND_SCOPE_CLARIFICATION','six_accepted_path_guards':guards,'independent_whole_support_clauses':apps,'remaining_necessary_rows':remaining,'bounds':{'whole_E34':8,'R34_Tc6abs':2,'N70_R3abs':3,'previously_unresolved_L70_R3abs_subfamily':3,'whole_original_L70_R3abs_including_old_complement':12},'L70_caution':'OldN6/R4/Tcemptycomplement retainsL12; neithernewcore3guardcoversitswholeenvelope. No assertion the room lacks someother3path. Parentresidual-only3claimaccepted, broadwhole3notestablished.','limits':'No peercheckerexecution/newroom/capcensus/discovery/archive/worker. Existingfiniteopticalboundsinheritedfromacceptedreviews; newwholecase/slotdispatch handchecked. SeparateEOproofmayalreadysupersedethatremainingrow. Fullmixed/Delta4OPEN.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('ACCEPT: mixedE34entire<=8, R34Tc6abs<=2, N70R3abs<=3, residualL70R3abs<=3; originalL70R3abs bound12 retained.')
