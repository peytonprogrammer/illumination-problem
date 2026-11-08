"""One analytically prescribed room and symbolic periodic path family.
No room, direction, word, cylinder or trajectory discovery scan.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
base=Path(__file__).resolve().parent
ring=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,count):
 return [tuple(sorted((a,(a[0]+ring[j%8][0],a[1]+ring[j%8][1]),
             (a[0]+ring[(j+1)%8][0],a[1]+ring[(j+1)%8][1]))))
         for j in range(start,start+count)]
room=[]
for args in [((-4,0),0,8),((0,0),0,8),((-2,0),0,4),
             ((-2,2),6,1),((2,0),3,1),((0,2),6,2),((0,-2),1,1),
             ((-6,0),0,1),((-4,2),6,1),((-4,-2),2,1)]:
 room+=fan(*args)
data={'triangles':room,'marked':[(-4,0),(0,0)],'require_simple':True}
source=base.parent/'k5-proof-pilot/inputs/illumination_geometry.py'
spec=importlib.util.spec_from_file_location('frozen_geometry',source);geom=importlib.util.module_from_spec(spec);spec.loader.exec_module(geom)
receipt=geom.check(data,strict=True)
assert receipt['tiles']==28 and receipt['walls']==25
assert set(map(tuple,receipt['interior_A']))=={(-4,0),(0,0)}
assert receipt['sectors']['(1, 1)']==[5] and receipt['sectors']['(1, 0)']==[6]
# Affine polynomials c + a*A + t*T, stored exactly as triples.
def poly(c=0,a=0,t=0):return tuple(map(F,(c,a,t)))
def plus(f,g):return tuple(x+y for x,y in zip(f,g))
def neg(f):return tuple(-x for x in f)
def minus(f,g):return plus(f,neg(g))
def scale(k,f):return tuple(F(k)*x for x in f)
def point(x,y):return (x,y)
def constpoint(x,y):return (poly(x),poly(y))
def psub(p,q):return tuple(minus(x,y) for x,y in zip(p,q))
def padd(p,q):return tuple(plus(x,y) for x,y in zip(p,q))
def pscale(k,p):return tuple(scale(k,f) for f in p)
def ref(p,n,c):
 value=minus(plus(scale(n[0],p[0]),scale(n[1],p[1])),c)
 return tuple(minus(p[i],scale(F(2*n[i],sum(x*x for x in n)),value)) for i in range(2))
D=((1,1),poly(2,0,1))
mirrors=[((0,1),poly(-1)),((1,0),poly(-1)),((1,0),poly(1)),
         ((0,1),poly(2)),((1,0),poly(0)),((0,1),poly(0,0,1))]
d0=point(poly(F(3,2),F(-1,2),F(1,2)),poly(F(1,2),F(1,2),F(1,2)))
d1=point(poly(F(3,2),F(1,2),F(-1,2)),poly(F(1,2),F(-1,2),F(3,2)))
points=[d0,point(poly(0,-1),poly(-1)),point(poly(-1),poly(0,-1)),
 point(poly(1),poly(2,-1)),point(poly(1,-1),poly(2)),
 point(poly(0),poly(1,1)),point(poly(1,1,-1),poly(0,0,1)),d1]
times=[poly(F(3,2),F(1,2),F(1,2)),poly(1,-1),poly(2),poly(0,1),
       poly(1,-1),poly(1,1,-1),poly(F(1,2),F(-1,2),F(1,2))]
v=(-1,-1)
for i,tau in enumerate(times):
 assert psub(points[i+1],points[i])==tuple(scale(vv,tau) for vv in v)
 if i<len(mirrors):
  n,c=mirrors[i];hit=points[i+1]
  assert plus(scale(n[0],hit[0]),scale(n[1],hit[1]))==c
  v=tuple(v[k]-F(2*sum(v[j]*n[j] for j in range(2))*n[k],sum(z*z for z in n)) for k in range(2))
assert tuple(sum(t[k] for t in times) for k in range(3))==poly(7)
assert v==(1,1) and ref(d0,*D)==d0 and ref(d1,*D)==d1
# All affine inequalities hold on |t|<=min(a,1-a)/8 by checking its four
# vertices. This is a prescribed convex-domain identity, not a parameter scan.
domain=[(F(0),F(0)),(F(1,2),F(1,16)),(F(1),F(0)),(F(1,2),F(-1,16))]
def evaluate(f,a,t):return f[0]+f[1]*a+f[2]*t
def nonnegative(f):assert all(evaluate(f,a,t)>=0 for a,t in domain),f
def rectangle(p,x0,x1,y0,y1):
 for f in [minus(p[0],poly(x0)),minus(poly(x1),p[0]),minus(p[1],poly(y0)),minus(poly(y1),p[1])]:nonnegative(f)
def pocket(p):
 for f in [minus(p[0],poly(1)),minus(p[1],poly(0,0,1)),minus(poly(2,0,1),plus(*p))]:nonnegative(f)
Y=point(poly(1),poly(0,1));U=point(poly(0,1),poly(1))
for p in [d0,Y,points[6],d1]:pocket(p)
for p in [Y,points[1],points[2],U]:rectangle(p,-1,1,-1,1)
for p in [U,points[3],points[4],points[5]]:rectangle(p,0,1,1,2)
for tau in times:nonnegative(tau)
# Portal split points are on the prescribed segments, by identical diagonal
# slope and coordinate order; convexity gives containment on each subsegment.
assert psub(Y,d0)[0]==psub(Y,d0)[1]
assert psub(U,points[2])[0]==psub(U,points[2])[1]
assert psub(U,points[5])[0]==neg(psub(U,points[5])[1])
assert psub(Y,U)[0]==neg(psub(Y,U)[1])
assert psub(points[6],Y)[0]==neg(psub(points[6],Y)[1])
def G(p):
 for mirror in reversed(mirrors):p=ref(p,*mirror)
 return p
gd=G(d1)
assert gd==padd(d0,constpoint(-7,-7))
# Three affine basis points prove the full plane-isometry identity for all t.
for p in [constpoint(0,0),constpoint(1,0),constpoint(0,1)]:
 assert G(p)==point(minus(poly(-4),p[0]),minus(poly(-6,0,2),p[1]))
 assert G(G(p))==p
 assert G(ref(G(ref(p,*D)),*D))==padd(p,constpoint(-14,-14))
out=dict(status='PRESCRIBED_RAW_ROOM_AND_SYMBOLIC_DIAGONAL_BLINDNESS_PASS',
 geometry=receipt,room=data,symbolic_bracket_time=7,full_period_vector=[-14,-14],period_derivative=[0,0],
 parameter_domain='0<a<1; sufficiently small |t|<min(a,1-a)/8',
 fixed_mirror_count=5,moving_AC_bounce='H_t:y=t',
 normal_family_formula=[str(p) for p in points],
 independent_review='ACCEPTED_SCOPED_HAND_PROOF',universal_goal_counterexample=False,
 scope='One prescribed actual raw25wall two-mark room; all-diagonal-cylinder coverage needs the hand proof.',discovery_runs=0)
(base/'pocket-diagonal-load.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['room','geometry','normal_family_formula']},indent=2))
print('geometry',receipt['walls'],'walls',receipt['tiles'],'triangles; strictraw PASS')
