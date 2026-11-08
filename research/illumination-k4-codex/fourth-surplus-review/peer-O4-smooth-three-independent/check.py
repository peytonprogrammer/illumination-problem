"""Independent fixed O4 path and whole two-root dispatch; no room or discovery."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
PEER=ROOT/'surplus-four-local/e2-e1-b1'
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import on,sub,cross,dot
rays=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=centers[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+rays[i%8][j] for j in (0,1)),tuple(a[j]+rays[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
mi=H|fan('B',(6,7,0,1))
ma=mi|fan('D',(0,1,2,5,6,7))|set().union(*(full(k) for k in ('L','R','E','Tc','N')))
P=[(F(0),F(0)),(F(1),F(-2)),(F(1,2),F(-3)),(F(0),F(-2)),(F(2),F(2))]
walls=[((1,-3),(1,-1)),((0,-3),(1,-3)),((0,-3),(0,-1))]
U,Z=path_requirements(P)
assert len(U)==11 and len(Z)==7 and U<=mi and not Z&ma
assert Z==fan('B',(2,3,4,5))|fan('D',(3,4))|fan((0,-4),(1,))
for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
 assert on(p,c,e) and p not in (c,e)
 v=sub(p,a);w=sub(e,c)
 reflected=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert cross(reflected,sub(b,p))==0 and dot(reflected,sub(b,p))>0
assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
assert incident((F(1),F(0)))<=H and on((1,0),P[-2],P[-1])
# Independent angular-wedge masks verify a single full half-plane at smooth hits.
probes=((2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1))
def mask(ts,p):
 bits=0
 for t in ts:
  if p not in t:continue
  a,b=[sub(v,p) for v in t if v!=p]
  if cross(a,b)<0:a,b=b,a
  new=sum(1<<i for i,v in enumerate(probes) if cross(a,v)>0 and cross(v,b)>0)
  assert not bits&new
  bits|=new
 return bits
for p,expected in [((1,-2),0b00111100),((0,-2),0b11000011)]:
 assert mask(mi,p)==expected and mask(mi,p).bit_count()==4
 assert incident(p)<=U|Z
 # All interior-side triangles required, exterior ones forbidden.
 assert incident(p)&mi<=U and incident(p)-mi<=Z
 assert mask(ma,p)==expected
q=P[-1]
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert q==(4,-8) and cross(q,(1,-2))==0
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
ur,zr=path_requirements(P[::-1]);assert (ur,zr)==(U,Z)
us,zs=path_requirements([sigma(p) for p in P[::-1]]);assert (us,zs)==(tr(U),tr(Z))
d=F(1,2)
assert F(3,7)<d<F(3,5)
assert P==[(F(0),F(0)),(F(1),-1/d),(2-3*d,F(-3)),(F(0),2/d-6),(8*d-2,F(2))]
assert -3<-1/d<-1 and 0<2-3*d<1 and -3<2/d-6<-1
assert 0<5*d-2<1 and 1<7*d-2<3
# Compare with frozen parent values; no parent execution/import.
reads=[]
def load(p):reads.append(p);return json.loads(p.read_text())
def dec(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
parent=load(PEER/'O4-smooth-three.json')
assert parent['status']=='PARENT_O4_SMOOTH_THREE_SUPPORT_PASS'
for key,own in [('minimum',mi),('maximum',ma),('required',U),('forbidden',Z)]:assert dec(parent['whole_support'][key])==own
for rel,digest in parent['source_sha256'].items():
 p=ROOT/rel;reads.append(p)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,rel
assert hashlib.sha256((PEER/'O4-smooth-three.py').read_bytes()).hexdigest()==parent['checker_sha256']
# Full other-site maximum gives a proof for ANY unit there, including bridges;
# no unit-direction enumeration is needed.
for k in ('L','R','E','Tc','N'):assert full(k)<=ma
assert fan('D',(1,2))<=ma
Dforms=[(j,(j+1)%8) for j in range(8) if j in (0,1,2)]
assert Dforms==[(0,1),(1,2),(2,3)]
assert all(mi|fan('D',ss)<=ma for ss in Dforms[:2])
oldpath=ROOT/'fourth-surplus-review/mixed-e2-e1/joined-square-check.json'
old=load(oldpath)
accepted=load(ROOT/'surplus-four-local/joined-square-review/check.json')
assert hashlib.sha256(oldpath.read_bytes()).hexdigest()==accepted['source_sha256'][str(oldpath.relative_to(ROOT))]
rest=H|fan('B',(6,7,0,1))|full('D')|set().union(*(full(k) for k in ('L','R','E','N')))
D23=fan('D',(2,3))
for key,minimum,maximum in [('two',mi|D23,rest|fan('Tc',(0,1,2,3,4,6,7))),('four',mi|D23|fan('Tc',(5,)),rest|fan('Tc',(5,)))]:
 record=old['paths'][key]
 path=[tuple(F(x) for x in p) for p in record['path']]
 u,z=path_requirements(path)
 assert u==dec(record['required']) and z==dec(record['forbidden'])
 assert u<=minimum and not z&maximum
# Both single leaves genuinely violate the NEW3 mirror conditions.
assert fan('D',(3,))&Z and fan('D',(4,))&Z
assert fan((0,-4),(1,))&Z and not fan((0,-4),(1,))&ma
reads += [PEER/'O4-smooth-three.txt',PEER/'O4-smooth-three.py',PEER/'argument.txt',ROOT/'surplus-four-local/joined-square-review/review.txt',ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']
result={'status':'INDEPENDENT_O4_SMOOTH_THREE_WHOLE_TWO_ROOT_B1_PASS','path':[[str(x) for x in p] for p in P],'U_count':len(U),'Z_count':len(Z),'smooth_contacts':{'(1,-2)':180,'(0,-2)':180},'unfolded_actual_target':list(map(str,q)),'finite_mirrors_firstT_reverse_sigma':'PASS','two_root_dispatch':'All away-D units and D01/D12 use NEW3, D23 uses accepted ordinary-Tc2/4. No L/E forcing. Bound4.','remote_scope':'Remote(0,-4)sector1 must be absent; ensured by local K only.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dict.fromkeys(reads)},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Fixed path/support only; no new rooms or discovery. Independent historical guard primitives, no parent execution/import. Inherited local two-root H-facing classification and D23 prior optical proof. No single-leaf transfer, fullDelta4 or universal minimum.'}
(HERE/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: NEW3 smooth C/A180,11U7Z,finite mirrors/firstT/reverse/sigma/unfold4,-8; whole local O4two-rootb1<=4; no leaf transfer.')
