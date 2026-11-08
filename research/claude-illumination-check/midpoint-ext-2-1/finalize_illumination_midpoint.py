"""Freeze the first conditional midpoint certificate and reconcile phase counts."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '.context/three-triples'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geometry(room):
    return tuple(sorted(tuple(sorted(map(tuple, t))) for t in room['triangles']))


def guard_key(guard):
    return tuple(sorted(map(tuple, guard['tile_facts'])))


def run():
    old_path = OUT / 'neck-budget-proof-inputs-2-1.json'
    old = json.loads(old_path.read_text())
    for name, expected in old['sha256'].items():
        assert digest(ROOT / name) == expected, name
    saved = json.loads((OUT / 'midpoint-cover-2-1.json').read_text())
    audit = json.loads((OUT / 'midpoint-cover-audit-2-1.json').read_text())
    core = json.loads((OUT / 'midpoint-cover-core-2-1.json').read_text())
    composed = json.loads((OUT / 'midpoint-parent-replay-2-1.json').read_text())
    peer = json.loads((OUT / 'peer-survivor-midpoint-2-1.json').read_text())
    source_hash = digest(OUT / 'midpoint-cover-2-1.json')
    assert all(d['source_sha256'] == source_hash for d in [audit, core, composed])
    assert audit['status'] == core['status'] == composed['status'] == 'PASS'
    assert core['core_replay'] == 'INFEASIBLE' and core['core_size'] == 37
    old_rooms, old_guards = set(), set()
    for name in old['paths']:
        path = ROOT / name
        if path.suffix != '.json':
            continue
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            continue
        records = data.get('records', [])
        if isinstance(records, list):
            for record in records:
                room = record.get('room', {})
                if room.get('marked') == [[0, 0], [4, 2]]:
                    old_rooms.add(geometry(room))
                if '/three-triples/' in name or name.endswith('/case-2-1.json'):
                    if room.get('marked') == [[0, 0], [4, 2]]:
                        old_guards.update(guard_key(g) for g in record.get('derived_guards', []))
        if name.endswith('/case-2-1.json'):
            for seed in data.get('seeds', []):
                old_guards.add(guard_key(seed))
    new_rooms = {geometry(r['room']) for r in saved['records']}
    seed_guards = {guard_key(g) for g in saved['seed_guards']}
    learned_guards = {guard_key(g) for r in saved['records'] for g in r['derived_guards']}
    novel_guards = (seed_guards | learned_guards) - old_guards
    dedup = dict(old_manifest_sha256=digest(old_path), old_matching_geometries=len(old_rooms),
                 old_matching_guards=len(old_guards), phase_geometries=len(new_rooms),
                 genuinely_new_geometries=len(new_rooms-old_rooms), revisited_geometries=len(new_rooms & old_rooms),
                 phase_learned_guards=len(learned_guards), genuinely_new_learned_guards=len(learned_guards-old_guards),
                 new_alternative_seed_guards=len(seed_guards-old_guards), total_new_unique_guards=len(novel_guards))
    assert dedup['old_matching_guards'] == 3207, dedup
    assert dedup['genuinely_new_geometries'] == 380, dedup
    assert len(novel_guards) == composed['new_unique_midpoint_guards'] == 586, dedup
    (OUT / 'midpoint-cover-dedup-2-1.json').write_text(json.dumps(dedup, indent=2)+'\n')
    report = '''# Conditional midpoint illumination certificate

[done] Every valid completion of canonical neck type 7 admits a source-to-target ray with exactly one exceptional B/C encounter, at its optical midpoint. This is a computer-assisted conditional theorem for simple canonical 45-degree tile rooms with at most 23 walls, exactly two full A stars, and exactly three B/C exceptions. It is conditional on the checked geometry reduction, ray checker, and CP-SAT result; no formal UNSAT proof is exported.

The fixed neck has no outside cells, mask 40 at A-cell (1,0), and mask 83 at A-cell (1,1). The physical marks are (0,0) and (4,2). Its two forced exceptional points are the smooth-boundary point (1,0) and interior point (2,1). The third exception varies.

The synthesis parent contains geometry, counting, and connectivity constraints only. It starts with 286 sufficient one-pass triangle patterns from 147 saved rooms and learns 780 additional patterns from 390 configurations. No historical illumination cuts enter this parent. Each sufficient pattern fixes the triangle presence/absence facts needed for its exact path. Any completion satisfying those facts retains that path. Infeasibility after forbidding every pattern proves that their disjunction covers every valid completion.

All 1,066 patterns pass exact ray verification and an independent closed-triangle segment-coverage check. Twelve fixed positive geometry controls, eight mutations, and eight corrupt-guard checks pass. The longest path has 33 reflections. A fresh geometry-only implication replay excludes type 7; the other eleven types remain feasible.

Of the 1,066 patterns, only 65 are compatible with the type-7 fixed facts. A solver assumption core selects 37; a fresh model with only those 37 exclusions is infeasible. This subset is sufficient, not claimed minimum. Its midpoint gates are (2,1):22, (1,0):7, (4,1):2, (5,2):1, (0,-1):1, (0,1):3, and (1,2):1. The proof therefore uses possible third-exception locations as well as the two forced gates.

The saved central-gate-only catalogue (58 patterns) and compatible forced-pair catalogue (33 patterns) each leave a feasible model. Neither result disproves a universal theorem for those gates: the tested catalogues are finite and may omit useful rays.

Composition with historical cuts adds 586 unique patterns to the old 3,207, giving 3,793. The set is closed under mark-exchange half-turn. Exactly one canonical neck type closes, so 24 raw patterns / 12 canonical types reduce to 22 / 11. All three surviving outside-cell sets and the unrestricted placement remain feasible. The broader counts remain 102/105 outside sets and 7/10 whole placements excluded.

The synthesis phase revisits ten historical geometries. Its 390 configurations contain 380 genuinely new geometries; 542 of the learned guards and 44 alternative seed guards are new. Cumulative three-triples counts become 2,045 new geometries and 4,886 unique new guards. The separate peer-survivor check is not included in these phase totals.

[done] Claude independently confirms all seven earlier placement exclusions. His 23-wall survivor (raw neck masks 44,80) matches none of the initial 1,066 sufficient patterns, but a bounded follow-up finds and exactly verifies a 12-reflection one-pass ray with midpoint gate (4,3). Its copied geometry, path, guard facts, and source hash are in `peer-survivor-midpoint-2-1.json`; Claude's original remains untouched.

[waiting on Claude] Independent review of the new conditional midpoint theorem, the 37-pattern core, and earlier gate/fan derivations. The manifest freezes all inputs and commands. Run audit commands in a copy preserving subdirectories; scripts write their receipts beside their copied inputs.

Reproduce with Python -B: `audit_illumination_midpoint_covers.py`, `analyze_illumination_midpoint_cover_core.py`, and `replay_illumination_midpoint_parent.py`. The first checks physical paths and geometry implications; the second checks the compact core; the third composes with earlier cuts. Presolve is disabled because of a prior solver internal assertion; constraints remain unchanged.

**Next move:** extend the finite sufficient midpoint cover across the eleven remaining types, seeded by the peer's hard survivor, while preserving this certificate.
'''
    (OUT / 'midpoint-cover-findings-2-1.md').write_text(report)
    names = ['search_illumination_midpoint_covers.py', 'audit_illumination_midpoint_covers.py',
             'analyze_illumination_midpoint_cover_core.py', 'replay_illumination_midpoint_parent.py',
             'check_illumination_peer_survivor.py', 'finalize_illumination_midpoint.py']
    names += ['three-triples/'+n for n in ['midpoint-cover-2-1.json','midpoint-cover-audit-2-1.json',
              'midpoint-cover-core-2-1.json','midpoint-parent-replay-2-1.json',
              'peer-survivor-midpoint-2-1.json','midpoint-cover-dedup-2-1.json','midpoint-cover-findings-2-1.md']]
    paths = sorted(set(old['paths'] + ['.context/'+n for n in names] + [str(old_path.relative_to(ROOT))]))
    manifest = dict(paths=paths, sha256={name:digest(ROOT/name) for name in paths},
                    commands=['audit_illumination_midpoint_covers.py','analyze_illumination_midpoint_cover_core.py',
                              'replay_illumination_midpoint_parent.py'],
                    scope='First geometry-only conditional midpoint cover; preserve all inputs. Run audit scripts in a claimed copy.')
    (OUT/'midpoint-cover-proof-inputs-2-1.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(manifest_paths=len(paths),dedup=dedup,peer_bounces=peer['witness']['bounces'])))


if __name__ == '__main__':
    run()
