"""Replay all exact guards and the complete listed-pair/complement partition."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_remainder_types import load_base,PATH,TARGET,fix_choice,GATE
from search_illumination_midpoint_covers import one_pass
from search_illumination_three_two_star import add_guard,room_from,typed_exceptions
from search_illumination_one_exception import tile_facts
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from audit_illumination_three_two_star import touched_tiles
from illumination_cover import D4,mat


def geometry(room):return tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))


def run():
    saved=json.loads(PATH.read_text());model,ts,x,bounded,terms,keys,ids,seeds,fans,choices,prov=load_base()
    assert saved['provenance']==json.loads(json.dumps(prov))
    assert len(saved['classes'])==len(choices)==3
    for i,(choice,claim) in enumerate(zip(choices,saved['classes']),1):
        assert claim['case_number']==i and claim['pair']==choice['pair'] and claim['interior_count']==choice['interior_count']
    solver=solver_for(30,457);solver.parameters.cp_model_presolve=False;controls=0
    projection=json.loads((OUT/'thin-tip-pairs-1-1.json').read_text())
    from project_illumination_thin_tip_pairs import load_base as control_parent
    control_model,control_ts,control_x,*_=control_parent();assert ts==control_ts
    for r in projection['classes'][:3]:
        branch=control_model.clone();selected=set(geometry(r['positive_room']))
        for t,v in zip(ts,control_x):branch.add(v==int(t in selected))
        assert solver.solve(branch) in (cp_model.FEASIBLE,cp_model.OPTIMAL);controls+=1
    count_controls=[]
    for choice in choices:
        candidates=[r for r in saved['records'] if r['interior_count']==choice['interior_count']]
        if not candidates:continue
        positive=model.clone();fix_choice(positive,x,terms,choice,choices);selected=set(geometry(candidates[0]['room']))
        for t,v in zip(ts,x):positive.add(v==int(t in selected))
        assert solver.solve(positive) in (cp_model.FEASIBLE,cp_model.OPTIMAL)
        count_controls.append(choice['interior_count']);controls+=1
    # Coverage is checked against the pre-learning remainder, not a possibly
    # already excluded parent, so successful closure cannot make it vacuous.
    from project_illumination_thin_tip_pairs import block_pair
    coverage_parent=model.clone()
    for pair in choices[0]['blocked_pairs']:block_pair(coverage_parent,terms,pair)
    total=coverage_parent.new_int_var(0,6,'coverage_defect_credit');coverage_parent.add(total==sum(terms['defects']))
    coverage_parent.add_forbidden_assignments([total],[[3],[4],[5]])
    logical_assignments=[]
    for u in [1,2]:
        for v in [1,2]:
            credit=1+u+v;interior=int(u==2)+int(v==2)
            assert credit==3+interior and interior in [0,1,2]
            assert sum(credit==3+c['interior_count'] for c in choices)==1
            logical_assignments.append(dict(free_types=[u,v],defect_credit=credit,interior_count=interior))
    solver.parameters.max_time_in_seconds=2;coverage=solver.solve(coverage_parent)
    print(json.dumps(dict(event='count_partition',solver_status=solver.status_name(coverage),logical_assignments=logical_assignments)),flush=True)
    assert coverage!=cp_model.MODEL_INVALID
    if coverage in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        raise AssertionError(('counterexample to type partition',solver.value(total)))
    # UNKNOWN is retained as UNKNOWN. The four-assignment argument supplies
    # coverage, using exactly three defects and the fixed smooth gate.

    initial=len(keys);owners=owners_of(ts);rooms=set();mutations=corruptions=0;max_bounces=0
    expected_pairs={tuple(map(tuple,p)) for p in choices[0]['blocked_pairs']}
    for n,r in enumerate(saved['records'],1):
        room,w=r['room'],r['witness'];validate(room,TARGET);one_pass(room,w)
        pair=tuple(map(tuple,r['pair']));triple=typed_exceptions(room);assert triple==tuple(sorted(pair+(GATE,)))
        choice=choices[r['case_number']-1]
        assert pair not in expected_pairs and sum(p[2]==2 for p in triple)==choice['interior_count']
        k=geometry(room);assert k not in rooms;rooms.add(k);selected=set(k)
        assert sum(1<<j for j,i in enumerate(ids) if ts[i] in selected)==191
        assert sum(1<<j for j,i in enumerate(fans['tip_triangle_ids']) if ts[i] in selected)==4
        # Every source room must survive all guards before its own learned ray.
        assert all(not all(int(ts[i] in selected)==v for i,v in key) for key in keys)
        for g in r['derived_guards']:
            data,ray=g['room'],g['witness'];validate(data,TARGET);one_pass(data,ray)
            facts=tile_facts(ts,owners,ray,data);assert facts==list(map(tuple,g['tile_facts']))
            key=tuple(facts);assert key not in keys;keys.add(key)
            required=touched_tiles(ts,ray);fixed=dict(facts);selected_guard=set(geometry(data))
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected_guard) for i in required)
            if corruptions<8:
                i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
                flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in selected_guard);corruptions+=2
            if mutations<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                    verify(dict(data,triangles=sorted(selected_guard^{ts[i]})),ray);mutations+=1
            add_guard(model,x,facts);max_bounces=max(max_bounces,ray['bounces'])
    assert len(keys)-initial==saved['summary']['new_guards']
    cases=[]
    for number,choice in enumerate(choices,1):
        branch=model.clone();fix_choice(branch,x,terms,choice,choices);solver.parameters.max_time_in_seconds=30 if saved['classes'][number-1]['exhausted'] else 8
        status=solver.solve(branch)
        if saved['classes'][number-1]['exhausted']:assert status==cp_model.INFEASIBLE
        survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
        if survivor:
            validate(survivor,TARGET);pair=tuple(p for p in typed_exceptions(survivor) if p!=GATE)
            assert pair not in expected_pairs and sum(p[2]==2 for p in typed_exceptions(survivor))==choice['interior_count']
        cases.append(dict(case_number=number,kind=choice['kind'],interior_count=choice['interior_count'],pair=choice['pair'],status=solver.status_name(status),survivor=survivor))
        print(json.dumps(dict(event='case_replay',**{k:v for k,v in cases[-1].items() if k!='survivor'})),flush=True)
    # Fresh replay of all original listed pairs with the combined guards.
    from project_illumination_thin_tip_pairs import fix_pair
    original_cases=[]
    for number,pair in enumerate(choices[0]['blocked_pairs'],1):
        branch=model.clone();fix_pair(branch,terms,pair);solver.parameters.max_time_in_seconds=8;st=solver.solve(branch)
        original_cases.append(dict(case_number=number,pair=pair,status=solver.status_name(st)))
    prior=json.loads((OUT/'interior-fans-audit-1-1.json').read_text());assert prior['original_listed_cases_excluded']==25
    mapping={t:i for i,t in enumerate(ts)};symmetries=0
    for g in D4:
        for swap in (False,True):
            if mat(g,(2,2))!=tuple(-v if swap else v for v in (2,2)):continue
            shift=(2,2) if swap else (0,0)
            perm=[mapping[tuple(sorted(tuple(mat(g,p)[k]+shift[k] for k in (0,1)) for p in t))] for t in ts]
            assert all(tuple(sorted((perm[i],v) for i,v in key)) in keys for key in keys);symmetries+=1
    assert symmetries==4
    solver.parameters.max_time_in_seconds=20;status=solver.solve(model);parent=solver.status_name(status)
    complete=all(c['status']=='INFEASIBLE' for c in cases)
    oldrooms=set()
    def collect(d):
        if isinstance(d,dict):
            if d.get('marked')==[[0,0],[2,2]] and 'triangles' in d:oldrooms.add(geometry(d))
            for v in d.values():collect(v)
        elif isinstance(d,list):
            for v in d:collect(v)
    mp=OUT/'interior-fans-proof-inputs-1-1.json';m=json.loads(mp.read_text())
    for name,h in m['sha256'].items():
        p=BASE.parent/name;assert digest(p)==h,name
        if p.suffix=='.json':collect(json.loads(p.read_text()))
    receipt=dict(status='PASS',source_sha256=digest(PATH),provenance=prov,positive_controls=controls,interior_count_positive_controls=count_controls,new_records=len(rooms),new_geometries=len(rooms-oldrooms),revisited_geometries=len(rooms&oldrooms),new_guards=len(keys)-initial,total_guards=len(keys),mutations=mutations,corrupt_guards=corruptions,max_new_reflections=max_bounces,cases=cases,interior_count_cases_excluded=sum(c['status']=='INFEASIBLE' for c in cases),count_partition_complement_status=solver.status_name(coverage),logical_count_partition_assignments=logical_assignments,count_partition_coverage_via='four_typed_assignments_exactly_three_exceptions_fixed_smooth_gate',original_pair_cases=original_cases,original_pair_cases_freshly_excluded=sum(c['status']=='INFEASIBLE' for c in original_cases),original_pair_cases_composed_excluded=25,partition_including_complement_complete=True,complete_partition_cover=complete,tip4_parent_status=parent,tip4_excluded=complete or parent=='INFEASIBLE',mark_stabilizer_closed=True,scope='Tip4 fixed parent only. Complete count split0/1/2 on the original complement; prior25 listed-pair exclusions retained by monotone guard inclusion. Historical sufficient ray cuts composed; no geometry-only universal midpoint claim. Caps and finite misses unresolved; whole placement not excluded.')
    (OUT/'remainder-types-audit-1-1.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['cases','provenance','original_pair_cases']}),flush=True)


if __name__=='__main__':run()
