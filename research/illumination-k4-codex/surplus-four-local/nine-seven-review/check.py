"""Review two supplied paths only. No search or new room construction.
Independent Fraction geometry; imports no peer or historical geometry code.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
import json, hashlib
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PEER=BASE/'fourth-surplus-review'
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def tri(t): return tuple(sorted(t))
def ccw(t):
 a,b,c=t
 return (a,b,c) if cross(sub(b,a),sub(c,a))>0 else (a,c,b)
def fan(a,ss):
 if isinstance(a,str): a=C[a]
 return {tri((a,(a[0]+R[i][0],a[1]+R[i][1]),(a[0]+R[(i+1)%8][0],a[1]+R[(i+1)%8][1]))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
# Finite local tiling universe only for incidence tests, not room generation.
TILES=set().union(*(fan((x,y),range(8)) for x in range(-6,9,2) for y in range(-6,9,2)))
def signs(p,t):
 t=ccw(t)
 return [cross(sub(t[(i+1)%3],t[i]),sub(p,t[i])) for i in range(3)]
def incident(p): return {t for t in TILES if min(signs(p,t))>=0}
def on(p,a,b): return cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0
def edge_times(a,b,c,d):
 v=sub(b,a);w=sub(d,c);den=cross(v,w)
 if den:
  t=F(cross(sub(c,a),w),den);u=F(cross(sub(c,a),v),den)
  return [t] if 0<=t<=1 and 0<=u<=1 else []
 if cross(sub(c,a),v):return []
 k=0 if v[0] else 1
 return [F(p[k]-a[k],v[k]) for p in (c,d) if on(p,a,b)]
def reflect(v,a,b):
 w=sub(b,a)
 return tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
def constraints(P,walls):
 used=set();absent=set();events=[]
 for a,b in zip(P,P[1:]):
  times={F(0),F(1)}
  for t in TILES:
   for c,d in zip(t,t[1:]+t[:1]):times.update(edge_times(a,b,c,d))
  times=sorted(times);samples=times[1:-1]+[(l+h)/2 for l,h in zip(times,times[1:])]
  for s in samples:
   p=tuple(a[k]+s*(b[k]-a[k]) for k in (0,1));used.update(incident(p))
  events.append(len(times)-2)
 for before,p,after,(a,b) in zip(P,P[1:],P[2:],walls):
  assert on(p,a,b) and p not in (a,b)
  v=reflect(sub(p,before),a,b);w=sub(after,p)
  assert cross(v,w)==0 and dot(v,w)>0
  side=cross(sub(b,a),sub(before,p));assert side
  assert side*cross(sub(b,a),sub(after,p))>0
  for t in incident(p):
   ss=[cross(sub(b,a),sub(q,p)) for q in t]
   assert min(ss)>=0 or max(ss)<=0
   s=sum(ss);assert s
   (used if s*side>0 else absent).add(t)
 assert not used&absent
 return used,absent,events
sigma=lambda p:(2-p[1],2-p[0])
def transform(ts):return {tri(tuple(sigma(p) for p in t)) for t in ts}
def audit(P,walls,minimum,maximum,target):
 assert P[0]==(0,0) and P[-1]==(2,2)
 for a,b in zip(P[:-2],P[1:-1]):assert not on((2,2),a,b)
 U,Z,events=constraints(P,walls)
 assert U<=minimum and not Z&maximum
 ur,zr,_=constraints(P[::-1],walls[::-1]);assert (ur,zr)==(U,Z)
 ps=[sigma(p) for p in P[::-1]];ws=[(sigma(a),sigma(b)) for a,b in walls[::-1]]
 us,zs,_=constraints(ps,ws);assert (us,zs)==(transform(U),transform(Z))
 # Independent specular checks above also cover reverse and sigma paths.
 q=P[-1]
 for a,b in walls[::-1]:
  v=reflect(sub(q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
 assert q==target
 return U,Z,{'reflections':len(walls),'required_count':len(U),'forbidden_count':len(Z),'segment_internal_edge_events':events,'unfolded_target':q,'forward_reverse_sigma':'PASS'}
def boundary(room):
 edges=Counter()
 for t in room:
  t=ccw(t)
  for a,b in zip(t,t[1:]+t[:1]):edges[(a,b)]+=1
 edge={e for e in edges if not edges[(e[1],e[0])]}
 nxt=defaultdict(list)
 for a,b in edge:nxt[a].append(b)
 assert all(len(v)==1 for v in nxt.values())
 p=min(nxt);start=p;cycle=[]
 while True:
  assert p not in cycle;cycle.append(p);p=nxt[p][0]
  if p==start:break
 assert len(cycle)==len(edge)
 return [p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
def inside(p,V):
 if any(on(p,a,b) for a,b in zip(V,V[1:]+V[:1])):return False
 n=0
 for a,b in zip(V,V[1:]+V[:1]):
  if (a[1]>p[1])!=(b[1]>p[1]):
   x=a[0]+F(p[1]-a[1],b[1]-a[1])*(b[0]-a[0]);n+=x>p[0]
 return n%2==1
def physical(P,V):
 for i,(a,b) in enumerate(zip(P,P[1:])):
  assert inside(tuple((a[k]+b[k])/2 for k in (0,1)),V)
  hits=[]
  for c,d in zip(V,V[1:]+V[:1]):
   for s in edge_times(a,b,c,d):
    if s>0:hits.append((s,c,d))
  if i==len(P)-2:assert not hits
  else:
   assert hits and min(h[0] for h in hits)==1
   hit=[h for h in hits if h[0]==1];assert len(hit)==1 and b not in V
   _,c,d=hit[0];v=reflect(sub(b,a),c,d);w=sub(P[i+2],b)
   assert cross(v,w)==0 and dot(v,w)>0

def path(d,nine):
 P=[(F(0),F(0)),(2*d/(1+d),2/(1+d)),(F(0),2-2*d),(2*d/(1-d),2-2*d/(1-d))]
 if nine:P +=[(4*d/(1-d),-4*d/(1-d)),(F(2),-6*d),(8*d/(1+d),-8*d/(1+d))]
 else:P +=[(5*d,F(-1))]
 k=16 if nine else 14
 P +=[((k-5)*d,F(3)),(k*d/(1+d),k*d/(1+d)-2),(F(1),(k-1)*d-2),(F(2),k*d-2)]
 return P
nw=[((0,2),(1,1)),((0,1),(0,2)),((0,2),(1,1))]
suffix=[((2,3),(3,3)),((3,1),(4,2)),((1,1),(1,2))]
w9=nw+[((1,-1),(2,-2)),((2,-2),(2,-1)),((1,-1),(2,-2))]+suffix
w7=nw+[((1,-1),(2,-1))]+suffix
p9=path(F(1,4),True);p7=path(F(2,7),False)
m9=H|fan('N',[6])|fan('D',[2])|fan('E',[3,4])
m7=H|fan('N',[6])|fan('E',[3,4])
extras=set().union(*(fan(k,range(8)) for k in ['L','B','R']))|fan('Tc',[4,5])
x9=m9|extras;x7=m7|extras|fan('D',[0,1,3,4,5,6,7])
u9,z9,a9=audit(p9,w9,m9,x9,(4,16));u7,z7,a7=audit(p7,w7,m7,x7,(4,14))
raw=json.loads((PEER/'single-room-search/room.json').read_text());room={tri(tuple(map(tuple,t))) for t in raw['triangles']}
assert room==H|set().union(*(fan(k,v) for k,v in raw['spec'].items()))
V=boundary(room);assert len(V)==20
assert set(V)==set(map(tuple,raw['vertices']))
physical(p9,V);physical(p9[::-1],V);physical([sigma(p) for p in p9[::-1]],[sigma(p) for p in V])
assert m9<=room<=x9
assert incident((F(3),F(2)))<=m9
assert inside((F(3),F(2)),V)
# Recompute frozen geometry ledger using exact local angle contributions.
def angle(room,p):
 n=0
 for t in room:
  if p not in t:continue
  other=[v for v in t if v!=p]
  v,w=[sub(q,p) for q in other]
  n+=90 if dot(v,w)==0 else 45
 return n
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
full={p for p in A if angle(room,p)==360};assert full=={(0,0),(2,0),(2,2)}
nonA=pts-A;J=sum(angle(room,p)==360 for p in nonA);sN=sum(angle(room,p)==180 for p in nonA)
assert (J,sN,J+sN)==(4,2,6)
# For every fixed family implication, permit all R sectors symbolically.
apps=[]
for label,ss in [('Bwest',[1,2,3]),('Brectangle',[0,1,2,3])]:
 for dsector,U,Z in [(2,u9,z9),(1,u7,z7)]:
  mi=H|fan('B',ss)|fan('L',[7,0])|fan('E',[3,4])|fan('Tc',[5])|fan('N',[6])|fan('D',[dsector])
  ma=mi|fan('R',range(8));assert U<=mi and not Z&ma
  apps.append({'B':label,'D':dsector,'R':'arbitrary','reflections':9 if dsector==2 else 7})
# Prior b0 classification prerequisites retained, not re-proved here.
local=H|fan('L',[7,0]);assert angle(local,(-1,1))==135
assert angle(local|fan('N',[5]),(-1,1))==180
for k in ['B','D','R','E','Tc']:assert not any((-1,1) in t for t in fan(k,range(8)))
top=H|fan('Tc',[5]);assert angle(top|fan('N',[0]),(1,3))==180
assert angle(H|fan('D',[1])|fan('R',[4]),(3,-1))==180
# b1 original inward application, with ordinary B1/Tc5/R4.
assert u9<=room and not z9&room
# Compare own derived paths and guards with peer receipts, not used as truth.
r9=json.loads((PEER/'single-room-search/verification.json').read_text())
r7=json.loads((PEER/'mixed-e2-e1/seven-path-floor-check.json').read_text())
def decode(x):return {tri(tuple(map(tuple,t))) for t in x}
for P,U,Z,rec in [(p9,u9,z9,r9['whole_family']),(p7,u7,z7,r7)]:
 assert U==decode(rec['required']) and Z==decode(rec['forbidden'])
assert p9==[tuple(F(v) for v in p) for p in r9['path']]
assert p7==[tuple(F(v) for v in p) for p in r7['path']]
files=[PEER/'single-room-search'/n for n in ['findings.txt','room.json','result.json','verification.json','verify.py']]+[PEER/'mixed-e2-e1'/n for n in ['seven-path-floor.txt','seven-path-floor-check.py','seven-path-floor-check.json','nine-path-transfer.txt','nine-path-transfer-check.py','nine-path-transfer-check.json','critical-B.txt']]
receipt={'status':'PASS','nine':a9,'seven':a7,'frozen_room':{'boundary_walls':20,'J':J,'s_N':sN,'interior_A':sorted(full),'physical_replay_forward_reverse_sigma':'PASS','E_inlet_3_2_interior':'PASS'},'whole_family_implications':apps,'local_angle_exclusions':'PASS','independence':'Standalone Fraction geometry, no peer/helper imports, no peer checker execution. Support extrema are conditional envelopes, not newly constructed rooms. Only frozen original room reconstructed.','limits':'Does not reprove upstream critical-B classification/forcing/budget, count validity of six descriptions, discover paths, or close Delta4. Broad parameter interval global support not computed: exact endpoint witnesses suffice.','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'check.json').write_text(json.dumps(receipt,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['source_sha256','checker_sha256']},indent=2,default=str))
