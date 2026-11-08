"""First-order rigidity of a dark room with walls in the 8 directions of the canonical 45-degree tiling.

Usage: rigidity45.py ROOM.json RMAX [validate]
ROOM.json has either "vertices" (cyclic corner list) or "triangles" (tile list), plus "marked" [s, t].

Parameters theta = (v0x, v0y, l_0..l_{W-1}, sx, sy, tx, ty), vertex k = v0 + sum_{i<k} l_i u_i,
where u_i is the primitive integer direction of edge i. Unfolding transforms are x -> L x + a with
L a signed permutation matrix and a a pair of linear forms in theta.
Event: a path s -> t whose only corner contact is one corner c. At a corner whose unfolded cone
angle is 2*pi (45 or 90 degrees) the path continues straight (room direction reverses). At any
other corner the path passes on one side, found by a local offset-ray simulation.
Darkness that survives a deformation theta needs f_e . theta >= 0 for every event e (both signs for
regular corners). If the f_e positively span the annihilator of the symmetries on the closure
subspace, every non-symmetric deformation lights the room.
"""
from fractions import Fraction as Fr
from math import gcd
import json,sys,random

room=json.load(open(sys.argv[1]));RMAX=int(sys.argv[2]);VALIDATE=len(sys.argv)>3
BOUNCES=600

def boundary_from_triangles(tris):
 tris=[tuple(map(tuple,t)) for t in tris];cnt={}
 for t in tris:
  for i in range(3):
   e=tuple(sorted((t[i],t[(i+1)%3])));cnt[e]=cnt.get(e,0)+1
 bd=[e for e,c in cnt.items() if c==1];nxt={}
 # orient boundary edges counterclockwise: interior on the left
 for t in tris:
  a,b,c=t;o=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  if o<0:a,b=b,a;t=(a,b,c)
  else:t=(a,b,c)
  for i in range(3):
   p,q=t[i],t[(i+1)%3]
   if cnt[tuple(sorted((p,q)))]==1:assert p not in nxt,'boundary not a simple cycle';nxt[p]=q
 start=min(nxt);cyc=[start];p=nxt[start]
 while p!=start:cyc.append(p);p=nxt[p]
 assert len(cyc)==len(nxt),'boundary has several components'
 # drop collinear points
 out=[]
 for i,p in enumerate(cyc):
  a,b=cyc[i-1],cyc[(i+1)%len(cyc)]
  if (p[0]-a[0])*(b[1]-p[1])-(p[1]-a[1])*(b[0]-p[0])!=0:out.append(p)
 return out

