"""Aggregate mine_n*.json into tables (printed; small JSON written as summary.json)."""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ns = [int(a) for a in sys.argv[1:]] or [4, 5, 6, 7, 8, 9, 10]
    summ = {}
    for n in ns:
        f = HERE / f'mine_n{n}.json'
        if not f.exists():
            continue
        d = json.loads(f.read_text())
        S = Counter()
        maxd_any = Counter()
        maxd_one = Counter()
        minchain = Counter()
        corners = Counter()
        dist_hist = Counter()
        examples = defaultdict(list)
        for o in d['orbits']:
            S['orbits'] += 1
            prim_ok = o['primitive'] and o['k'] >= 1 and all(len(c) < n for c in o['cts'][1:])
            if o['contains_An']:
                S['An orbits'] += 1
                if o['M_order'] == _fact(o['q']):
                    S['An orbits, M = S_q'] += 1
                elif o['M_pair_orbits'] == 1:
                    S['An orbits, M 2-homogeneous but not S_q'] += 1
                else:
                    S['An orbits, M not 2-homogeneous'] += 1
                    examples['An M not 2-homog'].append((o['cts'], o['rep'], o['M_order'], o['q'], o['M_pair_orbits']))
            if not o['M_sizes_constant']:
                S['M size not constant (bug)'] += 1
            # relations per corner
            ids = sorted({p['P'] for p in o['pairs']} | {p['Q'] for p in o['pairs']})
            for xi in range(3):
                rel = {(p['P'], p['Q']) for p in o['pairs'] if p['lit_x'][xi]}
                one = {(p['P'], p['Q']) for p in o['pairs'] if p['lit_x'][xi] and p['minchain_x'][xi] == 1}
                S['corner relations'] += 1
                if _transitive(rel, ids):
                    S['x-lit transitive'] += 1
                else:
                    examples['x-lit not transitive'].append((o['cts'], o['rep'], xi + 1))
                if _closure(one, ids) == _closure(rel, ids):
                    S['closure(one-mirror x) = closure(x-lit)'] += 1
                if one == rel:
                    S['one-mirror x = x-lit'] += 1
            relall = {(p['P'], p['Q']) for p in o['pairs'] if p['lit']}
            if _transitive(relall, ids):
                S['LIT transitive on orbit'] += 1
            else:
                examples['LIT not transitive'].append((o['cts'], o['rep']))
            for p in o['pairs']:
                S['pairs'] += 1
                for xi in range(3):
                    S['pair-corners'] += 1
                    xl, cert, same = p['lit_x'][xi], p['cert_x'][xi], p['same_fibre_x'][xi]
                    S['pc x-lit=%d cert=%d' % (xl, bool(cert))] += 1
                    if xl and cert:
                        examples['x-lit with cert'].append((o['cts'], o['rep'], p['P'], p['Q'], xi + 1, cert))
                    if not xl and not cert:
                        examples['not x-lit, no cert over B'].append((o['cts'], o['rep'], p['P'], p['Q'], xi + 1, p['lit']))
                        S['pc not x-lit, no cert over B; pair lit=%d' % p['lit']] += 1
                    if xl and not same:
                        S['x-lit but different B_x fibre (contradiction)'] += 1
                    if same:
                        S['pc same B_x fibre, x-lit=%d' % xl] += 1
                    if xl:
                        S['pc x-lit'] += 1
                        if p['minchain_x'][xi] == 1:
                            S['pc x-lit with a one-mirror witness'] += 1
                        if p['cyl_x'][xi]:
                            S['pc x-lit with a cylinder witness in class x'] += 1
                    elif p['cyl_x'][xi]:
                        S['cyl in class x but not x-lit'] += 1
                if not p['lit']:
                    S['DARK'] += 1
                    if any(p['cyl_x']):
                        S['DARK with cylinder witness (bug)'] += 1
                    continue
                S['LIT'] += 1
                if prim_ok:
                    S['LIT, PRIM hypotheses'] += 1
                corners[tuple(p['lit_x'])] += 1
                mc = min(c for c, l in zip(p['minchain_x'], p['lit_x']) if l)
                minchain[mc] += 1
                if mc > 1:
                    examples['LIT, no one-mirror witness'].append((o['cts'], o['rep'], p['P'], p['Q'], mc))
                cy = ''.join(sorted(set(''.join(p['cyl_x']))))
                S['LIT cyl=' + (cy or 'none')] += 1
                if not cy:
                    examples['LIT, no cylinder witness'].append((o['cts'], o['rep'], p['P'], p['Q'], o['k']))
                h = {int(a): b for a, b in p['dist_any'].items()}
                m = max(h)
                maxd_any[m] += 1
                for a, b in h.items():
                    dist_hist[a] += b
                if m >= 6:
                    examples['max dist >= 6'].append((o['cts'], o['rep'], p['P'], p['Q'], m, o['marked'], o['max_depth']))
                if p['dist_one']:
                    maxd_one[max(int(a) for a in p['dist_one'])] += 1
            if prim_ok:
                S['orbits with PRIM hypotheses'] += 1
                if all(p['lit'] for p in o['pairs']):
                    S['PRIM orbits all lit'] += 1
        print('=' * 20, 'n =', n, '(skipped orbits: %s)' % d.get('skipped_orbits'))
        for k in sorted(S):
            print('  %-60s %d' % (k, S[k]))
        print('  LIT pairs by lit corners (b,c,d):', dict(sorted(corners.items())))
        print('  LIT pairs by minimal chain length:', dict(sorted(minchain.items())))
        print('  LIT pairs by max distance to a witness state:', dict(sorted(maxd_any.items())))
        print('  LIT pairs by max distance to a one-mirror witness:', dict(sorted(maxd_one.items())))
        print('  states by distance to a witness (summed over lit pairs):', dict(sorted(dist_hist.items())))
        for k, v in examples.items():
            print('  examples', k, len(v))
            for e in v[:3]:
                print('     ', json.dumps(e))
        summ[n] = dict(counts=dict(S), lit_corners={str(k): v for k, v in corners.items()},
                       minchain=dict(minchain), max_dist_any=dict(maxd_any), max_dist_one=dict(maxd_one),
                       dist_hist=dict(dist_hist),
                       examples={k: v[:10] for k, v in examples.items()},
                       example_counts={k: len(v) for k, v in examples.items()})
    (HERE / 'summary.json').write_text(json.dumps(summ, indent=1) + '\n')


def _fact(q):
    r = 1
    for i in range(2, q + 1):
        r *= i
    return r


def _closure(rel, ids):
    par = {i: i for i in ids}

    def find(u):
        while par[u] != u:
            u = par[u]
        return u

    for a, b in rel:
        par[find(a)] = find(b)
    return frozenset(frozenset(j for j in ids if find(j) == find(i)) for i in ids)


def _transitive(rel, ids):
    cl = _closure(rel, ids)
    full = {(a, b) for c in cl for a in c for b in c if a < b}
    return full == set(rel)


if __name__ == '__main__':
    main()
