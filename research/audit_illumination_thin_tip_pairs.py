"""Check projected thin-tip pairs, explicit remainder, and the fixed local exception."""
from itertools import combinations,product
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from project_illumination_thin_tip_pairs import PATH,GATE,load_base,block_pair,fix_pair,TARGET
from illumination_geometry import label,owners_of,local_sectors
from illumination_three_two_star_bound import validate
from search_illumination_three_two_star import typed_exceptions,room_from


def run():
    saved=json.loads(PATH.read_text());model,ts,x,bounded,terms,keys,ids,seeds,fans,prov=load_base();assert saved['provenance']==prov
    pairs=set();positions=set();solver=solver_for(15,401);solver.parameters.cp_model_presolve=False;controls=0
    for r in saved['classes']:
        pair=tuple(map(tuple,r['pair']));assert pair==tuple(sorted(pair)) and len(pair)==2 and pair not in pairs;pairs.add(pair)
        assert len({p[:2] for p in pair})==2 and all(p[:2]!=GATE[:2] and p[2] in [1,2] for p in pair)
        room=r['positive_room'];validate(room,TARGET);assert typed_exceptions(room)==tuple(sorted(pair+(GATE,)))
        selected={tuple(sorted(map(tuple,t))) for t in room['triangles']};assert selected<=set(ts)
        assert sum(1<<j for j,i in enumerate(ids) if ts[i] in selected)==191
        assert sum(1<<j for j,i in enumerate(fans['tip_triangle_ids']) if ts[i] in selected)==4
        assert all(not all(int(ts[i] in selected)==v for i,v in key) for key in keys)
        if controls<3:
            branch=model.clone();fix_pair(branch,terms,pair)
            for t,v in zip(ts,x):branch.add(v==int(t in selected))
            assert solver.solve(branch) in (cp_model.OPTIMAL,cp_model.FEASIBLE);controls+=1
        positions.update(p[:2] for p in pair)
    # Independently test disjointness/complement over every assignment of two
    # typed positions, with two symbolic outside positions covering all unlisted ones.
    domain=sorted(positions)+[('outside',0),('outside',1)];assignments=0
    for a,b in combinations(domain,2):
        for u,v in product([1,2],repeat=2):
            values={a:u,b:v};hits=sum(all(values.get(p[:2],0)==p[2] for p in pair) for pair in pairs)
            assert hits in [0,1];residual=all(not all(values.get(p[:2],0)==p[2] for p in pair) for pair in pairs)
            assert hits+int(residual)==1;assignments+=1
    remainder=model.clone()
    for pair in pairs:block_pair(remainder,terms,pair)
    solver.parameters.max_time_in_seconds=60;status=solver.solve(remainder);residual_status=solver.status_name(status)
    if saved['summary']['projection_complete']:assert status==cp_model.INFEASIBLE
    remaining_room=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    remaining_pair=[p for p in typed_exceptions(remaining_room) if p!=GATE] if remaining_room else None
    if remaining_pair:assert tuple(remaining_pair) not in pairs
    # Derive every fully fixed local non-A vertex directly from tile facts.
    fixed={i:1 for i,t in enumerate(ts) if (0,0) in t or (2,2) in t}
    for indices,mask in [(ids,191),(fans['tip_triangle_ids'],4)]:
        for j,i in enumerate(indices):
            value=(mask>>j)&1;assert i not in fixed or fixed[i]==value;fixed[i]=value
    local=[]
    for p in sorted({p for t in ts for p in t if label(p)!='A'}):
        incident=[i for i,t in enumerate(ts) if p in t]
        if not all(i in fixed for i in incident):continue
        selected=[ts[i] for i in incident if fixed[i]]
        if not selected:continue
        os=owners_of(selected);opened={e for e,own in os.items() if len(own)==2};sizes,full=local_sectors(selected,p,opened)
        assert len(sizes)<=1
        defect=2 if full else 1 if sizes==[4] else 0
        if defect:local.append(dict(point=p,type=defect,incident_indices=incident,incident_bits=[fixed[i] for i in incident]))
    forced=tuple(sorted((*r['point'],r['type']) for r in local));assert forced==((2,1,1),)
    free_pairs=sorted(pairs)
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=prov,listed_pairs=len(pairs),positive_models=controls,
                logical_partition_assignments=assignments,partition_including_remainder_complete=True,residual_status=residual_status,
                pair_projection_complete=residual_status=='INFEASIBLE',source_projection_complete=saved['summary']['projection_complete'],unlisted_pair_witness=remaining_pair,unlisted_room_witness=remaining_room,
                forced_local_exceptions=local,free_exception_pairs=free_pairs,base_guards=len(keys),
                placement_excluded=False,scope='Complete pair projection only if residual INFEASIBLE. Each listed pair has a valid physical room satisfying all guards; such rooms are not dark claims. The fixed smooth exception independently follows from fixed local tiles. No new illumination cuts or placement exclusion.')
    (OUT/'thin-tip-pairs-audit-1-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['provenance','unlisted_room_witness','free_exception_pairs']}),flush=True)


if __name__=='__main__':run()
