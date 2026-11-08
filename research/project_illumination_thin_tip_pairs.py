"""Project the two free typed exceptions in the remaining thin-tip branch."""
import argparse
import json,time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_forced_c_cases import load_base as prior,PATH as PRIOR,TARGET,MASK,fix_hub
from search_illumination_fan_partitions import fix_fan
from search_illumination_three_two_star import add_guard,room_from,typed_exceptions

GATE=(2,1,1)
PATH=OUT/'thin-tip-pairs-1-1.json'


def load_base():
    mp=OUT/'forced-c-cases-proof-inputs-1-1.json';manifest=json.loads(mp.read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    model,ts,x,bounded,terms,keys,ids,seeds,fans,_,_=prior();saved=json.loads(PRIOR.read_text());audit=json.loads((OUT/'forced-c-cases-audit-1-1.json').read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PRIOR) and audit['tip5_excluded']
    for r in saved['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==audit['total_guards']==3411
    fix_hub(model,x,ids,MASK);fix_fan(model,x,fans['tip_triangle_ids'],4)
    model.add(terms['defect_at'][2,1]==1);model.add(terms['defect_at'][1,0]==0)
    seeds=seeds+[dict(room=r['room'],witness=r['witness']) for r in saved['records']]
    prov=dict(manifest_sha256=digest(mp),case_audit_sha256=digest(OUT/'forced-c-cases-audit-1-1.json'),tip_gate_sha256=digest(OUT/'tip-gate-1-1.json'))
    return model,ts,x,bounded,terms,keys,ids,seeds,fans,prov


def block_pair(model,terms,pair):
    assert len(pair)==2 and all(tuple(p[:2])!=GATE[:2] and p[2] in [1,2] for p in pair)
    model.add_forbidden_assignments([terms['defect_at'][tuple(p[:2])] for p in pair],[[p[2] for p in pair]])


def fix_pair(model,terms,pair):
    for a,b,v in pair:model.add(terms['defect_at'][a,b]==v)


def run(seconds,limit):
    assert not PATH.exists();begin=time.monotonic();model,ts,x,bounded,terms,keys,ids,seeds,fans,prov=load_base();discovery=model.clone()
    solver=solver_for(seconds,433);solver.parameters.cp_model_presolve=False;deadline=time.monotonic()+seconds;classes=[];seen=set();status=None;reason='class_limit'
    def save():
        data=dict(provenance=prov,classes=classes,summary=dict(status=solver.status_name(status) if status is not None else 'NOT_SOLVED',projection_complete=status==cp_model.INFEASIBLE,listed_pairs=len(classes),base_guards=len(keys),fixed_gate=GATE,seconds=time.monotonic()-begin,stop_reason=reason,scope='Necessary typed-pair projection after3411 positive-ray cuts. No new rays. Every capped/unlisted pair stays in an explicit residual branch.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(PATH);return data['summary']
    for _ in range(limit):
        if time.monotonic()>=deadline:reason='time_limit';break
        solver.parameters.max_time_in_seconds=max(.001,deadline-time.monotonic());status=solver.solve(discovery)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):reason='exhausted' if status==cp_model.INFEASIBLE else 'solver_cap';break
        room=room_from(TARGET,ts,x,solver);triple=typed_exceptions(room);assert GATE in triple
        actual=tuple(sorted((p[0],p[1],solver.value(v)) for p,v in terms['defect_at'].items() if solver.value(v)));assert actual==triple
        pair=tuple(p for p in triple if p!=GATE);assert len(pair)==2 and pair not in seen;seen.add(pair)
        classes.append(dict(pair=pair,positive_room=room));block_pair(discovery,terms,pair)
        if len(classes)%5==0:print(json.dumps(dict(event='projected',**save())),flush=True)
    print(json.dumps(dict(event='complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=90);ap.add_argument('--limit',type=int,default=500);args=ap.parse_args();run(args.seconds,args.limit)
