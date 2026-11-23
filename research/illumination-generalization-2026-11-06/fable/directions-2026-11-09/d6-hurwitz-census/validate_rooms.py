"""Validate the Hurwitz-orbit light decider on real rooms from the d4 record.

Square (pillow) framework, orthogonal rooms.  d4 gives g_c = (cross V-edge, then H-edge)
at each pillow corner A=(0,0), C1=(1,0), B=(1,1), C2=(0,1).  Around the top face these
loops are ccw at A and B and cw at C1 and C2, and the top-face corners occur in the ccw
order A, C1, B, C2.  So the geometric basis with tails from the top-face centre is
    (t0, t1, t2, t3) = (g_A, g_C1^-1, g_B, g_C2^-1),  t0 t1 t2 t3 = 1 (checked).

Triangle framework, 45-degree rooms.  d4's tri base is the double of the triangle
A(0,0), C(1,0), B(1,1) with angles pi/2, pi, pi/2.  Its ccw loops are x_A = g_A,
x_C = g_C^-1, x_B = g_B^-1 with x_A x_C x_B = 1 (checked).  The pillowcase is the double
cover branched at A and B (homomorphism x_A, x_B -> 1, x_C -> 0).  Rewriting
u v w = 1 (u=x_A, v=x_C, w=x_B) as u^2 . v . (w v w^-1) . w^2 = 1 gives the pulled-back
pillow tuple (u^2, v, w v w^-1, w^2), corners A', C', C'', B'.  A regular point of DP over
A (4-cycle of g_A) splits into two regular points (2-cycles of g_A^2) of the pull-back Q',
and Q' -> DP is unbranched over regular points, so light in DP and in Q' agree.
The basis is checked against the square framework on orthogonal rooms (where Q' splits
into two copies of the square cover).

Run: python3 -B validate_rooms.py   -> writes validate_rooms.json
"""
import ast
import json
import sys
import time
from collections import Counter
from pathlib import Path

import d4_monodromy as d4
from hurwitz import (mul, inv, ident, cycles, cycle_type, marked_orbit, initial_pt, is_transitive, move,
                     canon_plain, PURE_GENS_WITH_S2, plain_orbit)

HERE = Path(__file__).resolve().parent
D4 = HERE.parent / 'd4-monodromy-blocks'
INP = D4 / 'inputs'
CTX = HERE.parents[3]
assert CTX.name == '.context'


def square_tuple(room):
    g = room.gen
    t = (g[(0, 0)], inv(g[(1, 0)]), g[(1, 1)], inv(g[(0, 1)]))
    assert mul(mul(mul(t[0], t[1]), t[2]), t[3]) == ident(room.degree)
    return t


def tri_tuple(room):
    g = room.gen
    u, v, w = g['A'], inv(g['C']), inv(g['B'])
    assert mul(mul(u, v), w) == ident(room.degree)
    t = (mul(u, u), v, mul(mul(w, v), inv(w)), mul(w, w))
    assert mul(mul(mul(t[0], t[1]), t[2]), t[3]) == ident(room.degree)
    return t


def restrict(t, sheets):
    idx = {s: i for i, s in enumerate(sheets)}
    return tuple(tuple(idx[g[s]] for s in sheets) for g in t), idx


def component(t, x):
    seen = {x}
    q = [x]
    for y in q:
        for g in t:
            z = g[y]
            if z not in seen:
                seen.add(z)
                q.append(z)
    return sorted(seen)


