"""Census of genus-0 pillowcase covers (cycle lengths <= 3) at degree n, with the exact
all-arc light decider and the parity-factor conjecture test.

For each Nielsen class (ordered cycle types of g_a, g_b, g_c, g_d with index sum 2n-2):
  1. enumerate every transitive tuple up to simultaneous conjugation (enumerate_tuples);
  2. split the class into pure-braid orbits (generators s0^2, s1^2 and inverses).  For a
     tuple whose g_a has >= 2 two-cycles the orbit is run with every point over 'a'
     labelled (marked_orbit), which also decides LIT/DARK for every pair of 2-cycle
     points; otherwise the unmarked orbit is run.  Every tuple visited must be in the
     enumerated class (asserted), and the orbits must cover the class exactly.
  3. per orbit (one cover Q -> B up to pure mapping classes; all tuples in the orbit are
     the same cover in other bases, so all invariants below are constant on it):
     G (order, primitive, contains A_n), k, all block systems with induced tuples,
     parity property, separation of each pair, deck group, LIT/DARK per pair, and the
     conjecture verdict.  Per-tuple counts are orbit counts weighted by the number of
     tuples in the orbit.

Conjecture tested, per pair (sigma, tau) of distinct 2-cycles of g_a:
  DARK  <=>  some block system other than the one-block system (the singleton system,
             N = Q, included) has induced g_b, g_c, g_d without 2-cycles and puts sigma
             and tau over distinct points of N over 'a'.

Run: python3 -B census.py N [workers]   -> writes census_nN.json (+ census_nN.log)
"""
import json
import sys
import time
from collections import Counter, defaultdict
from math import factorial
from multiprocessing import Pool
from pathlib import Path

import d4_monodromy as d4
from hurwitz import (cycles, cycle_type, marked_orbit, plain_orbit, canon_plain, initial_pt,
                     mul, inv, PURE_GENS)
from enumerate_tuples import ClassEnumerator, genus0_classes

HERE = Path(__file__).resolve().parent
_E = None
DETAIL_LIMIT = 10 ** 9


def deck_group(t, n):
    """All permutations commuting with every generator (t transitive)."""
    out = []
    for y in range(n):
        phi = [-1] * n
        phi[0] = y
        q = [0]
        ok = True
        for x in q:
            for g in t:
                a, b = g[x], g[phi[x]]
                if phi[a] >= 0:
                    if phi[a] != b:
                        ok = False
                        break
                else:
                    phi[a] = b
                    q.append(a)
            if not ok:
                break
        if ok and len(set(phi)) == n:
            out.append(tuple(phi))
    return out


