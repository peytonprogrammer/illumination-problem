"""Own Fraction review of a supplied four-contact suffix; no peer execution."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];peer=BASE/'fourth-surplus-review/peer-O3-complete-independent'
j=json.loads((peer/'check.json').read_text())
assert j['status']=='INDEPENDENT_O3_COMPLETE_AND_CRITICAL_L_TWO_TRANSFER_PASS'
for rel,h in j['source_sha256'].items():assert hashlib.sha256((BASE/rel).read_bytes()).hexdigest()==h,rel
P=[(F(0),F(0)),(F(3),F(3,4)),(F(2,3),F(4,3)),(F(1,2),F(2)),(F(2,5),F(8,5)),(F(2),F(2))]
W=[((3,0),(3,1)),((0,2),(1,1)),((0,2),(1,2)),((0,2),(1,1))]
mi=H|fan('N',[7]);ma=mi|set().union(*(fan(k,range(8)) for k in ['L','B','D','E','Tc']))|fan('R',[0,1,2,4,5,6,7])|fan('N',[1,2,3,4,5])
U,Z,proof=e['audit'](P,W,mi,ma,(8,2));assert len(U)==9 and Z==fan('R',[3])|fan('N',[0,6])
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
d=F(1,4);assert F(1,5)<d<F(2,7) and 8*d==2
# Bare right reflection; triangle7 lower diagonal, horizontal upper, lower.
a=(2-6*d)/(1-d);b=(1-d)*a;c=b/(1+d)
assert P==[(F(0),F(0)),(F(3),3*d),(a,2-a),(b,F(2)),(c,2-c),(F(2),8*d)]
assert 0<3*d<1 and 1<5*d<7*d<2 and 0<a<1 and 0<b<1 and 0<c<1
# Literal suffix of the original legal eleven after a last source revisit.
old=json.loads((BASE/'surplus-four-local/L70-N7-search/verification.json').read_text())
P11=[tuple(F(x) for x in p) for p in old['eleven']['path']]
assert e['on']((0,0),P11[7],P11[8]) and P[1:]==P11[8:]
# O3 N7/R3abs ordinary support fits, including arbitrary bottom/L/E/Tc.
assert mi|fan('B',[7,0,1])|fan('L',[7,0])|fan('R',[4])<=ma
# Conditional mixed singleleaf Eouter residual upper, including BOTH D leaves.
upper=H|fan('B',[6,7,0,1,2])|fan('E',[4,5])|fan('N',[7])|set().union(*(fan(k,range(8)) for k in ['L','D','Tc']))
assert mi<=upper<=ma and not Z&upper
# Negative controls preserve the three restrictions explicitly.
for t in Z:
 try:e['audit'](P,W,mi,ma|{t},(8,2))
 except AssertionError:pass
 else:raise AssertionError('missed blocker')
sources=[src,peer/'check.py',peer/'check.json',peer/'review.txt',peer/'coverage.txt',BASE/'surplus-four-local/L70-N7-search/verification.json',BASE/'fourth-surplus-review/peer-L70-six-independent/review.txt']
out={'status':'INDEPENDENT_SOURCE_SUFFIX_FOUR_AND_O3_BOUND_NINE_ACCEPT','path':[[str(x) for x in p] for p in P],'proof':proof,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'root':'1/4','strict_gate':['1/5','2/7'],'literal_eleven_suffix':'PASS','O3_consequence':'New4 ordinaryN7/R3abs; already accepted6 N7abs and9 N7R3present; otherO3 partners<=6. Whole local O3 TWOroot b1<=9 accepted.','mixed_consequence':'Conditional support implication for Eouter O3/O4 N7 Rempty residual with eitherD leaf accepted; upstream mixed root/leaf classification not independently re-audited.','peer_hashes_verified':len(j['source_sha256']),'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Own Fraction arithmetic and fixed supplied suffix only. No peer execution, room or discovery. Independent AI review, not formal/expert verification.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('ACCEPT: source-suffix4, 9U3Z; whole O3<=9; conditional mixed residual support only;',len(j['source_sha256']),'peer hashes current.')
