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
P=fp([(0,0),(3,-1),(2,2)]);W=[((2,-2),(4,0))];u,z=path_requirements(P);mi=H|fan('D',[1])|fan('R',[4]);ma=(allK|full((-2,-2)))-z
assert z==fan('D',[0])|fan('R',[5])|fan((4,-2),[2,3])
optical('smooth_B_one',P,W,mi,ma,(6,-2),None)
assert angle(mi,(3,-1))==180 and not (incident((F(3),F(-1)))-mi-z)
assert u<=mi and not z&mi
assert sub(P[-1],P[1])==(-1,3) and sub(P[1],P[0])==(3,-1)
# Firstwallnotatacorner: two required radialhalves supplystrictmirrorsegment.
assert all(on(p,*W[0])for p in [(2,-2),(3,-1),(4,0)])
for k in ['L','B','E','Tc','N']:assert not z&full(k)
# EntireORDINARYD1R4branch hasD0/R5absent bysingle-cap exclusivity.
upper=H|fan('D',[1])|fan('R',[4])|full('L')|full('B')|full('E')|full('Tc')|full('N')|full((-2,-2))
assert u<=upper and not z&upper
reads += [ROOT/'triangle-composition/inputs/guard_checker.py',Path(__file__)]
out={'status':'PARENT_SMOOTH_B_ONE_WHOLE_ORDINARY_D1_R4_BRANCH_PASS','fixed_paths':records,'smooth_point':[3,-1],'angle':180,'actual_endpoint_image':[6,-2],'whole_support_lemma':'minimum H+D1+R4, blockers D0,R5,remote(4,-2)2/3; otherK andBremote(-2,-2) safe','geometry_scope':'No controlroomconstructed. Exactfullincidenthalf-star andopenlegcertificate provewholeimplication foranycanonicalcompletion withactualinteriorS/T.','limits':'Parentproofawaitsindependentreview. This closesX=[D1][R4] ordinarybudgetterm, notwholeBfamily.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dict.fromkeys(reads)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS smoothBONE',len(u),'U',len(z),'Z; H+D1R4 withD0R5andremote4,-2sectors2/3absent')
