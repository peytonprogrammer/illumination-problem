"""Independent exception extraction, symmetry checks, ray checks and replays."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
from ortools.sat.python import cp_model
from classify_illumination_two_exception import model_with_audited_cuts, REMAINING
from illumination_geometry import label, check, owners_of
from illumination_sector_paths import verify
from illumination_two_exception_bound import validate_counts, audit_cell_graph
from search_illumination_one_exception import tile_facts
from audit_illumination_one_exception import untrimmed_facts

BASE = Path(__file__).parent


def independent_pair(room):
    checked = check(room, strict=False)
    assert checked['simple_polygon']
    angles = Counter()
    for t in room['triangles']:
        for p in map(tuple, t):
            if label(p) != 'A':
                angles[p] += 2 if label(p) == 'C' else 1
    return tuple(sorted((p[0], p[1], 2 if angle == 8 else 1) for p, angle in angles.items() if angle in (4, 8)))


def independent_orbit(target, pair):
    tx, ty = (2*v for v in target)
    maps = [lambda x,y:(x,y), lambda x,y:(tx-x,ty-y)]
    if ty == 0:
        maps += [lambda x,y:(x,-y), lambda x,y:(tx-x,y)]
    elif tx == ty:
        maps += [lambda x,y:(y,x), lambda x,y:(tx-y,ty-x)]
    return tuple(sorted({tuple(sorted((*f(px,py), value) for px,py,value in pair)) for f in maps}))


def solver_for(seconds=20):
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.random_seed = 41
    return solver


def audit_case(target):
    projected_file = BASE/f'two-pair-{target[0]}-{target[1]}.json'
    search_file = BASE/f'two-pair-search-{target[0]}-{target[1]}.json'
    projection, saved = (json.loads(p.read_text()) for p in (projected_file, search_file))
    model, ts, variables, _, terms, provenance = model_with_audited_cuts(target)
    assert provenance == projection['summary']['provenance'] == saved['summary']['provenance']
    source = json.loads((BASE/provenance['source_file']).read_text())
    original_guards = {tuple(map(tuple, g['tile_facts'])) for r in source['records'] for g in r['derived_guards']}
    classes, group_keys = projection['classes'], set()
    projected_model = model.clone()
    positive_models = 0
    solver = solver_for()
    for group in classes:
        pair = independent_pair(group['witness_room'])
        assert pair == tuple(map(tuple, group['pair']))
        orbit = independent_orbit(target, pair)
        assert orbit == tuple(tuple(map(tuple, p)) for p in group['orbit'])
        assert min(orbit) == tuple(map(tuple, group['canonical']))
        assert min(orbit) not in group_keys
        group_keys.add(min(orbit))
        validate_counts(group['witness_room'])
        audit_cell_graph(group['witness_room'])
        selected = {tuple(sorted(map(tuple, t))) for t in group['witness_room']['triangles']}
        fixed = model.clone()
        for t, variable in zip(ts, variables):
            fixed.add(variable == int(t in selected))
        assert solver.solve(fixed) == cp_model.OPTIMAL
        positive_models += 1
        for ((px, py, a), (qx, qy, b)) in orbit:
            projected_model.add_forbidden_assignments([terms['defect_at'][px, py], terms['defect_at'][qx, qy]], [[a, b]])
    coverage_status = solver.solve(projected_model)
    assert projection['summary']['complete'] and coverage_status == cp_model.INFEASIBLE
    owners = owners_of(ts)
    seen_rooms, seen_guards = set(), set()
    full_comparisons = mutations = rays = 0
    for number, record in enumerate(saved['records'], 1):
        room, witness = record['room'], record['witness']
        key = tuple(sorted(tuple(sorted(map(tuple, t))) for t in room['triangles']))
        assert key not in seen_rooms
        seen_rooms.add(key)
        validate_counts(room); audit_cell_graph(room); verify(room, witness)
        assert min(independent_orbit(target, independent_pair(room))) == tuple(map(tuple, record['canonical_exception_pair']))
        for guard in record['derived_guards']:
            verify(guard['room'], guard['witness'])
            facts = tile_facts(ts, owners, guard['witness'], guard['room'])
            assert facts == list(map(tuple, guard['tile_facts']))
            fact_key = tuple(facts)
            assert fact_key not in seen_guards
            seen_guards.add(fact_key)
            model.add(sum(1-variables[i] if value else variables[i] for i, value in facts) >= 1)
            rays += 1
            if full_comparisons < 2:
                assert facts == untrimmed_facts(ts, guard['witness'], guard['room'])
                full_comparisons += 1
            if mutations < 16:
                selected = {tuple(sorted(map(tuple, t))) for t in guard['room']['triangles']}
                free = [i for i in range(len(ts)) if i not in dict(facts)]
                for i in free[:min(4,16-mutations)]:
                    changed = dict(guard['room'], triangles=sorted(selected ^ {ts[i]}))
                    verify(changed, guard['witness'])
                    mutations += 1
        if number % 50 == 0:
            print(json.dumps(dict(event='audit_rays',target=target,records=number,rays=rays)), flush=True)
    assert len(seen_guards) == saved['summary']['additional_cuts']
    claims = {tuple(map(tuple, c['canonical'])):c for c in saved['classes']}
    replayed = []
    for group in classes:
        fixed = model.clone()
        for px, py, value in group['pair']:
            fixed.add(terms['defect_at'][px, py] == value)
        status = solver.solve(fixed)
        canonical = tuple(map(tuple, group['canonical']))
        if claims.get(canonical, {}).get('exhausted'):
            assert status == cp_model.INFEASIBLE
        replayed.append(dict(canonical=group['canonical'], status=solver.status_name(status)))
    global_status = solver.solve(model)
    closed = sum(c['status'] == 'INFEASIBLE' for c in replayed)
    result = dict(target_A_cell=target, status='PASS', projection_exhaustion_replayed=True,
                  complete_exception_pair_classes=len(classes), fixed_positive_models=positive_models,
                  records=len(saved['records']), derived_rays_checked=rays,
                  distinct_additional_cuts=len(seen_guards-original_guards),
                  full_vs_clipped_comparisons=full_comparisons, guard_preserving_mutations=mutations,
                  classes_excluded_by_fresh_replay=closed, classes=replayed,
                  global_replay_status=solver.status_name(global_status),
                  excluded=global_status == cp_model.INFEASIBLE or closed == len(classes),
                  source_sha256=hashlib.sha256(search_file.read_bytes()).hexdigest(),
                  projection_sha256=hashlib.sha256(projected_file.read_bytes()).hexdigest(), provenance=provenance)
    path = BASE/f'two-pair-audit-{target[0]}-{target[1]}.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'classes'}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=int, nargs=2)
    args = parser.parse_args()
    for target in ([tuple(args.target)] if args.target else REMAINING):
        audit_case(target)
    results = []
    for target in REMAINING:
        path = BASE/f'two-pair-audit-{target[0]}-{target[1]}.json'
        search = BASE/f'two-pair-search-{target[0]}-{target[1]}.json'
        projection = BASE/f'two-pair-{target[0]}-{target[1]}.json'
        if path.exists():
            result = json.loads(path.read_text())
            if (result['source_sha256'] == hashlib.sha256(search.read_bytes()).hexdigest() and
                result['projection_sha256'] == hashlib.sha256(projection.read_bytes()).hexdigest()):
                results.append(result)
    if len(results) == len(REMAINING):
        summary = dict(status='PASS', two_exception_family='EXCLUDED' if all(r['excluded'] for r in results) else 'INCOMPLETE',
                       cases=results, scope='Composition with previous zero/one-exception, three-star, complete support and four placement audits; CP-SAT checks, no formal UNSAT proof.')
        (BASE/'two-pair-final-audit.json').write_text(json.dumps(summary, indent=2)+'\n')
