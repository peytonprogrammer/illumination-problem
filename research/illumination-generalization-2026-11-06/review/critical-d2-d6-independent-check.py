"""Independent actual-wall checks for A62/A63; no author optical code imports."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def poly(c,d,ws,wt,a,b):
 G=d+10;return [tuple(map(Q,z)) for z in [(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,7),(c+wt,7),(c+wt,9),(c,9),(c,G),(0,G),(0,d+7),(-b,d+7),(-b,d+5),(0,d+5),(0,5),(-a,5),(-a,3),(0,3)]]
def d6(c,d):return [(c,Q(2)),(0,Q(d+9,2)),(c,Q(d+7)),(c*Q(d-1,d+5),Q(d+10)),(0,Q(d+21,2)),(c,Q(8))]
rows=[]
for q in [Q(1,3),Q(1)]:
 for c,ws,a,b in [(Q(1,17),Q(100207),Q(1,251),Q(100213)),(Q(7,3),Q(1,257),Q(100237),Q(1,263)),(Q(100267),Q(1,269),Q(1,271),Q(1,277))]:
  V=poly(c,2,ws,q*c,a,b);g.simple(V)
  if q==Q(1,3):path=[(c,2),(0,Q(28,5)),(c,Q(46,5)),(2*c/9,12),(0,Q(56,5)),(7*c/6,7),(4*c/3,Q(38,5)),(c/9,12),(0,Q(58,5)),(c,8)]
  else:path=[(c,2),(c/4,0),(0,Q(2,3)),(c,Q(10,3)),(0,6),(9*c/8,9),(15*c/8,7),(2*c,Q(22,3)),(11*c/8,9),(c,8)]
  assert not any(g.on(A,B,path[-1]) for A,B in zip(path[:-2],path[1:-1]));z=g.path_check(V,path);assert z['reflections']==8;rows.append({'family':'A62','c':c,'target_ratio':q,**z})
for d in [3,6,12,1000]:
 for c in [Q(2,7),Q(100279)]:
  V=poly(c,d,Q(1,281),Q(1,283),Q(100291),Q(1,293));g.simple(V);path=d6(c,d)
  assert not any(g.on(A,B,path[-1]) for A,B in zip(path[:-2],path[1:-1]));z=g.path_check(V,path);assert z['reflections']==4;rows.append({'family':'A63','d':d,'c':c,**z})
invalid=poly(Q(1),7,Q(1),Q(1),Q(1),Q(1));bad=d6(Q(1),7);assert bad[-2] in invalid
try:g.path_check(invalid,bad)
except AssertionError:pass
else:raise AssertionError('d7 actual corner must be rejected')
pins={}
for f in ['critical-d2-target-review-request.json','critical-d6-core-review-request.json']:
 for rel,h in json.loads((P/f).read_text())['source_sha256'].items():assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==h;pins['../construction/'+rel]=h
out={'status':'A62_A63_ORIGINAL_CONTOUR_INDEPENDENT_CHECKS_PASS','whole_goal_complete':False,'author_code_executed':False,'actual_paths':len(rows),'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'excluded_d7_corner_rejected':True,'rows':rows,'source_sha256':pins}
(R/'critical-d2-d6-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print({k:v for k,v in out.items() if k not in ['rows','source_sha256']})
