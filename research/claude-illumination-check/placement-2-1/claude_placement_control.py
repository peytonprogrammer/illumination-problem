"""Control: without the newest mask12 rays the empty-outside branch must reopen, and every
room it finds must be lit by some mask12 ray. Also: each outside set is FEASIBLE with no cuts."""
import json, os, sys
import claude_placement_check as c
os.environ['CLAUDE_CAP'] = '120'
mask12 = {}
c.walk(json.loads((c.HERE/'run/.context/three-triples/mask12-search-2-1.json').read_text()), mask12)
_, allcuts = c.collect()
newest = set()
for room, path in mask12:
    ok, _, touched = c.check_path(room, json.loads(path), c.MARKS); assert ok
    newest.add(tuple(sorted((c.index[t], int(t in room)) for t in touched if t in c.index)))
older = [f for f in allcuts if f not in newest]
res = c.model(older, frozenset())
lit = None
if 'room' in res:
    room = c.norm(res['room'])
    lit = any(c.check_path(room, json.loads(p), c.MARKS)[0] for _, p in mask12)
print(json.dumps(dict(older_cuts=len(older), newest=len(newest), empty_outside_without_newest=res['status'],
                      reopened_room_lit_by_a_mask12_ray=lit)), flush=True)
sets = [frozenset(s) for s in c.connected_outside_sets(c.R, c.outside, c.r)]
st = [c.model([], s)['status'] for s in sets]
print(json.dumps(dict(outside_sets=len(sets), feasible_without_cuts=sum(s in ('OPTIMAL', 'FEASIBLE') for s in st),
                      other={s: st.count(s) for s in set(st)})), flush=True)
