"""One stopped candidate and its sigma; no search or additional room."""
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
assert P==[(F(0),F(0)),(F(-1),F(-1,4)),(F(14,5),F(-6,5)),(F(2),F(2))]
W=[((-1,-1),(-1,0)),((2,-2),(3,-1))]
U,Z,_=e['constraints'](P,W)
print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H|fan('D',[1,2]);ma=mi|fan('D',[3,4,5,6,7])|fan('L',[0,1,2,3,4,5,6])|set().union(*(fan(k,range(8)) for k in ['B','R','E','Tc','N']))
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,W,mi,ma,q)
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
assert mi<=room<=ma
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]];mis=e['transform'](mi);mas=e['transform'](ma)
assert mis==H|fan('R',[3,4])
qs=PS[-1]
for a,b in WS[::-1]:
 v=e['reflect'](e['sub'](qs,a),a,b);qs=tuple(a[k]+v[k] for k in (0,1))
us,zs,proofs=e['audit'](PS,WS,mis,mas,qs)
for k in ['L','B','D','R','E','Tc','N']:print('SIGMA Z',k,[i for i in range(8) if fan(k,[i])&zs])
# Exact named original table inclusions; no completed room.
ordinary=fan('B',[1])|fan('E',[4])|fan('Tc',[5])|fan('N',[5])
assert U<=mi|fan('L',[0,1,2,3])|ordinary<=ma
assert us<=mis|fan('L',[0,1,2,3])|ordinary<=mas
assert us<=mis|fan('L',[7,0,1,2])|ordinary|fan('D',[2])<=mas
assert Z==fan('L',[7])|fan('D',[0]) and zs==fan('R',[5])|fan('Tc',[6])
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
d=F(1,4);assert F(1,5)<d<F(1,3) and 4-8*d==2
c=(4-2*d)/(1+d);assert P==[(F(0),F(0)),(F(-1),-d),(c,c-4),(4-8*d,F(2))]
assert 1<1/d-2<3 and 2<c<3 and -2<c-4<-1
assert e['on']((2,-1),P[1],P[2]) and e['incident']((F(2),F(-1)))<=mi
# Independent frozen geometry ledger and simple maximal polygon.
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
table=BASE/'surplus-four-local/e2-e1-b1/critical-L.txt'
sources=[src,HERE/'room.json',HERE/'result.json',HERE/'search.py',table]
out={'status':'PARENT_D12_TWO_AND_SIGMA_R34_TWO_HAND_AND_THREE_ROWS_PASS','path':[[str(x) for x in p] for p in P],'walls':W,'proof':proof,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'image':list(map(str,q)),'sigma_two':{'path':[[str(x) for x in p] for p in PS],'proof':proofs,'required':sorted(us),'forbidden':sorted(zs),'minimum':sorted(mis),'maximum':sorted(mas),'image':list(map(str,qs))},'applications':['L0123 D12','L0123 R34','L7012 R34 with ordinaryD2'],'frozen_physical':'20wall firstwalls/firstactualT/reverse/sigma PASS','root':'1/4','strict_gate':['1/5','1/3'],'endpoint_equation':'4-8d=2','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stopped authorized pattern; no extra room/search/worker. Parent hand proof pending independent review. WholeL0123/fullcriticalL/Delta4 not claimed.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS',q,qs)
