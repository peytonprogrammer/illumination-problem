"""Try a central-gate-only cover and extract a replayable sufficient subset."""
from collections import Counter
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from analyze_illumination_exception_itineraries import independent_events
from search_illumination_midpoint_covers import PATH,TARGET,geometry_parent,fixed_neck
from audit_illumination_midpoint_covers import signature
from search_illumination_three_two_star import add_guard
from illumination_three_two_star_bound import validate
from illumination_geometry import label


def run():
    saved=json.loads(PATH.read_text());base,ts,x,bounded,terms,first,second,patterns=geometry_parent();number=7
    assert saved['classes'][number-1]['exhausted']
    fixed_neck(base,terms,bounded,x,first,second,patterns[number-1])
    guards=saved['seed_guards']+[g for r in saved['records'] for g in r['derived_guards']]
    central=[];points=Counter()
    for i,g in enumerate(guards):
        events=independent_events(g['witness']);assert len(events)==1;point=tuple(events[0]);points[str(point)]+=1
        if point==(2,1):central.append(i)
    control_index=next(i for i,g in enumerate(guards) if signature(g['room'],ts,first,second,bounded)==((),40,83))
    control=guards[control_index]['room'];validate(control,TARGET);selected={tuple(sorted(map(tuple,t))) for t in control['triangles']}
    positive=base.clone()
    for t,v in zip(ts,x):positive.add(v==int(t in selected))
    solver=solver_for(10,197);solver.parameters.cp_model_presolve=False;status=solver.solve(positive);assert status in (cp_model.OPTIMAL,cp_model.FEASIBLE)
    branch=base.clone()
    for i in central:add_guard(branch,x,guards[i]['tile_facts'])
    solver.parameters.max_time_in_seconds=60;status=solver.solve(branch)
    result=dict(status='PASS',source_sha256=digest(PATH),neck_type=number,pattern=patterns[number-1],central_gate=[2,1],central_guard_indices=central,central_guard_count=len(central),
                positive_control_guard=control_index,positive_control_status='ACCEPTED',central_cover_replay=solver.status_name(status),
                scope='Finite central-gate path catalogue only. INFEASIBLE proves its disjunction covers every geometry-only neck completion; feasible/unknown would not disprove central-gate sufficiency.')
    print(json.dumps(dict(event='central_gate_replay',guards=len(central),status=solver.status_name(status))),flush=True)
    constants={}
    for i,t in enumerate(ts):
        center=next(p for p in t if label(p)=='A');cell=(center[0]//2,center[1]//2)
        if cell in bounded['full']:constants[i]=1
        elif cell not in bounded['mandatory']:constants[i]=0
    for ids,mask in [(first,40),(second,83)]:
        for j,i in enumerate(ids):constants[i]=(mask>>j)&1
    compatible=[i for i,g in enumerate(guards) if all(j not in constants or constants[j]==value for j,value in g['tile_facts'])]
    result['compatible_guard_count']=len(compatible)
    selected_pool=[i for i in central if i in compatible];pool_kind='central_gate'
    if result['central_cover_replay']!='INFEASIBLE':
        selected_pool=[i for i in compatible if tuple(independent_events(guards[i]['witness'])[0]) in ((1,0),(2,1))]
        pair_model=base.clone()
        for i in selected_pool:add_guard(pair_model,x,guards[i]['tile_facts'])
        solver.parameters.max_time_in_seconds=60;pair_status=solver.solve(pair_model)
        result.update(forced_pair_guard_count=len(selected_pool),forced_pair_cover_replay=solver.status_name(pair_status))
        pool_kind='two_forced_gates'
        print(json.dumps(dict(event='forced_pair_replay',guards=len(selected_pool),status=solver.status_name(pair_status))),flush=True)
        if pair_status!=cp_model.INFEASIBLE:selected_pool=compatible;pool_kind='all_compatible_midpoint_guards'
    candidate=base.clone();assumptions={}
    for i in selected_pool:
        assumption=candidate.new_bool_var(f'guard_{i}');facts=guards[i]['tile_facts']
        candidate.add(sum(1-x[j] if value else x[j] for j,value in facts)>=1).only_enforce_if(assumption)
        candidate.add_assumption(assumption);assumptions[assumption.index]=i
    solver.parameters.num_search_workers=1;solver.parameters.max_time_in_seconds=60;status=solver.solve(candidate)
    result.update(assumption_pool=pool_kind,assumption_pool_size=len(selected_pool),assumption_status=solver.status_name(status))
    if status==cp_model.INFEASIBLE:
        core=[assumptions[literal] for literal in solver.sufficient_assumptions_for_infeasibility()]
        assert core
        replay=base.clone()
        for i in core:add_guard(replay,x,guards[i]['tile_facts'])
        solver.parameters.max_time_in_seconds=60;status=solver.solve(replay)
        assert status==cp_model.INFEASIBLE
        result.update(core_guard_indices=core,core_size=len(core),core_replay=solver.status_name(status),core_is_minimum=False,
                      core_directions=[guards[i]['witness']['direction'] for i in core],
                      core_midpoint_gates=[independent_events(guards[i]['witness'])[0] for i in core])
    (OUT/'midpoint-cover-core-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':run()