def g1_dark(t, n, systems, sheet_of, P, Q):
    """Generalised parity test G1.  Returns a witness (sizes of Pi and Pi') or None.

    Pi  : a block system whose induced tuple is a pillowcase cover P' -> B (all induced
          cycle lengths <= 2 and exactly 4 induced fixed points in total).  The one-block
          system gives P' = B.  Corners of P' are the pairs (corner y, Pi-block fixed by
          the induced g_y); Q -> P' is branched only over these corners.
    Need: both marks lie over one P'-corner c0 = (a, beta).
    Pi' : a block system refining Pi (N = Q / Pi' covers P').  Parity relative to P': no
          point of N over a P'-corner other than c0 is a 2-cycle (regular point).
    Sep : P and Q map to distinct points of N.
    Then the arc model over the pillowcase P' and the invariance argument give DARK.
    """
    def where_of(part):
        return {x: b for b, blk in enumerate(part) for x in blk}

    for big in systems:
        ig = [d4.induced(g, big) for g in t]
        if any(len(c) > 2 for g in ig for c in cycles(g)):
            continue
        if sum(1 for g in ig for c in cycles(g) if len(c) == 1) != 4:
            continue
        wb = where_of(big)
        beta = wb[sheet_of[P][0]]
        if ig[0][beta] != beta or wb[sheet_of[Q][0]] != beta:
            continue
        for small in systems:
            ws = where_of(small)
            if len(small) < len(big) or any(wb[x] != wb[small[ws[x]][0]] for x in range(n)):
                continue                                # small must refine big
            if len(small) == len(big):
                continue                                # N = P' cannot separate marks over c0
            ok = True
            for y, g in enumerate(t):
                for cy in cycles(d4.induced(g, small)):
                    if len(cy) != 2:
                        continue
                    b0 = wb[small[cy[0]][0]]            # P'-point under this N-point
                    if ig[y][b0] == b0 and not (y == 0 and b0 == beta):
                        ok = False                      # regular N-point over a P'-corner != c0
                        break
                if not ok:
                    break
            if not ok:
                continue
            ga = d4.induced(t[0], small)
            cyc = {b: k for k, cy in enumerate(cycles(ga)) for b in cy}
            if cyc[ws[sheet_of[P][0]]] != cyc[ws[sheet_of[Q][0]]]:
                return [n // len(big), n // len(small)]
    return None


def g5_dark(t, n, systems, sheet_of, P, Q):
    """Per-corner test G5.  Every light path from P to Q runs along a simple arc a -> x for
    one corner x in {b, c, d} (the corner of an arc is braid invariant), so it suffices to
    block each x separately.  Corner x is blocked by a block system Pi (not one-block;
    N = Q / Pi) if either
      parity : P, Q map to distinct points of N and N has no 2-cycle over x; or
      cut    : P, Q map to the same point of N, every 2-cycle of Q over a and over x
               maps to a 2-cycle of N (so a light walk in Q projects to a walk in N that
               avoids every branch point of Q -> N), and N's monodromy at one of the two
               remaining corners y, z is a single cycle.  Then the preimage T in N of the
               arc y -> z disjoint from the light arc is connected and holds every branch
               point over y, z.  A branch point over a or x is a pole of N under a 3-cycle
               of Q, i.e. a leaf of the light graph where walks stop; a path through the
               adjacent cylinder of N minus both graphs joins it to T.  Their union K is
               connected, holds every branch point and misses every closed light walk, and
               each component of N - K is simply connected.  So each closed walk in N lifts
               to a closed walk in Q, and Q (same image as P) is never reached.
    Returns {x: (route, block size)} if every corner is blocked, else None."""
    out = {}
    for x in (1, 2, 3):
        y, z = [w for w in (1, 2, 3) if w != x]
        for part in systems:
            m = len(part)
            if m == 1:
                continue
            ig = [d4.induced(g, part) for g in t]
            where = {s: b for b, blk in enumerate(part) for s in blk}
            cyc_a = {b: k for k, cy in enumerate(cycles(ig[0])) for b in cy}
            same = cyc_a[where[sheet_of[P][0]]] == cyc_a[where[sheet_of[Q][0]]]
            if not same:
                if all(len(c) != 2 for c in cycles(ig[x])):
                    out[x] = ('parity', n // m)
                    break
                continue
            unram = True
            for g, h in ((t[0], ig[0]), (t[x], ig[x])):
                hl = {b: len(cy) for cy in cycles(h) for b in cy}
                if any(len(c) == 2 and hl[where[c[0]]] != 2 for c in cycles(g)):
                    unram = False
                    break
            if unram and (len(cycles(ig[y])) == 1 or len(cycles(ig[z])) == 1):
                out[x] = ('cut', n // m)
                break
        if x not in out:
            return None
    return {'bcd'[x - 1]: v for x, v in out.items()}


def analyse_orbit(t, n, lit, plen, pt0):
    """Invariants of one cover and the per-pair verdicts.  pt0 = point IDs of t's 'a'-cycles."""
    gens = list(t)
    systems = d4.all_block_systems(gens, n)
    primitive = len(systems) == 2
    order = d4.schreier_sims(gens, n)[2]
    k = sum(1 for g in t[1:] for c in cycles(g) if len(c) == 2)
    two = sorted(P for P in range(len(plen)) if plen[P] == 2)
    sheet_of = {}
    for x in range(n):
        sheet_of.setdefault(pt0[x], []).append(x)
    bsys = []
    for part in systems:
        m = len(part)
        if m == 1:
            continue                       # one-block system excluded
        ig = [d4.induced(g, part) for g in t]
        where = {x: b for b, blk in enumerate(part) for x in blk}
        cid_a = {}
        for ci, cy in enumerate(cycles(ig[0])):
            for b in cy:
                cid_a[b] = ci
        image = {P: cid_a[where[sheet_of[P][0]]] for P in range(len(plen))}
        parity = all(len(c) != 2 for g in ig[1:] for c in cycles(g))
        bsys.append(dict(block_size=n // m, blocks=m,
                         induced_cycle_types=[cycle_type(g) for g in ig],
                         induced_tuple=[list(g) for g in ig] if 1 < m < n else None,
                         parity=parity, a_point_image=image))
    deck = deck_group(t, n)
    pairs = []
    for i in range(len(two)):
        for j in range(i + 1, len(two)):
            P, Q = two[i], two[j]
            is_lit = frozenset((P, Q)) in lit
            seps = [b['block_size'] for b in bsys if b['parity'] and b['a_point_image'][P] != b['a_point_image'][Q]]
            swapped = any(sorted({pt0[d[x]] for x in sheet_of[P]}) == [Q] and
                          sorted({pt0[d[x]] for x in sheet_of[Q]}) == [P] for d in deck)
            moved = any(sorted({pt0[d[x]] for x in sheet_of[P]}) == [Q] for d in deck)
            g1 = g1_dark(t, n, systems, sheet_of, P, Q)
            g5 = g5_dark(t, n, systems, sheet_of, P, Q)
            pairs.append(dict(P=P, Q=Q, sheets_P=sheet_of[P], sheets_Q=sheet_of[Q], lit=is_lit,
                              parity_separating_block_sizes=seps, predicted_dark=bool(seps),
                              g1_witness_block_sizes=g1, g1_predicted_dark=g1 is not None,
                              g5_witness=g5, g5_predicted_dark=g5 is not None,
                              deck_maps_P_to_Q=moved, deck_swaps_P_Q=swapped))
    return dict(order=order, is_sym=order == factorial(n), contains_An=order * 2 >= factorial(n),
                primitive=primitive, k=k, n_block_systems_excl_one_block=len(bsys),
                block_systems=[{kk: v for kk, v in b.items()} for b in bsys],
                deck_order=len(deck), pairs=pairs)


def work(cts):
    global _E
    n = sum(cts[0])
    if _E is None or _E.n != n:
        _E = ClassEnumerator(n)
    t0 = time.time()
    found = _E.enumerate_class(cts)
    covered = {}
    orbits = []
    for key, t in found.items():
        if key in covered:
            continue
        oid = len(orbits)
        pt0, plen = initial_pt(t[0])
        n2 = sum(1 for L in plen if L == 2)
        if n2 >= 2:
            res = marked_orbit(t, want_witness=True)
            members = set()
            for enc in res['seen']:
                from hurwitz import decode
                tt, _ = decode(enc, n, True)
                members.add(canon_plain(tt))
            marked_states = res['states']
            lit = res['lit']
            witness = res['witness']
        else:
            members = plain_orbit(t)
            marked_states = None
            lit, witness = set(), {}
        for c in members:
            assert c in found, 'orbit left the enumerated Nielsen class'
            assert c not in covered
            covered[c] = oid
        rec = dict(rep=[list(g) for g in t], plain_orbit_size=len(members), marked_orbit_size=marked_states,
                   n_two_cycles_a=n2)
        if n2 >= 2:
            rec.update(analyse_orbit(t, n, lit, plen, pt0))
            for p in rec['pairs']:
                if p['lit']:
                    w = witness[frozenset((p['P'], p['Q']))]
                    p['witness'] = dict(word=[list(x) for x in w[0]], arc_to=w[1])
        orbits.append(rec)
    assert len(covered) == len(found)
    return dict(cts=[list(x) for x in cts], n_tuples=len(found), orbits=orbits, seconds=round(time.time() - t0, 2))


def main():
    n = int(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    classes = genus0_classes(n)
    t0 = time.time()
    logf = (HERE / ('census_n%d.log' % n)).open('w')

    def log(*a):
        s = ' '.join(str(x) for x in a)
        print(s, flush=True)
        logf.write(s + '\n')
        logf.flush()

    log('n', n, 'Nielsen classes (index sum 2n-2, before transitivity):', len(classes), 'workers', workers)
    results = []
    if workers > 1:
        with Pool(workers) as pool:
            for r in pool.imap_unordered(work, classes, chunksize=1):
                results.append(r)
                if len(results) % 200 == 0:
                    log('  classes done', len(results), '%.0fs' % (time.time() - t0))
    else:
        for c in classes:
            results.append(work(c))
    results.sort(key=lambda r: r['cts'])
    summary = summarise(n, results)
    summary['seconds'] = round(time.time() - t0, 1)
    log(json.dumps({k: v for k, v in summary.items() if k not in ('counterexamples', 'nielsen')}, indent=1))
    log('counterexamples (dark, no parity factor):', len(summary['counterexamples']['dark_without_parity_factor']))
    log('counterexamples (lit, with parity factor):', len(summary['counterexamples']['lit_with_parity_factor']))
    out = dict(n=n, summary=summary, classes=[r for r in results if r['n_tuples']] )
    (HERE / ('census_n%d.json' % n)).write_text(json.dumps(out, default=str) + '\n')
    logf.close()


def summarise(n, results):
    S = Counter()
    nielsen = []
    cex_dark, cex_lit = [], []
    for r in results:
        if not r['n_tuples']:
            continue
        S['nielsen_classes_nonempty'] += 1
        S['tuples'] += r['n_tuples']
        S['braid_orbits'] += len(r['orbits'])
        nielsen.append(dict(cts=r['cts'], tuples=r['n_tuples'], orbits=len(r['orbits']),
                            orbit_sizes=sorted((o['plain_orbit_size'] for o in r['orbits']), reverse=True)))
        if len(r['orbits']) == 1:
            S['nielsen_classes_single_orbit'] += 1
        else:
            S['nielsen_classes_split'] += 1
        for o in r['orbits']:
            w = o['plain_orbit_size']
            if o['n_two_cycles_a'] < 2:
                S['tuples_without_pair'] += w
                continue
            S['orbits_with_pairs'] += 1
            S['tuples_with_pairs'] += w
            if o['marked_orbit_size'] != o['plain_orbit_size']:
                S['orbits_marked_size_ne_plain'] += 1
            for p in o['pairs']:
                S['pairs_per_orbit'] += 1
                S['pairs_per_tuple'] += w
                tag = ('LIT' if p['lit'] else 'DARK') + '/' + ('pred_DARK' if p['predicted_dark'] else 'pred_LIT')
                S['orbit_pairs ' + tag] += 1
                S['tuple_pairs ' + tag] += w
                kk = 'k=0' if o['k'] == 0 else 'k>=1'
                deg = degenerate(o)
                S['orbit_pairs %s %s' % ('degenerate' if deg else 'nondegenerate', tag)] += 1
                S['tuple_pairs %s %s' % ('degenerate' if deg else 'nondegenerate', tag)] += w
                S['orbit_pairs %s %s %s' % (kk, 'prim' if o['primitive'] else 'imprim', 'LIT' if p['lit'] else 'DARK')] += 1
                g1tag = ('LIT' if p['lit'] else 'DARK') + '/' + ('G1_DARK' if p['g1_predicted_dark'] else 'G1_LIT')
                S['orbit_pairs ' + g1tag] += 1
                S['tuple_pairs ' + g1tag] += w
                S['orbit_pairs %s %s' % ('degenerate' if deg else 'nondegenerate', g1tag)] += 1
                expl = p['g1_predicted_dark'] or p['g5_predicted_dark']
                g15 = ('LIT' if p['lit'] else 'DARK') + '/' + ('G1orG5_DARK' if expl else 'G1orG5_LIT')
                S['orbit_pairs ' + g15] += 1
                S['tuple_pairs ' + g15] += w
                S['orbit_pairs %s %s' % ('degenerate' if deg else 'nondegenerate', g15)] += 1
                if p['g1_predicted_dark'] and not p['predicted_dark']:
                    S['orbit_pairs dark_explained_only_by_proper_pillowcase_quotient'] += 1
                if not p['lit'] and not p['predicted_dark']:
                    cex_dark.append(cex_record(o, p, r['cts']))
                if p['lit'] and p['predicted_dark']:
                    cex_lit.append(cex_record(o, p, r['cts']))
    return dict(n=n, **dict(sorted(S.items())), counterexamples=dict(dark_without_parity_factor=cex_dark,
                                                                      lit_with_parity_factor=cex_lit),
                nielsen=nielsen)


def degenerate(o):
    """Some corner other than 'a' is not a branch value (its monodromy is the identity)."""
    return any(all(g[i] == i for i in range(len(g))) for g in o['rep'][1:])


def cex_record(o, p, cts):
    return dict(cts=cts, degenerate=degenerate(o), rep=o['rep'], P_sheets=p['sheets_P'], Q_sheets=p['sheets_Q'], lit=p['lit'],
                k=o['k'], order=o['order'], primitive=o['primitive'], contains_An=o['contains_An'],
                g1_witness_block_sizes=p['g1_witness_block_sizes'], g5_witness=p['g5_witness'],
                deck_order=o['deck_order'], deck_maps_P_to_Q=p['deck_maps_P_to_Q'], deck_swaps=p['deck_swaps_P_Q'],
                plain_orbit_size=o['plain_orbit_size'], marked_orbit_size=o['marked_orbit_size'],
                block_systems=[{kk: v for kk, v in b.items() if kk != 'a_point_image'} |
                               dict(separates=b['a_point_image'][p['P']] != b['a_point_image'][p['Q']])
                               for b in o['block_systems']],
                all_pairs_of_cover=[(q['P'], q['Q'], q['lit'], q['predicted_dark']) for q in o['pairs']])


if __name__ == '__main__':
    main()
