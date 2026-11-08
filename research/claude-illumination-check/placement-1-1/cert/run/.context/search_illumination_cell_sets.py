"""Search the complete forty-cell-set partition for A-cell target (2,2)."""
import argparse
import json
import time

from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT, digest, model_with_audited_cuts, solver_for
from illumination_geometry import label, owners_of
from illumination_paths import find_path
from illumination_sector_paths import verify
from illumination_three_two_star_bound import complete_support, validate
from illumination_triple_cell_sets import outside_sets
from search_illumination_one_exception import orbit, tile_facts
from search_illumination_three_two_star import add_guard, room_from

TARGET=(2,2)


def load_parent():
    model,ts,x,bounded,terms,provenance,keys=model_with_audited_cuts(TARGET)
    bootstrap=OUT/'cell-2-2-bootstrap.json'
    data=json.loads(bootstrap.read_text())
    assert data['summary']['provenance']==provenance
    receipt=OUT/'connectivity-audit.json'
    assert json.loads(receipt.read_text())['status']=='PASS'
    for record in data['records']:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']))
            assert key not in keys
            keys.add(key)
            add_guard(model,x,guard['tile_facts'])
    choices=outside_sets(TARGET)[0]
    assert len(choices)==40
    provenance=dict(seed=provenance,bootstrap_sha256=digest(bootstrap),
                    connectivity_audit_sha256=digest(receipt))
    return model,ts,x,bounded,terms,provenance,keys,choices


def fix_cells(model,terms,bounded,chosen):
    chosen=set(map(tuple,chosen))
    for a,b in bounded['allowed']-bounded['mandatory']:
        model.add(terms['used'][2*a,2*b]==int((a,b) in chosen))


def room_outside(room):
    required=complete_support(TARGET)['mandatory']
    return tuple(sorted({(p[0]//2,p[1]//2) for t in room['triangles'] for p in t if label(p)=='A'}-required))


def run(seconds=4,final_seconds=45):
    begin=time.monotonic()
    model,ts,x,bounded,terms,provenance,seed_keys,choices=load_parent()
    path=OUT/'cell-search-2-2.json'
    previous=json.loads(path.read_text()) if path.exists() else None
    if previous:assert previous['summary']['provenance']==provenance
    records=previous['records'] if previous else []
    prior={tuple(map(tuple,o['outside_cells'])):o for o in previous['classes']} if previous else {}
    seen=set(seed_keys)
    for record in records:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']))
            assert key not in seen
            seen.add(key)
            add_guard(model,x,guard['tile_facts'])
    outcomes=[]
    owners=owners_of(ts)
    solver=solver_for(seconds,71)
    global_status=None
    def save():
        visited={tuple(map(tuple,o['outside_cells'])) for o in outcomes}
        retained=outcomes+[o for k,o in prior.items() if k not in visited]
        summary=dict(target_A_cell=TARGET,complete_partition_size=len(choices),classes_searched=len(retained),
                     classes_excluded=sum(o['exhausted'] for o in retained),records=len(records),
                     new_guards=len(seen)-len(seed_keys),seconds=time.monotonic()-begin,
                     global_status=solver.status_name(global_status) if global_status is not None else 'NOT_SOLVED',
                     excluded=global_status==cp_model.INFEASIBLE or (len(retained)==len(choices) and all(o['exhausted'] for o in retained)),
                     provenance=provenance,scope='Complete connected outside-cell partition. Only positive-ray cuts enter the unrestricted parent. Caps and finite ray misses remain unresolved.')
        temp=path.with_suffix('.tmp')
        temp.write_text(json.dumps(dict(summary=summary,classes=retained,records=records),indent=2)+'\n')
        temp.replace(path)
        return summary
    for chosen in choices:
        if prior.get(chosen,{}).get('exhausted'):
            outcomes.append(prior[chosen])
            continue
        branch=model.clone()
        fix_cells(branch,terms,bounded,chosen)
        start=time.monotonic()
        status=None
        survivor=None
        before=len(records)
        while time.monotonic()-start<seconds:
            solver.parameters.max_time_in_seconds=max(.001,seconds-(time.monotonic()-start))
            status=solver.solve(branch)
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
            room=room_from(TARGET,ts,x,solver)
            assert room_outside(room)==chosen
            witness=find_path(room,16,1000)
            if witness['status']!='illuminated':witness=find_path(room,32,2000)
            if witness['status']!='illuminated':
                survivor=dict(room=room,bounded_screen=witness)
                break
            verify(room,witness)
            guards=[]
            for changed,ray in orbit(room,witness):
                verify(changed,ray)
                facts=tile_facts(ts,owners,ray,changed)
                key=tuple(facts)
                if key in seen:continue
                seen.add(key)
                guards.append(dict(room=changed,witness=ray,tile_facts=facts))
                add_guard(model,x,facts)
                add_guard(branch,x,facts)
            assert guards
            records.append(dict(room=room,witness=witness,counts=validate(room,TARGET),outside_cells=chosen,derived_guards=guards))
        result=dict(outside_cells=chosen,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                    exhausted=status==cp_model.INFEASIBLE,new_records=len(records)-before,
                    seconds=time.monotonic()-start,survivor=survivor)
        outcomes.append(result)
        print(json.dumps(dict(event='cell_class',number=len(outcomes),**result)),flush=True)
        save()
        if survivor:break
    solver.parameters.max_time_in_seconds=final_seconds
    global_status=solver.solve(model)
    result=save()
    print(json.dumps(dict(event='cell_search_complete',**result)),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--seconds-per-class',type=float,default=4)
    ap.add_argument('--final-seconds',type=float,default=45)
    args=ap.parse_args()
    run(args.seconds_per_class,args.final_seconds)
