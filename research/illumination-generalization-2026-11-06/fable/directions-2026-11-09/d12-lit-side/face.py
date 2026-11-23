"""Face certificate test (cycle types only, no orbit enumeration).

Face(x) holds for a class (alpha; types of b, c, d) when no cycle type lam satisfies both
  (i)  lam = type(g_a g_x) for some g_x of type xi whose graph with g_a has a chain joining
       two distinct 2-cycles of g_a through 2-cycles only, and
  (ii) lam = type(g_y g_z) for some g_y, g_z of the two other types.
Lemma F (notes.md): Face(x) implies that no pair is x-lit in the whole class.
The script compares Face(x) with the mined verdicts in mine_n*.json.
"""
import json, sys
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations
from pathlib import Path
HERE = Path(__file__).resolve().parent

def ctype(p):
    seen = [False] * len(p); out = []
    for i in range(len(p)):
        if not seen[i]:
            l = 0; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            out.append(l)
    return tuple(sorted(out, reverse=True))

def std(t):
    p = []; i = 0
    for l in t:
        p += [i + (k + 1) % l for k in range(l)]; i += l
    return tuple(p)

@lru_cache(None)
def klass(t):
    """All permutations of cycle type t (parts <= 3), by direct construction."""
    n = sum(t)
    out = set()
    def rec(free, parts, cur):
        if not parts:
            out.add(tuple(cur)); return
        l = parts[0]; i = free[0]; rest = free[1:]
        if l == 1:
            rec(rest, parts[1:], cur)
        elif l == 2:
            for j in rest:
                c = cur[:]; c[i] = j; c[j] = i
                rec([k for k in rest if k != j], parts[1:], c)
        else:
            for j in rest:
                for k in rest:
                    if k != j:
                        c = cur[:]; c[i] = j; c[j] = k; c[k] = i
                        rec([m for m in rest if m != j and m != k], parts[1:], c)
    # choose which part type the smallest free sheet takes: iterate over orderings of parts
    for order in set(permutations(t)):
        rec(list(range(n)), list(order), list(range(n)))
    return frozenset(out)

def has_chain(ga, gx):
    """True when some chain joins two distinct 2-cycles of ga through 2-cycles of gx, ga."""
    n = len(ga)
    two_a = [i for i in range(n) if ga[i] != i and ga[ga[i]] == i]
    two_x = set(i for i in range(n) if gx[i] != i and gx[gx[i]] == i)
    for s in two_a:
        if s > ga[s]:
            continue
        for start in (s, ga[s]):
            cur = start
            while cur in two_x:
                nxt = gx[cur]            # other sheet of the mirror
                if ga[nxt] == nxt or ga[ga[nxt]] != nxt:
                    break                # not a 2-cycle of g_a: light stops
                if nxt not in (s, ga[s]):
                    return True
                else:
                    break
    return False

@lru_cache(None)
def lam_chain(alpha, xi):
    ga = std(alpha); out = set()
    for gx in klass(xi):
        if has_chain(ga, gx):
            out.add(ctype(tuple(gx[ga[i]] for i in range(len(ga)))))
    return frozenset(out)

@lru_cache(None)
def lam_prod(eta, zeta):
    gy = std(eta)
    return frozenset(ctype(tuple(gz[gy[i]] for i in range(len(gy)))) for gz in klass(zeta))

for n in [int(a) for a in sys.argv[1:]]:
    d = json.loads((HERE / f'mine_n{n}.json').read_text())
    cls = defaultdict(list)
    for o in d['orbits']:
        cls[json.dumps(o['cts'])].append(o)
    S = Counter()
    for key, orbs in sorted(cls.items()):
        cts = [tuple(sorted(c, reverse=True)) for c in json.loads(key)]
        for xi in range(3):
            if 2 not in cts[xi + 1]:
                continue
            y, z = [cts[k + 1] for k in range(3) if k != xi]
            face = not (lam_chain(cts[0], cts[xi + 1]) & (lam_prod(y, z) | lam_prod(z, y)))
            empty = not any(p['lit_x'][xi] for o in orbs for p in o['pairs'])
            allcert = all(p['cert_x'][xi] for o in orbs for p in o['pairs'])
            S[('Face' if face else 'no Face', 'x-empty' if empty else 'not x-empty',
               'all certified over B' if allcert else 'some uncertified')] += 1
            if face and not empty:
                print('CONTRADICTION', n, cts, xi)
            if empty and not face and not allcert:
                print('  x-empty, no Face, uncertified:', n, cts, 'x=' + 'bcd'[xi])
    print(n)
    for k, v in sorted(S.items()):
        print('   ', k, v)
