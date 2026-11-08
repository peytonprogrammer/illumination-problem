"""Target the common empty-outside, first-mask12 parent after type6."""
import argparse
from collections import Counter
import json
import time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from search_illumination_type6 import load_base as prior_base
from search_illumination_midpoint_covers import TARGET,fixed_neck,one_pass,find_one_pass
from search_illumination_three_two_star import add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from search_illumination_cell_partitions import fix_cells
from search_illumination_fan_partitions import fix_fan
from illumination_three_two_star_bound import validate

PATH=OUT/'mask12-search-2-1.json'


def load_base():
    manifest_path=OUT/'type6-proof-inputs-2-1.json';manifest=json.loads(manifest_path.read_text())
    for name,expected in manifest['sha256'].items():assert digest(OUT.parent.parent/name)==expected,name
    model,ts,x,bounded,terms,first,second,patterns,keys,guards,_=prior_base()
    previous=json.loads((OUT/'type6-search-2-1.json').read_text())
    extra=[g for r in previous['records'] for g in r['derived_guards']]
    for g in extra:
        key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==5255
    provenance=dict(manifest_sha256=digest(manifest_path),prior_audit_sha256=digest(OUT/'type6-audit-2-1.json'))
    return model,ts,x,bounded,terms,first,second,patterns,keys,guards+extra,provenance


def fixed_parent(model,terms,bounded,x,first):
    fix_cells(model,terms,bounded,[])
    fix_fan(model,x,first,12)


def run(seconds):
    assert not PATH.exists(),'Preserve earlier phase outputs.'
    start=time.monotonic();model,ts,x,bounded,terms,first,second,patterns,keys,guards,provenance=load_base()
    initial=len(keys);branch=model.clone();fixed_parent(branch,terms,bounded,x,first)
    frequencies=Counter(tuple(g['witness']['direction']) for g in guards);library=[d for d,_ in frequencies.most_common()]
    owners=owners_of(ts);records=[];unresolved=None
    solver=solver_for(seconds,277);solver.parameters.cp_model_presolve=False
    deadline=time.monotonic()+seconds;status=None

    def save():
        result=dict(provenance=provenance,parent=dict(outside_cells=[],first_mask=12,second_mask=None),records=records,unresolved=unresolved,
                    summary=dict(status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                                 exhausted=status==cp_model.INFEASIBLE,base_guards=initial,new_records=len(records),new_guards=len(keys)-initial,
                                 total_guards=len(keys),seconds=time.monotonic()-start,
                                 scope='Historical-cut parent with empty outside set and first central mask12; exact sufficient one-pass paths only. Caps and finite direction misses unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH)
        return result['summary']

    while time.monotonic()<deadline:
        solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(branch)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
        room=room_from(TARGET,ts,x,solver);witness,screen=find_one_pass(room,library,deadline)
        if witness is None:unresolved=dict(room=room,screen=screen);break
        added=[]
        for changed,ray in orbit(room,witness):
            one_pass(changed,ray);facts=tile_facts(ts,owners,ray,changed);key=tuple(facts)
            if key in keys:continue
            keys.add(key);add_guard(model,x,facts);add_guard(branch,x,facts);added.append(dict(room=changed,witness=ray,tile_facts=facts))
        assert added
        records.append(dict(room=room,witness=witness,counts=validate(room,TARGET),derived_guards=added,direction_screen=screen))
        if len(records)%20==0:print(json.dumps(dict(event='mask12_progress',**save())),flush=True)
    if status!=cp_model.INFEASIBLE:solver.parameters.max_time_in_seconds=60;status=solver.solve(branch)
    print(json.dumps(dict(event='mask12_complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=180);run(ap.parse_args().seconds)
