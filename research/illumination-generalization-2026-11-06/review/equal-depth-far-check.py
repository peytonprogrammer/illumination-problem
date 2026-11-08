"""Eight prescribed genericfar candidates folded into original rooms; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def phase(p,q,r):
 A=p+q+2;np=(Q(p*r,A)+Q(1,2))//1;nq=(Q(q*r,A)+Q(1,2))//1
 assert Q(p*r,A).denominator!=2 and Q(q*r,A).denominator!=2
 return r-np-nq,Q((p-q)*r,A)-(np-nq)
def residue(p,q,parity):
 e=(q-p)//2;M=(p+q)//2+1
 if not parity:return 1 if e>=2 else 2
 return M-1 if p%2 or e>=2 else M-2

def prefix(E,tau,n,far=None):
 E=Q(E);sg=1 if n%2==0 else-1;k=n//2;r=sg+E*tau-4*k;assert 0<r<2
 pp=[(1+E,Q(1))]
 for j in range(1 if sg==1 else 0,2*k+1):pp.append((1+E-Q(2*j-sg,tau),Q(2 if j%2 else 0)))
 if E:pp.append((Q(1),r))
 if far is not None:
  extended=[pp[0]];crossings=0
  for a,b in zip(pp,pp[1:]):
   if a[0]>1+far>b[0]:
    y=a[1]+(b[1]-a[1])*(a[0]-1-far)/(a[0]-b[0]);assert 0<y<2;extended.append((1+far,y));crossings+=1
   extended.append(b)
  assert crossings==1
  pp=[(1+far-abs(x-1-far),y) for x,y in extended]
 return pp

def polygon(G,s,t,D,w,left):
 V=[(0,0),(1,0),(1,s-1),(D+2,s-1),(D+2,s+1),(1,s+1),(1,t-1),(1+w,t-1),(1+w,t+1),(1,t+1),(1,G),(0,G)]
 for a,b in sorted(left,reverse=True):V.extend([(0,b),(-2,b),(-2,a),(0,a)])
 while True:
  for i in range(len(V)):
   if V[i]==V[i-1] or g.det(g.vec(V[i-1],V[i]),g.vec(V[i],V[(i+1)%len(V)]))==0:V.pop(i);break
  else:break
 return [tuple(map(Q,z)) for z in V]
def witness(D,w,h,label):
 p=D;q=2*w-D;A=p+q+2;s=Q(6);t=s+2*h;G=Q(2*h+18)
 assert (p,q) not in((0,2),(1,3),(2,4))
 img={'mean':t,'bottom':-t,'top':2*G-t}[label];ell={'mean':(s+t)/2,'bottom':Q(h),'top':G-h}[label]
 left=[(ell,ell+2),(ell+4,ell+6)] if label!='top' else[(ell-4,ell-2),(ell,ell+2)];V=polygon(G,s,t,D,w,left);g.simple(V)
 a,b,Da,Db=s,img,p,q;swap=b<a
 if swap:a,b,Da,Db=b,a,Db,Da
 H=int((b-a)/2);r0=residue(p,q,H%2)
 for r in(r0,A-r0):
  f,d=phase(p,q,r);assert d and abs(d)<1;k=(H-f)//2;assert H-f==2*k and k>=0;N=r+A*k;tau=Q(2*N,A)
  assert Q(w-D)*tau and ((w-D)*tau).denominator!=1
  na=(Q(Da*N,A)+Q(1,2))//1;nb=(Q(Db*N,A)+Q(1,2))//1
  lower=[(x,a-1+y) for x,y in prefix(Da,tau,na,w if swap else None)];upper=[(x,b+1-y) for x,y in prefix(Db,tau,nb,None if swap else w)]
  z=(lower[-1][1]+upper[-1][1])/2;zf=g.fold(z,G);assert 0<abs(zf-ell)<1
  if any(l<=zf<=u for l,u in left):continue
  path=lower+[(0,z)]+list(reversed(upper))
  if swap:path=list(reversed(path))
  assert path[0]==(1+D,s) and path[-1]==(1+D,img)
  folded=[]
  for j,(a,b) in enumerate(zip(path,path[1:])):
   if not j:folded.append((a[0],g.fold(a[1],G)))
   cross=[]
   if a[1]!=b[1]:
    for kk in range(int(min(a[1],b[1])//G)-1,int(max(a[1],b[1])//G)+2):
     z0=Q(kk*G-a[1],b[1]-a[1])
     if 0<z0<1:
      x=a[0]+z0*(b[0]-a[0]);assert 0<x<1;cross.append((z0,(x,g.fold(kk*G,G))))
   folded.extend(pt for _,pt in sorted(cross));pt=(b[0],g.fold(b[1],G))
   if pt!=folded[-1]:folded.append(pt)
  target=(1+D,t);assert folded[-1]==target
  for j,(a,b) in enumerate(zip(folded,folded[1:])):
   if g.on(a,b,target):folded=folded[:j+1]+[target];break
  shift=0 if (1+D)%2==0 else 1;V=[(x+shift,y) for x,y in V];folded=[(x+shift,y) for x,y in folded];assert all(int(x)%2==int(y)%2==0 for x,y in(folded[0],folded[-1]))
  return {'D':D,'far_width':w,'h':h,'chart':label,'tau':str(tau),'far_phase':str((w-D)*tau),'path':folded,**g.path_check(V,folded)}
 raise AssertionError('both signed candidates blocked')
rows=[witness(*a) for a in[(0,2,3,'mean'),(1,3,4,'bottom'),(2,4,3,'top'),(3,4,4,'mean'),(4,5,3,'bottom'),(7,8,4,'top'),(12,20,3,'mean'),(21,30,2,'bottom')]]
out={'status':'EIGHT_PRESCRIBED_ACTUAL_EQUALDEPTH_FARFOLDS_PASS','rows':rows,'paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'equal-depth-far-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
