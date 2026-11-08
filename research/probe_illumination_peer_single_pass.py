"""Test a universal single-gate cover using only already saved exact paths."""
from pathlib import Path
from collections import Counter
import json,time
from ortools.sat.python import cp_model
from analyze_illumination_exception_itineraries import independent_events
from audit_illumination_three_two_star import touched_tiles
from illumination_sector_paths import verify
from search_illumination_three_two_star import make_model,add_guard,room_from
from illumination_triple_cell_sets import refine_connected_cells
BASE=Path(__file__).parent;OUT=BASE/'three-triples'
d=json.loads((OUT/'peer-2-0-rays.json').read_text());start=time.monotonic()
m,ts,x,b,t=make_model((2,0));refine_connected_cells((2,0),m,t);keys=set();counts=Counter();multiple=[]
def add(room,w):
 if len(independent_events(w))!=1:multiple.append((room,w));counts['multiple']+=1;return
 counts['single']+=1
 required=touched_tiles(ts,w);selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
 facts=tuple(sorted((i,int(ts[i] in selected)) for i in required))
 if facts not in keys:keys.add(facts);add_guard(m,x,facts)
for r in d['base']:add(r['room'],r['witness'])
for r in d['peer']:
 room=dict(triangles=r['room'],marked=[[0,0],[4,0]],require_simple=True);w=r['witness'];add(room,w)
 mr=dict(room,triangles=[[[a,-b] for a,b in tri] for tri in room['triangles']]);mw=dict(w,direction=[w['direction'][0],-w['direction'][1]],path=[[[a,ad],[-b,bd]] for (a,ad),(b,bd) in w['path']]);add(mr,mw)
print(json.dumps(dict(event='compiled',paths=dict(counts),guards=len(keys),seconds=time.monotonic()-start)),flush=True)
rows=[]
for cells in [None,[(1,-1)],[(1,1)]]:
 branch=m.clone()
 if cells is not None:
  for a,c in sorted(b['allowed']-b['mandatory']):branch.add(t['used'][2*a,2*c]==int((a,c) in cells))
 s=cp_model.CpSolver();s.parameters.cp_model_presolve=False;s.parameters.num_search_workers=2;s.parameters.max_time_in_seconds=60;s.parameters.random_seed=733
 status=s.solve(branch);row=dict(cells=cells,status=s.status_name(status),seconds=s.wall_time)
 if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
  room=room_from((2,0),ts,x,s);row['room']=room;bits={i for i in range(len(ts)) if s.value(x[i])}
  for source,w in multiple:
   selected={tuple(sorted(map(tuple,t))) for t in source['triangles']};f=tuple((i,int(ts[i] in selected)) for i in touched_tiles(ts,w))
   if all(int(i in bits)==v for i,v in f):verify(room,w);row['verified_multi_pass_witness']=w;break
 rows.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ('room','verified_multi_pass_witness')}),flush=True)
(OUT/'peer-2-0-single-pass.json').write_text(json.dumps(dict(status='CHECKED',paths=dict(counts),guards=len(keys),cases=rows,seconds=time.monotonic()-start,scope='Only saved single-event rays; feasibility does not prove single-event illumination impossible.'),indent=2)+'\n')
