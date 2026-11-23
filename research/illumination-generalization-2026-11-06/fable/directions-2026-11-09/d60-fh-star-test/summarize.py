"""Tabulate fh_star_*.json. Run: python3 -B summarize.py"""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
for f in ('fh_star_cross12.json', 'fh_star_dumb12.json', 'fh_star_R22.json', 'fh_star_P6.json',
          'fh_star_wall_cross12.json', 'fh_star_wall_R22.json'):
    rows = json.load(open(HERE / f))
    for r in rows:
        r['S'], r['T'] = tuple(r['S']), tuple(r['T'])
    pairs = {(r['S'], r['T']) for r in rows}
    same = {(r['S'], r['T']) for r in rows if r['cls_T'] == 'a'}
    print('==', f, '| pairs', len(pairs), '(same class %d)' % len(same))
    for minimal in (True, False):
        sub = [r for r in rows if r['minimal'] == minimal]
        if not sub:
            continue
        c = Counter(r['verdict_weak'].split(' (')[0] for r in sub)
        strong = Counter(r['strong'] for r in sub if r['hyp'])
        eqv = Counter(r['equal_images'] for r in sub if r['verdict_weak'] == 'VIOLATION')
        print('  N %s: (room, N, pair) rows %d  WEAK verdicts %s  STRONG {holds: %d, fails: %d, '
              'not computed: %d}  violations with equal images: %d'
              % ('minimal' if minimal else 'non-minimal', len(sub), dict(c), strong[True], strong[False],
                 strong[None], eqv[True]))
    truth = {(r['S'], r['T']): (r['truth'], r['certified'], r['cls_T']) for r in rows}
    sound = sum(1 for v in truth.values() if v[1] and v[0] == 'lit')
    unc = sum(1 for v in truth.values() if v[2] == 'a' and not v[1] and v[0] == 'dark')
    print('  ground truth: %d lit, %d dark; certified-but-lit %d; same-class dark-uncertified %d'
          % (sum(v[0] == 'lit' for v in truth.values()), sum(v[0] == 'dark' for v in truth.values()),
             sound, unc))
    for r in rows:
        if r['certified'] and r['minimal']:
            print('   cert %s-%s:' % (r['S'], r['T']), sorted({c['desc'] for c in r['cert']}))
