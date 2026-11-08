"""Fresh drop-pass-2 positive control using the previously checked path pool."""
from pathlib import Path
import json,hashlib,time
from ortools.sat.python import cp_model
from search_illumination_three_two_star import make_model,add_guard,room_from
from illumination_triple_cell_sets import refine_connected_cells
from audit_illumination_three_two_star import touched_tiles
from illumination_sector_paths import verify
BASE=Path(__file__).parent;OUT=BASE/'three-triples';p=OUT/'peer-2-0-rays.json';d=json.loads(p.read_text());audit=json.loads((OUT/'peer-2-0-audit.json').read_text());assert audit['source_sha256']==hashlib.sha256(p.read_bytes()).hexdigest() and audit['stats']['exact_paths']==6997
start=time.monotonic();model,ts,x,bounded,terms=make_model((2,0));refine_connected_cells((2,0),model,terms);keys=set();full={tuple(map(tuple,f)) for f in audit['cuts']};library={}
def collect(room,w,keep):
 selected={tuple(sorted(map(tuple,t))) for t in room['triangles']};f=tuple(sorted((i,int(ts[i] in selected)) for i in touched_tiles(ts,w)));assert f in full
 library.setdefault(f,w)
 if keep:keys.add(f)
for r in d['base']:collect(r['room'],r['witness'],True)
for n,r in enumerate(d['peer']):
 room=dict(triangles=r['room'],marked=[[0,0],[4,0]],require_simple=True);w=r['witness'];collect(room,w,n<1259)
 mr=dict(room,triangles=[[[a,-b] for a,b in t] for t in room['triangles']]);mw=dict(w,direction=[w['direction'][0],-w['direction'][1]],path=[[[a,ad],[-b,bd]] for (a,ad),(b,bd) in w['path']]);collect(mr,mw,n<1259)
assert set(library)==full
for f in keys:add_guard(model,x,f)
for a,b in bounded['allowed']-bounded['mandatory']:model.add(terms['used'][2*a,2*b]==int((a,b)==(1,-1)))
s=cp_model.CpSolver();s.parameters.cp_model_presolve=False;s.parameters.num_search_workers=2;s.parameters.max_time_in_seconds=60;s.parameters.random_seed=733
st=s.solve(model);assert st in (cp_model.FEASIBLE,cp_model.OPTIMAL)
room=room_from((2,0),ts,x,s);bits={i for i in range(len(ts)) if s.value(x[i])};hit=next(f for f in full-keys if all(int(i in bits)==v for i,v in f));w=library[hit];verify(room,w)
r=dict(status='PASS',retained_guards=len(keys),dropped_guards=len(full-keys),solver_status=s.status_name(st),room=room,dropped_witness=w,seconds=time.monotonic()-start)
(OUT/'peer-2-0-control.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('room','dropped_witness')}),flush=True)