def decide_room(room, t, max_states=None):
    """Return verdict for the room's marks S, T (all lift choices)."""
    S, T = room.marks[0], room.marks[1]
    _, s_cyc = room.points_at(S)
    _, t_cyc = room.points_at(T)
    s_sheets = [x for cy in s_cyc for x in cy]
    t_sheets = [x for cy in t_cyc for x in cy]
    n = room.degree
    out = dict(name=room.name, framework=room.fw, degree_DP=n)
    if not is_transitive(t, n):
        comps = []
        done = set()
        for x in range(n):
            if x not in done:
                c = component(t, x)
                done |= set(c)
                comps.append(c)
        out['pullback_components'] = [len(c) for c in comps]
    else:
        comps = [list(range(n))]
    lit_pairs = []
    sizes = []
    for comp in comps:
        if not any(s in comp for s in s_sheets):
            continue
        tc, idx = restrict(t, comp)
        pt, plen = initial_pt(tc[0])
        Sid = sorted({pt[idx[s]] for s in s_sheets if s in idx})
        Tid = sorted({pt[idx[s]] for s in t_sheets if s in idx})
        assert all(plen[i] == 2 for i in Sid + Tid), 'marks must be regular points'
        t0 = time.time()
        k = sum(1 for g in tc[1:] for c in cycles(g) if len(c) == 2)
        targets = {frozenset((p, q)) for p in Sid for q in Tid}
        res = marked_orbit(tc, max_states=max_states, want_witness=True, targets=targets)
        sizes.append(dict(component_degree=len(comp), orbit_states=res['states'], complete=res['complete'],
                          stopped_at_first_lit_ST=res.get('stopped_lit', False), k_transparent=k,
                          seconds=round(time.time() - t0, 1),
                          cycle_types=[cycle_type(g) for g in tc],
                          S_point_ids=Sid, T_point_ids=Tid))
        for p in Sid:
            for q in Tid:
                pr = frozenset((p, q))
                if pr in res['lit']:
                    lit_pairs.append(dict(S=p, T=q, witness_word=res['witness'][pr][0],
                                          witness_arc_to=res['witness'][pr][1]))
        if not res['complete'] and not res.get('stopped_lit'):
            # exhaustion cap reached.  With k = 0 no basis has a 2-cycle over b, c, d (cycle
            # types are braid invariant), so no arc transmits light: DARK is exact anyway.
            out['incomplete'] = k > 0
            out['dark_by_k0'] = k == 0
    out['components'] = sizes
    out['lit_ST_pairs'] = lit_pairs[:4]
    out['n_lit_ST_pairs'] = len(lit_pairs)
    out['verdict'] = 'LIT' if lit_pairs else ('DARK' if not out.get('incomplete') else 'UNDECIDED')
    out['verdict_basis'] = ('witness' if lit_pairs else 'k=0 (no transparent vertex in any basis)'
                            if out.get('dark_by_k0') else 'full orbit exhausted')
    return out


def build_constants():
    tree = ast.parse((INP / 'peyton-worksheet-build.py.txt').read_text())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('TOKARSKY26', 'CASTRO24', 'PUBLISHED_ST', 'ROOM22'):
                out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


