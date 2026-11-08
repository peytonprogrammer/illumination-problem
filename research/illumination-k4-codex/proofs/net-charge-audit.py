"""Adversarial local algebra and saved-room validation; no ray/room search."""
from pathlib import Path
from collections import defaultdict,Counter
from fractions import Fraction as F
import sys,json,math
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent.parent))
from illumination_geometry import patch,check,owners_of,local_sectors,label
star=sorted((t for t in patch(-1,1,-1,1) if (0,0) in t),key=lambda t:math.atan2(sum(p[1] for p in t),sum(p[0] for p in t)))
other=sorted({p for t in star for p in t if p!=(0,0)});tests=0;zeros=Counter();masks=0
for mask in range(256):
 chosen=[t for i,t in enumerate(star) if mask>>i&1];own=owners_of(chosen);opens={e for e,ids in own.items() if len(ids)==2}
 sectors,full=local_sectors(chosen,(0,0),opens)
 if chosen and not full and len(sectors)!=1:continue
 masks+=1;m=len(chosen);kind='empty' if not m else 'full' if full else 'smooth' if sectors==[4] else 'corner'
 cost=0 if not m else 6 if full else 3 if kind=='smooth' else m
 for flags in range(1<<len(other)):
  exceptions={p for j,p in enumerate(other) if flags>>j&1}
  w4=sum(2*(next(p for p in t if label(p)=='C') in exceptions)+(next(p for p in t if label(p)=='B') in exceptions) for t in chosen)
  net4=4*cost-w4
  assert net4>=0
  if kind=='corner':assert net4>=m
  if net4==0:zeros[kind]+=1
  tests+=1

def room_receipt(raw,name):
 ts=raw.get('triangles',raw.get('room'));room=dict(triangles=ts,marked=raw.get('marked',[[0,0],raw.get('_q')]),require_simple=True)
 geom=check(room,strict=False);ts=[tuple(sorted(map(tuple,t))) for t in ts];own=owners_of(ts);opens={e for e,ids in own.items() if len(ids)==2}
 verts={p for t in ts for p in t};full=set();smooth=set();corners=set()
 for p in verts:
  sectors,f=local_sectors(ts,p,opens)
  assert f or len(sectors)==1
  (full if f else smooth if sectors==[4] else corners).add(p)
 exc={p for p in full|smooth if label(p)!='A'}
 E=2*len(exc&full)+len(exc&smooth);cells=defaultdict(list)
 for t in ts:cells[next(p for p in t if label(p)=='A')].append(t)
 net={};costsum=0;weights=F(0)
 for a,tri in cells.items():
  cost=6 if a in full else 3 if a in smooth else len(tri)
  weight=sum(F(1,2)*(next(p for p in t if label(p)=='C') in exc)+F(1,4)*(next(p for p in t if label(p)=='B') in exc) for t in tri)
  net[a]=cost-weight;costsum+=cost;weights+=weight
 assert weights==E and 2+sum(net.values())==geom['walls'] and min(net.values())>=0
 return dict(input=name,walls=geom['walls'],E=E,sum_net=str(sum(net.values())),minimum_net=str(min(net.values())),marked_net={str(p):str(net[tuple(p)]) for p in room['marked']})
base=HERE.parent/'persisted-replay/inputs';rooms=[]
p=HERE.parent/'peer-fast-inputs/cand-2_2-1.json';rooms.append(room_receipt(json.loads(p.read_text()),str(p)))
for p in sorted(base.glob('*learned*.jsonl')):
 line=next((l for l in p.read_text().splitlines() if l.strip()),None)
 if line:
  r=json.loads(line);r['_q']=list(map(int,p.stem.split('-L')[1].split(',')));rooms.append(room_receipt(r,str(p)+':1'))
out=dict(status='PASS',legal_A_fans=masks,flag_assignments_per_fan=256,local_inequalities=tests,zero_net_cases=dict(zeros),saved_rooms=rooms,
 scope='Exhaustive local flag super-relaxation, not planar-room enumeration; seven saved physical controls; no optics searches.')
(HERE/'net-charge-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
