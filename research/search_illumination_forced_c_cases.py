"""Bounded exact one-pass covers of a complete six-case exception partition."""
import argparse
from collections import Counter
import json,time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_hub7_residual import load_base as prior,PATH as PRIOR,TARGET,MASK,fix_hub
from search_illumination_fan_partitions import fix_fan
from project_illumination_forced_c_pairs import fix_pair,GATE
from search_illumination_midpoint_covers import one_pass,find_one_pass
from search_illumination_three_two_star import add_guard,room_from,typed_exceptions
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of

PATH=OUT/'forced-c-cases-1-1.json'


def load_base():
    mp=OUT/'forced-c-pairs-proof-inputs-1-1.json';manifest=json.loads(mp.read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    model,ts,x,bounded,terms,keys,ids,seeds,fans,_=prior();saved=json.loads(PRIOR.read_text());audit=json.loads((OUT/'hub7-residual-audit-1-1.json').read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PRIOR)
    for r in saved['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==audit['total_guards']==3379
    seeds=seeds+[dict(room=r['room'],witness=r['witness']) for r in saved['records']]
    projected=json.loads((OUT/'forced-c-pairs-1-1.json').read_text());receipt=json.loads((OUT/'forced-c-pairs-audit-1-1.json').read_text())
    assert receipt['status']=='PASS' and receipt['source_sha256']==digest(OUT/'forced-c-pairs-1-1.json') and receipt['pair_projection_complete']
    assert len(projected['classes'])==receipt['listed_pairs']==6
    prov=dict(manifest_sha256=digest(mp),projection_audit_sha256=digest(OUT/'forced-c-pairs-audit-1-1.json'))
    return model,ts,x,bounded,terms,keys,ids,seeds,fans,projected['classes'],prov


def fix_branch(model,x,terms,ids,fans):
    fix_hub(model,x,ids,MASK);fix_fan(model,x,fans['tip_triangle_ids'],5)
    model.add(terms['defect_at'][1,0]==2);model.add(terms['defect_at'][2,1]==1)


def run(seconds):
    assert not PATH.exists();begin=time.monotonic();model,ts,x,bounded,terms,keys,ids,seeds,fans,choices,prov=load_base();initial=len(keys);owners=owners_of(ts)
    library=[d for d,n in Counter(tuple(r['witness']['direction']) for r in seeds).most_common()];records=[];classes=[]
    solver=solver_for(seconds,409);solver.parameters.cp_model_presolve=False
    def save():
        result=dict(provenance=prov,records=records,classes=classes,summary=dict(base_guards=initial,new_records=len(records),new_guards=len(keys)-initial,total_guards=len(keys),complete_partition_size=len(choices),visited=len(classes),exhausted_cases=sum(c['exhausted'] for c in classes),seconds=time.monotonic()-begin,scope='Six complete typed-pair cases under hub191/tip5; exact sufficient one-pass rays only. Finite misses/caps leave their cases unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH);return result['summary']
    for number,choice in enumerate(choices,1):
        pair=tuple(map(tuple,choice['pair']));branch=model.clone();fix_branch(branch,x,terms,ids,fans);fix_pair(branch,terms,pair)
        start=time.monotonic();deadline=start+seconds;status=None;unresolved=None;before=len(records)
        while time.monotonic()<deadline:
            solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(branch)
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
            room=room_from(TARGET,ts,x,solver);assert typed_exceptions(room)==tuple(sorted(pair+(GATE,)))
            witness,screen=find_one_pass(room,library,deadline)
            if witness is None:unresolved=dict(room=room,screen=screen);break
            library=[tuple(witness['direction'])]+library;guards=[]
            for data,w in orbit(room,witness):
                one_pass(data,w);facts=tile_facts(ts,owners,w,data);key=tuple(facts)
                if key in keys:continue
                keys.add(key);add_guard(model,x,key);add_guard(branch,x,key);guards.append(dict(room=data,witness=w,tile_facts=facts))
            assert guards
            records.append(dict(case_number=number,pair=pair,room=room,witness=witness,derived_guards=guards,direction_screen=screen))
        if status!=cp_model.INFEASIBLE:
            solver.parameters.max_time_in_seconds=5;status=solver.solve(branch)
        classes.append(dict(case_number=number,pair=pair,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,new_records=len(records)-before,seconds=time.monotonic()-start,unresolved=unresolved))
        print(json.dumps(dict(event='case_complete',case_number=number,**save())),flush=True)
    print(json.dumps(dict(event='complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=30);run(ap.parse_args().seconds)
