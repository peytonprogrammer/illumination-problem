"""Fresh exact-path and coverage audit; separate composed/geometry-only parents."""
import json
from collections import Counter
from analyze_illumination_exception_itineraries import independent_events
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_midpoint_1_1 import PATH,TARGET,load_base
from search_illumination_midpoint_covers import one_pass
from search_illumination_three_two_star import make_model,add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from audit_illumination_three_two_star import touched_tiles


def geometry(room):
    return tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))


def run():
    saved=json.loads(PATH.read_text());model,ts,x,bounded,terms,keys,seeds,provenance=load_base()
    assert saved['provenance']==provenance and saved['seeds']==json.loads(json.dumps(seeds))
    bare,bts,bx,bb,bt=make_model(TARGET);assert ts==bts
    solver=solver_for(30,307);solver.parameters.cp_model_presolve=False
    positive=[]
    for n,r in enumerate(seeds[:3]):
        branch=bare.clone();selected=set(geometry(r['room']))
        for t,v in zip(ts,bx):branch.add(v==int(t in selected))
        assert solver.solve(branch) in (cp_model.OPTIMAL,cp_model.FEASIBLE)
        positive.append(dict(seed_index=n,status='ACCEPTED'))
    owners=owners_of(ts);initial=len(keys);midpoint_keys=set();mutations=corruptions=0;max_bounces=0
    for r in seeds:
        validate(r['room'],TARGET);one_pass(r['room'],r['witness'])
        for room,w in orbit(r['room'],r['witness']):
            one_pass(room,w);facts=tile_facts(ts,owners,w,room);key=tuple(facts)
            required=touched_tiles(ts,w);fixed=dict(facts);selected=set(geometry(room))
            assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
            if key not in midpoint_keys:midpoint_keys.add(key);add_guard(bare,bx,facts)
    def check(g):
        nonlocal mutations,corruptions,max_bounces
        room,w=g['room'],g['witness'];validate(room,TARGET);one_pass(room,w)
        facts=tile_facts(ts,owners,w,room);assert facts==list(map(tuple,g['tile_facts']))
        key=tuple(facts);assert key not in keys;keys.add(key)
        required=touched_tiles(ts,w);fixed=dict(facts);selected=set(geometry(room))
        assert required<=fixed.keys() and all(fixed[i]==int(ts[i] in selected) for i in required)
        if corruptions<8:
            i=next(iter(required));dropped=dict(fixed);del dropped[i];assert not required<=dropped.keys()
            flipped=dict(fixed);flipped[i]=1-flipped[i];assert flipped[i]!=int(ts[i] in selected);corruptions+=2
        if mutations<8:
            for i in [i for i in range(len(ts)) if i not in fixed][:min(2,8-mutations)]:
                verify(dict(room,triangles=sorted(selected^{ts[i]})),w);mutations+=1
        add_guard(model,x,facts)
        if key not in midpoint_keys:midpoint_keys.add(key);add_guard(bare,bx,facts)
        max_bounces=max(max_bounces,w['bounces'])
    for g in saved['seed_guards']:check(g)
    rooms=set()
    for n,r in enumerate(saved['records'],1):
        validate(r['room'],TARGET);one_pass(r['room'],r['witness']);k=geometry(r['room']);assert k not in rooms;rooms.add(k)
        for g in r['derived_guards']:check(g)
        if n%50==0:print(json.dumps(dict(event='audit_progress',records=n,guards=len(keys)-initial)),flush=True)
    assert len(keys)-initial==saved['summary']['new_guards']
    solver.parameters.max_time_in_seconds=60;status=solver.solve(model);composed=solver.status_name(status)
    if saved['summary']['exhausted']:assert status==cp_model.INFEASIBLE
    survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    solver.parameters.max_time_in_seconds=30;status=solver.solve(bare);universal=solver.status_name(status)
    novel_rooms=set(rooms)
    manifest_path=OUT/'mask12-proof-inputs-2-1.json';manifest=json.loads(manifest_path.read_text())
    oldrooms=set()
    def collect(d):
        if isinstance(d,dict):
            if d.get('marked')==[[0,0],[2,2]] and 'triangles' in d:oldrooms.add(geometry(d))
            for v in d.values():collect(v)
        elif isinstance(d,list):
            for v in d:collect(v)
    for name,h in manifest['sha256'].items():
        p=BASE.parent/name;assert digest(p)==h,name
        if p.suffix=='.json':collect(json.loads(p.read_text()))
    novel_rooms-=oldrooms
    gate_counts=Counter(tuple(independent_events(r['witness'])[0]) for r in seeds+saved['records'])
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=provenance,positive_controls=positive,
                seeds_verified=len(seeds),gate_counts=[dict(point=p,paths=n) for p,n in gate_counts.most_common()],new_seed_guards=len(saved['seed_guards']),new_records=len(rooms),new_geometries=len(novel_rooms),revisited_geometries=len(rooms&oldrooms),
                new_guards=len(keys)-initial,total_guards=len(keys),mutations=mutations,corrupt_guards=corruptions,max_new_reflections=max_bounces,
                composed_parent=composed,geometry_only_midpoint_parent=universal,midpoint_catalogue=len(midpoint_keys),placement_excluded=composed=='INFEASIBLE',
                survivor=survivor,unresolved_direction_scan=saved['unresolved'],prior_manifest_sha256=digest(manifest_path),
                scope='Exact positive one-pass witnesses and independent sufficient triangle coverage. Geometry-only implication separate from historical-cut parent. Finite misses and UNKNOWN remain unresolved. No formal UNSAT proof.')
    (OUT/'midpoint-audit-1-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['survivor','provenance','unresolved_direction_scan']}),flush=True)


if __name__=='__main__':run()
