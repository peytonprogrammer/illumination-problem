from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import json,sys,traceback,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from encode import solve_case
from verify import verify

def job(case,i,pair):
 tag=f'{case["tag"]}-pair{i}';folder=HERE/'cases'/tag
 if (folder/'result.json').exists():result=json.loads((folder/'result.json').read_text())
 else:result=solve_case(case,i,pair,seconds=120)
 if (folder/'verification.json').exists():return json.loads((folder/'verification.json').read_text())
 return verify(folder)

if __name__=='__main__':
 cases=json.loads((HERE.parent/'branch-support.json').read_text())['cases'];out=[];t0=time.monotonic()
 with ProcessPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(job,c,i,p):f'{c["tag"]}-pair{i}' for c in cases for i,p in enumerate(c['mark_pairs'])}
  for future in as_completed(jobs):
   try:r=future.result()
   except Exception as e:r=dict(tag=jobs[future],status='ERROR',error=repr(e));traceback.print_exc()
   out.append(r);print('FINISHED',json.dumps(r),flush=True)
   summary=dict(status='RUNNING' if len(out)<len(jobs) else 'VERIFIED' if all(r['status']=='VERIFIED' for r in out) else 'INCOMPLETE',expected=len(jobs),finished=len(out),seconds=round(time.monotonic()-t0,2),cases=sorted(out,key=lambda r:r['tag']))
   (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print('SUMMARY',json.dumps({k:v for k,v in summary.items() if k!='cases'}),flush=True)
