from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from encode import solve_case
from verify import verify

def job(c):
 r=solve_case(c,0,c['mark_pairs'][0],solver_name='cadical300');return verify(HERE/'cases'/r['tag'])

if __name__=='__main__':
 cases=[c for c in json.loads((HERE.parent/'branch-support.json').read_text())['cases'] if c['tag'] in ('I2_2_0','I2_2_1')];out=[]
 with ProcessPoolExecutor(max_workers=2) as pool:
  fs=[pool.submit(job,c) for c in cases]
  for f in as_completed(fs):
   try:r=f.result()
   except Exception as e:r=dict(status='ERROR',error=repr(e))
   out.append(r);print('LAST',json.dumps(r),flush=True);(HERE/'last-two-summary.json').write_text(json.dumps(out,indent=2)+'\n')
