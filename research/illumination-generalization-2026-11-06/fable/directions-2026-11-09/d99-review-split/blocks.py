"""d99: sheet monodromy of named rooms: cycle types, primitivity, every block system, group order.
Sheets = unit cells; g_(p,q) = sigma_x,p o sigma_y,q as in d94 cross.py. Exact permutations.
Run: python3 -B blocks.py > blocks.log"""
import os, sys, json, time
from collections import Counter
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '..', 'd94-review-transfer'))
from cross import setup, cycles, closure, room

T0 = time.process_time()


def all_blocks(n, gens):
    """Every block containing 0 (as frozensets), by closing B u {j}."""
    whole = frozenset(range(n))
    found = {frozenset([0]), whole}
    todo = [frozenset([0])]
    while todo:
        B = todo.pop()
        for j in range(n):
            if j in B:
                continue
            C = next(frozenset(p) for p in closure(n, gens, [(min(B), x) for x in B] + [(min(B), j)]) if 0 in p)
            if C not in found:
                found.add(C)
                todo.append(C)
    return sorted(found, key=len)


def order(n, gens):
    """Deterministic Schreier-Sims (Holt's SCHREIERSIMS: strip every Schreier generator)."""
    ident = tuple(range(n))
    mul = lambda a, b: tuple(a[x] for x in b)  # a o b

    def inv(a):
        out = [0] * n
        for i, x in enumerate(a):
            out[x] = i
        return tuple(out)
    base, strong = [], []
    for g in map(tuple, gens):
        if g != ident:
            strong.append(g)
    if not strong:
        return 1

    def level_gens(i):
        return [s for s in strong if all(s[b] == b for b in base[:i])]

    def orbit(i):
        gs = level_gens(i)
        tr = {base[i]: ident}
        q = [base[i]]
        for y in q:
            for s in gs:
                z = s[y]
                if z not in tr:
                    tr[z] = mul(s, tr[y])
                    q.append(z)
        return gs, tr

    def strip(g):
        for i in range(len(base)):
            y = g[base[i]]
            if y not in T[i][1]:
                return g, i
            g = mul(inv(T[i][1][y]), g)
        return g, len(base)
    base.append(next(x for x in range(n) if strong[0][x] != x))
    T = [orbit(0)]
    i = 0
    while i >= 0:
        gs, tr = T[i]
        bad = None
        for y, ty in tr.items():
            for s in gs:
                h = mul(inv(tr[s[y]]), mul(s, ty))
                r, j = strip(h)
                if r != ident:
                    bad = (r, j)
                    break
            if bad:
                break
        if bad is None:
            i -= 1
            continue
        r, j = bad
        strong.append(r)
        if j == len(base):
            base.append(next(x for x in range(n) if r[x] != x))
            T.append(None)
        for l in range(i + 1, j + 1):
            T[l] = orbit(l)
        i = j
    o = 1
    for _, tr in T:
        o *= len(tr)
    return o


def report(name, cells, do_order=True):
    idx, n, S, g = setup(cells)
    gens = [g[k] for k in sorted(g)]
    print(f'== {name}: n = {n} sheets')
    r = 0
    for k in sorted(g):
        ct = Counter(len(c) for c in cycles(g[k]))
        assert set(ct) <= {1, 2, 3}
        r += ct[3]
        print(f'  class {k}: f={ct[1]} q={ct[2]} z={ct[3]}  (support of g^2 = {3*ct[3]})')
    print(f'  r = {r}, W = {2*r+4}, 2r+2 = {2*r+2}')
    blocks = all_blocks(n, gens)
    prop = [B for B in blocks if 1 < len(B) < n]
    print(f'  primitive: {not prop}; proper nontrivial blocks containing sheet 0: {len(prop)}')
    systems = Counter()
    for B in prop:
        systems[len(B)] += 1
    for size, cnt in sorted(systems.items()):
        print(f'    block size {size} ({n // size} blocks): {cnt} system(s)')
    from math import factorial
    for B in prop:
        P = closure(n, gens, [(min(B), x) for x in B])
        blk = {a: bi for bi, p in enumerate(P) for a in p}
        m = len(P)
        H = [[blk[gg[p[0]]] for p in P] for gg in gens]
        hb = [b for b in all_blocks(m, H) if 1 < len(b) < m]
        ho = order(m, H) if do_order else None
        alt = '' if ho is None else f', |H| = {ho}, contains A_{m}: {ho >= factorial(m) // 2}'
        cyc = [sorted(Counter(len(c) for c in cycles(h)).items()) for h in H]
        print(f'    size {len(B)}: block of 0 = {sorted(cells[a] for a in B)}; block action on {m}: '
              f'primitive {not hb}{alt}; cycle types {cyc}')
    if do_order:
        o = order(n, gens)
        print(f'  |G| = {o}')
    print(f'  cpu {time.process_time() - T0:.1f}s', flush=True)
    return idx, n, S, g, prop


if __name__ == '__main__':
    R22 = [tuple(c) for c in json.load(open(os.path.join(D, '..', 'd8-perturbation-test', 'rooms.json')))[0]['cells']]
    assert json.load(open(os.path.join(D, '..', 'd8-perturbation-test', 'rooms.json')))[0]['id'] == 'R22-base'
    report('R22-base', sorted(R22))
    report('cross b=7', room(7), do_order='order' in sys.argv)
