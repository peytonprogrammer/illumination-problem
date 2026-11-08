"""R47 same-effort genuine end charts for remaining D0,a2 adjacent family."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
import json,time,ast
R=Path(__file__).resolve().parent;eff=json.loads((R/'h2-A1-effort.json').read_text());deadline=datetime.fromisoformat(eff['deadline_utc']).timestamp()
# Reuse definitions only, never rerun another search or writer.
a=ast.parse((R/'h2-A1-chart-check.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ['guard','intersect','apply','pick']],type_ignores=[]),'local defs','exec'))
def ranges(side):
 actual=[(-4,-3),(-1,1),(3,5)] if side=='R' else [(-4,-2),(0,1),(3,5)]
 return [(lo+18*j,hi+18*j) for lo,hi in actual for j in range(-2,3)]+[(10-hi+18*j,10-lo+18*j) for lo,hi in actual for j in range(-2,3)]
def charts(Tz,base):
 out=[];D=0
 for es in [0,2]:
  for et in [0,2]:
   for m in range(5):
    for n in range(5):
     for ns in range(-5,6):
      for nt in range(-5,6):
       for epsilon in [1,-1]:
        for sign in [1,-1]:
         guard();sy=(-2+2*ns,epsilon*es);ty=(Tz+2*nt,-sign*et);p1=(sy[0],epsilon*(es+2*m+1));p2=(ty[0],-sign*(et+2*n+1));I=[(Q(0),Q(30))]
         for aa,bb,ran in [(*sy,[(-3,-1)]),(*ty,[(Tz-1,Tz+1)]),(*p1,[(base,base+2)]),(*p2,[(base,base+2)])]:
          I=apply(I,aa,bb,ran)
          if not I:break
         if not I:continue
         fields=[]
         for i in range(1,2*m+1):fields.append((sy[0],sy[1]+epsilon*i,ranges('L' if i%2 else 'R')))
         for i in range(1,2*n+1):fields.append((p2[0],p2[1]+sign*i,ranges('R' if i%2 else 'L')))
         for aa,bb,ran in fields:
          I=apply(I,aa,bb,ran)
          if not I:break
         if not I:continue
         den0=epsilon*p1[1]-sign*p2[1];num0=epsilon*(0 if sign==epsilon else 2*base+4)+sign*p2[0]-epsilon*p1[0]
         rr=Q(epsilon*p1[1]+sign*p2[1],2);C=epsilon*(p1[0]-base)+Q(num0,2)
         assert rr.denominator==C.denominator==1
         for L,U in I:
          roots={L,U}
          if es==2 or et==2:roots.update(Q(i) for i in range(int(L//1)-1,int(U//1)+2) if i%2 and L<i<U)
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
           ell=u-l;cut=max(1,int((Q(4)/ell-den0)/2//1)+1,int((Q(num0)/l-den0)/2//1)+1)
           out.append(dict(D=0,Tz=Tz,base=base,es=es,et=et,m=m,n=n,ns=ns,nt=nt,sign=sign,epsilon=epsilon,L=l,U=u,den0=den0,num0=num0,cut=cut,sy=sy,ty=ty,p1=p1,p2=p2))
 return out
allc=[]
for Tz,base in [(8,1),(8,7),(-10,1),(-10,-11)]:allc.extend(charts(Tz,base))
assert allc
best=min(allc,key=lambda z:z['cut']);covered=[];missing=[]
for w in range(1,best['cut']):
 matches=[z for c in allc if (z:=pick(c,w)) is not None]
 if matches:covered.append(min(matches,key=lambda z:2*z['m']+2*z['n']+2*z['k']))
 else:missing.append(w)
out={'status':'R47_END_CHART_DISCRIMINATION','discovery':True,'original_deadline_utc':eff['deadline_utc'],'finished_utc':datetime.now(timezone.utc).isoformat(),'chart_count':len(allc),'tail':best,'finite':covered,'missing':missing,'whole_goal_complete':False}
(R/'h2-A1-end-chart-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['tail','finite']}|{'cut':best['cut'],'finite_count':len(covered)}))
