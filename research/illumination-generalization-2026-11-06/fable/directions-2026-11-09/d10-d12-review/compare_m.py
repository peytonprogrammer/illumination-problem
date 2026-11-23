"""Compare m_nN.json (reviewer) with the census and with d12-lit-side/mine_nN.json (authors).

Run: python3 -B compare_m.py 4 5 6 7 8 9 10
"""
import json
import sys
from collections import Counter
from math import factorial

from lib import D12, load_out

tot = Counter()
for n in [int(a) for a in sys.argv[1:]]:
    mine = load_out(f'm_n{n}.json')
    theirs = {json.dumps(o['rep']): o for o in
              json.loads((D12 / f'mine_n{n}.json').read_text())['orbits']}
    S = Counter()
    S['skipped by cap'] = mine['skipped']
    for o in mine['orbits']:
        S['orbits'] += 1
        S['pairs'] += len(o['pairs'])
        S['plain orbit size differs from census'] += (not o['plain_matches_census'])
        S['pairs with verdict different from census'] += o['verdict_mismatch']
        S['orbits with a twist element outside M'] += (not o['twists_in_M'])
        S['orbits with a T1 transposition outside M'] += (not o['pinch_in_M'])
        for k, v in o['stats'].items():
            S['stat ' + k] += v
        # orbit-size identity: marked = plain * |M| / |image of the deck group|
        th = theirs[json.dumps(o['rep'])]
        S['M order differs from d12'] += (o['M_order'] != th['M_order'])
        S['M pair orbits differ from d12'] += (o['M_pair_orbits'] != th['M_pair_orbits'])
        tp = {(p['P'], p['Q']): p for p in th['pairs']}
        for p in o['pairs']:
            S['pair-corners'] += 3
            S['pair-corner x-lit differs from d12'] += sum(
                1 for a, b in zip(p['lit_x'], tp[(p['P'], p['Q'])]['lit_x']) if a != b)
            S['pair-corner one-mirror differs from d12'] += sum(
                1 for a, b in zip(p['one_x'], tp[(p['P'], p['Q'])]['minchain_x']) if a != (b == 1))
        q = o['q']
        hom = o['M_pair_orbits'] == 1
        cts = o['cts']
        prim_hyp = o['primitive'] and all(len(c) < n for c in cts[1:]) and any(2 in c for c in cts[1:])
        S['M 2-homogeneous'] += hom
        nl = sum(1 for p in o['pairs'] if p['lit'])
        S['Prop R violated (2-homogeneous, some LIT, some DARK)'] += (hom and 0 < nl < len(o['pairs']))
        # LIT must be a union of M-orbits on pairs
        by = {}
        for p in o['pairs']:
            by.setdefault(p['pair_orbit'], set()).add(p['lit'])
        S['M-orbits on pairs with mixed census verdict'] += sum(1 for v in by.values() if len(v) > 1)
        if o['contains_An']:
            S['G >= A_n: orbits'] += 1
            S['G >= A_n: M = S_q'] += (o['M_order'] == factorial(q))
            S['G >= A_n: 2-homogeneous, not S_q'] += (hom and o['M_order'] != factorial(q))
            S['G >= A_n: not 2-homogeneous'] += (not hom)
        if prim_hyp:
            S['PRIM: orbits'] += 1
            S['PRIM: not 2-homogeneous'] += (not hom)
            S['PRIM: pairs'] += len(o['pairs'])
            S['PRIM: pairs LIT'] += nl
            if o['contains_An']:
                S['PRIM, G >= A_n: orbits'] += 1
                S['PRIM, G >= A_n: pairs'] += len(o['pairs'])
                S['PRIM, G >= A_n: not 2-homogeneous'] += (not hom)
            if not hom:
                print('   PRIM, not 2-homogeneous:', n, cts, 'q', q, '|M|', o['M_order'],
                      'pair orbits', o['M_pair_orbits'], '|G|', o['order'])
        if o['contains_An'] and not hom:
            print('   G >= A_n, not 2-homogeneous:', n, cts, 'q', q, '|M|', o['M_order'])
        if not o['primitive']:
            S['imprimitive orbits'] += 1
        elif not o['contains_An']:
            S['primitive, no A_n: orbits'] += 1
    print(n)
    for k, v in S.items():
        print('   ', k, v)
    tot.update(S)
print('total')
for k, v in tot.items():
    print('   ', k, v)