V=[tuple(v) for v in room['vertices']] if 'vertices' in room else boundary_from_triangles(room['triangles'])
S,T=[tuple(m) for m in room['marked']]
W=len(V);D=2+W+4;IS,IT=2+W,2+W+2
area2=sum(V[i][0]*V[(i+1)%W][1]-V[(i+1)%W][0]*V[i][1] for i in range(W))
if area2<0:V=V[::-1]
def prim(dx,dy):g=gcd(abs(dx),abs(dy));return (dx//g,dy//g),g
U=[];L0=[]
for k in range(W):
 u,g=prim(V[(k+1)%W][0]-V[k][0],V[(k+1)%W][1]-V[k][1]);U.append(u);L0.append(g)
diagonal=any(u[0] and u[1] for u in U)
def unit(i):e=[Fr(0)]*D;e[i]=Fr(1);return e
zero=[Fr(0)]*D
def add(a,b):return [x+y for x,y in zip(a,b)]
def sc(k,a):return [k*x for x in a]
VX=[];VY=[];cx,cy=unit(0),unit(1)
for k in range(W):
 VX.append(cx);VY.append(cy);cx=add(cx,sc(U[k][0],unit(2+k)));cy=add(cy,sc(U[k][1],unit(2+k)))
theta0=[Fr(V[0][0]),Fr(V[0][1])]+[Fr(g) for g in L0]+[Fr(S[0]),Fr(S[1]),Fr(T[0]),Fr(T[1])]
def ev(f,th=None):return sum(a*b for a,b in zip(f,th or theta0))
assert all(ev(VX[k])==V[k][0] and ev(VY[k])==V[k][1] for k in range(W))
vidx={}
for i,v in enumerate(V):vidx.setdefault(v,[]).append(i)  # a pinch vertex appears twice
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
# interior angle in units of 45 degrees (polygon is counterclockwise)
import math
angle={}
for i in range(W):
 a=(V[i-1][0]-V[i][0],V[i-1][1]-V[i][1]);b=(V[(i+1)%W][0]-V[i][0],V[(i+1)%W][1]-V[i][1])
 ang=math.atan2(cross(b,a),a[0]*b[0]+a[1]*b[1])  # from b (next) counterclockwise to a (prev)
 if ang<=0:ang+=2*math.pi
 angle[i]=round(ang/(math.pi/4))
regular={i:(a in (1,2)) for i,a in angle.items()}
def corner_index(hv,d):
 ks=vidx[hv]
 if len(ks)==1:return ks[0]
 # pinch: pick the convex tip whose interior wedge contains the reversed ray
 w=(-d[0],-d[1]);hit_k=[]
 for k in ks:
  assert angle[k]<4,'pinch corner must be convex'
  a=(V[k-1][0]-V[k][0],V[k-1][1]-V[k][1]);b=(V[(k+1)%W][0]-V[k][0],V[(k+1)%W][1]-V[k][1])
  if cross(b,w)>0 and cross(w,a)>0:hit_k.append(k)
 assert len(hit_k)==1,(hv,d,hit_k);return hit_k[0]
def reflmat(u):
 a,b=u;n=a*a+b*b
 return ((Fr(a*a-b*b,n),Fr(2*a*b,n)),(Fr(2*a*b,n),Fr(b*b-a*a,n)))
def mv(M,d):return (M[0][0]*d[0]+M[0][1]*d[1],M[1][0]*d[0]+M[1][1]*d[1])
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
I2=((Fr(1),Fr(0)),(Fr(0),Fr(1)))
def det2(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def compose(tf,M,cxf,cyf):
 """tf o g where g(x) = M x + (I - M) c, c given by linear forms."""
 Lm,ax,ay=tf;IM=((1-M[0][0],-M[0][1]),(-M[1][0],1-M[1][1]))
 gx=add(sc(IM[0][0],cxf),sc(IM[0][1],cyf));gy=add(sc(IM[1][0],cxf),sc(IM[1][1],cyf))
 nax=add(add(sc(Lm[0][0],gx),sc(Lm[0][1],gy)),ax);nay=add(add(sc(Lm[1][0],gx),sc(Lm[1][1],gy)),ay)
 return (mm(Lm,M),nax,nay)
def apply(tf,qx,qy):
 Lm,ax,ay=tf
 return (add(add(sc(Lm[0][0],qx),sc(Lm[0][1],qy)),ax),add(add(sc(Lm[1][0],qx),sc(Lm[1][1],qy)),ay))

def seg_hit(pos,d,a,b):
 """Smallest u>0 with pos+u d on segment [a,b]; returns (u,point) or None."""
 e=(b[0]-a[0],b[1]-a[1]);den=cross(d,e)
 if den==0:return None
 w=(a[0]-pos[0],a[1]-pos[1]);u=Fr(cross(w,e),den);s=Fr(cross(w,d),den)
 if u>0 and 0<=s<=1:return u,(pos[0]+u*d[0],pos[1]+u*d[1])
 return None
def nexthit(P,pos,d):
 best=None;n=len(P)
 for i in range(n):
  h=seg_hit(pos,d,P[i],P[(i+1)%n])
  if h and (best is None or h[0]<best[0]):best=(h[0],i,h[1])
 return best
def on_open(pos,d,u,q):
 if d[0]:w=(q[0]-pos[0])/d[0]
 else:w=(q[1]-pos[1])/d[1]
 return 0<w<u and pos[0]+w*d[0]==q[0] and pos[1]+w*d[1]==q[1]

R_LOC=Fr(1,1000);ETA=Fr(1,10**7)
def local_exit(k,d,side):
 c=V[k];ws=[]
 for o_ in (V[k-1],V[(k+1)%W]):
  u,_=prim(o_[0]-c[0],o_[1]-c[1]);ws.append(((c[0],c[1]),(c[0]+Fr(u[0],10),c[1]+Fr(u[1],10)),u))
 n=(-d[1],d[0]) if side>0 else (d[1],-d[0])
 pos=(c[0]-R_LOC*d[0]+ETA*n[0],c[1]-R_LOC*d[1]+ETA*n[1]);dd=d;refl=[]
 for _ in range(10):
  best=None
  for a,b,u in ws:
   h=seg_hit(pos,dd,a,b)
   if h and (best is None or h[0]<best[0]):best=(h[0],h[1],u)
  if best is None or best[0]>4*R_LOC:break
  _,pos,u=best;M=reflmat(u);refl.append(M);dd=mv(M,dd)
 return refl,dd

def run(pos,d,tf,contact,out):
 for _ in range(BOUNCES):
  u,i,hit=nexthit(V,pos,d)
  if on_open(pos,d,u,T) or hit==T:out.append(('lit' if contact is None else 'event',contact,tf));return
  for v in V:
   if v!=hit and on_open(pos,d,u,v):return  # grazing contact: drop
  hv=(int(hit[0]),int(hit[1])) if hit[0].denominator==1 and hit[1].denominator==1 else None
  if hv in vidx:
   if contact is not None:return
   k=corner_index(hv,d);Lm=tf[0]
   if regular[k]:
    ntf=compose(tf,((Fr(-1),Fr(0)),(Fr(0),Fr(-1))),VX[k],VY[k])
    run(hit,(-d[0],-d[1]),ntf,(k,tf,0),out);return
   for side in (1,-1):
    refl,nd=local_exit(k,d,side);ntf=tf
    for M in refl:ntf=compose(ntf,M,VX[k],VY[k])
    run(hit,nd,ntf,(k,tf,side*det2(Lm)),out)
   return
  M=reflmat(U[i]);tf=compose(tf,M,VX[i],VY[i]);d=mv(M,d);pos=hit

funcs=[];events=[];lit=[]
for p in range(-RMAX,RMAX+1):
 for q in range(-RMAX,RMAX+1):
  if (p,q)==(0,0) or gcd(abs(p),abs(q))!=1:continue
  out=[];run((Fr(S[0]),Fr(S[1])),(Fr(p),Fr(q)),(I2,zero,zero),None,out)
  for status,contact,tf in out:
   if status=='lit':lit.append((p,q));continue
   k,tfc,side=contact
   cxf,cyf=apply(tfc,VX[k],VY[k]);txf,tyf=apply(tf,unit(IT),unit(IT+1));sx,sy=unit(IS),unit(IS+1)
   A=(add(txf,sc(-1,sx)),add(tyf,sc(-1,sy)));B=(add(cxf,sc(-1,sx)),add(cyf,sc(-1,sy)))
   a0=(ev(A[0]),ev(A[1]));b0=(ev(B[0]),ev(B[1]))
   assert a0[0]*b0[1]-a0[1]*b0[0]==0,'event not collinear'
   g=add(add(sc(b0[1],A[0]),sc(-b0[0],A[1])),add(sc(a0[0],B[1]),sc(-a0[1],B[0])))
   if all(x==0 for x in g):continue
   if side==0:funcs+=[g,sc(-1,g)]
   else:funcs.append(g if side>0 else sc(-1,g))
   events.append(dict(dir=[p,q],corner=list(V[k]),side=int(side),angle45=angle[k],g=g,A=A,B=B,L=[[int(x) for x in r] for r in tfc[0]],a0=[str(a0[0]),str(a0[1])]))

clos=[[Fr(0)]*2+[Fr(U[k][0]) for k in range(W)]+[Fr(0)]*4,[Fr(0)]*2+[Fr(U[k][1]) for k in range(W)]+[Fr(0)]*4]
def tvec(dx,dy):return [Fr(dx),Fr(dy)]+[Fr(0)]*W+[Fr(dx),Fr(dy),Fr(dx),Fr(dy)]
# a target inside wall k adds the active constraint h = n.(t - wall point) >= 0, n the inward normal
TW=[k for k in range(W) if cross(U[k],(T[0]-V[k][0],T[1]-V[k][1]))==0 and 0<(T[0]-V[k][0])*U[k][0]+(T[1]-V[k][1])*U[k][1]<L0[k]*(U[k][0]**2+U[k][1]**2)]
for k in TW:
 n=(-U[k][1],U[k][0]);funcs.append(add(sc(n[0],add(unit(IT),sc(-1,VX[k]))),sc(n[1],add(unit(IT+1),sc(-1,VY[k])))))
syms=[tvec(1,0),tvec(0,1),theta0[:]]
if not diagonal:syms.append([theta0[0],Fr(0)]+[theta0[2+k] if U[k][0] else Fr(0) for k in range(W)]+[theta0[IS],Fr(0),theta0[IT],Fr(0)])
for g in funcs:
 for sv in syms:assert sum(a*b for a,b in zip(g,sv))==0,'symmetry not in kernel'
def rank(M):
 M=[r[:] for r in M];rk=0
 for c in range(len(M[0]) if M else 0):
  piv=next((i for i in range(rk,len(M)) if M[i][c]!=0),None)
  if piv is None:continue
  M[rk],M[piv]=M[piv],M[rk]
  for i in range(len(M)):
   if i!=rk and M[i][c]!=0:f=M[i][c]/M[rk][c];M[i]=[x-f*y for x,y in zip(M[i],M[rk])]
  rk+=1
 return rk
nsym=rank(syms);r_on=(rank(funcs+clos)-rank(clos)) if funcs else 0;target=D-rank(clos)-nsym
tag=room.get('tag',sys.argv[1].split('/')[-1].replace('.json',''))
summary=dict(target_walls=TW,room=tag,W=W,diagonal=diagonal,RMAX=RMAX,events=len(events),lit_paths=len(lit),functionals=len(funcs),
             rank_on_closure=r_on,target=target,regular_corner_events=sum(1 for e in events if e['side']==0))
rowmeta=[]
for e in events:
 m=dict(L=e['L'],a0=e['a0'],dir=e['dir'],corner=e['corner'],side=e['side'],angle45=e['angle45'],unfolded_target_minus_s=[str(ev(e['A'][0])),str(ev(e['A'][1]))],unfolded_corner_minus_s=[str(ev(e['B'][0])),str(ev(e['B'][1]))])
 rowmeta+= [dict(m,sign=1),dict(m,sign=-1)] if e['side']==0 else [m]
json.dump(dict(rows=rowmeta,note='rows[i] describes funcs[i]; side +1 = ray offset to the left of the room direction at the corner, transported by det of the unfolding; sign convention: survival needs funcs[i].theta >= 0'),open(f'events-{tag}-R{RMAX}.json','w'),indent=1)
json.dump(dict(funcs=[[str(x) for x in f] for f in funcs],clos=[[str(x) for x in c] for c in clos],syms=[[str(x) for x in s] for s in syms],target=target),open(f'funcs-{tag}-R{RMAX}.json','w'))
if 'pinch' in room:
 # the closed family keeps the two tips at one point: two more closure rows
 k1,k2=vidx[tuple(room['pinch'])]
 clos_p=clos+[add(VX[k1],sc(-1,VX[k2])),add(VY[k1],sc(-1,VY[k2]))]
 summary.update(pinch_rank_on_closure=rank(funcs+clos_p)-rank(clos_p),pinch_target=D-rank(clos_p)-nsym)
 json.dump(dict(funcs=[[str(x) for x in f] for f in funcs],clos=[[str(x) for x in c] for c in clos_p],syms=[[str(x) for x in s] for s in syms],target=summary['pinch_target']),open(f'funcs-{tag}-closed-R{RMAX}.json','w'))

if VALIDATE and events:
 random.seed(1);agree=dis=0
 for trial in range(4):
  th=[Fr(random.randint(-5,5)) for _ in range(D)]
  # restore closure by adjusting two edges with independent directions
  k1=0;k2=next(k for k in range(W) if cross(U[k1],U[k])!=0)
  rx=sum(th[2+k]*U[k][0] for k in range(W));ry=sum(th[2+k]*U[k][1] for k in range(W))
  den=cross(U[k1],U[k2]);a=Fr(cross((rx,ry),U[k2]),den);b=Fr(cross(U[k1],(rx,ry)),den)
  th[2+k1]-=a;th[2+k2]-=b
  for k in TW:
   # keep a wall target on the room side: h = n.(t - wall point) > 0
   n=(-U[k][1],U[k][0]);h=sum(x*y for x,y in zip(funcs[-1],th))
   if h<=0:th[IT]+=n[0]*(1-h)/(n[0]**2+n[1]**2);th[IT+1]+=n[1]*(1-h)/(n[0]**2+n[1]**2)
  lam=Fr(1,10**5);par=[x+lam*y for x,y in zip(theta0,th)]
  P=[(ev(VX[k],par),ev(VY[k],par)) for k in range(W)];s=(par[IS],par[IS+1]);t=(par[IT],par[IT+1])
  Pset=set(P)
  for e in events:
   fth=sum(x*y for x,y in zip(e['g'],th))
   if fth==0 or e['side']==0:continue
   pred=(fth<0) if e['side']>0 else (fth>0)
   d=(ev(e['A'][0],par),ev(e['A'][1],par));pos=s;res=False
   for _ in range(BOUNCES):
    u,i,hit=nexthit(P,pos,d)
    if on_open(pos,d,u,t):res=True;break
    if hit in Pset:break
    M=reflmat(U[i]);d=mv(M,d);pos=hit
   if res==pred:agree+=1
   elif res and any(((sum(a*b for a,b in zip(x['g'],th))<0) if x['side']>0 else (sum(a*b for a,b in zip(x['g'],th))>0)) for x in events if x['dir']==e['dir'] and x['corner']==e['corner'] and x is not e):agree+=1  # lit through the other side, as that event predicts
   else:dis+=1
 summary.update(validate_agree=agree,validate_disagree=dis)
print(json.dumps(summary))
