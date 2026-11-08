"""Fixed affine map identities and eight declared tiles. No state/word search."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
I=((1,0,0),(0,1,0),(0,0,1))
V=((-1,0,0),(0,1,0),(0,0,1))
H=((0,-1,1),(-1,0,1),(0,0,1))
def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def word(w):
 A=I
 for c in w:A=mul({'H':H,'V':V}[c],A)
 return A
def apply(A,p):return tuple(sum(A[i][j]*p[j] for j in range(2))+A[i][2] for i in range(2))
# All maps are specified analytically before checking them.
expected={
 'H':((0,-1,1),(-1,0,1),(0,0,1)),
 'HV':((0,1,-1),(-1,0,1),(0,0,1)),
 'HVH':((1,0,0),(0,-1,2),(0,0,1)),
 'HVHV':((-1,0,0),(0,-1,2),(0,0,1)),
 'VHVH':((-1,0,0),(0,-1,2),(0,0,1)),
 'VHV':((0,1,-1),(1,0,1),(0,0,1)),
 'VH':((0,-1,1),(1,0,1),(0,0,1))}
for w,A in expected.items():
 assert word(w)==A
 assert apply(A,(0,1))==(0,1)
 assert all(sum(A[k][i]*A[k][j] for k in range(2))==int(i==j) for i in range(2) for j in range(2))
# Eight fixed dihedral images, no generation of reflection words.
words=['','V','H','HV','VH','HVH','VHV','HVHV']
base=[(0,0),(1,0),(0,1)];tiles=[];portals=[]
for w in words:
 A=word(w);t=tuple(sorted(apply(A,p) for p in base));tiles.append(t)
 portals.append(tuple(sorted(apply(A,p) for p in base[:2])))
 assert (0,1) in t and all(-1<=x<=1 and 0<=y<=2 for x,y in t)
 p,q,r=t
 assert abs((q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]))==1
assert len(set(tiles))==8 and len(set(portals))==8
expected_portals={((-1,0),(0,0)),((0,0),(1,0)),((1,0),(1,1)),((1,1),(1,2)),((0,2),(1,2)),((-1,2),(0,2)),((-1,1),(-1,2)),((-1,0),(-1,1))}
assert set(portals)==expected_portals
# Exact endpoint expressions: pair of linear coefficients in u and tau.
# Applying the fixed matrices to each boundary half-edge yields these
# identities for ALL coordinates, rather than checking selected rays.
for w,boundary,expected_coeff in [
 ('H','right',((-1,1),(0,0))),
 ('HV','right',((1,-1),(0,0))),
 ('HVH','top',((1,0),(0,0))),
 ('HVHV','top',((-1,0),(0,0))),
 ('VHVH','top',((-1,0),(0,0))),
 ('VHV','left',((1,-1),(0,0))),
 ('VH','left',((-1,1),(0,0)))]:
 A=word(w)
 if boundary=='right':coeff=tuple((A[i][1],A[i][0]+A[i][2]) for i in range(2))
 elif boundary=='left':coeff=tuple((A[i][1],-A[i][0]+A[i][2]) for i in range(2))
 else:coeff=tuple((A[i][0],2*A[i][1]+A[i][2]) for i in range(2))
 assert coeff==expected_coeff
# Exact symbolic singular-line events a=(c0+c1*u)/den at time t.
events=[('right_mid',(1,-1,1),1,(1,1)),('right_corner',(1,-1,2),2,(1,2)),('top_mid',(0,-1,2),2,(0,2)),('left_corner',(-1,-1,2),2,(-1,2)),('left_mid',(-1,-1,1),1,(-1,1)),('apex',(0,-1,1),1,(0,1))]
for name,(c0,c1,den),t,(x,y) in events:
 assert F(t*c0,den)==x and 1+F(t*c1,den)==0 and t==y
proof=ROOT/'surplus-four-local/e2-e1-b1/north-return-maps.txt'
self=Path(__file__)
out={'status':'INDEPENDENT_DECLARED_NORTH_MAP_ALGEBRA_AND_TILING_PASS','fixed_isometries':expected,'eight_fixed_tiles':tiles,'eight_portals':portals,'singular_events':[x[0] for x in events],
 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [proof,self]},
 'limits':'Affine coefficient/tile checks only; hand review proves sector disjointness, branch inequalities, chronological words and exhaustion. No generic state samples, cap/room enumeration, word search, solver, peer checker execution or global optical closure.'}
(HERE/'north-map-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: seven declared isometries, eight fixed square tiles/half-edge portals, exact boundary expressions and six singular events; no state samples.')
