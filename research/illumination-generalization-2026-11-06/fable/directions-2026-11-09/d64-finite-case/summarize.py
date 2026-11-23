"""d64: aggregate rl_test chunks (data/rl_*.json). Usage: python3 -B summarize.py"""
import glob
import json
from collections import Counter

rows, summ, tot = [], [], Counter()
for f in sorted(glob.glob('data/rl_*.json')):
    J = json.load(open(f))
    rows += J['special_rows']
    summ += J['summary']
    for k, v in (('rows', J['nrows']), ('lit', J['nlit']), ('rows_interior', J['rows_interior']),
                 ('lit_interior', J['lit_interior_pairs'])):
        tot[k] += v
    tot['max_states'] = max(tot['max_states'], J['max_states'])
    tot['max_depth'] = max(tot['max_depth'], J['max_depth'])
print(dict(tot))
key = lambda s: (s['room'], str(s['a']), s['x'])
sd = {key(s): s for s in summ}
print('(room, a, x) cases with 1 < deg N_x < n:', len(summ), ' rooms:', len({s['room'] for s in summ}))
print('cases by delta:', sorted(Counter(s['k'] for s in summ).items()))
print('cases by (delta, zeros N_x):', sorted(Counter((s['k'], s['zerosNx']) for s in summ).items()))
dark = [r for r in rows if not r['lit']]
print('dark', len(dark), 'counterexamples', sum(r['counterexample'] for r in dark), 'unresolved',
      sum(r['unresolved'] for r in dark), 'rigRy', sum(r['rigRy'] for r in dark), 'rig any',
      sum(r['rig'] for r in dark), 'cut', sum(r['cut'] for r in dark))
print('soundness violations (lit and rigRy):', sum(r['lit'] and r['rigRy'] for r in rows))


def kind(r):
    return 'same point' if r['pA'] == r['pB'] else '-'.join(sorted((r['sA'], r['sB'])))


print('dark by kind:', dict(Counter(kind(r) for r in dark)))
print('dark rooms:', len({r['room'] for r in dark}), ' rooms with a distinct-interior dark row:',
      len({r['room'] for r in dark if kind(r) == 'interior-interior'}))
print('dark by (delta, deg N_x, zeros N_x):', sorted(Counter(
    (sd[key(r)]['k'], sd[key(r)]['degNx'], sd[key(r)]['zerosNx']) for r in dark).items()))
print('dark by n:', sorted(Counter(r['n'] for r in dark).items()))
ii = sorted([r for r in dark if kind(r) == 'interior-interior'], key=lambda r: (r['n'], r['room']))
print('smallest distinct-interior counterexample rows:')
for r in ii:
    if r['room'] != ii[0]['room']:
        break
    print('  ', {k: r[k] for k in ('room', 'n', 'a', 'x', 'pA', 'pB', 'A', 'B', 'states')}, sd[key(r)])
sm = sorted(dark, key=lambda r: (r['n'], r['room']))[0]
print('smallest counterexample overall:', {k: sm[k] for k in ('room', 'n', 'a', 'x', 'pA', 'sA', 'pB', 'sB', 'states')},
      sd[key(sm)])
