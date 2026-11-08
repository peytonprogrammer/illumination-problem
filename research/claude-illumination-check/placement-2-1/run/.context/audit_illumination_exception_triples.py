"""Check projected witnesses, exact ray guards, class claims and complements."""
import argparse
from itertools import combinations
import json

from ortools.sat.python import cp_model
from audit_illumination_exception_pairs import independent_pair, independent_orbit
from audit_illumination_three_two_star import touched_tiles
from classify_illumination_three_exception import (
    OUT, REMAINING, block_triple, digest, model_with_audited_cuts, solver_for,
)
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from illumination_three_two_star_bound import complete_support
from illumination_family_bound import NEIGHBORS
from illumination_triple_cell_sets import outside_sets, refine_connected_cells
from search_illumination_one_exception import tile_facts
from search_illumination_three_two_star import add_guard, fix_triple


def audit_connectivity():
    cases=[]
    for target in REMAINING:
        bounded=complete_support(target)
        required=bounded['mandatory']
        outside=sorted(bounded['allowed']-required)
        actual=set()
        checked=0
        for size in range(bounded['extra_budget']+1):
            for added in combinations(outside,size):
                checked+=1
                cells=required|set(added)
                seen={(0,0)}
                frontier=set(seen)
                while frontier:
                    following={(x+dx,y+dy) for x,y in frontier for dx,dy in NEIGHBORS}
                    following=(following&cells)-seen
                    seen|=following
                    frontier=following
                if seen==cells:actual.add(added)
        assert actual==set(outside_sets(target)[0])
        cases.append(dict(target_A_cell=target,subsets_checked=checked,connected_sets=len(actual)))
        print(json.dumps(cases[-1]),flush=True)
    result=dict(status='PASS',cases=cases,
                scope='Independent complete subset enumeration agrees with frontier growth, including the two nearby supports with three/four outside cells.')
    (OUT/'connectivity-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def audit_case(target,connected_cells=False):
    projection_path=OUT/f'projection-{target[0]}-{target[1]}.json'
    prefix='connected-search' if connected_cells else 'search'
    search_path=OUT/f'{prefix}-{target[0]}-{target[1]}.json'
    projection,saved=(json.loads(p.read_text()) for p in (projection_path,search_path))
    model,ts,x,_,terms,provenance,seed_keys=model_with_audited_cuts(target)
    if connected_cells:
        refine_connected_cells(target,model,terms)
        assert saved['summary']['connectivity_audit_sha256']==digest(OUT/'connectivity-audit.json')
    assert projection['summary']['provenance']==saved['summary']['provenance']==provenance
    assert saved['summary']['projection_sha256']==digest(projection_path)
    coverage=model.clone()
    solver=solver_for(20,41)
    keys=set()
    for number,group in enumerate(projection['classes'],1):
        room=group['witness_room']
        validate(room,target)
        triple=independent_pair(room)
        assert len(triple)==3 and triple==tuple(map(tuple,group['triple']))
        orbit=independent_orbit(target,triple)
        assert orbit==tuple(tuple(map(tuple,t)) for t in group['orbit'])
        canonical=min(orbit)
        assert canonical==tuple(map(tuple,group['canonical'])) and canonical not in keys
        keys.add(canonical)
        selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
        fixed=model.clone()
        for t,v in zip(ts,x):fixed.add(v==int(t in selected))
        assert solver.solve(fixed)==cp_model.OPTIMAL
        for other in orbit:block_triple(coverage,terms,other)
        if number%20==0:
            print(json.dumps(dict(event='positive_projection_models',target=target,checked=number)),flush=True)
    owners=owners_of(ts)
    seen=set(seed_keys)
    room_keys=set()
    rays=mutations=corruptions=0
    max_bounces=0
    for number,record in enumerate(saved['records'],1):
        room=record['room']
        validate(room,target)
        verify(room,record['witness'])
        room_key=tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))
        assert room_key not in room_keys
        room_keys.add(room_key)
        canonical=min(independent_orbit(target,independent_pair(room)))
        assert canonical==tuple(map(tuple,record['canonical_exception_triple'])) and canonical in keys
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
                flipped=dict(fixed);flipped[i]=1-flipped[i]
                assert any(flipped[i]!=int(ts[i] in selected) for i in required)
                corruptions+=2
            if mutations<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                    verify(dict(guard['room'],triangles=sorted(selected^{ts[i]})),guard['witness'])
                    mutations+=1
            add_guard(model,x,facts)
            add_guard(coverage,x,facts)
            rays+=1
        if number%25==0:
            print(json.dumps(dict(event='new_ray_audit',target=target,records=number,rays=rays)),flush=True)
    assert rays==saved['summary']['additional_cuts']==len(seen)-len(seed_keys)
    additional=projection['summary'].get('additional_ray_source')
    if additional:
        from classify_illumination_three_exception import BASE
        source=BASE/additional['file']
        assert digest(source)==additional['sha256']
        learned=json.loads(source.read_text())
        assert learned['summary']['provenance']==provenance
        assert all(tuple(map(tuple,g['tile_facts'])) in seen
                   for r in learned['records'] for g in r['derived_guards'])
    solver.parameters.max_time_in_seconds=60
    coverage_status=solver.solve(coverage)
    if projection['summary']['complete']:
        assert coverage_status==cp_model.INFEASIBLE
    claims={tuple(map(tuple,c['canonical'])):c for c in saved['classes']}
    assert claims.keys()<=keys
    replayed=[]
    for group in projection['classes']:
        canonical=tuple(map(tuple,group['canonical']))
        claim=claims.get(canonical)
        # Replay every claimed exclusion. Open branches need no solver claim.
        if not claim or not claim['exhausted']:
            replayed.append(dict(canonical=canonical,status='UNRESOLVED'))
            continue
        branch=model.clone()
        fix_triple(branch,terms,tuple(map(tuple,group['triple'])))
        status=solver.solve(branch)
        assert status==cp_model.INFEASIBLE
        replayed.append(dict(canonical=canonical,status=solver.status_name(status)))
    solver.parameters.max_time_in_seconds=60
    global_status=solver.solve(model)
    if saved['summary']['exhausted']:
        assert global_status==cp_model.INFEASIBLE
    excluded=global_status==cp_model.INFEASIBLE or (
        coverage_status==cp_model.INFEASIBLE and all(r['status']=='INFEASIBLE' for r in replayed))
    result=dict(target_A_cell=target,status='PASS',projected_classes=len(projection['classes']),
                projection_complete=projection['summary']['complete'],coverage_replay=solver.status_name(coverage_status),
                positive_fixed_models=len(projection['classes']),records=len(saved['records']),exact_new_guards=rays,
                independent_closed_triangle_checks=rays,mutation_checks=mutations,corrupt_guard_checks=corruptions,
                max_new_reflections=max_bounces,classes=replayed,
                classes_excluded=sum(r['status']=='INFEASIBLE' for r in replayed),
                global_replay=solver.status_name(global_status),excluded=excluded,
                source_sha256=digest(search_path),projection_sha256=digest(projection_path),provenance=provenance)
    print(json.dumps({k:v for k,v in result.items() if k!='classes'}),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--target',type=int,nargs=2)
    ap.add_argument('--connectivity-only',action='store_true')
    ap.add_argument('--connected-cells',action='store_true')
    args=ap.parse_args()
    if args.connectivity_only:
        audit_connectivity()
        raise SystemExit(0)
    cases=[audit_case(t,args.connected_cells) for t in ([tuple(args.target)] if args.target else REMAINING)]
    result=dict(status='PASS',cases=cases,
                scope='New triple-classification and positive-ray audit; incomplete projections and open classes remain unresolved. Earlier guards are covered by their immutable audit.')
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
