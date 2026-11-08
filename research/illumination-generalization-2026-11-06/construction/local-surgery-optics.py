#!/usr/bin/env python3
"""A15: exact positive-witness discovery on five fixed surgery candidates only."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from math import gcd
import json,signal,time
R=Path(__file__).resolve().parent
E=json.loads((R/'local-surgery-effort.json').read_text())
D=datetime.fromisoformat(E['aggregate_deadline_utc']).timestamp()
rows=[];out={'effort':'A15','rows':rows,'status':'RUNNING','darkness_claim':False}
def save():
 out['updated_utc']=datetime.now(timezone.utc).isoformat()
 (R/'local-surgery-optics.json').write_text(json.dumps(out,indent=2)+'\n')
def timeout(*_):
 out['status']='ORIGINAL_DEADLINE_STOP';save();raise SystemExit('Original A15 deadline')
if time.time()>=D:timeout()
signal.signal(signal.SIGALRM,timeout);signal.alarm(max(1,int(D-time.time())))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def sub(v,w):return v[0]-w[0],v[1]-w[1]
def add(v,w):return v[0]+w[0],v[1]+w[1]
def scale(t,v):return t*v[0],t*v[1]
def serial(z):return [str(a) for a in z]
def trace(poly,S,T,vel):
 pos=tuple(map(F,S));T=tuple(map(F,T));vel=tuple(vel);path=[serial(pos)];walls=[];states=set()
 for step in range(501):
  if time.time()>=D:timeout()
  state=(pos,vel)
  if state in states:return None
  states.add(state)
  best=None;edge=None;u0=None
  for j,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
   e=sub(b,a);den=cross(vel,e)
   if den==0:continue
   t=F(cross(sub(a,pos),e),den);u=F(cross(sub(a,pos),vel),den)
   if t>0 and 0<=u<=1 and (best is None or t<best):best=t;edge=j;u0=u
  assert best is not None
  delta=sub(T,pos)
  if cross(delta,vel)==0:
   k=0 if vel[0] else 1;arrival=delta[k]/vel[k]
   if 0<arrival<best:
    return {'initial_direction':serial(tuple(vel0)), 'path':path+[serial(T)],'wall_indices':walls,'reflections':len(walls)}
  if u0==0 or u0==1 or step==500:return None
  pos=add(pos,scale(best,vel));path.append(serial(pos));walls.append(edge)
  a,b=poly[edge],poly[(edge+1)%len(poly)];e=sub(b,a);n=(-e[1],e[0]);dot=vel[0]*n[0]+vel[1]*n[1];norm=n[0]*n[0]+n[1]*n[1]
  vel=sub(vel,scale(F(2*dot,norm),n))
 return None
cases=[r for r in json.loads((R/'local-surgery-check.json').read_text())['rows'] if r['eligible'] and not r['covered_by_baseline']]
directions=[]
for m in range(1,33):
 for p in range(-m,m+1):
  for q in range(-m,m+1):
   if max(abs(p),abs(q))==m and gcd(abs(p),abs(q))==1:directions.append((p,q))
save()
for c in cases:
 poly=list(map(tuple,c['canonical_polygon']));S,T=c['marked'];witness=None;tested=0
 for vel0 in directions:
  tested+=1;witness=trace(poly,S,T,vel0)
  if witness:break
 row={'deleted_index':c['deleted_index'],'deleted_vertex':c['deleted_vertex'],'W':c['W'],'k':c['k'],'canonical_representative_factor':c['canonical_representative_factor'],'polygon':poly,'S':S,'T':T,'directions_tested':tested,'status':'ACTUAL_WITNESS_CANDIDATE' if witness else 'BOUNDED_SEARCH_FAILURE_NOT_DARK','witness':witness}
 rows.append(row);save();print(json.dumps({'index':c['deleted_index'],'status':row['status'],'tested':tested,'reflections':None if witness is None else witness['reflections']}),flush=True)
 if witness is None:break
out['status']='ALL_FIVE_HAVE_POSITIVE_WITNESSES' if len(rows)==5 and all(r['witness'] for r in rows) else 'INCOMPLETE_NO_DARKNESS_CLAIM'
out['within_original_deadline']=time.time()<D
save();signal.alarm(0)
