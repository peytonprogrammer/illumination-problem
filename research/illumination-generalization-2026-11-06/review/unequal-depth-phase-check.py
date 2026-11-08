"""Prescribed controls of an unbounded residue formula, plus eight actual witnesses; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def phase(p,q,r):
 A=p+q+2;np=(Q(p*r,A)+Q(1,2))//1;nq=(Q(q*r,A)+Q(1,2))//1
 strict=Q(p*r,A).denominator!=2 and Q(q*r,A).denominator!=2
 return r-np-nq,Q((p-q)*r,A)-(np-nq),strict

def residues(p,q):
 e=(q-p)//2;M=(p+q)//2+1
 assert q>p>=0 and (q-p)%2==0 and (p,q) not in((0,2),(1,3),(2,4))
 even=1 if e>=2 else 2
 odd=M-1 if p%2 or e>=2 else M-2
 return even,odd
cases=0;transport=0
for p in range(61):
 for e in range(1,41):
  q=p+2*e;A=p+q+2
  if (p,q) in((0,2),(1,3),(2,4)):continue
  for parity,r in enumerate(residues(p,q)):
   f,d,strict=phase(p,q,r);assert strict and f==parity and 0<abs(d)<1
   ff,dd,ss=phase(p,q,A-r);assert ss and ff==2-f and dd==-d
   for H in (2+parity,4+parity,36+parity):
    for rr in(r,A-r):
     f0,d0,_=phase(p,q,rr);k=(H-f0)//2;assert H-f0==2*k and k>=0
     N=rr+A*k;f1,d1,s1=phase(p,q,N);assert s1 and f1==H and d1==d0 and N>0;transport+=1
   cases+=1
exception_rows=[]
for p,q in((0,2),(1,3),(2,4)):
 nonzero={f%2 for r in range(p+q+2) for f,d,strict in[phase(p,q,r)] if strict and d}
 assert nonzero==({1} if(p,q)==(1,3) else set());exception_rows.append({'depths':[p,q],'nonzero_parities':sorted(nonzero)})
def polygon(G,s,t,ws,wt,left):
 V=[(0,0),(1,0),(1,s-1),(1+ws,s-1),(1+ws,s+1),(1,s+1),(1,t-1),(1+wt,t-1),(1+wt,t+1),(1,t+1),(1,G),(0,G)]
 for a,b in sorted(left,reverse=True):V.extend([(0,b),(-2,b),(-2,a),(0,a)])
 while True:
  for i in range(len(V)):
   if V[i]==V[i-1] or g.det(g.vec(V[i-1],V[i]),g.vec(V[i],V[(i+1)%len(V)]))==0:V.pop(i);break
  else:break
 return [tuple(map(Q,z)) for z in V]
def prefix(D,tau,n):
 k=n//2;sg=1 if n%2==0 else-1;r=sg+D*tau-4*k;assert 0<r<2
 pp=[(1+D,Q(1))]
 for j in range(1 if sg==1 else 0,2*k+1):pp.append((1+D-Q(2*j-sg,tau),Q(2 if j%2 else 0)))
 if D:pp.append((Q(1),r))
 return pp

def physical(p,q,h,label):
 sy=Q(6);ty=sy+2*h;G=Q(2*h+18);A=p+q+2;source=(Q(1+p),sy);target=(Q(1+q),ty)
 image={'mean':ty,'bottom':-ty,'top':2*G-ty}[label];level={'mean':(sy+ty)/2,'bottom':Q(h),'top':G-h}[label]
 left=[(level,level+2),(level+4,level+6)] if label!='top' else[(level-4,level-2),(level,level+2)]
 V=polygon(G,sy,ty,p+1,q+1,left);g.simple(V);assert len(V)<=23
 a,b,Da,Db=sy,image,p,q;swapped=b<a
 if swapped:a,b,Da,Db=b,a,Db,Da
 H=(b-a)/2;assert H.denominator==1;H=int(H);r0=residues(p,q)[H%2]
 for r in(r0,A-r0):
  f,d,_=phase(p,q,r);k=(H-f)//2;N=r+A*k;tau=Q(2*N,A)
  na=(Q(Da*N,A)+Q(1,2))//1;nb=(Q(Db*N,A)+Q(1,2))//1
  lower=[(x,a-1+y) for x,y in prefix(Da,tau,na)];upper=[(x,b+1-y) for x,y in prefix(Db,tau,nb)]
  z=(lower[-1][1]+upper[-1][1])/2;zf=g.fold(z,G);assert 0<abs(zf-level)<1
  if any(l<=zf<=u for l,u in left):continue
  path=lower+[(0,z)]+list(reversed(upper))
  if swapped:path=list(reversed(path))
  assert path[0]==source and path[-1]==(target[0],image)
  folded=[]
  for j,(u,v) in enumerate(zip(path,path[1:])):
   if not j:folded.append((u[0],g.fold(u[1],G)))
   crossing=[]
   if u[1]!=v[1]:
    for kk in range(int(min(u[1],v[1])//G)-1,int(max(u[1],v[1])//G)+2):
     time=Q(kk*G-u[1],v[1]-u[1])
     if 0<time<1:
      x=u[0]+time*(v[0]-u[0]);assert 0<x<1;crossing.append((time,(x,g.fold(kk*G,G))))
   folded.extend(point for _,point in sorted(crossing));point=(v[0],g.fold(v[1],G))
   if point!=folded[-1]:folded.append(point)
  assert folded[0]==source and folded[-1]==target
  for j,(u,v) in enumerate(zip(folded,folded[1:])):
   if g.on(u,v,target):folded=folded[:j+1]+[target];break
  xshift=0 if int(source[0])%2==0 else 1
  V=[(x+xshift,y) for x,y in V];folded=[(x+xshift,y) for x,y in folded]
  assert all(int(x)%2==int(y)%2==0 for x,y in(folded[0],folded[-1]))
  return {'depths':[p,q],'h':h,'chart':label,'tau':str(tau),'turn':str(zf),'path':folded,**g.path_check(V,folded)}
 raise AssertionError('both prescribed symmetric choices blocked')
rows=[physical(*f) for f in[(0,4,3,'mean'),(1,5,3,'bottom'),(2,6,4,'top'),(3,5,4,'mean'),(4,6,3,'mean'),(12,38,4,'bottom'),(11,49,3,'top'),(1,7,2,'bottom')]]
out={'status':'PRESCRIBED_RESIDUE_AND_ACTUAL_WITNESSES_PASS','phase_table_cases':cases,'exact_transports':transport,'exception_rows':exception_rows,'physical_paths':len(rows),'rows':rows,'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'unequal-depth-phase-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
