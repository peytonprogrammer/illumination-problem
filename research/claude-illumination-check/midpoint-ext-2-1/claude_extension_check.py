"""Claude's independent check of Codex's target(2,1) midpoint extension.

1. All 2,598 geometry-only guards are checked with Claude's exact path checker.
2. Geometry-only claim, types 5, 9, 10, 12: Claude's strong model (no historical cuts)
   with the neck fixed is FEASIBLE with no cuts and with Codex's control room fixed,
   INFEASIBLE with only the core cuts; drop-one control on each core.
3. Composed claim, types 4 and 11: Claude's strong model with every verified historical
   cut for (2,1) plus all 2,598 midpoint guards is INFEASIBLE with the neck fixed.
   The five live types are also run as a consistency check (Codex: FEASIBLE).
"""
import json
import os
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
K3 = HERE.parent/'two-star-k3'
sys.path[:0] = [str(HERE.parent), str(K3), str(HERE.parent/'three-star')]
from claude_ray_guard_check import cell_tiles, check_path
from claude_two_star_k3_geometry import support
from claude_three_star_reduction import neighbors
from claude_k3_strong import build

TARGET, MARKS = (2, 1), [(0, 0), (4, 2)]
norm = lambda tri: {tuple(sorted(tuple(v) for v in t)) for t in tri}
base = json.loads((HERE/'three-triples/midpoint-cover-2-1.json').read_text())
ext = json.loads((HERE/'three-triples/midpoint-extension-2-1.json').read_text())
core = json.loads((HERE/'three-triples/midpoint-extension-core-2-1.json').read_text())
guards = (base['seed_guards'] + [g for r in base['records'] for g in r['derived_guards']]
          + ext['peer_guards'] + [g for r in ext['records'] for g in r['derived_guards']])
assert len(guards) == 2598
patterns = {int(c['neck_type']): c['pattern'] for c in ext['classes']}

full, allowed, r = support(TARGET)
ts = sorted({t for c in allowed for t in cell_tiles(*c)})
index = {t: i for i, t in enumerate(ts)}
outside = allowed - (set(full) | neighbors(full))


def neck(pattern):
    cells, a, b = pattern
    fixed = {}
    for cell, mask in (((1, 0), a), ((1, 1), b)):
        p = (2*cell[0], 2*cell[1])
        ids = [t for t in ts if p in t]
        assert len(ids) == 8
        fixed.update({t: mask >> j & 1 for j, t in enumerate(ids)})
    return {tuple(c) for c in cells}, fixed


def restrict(pattern, cuts):
    cells, fixed = neck(pattern)
    assert cells <= outside

    def extra(m, x, idx, used, _):
        for c in outside:
            m.add(used[c] == int(c in cells))
        for t, v in fixed.items():
            m.add(x[idx[t]] == v)
        for i in cuts:
            m.add_bool_or([x[j].Not() if v else x[j] for j, v in guards[i]['tile_facts']])
    return extra


def run(name, out, pattern, cuts, use_cuts=False, fixed=None):
    res = build(TARGET, use_cuts=use_cuts, fixed=fixed, extra=restrict(pattern, cuts))
    out[name] = {k: v for k, v in res.items() if k != 'room'}
    print(name, json.dumps(out[name]), flush=True)
    return res


out = dict(guard_failures=[])
for gi, g in enumerate(guards):
    room = norm(g['room']['triangles'])
    ok, why, touched = check_path(room, g['witness']['path'], MARKS)
    facts = dict(map(tuple, g['tile_facts']))
    if (not ok or not room <= set(ts)
            or any(facts.get(index[t]) != int(t in room) for t in touched if t in index)
            or any(t in room for t in touched if t not in index)
            or any(v != int(ts[i] in room) for i, v in facts.items())):
        out['guard_failures'].append(dict(guard=gi, why=why))
print(json.dumps(dict(guards=len(guards), failures=len(out['guard_failures']))), flush=True)

for case in core['cases']:
    n, pat, ids = int(case['neck_type']), case['pattern'], case['core_guard_indices']
    assert pat == patterns[n]
    control = norm(guards[case['positive_control_guard']]['room']['triangles'])
    run(f'type{n}_no_cuts', out, pat, [])
    run(f'type{n}_codex_control', out, pat, [], fixed=control)
    run(f'type{n}_core_{len(ids)}', out, pat, ids)
    reopen = 0
    for i in ids:
        res = build(TARGET, use_cuts=False, extra=restrict(pat, [j for j in ids if j != i]))
        if 'room' in res:
            assert check_path(norm(res['room']), guards[i]['witness']['path'], MARKS)[0]
            reopen += 1
    out[f'type{n}_drop_one_reopen'] = [reopen, len(ids)]
    print(f'type{n} drop-one reopen {reopen}/{len(ids)} (each lit by the dropped ray)', flush=True)

# Composed: historical verified cuts (CLAUDE_INPUTS) + verified seeds + all midpoint guards.
for n in (4, 11, 1, 2, 3, 6, 8):
    run(f'type{n}_composed', out, patterns[n], range(len(guards)), use_cuts=True)
(HERE/'claude-extension-check.json').write_text(json.dumps(out, indent=1)+'\n')
