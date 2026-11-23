"""Per-variant table (results.tsv) and aggregates, merging reruns.

usage: python3 -B report53.py results.tsv RUNS... -- RERUNS...
"""
import json
import sys
from collections import defaultdict

out = sys.argv[1]
i = sys.argv.index('--')
runs, reruns = sys.argv[2:i], sys.argv[i + 1:]
rows = [json.loads(l) for f in runs for l in open(f)]
final = {}
for f in reruns:                       # later files win
    for l in open(f):
        r = json.loads(l)
        final[(r['k'], r['name'])] = r


def wit(b):
    return ('%d,%d' % tuple(b['dir']), b['m'], b['refl'], b['faces'] or '-', b['dQ2'], b['replay']) if b else ('', '', '', '', '', '')


cols = ['k', 'family', 'name', 'status', 'W', 'N', 'points', 'pairs', 'unlit_run1', 'bound_run1', 'unlit_final', 'bound_final',
        'need_pq', 'best_dir', 'best_m', 'best_refl', 'best_faces', 'best_dQ2', 'best_replay',
        'first_dir', 'first_m', 'first_refl', 'first_faces', 'first_dQ2', 'first_replay', 'in_d11']
agg = defaultdict(lambda: dict(n=0, ok=0, bad=defaultdict(int), W=[], le21=0, eq22=0, pairs=0, unlit=0, need=0))
with open(out, 'w') as fh:
    fh.write('\t'.join(cols) + '\n')
    for r in rows:
        if r['family'] == 'win1' and r['status'] != 'ok':
            agg[(r['k'], 'win1')]['bad'][r['status']] += 1
            agg[(r['k'], 'win1')]['n'] += 1
            continue                   # keep the table to rooms that exist as strictly simple rooms
        k, fam = r['k'], r['family']
        a = agg[(k, fam)]
        a['n'] += 1
        if r['status'] not in ('ok', 'pinched'):
            a['bad'][r['status']] += 1
            fh.write('\t'.join(map(str, [k, fam, r['name'], r['status'], r.get('W') or ''] + [''] * (len(cols) - 5))) + '\n')
            continue
        f = final.get((k, r['name']))
        unl = f['unlit'] if f else r['unlit']
        bfin = f['bound'] if f else r['bound']
        need = f['lastsum'] if f else r['lastsum']
        in_d11 = r['status'] == 'ok' and r['N'] <= 32 and r['W'] <= 24
        if r['status'] == 'ok':
            a['ok'] += 1
            a['W'].append(r['W'])
            a['le21'] += r['W'] <= 21
            a['eq22'] += r['W'] == 22
            a['pairs'] += r['pairs']
            a['unlit'] += unl
            a['need'] = max(a['need'], need)
            assert r['best'] is None or (r['best']['replay'] and r['first']['replay']), r['name']
        else:
            a['pinch_unlit'] = unl
            a['pairs'] += r['pairs']
            a['pinch_pts'] = r['n_points']
        fh.write('\t'.join(map(str, [k, fam, r['name'], r['status'], r['W'], r['N'], r['n_points'], r['pairs'], r['unlit'], r['bound'], unl, bfin, need,
                                      *wit(r['best']), *wit(r['first']), int(in_d11)])) + '\n')

print('| k | family | candidates | strictly simple | not simple / other | W range | W <= 21 | W = 22 | pairs tested | unlit pairs (final) | max p+q needed |')
print('|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|')
tot = defaultdict(int)
for (k, fam), a in sorted(agg.items()):
    if fam == 'pinched':
        print('| %d | pinched | 1 | - | - | 22 | - | - | %d | %d (the marks) | - |' % (k, a['pairs'], a['pinch_unlit']))
        continue
    bad = ', '.join('%s %d' % kv for kv in sorted(a['bad'].items())) or '-'
    wr = '%d-%d' % (min(a['W']), max(a['W'])) if a['W'] else '-'
    print('| %d | %s | %d | %d | %s | %s | %d | %d | %d | %d | %d |' % (k, fam, a['n'], a['ok'], bad, wr, a['le21'], a['eq22'], a['pairs'], a['unlit'], a['need']))
    for key in ('ok', 'le21', 'eq22', 'pairs', 'unlit'):
        tot[key] += a[key]
print('totals (resolutions):', dict(tot))
