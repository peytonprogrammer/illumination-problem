"""Search fixed typed exception pairs; every new exclusion is an exact ray."""
import argparse
import json
from pathlib import Path
import time
from ortools.sat.python import cp_model
from classify_illumination_two_exception import model_with_audited_cuts, exceptional_pair, pair_orbit, REMAINING
from search_illumination_one_exception import orbit, tile_facts
from illumination_geometry import owners_of
from illumination_two_exception_bound import validate_counts
from illumination_paths import find_path
from illumination_sector_paths import verify

BASE = Path(__file__).parent


def add_guards(model, variables, guards):
    for guard in guards:
        model.add(sum(1-variables[i] if value else variables[i] for i, value in guard['tile_facts']) >= 1)


def run(target, seconds_per_class=3, final_seconds=15):
    started = time.monotonic()
    projection_file = BASE/f'two-pair-{target[0]}-{target[1]}.json'
    projection = json.loads(projection_file.read_text())
    model, ts, variables, bounded, terms, provenance = model_with_audited_cuts(target)
    assert provenance == projection['summary']['provenance']
    owners = owners_of(ts)
    filename = BASE/f'two-pair-search-{target[0]}-{target[1]}.json'
    saved = json.loads(filename.read_text()) if filename.exists() else None
    records = saved['records'] if saved else []
    if saved:
        assert saved['summary']['provenance'] == provenance
        if saved['summary']['exhausted']:
            print(json.dumps(dict(event='reuse_exhausted', **saved['summary'])), flush=True)
            return saved['summary']
    cuts = set()
    for record in records:
        for guard in record['derived_guards']:
            key = tuple(map(tuple, guard['tile_facts']))
            assert key not in cuts
            cuts.add(key)
        add_guards(model, variables, record['derived_guards'])
    outcomes = []
    prior = {tuple(map(tuple, r['canonical'])): r for r in saved['classes']} if saved else {}
    final_status = None
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    solver.parameters.random_seed = 29
    def save():
        summary = dict(target_A_cell=target, projection_complete=projection['summary']['complete'],
                       projected_classes=len(projection['classes']), classes_searched=len(outcomes),
                       classes_excluded=sum(c['exhausted'] for c in outcomes),
                       records=len(records), additional_cuts=len(cuts),
                       global_solver_status=solver.status_name(final_status) if final_status is not None else 'NOT_SOLVED',
                       exhausted=final_status == cp_model.INFEASIBLE,
                       seconds=time.monotonic()-started, provenance=provenance)
        temp = filename.with_suffix('.tmp')
        temp.write_text(json.dumps(dict(summary=summary, classes=outcomes, records=records), indent=2)+'\n')
        temp.replace(filename)
        return summary
    for group in projection['classes']:
        key = tuple(map(tuple, group['canonical']))
        if key in prior and prior[key]['exhausted']:
            outcomes.append(prior[key])
            continue
        branch = model.clone()
        pair = tuple(map(tuple, group['pair']))
        for px, py, value in pair:
            branch.add(terms['defect_at'][px, py] == value)
        class_started = time.monotonic()
        status, reason, survivor = None, 'time_limit', None
        new = 0
        while time.monotonic()-class_started < seconds_per_class:
            solver.parameters.max_time_in_seconds = max(0.001, seconds_per_class-(time.monotonic()-class_started))
            status = solver.solve(branch)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                reason = 'exhausted' if status == cp_model.INFEASIBLE else 'solver_unknown'
                break
            room = dict(triangles=[t for t, variable in zip(ts, variables) if solver.value(variable)],
                        marked=[[0, 0], [2*v for v in target]], require_simple=True)
            validate_counts(room)
            assert exceptional_pair(room) == pair
            witness = find_path(room, 16, 1000)
            if witness['status'] != 'illuminated':
                witness = find_path(room, 32, 2000)
            if witness['status'] != 'illuminated':
                reason = 'unresolved_candidate'
                survivor = dict(room=room, bounded_screen=witness)
                break
            verify(room, witness)
            guards = []
            for changed, ray in orbit(room, witness):
                verify(changed, ray)
                facts = tile_facts(ts, owners, ray, changed)
                fact_key = tuple(facts)
                if fact_key in cuts:
                    continue
                cuts.add(fact_key)
                guards.append(dict(room=changed, witness=ray, tile_facts=facts))
            assert guards
            record = dict(room=room, witness=witness, counts=validate_counts(room), derived_guards=guards,
                          canonical_exception_pair=group['canonical'])
            records.append(record)
            add_guards(model, variables, guards)
            add_guards(branch, variables, guards)
            new += 1
        outcome = dict(pair=pair, canonical=group['canonical'], orbit=group['orbit'],
                       solver_status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                       exhausted=status == cp_model.INFEASIBLE, stop_reason=reason,
                       new_records=new, seconds=time.monotonic()-class_started, survivor=survivor)
        outcomes.append(outcome)
        print(json.dumps(dict(event='class', target=target, number=len(outcomes), total=len(projection['classes']),
                              pair=pair, status=outcome['solver_status'], records=new)), flush=True)
        if len(outcomes) % 5 == 0:
            save()
    solver.parameters.max_time_in_seconds = final_seconds
    final_status = solver.solve(model)
    result = save()
    print(json.dumps(dict(event='complete', **result)), flush=True)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', type=int, nargs=2)
    ap.add_argument('--seconds-per-class', type=float, default=3)
    ap.add_argument('--final-seconds', type=float, default=15)
    args = ap.parse_args()
    for target in ([tuple(args.target)] if args.target else REMAINING):
        run(target, args.seconds_per_class, args.final_seconds)
