"""Exact fixed three and sigma, frozen N45 room only; no discovery."""
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
assert P==[(F(0),F(0)),(F(2,3),F(1)),(F(2),F(-1)),(F(3),F(1,2)),(F(2),F(2))]
W=[((0,1),(1,1)),((1,-1),(3,-1)),((3,0),(3,1))]
U,Z,_=e['constraints'](P,W)
print('COUNTS',len(U),len(Z))
for k in ['L','B','D','R','E','Tc','N']:print('U',k,[i for i in range(8) if fan(k,[i])&U]);print('Z',k,[i for i in range(8) if fan(k,[i])&Z])
mi=H;ma=H|fan('D',[0,3,4,5,6,7])|fan('R',[0,1,2,4,5,6,7])|fan('N',[0,1,2,3,4,5,7])|set().union(*(fan(k,range(8)) for k in ['L','B','E','Tc']))
q=P[-1]
for a,b in W[::-1]:
 v=e['reflect'](e['sub'](q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
u,z,proof=e['audit'](P,W,mi,ma,q)
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};assert room==H|set().union(*(fan(k,ss) for k,ss in raw['spec'].items()))
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);sigma=e['sigma'];e['physical']([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
assert mi<=room<=ma and (2,-1) not in V
CW=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if e['on']((2,-1),a,b)]
assert len(CW)==1 and set(CW[0])=={(1,-1),(3,-1)}
PS=[sigma(p) for p in P[::-1]];WS=[(sigma(a),sigma(b)) for a,b in W[::-1]];mis=e['transform'](mi);mas=e['transform'](ma)
qs=PS[-1]
for a,b in WS[::-1]:
 v=e['reflect'](e['sub'](qs,a),a,b);qs=tuple(a[k]+v[k] for k in (0,1))
us,zs,proofs=e['audit'](PS,WS,mis,mas,qs)
for k in ['L','B','D','R','E','Tc','N']:print('SIGMA Z',k,[i for i in range(8) if fan(k,[i])&zs])
# Whole conditional rows; symbolic envelopes, no completed room.
refs=fan('B',[1])|fan('E',[4])|fan('Tc',[5])
N45=H|fan('L',[0,1,2,3])|refs|fan('N',[4,5]);assert U<=N45<=ma
for ns in [[4,5],[5]]:
 base=H|fan('L',[7,0,1,2])|refs|fan('N',ns)
 assert U<=base|fan('R',[4])<=ma
 assert us<=base|fan('D',[1])<=mas
# Eouter L7012 also fits the same D1/R4 split.
base=H|fan('L',[7,0,1,2])|fan('B',[1])|fan('E',[4,5])|fan('Tc',[5])|fan('N',[5])
assert U<=base|fan('R',[4])<=ma and us<=base|fan('D',[1])<=mas
assert Z==fan('D',[1,2])|fan('R',[3])|fan('N',[6])
assert zs==fan('D',[2])|fan('R',[3,4])|fan('N',[7])
assert all(not e['on']((0,0),a,b) for a,b in zip(P[1:],P[2:]))
d=F(2,3);assert F(3,5)<d<F(3,4) and 6-6*d==2
assert P==[(F(0),F(0)),(d,F(1)),(3*d,F(-1)),(F(3),3/d-4),(6-6*d,F(2))]
assert 0<d<1 and 1<3*d<3 and 0<3/d-4<1 and 1<6-5*d<3
assert q==(4,6) and qs==(6,-4)
def angle(ts,p):
 n=0
 for t in ts:
  if p in t:
   a,b=[e['sub'](x,p) for x in t if x!=p];n+=90 if e['dot'](a,b)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
assert sum(angle(room,p)==360 for p in pts-A)==2 and sum(angle(room,p)==180 for p in pts-A)==4
assert angle(room,(2,-1))==180
for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
 for k,(c,f) in enumerate(zip(V,V[1:]+V[:1])):
  if i<k and (k-i) not in (1,len(V)-1):assert not e['edge_times'](a,b,c,f)
for t in Z:
 try:e['audit'](P,W,mi,ma|{t},q)
 except AssertionError:pass
 else:raise AssertionError('missed blocker')
sources=[src,HERE/'room.json',HERE/'result.json',HERE/'search.py',BASE/'surplus-four-local/e2-e1-b1/critical-L.txt']
out={'status':'PARENT_CORE_THREE_AND_SIGMA_HAND_FIVE_OUTSIDE_TRANSFERS_PASS','path':[[str(x) for x in p] for p in P],'walls':W,'proof':proof,'required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(mi),'maximum':sorted(ma),'image':list(map(str,q)),'sigma_three':{'path':[[str(x) for x in p] for p in PS],'proof':proofs,'required':sorted(us),'forbidden':sorted(zs),'minimum':sorted(mis),'maximum':sorted(mas),'image':list(map(str,qs))},'applications':['L0123N45 noD/R','L7012N45/R4','L7012N45/D1 sigma','L7012E45/R4','L7012E45/D1 sigma'],'frozen_physical':'20wall firstwalls/firstactualT/reverse/sigma PASS; floor2,-1 smooth180 inside maximal wall(1,-1)--(3,-1)','root':'2/3','strict_gate':['3/5','3/4'],'endpoint_equation':'6-6d=2','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'ONE stopped authorizedpattern, onlyfrozenroom physicallyreconstructed. Parentproofpendingreview, nootherroom/search/worker; fullDelta4open.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS',q,qs)
