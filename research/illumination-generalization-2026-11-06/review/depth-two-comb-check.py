"""Prescribed exact phase identities, actual twists and c4 affine transport; no search."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def match(c,H,D):
 c,H,D=map(Q,(c,H,D));t=Q(0)
 for j in range(10000):
  nf=((4-D)*t/2+Q(1,2))//1;nd=(D*t/2+Q(1,2))//1;nxt=(H+nf+nd)/(c+2)
  if nxt==t:break
  assert nxt>t;t=nxt
 else:raise AssertionError('prescribed phase cap')
 assert 0<(4-D)*t+1-2*nf<2 and 0<D*t+1-2*nd<2
 m=(2-D)*t-(nf-nd)
 if m==0:
  if D==1:assert t.denominator==1 and int(t)%2==0 and H%(2*c)==0
  else:assert c and (2*H)%c==0
 return t,nf,nd,m
phase=0;resonance=0
for c in range(2,11):
 for H in range(2,81):
  for D in(0,1):
   t,nf,nd,m=match(c,H,D);phase+=1;resonance+=m==0

def prefix(c,D,t,n,far):
 w=Q(2);E=2*w-D if far else D;k=n//2;sg=1 if n%2==0 else-1;r=sg+E*t-4*k;assert 0<r<2
 p=[(c+E,Q(1))]
 for j in range(1 if sg==1 else 0,2*k+1):p.append((c+E-(2*j-sg)/t,Q(2 if j%2 else 0)))
 if E:p.append((c,r))
 if far:
  ext=[p[0]]
  for a,b in zip(p,p[1:]):
   if a[0]>c+w>b[0]:
    y=a[1]+(b[1]-a[1])*(a[0]-c-w)/(a[0]-b[0]);assert 0<y<2;ext.append((c+w,y))
   ext.append(b)
  p=[(c+w-abs(x-c-w),y) for x,y in ext]
 return p
rows=[]
for c,H in[(2,3),(3,4),(3,5),(4,6),(5,6),(6,8)]:
 c,H=Q(c),Q(H);D=Q(1);t,nf,nd,m=match(c,H,D);assert m and t.denominator!=1
 sf=m<0;ps=prefix(c,D,t,nf if sf else nd,sf);pt=prefix(c,D,t,nd if sf else nf,not sf);mu=H+2
 path=[(x,1+y) for x,y in ps]+[(0,mu-abs(m))]+[(x,2*H+3-y) for x,y in reversed(pt)]
 V=[(0,0),(c,0),(c,1),(c+2,1),(c+2,3),(c,3),(c,2*H+1),(c+2,2*H+1),(c+2,2*H+3),(c,2*H+3),(c,2*H+4),(0,2*H+4),(0,mu+2),(-2,mu+2),(-2,mu),(0,mu)]
 V=[tuple(map(Q,z)) for z in V];g.simple(V)
 target=path[-1]
 for j,(a,b) in enumerate(zip(path,path[1:])):
  if g.on(a,b,target):path=path[:j+1]+[target];break
 assert path[0]==(c+1,2) and path[-1]==(c+1,2*H+2)
 rows.append({'case':'D1_twist','c':str(c),'H':str(H),'tau':str(t),'m':str(m),**g.path_check(V,path)})
V=[(0,0),(2,0),(2,1),(3,1),(3,3),(2,3),(2,5),(3,5),(3,7),(2,7),(2,10),(0,10),(0,8),(-1,8),(-1,6),(0,6),(0,4),(-1,4),(-1,2),(0,2)]
path=[(2,2),(-1,3),(2,4),(0,Q(14,3)),(3,Q(17,3)),(2,6)]
for reflect in(False,True):
 VV=[(2*Q(x),Q(y)) for x,y in V];pp=[(2*Q(x),Q(y)) for x,y in path]
 if reflect:VV=[(4-x,y) for x,y in VV];pp=[(4-x,y) for x,y in pp]
 g.simple(VV);assert all(x.denominator==1 and y.denominator==1 for x,y in VV)
 assert all(int(z[0])%2==int(z[1])%2==0 for z in(pp[0],pp[-1]))
 rows.append({'case':'c4_D0_transport','reflected':reflect,**g.path_check(VV,pp)})
out={'status':'PRESCRIBED_PHASE_AND_PHYSICAL_CONTROLS_PASS','phase_cases':phase,'zero_displacement_cases':resonance,'physical_paths':len(rows),'rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'depth-two-comb-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
