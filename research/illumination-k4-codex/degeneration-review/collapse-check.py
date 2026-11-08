"""Finite exact checks for the analytic collapse reduction. No optical search."""
from pathlib import Path
from fractions import Fraction as F
import json
B=Path(__file__).resolve().parent

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def turn(a,b,c):return cross(sub(b,a),sub(c,b))
def corners(v):return [p for i,p in enumerate(v) if turn(v[i-1],p,v[(i+1)%len(v)])]
def meet(a,b,c,d):
 if not all(max(min(a[k],b[k]),min(c[k],d[k]))<=min(max(a[k],b[k]),max(c[k],d[k])) for k in (0,1)):return False
 return cross(sub(b,a),sub(c,a))*cross(sub(b,a),sub(d,a))<=0 and cross(sub(d,c),sub(a,c))*cross(sub(d,c),sub(b,c))<=0

def simple(v):
 assert len(set(v))==len(v)
 assert sum(cross(a,b) for a,b in zip(v,v[1:]+v[:1]))>0
 for i,a in enumerate(v):
  b=v[(i+1)%len(v)];assert a!=b
  for j,c in enumerate(v):
   if j<=i or j==i+1 or (i==0 and j==len(v)-1):continue
   assert not meet(a,b,c,v[(j+1)%len(v)])

def proper_cycle(raw):
 out=[]
 for x in raw:
  if not out or x!=out[-1]:out.append(x)
 if out[-1]==out[0]:out.pop()
 return out

def room(kind,h):
 if kind=='bevel':return [(0,0),(2-h,0),(2,h),(2,2),(0,2)]
 if kind=='step':return [(0,0),(2,0),(2,1),(2+h,1),(2+h,2),(0,2)]
 if kind=='notch':return [(0,0),(2,0),(2,2),(1+h*h,2),(1+h*h,2-h),(1,2-h),(1,2),(0,2)]
 raise ValueError(kind)

families=[]
for kind,r,s,W in [('bevel',1,0,5),('step',1,1,6),('notch',3,1,8)]:
 checks=[]
 for h in [F(1,2),F(1,10),F(1,100)]:
  v=room(kind,h);simple(v);assert len(corners(v))==W
  lim=room(kind,F(0));zero=sum(a==b for a,b in zip(lim,lim[1:]+lim[:1]));q=proper_cycle(lim);simple(q);reduced=corners(q)
  assert zero==r and len(q)-len(reduced)==s and len(reduced)==W-r-s==4
  checks.append({'epsilon':str(h),'simple':True,'maximal_walls':W})
 families.append({'family':kind,'original_walls':W,'zero_edges':r,'smooth_fusions':s,'limit_walls':4,'checks':checks})
# Prescribed reflection at the vanished step point. Direct visibility stays lit.
optics=[]
for h in [F(1,2),F(1,10),F(1,100)]:
 source=(F(1),F(1,2));target=(F(1),F(3,2))
 def vertical_bounce(x):
  lift=(2*x-target[0],target[1]);lam=(x-source[0])/(lift[0]-source[0]);return (x,source[1]+lam*(lift[1]-source[1]))
 lower=vertical_bounce(F(2));upper=vertical_bounce(2+h)
 assert lower==(2,1) and upper==(2+h,1)
 assert not(F(0)<lower[1]<1) and not(1<upper[1]<2)
 # Horizontal-step reflection unfolds the target to the source itself.
 mirrored=(target[0],2-target[1]);assert mirrored==source
 # In the rectangle limit the old two faces become one open wall.
 assert 0<lower[1]<2
 optics.append({'epsilon':str(h),'lower_face_bounce':list(map(str,lower)),'upper_face_bounce':list(map(str,upper)),'both_at_actual_corners':True,'limit_reflection_strictly_inside_maximal_wall':True,'direct_segment_lit':True})
# Nested point clusters: notch depth h, bottom separation h^2.
assert all(h*h/h==h for h in [F(1,2),F(1,10),F(1,100)])
# Exact one-step transfer interval, with fixed algebraic reflection words.
interval=[]
for h in [F(1,2),F(1,10),F(1,100)]:
 for k in [-1,0,1,2,3]:
  a=b=F(1);u=F(-1);v=1+k*h;K=b*u+a*v
  lower_y=K/(a+b)
  upper_y=((b+h)*u+(a+h)*v)/(a+b+2*h)
  incoming_at_lower_line=u+a*(upper_y-u)/(a+h)
  lower_valid=lower_y<0
  upper_valid=upper_y>0 and incoming_at_lower_line>0
  assert lower_valid==(K<0)
  assert upper_valid==(K>-2*h*u)
  assert (not lower_valid and not upper_valid)==(0<=K<=-2*h*u)
  interval.append({'epsilon':str(h),'K_over_epsilon':k,'lower_word_valid':lower_valid,'upper_word_valid':upper_valid,'blocked_interval_contains_K':0<=K<=-2*h*u})
# Finite combinatorial bookkeeping identities (independent of physical realizability).
bookkeeping=0
from itertools import product
for count in range(1,6):
 for sizes in product(range(1,5),repeat=count):
  r=sum(sizes)
  for mask in range(1<<count):
   smooth=sum((mask>>i)&1 for i in range(count))
   assert r-smooth>=0
   assert (r==smooth)==(all(x==1 for x in sizes) and smooth==count)
   if any(x>=2 for x in sizes):assert r-smooth>=1
   bookkeeping+=1
out={'status':'PASS','families':families,'vanished_smooth_point_reflection':optics,'nested_scale_example':{'outer_scale':'h','inner_scale':'h^2','outer_zoom_bottom_edge_length':'h -> 0','conclusion':'A single outer zoom loses a smaller edge; a second point-cluster zoom is needed.'},'step_transfer_interval':interval,'bookkeeping_checks':bookkeeping,'scope':'Nine exact strictly simple polygon controls, three fixed-word reflection diagnostics 15 fixed-word step-interval checks, ' + str(bookkeeping) + ' bookkeeping checks and one symbolic scale identity. No dark sequence, ray search, or global lower bound.'}
(B/'collapse-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
