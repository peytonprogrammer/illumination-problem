"""Own-model replays of audited ray cuts, with redundant exact connectivity flow."""
from pathlib import Path
import json,time,hashlib
from ortools.sat.python import cp_model
from search_illumination_three_two_star import make_model
from illumination_geometry import owners_of
from illumination_triple_cell_sets import outside_sets,refine_connected_cells
BASE=Path(__file__).parent;OUT=BASE/'three-triples';PATH=OUT/'peer-2-0-replay.json'
start=time.monotonic();inp=OUT/'peer-2-0-audit.json';audit=json.loads(inp.read_text());assert audit['stats']['exact_paths']==6997 and audit['stats']['peer_geometry']==2299
assert len(audit['cuts'])==5710
model,ts,x,bounded,terms=make_model((2,0));refine_connected_cells((2,0),model,terms)
# Every occupied triangle consumes one unit. The occupied root supplies all
# others through shared edges. This is equivalent to connected occupancy;
# rank-parent connectivity remains in the own builder as an independent check.
root=next(i for i,t in enumerate(ts) if (0,0) in t);assert model is not None
incoming=[[] for _ in ts];outgoing=[[] for _ in ts];bound=terms['max_tiles']
for e,ids in owners_of(ts).items():
 if len(ids)!=2:continue
 for a,b in (ids,ids[::-1]):
  f=model.new_int_var(0,bound,f'check_flow_{a}_{b}');model.add(f<=bound*x[a]);model.add(f<=bound*x[b]);outgoing[a].append(f);incoming[b].append(f)
for i in range(len(ts)):
 if i==root:model.add(sum(outgoing[i])-sum(incoming[i])==sum(x)-1)
 else:model.add(sum(incoming[i])-sum(outgoing[i])==x[i])
geometry_control=model.clone()
source=json.loads((OUT/'peer-2-0-rays.json').read_text())['peer'][0]
selected={tuple(sorted(map(tuple,t))) for t in source['room']}
for i,t in enumerate(ts):geometry_control.add(x[i]==int(t in selected))
for facts in audit['cuts']:model.add_bool_or([x[i].Not() if value else x[i] for i,value in facts])
result=dict(status='RUNNING',guard_count=len(audit['cuts']),source_sha256=hashlib.sha256(inp.read_bytes()).hexdigest(),partition=[])
def save(event):
 result['seconds']=time.monotonic()-start;tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH);print(json.dumps(dict(event=event,seconds=result['seconds'],partition=len(result['partition']),monolithic=result.get('monolithic'))),flush=True)
def solve(m,cap):
 s=cp_model.CpSolver();s.parameters.cp_model_presolve=False;s.parameters.num_search_workers=2;s.parameters.random_seed=733;s.parameters.max_time_in_seconds=cap;st=s.solve(m);return dict(status=s.status_name(st),seconds=s.wall_time)
result['fixed_geometry_flow_control']=solve(geometry_control,30)
assert result['fixed_geometry_flow_control']['status'] in ('OPTIMAL','FEASIBLE')
result['monolithic']=solve(model,180);save('monolithic')
if result['monolithic']['status']=='INFEASIBLE':result.update(status='PASS',placement_excluded=True)
else:
 choices,levels=outside_sets((2,0));assert len(choices)==699;outside=sorted(bounded['allowed']-bounded['mandatory'])
 for n,cells in enumerate(choices,1):
  branch=model.clone()
  for a,b in outside:branch.add(terms['used'][2*a,2*b]==int((a,b) in cells))
  row=solve(branch,3)
  if row['status']=='UNKNOWN':row=solve(branch,30)
  result['partition'].append(dict(cells=cells,**row))
  if n%25==0:save('partition')
 result['placement_excluded']=all(r['status']=='INFEASIBLE' for r in result['partition']);result['status']='PASS' if result['placement_excluded'] else 'OPEN'
save('complete')
