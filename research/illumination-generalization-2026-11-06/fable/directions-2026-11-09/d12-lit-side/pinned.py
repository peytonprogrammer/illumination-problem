"""Pure braid orbit of (g_b, g_c, g_d) with g_a pinned (exact triples, no conjugation).

PB_3 acts on triples with product g_a^-1 by the squares s1^2, s2^2 and s1 s2^2 s1^-1 of
the Hurwitz moves on positions (1,2), (2,3).  The set X_x of values taken by g_x over the
orbit is the set of monodromies of lassos along simple arcs from (a neighbourhood of) a to x.
"""
import sys, json
from collections import deque, Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
from hurwitz import mul, inv, cycles

def hm(t, i, sign):
    t = list(t); a, b = t[i], t[i+1]
    if sign > 0:
        t[i], t[i+1] = mul(mul(a, b), inv(a)), a
    else:
        t[i], t[i+1] = b, mul(mul(inv(b), a), b)
    return tuple(t)

def gens(t):
    out = []
    for i in (1, 2):
        for s in (1, -1):
            out.append(hm(hm(t, i, s), i, s))
    for s in (1, -1):                      # s1 s2^(2s) s1^-1
        u = hm(t, 1, 1); u = hm(hm(u, 2, s), 2, s); u = hm(u, 1, -1)
        out.append(u)
    return out

def pinned_orbit(t):
    seen = {t}; q = deque([t])
    while q:
        u = q.popleft()
        for v in gens(u):
            assert v[0] == t[0]
            if v not in seen:
                seen.add(v); q.append(v)
    return seen

def cyc_str(p):
    return ''.join('(' + ' '.join(map(str, c)) + ')' for c in cycles(p) if len(c) > 1) or '1'

if __name__ == '__main__':
    t = tuple(tuple(g) for g in json.loads(sys.argv[1]))
    orb = pinned_orbit(t)
    print('g_a =', cyc_str(t[0]), ' pinned orbit size', len(orb))
    for x in (1, 2, 3):
        X = Counter(u[x] for u in orb)
        print('corner', 'abcd'[x], ': distinct values of g_x:', len(X))
        if len(X) <= 40:
            for g in sorted(X):
                print('    ', cyc_str(g), X[g])
