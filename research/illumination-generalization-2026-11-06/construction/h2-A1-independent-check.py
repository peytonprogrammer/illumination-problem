from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review';req=json.loads((P/'h2-A1-review-request.json').read_text())
for n,h in req['source_sha256'].items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
# Three literal exceptional tuples, with a separate rational implementation.
rows=[]
for D,a,es,et,n,ns,nt,k,tau in [(1,1,3,1,1,-1,0,0,F(3,5)),(2,2,4,2,1,-1,0,0,F(3,7)),(2,4,2,4,0,-2,3,3,F(13,8))]:
 ys=-2+2*ns+es*tau;yt=2+2*nt-et*tau;entry=ys+tau;exit=yt-(2*n+1)*tau
 assert -3<ys<-1 and 1<yt<3 and -2<entry<0 and -2<exit<0
 assert entry+2*a*tau==exit+4*k
 for i in range(1,n+1):assert -1<exit+(2*i-1)*tau<1 and 0<exit+2*i*tau<1
 phase=entry+2+a*tau;assert not(phase.denominator==1 and phase.numerator%2==0)
 assert not(tau.denominator==1 and tau.numerator%2)
 rows.append({'D':D,'a':a,'source_portal':ys,'target_portal':yt,'entry':entry,'exit':exit,'far_phase':phase})
# Independently replay the literal D0 universal path, with unequal real widths.
a,b=F(3,2),F(17,3);V=[(0,-4),(1,-4),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(2,1),(2,3),(1,3),(1,5),(0,5),(0,3),(-b,3),(-b,1),(0,1),(0,0),(-a,0),(-a,-2),(0,-2)];V=[tuple(map(F,v)) for v in V]
path=[(1,-2),(0,F(2,3)),(1,F(10,3)),(F(3,8),5),(0,4),(F(9,8),1),(F(15,8),3),(2,F(8,3)),(F(11,8),1),(1,2)];path=[tuple(map(F,v)) for v in path];edges=list(zip(V,V[1:]+V[:1]))
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
wall_ids=[];guards=0
for j,(x,y) in enumerate(zip(path,path[1:])):
 v=sub(y,x);hits=[]
 for i,(p,q) in enumerate(edges):
  guards+=1;e=sub(q,p);den=det(v,e);assert den
  t=F(det(sub(p,x),e),den);u=F(det(sub(p,x),v),den)
  assert not(0<t<1 and 0<=u<=1)
  if t==1 and 0<=u<=1:hits.append((i,u))
 if j<len(path)-2:assert len(hits)==1 and 0<hits[0][1]<1;wall_ids.append(hits[0][0])
 else:assert not hits
 target=(F(1),F(2));tt=F(target[0]-x[0],v[0])
 if 0<tt<=1 and tuple(x[k]+tt*v[k] for k in(0,1))==target:assert j==len(path)-2 and tt==1
for j,i in enumerate(wall_ids,1):
 e=sub(edges[i][1],edges[i][0]);v=sub(path[j],path[j-1]);vout=sub(path[j+1],path[j]);ref=(-v[0],v[1]) if not e[0] else(v[0],-v[1]);assert det(ref,vout)==0 and dot(ref,vout)>0
assert len(wall_ids)==8
out={'status':'THREE_EXCEPTIONAL_ROWS_AND_LITERAL_D0_ACTUAL_PATH_PASS','exceptional_rows':rows,'actual_D0_path':path,'polygon':V,'reflections':8,'all_wall_leg_guards':guards,'peer_pins_checked':len(req['source_sha256']),'peer_optical_code_executed':False,'peer_controls_replayed':False,'discovery':False,'finished_utc':datetime.now(timezone.utc).isoformat(),'whole_goal_complete':False}
(R/'h2-A1-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('exceptional_rows','actual_D0_path','polygon')}))
