"""Necessary Q+m lower bounds from paths in the complete occupied-cell graph.

For I=2,k=3,W<=23,D>=3, b=8 mandatory partial cells and at most2
outside cells exist. Every connected room supplies a simple full-cell-to-full-cell
path in R plus at most2 outside cells. Every partial path cell has charge>=2,
or>=3 when entering and leaving through opposite sides. Missing mandatory
cells' unit charges are restored by m, so Q+m >= b + sum(path charges minus
one per mandatory path cell). This enumeration relaxes all other geometry.
"""
from itertools import combinations
from functools import lru_cache
import json
from pathlib import Path
from illumination_geometry import owners_of,check_fan_angles
from illumination_family_bound import NEIGHBORS,triangles_in_cells
from illumination_three_two_star_bound import TARGETS,complete_support

BASE=Path(__file__).parent


def fan_charge_check():
    ts=triangles_in_cells({(0,0)});checked=pairs=0
    for mask in range(1,255):
        selected=[t for i,t in enumerate(ts) if mask>>i&1];owners=owners_of(selected)
        angles,full=check_fan_angles(selected,(0,0),owners,{e for e,ids in owners.items() if len(ids)==2})
        if len(angles)!=1:continue
        Q=3 if angles==[4] else angles[0]
        sides={(axis,value) for t in selected for axis in (0,1) for value in (-1,1) if sum(p[axis]==value for p in t)==2}
        for a,b in combinations(sides,2):
            opposite=a[0]==b[0] and a[1]==-b[1]
            assert Q>=2+int(opposite),(mask,Q,a,b)
            pairs+=1
        checked+=1
    assert checked==56
    return dict(partial_fans_checked=checked,side_pair_checks=pairs)


def path_charge_lower_bound(target):
    assert tuple(target) in TARGETS and sum(target)>=3
    # The finite enumeration below independently checks this closed form for
    # every complete target support to which the model applies it.
    return 2*sum(target)+4+max(0,target[0]-target[1]-1)



@lru_cache(maxsize=None)
def connected_cell_sets(target):
    """All possible outside-cell sets in the necessary coordinate graph.

    Adding every mandatory cell to an actual connected occupied-cell graph
    preserves connectivity: every added mandatory cell is adjacent to a full
    root. Hence R plus the actual outside set is connected, with <=2 outside.
    """
    assert tuple(target) in TARGETS and sum(target)>=3
    bounded=complete_support(target);required=bounded['mandatory']
    outside=sorted(bounded['allowed']-required);result=[]
    for n in range(3):
        for added in combinations(outside,n):
            allowed=required|set(added);seen={(0,0)};todo=[(0,0)]
            for p in todo:
                for dx,dy in NEIGHBORS:
                    q=(p[0]+dx,p[1]+dy)
                    if q in allowed and q not in seen:seen.add(q);todo.append(q)
            if seen==allowed:result.append(added)
    assert result
    return tuple(result)


def enumerate_paths(target):
    bounded=complete_support(target);required=bounded['mandatory'];source=(0,0);target=tuple(target)
    outside=sorted(bounded['allowed']-required);b=len(required-bounded['full']);assert b==8
    minimum=10**6;configurations=connected=paths=0;example=None
    for n in range(3):
        for added in combinations(outside,n):
            configurations+=1;allowed=required|set(added)
            adjacency={p:[(p[0]+dx,p[1]+dy) for dx,dy in NEIGHBORS if (p[0]+dx,p[1]+dy) in allowed] for p in allowed}
            seen={source};todo=[source]
            for p in todo:
                for q in adjacency[p]:
                    if q not in seen:seen.add(q);todo.append(q)
            if target not in seen:continue
            connected+=1
            def walk(path,cost):
                nonlocal minimum,paths,example
                p=path[-1]
                if p==target:
                    paths+=1
                    if b+cost<minimum:minimum=b+cost;example=path
                    return
                for q in adjacency[p]:
                    if q in path:continue
                    extra=0
                    if len(path)>1:
                        previous=path[-2]
                        straight=(p[0]-previous[0],p[1]-previous[1])==(q[0]-p[0],q[1]-p[1])
                        extra=2+int(straight)-int(p in required)
                    walk(path+[q],cost+extra)
            walk([source],0)
    assert minimum==path_charge_lower_bound(target),(target,minimum)
    return dict(target_A_cell=target,abstract_cell_sets_checked=configurations,connecting_cell_sets=connected,
                simple_paths_checked=paths,minimum_Q_plus_missing=minimum,wall_lower_bound=8+minimum,
                minimizing_path=example,connected_outside_cell_sets=connected_cell_sets(target))


if __name__=='__main__':
    fan=fan_charge_check();results=[enumerate_paths(t) for t in TARGETS if sum(t)>=3]
    data=dict(status='PASS',local_fan_check=fan,cases=results,
              proof_scope='Necessary cell-path charge bound for complete I=2,k=3,W<=23 supports. Missing mandatory cells are allowed by taking all of R as a relaxation; all outside subsets of size<=2 and every simple connecting path are enumerated.')
    (BASE/'three-two-star'/'path-charge-bound.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data))
