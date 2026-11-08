"""Check every lighting certificate's path with Claude's exact checker, in the room U (Z absent)."""
import sys, time, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
from claude_lit_certs import certificates, around
from fractions import Fraction as F
from claude_ray_guard_check import check_path
for q in [tuple(map(int, a.split(','))) for a in sys.argv[1:]]:
    t0 = time.time(); cs = certificates(q); bad = vac = 0
    stars = around(F(0), F(0)) | around(F(q[0]), F(q[1]))
    for U, Z, path in cs:
        if Z & stars:
            vac += 1; continue
        ok, why, _ = check_path(frozenset(U | stars), [[[c.numerator, c.denominator] for c in p] for p in path], [(0, 0), q])
        bad += not ok
        if not ok: print('BAD', q, why, path)
    print(json.dumps(dict(q=q, certs=len(cs), vacuous=vac, bad=bad, seconds=round(time.time()-t0, 1), sizes=sorted(len(c[0]) for c in cs)[:5])), flush=True)
