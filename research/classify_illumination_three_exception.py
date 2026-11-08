"""Project the four remaining audited ray parents onto typed exception triples."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from ortools.sat.python import cp_model
from illumination_cover import D4, mat
from illumination_three_two_star_bound import validate
from search_illumination_three_two_star import (
    add_guard, fix_triple, make_model, room_from, triple_orbit, typed_exceptions,
)

BASE = Path(__file__).parent
OUT = BASE / 'three-triples'
REMAINING = ((1, 1), (2, 0), (2, 1), (2, 2))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solver_for(seconds, seed=17):
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 2
    solver.parameters.random_seed = seed
    solver.parameters.max_time_in_seconds = seconds
    return solver


def model_with_audited_cuts(target):
    source_path = BASE / 'three-two-star' / f'case-{target[0]}-{target[1]}.json'
    audit_path = BASE / 'three-two-star' / 'audit.json'
    source = json.loads(source_path.read_text())
    audit = json.loads(audit_path.read_text())
    assert audit['status'] == 'PASS'
    receipt = next(c for c in audit['cases'] if tuple(c['target_A_cell']) == target)
    assert receipt['status'] == 'PASS' and receipt['source_sha256'] == digest(source_path)
    model, ts, x, bounded, terms = make_model(target)
    assert hashlib.sha256(json.dumps(ts).encode()).hexdigest() == source['summary']['triangle_index_sha256']
    keys = set()
    for facts in ([s['tile_facts'] for s in source['seeds']] +
                  [g['tile_facts'] for r in source['records'] for g in r['derived_guards']]):
        key = tuple(map(tuple, facts))
        assert key not in keys
        keys.add(key)
        add_guard(model, x, facts)
    assert len(keys) == receipt['exact_rays_checked'] == source['summary']['cuts']
    provenance = dict(source_file=str(source_path.relative_to(BASE)), source_sha256=digest(source_path),
                      prior_audit_sha256=digest(audit_path),
                      triangle_index_sha256=source['summary']['triangle_index_sha256'],
                      seed_cuts=len(keys))
    return model, ts, x, bounded, terms, provenance, keys


def block_triple(model, terms, triple):
    model.add_forbidden_assignments([terms['defect_at'][p[:2]] for p in triple],
                                    [[p[2] for p in triple]])


def observed():
    rows = []
    for target in REMAINING:
        data = json.loads((BASE/'three-two-star'/f'case-{target[0]}-{target[1]}.json').read_text())
        counts = Counter(min(triple_orbit(target, typed_exceptions(r['room']))) for r in data['records'])
        rows.append(dict(target_A_cell=target, configurations=len(data['records']),
                         observed_classes=len(counts),
                         groups=[dict(canonical=k, configurations=v) for k,v in sorted(counts.items())]))
    (OUT/'observed.json').write_text(json.dumps(rows, indent=2)+'\n')
    return rows


def project(target, seconds=90, limit=2000, additional_search=None):
    started = time.monotonic()
    model, ts, x, _, terms, provenance, _ = model_with_audited_cuts(target)
    additional=None
    if additional_search:
        additional_path=Path(additional_search).resolve()
        learned=json.loads(additional_path.read_text())
        assert learned['summary']['provenance']==provenance
        for record in learned['records']:
            for guard in record['derived_guards']:
                add_guard(model,x,guard['tile_facts'])
        additional=dict(file=str(additional_path.relative_to(BASE)),sha256=digest(additional_path),
                        guards=learned['summary']['additional_cuts'])
    physical = tuple(2*v for v in target)
    for g in D4:
        for swap in (False, True):
            if mat(g, physical) != tuple(-v if swap else v for v in physical):
                continue
            shift = physical if swap else (0,0)
            assert {tuple(sorted(tuple(mat(g,p)[k]+shift[k] for k in (0,1)) for p in t))
                    for t in ts} == set(ts)
    path = OUT/f'projection-{target[0]}-{target[1]}.json'
    prior = json.loads(path.read_text()) if path.exists() else None
    classes = prior['classes'] if prior else []
    if prior:
        assert prior['summary']['provenance'] == provenance
        if prior['summary']['complete']:
            print(json.dumps(dict(event='reuse_projection', **prior['summary'])), flush=True)
            return prior['summary']
        for group in classes:
            for triple in group['orbit']:
                block_triple(model, terms, tuple(map(tuple,triple)))
    seen = {tuple(map(tuple,g['canonical'])) for g in classes}
    solver = solver_for(seconds)
    status = None
    reason = 'class_limit'
    begin = time.monotonic()
    def save():
        summary = dict(target_A_cell=target, complete=status==cp_model.INFEASIBLE,
                       solver_status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                       stop_reason=reason, classes=len(classes), seconds=time.monotonic()-started,
                       provenance=provenance,
                       additional_ray_source=additional,
                       scope='Projection of possible counterexamples after audited positive-ray cuts. A cap leaves unlisted classes unresolved.')
        temporary = path.with_suffix('.tmp')
        temporary.write_text(json.dumps(dict(summary=summary,classes=classes),indent=2)+'\n')
        temporary.replace(path)
        return summary
    for _ in range(limit):
        remaining = seconds-(time.monotonic()-begin)
        if remaining<=0:
            reason='time_limit'
            break
        solver.parameters.max_time_in_seconds=remaining
        status=solver.solve(model)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            reason='exhausted' if status==cp_model.INFEASIBLE else 'solver_unknown'
            break
        room=room_from(target,ts,x,solver)
        triple=typed_exceptions(room)
        actual=tuple(sorted((p[0],p[1],solver.value(v)) for p,v in terms['defect_at'].items() if solver.value(v)))
        assert triple==actual
        orbit=triple_orbit(target,triple)
        assert min(orbit) not in seen
        seen.add(min(orbit))
        validate(room,target)
        classes.append(dict(triple=triple,canonical=min(orbit),orbit=orbit,witness_room=room))
        for other in orbit:
            block_triple(model,terms,other)
        if len(classes)%10==0:
            print(json.dumps(dict(event='projected',**save())),flush=True)
    result=save()
    print(json.dumps(dict(event='projection_complete',**result)),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--target',type=int,nargs=2)
    ap.add_argument('--seconds',type=float,default=90)
    ap.add_argument('--observed-only',action='store_true')
    ap.add_argument('--additional-search')
    args=ap.parse_args()
    if args.observed_only:
        print(json.dumps(observed()))
    else:
        for t in ([tuple(args.target)] if args.target else REMAINING):
            project(t,args.seconds,additional_search=args.additional_search)
