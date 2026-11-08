"""Independent, theory-bounded fixed-class exhaustion. No optical tracing.
Affine translations and triangle vertices use coordinates scaled by two.
"""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as F
from math import gcd
import json,hashlib,time
B=Path(__file__).resolve().parent;ID=(1,0,0,1,0,0)
def apply(g,p):a,b,c,d,e,f=g;return(a*p[0]+b*p[1]+e,c*p[0]+d*p[1]+f)
def compose(g,h):
 a,b,c,d,e,f=g;A,D,C,E,x,y=h
 return(a*A+b*C,a*D+b*E,c*A+d*C,c*D+d*E,a*x+b*y+e,c*x+d*y+f)
def reflect(p,q):
 dx,dy=q[0]-p[0],q[1]-p[1];z=gcd(abs(dx),abs(dy));nx,ny=-dy//z,dx//z;norm=nx*nx+ny*ny;v=nx*p[0]+ny*p[1]
 vals=(1-F(2*nx*nx,norm),-F(2*nx*ny,norm),-F(2*nx*ny,norm),1-F(2*ny*ny,norm),F(2*nx*v,norm),F(2*ny*v,norm));assert all(v.denominator==1 for v in vals);return tuple(map(int,vals))
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def on(a,b,p):return cross(sub(b,a),sub(p,a))==0 and all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1))
def inside(V,p):
 if any(on(a,b,p) for a,b in zip(V,V[1:]+V[:1])):return False
 w=0
 for a,b in zip(V,V[1:]+V[:1]):
  if a[1]<=p[1]<b[1] and cross(sub(b,a),sub(p,a))>0:w+=1
  if b[1]<=p[1]<a[1] and cross(sub(b,a),sub(p,a))<0:w-=1
 return bool(w)
def triangles(V):
 out=set()
 for x in range(min(x for x,y in V),max(x for x,y in V)):
  for y in range(min(y for x,y in V),max(y for x,y in V)):
   c=(2*x+1,2*y+1);corners=[(2*x,2*y),(2*x+2,2*y),(2*x+2,2*y+2),(2*x,2*y+2)]
   for i in range(4):
    t=tuple(sorted((c,corners[i],corners[(i+1)%4])));p=(sum(a for a,b in t)/6,sum(b for a,b in t)/6)
    # Use exact centroid instead of floating point.
    p=(F(sum(a for a,b in t),6),F(sum(b for a,b in t),6))
    if inside(V,p):out.add(t)
 return frozenset(out)
def edges(T):
 d=defaultdict(list)
 for t in T:
  for i in range(3):d[tuple(sorted((t[i],t[(i+1)%3])))].append(t)
 return d
