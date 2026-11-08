"""Exact prescribed physical insertions for R36; no direction or room discovery."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from math import lcm
import importlib.util,json,hashlib,signal
R=Path(__file__).resolve().parent
end=datetime.fromisoformat(json.loads((R/'four-corner-critical-effort.json').read_text())['deadline_utc'])
signal.setitimer(signal.ITIMER_REAL,max(.001,(end-datetime.now(timezone.utc)).total_seconds()))
def deadline():assert datetime.now(timezone.utc)<end
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
base=json.loads((R/'four-corner-critical-check.json').read_text());V0=[tuple(map(Q,z)) for z in base['polygon']];p0=[tuple(map(Q,z)) for z in base['witness']['path']]
Y=list(map(Q,[0,1,2,3,6,8,10,12,13,14,15,16]));X=list(map(Q,[-1,0,1,2,3]))
def cuts(levels,axis):
 out=[];used={p[axis] for p in p0}
 for a,b in zip(levels,levels[1:]):
  for d in range(2,100):
   c=a+(b-a)/d
   if c not in used:out.append(c);break
  else:raise AssertionError('no strict prescribed cut')
 return out
YC=cuts(Y,1);XC=cuts(X,0)
def intervals(V,axis,cut):
 tr=1-axis;points=[]
 for a,b in g.edges(V):
  if min(a[axis],b[axis])<cut<max(a[axis],b[axis]):
   points.append(a[tr]+(b[tr]-a[tr])*(cut-a[axis])/(b[axis]-a[axis]))
 points=sorted(set(points));assert len(points)%2==0
 return list(zip(points[::2],points[1::2]))
def insert(V,path,axis,cut,delta):
 deadline()
 if delta==0:return V,path,0
 tr=1-axis;bounds=intervals(V,axis,cut)
 def shift(p):q=list(p);q[axis]+=delta if p[axis]>cut else 0;return tuple(q)
 new=[shift(path[0])];ports=0
 for a,b in zip(path,path[1:]):
  deadline();assert a[axis]!=cut and b[axis]!=cut
  if min(a[axis],b[axis])<cut<max(a[axis],b[axis]):
   f=(cut-a[axis])/(b[axis]-a[axis]);z=a[tr]+f*(b[tr]-a[tr]);matches=[(lo,hi) for lo,hi in bounds if lo<z<hi];assert len(matches)==1
   lo,hi=matches[0];w=hi-lo;rate=(b[tr]-a[tr])/abs(b[axis]-a[axis]);assert (rate*delta/(2*w)).denominator==1
   sign=1 if b[axis]>a[axis] else-1;enter=cut if sign==1 else cut+delta
   q=[Q(0),Q(0)];q[axis]=enter;q[tr]=z;new.append(tuple(q));ports+=2
   t0=z-lo;t1=t0+rate*delta;hits=[]
   for j in range(int(min(t0,t1)//w)-1,int(max(t0,t1)//w)+2):
    s=(j*w-t0)/rate
    if 0<s<delta:
     q=[Q(0),Q(0)];q[axis]=enter+sign*s;q[tr]=lo+g.fold(j*w,w);hits.append((s,tuple(q)))
   new.extend(q for _,q in sorted(hits));q=[Q(0),Q(0)];q[axis]=enter+sign*delta;q[tr]=z;new.append(tuple(q))
  new.append(shift(b))
 return[shift(p) for p in V],[p for i,p in enumerate(new) if i==0 or p!=new[i-1]],ports

def control(n,m):
 deadline();V,p=V0,p0;offset=Q(0);ports=0
 for cut,k in zip(YC,n):
  delta=Q(14*k);V,p,z=insert(V,p,1,cut+offset,delta);offset+=delta;ports+=z
 hs=[hi-lo for cut in XC for lo,hi in intervals(V,0,cut)];assert all(h.denominator==1 for h in hs)
 K=lcm(*map(int,hs));assert K==lcm(16+14*sum(n),2+14*n[4],2+14*n[6],2+14*(n[1]+n[2]),2+14*(n[8]+n[9]))
 offset=Q(0)
 for cut,k in zip(XC,m):
  delta=Q(24*K*k);V,p,z=insert(V,p,0,cut+offset,delta);offset+=delta;ports+=z
 g.simple(V);assert len(V)==20
 assert all(z.denominator==1 and z%2==0 for point in(p[0],p[-1]) for z in point)
 assert p[0]==(Q(2)+24*K*sum(m[:3]),Q(2)+14*sum(n[:2]))
 assert p[-1]==(Q(2)+24*K*sum(m[:3]),Q(14)+14*sum(n[:9]))
 assert not any(g.on(a,b,p[-1]) for a,b in zip(p[:-2],p[1:-1]))
 result=g.path_check(V,p);digest=hashlib.sha256(json.dumps(p,default=str).encode()).hexdigest()
 return {'n':n,'m':m,'K':K,'source':p[0],'target':p[-1],'walls':len(V),'inserted_port_nodes':ports,'path_sha256':digest,**result}
Z=[0]*11;controls=[(Z,[0]*4),([0,1,0,0,0,0,0,0,0,0,0],[0]*4),([1]*11,[0]*4),(Z,[1,1,1,1]),([0,1,0,0,0,0,0,0,0,0,0],[1,0,0,0]),([0,0,0,1,0,0,0,0,0,0,0],[0,1,0,0])]
rows=[control(n,m) for n,m in controls]
out={'status':'SIX_PRESCRIBED_EXACT_JOINT_PERIOD_CONTROLS_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'discovery':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['four-corner-critical-check.json','resumed-exact-check.py']},'scope':'Exact all-wall controls for explicit period family; hand proof covers all parameter vectors, not all gap residues.'}
deadline();(R/'four-corner-critical-strip-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}));print(json.dumps(rows,default=str))
