"""Compare replayed result JSON files with the saved originals, ignoring timing keys."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; SRC = HERE.parent
def strip(x):
    if isinstance(x, dict): return {k: strip(v) for k, v in x.items() if 'seconds' not in k}
    if isinstance(x, list): return [strip(v) for v in x]
    return x
def diff(a, b, path, out):
    if type(a) != type(b): out.append(path); return
    if isinstance(a, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b: out.append(f'{path}.{k} (missing)')
            else: diff(a[k], b[k], f'{path}.{k}', out)
    elif isinstance(a, list):
        if len(a) != len(b): out.append(f'{path} (len {len(a)} vs {len(b)})')
        else:
            for i, (u, v) in enumerate(zip(a, b)): diff(u, v, f'{path}[{i}]', out)
    elif a != b: out.append(f'{path}: {a!r} vs {b!r}')
pairs = [('d21-bipole', f'result_d{d}.json') for d in range(2, 9)] + \
        [('d22-structured', f) for f in ['result_small.json', 'result_exh_d4.json', 'result_exh_d6_P1.json'] + [f'result_z1_d{d}.json' for d in range(2, 9)]] + \
        [('d23-equivariance', 'result_groups.json')]
for d, f in pairs:
    new = HERE / 'replay' / d / f
    if not new.exists(): print(f'{d}/{f}: NOT REPLAYED'); continue
    out = []; diff(strip(json.load(open(SRC / d / f))), strip(json.load(open(new))), '', out)
    print(f'{d}/{f}: ' + ('IDENTICAL (timing keys ignored)' if not out else f'{len(out)} DIFFS: ' + '; '.join(out[:6])))
