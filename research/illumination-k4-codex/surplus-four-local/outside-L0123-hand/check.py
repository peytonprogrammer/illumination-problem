"""REJECTED: open leg crosses true270 corner(1,1); intentionally fails."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
d=F(1,7)
# From L exit(-1,5d), E4 entry(3,9d); same normal-three triangle identity.
a=(2+6*d)/(1-d);b=2+10*d;c=(2+14*d)/(1+d)
P=[(F(0),F(0)),(F(-3),3*d),(a,a-2),(b,F(2)),(c,c-2),(F(1),13*d),(F(2),14*d)]
W=[((-3,0),(-3,1)),((3,1),(4,2)),((3,2),(4,2)),((3,1),(4,2)),((1,1),(1,2))]
U,Z,_=e['constraints'](P,W)
print('PATH',P,'COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H|fan('L',[0,1,2,3])|fan('E',[4]);ma=mi|fan('L',[4,5,6,7])|fan('E',[0,1,2,6,7])|fan('N',[0,1,2,3,4,5,6])|set().union(*(fan(k,range(8)) for k in ['B','D','R','Tc']))
q=P[-1]
for aa,bb in W[::-1]:
 v=e['reflect'](e['sub'](q,aa),aa,bb);q=tuple(aa[k]+v[k] for k in (0,1))
print('BAD',Z&ma,'MISSING',U-mi,'IMAGE',q)
u,z,proof=e['audit'](P,W,mi,ma,q)
assert all(not e['on']((0,0),aa,bb) for aa,bb in zip(P[1:],P[2:]))
ordinary=fan('B',[1])|fan('Tc',[5])|fan('N',[5])
lowD=mi|ordinary|fan('D',[1,2]);lowR=mi|ordinary|fan('R',[3,4]);lowN=mi|fan('B',[1])|fan('Tc',[5])|fan('N',[4,5])
assert all(U<=low<=ma for low in [lowD,lowR,lowN])
out={'status':'PARENT_OUTSIDE_L0123_FIVE_PASS_HAND_GATES_PENDING','path':[[str(x) for x in p] for p in P],'walls':W,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'proof':proof,'image':list(map(str,q)),'applications':{'D12':sorted(lowD),'R34':sorted(lowR),'N45':sorted(lowN)}}
(HERE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS THREE REMAINING ROWS')
