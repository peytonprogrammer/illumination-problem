"""Exact-ray synthesis on the union of two audited residual tip fans."""
import argparse
from collections import Counter
import json,time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_hub7_fan_cover import load_base as prior,PATH as PRIOR,TARGET,MASK,fix_hub
from search_illumination_midpoint_covers import one_pass,find_one_pass
from search_illumination_three_two_star import add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_three_two_star_bound import validate

PATH=OUT/'hub7-residual-search-1-1.json'


def load_base():
    mp=OUT/'hub7-fan-proof-inputs-1-1.json';manifest=json.loads(mp.read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    model,ts,x,bounded,terms,keys,ids,seeds,fans,_=prior();saved=json.loads(PRIOR.read_text());audit=json.loads((OUT/'hub7-fan-audit-1-1.json').read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PRIOR)
    assert {c['tip_mask'] for c in audit['fan_cases'] if c['status']!='INFEASIBLE'}=={4,5}
    for r in saved['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==audit['total_guards']==3259
    seeds=seeds+[dict(room=r['room'],witness=r['witness']) for r in saved['records']]
    prov=dict(prior_manifest_sha256=digest(mp),prior_audit_sha256=digest(OUT/'hub7-fan-audit-1-1.json'),fan_partition_sha256=digest(OUT/'hub7-fans-1-1.json'))
    return model,ts,x,bounded,terms,keys,ids,seeds,fans,prov


def run(seconds):
    assert not PATH.exists();start=time.monotonic();model,ts,x,bounded,terms,keys,ids,seeds,fans,prov=load_base();initial=len(keys);owners=owners_of(ts)
    branch=model.clone();fix_hub(branch,x,ids,MASK);tip=fans['tip_triangle_ids']
    rows=[[(m>>j)&1 for j in range(8)] for m in [4,5]];assert [j for j in range(8) if rows[0][j]!=rows[1][j]]==[0]
    branch.add_allowed_assignments([x[i] for i in tip],rows)
    old=json.loads((OUT/'hub7-fan-audit-1-1.json').read_text());prior_status={c['tip_mask']:c['status'] for c in old['fan_cases']}
    library=[d for d,n in Counter(tuple(r['witness']['direction']) for r in seeds).most_common()]
    solver=solver_for(seconds,379);solver.parameters.cp_model_presolve=False;deadline=time.monotonic()+seconds;status=None;records=[];unresolved=None
    def save():
        name=solver.status_name(status) if status is not None else 'NOT_SOLVED'
        classes=[dict(tip_mask=m,status=name if m in [4,5] else prior_status[m],exhausted=(status==cp_model.INFEASIBLE) if m in [4,5] else prior_status[m]=='INFEASIBLE',via='residual_union' if m in [4,5] else 'frozen_prior_fan_exclusion') for m in fans['compatible_fan_masks']]
        result=dict(provenance=prov,records=records,classes=classes,unresolved=unresolved,summary=dict(status=name,exhausted=status==cp_model.INFEASIBLE,base_guards=initial,new_records=len(records),new_guards=len(keys)-initial,total_guards=len(keys),seconds=time.monotonic()-start,scope='Hub191 and exact residual tip masks4/5. Five other tip branches previously excluded in the same historical-cut parent. Caps and finite misses unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH);return result['summary']
    print(json.dumps(dict(event='start',**save())),flush=True)
    while time.monotonic()<deadline:
        solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(branch)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
        room=room_from(TARGET,ts,x,solver);selected={tuple(sorted(map(tuple,t))) for t in room['triangles']};tipmask=sum(1<<j for j,i in enumerate(tip) if ts[i] in selected);assert tipmask in [4,5]
        witness,screen=find_one_pass(room,library,deadline)
        if witness is None:unresolved=dict(room=room,screen=screen);break
        guards=[]
        for data,w in orbit(room,witness):
            one_pass(data,w);facts=tile_facts(ts,owners,w,data);key=tuple(facts)
            if key in keys:continue
            keys.add(key);add_guard(model,x,key);add_guard(branch,x,key);guards.append(dict(room=data,witness=w,tile_facts=facts))
        assert guards
        records.append(dict(tip_mask=tipmask,room=room,witness=witness,counts=validate(room,TARGET),derived_guards=guards,direction_screen=screen))
        if len(records)%20==0:print(json.dumps(dict(event='progress',**save())),flush=True)
    if status!=cp_model.INFEASIBLE:
        solver.parameters.max_time_in_seconds=30;status=solver.solve(branch)
    print(json.dumps(dict(event='complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=180);run(ap.parse_args().seconds)
