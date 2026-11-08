"""Replay a ray-cut parent by explicit typed-triple branches and complement.

The partition is exhaustive by construction; it does not rely on discovering
every feasible triple, or on a symmetry argument to transfer solver results.
"""
import argparse
import hashlib
import json
from pathlib import Path

from ortools.sat.python import cp_model
from search_illumination_three_two_star import (
    add_guard, fix_triple, make_model, new_solver, triple_orbit,
)

BASE = Path(__file__).parent
OUT = BASE / 'three-two-star'


def replay(target, seconds, parent_only=False):
    source = OUT / f'case-{target[0]}-{target[1]}.json'
    raw = source.read_bytes()
    data = json.loads(raw)
    model, ts, x, _, terms = make_model(target)
    assert hashlib.sha256(json.dumps(ts).encode()).hexdigest() == data['summary']['triangle_index_sha256']
    for seed in data['seeds']:
        add_guard(model, x, seed['tile_facts'])
    for record in data['records']:
        for guard in record['derived_guards']:
            add_guard(model, x, guard['tile_facts'])
    if parent_only:
        solver = new_solver(seconds)
        status = solver.solve(model)
        assert source.read_bytes() == raw, 'Inputs changed during replay'
        result = dict(target_A_cell=target, status=solver.status_name(status),
                      seconds=solver.wall_time, case_sha256=hashlib.sha256(raw).hexdigest(),
                      ray_cuts=data['summary']['cuts'],
                      scope='Fresh necessary parent plus positive-ray cuts only; no exception partition restrictions.')
        (OUT / f'parent-{target[0]}-{target[1]}.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result), flush=True)
        return
    triples = sorted({other for outcome in data['triples']
                      for other in triple_orbit(target, tuple(map(tuple, outcome['triple'])))})
    assert triples
    # Every real room has exactly three exceptions. Matching these three typed
    # coordinates therefore fixes its entire exception set.
    results = []
    for triple in triples:
        branch = model.clone()
        fix_triple(branch, terms, triple)
        solver = new_solver(seconds)
        status = solver.solve(branch)
        row = dict(triple=triple, status=solver.status_name(status), seconds=solver.wall_time)
        results.append(row)
        print(json.dumps(dict(event='branch_replay', **row)), flush=True)
    complement = model.clone()
    for triple in triples:
        complement.add_forbidden_assignments(
            [terms['defect_at'][p[:2]] for p in triple], [[p[2] for p in triple]])
    solver = new_solver(seconds)
    status = solver.solve(complement)
    rest = dict(status=solver.status_name(status), seconds=solver.wall_time)
    print(json.dumps(dict(event='complement_replay', **rest)), flush=True)
    assert source.read_bytes() == raw, 'Inputs changed during replay'
    result = dict(target_A_cell=target, case_sha256=hashlib.sha256(raw).hexdigest(),
                  explicit_triples=len(triples), branches=results, complement=rest,
                  status='EXCLUDED' if rest['status']=='INFEASIBLE' and all(
                      r['status']=='INFEASIBLE' for r in results) else 'INCOMPLETE',
                  scope='Finite disjunction of every listed explicit typed triple plus its complement; all branches replayed without symmetry transfer. Depends on the separately audited necessary geometry and positive-ray guards. No formal UNSAT proof.')
    (OUT / f'partition-{target[0]}-{target[1]}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', type=int, nargs=2, required=True)
    ap.add_argument('--seconds', type=float, default=30)
    ap.add_argument('--parent-only', action='store_true')
    args = ap.parse_args()
    replay(tuple(args.target), args.seconds, args.parent_only)
