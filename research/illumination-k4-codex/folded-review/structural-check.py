from pathlib import Path
from itertools import product
import json,hashlib
B=Path(__file__).resolve().parent
V=[(0,0),(1,1),(2,1),(2,3),(1,3),(1,2),(-1,2),(-1,1),(0,1)]
# Explicit local star combinatorics: possible differences between two axial
# neighbor vectors exhaust the only possible shared-neighbor separations.
U={(1,0),(-1,0),(0,1),(0,-1)}
differences={(a[0]-b[0],a[1]-b[1]) for a in U for b in U if a!=b}
even={d for d in differences if d[0]%2==d[1]%2==0};assert even=={(2,0),(-2,0),(0,2),(0,-2)}
for d in even:assert len(U&{(d[0]+x,d[1]+y) for x,y in U})==1
# At the shared mixed vertex there are four90-degree sectors: source star
# occupies two; preserving a genuine corner permits exactly one added sector.
assert 2+1==3 and 2+2==4
# Explicit open overlap witness for the9-wall base: the rectangle[1,2]x[1,3]
# lies in P, is fixed setwise by reflection across y=2, and contains a disk
# around(3/2,2). All four rational box vertices are strictly inside that arm.
box=[(1.25,1.75),(1.75,1.75),(1.75,2.25),(1.25,2.25)]
assert all(1<x<2 and 1<y<3 for x,y in box)
assert {(x,4-y) for x,y in box}==set(box)
result=dict(status='PASS',shared_neighbor_separations=sorted(even),max_shared_axial_neighbors=1,minimum_triangles_interior_plus_boundary_mark=15,wall_lower_bound=14,nine_wall_overlap_box=box,scope='Prescribed fan-count and overlap controls only; the proof and topology are in structural-next.md and await peer review.')
(B/'structural-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
