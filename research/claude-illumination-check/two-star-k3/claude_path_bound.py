"""Claude's own enumeration of the cell-path charge minimum for I=2/k=3, D>=3."""
import json, sys
from itertools import combinations
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent/'three-star'))
from claude_three_star_reduction import neighbors
NB = ((1, 0), (-1, 0), (0, 1), (0, -1))

def minimum(target):
    full = [(0, 0), tuple(target)]
    R = set(full) | neighbors(full); b = len(R) - 2; assert b == 8
    allowed = {(x, y) for x in range(-12, 18) for y in range(-12, 18) if min(abs(x-u)+abs(y-v) for u, v in R) <= 2}
    outside = sorted(allowed - R); best = None
    for n in range(3):
        for add in combinations(outside, n):
            cells = R | set(add)
            def dfs(path, cost):
                nonlocal best
                p = path[-1]
                if p == full[1]:
                    best = cost if best is None else min(best, cost); return
                if best is not None and cost >= best: return
                for dx, dy in NB:
                    q = (p[0]+dx, p[1]+dy)
                    if q not in cells or q in path: continue
                    c = 0
                    if len(path) > 1:
                        a = path[-2]
                        c = (3 if (p[0]-a[0], p[1]-a[1]) == (dx, dy) else 2) - (p in R)
                    dfs(path+[q], cost+c)
            dfs([full[0]], 0)
    return b + best

if __name__ == '__main__':
    out = {}
    for t in [(2, 1), (3, 0), (2, 2), (3, 1), (4, 0), (3, 2), (4, 1), (5, 0)]:
        mn = minimum(t)
        out[str(t)] = dict(min_Q_plus_m=mn, wall_lower_bound=8+mn, closed_form=2*sum(t)+4+max(0, t[0]-t[1]-1),
                           excluded_by_bound_alone=8+mn >= 24)
        print(t, out[str(t)], flush=True)
    (HERE/'claude-path-bound.json').write_text(json.dumps(out, indent=1)+'\n')
