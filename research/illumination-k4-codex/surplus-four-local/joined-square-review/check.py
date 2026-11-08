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
# Independently hard-coded TWO supplied paths; no inherited substitution code.
P2=[(F(0),F(0)),(F(3,5),F(-3)),(F(9,5),F(3)),(F(2),F(2))]
P4=[(F(0),F(0)),(F(1,2),F(-3)),(F(8,5),F(18,5)),(F(2),F(11,3)),(F(12,7),F(26,7)),(F(2),F(2))]
w2=[((0,-3),(1,-3)),((1,3),(2,3))]
w4=[((0,-3),(1,-3)),((1,3),(2,4)),((2,3),(2,4)),((1,3),(2,4))]
O4=fan('B',[6,7,0,1]);allD=fan('D',range(8));rest=set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
min2=H|O4|fan('D',[2,3]);max2=min2|allD|rest|fan('Tc',[0,1,2,3,4,6,7])
min4=H|O4|fan('Tc',[5]);max4=min4|allD|rest|fan('Tc',[0,1,2,3,5,7])
u2,z2,r2=audit(P2,w2,min2,max2,(2,-10))
u4,z4,r4=audit(P4,w4,min4,max4,(2,-12))
assert on((1,-1),P2[1],P2[2])
assert incident((F(1),F(-1)))<=min2
assert not incident((F(1),F(-1)))<=(min2-fan('D',[2]))
assert not (u4|z4)&allD and not z2&allD
# The ONLY extra forbidden floor mate is at remote center(0,-4).
remote=fan((0,-4),[1])
assert len(z2)==2 and len(z4)==3
assert z2==remote|fan('Tc',[5])
assert z4==remote|fan('Tc',[4,6])
assert not remote&(H|set().union(*(fan(k,range(8)) for k in C)))
# Fixed rational endpoint parameters and local portal equalities.
for d,P in [(F(1,5),P2),(F(1,6),P4)]:
 inlet=(2*d,F(-2));hit=(3*d,F(-3));outlet=(4*d,F(-2))
 assert P[1]==hit and 0<2*d<3*d<4*d<1
 for a,b,v in [(inlet,hit,(d,-1)),(hit,outlet,(d,1)),(P[0],inlet,(d,-1))]:
  w=sub(b,a);assert cross(w,v)==0 and dot(w,v)>0
 # Old triangle triple contact state, derived directly, matches same ports.
 old=[(2*d/(1-d),-2/(1-d)),(F(1),-2-3*d),(4*d/(1+d),-2-4*d/(1+d))]
 assert cross(sub(old[0],inlet),(d,-1))==0
 assert cross(sub(outlet,old[-1]),(d,1))==0
 assert dot(sub(outlet,old[-1]),(d,1))>0
assert 10*F(1,5)==12*F(1,6)==2
# Four predeclared symbolic applications, no completed room construction.
applications=[]
applications.append({'branch':'mixed O4+D23, ordinaryTc empty/6','reflections':2})
applications.append({'branch':'mixed O4+D23, ordinaryTc5','reflections':4})
# b1 O4 has an ordinaryTc5, root partner awayTc. Full D safe.
assert u4<=min4 and not z4&max4
applications.append({'branch':'b1 O4+ordinaryTc5, ANY root partner awayTc, fullD safe','reflections':4})
# Same optical transfer for original single leaf3 OR4.
for leaf in [3,4]:
 mi=H|O4|fan('D',[leaf])|fan('Tc',[5]);ma=mi|rest
 assert u4<=mi and not z4&ma
 applications.append({'branch':'singleDleaf'+str(leaf)+',O4,ordinaryTc5','reflections':4})
# Compare derived guards/coordinates to peer receipt only AFTER own audit.
source=PEER/'mixed-e2-e1/joined-square-check.json';raw=json.loads(source.read_text())
def decode(x):return {tri(tuple(map(tuple,t))) for t in x}
for label,P,U,Z in [('two',P2,u2,z2),('four',P4,u4,z4)]:
 rec=raw['paths'][label]
 assert P==[tuple(F(x) for x in p) for p in rec['path']]
 assert U==decode(rec['required']) and Z==decode(rec['forbidden'])
# Earlier accepted four/six receipt must still be the identical optical input.
oldsource=PEER/'mixed-e2-e1/joined-four-check.json'
oldreview=json.loads((BASE/'surplus-four-local/joined-six-review/check.json').read_text())
assert hashlib.sha256(oldsource.read_bytes()).hexdigest()==oldreview['source_sha256'][str(oldsource.relative_to(BASE))]
inputs=[source,PEER/'mixed-e2-e1/joined-square.txt',PEER/'mixed-e2-e1/joined-square-check.py',oldsource,PEER/'mixed-e2-e1/argument.txt',PEER/'mixed-e2-e1/critical-B.txt',BASE/'surplus-four-local/joined-six-review/review.txt',BASE/'surplus-four-local/mixed-critical-B-review/review.txt',BASE/'surplus-four-local/mixed-Beast-four-review/review.txt',BASE/'surplus-four-local/two-bounce-review/review.txt']
receipt={'status':'PASS','two':r2,'four':r4,'square_exchange':'strict same entry/exit and tangent/normal velocity','floor_exterior_mate':'remote(0,-4) sector1, outsideK','D_support':'two requiresD2/D3 crossing; four U AND Z avoid ENTIRE D star','applications':applications,'accepted_join':'previous accepted seven-window b0 classification + Beast<=13 + west/rectangle<=2 + O3/H4<=7 + O4ordinaryTc<=4 and previousTcunit<=7 => entire criticalB/E allroot mixed<=13','source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Fixed optical proofs only; previous classification/forcing/row reduction/Tcunit and sigma inherited. No new room, cap census, ray/word search or peer script execution. Does not accept separate Beast012 b1 consolidation.'}
(OUT/'check.json').write_text(json.dumps(receipt,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['source_sha256','checker_sha256']},indent=2,default=str))
