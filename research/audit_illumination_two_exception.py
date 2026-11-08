"""Bounds, clipped ray guards, and fixed-geometry model checks."""
import json
from pathlib import Path
from ortools.sat.python import cp_model
from illumination_geometry import owners_of, check
from illumination_two_exception_bound import validate_counts as counts, equality_patterns as three_vertex_boundary_check, complete_support, degree_lemma, TARGETS, audit_cell_graph
from illumination_sector_paths import verify
from search_illumination_family import build_model
from search_illumination_one_exception import tile_facts
from audit_illumination_one_exception import untrimmed_facts

BASE = Path(__file__).parent


def main():
    lemma = three_vertex_boundary_check()
    saved = json.loads((BASE/'transparent-simple-two-symmetric-screen.json').read_text())
    known = [r for r in saved['records'] if len(r['transparent']) == 2]
    for record in known:
        counts(record['room'])
        audit_cell_graph(record['room'])
    model_checks = 0
    seen_types = set()
    for record in known:
        result = counts(record['room'])
        kind = (result['interior_nonA'], result['smooth_boundary_nonA'])
        if kind in seen_types:
            continue
        seen_types.add(kind)
        room = record['room']
        target = tuple(v//2 for v in room['marked'][1])
        model, ts, variables, _, _ = build_model(target, 23, 2, complete_support(target))
        selected = {tuple(sorted(map(tuple, t))) for t in room['triangles']}
        assert selected <= set(ts)
        for t, variable in zip(ts, variables):
            model.add(variable == int(t in selected))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 5
        assert solver.solve(model) == cp_model.OPTIMAL
        model_checks += 1
    full_comparisons = mutations = rays = cases = guards = records = 0
    historical = set()
    def room_key(room):
        return (tuple(map(tuple, room['marked'])), tuple(sorted(tuple(sorted(map(tuple, t))) for t in room['triangles'])))
    for path in sorted(set(BASE.glob('transparent*-screen.json')) | set(BASE.glob('placement*-screen.json'))):
        for record in json.loads(path.read_text()).get('records', []):
            historical.add(room_key(record['room']))
    distinct, new_keys = set(), set()
    max_bounces = 0
    exhausted = []
    for path in sorted(BASE.glob('two-global-*-*.json')):
        data = json.loads(path.read_text())
        if 'summary' not in data:
            continue
        summary = data['summary']
        target = tuple(summary['target_A_cell'])
        if target not in TARGETS:
            continue
        model, ts, variables, _, _ = build_model(target, 23, 2, complete_support(target))
        owners = owners_of(ts)
        cases += 1
        case_guards = 0
        for record in data['records']:
            counts(record['room'])
            audit_cell_graph(record['room'])
            verify(record['room'], record['witness'])
            records += 1
            key = room_key(record['room'])
            distinct.add(key)
            if key not in historical:
                new_keys.add(key)
            max_bounces = max(max_bounces, record['witness']['bounces'])
            for guard in record['derived_guards']:
                room, witness = guard['room'], guard['witness']
                verify(room, witness)
                rays += 1
                facts = tile_facts(ts, owners, witness, room)
                assert facts == list(map(tuple, guard['tile_facts']))
                model.add(sum(1-variables[i] if value else variables[i]
                              for i, value in facts) >= 1)
                guards += 1
                case_guards += 1
                if full_comparisons < 3:
                    assert facts == untrimmed_facts(ts, witness, room)
                    full_comparisons += 1
                if mutations < 64:
                    fixed = dict(facts)
                    selected = {tuple(sorted(map(tuple, t))) for t in room['triangles']}
                    choices = [i for i in range(len(ts)) if i not in fixed]
                    # Include both nearby and distant unconstrained changes.
                    choices.sort(key=lambda i: min(abs(p[0])+abs(p[1]) for p in ts[i]))
                    for i in choices[:min(8, 64-mutations)]:
                        changed = dict(room, triangles=sorted(selected ^ {ts[i]}))
                        verify(changed, witness)
                        mutations += 1
        assert case_guards == summary['cuts']
        if summary['exhausted']:
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = 30
            solver.parameters.num_search_workers = 4
            assert solver.solve(model) == cp_model.INFEASIBLE
            exhausted.append(list(target))
    assert cases == len(TARGETS)
    assert len(distinct) == records
    result = dict(status='PASS', grid_lemma=lemma, degree_lemma=degree_lemma(),
                  prior_two_exception_geometries_checked=len(known),
                  fixed_models_checked=model_checks, defect_types=sorted(seen_types),
                  case_files_checked=cases, saved_room_records_checked=records, distinct_room_and_mark_configurations=len(distinct),
                  configurations_new_this_turn=len(new_keys), maximum_witness_reflections=max_bounces,
                  exact_derived_rays_checked=rays, replayed_cuts=guards,
                  full_vs_clipped_guard_comparisons=full_comparisons,
                  guard_preserving_tile_mutations_checked=mutations,
                  exhausted_cases_independently_replayed=exhausted,
                  scope='No negative conclusion from a ray miss or solver cap.')
    (BASE/'two-global-final-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
