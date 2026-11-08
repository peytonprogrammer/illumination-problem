"""Necessary complete shape bounds for exactly three full A stars and <=3 exceptions.

For W<=23: I>=4 is excluded by W>=6+6I-2k. At I=3, Q<=3+E.
With P partial cells and m absent required neighbors, connectivity gives
Q>=2P-8+m and E+m<=2k<=6. Thus P+m<=8. The external full-star
neighborhood has b<=8 cells; all occupied cells lie within radius8-b of it.
This is a necessary finite reduction, not a geometric or darkness exclusion.
"""
import itertools
import json
from pathlib import Path
from illumination_family_bound import NEIGHBORS
from illumination_two_exception_bound import canonical

BASE = Path(__file__).parent


def shapes():
    diamond = [(x,y) for x in range(-4,5) for y in range(-4,5) if 0<abs(x)+abs(y)<=4]
    found = {}
    checked = 0
    for a,b in itertools.combinations(diamond,2):
        full = {(0,0),a,b}
        reached,todo = {(0,0)},[(0,0)]
        for p in todo:
            for q in full-reached:
                if abs(p[0]-q[0])+abs(p[1]-q[1])<=2:
                    reached.add(q);todo.append(q)
        if reached!=full:
            continue
        checked+=1
        external={(x+dx,y+dy) for x,y in full for dx,dy in NEIGHBORS}-full
        assert len(external)>=7
        if len(external)>8:
            continue
        normalized=canonical(full)
        full=set(normalized)
        external={(x+dx,y+dy) for x,y in full for dx,dy in NEIGHBORS}-full
        b=len(external);allowed=full|external
        for _ in range(8-b):
            allowed|={(x+dx,y+dy) for x,y in allowed for dx,dy in NEIGHBORS}
        pairs=[(p,q) for p,q in itertools.combinations(normalized,2) if abs(p[0]-q[0])+abs(p[1]-q[1])>1]
        found[normalized]=dict(full_A_cells=normalized,external_neighbor_count=b,
                               outside_cell_budget=8-b,allowed_A_cells=sorted(allowed),
                               nonadjacent_mark_pairs=pairs)
    return dict(status='NECESSARY_BOUND_ONLY',overlap_connected_rooted_patterns_checked=checked,
                maximum_triangles=36,maximum_partial_plus_missing=8,
                normalized_three_star_shapes=len(found),
                shapes=[found[k] for k in sorted(found)],
                scope='I=3 branch with at most3 B/C exceptions and at most23 walls. I=2 not covered. No room feasibility, illumination or darkness conclusion.')


if __name__=='__main__':
    result=shapes()
    (BASE/'three-star-shapes.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='shapes'}))
    for shape in result['shapes']:
        print(json.dumps(dict(full_A_cells=shape['full_A_cells'],external_neighbors=shape['external_neighbor_count'],
                              allowed_A_cells=len(shape['allowed_A_cells']),mark_pairs=len(shape['nonadjacent_mark_pairs']))))
