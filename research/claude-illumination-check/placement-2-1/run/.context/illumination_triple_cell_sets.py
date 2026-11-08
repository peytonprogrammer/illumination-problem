"""Enumerate all connected outside-cell sets for the remaining k=3 supports.

P+m=b+outside<=10 gives outside<=10-b. Adding every missing mandatory cell
preserves connectivity because it touches a full root. Every outside component
can therefore be grown from the mandatory set, one adjacent cell at a time.
"""
from functools import lru_cache
import json
from pathlib import Path

from illumination_family_bound import NEIGHBORS
from illumination_three_two_star_bound import complete_support
from illumination_cell_path_bound import connected_cell_sets


def connected(cells):
    todo=[(0,0)]
    seen=set(todo)
    for x,y in todo:
        for dx,dy in NEIGHBORS:
            q=x+dx,y+dy
            if q in cells and q not in seen:
                seen.add(q)
                todo.append(q)
    return seen==cells


@lru_cache(maxsize=None)
def outside_sets(target):
    bounded=complete_support(target)
    required=frozenset(bounded['mandatory'])
    allowed=bounded['allowed']
    budget=bounded['extra_budget']
    layer={frozenset()}
    result=set()
    levels=[]
    for size in range(budget+1):
        accepted={tuple(sorted(s)) for s in layer if connected(required|s)}
        result.update(accepted)
        levels.append(dict(outside_cells=size,grown_sets=len(layer),connected_sets=len(accepted)))
        if size<budget:
            following=set()
            for chosen in layer:
                full=required|chosen
                for x,y in full:
                    for dx,dy in NEIGHBORS:
                        q=x+dx,y+dy
                        if q in allowed and q not in full:
                            following.add(chosen|{q})
            layer=following
    sets=tuple(sorted(result))
    if sum(target)>=3:
        assert set(sets)==set(connected_cell_sets(target))
    return sets,tuple((r['outside_cells'],r['grown_sets'],r['connected_sets']) for r in levels)


def refine_connected_cells(target,model,terms):
    receipt=Path(__file__).parent/'three-triples'/'connectivity-audit.json'
    assert json.loads(receipt.read_text())['status']=='PASS'
    if sum(target)==2:
        bounded=complete_support(target)
        outside=sorted(bounded['allowed']-bounded['mandatory'])
        rows=[[int(p in selected) for p in outside] for selected in outside_sets(target)[0]]
        model.add_allowed_assignments([terms['used'][2*a,2*b] for a,b in outside],rows)


if __name__=='__main__':
    rows=[]
    for target in [(1,1),(2,0),(2,1),(2,2)]:
        choices,levels=outside_sets(target)
        row=dict(target_A_cell=target,sets=len(choices),levels=levels,choices=choices)
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='choices'}),flush=True)
    out=Path(__file__).parent/'three-triples'/'connectivity-sets.json'
    out.write_text(json.dumps(dict(status='ENUMERATED',cases=rows,
        scope='Necessary connected outside-cell sets; near-target independent combinatorial verification pending.'),indent=2)+'\n')
