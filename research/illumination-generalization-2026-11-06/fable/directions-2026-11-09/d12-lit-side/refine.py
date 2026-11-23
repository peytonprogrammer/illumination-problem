"""Second-pass questions on mine_n*.json (reads saved data only).

A. PRIM per corner: G primitive, no identity among g_b, g_c, g_d, g_x has a 2-cycle
   => every pair x-lit?  every pair x-lit by one mirror?
B. Is x-lit an equivalence relation?  How many tests are nontrivial (three distinct
   points with two of the three pairs x-lit)?  Do failures need a proper pillowcase factor?
C. Per corner version of U*: not x-lit <=> Par/Rig/Cut over B at x.  Do the exceptions all
   have a proper pillowcase factor?
"""
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
import d4_monodromy as d4          # noqa: E402
import unified_test as UT          # noqa: E402


def has_proper_pillow(t, n):
    for part in d4.all_block_systems(list(t), n):
        if 1 < len(part) < n:
            if UT.is_pillowcase(UT.Factor(t, part)):
                return True
    return False


def main():
    for n in [int(a) for a in sys.argv[1:]]:
        d = json.loads((HERE / f'mine_n{n}.json').read_text())
        S = Counter()
        ex = {}
        for o in d['orbits']:
            t = tuple(tuple(g) for g in o['rep'])
            cts = o['cts']
            nondeg = all(len(c) < n for c in cts[1:])
            prim = o['primitive'] and nondeg and o['k'] >= 1
            pil = None
            ids = sorted({p['P'] for p in o['pairs']} | {p['Q'] for p in o['pairs']})
            for xi in range(3):
                has2 = 2 in cts[xi + 1]
                rel = {(p['P'], p['Q']): p['lit_x'][xi] for p in o['pairs']}
                one = {(p['P'], p['Q']): (p['lit_x'][xi] and p['minchain_x'][xi] == 1) for p in o['pairs']}
                if prim and has2:
                    S['A: PRIM corner with a 2-cycle'] += 1
                    S['A: pairs'] += len(rel)
                    S['A: pairs x-lit'] += sum(rel.values())
                    S['A: pairs x-lit by one mirror'] += sum(one.values())
                    if not all(rel.values()):
                        ex.setdefault('A fails', []).append((cts, o['rep'], xi + 1))
                # B: transitivity tests
                bad = False
                for tr in combinations(ids, 3):
                    e = [rel[(tr[0], tr[1])], rel[(tr[0], tr[2])], rel[(tr[1], tr[2])]]
                    if sum(e) >= 2:
                        S['B: nontrivial transitivity tests'] += 1
                        if sum(e) == 2:
                            S['B: failures'] += 1
                            bad = True
                excC = [p for p in o['pairs'] if not p['lit_x'][xi] and not p['cert_x'][xi]]
                if bad or excC:
                    if pil is None:
                        pil = has_proper_pillow(t, n)
                    if bad:
                        S['B: corner relations not transitive, proper pillowcase factor=%s' % pil] += 1
                    if excC:
                        S['C: pair-corners not x-lit without cert over B, proper pillowcase factor=%s' % pil] += len(excC)
                        if not pil:
                            ex.setdefault('C no pillow', []).append((cts, o['rep'], xi + 1,
                                                                     [(p['P'], p['Q'], p['lit'], p['same_fibre_x'][xi]) for p in excC]))
                for p in o['pairs']:
                    if p['same_fibre_x'][xi] and not p['lit_x'][xi]:
                        S['same B_x fibre, not x-lit, cert=%s' % (p['cert_x'][xi] or 'none')] += 1
                    if not p['same_fibre_x'][xi]:
                        S['different B_x fibre (Par), not x-lit'] += 1 - p['lit_x'][xi]
        print('=' * 10, 'n =', n)
        for k in sorted(S):
            print('  %-75s %d' % (k, S[k]))
        for k, v in ex.items():
            print('  examples', k, len(v))
            for e in v[:4]:
                print('    ', json.dumps(e))


if __name__ == '__main__':
    main()
