from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
from math import gcd
import json,time
ROOT=Path(__file__).resolve().parent
meta=json.loads((ROOT/'reflex-coalescence-effort.json').read_text())
END=datetime.fromisoformat(meta['deadline_utc']).timestamp()
P=[(2,2),(4,2),(4,0),(2,0),(2,-4),(-2,-4),(-2,-3),(0,-3),(0,0),(-3,0),(-3,-2),(-4,-2),(-4,2),(0,2),(0,4),(2,4)]
P=[tuple(map(F,p)) for p in P]; O=P[0]
area2=sum(P[i][0]*P[(i+1)%len(P)][1]-P[i][1]*P[(i+1)%len(P)][0] for i in range(len(P)))
def cross(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
convex={p for i,p in enumerate(P) if cross(P[i-1],p,P[(i+1)%len(P)])*area2>0}
def deadline():
 if time.time()>=END:raise TimeoutError('Original A26 aggregate deadline reached')
def trace(v,cap=400):
 x=O; wallword=[]; pts=[x]; elapsed=F(0)
 for j in range(cap):
  deadline(); cand=[]
  for i,a in enumerate(P):
   b=P[(i+1)%len(P)]
   if a[0]==b[0]:
    if not v[0]:continue
    t=(a[0]-x[0])/v[0]; z=(a[0],x[1]+t*v[1]); inside=min(a[1],b[1])<=z[1]<=max(a[1],b[1])
   else:
    if not v[1]:continue
    t=(a[1]-x[1])/v[1]; z=(x[0]+t*v[0],a[1]); inside=min(a[0],b[0])<=z[0]<=max(a[0],b[0])
   if t>0 and inside:cand.append((t,i,z))
  if not cand:return None
  t,i,z=min(cand);elapsed+=t;pts.append(z)
  if z in P:
   if z in convex:return {'velocity':v0,'word':wallword,'corner':z,'points':pts,'elapsed':elapsed,'first_corner_convex':True}
   return None
  a=P[i];b=P[(i+1)%len(P)];wallword.append(i)
  v=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1]);x=z
 return None
attempts=0;ans=None
for size in range(1,25):
 for p in range(1,size+1):
  for q in range(1,size+1):
   if max(p,q)!=size or gcd(p,q)!=1:continue
   deadline();attempts+=1;v0=(-p,-q);ans=trace(v0)
   if ans:break
  if ans:break
 if ans:break
def ser(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,tuple):return [ser(y) for y in x]
 if isinstance(x,list):return [ser(y) for y in x]
 if isinstance(x,dict):return {k:ser(v) for k,v in x.items()}
 return x
out={'mode':'ONE prescribed-room first-positive corner-to-convex return search','attempts':attempts,'vertices':P,'origin':O,'area2':area2,'convex_count':len(convex),'reflex_count':len(P)-len(convex),'result':ans,'deadline':meta['deadline_utc'],'does_not_prove_darkness_on_failure':True}
(ROOT/'reflex-return-control.json').write_text(json.dumps(ser(out),indent=2)+'\n')
print(json.dumps(ser(out),indent=2))
