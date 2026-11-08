"""One prescribed hand-derived West/R4/D2 roof path; no discovery/room."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
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
d=F(2,13)
P=[(F(0),F(0)),(d,F(1)),(4*d/(1+d),(2*d-2)/(1+d)),(F(-1),5*d-2),((2+6*d)/(1-d),(2+6*d)/(1-d)-4),(2+10*d,F(0)),((2+14*d)/(1+d),(2+14*d)/(1+d)-4),((14*d-4)/(1+d),(14*d-4)/(1+d)+2),((18*d-4)/(1-d),-(16*d-2)/(1-d)),(F(2),2-20*d),((22*d-2)/(1+d),-(22*d-2)/(1+d)),(25*d-2,F(3)),(F(2),26*d-2)]
# Explicit geometric transcription provides a second formula consistency check.
assert P==[(F(0),F(0)),(F(2,13),F(1)),(F(8,15),F(-22,15)),(F(-1),F(-16,13)),(F(38,11),F(-6,11)),(F(46,13),F(0)),(F(18,5),F(-2,5)),(F(-8,5),F(2,5)),(F(-16,11),F(-6,11)),(F(2),F(-14,13)),(F(6,5),F(-6,5)),(F(24,13),F(3)),(F(2),F(2))]
minimum=H|fan('B',(1,2,3,4))|fan('L',(7,0))|fan('R',(4,))|fan('D',(2,))
maximum=minimum|full('E')|fan('N',(0,1,2,3,4,5,7))|fan('Tc',(0,1,2,3,4,6,7))|fan('D',(0,2,4,5,6,7))|fan('R',(0,1,2,4,6,7))
U,Z=path_requirements(P)
assert U<=minimum,('missing',U-minimum)
assert not Z&maximum,('blocked',Z&maximum)
walls=[((0,1),(1,1)),((0,-2),(1,-1)),((-1,-2),(-1,-1)),((3,-1),(4,0)),((3,0),(4,0)),((3,-1),(4,0)),((-2,0),(-1,1)),((-2,0),(-1,-1)),((2,-2),(2,-1)),((1,-1),(2,-2)),((1,3),(2,3))]
for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
 assert on(p,c,e) and p not in (c,e),(p,c,e)
 v=sub(p,a);w=sub(e,c)
 reflected=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert cross(reflected,sub(b,p))==0 and dot(reflected,sub(b,p))>0,(a,p,b)
assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
a,b=path_requirements(P[::-1]);assert (a,b)==(U,Z)
a,b=path_requirements([sigma(p) for p in P[::-1]]);assert (a,b)==(tr(U),tr(Z))
q=P[-1]
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert cross(q,(2,13))==0
assert F(3,20)<d<F(3,19)
assert 0<1/d-6<1 and -1<9*d-2<0 and 0<15*d-2<1
assert -1<2-17*d<0 and 1<3/d-18<2
assert -2<2-20*d<-1 and 1<(22*d-2)/(1+d)<2
assert 1<25*d-2<2 and 1<23*d-2<3
assert fan('N',(7,))<=maximum and fan('Tc',(6,))<=maximum
# Fixed support implication covers the named residual, no assembled room.
inputs=[Path(__file__),HERE/'roof-N7-hand.txt',ROOT/'surplus-four-local/e2-e1-b1/critical-B.txt',ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']
out={'status':'PARENT_WEST_R4_D2_ROOF_ELEVEN_PASS','path':[[str(x) for x in p] for p in P],'reflections':11,'parameter':'2/13','strict_gate':['3/20','3/19'],'whole_support':{'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z)},'U_count':len(U),'Z_count':len(Z),'actual_unfolded_target':list(map(str,q)),'finite_mirrors_firstT_reverse_sigma':'PASS','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'limits':'One prescribed analytic path, no room/discovery. Covers WestTc6/R4/N7/D2 and N0 as well, not N6. Remaining WestR3 separate. Parent awaiting independent hand review.'}
(HERE/'roof-N7-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: WestR4/D2 roof ELEVEN, U',len(U),'Z',len(Z),'unfold',q,'actualST finite mirrors/firstT/reverse/sigma.')
