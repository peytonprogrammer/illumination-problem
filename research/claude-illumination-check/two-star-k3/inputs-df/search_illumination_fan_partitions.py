"""Complete local-fan refinements of the frozen target (2,1) cell partition."""
import argparse
import json
import time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT, digest, solver_for
from illumination_geometry import local_sectors, owners_of
from illumination_paths import find_path
from illumination_sector_paths import verify
from illumination_three_two_star_bound import validate
from search_illumination_cell_partitions import load_parent, fix_cells, room_outside
from search_illumination_one_exception import orbit, tile_facts
from search_illumination_three_two_star import add_guard, room_from

TARGET=(2,1)
CELL=(1,0)
PATH=OUT/'fan-search-2-1.json'

def load_seed():
    model,ts,x,bounded,terms,provenance,keys,choices=load_parent(TARGET)
    source=OUT/'cell-search-2-1.json'
    saved=json.loads(source.read_text())
    receipt_path=OUT/'cell-audit-2-1.json'
    receipt=json.loads(receipt_path.read_text())
    assert receipt['status']=='PASS' and receipt['source_sha256']==digest(source)
    assert saved['summary']['provenance']==provenance
    for record in saved['records']:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']))
            assert key not in keys
            keys.add(key);add_guard(model,x,guard['tile_facts'])
    residual=[tuple(map(tuple,c['outside_cells'])) for c in receipt['classes'] if c['status']!='INFEASIBLE']
    assert len(residual)==5 and set(residual)<=set(choices)
    provenance=dict(parent=provenance,cell_search_sha256=digest(source),cell_audit_sha256=digest(receipt_path))
    return model,ts,x,bounded,terms,keys,residual,provenance

def fan_masks(ts,cell=CELL):
    p=tuple(2*v for v in cell)
    ids=[i for i,t in enumerate(ts) if p in t]
    assert len(ids)==8
    masks=[]
    for mask in range(256):
        chosen=[ts[i] for j,i in enumerate(ids) if mask>>j&1]
        es=owners_of(chosen)
        sizes,full=local_sectors(chosen,p,{e for e,os in es.items() if len(os)==2})
        if len(sizes)<=1 and not full:masks.append(mask)
    assert len(masks)==57 and 0 in masks and 255 not in masks
    return ids,masks

def fix_fan(model,x,ids,mask):
    for j,i in enumerate(ids):model.add(x[i]==(mask>>j&1))

def run(seconds,final_seconds):
    begin=time.monotonic()
    model,ts,x,bounded,terms,seed_keys,residual,provenance=load_seed()
    ids,masks=fan_masks(ts)
    previous=json.loads(PATH.read_text()) if PATH.exists() else None
    if previous:assert previous['provenance']==provenance
    records=previous['records'] if previous else []
    prior={(tuple(map(tuple,c['outside_cells'])),c['mask']):c for c in previous['classes']} if previous else {}
    seen=set(seed_keys)
    for record in records:
        for guard in record['derived_guards']:
            key=tuple(map(tuple,guard['tile_facts']));assert key not in seen
            seen.add(key);add_guard(model,x,guard['tile_facts'])
    outcomes=[];owners=owners_of(ts);solver=solver_for(seconds,101);global_status=None
    def save():
        visited={(tuple(map(tuple,c['outside_cells'])),c['mask']) for c in outcomes}
        retained=outcomes+[c for key,c in prior.items() if key not in visited]
        summary=dict(target_A_cell=TARGET,fan_cell=CELL,fan_triangle_ids=ids,masks=masks,
                     residual_cell_sets=residual,partition_size=len(residual)*len(masks),
                     visited=len(retained),excluded=sum(c['exhausted'] for c in retained),
                     records=len(records),new_guards=len(seen)-len(seed_keys),seconds=time.monotonic()-begin,
                     global_status=solver.status_name(global_status) if global_status is not None else 'NOT_SOLVED')
        temp=PATH.with_suffix('.tmp');temp.write_text(json.dumps(dict(summary=summary,provenance=provenance,classes=retained,records=records),indent=2)+'\n');temp.replace(PATH)
        return summary
    for outside in residual:
        for mask in masks:
            if prior.get((outside,mask),{}).get('exhausted'):
                outcomes.append(prior[outside,mask]);continue
            branch=model.clone();fix_cells(branch,terms,bounded,outside);fix_fan(branch,x,ids,mask)
            start=time.monotonic();status=None;survivor=None;before=len(records)
            while time.monotonic()-start<seconds:
                solver.parameters.max_time_in_seconds=max(.001,seconds-(time.monotonic()-start))
                status=solver.solve(branch)
                if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
                room=room_from(TARGET,ts,x,solver)
                assert room_outside(room,TARGET)==outside
                witness=find_path(room,16,1000)
                if witness['status']!='illuminated':witness=find_path(room,32,2000)
                if witness['status']!='illuminated':
                    survivor=dict(room=room,bounded_screen=witness);break
                verify(room,witness);guards=[]
                for changed,ray in orbit(room,witness):
                    verify(changed,ray);facts=tile_facts(ts,owners,ray,changed);key=tuple(facts)
                    if key in seen:continue
                    seen.add(key);guards.append(dict(room=changed,witness=ray,tile_facts=facts))
                    add_guard(model,x,facts);add_guard(branch,x,facts)
                assert guards
                records.append(dict(room=room,witness=witness,counts=validate(room,TARGET),outside_cells=outside,mask=mask,derived_guards=guards))
            outcomes.append(dict(outside_cells=outside,mask=mask,status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                                 exhausted=status==cp_model.INFEASIBLE,new_records=len(records)-before,seconds=time.monotonic()-start,survivor=survivor))
            summary=save()
            print(json.dumps(dict(event='fan_branch',outside_cells=outside,mask=mask,visited=summary['visited'],excluded=summary['excluded'],records=summary['records'],status=outcomes[-1]['status'])),flush=True)
    solver.parameters.max_time_in_seconds=final_seconds;global_status=solver.solve(model)
    summary=save();print(json.dumps(dict(event='fan_complete',**summary)),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=1);ap.add_argument('--final-seconds',type=float,default=30)
    args=ap.parse_args();run(args.seconds,args.final_seconds)
