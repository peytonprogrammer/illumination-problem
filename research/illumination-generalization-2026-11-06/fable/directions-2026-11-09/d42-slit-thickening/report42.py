"""Summarise run42 results: per-variant TSV and aggregated tables.
usage: python3 -B report42.py out.tsv file.jsonl ...
"""
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from math import sqrt


def on_seg(P, a, b):
    if (b[0] - a[0]) * (P[1] - a[1]) - (b[1] - a[1]) * (P[0] - a[0]) != 0:
        return False
    return min(a[0], b[0]) <= P[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= P[1] <= max(a[1], b[1])


def faces(r, key):
    w = r[key]
    if not w or not r.get('obs'):
        return ''
    obs = [tuple(p) for p in r['obs']]
    k = r['k']
    tags = []
    for x, y, _ in w['hits']:
        P = (Fr(x), Fr(y))
        t = 'o'
        for i in range(len(obs)):
            a, b = obs[i], obs[(i + 1) % len(obs)]
            if a[1] == k and b[1] == k:
                continue
            if on_seg(P, a, b):
                t = 'S' if a[0] == b[0] else 'E'
        tags.append(t)
    return ''.join(tags)


rows = []
seen = set()
for f in sys.argv[2:]:
    for l in open(f):
        r = json.loads(l)
        if r['status'] != 'ok':
            continue
        key = (r['k'], r['kind'], r['w'], r['xl'], r['top'], r['end'])
        if key in seen:
            continue
        seen.add(key)
        rows.append(r)
rows.sort(key=lambda r: (r['k'], r['kind'], r['w'], r['xl'], r['top'], r['end']))
with open(sys.argv[1], 'w') as fh:
    fh.write('k\tkind\tplace\tw\txl\ttop\tend\tW\tc\tN_tiles\tpoints\tpairs\tunlit\tbound\tlastsum\tbest_dir\tbest_m\tbest_len_over_k\tbest_refl\tbest_faces\tfirst_dir\tfirst_refl\tfirst_faces\treplay\tobstacle\n')
    for r in rows:
        b, f0 = r['best'], r['first']
        fh.write('\t'.join(map(str, [r['k'], r['kind'], r.get('place', '-'), r['w'], r['xl'], r['top'], r['end'], r['W'], r['c'], r['N'],
                                      r['n_points'], r['pairs'], r['unlit'], r['bound'], r['lastsum'],
                                      b and tuple(b['dir']), b and b['m'], b and round(sqrt(b['len2_room']) / r['k'], 3), b and b['refl'], faces(r, 'best'),
                                      f0 and tuple(f0['dir']), f0 and f0['refl'], faces(r, 'first'),
                                      (b['replay'] and f0['replay']) if b else '-', r.get('obs')])) + '\n')
# aggregate per (k, kind)
agg = defaultdict(lambda: Counter())
for r in rows:
    a = agg[(r['k'], r['kind'])]
    a['variants'] += 1
    a['pairs'] += r['pairs']
    a['unlit'] += r['unlit']
    a['W<=21'] += r['W'] <= 21
    a['minW'] = min(a['minW'] or 99, r['W'])
    a['maxlastsum'] = max(a['maxlastsum'], r['lastsum']) if r['kind'] != 'slit' else a['maxlastsum']
print('| k | kind | variants | W <= 21 | min W | pairs tested | unlit pairs | max p+q needed |')
print('|---:|---|---:|---:|---:|---:|---:|---:|')
for (k, kind), a in sorted(agg.items()):
    print('| %d | %s | %d | %d | %d | %d | %d | %s |' % (k, kind, a['variants'], a['W<=21'], a['minW'], a['pairs'], a['unlit'], a['maxlastsum'] if kind != 'slit' else '-'))
# witness trend for thick variants
print()
print('thick: best witness reflections by k (min / median / max), and share hitting the end face')
for k in sorted({r['k'] for r in rows}):
    th = [r for r in rows if r['k'] == k and r['kind'] == 'thick' and r['best']]
    if not th:
        continue
    rf = sorted(r['best']['refl'] for r in th)
    ln = sorted(sqrt(r['best']['len2_room']) / k for r in th)
    endhit = sum('E' in faces(r, 'best') for r in th)
    anyobs = sum(any(t in faces(r, 'best') for t in 'ES') for r in th)
    print(k, len(th), 'refl', rf[0], rf[len(rf) // 2], rf[-1], 'len/k', round(ln[0], 2), round(ln[len(ln) // 2], 2), round(ln[-1], 2),
          'end-face', endhit, 'any obstacle face', anyobs)
