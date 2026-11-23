"""d65: which room hypotheses do the d14 n = 10 non-transitive relations violate?

Reads saved data only (d12 mine_n10.json).  For every orbit with |G| in {1920, 3840},
one block system of block size 2, and a corner x where the saved x-lit relation is not
transitive, it:
  - recomputes the non-transitivity from the saved lit_x verdicts;
  - finds the deck involution delta (centraliser) and checks that every x-dark pair
    inside one connected x-lit class is a delta-pair;
  - walks the plain pure-braid orbit (hurwitz.plain_orbit) of the tuple and of its
    b <-> d mirror, and classifies every seam-reflection lift iota of every state:
      no_lift, RP2 (no fixed edge), cone (interior cone point), overlap (immersed,
      not injective), slit, pinch, planar.
Exact permutation arithmetic.  Run: python3 -B d14_reality.py
"""
import json
import sys
from collections import Counter
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
D12 = HERE.parent / 'd12-lit-side'
sys.path.insert(0, str(D6))
import d4_monodromy as d4                                         # noqa: E402
from hurwitz import inv, mul, cycles, plain_orbit, decode, initial_pt   # noqa: E402
from involution_flag import edge_maps, reflections, step, EDGES   # noqa: E402
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
import unified_test as U                                          # noqa: E402
from roomtools import class_congruence                            # noqa: E402

PAR = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}   # corner y of a cell: parity class


def classify(t, phi):
    """Status of the seam-reflection lift phi of tuple t (d6 model)."""
    n = len(t[0])
    E = edge_maps(t)
    fixed = {(i, e) for e in EDGES for i in range(n) if E[e][i] == phi[i]}
    if not fixed:
        return 'RP2'
    # corner points touching a fixed edge (edge -> its two corners)
    ends = {'bottom': (0, 1), 'right': (1, 2), 'top': (2, 3), 'left': (3, 0)}
    cyc = [{x: k for k, c in enumerate(cycles(t[y])) for x in c} for y in range(4)]
    lens = [[len(c) for c in cycles(t[y])] for y in range(4)]
    on_wall = set()
    for (i, e) in fixed:
        for y in ends[e]:
            on_wall.add((y, cyc[y][i]))
    for y in range(4):
        for k, L in enumerate(lens[y]):
            if L != 2 and (y, k) not in on_wall:
                return 'cone'
    pos = {0: (0, 0)}
    q = [0]
    glued = set()
    for i in q:
        for e in EDGES:
            if E[e][i] == phi[i]:
                continue
            j = phi[E[e][i]]
            c = step(pos[i], e)
            glued.add(frozenset((pos[i], c)))
            if j not in pos:
                pos[j] = c
                q.append(j)
            elif pos[j] != c:
                return 'cone_holonomy'          # should not happen after the cone test
    cells = list(pos.values())
    if len(set(cells)) != len(cells):
        return 'overlap'
    cs = set(cells)
    if any(step(c, e) in cs and frozenset((c, step(c, e))) not in glued for c in cs for e in EDGES):
        return 'slit'
    # pinch: two distinct iota-orbits of corner points at one lattice position
    where = {}
    for i, (x, y) in pos.items():
        for yy in range(4):
            px, py = PAR[yy]
            corner = next((x + dx, y + dy) for dx in (0, 1) for dy in (0, 1)
                          if (x + dx) % 2 == px and (y + dy) % 2 == py)
            where.setdefault(corner, set()).add((yy, cyc[yy][i]))
    # a point and its iota-image develop to the same position; iota-orbits:
    # a lattice position belongs to one corner class, so >1 cycle there means either
    # an iota-pair (interior point, front/back) or a pinch.  Interior points have 2
    # cycles (front/back) and wall points 1; a pinch shows as > 2, or 2 on the wall.
    for corner, pts in where.items():
        walls = [p for p in pts if p in on_wall]
        if len(walls) > 1 or len(pts) > 2:
            return 'pinch'
    return 'planar'


def mirror(t):
    """b <-> d mirror: (g_a^-1, g_d^-1, g_c^-1, g_b^-1); product 1 in the right action."""
    a, b, c, d = t
    m = (inv(a), inv(d), inv(c), inv(b))
    e = mul(mul(mul(m[0], m[1]), m[2]), m[3])
    assert e == tuple(range(len(a)))
    return m


def centraliser_involutions(t):
    n = len(t[0])
    out = []
    for v in range(1, n):
        phi = [-1] * n
        phi[0] = v
        q = [0]
        ok = True
        for x in q:
            for g in t:
                y, fy = g[x], g[phi[x]]
                if phi[y] < 0:
                    phi[y] = fy
                    q.append(y)
                elif phi[y] != fy:
                    ok = False
                    break
            if not ok:
                break
        if ok and sorted(phi) == list(range(n)) and all(phi[phi[i]] == i for i in range(n)):
            out.append(tuple(phi))
    return out


