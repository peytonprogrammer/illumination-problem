"""D91 checks. Run: python3 -B check.py > check.log"""
import time
from origami import (Surface, cross_cells, staircase_cells, compose, inv, apply_word,
                     to_horizontal, isomorphisms, descend, direction_stabilizer, qperm,
                     orbits, stabilizer_gens, dedupe, cylinders)

T0 = time.process_time()


def check_vertices(S, r, u):
    c = compose(u, compose(r, compose(inv(u), inv(r))))
    seen = [False] * S.N
    for q in range(S.N):
        if not seen[q]:
            cyc, x = [], q
            while not seen[x]:
                seen[x] = True
                cyc.append(x)
                x = c[x]
            labs = {S.LL[x] for x in cyc}
            assert len(labs) == 1, 'commutator cycle spans labels'
            v = labs.pop()
            k = sum(1 for y in range(S.N) if S.LL[y] == v)
            assert k == len(cyc)
            want = 3 if S.vtype[v[0]] == 'reflex' else 1
            assert len(cyc) == want, (v, len(cyc))


def setup(S):
    qpts = sorted({S.qpoint(v) for v in S.verts})
    qidx = {v: k for k, v in enumerate(qpts)}
    autos = [vm for phi in isomorphisms(S.r, S.u, S.r, S.u)
             for vm in [descend(S, phi)] if vm is not None]
    return qpts, qidx, autos


def lifts(S, qpts, p):
    return [k for k, v in enumerate(qpts) if v[0] == p]


def run_cross(b, extra_dirs):
    S = Surface(cross_cells(b))
    n = len(S.cells)
    check_vertices(S, S.r, S.u)
    qpts, qidx, autos = setup(S)
    print(f'\n=== cross b={b}: area {n} (16b-16={16*b-16}), M squares {S.N}, '
          f'Q lattice points {len(qpts)}')
    Kq = dedupe([qperm(S, vm, qpts, qidx) for vm in autos])
    print(f'  derivative-I automorphisms of M descending to Q: {len(autos)}; '
          f'distinct Q actions (= K): {len(Kq)}')
    # physical action of K
    for g in Kq:
        img = qpts[g[qidx[S.qpoint(((6, 0), (1, 1)))]]][0]
        print(f'    K element sends (6,0) to {img}')
    s = lifts(S, qpts, (6, 0))
    t = lifts(S, qpts, (0, 6))
    Korb = orbits(len(qpts), Kq)
    print(f'  max |K.z| over lattice lifts: {max(len(o) for o in Korb)}')

    results = {}
    for d in [(1, 0), (0, 1)] + extra_dirs:
        word = to_horizontal(*d)
        r, u = apply_word(S.r, S.u, word)
        check_vertices(S, r, u)
        cyl, lam_mt, (lam0, maps) = direction_stabilizer(S, word, autos)
        gens = dedupe([qperm(S, vm, qpts, qidx) for vm in maps])
        results[d] = gens
        print(f'  direction {d}: M cylinders (circ,height) '
              f'{sorted((c, h) for c, h, _ in cyl)}; multitwist lambda {lam_mt}; '
              f'least lambda in stabilizer {lam0}; {len(maps)} maps at that lambda')

    # A = <horizontal, vertical, K>
    A = dedupe(results[(1, 0)] + results[(0, 1)] + Kq)
    Aorb = orbits(len(qpts), A)
    same = sorted(map(sorted, Aorb)) == sorted(map(sorted, Korb))
    print(f'  A-orbits on lattice lifts equal K-orbits: {same}; '
          f'max |A.z| = {max(len(o) for o in Aorb)}')
    for si in s:
        sg, osz = stabilizer_gens(len(qpts), A, si)
        o = orbits(len(qpts), sg)
        sizes = [len(next(x for x in o if ti in x)) for ti in t]
        print(f'  A_s, s={qpts[si]}: |A.s|={osz}; |A_s . t| over lifts of (0,6): {sizes}')

    # larger group from several cusps
    H = dedupe([g for gs in results.values() for g in gs] + Kq)
    Horb = orbits(len(qpts), H)
    print(f'  H = <stabilizers of {len(results)} directions>: orbit sizes on lattice lifts '
          f'{sorted((len(o) for o in Horb), reverse=True)[:8]} ...')
    for si in s:
        sg, osz = stabilizer_gens(len(qpts), H, si)
        sg = dedupe(sg)
        o = orbits(len(qpts), sg)
        sizes = [len(next(x for x in o if ti in x)) for ti in t]
        rev = []
        for ti in t:
            sg2, _ = stabilizer_gens(len(qpts), H, ti)
            o2 = orbits(len(qpts), dedupe(sg2))
            rev.append(len(next(x for x in o2 if si in x)))
        print(f'  H_s, s={qpts[si]}: |H.s|={osz}; |H_s . t| = {sizes}; '
              f'|H_t . s| = {rev}')


def run_staircase(m):
    S = Staircase = Surface(staircase_cells(m))
    check_vertices(S, S.r, S.u)
    qpts, qidx, autos = setup(S)
    Kq = dedupe([qperm(S, vm, qpts, qidx) for vm in autos])
    cyl, lam_mt, (lam0, maps) = direction_stabilizer(S, [], autos)
    s = lifts(S, qpts, (m - 1, m - 1))
    t = lifts(S, qpts, (m + 1, m + 1))
    print(f'\n=== staircase m={m}: area {len(S.cells)} (2m^2+6={2*m*m+6}); |K| = {len(Kq)}; '
          f'horizontal M cylinders {sorted((c, h) for c, h, _ in cyl)}; '
          f'multitwist {lam_mt}; least lambda {lam0}')
    F = [qperm(S, vm, qpts, qidx) for vm in maps]
    g6 = None
    # the note's F has derivative T^6; find an element of that derivative fixing t
    from origami import shearT
    r2, u2 = shearT(S.r, S.u, 6)
    for phi in isomorphisms(r2, u2, S.r, S.u):
        vm = descend(S, phi)
        if vm is None:
            continue
        g = qperm(S, vm, qpts, qidx)
        if all(g[ti] == ti for ti in t):
            g6 = g
            break
    for si in s:
        x, k = g6[si], 1
        while x != si:
            x, k = g6[x], k + 1
        print(f'  T^6 element fixing both lifts of T: period of s={qpts[si]} is {k}; '
              f'm/gcd(m,3) = {m // __import__("math").gcd(m, 3)}')
    # K-centrality fixed points
    for ti in t:
        print(f'  K-orbit of t={qpts[ti]}: {sorted(qpts[g[ti]] for g in Kq)}')


for m in (4, 5, 8):
    run_staircase(m)
dirs = [(1, 1), (1, -1), (1, 2), (2, 1)]
for b in (7, 9, 11):
    run_cross(b, dirs)
print(f'\nCPU seconds: {time.process_time() - T0:.1f}')
