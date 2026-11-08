"""Claude's independent check of Codex's target(2,1) neck-type-7 midpoint cover.

1. Every guard (286 seeds + 780 derived) is checked with Claude's exact path checker
   against Claude's k=3 support for (2,1).
2. Claude's strengthened model (claude_k3_strong.py, no Codex code) is restricted to
   neck type 7: no outside cells, mask 40 at A-cell (1,0), mask 83 at A-cell (1,1),
   with bit j = the j-th sorted tile containing the cell's A vertex.
   - control A: no cuts -> must be FEASIBLE
   - control B: Codex's positive-control room fixed, no cuts -> must be FEASIBLE
   - claim: only the 37 core cuts -> INFEASIBLE proves the cover in Claude's model.
"""
import json
import sys
from pathlib import Path
HERE = Path(__file__).parent
K3 = HERE.parent/'two-star-k3'
sys.path[:0] = [str(HERE.parent), str(K3), str(HERE.parent/'three-star')]
from claude_ray_guard_check import cell_tiles, check_path
from claude_two_star_k3_geometry import support
from claude_three_star_reduction import neighbors
from claude_k3_strong import build

TARGET = (2, 1)
MARKS = [(0, 0), (4, 2)]
norm = lambda tri: {tuple(sorted(tuple(v) for v in t)) for t in tri}
data = json.loads((HERE/'three-triples/midpoint-cover-2-1.json').read_text())
core = json.loads((HERE/'three-triples/midpoint-cover-core-2-1.json').read_text())
guards = data['seed_guards'] + [g for r in data['records'] for g in r['derived_guards']]
assert len(guards) == 1066

full, allowed, r = support(TARGET)
ts = sorted({t for c in allowed for t in cell_tiles(*c)})
index = {t: i for i, t in enumerate(ts)}
outside = allowed - (set(full) | neighbors(full))


def fan(cell, mask):
    p = (2*cell[0], 2*cell[1])
    ids = [t for t in ts if p in t]
    assert len(ids) == 8
    return {t: mask >> j & 1 for j, t in enumerate(ids)}


neck = {**fan((1, 0), 40), **fan((1, 1), 83)}


def signature(room):
    used = {c for c in allowed if any(t in room for t in cell_tiles(*c))}
    return (sorted(used & outside), [int(t in room) for t in neck])


fails = []
for gi, g in enumerate(guards):
    room = norm(g['room']['triangles'])
    ok, why, touched = check_path(room, g['witness']['path'], MARKS)
    facts = dict(map(tuple, g['tile_facts']))
    bad = (not ok or not room <= set(ts)
           or any(facts.get(index.get(t)) != int(t in room) for t in touched if t in index)
           or any(t in room for t in touched if t not in index)
           or any(v != int(ts[i] in room) for i, v in facts.items()))
    if bad:
        fails.append(dict(guard=gi, why=why))
print(json.dumps(dict(guards=len(guards), failures=len(fails), first=fails[:3])), flush=True)

want = [int(v) for v in neck.values()]
matching = [gi for gi, g in enumerate(guards) if signature(norm(g['room']['triangles'])) == ([], want)]
print(json.dumps(dict(guards_in_type7=len(matching), codex_control=core['positive_control_guard'],
                      control_in_type7=core['positive_control_guard'] in matching)), flush=True)


def restrict(cuts):
    def extra(m, x, idx, used, _):
        for c in outside:
            m.add(used[c] == 0)
        for t, v in neck.items():
            m.add(x[idx[t]] == v)
        for i in cuts:
            m.add_bool_or([x[j].Not() if v else x[j] for j, v in guards[i]['tile_facts']])
    return extra


out = dict(guards=len(guards), guard_failures=fails, guards_in_type7=len(matching))
control = norm(guards[core['positive_control_guard']]['room']['triangles'])
for name, kw in [('no_cuts', dict(extra=restrict([]))),
                 ('codex_control_fixed', dict(extra=restrict([]), fixed=control)),
                 ('core_37_cuts', dict(extra=restrict(core['core_guard_indices']))),
                 ('all_1066_cuts', dict(extra=restrict(range(len(guards)))))]:
    res = build(TARGET, use_cuts=False, **kw)
    out[name] = {k: v for k, v in res.items() if k != 'room'}
    print(name, json.dumps(out[name]), flush=True)
(HERE/'claude-midpoint-check.json').write_text(json.dumps(out, indent=1)+'\n')
