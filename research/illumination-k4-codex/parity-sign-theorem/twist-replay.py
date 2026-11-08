"""Replay52theory-prescribed paths; no direction/word search or fitting."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,hashlib,time
if not __debug__:raise RuntimeError('Do not use -O')
B=Path(__file__).resolve().parent
C=json.loads((B/'twist-action.json').read_text());D=json.loads((B/'coupling.json').read_text())
spec=importlib.util.spec_from_file_location('old_event_model',B/'inputs/event_model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
model=m.EventModel(D['room']);W=model.W;dim=W+4
K=[m.add(m.scale(n[0],p[0]),m.scale(n[1],p[1])) for n,p in zip(D['offset_normals'],model.vforms)]+list(model.sform)+list(model.tform)
selection={}
for twist in ('horizontal','vertical'):
    ordered=list(dict.fromkeys(p['saved_index'] for p in C['orbit_stress_certificate'] if p['twist']==twist))
    selection[twist]=ordered
records=[]
receipt=B/'twist-replay.json'
if receipt.exists():
    prior=json.loads(receipt.read_text())
    assert all(hashlib.sha256((B/name).read_bytes()).hexdigest()==digest for name,digest in prior['inputs_sha256'].items())
    records=prior['cases']
    print('Reusing hash-bound completed cases:',len(records),flush=True)
completed={(r['saved_index'],r['twist'],r['power']) for r in records}
for p in C['orbit_stress_certificate']:
    if (p['saved_index'],p['twist'],p['power']) in completed:continue
    e=D['events'][p['saved_index']];x,y=e['direction'];n=p['power'];a=C['summary'][p['twist']+'_shear']
    direction=(x+n*a*y,y) if p['twist']=='horizontal' else (x,y+n*a*x)
    # Full segment has displacement 2w. Mirror lines in its development have
    # integer x/y or even x+y/x-y. Counting all these transverse crossings
    # bounds the wall contacts before that prescribed target, not a scan.
    cap=4*(abs(direction[0])+abs(direction[1]))+12
    started=time.monotonic();event=model.event(direction,e['side'],maxhits=cap)
    assert event['status']=='EVENT',(p['saved_index'],p['twist'],n,event)
    assert tuple(event['corner'])==tuple(e['corner'])
    assert tuple(map(F,event['unfolded_target_minus_s']))==tuple(2*z for z in direction)
    expected=list(map(F,p['row']))
    pullback=[sum(expected[j]*K[j][k] for j in range(dim)) for k in range(model.dim)]
    assert model.project(pullback)==model.project(tuple(map(F,event['gradient']))),(p['saved_index'],p['twist'],n,'gradient mismatch')
    record={'saved_index':p['saved_index'],'twist':p['twist'],'power':n,'direction':direction,'side':e['side'],'corner':event['corner'],'word':event['word'],'word_length':len(event['word']),'corner_prefix_hits':event['corner_prefix_hits'],'proven_contact_bound':cap,'elapsed_seconds':time.monotonic()-started}
    records.append(record)
    print(json.dumps({k:v for k,v in record.items() if k!='word'}),flush=True)
assert len(records)==52
out={'status':'EXACT_PRESCRIBED_ORBIT_REPLAY_PASS','cases':records,'scope':'All52fixed theory-predicted affine images, independent old-chart optical/gradient replay, no discovery search.',
 'inputs_sha256':{name:hashlib.sha256((B/name).read_bytes()).hexdigest() for name in ('twist-action.json','coupling.json','inputs/event_model.py','inputs/inputs/dual.py')}}
(B/'twist-replay.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
