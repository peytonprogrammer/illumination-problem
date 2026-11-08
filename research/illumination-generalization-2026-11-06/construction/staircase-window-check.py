#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import ast,json,hashlib,signal,time
ROOT=Path(__file__).resolve().parent
eff=json.loads((ROOT/'staircase-onepass-effort.json').read_text());end=datetime.fromisoformat(eff['aggregate_deadline_utc']).timestamp()
if time.time()>=end:raise SystemExit('A11 original deadline expired')
signal.alarm(max(1,int(end-time.time())))
# Reuse only pure local exact-wall guard functions; do not execute its driver/writes.
source=ROOT/'T-whole-check.py';mod=ast.parse(source.read_text());ns={'F':F}
exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(source),'exec'),ns)
verify=ns['verify']
def near(x):
 k=x.numerator//x.denominator
 return min((k,k+1),key=lambda n:(abs(x-n),n))
def ceil(x):return -((-x.numerator)//x.denominator)
def fold(z,w):return w-abs(z%(2*w)-w)
def construct(A,b,a,c,d,H,S,T):
 xs,ys=S;xt,yt=T;Hs=c-ys;g=d-c;Ht=yt-d;D=Hs+g+Ht;rho=g/Hs
 if rho<=(b-a)/(A-b):
  k=1+ceil(A*g/(b*Hs));K=2*k*b
  n=near((Hs*K+g*xs)/(2*A*g));regime='round_source'
 else:
  assert rho>=a/b
  n=1;theta=(2*n*A-xs)/Hs;K=2*b*near(g*theta/(2*b));regime='round_exit'
 theta=(2*n*A-xs)/Hs;R=b*(Hs+g)/Hs
 assert n>=1 and K>=0 and abs(K-g*theta)+a<=R
 lo=(2*n*A+K-xs-a)/(Hs+g);hi=(2*n*A+K-xs+a)/(Hs+g)
 Zlo=xs+D*lo-2*n*A-K;Zhi=xs+D*hi-2*n*A-K
 candidates=[]
 for sign in (1,-1):
  r=(Zlo-sign*xt)/(2*a);m=r.numerator//r.denominator+1
  candidates.append(sign*xt+2*m*a)
 Y=min(candidates);assert Zlo<Y<Zhi
 tau=(2*n*A+K+Y-xs)/D;assert lo<tau<hi
 z=xs+Hs*tau-2*n*A;w=xs+(Hs+g)*tau-2*n*A-K
 assert abs(z)<b and abs(w)<a and fold(Y,a)==xt
 events=set()
 for y0,y1,u0,width in [(ys,c,xs,A),(c,d,z,b),(d,yt,w,a)]:
  low=u0//width-1;high=(u0+tau*(y1-y0))//width+2
  for j in range(int(low),int(high)+1):
   yy=y0+(j*width-u0)/tau
   if y0<=yy<=y1 and ys<yy<yt:events.add((F(0) if j%2==0 else width,yy))
 points=[S]+sorted(events,key=lambda p:p[1])+[T]
 assert len({p[1] for p in points})==len(points)
 polygon=[(0,0),(A,0),(A,c),(b,c),(b,d),(a,d),(a,H),(0,H)]
 result=verify(polygon,points)
 return {'regime':regime,'tau':str(tau),'z':str(z),'w':str(w),'n':n,'K':str(K),'Ht':str(Ht),'segments':result['segments'],'contacts':result['contacts'],'all_actual_wall_guards':'PASS'}
fixtures=[
 (9,6,2,2,3,5,(F(17,2),F(1)),(F(1,2),F(4))),
 (9,6,2,2,9,12,(F(17,2),F(3,2)),(F(3,2),F(10))),
 (4,2,1,2,F(5,2),4,(F(3),F(1)),(F(1,2),F(7,2))),
 (4,2,1,2,3,4,(F(2),F(1)),(F(1,2),F(3))),
 (10,2,1,1,2,3,(F(9),F(1,2)),(F(1,2),F(5,2))),
]
results=[]
for row in fixtures:
 vals=[F(x) for x in row[:6]];results.append(construct(*vals,row[6],row[7]))
signal.alarm(0)
out={'status':'PASS','kind':'prescribed exact constructor and actual-wall checks; not discovery','fixtures':results,'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'staircase-window-proof.md',source]},'within_original_A11_deadline':time.time()<end,'ended_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False}
(ROOT/'staircase-window-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(results,indent=2))
