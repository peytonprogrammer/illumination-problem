from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
src=ROOT/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)};exec(src.read_text().split('\ndef path(d,nine):')[0],e)
globals().update({k:v for k,v in e.items()if not k.startswith('__')});HERE=Path(__file__).resolve().parent
P=[(F(0),F(0)),(F(3),F(3,4)),(F(2,3),F(4,3)),(F(2,5),F(12,5)),(F(2),F(2))]
walls=[((3,0),(3,1)),((0,2),(1,1)),((0,2),(1,3))]
minimum=H|fan('N',[7,0]);U,Z,_=constraints(P,walls)
maximum=(H|set().union(*(fan(k,range(8))for k in C))|fan((-2,-2),range(8)))-Z
u,z,proof=audit(P,walls,minimum,maximum,(8,2));assert Z==fan('R',[3])|fan('N',[1,6])
assert all(not on((0,0),a,b)for a,b in zip(P[1:],P[2:]))
d=F(1,4);a=(2-6*d)/(1-d);b=(2-6*d)/(1+d)
assert F(1,5)<d<F(2,7) and P==[(F(0),F(0)),(3,3*d),(a,2-a),(b,b+2),(F(2),4-8*d)]
assert not (U|Z)&set().union(*(fan(k,range(8))for k in ['L','B','D','E','Tc']))
# Oldnormalcaproofreturn reflectsitsremaining suffix across horizontaly2;
# T liesonthisaxis andisfixed. CompleteN70 replacesroofwithupperdiagonal.
old=[(F(0),F(0)),(F(3),F(3,4)),(F(2,3),F(4,3)),(F(1,2),F(2)),(F(2,5),F(8,5)),(F(2),F(2))]
assert P[:3]==old[:3] and P[3:]==[(x,4-y)for x,y in old[4:]]
reads=[src,Path(__file__),ROOT/'surplus-four-local/source-suffix-four-review/review.txt']
(HERE/'check.json').write_text(json.dumps({'status':'PARENT_N70_CENTER_THREE_PASS','path':[[str(v)for v in p]for p in P],'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(minimum),'maximum':sorted(maximum),'proof':proof,'root':'1/4','strict_gate':['1/5','2/7'],'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in reads},'limits':'HandfixedTHREE andexactfullguard; independentreviewpending. No discovery/newpolygon/archive.'},indent=2,default=str)+'\n')
print('PASS3',len(U),'U',len(Z),'Z R3,N1,N6; entireL/B/D/E/Tc/remote safe')
