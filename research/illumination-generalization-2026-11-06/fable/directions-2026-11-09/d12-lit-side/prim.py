"""PRIM summary from mine_n*.json: verdicts, one-mirror witnesses, and the group M."""
import sys, json
from collections import Counter
from math import factorial
from pathlib import Path
HERE = Path(__file__).resolve().parent
for n in [int(a) for a in sys.argv[1:]]:
    d = json.loads((HERE / f'mine_n{n}.json').read_text())
    S = Counter()
    for o in d['orbits']:
        cts = o['cts']
        if not o['primitive']:
            continue
        S['primitive orbits'] += 1
        hyp = all(len(c) < n for c in cts[1:]) and any(2 in c for c in cts[1:])
        if not hyp:
            S['primitive orbits outside PRIM hypotheses'] += 1
            S['  their pairs: LIT'] += sum(1 for p in o['pairs'] if p['lit'])
            S['  their pairs: DARK'] += sum(1 for p in o['pairs'] if not p['lit'])
            continue
        S['PRIM orbits'] += 1
        S['PRIM orbits with G not containing A_n'] += (not o['contains_An'])
        q = o['q']
        S['PRIM orbits, M = S_q'] += (o['M_order'] == factorial(q))
        S['PRIM orbits, M 2-homogeneous (one orbit on pairs)'] += (o['M_pair_orbits'] == 1)
        if o['M_pair_orbits'] != 1:
            print('   M not 2-homogeneous:', n, cts, 'q', q, '|M|', o['M_order'], 'pair orbits', o['M_pair_orbits'], '|G|', o['order'])
        if o['M_order'] != factorial(q) and o['M_pair_orbits'] == 1:
            S[f'PRIM orbits, M 2-homogeneous but not S_q (q={q}, |M|={o["M_order"]})'] += 1
        for p in o['pairs']:
            S['PRIM pairs'] += 1
            S['PRIM pairs LIT'] += bool(p['lit'])
            mc = [m for m in p['minchain_x'] if m]
            S['PRIM pairs with a one-mirror witness'] += (bool(mc) and min(mc) == 1)
            ncorner = sum(1 for xi in range(3) if 2 in cts[xi + 1])
            S['PRIM pair-corners (corner has a 2-cycle)'] += ncorner
            S['PRIM pair-corners x-lit'] += sum(1 for xi in range(3) if 2 in cts[xi + 1] and p['lit_x'][xi])
            S['PRIM pair-corners one-mirror x-lit'] += sum(1 for xi in range(3) if p['minchain_x'][xi] == 1)
            S['PRIM pairs with a cylinder witness'] += any(p['cyl_x'])
    print(n)
    for k, v in S.items():
        print('   ', k, v)
