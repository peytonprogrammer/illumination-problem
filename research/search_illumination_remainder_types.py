"""Bounded exact one-pass covers of twenty-five pairs and their complement."""
import argparse
from collections import Counter
import json,time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_hub7_residual import TARGET
from project_illumination_thin_tip_pairs import fix_pair,block_pair,GATE
from search_illumination_interior_fans import load_base as fan_parent,PATH as FAN_PATH
from search_illumination_fan_partitions import fix_fan
from search_illumination_midpoint_covers import one_pass,find_one_pass
from search_illumination_three_two_star import add_guard,room_from,typed_exceptions
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of

PATH=OUT/'remainder-types-1-1.json'


def load_base():
    mp=OUT/'interior-fans-proof-inputs-1-1.json';manifest=json.loads(mp.read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    model,ts,x,bounded,terms,keys,ids,seeds,fans,old_choices,prov=fan_parent()
    saved=json.loads(FAN_PATH.read_text());audit=json.loads((OUT/'interior-fans-audit-1-1.json').read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(FAN_PATH) and audit['original_listed_cases_excluded']==25
    for r in saved['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==audit['total_guards']==3883
    seeds=seeds+[dict(room=r['room'],witness=r['witness']) for r in saved['records']]
    choices=[dict(pair=None,kind='interior_count',interior_count=n,blocked_pairs=old_choices[-1]['blocked_pairs']) for n in range(3)]
    return model,ts,x,bounded,terms,keys,ids,seeds,fans,choices,dict(prov,fan_manifest_sha256=digest(mp))


def fix_choice(model,x,terms,choice,choices):
    for pair in choice['blocked_pairs']:block_pair(model,terms,pair)
    model.add(sum(terms['defects'])==3+choice['interior_count'])


def run(seconds):
    assert not PATH.exists();begin=time.monotonic();model,ts,x,bounded,terms,keys,ids,seeds,fans,choices,prov=load_base();initial=len(keys);owners=owners_of(ts)
    library=prov['peer_directions']+[d for d,n in Counter(tuple(r['witness']['direction']) for r in seeds).most_common()];records=[];classes=[]
    solver=solver_for(seconds,409);solver.parameters.cp_model_presolve=False
    def save():
        result=dict(provenance=prov,records=records,classes=classes,summary=dict(base_guards=initial,new_records=len(records),new_guards=len(keys)-initial,total_guards=len(keys),complete_partition_size=len(choices),visited=len(classes),exhausted_cases=sum(c['exhausted'] for c in classes),seconds=time.monotonic()-begin,scope='Complete0/1/2 interior-exception split of the original unlisted complement under hub191/tip4; exact sufficient one-pass rays only. Finite misses/caps leave their cases unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH);return result['summary']
    for number,choice in enumerate(choices,1):
        pair=tuple(map(tuple,choice['pair'])) if choice['pair'] is not None else None;branch=model.clone();fix_choice(branch,x,terms,choice,choices)
        start=time.monotonic();deadline=start+seconds;status=None;unresolved=None;before=len(records)
        while time.monotonic()<deadline:
            solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(branch)
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
            room=room_from(TARGET,ts,x,solver);triple=typed_exceptions(room);assert GATE in triple
            actual=tuple(p for p in triple if p!=GATE);assert sum(p[2]==2 for p in triple)==choice['interior_count']
            if pair is not None:assert actual==pair
            else:assert actual not in [tuple(map(tuple,p)) for p in choice['blocked_pairs']]
            witness,screen=find_one_pass(room,library,deadline)
            if witness is None:unresolved=dict(room=room,screen=screen);break
            library=[tuple(witness['direction'])]+library;guards=[]
            for data,w in orbit(room,witness):
                one_pass(data,w);facts=tile_facts(ts,owners,w,data);key=tuple(facts)
                if key in keys:continue
                keys.add(key);add_guard(model,x,key);add_guard(branch,x,key);guards.append(dict(room=data,witness=w,tile_facts=facts))
            assert guards
            records.append(dict(case_number=number,pair=actual,interior_count=choice['interior_count'],room=room,witness=witness,derived_guards=guards,direction_screen=screen))
        if status!=cp_model.INFEASIBLE:
            solver.parameters.max_time_in_seconds=2;status=solver.solve(branch)
        classes.append(dict(case_number=number,pair=pair,interior_count=choice['interior_count'],status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,new_records=len(records)-before,seconds=time.monotonic()-start,unresolved=unresolved))
        print(json.dumps(dict(event='case_complete',case_number=number,**save())),flush=True)
    print(json.dumps(dict(event='complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=30);run(ap.parse_args().seconds)
