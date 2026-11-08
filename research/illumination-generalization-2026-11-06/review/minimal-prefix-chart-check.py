"""R46 focused exact chart discrimination; deadline includes all preliminary work."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
import json,time
R=Path(__file__).resolve().parent;eff=json.loads((R/'minimal-prefix-effort.json').read_text());deadline=datetime.fromisoformat(eff['deadline_utc']).timestamp()
def guard():
    if time.time()>=deadline:raise TimeoutError('Original aggregate R46 deadline reached')
def restrict(I,a,b,lo,hi):
    L,U=I
    if b==0:return I if lo<a<hi else None
    x,y=Q(lo-a,b),Q(hi-a,b)
    if b<0:x,y=y,x
    L=max(L,x);U=min(U,y)
    return (L,U) if L<U else None
def charts(D):
    out=[]
    for es in [D,D+2]:
      for et in [D,D+2]:
       for m in range(9):
        for ns in range(-8,1):
         for nt in range(-8,9):
          for sign in [1,-1]:
           guard();sy=(-2+2*ns,es);p1=(sy[0],es+2*m+1);ty=(2+2*nt,-sign*et);p2=(ty[0],ty[1]-sign)
           cond=[(*sy,-3,-1),(*ty,1,3),(*p1,0,2),(*p2,0,2)]
           cond += [(sy[0],sy[1]+2*i-1,-2,0) for i in range(1,m+1)]
           cond += [(sy[0],sy[1]+2*i,-1,1) for i in range(1,m+1)]
           I=(Q(0),Q(100))
           for a,b,lo,hi in cond:
            I=restrict(I,a,b,lo,hi)
            if I is None:break
           if I is None:continue
           # R_s + 2w*tau = R_t +4k (up), or 4-R_t+4k (down).
           den0=p1[1]-sign*p2[1];num0=(0 if sign==1 else 4)+sign*p2[0]-p1[0]
           out.append(dict(D=D,es=es,et=et,m=m,ns=ns,nt=nt,sign=sign,L=I[0],U=I[1],den0=den0,num0=num0,sy=sy,ty=ty,p1=p1,p2=p2))
    return out
def pick(c,w):
    den=2*w+c['den0'];num=c['num0'];L,U=c['L'],c['U']
    if den<=0:return None
    low=(L*den-num)/4;high=(U*den-num)/4
    for k in range(max(0,int(low//1)+1),int(-((-high)//1))):
      tau=Q(num+4*k,den)
      if not L<tau<U:continue
      if (c['es']==c['D']+2 or c['et']==c['D']+2) and tau.denominator==1 and tau.numerator%2:continue
      far=c['p1'][0]+c['p1'][1]*tau+w*tau
      if far.denominator==1 and far.numerator%2==0:continue
      return dict(c,w=w,k=k,tau=tau)
    return None
rows=[];missing=[];counts=[]
for D,cut in enumerate([13,20,67]):
    C=charts(D);counts.append(len(C))
    for w in range(1,cut):
      matches=[v for c in C if (v:=pick(c,w)) is not None]
      if not matches:missing.append([D,w]);continue
      c=min(matches,key=lambda z:2*z['m']+2*z['k']+(z['es']>D)+(z['et']>D));rows.append(c)
out={'status':'EXACT_PROTECTED_CHART_DISCRIMINATION','discovery':True,'original_deadline_utc':eff['deadline_utc'],'finished_utc':datetime.now(timezone.utc).isoformat(),'chart_counts':counts,'covered':len(rows),'missing':missing,'rows':rows,'whole_goal_complete':False}
(R/'minimal-prefix-chart-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
