"""Compose the audited extended midpoint cover with historical positive rays."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from extend_illumination_midpoint_covers import PATH,load_base as midpoint_base
from search_illumination_double_fans import load_base
from search_illumination_midpoint_covers import TARGET,fixed_neck
from search_illumination_fan_partitions import fan_masks
from search_illumination_cell_partitions import fix_cells
from search_illumination_three_two_star import add_guard,room_from


def run():
    saved=json.loads(PATH.read_text());ap=OUT/'midpoint-extension-audit-2-1.json';audit=json.loads(ap.read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PATH)
    _,_,_,_,_,_,_,patterns,_,base_guards,peer_guards,_=midpoint_base()
    model,ts,x,bounded,terms,keys,first,_,provenance,_=load_base()
    double=json.loads((OUT/'double-fan-search-2-1.json').read_text());assert double['provenance']==provenance
    for r in double['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']))
            if key not in keys:keys.add(key);add_guard(model,x,key)
    historical=len(keys);assert historical==3207
    guards=base_guards+peer_guards+[g for r in saved['records'] for g in r['derived_guards']]
    for g in guards:
        key=tuple(map(tuple,g['tile_facts']))
        if key not in keys:keys.add(key);add_guard(model,x,key)
    mapping={t:i for i,t in enumerate(ts)};perm=[mapping[tuple(sorted((4-p[0],2-p[1]) for p in t))] for t in ts]
    assert all(tuple(sorted((perm[i],v) for i,v in key)) in keys for key in keys)
    second,_=fan_masks(ts,(1,1));solver=solver_for(60,251);solver.parameters.cp_model_presolve=False
    status=solver.solve(model);parent=solver.status_name(status)
    survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    print(json.dumps(dict(parent=parent,guards=len(keys))),flush=True)
    cases=[]
    for n,p in enumerate(patterns,1):
        branch=model.clone();fixed_neck(branch,terms,bounded,x,first,second,p)
        solver.parameters.max_time_in_seconds=60 if audit['cases'][n-1]['conditional_lemma'] else 10
        status=solver.solve(branch);cases.append(dict(neck_type=n,status=solver.status_name(status)))
        print(json.dumps(cases[-1]),flush=True)
    outside=[]
    for cells in [[],[[1,-1]],[[1,2]]]:
        branch=model.clone();fix_cells(branch,terms,bounded,cells);solver.parameters.max_time_in_seconds=10
        outside.append(dict(outside_cells=cells,status=solver.status_name(solver.solve(branch))))
    result=dict(status='PASS',source_sha256=digest(PATH),audit_sha256=digest(ap),historical_guards=historical,
                added_unique_midpoint_guards=len(keys)-historical,total_guards=len(keys),half_turn_closed=True,
                unrestricted_parent=parent,survivor=survivor,cases=cases,outside_cases=outside,
                canonical_types_excluded=sum(c['status']=='INFEASIBLE' for c in cases),
                cumulative_outside_sets_excluded=102+sum(c['status']=='INFEASIBLE' for c in outside),
                placement_excluded=parent=='INFEASIBLE' or all(c['status']=='INFEASIBLE' for c in cases),
                scope='Historical positive-ray cuts plus audited one-pass conditions; fresh replays, caps unresolved.')
    (OUT/'midpoint-extension-parent-2-1.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':run()
