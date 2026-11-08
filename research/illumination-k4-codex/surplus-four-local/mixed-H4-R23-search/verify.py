"""One stopped six-contact witness, exact fullsupport; no search."""
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
assert P==[(F(0),F(0)),(F(4,5),F(1)),(F(12,5),F(-1)),(F(3),F(-1,4)),(F(1),F(9,4)),(F(8,5),F(3)),(F(28,9),F(10,9)),(F(2),F(2))]
W=[((0,1),(1,1)),((2,-1),(3,-1)),((3,-1),(3,0)),((1,2),(1,3)),((1,3),(2,3)),((3,1),(4,2))]
U,Z,_=e['constraints'](P,W)
print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H|fan('E',[4]);ma=mi|fan('E',[0,1,2,3,6,7])|fan('D',[0,2,3,4,5,6,7])|fan('R',[0,1,2,3,5,6,7])|fan('N',[1,2,3,4,5,7])|fan('Tc',[0,1,2,3,4,6,7])|fan('L',range(8))|fan('B',range(8))
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,W,mi,ma,q)
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
assert mi<=room<=ma
# One mixed envelope allows BOTH Dleaves; BOTH O3/O4 in B6701 upper.
ref=fan('L',[0])|fan('E',[4])|fan('N',[7])
upperR=H|fan('B',[7,0,1,2])|fan('D',[3,4])|fan('R',[2,3])|ref
assert U<=upperR<=ma
base=H|fan('B',[6,7,0,1])|fan('D',[3,4])|fan('L',[7,0])|fan('E',[4])|fan('R',[3])
assert U<=base|fan('N',[7])<=ma and U<=base|fan('Tc',[6])<=ma
assert Z==fan('D',[1])|fan('R',[4])|fan('N',[0,6])|fan('Tc',[5])|fan('E',[5])
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
d=F(4,5);assert F(7,9)<d<F(5,6) and 10*d-6==2
c=(12*d-4)/(1+d)
assert P==[(F(0),F(0)),(d,F(1)),(3*d,F(-1)),(F(3),3/d-4),(F(1),5/d-4),(7*d-4,F(3)),(c,c-2),(F(2),10*d-6)]
assert 0<d<1 and 2<3*d<3 and -1<3/d-4<0 and 2<5/d-4<3
assert 1<7*d-4<2 and 3<c<4 and 1<9*d-6<2 and q==(8,10)
assert e['on']((2,1),P[3],P[4]) and e['incident']((F(2),F(1)))<=H
# Frozen polygon angle ledger and simplicity, no other room.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](x,p) for x in t if x!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==3 and sum(angle(room,p)==180 for p in pts-A)==3
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for k,(c,f) in enumerate(zip(V,V[1:]+V[:1])):
  if i<k and (k-i) not in (1,len(V)-1):assert not e['edge_times'](a,b,c,f)
for t in Z:
 try:e['audit'](P,W,mi,ma|{t},q)
 except AssertionError:pass
 else:raise AssertionError('missed blocker')
sources=[src,HERE/'room.json',HERE/'result.json',HERE/'search.py',BASE/'fourth-surplus-review/mixed-e2-e1/argument.txt',BASE/'surplus-four-local/mixed-H4-D3-EO-search/findings.txt']
out={'status':'PARENT_E4_SIX_AND_R23_WHOLE_ROW_L70_TWO_SUBFAMILIES_PASS','path':[[str(x) for x in p] for p in P],'walls':W,'proof':proof,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'image':list(map(str,q)),'applications':['R23/H4 bothDleaves','L70 O3/O4 R3/N7 bothDleaves','L70 O3/O4 R3/Tc6 bothDleaves'],'frozen_physical':'20wall firstwalls/firstT/reverse/sigma PASS','root':'4/5','strict_gate':['7/9','5/6'],'endpoint_equation':'10d-6=2','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stoppedauthorizedpattern; noextra room/search/worker. Parentnewoptics/rowtransfersawaitreview, fullDelta4open.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS',q)
