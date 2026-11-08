"""Bounded event-certificate construction for the certified historical room."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,math,time,hashlib
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,canon,rank,dot

def controls():
 base=B.parent/'rigidity-review';records=[]
 for roomname,eventsname in [(B.parent/'peer-fast-inputs/cand-2_2-1.json',base/'events.json'),(base/'room24/inputs/room-illumination-search-simple-unrestricted.json',base/'room24/events.json')]:
  model=EventModel(json.loads(roomname.read_text()));supplied=json.loads(eventsname.read_text());expected=[]
  for e in supplied:
   g=list(map(F,e['gradient']))
   if model.W==22:
    # Older orthogonal checker used signed edge displacements, not positive
    # primitive-direction lengths. Pull each row back into this chart.
    for i,d in enumerate(model.dirs):g[2+i]*=d[0] or d[1]
   expected.append(canon(g))
  found={}
  for q in sorted({tuple(e['direction']) for e in supplied}):
   for side in (-1,1):
    e=model.event(q,side)
    if e['status']=='EVENT':found[tuple(e['row'])]=e
  assert set(expected)<=set(found)
  records.append(dict(walls=model.W,expected=len(expected),matched=len(set(expected)&set(found)),rank=rank([*model.closure,*found])-2))
 (B/'controls.json').write_text(json.dumps(dict(status='PASS',cases=records),indent=2)+'\n');print('CONTROLS',records,flush=True)

def construct(radius):
 model=EventModel(json.loads((B/'room.json').read_text()));events={};other=Counter();directions=[];start=time.monotonic()
 for p in range(-radius,radius+1):
  for q in range(-radius,radius+1):
   if p and q and math.gcd(abs(p),abs(q))==1:directions.append((p,q))
 for q in directions:
  for side in (-1,1):
   e=model.event(q,side)
   if e['status']=='EVENT':events.setdefault(tuple(e['row']),e)
   else:other[e['status']]+=1
 rows=list(events);r=rank([*model.closure,*rows])-2;ann=all(dot(g,s)==0 for g in rows for s in model.syms)
 assert ann
 out=dict(status='EVENTS_BUILT',radius=radius,directions=len(directions),sides=2*len(directions),events=len(events),rank_on_closure=r,closure_dimension=model.dim-2,symmetry_dimension=rank(model.syms),target_rank=model.dim-2-rank(model.syms),kernel_dimension=model.dim-2-r,affine_annihilation=ann,other_limits=dict(other),seconds=round(time.monotonic()-start,3),room_sha256=hashlib.sha256((B/'room.json').read_bytes()).hexdigest(),scope='Bounded fixed-room event-certificate construction, not a room search. No rank or positive-span conclusion beyond this finite certificate.')
 (B/f'events-R{radius}.json').write_text(json.dumps(list(events.values()),indent=2)+'\n');(B/f'rigidity-R{radius}.json').write_text(json.dumps(out,indent=2)+'\n');(B/'events.json').write_text(json.dumps(list(events.values()),indent=2)+'\n');(B/'rigidity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
 return model,events,out
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='controls':controls()
 else:construct(int(sys.argv[1]) if len(sys.argv)>1 else 6)
