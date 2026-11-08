"""Compose the newly audited sufficient midpoint patterns with old ray proofs."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from search_illumination_double_fans import load_base
from search_illumination_midpoint_covers import PATH,TARGET,fixed_neck
from search_illumination_fan_partitions import fan_masks
from search_illumination_cell_partitions import fix_cells
from search_illumination_three_two_star import add_guard,room_from


def run():
    saved=json.loads(PATH.read_text());audit_path=OUT/'midpoint-cover-audit-2-1.json';audit=json.loads(audit_path.read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PATH)
    model,ts,x,bounded,terms,keys,first,_,base_provenance,_=load_base()
    double_path=OUT/'double-fan-search-2-1.json';double=json.loads(double_path.read_text())
    assert double['provenance']==base_provenance
    for record in double['records']:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']));assert key not in keys
            keys.add(key);add_guard(model,x,guard['tile_facts'])
    prior_count=len(keys)
    guards=saved['seed_guards']+[g for r in saved['records'] for g in r['derived_guards']]
    for guard in guards:
        key=tuple(map(tuple,guard['tile_facts']))
        if key in keys:continue
        keys.add(key);add_guard(model,x,guard['tile_facts'])
    mapping={t:i for i,t in enumerate(ts)};perm=[mapping[tuple(sorted((4-p[0],2-p[1]) for p in t))] for t in ts]
    closed=all(tuple(sorted((perm[i],value) for i,value in key)) in keys for key in keys)
    second,_=fan_masks(ts,(1,1));patterns=json.loads((OUT/'neck-patterns-2-1.json').read_text())['canonical_patterns']
    solver=solver_for(60,211);solver.parameters.cp_model_presolve=False;status=solver.solve(model)
    survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    print(json.dumps(dict(event='midpoint_composed_parent',prior_guards=prior_count,new_unique_guards=len(keys)-prior_count,status=solver.status_name(status),guard_set_half_turn_closed=closed)),flush=True)
    parent_status=solver.status_name(status);cases=[]
    for number,pattern in enumerate(patterns,1):
        if parent_status=='INFEASIBLE':name='INFEASIBLE';via='unrestricted_parent'
        else:
            branch=model.clone();fixed_neck(branch,terms,bounded,x,first,second,pattern);solver.parameters.max_time_in_seconds=10;name=solver.status_name(solver.solve(branch));via='fixed_neck'
        cases.append(dict(neck_type=number,pattern=pattern,status=name,via=via))
        print(json.dumps(dict(event='midpoint_composed_neck',**cases[-1])),flush=True)
    outside_cases=[]
    for outside in [[],[[1,-1]],[[1,2]]]:
        if parent_status=='INFEASIBLE':name='INFEASIBLE'
        else:
            branch=model.clone();fix_cells(branch,terms,bounded,outside);solver.parameters.max_time_in_seconds=10;name=solver.status_name(solver.solve(branch))
        outside_cases.append(dict(outside_cells=outside,status=name))
    result=dict(status='PASS',source_sha256=digest(PATH),midpoint_audit_sha256=digest(audit_path),base_provenance=base_provenance,double_search_sha256=digest(double_path),
                prior_guards=prior_count,new_unique_midpoint_guards=len(keys)-prior_count,total_guards=len(keys),guard_set_half_turn_closed=closed,
                unrestricted_parent=parent_status,survivor=survivor,cases=cases,neck_classes_excluded=sum(c['status']=='INFEASIBLE' for c in cases),outside_cases=outside_cases,
                cumulative_outside_sets_excluded=102+sum(c['status']=='INFEASIBLE' for c in outside_cases),
                placement_excluded=parent_status=='INFEASIBLE' or all(c['status']=='INFEASIBLE' for c in cases),
                scope='Composition of historical positive-ray exclusions and newly audited one-pass guards. Fixed-neck negatives need not prove a universal single-pass lemma without the historical cuts. Caps unresolved.')
    (OUT/'midpoint-parent-replay-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('cases','outside_cases','base_provenance','survivor')}),flush=True)

if __name__=='__main__':run()
