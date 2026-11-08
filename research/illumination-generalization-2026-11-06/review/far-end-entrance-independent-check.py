"""Independent prescribed A34 exact charts, equality and first-target corner controls."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('mid',R/'midheight-comb-independent-check.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);g=m.g
rows=[]
# Fixed supplied controls, not a search. First tests equality plus-image mouth failure.
for chart,xs,ys,w,D,b in [('direct',1,4,Q(3,2),1,1),('direct',1,Q(7,2),3,1,1),('left',3,2,5,1,Q(2,3)),('direct',2,10,2,Q(7,4),Q(1,3)),('left',1,11,4,1,Q(3,2))]:
 c=Q(3);l=Q(5);u=Q(2);xs,ys,w,D,b=map(Q,(xs,ys,w,D,b));C=c-xs if chart=='direct' else c+xs;L=2*w-D;assert L>=C
 choices=[]
 for sigma in (1,-1):
  low=((l-ys)*(C+L)/C+ys-l-sigma*b)/(2*u);n=int(low//1)+1;Y=l+sigma*b+2*u*n;t=(Y-ys)/(C+L);z=ys+C*t
  if l<z<l+u:choices.append((sigma,n,Y,t,z))
 assert choices
 sigma,n,Y,t,z=choices[0]
 if chart=='direct' and ys==Q(7,2):
  sigma=1;n=2;Y=l+b+2*u*n;t=(Y-ys)/(C+L);z=ys+C*t;assert l<z<l+u
 qf=C+w;qt=C+L;yf=ys+qf*t;corner=(yf-l)%u==0
 stop=C+D if corner else qt;events=[C,stop]
 if chart=='left':events.append(xs)
 if not corner:events.append(qf)
 for j in range(int((min(z,ys+stop*t)-l)//u)-1,int((max(z,ys+stop*t)-l)//u)+2):
  q=(l+j*u-ys)/t
  if C<q<stop:events.append(q)
 path=[(xs,ys)]
 for q in sorted(set(events)):
  if q<C:
   x=abs(-xs+q) if chart=='left' else xs+q;y=ys+q*t
  else:
   advance=q-C;x=c+(advance if advance<=w else 2*w-advance);y=l+g.fold(ys+q*t-l,u)
  path.append((x,y))
 assert path[-1]==(c+D,l+b)
 V=m.polygon(c,[(Q(1),Q(3),Q(5)),(l,l+u,c+w),(Q(9),Q(12),Q(6))],Q(0),Q(13));result=g.path_check(V,path)
 rows.append({'chart':chart,'source':path[0],'target':path[-1],'C':C,'L':L,'sigma':sigma,'n':n,'slope':t,'strict_portal':z,'equality':L==C,'far_corner_early_target':corner,**result})
assert rows[0]['equality'] and rows[0]['sigma']==-1 and rows[1]['far_corner_early_target']
out={'status':'FIVE_PRESCRIBED_ACTUAL_CHARTS_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'discovery':False}
(R/'far-end-entrance-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
