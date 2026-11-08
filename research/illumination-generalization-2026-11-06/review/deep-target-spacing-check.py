"""Eight prescribed explicit image-spacing witnesses; no direction or room discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(c,G,sy,ty,D,left):
 V=[(0,0),(c,0),(c,sy-1),(c+1,sy-1),(c+1,sy+1),(c,sy+1),(c,ty-1),(c+D+1,ty-1),(c+D+1,ty+1),(c,ty+1),(c,G),(0,G)]
 for a,b in sorted(left,reverse=True):V.extend([(0,b),(-2,b),(-2,a),(0,a)])
 while True:
  for i in range(len(V)):
   if V[i]==V[i-1] or g.det(g.vec(V[i-1],V[i]),g.vec(V[i],V[(i+1)%len(V)]))==0:V.pop(i);break
  else:break
 return [tuple(map(Q,z)) for z in V]
def witness(c,D,h,label):
 c,D,h=map(Q,(c,D,h));assert D>2*c;s=Q(6);t=s+2*h;G=2*h+18
 image={'mean':t,'bottom':-t,'top':2*G-t}[label];level={'mean':(s+t)/2,'bottom':h,'top':G-h}[label]
 left=[(level,level+2),(level+4,level+6)] if label!='top' else[(level-4,level-2),(level,level+2)]
 V=polygon(c,G,s,t,D,left);g.simple(V);assert len(V)<=23
 orient=1 if image>s else-1;a,b=orient*s,orient*image;H=(b-a)/2;A=2*c+D;x=D*H/(2*c);nm=-((-x)//1)-1;np=x//1+1
 dminus=(2*c*nm-D*H)/A;dplus=(2*c*np-D*H)/A;assert -Q(1,2)<dminus<0<dplus<Q(1,2)
 for n in(nm,np):
  tau=(2*H+2*n)/A;delta=(2*c*n-D*H)/A;M=a+c*tau;portal=a+2*c*tau;assert portal==b+2*delta and abs(delta)<Q(1,2)
  nominal=g.fold(orient*M,G);assert 0<abs(nominal-level)<Q(1,2)
  if any(l<=nominal<=u for l,u in left):continue
  phase=portal-b+1;path=[(c,a),(0,M),(c,portal)]
  for j in range(1,int(n)+1):
   xx=c+(2*j-phase)/tau;assert c<xx<c+D;path.append((xx,b-1+g.fold(Q(2*j),Q(2))))
  path.append((c+D,b));path=[(xx,orient*y) for xx,y in path];folded=[]
  for i,(u,v) in enumerate(zip(path,path[1:])):
   if not i:folded.append((u[0],g.fold(u[1],G)))
   contacts=[]
   if u[1]!=v[1]:
    for k in range(int(min(u[1],v[1])//G)-1,int(max(u[1],v[1])//G)+2):
     z=Q(k*G-u[1],v[1]-u[1])
     if 0<z<1:
      xx=u[0]+z*(v[0]-u[0]);assert 0<xx<c;contacts.append((z,(xx,g.fold(k*G,G))))
   folded.extend(pt for _,pt in sorted(contacts));pt=(v[0],g.fold(v[1],G))
   if pt!=folded[-1]:folded.append(pt)
  assert folded[0]==(c,s) and folded[-1]==(c+D,t)
  target=folded[-1]
  for i,(u,v) in enumerate(zip(folded,folded[1:])):
   if g.on(u,v,target):folded=folded[:i+1]+[target];break
  return {'c':str(c),'D':str(D),'h':str(h),'chart':label,'image_index':int(n),'delta':str(delta),'path':folded,**g.path_check(V,folded)}
 raise AssertionError('both explicit candidates blocked')
rows=[witness(*args) for args in[(1,4,3,'mean'),(2,6,4,'bottom'),(3,8,2,'top'),(5,12,3,'mean'),(Q(3,2),Q(7,2),3,'bottom'),(Q(2,3),Q(5,3),4,'top'),(7,100,3,'mean'),(4,10,2,'bottom')]]
# Strict threshold is substantive: an integral image-center with D=2c has nearest nonzero deltas exactly+/-1/2.
c=Q(2);D=2*c;H=Q(2);A=2*c+D;x=D*H/(2*c);assert x.denominator==1
assert {Q(2*c*n-D*H,A) for n in (int(x)-1,int(x)+1)}=={-Q(1,2),Q(1,2)}
out={'status':'PRESCRIBED_DEEP_TARGET_SPACING_PATHS_PASS','rows':rows,'paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'threshold_control':'D=2c nearest nonzero deltas are mouth-corner equalities in the prescribed exact phase','discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'deep-target-spacing-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
