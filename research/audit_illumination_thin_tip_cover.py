"""Replay all exact guards and the complete listed-pair/complement partition."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_thin_tip_cover import load_base,PATH,TARGET,fix_choice,GATE
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
    assert len(saved['classes'])==len(choices)==26
    for i,(choice,claim) in enumerate(zip(choices,saved['classes']),1):
        assert claim['case_number']==i and claim['pair']==choice['pair']
    solver=solver_for(30,457);solver.parameters.cp_model_presolve=False;controls=0
    projection=json.loads((OUT/'thin-tip-pairs-1-1.json').read_text())
    for r in projection['classes'][:3]:
        branch=model.clone();selected=set(geometry(r['positive_room']))
        for t,v in zip(ts,x):branch.add(v==int(t in selected))
        assert solver.solve(branch) in (cp_model.FEASIBLE,cp_model.OPTIMAL);controls+=1
    initial=len(keys);owners=owners_of(ts);rooms=set();mutations=corruptions=0;max_bounces=0
    expected_pairs={tuple(map(tuple,c['pair'])) for c in choices if c['pair'] is not None}
    for n,r in enumerate(saved['records'],1):
        room,w=r['room'],r['witness'];validate(room,TARGET);one_pass(room,w)
        pair=tuple(map(tuple,r['pair']));triple=typed_exceptions(room);assert triple==tuple(sorted(pair+(GATE,)))
        choice=choices[r['case_number']-1]
        if choice['pair'] is not None:assert pair==tuple(map(tuple,choice['pair']))
        else:assert pair not in expected_pairs
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
        branch=model.clone();fix_choice(branch,terms,choice,choices);solver.parameters.max_time_in_seconds=30 if saved['classes'][number-1]['exhausted'] else 8
        status=solver.solve(branch)
        if saved['classes'][number-1]['exhausted']:assert status==cp_model.INFEASIBLE
        survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
        if survivor:
            validate(survivor,TARGET);pair=tuple(p for p in typed_exceptions(survivor) if p!=GATE)
            if choice['pair'] is not None:assert pair==tuple(map(tuple,choice['pair']))
            else:assert pair not in expected_pairs
        cases.append(dict(case_number=number,kind=choice['kind'],pair=choice['pair'],status=solver.status_name(status),survivor=survivor))
        print(json.dumps(dict(event='case_replay',**{k:v for k,v in cases[-1].items() if k!='survivor'})),flush=True)
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
    mp=OUT/'thin-tip-pairs-proof-inputs-1-1.json';m=json.loads(mp.read_text())
    for name,h in m['sha256'].items():
        p=BASE.parent/name;assert digest(p)==h,name
        if p.suffix=='.json':collect(json.loads(p.read_text()))
    receipt=dict(status='PASS',source_sha256=digest(PATH),provenance=prov,positive_controls=controls,new_records=len(rooms),new_geometries=len(rooms-oldrooms),revisited_geometries=len(rooms&oldrooms),new_guards=len(keys)-initial,total_guards=len(keys),mutations=mutations,corrupt_guards=corruptions,max_new_reflections=max_bounces,cases=cases,listed_cases_excluded=sum(c['status']=='INFEASIBLE' for c in cases[:-1]),complement_status=cases[-1]['status'],partition_including_complement_complete=True,complete_partition_cover=complete,tip4_parent_status=parent,tip4_excluded=complete or parent=='INFEASIBLE',mark_stabilizer_closed=True,scope='Tip4 fixed parent only. Every listed pair plus explicit complement retained. Historical sufficient ray cuts composed; no geometry-only universal midpoint claim. Caps and finite misses unresolved; whole placement not excluded.')
    (OUT/'thin-tip-cover-audit-1-1.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['cases','provenance']}),flush=True)


if __name__=='__main__':run()
