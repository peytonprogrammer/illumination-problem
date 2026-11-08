"""One hand-forced residue; retained fixed paths only, no archive access."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
check=runpy.run_path(str(ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py'))
tri=lambda t:tuple(sorted(map(tuple,t)))
slots={n:tri(t) for n,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,m):
 return {tri((a,(a[0]+dirs[i%8][0],a[1]+dirs[i%8][1]),(a[0]+dirs[(i+1)%8][0],a[1]+dirs[(i+1)%8][1]))) for i in range(start,start+m)}
room=set().union(*(check['incident']((F(x),F(y))) for x,y in ((0,0),(2,0),(2,2))))
room |= fan((-2,0),7,4)|fan((-2,2),6,2)|{slots[n] for n in ['B+','E-','T-','R-']}
edges=Counter();angles=Counter()
for t in room:
 for i,p in enumerate(t):
  q=t[(i+1)%3];edges[tuple(sorted((p,q)))]+=1
  angles[p]+=1 if p[0]%2==p[1]%2 else 2 # units of45degrees
assert max(edges.values())==2
boundary=[edge for edge,n in edges.items() if n==1];adj=defaultdict(set)
for p,q in boundary:adj[p].add(q);adj[q].add(p)
assert all(len(v)==2 for v in adj.values())
seen=set();todo=[min(adj)]
while todo:
 p=todo.pop()
 if p in seen:continue
 seen.add(p);todo.extend(adj[p]-seen)
assert seen==set(adj)
W=sum(angles[p]!=4 for p in adj)
interiorA={p for p,n in angles.items() if n==8 and p[0]%2==p[1]%2==0}
assert interiorA=={(0,0),(2,0),(2,2)}
Q=sum(3 if n==4 else n for p,n in angles.items() if p[0]%2==p[1]%2==0 and n<8)
sA=sum(n==4 and p[0]%2==p[1]%2==0 for p,n in angles.items())
sN=sum(n==4 and not(p[0]%2==p[1]%2==0) for p,n in angles.items())
J=sum(n==8 and not(p[0]%2==p[1]%2==0) for p,n in angles.items())
ledger={'triangles':len(room),'W':W,'Q':Q,'sA':sA,'sN':sN,'J':J,'k':J+sN,'Delta':Q+sN-8}
assert ledger=={'triangles':34,'W':20,'Q':9,'sA':1,'sN':3,'J':3,'k':6,'Delta':4},ledger
hits={};trials={};sources={}
for rel in ['third-surplus-review/local-mixed-residue-frozen.json','third-surplus-review/local-e2-residue-frozen.json','third-surplus-review/center-residue-frozen.json']:
 p=ROOT/rel;raw=p.read_bytes();sources[rel]=hashlib.sha256(raw).hexdigest()
 for name,t in json.loads(raw)['hits'].items():
  path=[tuple(F(*c) for c in p) for p in t['path']]
  assert path[0]==(0,0) and path[-1]==(2,2)
  U,Z=check['path_requirements'](path);key=rel+':'+name
  trials[key]={'source_line':t['source_line'],'missing':sorted(U-room),'blocked':sorted(Z&room)}
  if U<=room and not Z&room:hits[key]={'source_line':t['source_line'],'frame':t['frame'],'endpoint_reversal':t['endpoint_reversal'],'reflections':len(path)-2,'path':t['path'],'required_triangles':sorted(U),'forbidden_triangles':sorted(Z)}
(HERE/'remote22-residue-check.json').write_text(json.dumps({'status':'COVERED' if hits else 'OPTICAL_RESIDUE','ledger':ledger,'triangles':sorted(room),'sources':sources,'trials':trials,'hits':hits,'scope':'Exactly one hand-forced geometry, previously retained fixed paths only; no archives, discovery or cap assignments.'},indent=2)+'\n')
print(json.dumps({'status':'COVERED' if hits else 'OPTICAL_RESIDUE','ledger':ledger,'hits':[{k:v[k] for k in ['source_line','frame','endpoint_reversal','reflections']} for v in hits.values()]}))
