"""Counts for d61. Run: python3 -B summarize.py fc.json [fc_wall.json ...]"""
import json, sys
from collections import Counter

for fn in sys.argv[1:]:
    rows = json.load(open(fn))
    C = Counter()
    arcs = {}
    for r in rows:
        lvl = 'B' if r['blocks'] == 1 else ('min' if r['minimal'] else 'nonmin')
        key = (r['room'], lvl)
        C[key + ('rows',)] += 1
        C[key + ('H agrees',)] += r['H'] == r['lit_x']
        C[key + ('Hfull disagrees',)] += r['Hfull'] != r['lit_x']
        dark = not r['lit_x']
        cert = bool(r['cert_x'])
        C[key + ('dark_x',)] += dark
        C[key + ('dark_x & cert',)] += dark and cert
        C[key + ('dark_x & NO cert',)] += dark and not cert
        C[key + ('lit_x & cert (must be 0)',)] += (not dark) and cert
        if dark and cert:
            C[key + ('dark_x cert kinds',) + tuple(sorted(set(
                '%s/%s%s' % (k, m, '=' if e else '!=') for k, m, e in r['cert_detail'])))] += 1
        if r['lit_x']:
            for w in r['witness']:
                C[key + ('witness kind',) + (w,)] += 1
        arcs[(r['room'], lvl, r['tag'], r['blocks'], r['fid'])] = r['arcs']
    for k, v in arcs.items():
        C[k[:2] + ('arc instances',)] += v
    print('==', fn)
    for k in sorted(C, key=str):
        print('  ', k, C[k])
