"""Compose complete audited partitions; never infer exclusion from a capped solve."""
import json
from collections import Counter
from classify_illumination_three_exception import OUT,digest
from search_illumination_mask12 import load_base,PATH
from search_illumination_cell_partitions import load_parent
from search_illumination_fan_partitions import load_seed,fan_masks
from search_illumination_double_fans import load_base as double_base
from audit_illumination_double_fans import independent_masks
from illumination_triple_cell_sets import outside_sets


def read(name):
    return json.loads((OUT/name).read_text())


def outside(row):
    return tuple(map(tuple,row['outside_cells']))


def run():
    current=read('mask12-audit-2-1.json');source=json.loads(PATH.read_text())
    assert current['status']=='PASS' and current['source_sha256']==digest(PATH)
    model,ts,x,bounded,terms,first,second,patterns,keys,guards,provenance=load_base()
    assert current['provenance']==source['provenance']==provenance
    for r in source['records']:
        for g in r['derived_guards']:
            key=tuple(map(tuple,g['tile_facts']));assert key not in keys;keys.add(key)
    assert len(keys)==current['total_guards']==5615
    inclusion=[]
    loaders=[('cell',load_parent((2,1)),'cell-search-2-1.json','cell-audit-2-1.json'),
             ('fan',load_seed(),'fan-search-2-1.json','fan-audit-2-1.json'),
             ('double',double_base(),'double-fan-search-2-1.json','double-fan-audit-2-1.json')]
    for label,loaded,src,receipt in loaders:
        assert loaded[1]==ts
        oldkeys=set(loaded[6] if label=='cell' else loaded[5])
        oldprov=loaded[5] if label=='cell' else loaded[7] if label=='fan' else loaded[8]
        saved=read(src);audit=read(receipt)
        assert audit['status']=='PASS' and audit['source_sha256']==digest(OUT/src)
        assert audit['provenance']==oldprov,label
        for r in saved['records']:
            oldkeys.update(tuple(map(tuple,g['tile_facts'])) for g in r['derived_guards'])
        assert oldkeys<=keys,(label,len(oldkeys-keys))
        inclusion.append(dict(stage=label,guards=len(oldkeys),included_in_current=True,receipt_sha256=digest(OUT/receipt)))
    cells=read('cell-audit-2-1.json');fans=read('fan-audit-2-1.json');double=read('double-fan-audit-2-1.json');neck=read('neck-patterns-2-1.json')
    choices={tuple(sorted(c)) for c in outside_sets((2,1))[0]}
    cellrows={outside(c):c for c in cells['classes']}
    assert len(cellrows)==len(cells['classes'])==105 and set(cellrows)==choices
    first_masks=independent_masks(ts,first);second_masks=independent_masks(ts,second)
    assert first_masks==fan_masks(ts,(1,0))[1]==fans['fan_masks']
    assert second_masks==fan_masks(ts,(1,1))[1]==read('double-fan-search-2-1.json')['summary']['masks']
    residual_cells={c for c,r in cellrows.items() if r['status']!='INFEASIBLE'}
    fanrows={(outside(c),c['mask']):c for c in fans['classes']}
    assert len(fanrows)==len(fans['classes'])==285
    assert set(fanrows)=={(c,m) for c in residual_cells for m in first_masks}
    residual_fans={k for k,r in fanrows.items() if r['status']!='INFEASIBLE'}
    doublerows={(outside(c),c['first_mask'],c['second_mask']):c for c in double['classes']}
    assert len(doublerows)==len(double['classes'])==1026
    assert set(doublerows)=={(c,m,n) for c,m in residual_fans for n in second_masks}
    residual_double={k for k,r in doublerows.items() if r['status']!='INFEASIBLE'}
    assert residual_double=={(tuple(map(tuple,c)),m,n) for c,m,n in neck['raw_residual_patterns']}
    assert neck['audit_sha256']==digest(OUT/'double-fan-audit-2-1.json')
    mapping={t:i for i,t in enumerate(ts)}
    transform=lambda t:tuple(sorted((4-p[0],2-p[1]) for p in t))
    assert set(map(transform,ts))==set(ts)
    perm=[mapping[transform(t)] for t in ts]
    assert all(tuple(sorted((perm[i],v) for i,v in key)) in keys for key in keys)
    p12=[second.index(perm[i]) for i in first];p21=[first.index(perm[i]) for i in second]
    assert p12==neck['first_to_second_permutation'] and p21==neck['second_to_first_permutation']
    move=lambda m,p:sum(1<<p[j] for j in range(8) if m>>j&1)
    swap=lambda r:(tuple(sorted((2-a,1-b) for a,b in r[0])),move(r[2],p21),move(r[1],p12))
    canonical={min(r,swap(r)) for r in residual_double}
    assert len(residual_double)==24 and {swap(r) for r in residual_double}==residual_double
    assert sorted(canonical)==[(tuple(map(tuple,c)),m,n) for c,m,n in patterns]
    replays={c['neck_type']:c['status'] for c in current['cases']}
    assert set(replays)==set(range(1,13)) and all(v=='INFEASIBLE' for v in replays.values())
    numbered={r:i for i,r in enumerate(sorted(canonical),1)}
    leaves=[]
    for row in sorted(residual_double):
        number=numbered[min(row,swap(row))];assert replays[number]=='INFEASIBLE'
        leaves.append(dict(outside_cells=row[0],first_mask=row[1],second_mask=row[2],canonical_neck=number,status='INFEASIBLE',via='fresh_neck_replay_and_checked_half_turn'))
    assert sum(r['status']=='INFEASIBLE' for r in cellrows.values())==100
    assert sum(r['status']=='INFEASIBLE' for r in fanrows.values())==267
    assert sum(r['status']=='INFEASIBLE' for r in doublerows.values())==1002
    # Exhaustive nested disjunction: every remaining leaf has a checked exclusion.
    for cell in residual_cells:
        for a in first_masks:
            if fanrows[cell,a]['status']=='INFEASIBLE':continue
            for b in second_masks:
                row=(cell,a,b)
                if doublerows[row]['status']=='INFEASIBLE':continue
                assert numbered[min(row,swap(row))] in replays
    result=dict(status='PASS',placement_excluded=True,proof_method='EXHAUSTIVE_PARTITION_COMPOSITION',
                complete_cell_sets=105,earlier_cell_exclusions=100,remaining_cells_refined=5,
                complete_first_fan_branches=285,earlier_first_fan_exclusions=267,remaining_first_fans_refined=18,
                complete_second_fan_branches=1026,earlier_second_fan_exclusions=1002,
                terminal_raw_patterns=24,terminal_canonical_patterns=12,terminal_replays=leaves,
                all_105_cell_sets_excluded_by_composition=True,monotone_guard_inclusion=inclusion,
                current_guards=len(keys),current_audit_sha256=digest(OUT/'mask12-audit-2-1.json'),
                monolithic_solver_status=current['unrestricted_parent'],
                scope='Conditional on frozen complete geometry/cell/fan reductions, exact positive-ray checks, and audited CP-SAT branch exclusions. Monolithic UNKNOWN is not used as evidence. No formal UNSAT proof.')
    (OUT/'partition-closure-2-1.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='terminal_replays'}),flush=True)


if __name__=='__main__':run()
