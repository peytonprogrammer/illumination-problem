"""Necessary k6 support census only. No SAT calls or optical discovery."""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import importlib.util,json,hashlib,shutil
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
N=((1,0),(-1,0),(0,1),(0,-1))

def neighbors(S):return {(x+a,y+b) for x,y in S for a,b in N}
def connected(S):
    seen={next(iter(S))};todo=list(seen)
    for p in todo:
        for q in neighbors({p}) & S:
            if q not in seen:seen.add(q);todo.append(q)
    return seen==S

def images(S):
    for flip in (False,True):
        for sx,sy in product((-1,1),repeat=2):
            yield {(sx*(y if flip else x),sy*(x if flip else y)) for x,y in S}

def canonical(S):
    return min(tuple(sorted((x-a,y-b) for x,y in T)) for T in images(S) for a,b in T)

def marked_key(S,pair):
    outs=[]
    for flip in (False,True):
        for sx,sy in product((-1,1),repeat=2):
            f=lambda p:(sx*(p[1] if flip else p[0]),sy*(p[0] if flip else p[1]))
            T={f(p) for p in S};P={f(p) for p in pair}
            for a,b in T:
                outs.append((tuple(sorted((x-a,y-b) for x,y in T)),tuple(sorted((x-a,y-b) for x,y in P))))
    return min(outs)

def triple_shapes(radius,cap):
    diamond=[(x,y) for x in range(-radius,radius+1) for y in range(-radius,radius+1) if 0<abs(x)+abs(y)<=radius]
    shapes={};rooted=0;disconnected_R_rejected=0
    for a,b in combinations(diamond,2):
        S={(0,0),a,b};R=S|neighbors(S);boundary=len(R)-3
        if boundary>cap:continue
        # At cap10 disconnected distance-two full components force b>=10.
        # Hence no outside cell is available to join disconnected R components.
        if not connected(R):
            assert boundary==10
            disconnected_R_rejected+=1;continue
        rooted+=1;shapes[canonical(S)]=boundary
    return shapes,rooted,disconnected_R_rejected

# Freeze read-only input sources used to bind this enumeration.
for source,name in [(BASE/'branch-support.json','old-branch-support.json'),(ROOT.parents[1]/'illumination_geometry.py','illumination_geometry.py')]:
    destination=ROOT/'inputs'/name
    if not destination.exists():shutil.copyfile(source,destination)
spec=importlib.util.spec_from_file_location('frozen_geometry',ROOT/'inputs/illumination_geometry.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
old=json.loads((ROOT/'inputs/old-branch-support.json').read_text())['cases']
old_shapes={canonical(set(map(tuple,c['full']))):c['tag'] for c in old if c['I']==3}
old_tags={c['tag'] for c in old}
shapes,rooted,rejected=triple_shapes(12,10)
small,smallrooted,_=triple_shapes(5,10)
assert shapes==small and rooted==smallrooted
assert len(shapes)==18
# Explicit check of the new disconnected-overlap cases, rather than silently
# importing k5's now-invalid connected-distance-two premise.
def overlap_connected(S):
    seen={next(iter(S))};todo=list(seen)
    for p in todo:
        for q in S-seen:
            if abs(p[0]-q[0])+abs(p[1]-q[1])<=2:seen.add(q);todo.append(q)
    return seen==S

rows=[]
def add(tag,S,cap,pairs):
    R=S|neighbors(S);boundary=len(R-S);extra=cap-boundary;assert extra>=0
    allowed=set(R)
    for step in range(extra):allowed|=neighbors(allowed)
    ts={t for x,y in allowed for t in g.patch(2*x-1,2*x+1,2*y-1,2*y+1)}
    assert len(ts)==8*len(allowed)
    keys={marked_key(S,pair) for pair in pairs}
    rows.append({'tag':tag,'I':len(S),'full':sorted(S),'mandatory':sorted(R),'allowed':sorted(allowed),
                 'external_neighbors':boundary,'partial_plus_missing_cap':cap,'outside_cell_cap':extra,
                 'mark_pairs':pairs,'marked_pairs_raw':len(pairs),'marked_pair_orbits':len(keys),
                 'allowed_cells':len(allowed),'triangle_universe':len(ts),
                 'new_support':tag not in old_tags,'overlap_connected':overlap_connected(S)})

# A connected H=occupied cells union mandatory neighbors has <=I+cap cells.
# Thus I2 full marks have distance <=I+cap-1=13. Enumerate that conservative
# complete range, then use the exact two-R-component connector lower bound.
excluded_distances=[]
for distance in range(2,14):
    for x in range((distance+1)//2,distance+1):
        y=distance-x;S={(0,0),(x,y)};boundary=len(neighbors(S)-S)
        required_outside=max(0,distance-3)
        if required_outside>12-boundary:
            excluded_distances.append((x,y));continue
        add(f'I2_{x}_{y}',S,12,[[(0,0),(x,y)]])
assert sum(r['I']==2 for r in rows)==18
new_index=0
for shape,boundary in sorted(shapes.items()):
    S=set(shape)
    tag=old_shapes.get(shape)
    if tag is None:tag=f'I3_k6_{new_index}';new_index+=1
    pairs=[list(p) for p in combinations(shape,2) if abs(p[0][0]-p[1][0])+abs(p[0][1]-p[1][1])>1]
    assert pairs
    add(tag,S,10,pairs)
for c in old:
    r=next(r for r in rows if r['tag']==c['tag'])
    assert set(map(tuple,c['full']))==set(map(tuple,r['full']))
    assert set(map(tuple,c['allowed']))<=set(map(tuple,r['allowed']))
summary={}
for I in (2,3):
    rs=[r for r in rows if r['I']==I]
    summary[str(I)]={'supports':len(rs),'new_supports':sum(r['new_support'] for r in rs),
                    'marked_pairs_raw':sum(r['marked_pairs_raw'] for r in rs),
                    'marked_pair_orbits':sum(r['marked_pair_orbits'] for r in rs),
                    'triangle_universe_min':min(r['triangle_universe'] for r in rs),
                    'triangle_universe_max':max(r['triangle_universe'] for r in rs),
                    'triangle_universe_sum_per_raw_pair':sum(r['triangle_universe']*r['marked_pairs_raw'] for r in rs),
                    'disconnected_overlap_supports':sum(not r['overlap_connected'] for r in rs)}
out={'status':'COMPLETE_NECESSARY_SUPPORT_CENSUS','W_cap':21,'k_cap':6,'N_cap':41,
     'input_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'inputs').iterdir() if p.is_file()},
     'summary':summary,'total_supports':len(rows),'total_marked_pairs_raw':sum(r['marked_pairs_raw'] for r in rows),
     'total_marked_pair_orbits':sum(r['marked_pair_orbits'] for r in rows),
     'I3_radius12_rooted':rooted,'I3_disconnected_mandatory_rejected':rejected,
     'I2_excluded_by_connector_count':excluded_distances,'cases':rows,
     'scope':'Necessary full-cell supports and conservative encoder-style universes, not geometrically feasible rooms or SAT workload timings. I4 is peer-owned and excluded from this count.'}
(ROOT/'count.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('cases','I2_excluded_by_connector_count')},indent=2))
