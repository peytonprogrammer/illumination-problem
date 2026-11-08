"""Necessary orthogonal k<=7/W<=20 marked supports, not room assignments.
Adapted from the existing k6-support-census/count.py geometry-only workflow.
The new orthogonal cap and distance-eight exclusion are proved in proof.txt.
"""
from pathlib import Path
from itertools import combinations, product
import csv
import hashlib
import json

ROOT=Path(__file__).resolve().parent
N=((1,0),(-1,0),(0,1),(0,-1))
WMAX,KMAX=20,7

def neighbors(S): return {(x+dx,y+dy) for x,y in S for dx,dy in N}
def connected(S):
    seen={next(iter(S))}; todo=list(seen)
    for x,y in todo:
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if p in S and p not in seen: seen.add(p); todo.append(p)
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
            def f(p): return sx*(p[1] if flip else p[0]),sy*(p[0] if flip else p[1])
            T={f(p) for p in S}; pair_image={f(p) for p in pair}
            for a,b in T:
                outs.append((tuple(sorted((x-a,y-b) for x,y in T)),
                             tuple(sorted((x-a,y-b) for x,y in pair_image))))
    return min(outs)

def overlap_connected(S):
    seen={next(iter(S))}; todo=list(seen)
    for p in todo:
        for q in S-seen:
            if abs(p[0]-q[0])+abs(p[1]-q[1])<=2:
                seen.add(q); todo.append(q)
    return seen==S

