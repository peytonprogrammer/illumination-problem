"""Nielsen classes in which two or more pure-braid orbits have G >= A_n (saved census only).

For each such class: cycle types, orbit sizes, and a test of one explanation: an isometry
of Q covering a translation of the pillowcase (Klein four-group elements, realised on
tuples by s0 s2^-1 and its conjugate).  A cover is called j-symmetric when j(t) is conjugate
to t.  The count of j-symmetric tuples per orbit is reported for the Klein elements
compatible with the cycle types.
"""
import json, sys
from collections import Counter, deque
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
from hurwitz import move, pure_move, canon_plain, PURE_GENS
L = ('a', 'b', 'c', 'd')

def klein(t, which):
    if which == 0:      # (a b)(c d): s0 s2^-1
        u, _, _ = move(t, L, None, 0, 1); u, _, _ = move(u, L, None, 2, -1); return u
    if which == 2:      # (a c)(b d): rotate the cyclic order by two places
        return (t[2], t[3], t[0], t[1])
    return klein(klein(t, 0), 2)          # (a d)(b c)

def orbit(t):
    seen = {canon_plain(t): t}; q = deque([t])
    while q:
        u = q.popleft()
        for (i, s) in PURE_GENS:
            v, _, _ = pure_move(u, L, None, i, s)
            c = canon_plain(v)
            if c not in seen:
                seen[c] = v; q.append(v)
    return seen

def main():
    tot = Counter()
    for n in [int(a) for a in sys.argv[1:]]:
        d = json.load(open(HERE.parent / 'd6-hurwitz-census' / f'census_n{n}.json'))
        for cl in d['classes']:
            orbs = [o for o in cl['orbits'] if o.get('contains_An')]
            if len(orbs) < 2:
                continue
            cts = cl['cts']
            tot[(n, 'classes')] += 1
            rep = len({tuple(c) for c in cts})
            tot[(n, 'distinct cycle types among corners = %d' % rep)] += 1
            sizes = sorted(o['plain_orbit_size'] for o in orbs)
            if len(set(sizes)) < len(sizes):
                tot[(n, 'classes with two A_n-orbits of equal size')] += 1
            if max(sizes) > 3000:
                tot[(n, 'symmetry test skipped (orbit > 3000)')] += 1
                continue
            compat = [w for w, perm in enumerate(((1, 0, 3, 2), (3, 2, 1, 0), (2, 3, 0, 1)))
                      if all(cts[i] == cts[perm[i]] for i in range(4))]
            row = []
            for o in orbs:
                t = tuple(tuple(g) for g in o['rep'])
                orb = orbit(t)
                assert len(orb) == o['plain_orbit_size']
                sym = {w: sum(1 for c, u in orb.items() if canon_plain(klein(u, w)) == c) for w in compat}
                pres = {w: (canon_plain(klein(t, w)) in orb) for w in compat}
                row.append((len(orb), sym, pres))
            kinds = tuple(sorted(any(v > 0 for v in r[1].values()) for r in row))
            tot[(n, 'A_n-orbits with/without a j-symmetric tuple: %s' % (kinds,))] += 1
            if not any(kinds) or len(set(kinds)) == 1 or tot[(n, 'printed')] < 2:
                tot[(n, 'printed')] += 1
                print(n, cts, row)
    for k in sorted(tot):
        print(k, tot[k])

if __name__ == '__main__':
    main()
