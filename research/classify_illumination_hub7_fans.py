"""Independent finite fan refinement at the tip of the absent hub triangle."""
import json
from classify_illumination_three_exception import BASE,OUT,digest
from illumination_three_two_star_bound import complete_support
from illumination_family_bound import triangles_in_cells
from illumination_geometry import label,owners_of,local_sectors
from search_illumination_fan_partitions import fan_masks


def run():
    manifest=json.loads((OUT/'midpoint-proof-inputs-1-1.json').read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    hub=json.loads((OUT/'hub-analysis-1-1.json').read_text());assert hub['status']=='PASS'
    ts=triangles_in_cells(complete_support((1,1))['allowed']);ids=hub['hub_triangle_ids'];mask=191
    absent=[i for j,i in enumerate(ids) if not(mask>>j&1)];assert len(absent)==1
    vertex=next(p for p in ts[absent[0]] if label(p)=='A');assert vertex not in [(0,0),(2,2)]
    first,all_masks=fan_masks(ts,tuple(v//2 for v in vertex));assert len(first)==8
    fixed={j:int(mask>>ids.index(i)&1) for j,i in enumerate(first) if i in ids}
    assert sorted(fixed.values())==[0,1]
    candidates=[m for m in all_masks if all((m>>j&1)==v for j,v in fixed.items())]
    # Independent graph traversal, including an explicit rejection of a full A star.
    adjacency={j:set() for j in range(8)}
    for edge,os in owners_of([ts[i] for i in first]).items():
        if vertex in edge and len(os)==2:a,b=os;adjacency[a].add(b);adjacency[b].add(a)
    assert all(len(v)==2 for v in adjacency.values());independent=[]
    for m in range(255):
        if not all((m>>j&1)==v for j,v in fixed.items()):continue
        selected={j for j in range(8) if m>>j&1};seen={min(selected)};todo=list(seen)
        for j in todo:
            for k in adjacency[j]&selected-seen:seen.add(k);todo.append(k)
        if seen==selected:independent.append(m)
    assert candidates==independent and len(candidates)==7
    result=dict(status='PASS',hub_audit_sha256=digest(OUT/'hub-analysis-1-1.json'),hub_mask=mask,
                missing_hub_triangle_index=absent[0],tip_vertex=vertex,tip_cell=[v//2 for v in vertex],
                tip_triangle_ids=first,fixed_tip_bits=sorted(fixed.items()),complete_partial_star_fan_masks=all_masks,
                compatible_fan_masks=candidates,fan_triangles={str(m):m.bit_count() for m in candidates},
                scope='Complete necessary seven-way fan partition for canonical hub191. Local cyclic adjacency independently checks geometric sectors. No solver run, ray discovery or illumination/exclusion claim.')
    (OUT/'hub7-fans-1-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='complete_partial_star_fan_masks'}),flush=True)


if __name__=='__main__':run()
