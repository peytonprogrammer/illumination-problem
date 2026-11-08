"""Re-solve only the open (1,1) outside sets. Adding verified cuts can't reopen an excluded
set, so the 2,484 excluded sets stay excluded. Cuts: Codex's certificate witnesses, plus
optionally Claude's own traced rays (CLAUDE_OWN=1)."""
import json, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
os.environ['CLAUDE_TARGET'] = '1,1'; os.environ['CLAUDE_PLACEMENT_INPUTS'] = str(HERE/'cert/run/.context')
sys.path.insert(0, str(HERE.parent/'placement-2-1'))
import claude_placement_check as c
stats, cuts = c.collect(); cuts = set(cuts)
prev = json.loads((HERE/'claude-placement-1-1.json').read_text())
old = set()
_, oldcuts = None, None
if os.environ.get('CLAUDE_OWN') == '1':
    for r in json.loads((HERE/'claude-placement-1-1-traced.json').read_text()):
        room = c.norm(r['room']); path = r.get('path')
        f = HERE/f"unlit-{'_'.join(f'{a}{b}' for a, b in r['cells'])}.json"
        if not r.get('verified'): path = json.loads(f.read_text())['retrace']['path']
        ok, _, touched = c.check_path(room, path, c.MARKS); assert ok
        cuts.add(tuple(sorted((c.index[t], int(t in room)) for t in touched if t in c.index)))
cuts = sorted(cuts)
print(json.dumps(stats | dict(cuts=len(cuts), own=os.environ.get('CLAUDE_OWN') == '1')), flush=True)
os.environ['CLAUDE_CAP'] = '120'
still = []
for leaf in prev['open']:
    res = c.model(cuts, frozenset(map(tuple, leaf['cells'])))
    if res['status'] != 'INFEASIBLE':
        still.append(dict(cells=leaf['cells'], status=res['status'], room=res.get('room')))
print(json.dumps(dict(previously_open=len(prev['open']), still_open=len(still), statuses=sorted({s['status'] for s in still}))), flush=True)
tag = 'own' if os.environ.get('CLAUDE_OWN') == '1' else 'codex'
(HERE/f'claude-recheck-open-{tag}.json').write_text(json.dumps(dict(stats=stats, cuts=len(cuts), open=still), indent=1)+'\n')
