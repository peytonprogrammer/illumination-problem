"""Exact necessary local-fan propagation for the surviving typed interior pair."""
from collections import defaultdict
import json
from classify_illumination_three_exception import BASE,OUT,digest
from illumination_geometry import label,owners_of,local_sectors,check_fan_angles
from search_illumination_three_two_star import add_guard,typed_exceptions
from search_illumination_thin_tip_extension import load_base as prior,PATH as PRIOR

PAIR=((1,2,2),(2,3,2))
PATH=OUT/'interior-pair-1-1.json'


def load_base():
    mp=OUT/'thin-tip-extension-proof-inputs-1-1.json';manifest=json.loads(mp.read_text())
    for name,h in manifest['sha256'].items():assert digest(BASE.parent/name)==h,name
    model,ts,x,bounded,terms,keys,ids,seeds,fans,choices,prov=prior()
    saved=json.loads(PRIOR.read_text());audit=json.loads((OUT/'thin-tip-extension-audit-1-1.json').read_text())
    assert audit['status']=='PASS' and audit['source_sha256']==digest(PRIOR)
    for r in saved['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key);add_guard(model,x,key)
    assert len(keys)==audit['total_guards']==3867
    seeds=seeds+[dict(room=r['room'],witness=r['witness']) for r in saved['records']]
    return model,ts,x,bounded,terms,keys,ids,seeds,fans,choices,dict(prov,extension_manifest_sha256=digest(mp))


def run():
    model,ts,x,bounded,terms,keys,hub,seeds,fans,choices,prov=load_base()
    incident=defaultdict(list)
    for i,t in enumerate(ts):
        for p in t:incident[p].append(i)
    wanted={(1,2):2,(2,3):2,(2,1):1};fulls={(0,0),(2,2)};tables={};checked=0
    for p,ids in sorted(incident.items()):
        rows=[]
        for mask in range(1<<len(ids)):
            chosen=[ts[i] for j,i in enumerate(ids) if mask>>j&1];os=owners_of(chosen);opens={e for e,o in os.items() if len(o)==2}
            sizes,full=local_sectors(chosen,p,opens);assert (sorted(sizes),full)==check_fan_angles(chosen,p,os,opens);checked+=1
            if len(sizes)>1:continue
            if label(p)=='A' and full!=(p in fulls):continue
            defect=(2 if full else 1) if label(p)!='A' and (full or 4 in sizes) else 0
            if defect!=wanted.get(p,0):continue
            rows.append(mask)
        tables[p]=rows
    fixed={i:1 for i,t in enumerate(ts) if fulls&set(t)}
    for ids,mask in [(hub,191),(fans['tip_triangle_ids'],4)]:
        for j,i in enumerate(ids):
            value=(mask>>j)&1;assert i not in fixed or fixed[i]==value;fixed[i]=value
    initial=dict(fixed);steps=[];rounds=0
    while True:
        rounds+=1;new=0
        for p,ids in sorted(incident.items()):
            valid=[m for m in tables[p] if all(i not in fixed or (m>>j&1)==fixed[i] for j,i in enumerate(ids))]
            assert valid,('local contradiction',p)
            tables[p]=valid
            for j,i in enumerate(ids):
                bits={m>>j&1 for m in valid}
                if len(bits)==1 and i not in fixed:
                    fixed[i]=next(iter(bits));steps.append(dict(vertex=p,index=i,value=fixed[i],compatible_masks=valid,round=rounds));new+=1
        if not new:break
    controls=[]
    audit=json.loads((OUT/'thin-tip-extension-audit-1-1.json').read_text())
    for c in audit['cases']:
        if c['pair']!=list(map(list,PAIR)) or not c['survivor']:continue
        room=c['survivor'];selected={tuple(sorted(map(tuple,t))) for t in room['triangles']}
        assert typed_exceptions(room)==tuple(sorted(PAIR+((2,1,1),)))
        assert all(int(ts[i] in selected)==v for i,v in fixed.items());controls.append(c['case_number'])
    assert controls
    rows=[dict(vertex=p,label=label(p),triangle_ids=ids,masks=tables[p],triangle_counts=[m.bit_count() for m in tables[p]],fixed_bits=sum(i in fixed for i in ids)) for p,ids in sorted(incident.items()) if label(p)=='A' and any(fixed.get(i)==1 for i in ids)]
    result=dict(status='PASS',provenance=prov,pair=PAIR,gate=(2,1,1),base_guards=len(keys),independent_local_mask_checks=checked,propagation_rounds=rounds,initial_fixed_tiles=len(initial),fixed_present=sum(fixed.values()),fixed_absent=len(fixed)-sum(fixed.values()),fixed_facts=sorted(fixed.items()),propagation_steps=steps,forced_A_fans=rows,accepted_saved_controls=controls,scope='Necessary finite local geometry only; independent angular and adjacency checks agree. Fixed typed-pair branch only, unlisted complement remains open. No new ray conditions or global exclusion.')
    PATH.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['provenance','propagation_steps','fixed_facts']}),flush=True)


if __name__=='__main__':run()
