"""Eight prescribed R39 matching controls, not a room or direction discovery search."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def polygon(c,G,right,left):
 V=[(0,0),(c,0)]
 for a,b,w in right:V.extend([(c,a),(c+w,a),(c+w,b),(c,b)])
 V.extend([(c,G),(0,G)])
 for a,b,w in reversed(left):V.extend([(0,b),(-w,b),(-w,a),(0,a)])
 # Only flush attachments create redundant core-end vertices.
 changed=True
 while changed:
  changed=False
  for i in range(len(V)):
   if V[i]==V[i-1] or g.det(g.vec(V[i-1],V[i]),g.vec(V[i],V[(i+1)%len(V)]))==0:
    V.pop(i);changed=True;break
 return [tuple(map(Q,z)) for z in V]
def prefix(c,depth,u,tau):
 n=(depth*tau/u+Q(1,2))//1;sign=1 if n%2==0 else-1;start=sign*u/2;end=start+depth*tau
 out=[(c+depth,u/2)]
 for j in range(int(start//u)-1,int(end//u)+2):
  if start<j*u<end:out.append((c+depth-(j*u-start)/tau,g.fold(j*u,u)))
 if depth:out.append((c,g.fold(end,u)))
 return out,n,1+(depth*tau/u+Q(1,2)-n)*0 # n retained explicitly

def chart(c,G,S,T,u,v,image):
 a=S[1];b=image;Da=S[0]-c;Db=T[0]-c;swapped=b<a
 if swapped:a,b,Da,Db,u,v=b,a,Db,Da,v,u
 Delta=b-a;A=Da+Db+2*c;tau=Q(0);iterations=0
 while True:
  n1=(Da*tau/u+Q(1,2))//1;n2=(Db*tau/v+Q(1,2))//1
  nxt=(Delta+u*n1+v*n2)/A;iterations+=1
  assert 0<nxt<=(Delta+(u+v)/2)/(2*c)
  if nxt==tau:break
  assert nxt>tau;tau=nxt
  assert iterations<100000
 rs=u/2+Da*tau-u*n1;rt=v/2+Db*tau-v*n2
 assert 0<rs<u and 0<rt<v
 lower,_,_=prefix(c,Da,u,tau);upper,_,_=prefix(c,Db,v,tau)
 lower=[(x,a-u/2+y) for x,y in lower];upper=[(x,b+v/2-y) for x,y in upper]
 z=(lower[-1][1]+upper[-1][1])/2;assert abs(z-(a+b)/2)<(u+v)/4
 path=lower+[(0,z)]+list(reversed(upper))
 if swapped:path=list(reversed(path))
 assert path[0]==S and path[-1]==(T[0],image)
 folded=[]
 for j,(p,r) in enumerate(zip(path,path[1:])):
  if not j:folded.append((p[0],g.fold(p[1],G)))
  if p[1]!=r[1]:
   ks=range(int(min(p[1],r[1])//G)-1,int(max(p[1],r[1])//G)+2);cross=[]
   for k in ks:
    t=Q(k*G-p[1],r[1]-p[1])
    if 0<t<1:
     x=p[0]+t*(r[0]-p[0]);assert 0<x<c;cross.append((t,(x,g.fold(k*G,G))))
   folded.extend(pt for _,pt in sorted(cross))
  point=(r[0],g.fold(r[1],G))
  if point!=folded[-1]:folded.append(point)
 assert folded[0]==S and folded[-1]==T
 # First actual target prefix, preserving any original direction/contact sequence.
 for j,(a,b) in enumerate(zip(folded,folded[1:])):
  if g.on(a,b,T):folded=folded[:j+1]+[T];break
 return z,g.fold(z,G),tau,iterations,folded

# c,G,s,t,u,v, source width,target width,source depth,target depth,left bands.
fixtures=[
 (4,40,10,26,2,2,8,10,2,6,[(7,9,3),(17,19,5)]),
 (Q(3,2),30,8,20,3,1,4,5,Q(7,3),Q(11,5),[(5,7,2),(13,15,Q(5,2))]),
 (3,14,4,10,2,2,5,2,3,1,[(2,4,3),(6,8,2)]),
 (2,40,10,26,2,2,8,10,0,8,[(7,9,4),(17,19,2)]),
 (3,40,10,26,2,2,5,6,0,0,[(7,9,2),(17,19,3)]),
 (2,40,10,26,2,2,8,10,4,6,[(0,2,5),(38,40,3)]),
 (Q(9,4),50,12,34,4,2,20,17,12,13,[(10,12,3),(22,24,4)]),
 (2,40,10,26,2,2,80,100,24,68,[(7,9,30),(17,19,50)])]
rows=[]
for num,f in enumerate(fixtures):
 c,G,sy,ty,u,v,ws,wt,Ds,Dt=map(Q,f[:10]);left=[tuple(map(Q,z)) for z in f[10]]
 B=max(b-a for a,b,w in left);delta=(u+v)/4;h=(ty-sy)/2;q=min(sy,G-ty)
 assert h>=B+delta and q>=B+2*delta
 right=[(sy-u/2,sy+u/2,ws),(ty-v/2,ty+v/2,wt)];V=polygon(c,G,right,left);g.simple(V)
 assert len(V)<=23 and 0<=Ds<ws and 0<=Dt<wt
 S=(c+Ds,sy);T=(c+Dt,ty);turns=[];valid=[]
 for label,img,level in [('mean',ty,(sy+ty)/2),('bottom',-ty,h),('top',2*G-ty,G-h)]:
  z,zf,tau,it,path=chart(c,G,S,T,u,v,img);assert abs(zf-level)<delta
  blocked=any(a<=zf<=b for a,b,w in left)
  turns.append({'chart':label,'height':str(zf),'blocked':blocked,'iterations':it})
  if blocked:continue
  res=g.path_check(V,path);valid.append({'chart':label,'slope':str(tau),'path':path,**res})
 assert valid
 rows.append({'control':num,'walls':len(V),'turns':turns,'valid':valid})
out={'status':'PRESCRIBED_THREE_WINDOW_CONTROLS_PASS','rows':rows,'valid_paths':sum(len(z['valid']) for z in rows),'reflections':sum(p['reflections'] for r in rows for p in r['valid']),'wall_leg_guards':sum(p['wall_leg_guards'] for r in rows for p in r['valid']),'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'deep-comb-window-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
