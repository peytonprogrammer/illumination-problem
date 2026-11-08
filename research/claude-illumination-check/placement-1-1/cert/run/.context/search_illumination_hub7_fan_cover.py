"""Bounded exact-ray covers of every compatible tip fan for hub191."""
import argparse
from collections import Counter
import json,time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_hub7_1_1 import load_base as prior,PATH as PRIOR,TARGET,MASK,fix_hub
from search_illumination_midpoint_covers import one_pass,find_one_pass
from search_illumination_fan_partitions import fix_fan
from search_illumination_three_two_star import add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_three_two_star_bound import validate

PATH=OUT/'hub7-fan-search-1-1.json'


def load_base():
    mp=OUT/'hub7-proof-inputs-1-1.json';manifest=json.loads(mp.read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    model,ts,x,bounded,terms,keys,ids,seeds,_=prior();saved=json.loads(PRIOR.read_text());audit=json.loads((OUT/'hub7-audit-1-1.json').read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PRIOR)
    for r in saved['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==audit['total_guards']
    seeds=seeds+[dict(room=r['room'],witness=r['witness']) for r in saved['records']]
    fans=json.loads((OUT/'hub7-fans-1-1.json').read_text());assert fans['status']=='PASS' and fans['hub_mask']==MASK
    provenance=dict(prior_manifest_sha256=digest(mp),prior_audit_sha256=digest(OUT/'hub7-audit-1-1.json'),fan_partition_sha256=digest(OUT/'hub7-fans-1-1.json'))
    return model,ts,x,bounded,terms,keys,ids,seeds,fans,provenance


def run(seconds):
    assert not PATH.exists();start=time.monotonic();model,ts,x,bounded,terms,keys,ids,seeds,fans,prov=load_base();initial=len(keys);owners=owners_of(ts)
    library=[d for d,n in Counter(tuple(r['witness']['direction']) for r in seeds).most_common()];records=[];classes=[]
    solver=solver_for(seconds,359);solver.parameters.cp_model_presolve=False
    def save():
        result=dict(provenance=prov,records=records,classes=classes,summary=dict(base_guards=initial,new_records=len(records),new_guards=len(keys)-initial,total_guards=len(keys),complete_fan_partition=fans['compatible_fan_masks'],branches_visited=len(classes),branches_exhausted=sum(c['exhausted'] for c in classes),seconds=time.monotonic()-start,scope='Complete necessary seven-fan partition of hub191; exact sufficient one-pass conditions only. Finite misses and caps unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH);return result['summary']
    for mask in fans['compatible_fan_masks']:
        branch=model.clone();fix_hub(branch,x,ids,MASK);fix_fan(branch,x,fans['tip_triangle_ids'],mask)
        begin=time.monotonic();deadline=begin+seconds;status=None;unresolved=None;before=len(records)
        while time.monotonic()<deadline:
            solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(branch)
            if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
            room=room_from(TARGET,ts,x,solver);witness,screen=find_one_pass(room,library,deadline)
            if witness is None:unresolved=dict(room=room,screen=screen);break
            guards=[]
            for data,w in orbit(room,witness):
                one_pass(data,w);facts=tile_facts(ts,owners,w,data);key=tuple(facts)
                if key in keys:continue
                keys.add(key);add_guard(model,x,key);add_guard(branch,x,key);guards.append(dict(room=data,witness=w,tile_facts=facts))
            assert guards
            records.append(dict(tip_mask=mask,room=room,witness=witness,counts=validate(room,TARGET),derived_guards=guards,direction_screen=screen))
        if status!=cp_model.INFEASIBLE:
            solver.parameters.max_time_in_seconds=5;status=solver.solve(branch)
        classes.append(dict(tip_mask=mask,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,new_records=len(records)-before,seconds=time.monotonic()-begin,unresolved=unresolved))
        print(json.dumps(dict(event='fan_complete',tip_mask=mask,**save())),flush=True)
    print(json.dumps(dict(event='complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=15);run(ap.parse_args().seconds)
