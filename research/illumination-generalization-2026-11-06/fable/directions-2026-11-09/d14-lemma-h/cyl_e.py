"""Orbit-level test of the two sources of one LIT pair (task 2) on the saved d12 data.

For every saved orbit under the PRIM hypotheses the script reads the per-pair fields of
../d12-lit-side/mine_nN.json and counts the orbits in which
  link : some pair has a one-mirror witness (minimal chain length 1 at some corner);
  cyl  : some pair has a cylinder witness of Lemma C (CylA or CylB in some state).
Counts are split by q = 2 and q >= 3, and by G containing A_n or not.

Run: python3 -B cyl_e.py 4 5 6 7 8 9 10
"""
import json
import sys
from collections import Counter
from pathlib import Path

D12 = Path(__file__).resolve().parent.parent / 'd12-lit-side'

tot = Counter()
first = {}
for n in [int(a) for a in sys.argv[1:]]:
    S = Counter()
    for o in sorted(json.loads((D12 / f'mine_n{n}.json').read_text())['orbits'], key=lambda o: o['plain']):
        cts = o['cts']
        if not (o['primitive'] and all(len(c) < n for c in cts[1:]) and any(2 in c for c in cts[1:])):
            continue
        fam = 'AN' if o['contains_An'] else 'PRIM without A_n'
        qq = 'q=2' if o['q'] == 2 else 'q>=3'
        link = any(1 in p['minchain_x'] for p in o['pairs'])
        cyl = any(any(p['cyl_x']) for p in o['pairs'])
        lit = any(p['lit'] for p in o['pairs'])
        S[(fam, qq, 'orbits')] += 1
        S[(fam, qq, 'some pair LIT')] += lit
        S[(fam, qq, 'link')] += link
        S[(fam, qq, 'cyl')] += cyl
        if not cyl and (fam, qq) not in first:
            first[(fam, qq)] = (n, cts, o['plain'], o['order'])
    print(n, dict(sorted(S.items())))
    tot.update(S)
print('TOTAL')
for k, v in sorted(tot.items()):
    print('  ', k, v)
print('first orbit with no cylinder witness for any pair:')
for k, v in sorted(first.items()):
    print('  ', k, v)
