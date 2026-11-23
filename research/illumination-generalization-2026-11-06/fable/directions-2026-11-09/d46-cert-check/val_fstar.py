"""d46 requirement 2: the C F* (cert_check fstar_dump) against d44 filter_rate.passes and the
d45 referee's fstar() (check_fstar.py), on every reflex-class vector rho and every area n.
Required range: r = 5..8, 21 <= n <= 5r.  Extended range: r = 0..15, 1 <= n <= 63 (C vs passes;
the referee's version also allows d = 2, so it is compared on the required range only, where the
referee showed the two agree).
"""
import ast, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
P = HERE.parent

def defs(path):
    mod = ast.parse(path.read_text()); mod.body = [b for b in mod.body if isinstance(b, ast.FunctionDef)]
    ns = {}; exec(compile(mod, str(path), 'exec'), ns); return ns

d44 = defs(P / 'd44-cert-check-sizing' / 'filter_rate.py')
d45 = defs(P / 'd45-review-fstar' / 'check_fstar.py')

def c_dump(r0, r1, n0, n1):
    out = subprocess.run([str(HERE / 'cert_check'), 'fstar_dump', str(r0), str(r1), str(n0), str(n1)],
                         capture_output=True, text=True, check=True).stdout
    for ln in out.splitlines():
        r, a, b, c, d, n, v = map(int, ln.split())
        yield r, [a, b, c, d], n, v

allowed = {}
cnt = mm44 = mm45 = 0
for r, rho, n, v in c_dump(5, 8, 21, 40):
    if n > 5 * r:
        continue
    cnt += 1
    mm44 += v != bool(d44['passes'](rho, n, r))
    mm45 += v != bool(d45['fstar'](rho, n, r))
    if v:
        allowed.setdefault(r, set()).add(n)
print('required range r 5..8, 21 <= n <= 5r: (rho, n) cases', cnt, 'mismatch vs d44 passes', mm44, 'mismatch vs d45 fstar', mm45)
for r in sorted(allowed):
    print('  r', r, 'areas with some passing rho:', sorted(allowed[r]))
cnt = mm = 0
for r, rho, n, v in c_dump(0, 15, 1, 63):
    cnt += 1
    mm += v != bool(d44['passes'](rho, n, r))
print('extended range r 0..15, 1 <= n <= 63: cases', cnt, 'mismatch vs d44 passes', mm)
