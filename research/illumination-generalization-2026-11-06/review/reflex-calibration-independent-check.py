"""Independent validation of A26 frozen paths and all-real affine first-hit guards."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import pairwise
import importlib.util,json,hashlib
H=Path(__file__).resolve().parent;C=H.parent/'construction'
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
P0=[(2,2),(4,2),(4,0),(2,0),(2,-4),(-2,-4),(-2,-3),(0,-3),(0,0),(-3,0),(-3,-2),(-4,-2),(-4,2),(0,2),(0,4),(2,4)]
own.simple(P0)
req=json.loads((C/'reflex-return-calibration-review-request.json').read_text())
for pin in req['sources']:assert hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()==pin['sha256']
rows=[]
certs=json.loads((C/'reflex-prefix-check.json').read_text())['cases']
assert [r['lambda'] for r in certs]==list(range(2,9))
for row in certs:
 L=Q(row['lambda']);cert=row['certificate'];poly=[(L*x,L*y) for x,y in P0]
 path=[tuple(map(Q,z)) for z in cert['points']]
 assert path[0]==(2*L-2,2*L+2) and path[-1]==(2*L+2,2*L-2)
 assert all(z%2==0 for p in (path[0],path[-1]) for z in p)
 assert all(not own.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
 guards=own.path_check(poly,path);assert guards['reflections']==cert['reflections']
 word=[]
 for p in path[1:-1]:
  hits=[i for i,(a,b) in enumerate(own.edges(poly)) if own.on(a,b,p)];assert len(hits)==1
  word.append(hits[0])
 assert word==cert['word']
 rows.append({'lambda':str(L),'word':word,**guards})
# Affine coordinates represented as (coefficient,constant), independently
# built from the displayed contact formulas rather than author ray code.
def af(a,b=0):return(Q(a),Q(b))
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def scale(a,s):return(a[0]*s,a[1]*s)
def val(a,L):return a[0]*L+a[1]
poly=[(af(x),af(y)) for x,y in P0]
S=(af(2,-2),af(2,2));T=(af(2,2),af(2,-2))
contacts=[(af(-Q(j,3),-Q(8,3)),af(-4 if j%2==0 else -3)) for j in range(6)]
contacts += [(af(-2),af(-4,8)),(af(-2,Q(8,3)),af(-4))]
contacts += [(af(-Q(j,3),Q(8,3)),af(-3 if j%2 else -4)) for j in range(5,-1,-1)]
path=[S]+contacts+[T];word=[4,6]*3+[5,4]+[6,4]*3
assert len(contacts)==14
predicates=[];total=af(0);velocity=(-1,-3)
for step,(a,b) in enumerate(pairwise(path)):
 duration=scale(sub(b[0],a[0]),Q(1,velocity[0]));assert scale(duration,velocity[1])==sub(b[1],a[1])
 predicates.append(duration);total=add(total,duration);events=[]
 for idx,(c,d) in enumerate(own.edges(poly)):
  axis=0 if c[0]==d[0] else 1;other=1-axis
  dt=scale(sub(c[axis],a[axis]),Q(1,velocity[axis]))
  hit=add(a[other],scale(dt,velocity[other]))
  lo,hi=(c[other],d[other]) if P0[idx][other]<P0[(idx+1)%16][other] else (d[other],c[other])
  low=sub(hit,lo);high=sub(hi,hit);before=sub(dt,duration)
  predicates += [dt,low,high,before]
  if val(dt,9)>0 and val(low,9)>=0 and val(high,9)>=0 and val(before,9)<=0:events.append((idx,dt,low,high))
 if step<14:
  assert len(events)==1 and events[0][0]==word[step] and events[0][1]==duration
  assert val(events[0][2],9)>0 and val(events[0][3],9)>0
  idx=word[step];axis=0 if poly[idx][0]==poly[(idx+1)%16][0] else 1
  velocity=tuple(-v if k==axis else v for k,v in enumerate(velocity))
 else:assert events==[]
assert total==af(8)
roots=[abs(b/a) for a,b in predicates if a]
assert len(predicates)==975 and max(roots)==8
# Every atomic decision is constant throughout lambda>8, since all its
# roots have absolute value<=8; identically-zero predicates remain zero.
assert all(a==0 or abs(b/a)<=8 for a,b in predicates)
for L in (Q(9),Q(17,2),Q(21,2)):
 pp=[(L*x,L*y) for x,y in P0];pts=[tuple(val(z,L) for z in p) for p in path]
 result=own.path_check(pp,pts);assert result['reflections']==14
out={'status':'ALL_SEVEN_PREFIX_PATHS_AND_ALL_REAL_TAIL_GT8_INDEPENDENTLY_VERIFIED','prefix_rows':rows,'prefix_reflections':sum(r['reflections'] for r in rows),'prefix_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'symbolic_affine_predicates':len(predicates),'all_absolute_roots_at_most':'8','symbolic_reflections':14,'symbolic_total_time':['8','0'],'source_sha256':{pin['path']:pin['sha256'] for pin in req['sources']},'whole_goal_complete':False,'discovery':False,'limits':'One specified16wallmarkedfamily, allintegerlambda>=2; no newdirection/roomsearch or universalW21claim.'}
(H/'reflex-calibration-independent-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('prefix_rows','source_sha256')}))
