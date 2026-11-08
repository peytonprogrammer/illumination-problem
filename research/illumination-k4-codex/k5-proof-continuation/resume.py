"""Resume the open finite support cases with all exact learned path guards."""
from pathlib import Path
from collections import Counter
import importlib.util,json,shutil
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('continuation',ROOT/'run.py');r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
summary=json.loads((ROOT/'summary.json').read_text());snapshot=ROOT/'inputs/round0-summary.json'
if not snapshot.exists():shutil.copy2(ROOT/'summary.json',snapshot)
records=[json.loads((r.PILOT/'orbit-guard.json').read_text())]+json.loads((ROOT/'peer-guards.json').read_text())+[json.loads(l) for l in (ROOT/'learned.jsonl').read_text().splitlines() if l]
cases=json.loads((r.PILOT/'inputs/branch-support.json').read_text())['cases']
lookup={f'{c["tag"]}-pair{i}':(c,i,pair) for c in cases for i,pair in enumerate(c['mark_pairs'])}
for i,old in enumerate(summary['results']):
 if old['status'] not in ('OPEN_ROUND_LIMIT','OPEN_TIME_LIMIT','OPEN_SAT_TIMEOUT'):continue
 tag=old['tag'];folder=ROOT/'cases'/tag;indices=[int(z.name) for z in (folder/'generations').iterdir()];offset=max(indices)+1
 archive=folder/'passes'/str(offset);archive.mkdir(parents=True,exist_ok=False)
 for name in ('formula.cnf','proof.drat','proof-check.log','result.json'):
  if (folder/name).exists():shutil.copy2(folder/name,archive/name)
 case,index,pair=lookup[tag];new=r.run(case,index,pair,records,rounds=20000,budget=180,peer_guards_used=True)
 summary['results'][i]=new;summary['status_counts']=dict(Counter(x['status'] for x in summary['results']));summary['learned_guards']=sum(1 for line in (ROOT/'learned.jsonl').open() if line.strip());summary['peer_guards']=10
 r.write(ROOT/'summary.json',summary)
 # Verify the known dark room is still allowed under all accumulated patterns.
 c=dict(next(c for c in cases if c['tag']=='I2_1_1'));allowed=set(map(tuple,c['allowed']));allowed|={(x+dx,y+dy) for x,y in list(allowed) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))};c['allowed']=sorted(allowed)
 cnf,pool,x,ts=r.p.model.geometry(c,wmax=22,kmax=5);r.p.frozen_guards(c['mark_pairs'][0],x,cnf)
 clauses=r.guard_clauses(records,c['mark_pairs'][0],x);chosen={tuple(sorted(map(tuple,t))) for t in json.loads((r.PILOT/'inputs/cand-2_2-1.json').read_text())['triangles']}
 with r.Solver(name='glucose4',bootstrap_with=cnf.clauses+list(map(list,clauses))) as solver:assert solver.solve(assumptions=[v if t in chosen else -v for t,v in x.items()])
 r.write(ROOT/'controls.json',dict(known_dark22_allowed=True,guard_records=len(records),new_clauses=len(clauses)))
print('COMPLETE',summary['status_counts'],'learned',summary['learned_guards'],flush=True)
