"""Exact corner/interior switch between the two remaining tip fans."""
import json
from classify_illumination_three_exception import OUT,digest
from illumination_three_two_star_bound import complete_support
from illumination_family_bound import triangles_in_cells
from illumination_geometry import label,owners_of,local_sectors


def run():
    audit=json.loads((OUT/'hub7-residual-audit-1-1.json').read_text());assert audit['status']=='PASS'
    assert {c['tip_mask'] for c in audit['fan_cases'] if c['status']!='INFEASIBLE'}=={4,5}
    ts=triangles_in_cells(complete_support((1,1))['allowed']);hub=json.loads((OUT/'hub-analysis-1-1.json').read_text());fan=json.loads((OUT/'hub7-fans-1-1.json').read_text())
    fixed={i:1 for i,t in enumerate(ts) if (0,0) in t or (2,2) in t}
    for j,i in enumerate(hub['hub_triangle_ids']):
        value=(191>>j)&1;assert i not in fixed or fixed[i]==value;fixed[i]=value
    gate=(1,0);assert label(gate)!='A';incident=[i for i,t in enumerate(ts) if gate in t];assert len(incident)==4
    for i in incident:
        vectors=[(p[0]-gate[0],p[1]-gate[1]) for p in ts[i] if p!=gate]
        assert len(vectors)==2 and sum(vectors[0][k]*vectors[1][k] for k in (0,1))==0
    rows=[]
    for mask in [4,5]:
        facts=dict(fixed)
        for j,i in enumerate(fan['tip_triangle_ids']):
            v=(mask>>j)&1;assert i not in facts or facts[i]==v;facts[i]=v
        assert all(i in facts for i in incident)
        selected=[ts[i] for i in incident if facts[i]];os=owners_of(selected);opened={e for e,owners in os.items() if len(owners)==2}
        sizes,full=local_sectors(selected,gate,opened)
        assert (sizes,full)==(([6],False) if mask==4 else ([],True))
        rows.append(dict(tip_mask=mask,gate=gate,incident_triangle_indices=incident,incident_bits=[facts[i] for i in incident],
                         occupied_right_triangles=len(selected),angle_degrees=90*len(selected),interior=full,
                         exceptional_BC_vertex=full or 4 in sizes,
                         remaining_BC_exceptions=3-int(full or 4 in sizes)))
    result=dict(status='PASS',residual_audit_sha256=digest(OUT/'hub7-residual-audit-1-1.json'),cases=rows,
                scope='Exact implication of forced marked stars, hub191 and tip mask4/5. Every incident triangle at C(1,0) is fixed. No room enumeration, illumination claim or global exclusion.')
    (OUT/'tip-gate-1-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':run()
