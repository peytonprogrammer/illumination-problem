"""Fresh physical rays, sufficient cores, and seven-mask model replays."""
import json
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_hub7_1_1 import load_base,PATH,MASK,TARGET,fix_hub
from search_illumination_midpoint_covers import one_pass
from search_illumination_three_two_star import make_model,add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from illumination_triple_cell_sets import refine_connected_cells
from audit_illumination_three_two_star import touched_tiles


def geometry(room):return tuple(sorted(tuple(sorted(map(tuple,t))) for t in room['triangles']))


def run():
    saved=json.loads(PATH.read_text());model,ts,x,bounded,terms,keys,ids,seeds,prov=load_base()
    assert saved['provenance']==prov and saved['hub_mask']==MASK
    bare,bts,bx,bb,bt=make_model(TARGET);assert bts==ts;refine_connected_cells(TARGET,bare,bt)
    solver=solver_for(30,347);solver.parameters.cp_model_presolve=False
    positive=bare.clone();fix_hub(positive,bx,ids,MASK)
    if saved['records']:
        room=saved['records'][0]['room'];selected=set(geometry(room))
        for t,v in zip(ts,bx):positive.add(v==int(t in selected))
    status=solver.solve(positive);assert status in (cp_model.OPTIMAL,cp_model.FEASIBLE)
    positive_room=room_from(TARGET,ts,bx,solver)
    owners=owners_of(ts);midpoint_keys=set()
    for r in seeds:
        one_pass(r['room'],r['witness'])
        for room,w in orbit(r['room'],r['witness']):
            facts=tile_facts(ts,owners,w,room);key=tuple(facts)
            if key not in midpoint_keys:midpoint_keys.add(key);add_guard(bare,bx,facts)
    initial=len(keys);rooms=set();mutations=corruptions=0;max_bounces=0
    for n,r in enumerate(saved['records'],1):
        validate(r['room'],TARGET);one_pass(r['room'],r['witness']);k=geometry(r['room']);assert k not in rooms;rooms.add(k)
        assert sum(1<<j for j,i in enumerate(ids) if ts[i] in set(k))==MASK
        for g in r['derived_guards']:
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
        if n%50==0:print(json.dumps(dict(event='path_audit',records=n,guards=len(keys)-initial)),flush=True)
    assert len(keys)-initial==saved['summary']['new_guards']
    fixed=bare.clone();fix_hub(fixed,bx,ids,MASK);solver.parameters.max_time_in_seconds=30;status=solver.solve(fixed);universal=solver.status_name(status)
    print(json.dumps(dict(geometry_only_hub191=universal)),flush=True)
    hub=json.loads((OUT/'hub-analysis-1-1.json').read_text());cases=[]
    for mask in hub['complete_hub_masks']:
        branch=model.clone();fix_hub(branch,x,ids,mask);solver.parameters.max_time_in_seconds=60 if mask.bit_count()==7 else 15;status=solver.solve(branch)
        if saved['summary']['exhausted'] and mask==MASK:assert status==cp_model.INFEASIBLE
        cases.append(dict(mask=mask,status=solver.status_name(status)));print(json.dumps(cases[-1]),flush=True)
    solver.parameters.max_time_in_seconds=30;status=solver.solve(model);parent=solver.status_name(status)
    survivor=room_from(TARGET,ts,x,solver) if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    oldrooms=set()
    def collect(d):
        if isinstance(d,dict):
            if d.get('marked')==[[0,0],[2,2]] and 'triangles' in d:oldrooms.add(geometry(d))
            for v in d.values():collect(v)
        elif isinstance(d,list):
            for v in d:collect(v)
    manifest_path=OUT/'midpoint-proof-inputs-1-1.json';manifest=json.loads(manifest_path.read_text())
    for name,h in manifest['sha256'].items():
        p=BASE.parent/name;assert digest(p)==h,name
        if p.suffix=='.json':collect(json.loads(p.read_text()))
    result=dict(status='PASS',source_sha256=digest(PATH),provenance=prov,positive_geometry_control='ACCEPTED',positive_control=positive_room,
                new_records=len(rooms),new_geometries=len(rooms-oldrooms),revisited_geometries=len(rooms&oldrooms),new_guards=len(keys)-initial,total_guards=len(keys),
                mutations=mutations,corrupt_guards=corruptions,max_new_reflections=max_bounces,geometry_only_hub191=universal,midpoint_catalogue=len(midpoint_keys),
                cases=cases,composed_parent=parent,placement_excluded=parent=='INFEASIBLE' or all(c['status']=='INFEASIBLE' for c in cases),survivor=survivor,
                seven_hub_family_excluded=all(c['status']=='INFEASIBLE' for c in cases if c['mask'].bit_count()==7),
                scope='Checked sufficient one-pass rays; geometry-only hub implication separate from historical-cut exclusions. All seven local masks form the prior complete hub partition. Caps and finite misses unresolved; no formal UNSAT proof.')
    (OUT/'hub7-audit-1-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['positive_control','provenance','survivor','cases']}),flush=True)


if __name__=='__main__':run()
