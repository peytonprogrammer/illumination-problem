"""Negative control: drop each core cut in turn; count how many drops make the fixed neck feasible."""
import json, sys, os
os.environ.setdefault('CLAUDE_WORKERS', '4')
sys.argv = [sys.argv[0]]
import claude_midpoint_check as c  # reruns the main check; cheap
from claude_k3_strong import build
core = c.core['core_guard_indices']; feasible = []
for i in core:
    res = build(c.TARGET, use_cuts=False, extra=c.restrict([j for j in core if j != i]))
    if res['status'] in ('OPTIMAL', 'FEASIBLE'):
        lit = c.check_path(c.norm(res['room']), c.guards[i]['witness']['path'], c.MARKS)[0]
        feasible.append(dict(dropped=i, walls=res['walls'], dropped_ray_lights_it=lit))
print(json.dumps(dict(core=len(core), drops_that_reopen=len(feasible), detail=feasible)))
