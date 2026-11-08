"""Replay every finite R46 chart against actual polygons; no ray search."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(D,mu,G,w,f,roof):
 p=[(0,0),(1,0)]
 for lo,hi in [(mu-3,mu-1),(mu+1,mu+3)]:p.extend([(1,lo),(D+2,lo),(D+2,hi),(1,hi)])
 p.extend([(1,G),(0,G)])
 if roof is not None:p.extend([(-roof,G),(-roof,G-2),(0,G-2)])
 p.extend([(0,mu+2),(-w,mu+2),(-w,mu),(0,mu),(0,2),(-f,2),(-f,0)])
 while True:
  drop=next((i for i in range(len(p)) if g.det(g.vec(p[i-1],p[i]),g.vec(p[i],p[(i+1)%len(p)]))==0),None)
  if drop is None:break
  p.pop(drop)
 return [tuple(map(Q,z)) for z in p]
def events(z,v,e,width):
 E={Q(0),Q(e)}
 if e>width:E.add(Q(width))
 for n in range(int(min(z,z+v*e)//2)-1,int(max(z,z+v*e)//2)+2):
  r=(2*n-z)/v
  if 0<r<e:E.add(r)
 return sorted(E)
def arm(y,e,W,tau,sign,lower):
 if e==0:return [(Q(1),y)]
 out=[]
 for r in events(y-lower,sign*tau,e,W):
  depth=r if r<=W else 2*W-r
  out.append((1+depth,lower+g.fold(y-lower+sign*tau*r,Q(2))))
 return out
def construct(c,mu):
 D=c['D'];tau=Q(c['tau']);es=c['es'];et=c['et'];m=c['m'];w=c['w'];sign=c['sign']
 sy=Q(c['sy'][0])+Q(c['sy'][1])*tau;ty=Q(c['ty'][0])+Q(c['ty'][1])*tau
 p1=Q(c['p1'][0])+Q(c['p1'][1])*tau;p2=Q(c['p2'][0])+Q(c['p2'][1])*tau
 path=list(reversed(arm(sy,es,D+1,tau,-1,-3)))
 for i in range(1,2*m+1):path.append((Q(0 if i%2 else 1),sy+i*tau))
 path.append((Q(0),p1))
 for r in events(p1,tau,2*w,w)[1:]:path.append((-r if r<=w else r-2*w,g.fold(p1+tau*r,Q(2))))
 assert path[-1]==(0,p2)
 path.append((Q(1),ty));path.extend(arm(ty,et,D+1,tau,sign,1)[1:])
 path=[(x,y+mu) for x,y in path];assert path[0]==(1+D,mu-2) and path[-1]==(1+D,mu+2)
 assert all(a!=b for a,b in zip(path,path[1:]));return path
input=json.loads((R/'minimal-prefix-chart-check.json').read_text());assert input['missing']==[]
table=[]
for line in (R/'minimal-prefix-proof.md').read_text().splitlines():
 if line.startswith('|') and len(line.split('|'))==12 and line.split('|')[1].isdigit():
  vals=line.split('|')[1:-1];table.append(tuple(map(Q,vals)))
assert len(table)==97
for c,entry in zip(input['rows'],table):
 assert entry==tuple(Q(c[k]) for k in ['D','w','es','et','m','ns','nt','sign','k','tau'])
 D,w,es,et,m,ns,nt,sigma,k,tau=entry
 assert es in (D,D+2) and et in (D,D+2) and m>=0 and k>=0 and sigma in (-1,1) and tau>0
 sy=-2+2*ns+es*tau;ty=2+2*nt-sigma*et*tau;p1=sy+(2*m+1)*tau;p2=ty-sigma*tau
 assert -3<sy<-1 and 1<ty<3 and 0<p1<2 and 0<p2<2
 for i in range(1,int(m)+1):assert -2<sy+(2*i-1)*tau<0 and -1<sy+2*i*tau<1
 assert p1+2*w*tau==(p2 if sigma==1 else 4-p2)+4*k
 far=p1+w*tau;assert not(far.denominator==1 and far.numerator%2==0)
 if es==D+2 or et==D+2:assert not(tau.denominator==1 and tau.numerator%2==1)
 for field,val in [('sy',sy),('ty',ty),('p1',p1),('p2',p2)]:assert Q(c[field][0])+Q(c[field][1])*tau==val

assert {(c['D'],c['w']) for c in input['rows']}=={(D,w) for D,cut in enumerate([13,20,67]) for w in range(1,cut)}
rows=[]
for c in input['rows']:
 for mu,G,f,roof in [(4,8,Q(100003,7),None),(4,10,Q(1,3),Q(100009,11)),(5,10,100003,Q(2,7)),(1000000,2000002,Q(17,3),100009)]:
  p=polygon(c['D'],mu,G,c['w'],f,roof);g.simple(p);assert len(p)==(18 if roof is None else 20)
  path=construct(c,mu);T=path[-1];assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
  res=g.path_check(p,path);rows.append({'D':c['D'],'w':c['w'],'mu':mu,'G':G,'floor_width':str(f),'roof_width':str(roof),'polygon':p,'path':path,**res})
out={'status':'ALL_R46_FINITE_PREFIX_CERTIFICATES_ACTUAL_WALL_PASS','discovery':False,'finite_charts':97,'actual_paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'rows':rows,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['minimal-prefix-proof.md','minimal-prefix-chart-check.py','minimal-prefix-chart-check.json','resumed-exact-check.py']},'whole_goal_complete':False}
(R/'minimal-prefix-physical-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_sha256']}))
