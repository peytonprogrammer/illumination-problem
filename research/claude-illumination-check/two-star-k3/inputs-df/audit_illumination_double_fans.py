"""Check sample-ray claims, exact guards, complete double-fan coverage and replays."""
import argparse
from collections import Counter,defaultdict
import json
from ortools.sat.python import cp_model
from audit_illumination_three_two_star import touched_tiles
from classify_illumination_three_exception import OUT,digest,solver_for
from illumination_geometry import owners_of
from illumination_paths import trace
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from illumination_residual_fans import TARGET,SECOND_CELL,fix_first,fan_masks,fix_fan
from search_illumination_cell_partitions import room_outside
from search_illumination_double_fans import PATH,load_base
from search_illumination_three_two_star import add_guard
from search_illumination_one_exception import tile_facts


def independent_masks(ts,ids):
    local=[ts[i] for i in ids];adj={j:set() for j in range(8)}
    for _,os in owners_of(local).items():
        if len(os)==2:a,b=os;adj[a].add(b);adj[b].add(a)
    assert all(len(v)==2 for v in adj.values())
    masks=[0]
    for mask in range(1,255):
        selected={j for j in range(8) if mask>>j&1};seen={min(selected)};todo=list(seen)
        for j in todo:
            for k in adj[j]&selected-seen:seen.add(k);todo.append(k)
        if seen==selected:masks.append(mask)
    assert len(masks)==57
    return masks


