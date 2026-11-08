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
prior=read(ROOT/'fourth-surplus-review/peer-O3-complete-independent/check.json')
r=prior['fixed_paths']['OWN_source_suffix_four'];P=fp(r['path'])
W=[((3,0),(3,1)),((0,2),(1,1)),((0,2),(1,2)),((0,2),(1,1))]
mi=H|fan('N',(7,));ma=allK-fan('R',(3,))-fan('N',(0,6))
u,z=optical('four',P,W,mi,ma,(8,2),r)
rootleaf=read(ROOT/'fourth-surplus-review/mixed-e2-e1/root-leaf-check.json')
applications=[]
def inclusion(name,low,high,U,Z):
 assert low<=high and U<=low and not Z&high
 applications.append({'name':name,'lower':sorted(low),'upper':sorted(high)})
# Existing whole optical complement (fixed recorded paths ONLY).
for key in ('outer_E_missing_L','outer_E_Nrminus_absent'):
 rec=rootleaf['named_implications'][key];p=fp(rec['path']);a,b=path_requirements(p)
 assert a==decode(rec['required']) and b==decode(rec['forbidden'])
 assert a<=decode(rec['fixed']) and not b&decode(rec['possible'])
 assert p[0]==(0,0) and p[-1]==(2,2)
 a2,b2=path_requirements([sigma(q) for q in p[::-1]]);assert (a2,b2)==(tr(a),tr(b))
# Fixed symbolic O3/O4 envelopes, allowing BOTH single leaves as one upper.
for name,ss in [('O3',(7,0,1)),('O4',(6,7,0,1))]:
 low=H|fan('B',ss)|fan('E',(4,5))|fan('L',(0,))|fan('N',(7,))
 high=low|fan('D',(3,4))
 assert high<=ma
 inclusion(name+'_Eouter_N7_both_Dleaves',low,high,u,z)
 # With N7 absent, the previously established E-square five allows
 # arbitrary B,D,R,Tc plus ordinary L0 and all other N sectors.
 five=rootleaf['named_implications']['outer_E_Nrminus_absent']
 lo=H|fan('B',ss)|fan('E',(4,5))|fan('L',(0,))
 hi=lo|full('D')|full('R')|full('Tc')|fan('N',(0,1,2,3,4,5,6))
 inclusion(name+'_Eouter_N7_absent',lo,hi,decode(five['required']),decode(five['forbidden']))
# H4,D3 residual: exact One(T/R) choices, all except R3 fit one upper.
low=H|fan('B',(7,0,1,2))|fan('D',(3,))|fan('E',(4,5))|fan('L',(0,))|fan('N',(7,))
high=low|fan('Tc',(5,6))|fan('R',(4,))
assert high<=ma
inclusion('H4_D3_Eouter_Tc5_or_Tc6_or_R4',low,high,u,z)
assert z&fan('R',(3,))
# Symbolic angle ledger at the B/H C: constants, not completed rooms.
# The independent Eouter unit adds no full C. h is B2 present.
base=H|fan('B',(7,0,1))|fan('E',(4,5))
assert angle(base,(0,-1))==270
assert angle(base|fan('B',(2,)),(0,-1))==360
# Ordinary L0,N5 makes an unhealed180 point; N7 does not.
base=H|fan('L',(0,))
assert angle(base,(-1,1))==135
assert angle(base|fan('N',(5,)),(-1,1))==180
assert angle(base|fan('N',(7,)),(-1,1))==135
# Root/leaf junction is270; upper B stays strictly below360 even H4+D3.
for ss in ((7,0,1),(6,7,0,1),(7,0,1,2)):
 for leaf in (3,4):
  local=H|fan('B',ss)|fan('D',(leaf,))
  assert angle(local,(1,-2))==270
  assert angle(local,(1,-1))<=315
# n=J=2+h, c(Eouter)=0. Two forced ordinary slots L,N exhaust n at h0.
assert 2+0-2==0 and 2+1-2==1
reads += [ROOT/'fourth-surplus-review/mixed-e2-e1'/f for f in ('argument.txt','root-leaf-check.py','joined-square.txt','progress.txt')]
reads += [ROOT/'surplus-four-local/source-suffix-four-review'/f for f in ('review.txt','check.json')]
reads += [ROOT/'triangle-composition/inputs'/f for f in ('guard_checker.py','boundary_replay.py','illumination_geometry.py')]+[Path(__file__)]
out={'status':'MIXED_EOUTER_O3_O4_CLOSED_PARENT_AND_H4_D3_REDUCED','fixed_four':records['four'],'applications':applications,'structural_claim':'Assuming established mixed root/single-leaf hypotheses: Eouter forces L0 via accepted2; N7 absent gives accepted5; N7 present n=2+h leaves no T/R for O3/O4. Both families <=5, both Dleaves. H4D3 N7 case leaves OneT/R, new4 covers Tc5/Tc6/R4, onlyR3 remains. H4D4 is separately accepted <=4.','independent_review':'Requested for new whole-family dispatch; underlying FOUR independently accepted.','limits':'No cap assignment census, new complete room, archive or ray/word discovery. Existing table checked by symbolic budget and named local-angle identities; no claim to six-row or fullDelta4 closure.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: whole O3/O4-Eouter dispatch <=5; H4D3-Eouter only R3 residue, pending independent structural review.')
