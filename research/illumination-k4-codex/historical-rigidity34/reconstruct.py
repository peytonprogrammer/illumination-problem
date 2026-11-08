"""Reconstruct the one fixed published vector boundary and its square cells."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,sys
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent.parent))
from illumination_geometry import patch,check
edges=json.loads((B/'inputs/novelty-geometry-check.json').read_text())['orourke']['edges'];adj=defaultdict(list)
for a,b in edges:a,b=tuple(a),tuple(b);adj[a].append(b);adj[b].append(a)
assert len(adj)==34 and all(len(v)==2 for v in adj.values())
start=min(adj);vertices=[start];old=None;p=start
while True:
 q=min(q for q in adj[p] if q!=old)
 if q==start:break
 vertices.append(q);old,p=p,q
assert len(vertices)==34

def inside(p):
 odd=False
 for a,b in zip(vertices,vertices[1:]+vertices[:1]):
  if (a[1]>p[1])!=(b[1]>p[1]):
   x=F(a[0])+F(p[1]-a[1])*F(b[0]-a[0],b[1]-a[1])
   if x>p[0]:odd=not odd
 return odd
cells=[]
for x in range(min(p[0] for p in vertices),max(p[0] for p in vertices)):
 for y in range(min(p[1] for p in vertices),max(p[1] for p in vertices)):
  if inside((F(2*x+1,2),F(2*y+1,2))):cells.append((x,y))
triangles=[t for x,y in cells for t in patch(x,x+1,y,y+1)]
marks=[(2,0),(6,0)]
for p in marks:
 assert inside(p) and all((p[0]+dx,p[1]+dy) in cells for dx in (-1,0) for dy in (-1,0))
room=dict(triangles=triangles,marked=marks,require_simple=True,slits=[],provenance='O’Rourke public Fig9.14 vector boundary; marks read from rendered grid as(2,0),(6,0). Historical association with1995 original not established here.')
(B/'room.json').write_text(json.dumps(room,indent=2)+'\n');receipt=check(room,strict=False)
result=dict(status='PASS',vertices=vertices,cells=cells,marks=marks,geometry=receipt,figure='https://www.science.smith.edu/~jorourke/AGVT/Templates/OrthoTokarsky.pdf',ambiguities=['Figure integer unit and orientation chosen by the previously audited vector-to-grid map.','Mark centers identified from visible dotted grid, not from an original1995 coordinate table.','Do not identify this figure byte-for-byte with a1995 original before source comparison.'])
(B/'reconstruct.json').write_text(json.dumps(result,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('vertices','cells')},indent=2,default=str))
