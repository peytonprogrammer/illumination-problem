"""Exact verification of the one stopped BO/D2 candidate and whole support."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H']
raw=json.loads((HERE/'room.json').read_text());j=json.loads((HERE/'result.json').read_text())
assert j['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
assert hashlib.sha256((HERE/'room.json').read_bytes()).hexdigest()==j['room_sha256']
assert hashlib.sha256((HERE/'search.py').read_bytes()).hexdigest()==j['search_source_sha256']
P=[tuple(F(*x) for x in p) for p in j['candidate']['path']]
assert P==[(F(0),F(0)),(F(1),F(-4,3)),(F(1,2),F(-2)),(F(0),F(-4,3)),(F(3),F(8,3)),(F(11,4),F(3)),(F(2),F(2))]
W=[((1,-2),(1,-1)),((0,-2),(1,-2)),((0,-2),(0,-1)),((3,2),(3,3)),((2,3),(3,3))]
U,Z,events=e['constraints'](P,W)
print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H|fan('B',[0,1])
ma=mi|fan('B',[3,4,5,6])|fan('D',[0,1,2,4,5,6,7])|fan('E',[0,1,2,4,5,6,7])|fan('Tc',[0,1,2,3,4,5,7])|set().union(*(fan(k,range(8)) for k in ['L','R','N']))
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,W,mi,ma,q)
print('IMAGE',q)
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']}
assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);s=e['sigma'];e['physical']([s(p) for p in P[::-1]],[s(p) for p in V])
assert mi<=room<=ma and all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
common=H|fan('L',[6,7,0])|fan('B',[0,1])|fan('E',[4])|fan('Tc',[5])|fan('N',[6])
upper=common|fan('D',[1,2])|fan('R',[3,4])
assert U<=common<=upper<=ma and not Z&upper
assert Z==fan('B',[2,7])|fan('D',[3])|fan('E',[3])|fan('Tc',[6])
# Independent frozen-room geometry and angle ledger.
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](q,p) for q in t if q!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
pts={p for t in room for p in t};As={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in As if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-As);sN=sum(angle(room,p)==180 for p in pts-As)
assert (J,sN,len(room))==(3,3,33)
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for k,(c,f) in enumerate(zip(V,V[1:]+V[:1])):
  if i<k and (k-i) not in (1,len(V)-1):assert not e['edge_times'](a,b,c,f)
# Hand forced root only; no parameter discovery or second room.
d=F(3,4);assert F(5,7)<d<F(5,6) and 8-8*d==2
assert P==[(F(0),F(0)),(F(1),-1/d),(2-2*d,F(-2)),(F(0),2/d-4),(F(3),5/d-4),(8-7*d,F(3)),(8-8*d,F(2))]
assert -2<-1/d<-1 and 0<2-2*d<1 and -2<2/d-4<-1
assert 0<3*d-2<1 and 1<5*d-2<3 and 2<5/d-4<3 and 2<8-7*d<3
assert q==(6,-8)
assert e['incident']((F(1),F(0)))<=H and e['on']((1,0),P[3],P[4])
# Entire outside-C Bouter rows of the original necessary table, one envelope.
BOlow=H|fan('B',[0,1])|fan('E',[4])|fan('Tc',[5])|fan('N',[5])
BOhigh=BOlow|fan('L',range(8))|fan('D',[1,2])|fan('R',[3,4])
assert U<=BOlow<=BOhigh<=ma
# Sigma plus reversal: Eouter45 with L7/B2/R2 absent; same path, no room.
PS=[s(p) for p in P[::-1]];WS=[(s(a),s(b)) for a,b in W[::-1]]
mis=e['transform'](mi);mas=e['transform'](ma)
assert mis==H|fan('E',[4,5])
qs=PS[-1]
for a,b in WS[::-1]:
 v=e['reflect'](e['sub'](qs,a),a,b);qs=tuple(a[k]+v[k] for k in (0,1))
us,zs,proofs=e['audit'](PS,WS,mis,mas,qs)
assert zs==fan('E',[3,6])|fan('R',[2])|fan('B',[2])|fan('L',[7])
EOlow=mis|fan('B',[1])|fan('Tc',[5])|fan('N',[5])
EOhigh=EOlow|fan('L',[0,1,2,3])|fan('D',[1,2])|fan('R',[3,4])
assert us<=EOlow<=EOhigh<=mas
# The remaining L7012 Eouter row contains L7 and is deliberately excluded.
assert zs&fan('L',[7])
# Every forbidden tile removes a necessary mirror.
for t in Z:
 try:e['audit'](P,W,mi,ma|{t},q)
 except AssertionError:pass
 else:raise AssertionError('missed blocker')
table=BASE/'surplus-four-local/e2-e1-b1/critical-L.txt'
assert 'FOUR:  L670 +BO+E-/T-/Nb+ and exactly ONE D-/D+/R-/R+.' in table.read_text()
sources=[src,HERE/'room.json',HERE/'result.json',HERE/'search.py',table,BASE/'fourth-surplus-review/peer-critical-L-classification-independent/review.txt',BASE/'fourth-surplus-review/peer-critical-L-optical-independent/review.txt']
out={'status':'PARENT_BO_FIVE_FOUR_INWARD_AND_OUTSIDE_TRANSFERS_PASS','path':[[str(x) for x in p] for p in P],'walls':W,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'proof':proof,'image':list(map(str,q)),'four_inward_common_minimum':sorted(common),'four_inward_upper':sorted(upper),'physical_frozen_room':'firstwall/firstactualT/noSrevisit/reverse/sigma20walls PASS','geometry':{'W':20,'J':J,'s_N':sN,'Q':9,'k':6,'Delta':4,'tiles':33,'full_A':'S,U,T'},'root':'3/4','strict_gate':['5/7','5/6'],'endpoint_equation':'8-8d=2','outside_BO_upper':sorted(BOhigh),'sigma_five':{'path':[[str(x) for x in p] for p in PS],'proof':proofs,'required':sorted(us),'forbidden':sorted(zs),'minimum':sorted(mis),'maximum':sorted(mas),'outside_EO_upper':sorted(EOhigh)},'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stopped authorized pattern search, no second room/search/cap product/worker. Parent proof pending independent review; full criticalL/Delta4 not claimed.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS WHOLE FOUR INWARD')
