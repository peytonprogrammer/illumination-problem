from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import json,shutil,sys,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from encode import solve_case
from verify import verify

def job(c,i,p):
 r=solve_case(c,i,p,solver_name='cadical300')
 return verify(HERE/'cases'/r['tag'])

if __name__=='__main__':
 cases=json.loads((HERE.parent/'branch-support.json').read_text())['cases'];tasks=[];old=HERE/'inconclusive-v5';old.mkdir(exist_ok=True)
 for c in cases:
  for i,p in enumerate(c['mark_pairs']):
   tag=f'{c["tag"]}-pair{i}';folder=HERE/'cases'/tag
   if (folder/'result.json').exists() and json.loads((folder/'result.json').read_text())['status']=='UNKNOWN':
    shutil.move(str(folder),str(old/tag));tasks.append((c,i,p))
 out=[]
 with ProcessPoolExecutor(max_workers=3) as pool:
  futures=[pool.submit(job,*t) for t in tasks]
  for f in as_completed(futures):
   try:r=f.result()
   except Exception as e:r=dict(status='ERROR',error=repr(e))
   out.append(r);(HERE/'fallback-summary.json').write_text(json.dumps(dict(expected=len(tasks),finished=len(out),cases=out),indent=2)+'\n');print('FALLBACK',json.dumps(r),flush=True)
