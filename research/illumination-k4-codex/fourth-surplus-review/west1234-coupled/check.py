"""One hand-derived West1234/Tc5 path. No room or discovery."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import sub,cross,dot,on
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(k,ss):
 a=C[k] if isinstance(k,str) else k
 return {tuple(sorted((a,tuple(a[j]+R[i%8][j] for j in (0,1)),tuple(a[j]+R[(i+1)%8][j] for j in (0,1))))) for i in ss}
def full(k):return fan(k,range(8))
H=set().union(*(full(p) for p in ((0,0),(2,0),(2,2))))
d=F(1,6)
P=[(F(0),F(0)),(2*d/(1+d),-2/(1+d)),(F(-1),3*d-2),(4*d/(1-d),(6*d-2)/(1-d)),(8*d/(1-d),2+8*d/(1-d)),(F(2),2+10*d),(12*d/(1+d),2+12*d/(1+d)),(F(2),F(2))]
assert P==[(F(0),F(0)),(F(2,7),F(-12,7)),(F(-1),F(-3,2)),(F(4,5),F(-6,5)),(F(8,5),F(18,5)),(F(2),F(11,3)),(F(12,7),F(26,7)),(F(2),F(2))]
minimum=H|fan('B',(1,2,3,4))|fan('Tc',(5,))
maximum=minimum|set().union(*(full(k) for k in ('L','D','R','E','N')))
U,Z=path_requirements(P)
assert U<=minimum,('missing',U-minimum)
assert not Z&maximum,('blocked',Z&maximum)
walls=[((0,-2),(1,-1)),((-1,-2),(-1,-1)),((0,-2),(1,-1)),((1,3),(2,4)),((2,3),(2,4)),((1,3),(2,4))]
for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
 assert on(p,c,e) and p not in (c,e)
 v=sub(p,a);w=sub(e,c)
 reflect=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert cross(reflect,sub(b,p))==0 and dot(reflect,sub(b,p))>0
assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
assert incident((F(1),F(0)))<=H and on((1,0),P[3],P[4])
assert F(1,7)<d<F(2,11)<F(1,5)
q=P[-1]
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert cross(q,(1,-6))==0
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
ur,zr=path_requirements(P[::-1]);assert (ur,zr)==(U,Z)
us,zs=path_requirements([sigma(p) for p in P[::-1]]);assert (us,zs)==(tr(U),tr(Z))
# Compare only the named accepted upper return, not a path/word lookup.
oldsource=ROOT/'fourth-surplus-review/mixed-e2-e1/joined-four-check.json'
old=json.loads(oldsource.read_text())
upper=[tuple(F(x) for x in p) for p in old['six_path_complement']['path']][4:]
assert P[4:]==upper
assert on((9*d,F(3)),P[3],P[4])
assert on((11*d,F(3)),P[-2],P[-1])
# All residual West/Tc5 supports: full L/D/R/E/N, no cap-direction selection.
for k in ('L','D','R','E','N'):assert full(k)<=maximum
assert fan('L',(7,0))<=maximum and fan('N',(7,))<=maximum
# Stronger bottom minimum B123 also suffices, though class root is B1234.
assert U<=H|fan('B',(1,2,3))|fan('Tc',(5,))
# Second hand prescription: negative bottom return, L70/R3-absent/L70/E4.
e=F(2,13)
P11=[(F(0),F(0)),(-2*e/(1-e),-2/(1-e)),(F(-1),-2-3*e),(-4*e/(1+e),-(2+6*e)/(1+e)),(-8*e/(1+e),2-8*e/(1+e)),(F(3),2-11*e),((14*e-4)/(1+e),(2-16*e)/(1+e)),((18*e-4)/(1-e),(16*e-2)/(1-e)),(18*e/(1-e),18*e/(1-e)-2),(22*e,F(2)),(26*e/(1+e),26*e/(1+e)-2),(F(1),25*e-2),(F(2),26*e-2)]
mi11=H|fan('B',(1,2,3,4))|fan('L',(7,0))|fan('E',(4,))
ma11=mi11|full('D')|fan('R',(0,1,2,4,5,6,7))|full('Tc')|fan('N',(0,1,2,3,4,5,6))
u11,z11=path_requirements(P11)
assert u11<=mi11,('missing11',u11-mi11)
assert not z11&ma11,('blocked11',z11&ma11)
w11=[((-1,-3),(0,-2)),((-1,-3),(-1,-2)),((-1,-3),(0,-2)),((-2,0),(-1,1)),((3,0),(3,1)),((-2,0),(-1,-1)),((-2,0),(-1,1)),((3,1),(4,2)),((3,2),(4,2)),((3,1),(4,2)),((1,1),(1,2))]
for a,p,b,(c,f) in zip(P11,P11[1:],P11[2:],w11):
 assert on(p,c,f) and p not in (c,f)
 v=sub(p,a);w=sub(f,c)
 reflect=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert cross(reflect,sub(b,p))==0 and dot(reflect,sub(b,p))>0
assert P11[0]==(0,0) and P11[-1]==(2,2)
assert all(not on((2,2),a,b) for a,b in zip(P11[:-2],P11[1:-1]))
a,b=path_requirements(P11[::-1]);assert (a,b)==(u11,z11)
a,b=path_requirements([sigma(p) for p in P11[::-1]]);assert (a,b)==(tr(u11),tr(z11))
q11=P11[-1]
for a,b in w11[::-1]:
 w=sub(b,a);v=sub(q11,a);q11=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert cross(q11,(-2,-13))==0
assert F(1,7)<e<F(3,19)
assert 0<1/e-6<1 and 0<2-7*e<1 and 0<2-11*e<1
assert -1<2-15*e<0 and 0<17*e-2<1 and 1<3/e-18<3
assert 1<21*e-2<23*e-2<25*e-2<2
assert fan('R',(4,))<=ma11 and fan('N',(0,6))<=ma11 and fan('Tc',(5,6))<=ma11

inputs=[Path(__file__),HERE/'argument.txt',oldsource,ROOT/'surplus-four-local/e2-e1-b1/critical-B.txt',ROOT/'fourth-surplus-review/mixed-e2-e1/joined-four.txt',ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']
out={'status':'PARENT_WEST1234_SIX_ELEVEN_SUPPORT_PASS','path':[[str(x) for x in p] for p in P],'reflections':6,'parameter':'1/6','strict_gate':['1/7','2/11'],'whole_support':{'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z)},'U_count':len(U),'Z_count':len(Z),'unfolded_actual_target':list(map(str,q)),'finite_mirrors_firstT_reverse_sigma':'PASS','inherited_upper_return':'Identical to accepted joined-six at d1/6, same portal (9d,3),(d,1).','limits':'One hand-derived actualST path/whole local envelope, no room/cap or ray/direction/word discovery. Entire WestTc5 residual parent closed<=6 pending independent review. Tc6 remains open; no global closure.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
out['eleven_path']={'path':[[str(x) for x in p] for p in P11],'reflections':11,'parameter':'2/13','strict_gate':['1/7','3/19'],'minimum':sorted(mi11),'maximum':sorted(ma11),'required':sorted(u11),'forbidden':sorted(z11),'unfolded_actual_target':list(map(str,q11)),'limits':'Full D/Tc, R3 absent and N7 absent; no whole West closure.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: West1234/Tc5 SIX; U',len(U),'Z',len(Z),'unfold',q,'finite mirrors/firstT/reverse/sigma; fullLDR EN supported.')
print('Forbidden:',sorted(Z))

print('PASS: coupled West/L70 ELEVEN; U',len(u11),'Z',len(z11),'unfold',q11,'R3/N7 absent, fullD/Tc allowed.')
