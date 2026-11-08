"""Build a finite algebraic certificate for the one fixed room; no rays or new rooms."""
import importlib.util
import json
import hashlib
from collections import deque
from pathlib import Path
HERE=Path(__file__).resolve().parent

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path)
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 return mod

if __name__=='__main__':
 audit=module('independent_checker',HERE/'closed-orbit-audit.py')
 geometry=module('own_physical_geometry',HERE/'peer-fast-audit.py')
 room_path=HERE/'peer-fast-inputs/cand-2_2-1.json'
 initial=geometry.direct_orthogonal_unfold(json.loads(room_path.read_text()))
 state=audit.canonical(initial)
 seen={state};queue=deque([state]);processed=0
 while queue:
  current=queue.popleft();processed+=1
  audit.check_horizontal(current)
  for changed in audit.transforms(current):
   key=audit.canonical(changed)
   if key not in seen:
    seen.add(key);queue.append(key)
  if processed%500==0:print('processed',processed,'known',len(seen),'pending',len(queue),flush=True)
  if len(seen)>50000:raise RuntimeError('resource guard: INCONCLUSIVE; no certificate written')
 result=dict(convention='stop_at_actual_corners',input_sha256=hashlib.sha256(room_path.read_bytes()).hexdigest(),
             independent_initial=initial,states=[dict(r=s[0],u=s[1],label=s[2]) for s in sorted(seen)])
 (HERE/'independent-orbit-certificate.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
 print('COMPLETE CLOSED SET',len(seen),flush=True)
