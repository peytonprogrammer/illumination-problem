"""Exact cell/seam checks for the three-copy hand proof; no billiard trajectories."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
import json,hashlib
HERE=Path(__file__).resolve().parent
BASE={(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3)}

def edges(cells):
 out=Counter()
 for x,y in cells:
  for a,b in [((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),((x+1,y+1),(x,y+1)),((x,y+1),(x,y))]:out[tuple(sorted((a,b)))]+=1
 return {e for e,n in out.items() if n==1}

def roles(cells):
 points={(x+dx,y+dy) for x,y in cells for dx in (0,1) for dy in (0,1)}
 out={}
 for p in points:
  incidence={(p[0]+dx,p[1]+dy) for dx in (-1,0) for dy in (-1,0)} & cells
  if len(incidence)==4:kind='interior'
  elif len(incidence)==1:kind='convex'
  elif len(incidence)==3:kind='concave'
  elif len(incidence)==2:
   a,b=incidence
   assert abs(a[0]-b[0])+abs(a[1]-b[1])==1, ('pinch',p)
   kind='smooth'
  else:raise AssertionError(p)
  out[p]=kind
 return out

MAPS=[lambda p:p,lambda p:(p[0],-p[1]),lambda p:(4-p[0],-p[1])]

def image_cell(cell,f):
 points=[f((cell[0]+dx,cell[1]+dy)) for dx in (0,1) for dy in (0,1)]
 return min(x for x,y in points),min(y for x,y in points)

if __name__=='__main__':
 room_path=HERE/'peer-fast-inputs/cand-2_2-1.json';room=json.loads(room_path.read_text())
 physical={(min(p[0] for p in t),min(p[1] for p in t)) for t in room['triangles']}
 copies=[{image_cell(c,f) for c in BASE} for f in MAPS]
 assert all(not a&b for a,b in combinations(copies,2))
 assert set.union(*copies)==physical
 base_roles=roles(BASE);assert {p for p,k in base_roles.items() if k not in ['convex','concave']}=={(0,0),(2,-2)}
 assert all(x%2==0 and y%2==0 for (x,y),k in base_roles.items() if k not in ['convex','concave'])
 assert sum(k in ['convex','concave'] for k in base_roles.values())==10
 seam01=edges(copies[0])&edges(copies[1]);seam12=edges(copies[1])&edges(copies[2]);seam02=edges(copies[0])&edges(copies[2])
 assert seam01=={((-1,0),(0,0)),((0,0),(1,0))}
 assert seam12=={((2,1),(2,2)),((2,2),(2,3))};assert not seam02
 for i,j,seam in [(0,1,seam01),(1,2,seam12)]:
  for edge in seam:
   for p in edge:assert MAPS[i](p)==MAPS[j](p)
 physical_roles=roles(physical);smooth_exceptions={p for p,k in physical_roles.items() if k=='smooth' and (p[0]%2 or p[1]%2)}
 assert smooth_exceptions=={(-1,0),(1,0),(2,1),(2,3)}
 for p in smooth_exceptions:
  for cells,f in zip(copies,MAPS):
   if p in roles(cells):assert base_roles[f(p)]=='convex'
 assert physical_roles[(0,0)]==physical_roles[(2,2)]=='interior'
 for p,expected in [((0,0),(0,0)),((2,2),(2,-2))]:
  images={f(p) for cells,f in zip(copies,MAPS) if p in roles(cells)}
  assert images=={expected}
 # Every physical smooth/interior vertex maps to a smooth marked base point or convex base corner.
 # Thus a path avoiding physical corners never crosses a concave base corner.
 fiber_roles=defaultdict(set)
 for cells,f in zip(copies,MAPS):
  for p in roles(cells):fiber_roles[f(p)].add(physical_roles[p])
 assert all(fiber_roles[p] <= {'concave','convex'} for p,k in base_roles.items() if k=='concave')
 assert sum(k in ['convex','concave'] for k in physical_roles.values())==22
 result=dict(status='PASS',room_sha256=hashlib.sha256(room_path.read_bytes()).hexdigest(),base_cells=sorted(BASE),base_vertex_roles={str(p):k for p,k in sorted(base_roles.items())},copies=[sorted(c) for c in copies],fold_maps=['(x,y)','(x,-y)','(4-x,-y)'],seams=[sorted(seam01),sorted(seam12)],smooth_exceptions=sorted(smooth_exceptions),base_corner_fiber_roles={str(p):sorted(fiber_roles[p]) for p,k in sorted(base_roles.items()) if k in ['convex','concave']},walls=dict(base=10,three_copy=22),scope='Exact geometry and parity hypotheses only. The general primitive-step / retroreflection argument is in geometric-proof.md; no rays or direction search.')
 (HERE/'geometric-proof-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
