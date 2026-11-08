"""Fresh exact rays and complete six-case/complement exclusion checks."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_forced_c_cases import load_base,PATH,TARGET,fix_branch,fix_pair,GATE
from project_illumination_forced_c_pairs import block_pair
from search_illumination_hub7_residual import fix_hub
from search_illumination_fan_partitions import fix_fan
from search_illumination_midpoint_covers import one_pass
from search_illumination_three_two_star import make_model,add_guard,room_from,typed_exceptions
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_triple_cell_sets import refine_connected_cells
from illumination_cover import D4,mat
from illumination_three_two_star_bound import validate
from audit_illumination_three_two_star import touched_tiles


def geometry(room):return tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))


def run():
    saved=json.loads(PATH.read_text());model,ts,x,bounded,terms,keys,ids,seeds,fans,choices,prov=load_base();assert saved['provenance']==prov
    expected={tuple(map(tuple,c['pair'])):i for i,c in enumerate(choices,1)};claims={tuple(map(tuple,c['pair'])):c for c in saved['classes']}
    assert set(claims)==set(expected) and len(claims)==len(saved['classes'])==6
    bare,bts,bx,bb,bt=make_model(TARGET);assert ts==bts;refine_connected_cells(TARGET,bare,bt)
    solver=solver_for(10,419);solver.parameters.cp_model_presolve=False;controls=[]
    for choice in choices:
        room=choice['positive_room'];validate(room,TARGET);selected=set(geometry(room));pair=tuple(map(tuple,choice['pair']));branch=bare.clone();fix_branch(branch,bx,bt,ids,fans);fix_pair(branch,bt,pair)
        for t,v in zip(ts,bx):branch.add(v==int(t in selected))
        assert solver.solve(branch) in (cp_model.OPTIMAL,cp_model.FEASIBLE)
        controls.append(dict(case_number=expected[pair],status='ACCEPTED'))
    owners=owners_of(ts);initial=len(keys);midpoint_keys=set()
    for r in seeds:
        for room,w in orbit(r['room'],r['witness']):
            facts=tile_facts(ts,owners,w,room);key=tuple(facts)
            if key not in midpoint_keys:midpoint_keys.add(key);add_guard(bare,bx,facts)
    rooms=set();mutations=corruptions=0;max_bounces=0
    for n,r in enumerate(saved['records'],1):
        room,w=r['room'],r['witness'];validate(room,TARGET);one_pass(room,w);pair=tuple(map(tuple,r['pair']));assert pair in expected and r['case_number']==expected[pair]
        assert typed_exceptions(room)==tuple(sorted(pair+(GATE,)))
        k=geometry(room);assert k not in rooms;rooms.add(k);selected=set(k)
        assert sum(1<<j for j,i in enumerate(ids) if ts[i] in selected)==191 and sum(1<<j for j,i in enumerate(fans['tip_triangle_ids']) if ts[i] in selected)==5
        for g in r['derived_guards']:
            data,ray=g['room'],g['witness'];validate(data,TARGET);one_pass(data,ray);facts=tile_facts(ts,owners,ray,data);assert facts==list(map(tuple,g['tile_facts']))
            key=tuple(facts);assert key not in keys;keys.add(key);required=touched_tiles(ts,ray);fixed=dict(facts);selected=set(geometry(data))
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
            if corruptions<8:
                i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
                flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in selected);corruptions+=2
            if mutations<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:verify(dict(data,triangles=sorted(selected^{ts[i]})),ray);mutations+=1
            add_guard(model,x,facts)
            if key not in midpoint_keys:midpoint_keys.add(key);add_guard(bare,bx,facts)
            max_bounces=max(max_bounces,ray['bounces'])
        if n%25==0:print(json.dumps(dict(event='ray_audit',records=n,guards=len(keys)-initial)),flush=True)
    assert len(keys)-initial==saved['summary']['new_guards']
    cases=[]
    for pair,number in expected.items():
        branch=model.clone();fix_branch(branch,x,terms,ids,fans);fix_pair(branch,terms,pair);solver.parameters.max_time_in_seconds=30;status=solver.solve(branch)
        if claims[pair]['exhausted']:assert status==cp_model.INFEASIBLE
        cases.append(dict(case_number=number,pair=pair,status=solver.status_name(status)));print(json.dumps(dict(event='case_replay',**cases[-1])),flush=True)
    remainder=model.clone();fix_branch(remainder,x,terms,ids,fans)
    for pair in expected:block_pair(remainder,terms,pair)
    solver.parameters.max_time_in_seconds=30;status=solver.solve(remainder);remainder_status=solver.status_name(status)
    prior=json.loads((OUT/'forced-c-pairs-audit-1-1.json').read_text());assert prior['pair_projection_complete'] and prior['residual_status']=='INFEASIBLE'
    remainder_proved=status==cp_model.INFEASIBLE or prior['pair_projection_complete']
    complete_cover=remainder_proved and all(c['status']=='INFEASIBLE' for c in cases)
    conditional=bare.clone();fix_branch(conditional,bx,bt,ids,fans);solver.parameters.max_time_in_seconds=20;status=solver.solve(conditional);universal=solver.status_name(status)
    direct=model.clone();fix_branch(direct,x,terms,ids,fans);solver.parameters.max_time_in_seconds=30;status=solver.solve(direct);tip5_status=solver.status_name(status)
    tip5_excluded=complete_cover or status==cp_model.INFEASIBLE
    fan_cases=[]
    for mask in fans['compatible_fan_masks']:
        if mask==5 and tip5_excluded:name='INFEASIBLE';via='six_case_composition' if complete_cover else 'fresh_tip5_parent'
        else:
            branch=model.clone();fix_hub(branch,x,ids,191);fix_fan(branch,x,fans['tip_triangle_ids'],mask);solver.parameters.max_time_in_seconds=15;status=solver.solve(branch);name=solver.status_name(status);via='fresh_tip_fan_replay'
        fan_cases.append(dict(tip_mask=mask,status=name,via=via));print(json.dumps(dict(event='tip_replay',**fan_cases[-1])),flush=True)
    mapping={t:i for i,t in enumerate(ts)};symmetries=0
    for g in D4:
        for swap in (False,True):
            if mat(g,(2,2))!=tuple(-v if swap else v for v in (2,2)):continue
            shift=(2,2) if swap else (0,0)
            perm=[mapping[tuple(sorted(tuple(mat(g,p)[k]+shift[k] for k in (0,1)) for p in t))] for t in ts]
            assert all(tuple(sorted((perm[i],v) for i,v in key)) in keys for key in keys);symmetries+=1
    assert symmetries==4
    solver.parameters.max_time_in_seconds=20;status=solver.solve(model);parent=solver.status_name(status)
    survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    oldrooms=set()
    def collect(d):
        if isinstance(d,dict):
            if d.get('marked')==[[0,0],[2,2]] and 'triangles' in d:oldrooms.add(geometry(d))
            for v in d.values():collect(v)
        elif isinstance(d,list):
            for v in d:collect(v)
    mp=OUT/'forced-c-pairs-proof-inputs-1-1.json';m=json.loads(mp.read_text())
    for name,h in m['sha256'].items():
        p=BASE.parent/name;assert digest(p)==h,name
        if p.suffix=='.json':collect(json.loads(p.read_text()))
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=prov,positive_controls=controls,new_records=len(rooms),new_geometries=len(rooms-oldrooms),revisited_geometries=len(rooms&oldrooms),new_guards=len(keys)-initial,total_guards=len(keys),mutations=mutations,corrupt_guards=corruptions,max_new_reflections=max_bounces,pair_cases=cases,cases_excluded=sum(c['status']=='INFEASIBLE' for c in cases),fresh_remainder_status=remainder_status,remainder_proved_infeasible=remainder_proved,prior_remainder_audit_sha256=digest(OUT/'forced-c-pairs-audit-1-1.json'),complete_six_case_cover=complete_cover,tip5_parent_status=tip5_status,tip5_excluded=tip5_excluded,geometry_only_tip5_midpoint=universal,fan_cases=fan_cases,mark_stabilizer_closed=True,composed_parent=parent,survivor=survivor,scope='Complete six-case partition plus previously audited complement; all new guards exact sufficient rays. Geometry-only midpoint implication separate from historical-cut model. Finite misses/UNKNOWN unresolved; no formal UNSAT proof.')
    (OUT/'forced-c-cases-audit-1-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['provenance','survivor','fan_cases','pair_cases']}),flush=True)


if __name__=='__main__':run()
