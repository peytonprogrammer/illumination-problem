"""A57 prescribed independent exact first-hit tracing. No author optical imports/discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def contour(c,ws,wt,a,b):
 return [tuple(map(Q,z)) for z in [(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,11),(0,11),(0,8),(-b,8),(-b,6),(0,6),(0,5),(-a,5),(-a,3),(0,3)]]
def trace(V,S,T,v,expected):
 z=S;path=[z];refs=0
 for step in range(expected+2):
  candidates=[]
  for i,(a,b) in enumerate(g.edges(V)):
   edge=g.vec(a,b);den=g.det(v,edge)
   if not den:continue
   t=Q(g.det(g.vec(z,a),edge),den);r=Q(g.det(g.vec(z,a),v),den)
   if t>0 and 0<=r<=1:candidates.append((t,i,r))
  assert candidates
  tm=min(t for t,_,_ in candidates)
  d=g.vec(z,T)
  if g.det(v,d)==0 and g.dot(v,d)>0:
   tt=Q(d[0],v[0]) if v[0] else Q(d[1],v[1])
   if tt<=tm:
    assert tt<tm;path.append(T);assert refs==expected,(refs,expected)
    return path,refs
  hits=[(i,r) for t,i,r in candidates if t==tm];assert len(hits)==1 and 0<hits[0][1]<1,hits
  i,_=hits[0];a,b=g.edges(V)[i]
  z=(z[0]+tm*v[0],z[1]+tm*v[1]);path.append(z);refs+=1
  v=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])
 raise AssertionError('actual target did not arrive at formula count')
def run(c,beta,ds,dt,widths):
 c,beta,ds,dt=map(Q,(c,beta,ds,dt));tau=beta/c
 ns=ds*tau/2;nt=dt*tau/2;assert ns.denominator==nt.denominator==1
 w1,w2,a,b=widths;V=contour(c,ds+w1,dt+w2,a,b);g.simple(V)
 expected=int(ns+nt)+3+int((2+4*beta)//11)
 S=(c+ds,Q(2));T=(c+dt,Q(8));path,refs=trace(V,S,T,(Q(-1),(-1)**int(ns)*tau),expected)
 out=g.path_check(V,path)
 return {'c':c,'beta':beta,'Ds':ds,'Dt':dt,'width_increments':widths,'expected':expected,'path':path,**out}
rows=[]
for c in [Q(1),Q(2,7),Q(1000003),Q(121)]:
 for beta in [7,18,29,40,51,62]:
  rows.append(run(c,beta,0,0,(Q(1,101),Q(100003),Q(2,71),Q(10009))))
for c in [1,2,6,11,22,37,121,1331]:
 p=1
 while c%(11*p)==0:p*=11
 u=c//p;k=next(k for k in range(1,11) if u*k%11==9);beta=2*u*k
 for ds,dt in [(0,p),(p,3*p),(2*p,0),(3*p,4*p)]:
  rows.append(run(c,beta,ds,dt,(Q(2,103),Q(3,107),Q(100019),Q(1,113))))
for c in range(1,10001):
 p=1
 while c%(11*p)==0:p*=11
 u=c//p;k=next(k for k in range(1,11) if u*k%11==9)
 assert (2*u*k)%22==18 and Q(2*u*k,c)==Q(2*k,p)
 for D in [0,p,7*p]:assert (Q(D)*2*k/p/2).denominator==1
req=json.loads((P/'actual-word-cell-review-request.json').read_text());pins=req['source_pins']
for f,h in pins.items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
out={'status':'A57_ALL_INDEPENDENT_ACTUAL_FIRST_HIT_CHECKS_PASS','whole_goal_complete':False,'author_code_executed':False,'author_control_replay_claimed':False,'actual_paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'integer_corollary_controls':10000,'source_pins':pins,'own_validator_sha256':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest(),'rows':rows}
(R/'tooth-free-core-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_pins']})
