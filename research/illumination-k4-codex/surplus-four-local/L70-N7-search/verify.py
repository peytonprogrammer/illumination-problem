"""Own exact verification: stopped eleven plus hand companion nine.
No search/new room; only the frozen authorized room physically replayed.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H,audit=e['fan'],e['H'],e['audit']
P11=[(F(0),F(0)),(F(-1,4),F(-1)),(F(-3,4),F(1)),(F(-6,5),F(-4,5)),(F(3),F(1,4)),(F(0),F(1)),(F(-4,3),F(2,3)),(F(-8,5),F(-2,5)),(F(3),F(3,4)),(F(2,3),F(4,3)),(F(1,2),F(2)),(F(2,5),F(8,5)),(F(2),F(2))]
P9=P11[:4]+[(F(18,5),F(2,5)),(F(7,2),F(0)),(F(10,3),F(2,3))]+P11[9:]
SL=((-1,-1),(0,-1));SC=((-1,1),(1,1));LL=((-2,0),(-1,-1));LU=((-2,0),(-1,1));UR=((3,0),(3,1));ND=((0,2),(1,1));NT=((0,2),(1,2));RD=((3,1),(4,0));RF=((3,0),(4,0))
W11=[SL,SC,LL,UR,SC,LU,LL,UR,ND,NT,ND]
W9=[SL,SC,LL,RD,RF,RD,ND,NT,ND]
mi11=H|fan('L',[7,0])|fan('N',[7]);ma11=mi11|fan('B',[0,1,3,4,5,6,7])|fan('D',range(8))|fan('E',range(8))|fan('Tc',range(8))|fan('R',[0,1,2,4,5,6,7])|fan('N',[1,2,3,4])
mi9=mi11|fan('R',[3]);ma9=mi9|fan('B',[0,1,3,4,5,6,7])|fan('D',range(8))|fan('E',range(8))|fan('Tc',range(8))|fan('R',[0,1,5,6,7])|fan('L',[1,2,3,4,5])|fan('N',[1,2,3,4])
def run(P,W,mi,ma):
 q=P[-1]
 for a,b in W[::-1]:
  v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
 u,z,p=audit(P,W,mi,ma,q)
 return {'path':[[str(x) for x in pt] for pt in P],'reflections':len(W),'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z),'proof':p,'image':list(map(str,q))},u,z
r11,u11,z11=run(P11,W11,mi11,ma11);r9,u9,z9=run(P9,W9,mi9,ma9)
print('COUNTS11',len(u11),len(z11),'9',len(u9),len(z9));print('IMAGES',r11['image'],r9['image'])
for label,z in [('11',z11),('9',z9)]:
 for k in ['L','B','D','R','E','Tc','N']:print(label,'Z',k,[i for i in range(8) if fan(k,[i])&z])
assert z11==fan('L',[1,6])|fan('B',[2])|fan('R',[3])|fan('N',[0,5,6])
assert z9==fan('L',[6])|fan('B',[2])|fan('R',[2,4])|fan('N',[0,5,6])
raw=json.loads((HERE/'room.json').read_text());found=json.loads((HERE/'result.json').read_text())
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
assert hashlib.sha256((HERE/'room.json').read_bytes()).hexdigest()==found['room_sha256']
assert hashlib.sha256((HERE/'search.py').read_bytes()).hexdigest()==found['search_source_sha256']
assert P11==[tuple(F(*x) for x in p) for p in found['candidate']['path']]
assert found['candidate']['initial_direction']==[-1,-4] and found['candidate']['reflections']==11
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};V=e['boundary'](room)
assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P11,V);e['physical'](P11[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P11[::-1]],[sigma(p) for p in V])
assert mi11<=room<=ma11
# At (0,1) the searched path reflects inside a straight maximal source ceiling.
assert (0,1) not in V
cw=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if e['on']((0,1),a,b)]
assert len(cw)==1 and set(cw[0])=={(-1,1),(1,1)}
# Hand transport at exact common root. No direction/parameter enumeration.
d=F(1,4);assert F(5,21)<d<F(6,23) and F(3,13)<d<F(4,15)
assert P11[1:4]==[(-d,F(-1)),(-3*d,F(1)),(-6*d/(1+d),(4*d-2)/(1+d))]
assert P11[4]==(F(3),9*d-2) and P11[5]==(12-3/d,F(1))
assert P11[6:8]==[((2-12*d)/(1-d),(4-14*d)/(1-d)),((2-16*d)/(1+d),(14*d-4)/(1+d))]
assert P11[8]==(F(3),19*d-4) and 24*d-4==2
assert P9[4:7]==[(6*(1-d)/(1+d),4-6*(1-d)/(1+d)),(6-10*d,F(0)),((6-14*d)/(1-d),(10*d-2)/(1-d))]
assert 16*d-2==2
Nentry11=21*d-4;Nentry9=13*d-2
for entry in [Nentry11,Nentry9]:
 a=(2-entry-d)/(1-d);top=(1-d)*a;c=top/(1+d)
 assert P11[9:12]==[(a,2-a),(top,F(2)),(c,2-c)]
 assert 1<entry<entry+2*d<2
# Complementary ordinary R cases: bare mirror if absent3; triangular R3 if present.
assert fan('R',[4])<=ma11 and fan('R',[3])<=ma9
assert all(fan('D',range(8))<=m and fan('E',range(8))<=m and fan('Tc',range(8))<=m for m in [ma11,ma9])
sources=[HERE/'search.py',HERE/'room.json',HERE/'result.json',src,BASE/'surplus-four-local/O3-L70-hand/check.json',BASE/'surplus-four-local/e2-e1-b1/joined-top-absent.txt']
out={'status':'PARENT_L70_N7_ELEVEN_NINE_PASS','eleven':r11,'nine':r9,'root':'1/4','hand_equations':{'eleven':'24d-4=2','nine':'16d-2=2'},'strict_gates':{'eleven':['5/21','6/23'],'nine':['3/13','4/15']},'searched_frozen_room_only':'eleven strict20wall/firstT/reverse/sigma PASS; nine via whole support only, no other room built','parent_dispatch':'O3+L70: N7absent separate parent6; ordinaryN7 andR3abs new11; ordinaryR3 new9. Therefore entireO3+L70 parent<=11. Independent review pending.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE bounded new authorized pattern STOPPED firstcandidate35directions. Nine derived by analytic normal triangle replacement, no discovery. No extra room, search, parameter/word scan, archive or workers. Parent checks not independent/formal/expert proof; wholeO3 join depends separately on newfive review.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS11and9 fullsupport/strictmirrors/firstT/reverse/sigma; frozen11physical; parentwholeL70<=11pendingreview.')
