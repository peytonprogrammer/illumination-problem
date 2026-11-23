"""Per-class certificates on the rooms SAVED by d8-perturbation-test (no new room search).

Input: ../d8-perturbation-test/results.jsonl (1,027 rooms, each with same-class interior
pairs, the N_min verdict `separated`, and the LIT/DARK verdict with a traced witness).
For each saved pair the script computes, with the pair's class as class a:

  * whether B_b, B_c, B_d (finest factor with no regular point over one class) separate
    the lifts, and whether their join B_min does;
  * the static certificates Par, Rig, Cut of Theorem U over every block system.

Questions:
  1. soundness on rooms: is any LIT pair fully certified?  (must be 0)
  2. second kind: is any pair certified in all three classes while B_min does not separate?
  3. teeth: how many LIT pairs are certified in two of three classes?

Run: python3 -B check_saved_rooms.py     (writes check_saved_rooms.json)
"""
import json
from collections import Counter
from pathlib import Path

from roomtools import *
import unified_test as U

SRC = HERE.parent / 'd8-perturbation-test' / 'results.jsonl'


def main():
    S = Counter()
    kinds = Counter()
    flagged = []
    cache = {}
    for line in SRC.open():
        r = json.loads(line)
        cells = {tuple(c) for c in r['cells']}
        for p in r.get('pairs', []):
            s_pt, t_pt = tuple(p['p']), tuple(p['q'])
            key = (r['id'], s_pt[0] % 2, s_pt[1] % 2)
            if key not in cache:
                cache.clear()
                room, t = room_tuple(cells, s_pt)
                systems = d4.all_block_systems(list(t), len(t[0]))
                cache[key] = (s_pt, room, t, [U.Factor(t, part) for part in systems],
                              {x: class_congruence(t, cl) for x, cl in
                               (('b', [1]), ('c', [2]), ('d', [3]), ('min', [1, 2, 3]))})
            origin, room, t, factors, cong = cache[key]
            LS, LT = lifts(room, t, s_pt, origin), lifts(room, t, t_pt, origin)
            assert LS and LT
            sep = {}
            for x, part in cong.items():
                iS = {a_image(t, part, s[0])[0] for s in LS}
                iT = {a_image(t, part, s[0])[0] for s in LT}
                sep[x] = not (iS & iT)
            per_class = {x: None for x in (1, 2, 3)}
            for s in LS:
                for q in LT:
                    _, _, perx, _ = U.analyse_pair(t, factors, s[0], q[0])
                    for x in (1, 2, 3):
                        per_class[x] = perx[x] if per_class[x] is None else per_class[x] & perx[x]
            # a class counts as certified when every lift pair has a certificate there
            blocked = 0
            for x in (1, 2, 3):
                ok = True
                for s in LS:
                    for q in LT:
                        if not U.analyse_pair(t, factors, s[0], q[0])[2][x]:
                            ok = False
                blocked += ok
            lit = p['verdict'] == 'LIT'
            S['pairs'] += 1
            S['LIT' if lit else 'DARK'] += 1
            S['%s, %d of 3 classes certified' % ('LIT' if lit else 'DARK', blocked)] += 1
            S['B_min separates'] += sep['min']
            if sep['min'] != p['separated']:
                S['B_min verdict differs from the saved d8 verdict'] += 1
            if all(sep[x] for x in 'bcd') and not sep['min']:
                S['B_b, B_c, B_d separate but B_min does not'] += 1
            if blocked == 3 and lit:
                S['LIT pair fully certified (unsound)'] += 1
            if blocked == 3 and not sep['min']:
                S['fully certified without a separating parity factor (second kind)'] += 1
                flagged.append(dict(id=r['id'], p=s_pt, q=t_pt))
            if blocked == 3:
                kinds[' / '.join('+'.join(sorted(per_class[x])) for x in (1, 2, 3))] += 1
            for x in (1, 2, 3):
                for kind in per_class[x] or ():
                    S['class certificates of kind ' + kind] += 1
    print(dict(S))
    print(dict(kinds))
    out = dict(counts=dict(S), full_certificate_kinds=dict(kinds), flagged=flagged)
    (HERE / 'check_saved_rooms.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
