"""d45: compare d44 filter_rate.passes with an independent F* on every rho vector, r = 5..8,
and recompute the allowed-area lists (some rho vector passes)."""
import ast, itertools
from pathlib import Path
src = (Path(__file__).resolve().parent.parent / 'd44-cert-check-sizing' / 'filter_rate.py').read_text()
mod = ast.parse(src); mod.body = [b for b in mod.body if isinstance(b, ast.FunctionDef)]
ns = {}; exec(compile(mod, 'filter_rate_defs', 'exec'), ns)

def zmin(d): return -(-(d - 1) // 4) if d % 2 else -(-d // 4)
def mine(rho, n, r):
    return any(sum(x // dl for x in rho) >= zmin(n // dl) and zmin(n // dl) * dl <= r
               for dl in range(3, n + 1) if n % dl == 0 and n // dl >= 3)
claimed = {5: {25}, 6: {21, 24, 25, 27, 30}, 7: {21, 24, 25, 27, 28, 30, 35},
           8: {21, 24, 25, 27, 28, 30, 32, 35, 36, 40}}
for r in range(5, 9):
    allowed = set(); mism = 0
    for rho in itertools.product(range(r + 1), repeat=4):
        if sum(rho) != r: continue
        for n in range(21, 5 * r + 1):
            a, b = ns['passes'](list(rho), n, r), mine(rho, n, r)
            mism += a != b
            if b: allowed.add(n)
    print('r', r, 'mismatches', mism, 'allowed', sorted(allowed), 'matches README', allowed == claimed[r])
