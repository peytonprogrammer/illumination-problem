"""A60/A61 independent literal full-contour controls; no author optical imports."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
paths={3:[(1,2),(Q(1,4),0),(0,Q(2,3)),(1,Q(10,3)),(0,6),(Q(9,8),9),(Q(15,8),7),(2,Q(22,3)),(Q(11,8),9),(1,8)],5:[(1,2),(Q(3,7),0),(0,Q(3,2)),(1,5),(0,Q(17,2)),(1,12)]}
rows=[]
for h in [3,5]:
 G=2*h+4;Y=h+4;t=2*h+2
 for c,ws,wt,a,b in [(Q(1,13),Q(1,197),Q(100109),Q(1,199),Q(100129)),(Q(1),Q(100151),Q(1,211),Q(100153),Q(1,223)),(Q(100169),Q(1,227),Q(1,229),Q(100183),Q(100189))]:
  if h==3:wt=c
  V=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,t-1),(c+wt,t-1),(c+wt,t+1),(c,t+1),(c,G),(0,G),(0,Y+2),(-b,Y+2),(-b,Y),(0,Y),(0,h+2),(-a,h+2),(-a,h),(0,h)];V=[tuple(map(Q,p)) for p in V];g.simple(V)
  path=[(c*x,y) for x,y in paths[h]];assert path[0]==(c,2) and path[-1]==(c,t)
  assert not any(g.on(A,B,path[-1]) for A,B in zip(path[:-2],path[1:-1]));out=g.path_check(V,path);assert out['reflections']==(8 if h==3 else 4)
  rows.append({'h':h,'c':c,'source_width':ws,'target_width':wt,'left_widths':[a,b],**out})
pins={}
for filename in ['critical-quarter-protected-review-request.json','critical-five-source-review-request.json']:
 for f,h in json.loads((P/filename).read_text())['source_sha256'].items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h;pins['../construction/'+f]=h
out={'status':'A60_A61_ORIGINAL_SEAMS_INDEPENDENT_ALL_WALL_PASS','whole_goal_complete':False,'author_code_executed':False,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'rows':rows,'source_sha256':pins}
(R/'critical-seams-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
