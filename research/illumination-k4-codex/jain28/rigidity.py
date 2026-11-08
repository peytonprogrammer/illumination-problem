"""Bounded certificate construction on the one published room, first target."""
from pathlib import Path
from collections import Counter
import importlib.util,json,math,time,sys
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('boundary_events',B/'boundary-check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
model=mod.BoundaryEventModel(json.loads((B/'room.json').read_text()));radius=int(sys.argv[1]) if len(sys.argv)>1 else 6
rows={};other=Counter();start=time.monotonic();directions=0
for p in range(-radius,radius+1):
 for q in range(-radius,radius+1):
  if not(p and q) or math.gcd(abs(p),abs(q))!=1:continue
  directions+=1
  for side in (-1,1):
   e=model.event((p,q),side)
   if e['status']=='EVENT':rows.setdefault(tuple(e['row']),e)
   else:other[e['status']]+=1
boundary,wall,normal=model.boundary_row();allrows=[*rows,boundary];r=mod.rank([*model.closure,*allrows])-2
result=dict(status='FINITE_EVENT_ROWS_BUILT',radius=radius,events=len(rows),directions=directions,rank_with_boundary=r,closure_dimension=model.dim-2,symmetry_dimension=mod.rank(model.syms),target_rank=model.dim-2-mod.rank(model.syms),boundary_wall=wall,boundary_normal=normal,boundary_row=list(map(str,boundary)),other=dict(other),seconds=time.monotonic()-start,scope='Candidate fixed-room certificate only. Optical replay and exact positive dependence are required before any rigidity conclusion.')
(B/'events.json').write_text(json.dumps(list(rows.values()),indent=2)+'\n');(B/'rigidity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
