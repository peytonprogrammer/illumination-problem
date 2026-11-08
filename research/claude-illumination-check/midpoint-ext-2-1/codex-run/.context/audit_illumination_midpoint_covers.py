"""Audit sufficient one-pass path patterns and fresh geometry-only implications."""
from collections import Counter
import json
from ortools.sat.python import cp_model
from audit_illumination_three_two_star import touched_tiles
from classify_illumination_three_exception import OUT,digest,solver_for
from illumination_geometry import owners_of,label
from search_illumination_midpoint_covers import TARGET,PATH,geometry_parent,fixed_neck,one_pass,seed_paths
from search_illumination_three_two_star import add_guard
from search_illumination_one_exception import orbit,tile_facts
from illumination_three_two_star_bound import validate
from illumination_sector_paths import verify
from search_illumination_cell_partitions import room_outside


def signature(data,ts,first,second,bounded):
    selected={tuple(sorted(map(tuple,t))) for t in data['triangles']}
    return (room_outside(data,TARGET),sum(1<<j for j,i in enumerate(first) if ts[i] in selected),sum(1<<j for j,i in enumerate(second) if ts[i] in selected))


def positive_controls(base,ts,x,bounded,terms,first,second,patterns):
    wanted={(tuple(map(tuple,p[0])),p[1],p[2]):i for i,p in enumerate(patterns)};controls={}
    for name in ['double-fan-search-2-1.json','ray-pattern-probe-2-1.json','fan-search-2-1.json','cell-search-2-1.json','cell-2-1-bootstrap.json']:
        for record in json.loads((OUT/name).read_text())['records']:
            room=record['room']
            for swap in [False,True]:
                data=room if not swap else dict(room,triangles=[tuple(sorted((4-p[0],2-p[1]) for p in t)) for t in room['triangles']])
                key=signature(data,ts,first,second,bounded)
                if key in wanted and wanted[key] not in controls:controls[wanted[key]]=data
        if len(controls)==12:break
    assert len(controls)==12
    solver=solver_for(10,181);solver.parameters.cp_model_presolve=False
    for i,data in sorted(controls.items()):
        validate(data,TARGET);branch=base.clone();fixed_neck(branch,terms,bounded,x,first,second,patterns[i]);selected={tuple(sorted(map(tuple,t))) for t in data['triangles']}
        for t,v in zip(ts,x):branch.add(v==int(t in selected))
        status=solver.solve(branch);assert status in (cp_model.OPTIMAL,cp_model.FEASIBLE),(i,solver.status_name(status))
    return [dict(neck_type=i+1,triangles=len(controls[i]['triangles'])) for i in range(12)]


def audit():
    saved=json.loads(PATH.read_text());model,ts,x,bounded,terms,first,second,patterns=geometry_parent()
    seed,provenance=seed_paths();assert saved['provenance']==provenance and saved['patterns']==patterns
    controls=positive_controls(model,ts,x,bounded,terms,first,second,patterns)
    owners=owners_of(ts);expected=set()
    for r in seed:
        for data,witness in orbit(r['room'],r['witness']):expected.add(tuple(tile_facts(ts,owners,witness,data)))
    keys=set();mutations=corruptions=0;max_bounces=0
    def check(guard):
        nonlocal mutations,corruptions,max_bounces
        data=guard['room'];witness=guard['witness'];validate(data,TARGET);one_pass(data,witness)
        facts=tile_facts(ts,owners,witness,data);assert facts==list(map(tuple,guard['tile_facts']))
        key=tuple(facts);assert key not in keys;keys.add(key)
        required=touched_tiles(ts,witness);fixed=dict(facts);selected={tuple(sorted(map(tuple,t))) for t in data['triangles']}
        assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
        if corruptions<8:
            i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
            flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in selected);corruptions+=2
        if mutations<8:
            for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                verify(dict(data,triangles=sorted(selected^{ts[i]})),witness);mutations+=1
        max_bounces=max(max_bounces,witness['bounces']);add_guard(model,x,facts)
    for guard in saved['seed_guards']:check(guard)
    assert keys==expected and len(keys)==saved['summary']['unique_seed_guards']
    print(json.dumps(dict(event='midpoint_seed_audit',guards=len(keys),fixed_positive_controls=len(controls))),flush=True)
    seed_count=len(keys);rooms=set()
    for n,record in enumerate(saved['records'],1):
        data=record['room'];selected=tuple(sorted(tuple(sorted(map(tuple,t))) for t in data['triangles']));assert selected not in rooms;rooms.add(selected)
        number=record['neck_type'];p=patterns[number-1];assert signature(data,ts,first,second,bounded)==(tuple(map(tuple,p[0])),p[1],p[2])
        one_pass(data,record['witness'])
        for guard in record['derived_guards']:check(guard)
        if n%25==0:print(json.dumps(dict(event='midpoint_guard_audit',records=n,guards=len(keys))),flush=True)
    assert len(keys)-seed_count==saved['summary']['new_guards'] and len(keys)==saved['summary']['total_guards']
    assert len(rooms)==saved['summary']['new_records']
    claims={c['neck_type']:c for c in saved['classes']};assert set(claims)==set(range(1,13))
    solver=solver_for(10,191);solver.parameters.cp_model_presolve=False;replays=[]
    for number,p in enumerate(patterns,1):
        branch=model.clone();fixed_neck(branch,terms,bounded,x,first,second,p)
        solver.parameters.max_time_in_seconds=60 if claims[number]['exhausted'] else 10
        status=solver.solve(branch)
        if claims[number]['exhausted']:assert status==cp_model.INFEASIBLE,(number,solver.status_name(status))
        replays.append(dict(neck_type=number,pattern=p,status=solver.status_name(status),conditional_midpoint_lemma=status==cp_model.INFEASIBLE))
        print(json.dumps(dict(event='midpoint_implication_replay',**replays[-1])),flush=True)
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=provenance,geometry_only_parent=True,historical_illumination_cuts=False,
                fixed_positive_controls=controls,seed_guards=seed_count,new_rooms=len(rooms),new_guards=len(keys)-seed_count,total_guards=len(keys),mutation_checks=mutations,corrupt_guard_checks=corruptions,max_reflections=max_bounces,
                conditional_midpoint_lemmas=sum(c['conditional_midpoint_lemma'] for c in replays),cases=replays,all_necks_covered=all(c['conditional_midpoint_lemma'] for c in replays),
                scope='Every guard preserves an exact one-exception midpoint ray. An infeasible geometry-only fixed-neck parent proves its finite sufficient-condition disjunction covers all valid completions. Caps and finite directional misses remain open. Computer-assisted implication, not a formal UNSAT proof.')
    (OUT/'midpoint-cover-audit-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('cases','fixed_positive_controls','provenance')}),flush=True)

if __name__=='__main__':audit()
