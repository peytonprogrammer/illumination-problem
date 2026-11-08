"""Audit exact paths and compose the complete seven-tip-fan partition."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_hub7_residual import load_base,PATH,TARGET,MASK,fix_hub
from search_illumination_fan_partitions import fix_fan,fan_masks
from search_illumination_midpoint_covers import one_pass
from search_illumination_three_two_star import make_model,add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_triple_cell_sets import refine_connected_cells
from illumination_three_two_star_bound import validate
from illumination_cover import D4,mat
from audit_illumination_three_two_star import touched_tiles


def geometry(room):return tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))


def run():
    saved=json.loads(PATH.read_text());model,ts,x,bounded,terms,keys,ids,seeds,fans,prov=load_base()
    assert saved['provenance']==prov
    tip=fans['tip_triangle_ids'];assert fan_masks(ts,tuple(fans['tip_cell']))[0]==tip
    compatible=[m for m in fan_masks(ts,tuple(fans['tip_cell']))[1] if all((m>>j&1)==v for j,v in fans['fixed_tip_bits'])]
    assert compatible==fans['compatible_fan_masks']
    claims={c['tip_mask']:c for c in saved['classes']};assert set(claims)==set(compatible) and len(claims)==len(saved['classes'])
    bare,bts,bx,bb,bt=make_model(TARGET);assert bts==ts;refine_connected_cells(TARGET,bare,bt)
    solver=solver_for(15,367);solver.parameters.cp_model_presolve=False
    controls=[]
    for r in saved['records'][:3]:
        branch=bare.clone();selected=set(geometry(r['room']))
        for t,v in zip(ts,bx):branch.add(v==int(t in selected))
        assert solver.solve(branch) in (cp_model.OPTIMAL,cp_model.FEASIBLE)
        controls.append(dict(tip_mask=r['tip_mask'],status='ACCEPTED'))
    geometry_model=bare.clone()
    owners=owners_of(ts);initial=len(keys);midpoint_keys=set()
    for r in seeds:
        for room,w in orbit(r['room'],r['witness']):
            facts=tile_facts(ts,owners,w,room);key=tuple(facts)
            if key not in midpoint_keys:midpoint_keys.add(key);add_guard(bare,bx,facts)
    rooms=set();mutations=corruptions=0;max_bounces=0
    for n,r in enumerate(saved['records'],1):
        validate(r['room'],TARGET);one_pass(r['room'],r['witness']);k=geometry(r['room']);assert k not in rooms;rooms.add(k);selected=set(k)
        assert sum(1<<j for j,i in enumerate(ids) if ts[i] in selected)==MASK
        assert sum(1<<j for j,i in enumerate(tip) if ts[i] in selected)==r['tip_mask'] in compatible
        for g in r['derived_guards']:
            room,w=g['room'],g['witness'];validate(room,TARGET);one_pass(room,w);facts=tile_facts(ts,owners,w,room);assert facts==list(map(tuple,g['tile_facts']))
            key=tuple(facts);assert key not in keys;keys.add(key);selected=set(geometry(room));required=touched_tiles(ts,w);fixed=dict(facts)
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
            if corruptions<8:
                i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
                flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in selected);corruptions+=2
            if mutations<8:
                for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:verify(dict(room,triangles=sorted(selected^{ts[i]})),w);mutations+=1
            add_guard(model,x,facts)
            if key not in midpoint_keys:midpoint_keys.add(key);add_guard(bare,bx,facts)
            max_bounces=max(max_bounces,w['bounces'])
        if n%50==0:print(json.dumps(dict(event='fan_ray_audit',records=n,guards=len(keys)-initial)),flush=True)
    assert len(keys)-initial==saved['summary']['new_guards']
    cases=[]
    for mask in compatible:
        branch=model.clone();fix_hub(branch,x,ids,MASK);fix_fan(branch,x,tip,mask);solver.parameters.max_time_in_seconds=30;status=solver.solve(branch)
        if claims[mask]['exhausted']:assert status==cp_model.INFEASIBLE
        cases.append(dict(tip_mask=mask,status=solver.status_name(status)));print(json.dumps(dict(event='fan_replay',**cases[-1])),flush=True)
    geometry_cases=[]
    for c in cases:
        if c['status']!='INFEASIBLE':continue
        branch=geometry_model.clone();fix_hub(branch,bx,ids,MASK);fix_fan(branch,bx,tip,c['tip_mask']);solver.parameters.max_time_in_seconds=15;status=solver.solve(branch)
        baseline=solver.status_name(status)
        control=room_from(TARGET,ts,bx,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
        covered=bare.clone();fix_hub(covered,bx,ids,MASK);fix_fan(covered,bx,tip,c['tip_mask']);solver.parameters.max_time_in_seconds=15;status=solver.solve(covered)
        geometry_cases.append(dict(tip_mask=c['tip_mask'],base_geometry_status=baseline,positive_control=control,midpoint_cover_status=solver.status_name(status)))
        print(json.dumps(dict(event='geometry_fan_check',tip_mask=c['tip_mask'],base_geometry=baseline,midpoint_cover=solver.status_name(status))),flush=True)
    mapping={t:i for i,t in enumerate(ts)};symmetries=0
    for g in D4:
        for swap in (False,True):
            if mat(g,(2,2))!=tuple(-v if swap else v for v in (2,2)):continue
            shift=(2,2) if swap else (0,0)
            def transformed(t):
                return tuple(sorted(tuple(mat(g,p)[k]+shift[k] for k in (0,1)) for p in t))
            perm=[mapping[transformed(t)] for t in ts]
            assert all(tuple(sorted((perm[i],v) for i,v in key)) in keys for key in keys)
            symmetries+=1
    assert symmetries==4
    complete_cover=all(c['status']=='INFEASIBLE' for c in cases)
    fixed=bare.clone();fix_hub(fixed,bx,ids,MASK);solver.parameters.max_time_in_seconds=20;status=solver.solve(fixed);universal=solver.status_name(status)
    hub=json.loads((OUT/'hub-analysis-1-1.json').read_text());hub_cases=[]
    for mask in hub['complete_hub_masks']:
        if mask.bit_count()==7 and complete_cover:
            name='INFEASIBLE';via='complete_tip_fan_cover_and_checked_symmetry'
        else:
            branch=model.clone();fix_hub(branch,x,ids,mask);solver.parameters.max_time_in_seconds=15;status=solver.solve(branch);name=solver.status_name(status);via='fresh_fixed_hub_solve'
        hub_cases.append(dict(mask=mask,status=name,via=via));print(json.dumps(dict(event='hub_replay',**hub_cases[-1])),flush=True)
    solver.parameters.max_time_in_seconds=30;status=solver.solve(model);parent=solver.status_name(status)
    survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    oldrooms=set()
    def collect(d):
        if isinstance(d,dict):
            if d.get('marked')==[[0,0],[2,2]] and 'triangles' in d:oldrooms.add(geometry(d))
            for v in d.values():collect(v)
        elif isinstance(d,list):
            for v in d:collect(v)
    mp=OUT/'hub7-fan-proof-inputs-1-1.json';m=json.loads(mp.read_text())
    for name,h in m['sha256'].items():
        p=BASE.parent/name;assert digest(p)==h,name
        if p.suffix=='.json':collect(json.loads(p.read_text()))
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=prov,positive_controls=controls,new_records=len(rooms),new_geometries=len(rooms-oldrooms),revisited_geometries=len(rooms&oldrooms),new_guards=len(keys)-initial,total_guards=len(keys),mutations=mutations,corrupt_guards=corruptions,max_new_reflections=max_bounces,fan_cases=cases,geometry_only_fan_cases=geometry_cases,fan_branches_excluded=sum(c['status']=='INFEASIBLE' for c in cases),complete_tip_fan_cover=complete_cover,mark_stabilizer_closed=True,geometry_only_hub191=universal,hub_cases=hub_cases,seven_hub_family_excluded=all(c['status']=='INFEASIBLE' for c in hub_cases if c['mask'].bit_count()==7),composed_parent=parent,placement_excluded=parent=='INFEASIBLE' or all(c['status']=='INFEASIBLE' for c in hub_cases),survivor=survivor,scope='Complete seven-fan partition composition when every branch is INFEASIBLE; geometric symmetry and guard closure checked. Finite misses and caps unresolved; no formal UNSAT proof.')
    (OUT/'hub7-residual-audit-1-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['provenance','survivor','hub_cases','fan_cases','geometry_only_fan_cases']}),flush=True)


if __name__=='__main__':run()
