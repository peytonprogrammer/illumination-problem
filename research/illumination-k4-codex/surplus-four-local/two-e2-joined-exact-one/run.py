"""One frozen room, one finite-orbit traversal; no direction grid or room generation."""
from pathlib import Path
from collections import deque
from fractions import Fraction as F
from math import gcd
import importlib.util,json,signal,time,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FRAME=ROOT/'k5-proof-pilot/inputs/origami_frame.py'
TRACE=ROOT.parent/'claude-illumination-check/folded/exact.py'
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def expired(*_):raise TimeoutError('60-second hard process budget')
signal.signal(signal.SIGALRM,expired);signal.alarm(60)
t0=time.monotonic();out={'status':'STARTED','room':'Bouter3_Dhalf3_Rplus_Tempty','state_limit':20000,'seconds_limit':60,'states':0}
try:
 room=json.loads((HERE/'geometry.json').read_text());V=[tuple(p) for p in room['vertices']];S=tuple(room['source']);T=tuple(room['target'])
 o=load('frozen_origami_frame',FRAME);r,u,lab,s0,fr=o.build(V,S,T)
 start=o.canon(r,u,lab,s0);seen={start};Q=deque([(start,((1,0),(0,1)),0)])
 mul=lambda A,B:tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
 direction=None
 while Q:
  (R,U,L),M,depth=Q.popleft();s=R[0]
  while s!=0:
   if L[s]=='block':break
   if L[s]=='T':
    dev=(M[0][0],M[1][0]);direction=(fr[0][0]*dev[0]+fr[1][0]*dev[1],fr[0][1]*dev[0]+fr[1][1]*dev[1]);n=gcd(*direction);direction=tuple(c//n for c in direction)
    out.update(status='ORBIT_LIT_WITNESS_PENDING',direction=direction,shear_depth=depth);break
   s=R[s]
  if direction is not None:break
  Ri,Ui=o.inv(R),o.inv(U)
  for a,b,N in [(R,tuple(o.comp(U,Ri)),((1,-1),(0,1))),(tuple(o.comp(R,Ui)),U,((1,0),(-1,1)))]:
   st=o.canon(a,b,L,0)
   if st not in seen:
    if len(seen)>=20000:out['status']='UNDECIDED_STATE_LIMIT';Q.clear();break
    seen.add(st);Q.append((st,mul(M,N),depth+1))
  if out['status']=='UNDECIDED_STATE_LIMIT':break
 out['states']=len(seen);out['square_count']=len(start[0])
 if direction is None and out['status']=='STARTED':out['status']='COMPLETED_ORBIT_NO_CONNECTION_REQUIRES_INDEPENDENT_DARKNESS_REVIEW'
 if direction is not None:
  trace=load('frozen_exact_single_direction',TRACE)
  dr,P=trace.run(V,S,T,B=20000,dirs=[direction])
  if dr is None:out['status']='ORBIT_LIT_SINGLE_DIRECTION_EXTRACTION_UNDECIDED'
  else:
   out.update(status='LIT_PATH_AWAITING_INDEPENDENT_REPLAY',path=[[str(c) for c in p] for p in P],reflections=len(P)-2)
except TimeoutError:
 out.update(status='UNDECIDED_TIME_LIMIT',states=len(seen) if 'seen' in globals() else 0)
finally:
 signal.alarm(0);out['seconds']=round(time.monotonic()-t0,6)
 out['inputs_sha256']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'geometry.json',FRAME,TRACE]}
 (HERE/'result.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['path','inputs_sha256']}),flush=True)