def polygon(T):
 adj=defaultdict(set)
 for (a,b),ts in edges(T).items():
  assert len(ts)<=2
  if len(ts)==1:adj[a].add(b);adj[b].add(a)
 if any(len(ns)!=2 for ns in adj.values()):return None
 start=min(adj);v=start;old=None;cycle=[]
 while True:
  cycle.append(v);q=min(adj[v]-({old} if old is not None else set()))
  if q==start:break
  if q in cycle:return None
  old,v=v,q
 if len(cycle)!=len(adj):return None
 return [p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
def shape(V):
 out=[]
 for swap in (False,True):
  for sx in (-1,1):
   for sy in (-1,1):
    T=[(sx*(y if swap else x),sy*(x if swap else y)) for x,y in V];ox=min(x for x,y in T);oy=min(y for x,y in T);T=[(x-ox,y-oy) for x,y in T]
    for C in [T,T[::-1]]:
     i=C.index(min(C));out.append(tuple(C[i:]+C[:i]))
 return min(out)
def parse(text):
 result=[]
 for line in text.splitlines():
  z=line.split();result.append((int(z[0]),int(z[1]),[tuple(map(int,p.split(','))) for p in z[2:]]))
 return result
start=time.monotonic();raw=(B/'base-replay.txt').read_text();supplied=(B/'inputs/bases-W12.txt').read_text();assert Counter(raw.splitlines())==Counter(supplied.splitlines())
bases=parse(raw);assert Counter(w for w,n,V in bases)=={9:8,10:52,11:128,12:224}
known=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
knownkey=shape([(2*x,2*y) for x,y in known]);receipt=[];positives=[];below=[]
for index,(w,n,V) in enumerate(bases):
 base=triangles(V);base_edges=list(edges(base));mirrors=[reflect((2*a[0],2*a[1]),(2*b[0],2*b[1])) for a,b in zip(V,V[1:]+V[:1])];cap=(22-4)//(w-4)
 marks=[]
 for x in range(min(x for x,y in V),max(x for x,y in V)+1):
  for y in range(min(y for x,y in V),max(y for x,y in V)+1):
   if (x,y) not in V and x%2==y%2==0 and (inside(V,(x,y)) or any(on(a,b,(x,y)) for a,b in zip(V,V[1:]+V[:1]))):marks.append((2*x,2*y))
 assert len(marks)==n
 seen=set();cache={ID:base};counts=Counter()
 def cells(g):
  if g not in cache:cache[g]=frozenset(tuple(sorted(apply(g,p) for p in t)) for t in base)
  return cache[g]
 def visit(gs,U):
  key=frozenset(gs)
  if key in seen:return
  seen.add(key);counts['states']+=1
  if len(gs)>1:
   counts['evaluated']+=1;poly=polygon(U)
   if poly is not None:
    owners=defaultdict(set)
    for g in gs:
     for a,b in base_edges:owners[tuple(sorted((apply(g,a),apply(g,b))))].add(g)
    coherent=True
    for (a,b),own in owners.items():
     if len(own)>1:
      assert len(own)==2;g,h=tuple(own)
      if compose(reflect(a,b),g)!=h:coherent=False;break
    if coherent:
     counts['coherent_simple']+=1
     incident=Counter(p for t in U for p in t)
     lifts={mk:sorted({apply(g,mk) for g in gs if incident[apply(g,mk)]==8}) for mk in marks}
     live=[mk for mk in marks if lifts[mk]]
     if len(live)>=2 and len(poly)<=22:
      record=dict(base_index=index,base_walls=w,copies=len(gs),walls=len(poly),vertices_scaled2=poly,copy_maps_scaled2=gs,base_marks_scaled2=live,lifts_scaled2={str(k):lifts[k] for k in live})
      positives.append(record)
      if len(poly)<22:below.append(record)
      else:assert shape(poly)==knownkey
  if len(gs)==cap:return
  # Precomposition by every base wall reflection is independent of peer's
  # world-wall implementation and spans the connected adjacency graph.
  for g in gs:
   for r in mirrors:
    h=compose(g,r)
    if h in key:continue
    C=cells(h)
    if not C&U:visit(gs+(h,),U|C)
 visit((ID,),base);receipt.append(dict(base=index,walls=w,marks=n,copy_cap=cap,counts=dict(counts)))
 if index%50==49:print(json.dumps(dict(bases=index+1,positive_controls=len(positives),below22=len(below),elapsed_seconds=round(time.monotonic()-start,2))),flush=True)
assert not below;assert len(positives)==12
result=dict(status='PASS',source_bases=len(bases),base_replay_matches_saved_multiset=True,positive_22_controls=len(positives),all_positive_shapes_match_known=True,below22=below,totals=dict(sum((Counter(r['counts']) for r in receipt),Counter())),per_base=receipt,positive_controls=positives,elapsed_seconds=round(time.monotonic()-start,3),scope='Complete independent finite full-wall fold replay through W22 for supplied bases, with fresh frozen-source base enumeration. m=1 exclusion uses earlier audited parity result. No optical search.')
(B/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['per_base','positive_controls']},indent=2))
