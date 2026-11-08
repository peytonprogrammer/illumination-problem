from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
src=ROOT/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)};exec(src.read_text().split('\ndef path(d,nine):')[0],e)
globals().update({k:v for k,v in e.items()if not k.startswith('__')});HERE=Path(__file__).resolve().parent
P=[(F(0),F(0)),(F(1,4),F(1)),(F(4,5),F(-6,5)),(F(-1),F(-3,4)),(F(4),F(1,2)),(F(2,3),F(4,3)),(F(1,2),F(2)),(F(2,5),F(8,5)),(F(2),F(2))]
walls=[((0,1),(1,1)),((0,-2),(1,-1)),((-1,-1),(-1,0)),((4,0),(4,1)),((0,2),(1,1)),((0,2),(1,2)),((0,2),(1,1))]
minimum=H|fan('B',[1,2])|fan('R',[2,3])|fan('N',[7]);U,Z,_=constraints(P,walls)
maximum=(H|set().union(*(fan(k,range(8))for k in C))|fan((-2,-2),range(8)))-Z
u,z,proof=audit(P,walls,minimum,maximum,(4,16));assert len(U)==len(u) and len(Z)==len(z)
assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
d=F(1,4);assert F(3,13)<d<F(4,15);assert 9*d-2<10*d-2<11*d-2 and 0<9*d-2 and 11*d-2<1
assert P[4]==(4,10*d-2) and 16*d-2==2
# Othercontacts/endpoint fromacceptedNINE'ssameprefixandsuffix.
old=json.loads((ROOT/'fourth-surplus-review/remote2101-B-upper/check.json').read_text());g=next(iter(old['fixed_paths'].values()));oldP=[tuple(F(v)for v in p)for p in g['path']]
assert P[:4]==oldP[:4] and P[5:]==oldP[7:]
labels=[k+str(i)for k in C for i in range(8)if Z&fan(k,[i])]
assert not Z&fan((-2,-2),range(8))
reads=[src,Path(__file__),ROOT/'fourth-surplus-review/remote2101-B-upper/check.json',ROOT/'surplus-four-remote2110/peer-optical-review/review.txt']
(HERE/'check.json').write_text(json.dumps({'status':'PARENT_R23_NORMAL_SQUARE_SEVEN_PASS','path':[[str(v)for v in p]for p in P],'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(minimum),'maximum':sorted(maximum),'proof':proof,'labels':labels,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in reads},'limits':'Fixedhandnormal-square substitution, completeguardandfinitepath; independentreviewpending. No newroom/discovery.'},indent=2,default=str)+'\n')
print('PASS7',len(U),'U',len(Z),'Z',labels)
