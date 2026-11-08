"""One prescribed lower-L-square replacement, exact fixed root only."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
d=F(4,11)
P=[(F(0),F(0)),(2/(1-d),2*d/(1-d)),((2+8*d)/(1+d),6-(2+8*d)/(1+d)),(F(1),4-7*d),(F(3),4-9*d),(12-5/d,F(-1)),(F(-2),14*d-6),(F(3),19*d-6),(F(1),21*d-6),(F(2),22*d-6)]
W=[((3,1),(4,2)),((3,3),(4,2)),((1,1),(1,2)),((3,0),(3,1)),((-2,-1),(0,-1)),((-2,-1),(-2,0)),((3,0),(3,1)),((1,1),(1,2))]
U,Z,ev=e['constraints'](P,W)
print('P',P);print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H|fan('L',[6,7])|fan('E',[3,4])
ma=mi|fan('L',[0,1,2,3,4])|fan('B',range(8))|fan('D',range(8))|fan('R',[0,1,2,4,5,6,7])|fan('Tc',range(8))|fan('N',[0,1,2,3,4,5,6])
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
print('MISSING U',U-mi,'BAD Z',Z&ma,'IMAGE',q)
u,z,proof=e['audit'](P,W,mi,ma,q)
low=H|fan('L',[6,7,0,1])|fan('E',[3,4])|fan('B',[1])|fan('Tc',[5])|fan('N',[5])|fan('D',[2])|fan('R',[4])
assert U<=low<=ma and not Z&low
assert Z==fan('L',[5])|fan('E',[2,5])|fan('R',[3])|fan('N',[7])|fan((-2,-2),[1])
assert F(5,14)<d<F(7,19) and 22*d-6==2 and q==(22,8)
assert 3<P[1][0]<4 and 1<P[1][1]<2 and 3<P[2][0]<4 and 2<P[2][1]<3
assert 1<4-7*d<2 and 0<4-9*d<1 and -2<12-5/d<-1
assert -1<14*d-6<0 and -1<15*d-6<0 and 0<19*d-6<1 and 1<21*d-6<2
negative=[]
for t in Z:
 try:e['audit'](P,W,mi,ma|{t},q)
 except AssertionError:negative.append(t)
 else:raise AssertionError('missed blocker')
assert len(negative)==6
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
out={'status':'PARENT_LLOWER_SQUARE_ECENTER_EIGHT_AND_INWARD_TRANSFER_PASS','path':[[str(x) for x in p] for p in P],'walls':W,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'application':sorted(low),'proof':proof,'root':str(d),'endpoint_equation':'22d-6=2','strict_gate':['5/14','7/19'],'image':list(map(str,q)),'negative_controls':len(negative),'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,BASE/'surplus-four-local/L670-B12-D1-search/findings.txt',BASE/'surplus-four-local/L670-B12-D1-search/verification.json',BASE/'surplus-four-local/e2-e1-b1/critical-L.txt']},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE hand-prescribed fixed path/root, no completed room/search/parameter scan/worker. Remote lower-floor mate absent by local K scope. Parent result pending independent hand review.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS')
