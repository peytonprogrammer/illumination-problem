"""Full orientation-preserving affine group G of the cross double Q, acting on lattice lifts.

Enumerates the SL(2,Z)-orbit of the marked, sigma-equipped origami of Q (the index of the
Veech group), lifts every Schreier generator to an affine map, adds K, and computes
G-orbits and point-stabilizer orbits on lattice lifts. Run: python3 -B fullG.py b"""
import sys
import time
import hashlib
from array import array
from origami import (Surface, cross_cells, sigma_squares, stepT, stepV, canon, inv,
                     descend, qperm, orbits, stabilizer_gens, dedupe)
import many

b = int(sys.argv[1])
S = Surface(cross_cells(b))
N = S.N
mk = [1 if S.vtype[S.LL[q][0]] == 'convex' else 0 for q in range(N)]
starts = [q for q in range(N) if mk[q]]
qpts = sorted({S.qpoint(v) for v in S.verts})
qidx = {v: k for k, v in enumerate(qpts)}
T0 = time.process_time()


def pack(*lists):
    return array('H', [x for l in lists for x in l]).tobytes()


def unpack(bs, k):
    a = array('H')
    a.frombytes(bs)
    a = a.tolist()
    return [a[i * N:(i + 1) * N] for i in range(k)]


def h(key):
    return hashlib.blake2b(repr(key).encode(), digest_size=16).digest()


st0 = (S.r, S.u, sigma_squares(S))
k0, lab0 = canon(st0, mk, starts)
index = {h(k0): 0}
store = [pack(*st0, lab0)]
gens = set()
i = 0
while i < len(store):
    r, u, sg, lab = unpack(store[i], 4)
    i += 1
    for step in (stepT, stepV):
        n = step((r, u, sg), 1)
        key, nlab = canon(n, mk, starts)
        hk = h(key)
        if hk not in index:
            index[hk] = len(store)
            store.append(pack(*n, nlab))
        jlab = unpack(store[index[hk]], 4)[3]
        jinv = inv(jlab)
        psi = [jinv[nlab[q]] for q in range(N)]
        vm = descend(S, psi)
        assert vm is not None
        gens.add(tuple(qperm(S, vm, qpts, qidx)))
K = [tuple(qperm(S, vm, qpts, qidx)) for phi in many.isos_marked(S, S.r, S.u, S.r, S.u)
     for vm in [descend(S, phi)] if vm is not None]
G = [list(g) for g in gens | set(K)]
print(f'cross b={b}: area {len(S.cells)}; Veech index (SL orbit) {len(store)}; '
      f'distinct generator actions on {len(qpts)} lattice lifts: {len(G)}; |K|={len(set(K))}; '
      f'cpu {time.process_time() - T0:.0f}s')
orb = orbits(len(qpts), G)
print('  G-orbit sizes (with multiplicity):', sorted((len(o) for o in orb), reverse=True))
size = {}
for o in orb:
    for k in o:
        p = qpts[k][0]
        size[p] = max(size.get(p, 0), len(o))
for y in range(b, -b - 1, -1):
    print(''.join(f'{size[(x, y)]:4d}' if (x, y) in size else '    ' for x in range(-b, b + 1)))

sys.stdout.flush()


def stab_orbits(si):
    """Orbits of G_s on lattice lifts, via G-orbits of pairs (s, x)."""
    Gs = [si]
    seen = {si}
    for y in Gs:
        for g in G:
            if g[y] not in seen:
                seen.add(g[y])
                Gs.append(g[y])
    pos = {y: k for k, y in enumerate(Gs)}
    n = len(qpts)
    parent = list(range(len(Gs) * n))

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for g in G:
        for y in Gs:
            base, gb = pos[y] * n, pos[g[y]] * n
            for x in range(n):
                a, c = f(base + x), f(gb + g[x])
                if a != c:
                    parent[a] = c
    size = {}
    for x in range(n):
        size[f(x)] = size.get(f(x), 0) + 1  # block sizes within the fibre over s
    return len(Gs), {x: size[f(x)] for x in range(n)}


PAIRS = [((6, 0), (0, 6)), ((5, 1), (1, 5)), ((4, 0), (0, 4))]
if len(sys.argv) > 2 and sys.argv[2] == "one":
    PAIRS = PAIRS[:1]
for P, Tp in PAIRS:
    for si in [k for k, v in enumerate(qpts) if v[0] == P]:
        osz, w = stab_orbits(si)
        t = [k for k, v in enumerate(qpts) if v[0] == Tp]
        same = [x for x in range(len(qpts)) if S.vtype[qpts[x][0]] == 'int'
                and (qpts[x][0][0] - P[0]) % 2 == 0 and (qpts[x][0][1] - P[1]) % 2 == 0 and x != si]
        mx = max(w[x] for x in same)
        print(f'  s={P} lift {qpts[si][1]}: |G.s|={osz}; |G_s.t| over lifts of {Tp}: '
              f'{[w[k] for k in t]}; max over same-parity interior targets {mx}; '
              f'cpu {time.process_time() - T0:.0f}s', flush=True)
