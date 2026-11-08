from fractions import Fraction as F
from pathlib import Path
from datetime import datetime
from math import gcd
import json,time
R=Path(__file__).resolve().parent
END=datetime.fromisoformat(json.loads((R/'reflex-coalescence-effort.json').read_text())['deadline_utc']).timestamp()
P0=[(2,2),(4,2),(4,0),(2,0),(2,-4),(-2,-4),(-2,-3),(0,-3),(0,0),(-3,0),(-3,-2),(-4,-2),(-4,2),(0,2),(0,4),(2,4)]
def chk():
 if time.time()>=END:raise TimeoutError('Original A26 deadline')
def trace(lam,p,q):
 P=[(F(lam*x),F(lam*y)) for x,y in P0];S=(F(2*lam-2),F(2*lam+2));T=(F(2*lam+2),F(2*lam-2));x=S;v=(p,q);word=[];pts=[x]
 for n in range(250):
  chk();cs=[]
  for i,a in enumerate(P):
   b=P[(i+1)%len(P)]
   if a[0]==b[0]:
    t=(a[0]-x[0])/v[0];z=(a[0],x[1]+t*v[1]);ins=min(a[1],b[1])<=z[1]<=max(a[1],b[1])
   else:
    t=(a[1]-x[1])/v[1];z=(x[0]+t*v[0],a[1]);ins=min(a[0],b[0])<=z[0]<=max(a[0],b[0])
   if t>0 and ins:cs.append((t,i,z))
  if not cs:return None
  t,i,z=min(cs);tx=(T[0]-x[0])/v[0]
  if tx>0 and x[1]+tx*v[1]==T[1] and tx<t:
   return {'lambda':lam,'velocity':[p,q],'word':word,'points':pts+[T],'reflections':len(word),'source':S,'target':T}
  if z in P:return None
  pts.append(z);word.append(i);a=P[i];b=P[(i+1)%len(P)];v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1]);x=z
 return None
out=[]
for lam in range(2,9):
 ans=None;count=0
 for n in range(1,11):
  for p in range(1,n+1):
   for q in range(1,n+1):
    if max(p,q)!=n or gcd(p,q)!=1:continue
    for sx,sy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
     count+=1;ans=trace(lam,sx*p,sy*q)
     if ans:break
    if ans:break
   if ans:break
  if ans:break
 out.append({'lambda':lam,'directions_checked':count,'certificate':ans})
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,(tuple,list)):return [enc(y) for y in x]
 if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
 return x
res={'status':'ALL_PREFIX_POSITIVE' if all(x['certificate'] for x in out) else 'PARTIAL_POSITIVE_ONLY','inputs':'exactly integerlambda2..8, fixed16wallfamily/actualmarks','maxnorm':10,'per_direction_contact_cap':250,'original_deadline':END,'cases':out,'no_failure_darkness_inference':True}
(R/'reflex-prefix-check.json').write_text(json.dumps(enc(res),indent=2)+'\n')
for x in out:print(x['lambda'],x['directions_checked'],None if not x['certificate'] else (x['certificate']['velocity'],x['certificate']['reflections'],x['certificate']['word']))
print(res['status'])
