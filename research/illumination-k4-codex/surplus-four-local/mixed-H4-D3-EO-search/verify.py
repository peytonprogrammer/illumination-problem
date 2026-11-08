"""One stopped mixed candidate exact replay and symbolic support only."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
raw=json.loads((HERE/'room.json').read_text());j=json.loads((HERE/'result.json').read_text())
assert j['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for name,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==j[key]
P=[tuple(F(*x) for x in p) for p in j['candidate']['path']]
assert P==[(F(0),F(0)),(F(2,3),F(1)),(F(2),F(-1)),(F(16,5),F(4,5)),(F(-2,5),F(-8,5)),(F(2),F(2))]
W=[((0,1),(1,1)),((1,-1),(3,-1)),((3,1),(4,0)),((-1,-1),(0,-2))]
U,Z,_=e['constraints'](P,W)
print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H|fan('B',[1,2])|fan('R',[3]);ma=mi|fan('B',[0,4,5,6,7])|fan('R',[0,1,4,5,6,7])|fan('D',[0,3,4,5,6,7])|fan('N',[0,1,2,3,4,5,7])|set().union(*(fan(k,range(8)) for k in ['L','E','Tc']))
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,W,mi,ma,q)
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
assert mi<=room<=ma and (2,-1) not in V
cw=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if e['on']((2,-1),a,b)];assert len(cw)==1 and set(cw[0])=={(1,-1),(3,-1)}
# H4 Broot supplies B12, omits3; allow BOTH Dleaves in one upper.
base=H|fan('B',[7,0,1,2])|fan('D',[3,4])|fan('L',[0])|fan('E',[4])|fan('N',[7])|fan('R',[3])
assert U<=base|fan('E',[5])<=ma # last Eouter H4D3 residual
assert U<=base|fan('R',[4])|fan('Tc',[6])<=ma # R34/Tc6 BOTHleaves
assert U<=base|fan('N',[0])|fan('Tc',[6])<=ma # N70/R3/Tc6 BOTHleaves
assert Z==fan('B',[3])|fan('D',[1,2])|fan('R',[2])|fan('N',[6])
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
d=F(2,3);assert F(7,11)<d<F(5,7) and 12*d-6==2
r=8*d/(1+d);b=(8*d-6)/(1+d)
assert P==[(F(0),F(0)),(d,F(1)),(3*d,F(-1)),(r,4-r),(b,-b-2),(12*d-6,F(2))]
assert 0<d<1 and 1<3*d<3 and 0<3/d-4<1 and 3<r<4 and -1<b<0
assert -1<8-5/d<1 and -1<9*d-6<1 and 1<11*d-6<3 and q==(8,12)
assert e['on']((2,0),P[3],P[4]) and e['incident']((F(2),F(0)))<=H
# Independent frozen geometry ledger/simplicity, smooth midpoint at floor.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](x,p) for x in t if x!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
assert angle(room,(2,-1))==180
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for k,(c,f) in enumerate(zip(V,V[1:]+V[:1])):
  if i<k and (k-i) not in (1,len(V)-1):assert not e['edge_times'](a,b,c,f)
for t in Z:
 try:e['audit'](P,W,mi,ma|{t},q)
 except AssertionError:pass
 else:raise AssertionError('missed blocker')
sources=[src,HERE/'room.json',HERE/'result.json',HERE/'search.py',BASE/'surplus-four-local/mixed-singleleaf-short-transfer/check.json',BASE/'fourth-surplus-review/mixed-Eouter-four-transfer/argument.txt',BASE/'fourth-surplus-review/mixed-e2-e1/argument.txt']
out={'status':'PARENT_B12_R3_FOUR_AND_THREE_MIXED_ROW_COMPLETIONS_PASS','path':[[str(x) for x in p] for p in P],'walls':W,'proof':proof,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'image':list(map(str,q)),'frozen_physical':'20wall/firstwall/firstT/reverse/sigma, smoothfloor2,-1 inside maximal1,-1--3,-1 PASS','applications':['H4D3 Eouter lastR3 residual','H4/R34/Tc6 bothDleaves','H4/N70/R3/Tc6 bothDleaves'],'root':'2/3','strict_gate':['7/11','5/7'],'endpoint_equation':'12d-6=2','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stoppedauthorizedpattern; nootherroom/search/worker. Parentnewfour/rowjoinsawaitindependentreview. FullDelta4notclaimed.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS',q)
