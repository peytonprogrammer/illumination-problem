"""Aggregate census_nN.json files into summary.json and print the tables used in README.md.

Run: python3 -B summarize.py
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import d4_monodromy as d4
from rigid_factor import g6_dark

HERE = Path(__file__).resolve().parent


def mechanism(x):
    t = tuple(tuple(g) for g in x['rep'])
    n = len(t[0])
    g6 = g6_dark(t, n, d4.all_block_systems(list(t), n), x['P_sheets'][0], x['Q_sheets'][0])
    if x['g1_witness_block_sizes']:
        return 'G1 (parity over a proper pillowcase quotient P\', block sizes %s)' % x['g1_witness_block_sizes']
    if x['g5_witness']:
        routes = sorted({v[0] for v in x['g5_witness'].values()})
        return 'G5 per-corner (%s)' % '+'.join(routes)
    if g6 and g6[0] == 1:
        return 'G6 rigid, N = Q (Q degenerate: g_%s = 1)' % g6[1]
    if g6:
        return 'G6 rigid factor (block size %d, induced g_%s = 1)' % tuple(g6)
    return 'not G1, G5 or G6 (see README: G7, rigid over a pillowcase quotient)'


def bcd_key(cts):
    """Nielsen class up to permuting the corners b, c, d."""
    return (tuple(cts[0]),) + tuple(sorted(tuple(c) for c in cts[1:]))


def main():
    out = {'per_n': {}, 'counterexample_families': {}, 'nielsen_split': {}}
    for f in sorted(HERE.glob('census_n*.json'), key=lambda p: int(p.stem[8:])):
        d = json.loads(f.read_text())
        n = d['n']
        s = d['summary']
        row = {k: v for k, v in s.items() if k not in ('counterexamples', 'nielsen')}
        cex = s['counterexamples']['dark_without_parity_factor']
        row['orig_conjecture_cex_orbit_pairs'] = len(cex)
        row['orig_conjecture_cex_tuple_pairs'] = sum(x['plain_orbit_size'] for x in cex)
        row['lit_with_parity_factor'] = len(s['counterexamples']['lit_with_parity_factor'])
        mech = Counter(mechanism(x).split(' (')[0] for x in cex)
        row['cex_by_mechanism'] = dict(mech)
        # k = 0 always dark?  primitive and k >= 1 always lit?
        k0_lit = 0
        prim_k_dark = Counter()
        nonsplit_k_dark = 0
        fam = defaultdict(list)
        for cl in d['classes']:
            for o in cl['orbits']:
                if o['n_two_cycles_a'] < 2:
                    continue
                for p in o['pairs']:
                    if o['k'] == 0 and p['lit']:
                        k0_lit += 1
                    if o['k'] >= 1 and o['primitive'] and not p['lit']:
                        deg = any(all(g[i] == i for i in range(n)) for g in o['rep'][1:])
                        prim_k_dark['degenerate' if deg else 'nondegenerate'] += 1
        row['k0_pairs_lit'] = k0_lit
        row['primitive_k_ge_1_dark_pairs'] = dict(prim_k_dark)
        for x in cex:
            key = (n, bcd_key(x['cts']), mechanism(x))
            fam[key].append(x)
        for (nn, ck, m), xs in sorted(fam.items(), key=lambda kv: str(kv[0])):
            r = xs[0]
            out['counterexample_families'].setdefault(str(n), []).append(dict(
                nielsen_class_up_to_bcd=[list(c) for c in ck], mechanism=m, orbit_pairs=len(xs),
                corner_orders=sorted({json.dumps(x['cts']) for x in xs}),
                representative=dict(cts=r['cts'], rep=r['rep'], P_sheets=r['P_sheets'], Q_sheets=r['Q_sheets'],
                                    k=r['k'], G_order=r['order'], primitive=r['primitive'],
                                    contains_An=r['contains_An'], deck_order=r['deck_order'],
                                    deck_maps_P_to_Q=r['deck_maps_P_to_Q'], plain_orbit_size=r['plain_orbit_size'],
                                    marked_orbit_size=r['marked_orbit_size'],
                                    block_systems=[dict(block_size=b['block_size'], induced=b['induced_cycle_types'],
                                                        parity=b['parity'], separates=b['separates'])
                                                   for b in r['block_systems']],
                                    g1=r['g1_witness_block_sizes'], g5=r['g5_witness'])))
        # Nielsen classes: split versus single orbit; do split orbits differ in |G| or primitivity?
        split = []
        for cl in d['classes']:
            if len(cl['orbits']) > 1:
                orders = sorted({o.get('order') for o in cl['orbits'] if 'order' in o})
                prims = sorted({o.get('primitive') for o in cl['orbits'] if 'primitive' in o})
                dark_counts = sorted({sum(1 for p in o.get('pairs', []) if not p['lit']) for o in cl['orbits']})
                split.append(dict(cts=cl['cts'], tuples=cl['n_tuples'],
                                  orbit_sizes=sorted((o['plain_orbit_size'] for o in cl['orbits']), reverse=True),
                                  G_orders=orders, primitive_values=prims, dark_pairs_per_orbit=dark_counts,
                                  has_pairs=cl['orbits'][0]['n_two_cycles_a'] >= 2))
        with_pairs = [x for x in split if x['has_pairs']]
        row['split_classes_with_pairs'] = len(with_pairs)
        row['split_classes_with_pairs_orbits_differ_in_G_order'] = sum(1 for x in with_pairs if len(x['G_orders']) > 1)
        row['split_classes_with_pairs_orbits_differ_in_primitivity'] = sum(
            1 for x in with_pairs if len(x['primitive_values']) > 1)
        row['split_classes_with_pairs_orbits_differ_in_dark_count'] = sum(
            1 for x in with_pairs if len(x['dark_pairs_per_orbit']) > 1)
        row['split_classes_with_pairs_same_G_order_but_differ_in_dark_count'] = sum(
            1 for x in with_pairs if len(x['dark_pairs_per_orbit']) > 1 and len(x['G_orders']) == 1)
        out['nielsen_split'][str(n)] = split
        out['per_n'][str(n)] = row
    (HERE / 'summary.json').write_text(json.dumps(out, indent=1) + '\n')
    keys = ['tuples', 'nielsen_classes_nonempty', 'nielsen_classes_split', 'braid_orbits', 'tuples_with_pairs',
            'orbits_with_pairs', 'pairs_per_tuple', 'pairs_per_orbit', 'tuple_pairs LIT/pred_LIT',
            'tuple_pairs DARK/pred_DARK', 'tuple_pairs DARK/pred_LIT', 'orbit_pairs DARK/pred_LIT',
            'orbit_pairs nondegenerate DARK/pred_LIT', 'orbit_pairs nondegenerate DARK/G1orG5_LIT',
            'orbit_pairs degenerate DARK/G1orG5_LIT', 'lit_with_parity_factor', 'k0_pairs_lit',
            'split_classes_with_pairs', 'split_classes_with_pairs_orbits_differ_in_G_order',
            'split_classes_with_pairs_orbits_differ_in_primitivity', 'split_classes_with_pairs_orbits_differ_in_dark_count',
            'split_classes_with_pairs_same_G_order_but_differ_in_dark_count', 'orbits_marked_size_ne_plain', 'seconds']
    for k in keys:
        print('%-55s' % k, ' '.join('%10s' % out['per_n'][n].get(k, 0) for n in out['per_n']))
    for n, row in out['per_n'].items():
        print(n, 'primitive k>=1 dark pairs', row['primitive_k_ge_1_dark_pairs'], 'cex by mechanism', row['cex_by_mechanism'])
    for n, fams in out['counterexample_families'].items():
        for f in fams:
            print(n, f['nielsen_class_up_to_bcd'], f['orbit_pairs'], f['mechanism'])


if __name__ == '__main__':
    main()
