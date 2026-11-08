"""Prescribed four-candidate farfold controls, including a deliberately bad nearest candidate."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(c,G,s,t,w,left):
 V=[(0,0),(c,0),(c,s-1),(c+1,s-1),(c+1,s+1),(c,s+1),(c,t-1),(c+w,t-1),(c+w,t+1),(c,t+1),(c,G),(0,G)]
 for a,b in sorted(left,reverse=True):V.extend([(0,b),(-2,b),(-2,a),(0,a)])
 while True:
  for i in range(len(V)):
   if V[i]==V[i-1] or g.det(g.vec(V[i-1],V[i]),g.vec(V[i],V[(i+1)%len(V)]))==0:V.pop(i);break
  else:break
 return [tuple(map(Q,z)) for z in V]
def witness(c,D,w,h,label):
 c,D,w,h=map(Q,(c,D,w,h));assert 0<=D<w;E=2*w-D;special=D==0;assert w>c if special else E>6*c
 s=Q(6);t=s+2*h;G=2*h+18;img={'mean':t,'bottom':-t,'top':2*G-t}[label];ell={'mean':(s+t)/2,'bottom':h,'top':G-h}[label]
 left=[(ell,ell+2),(ell+4,ell+6)] if label!='top' else[(ell-4,ell-2),(ell,ell+2)];V=polygon(c,G,s,t,w,left);g.simple(V)
 orient=1 if img>s else -1;a=orient*s;b=orient*img;H=(b-a)/2;A=2*c+E;eta=2*c/A;x=E*H/(2*c);ceilx=-((-x)//1);floorx=x//1
 sides=[[ceilx-1],[floorx+1]] if special else [[ceilx-1,ceilx-2],[floorx+1,floorx+2]]
 bad=[]
 def corner(n):
  far=(w-D)*(2*H+2*n)/A
  return far.denominator==1 and far.numerator%2!=0
 for side in sides:
  assert any(not corner(n) for n in side)
  for n in side:
   dd=(2*c*n-E*H)/A;assert n>0 and 0<abs(dd)<Q(1,2)
   if corner(n):bad.append(int(n))
 for n in sides[0]+sides[1]:
  if corner(n):continue
  tau=(2*H+2*n)/A;delta=(2*c*n-E*H)/A;M=a+c*tau;portal=a+2*c*tau;assert portal==b+2*delta
  physicalturn=g.fold(orient*M,G);assert 0<abs(physicalturn-ell)<Q(1,2)
  if any(l<=physicalturn<=u for l,u in left):continue
  phase=portal-b+1;path=[(c,a),(0,M),(c,portal)]
  for j in range(1,int(n)+1):
   xx=c+(2*j-phase)/tau;assert c<xx<c+E;path.append((xx,b-1+g.fold(Q(2*j),Q(2))))
  path.append((c+E,b));ext=[path[0]];crossings=0
  for u,v in zip(path,path[1:]):
   if (u[0]-c-w)*(v[0]-c-w)<0:
    f=Q(c+w-u[0],v[0]-u[0]);yy=u[1]+f*(v[1]-u[1]);assert b-1<yy<b+1;ext.append((c+w,yy));crossings+=1
   ext.append(v)
  assert crossings==1
  path=[(xx if xx<=c+w else 2*(c+w)-xx,orient*y) for xx,y in ext];folded=[]
  for j,(u,v) in enumerate(zip(path,path[1:])):
   if not j:folded.append((u[0],g.fold(u[1],G)))
   crossings=[]
   if u[1]!=v[1]:
    for k in range(int(min(u[1],v[1])//G)-1,int(max(u[1],v[1])//G)+2):
     z=Q(k*G-u[1],v[1]-u[1])
     if 0<z<1:
      xx=u[0]+z*(v[0]-u[0]);assert 0<xx<c;crossings.append((z,(xx,g.fold(k*G,G))))
   folded.extend(point for _,point in sorted(crossings));point=(v[0],g.fold(v[1],G))
   if point!=folded[-1]:folded.append(point)
  assert folded[0]==(c,s) and folded[-1]==(c+D,t);target=folded[-1]
  for j,(u,v) in enumerate(zip(folded,folded[1:])):
   if g.on(u,v,target):folded=folded[:j+1]+[target];break
  return {'c':str(c),'D':str(D),'w':str(w),'h':str(h),'chart':label,'sharper_D0':special,'bad_candidates':bad,'selected_index':int(n),'delta':str(delta),'path':folded,**g.path_check(V,folded)}
 raise AssertionError('no clean candidate on required smooth side')
rows=[witness(*args) for args in[(1,0,2,3,'mean'),(1,0,5,4,'bottom'),(2,2,8,3,'top'),(3,4,Q(37,3),2,'mean'),(Q(3,2),1,6,3,'bottom'),(4,6,16,4,'top'),(2,0,3,3,'mean'),(Q(2,3),Q(1,3),3,4,'bottom')]]
assert rows[3]['bad_candidates'] and rows[3]['selected_index'] not in rows[3]['bad_candidates']
out={'status':'PRESCRIBED_WIDE_FARFOLD_CONTROLS_PASS','rows':rows,'paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'bad_nearest_candidate_control':'c3,D4,w37/3,H2: nearest negative candidate has a far corner; second same-side candidate passes','discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'wide-target-far-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
