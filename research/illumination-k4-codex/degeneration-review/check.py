"""Exact deterministic geometry of a shrinking-overlap limit, no optics search."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json
B=Path(__file__).resolve().parent

def polygon(e):return [(-1,-1),(e,-1),(e,0),(1,0),(1,1),(0,1),(0,e),(-1,e)]
def area2(v):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(v,v[1:]+v[:1]))
def inside(p,v):
 parity=False
 for a,b in zip(v,v[1:]+v[:1]):
  if (a[1]>p[1])!=(b[1]>p[1]):
   if a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])>p[0]:parity=not parity
 return parity

def simple(v):
 edges=list(zip(v,v[1:]+v[:1]));assert len(set(v))==len(v)
 for i,(a,b) in enumerate(edges):
  assert (a[0]==b[0])!=(a[1]==b[1])
  c=v[(i+2)%len(v)];assert (b[0]-a[0])*(c[1]-b[1])!=(b[1]-a[1])*(c[0]-b[0])
  for j,(c,d) in enumerate(edges):
   if j<=i or j==i+1 or (i==0 and j==len(v)-1):continue
   vertical=a[0]==b[0];othervertical=c[0]==d[0]
   if vertical==othervertical:
    axis=1 if vertical else 0;fixed=1-axis
    hit=a[fixed]==c[fixed] and max(min(a[axis],b[axis]),min(c[axis],d[axis]))<=min(max(a[axis],b[axis]),max(c[axis],d[axis]))
   else:
    if vertical:vert=(a,b);horiz=(c,d)
    else:vert=(c,d);horiz=(a,b)
    hit=min(horiz[0][0],horiz[1][0])<=vert[0][0]<=max(horiz[0][0],horiz[1][0]) and min(vert[0][1],vert[1][1])<=horiz[0][1]<=max(vert[0][1],vert[1][1])
   assert not hit,(i,j)
 return True

if __name__=='__main__':
 controls=[];s=(F(-1,2),F(-1,2));t=(F(1,2),F(1,2))
 for n in (2,4,8,16,32,64):
  e=F(1,n);v=polygon(e);assert simple(v) and inside(s,v) and inside(t,v)
  assert area2(v)/2==2+2*e
  # The entire diagonal source-target segment lies inside the approximant.
  # For u<=e it is in square[-1,e]^2; for u>=0 it is in square[0,1]^2;
  # these intervals overlap because e>0.
  assert e>0
  controls.append(dict(epsilon=str(e),walls=8,area=str(area2(v)/2),simple=True,approximant_pair='DIRECTLY_LIT'))
 # Limits of the two squares meet only at the origin.
 intersection=((max(-1,0),min(0,1)),(max(-1,0),min(0,1)))
 assert intersection==((0,0),(0,0))
 # The Hausdorff distance to the union of the two limit squares is <=sqrt(2)*e.
 # The entire family can also be normalized to diameter1 without changing walls.
 result=dict(status='PASS',controls=controls,limit='[-1,0]^2 union [0,1]^2',collapse_blocker=[0,0],limit_interior_components=2,marked_points=[list(map(str,s)),list(map(str,t))],upper_bound_on_weight=8,
 conclusion='Every connecting continuous path in the limit crosses the blocked contact, yet it has8-wall strictly simple approximants. This disproves a lower weight bound over all blocked limits; it is NOT a limit of dark approximants or a sub22 dark simple room.')
 (B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
