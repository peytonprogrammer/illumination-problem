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
u,z,P=verify('B_R3_eight','remote2101-B-roof-D2',[(0,0),('4/7','-10/7'),(-1,'-4/5'),('22/7','6/7'),('12/5',-1),(1,'5/2'),('6/5',3),('14/5',-1),(3,'-1/2'),(2,2)],H|fan('B',[1,2])|fan('R',[3]),fan('L',[7])|fan('B',[0])|fan('D',[1])|fan('R',[2,4])|fan('Tc',[5])|fan('N',[0]),(21,7),(8,-20))
d=F(2,5);a=2*d/(1+d);b=(6-4*d)/(1+d)
assert F(7,18)<d<F(7,17) and P==fp([(0,0),(a,a-2),(-1,3*d-2),(b,4-b),(6-9*d,-1),(1,5/d-10),(13*d-4,3),(17*d-4,-1),(3,7/d-18),(10-20*d,2)])
assert on(P[5],(1,2),(1,3)) and P[5] not in [(1,2),(1,3)]
assert not z&(fan((-2,-2),range(8))|fan('D',[2])|fan('Tc',[6])|fan('N',[5,6,7]))
pins[str(engine.relative_to(BASE))]=hashlib.sha256(engine.read_bytes()).hexdigest()
pins[str(Path(__file__).resolve().relative_to(BASE))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'check.json').write_text(json.dumps({'status':'INDEPENDENT_B_R3_EIGHT_ACCEPTED','paths':results,'source_sha256':pins},indent=2,default=str)+'\n')
print('PASS B/R3 EIGHT21U7Z; actualT/unfold8,-20/wholeguard')
