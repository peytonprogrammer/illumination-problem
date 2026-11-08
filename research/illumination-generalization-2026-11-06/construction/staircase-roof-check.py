#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import ast,json,hashlib,signal,time
ROOT=Path(__file__).resolve().parent
EFF=ROOT/'staircase-roof-effort.json';eff=json.loads(EFF.read_text());end=datetime.fromisoformat(eff['aggregate_deadline_utc']).timestamp()
if time.time()>=end:raise SystemExit('Original A12 deadline expired')
signal.alarm(max(1,int(end-time.time())))
source=ROOT/'T-whole-check.py';ns={'F':F};mod=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(source),'exec'),ns)
verify=ns['verify']
def near(x):
 k=x.numerator//x.denominator
 return min((k,k+1),key=lambda n:(abs(x-n),n))
def fold(x,w):return w-abs(x%(2*w)-w)
def construct(A,b,a,c,d,H,S,T):
 xs,ys=S;xt,yt=T;Hs=c-ys;g=d-c;h=H-d;Ht=yt-d;T0=Hs+g;v=2*h-Ht;D=T0+v
 assert v>=2*T0 and h<v<=2*h
 theta=(2*A-xs)/Hs;K=2*b*near(g*theta/(2*b));R=b*T0/Hs
 ul=max(g*theta-R,K-a);uh=min(g*theta+R,K+a);assert uh-ul>a
 tl=(ul+2*A-xs)/T0;th=(uh+2*A-xs)/T0
 zl=xs+D*tl-2*A-K;zh=xs+D*th-2*A-K;assert zh-zl>3*a
 u=min(xt,a-xt);c0=F(0) if xt<=a/2 else a;C=c0+2*a*near(((zl+zh)/2-c0)/(2*a));cand=[C-u,C+u]
 good=[];bad=0
 for Y in cand:
  assert zl<Y<zh and fold(Y,a)==xt
  tau=(2*A+K+Y-xs)/D;assert tl<tau<th
  roof=xs+(T0+h)*tau-2*A-K
  if (roof/a).denominator==1:bad+=1
  else:good.append((Y,tau,roof))
 assert good
 Y,tau,roof=good[0];z=xs+Hs*tau-2*A;w=xs+T0*tau-2*A-K;assert abs(z)<b and abs(w)<a
 events={}
 for y0,y1,u0,width,upper in [(ys,c,xs,A,False),(c,d,z,b,False),(d,d+v,w,a,True)]:
  for j in range(int(u0//width)-1,int((u0+tau*(y1-y0))//width)+2):
   et=y0+(j*width-u0)/tau
   if y0<=et<=y1 and ys<et<d+v:
    yy=d+fold(et-d,h) if upper else et
    p=(F(0) if j%2==0 else width,yy)
    assert et not in events or events[et]==p
    events[et]=p
 roof_time=d+h;events[roof_time]=(fold(roof,a),H)
 pts=[S]+[p for _,p in sorted(events.items())]+[T]
 polygon=[(0,0),(A,0),(A,c),(b,c),(b,d),(a,d),(a,H),(0,H)]
 check=verify(polygon,pts)
 return {'tau':str(tau),'z':str(z),'w':str(w),'roof_unfolded_x':str(roof),'Ht':str(Ht),'rejected_roof_candidate_count':bad,'contacts':check['contacts'],'segments':check['segments'],'all_actual_wall_guards':'PASS'}
fixtures=[
 (2,F(11,10),1,1,F(11,10),4,(F(19,10),F(1,2)),(F(1,2),F(21,10))),
 (5,F(11,10),1,1,F(11,10),4,(F(11,10),F(1,2)),(F(1,4),F(11,10))),
 (100,F(11,10),1,1,F(11,10),4,(F(99),F(1,2)),(F(3,4),F(3))),
 (4,F(3,2),1,1,F(3,2),F(9,2),(F(7,2),F(1,4)),(F(1,3),F(2))),
]
res=[construct(*[F(x) for x in row[:6]],row[6],row[7]) for row in fixtures]
signal.alarm(0)
out={'status':'PASS','kind':'prescribed exact two-candidate constructor and actual wall controls, not discovery','fixtures':res,'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'staircase-roof-proof.md',source]},'ended_utc':datetime.now(timezone.utc).isoformat(),'within_original_A12_deadline':time.time()<end,'whole_goal_complete':False}
(ROOT/'staircase-roof-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(res,indent=2))
