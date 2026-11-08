"""Exact endpoint/gate identities for TWO hand-prescribed reverse routes.
No geometry engine, ray/word/direction generation, samples, room or search.
Laurent polynomials encode the already-derived affine/reciprocal states.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
# Tiny exact Laurent polynomial arithmetic; no equation solver.
def add(*terms):
 out={}
 for term in terms:
  for k,v in term.items():out[k]=out.get(k,F(0))+v
 return {k:v for k,v in out.items() if v}
def scale(term,f):return {k:v*f for k,v in term.items() if v*f}
def shift(term,p):return {k+p:v for k,v in term.items()}
def const(n):return {0:F(n)} if n else {}
def evaluate(term,d):return sum(v*d**k for k,v in term.items())
d={1:F(1)}
# T=(2,2), velocity(1,-d); E4 normal triple returns atx3,y2-3d.
Eexit=add(const(2),scale(d,-3))
Lentry=add(Eexit,scale(d,-4));assert Lentry=={0:F(2),1:F(-7)}
# BranchA: L0 THREE returns with same tangential sign.
Lthree=add(Lentry,scale(d,-2));assert Lthree=={0:F(2),1:F(-9)}
rightwall=add(Lthree,scale(d,-4));assert rightwall=={0:F(2),1:F(-13)}
floorx=add(const(3),scale(shift(add(rightwall,const(1)),-1),-1))
assert floorx=={0:F(16),-1:F(-3)}
endpointA=add(const(-1),shift(floorx,1));assert endpointA=={0:F(-4),1:F(16)}
rootA=F(1,4);gateA=(F(1,5),F(2,9))
assert evaluate(endpointA,rootA)==0 and not gateA[0]<rootA<gateA[1]
# This root satisfies the L0 apex singular slope a=-u.
assert evaluate(Lentry,rootA)==rootA
# BranchB: L0 FOUR flips tangential sign.
Lfour=add(scale(Lentry,-1),scale(d,2));assert Lfour=={0:F(-2),1:F(9)}
Rentry=add(Lfour,scale(d,4));assert Rentry=={0:F(-2),1:F(13)}
Rtopx=add(const(3),shift(add(const(1),scale(Rentry,-1)),-1))
assert Rtopx=={0:F(-10),-1:F(3)}
Rfar=add(const(1),scale(shift(add(const(4),scale(Rtopx,-1)),1),-1))
assert Rfar=={0:F(4),1:F(-14)}
Rexit=add(Rfar,scale(d,-1));assert Rexit=={0:F(4),1:F(-15)}
endpointB=add(Rexit,scale(d,-3));assert endpointB=={0:F(4),1:F(-18)}
rootB=F(2,9);gateB=(F(2,9),F(3,13))
assert evaluate(endpointB,rootB)==0 and rootB==gateB[0]
assert evaluate(Lfour,rootB)==0
# Check only actual corner angle at the TWO decisive points, locally.
rays=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,ss):return {tuple(sorted((a,(a[0]+rays[i][0],a[1]+rays[i][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
def angle(tiles,p):
 total=0
 for t in tiles:
  if p in t:
   a,b=[(q[0]-p[0],q[1]-p[1]) for q in t if q!=p];total+=90 if a[0]*b[0]+a[1]*b[1]==0 else 45
 return total
local=fan((0,0),range(8))|fan((-2,0),[0])
assert angle(local,(-2,0))==45
assert angle(local,(-1,0))==270
# None of the other fixed cells can heal either corner. Checked cellwise,
# not by building a new completed room or testing its geometry.
for a,ss in [((0,-2),[7,0,1,2]),((4,0),[2,3]),((4,2),[4]),((0,2),[7]),((2,4),[6]),((2,0),range(8)),((2,2),range(8))]:
 for p in [(-2,0),(-1,0)]:assert angle(fan(a,ss),p)==0
source=HERE/'joined-top-absent.txt'
result={'status':'TWO_PRESCRIPTIONS_REJECTED_BY_HAND_GATE_IDENTITIES','family':'conditional H+B7012+R23+L0+E4+N7+Tc6,Dempty','A':{'prefix':'T->E4normal3->L0normal3->Urightbelow0->bareUfloor->xS0','endpoint_equation':'16d-4=0','root':str(rootA),'strict_gate':list(map(str,gateA)),'decisive_corner':[-2,0],'corner_degrees':45},'B':{'prefix':'T->E4normal3->L0four->R23upperwall+farwall->xS0','endpoint_equation':'4-18d=0','root':str(rootB),'strict_gate':list(map(str,gateB)),'decisive_corner':[-1,0],'corner_degrees':270},'limits':'Only exact identities for two prespecified hand transports and endpoint/branch contradiction. No complete optical replay or full U/Z certificate, no new room or validity assertion, no discovery/trajectory/word search. This does not show the family dark or exhaust possible paths.','source_sha256':{source.name:hashlib.sha256(source.read_bytes()).hexdigest()},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'R23-top6-algebra.json').write_text(json.dumps(result,indent=2)+'\n')
print('REJECTED A: root1/4 outside(1/5,2/9), L0apex45corner. REJECTED B: root2/9 at strict lowergate, L0portal270corner. No new optical cover.')
