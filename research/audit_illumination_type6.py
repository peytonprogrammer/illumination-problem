"""Fresh path checks and separate geometry-only/composed implications for type6."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from search_illumination_type6 import PATH,load_base
from search_illumination_midpoint_covers import TARGET,geometry_parent,fixed_neck,one_pass
from search_illumination_three_two_star import add_guard,room_from
from search_illumination_cell_partitions import fix_cells
from search_illumination_one_exception import tile_facts
from audit_illumination_midpoint_covers import signature
from audit_illumination_three_two_star import touched_tiles
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate


def run():
    saved=json.loads(PATH.read_text())
    model,ts,x,bounded,terms,first,second,patterns,keys,midpoint_guards,provenance=load_base()
    assert saved['provenance']==provenance and saved['pattern']==patterns[5]
    bare,bts,bx,bb,bt,bf,bs,bp=geometry_parent();assert bts==ts
    control=next(g['room'] for g in midpoint_guards if signature(g['room'],ts,first,second,bounded)==(tuple(map(tuple,patterns[5][0])),patterns[5][1],patterns[5][2]))
    positive=bare.clone();fixed_neck(positive,bt,bb,bx,bf,bs,bp[5]);selected={tuple(sorted(map(tuple,t))) for t in control['triangles']}
    for t,v in zip(ts,bx):positive.add(v==int(t in selected))
    solver=solver_for(60,269);solver.parameters.cp_model_presolve=False
    assert solver.solve(positive) in (cp_model.OPTIMAL,cp_model.FEASIBLE)
    for g in midpoint_guards:add_guard(bare,bx,g['tile_facts'])
    owners=owners_of(ts);rooms=set();mutations=corruptions=0;max_bounces=0;before=len(keys)
    for n,r in enumerate(saved['records'],1):
        room=r['room'];validate(room,TARGET);one_pass(room,r['witness'])
        assert signature(room,ts,first,second,bounded)==(tuple(map(tuple,patterns[5][0])),patterns[5][1],patterns[5][2])
        room_key=tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))
        assert room_key not in rooms;rooms.add(room_key)
        for g in r['derived_guards']:
            data,witness=g['room'],g['witness'];validate(data,TARGET);one_pass(data,witness)
            facts=tile_facts(ts,owners,witness,data);assert facts==list(map(tuple,g['tile_facts']))
            key=tuple(facts);assert key not in keys;keys.add(key)
            fixed=dict(facts);required=touched_tiles(ts,witness);selected={tuple(sorted(map(tuple,t))) for t in data['triangles']}
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
            if corruptions<8:
                i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
                flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in selected);corruptions+=2
            if mutations<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                    verify(dict(data,triangles=sorted(selected^{ts[i]})),witness);mutations+=1
            add_guard(model,x,facts);add_guard(bare,bx,facts);max_bounces=max(max_bounces,witness['bounces'])
        if n%50==0:print(json.dumps(dict(event='type6_ray_audit',records=n,guards=len(keys)-before)),flush=True)
    assert len(keys)-before==saved['summary']['new_guards']
    fixed_neck(bare,bt,bb,bx,bf,bs,bp[5]);status=solver.solve(bare)
    universal=solver.status_name(status);cases=[]
    print(json.dumps(dict(geometry_only_type6=universal)),flush=True)
    for number in [1,2,3,4,5,6,7,8,9,10,11,12]:
        branch=model.clone();fixed_neck(branch,terms,bounded,x,first,second,patterns[number-1])
        solver.parameters.max_time_in_seconds=60 if number==6 else 10;status=solver.solve(branch)
        if number==6 and saved['summary']['exhausted']:assert status==cp_model.INFEASIBLE
        cases.append(dict(neck_type=number,status=solver.status_name(status)))
        print(json.dumps(cases[-1]),flush=True)
    outside=[]
    for cells in [[],[[1,-1]],[[1,2]]]:
        branch=model.clone();fix_cells(branch,terms,bounded,cells);solver.parameters.max_time_in_seconds=60 if cells else 10
        status=solver.solve(branch);outside.append(dict(outside_cells=cells,status=solver.status_name(status)))
    solver.parameters.max_time_in_seconds=30;status=solver.solve(model)
    parent_status=solver.status_name(status)
    survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    mapping={t:i for i,t in enumerate(ts)};perm=[mapping[tuple(sorted((4-p[0],2-p[1]) for p in t))] for t in ts]
    assert all(tuple(sorted((perm[i],v) for i,v in key)) in keys for key in keys)
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=provenance,positive_type6_control='ACCEPTED',new_records=len(rooms),
                new_guards=len(keys)-before,total_guards=len(keys),mutations=mutations,corrupt_guards=corruptions,max_reflections=max_bounces,
                geometry_only_type6=universal,cases=cases,outside_cases=outside,unrestricted_parent=parent_status,survivor=survivor,
                half_turn_closed=True,canonical_types_excluded=sum(c['status']=='INFEASIBLE' for c in cases),
                cumulative_outside_sets_excluded=102+sum(c['status']=='INFEASIBLE' for c in outside),
                scope='Separate geometry-only midpoint implication and composed historical-ray exclusions. Finite misses/caps unresolved.')
    (OUT/'type6-audit-2-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','outside_cases','survivor','provenance']}),flush=True)


if __name__=='__main__':run()
