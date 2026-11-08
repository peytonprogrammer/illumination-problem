"""Own Fraction replay of four supplied peer paths. No peer execution or discovery."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]
engine=BASE/'surplus-four-local/R23-top6-search/verify.py'
ns={'__file__':str(engine)}
exec(engine.read_text().split('\ndef path(d,nine):')[0],ns)
globals().update({k:v for k,v in ns.items() if not k.startswith('__')})
PEER=BASE/'fourth-surplus-review'; HERE=Path(__file__).resolve().parent
pins={};results={}
def read(p):
 pins[str(p.relative_to(BASE))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return json.loads(p.read_text())
def decode(ts):return {tri(tuple(map(tuple,t))) for t in ts}
def fp(P):return [tuple(F(v) for v in p) for p in P]
def walls_for(P):
 out=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  v=sub(p,a);w=sub(b,p);v=tuple(x/max(map(abs,v)) for x in v);w=tuple(x/max(map(abs,w)) for x in w)
  t=tuple(v[i]+w[i] for i in (0,1))
  if t==(0,0):t=(-v[1],v[0])
  out.append((tuple(p[i]-t[i] for i in (0,1)),tuple(p[i]+t[i] for i in (0,1))))
 return out
def angle(room,p):
 return sum(90 if dot(sub(a,p),sub(b,p))==0 else 45 for t in room if p in t for a,b in [[v for v in t if v!=p]])
allK=H|set().union(*(fan(k,range(8)) for k in C))
def verify(name,folder,P,mi,Z,count,image,smooth=()):
 d=PEER/folder;raw=read(d/'room.json');result=read(d/'result.json');receipt=read(d/'check.json')
 for f,key in [('room.json','room_sha256'),('search.py','search_source_sha256')]:
  readpath=d/f;pins[str(readpath.relative_to(BASE))]=hashlib.sha256(readpath.read_bytes()).hexdigest();assert pins[str(readpath.relative_to(BASE))]==result[key]
 for rel,h in receipt['source_sha256'].items():
  p=BASE/rel;assert hashlib.sha256(p.read_bytes()).hexdigest()==h,rel
  pins[rel]=h
 for f in ('argument.txt','coverage.txt'):
  p=d/f;pins[str(p.relative_to(BASE))]=hashlib.sha256(p.read_bytes()).hexdigest()
 P=fp(P);walls=walls_for(P);ma=(allK|fan((-2,2),range(8))|fan((-2,-2),range(8)))-Z
 U,z,detail=audit(P,walls,mi,ma,image);assert z==Z and (len(U),len(z))==count
 assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
 saved=next(iter(receipt['fixed_paths'].values()));assert U==decode(saved['required']) and Z==decode(saved['forbidden'])
 room=decode(raw['triangles']);V=boundary(room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
 for i,(a,b) in enumerate(zip(V,V[1:]+V[:1])):
  for j,(c,d1) in enumerate(zip(V,V[1:]+V[:1])):
   if i<j and j-i not in (1,len(V)-1):assert not edge_times(a,b,c,d1)
 assert U<=room and not Z&room
 physical(P,V);physical(P[::-1],V);physical([sigma(p) for p in P[::-1]],[sigma(p) for p in V])
 pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
 assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
 J=sum(angle(room,p)==360 for p in pts-A);sN=sum(angle(room,p)==180 for p in pts-A)
 assert J+sN==6 and len(P)-2==detail['reflections']
 for p in smooth:assert angle(room,p)==180 and p not in V
 results[name]={'reflections':len(P)-2,'required':sorted(U),'forbidden':sorted(Z),'audit':detail,'room':{'tiles':len(room),'walls':len(V),'J':J,'s_N':sN},'smooth_contacts':smooth}
 return U,Z,P
u,z,P=verify('core_three','remote2101-left-N6',[(0,0),('3/2',-1),(3,0),(1,'4/3'),(2,2)],H,fan('D',[2])|fan('R',[3,4])|fan('N',[7]),(10,4),(6,-4),[(3,0)])
d=F(2,3);assert F(3,5)<d<F(4,5) and P==fp([(0,0),(1/d,-1),(3,3*d-2),(1,5*d-2),(2,6*d-2)])
# The general first mirror is only this finite subinterval; D1 may be present.
assert on(P[1],(1,-1),(2,-1)) and P[1] not in [(1,-1),(2,-1)]
assert not z&(fan('L',range(8))|fan((-2,2),range(8)))
u,z,P=verify('left_four','remote2101-left-full',[(0,0),('-4/3',1),('-16/7','2/7'),('-7/4',1),('-1/4',-1),(2,2)],H|fan('L',[7,0,1,2]),fan('L',[3])|fan('B',[2])|fan((-2,2),[6]),(13,3),(-8,6))
d=F(3,4);a=-4/(1+d);assert F(5,7)<d<F(4,5) and P==fp([(0,0),(-1/d,1),(a,-a-2),(3*d-4,1),(5*d-4,-1),(8*d-4,2)])
prior=read(BASE/'surplus-four-local/L7012-D23-search/verification.json')
assert prior['path']==[[str(x) for x in p] for p in P]
assert decode(prior['required'])==u and decode(prior['forbidden'])==z
# Whole2110 full-L-left: with B1 active, B12 impossible b0 at odd/odd(-1,-1).
assert angle(H|fan('L',[7,0,1,2])|fan('B',[1,2])|fan((-2,2),[5]),(-1,-1))==180
assert not z&(fan('B',[0,1])|set().union(*(fan(k,range(8)) for k in ['D','R','E','Tc','N']))|fan((-2,2),[5]))
u,z,P=verify('B_upper_nine','remote2101-B-upper',[(0,0),('1/4',1),('4/5','-6/5'),(-1,'-3/4'),('18/5','2/5'),('7/2',0),('10/3','2/3'),('2/3','4/3'),('1/2',2),('2/5','8/5'),(2,2)],H|fan('B',[1,2])|fan('R',[3])|fan('N',[7]),fan('L',[7])|fan('B',[0])|fan('R',[2,4])|fan('N',[0,6]),(21,6),(4,16))
d=F(1,4);a=4*d/(1+d);j=6*(1-d)/(1+d);k=(6-14*d)/(1-d);l=(4-14*d)/(1-d);m=(4-14*d)/(1+d)
assert F(3,13)<d<F(4,15) and P==fp([(0,0),(d,1),(a,a-2),(-1,5*d-2),(j,4-j),(6-10*d,0),(k,4-k),(l,2-l),(4-14*d,2),(m,2-m),(2,16*d-2)])
assert not z&(set().union(*(fan(k,range(8)) for k in ['D','E','Tc']))|fan((-2,-2),range(8)))
u,z,P=verify('B_roof_six','remote2101-B-roof',[(0,0),('-4/3',-2),('-8/5','-8/5'),(-1,-2),(3,'2/3'),(1,2),('14/5','16/5'),(2,2)],H|fan('B',[1,2,3])|fan((-2,-2),[0])|fan('Tc',[6]),fan('B',[4])|fan('R',[3])|fan('Tc',[7])|fan('N',[0,7])|fan((-2,-2),[1,7]),(22,7),(-8,-12),[(-1,-2),(1,2)])
d=F(2,3);a=-4*d/(1+d);b=(10-8*d)/(1+d);assert F(7,11)<d<F(7,10) and P==fp([(0,0),(-2*d,-2),(a,a),(2/d-4,-2),(3,7*d-4),(1,9*d-4),(b,6-b),(10-12*d,2)])
assert not z&(fan('D',range(8))|fan('R',[4])|fan('N',[5,6]))
pins[str(engine.relative_to(BASE))]=hashlib.sha256(engine.read_bytes()).hexdigest()
pins[str(Path(__file__).resolve().relative_to(BASE))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'check.json').write_text(json.dumps({'status':'INDEPENDENT_FOUR_PEER_OPTICAL_LEMMAS_PASS','paths':results,'source_sha256':pins,'limits':'No classification completeness claimed; whole-support implications only. No discovery; supplied polygons only; own Fraction primitives.'},indent=2,default=str)+'\n')
print('PASS four peer optical lemmas: THREE10U4Z / FOUR13U3Z / NINE21U6Z / SIX22U7Z')
