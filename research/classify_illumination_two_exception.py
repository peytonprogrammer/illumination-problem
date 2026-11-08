"""Project the remaining finite room models onto typed exceptional vertices.

Classification is complete only after INFEASIBLE. Previously audited positive
ray cuts remain active: these are classes of possible counterexamples, not all
geometrically possible rooms. A projected class is not a dark construction.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time
from ortools.sat.python import cp_model
from illumination_cover import D4, mat
from illumination_geometry import check, label, owners_of, check_fan_angles
from illumination_two_exception_bound import complete_support, validate_counts
from search_illumination_family import build_model

BASE = Path(__file__).parent
REMAINING = ((1, 1), (2, 0), (2, 1))


def exceptional_pair(room):
    geometry = check(room, strict=False)
    assert geometry['simple_polygon']
    ts = [tuple(map(tuple, t)) for t in room['triangles']]
    owners = owners_of(ts)
    opened = {e for e, ids in owners.items() if len(ids) == 2}
    pair = []
    for p in geometry['transparent_vertices']:
        angles, interior = check_fan_angles(ts, p, owners, opened)
        assert interior or angles == [4]
        pair.append((p[0], p[1], 2 if interior else 1))
    assert len(pair) == 2
    return tuple(sorted(pair))


def pair_orbit(target, pair):
    target = tuple(2*v for v in target)
    result = set()
    for g in D4:
        for swap in (False, True):
            if mat(g, target) != tuple(-v if swap else v for v in target):
                continue
            shift = target if swap else (0, 0)
            result.add(tuple(sorted((*tuple(mat(g, p[:2])[k]+shift[k] for k in (0, 1)), p[2])
                                    for p in pair)))
    return tuple(sorted(result))


def model_with_audited_cuts(target):
    model, ts, x, bounded, terms = build_model(target, 23, 2, complete_support(target))
    case_file = BASE/f'two-global-{target[0]}-{target[1]}.json'
    source = json.loads(case_file.read_text())
    audit = json.loads((BASE/'two-global-final-audit.json').read_text())
    assert audit['status'] == 'PASS'
    assert source['summary']['complete_support_triangles'] == len(ts)
    cuts = 0
    for record in source['records']:
        for guard in record['derived_guards']:
            selected = {tuple(sorted(map(tuple, t))) for t in guard['room']['triangles']}
            assert selected <= set(ts)
            facts = guard['tile_facts']
            assert all(0 <= i < len(ts) and int(ts[i] in selected) == value for i, value in facts)
            model.add(sum(1-x[i] if value else x[i] for i, value in facts) >= 1)
            cuts += 1
    assert cuts == source['summary']['cuts']
    provenance = dict(source_file=case_file.name, source_sha256=hashlib.sha256(case_file.read_bytes()).hexdigest(),
                      prior_audit_sha256=hashlib.sha256((BASE/'two-global-final-audit.json').read_bytes()).hexdigest(),
                      triangle_index_sha256=hashlib.sha256(json.dumps(ts).encode()).hexdigest(), cuts=cuts)
    return model, ts, x, bounded, terms, provenance


def block_pair(model, terms, pair):
    (px, py, a), (qx, qy, b) = pair
    model.add_forbidden_assignments([terms['defect_at'][px, py], terms['defect_at'][qx, qy]], [[a, b]])


def observed_classes():
    results = []
    for target in REMAINING:
        source = json.loads((BASE/f'two-global-{target[0]}-{target[1]}.json').read_text())
        counts, descriptions = Counter(), {}
        for record in source['records']:
            pair = exceptional_pair(record['room'])
            canonical = min(pair_orbit(target, pair))
            counts[canonical] += 1
            descriptions[canonical] = [f'{label(p[:2])}:{"interior" if p[2] == 2 else "smooth"}' for p in canonical]
        results.append(dict(target_A_cell=target, configurations=sum(counts.values()), classes=len(counts),
                            groups=[dict(pair=k, types=descriptions[k], configurations=v) for k, v in sorted(counts.items())]))
    (BASE/'two-pair-observed.json').write_text(json.dumps(results, indent=2)+'\n')
    return results


def project(target, seconds=90, limit=1000):
    started = time.monotonic()
    model, ts, x, bounded, terms, provenance = model_with_audited_cuts(target)
    # Every mark-preserving isometry must preserve the complete finite support.
    for g in D4:
        for swap in (False, True):
            physical = tuple(2*v for v in target)
            if mat(g, physical) != tuple(-v if swap else v for v in physical):
                continue
            shift = physical if swap else (0, 0)
            transformed = {tuple(sorted(tuple(mat(g, p)[k]+shift[k] for k in (0, 1)) for p in t)) for t in ts}
            assert transformed == set(ts)
    filename = BASE/f'two-pair-{target[0]}-{target[1]}.json'
    previous = json.loads(filename.read_text()) if filename.exists() else None
    classes = previous['classes'] if previous else []
    if previous:
        assert previous['summary']['provenance'] == provenance
        if previous['summary']['complete']:
            print(json.dumps(dict(event='reuse_exhausted', **previous['summary'])), flush=True)
            return previous['summary']
        for group in classes:
            for pair in group['orbit']:
                block_pair(model, terms, pair)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    solver.parameters.random_seed = 17
    search_started = time.monotonic()
    status, reason = None, 'class_limit'
    filename = BASE/f'two-pair-{target[0]}-{target[1]}.json'
    def save():
        result = dict(target_A_cell=target, complete=status == cp_model.INFEASIBLE,
                      solver_status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                      stop_reason=reason, classes=len(classes), seconds=time.monotonic()-started,
                      provenance=provenance)
        temporary = filename.with_suffix('.tmp')
        temporary.write_text(json.dumps(dict(summary=result, classes=classes), indent=2)+'\n')
        temporary.replace(filename)
        return result
    for _ in range(limit):
        remaining = seconds-(time.monotonic()-search_started)
        if remaining <= 0:
            reason = 'time_limit'
            break
        solver.parameters.max_time_in_seconds = remaining
        status = solver.solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            reason = 'exhausted' if status == cp_model.INFEASIBLE else 'solver_unknown'
            break
        room = dict(triangles=[t for t, v in zip(ts, x) if solver.value(v)],
                    marked=[[0, 0], [2*v for v in target]], require_simple=True)
        validate_counts(room)
        pair = exceptional_pair(room)
        assert pair == tuple(sorted((p[0], p[1], solver.value(v)) for p, v in terms['defect_at'].items() if solver.value(v)))
        orbit = pair_orbit(target, pair)
        assert not any(tuple(map(tuple, c['canonical'])) == min(orbit) for c in classes)
        classes.append(dict(pair=pair, canonical=min(orbit), orbit=orbit, witness_room=room,
                            types=[f'{label(p[:2])}:{"interior" if p[2] == 2 else "smooth"}' for p in pair]))
        for other in orbit:
            block_pair(model, terms, other)
        if len(classes) % 10 == 0:
            print(json.dumps(dict(event='projected', **save())), flush=True)
    result = save()
    print(json.dumps(dict(event='complete', **result)), flush=True)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=90)
    ap.add_argument('--target', type=int, nargs=2)
    ap.add_argument('--observed-only', action='store_true')
    args = ap.parse_args()
    if args.observed_only:
        print(json.dumps([dict(target=r['target_A_cell'], configurations=r['configurations'], classes=r['classes']) for r in observed_classes()]))
    else:
        for target in ([tuple(args.target)] if args.target else REMAINING):
            project(target, args.seconds)
