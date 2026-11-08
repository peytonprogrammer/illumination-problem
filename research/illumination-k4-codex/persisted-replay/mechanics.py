"""Check frozen peer bookkeeping against full independent state reconstruction.
No room enumeration, billiard paths or solver invocation.
"""
import ast, json, math, random, time
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent
p=HERE/'inputs/claude_k_enum_fast.py'
tree=ast.parse(p.read_text()); names={'tiling','patterns','options','set_tile','undo','learn','simple'}
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
g={'math':math,'combinations':__import__('itertools').combinations}
exec(compile(ast.fix_missing_locations(ast.Module(body=functions,type_ignores=[])),str(p),'exec'),g)
tiles,role,unit,_=g['tiling'](4,2);verts=sorted({p for t in tiles for p in t});vid={p:i for i,p in enumerate(verts)};tid={t:i for i,t in enumerate(tiles)}
ring=[];pos=[];complete=[]
for p in verts:
 r=sorted((t for t in tiles if p in t),key=lambda t:math.atan2(sum(q[1] for q in t)/3-p[1],sum(q[0] for q in t)/3-p[0]))
 ring.append([tid[t] for t in r]);pos.append({tid[t]:i for i,t in enumerate(r)});complete.append(len(r)*unit[role[p]]==8)
g.update(tiles=tiles,role=role,verts=verts,vid=vid,tid=tid,ring=ring,pos=pos,complete=complete,
         CORNER={'B':{1,2,3,5,6,7},'C':{1,3}},EXCEPT={'B':{4,8},'C':{2,4}})
g.update(PAT=[g['patterns'](i) if complete[i] else {} for i in range(len(verts))],OPT=[{} for p in verts])
g.update(assign=[-1]*len(tiles),known=[0]*len(verts),value=[0]*len(verts),nused=[0]*len(verts),
         FULL=[(1<<len(r))-1 for r in ring],tot=dict(walls=0,exc=0,full=0,und_bc=0,n=0),active=set(),
         tverts=[[vid[p] for p in t] for t in tiles],isA=[role[p]=='A' for p in verts],isBC=[role[p]!='A' for p in verts],
         stats=dict(hit_window=0),rem=[],sat=[0],watch={})

def reconstruct(guards):
 a=g['assign']; expected=dict(walls=0,exc=0,full=0,und_bc=0,n=a.count(1));active=set()
 for v,r in enumerate(ring):
  known=sum(1<<i for i,t in enumerate(r) if a[t]!=-1);value=sum(1<<i for i,t in enumerate(r) if a[t]==1);n=value.bit_count()
  assert (g['known'][v],g['value'][v],g['nused'][v])==(known,value,n)
  if n and known==g['FULL'][v]:
   kd=g['PAT'][v].get(value,(0,0,0))
   for key,inc in zip(('walls','exc','full'),kd):expected[key]+=inc
  elif n:
   active.add(v)
   if role[verts[v]]!='A':expected['und_bc']+=1
  if n and complete[v]:
   options=[m for m in g['PAT'][v] if m&known==value]
   assert g['options'](v,known,value)==options
 assert g['tot']==expected,(g['tot'],expected)
 assert g['active']==active
 rem=[sum(a[t]!=x for t,x in need.items()) for need in guards]
 assert rem==g['rem'];assert g['sat'][0]==rem.count(0)

rng=random.Random(20261031);trail=[];stack=[];guards=[];bad_returns=0;t0=time.monotonic()
for step in range(15000):
 free=[t for t,a in enumerate(g['assign']) if a==-1]
 if step%19==0:
  need={rng.randrange(len(tiles)):rng.randrange(2) for j in range(7)};guards.append(need)
  g['learn']({tiles[t] for t,x in need.items() if x},{tiles[t] for t,x in need.items() if not x})
 elif stack and (not free or rng.random()<0.45):g['undo'](trail,stack.pop())
 elif free:
  stack.append(len(trail));bad_returns+=not g['set_tile'](rng.choice(free),rng.randrange(2),trail)
 reconstruct(guards)
 # Check local lower bound against every independent fan option at each active vertex.
 for v in g['active']:
  if not complete[v]:continue
  opts=g['options'](v,g['known'][v],g['value'][v])
  if role[verts[v]]!='A':
   assert all(sum(g['PAT'][v][m][:2])==1 for m in opts)
g['undo'](trail,0);reconstruct(guards)
assert all(a==-1 for a in g['assign'])
result=dict(status='PASS',operations=15000,reconstructions=15001,guards=len(guards),invalid_local_set_returns=bad_returns,
            tiles=len(tiles),vertices=len(verts),seconds=round(time.monotonic()-t0,2),
            scope='Full known/value/active/total/guard state and memoized options under arbitrary assignments, rollback and late learning; not complete branch replay.')
(HERE/'mechanics.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
