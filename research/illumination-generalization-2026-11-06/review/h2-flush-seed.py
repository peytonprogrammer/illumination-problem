"""R48 ONE fixed D0,a2,f1,g1 room, first positive path avoiding both unused flush teeth."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from math import gcd
import importlib.util,json,time
R=Path(__file__).resolve().parent;eff=json.loads((R/'h2-flush-effort.json').read_text());deadline=datetime.fromisoformat(eff['deadline_utc']).timestamp()
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
# Literal room: core[-3,5], selectedlowerflush andupper width1, LEFTfloor1,central2,roof1.
V=[(-1,-3),(2,-3),(2,-1),(1,-1),(1,1),(2,1),(2,3),(1,3),(1,5),(-1,5),(-1,3),(0,3),(0,2),(-2,2),(-2,0),(0,0),(0,-1),(-1,-1)]
V=[tuple(map(Q,z)) for z in V];g.simple(V);S=(Q(1),Q(-2));T=(Q(1),Q(2));assert g.location(V,S)==g.location(V,T)==1

def guard():
 if time.time()>=deadline:raise TimeoutError('Original R48 aggregate deadline')
def protected(a,b):
 # Any leg entering x<0 must stay within the CENTRAL band, never either flush tooth.
 if min(a[0],b[0])>=0:return True
 pts=[a,b]
 if a[0]*b[0]<0:
  r=-a[0]/(b[0]-a[0]);pts.append((Q(0),a[1]+r*(b[1]-a[1])))
 ys=[z[1] for z in pts if z[0]<=0]
 return min(ys)>=0 and max(ys)<=2

def trace(vel,cap=400):
 p=S;v=tuple(map(Q,vel));path=[p]
 for step in range(cap):
  guard();ev=[]
  for i,(a,b) in enumerate(g.edges(V)):
   e=g.vec(a,b);den=g.det(v,e)
   if not den:continue
   t=Q(g.det(g.vec(p,a),e),den);r=Q(g.det(g.vec(p,a),v),den)
   if t>0 and 0<=r<=1:ev.append((t,i,r))
  if not ev:return None
  dt=Q(T[0]-p[0],v[0]) if v[0] else Q(T[1]-p[1],v[1]);tmin=min(x[0] for x in ev)
  if dt>0 and tuple(p[k]+dt*v[k] for k in (0,1))==T and dt<tmin:
   if not protected(p,T):return None
   path.append(T);return path
  hits=[z for z in ev if z[0]==tmin]
  if len(hits)!=1 or not 0<hits[0][2]<1:return None
  q=tuple(p[k]+tmin*v[k] for k in (0,1))
  if not protected(p,q):return None
  path.append(q);p=q;a,b=g.edges(V)[hits[0][1]];e=g.vec(a,b);normal=(-e[1],e[0]);f=2*g.dot(v,normal)/g.dot(normal,normal);v=tuple(v[k]-f*normal[k] for k in (0,1))
 return None
tried=0;found=None
for norm in range(1,129):
 for dx in range(-norm,norm+1):
  dy=norm-abs(dx)
  for yy in ([0] if not dy else [dy,-dy]):
   if gcd(abs(dx),abs(yy))!=1:continue
   tried+=1;path=trace((dx,yy))
   if path:
    res=g.path_check(V,path);found={'direction':(dx,yy),'path':path,**res};break
  if found:break
 if found:break
out={'status':'FIRST_UNIFORM_PROTECTED_ACTUAL_PATH' if found else 'BOUNDED_UNDECIDED_NOT_DARKNESS','discovery':True,'original_deadline_utc':eff['deadline_utc'],'finished_utc':datetime.now(timezone.utc).isoformat(),'geometry_verified':True,'D':0,'central_width':2,'floor_width':1,'roof_width':1,'polygon':V,'source':S,'target':T,'directions_tried':tried,'witness':found,'whole_goal_complete':False}
(R/'h2-flush-seed.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str))