coarse_caps={I:(WMAX-4*I+2*KMAX)//2 for I in (2,3,4)}
orthogonal_caps={I:(WMAX+3*KMAX-2-6*I)//2 for I in (2,3,4)}
assert coarse_caps=={2:13,3:11,4:9}
assert orthogonal_caps=={2:13,3:10,4:7}
old=json.loads((ROOT/'inputs/k6-count.json').read_text())
old_support_tags={canonical(set(map(tuple,r['full']))):r['tag'] for r in old['cases']}
old_supports=set(old_support_tags)
old_marked={marked_key(set(map(tuple,r['full'])),p) for r in old['cases'] for p in r['mark_pairs']}
rows=[]

def add(tag,S,cap):
    R=S|neighbors(S); b=len(R-S); extra=cap-b
    assert extra>=0
    allowed=set(R)
    for _ in range(extra): allowed|=neighbors(allowed)
    pairs=[p for p in combinations(sorted(S),2) if abs(p[0][0]-p[1][0])+abs(p[0][1]-p[1][1])>1]
    assert pairs
    groups={}
    for pair in pairs:
        key=marked_key(S,pair)
        groups.setdefault(key,[]).append(pair)
    row={'tag':tag,'I':len(S),'full':sorted(S),'neighborhood':sorted(R),
         'neighborhood_note':'Contains possible empty cells; do not force all neighborhood cells occupied.',
         'allowed':sorted(allowed),'external_neighbors':b,'partial_plus_missing_cap':cap,
         'outside_cell_cap':extra,'mark_pairs':pairs,
         'mark_pairs_original_coordinates':[[[2*x,2*y] for x,y in pair] for pair in pairs],
         'marked_pairs_raw':len(pairs),'marked_pair_orbits':len(groups),
         'mark_orbit_representatives':[min(v) for k,v in sorted(groups.items())],
         'mark_orbit_multiplicities':[len(v) for k,v in sorted(groups.items())],
         'allowed_A_cells':len(allowed),'canonical_triangle_universe':8*len(allowed),
         'unit_square_universe':4*len(allowed),'overlap_connected':overlap_connected(S),
         'previous_k6_tag':old_support_tags.get(canonical(S)),
         'new_support_vs_k6':canonical(S) not in old_supports,
         'new_marked_orbits_vs_k6':sum(k not in old_marked for k in groups)}
    rows.append(row)

# Connected H has <=I+cap=15 cells, so d<=14 is an a priori complete domain.
# The outside-cell connector bound first leaves d<=8. The orthogonal all-
# quarter-fan chain argument then excludes every d=8 case (proof.txt section4).
distance_eight=[]; connector_rejected=[]
for distance in range(2,15):
    for x in range((distance+1)//2,distance+1):
        y=distance-x; F={(0,0),(x,y)}; b=len(neighbors(F)-F)
        needed=max(0,distance-3)
        if needed>orthogonal_caps[2]-b:
            connector_rejected.append((x,y)); continue
        if distance==8:
            distance_eight.append({'full':sorted(F),'distance':8,'external_neighbors':b,
                                   'minimum_outside':5,'reason':'orthogonal_quarter_chain_obstruction'})
            continue
        add(f'I2_{x}_{y}',F,orthogonal_caps[2])

# Connected H has <=13 cells. Thus radius12 is complete for all rooted triples.
diamond=[(x,y) for x in range(-12,13) for y in range(-12,13) if 0<abs(x)+abs(y)<=12]
triple_shapes=set(); rooted=0; disconnected_R_rejected=0
for p,q in combinations(diamond,2):
    F={(0,0),p,q}; R=F|neighbors(F); b=len(R-F)
    if b>orthogonal_caps[3]: continue
    if not connected(R):
        assert b==10
        disconnected_R_rejected+=1; continue
    rooted+=1; triple_shapes.add(canonical(F))
for index,shape in enumerate(sorted(triple_shapes)):
    add(f'I3_{index:02d}',set(shape),orthogonal_caps[3])

# The coarse I4 charge b<=8 permits exactly the old O/T/S equality supports.
# All are excluded in the orthogonal model by b>=8>cap7. Enumeration of these
# SUPPORTS is a comparison/control only; no local fans or rooms are generated.
diamond6=[(x,y) for x in range(-6,7) for y in range(-6,7) if 0<abs(x)+abs(y)<=6]
i4_shapes=set(); i4_rooted=0
for pp in combinations(diamond6,3):
    F={(0,0),*pp}
    if len(neighbors(F)-F)>8 or not overlap_connected(F): continue
    i4_rooted+=1; i4_shapes.add(canonical(F))
i4_excluded=[{'full':shape,'external_neighbors':len(neighbors(set(shape))-set(shape)),
              'orthogonal_partial_plus_missing_cap':7,'reason':'external_boundary_exceeds_cap'}
             for shape in sorted(i4_shapes)]

summary={}
for I in (2,3):
    rr=[r for r in rows if r['I']==I]
    summary[str(I)]={'supports':len(rr),'marked_pairs_raw':sum(r['marked_pairs_raw'] for r in rr),
                    'marked_pair_orbits':sum(r['marked_pair_orbits'] for r in rr),
                    'disconnected_overlap_supports':sum(not r['overlap_connected'] for r in rr),
                    'new_supports_vs_k6':sum(r['new_support_vs_k6'] for r in rr),
                    'new_marked_orbits_vs_k6':sum(r['new_marked_orbits_vs_k6'] for r in rr),
                    'allowed_A_cells_range':[min(r['allowed_A_cells'] for r in rr),max(r['allowed_A_cells'] for r in rr)],
                    'triangle_universe_range':[min(r['canonical_triangle_universe'] for r in rr),max(r['canonical_triangle_universe'] for r in rr)]}
summary['4']={'supports_retained':0,'coarse_equality_supports_excluded':len(i4_excluded),
              'reason':'orthogonal cap7 is below the all-four-support boundary minimum8'}
# Mechanical incidence/turn controls underpinning the orthogonal cap and d8 proof.
# A partial orthogonal A fan consists of 1,2,3 consecutive unit quadrants.
quarter_fans=[{'unit_quadrants':1,'triangles':2,'Q':2},
              {'unit_quadrants':2,'triangles':4,'Q':3},
              {'unit_quadrants':3,'triangles':6,'Q':6}]
assert all(r['Q']>=2 for r in quarter_fans)
assert len(distance_eight)==5 and len(i4_excluded)==3
out={'status':'COMPLETE_NECESSARY_ORTHOGONAL_SUPPORT_CENSUS',
     'wall_cap':20,'exception_cap':7,'selected_triangle_cap':42,'selected_unit_square_cap':21,
     'interior_A_cap_coarse':4,'interior_A_cap_after_orthogonality':3,
     'canonical45_partial_plus_missing_caps':coarse_caps,
     'orthogonal_partial_plus_missing_caps':orthogonal_caps,
     'summary':summary,'total_supports':len(rows),
     'total_marked_pairs_raw':sum(r['marked_pairs_raw'] for r in rows),
     'total_marked_pair_orbits':sum(r['marked_pair_orbits'] for r in rows),
     'I3_root_radius':12,'I3_rooted_triples_retained':rooted,
     'I3_disconnected_neighborhood_rejections':disconnected_R_rejected,
     'I4_comparison_root_radius':6,'I4_coarse_rooted_equality_patterns':i4_rooted,
     'orthogonal_partial_fan_controls':quarter_fans,
     'distance_eight_exclusions':distance_eight,'I4_exclusions':i4_excluded,
     'I2_connector_excluded_offsets':connector_rejected,
     'comparison_to_k6':{'supports':old['total_supports'],'raw_marked_pairs':old['total_marked_pairs_raw'],
                         'marked_pair_orbits':old['total_marked_pair_orbits']},
     'input_sha256':{'k6-count.json':hashlib.sha256((ROOT/'inputs/k6-count.json').read_bytes()).hexdigest()},
     'cases':rows,
     'scope':'Complete necessary support cover, not a list of feasible rooms. Orthogonal unit-square unions in the fixed canonical grid, interior A marks, k<=7, W<=20. Adjacent marked pairs and proved geometric exclusions omitted. No room assignments, SAT, optical guards, ray/orbit tests or pilot.'}
(ROOT/'count.json').write_text(json.dumps(out,indent=2)+'\n')
marked=[]
for support_index,row in enumerate(rows):
    for index,(pair,multiplicity) in enumerate(zip(row['mark_orbit_representatives'],row['mark_orbit_multiplicities'])):
        marked.append({'case_id':f"{row['tag']}_p{index:02d}",'support_tag':row['tag'],
                       'support_index':support_index,'I':row['I'],'full':row['full'],
                       'marked_cell_coordinates':pair,
                       'marked_original_coordinates':[[2*x,2*y] for x,y in pair],
                       'raw_pair_multiplicity':multiplicity})
(ROOT/'marked-cases.json').write_text(json.dumps({'support_file':'count.json','count':len(marked),'cases':marked},indent=2)+'\n')
with (ROOT/'supports.tsv').open('w',newline='') as fh:
    writer=csv.writer(fh,delimiter='\t')
    writer.writerow(['support','I','full_A_cells','b','P_plus_missing_cap','outside_cell_cap','allowed_A_cells',
                     'triangle_universe','raw_marked_pairs','marked_orbits','previous_k6_tag'])
    for r in rows:
        writer.writerow([r['tag'],r['I'],json.dumps(r['full'],separators=(',',':')),r['external_neighbors'],
                         r['partial_plus_missing_cap'],r['outside_cell_cap'],r['allowed_A_cells'],
                         r['canonical_triangle_universe'],r['marked_pairs_raw'],r['marked_pair_orbits'],r['previous_k6_tag']])
with (ROOT/'marked-cases.tsv').open('w',newline='') as fh:
    writer=csv.writer(fh,delimiter='\t')
    writer.writerow(['case','support','I','full_A_cells','actual_pair_original_coordinates','raw_pair_multiplicity'])
    for r in marked:
        writer.writerow([r['case_id'],r['support_tag'],r['I'],json.dumps(r['full'],separators=(',',':')),
                         json.dumps(r['marked_original_coordinates'],separators=(',',':')),r['raw_pair_multiplicity']])
print(json.dumps({k:v for k,v in out.items() if k not in ('cases','I2_connector_excluded_offsets','distance_eight_exclusions','I4_exclusions')},indent=2))
