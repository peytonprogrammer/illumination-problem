"""Independent final check of (2,0): rebuild every cut from scratch, then
(a) one monolithic solve with all cuts, (b) drop the pass-2 rays and confirm {(1,-1)} reopens
with a room lit by a dropped ray. Writes claude-rays-2-0.json (all rays, for Codex)."""
import json, os, sys
os.environ.setdefault('CLAUDE_TARGET', '2,0')
import claude_cut_loop as L
c = L.c
_, base = c.collect()
rays = [r for f in ('claude-cut-loop-2-0-pass1.json', 'claude-cut-loop-2-0-pass2.json')
        for r in json.loads((L.HERE/f).read_text())['rays']]
p1 = len(json.loads((L.HERE/'claude-cut-loop-2-0-pass1.json').read_text())['rays'])
own = []
for r in rays:
    own.append(L.cut_of(r['room'], r['witness']['path']))
    own.append(L.cut_of(*L.mirror(r['room'], r['witness']['path'])))
cuts = sorted(set(base) | set(own))
print(json.dumps(dict(codex_cuts=len(base), claude_rays=len(rays), total_cuts=len(cuts))), flush=True)
os.environ['CLAUDE_CAP'] = sys.argv[1] if len(sys.argv) > 1 else '1200'
mono = c.model(cuts)
print('monolithic', json.dumps({k: v for k, v in mono.items() if k != 'room'}), flush=True)
os.environ['CLAUDE_CAP'] = '120'
early = sorted(set(base) | {L.cut_of(r['room'], r['witness']['path']) for r in rays[:p1]}
               | {L.cut_of(*L.mirror(r['room'], r['witness']['path'])) for r in rays[:p1]})
res = c.model(early, frozenset({(1, -1)}))
lit = 'room' in res and any(c.check_path(c.norm(res['room']), r['witness']['path'], c.MARKS)[0]
                            or c.check_path(c.norm(res['room']), L.mirror(r['room'], r['witness']['path'])[1], c.MARKS)[0]
                            for r in rays[p1:])
print(json.dumps(dict(control_without_pass2=res['status'], reopened_room_lit_by_dropped_ray=lit)), flush=True)
(L.HERE/'claude-rays-2-0.json').write_text(json.dumps(dict(
    target=[2, 0], marks=[[0, 0], [4, 0]],
    note='Each ray checked by Claude exact checker; mirror y->-y of each is also valid.',
    rays=[dict(room=r['room'], witness=r['witness']) for r in rays]))+'\n')
