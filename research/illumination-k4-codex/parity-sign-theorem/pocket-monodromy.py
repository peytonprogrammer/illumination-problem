"""Prescribed finite-group/period controls only. No origami orbit or ray search."""
from pathlib import Path
from fractions import Fraction as F
from collections import deque
import hashlib,json,sys
if not __debug__:
    raise SystemExit('Optimized Python disables proof assertions; rerun without -O.')
B=Path(__file__).resolve().parent
COUPLING_PIN='9f81b7bf93b258958fa3d6347631e50f8165e57ad32166547431a3be9ed26bec'
assert hashlib.sha256((B/'coupling.json').read_bytes()).hexdigest()==COUPLING_PIN
I=((F(1),F(0)),(F(0),F(1))); Z=(F(0),F(0))
def ap(A,x):return tuple(sum(A[i][j]*x[j] for j in range(2)) for i in range(2))
def mm(A,C):return tuple(tuple(sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def reflection(n,h,dh):
 n=tuple(map(F,n));den=sum(x*x for x in n)
 return tuple(tuple(I[i][j]-2*n[i]*n[j]/den for j in range(2)) for i in range(2)),tuple(2*h*x/den for x in n),tuple(2*dh*x/den for x in n)
def develop(fs):
 R,b,db=I,Z,Z
 for M,q,dq in fs:
  b=add(b,ap(R,q));db=add(db,ap(R,dq));R=mm(R,M)
 return R,b,db
saved=json.loads((B/'coupling.json').read_text());V=[tuple(map(F,p)) for p in saved['room']['vertices']]
h=list(map(F,saved['offset_base_point']));normals=saved['offset_normals']
dh=[F(0)]*len(V);dh[2]=-F(1);dh[3]=F(1)
mirrors=[reflection(n,h[i],dh[i]) for i,n in enumerate(normals)]
assert V[2:5]==[(1,1),(2,2),(1,2)]
assert normals[1]==[-1,0] and h[1]==-1
assert normals[2]==[-1,1] and h[2]==0
assert normals[3]==[0,-1] and h[3]==-2
# V_1 D H D = V_1 R_{x=2}, where R_{x=2} is a virtual mirror.
# Reduce the conjugate word by canceling its terminal D D.
wx=(1,2,3,2);wy=(2,1,2,3)
Rx,bx,dx=develop([mirrors[i] for i in wx]);Ry,by,dy=develop([mirrors[i] for i in wy])
assert Rx==Ry==I and bx==(-2,0) and by==(0,-2) and dx==dy==Z
# Every canonical reflection has an even integral translation at the grid base.
assert all(all(x.denominator==1 and int(x)%2==0 for x in m[1]) for m in mirrors)

# Bind each mirror to the actual positive-length edge at the grid base.
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def point_segment_d2(p,a,b):
 d=sub(b,a);v=sub(p,a);den=dot(d,d);assert den>0
 q=max(F(0),min(F(1),dot(v,d)/den))
 z=sub(v,tuple(q*x for x in d));return dot(z,z)
def orient(a,b,c):return cross(sub(b,a),sub(c,a))
def segments_disjoint(a,b,c,d):
 x,y,z,w=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
 if x*y<0 and z*w<0:return False
 return min(point_segment_d2(a,c,d),point_segment_d2(b,c,d),point_segment_d2(c,a,b),point_segment_d2(d,a,b))>0
nonadjacent=[(i,j) for i in range(len(V)) for j in range(i+1,len(V)) if (j-i)%len(V) not in (1,len(V)-1)]
for i,n in enumerate(normals):
 assert dot(n,V[i])==dot(n,V[(i+1)%len(V)])==h[i]
 assert dot(sub(V[i],V[(i+1)%len(V)]),sub(V[i],V[(i+1)%len(V)]))>0
minimum_d2=None
for i,j in nonadjacent:
 a,b=V[i],V[(i+1)%len(V)];c,d=V[j],V[(j+1)%len(V)]
 assert segments_disjoint(a,b,c,d)
 d2=min(point_segment_d2(a,c,d),point_segment_d2(b,c,d),point_segment_d2(c,a,b),point_segment_d2(d,a,b))
 minimum_d2=d2 if minimum_d2 is None else min(minimum_d2,d2)
ell=min(abs(V[2][1]-V[1][1]),abs(V[5][1]-V[4][1]))
epsilon_squared=min(minimum_d2,ell*ell)/16
assert epsilon_squared>0

# One prescribed exterior -I word, using fixed walls x=1 and y=0.
# Composing it with the pocket half-turn gives an absolute period with
# exact affine dependence (-2,-4+2t), not merely a nonzero derivative.
assert normals[0]==[0,1] and h[0]==0 and dh[0]==dh[1]==0
arithmetic_word=(1,0,2,3,2,3)
Ra,ba,da=develop([mirrors[i] for i in arithmetic_word])
assert Ra==I and ba==(-2,-4) and da==(0,2)
for t in (F(-1,100),F(0),F(1,100)):
 changed=[reflection(n,h[i]+t*dh[i],dh[i]) for i,n in enumerate(normals)]
 Rt,bt,dt=develop([changed[i] for i in arithmetic_word])
 assert Rt==I and bt==(-2,-4+2*t) and dt==da
 assert t*t<epsilon_squared
 vertices=[(x,y-t if i in (2,3,4) else y) for i,(x,y) in enumerate(V)]
 for i,n in enumerate(normals):
  assert dot(n,vertices[i])==dot(n,vertices[(i+1)%len(V)])==h[i]+t*dh[i]
  assert vertices[i]!=vertices[(i+1)%len(V)]
 for i,j in nonadjacent:
  assert segments_disjoint(vertices[i],vertices[(i+1)%len(V)],vertices[j],vertices[(j+1)%len(V)])

# Explicit connected six-square unramified double cover of the three-square L.
# Square labels 2*i+epsilon, i a base square and epsilon in {0,1}.
r=(0,1,5,4,2,3);u=(2,3,0,1,4,5)
r0=(0,2,1);u0=(1,0,2)
def comp(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inv(a):
 q=[0]*len(a)
 for i,j in enumerate(a):q[j]=i
 return tuple(q)
def cycles(a):
 seen=set();out=[]
 for i in range(len(a)):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=a[j]
  assert j==i;out.append(tuple(c))
 return out
assert sorted(r)==sorted(u)==list(range(6))
assert all(r[i]//2==r0[i//2] and u[i]//2==u0[i//2] for i in range(6))
# Connectedness of this prescribed six-state graph, not a surface search.
seen={0};todo=deque([0])
while todo:
 x=todo.popleft()
 for y in (r[x],u[x]):
  if y not in seen:seen.add(y);todo.append(y)
assert len(seen)==6
blocks=[frozenset((2*i,2*i+1)) for i in range(3)]
for perm in (r,u):
 assert all(frozenset(perm[x] for x in block) in blocks for block in blocks)
comm=comp(u,comp(r,comp(inv(u),inv(r))))
comm0=comp(u0,comp(r0,comp(inv(u0),inv(r0))))
assert sorted(map(len,cycles(comm)))==[3,3] and sorted(map(len,cycles(comm0)))==[3]
# Each upstairs cone cycle projects bijectively onto the base cone cycle: no new ramification.
for c in cycles(comm):assert len({x//2 for x in c})==3
assert r[0]==0 and u[4]==4
# A horizontal core in square0 has period(1,0); vertical core in square4 period(0,1).
# All square-tiled periods are integral, so the absolute period lattice is exactly Z^2.
assert (6-len(cycles(comm)))%2==0
up_genus=1+(6-len(cycles(comm)))//2
base_genus=1+(3-len(cycles(comm0)))//2
assert up_genus==3 and base_genus==2 and 2-2*up_genus==2*(2-2*base_genus)

# Prescribed SL(2,F7) regular-cover obstruction to a BROADER realization claim.
# This is matrix algebra, not a search over polygon rooms or primitive words.
mod=7
J=(1,0,0,1)
def gm(a,b):
 return ((a[0]*b[0]+a[1]*b[2])%mod,(a[0]*b[1]+a[1]*b[3])%mod,
         (a[2]*b[0]+a[3]*b[2])%mod,(a[2]*b[1]+a[3]*b[3])%mod)
def gi(a):return (a[3]%mod,-a[1]%mod,-a[2]%mod,a[0]%mod)
def gp(a,n):
 if n<0:return gp(gi(a),-n)
 ans=J
 for _ in range(n):ans=gm(ans,a)
 return ans
def gc(a,b):return gm(gm(gm(a,b),gi(a)),gi(b))
r7=(1,1,0,1);u7=(1,0,2,1);z7=(6,0,0,6);diag=(2,0,0,4)
all_sl2={(a,b,c,d) for a in range(7) for b in range(7) for c in range(7) for d in range(7) if (a*d-b*c)%7==1}
assert len(all_sl2)==336
# Fixed finite generator graph verifies this prescribed group, retaining no words.
seen7={J};todo7=deque([J])
while todo7:
 x=todo7.popleft()
 for y in (gm(x,r7),gm(x,u7)):
  if y not in seen7:seen7.add(y);todo7.append(y)
assert seen7==all_sl2
assert gm(gm(gp(r7,2),gp(u7,5)),gp(r7,2))==(0,2,3,0)
assert gm(gm(gp(r7,6),gp(u7,4)),gp(r7,6))==(0,6,1,0)
dword=gm(gm(gm(gp(r7,2),gp(u7,5)),gp(r7,2)),gm(gm(gp(r7,6),gp(u7,4)),gp(r7,6)))
assert dword==diag
assert gc(diag,gp(r7,5))==r7 and gc(diag,u7)==u7
# Hence both group generators are commutators, so this entire group is perfect.
assert z7!=J and gp(z7,2)==J and all(gm(z7,x)==gm(x,z7) for x in all_sl2)
comm7=gc(r7,u7)
assert comm7==(0,5,4,6) and gp(comm7,3)==J and comm7!=J
# Cover periods: a commutator word has zero exponent sums. The following
# matrix identities prove that r*[d,r^5]^-1 and u*[d,u]^-1 lie in the kernel;
# their exponent sums are (1,0),(0,1), respectively.
assert gm(r7,gi(gc(diag,gp(r7,5))))==J
assert gm(u7,gi(gc(diag,u7)))==J
regular_degree=336;ramification_order=3
regular_genus=1+(regular_degree-regular_degree//ramification_order)//2
assert regular_genus==113

def clean(x):
 if isinstance(x,F):return int(x) if x.denominator==1 else str(x)
 if isinstance(x,(tuple,list)):return [clean(y) for y in x]
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 return x
out=clean(dict(status='PASS',coupling_sha256=COUPLING_PIN,
 pocket_period_controls=dict(x_word=wx,y_word=wy,periods=[bx,by],slide_derivatives=[dx,dy],base_mirror_translations_even=True,arithmetic_word=arithmetic_word,arithmetic_period_at_zero=ba,arithmetic_slide_derivative=da,arithmetic_exact_affine_checks=3,geometry_minimum_nonadjacent_distance_squared=minimum_d2,geometry_epsilon_squared=epsilon_squared,geometry_incidence_and_positive_lengths=True,geometry_simplicity_checks=3),
 perfect_central_obstruction=dict(modulus=7,degree=regular_degree,genus=regular_genus,r=r7,u=u7,central_target=z7,commutator=comm7,ramification_order=ramification_order,diagonal_commutator_witness=diag,full_period_kernel_basis=[(1,0),(0,1)],scope='General marked translation-surface control, not a raw-parity polygon. Primitive free-group element cannot map to nontrivial central target in a nonabelian two-generated quotient.'),
 full_period_imprimitive_control=dict(r=r,u=u,base_r=r0,base_u=u0,connected_squares=6,blocks=[sorted(x) for x in blocks],cone_cycles=cycles(comm),base_cone_cycles=cycles(comm0),genus=up_genus,base_genus=base_genus,period_basis=[(1,0),(0,1)],unramified_degree=2),
 scope='Two prescribed reflection-loop identities, one prescribed six-square control, and one prescribed SL2(F7) regular-cover control. The control is not asserted to be a raw parity room or a counterexample to pocket detection. No rays, directions, event words or surface orbits searched.'))
(B/'pocket-monodromy.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
