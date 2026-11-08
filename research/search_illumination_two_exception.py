"""Ray-cut search of the complete finite two-exception supports.

Every exclusion cut has an exact connecting ray. A finite ray miss returns
UNRESOLVED and preserves the candidate; it never excludes that geometry.
"""
import argparse
import json
from pathlib import Path
import time
from ortools.sat.python import cp_model
from search_illumination_family import build_model
from search_illumination_one_exception import orbit, tile_facts
from illumination_geometry import owners_of, check
from illumination_paths import find_path
from illumination_sector_paths import verify
from illumination_two_exception_bound import TARGETS, complete_support, validate_counts as counts

BASE = Path(__file__).parent


def seed_records(target):
    wanted = [[0, 0], [2*v for v in target]]
    records, seen = [], set()
    patterns = ['transparent*-screen.json', 'placement*-screen.json',
                f'two-global-{target[0]}-{target[1]}.json']
    for path in sorted({p for pat in patterns for p in BASE.glob(pat)}):
        saved = json.loads(path.read_text())
        for record in saved.get('records', []):
            room = record['room']
            if room['marked'] != wanted or room.get('slits') or record['witness']['status'] != 'illuminated':
                continue
            bad_count = (len(record['transparent']) if 'transparent' in record else
                         record.get('counts', {}).get('interior_nonA', 0)+
                         record.get('counts', {}).get('smooth_boundary_nonA', 0))
            if bad_count != 2:
                continue
            key = tuple(sorted(tuple(sorted(map(tuple, t))) for t in room['triangles']))
            if key in seen:
                continue
            geometry = check(room, strict=False)
            if not geometry['simple_polygon']:
                continue
            seen.add(key)
            records.append(record)
    return records


def solve_case(target, seconds=30, max_candidates=1000, use_seeds=True):
    started = time.monotonic()
    model, ts, variables, bounded, terms = build_model(target, 23, 2, complete_support(target))
    owners = owners_of(ts)
    records, cut_keys = [], set()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    solver.parameters.random_seed = 7
    filename = BASE/f'two-global-{target[0]}-{target[1]}.json'
    cuts = 0
    def add_record(room, witness, seeded, cached=None):
        nonlocal cuts
        verify(room, witness)
        checked = counts(room)
        guards = []
        source = ((g['room'], g['witness'], list(map(tuple, g['tile_facts']))) for g in cached) if cached is not None else (
            (changed, ray, None) for changed, ray in orbit(room, witness))
        for changed, ray, cached_facts in source:
            verify(changed, ray)
            facts = cached_facts if cached_facts is not None else tile_facts(ts, owners, ray, changed)
            if cached_facts is not None:
                chosen = {tuple(sorted(map(tuple, t))) for t in changed['triangles']}
                assert all(0 <= i < len(ts) and int(ts[i] in chosen) == value for i, value in facts)
            key = tuple(facts)
            if key in cut_keys:
                continue
            cut_keys.add(key)
            model.add(sum((1-variables[i]) if v else variables[i] for i, v in facts) >= 1)
            guards.append(dict(room=changed, witness=ray, tile_facts=facts))
            cuts += 1
        records.append(dict(room=room, witness=witness, counts=checked,
                            seeded=seeded, derived_guards=guards))
    print(json.dumps(dict(event='model', target=target, triangles=len(ts),
                          A_cells=len(bounded['allowed']))), flush=True)
    if use_seeds:
        for number, record in enumerate(seed_records(target), 1):
            add_record(record['room'], record['witness'], True)
            if number % 50 == 0:
                print(json.dumps(dict(event='seeding', target=target, records=number, cuts=cuts,
                                      seconds=time.monotonic()-started)), flush=True)
    seeded = len(records)
    print(json.dumps(dict(event='seeded', target=target, records=seeded, cuts=cuts,
                          seconds=time.monotonic()-started)), flush=True)
    search_started = time.monotonic()
    status, reason, survivor = None, 'candidate_limit', None
    new = 0
    def checkpoint():
        summary = dict(target_A_cell=target, status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                       stop_reason=reason, exhausted=status == cp_model.INFEASIBLE,
                       seeded_records=seeded, new_records=new, records=len(records),
                       cuts=cuts, seconds=time.monotonic()-started,
                       complete_support_triangles=len(ts), survivor=survivor)
        temporary = filename.with_suffix('.tmp')
        temporary.write_text(json.dumps(dict(summary=summary, records=records), indent=2)+'\n')
        temporary.replace(filename)
        return summary
    for _ in range(max_candidates):
        remaining = seconds-(time.monotonic()-search_started)
        if remaining <= 0:
            reason = 'time_limit'
            break
        solver.parameters.max_time_in_seconds = remaining
        status = solver.solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            reason = 'exhausted' if status == cp_model.INFEASIBLE else 'solver_unknown'
            break
        room = dict(triangles=[t for i, t in enumerate(ts) if solver.value(variables[i])],
                    marked=[[0, 0], [2*v for v in target]], require_simple=True)
        geometry = check(room, strict=False)
        assert geometry['simple_polygon'] and len(geometry['transparent_vertices']) == 2
        counts(room)
        witness = find_path(room, 16, 1000)
        if witness['status'] != 'illuminated':
            witness = find_path(room, 32, 2000)
        if witness['status'] != 'illuminated':
            reason = 'unresolved_candidate'
            survivor = dict(room=room, bounded_screen=witness)
            break
        add_record(room, witness, False)
        new += 1
        if new % 10 == 0:
            summary = checkpoint()
            print(json.dumps(dict(event='screened', **summary)), flush=True)
    result = checkpoint()
    print(json.dumps(dict(event='complete', **result)), flush=True)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', type=int, nargs=2)
    ap.add_argument('--seconds', type=float, default=30)
    ap.add_argument('--no-seeds', action='store_true')
    args = ap.parse_args()
    results = []
    for target in ([tuple(args.target)] if args.target else TARGETS):
        saved = BASE/f'two-global-{target[0]}-{target[1]}.json'
        previous = json.loads(saved.read_text())['summary'] if saved.exists() else None
        if previous and previous['exhausted']:
            print(json.dumps(dict(event='reuse_exhausted', **previous)), flush=True)
            results.append(previous)
        else:
            results.append(solve_case(target, args.seconds, use_seeds=not args.no_seeds))
    all_results = [json.loads(path.read_text())['summary'] for target in TARGETS
                   if (path := BASE/f'two-global-{target[0]}-{target[1]}.json').exists()]
    summary = dict(status='EXCLUDED' if len(all_results) == len(TARGETS) and all(r['exhausted'] for r in all_results)
                   else 'INCOMPLETE', cases=all_results,
                   scope='Complete finite supports for simple canonical rooms with exactly two transparent B/C points; caps and unresolved candidates do not exclude.')
    (BASE/'two-global-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
