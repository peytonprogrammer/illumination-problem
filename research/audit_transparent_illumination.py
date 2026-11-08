import json,sys,hashlib
from pathlib import Path
from collections import Counter
from illumination_geometry import check,patch,owners_of,edge,save
from illumination_paths import find_path
from verify_illumination_paths import verify
from illumination_path_cuts import path_facts
from illumination_group import describe

base=Path(__file__).parent
names=['transparent-two-screen','transparent-one-wide','transparent-simple-wide','transparent-one-pathcuts','transparent-simple-pathcuts']
unique={};summaries=[]
def key(d):
    return (tuple(sorted(tuple(sorted(map(tuple,t))) for t in d['triangles'])),tuple(sorted(edge(*e) for e in d['slits'])),tuple(map(tuple,d['marked'])))
for name in names:
    f=json.loads((base/(name+'-screen.json')).read_text());summaries.append(dict(name=name,**f['summary']))
    for record in f['records']:
        assert record['witness']['status']=='illuminated'
        k=key(record['room'])
        if k not in unique or record['witness']['bounces']<unique[k]['witness']['bounces']:unique[k]=record
for record in unique.values():
    r=check(record['room'],strict=False);assert r['walls']==record['walls'];verify(record['room'],record['witness'])
# Validate that local path facts preserve witnesses under unrelated tile/edge changes.
mutations=0;facts_audited=0
f=json.loads((base/'transparent-simple-pathcuts-screen.json').read_text())
for record in f['records'][:20]:
    data=record['room'];w=record['witness'];ts=patch(*data['search']['bounds']);owners=owners_of(ts);shared={e:o for e,o in owners.items() if len(o)==2};chosen={tuple(sorted(map(tuple,t))) for t in data['triangles']};cuts={edge(*e) for e in data['slits']}
    selected=[int(t in chosen) for t in ts];opened={e:int(all(ts[i] in chosen for i in os) and e not in cuts) for e,os in shared.items()}
    facts=path_facts(ts,owners,shared,w,selected,opened);facts_audited+=1
    for i in range(len(ts)):
        if ('tile',i) in facts:continue
        new_chosen=chosen^{ts[i]};newcuts={e for e in cuts if all(ts[j] in new_chosen for j in shared[e])};ns=[int(t in new_chosen) for t in ts];no={e:int(all(ts[j] in new_chosen for j in os) and e not in newcuts) for e,os in shared.items()}
        if not all((ns[k] if kind=='tile' else no[k])==v for (kind,k),v in facts.items()):continue
        changed=dict(data,triangles=list(new_chosen),slits=list(newcuts));verify(changed,w);mutations+=1
    for e,os in shared.items():
        if ('open',e) in facts or not all(selected[i] for i in os):continue
        newcuts=cuts^{e};changed=dict(data,slits=list(newcuts));verify(changed,w);mutations+=1
# Exact group result for every distinct room, not just modular sampling.
groups=Counter(describe(v['room'])['full_even_translation_D4_group'] for v in unique.values())
result=dict(status='PASS',distinct_geometries=len(unique),independent_paths_verified=len(unique),walls=Counter(v['walls'] for v in unique.values()),transparent_counts=Counter(len(v['transparent']) for v in unique.values()),max_reflections=max(v['witness']['bounces'] for v in unique.values()),full_affine_group_counts={str(k):v for k,v in groups.items()},path_cut_patterns_audited=facts_audited,unrelated_mutations_preserving_paths=mutations,runs=summaries)
save(base/'transparent-final-audit.json',result);print(json.dumps(result,indent=2))
