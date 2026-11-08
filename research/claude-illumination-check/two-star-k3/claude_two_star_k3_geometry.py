"""Geometry-only screen for I=2 full A stars with exactly three B/C exceptions.

Claude's own bound: P+m <= 10, so outside cells <= 10-b and the separation D <= 5.
The relaxed model (claude_three_star_replay.build) fixes the two marks as full stars,
requires exactly three exceptions and walls <= 23, and adds no ray cuts. INFEASIBLE
excludes a placement outright; FEASIBLE means rays are needed.
"""
import json
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parent/'three-star'))
from claude_three_star_reduction import neighbors
from claude_three_star_replay import build

TARGETS = [(x, d-x) for d in range(2, 6) for x in range((d+1)//2, d+1)]


def support(target):
    full = [(0, 0), tuple(target)]
    R = set(full) | neighbors(full)
    r = 10 - (len(R) - 2)
    allowed = {(x, y) for x in range(-14, 20) for y in range(-14, 20)
               if min(abs(x-u)+abs(y-v) for u, v in R) <= r}
    return full, allowed, r


if __name__ == '__main__':
    out = []
    for t in TARGETS:
        full, allowed, r = support(t)
        ts, res = build(full, allowed, [])
        row = dict(target=t, outside_budget=r, cells=len(allowed), triangles=len(ts), status=res['status'],
                   walls=res.get('walls'), room=res.get('room'))
        out.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'room'}), flush=True)
    (HERE/'claude-two-star-k3-geometry.json').write_text(json.dumps(out, indent=1)+'\n')
