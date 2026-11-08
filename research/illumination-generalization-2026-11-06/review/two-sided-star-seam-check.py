"""Prescribed exhaustive actual-A controls for R35's whole alternating family."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import importlib.util,json
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('star',R/'two-sided-star-check.py');star=importlib.util.module_from_spec(sp);sp.loader.exec_module(star);g=star.g
sp=importlib.util.spec_from_file_location('twist',R/'mouth-endpoint-twist-independent-check.py');tw=importlib.util.module_from_spec(sp);sp.loader.exec_module(tw)
def clean(path):return [p for i,p in enumerate(path) if i==0 or p!=path[i-1]]
def construct(c,left,right,S,T):
 star.deadline()
 if 0<S[0]<c or 0<T[0]<c or S[0]!=T[0]:return[S,T],'direct_core'
 if S[1]>T[1]:p,k=construct(c,left,right,T,S);return list(reversed(p)),k
 mu=(S[1]+T[1])/2;h=(T[1]-S[1])/2;side='right' if S[0]==c else'left';opp=left if side=='right' else right
 contains=[b for b in opp if b[0]<=mu<=b[1]]
 if not contains:return[S,(Q(0) if side=='right' else c,mu),T],'smooth_mirror'
 lo,hi,w=contains[0]
 if lo<mu<hi:
  assert mu==(lo+hi)/2
  half,_=star.transit(c,Q(2),Q(2),h+2,Q(0),w,side,S[1]-1)
  p=half+[(x,2*mu-y) for x,y in reversed(half[:-1])];return clean(p),'actual_midpoint_return'
 assert h%2==1 and c%2==0
 t=Q(0)
 for _ in range(10000):
  nf=int((t+Q(1,2))//1);nxt=(h+nf)/(c+1)
  if nxt==t:break
  t=nxt
 else:raise AssertionError('prescribed finite matching cap')
 m=t-nf;assert m!=0 and t.denominator!=1
 protected_sign=-1 if mu==lo else 1;sf=m*protected_sign>0
 ps,rs=tw.prefix(c,Q(1),Q(0),t,nf if sf else 0,sf)
 pt,rt=tw.prefix(c,Q(1),Q(0),t,0 if sf else nf,not sf)
 p=[(x,S[1]-1+y) for x,y in ps]+[(Q(0),mu+protected_sign*abs(m))]+[(x,T[1]+1-y) for x,y in reversed(pt)]
 if side=='left':p=[(c-x,y) for x,y in p]
 return clean(p),'mouth_corner_twist'
rows=[]
for c in map(Q,(2,4,6)):
 left=[(Q(7),Q(9),Q(1)),(Q(15),Q(17),Q(1))];right=[(Q(1),Q(3),Q(1)),(Q(11),Q(13),Q(1))]
 V=star.polygon(c,left,right,Q(0),Q(18));assert len(V)==20
 A=[(Q(x),Q(y)) for x in range(0,int(c)+1,2) for y in range(0,19,2) if g.location(V,(x,y))==1]
 paths=[]
 for i,S in enumerate(A):
  for T in A[i+1:]:
   path,kind=construct(c,left,right,S,T);assert path[0]==S and path[-1]==T
   # Keep the actual first target if an image chart reaches it early.
   for j,(a,b) in enumerate(zip(path,path[1:])):
    if g.on(a,b,T):path=path[:j+1]+[T];break
   res=g.path_check(V,path);paths.append({'source':S,'target':T,'kind':kind,**res})
 rows.append({'spine_width':c,'walls':len(V),'actual_A_count':len(A),'all_unordered_pairs':len(paths),'paths':paths})
out={'status':'ALL_ACTUAL_A_PAIRS_IN_THREE_PRESCRIBED_ALTERNATING_W20_ROOMS_PASS','rows':rows,'actual_pairs':sum(r['all_unordered_pairs'] for r in rows),'reflections':sum(p['reflections'] for r in rows for p in r['paths']),'wall_leg_guards':sum(p['wall_leg_guards'] for r in rows for p in r['paths']),'whole_goal_complete':False,'discovery':False,'limits':'Exact prescribed controls, not a room census or universal W21 proof; whole-family hand statement awaits A37D0 supplement.'}
(R/'two-sided-star-seam-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
