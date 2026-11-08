"""Check finite hypotheses of an all-finite-word parity obstruction, no rays."""
from pathlib import Path
from itertools import product
from collections import Counter
import json,hashlib
B=Path(__file__).resolve().parent
room=json.loads((B/'room.json').read_text());geo=json.loads((B/'reconstruct.json').read_text())
cells=set(map(tuple,geo['cells']));assert cells=={(-y-1,x) for x,y in cells};corners=set(map(tuple,geo['vertices']));points={(x+a,y+b) for x,y in cells for a,b in product((0,1),repeat=2)}
checks=[]
for p in sorted(points):
 incident=cells & {(p[0]+a,p[1]+b) for a,b in product((-1,0),repeat=2)}
 if p[0]%2 or p[1]%2:
  assert len(incident) in (1,3) and p in corners,(p,incident)
  checks.append(dict(point=p,incident_cells=len(incident)))
assert (0,0) not in corners
assert sum((x+a,y+b) in cells for a,b in product((-1,0),repeat=2) for x,y in [(0,0)])==4
boundary=[]
vs=geo['vertices']
for t in room['boundary_targets']:
 assert all(v%2==0 for v in t) and t!=[0,0]
 matches=[]
 for i,(a,b) in enumerate(zip(vs,vs[1:]+vs[:1])):
  cross=(t[0]-a[0])*(b[1]-a[1])-(t[1]-a[1])*(b[0]-a[0])
  if cross==0 and min(a[0],b[0])<=t[0]<=max(a[0],b[0]) and min(a[1],b[1])<=t[1]<=max(a[1],b[1]):matches.append(i)
 assert len(matches)==1 and tuple(t) not in corners
 i=matches[0];a,b=vs[i],vs[(i+1)%len(vs)];assert [a[j]+b[j] for j in (0,1)]==[2*v for v in t]
 boundary.append(dict(target=t,wall=i,endpoints=[a,b]))
# Reflection in each integer-coordinate wall fixes all four parity classes.
for a,b in zip(vs,vs[1:]+vs[:1]):
 axis=0 if a[0]==b[0] else 1
 for p in product(range(2),repeat=2):
  q=list(p);q[axis]=2*a[axis]-q[axis];assert tuple(v%2 for v in q)==p
# Exhaust the possible primitive parity directions, rather than sample lengths.
primitive_residues=[(0,1),(1,0),(1,1)]
assert all(any(p) and p!=(0,0) for p in primitive_residues)
out=dict(status='PASS',darkness='PARITY_THEOREM_HYPOTHESES_VERIFIED',walls=len(corners),squares=len(cells),quarter_turn_symmetry=True,non_A_corner_checks=checks,boundary_targets=boundary,primitive_residues=primitive_residues,room_sha256=hashlib.sha256((B/'room.json').read_bytes()).hexdigest(),scope='All positive-length finite specular paths, center to each boundary target and to itself. Polygon corners stop paths; final smooth-wall target is permitted. Geometry is idealized from raster, not author coordinates.')
(B/'darkness-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='non_A_corner_checks'},indent=2))
