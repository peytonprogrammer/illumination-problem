"""First-order rigidity of a dark orthogonal room (exact rationals).

Parameters theta = (v0x, v0y, l_0..l_{W-1}, sx, sy, tx, ty); vertex k = v0 + sum_{i<k} l_i d_i.
An event is a billiard path s -> t whose only corner contact is one convex 90-degree corner c
(a regular point of the unfolded surface, so the path continues straight through it in the unfolding).
Darkness that persists along a deformation needs det(t'-s, c'-s) == 0 along it; its gradient is a
linear functional. If the gradients span everything except the 4 symmetry directions
(2 translations, 2 axis stretches) on the closure subspace, every other deformation lights the room.
"""
from fractions import Fraction as Fr
import json,sys
V=[(-1,-1),(-1,1),(0,1),(0,2),(1,2),(1,3),(3,3),(3,2),(4,2),(4,1),(5,1),(5,0),(3,0),(3,1),(1,1),(1,-1),(2,-1),(2,-3),(1,-3),(1,-2),(0,-2),(0,-1)]
S=(0,0);T=(2,2);RMAX=int(sys.argv[1]) if len(sys.argv)>1 else 8;BOUNCES=400
W=len(V);D=2+W+4;IS,IT=2+W,2+W+2
def unit(i):e=[Fr(0)]*D;e[i]=Fr(1);return e
def add(a,b):return [x+y for x,y in zip(a,b)]
def sc(k,a):return [k*x for x in a]
zero=[Fr(0)]*D
# linear forms for vertex coordinates
VX=[];VY=[];cx,cy=unit(0),unit(1)
for k in range(W):
 VX.append(cx);VY.append(cy)
 dx=V[(k+1)%W][0]-V[k][0];dy=V[(k+1)%W][1]-V[k][1]
 # l_k is the signed length; it multiplies the unit direction of edge k
 if dx:cx=add(cx,unit(2+k))
 else:cy=add(cy,unit(2+k))
theta0=[Fr(V[0][0]),Fr(V[0][1])]+[Fr((V[(k+1)%W][0]-V[k][0]) or (V[(k+1)%W][1]-V[k][1])) for k in range(W)]+[Fr(S[0]),Fr(S[1]),Fr(T[0]),Fr(T[1])]
def ev(f):return sum(a*b for a,b in zip(f,theta0))
assert all(ev(VX[k])==V[k][0] and ev(VY[k])==V[k][1] for k in range(W))
area2=sum(V[i][0]*V[(i+1)%W][1]-V[(i+1)%W][0]*V[i][1] for i in range(W));o=1 if area2>0 else -1
convex={}
for i in range(W):
 a,b,c=V[i-1],V[i],V[(i+1)%W];cr=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]);convex[b]=(cr*o>0)
vidx={v:i for i,v in enumerate(V)}
edges=[(V[i],V[(i+1)%W],i) for i in range(W)]

R_LOC=Fr(1,1000);ETA=Fr(1,10**7)
def local_exit(k,d,side):
 """Offset ray past corner k on the given side; return (list of 'v'/'h' reflections, exit direction)."""
 c=V[k];prev=V[k-1];nxt=V[(k+1)%W]
 walls=[]
 for o_ in (prev,nxt):
  e=((o_[0]>c[0])-(o_[0]<c[0]),(o_[1]>c[1])-(o_[1]<c[1]));walls.append(('v' if e[0]==0 else 'h',e))
 n=(-d[1],d[0]) if side>0 else (d[1],-d[0])
 px=c[0]-R_LOC*d[0]+ETA*n[0];py=c[1]-R_LOC*d[1]+ETA*n[1];dd=d;refl=[]
 for _ in range(6):
  best=None
  for kind,e in walls:
   if kind=='v':
    if dd[0]==0:continue
    u=(c[0]-px)/dd[0];y=py+u*dd[1]
    if u>0 and (y-c[1])*e[1]>0 and abs(y-c[1])<=1:best=min(best,(u,kind)) if best else (u,kind)
   else:
    if dd[1]==0:continue
    u=(c[1]-py)/dd[1];x=px+u*dd[0]
    if u>0 and (x-c[0])*e[0]>0 and abs(x-c[0])<=1:best=min(best,(u,kind)) if best else (u,kind)
  if best is None or best[0]>4*R_LOC:break
  u,kind=best;px+=u*dd[0];py+=u*dd[1];refl.append(kind)
  dd=(-dd[0],dd[1]) if kind=='v' else (dd[0],-dd[1])
 return refl,dd
def nexthit(pos,d):
 best=None
 for a,b,i in edges:
  if a[0]==b[0]:
   if d[0]==0:continue
   u=(a[0]-pos[0])/d[0]
   if u<=0:continue
   y=pos[1]+u*d[1]
   if min(a[1],b[1])<=y<=max(a[1],b[1]) and (best is None or u<best[0]):best=(u,i,'v',(Fr(a[0]),y))
  else:
   if d[1]==0:continue
   u=(a[1]-pos[1])/d[1]
   if u<=0:continue
   x=pos[0]+u*d[0]
   if min(a[0],b[0])<=x<=max(a[0],b[0]) and (best is None or u<best[0]):best=(u,i,'h',(x,Fr(a[1])))
 return best
