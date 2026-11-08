"""Learn sufficient one-pass rays on the reconciled canonical seven-tile hub."""
import argparse
from collections import Counter
import json,time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import BASE,OUT,digest,solver_for
from search_illumination_midpoint_1_1 import load_base as original,PATH as PRIOR,TARGET
from search_illumination_midpoint_covers import one_pass,find_one_pass
from search_illumination_three_two_star import add_guard,room_from
from search_illumination_one_exception import orbit,tile_facts
from illumination_geometry import owners_of
from illumination_triple_cell_sets import refine_connected_cells
from illumination_three_two_star_bound import validate

PATH=OUT/'hub7-search-1-1.json'
MASK=191


def fix_hub(model,x,ids,mask):
    for j,i in enumerate(ids):model.add(x[i]==(mask>>j&1))


def load_base():
    manifest_path=OUT/'midpoint-proof-inputs-1-1.json';manifest=json.loads(manifest_path.read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    model,ts,x,bounded,terms,keys,seeds,prov=original()
    current=json.loads(PRIOR.read_text());hub=json.loads((OUT/'hub-analysis-1-1.json').read_text())
    audit=json.loads((OUT/'midpoint-audit-1-1.json').read_text())
    assert current['provenance']==prov and hub['status']==audit['status']=='PASS'
    assert hub['current_audit_sha256']==digest(OUT/'midpoint-audit-1-1.json') and audit['source_sha256']==digest(PRIOR)
    extras=current['seed_guards']+[g for r in current['records'] for g in r['derived_guards']]+hub['restored_guards']
    for g in extras:
        key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==hub['total_guards']==2963
    refine_connected_cells(TARGET,model,terms)
    ids=[i for i,t in enumerate(ts) if (1,1) in t];assert ids==hub['hub_triangle_ids']
    seed_rays=seeds+[dict(room=r['room'],witness=r['witness']) for r in current['records']]
    provenance=dict(manifest_sha256=digest(manifest_path),prior_audit_sha256=digest(OUT/'midpoint-audit-1-1.json'),hub_audit_sha256=digest(OUT/'hub-analysis-1-1.json'))
    return model,ts,x,bounded,terms,keys,ids,seed_rays,provenance


def run(seconds):
    assert not PATH.exists(),'Preserve earlier outputs.'
    begin=time.monotonic();model,ts,x,bounded,terms,keys,ids,seeds,provenance=load_base();initial=len(keys)
    branch=model.clone();fix_hub(branch,x,ids,MASK);owners=owners_of(ts)
    freq=Counter(tuple(r['witness']['direction']) for r in seeds);library=[d for d,n in freq.most_common()]
    solver=solver_for(seconds,337);solver.parameters.cp_model_presolve=False;deadline=time.monotonic()+seconds;status=None;records=[];unresolved=None
    def save():
        result=dict(provenance=provenance,hub_mask=MASK,records=records,unresolved=unresolved,summary=dict(status=solver.status_name(status) if status is not None else 'NOT_SOLVED',exhausted=status==cp_model.INFEASIBLE,base_guards=initial,new_records=len(records),new_guards=len(keys)-initial,total_guards=len(keys),seconds=time.monotonic()-begin,scope='Merged historical-cut parent fixed to hub191 plus exact sufficient one-pass conditions. Caps and finite-direction misses unresolved.'))
        tmp=PATH.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2)+'\n');tmp.replace(PATH);return result['summary']
    print(json.dumps(dict(event='start',**save())),flush=True)
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
        records.append(dict(room=room,witness=witness,counts=validate(room,TARGET),derived_guards=guards,direction_screen=screen))
        if len(records)%20==0:print(json.dumps(dict(event='progress',**save())),flush=True)
    if status!=cp_model.INFEASIBLE:
        solver.parameters.max_time_in_seconds=30;status=solver.solve(branch)
    print(json.dumps(dict(event='complete',**save())),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=180);run(ap.parse_args().seconds)
