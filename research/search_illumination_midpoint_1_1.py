"""Bounded complete (1,1) historical parent, learning exact one-pass guards."""
import argparse
from collections import Counter
import json,time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for,model_with_audited_cuts
from search_illumination_midpoint_covers import one_pass,find_one_pass
from search_illumination_one_exception import orbit,tile_facts
from search_illumination_three_two_star import add_guard,room_from
from illumination_geometry import owners_of
from illumination_three_two_star_bound import validate
from probe_illumination_midpoint_1_1 import SOURCE,PATH as PROBE

TARGET=(1,1)
PATH=OUT/'midpoint-search-1-1.json'


def load_base():
    model,ts,x,bounded,terms,prov,keys=model_with_audited_cuts(TARGET)
    probe=json.loads(PROBE.read_text());assert probe['source_sha256']==digest(SOURCE)
    source=json.loads(SOURCE.read_text());alternatives={r['record_index']:r['witness'] for r in probe['records'] if r['witness']}
    provenance=dict(parent=prov,probe_sha256=digest(PROBE))
    seeds=[]
    for i,r in enumerate(source['records']):
        witness=alternatives.get(i,r['witness']);one_pass(r['room'],witness)
        seeds.append(dict(record_index=i,room=r['room'],witness=witness))
    return model,ts,x,bounded,terms,keys,seeds,provenance


def run(seconds):
    assert not PATH.exists(),'Preserve original phase.'
    start=time.monotonic();model,ts,x,bounded,terms,keys,seeds,provenance=load_base();initial=len(keys);owners=owners_of(ts)
    seed_guards=[];records=[];unresolved=None
    for r in seeds:
        for room,witness in orbit(r['room'],r['witness']):
            one_pass(room,witness);facts=tile_facts(ts,owners,witness,room);key=tuple(facts)
            if key in keys:continue
            keys.add(key);add_guard(model,x,facts);seed_guards.append(dict(room=room,witness=witness,tile_facts=facts))
    frequencies=Counter(tuple(r['witness']['direction']) for r in seeds);library=[d for d,n in frequencies.most_common()]
    solver=solver_for(seconds,293);solver.parameters.cp_model_presolve=False;status=None;deadline=time.monotonic()+seconds
    def save():
        result=dict(provenance=provenance,seeds=seeds,seed_guards=seed_guards,records=records,unresolved=unresolved,
                    summary=dict(target_A_cell=TARGET,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,
                                 base_guards=initial,new_seed_guards=len(seed_guards),new_records=len(records),new_learned_guards=len(keys)-initial-len(seed_guards),
                                 new_guards=len(keys)-initial,total_guards=len(keys),seconds=time.monotonic()-start,
                                 scope='Complete finite (1,1) geometry parent with historical exact-ray cuts and sufficient one-pass conditions. Finite direction misses and solver caps unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH)
        return result['summary']
    print(json.dumps(dict(event='seeded',**save())),flush=True)
    while time.monotonic()<deadline:
        solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(model)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
        room=room_from(TARGET,ts,x,solver);witness,screen=find_one_pass(room,library,deadline)
        if witness is None:unresolved=dict(room=room,screen=screen);break
        guards=[]
        for data,ray in orbit(room,witness):
            one_pass(data,ray);facts=tile_facts(ts,owners,ray,data);key=tuple(facts)
            if key in keys:continue
            keys.add(key);add_guard(model,x,facts);guards.append(dict(room=data,witness=ray,tile_facts=facts))
        assert guards
        records.append(dict(room=room,witness=witness,counts=validate(room,TARGET),derived_guards=guards,direction_screen=screen))
        if len(records)%20==0:print(json.dumps(dict(event='progress',**save())),flush=True)
    if status!=cp_model.INFEASIBLE:
        solver.parameters.max_time_in_seconds=30;status=solver.solve(model)
    print(json.dumps(dict(event='complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=180);run(ap.parse_args().seconds)