def run(pos,d,tf,contact,out,budget):
 for _ in range(budget):
  u,i,kind,hit=nexthit(pos,d)
  du=(T[0]-pos[0])/d[0] if d[0] else (T[1]-pos[1])/d[1]
  if 0<du<u and pos[0]+du*d[0]==T[0] and pos[1]+du*d[1]==T[1]:
   out.append(('lit' if contact is None else 'event',contact,tf));return
  for v in V:
   if v==hit:continue
   w=(v[0]-pos[0])/d[0] if d[0] else (v[1]-pos[1])/d[1]
   if 0<w<u and pos[0]+w*d[0]==v[0] and pos[1]+w*d[1]==v[1]:return  # grazing contact: drop
  hv=(int(hit[0]),int(hit[1])) if hit[0].denominator==1 and hit[1].denominator==1 else None
  ex,ey,ax,ay=tf
  if hv in vidx:
   if contact is not None:return
   k=vidx[hv]
   if convex[hv]:
    ntf=(-ex,-ey,add(ax,sc(2*ex,VX[k])),add(ay,sc(2*ey,VY[k])))
    run(hit,(-d[0],-d[1]),ntf,(k,tf,0),out,budget);return
   for side in (1,-1):
    refl,nd=local_exit(k,d,side);nex,ney,nax,nay=ex,ey,ax,ay
    for r in refl:
     if r=='v':nax=add(nax,sc(2*nex,VX[k]));nex=-nex
     else:nay=add(nay,sc(2*ney,VY[k]));ney=-ney
    run(hit,nd,(nex,ney,nax,nay),(k,tf,side*ex*ey),out,budget)
   return
  if kind=='v':tf=(-ex,ey,add(ax,sc(2*ex,VX[i])),ay);d=(-d[0],d[1])
  else:tf=(ex,-ey,ax,add(ay,sc(2*ey,VY[i])));d=(d[0],-d[1])
  pos=hit
def apply(tf,qx,qy):ex,ey,ax,ay=tf;return (add(sc(ex,qx),ax),add(sc(ey,qy),ay))
from math import gcd
funcs=[];events=[];lit=[]
for p in range(-RMAX,RMAX+1):
 for q in range(-RMAX,RMAX+1):
  if (p,q)==(0,0) or gcd(abs(p),abs(q))!=1:continue
  out=[];run((Fr(S[0]),Fr(S[1])),(p,q),(1,1,zero,zero),None,out,BOUNCES)
  for status,contact,tf in out:
   if status=='lit':lit.append((p,q));continue
   k,tfc,side=contact
   cxf,cyf=apply(tfc,VX[k],VY[k]);txf,tyf=apply(tf,unit(IT),unit(IT+1));sx,sy=unit(IS),unit(IS+1)
   A=(add(txf,sc(-1,sx)),add(tyf,sc(-1,sy)));B=(add(cxf,sc(-1,sx)),add(cyf,sc(-1,sy)))
   a0=(ev(A[0]),ev(A[1]));b0=(ev(B[0]),ev(B[1]))
   assert a0[0]*b0[1]-a0[1]*b0[0]==0
   g=add(add(sc(b0[1],A[0]),sc(-b0[0],A[1])),add(sc(a0[0],B[1]),sc(-a0[1],B[0])))
   if all(x==0 for x in g):continue
   if side==0:funcs+= [g,sc(-1,g)]
   else:funcs.append(g if side>0 else sc(-1,g))
   events.append(dict(dir=[p,q],corner=list(V[k]),side=side))
# closure constraints and symmetry directions
clos=[ [Fr(0)]*2+[Fr(1) if (V[(k+1)%W][0]-V[k][0]) else Fr(0) for k in range(W)]+[Fr(0)]*4,
       [Fr(0)]*2+[Fr(1) if (V[(k+1)%W][1]-V[k][1]) else Fr(0) for k in range(W)]+[Fr(0)]*4 ]
def rank(M):
 M=[r[:] for r in M];rk=0;cols=len(M[0]) if M else 0
 for c in range(cols):
  piv=next((i for i in range(rk,len(M)) if M[i][c]!=0),None)
  if piv is None:continue
  M[rk],M[piv]=M[piv],M[rk]
  for i in range(len(M)):
   if i!=rk and M[i][c]!=0:
    f=M[i][c]/M[rk][c];M[i]=[x-f*y for x,y in zip(M[i],M[rk])]
  rk+=1
 return rk
# symmetry directions: tangent vectors of (x,y)->(x+e,y), (x,y+e), (x(1+e),y), (x,y(1+e))
def symvec(fx,fy):
 v=[fx(V[0][0],0),fy(V[0][1],0)]
 for k in range(W):
  dx=V[(k+1)%W][0]-V[k][0];dy=V[(k+1)%W][1]-V[k][1]
  v.append(fx(dx,1) if dx else fy(dy,1))
 return [Fr(x) for x in v+[fx(S[0],0),fy(S[1],0),fx(T[0],0),fy(T[1],0)]]
syms=[symvec(lambda x,l:0 if l else 1,lambda y,l:0),symvec(lambda x,l:0,lambda y,l:0 if l else 1),
      symvec(lambda x,l:x,lambda y,l:0),symvec(lambda x,l:0,lambda y,l:y)]
for g in funcs:
 for sv in syms:assert sum(a*b for a,b in zip(g,sv))==0,'symmetry not in kernel'
# rank of event functionals restricted to closure subspace = rank([rows;clos]) - rank(clos)
r_on=rank(funcs+clos)-rank(clos)
target=D-2-4
json.dump(dict(funcs=[[str(x) for x in f] for f in funcs],clos=[[str(x) for x in c] for c in clos],syms=[[str(x) for x in s] for s in syms]),open(f'funcs-R{RMAX}.json','w'))
out=dict(funcs=len(funcs),RMAX=RMAX,events=len(events),lit_paths=len(lit),rank_on_closure=r_on,target=target,rigid=(r_on==target),
         distinct_corners=sorted({tuple(e['corner']) for e in events}))
print(json.dumps(out))
json.dump(dict(out,event_list=events),open(f'rigidity-R{RMAX}.json','w'),indent=1)
