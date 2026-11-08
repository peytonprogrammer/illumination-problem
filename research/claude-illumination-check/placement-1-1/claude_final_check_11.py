"""Final check of (1,1): rebuild all cuts from scratch, monolithic solve, drop control,
and export every Claude ray for Codex."""
import json, os, sys
import claude_cut_loop_11 as L
c = L.c
_, base = c.collect()
traced = []
for r in json.loads((L.HERE/'claude-placement-1-1-traced.json').read_text()):
    path = r['path'] if r.get('verified') else json.loads(
        (L.HERE/f"unlit-{'_'.join(f'{a}{b}' for a, b in r['cells'])}.json").read_text())['retrace']['path']
    traced.append(dict(room=r['room'], path=path))
loop = [json.loads(l) for l in L.RAYS.read_text().splitlines()]
mine = set()
for r in traced + loop:
    mine |= L.cuts_of(r['room'], r['path'])
cuts = sorted(set(base) | mine)
print(json.dumps(dict(codex_cuts=len(base), claude_rays=len(traced) + len(loop), total_cuts=len(cuts))), flush=True)
os.environ['CLAUDE_CAP'] = sys.argv[1] if len(sys.argv) > 1 else '2400'
mono = c.model(cuts)
print('monolithic', json.dumps({k: v for k, v in mono.items() if k != 'room'}), flush=True)
os.environ['CLAUDE_CAP'] = '120'
reopened = []
for cells in sorted({tuple(map(tuple, r['cells'])) for r in loop}, key=len)[:5]:
    res = c.model(sorted(base), frozenset(cells))
    lit = 'room' in res and any(c.check_path(c.norm(res['room']), p, c.MARKS)[0]
                                for r in loop for rm, p in [(r['room'], r['path'])] + [L.image(g, r['room'], r['path']) for g in L.MAPS])
    reopened.append(dict(cells=cells, without_claude_rays=res['status'], lit_by_a_claude_ray=lit))
print(json.dumps(dict(drop_control=reopened)), flush=True)
(L.HERE/'claude-rays-1-1.json').write_text(json.dumps(dict(
    target=[1, 1], marks=[[0, 0], [2, 2]],
    note='Each ray checked by Claude exact checker; its images under (y,x), (2-x,2-y), (2-y,2-x) are also valid.',
    rays=traced + [dict(room=r['room'], path=r['path']) for r in loop]))+'\n')
