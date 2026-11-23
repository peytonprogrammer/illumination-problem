"""Proof attempt (b), induction on the degree: sheet removal test.

A sheet i fixed by g_a and by g_x (x in b, c, d) can be deleted: shorten the cycles through i
of the two other loops.  The result is a product-one transitive genus-0 tuple of degree n-1
with the same 2-cycles of g_a.  The script
  1. counts the orbits that have such a sheet in some state of the plain pure-braid orbit;
  2. compares the LIT/DARK verdict of every marked pair before and after the removal
     (first removable state found per orbit and corner).
"""
import sys, json
from collections import deque, Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
from hurwitz import (mul, inv, cycles, cycle_index, move, pure_move, PURE_GENS, canon_plain,
                     initial_pt, marked_orbit, is_transitive)
LABELS = ('a', 'b', 'c', 'd')

def drop(p, i):
    """Delete sheet i from its cycle of p and relabel the sheets to 0..n-2."""
    n = len(p)
    q = list(p)
    if p[i] != i:
        m = p.index(i)
        q[m] = p[i]
    q[i] = i
    ren = [k if k < i else k - 1 for k in range(n)]
    out = [0] * (n - 1)
    for k in range(n):
        if k != i:
            out[ren[k]] = ren[q[k]]
    return tuple(out)

def remove(t, pt, i, x):
    """Sheet i is fixed by t[0] and t[x].  Return the degree n-1 tuple and its point labels."""
    if x == 2:
        t, _, pt = move(t, LABELS, pt, 0, +1)          # (b', a, c, d)
        t = (drop(t[0], i), drop(t[1], i), drop(t[2], i), drop(t[3], i))
        pt = tuple(pt[k] for k in range(len(pt)) if k != i)
        t, _, pt = move(t, LABELS, pt, 0, -1)
    else:
        t = tuple(drop(g, i) for g in t)
        pt = tuple(pt[k] for k in range(len(pt)) if k != i)
    return tuple(t), pt

for n in [int(a) for a in sys.argv[1:]]:
    d = json.loads((HERE / f'mine_n{n}.json').read_text())
    S = Counter(); T = Counter()
    for o in d['orbits']:
        t0 = tuple(tuple(g) for g in o['rep'])
        cid, plen = initial_pt(t0[0])
        pt0 = tuple(c if plen[c] == 2 else -1 for c in cid)
        verdict = {frozenset((p['P'], p['Q'])): p['lit'] for p in o['pairs']}
        seen = {canon_plain(t0)}; queue = deque([(t0, pt0)])
        found = {}
        while queue:
            t, pt = queue.popleft()
            for x in (1, 2, 3):
                if x not in found:
                    for i in range(n):
                        if t[0][i] == i and t[x][i] == i:
                            found[x] = (t, pt, i); break
            for (i, s) in PURE_GENS:
                t2, _, pt2 = pure_move(t, LABELS, pt, i, s)
                c = canon_plain(t2)
                if c not in seen:
                    seen.add(c); queue.append((t2, pt2))
        S['orbits'] += 1
        S['orbits with a removable sheet (fixed by a and one of b, c, d)'] += bool(found)
        for x, (t, pt, i) in found.items():
            ts, pts = remove(t, pt, i, x)
            e = tuple(range(n - 1))
            assert mul(mul(mul(ts[0], ts[1]), ts[2]), ts[3]) == e, (t, i, x)
            assert is_transitive(list(ts), n - 1)
            assert sum(len(cycles(g)) for g in ts) == 2 * (n - 1) + 2
            cid2, plen2 = initial_pt(ts[0])
            # map small point IDs to big point IDs
            m = {}
            for k in range(n - 1):
                if plen2[cid2[k]] == 2:
                    assert pts[k] >= 0
                    m[cid2[k]] = pts[k]
            assert len(m) == len(set(m.values())) == o['q']
            r = marked_orbit(ts)
            lit_small = {frozenset((m[a], m[b])) for a, b in (tuple(pr) for pr in r['lit'])}
            for pr, big in verdict.items():
                T[('big LIT' if big else 'big DARK', 'small LIT' if pr in lit_small else 'small DARK')] += 1
                if bool(big) != (pr in lit_small) and T[('example', bool(big))] < 2:
                    T[('example', bool(big))] += 1
                    print('   example', n, 'big', 'LIT' if big else 'DARK', 'cts', o['cts'], 'x=' + 'abcd'[x],
                          'small cts', [sorted((len(c) for c in cycles(g)), reverse=True) for g in ts])
    print(n, dict(S))
    for k, v in sorted((k, v) for k, v in T.items() if k[0] != 'example'):
        print('   ', k, v)
