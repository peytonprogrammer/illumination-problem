"""Build a finite closed algebraic orbit for the one fixed published room."""
from pathlib import Path
from collections import deque
import importlib.util,json,hashlib,time
B=Path(__file__).resolve().parent;C=B.parent

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
if __name__=='__main__':
 audit=load('codex_orbit_audit',C/'closed-orbit-audit.py');geom=load('codex_physical_unfold',C/'peer-fast-audit.py')
 room=json.loads((B/'room.json').read_text());initial=geom.direct_orthogonal_unfold(room);state=audit.canonical(initial)
 seen={state};queue=deque([state]);processed=0;start=time.monotonic();cap_seconds=55
 while queue:
  s=queue.popleft();processed+=1;audit.check_horizontal(s)
  for t in audit.transforms(s):
   key=audit.canonical(t)
   if key not in seen:seen.add(key);queue.append(key)
  if processed%250==0:print(json.dumps(dict(processed=processed,known=len(seen),pending=len(queue),seconds=round(time.monotonic()-start,2))),flush=True)
  if len(seen)>50000 or time.monotonic()-start>cap_seconds:
   (B/'orbit-build.json').write_text(json.dumps(dict(status='INCONCLUSIVE_RESOURCE_CAP',processed=processed,known=len(seen),pending=len(queue),seconds=time.monotonic()-start),indent=2)+'\n');print('INCONCLUSIVE_RESOURCE_CAP',flush=True);break
 else:
  result=dict(convention='stop_at_actual_corners',input_sha256=hashlib.sha256((B/'room.json').read_bytes()).hexdigest(),independent_initial=initial,states=[dict(r=s[0],u=s[1],label=s[2]) for s in sorted(seen)])
  (B/'orbit-certificate.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
  (B/'orbit-build.json').write_text(json.dumps(dict(status='COMPLETE',states=len(seen),seconds=time.monotonic()-start),indent=2)+'\n');print('COMPLETE',len(seen),flush=True)
