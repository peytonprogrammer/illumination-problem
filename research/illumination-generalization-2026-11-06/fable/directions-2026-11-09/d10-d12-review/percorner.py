"""Join u_nN.json (certificates) with m_nN.json (per-corner lit sets, reviewer's own).

Checks:
  * corner-by-corner soundness of Theorem U over B: a certificate at x implies not x-lit;
  * the d12 counts of uncertified dark pair-corners and of PRIM one-mirror witnesses;
  * the n = 8 counterexample to the per-corner converse.

Run: python3 -B percorner.py 4 5 6 7 8 9 10
"""
import json
import sys
from collections import Counter

from lib import census_orbits, load_out

CEX = [[1, 2, 0, 4, 3, 6, 5, 7], [0, 1, 2, 3, 4, 5, 7, 6], [5, 6, 3, 2, 7, 0, 1, 4],
       [6, 7, 4, 1, 5, 2, 0, 3]]

tot = Counter()
for n in [int(a) for a in sys.argv[1:]]:
    U = {(json.dumps(p['rep']), p['P'], p['Q']): p
         for p in load_out(f'u_n{n}.json')['pairs']}
    M = load_out(f'm_n{n}.json')['orbits']
    S = Counter()
    for o in M:
        cts = o['cts']
        prim_hyp = o['primitive'] and all(len(c) < n for c in cts[1:]) and any(2 in c for c in cts[1:])
        for p in o['pairs']:
            u = U[(json.dumps(o['rep']), p['P'], p['Q'])]
            assert u['lit'] == p['lit'] == bool(any(p['lit_x']))
            for xi in range(3):
                S['pair-corners'] += 1
                cert = bool(u['certB'][xi])
                xl = bool(p['lit_x'][xi])
                S['x-lit with a certificate at x (Theorem U false at a corner)'] += (cert and xl)
                S['not x-lit, no certificate over B'] += (not cert and not xl)
                S['not x-lit, no certificate over B, pair DARK'] += (not cert and not xl and not p['lit'])
                S['not x-lit, certificate over B'] += (cert and not xl)
                if prim_hyp and 2 in cts[xi + 1]:
                    S['PRIM pair-corners with a 2-cycle at x'] += 1
                    S['PRIM pair-corners one-mirror x-lit'] += p['one_x'][xi]
            if prim_hyp:
                S['PRIM pairs'] += 1
                S['PRIM pairs with a one-mirror witness'] += bool(any(p['one_x']))
            if p['lit']:
                S['LIT pairs'] += 1
                S['LIT pairs with a one-mirror witness'] += bool(any(p['one_x']))
        if o['rep'] == CEX:
            print('   n = 8 counterexample: |G| =', o['order'], 'primitive', o['primitive'],
                  'plain', o['plain'], 'pairs', [(p['lit'], p['lit_x'],
                  U[(json.dumps(o['rep']), p['P'], p['Q'])]['certB']) for p in o['pairs']])
    print(n)
    for k, v in S.items():
        print('   ', k, v)
    tot.update(S)
print('total')
for k, v in tot.items():
    print('   ', k, v)

# Nielsen classes quoted in the notes
for n, cts in ((6, [[2, 2, 1, 1], [2, 2, 1, 1], [3, 2, 1], [3, 2, 1]]),
               (7, [[2, 2, 2, 1], [3, 2, 1, 1], [3, 2, 1, 1], [3, 2, 1, 1]])):
    print('class', n, cts, [(o['plain_orbit_size'], o['order']) for c, o in census_orbits(n) if c == cts])
