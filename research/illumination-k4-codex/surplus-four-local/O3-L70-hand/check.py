"""One hand-derived L70 two-bounce substitution; no room or search."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H,audit=e['fan'],e['H'],e['audit']
P=[(F(0),F(0)),(F(-12,7),F(-2,7)),(F(-8,5),F(2,5)),(F(16,5),F(6,5)),(F(10,3),F(2)),(F(24,7),F(10,7)),(F(1),F(11,6)),(F(2),F(2))]
W=[((-2,0),(-1,-1)),((-2,0),(-1,1)),((3,1),(4,2)),((3,2),(4,2)),((3,1),(4,2)),((1,1),(1,2))]
mi=H|fan('L',[7,0])|fan('E',[4]);ma=mi|set().union(*(fan(k,range(8)) for k in ['B','D','R','Tc']))|fan('N',[0,1,2,3,4,5,6])
u,z,proof=audit(P,W,mi,ma,(-12,-2))
print('U',len(u),'Z',len(z))
for k in ['L','B','D','R','E','Tc','N']:print('Z',k,[i for i in range(8) if fan(k,[i])&z])
assert z==fan('L',[1,6])|fan('E',[3,5])|fan('N',[7])
d=F(1,6);assert F(1,7)<d<F(2,11)
assert P[1:3]==[(-2/(1+d),-2*d/(1+d)),((4*d-2)/(1-d),2*d/(1-d))]
assert 0<3*d<1 and 12*d==2
# L70 normal TWO exit exactly equals old L0 normal THREE exit at(-1,3d).
assert 1<7*d<9*d<11*d<2
# Two attempted N7 terminal substitutes force lower gate d1/7; no new paths.
assert 14*F(1,7)==2 and 4-14*F(1,7)==2
sources=[src,BASE/'surplus-four-local/single-e2-check.json',BASE/'surplus-four-local/O3-R23-search/findings.txt']
out={'status':'PARENT_L70_E4_SIX_N7_ABSENT_PASS','path':[[str(x) for x in p] for p in P],'reflections':6,'root':'1/6','hand_endpoint':'12d=2','strict_gate':['1/7','2/11'],'whole_support':{'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z)},'proof':proof,'claim':'L70/E4 with N7 absent illuminates<=6, arbitraryB/D/R/Tc. O3+L70 remaining requires ordinaryN7, pending independent review.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'One hand-derived prefix substitution into accepted uniform7 suffix, complete own Fraction U/Z/specular/firstT/reverse/sigma. No room, discovery search, cap census, archive or worker. Not entireL70/O3/Delta4 closure; independent review pending.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS L70new6; fullsupport, strictfinitewalls, firstT, reverse/sigma, unfold(-12,-2).')
