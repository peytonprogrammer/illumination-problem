"""Prescribed A37 real-far-chart controls, including separately proposed D0 extension."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def prefix(c,w,D,t,n,far):
    E=2*w-D if far else D;k=n//2;sgn=1 if n%2==0 else -1;r=sgn+E*t-4*k;assert 0<r<2
    p=[(c+E,Q(1))]
    for j in range(1 if sgn==1 else 0,2*k+1):p.append((c+E-(2*j-sgn)/t,Q(2 if j%2 else 0)))
    if E:p.append((c,r))
    if far:
        ext=[p[0]]
        for a,b in zip(p,p[1:]):
            if a[0]>c+w>b[0]:
                y=a[1]+(b[1]-a[1])*(a[0]-c-w)/(a[0]-b[0]);assert 0<y<2;ext.append((c+w,y))
            ext.append(b)
        p=[(c+w-abs(x-c-w),y) for x,y in ext]
    return p,r
rows=[]
for c,D,w,h in [(3,1,2,5),(2,2,3,5),(2,2,5,7),(2,0,1,5),(4,0,1,7),(6,0,1,9)]:
 c,D,w,h=map(Q,(c,D,w,h));z=w-D;assert z>0
 t=Q(0)
 for j in range(10000):
  nf=int(((2*w-D)*t/2+Q(1,2))//1);nd=int((D*t/2+Q(1,2))//1);nxt=(2*h+2*nf+2*nd)/(2*(c+w))
  if nxt==t:break
  assert nxt>t;t=nxt
 else:raise AssertionError('fixed control iteration cap')
 m=z*t-(nf-nd);assert m!=0 and(z*t).denominator!=1
 sf=m<0;ns=nf if sf else nd;nt=nd if sf else nf
 ps,rs=prefix(c,w,D,t,ns,sf);pt,rt=prefix(c,w,D,t,nt,not sf);mu=h+2;lo=Q(1);H=2*h+2
 path=[(x,lo+y) for x,y in ps]+[(Q(0),mu-abs(m))]+[(x,lo+H-y) for x,y in reversed(pt)]
 assert path[0]==(c+D,2) and path[-1]==(c+D,2*h+2)
 # Source or target normal zero arm is one point, no duplicate portal.
 V=[(Q(0),Q(0)),(c,Q(0)),(c,Q(1)),(c+w,Q(1)),(c+w,Q(3)),(c,Q(3)),(c,2*h+1),(c+w,2*h+1),(c+w,2*h+3),(c,2*h+3),(c,2*h+4),(Q(0),2*h+4),(Q(0),mu+2),(Q(-1),mu+2),(Q(-1),mu),(Q(0),mu)]
 g.simple(V);target=path[-1]
 for i,(a,b) in enumerate(zip(path,path[1:])):
  if g.on(a,b,target):path=path[:i+1]+[target];break
 result=g.path_check(V,path)
 rows.append({'parameters':[c,D,w,h],'seam_extension':D==0,'slope':t,'z_times_slope':z*t,'central_offset':-abs(m),'source_far':sf,**result})
out={'status':'SIX_PRESCRIBED_ACTUAL_FAR_TWISTS_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'discovery':False,'scope':'Three A37 D>0 controls and three proposed D=0 seam-extension controls, distinguished.'}
(R/'mouth-endpoint-twist-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
