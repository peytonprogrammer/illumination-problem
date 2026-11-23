"""Check of Lemma H1 (general twist lemma) for the arc a-b on the saved orbits.

For every state t of every saved plain orbit (q >= 2) and m = 1, 2, ... up to the first
return of the plain state, the script checks, in the conventions of hurwitz.py:
  1. m positive full twists s0^2 give (h^-m . g_a, h^-m . g_b, g_c, g_d), where h = g_a g_b
     (apply g_a first) and  k . g  denotes the permutation  k o g o k^-1  (cycles moved by k),
     and the label of the a-point through sheet i moves to the sheet h^-m(i);
  2. the plain state returns after m twists  <=>  h^m lies in C_Gamma C_T, where C_Gamma is
     the centraliser of <g_a, g_b> and C_T the centraliser of <g_c, g_d> in S_n.
     ("=>" is checked by exhibiting c in C_T with c o h^-m in C_Gamma; "<=" by brute force
     over C_T when |C_T| <= 5000.)
  3. at a literal return (the tuple itself returns, c = 1), k = h^-m acts freely on every
     Gamma-component where it is nontrivial, and such a component has at most 2 faces.

Run: python3 -B twistcheck.py 4 5 6 7 8
"""
import json
import sys
from collections import Counter, deque
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
D12 = HERE.parent / 'd12-lit-side'
sys.path.insert(0, str(D6))
from hurwitz import mul, inv, pure_move, canon_plain, initial_pt, PURE_GENS  # noqa: E402

LABELS = ('a', 'b', 'c', 'd')


def act(k, g):
    """k o g o k^-1 as a function on sheets"""
    ki = inv(k)
    return tuple(k[g[ki[s]]] for s in range(len(g)))


def power(h, m):
    r = tuple(range(len(h)))
    for _ in range(m):
        r = mul(r, h)
    return r


def cyc_of(h, s):
    out, x = [s], h[s]
    while x != s:
        out.append(x)
        x = h[x]
    return out


def commutes(a, b):
    return mul(a, b) == mul(b, a)


def centraliser(gens, n, cap=5000):
    """all permutations commuting with gens (the group need not be transitive); None if large"""
    # orbits of <gens>; an element of the centraliser is fixed by the images of orbit roots
    seen = [-1] * n
    orbs = []
    for r in range(n):
        if seen[r] >= 0:
            continue
        orb = [r]
        seen[r] = len(orbs)
        word = {r: ()}
        for x in orb:
            for gi, g in enumerate(gens):
                y = g[x]
                if seen[y] < 0:
                    seen[y] = len(orbs)
                    word[y] = word[x] + (gi,)
                    orb.append(y)
        orbs.append((orb, word))
    out = []
    count = 1
    for orb, _ in orbs:
        count *= n
        if count > 10 ** 7:
            return None
    for images in product(range(n), repeat=len(orbs)):
        c = [-1] * n
        ok = True
        for (orb, word), im in zip(orbs, images):
            for x in orb:
                y = im
                for gi in word[x]:
                    y = gens[gi][y]
                c[x] = y
        if sorted(c) != list(range(n)):
            continue
        c = tuple(c)
        if all(commutes(c, g) for g in gens):
            out.append(c)
            if len(out) > cap:
                return None
    return out


def main():
    for n in [int(a) for a in sys.argv[1:]]:
        mine = json.loads((D12 / f'mine_n{n}.json').read_text())['orbits']
        S = Counter()
        for o in mine:
            t0 = tuple(tuple(g) for g in o['rep'])
            cid, plen = initial_pt(t0[0])
            pt0 = tuple(c if plen[c] == 2 else -1 for c in cid)
            seen = {canon_plain(t0)}
            queue = deque([(t0, pt0)])
            while queue:
                t, pt = queue.popleft()
                for (i, s) in PURE_GENS:
                    t2, _, pt2 = pure_move(t, LABELS, pt, i, s)
                    c = canon_plain(t2)
                    if c not in seen:
                        seen.add(c)
                        queue.append((t2, pt2))
                # the twist test at this state
                h = mul(t[0], t[1])
                pc, labs = canon_plain(t, want_map=True)
                CT = centraliser([t[2], t[3]], n)
                u, pu = t, pt
                m = 0
                while True:
                    m += 1
                    u, _, pu = pure_move(u, LABELS, pu, 0, +1)
                    hm = power(h, m)
                    hmi = inv(hm)
                    assert u == (act(hmi, t[0]), act(hmi, t[1]), t[2], t[3]), 'tuple formula'
                    assert all(pu[hmi[s]] == pt[s] for s in range(n)), 'label formula'
                    S['twist steps checked'] += 1
                    pcu, labsu = canon_plain(u, want_map=True)
                    returned = pcu == pc
                    if CT is not None:
                        inprod = any(commutes(mul(hmi, c), t[0]) and commutes(mul(hmi, c), t[1]) for c in CT)
                        assert inprod == returned, 'Lemma H1 equivalence'
                        S['equivalence checked by brute force'] += 1
                    if u == t:
                        # literal return (c = 1): k = h^-m is nontrivial only on
                        # Gamma-components with at most 2 faces (Lemma H1, part 4)
                        comp = list(range(n))
                        ch = True
                        while ch:
                            ch = False
                            for g in (t[0], t[1]):
                                for s in range(n):
                                    lo = min(comp[s], comp[g[s]])
                                    if comp[s] != lo or comp[g[s]] != lo:
                                        comp[s] = comp[g[s]] = lo
                                        ch = True
                        for y in set(comp):
                            Y = [s for s in range(n) if comp[s] == y]
                            if any(hmi[s] != s for s in Y):
                                assert all(hmi[s] != s for s in Y), 'deck map acts freely'
                                faces = len({min(cyc_of(h, s)) for s in Y})
                                assert faces <= 2, 'more than 2 faces'
                                S['literal returns: nontrivial components with %d face(s)' % faces] += 1
                        S['literal returns checked'] += 1
                    if returned:
                        # c : sheets of u -> sheets of t through the canonical labels
                        lt = inv(tuple(labs[0]))
                        c = tuple(lt[labsu[0][s]] for s in range(n))
                        assert all(act(c, g) == g for g in (t[2], t[3])), 'c in C_T'
                        k = mul(hmi, c)                      # apply h^-m, then c
                        assert commutes(k, t[0]) and commutes(k, t[1]), 'k in C_Gamma'
                        S['returns checked'] += 1
                        S['returns with k trivial on regular a-points'] += all(
                            pt[k[s]] == pt[s] for s in range(n) if pt[s] >= 0)
                        break
        print(n, dict(S))


if __name__ == '__main__':
    main()
