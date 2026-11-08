"""Prescribed local fan degree/charge and forest arithmetic; no rooms."""
from pathlib import Path
import json
b=Path(__file__).resolve().parent
local=[]
for m in range(1,8):
 for q in range(3):
  z=m-2+q
  if z<0 or z%2:continue
  outgoing=z//2;incoming_max=2-q;degree_max=outgoing+incoming_max
  charge=3 if m==4 else m
  assert charge>=degree_max
  local.append({'m':m,'AB_radial_ends':q,'outgoing':outgoing,'incoming_max':incoming_max,'degree_max':degree_max,'charge':charge})
assert len(local)==10
counts=[]
for I in range(1,65):
 bmin=3*I+1;Qmin=2*bmin-2*I-2;Wmin=2+6*I+Qmin
 assert Qmin==4*I and Wmin==10*I+2
 counts.append({'I':I,'partial_neighbors_min':bmin,'Q_min':Qmin,'W_min':Wmin})
assert [x['W_min'] for x in counts[:4]]==[12,22,32,42]
out={'status':'PRESCRIBED_RAW_FAN_BOUND_ALGEBRA_PASS','local_types':local,'arithmetic_controls':counts,
'formula':'W >= 10 I + 2','scope':'Raw strictly simple canonical rooms only. Uses fan-tree theorem and raw wall identity. Ten prescribed partial-fan degree types and64integer substitutions; no geometry, rays, directions, event words, room or orbit enumeration.',
'universal_pocket_event':'OPEN'}
(b/'pocket-full-fan-bound.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'local_types':len(local),'arithmetic_controls':len(counts),'first_bounds':counts[:4]},indent=2))
