"""Recheck geometry, exact rays, and symmetry cuts for placement sweeps."""
import json,sys
from pathlib import Path
from illumination_geometry import check,patch,owners_of,edge,save
from illumination_symmetry import orbit
from illumination_path_cuts import path_facts
from verify_illumination_paths import verify
base=Path(__file__).parent
names=sys.argv[1:] or ['placement-22-simple-symmetric','placement-42-simple-symmetric','placement-44-simple-symmetric','placement-22-slit-symmetric']
results=[];allkeys=set()
for name in names:
    run=json.loads((base/(name+'-screen.json')).read_text());args=run['summary']['args'];ts=patch(*args['bounds']);owners=owners_of(ts);shared={e:o for e,o in owners.items() if len(o)==2};keys=set();paths=0;mutations=0
    for index,record in enumerate(run['records']):
        data=record['room'];ray=record['witness'];r=check(data,strict=False);assert r['walls']==record['walls']<=args['max_walls'];assert len(r['transparent_vertices'])<=args['transparent_budget'];assert data['marked']==[[0,0],args['target']]
        chosen={tuple(sorted(map(tuple,t))) for t in data['triangles']};assert chosen<=set(ts)
        key=(tuple(map(tuple,data['marked'])),tuple(sorted(chosen)),tuple(sorted(tuple(sorted(map(tuple,e))) for e in data['slits'])));keys.add(key);allkeys.add(key)
        variants=orbit(data,ray) if args['symmetry_cuts'] else [(data,ray)]
        for changed,witness in variants:
            check(changed,strict=False);verify(changed,witness);paths+=1
            chosen={tuple(sorted(map(tuple,t))) for t in changed['triangles']};cuts={edge(*e) for e in changed['slits']};selected=[int(t in chosen) for t in ts];opened={e:int(all(ts[i] in chosen for i in os) and e not in cuts) for e,os in shared.items()};facts=path_facts(ts,owners,shared,witness,selected,opened)
            if index<3:
                for i,t in enumerate(ts):
                    if ('tile',i) in facts:continue
                    modified=chosen^{t};ns=[int(t in modified) for t in ts];no={e:int(all(ts[j] in modified for j in os) and e not in cuts) for e,os in shared.items()}
                    if not all((ns[k] if kind=='tile' else no[k])==v for (kind,k),v in facts.items()):continue
                    verify(dict(changed,triangles=list(modified)),witness);mutations+=1
        if (index+1)%50==0:print(json.dumps(dict(event='progress',run=name,records=index+1,paths=paths)),flush=True)
    results.append(dict(run=name,records=len(run['records']),distinct_rooms=len(keys),verified_paths=paths,rebuilt_cuts=paths,unrelated_mutations=mutations,max_reflections=max((r['witness']['bounces'] for r in run['records']),default=0),summary=run['summary']))
result=dict(status='PASS',distinct_rooms=len(allkeys),runs=results);save(base/'placement-final-audit.json',result);print(json.dumps(result),flush=True)
