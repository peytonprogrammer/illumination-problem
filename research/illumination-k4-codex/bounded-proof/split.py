"""Exhaustive legal central-fan partition of capped CNFs; proof checked per leaf."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import json,sys,hashlib,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from encode import fan_table
from verify import verify
from pysat.formula import CNF
from pysat.solvers import Solver


def leaf_job(parent_name,mask,ring):
 parent=HERE/'cases'/parent_name;folder=parent/'split'/f'mask{mask}';folder.mkdir(parents=True,exist_ok=True)
 if (folder/'verification.json').exists():return json.loads((folder/'verification.json').read_text())
 cnf=CNF(from_file=str(parent/'formula.cnf'));units=[[v if mask>>i&1 else -v] for i,v in enumerate(ring)];cnf.extend(units)
 start=time.monotonic()
 with Solver(name='cadical300',bootstrap_with=cnf.clauses,with_proof=True) as s:
  s.conf_budget(100000);status=s.solve_limited();proof=s.get_proof() if status is False else [];stats=s.accum_stats()
 cnf.to_file(str(folder/'formula.cnf'))
 if status is False:(folder/'proof.drat').write_text('\n'.join(proof)+'\n')
 (folder/'tile-variables.json').write_bytes((parent/'tile-variables.json').read_bytes());(folder/'connectivity-cuts.json').write_text('[]\n')
 result=dict(json.loads((parent/'result.json').read_text()),tag=parent_name+f'/mask{mask}',status='UNSAT' if status is False else 'UNKNOWN' if status is None else 'SAT',connectivity_cuts=0,seconds=round(time.monotonic()-start,3),solver_stats=stats)
 (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 if status is False:return verify(folder)
 return dict(tag=result['tag'],status=result['status'])


def main():
 pending=[];parents={}
 for name in ('I2_2_0-pair0','I2_2_1-pair0'):
  parent=HERE/'cases'/name;tiles={tuple(sorted(map(tuple,t))):v for t,v in json.loads((parent/'tile-variables.json').read_text())}
  center=(2,0);tris=sorted(t for t in tiles if center in t);assert len(tris)==8
  relative=tuple(tuple((p[0]-2,p[1]) for p in t) for t in tris)
  masks=[r[0] for r in fan_table(relative) if not r[2]];assert len(masks)==57
  ring=[tiles[t] for t in tris];parents[name]=dict(center=center,masks=masks,ring_variables=ring,
      base_sha256=hashlib.sha256((parent/'formula.cnf').read_bytes()).hexdigest())
  (parent/'split-manifest.json').write_text(json.dumps(parents[name],indent=2)+'\n')
  pending.extend((name,m,ring) for m in masks)
 results=[]
 with ProcessPoolExecutor(max_workers=6) as pool:
  fs={pool.submit(leaf_job,*task):task for task in pending}
  for future in as_completed(fs):
   try:r=future.result()
   except Exception as e:r=dict(tag=fs[future][:2],status='ERROR',error=repr(e))
   results.append(r)
   if len(results)%10==0 or r['status']!='VERIFIED':print('SPLIT',len(results),json.dumps(r),flush=True)
   (HERE/'split-summary.json').write_text(json.dumps(dict(expected=len(pending),finished=len(results),verified=sum(r['status']=='VERIFIED' for r in results),cases=results),indent=2)+'\n')
 for name,manifest in parents.items():
  rows=[r for r in results if isinstance(r['tag'],str) and r['tag'].startswith(name+'/')]
  ok=len(rows)==57 and all(r['status']=='VERIFIED' for r in rows)
  composition=dict(status='COMPOSED_VERIFIED' if ok else 'INCOMPLETE',manifest=manifest,children=rows)
  (HERE/'cases'/name/'composition.json').write_text(json.dumps(composition,indent=2)+'\n')
 print('SPLIT FINISHED',len(results),'verified',sum(r['status']=='VERIFIED' for r in results),flush=True)

if __name__=='__main__':main()
