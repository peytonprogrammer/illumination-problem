"""Independent fixed-path West review using own standalone Fraction engine.
No peer execution, room construction or discovery/search.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
peer=BASE/'fourth-surplus-review/west1234-coupled'
engine_source=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(engine_source.resolve())}
exec(compile(engine_source.read_text().split('\ndef path(d,nine):')[0],str(engine_source),'exec'),e)
fan,H,audit=e['fan'],e['H'],e['audit']
P6=[(F(0),F(0)),(F(2,7),F(-12,7)),(F(-1),F(-3,2)),(F(4,5),F(-6,5)),(F(8,5),F(18,5)),(F(2),F(11,3)),(F(12,7),F(26,7)),(F(2),F(2))]
P11=[(F(0),F(0)),(F(-4,11),F(-26,11)),(F(-1),F(-32,13)),(F(-8,15),F(-38,15)),(F(-16,15),F(14,15)),(F(3),F(4,13)),(F(-8,5),F(-2,5)),(F(-16,11),F(6,11)),(F(36,11),F(14,11)),(F(44,13),F(2)),(F(52,15),F(22,15)),(F(1),F(24,13)),(F(2),F(2))]
diag=((-1,-3),(1,-1));west=((-1,-3),(-1,-1));roof=((1,3),(2,4));lowerL=((-2,0),(-1,-1));upperL=((-2,0),(-1,1));Ediag=((3,1),(4,2))
W6=[diag,west,diag,roof,((2,3),(2,4)),roof]
W11=[diag,west,diag,upperL,((3,0),(3,1)),lowerL,upperL,Ediag,((3,2),(4,2)),Ediag,((1,1),(1,2))]
B=fan('B',[1,2,3,4]);mi6=H|B|fan('Tc',[5]);ma6=mi6|set().union(*(fan(k,range(8)) for k in ['L','D','R','E','N']))
mi11=H|B|fan('L',[7,0])|fan('E',[4]);ma11=mi11|fan('D',range(8))|fan('Tc',range(8))|fan('R',[0,1,2,4,5,6,7])|fan('N',[0,1,2,3,4,5,6])
u6,z6,c6=audit(P6,W6,mi6,ma6,(2,-12));u11,z11,c11=audit(P11,W11,mi11,ma11,(-4,-26))
assert (len(u6),len(z6),len(u11),len(z11))==(14,4,23,8)
assert z6==fan('B',[0])|fan((-2,-2),[0])|fan('Tc',[4,6])
assert z11==fan('B',[5])|fan((-2,-2),[7])|fan('L',[1,6])|fan('R',[3])|fan('E',[3,5])|fan('N',[7])
parent=json.loads((peer/'check.json').read_text());el=parent['eleven_path']
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
for own,foreign in [(u6,parent['whole_support']['required']),(z6,parent['whole_support']['forbidden']),(u11,el['required']),(z11,el['forbidden'])]:assert own==decode(foreign)
assert mi6==decode(parent['whole_support']['minimum']) and ma6==decode(parent['whole_support']['maximum'])
assert mi11==decode(el['minimum']) and ma11==decode(el['maximum'])
hashes={k:hashlib.sha256((BASE/k).read_bytes()).hexdigest()==v for k,v in parent['source_sha256'].items()};assert all(hashes.values())
# Exact hand contact formulas/root gates; no parameter or word enumeration.
d=F(1,6);assert F(1,7)<d<F(2,11)<F(1,5)
assert P6[1:4]==[(2*d/(1+d),-2/(1+d)),(F(-1),3*d-2),(4*d/(1-d),(6*d-2)/(1-d))]
assert P6[4:7]==[(8*d/(1-d),2+8*d/(1-d)),(F(2),2+10*d),(12*d/(1+d),2+12*d/(1+d))] and 12*d==2
d=F(2,13);assert F(1,7)<d<F(3,19)
assert P11[1:4]==[(-2*d/(1-d),-2/(1-d)),(F(-1),-2-3*d),(-4*d/(1+d),-(2+6*d)/(1+d))]
assert 0<1/d-6<1
assert P11[4]==(-8*d/(1+d),2-8*d/(1+d))
assert P11[5]==(F(3),2-11*d) and 0<2-11*d<1
assert -1<2-15*d<0
assert P11[6:8]==[((14*d-4)/(1+d),(2-16*d)/(1+d)),((18*d-4)/(1-d),(16*d-2)/(1-d))]
assert 0<17*d-2<1 and 1<3/d-18<3
assert P11[8:11]==[(18*d/(1-d),18*d/(1-d)-2),(22*d,F(2)),(26*d/(1+d),26*d/(1+d)-2)]
assert 1<21*d-2<23*d-2<25*d-2<2 and 26*d-2==2
# Precise symbolic frontier subtraction. No room-completion census.
# After six: Tc6 only. Eleven: R3 absent means ordinaryR4;
# N7 absent leaves N0/6, and b1 forbids D1R4, soD2 forced.
assert fan('R',[4])<=ma11 and fan('N',[0,6])<=ma11
assert fan('D',[1,2])<=ma11 and fan('Tc',[6])<=ma11
assert z11&fan('R',[3]) and z11&fan('N',[7])
sources=[peer/'argument.txt',peer/'coverage.txt',peer/'check.py',peer/'check.json',engine_source,BASE/'surplus-four-local/e2-e1-b1/critical-B.txt']
out={'status':'INDEPENDENT_WEST_SIX_ELEVEN_ACCEPT','six':c6,'eleven':c11,'support_counts':{'six':[14,4],'eleven':[23,8]},'parent_pinned_hashes':hashes,'remote_restriction':'West vertical mates remote(-2,-2) sectors0/7 absent only in localK','frontier':'Tc6,R3,N0/6/7,D1or2; orTc6,R4,N7,D2. Necessary descriptions, not roomcounts.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'Own standalone Fraction support/specular/firstT/reverse/sigma engine; no peer code executed, no room or search. Inherited West classification/budget and earlier covers. No fullWest/Delta4 closure.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('ACCEPT: West6/11 full14U4Z/23U8Z, strictfinitewalls/firstT/reverse/sigma, distinctLvisits and roots; localK remote restriction and exact frontier subtraction.')
