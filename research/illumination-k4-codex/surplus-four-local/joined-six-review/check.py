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
# TWO supplied hand candidates only. No ray tracing, room or word search.
P4=[(F(0),F(0)),(F(1,2),F(-5,2)),(F(1),F(-13,5)),(F(2,3),F(-8,3)),(F(9,5),F(3)),(F(2),F(2))]
P6=[(F(0),F(0)),(F(2,5),F(-12,5)),(F(1),F(-5,2)),(F(4,7),F(-18,7)),(F(8,5),F(18,5)),(F(2),F(11,3)),(F(12,7),F(26,7)),(F(2),F(2))]
bottom=[((0,-2),(1,-3)),((1,-3),(1,-2)),((0,-2),(1,-3))]
w4=bottom+[((1,3),(2,3))]
w6=bottom+[((1,3),(2,4)),((2,3),(2,4)),((1,3),(2,4))]
min4=H|fan('B',[7,0,1])|fan('D',[2,3])
min6=H|fan('B',[7,0,1])|fan('Tc',[5])
common=H|fan('B',[0,1,2,3,4,5,7])|fan('D',[0,1,2,3,5,6,7])|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
max4=common|fan('Tc',[0,1,2,3,4,6,7])
max6=common|fan('Tc',[0,1,2,3,5,7])
u4,z4,r4=audit(P4,w4,min4,max4,(2,-10))
u6,z6,r6=audit(P6,w6,min6,max6,(2,-12))
assert on((1,-1),P4[3],P4[4]) and incident((F(1),F(-1)))<=min4
assert not incident((F(1),F(-1)))<=(min4-fan('D',[2]))
assert not u6&fan('D',range(8))
assert on((1,0),P6[3],P6[4]) and incident((F(1),F(0)))<=H
# Independently check the two normalized endpoint formulae at strict roots.
for d,P,six in [(F(1,5),P4,False),(F(1,6),P6,True)]:
 assert F(1,7)<d<(F(2,11) if six else F(2,9))
 prefix=[(F(0),F(0)),(2*d/(1-d),-2/(1-d)),(F(1),-2-3*d),(4*d/(1+d),-2-4*d/(1+d))]
 assert P[:4]==prefix
 if six:
  assert P[4:]==[(8*d/(1-d),2+8*d/(1-d)),(F(2),2+10*d),(12*d/(1+d),2+12*d/(1+d)),(12*d,F(2))]
 else:assert P[4:]==[(9*d,F(3)),(10*d,F(2))]
apps=[]
for label,ss in [('O3',[7,0,1]),('H4',[7,0,1,2])]:
 b=fan('B',ss)
 # Peer mixed conditional whole support with D23 and ordinary Tc.
 mi=H|b|fan('D',[2,3]);ma=mi|fan('Tc',[4,6,7])|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
 assert u4<=mi and not z4&ma
 apps.append({'B':label,'condition':'D23,Tc5 absent','reflections':4})
 mi6=mi|fan('Tc',[5]);ma6=mi6|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
 assert u6<=mi6 and not z6&ma6
 apps.append({'B':label,'condition':'D23,Tc5 present and Tc4/6 absent','reflections':6})
 # Own b1 conditional transfer: ANY partner away Tc with ordinary Tc5,
 # D absent/ordinary1or2/unit01/12/23, or even arbitrary D except4.
 mi=H|b|fan('Tc',[5]);ma=mi|fan('D',[0,1,2,3,5,6,7])|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
 assert u6<=mi and not z6&ma
 apps.append({'B':label,'condition':'b1 ordinaryTc5, ANY partner awayTc; D4 absent','reflections':6})
# Explicit mirror blockers, no stronger claim for O4 or occupied Tc4/6.
for ts in [fan('B',[6]),fan('D',[4]),fan('Tc',[4]),fan('Tc',[6])]:assert z6&ts
assert z4&fan('Tc',[5])
# Read peer receipt only for comparison AFTER independent audit.
source=PEER/'mixed-e2-e1/joined-four-check.json'
raw=json.loads(source.read_text())
def decode(x):return {tri(tuple(map(tuple,t))) for t in x}
assert P4==[tuple(F(x) for x in p) for p in raw['path']]
assert u4==decode(raw['required']) and z4==decode(raw['forbidden'])
six=raw['six_path_complement'];assert P6==[tuple(F(x) for x in p) for p in six['path']]
assert u6==decode(six['required']) and z6==decode(six['forbidden'])
inputs=[source,PEER/'mixed-e2-e1/joined-four-check.py',PEER/'mixed-e2-e1/argument.txt',PEER/'mixed-e2-e1/critical-B.txt',BASE/'surplus-four-local/mixed-critical-B-review/review.txt']
proof=PEER/'mixed-e2-e1/joined-four.txt'
if proof.exists():inputs.append(proof)
receipt={'status':'PASS','four':r4,'six':r6,'intermediate_corners':'four passes interior(1,-1) requiringD2; six passes interior(1,0) entirelyH','whole_family_applications':apps,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Two supplied fixed paths and conditional support transfer only. Reuses own helper-free engine; no peer checker execution, new room, search or mixed classification review. Four/six ordinaryTc split assumes Tc ordinary or absent, not arbitrary Tc unit.'}
(OUT/'check.json').write_text(json.dumps(receipt,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['source_sha256','checker_sha256']},indent=2,default=str))
