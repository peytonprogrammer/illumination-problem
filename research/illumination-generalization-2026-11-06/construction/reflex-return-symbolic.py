from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import json,time,math
R=Path(__file__).resolve().parent
END=datetime.fromisoformat(json.loads((R/'reflex-coalescence-effort.json').read_text())['deadline_utc']).timestamp()
def guardtime():
 if time.time()>=END:raise TimeoutError('Original A26 deadline reached')
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def sub(x,y):return(x[0]-y[0],x[1]-y[1])
def mul(x,k):return(x[0]*k,x[1]*k)
def div(x,k):return(x[0]/k,x[1]/k)
def val(x,l):return x[0]*l+x[1]
def enc(x):return [str(x[0]),str(x[1])]
P0=[(2,2),(4,2),(4,0),(2,0),(2,-4),(-2,-4),(-2,-3),(0,-3),(0,0),(-3,0),(-3,-2),(-4,-2),(-4,2),(0,2),(0,4),(2,4)]
P=[((F(x),F(0)),(F(y),F(0))) for x,y in P0]
S=((F(2),F(-2)),(F(2),F(2)));T=((F(2),F(2)),(F(2),F(-2)))
word=[4,6]*3+[5,4]+[6,4]*3
x=S;v=(-1,-3);polys=[];legs=[];total=(F(0),F(0))
for step,idx in enumerate(word+[None]):
 guardtime()
 if idx is None:
  tt=div(sub(T[0],x[0]),v[0]);z=T
  assert sub(sub(T[1],x[1]),mul(tt,v[1]))==(0,0)
 else:
  a,b=P[idx],P[(idx+1)%len(P)]
  axis=0 if a[0]==b[0] else 1
  tt=div(sub(a[axis],x[axis]),v[axis])
  z=(add(x[0],mul(tt,v[0])),add(x[1],mul(tt,v[1])))
 polys.append(tt);candidates=[]
 for j,a in enumerate(P):
  b=P[(j+1)%len(P)];axis=0 if a[0]==b[0] else 1;other=1-axis
  tj=div(sub(a[axis],x[axis]),v[axis]);qj=add(x[other],mul(tj,v[other]))
  lo,hi=(a[other],b[other]) if P0[j][other]<P0[(j+1)%len(P)][other] else(b[other],a[other])
  low=sub(qj,lo);high=sub(hi,qj);rel=sub(tj,tt)
  polys.extend([tj,low,high,rel]);candidates.append((j,tj,low,high,rel))
 legs.append({'step':step,'wall':idx,'start':x,'end':z,'velocity':v,'duration':tt,'candidates':candidates})
 total=add(total,tt);x=z
 if idx is not None:
  a,b=P[idx],P[(idx+1)%len(P)];v=(-v[0],v[1]) if a[0]==b[0] else(v[0],-v[1])
assert x==T
# Every decision uses only signs of these affine polynomials. Choose a tail
# beyond ALL nonnegative roots. No test at finitely many lambdas is generalized.
roots=[abs(b/a) for a,b in polys if a]
M=max(2,math.floor(max(roots,default=F(0)))+2)
assert all(not a or M>abs(b/a) for a,b in polys)
for leg in legs:
 guardtime();tt=val(leg['duration'],M);assert tt>0,(leg['step'],'negative time')
 hits=[]
 for j,tj,low,high,rel in leg['candidates']:
  tjv=val(tj,M)
  if tjv>0 and val(low,M)>=0 and val(high,M)>=0 and val(rel,M)<=0:
   hits.append((j,tjv,val(low,M),val(high,M)))
 if leg['wall'] is None:assert not hits,('final extra hit',hits)
 else:
  assert len(hits)==1 and hits[0][0]==leg['wall'] and hits[0][1]==tt,(leg['step'],hits,leg['wall'])
  assert hits[0][2]>0 and hits[0][3]>0,('corner',leg['step'],hits)
# Source/target lie strictly in top/right arms for all lambda>=M because lambda>1.
assert M>1
out={'status':'PASS_SYMBOLIC_ALL_REAL_LAMBDA_GE_CUTOFF','cutoff':M,'word':word,'reflections':len(word),'source':[enc(z) for z in S],'target':[enc(z) for z in T],'total_time':enc(total),'guard_polynomials':len(polys),'nonconstant_guard_polynomials':sum(bool(a) for a,b in polys),'max_absolute_root':str(max(roots,default=F(0))),'logic':'Each positive-ray/finite-wall membership and earlier-hit decision has fixed affine sign above the displayed all-root bound. Exact evaluation at one tail point establishes that fixed decision for the whole tail. All intended contacts strict; all other walls excluded.','legs':[{'step':z['step'],'wall':z['wall'],'start':[enc(t) for t in z['start']],'end':[enc(t) for t in z['end']],'velocity':z['velocity'],'duration':enc(z['duration'])} for z in legs],'full_guard_coefficients':[enc(z) for z in polys],'scope':'ONE fixed16wall scaled family and the stated actual marks; no darkness or universal wall claim'}
(R/'reflex-return-symbolic.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['legs','full_guard_coefficients']},indent=2))
print('contacts:')
for z in out['legs']:print(z['step'],z['wall'],z['end'])
