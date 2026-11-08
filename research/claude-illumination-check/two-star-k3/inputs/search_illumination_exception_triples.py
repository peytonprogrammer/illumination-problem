"""Search fixed typed exception triples; retain every cap and finite ray miss."""
import argparse
import json
import time

from ortools.sat.python import cp_model
from classify_illumination_three_exception import (
    OUT, REMAINING, digest, model_with_audited_cuts, solver_for, fix_triple,
    room_from, triple_orbit, typed_exceptions,
)
from illumination_geometry import owners_of
from illumination_paths import find_path
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from search_illumination_one_exception import orbit, tile_facts
from search_illumination_three_two_star import add_guard
from illumination_triple_cell_sets import refine_connected_cells


def run(target, seconds_per_class=5, total_seconds=300, final_seconds=45, connected_cells=False):
    started=time.monotonic()
    projection_path=OUT/f'projection-{target[0]}-{target[1]}.json'
    projection=json.loads(projection_path.read_text())
    model,ts,x,_,terms,provenance,seed_keys=model_with_audited_cuts(target)
    if connected_cells:
        refine_connected_cells(target,model,terms)
    assert projection['summary']['provenance']==provenance
    projection_hash=digest(projection_path)
    prefix='connected-search' if connected_cells else 'search'
    path=OUT/f'{prefix}-{target[0]}-{target[1]}.json'
    bootstrap=OUT/f'search-{target[0]}-{target[1]}.json'
    prior_path=path if path.exists() else bootstrap if connected_cells and bootstrap.exists() else None
    previous=json.loads(prior_path.read_text()) if prior_path else None
    bootstrap_hash=digest(prior_path) if prior_path and prior_path!=path else None
    records=previous['records'] if previous else []
    if previous:
        assert previous['summary']['provenance']==provenance
        if previous['summary']['exhausted'] and prior_path==path:
            print(json.dumps(dict(event='reuse_search',**previous['summary'])),flush=True)
            return previous['summary']
    owners=owners_of(ts)
    seen=set(seed_keys)
    for record in records:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']))
            assert key not in seen
            seen.add(key)
            add_guard(model,x,guard['tile_facts'])
    prior={tuple(map(tuple,o['canonical'])):o for o in previous['classes']} if previous else {}
    outcomes=[]
    status=None
    solver=solver_for(seconds_per_class,29)
    initial=len(records)
    reason='all_listed_classes_visited'
    begin=time.monotonic()
    def save():
        visited={tuple(map(tuple,o['canonical'])) for o in outcomes}
        retained=outcomes+[o for k,o in prior.items() if k not in visited]
        summary=dict(target_A_cell=target,projection_complete=projection['summary']['complete'],
                     projected_classes=len(projection['classes']),classes_searched=len(retained),
                     classes_excluded=sum(o['exhausted'] for o in retained),
                     records=len(records),new_records=len(records)-initial,additional_cuts=len(seen)-len(seed_keys),
                     global_solver_status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                     exhausted=status==cp_model.INFEASIBLE,stop_reason=reason,seconds=time.monotonic()-started,
                     provenance=provenance,projection_sha256=projection_hash,
                     connected_cells=connected_cells,
                     connectivity_audit_sha256=digest(OUT/'connectivity-audit.json') if connected_cells else None,
                     bootstrap_sha256=bootstrap_hash,
                     scope='Necessary parent plus audited seed guards and exact new positive-ray guards only. Fixed triples guide discovery; projection caps remain unresolved.')
        temp=path.with_suffix('.tmp')
        temp.write_text(json.dumps(dict(summary=summary,classes=retained,records=records),indent=2)+'\n')
        temp.replace(path)
        return summary
    for group in projection['classes']:
        canonical=tuple(map(tuple,group['canonical']))
        if canonical in prior and prior[canonical]['exhausted']:
            outcomes.append(prior[canonical])
            continue
        remaining=total_seconds-(time.monotonic()-begin)
        if remaining<=0:
            reason='total_time_limit'
            break
        triple=tuple(map(tuple,group['triple']))
        branch=model.clone()
        fix_triple(branch,terms,triple)
        branch_started=time.monotonic()
        allowance=min(seconds_per_class,remaining)
        branch_status=None
        stop='time_limit'
        survivor=None
        count_before=len(records)
        while time.monotonic()-branch_started<allowance:
            solver.parameters.max_time_in_seconds=max(.001,allowance-(time.monotonic()-branch_started))
            branch_status=solver.solve(branch)
            if branch_status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
                stop='exhausted' if branch_status==cp_model.INFEASIBLE else 'solver_unknown'
                break
            room=room_from(target,ts,x,solver)
            assert typed_exceptions(room)==triple
            witness=find_path(room,16,1000)
            if witness['status']!='illuminated':
                witness=find_path(room,32,2000)
            if witness['status']!='illuminated':
                stop='unresolved_candidate'
                survivor=dict(room=room,bounded_screen=witness)
                break
            verify(room,witness)
            guards=[]
            for changed,ray in orbit(room,witness):
                verify(changed,ray)
                facts=tile_facts(ts,owners,ray,changed)
                key=tuple(facts)
                if key in seen:
                    continue
                seen.add(key)
                guards.append(dict(room=changed,witness=ray,tile_facts=facts))
                add_guard(model,x,facts)
                add_guard(branch,x,facts)
            assert guards
            records.append(dict(room=room,witness=witness,counts=validate(room,target),
                                canonical_exception_triple=canonical,derived_guards=guards))
        outcome=dict(triple=triple,canonical=canonical,orbit=triple_orbit(target,triple),
                     solver_status=solver.status_name(branch_status) if branch_status is not None else 'NOT_SOLVED',
                     exhausted=branch_status==cp_model.INFEASIBLE,stop_reason=stop,
                     new_records=len(records)-count_before,seconds=time.monotonic()-branch_started,survivor=survivor)
        outcomes.append(outcome)
        print(json.dumps(dict(event='class',target=target,number=len(outcomes),total=len(projection['classes']),
                              triple=triple,status=outcome['solver_status'],new_records=outcome['new_records'])),flush=True)
        save()
        if survivor:
            reason='unresolved_candidate'
            break
    # A resumed partial sweep must retain earlier outcomes for unvisited groups.
    visited={tuple(map(tuple,o['canonical'])) for o in outcomes}
    outcomes.extend(o for k,o in prior.items() if k not in visited)
    solver.parameters.max_time_in_seconds=final_seconds
    status=solver.solve(model)
    if status==cp_model.INFEASIBLE:
        reason='exhausted_parent'
    assert digest(projection_path)==projection_hash,'Projection changed during search'
    result=save()
    print(json.dumps(dict(event='search_complete',**result)),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--target',type=int,nargs=2)
    ap.add_argument('--seconds-per-class',type=float,default=5)
    ap.add_argument('--total-seconds',type=float,default=300)
    ap.add_argument('--final-seconds',type=float,default=45)
    ap.add_argument('--connected-cells',action='store_true')
    args=ap.parse_args()
    for t in ([tuple(args.target)] if args.target else REMAINING):
        run(t,args.seconds_per_class,args.total_seconds,args.final_seconds,args.connected_cells)
