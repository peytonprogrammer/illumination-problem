"""Extend the frozen geometry-only midpoint catalogue without changing it."""
import argparse
from collections import Counter
import json
import time
from ortools.sat.python import cp_model
from classify_illumination_three_exception import OUT, digest, solver_for
from illumination_geometry import owners_of
from search_illumination_midpoint_covers import TARGET, geometry_parent, fixed_neck, one_pass, find_one_pass
from search_illumination_three_two_star import add_guard, room_from
from search_illumination_one_exception import orbit, tile_facts
from illumination_three_two_star_bound import validate

PATH = OUT / 'midpoint-extension-2-1.json'


def load_base():
    manifest_path = OUT / 'midpoint-cover-proof-inputs-2-1.json'
    manifest = json.loads(manifest_path.read_text())
    for name, expected in manifest['sha256'].items():
        assert digest(OUT.parent.parent / name) == expected, name
    source = OUT / 'midpoint-cover-2-1.json'
    saved = json.loads(source.read_text())
    peer_path = OUT / 'peer-survivor-midpoint-2-1.json'
    peer = json.loads(peer_path.read_text())
    model, ts, x, bounded, terms, first, second, patterns = geometry_parent()
    guards = saved['seed_guards'] + [g for r in saved['records'] for g in r['derived_guards']]
    keys = set()
    for guard in guards:
        key = tuple(map(tuple, guard['tile_facts']))
        assert key not in keys
        keys.add(key)
        add_guard(model, x, key)
    owners = owners_of(ts)
    peer_guards = []
    for data, ray in orbit(peer['room'], peer['witness']):
        one_pass(data, ray)
        facts = tile_facts(ts, owners, ray, data)
        key = tuple(facts)
        if key not in keys:
            keys.add(key)
            add_guard(model, x, facts)
            peer_guards.append(dict(room=data, witness=ray, tile_facts=facts))
    provenance = dict(frozen_manifest_sha256=digest(manifest_path), source_sha256=digest(source),
                      peer_witness_sha256=digest(peer_path))
    return model, ts, x, bounded, terms, first, second, patterns, keys, guards, peer_guards, provenance


def run(seconds):
    start = time.monotonic()
    model, ts, x, bounded, terms, first, second, patterns, keys, base_guards, peer_guards, provenance = load_base()
    base_count = len(keys)
    assert not PATH.exists(), 'Preserve an existing extension; choose a new claimed path for another phase.'
    records, classes = [], []
    owners = owners_of(ts)
    frequencies = Counter(tuple(g['witness']['direction']) for g in base_guards+peer_guards)
    library = [d for d, _ in frequencies.most_common()]
    solver = solver_for(seconds, 229)
    solver.parameters.cp_model_presolve = False

    def save():
        summary = dict(base_catalogue_guards=len(base_guards), peer_seed_guards=len(peer_guards),
                       new_records=len(records), new_guards=len(keys)-base_count, total_guards=len(keys),
                       visited=len(classes), types_proved=sum(c['exhausted'] for c in classes),
                       seconds=time.monotonic()-start, cp_model_presolve=False)
        temp = PATH.with_suffix('.tmp')
        temp.write_text(json.dumps(dict(summary=summary, provenance=provenance, peer_guards=peer_guards,
                                        patterns=patterns, records=records, classes=classes), indent=2)+'\n')
        temp.replace(PATH)
        return summary

    for number, pattern in enumerate(patterns, 1):
        branch = model.clone()
        fixed_neck(branch, terms, bounded, x, first, second, pattern)
        deadline = time.monotonic() + seconds
        before, unresolved, status = len(records), None, None
        while time.monotonic() < deadline:
            solver.parameters.max_time_in_seconds = max(.001, deadline-time.monotonic())
            status = solver.solve(branch)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                break
            data = room_from(TARGET, ts, x, solver)
            witness, screen = find_one_pass(data, library, deadline)
            if witness is None:
                unresolved = dict(room=data, screen=screen)
                break
            guards = []
            for changed, ray in orbit(data, witness):
                one_pass(changed, ray)
                facts = tile_facts(ts, owners, ray, changed)
                key = tuple(facts)
                if key in keys:
                    continue
                keys.add(key)
                add_guard(model, x, facts)
                add_guard(branch, x, facts)
                guards.append(dict(room=changed, witness=ray, tile_facts=facts))
            assert guards
            records.append(dict(neck_type=number, room=data, witness=witness, counts=validate(data,TARGET),
                                derived_guards=guards, direction_screen=screen))
        classes.append(dict(neck_type=number, pattern=pattern, status=solver.status_name(status) if status is not None else 'NOT_SOLVED',
                            exhausted=status==cp_model.INFEASIBLE, new_records=len(records)-before, unresolved=unresolved))
        print(json.dumps(dict(event='midpoint_extension_type', neck_type=number, **save())), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seconds',type=float,default=30)
    run(parser.parse_args().seconds)
