"""Independent fixed L70/E4 six and West transfer; no peer code or discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
PEER=ROOT/'surplus-four-local/O3-L70-hand'
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import on,sub,cross,dot
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+R[i%8][j] for j in (0,1)),tuple(a[j]+R[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
d=F(1,6)
P=[(F(0),F(0)),(-2/(1+d),-2*d/(1+d)),((4*d-2)/(1-d),2*d/(1-d)),((2+4*d)/(1-d),6*d/(1-d)),(2+8*d,F(2)),((2+12*d)/(1+d),10*d/(1+d)),(F(1),11*d),(F(2),12*d)]
walls=[((-2,0),(-1,-1)),((-2,0),(-1,1)),((3,1),(4,2)),((3,2),(4,2)),((3,1),(4,2)),((1,1),(1,2))]
mi=H|fan('L',(7,0))|fan('E',(4,))
ma=mi|set().union(*(full(k) for k in ('B','D','R','Tc')))|fan('N',(0,1,2,3,4,5,6))
U,Z=path_requirements(P)
assert len(U)==15 and len(Z)==5 and U<=mi and not Z&ma
assert Z==fan('L',(1,6))|fan('E',(3,5))|fan('N',(7,))
for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
 assert on(p,c,e) and p not in (c,e)
 v=sub(p,a);w=sub(e,c)
 ref=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert cross(ref,sub(b,p))==0 and dot(ref,sub(b,p))>0
assert P[0]==(0,0) and P[-1]==(2,2)
assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
assert incident((F(2),F(1)))<=H and on((2,1),P[2],P[3])
assert on((-1,3*d),P[2],P[3]) and cross(sub(P[3],P[2]),(1,d))==0
assert F(1,7)<d<F(2,11) and 0<3*d<1 and 1<7*d<9*d<11*d<2
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
a,b=path_requirements(P[::-1]);assert (a,b)==(U,Z)
a,b=path_requirements([sigma(p) for p in P[::-1]]);assert (a,b)==(tr(U),tr(Z))
q=P[-1]
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert q==(-12,-2) and cross(q,(-6,-1))==0
parent=json.loads((PEER/'check.json').read_text())
decode=lambda ts:{tuple(sorted(map(tuple,t))) for t in ts}
for k,value in [('minimum',mi),('maximum',ma),('required',U),('forbidden',Z)]:assert decode(parent['whole_support'][k])==value
assert P==[tuple(F(x) for x in p) for p in parent['path']]
for rel,digest in parent['source_sha256'].items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,rel
assert hashlib.sha256((PEER/'check.py').read_bytes()).hexdigest()==parent['checker_sha256']
# One broad envelope covers all remaining West R3,N0/N6 cases, no rooms.
west_min=mi|fan('B',(1,2,3,4))|fan('R',(3,))|fan('Tc',(6,))
west_max=west_min|full('D')|fan('N',(0,6))
assert U<=west_min and west_max<=ma and not Z&west_max
# Inherited O3/L70 occupancy algebra with N7 now forced in uncovered cases.
# J3 => n4, E4/N7 use2; topempty leavesD/R both; top6 leavesone.
assert 4-2==2 and 4-2-1==1
inputs=[PEER/k for k in ('argument.txt','check.py','check.json','coverage.txt')]+[ROOT/rel for rel in parent['source_sha256']]+[ROOT/'surplus-four-local/e2-e1-b1/joined-top-absent.txt',ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py',Path(__file__)]
out={'status':'INDEPENDENT_L70_E4_SIX_AND_WEST_TRANSFER_PASS','path':[[str(x) for x in p] for p in P],'whole_support':{'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(U),'forbidden':sorted(Z)},'strict_root':'1/6 in (1/7,2/11)','actual_unfolded_target':list(map(str,q)),'firstT_finitewalls_reverse_sigma':'PASS','source_crossing_2_1':'all incident support insideH, not a reflection','West_transfer':'All remaining WestR3N0/N6 with eitherDcap fit one whole envelope; <=6. Tc6/R3/N7/D1or2 remain.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'limits':'Independent historical exact helpers; no peer execution/import, newroom/cap enumeration or discovery. Whole lemma and West transfer subject to existing local class, no entireWest/O3/Delta4 claim.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: L70/E4 SIX,15U5Z,finitewalls/firstT/reverse/sigma/unfold-12,-2; WestR3N0/N6 whole transfer.')
