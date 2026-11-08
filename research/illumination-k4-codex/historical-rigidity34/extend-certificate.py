"""Counterexample-guided finite certificate extension, hard direction radius24."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,math,subprocess,time
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,dot

def save(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def invoke(name,args,log):
 with (B/log).open('w') as f:r=subprocess.run([sys.executable,'-B',str(B/name),*args],stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,(name,'see '+log)
if __name__=='__main__':
 model=EventModel(json.loads((B/'room.json').read_text()));active=json.loads((B/'events-R12.json').read_text());seen={tuple(e['row']) for e in active};delta=list(map(F,json.loads((B/'cone-witness.json').read_text())['delta']));history=[];tested=0;start=time.monotonic();complete=False
 for radius in range(13,25):
  directions=[(p,q) for p in range(-radius,radius+1) for q in range(-radius,radius+1) if p and q and max(abs(p),abs(q))==radius and math.gcd(abs(p),abs(q))==1]
  for direction in directions:
   for side in (-1,1):
    tested+=1;e=model.event(direction,side)
    if e['status']!='EVENT' or tuple(e['row']) in seen or dot(map(F,e['row']),delta)>=0:continue
    active.append(e);seen.add(tuple(e['row']));save(B/'events.json',active)
    invoke('positive-span.py',[],'positive-span.log');result=json.loads((B/'positive-span.json').read_text())
    row=dict(added_direction=direction,side=side,events=len(active),radius=radius,seconds=round(time.monotonic()-start,2),positive_span=result['status']);history.append(row);print(json.dumps(row),flush=True)
    if result['status']=='PASS':complete=True;break
    invoke('cone-witness.py',['events.json','adaptive-cone.json'],'adaptive-cone.log');delta=list(map(F,json.loads((B/'adaptive-cone.json').read_text())['delta']))
   if complete:break
  if complete:break
  print(json.dumps(dict(completed_radius=radius,tested_sides=tested,events=len(active),seconds=round(time.monotonic()-start,2))),flush=True)
 save(B/'events-targeted.json',active);save(B/'events.json',active);save(B/'adaptive-cone-history.json',history)
 out=dict(status='CERTIFICATE_BUILT' if complete else 'INCONCLUSIVE_RADIUS24',events=len(active),base_events=84,additional_events=len(active)-84,additional_sides_tested=tested,maximum_radius=radius,seconds=round(time.monotonic()-start,2),positive_span=complete,scope='Adaptive finite extension on one certified fixed room. Each retained event eliminates an exact surviving cone vector. No room discovery; radius never exceeds24.')
 save(B/'rigidity-extended.json',out);print(json.dumps(out,indent=2),flush=True)
