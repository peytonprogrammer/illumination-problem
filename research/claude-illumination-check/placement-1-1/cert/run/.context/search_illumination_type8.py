"""Target the last canonical outside-cell neck using exact positive-ray cuts."""
import argparse
from collections import Counter
import json
import time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT,digest,solver_for
from extend_illumination_midpoint_covers import load_base as midpoint_base
from search_illumination_double_fans import load_base as historical_base
from search_illumination_midpoint_covers import TARGET,fixed_neck,one_pass,find_one_pass
from search_illumination_fan_partitions import fan_masks
from search_illumination_three_two_star import add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_three_two_star_bound import validate

PATH=OUT/'type8-search-2-1.json'


def load_base():
    manifest_path=OUT/'midpoint-extension-proof-inputs-2-1.json'
    manifest=json.loads(manifest_path.read_text())
    for name,expected in manifest['sha256'].items():
        assert digest(OUT.parent.parent/name)==expected,name
    _,_,_,_,_,_,_,patterns,_,base_guards,peer_guards,_=midpoint_base()
    extension=json.loads((OUT/'midpoint-extension-2-1.json').read_text())
    midpoint_guards=base_guards+peer_guards+[g for r in extension['records'] for g in r['derived_guards']]
    model,ts,x,bounded,terms,keys,first,_,provenance,_=historical_base()
    double=json.loads((OUT/'double-fan-search-2-1.json').read_text())
    assert double['provenance']==provenance
    for g in [g for r in double['records'] for g in r['derived_guards']]+midpoint_guards:
        key=tuple(map(tuple,g['tile_facts']))
        if key not in keys:keys.add(key);add_guard(model,x,key)
    assert len(keys)==5063 and len(midpoint_guards)==2598
    second,_=fan_masks(ts,(1,1))
    provenance=dict(manifest_sha256=digest(manifest_path),composed_receipt_sha256=digest(OUT/'midpoint-extension-parent-2-1.json'))
    return model,ts,x,bounded,terms,first,second,patterns,keys,midpoint_guards,provenance


def run(seconds):
    assert not PATH.exists(),'Preserve earlier phase outputs.'
    start=time.monotonic()
    model,ts,x,bounded,terms,first,second,patterns,keys,midpoint_guards,provenance=load_base()
    initial=len(keys);branch=model.clone();fixed_neck(branch,terms,bounded,x,first,second,patterns[7])
    frequencies=Counter(tuple(g['witness']['direction']) for g in midpoint_guards)
    library=[d for d,_ in frequencies.most_common()]
    owners=owners_of(ts);records=[];unresolved=None
    solver=solver_for(seconds,263);solver.parameters.cp_model_presolve=False
    deadline=time.monotonic()+seconds;status=None

    def save():
        result=dict(provenance=provenance,neck_type=8,pattern=patterns[7],records=records,unresolved=unresolved,
                    summary=dict(status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                                 exhausted=status==cp_model.INFEASIBLE,base_guards=initial,new_records=len(records),
                                 new_guards=len(keys)-initial,total_guards=len(keys),seconds=time.monotonic()-start,
                                 scope='Historical-cut parent fixed to type8; exact sufficient one-pass paths only. Caps and finite direction misses unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH)
        return result['summary']

    while time.monotonic()<deadline:
        solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(branch)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
        room=room_from(TARGET,ts,x,solver);witness,screen=find_one_pass(room,library,deadline)
        if witness is None:unresolved=dict(room=room,screen=screen);break
        guards=[]
        for changed,ray in orbit(room,witness):
            one_pass(changed,ray);facts=tile_facts(ts,owners,ray,changed);key=tuple(facts)
            if key in keys:continue
            keys.add(key);add_guard(model,x,facts);add_guard(branch,x,facts)
            guards.append(dict(room=changed,witness=ray,tile_facts=facts))
        assert guards
        records.append(dict(room=room,witness=witness,counts=validate(room,TARGET),derived_guards=guards,direction_screen=screen))
        if len(records)%20==0:print(json.dumps(dict(event='type8_progress',**save())),flush=True)
    if status!=cp_model.INFEASIBLE:
        solver.parameters.max_time_in_seconds=60;status=solver.solve(branch)
    print(json.dumps(dict(event='type8_complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=180)
    run(ap.parse_args().seconds)