def main():
    # default: the d14 section 4.3 family at n = 10; '--all N ...': every orbit with a
    # non-transitive saved x-lit relation at degree N.
    allmode = '--all' in sys.argv
    degrees = [int(a) for a in sys.argv[1:] if a.isdigit()] or [10]
    report = []
    tot = Counter()
    for n in degrees:
        run_degree(n, allmode, report, tot)
    print('TOTAL', dict(tot))
    tag = ('_all_' + '_'.join(map(str, degrees))) if allmode else ''
    (HERE / ('d14_reality%s.json' % tag)).write_text(json.dumps(dict(orbits=report, totals=dict(tot)), indent=1) + '\n')


def run_degree(n, allmode, report, tot):
    mine = json.loads((D12 / f'mine_n{n}.json').read_text())['orbits']
    for o in mine:
        t0 = tuple(tuple(g) for g in o['rep'])
        if not allmode:
            if o['primitive'] or o['order'] not in (1920, 3840):
                continue
            systems = [p for p in d4.all_block_systems(list(t0), n) if len(p) * 2 == n]
            if len(systems) != 1:
                continue
            part = systems[0]
        else:
            systems = [p for p in d4.all_block_systems(list(t0), n) if 1 < len(p) < n]
            part = max(systems, key=len) if systems else [list(range(n))]
        cid, plen = initial_pt(t0[0])
        ids = sorted({c for c in cid if plen[c] == 2})
        pos = {p: k for k, p in enumerate(ids)}
        q = len(ids)
        sheets = {k: sorted(i for i in range(n) if cid[i] == p) for p, k in pos.items()}
        rels = []
        for x in (1, 2, 3):
            lit = {(pos[p['P']], pos[p['Q']]) for p in o['pairs'] if p['lit_x'][x - 1]}
            lit |= {(j, i) for i, j in lit}
            par = list(range(q))

            def f(u):
                while par[u] != u:
                    u = par[u]
                return u
            for i, j in lit:
                par[f(i)] = f(j)
            bad = [(i, j) for i in range(q) for j in range(i + 1, q) if f(i) == f(j) and (i, j) not in lit]
            if bad:
                rels.append((x, bad))
        if not rels:
            continue
        ind = [d4.induced(g, part) for g in t0]
        ident_corner = [y for y in range(4) if ind[y] == tuple(range(len(part)))]
        deck = centraliser_involutions(t0)
        # are the dark pairs delta-pairs?
        dpairs = []
        for (x, bad) in rels:
            for (i, j) in bad:
                si, sj = set(sheets[i]), set(sheets[j])
                dpairs.append(any({dl[s] for s in si} == sj for dl in deck))
        # certificates (Par, Rig, Cut over every block system, rep state) and B_x
        allf = [U.Factor(t0, P) for P in d4.all_block_systems(list(t0), n)]
        certs, bx = [], []
        for (x, bad) in rels:
            bx.append(len(class_congruence(t0, [x])))
            for (i, j) in bad:
                s0, s1 = sheets[i][0], sheets[j][0]
                certs.append(any(U.par(F, x, s0, s1) or U.rig(F, x, s0, s1) or U.cut(F, t0, x, s0, s1) for F in allf))
        stat = Counter()
        orbit_sizes = []
        for which, tt0 in (('t', t0), ('mirror', mirror(t0))):
            orb = plain_orbit(tt0)
            orbit_sizes.append(len(orb))
            for enc in sorted(orb):
                tt, _ = decode(enc, n, False)
                phis = reflections(tt)
                if not phis:
                    stat[which + ':no_lift'] += 1
                for phi in phis:
                    stat[which + ':' + classify(tt, phi)] += 1
        rec = dict(order=o['order'], cts=o['cts'], rep=o['rep'], plain=o['plain'],
                   relations=[dict(x='abcd'[x], dark_pairs_in_one_class=bad) for x, bad in rels],
                   N_identity_corners=['abcd'[y] for y in ident_corner],
                   N_types=[sorted((len(c) for c in cycles(g)), reverse=True) for g in ind],
                   deck_involutions=len(deck), dark_pairs_are_delta_pairs=dpairs,
                   blocks_of_B_x=bx, dark_pairs_certified=certs,
                   plain_orbit_sizes=orbit_sizes, reflection_status=dict(stat))
        rec['n'] = n
        report.append(rec)
        tot['relations'] += len(rels)
        tot['relations, N without identity corner'] += len(rels) if not ident_corner else 0
        for k, v in stat.items():
            tot[k.split(':')[1]] += v
        print(n, o['order'], o['cts'], 'x', [r['x'] for r in rec['relations']], 'Nid', rec['N_identity_corners'],
              'N types', rec['N_types'], 'deck', len(deck), 'delta-pairs', dpairs, 'B_x blocks', bx, 'certified', certs, 'orbits', orbit_sizes, dict(stat))


if __name__ == '__main__':
    main()
