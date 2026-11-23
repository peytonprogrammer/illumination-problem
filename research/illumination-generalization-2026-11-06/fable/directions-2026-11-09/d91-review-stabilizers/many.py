"""Stabilizers of all primitive directions with max(|p|,|q|) <= R. Run: python3 -B many.py > many.log"""
import sys
import time
from math import gcd
from origami import (Surface, cross_cells, staircase_cells, apply_word, to_horizontal, cylinders,
                     shearT, descend, qperm, orbits, stabilizer_gens, dedupe, lcm, divisors,
                     isomorphisms)

T0 = time.process_time()


def isos_marked(S, r1, u1, r2, u2):
    """phi with phi o r1 = r2 o phi, phi o u1 = u2 o phi, sending a marked square to a marked one."""
    mk = [S.LL[q] in S.marked and S.vtype[S.LL[q][0]] == 'convex' for q in range(S.N)]
    q0 = mk.index(True)
    N = S.N
    out = []
    for start in [q for q in range(N) if mk[q]]:
        phi = [-1] * N
        phi[q0] = start
        stack = [q0]
        ok = True
        while stack and ok:
            x = stack.pop()
            for a, b in ((r1, r2), (u1, u2)):
                y, z = a[x], b[phi[x]]
                if phi[y] == -1:
                    phi[y] = z
                    stack.append(y)
                elif phi[y] != z:
                    ok = False
                    break
        if ok and -1 not in phi and len(set(phi)) == N:
            out.append(phi)
    return out


def run(name, cells, R, pairs):
    S = Surface(cells)
    qpts = sorted({S.qpoint(v) for v in S.verts})
    qidx = {v: k for k, v in enumerate(qpts)}
    K = dedupe([qperm(S, vm, qpts, qidx) for phi in isos_marked(S, S.r, S.u, S.r, S.u)
                for vm in [descend(S, phi)] if vm is not None])
    dirs = [(p, q) for p in range(0, R + 1) for q in range(-R, R + 1)
            if gcd(p, q) == 1 and (p > 0 or q == 1)]
    gens = list(K)
    maxper = {}
    for d in dirs:
        word = to_horizontal(*d)
        r, u = apply_word(S.r, S.u, word)
        cyl = cylinders(S, r, u)
        lam_mt = 1
        for c, h, _ in cyl:
            lam_mt = lcm(lam_mt, c // gcd(c, h))
        got = None
        for dd in divisors(lam_mt):
            r2, u2 = shearT(r, u, dd)
            ms = [vm for phi in isos_marked(S, r2, u2, r, u) for vm in [descend(S, phi)] if vm is not None]
            if ms:
                got = (dd, ms)
                break
        assert got
        g = [qperm(S, vm, qpts, qidx) for vm in got[1]]
        gens += g
        maxper[d] = max(gcd(c, h) for c, h, _ in cyl)
    gens = dedupe(gens)
    orb = orbits(len(qpts), gens)
    print(f'\n=== {name}: area {len(cells)}; {len(dirs)} directions with max(|p|,|q|)<={R}; '
          f'max over directions of max_i gcd(C_i,H_i) (M units) = {max(maxper.values())}')
    print(f'  orbit sizes of H on {len(qpts)} lattice lifts: '
          f'{sorted({len(o) for o in orb}, reverse=True)}')
    for P, Tp in pairs:
        s = [k for k, v in enumerate(qpts) if v[0] == P]
        t = [k for k, v in enumerate(qpts) if v[0] == Tp]
        for si in s:
            sg, osz = stabilizer_gens(len(qpts), gens, si)
            o = orbits(len(qpts), dedupe(sg))
            sizes = [len(next(x for x in o if ti in x)) for ti in t]
            print(f'  S={P} lift {qpts[si][1]}: |H.s|={osz}; |H_s.t| for T={Tp}: {sizes}')
    sys.stdout.flush()


if __name__ == '__main__':
  R = int(sys.argv[1]) if len(sys.argv) > 1 else 6
  for m in (4, 5, 8):
      run(f'staircase m={m}', staircase_cells(m), R, [((m - 1, m - 1), (m + 1, m + 1))])
  for b in (7, 9, 11):
      run(f'cross b={b}', cross_cells(b), R, [((6, 0), (0, 6)), ((1, 0), (0, 1)), ((5, 1), (1, 5))])
  print(f'\nCPU seconds: {time.process_time() - T0:.1f}')