def main():
    which = sys.argv[1:] or ['room22', 'room22_tri', 'orourke34', 'k7', 'tri_lit', 'castro', 'tokarsky']
    results = {}
    k = build_constants()

    def rep(r):
        print(r['name'], r['framework'], 'deg', r['degree_DP'], r['verdict'],
              [(c['component_degree'], c['orbit_states'], c['seconds']) for c in r['components']],
              r.get('pullback_components', ''), flush=True)

    if 'room22' in which:
        sq = d4.squares_from_polygon(k['ROOM22'])
        room = d4.Room('room22', 'square', sq, [(0, 0), (2, 2)])
        assert room.ledger()['walls'] == 22
        t = square_tuple(room)
        r = decide_room(room, t)
        rep(r)
        # pure generators s0^2, s1^2 versus adding s2^2: orbit must not grow
        pt, _ = initial_pt(t[0])
        r2 = marked_orbit(t, gens=PURE_GENS_WITH_S2)
        r['orbit_states_with_s2_squared_added'] = r2['states']
        r['plain_tuple_orbit_size'] = len(plain_orbit(t))
        r['plain_tuple_orbit_size_with_s2_squared'] = len(plain_orbit(t, PURE_GENS_WITH_S2))
        r['all_A_point_lit_pairs'] = sorted(sorted(p) for p in r2['lit'])
        r['A_point_lengths'] = r2['plen']
        print('  with s2^2:', r2['states'], 'plain orbit', r['plain_tuple_orbit_size'],
              r['plain_tuple_orbit_size_with_s2_squared'], 'all lit A-pairs', r['all_A_point_lit_pairs'])
        results['room22_square'] = r
    if 'room22_tri' in which:
        sq = d4.squares_from_polygon(k['ROOM22'])
        room = d4.Room('room22_tri', 'tri', d4.tris_of_squares(sq), [(0, 0), (2, 2)])
        t = tri_tuple(room)
        r = decide_room(room, t)
        rep(r)
        # cross-check: each pull-back component should be the square cover in some geometric
        # basis, i.e. lie in the FULL braid-group (B_4) orbit of the square tuple, with the
        # pull-back corner order (A', C', C'', B') matching (A, C1|C2, C2|C1, B).
        sroom = d4.Room('room22', 'square', sq, [(0, 0), (2, 2)])
        st = square_tuple(sroom)
        labs = ('A', 'C1', 'B', 'C2')
        seen = {(labs, canon_plain(st))}
        q = [(st, labs)]
        for tq, L in q:
            for i in range(3):
                for sg in (1, -1):
                    t2, L2, _ = move(tq, L, None, i, sg)
                    key = (L2, canon_plain(t2))
                    if key not in seen:
                        seen.add(key)
                        q.append((t2, L2))
        hits = []
        done = set()
        for x in range(room.degree):
            if x in done:
                continue
            c = component(t, x)
            done |= set(c)
            tc, _ = restrict(t, c)
            cc = canon_plain(tc)
            hits.append(sorted(L for (L, cf) in seen if cf == cc))
        r['square_B4_orbit_states'] = len(seen)
        r['pullback_component_corner_orders_found_in_square_B4_orbit'] = hits
        print('  square B4 orbit', len(seen), '; pull-back components found with corner orders:', hits)
        results['room22_tri'] = r
    if 'orourke34' in which:
        h = json.loads((INP / 'historical34-room.json').read_text())
        cells = Counter()
        for tr in h['triangles']:
            cells[(min(p[0] for p in tr), min(p[1] for p in tr))] += 1
        room = d4.Room('orourke34_square', 'square', list(cells), h['marked'])
        r = decide_room(room, square_tuple(room), max_states=200_000)
        rep(r)
        results['orourke34_square'] = r
    if 'k7' in which:
        out = []
        for f in sorted((INP / 'k7-models').glob('model-*.json')):
            d = json.loads(f.read_text())
            room = d4.Room(f.stem, 'square', [tuple(c) for c in d['cells']], d['marks'])
            r = decide_room(room, square_tuple(room))
            rep(r)
            out.append(r)
        c = json.loads((INP / 'k7-controls.json').read_text())['controls'][0]
        room = d4.Room('k7-control-W18', 'square', [tuple(x) for x in c['cells']], c['geometry']['interior_A'])
        r = decide_room(room, square_tuple(room))
        rep(r)
        out.append(r)
        results['k7_lit_controls'] = out
        print('k7 verdicts', Counter(x['verdict'] for x in out))
    if 'tri_lit' in which:
        p = CTX / 'transparent-simple-two-symmetric-screen.json'
        out = []
        for i, rec in enumerate(json.loads(p.read_text())['records']):
            if rec['walls'] <= 21 and len(out) < 8:
                room = d4.Room('screen-%d' % i, 'tri', [tuple(map(tuple, tr)) for tr in rec['room']['triangles']],
                               rec['room']['marked'])
                r = decide_room(room, tri_tuple(room))
                rep(r)
                out.append(r)
        results['tri_lit_controls_screen'] = out
        print('tri lit verdicts', Counter(x['verdict'] for x in out))
    for name, key in (('castro', 'CASTRO24'), ('tokarsky', 'TOKARSKY26')):
        if name in which:
            room = d4.Room(key.lower(), 'tri', d4.tris_from_polygon(k[key]), k['PUBLISHED_ST'])
            r = decide_room(room, tri_tuple(room), max_states=200_000)
            rep(r)
            results[key.lower()] = r
    tag = '' if len(sys.argv) == 1 else '_' + '_'.join(which)
    (HERE / ('validate_rooms%s.json' % tag)).write_text(json.dumps(results, indent=1, default=str) + '\n')


if __name__ == '__main__':
    main()
