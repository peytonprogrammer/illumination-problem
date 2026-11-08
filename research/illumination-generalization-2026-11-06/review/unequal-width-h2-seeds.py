"""R55 three exact residual ratios, stop first left-tooth-free actual path each."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd
import time,datetime,importlib.util,json
R=Path(__file__).resolve().parent;DEADLINE=datetime.datetime.fromisoformat('2026-11-07T08:04:00+00:00').timestamp()
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def clock():
 if time.time()>=DEADLINE:raise TimeoutError('R55 original aggregate deadline')
def trace(V,v,cap=200):
 S=(Q(1),Q(2));T=(Q(1),Q(6));z=S;path=[z];word=[]
 for _ in range(cap+1):
  clock();hits=[]
  for i,(a,b) in enumerate(g.edges(V)):
   e=g.vec(a,b);den=g.det(v,e)
   if den:
    tt=Q(g.det(g.vec(z,a),e),den);rr=Q(g.det(g.vec(z,a),v),den)
    if tt>0 and 0<=rr<=1:hits.append((tt,i,rr))
  if not hits:return 'no hit',None
  tm=min(x[0] for x in hits);d=g.vec(z,T)
  if g.det(v,d)==0 and g.dot(v,d)>0:
   tt=Q(d[0],v[0]) if v[0] else Q(d[1],v[1])
   if tt<tm:
    path.append(T);return 'success',{'path':path,'word':word,'initial':initial}
  hh=[(i,r) for t,i,r in hits if t==tm]
  if len(hh)!=1 or not 0<hh[0][1]<1:return 'corner',None
  i,_=hh[0];a,b=g.edges(V)[i];z=(z[0]+tm*v[0],z[1]+tm*v[1])
  if z[0]<0:return 'entered left tooth',None
  path.append(z);word.append(i);v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1])
 return 'cap',None
rows=[]
for ws,wt in [(Q(1,3),Q(1,5)),(Q(1,3),Q(1)),(Q(1),Q(1,5))]:
 clock();V=[(0,0),(1,0),(1,1),(1+ws,1),(1+ws,3),(1,3),(1,5),(1+wt,5),(1+wt,7),(1,7),(1,9),(0,9),(0,7),(-1,7),(-1,5),(0,5),(0,4),(-1,4),(-1,2),(0,2)];V=[tuple(map(Q,z)) for z in V];g.simple(V);assert g.location(V,(1,2))==g.location(V,(1,6))==1
 counters={};found=None;seen=0
 for size in range(2,129):
  for p in range(1,size):
   q=size-p
   if gcd(p,q)>1:continue
   for sx,sy in [(-1,1),(-1,-1),(1,1),(1,-1)]:
    initial=(Q(sx*p),Q(sy*q));status,z=trace(V,initial);seen+=1;counters[status]=counters.get(status,0)+1
    if z:
     g.path_check(V,z['path']);found=z;break
   if found:break
  if found:break
 row={'ws':ws,'wt':wt,'geometry':'strictly simple20walls, actual seams2/6','directions':seen,'outcomes':counters,'candidate':found};rows.append(row)
 print(json.dumps({'ws':str(ws),'wt':str(wt),'directions':seen,'found':bool(found),'reflections':len(found['word']) if found else None}),flush=True)
 (R/'unequal-width-h2-seeds.json').write_text(json.dumps({'discovery':True,'whole_goal_complete':False,'deadline_utc':'2026-11-07T08:04:00Z','rows':rows},indent=2,default=str)+'\n')
 if not found:break
