"""Independent supplied West R4 roof path; own helper-free exact engine."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
peer=BASE/'fourth-surplus-review/west1234-coupled'
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H,audit=e['fan'],e['H'],e['audit']
P=[(F(0),F(0)),(F(2,13),F(1)),(F(8,15),F(-22,15)),(F(-1),F(-16,13)),(F(38,11),F(-6,11)),(F(46,13),F(0)),(F(18,5),F(-2,5)),(F(-8,5),F(2,5)),(F(-16,11),F(-6,11)),(F(2),F(-14,13)),(F(6,5),F(-6,5)),(F(24,13),F(3)),(F(2),F(2))]
W=[((0,1),(1,1)),((-1,-3),(1,-1)),((-1,-3),(-1,-1)),((3,-1),(4,0)),((3,0),(4,0)),((3,-1),(4,0)),((-2,0),(-1,1)),((-2,0),(-1,-1)),((2,-2),(2,-1)),((1,-1),(2,-2)),((1,3),(2,3))]
mi=H|fan('B',[1,2,3,4])|fan('L',[7,0])|fan('R',[4])|fan('D',[2])
ma=mi|fan('E',range(8))|fan('N',[0,1,2,3,4,5,7])|fan('Tc',[0,1,2,3,4,6,7])|fan('D',[0,2,4,5,6,7])|fan('R',[0,1,2,4,6,7])
u,z,proof=audit(P,W,mi,ma,(4,26))
assert (len(u),len(z))==(25,10)
assert z==fan((-2,-2),[0])|fan('L',[1,6])|fan('B',[0])|fan('N',[6])|fan('D',[1,3])|fan('Tc',[5])|fan('R',[3,5])
j=json.loads((peer/'roof-N7-check.json').read_text());print('PARENTKEYS',list(j))
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
whole=j.get('whole_support',j)
assert decode(whole['required'])==u and decode(whole['forbidden'])==z
assert decode(whole['minimum'])==mi and decode(whole['maximum'])==ma
h={k:hashlib.sha256((BASE/k).read_bytes()).hexdigest()==v for k,v in j['source_sha256'].items()};assert all(h.values())
d=F(2,13);assert F(3,20)<d<F(3,19)
assert P[1:4]==[(d,F(1)),(4*d/(1+d),(2*d-2)/(1+d)),(F(-1),5*d-2)]
assert 0<1/d-6<1 and -1<9*d-2<11*d-2<0
assert P[4:7]==[((2+6*d)/(1-d),(2+6*d)/(1-d)-4),(2+10*d,F(0)),((2+14*d)/(1+d),(2+14*d)/(1+d)-4)]
assert 0<15*d-2<1
assert P[7:9]==[((14*d-4)/(1+d),(16*d-2)/(1+d)),((18*d-4)/(1-d),-(16*d-2)/(1-d))]
assert 1<3/d-18<2 and -1<2-17*d<0
portal=(3/d-18,F(-1));assert e['incident'](portal)<=mi
assert P[9:11]==[(F(2),2-20*d),((22*d-2)/(1+d),-(22*d-2)/(1+d))]
assert -2<2-20*d<-1 and 1<(22*d-2)/(1+d)<2
assert 1<23*d-2<25*d-2<2 and 26*d-2==2
# Tc6,N7 may be added; forbidden roof half is exactly Tc5.
assert fan('Tc',[6])<=ma and fan('N',[7])<=ma
sources=[peer/'roof-N7-hand.txt',peer/'roof-N7-check.py',peer/'roof-N7-check.json',src,BASE/'surplus-four-local/e2-e1-b1/critical-B.txt']
out={'status':'INDEPENDENT_WEST_R4_ROOF_ELEVEN_ACCEPT','proof':proof,'required_count':len(u),'forbidden_count':len(z),'parent_pinned_hashes':h,'portal':'y=-1,x3/d-18 strictly1..2; completeincident support in H+D2','whole_R4_join':'Prior acceptedWest6/11 plusnewroof11 => allremaining ordinaryR4 cases<=11, underacceptedWesttwo-rootb1 class.','remaining':'With acceptedL70six transfer, onlyWestTc6/R3/N7/D1or2 remains.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'Own standalone Fraction finitewall/support/firstT/reverse/sigma review; nopeerexecution/newroom/search/worker. RemoteWestmate absentonlyunderlocalK. NoentireWest/Delta4claim.'}
(HERE/'roof-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('ACCEPT: WestR4roof11 strictfinitewalls/full25U10Z/D2transparentportal/Tc6-safe roof/firstT/reverse/sigma/unfold4,26.')
