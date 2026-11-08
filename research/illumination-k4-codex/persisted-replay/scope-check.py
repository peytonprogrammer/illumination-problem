"""Arithmetic, placement, finished-run and rejection-control checks. No searches for paths/rooms."""
import importlib.util, json, hashlib
from pathlib import Path
from fractions import Fraction as F
from collections import deque
from itertools import combinations
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_replay',HERE/'audit.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

def neighbor(t,e):
 v=next(p for p in t if p not in e);a,b=e;d=audit.sub(b,a);w=audit.sub(v,a);n=audit.dot(d,d);dot=audit.dot(w,d)
 p=tuple(F(2*dot*d[k],n)-w[k]+a[k] for k in (0,1));assert all(c.denominator==1 for c in p)
 return tuple(sorted((*e,tuple(map(int,p)))))

# Unbounded tiling dual BFS, not room enumeration: minimum connector distances only.
star=audit.incident((F(0),F(0)));dist={t:0 for t in star};dq=deque(star)
while dq:
 t=dq.popleft()
 if dist[t]==23:continue
 for e in combinations(t,2):
  nxt=neighbor(t,e)
  # Check the centroid displacement used in the finite-window argument.
  c=lambda tri:tuple(F(sum(v[k] for v in tri),3) for k in (0,1))
  assert max(map(abs,audit.sub(c(nxt),c(t))))<=F(2,3)
  if nxt not in dist:dist[nxt]=dist[t]+1;dq.append(nxt)
placements=sorted({p for t in dist for p in t if p!=(0,0) and p[0]%2==p[1]%2==0 and 0<=p[1]<=p[0]})
logs=[]
for q in placements:
 if q==(2,0):continue
 tag=f'L{q[0]},{q[1]}';p=HERE/'inputs'/f'claude-k4-w21-stats-{tag}.json';d=json.loads(p.read_text())
 assert all(d[k]==v for k,v in dict(K=4,WMAX=21,NMAX=38,IMAX=3).items())
 lines=(HERE/'inputs'/f'log-k4w21-{tag}.txt').read_text().splitlines()
 assert lines[-1]=='exit 0' and json.loads(lines[-2])==d['stats']
 assert d['stats']['rooms']==d['stats']['candidates']==d['stats']['hit_window']==0
 logs.append(dict(q=q,nodes=d['stats']['nodes'],learned=d['stats']['learned']))
# Adjacent marks close because the two stars alone contain the direct open segment.
q=(2,0);stars=star|audit.incident(tuple(map(F,q)))
assert audit.segment((F(0),F(0)),tuple(map(F,q)))<=stars

# Inventory arithmetic at W<=21, k<=4, using only Q>=max(0,4-s_N), 3s_A<=Q.
rows=[]
for k in range(5):
 for I in range(2,12):
  for J in range(k+1):
   sn=k-J
   for W in range(3,22):
    Q=W-2-6*I+2*J+sn
    if Q<max(0,4-sn):continue
    for sa in range(Q//3+1):
     N=8*I+Q+sa
     if N>=W+6: rows.append((k,I,J,sn,W,Q,sa,N))
assert max(r[1] for r in rows)==3 and max(r[-1] for r in rows)==36
# Each full A cell is [-1,1]^2 about its A point. Missing adjacent cell makes
# the intervening C midpoint a smooth half-plane, independently by incidence.
for c in ((2,0),(-2,0),(0,2),(0,-2)):
 mid=tuple(F(x,2) for x in c);ring=audit.incident(mid);occupied=ring&star
 assert len(ring)==4 and len(occupied)==2
 normal=c
 for t in ring:
  center=tuple(F(sum(v[k] for v in t),3) for k in (0,1))
  assert (audit.dot(audit.sub(center,mid),normal)<0)==(t in occupied)

# Adversarial controls: alter necessary used/absent requirements or a bounce.
controls=[]
for p in sorted((HERE/'inputs').glob('certs-paths-*.json')):
 q=tuple(map(int,p.stem.removeprefix('certs-paths-').split('_')))
 for rec in json.loads(p.read_text()):
  if len(rec['path'])<3:continue
  path=tuple(tuple(F(*c) for c in pt) for pt in rec['path'])
  u,z=audit.path_requirements(path);stars=audit.incident((F(0),F(0)))|audit.incident(tuple(map(F,q)))
  U=audit.triangles(rec['U']);Z=audit.triangles(rec['Z'])
  if Z&stars or not z or not u-stars:continue
  variants=[]
  a=dict(rec);a['U']=list(U-{next(iter(u-stars))});variants.append(('missing-used',a))
  a=dict(rec);a['Z']=list(Z-{next(iter(z))});variants.append(('missing-absent',a))
  a=json.loads(json.dumps(rec));a['path'][1][0]=[1234567,101];variants.append(('wrong-reflection',a))
  a=json.loads(json.dumps(rec));a['path'][-1]=[[0,1],[0,1]];variants.append(('wrong-target',a))
  for label,a in variants:
   try:audit.check_record(a,q,False)
   except Exception:controls.append(label)
   else:raise AssertionError(('corruption accepted',label,p.name))
  break
 if len(controls)>=12:break
assert len(controls)==12
result=dict(status='PASS',placements=placements,completed_run_receipts=logs,adjacent_direct_segment=True,
 max_I_W21_k4=3,max_N_W21_k4=36,arithmetic_rows=len(rows),
 coordinate_bound_for_N38=str(F(2*(38-8)+4,3)),
 mutation_controls_rejected=controls,
 limitations=['Run receipts confirm completion metadata but do not cryptographically bind the executable/argv/environment at launch.',
 'BFS verifies all placements for N<=38; no full enumeration rerun or formal UNSAT proof.'])
(HERE/'bounds.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='completed_run_receipts'},indent=2))
