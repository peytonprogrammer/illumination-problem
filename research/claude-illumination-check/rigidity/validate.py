"""Validate event sign conventions: perturb the room along random closure-preserving directions,
then trace the predicted path in the perturbed room with exact rationals."""
import sys,random,json
sys.argv=['x','12'];src=open('rigidity_check.py').read().split('# closure constraints and symmetry directions')[0]
# keep event data per functional
src=src.replace("events.append(dict(dir=[p,q],corner=list(V[k]),side=side))","events.append(dict(dir=[p,q],corner=list(V[k]),side=side,g=g,A=A))")
exec(src)
from fractions import Fraction as Fr
def trace_poly(P,s,t,d,maxb=600):
 n=len(P);E=[(P[i],P[(i+1)%n]) for i in range(n)];pos=s
 for _ in range(maxb):
  best=None
  for a,b in E:
   if a[0]==b[0]:
    if d[0]==0:continue
    u=(a[0]-pos[0])/d[0];y=pos[1]+u*d[1]
    if u>0 and min(a[1],b[1])<=y<=max(a[1],b[1]) and (best is None or u<best[0]):best=(u,'v',(a[0],y))
   else:
    if d[1]==0:continue
    u=(a[1]-pos[1])/d[1];x=pos[0]+u*d[0]
    if u>0 and min(a[0],b[0])<=x<=max(a[0],b[0]) and (best is None or u<best[0]):best=(u,'h',(x,a[1]))
  u,kind,hit=best
  du=(t[0]-pos[0])/d[0] if d[0] else (t[1]-pos[1])/d[1]
  if 0<du<u and pos[0]+du*d[0]==t[0] and pos[1]+du*d[1]==t[1]:return 'reach'
  if hit in set(P):return 'corner'
  d=(-d[0],d[1]) if kind=='v' else (d[0],-d[1]);pos=hit
 return 'budget'
random.seed(1);ok=bad=0;checked=0
for trial in range(6):
 th=[Fr(random.randint(-5,5)) for _ in range(D)]
 # project onto closure: fix by adjusting last horizontal and last vertical edge lengths
 hs=[k for k in range(W) if V[(k+1)%W][0]-V[k][0]];vs=[k for k in range(W) if V[(k+1)%W][1]-V[k][1]]
 th[2+hs[-1]]-=sum(th[2+k] for k in hs);th[2+vs[-1]]-=sum(th[2+k] for k in vs)
 lam=Fr(1,10**5);par=[a+lam*b for a,b in zip(theta0,th)]
 P=[(sum(a*b for a,b in zip(VX[k],par)),sum(a*b for a,b in zip(VY[k],par))) for k in range(W)]
 s=(par[IS],par[IS+1]);t=(par[IT],par[IT+1])
 for e in events:
  fth=sum(a*b for a,b in zip(e['g'],th))
  if fth==0:continue
  pred_lit=(fth<0) if e['side']>0 else (fth>0)
  A=e['A'];dvec=(sum(a*b for a,b in zip(A[0],par)),sum(a*b for a,b in zip(A[1],par)))
  # unfolded direction -> room direction at start is the same (transform is identity at s)
  r=trace_poly(P,s,t,dvec);actual=(r=='reach');checked+=1
  if actual==pred_lit:ok+=1
  else:bad+=1
print(json.dumps(dict(checked=checked,agree=ok,disagree=bad)))
