"""Independent local fan checks, exhaustive budget fixtures and room controls."""
from collections import Counter
from itertools import product
import hashlib
import json
from pathlib import Path
import random
from illumination_geometry import label,owners_of,check_fan_angles
from illumination_family_bound import triangles_in_cells
from illumination_three_two_star_bound import complete_support,validate
from illumination_neck_budget import OUT,factors_for,metric_support,propagate,connectivity_backbone


def independent_rows(ts,bounded,factor):
    p=factor['point'];ids=factor['ids'];kind=label(p);rows=[]
    for mask in range(1<<len(ids)):
        chosen=[ts[i] for j,i in enumerate(ids) if mask>>j&1]
        owners=owners_of(chosen);opened={e for e,os in owners.items() if len(os)==2}
        angles,full=check_fan_angles(chosen,p,owners,opened)
        if len(angles)>1:continue
        if kind=='A' and full!=((p[0]//2,p[1]//2) in bounded['full']):continue
        wall=sum(angle!=4 for angle in angles)
        bad=int(kind!='A' and (full or angles==[4]))
        defect=(2 if full else 1) if bad else 0
        charge=0 if kind!='A' or full or not angles else (3 if angles==[4] else angles[0])
        missing=int(kind=='A' and (p[0]//2,p[1]//2) in bounded['mandatory']-bounded['full'] and not chosen)
        rows.append((mask,wall,bad,charge-defect,len(chosen) if kind=='A' else 0,defect+missing))
    return rows


def brute_budget(options,cap,base,exceptions):
    supported=[set() for _ in options];walls=set()
    for chosen in product(*options):
        w,b,q=map(sum,zip(*chosen))
        if w<=cap and b==exceptions and q==w-base:
            walls.add(w)
            for support,option in zip(supported,chosen):support.add(option)
    return supported,sorted(walls)


def audit():
    source=OUT/'neck-budget-2-1.json';saved=json.loads(source.read_text());bounded=complete_support((2,1));ts=triangles_in_cells(bounded['allowed'])
    assert saved['triangle_index_sha256']==hashlib.sha256(json.dumps(ts).encode()).hexdigest()
    patterns_path=OUT/'neck-patterns-2-1.json';patterns=json.loads(patterns_path.read_text())['canonical_patterns']
    assert saved['source_sha256']==hashlib.sha256(patterns_path.read_bytes()).hexdigest()
    factors=factors_for(ts,bounded);local_states=0
    for f in factors:
        assert f['rows']==independent_rows(ts,bounded,f)
        local_states+=1<<len(f['ids'])
    rng=random.Random(151);pool=[(0,0,0),(1,0,0),(0,1,-1),(0,1,-2),(1,0,1),(1,0,2),(0,0,3)];positive_fixtures=0
    for _ in range(200):
        options=[rng.sample(pool,rng.randint(1,3)) for _ in range(6)]
        got=metric_support(options,cap=6,base=4,exceptions=2)
        expected=brute_budget(options,6,4,2)
        assert got==expected,(options,got,expected)
        positive_fixtures+=bool(expected[1])
    assert positive_fixtures>20
    graph_fixtures=200;connected_fixtures=0
    for _ in range(graph_fixtures):
        adjacency={i:set() for i in range(7)}
        for i in range(7):
            for j in range(i+1,7):
                if rng.random()<.3:adjacency[i].add(j);adjacency[j].add(i)
        domains=[rng.choice([1,2,3,3]) for _ in range(7)];domains[0]=2
        got=connectivity_backbone(adjacency,domains);observed=[0]*7;valid=0
        for mask in range(128):
            if any(not domains[i]&(1<<((mask>>i)&1)) for i in range(7)):continue
            selected={i for i in range(7) if mask>>i&1};seen={0};todo=[0]
            for i in todo:
                for j in adjacency[i]&selected-seen:seen.add(j);todo.append(j)
            if seen!=selected:continue
            valid+=1
            for i in range(7):observed[i]|=1<<((mask>>i)&1)
        assert (got is None)==(valid==0)
        if valid:assert got==observed;connected_fixtures+=1
    assert connected_fixtures>20
    assert len(saved['cases'])==len(patterns)==12
    for number,(case,pattern) in enumerate(zip(saved['cases'],patterns),1):
        rebuilt=propagate(ts,bounded,factors,pattern,connectivity=True);rebuilt['neck_type']=number
        assert json.loads(json.dumps(rebuilt))==case
        baseline=propagate(ts,bounded,factors,pattern);baseline['neck_type']=number
        assert json.loads(json.dumps(baseline))==saved['budget_only_baselines'][number-1]
    print(json.dumps(dict(event='budget_rules_audited',local_states=local_states,budget_fixtures=200,positive_fixtures=positive_fixtures)),flush=True)
    index={t:i for i,t in enumerate(ts)}
    first=[i for i,t in enumerate(ts) if (2,0) in t];second=[i for i,t in enumerate(ts) if (2,2) in t]
    wanted={(tuple(map(tuple,p[0])),p[1],p[2]):i for i,p in enumerate(patterns)}
    controls=[set() for _ in patterns];sources={};counts=Counter()
    names=['double-fan-search-2-1.json','ray-pattern-probe-2-1.json','fan-search-2-1.json','cell-search-2-1.json','cell-2-1-bootstrap.json']
    for name in names:
        path=OUT/name;sources[name]=hashlib.sha256(path.read_bytes()).hexdigest()
        for record in json.loads(path.read_text())['records']:
            original=record['room']
            for swapped in (False,True):
                selected={tuple(sorted((4-p[0],2-p[1]) if swapped else tuple(p) for p in t)) for t in original['triangles']}
                assert selected<=index.keys()
                actual={index[t] for t in selected}
                outside=tuple(sorted({(p[0]//2,p[1]//2) for t in selected for p in t if label(p)=='A'}-bounded['mandatory']))
                mask1=sum(1<<j for j,i in enumerate(first) if i in actual);mask2=sum(1<<j for j,i in enumerate(second) if i in actual)
                signature=(outside,mask1,mask2)
                if signature not in wanted:continue
                number=wanted[signature];key=tuple(sorted(actual))
                if key in controls[number]:continue
                room=dict(original,triangles=sorted(selected));validate(room,(2,1))
                case=saved['cases'][number];assert case['status']=='RELAXATION_FEASIBLE'
                assert all(domain&(1<<int(i in actual)) for i,domain in enumerate(case['triangle_domains']))
                for f,retained in zip(factors,case['factor_masks']):
                    assert list(f['point'])==retained['point']
                    mask=sum(1<<j for j,i in enumerate(f['ids']) if i in actual)
                    assert mask in retained['masks'],(number,f['point'],mask)
                controls[number].add(key);counts[name]+=1
    per_case=[len(c) for c in controls];assert all(per_case),('uncovered neck types',per_case)
    result=dict(status='PASS',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),local_masks_independently_checked=local_states,
                factors=len(factors),exhaustive_connectivity_fixtures=graph_fixtures,fixtures_with_connected_completion=connected_fixtures,exhaustive_budget_fixtures=200,fixtures_with_solution=positive_fixtures,recomputed_cases=12,
                distinct_room_controls=sum(per_case),controls_per_case=per_case,control_sources=sources,controls_first_seen=dict(counts),
                scope='Local-sector rows checked with independent fan graph; exact budget-support DP compared to exhaustive products on200 fixtures; all propagated consequences retain every checked valid room. Necessary relaxation only; no new global exclusion or illumination lemma.')
    (OUT/'neck-budget-audit-2-1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':audit()
