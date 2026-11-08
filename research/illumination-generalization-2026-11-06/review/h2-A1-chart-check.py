"""Focused R47 protected one-tooth chart discriminator; original deadline enforced."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
import json,time,math
R=Path(__file__).resolve().parent;eff=json.loads((R/'h2-A1-effort.json').read_text());deadline=datetime.fromisoformat(eff['deadline_utc']).timestamp()
def guard():
 if time.time()>=deadline:raise TimeoutError('R47 original deadline')
def intersect(I,a,b,lo,hi):
 L,U=I
 if b==0:return I if lo<a<hi else None
 x,y=Q(lo-a,b),Q(hi-a,b)
 if b<0:x,y=y,x
 L=max(L,x);U=min(U,y);return (L,U) if L<U else None
def apply(intervals,a,b,ranges):
 return [J for I in intervals for lo,hi in ranges if (J:=intersect(I,a,b,lo,hi)) is not None]
def charts(D,base):
 out=[]
 for es in [D,D+2]:
  for et in [D,D+2]:
   for m in range(4):
    for n in range(4):
     for ns in range(-4,5):
      for nt in range(-4,5):
       for epsilon in [1,-1]:
        for sign in [1,-1]:
         guard();sy=(-2+2*ns,epsilon*es);ty=(2+2*nt,-sign*et);p1=(sy[0],epsilon*(es+2*m+1));p2=(ty[0],ty[1]-sign*(2*n+1));I=[(Q(0),Q(20))]
         for a,b,ranges in [(*sy,[(-3,-1)]),(*ty,[(1,3)]),(*p1,[(base,base+2)]),(*p2,[(base,base+2)])]:
          I=apply(I,a,b,ranges)
          if not I:break
         if not I:continue
         fields=[]
         for i in range(1,2*m+1):fields.append((sy[0],sy[1]+epsilon*i,[(-3,-2),(0,1)] if i%2 else [(-1,1)]))
         for i in range(1,2*n+1):fields.append((p2[0],p2[1]+sign*i,[(-1,1)] if i%2 else [(-3,-2),(0,1)]))
         for a,b,ranges in fields:
          I=apply(I,a,b,ranges)
          if not I:break
         if not I:continue
         den0=epsilon*p1[1]-sign*p2[1];num0=epsilon*(0 if sign==epsilon else 2*base+4)+sign*p2[0]-epsilon*p1[0]
         rr=Q(epsilon*p1[1]+sign*p2[1],2);C=epsilon*Q(p1[0]-base)+Q(num0,2)
         assert rr.denominator==C.denominator==1
         for L,U in I:
          roots={L,U}
          if es==D+2 or et==D+2:
           roots.update(Q(i) for i in range(int(L//1)-1,int(U//1)+2) if i%2 and L<i<U)
          if rr==0:
           if C.numerator%2==0:continue
          else:
           low,high=sorted([C+rr*L,C+rr*U])
           for j in range(int(low//2)-1,int(high//2)+2):
            z=(2*j-C)/rr
            if L<z<U:roots.add(z)
          roots=sorted(roots)
          for l,u in zip(roots,roots[1:]):
           if l<=0 or l>=u:continue
           ell=u-l
           cut=max(1,int((Q(4)/ell-den0)/2//1)+1,int((Q(num0)/l-den0)/2//1)+1)
           out.append(dict(D=D,base=base,es=es,et=et,m=m,n=n,ns=ns,nt=nt,sign=sign,epsilon=epsilon,L=l,U=u,den0=den0,num0=num0,cut=cut,sy=sy,ty=ty,p1=p1,p2=p2))
 return out
def pick(c,w):
 den=2*w+c['den0'];num=c['num0'];L,U=c['L'],c['U'];assert den>0
 k=max(0,int(((L*den-num)/4)//1)+1);tau=Q(num+4*k,den)
 return dict(c,w=w,k=k,tau=tau) if L<tau<U else None
families=[]
for D in range(3):
 for base in [-2,1]:
  C=charts(D,base)
  if not C:
   families.append({"D":D,"base":base,"empty":True});print("EMPTY",D,base);continue
  best=min(C,key=lambda z:z['cut']);cut=best['cut'];covered=[];missing=[]
  for w in range(1,cut):
   matches=[z for c in C if (z:=pick(c,w)) is not None]
   if matches:covered.append(min(matches,key=lambda z:2*z['m']+2*z['n']+2*z['k']+(z['sign']==-1)+(z['es']>D)+(z['et']>D)))
   else:missing.append(w)
  families.append({'D':D,'base':base,'chart_count':len(C),'tail':best,'finite':covered,'missing':missing})
out={'status':'EXACT_R47_CHART_DISCRIMINATION','discovery':True,'original_deadline_utc':eff['deadline_utc'],'finished_utc':datetime.now(timezone.utc).isoformat(),'families':families,'whole_goal_complete':False}
(R/'h2-A1-chart-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps([{k:v for k,v in f.items() if k not in ['tail','finite']}|{'cut':f['tail']['cut'],'finite_count':len(f['finite'])} for f in families if not f.get('empty')]))
