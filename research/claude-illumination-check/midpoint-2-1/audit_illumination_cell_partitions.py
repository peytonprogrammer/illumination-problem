"""Audit new cell-partition rays and replay every claimed outside-set exclusion."""
import argparse
import json

from ortools.sat.python import cp_model
from audit_illumination_three_two_star import touched_tiles
from classify_illumination_three_exception import OUT, digest, solver_for
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from search_illumination_cell_partitions import fix_cells, load_parent, room_outside
from search_illumination_one_exception import tile_facts
from search_illumination_three_two_star import add_guard


def audit(target):
    path=OUT/f'cell-search-{target[0]}-{target[1]}.json'
    saved=json.loads(path.read_text())
    prior_audit=json.loads((OUT/'audit.json').read_text())
    assert prior_audit['status']=='PASS'
    model,ts,x,bounded,terms,provenance,seed_keys,choices=load_parent(target)
    assert saved['summary']['provenance']==provenance
    receipt=next(c for c in prior_audit['cases'] if c['target_A_cell']==list(target))
    assert receipt['source_sha256']==provenance['bootstrap_sha256']
    owners=owners_of(ts)
    seen=set(seed_keys)
    rooms=set()
    rays=mutations=corruptions=0
    max_bounces=0
    for number,record in enumerate(saved['records'],1):
        room=record['room']
        validate(room,target)
        verify(room,record['witness'])
        chosen=room_outside(room,target)
        assert chosen in choices and chosen==tuple(map(tuple,record['outside_cells']))
        key=tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))
        assert key not in rooms
        rooms.add(key)
        max_bounces=max(max_bounces,record['witness']['bounces'])
        for guard in record['derived_guards']:
            verify(guard['room'],guard['witness'])
            facts=tile_facts(ts,owners,guard['witness'],guard['room'])
            assert facts==list(map(tuple,guard['tile_facts']))
            key=tuple(facts)
            assert key not in seen
            seen.add(key)
            required=touched_tiles(ts,guard['witness'])
            fixed=dict(facts)
            selected={tuple(sorted(map(tuple,t))) for t in guard['room']['triangles']}
            assert required<=fixed.keys()
            assert all(fixed[i]==int(ts[i] in selected) for i in required)
            if corruptions<8:
                i=next(iter(required));removed=dict(fixed);del removed[i]
                assert not required<=removed.keys()
                changed=dict(fixed);changed[i]=1-changed[i]
                assert any(changed[i]!=int(ts[i] in selected) for i in required)
                corruptions+=2
            if mutations<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                    verify(dict(guard['room'],triangles=sorted(selected^{ts[i]})),guard['witness'])
                    mutations+=1
            add_guard(model,x,facts)
            rays+=1
        if number%25==0:
            print(json.dumps(dict(event='cell_ray_audit',records=number,rays=rays)),flush=True)
    assert rays==saved['summary']['new_guards']==len(seen)-len(seed_keys)
    claims={tuple(map(tuple,c['outside_cells'])):c for c in saved['classes']}
    assert len(claims)==len(saved['classes']) and claims.keys()<=set(choices)
    replays=[]
    solver=solver_for(30,83)
    for chosen in choices:
        claim=claims.get(chosen)
        branch=model.clone()
        fix_cells(branch,terms,bounded,chosen)
        solver.parameters.max_time_in_seconds=30 if claim and claim['exhausted'] else 20
        status=solver.solve(branch)
        if claim and claim['exhausted']:
            assert status==cp_model.INFEASIBLE
        replays.append(dict(outside_cells=chosen,status=solver.status_name(status)))
        if len(replays)%20==0:
            print(json.dumps(dict(event='cell_model_audit',checked=len(replays),
                                  excluded=sum(r['status']=='INFEASIBLE' for r in replays))),flush=True)
    solver.parameters.max_time_in_seconds=90
    global_status=solver.solve(model)
    excluded=global_status==cp_model.INFEASIBLE or all(r['status']=='INFEASIBLE' for r in replays)
    if saved['summary']['excluded']:assert excluded
    result=dict(status='PASS',target_A_cell=target,complete_partition_size=len(choices),
                replayed_all_cells=True,unclaimed_branch_seconds=20,
                classes_excluded=sum(r['status']=='INFEASIBLE' for r in replays),classes=replays,
                global_replay=solver.status_name(global_status),excluded=excluded,
                new_records=len(saved['records']),exact_new_guards=rays,
                independent_closed_triangle_checks=rays,mutation_checks=mutations,corrupt_guard_checks=corruptions,
                max_new_reflections=max_bounces,source_sha256=digest(path),provenance=provenance,
                scope='Complete connected outside-cell necessary partition; each claimed negative branch replayed, new positive rays independently checked, earlier guard audit referenced by hash. No formal UNSAT proof.')
    (OUT/f'cell-audit-{target[0]}-{target[1]}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='classes'}),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--target',type=int,nargs=2,required=True)
    args=ap.parse_args()
    audit(tuple(args.target))
