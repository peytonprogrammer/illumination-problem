"""Read-only gluing/period calculation; no billiard trajectories or searches."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from collections import deque
from math import gcd
from functools import reduce
from itertools import combinations
import json, hashlib
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from illumination_cover import build
from illumination_midpoint import vertex_data, half_turns, components, inspect_turn

def index(vectors):
    return reduce(gcd, (abs(a*d-b*c) for (a,b),(c,d) in combinations(vectors,2)),0)

records=[]
for filename in ('illumination-22.json','illumination-search-simple-unrestricted.json'):
    path=ROOT.parent/filename
    c=build(json.loads(path.read_text()));v=vertex_data(c)
    pos={0:(0,0)};todo=deque([0])
    while todo:
        i=todo.popleft()
        for p,e in ((c['H'],(1,0)),(c['V'],(0,1))):
            j=p[i];q=(pos[i][0]+e[0],pos[i][1]+e[1])
            if j not in pos:pos[j]=q;todo.append(j)
    assert len(pos)==len(c['H'])
    generators=set()
    for i in pos:
        for p,e in ((c['H'],(1,0)),(c['V'],(0,1))):
            j=p[i];generators.add((pos[i][0]+e[0]-pos[j][0],pos[i][1]+e[1]-pos[j][1]))
    generators.discard((0,0))
    corners=((0,0),(1,0),(1,1),(0,1))
    representatives=[]
    for group in v['members']:
        i,q=group[0];representatives.append((pos[i][0]+corners[q][0],pos[i][1]+corners[q][1]))
    cones=[k for k,g in enumerate(v['members']) if len(g)>4]
    base=representatives[cones[0]]
    relative=set(generators)
    relative.update((representatives[k][0]-base[0],representatives[k][1]-base[1]) for k in cones)
    source=[representatives[k] for k,col in enumerate(v['colors']) if col==1]
    target=[representatives[k] for k,col in enumerate(v['colors']) if col==2]
    turns=half_turns(c['H'],c['V'],components(c['H'],c['V'])[0])
    assert len(turns)==1
    turn=inspect_turn(c,v,components(c['H'],c['V'])[0],turns[0])
    fixed=set(turn['fixed_vertices'])
    regular={k for k,g in enumerate(v['members']) if len(g)==4}
    marked={k for k,col in enumerate(v['colors']) if col in (1,2)}
    all_even=all(a%2==0 and b%2==0 for a,b in generators)
    assert all_even and index(generators)==4
    if filename=='illumination-22.json':assert regular-fixed==marked
    anchor=next((representatives[k] for k,g in enumerate(v['members']) if len(g)==28),None)
    source_residue=tuple(x%2 for x in source[0])
    assert all(tuple(x%2 for x in p)==source_residue for p in source+target)
    for group in v['members']:
        residues={( (pos[i][0]+corners[q][0])%2,(pos[i][1]+corners[q][1])%2) for i,q in group}
        assert len(residues)==1
    records.append(dict(absolute_lattice_is_2Z2=all_even and index(generators)==4, regular_nonfixed_equals_source_union_target=regular-fixed==marked, regular_nonfixed_count=len(regular-fixed), source_target_residue=source_residue, unique_m7_anchor=anchor, unique_m7_anchor_residue=None if anchor is None else tuple(x%2 for x in anchor), input=filename,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),squares=len(pos),absolute_generators=sorted(generators),absolute_lattice_index_in_Z2=index(generators),cone_relative_lattice_index_in_Z2=index(relative),source_representatives=source,target_representatives=target,scope='Spanning-tree periods and cone-relative periods. No affine group, ray, or quotient enumeration.'))
result=dict(status='PASS',records=records,dependencies_sha256={name:hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest() for name in ('illumination_cover.py','illumination_midpoint.py','illumination_geometry.py')})
(ROOT/'literature-lattice-probe.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