def audit(seconds):
    saved=json.loads(PATH.read_text());probe=json.loads((OUT/'ray-pattern-probe-2-1.json').read_text())
    model,ts,x,bounded,terms,keys,ids,residual,provenance,library=load_base()
    assert saved['provenance']==provenance
    second_ids,masks=fan_masks(ts,SECOND_CELL)
    assert independent_masks(ts,ids)==fan_masks(ts)[1] and independent_masks(ts,second_ids)==masks
    assert saved['summary']['second_triangle_ids']==second_ids and saved['summary']['masks']==masks
    owners=owners_of(ts);checked=set();rays=mutations=corruptions=0;max_bounces=0
    def check_guard(guard):
        nonlocal rays,mutations,corruptions,max_bounces
        verify(guard['room'],guard['witness']);facts=tile_facts(ts,owners,guard['witness'],guard['room'])
        assert facts==list(map(tuple,guard['tile_facts']))
        key=tuple(facts)
        if key in checked:return False
        checked.add(key);required=touched_tiles(ts,guard['witness']);fixed=dict(facts)
        tiles={tuple(sorted(map(tuple,t))) for t in guard['room']['triangles']}
        assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in tiles) for i in required)
        max_bounces=max(max_bounces,guard['witness']['bounces'])
        if corruptions<8:
            i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
            flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in tiles);corruptions+=2
        if mutations<8:
            for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                verify(dict(guard['room'],triangles=sorted(tiles^{ts[i]})),guard['witness']);mutations+=1
        rays+=1;return True
    assert len(probe['branches'])==len(residual)
    sample_pairs=set()
    for record in probe['records']:
        validate(record['room'],TARGET);verify(record['room'],record['witness'])
        outside=room_outside(record['room'],TARGET);pair=(outside,record['first_mask']);assert pair in residual and pair not in sample_pairs;sample_pairs.add(pair)
        selected={tuple(sorted(map(tuple,t))) for t in record['room']['triangles']}
        assert sum(1<<j for j,i in enumerate(ids) if ts[i] in selected)==record['first_mask']
        assert sum(1<<j for j,i in enumerate(second_ids) if ts[i] in selected)==record['second_mask']
        for guard in record['derived_guards']:check_guard(guard)
    probe_guards=rays
    catalogue=probe['expanded_direction_coverage'];trace_statuses=Counter()
    for row in catalogue:
        actual=[]
        for i,record in enumerate(probe['records']):
            ray=trace(record['room'],row['direction'],64);trace_statuses[ray['status']]+=1
            if ray['status']=='illuminated':verify(record['room'],ray);actual.append(i)
        assert actual==row['records']
    assert dict(trace_statuses)==probe['summary']['expanded_trace_statuses']
    cover_model=cp_model.CpModel();pick=[cover_model.new_bool_var(f'direction{i}') for i in range(len(catalogue))]
    for j in range(len(probe['records'])):cover_model.add(sum(pick[i] for i,row in enumerate(catalogue) if j in row['records'])>=1)
    cover_model.minimize(sum(pick));cover_solver=solver_for(10,149);cover_solver.parameters.cp_model_presolve=False
    cover_status=cover_solver.solve(cover_model);assert cover_status==cp_model.OPTIMAL
    minimum_sample_cover=int(cover_solver.objective_value)
    covered=set()
    for row in probe['expanded_greedy_cover']:
        actual=next(set(c['records']) for c in catalogue if c['direction']==row['direction'])
        assert set(row['newly_covered'])==actual-covered;covered|=actual
    assert covered==set(range(len(probe['records'])))
    print(json.dumps(dict(event='pattern_audit',samples=len(sample_pairs),directions=len(catalogue),cross_traces=sum(trace_statuses.values()),exact_guards=probe_guards)),flush=True)
    rooms=set();new_guards=0
    for n,record in enumerate(saved['records'],1):
        validate(record['room'],TARGET);verify(record['room'],record['witness'])
        outside=room_outside(record['room'],TARGET);assert outside==tuple(map(tuple,record['outside_cells']))
        assert (outside,record['first_mask']) in residual and record['second_mask'] in masks
        selected={tuple(sorted(map(tuple,t))) for t in record['room']['triangles']};key=tuple(sorted(selected));assert key not in rooms;rooms.add(key)
        for cell_ids,name in [(ids,'first_mask'),(second_ids,'second_mask')]:assert sum(1<<j for j,i in enumerate(cell_ids) if ts[i] in selected)==record[name]
        for guard in record['derived_guards']:
            assert check_guard(guard);facts=guard['tile_facts'];key=tuple(map(tuple,facts));assert key not in keys;keys.add(key);add_guard(model,x,facts);new_guards+=1
        if n%25==0:print(json.dumps(dict(event='double_guard_audit',records=n,new_guards=new_guards)),flush=True)
    assert new_guards==saved['summary']['new_guards']
    assert dict(Counter(r['witness_source'] for r in saved['records']))==saved['summary']['witness_sources']
    claims={(tuple(map(tuple,c['outside_cells'])),c['first_mask'],c['second_mask']):c for c in saved['classes']}
    expected={(outside,mask,second) for outside,mask in residual for second in masks}
    assert len(claims)==len(saved['classes']) and set(claims)==expected
    solver=solver_for(seconds,151);solver.parameters.cp_model_presolve=False;replays=[];parents=[]
    for outside,first in residual:
        parent=model.clone();fix_first(parent,terms,bounded,x,ids,outside,first)
        solver.parameters.max_time_in_seconds=seconds;status=solver.solve(parent)
        parents.append(dict(outside_cells=outside,first_mask=first,status=solver.status_name(status)))
        parent_closed=status==cp_model.INFEASIBLE
        for second in masks:
            if parent_closed:
                name='INFEASIBLE';via='fresh_first_fan_parent'
            else:
                branch=parent.clone();fix_fan(branch,x,second_ids,second);solver.parameters.max_time_in_seconds=seconds;status=solver.solve(branch)
                if claims[outside,first,second]['exhausted'] and status!=cp_model.INFEASIBLE:
                    solver.parameters.max_time_in_seconds=30;status=solver.solve(branch)
                    assert status==cp_model.INFEASIBLE,('unreproduced',outside,first,second,solver.status_name(status))
                name=solver.status_name(status);via='direct_second_fan_solve'
            replays.append(dict(outside_cells=outside,first_mask=first,second_mask=second,status=name,via=via))
        print(json.dumps(dict(event='double_parent_audit',checked=len(parents),excluded_parents=sum(p['status']=='INFEASIBLE' for p in parents),checked_branches=len(replays),excluded_branches=sum(c['status']=='INFEASIBLE' for c in replays))),flush=True)
    solver.parameters.max_time_in_seconds=60;global_status=solver.solve(model)
    result=dict(status='PASS',source_sha256=digest(PATH),probe_sha256=digest(OUT/'ray-pattern-probe-2-1.json'),provenance=provenance,
                samples=len(sample_pairs),sample_catalogue=len(catalogue),sample_trace_statuses=dict(trace_statuses),sample_cover_directions=len(probe['expanded_greedy_cover']),minimum_sample_cover=minimum_sample_cover,
                probe_guards=probe_guards,new_records=len(saved['records']),new_guards=new_guards,total_new_exact_guards=rays,mutations=mutations,corruptions=corruptions,max_bounces=max_bounces,
                partition_size=len(replays),branches_excluded=sum(c['status']=='INFEASIBLE' for c in replays),classes=replays,first_fan_parents=parents,
                unrestricted_parent=solver.status_name(global_status),placement_excluded=global_status==cp_model.INFEASIBLE or all(c['status']=='INFEASIBLE' for c in replays),
                scope='Complete second-fan refinement of the18 first-fan residuals. Earlier exclusions compose monotonically with verified positive-ray constraints. Sample direction coverage is not universal. Caps unresolved; no formal UNSAT proof.')
    (OUT/'double-fan-audit-2-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('classes','first_fan_parents','provenance')}),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=3);args=ap.parse_args();audit(args.seconds)
