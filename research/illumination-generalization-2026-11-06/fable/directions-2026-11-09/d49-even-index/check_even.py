"""d49 read-only check on named rooms only (22-wall room, 12-wall cross). No search.

For a normalized room R with lattice marks S, T and a rectangular base Lambda = A^{-1} Z^2,
A = diag(a, b), d47 Prop 2.1 identifies certificates over P_Lambda with ordinary certificates of
the lattice room A R over its unit pillowcase.  So the monodromy of Q -> P_Lambda is room_tuple(A R).

For each base and each corner x it computes the canonical Par factor B_x and, for each y, the
canonical Rig factor R_y (d10 R3, valid over any base), tests Par / Rig per lift pair with the
d10 unified_test definitions (live vertices, basic arc), and records (delta, d, z, poles).
It checks the d49 claims on every separating certificate it finds:
  * Lemma Z: z >= 1 forces n <= 8r (Par), 5r (Rig);
  * a zero-free separating certificate is a pillowcase (p = 4);
  * a zero-free separating Rig has d = 4 and no pole of N over a or over x (Lemma R0).
Cut: d49 Lemma Z bounds (n <= 3r with a zero, n <= 4r+4 zero-free and then g_x has no 2-cycle)
are evaluated; when they exclude Cut it is not searched.
The 45-degree base Z^2 + Z(1/2, 1/2) is not rectangular and is not covered here.
"""
import sys
import time
import resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from roomtools import *  # noqa
from unified_test import Factor, par, rig  # noqa


def rigid(t, y):
    seeds = [(c[0], s) for c in cycles(t[y]) for s in c[1:]]
    return closure_partition(len(t[0]), t, seeds)


def data(F):
    z = sum(1 for y in range(4) for L in F.nlen[y] if L == 3)
    p = sum(1 for y in range(4) for L in F.nlen[y] if L == 1)
    return z, p


def scale(cells, a, b):
    return {(a * i + u, b * j + v) for (i, j) in cells for u in range(a) for v in range(b)}


def report(label, cells, S, T, a, b):
    t0 = time.process_time()
    C = scale(cells, a, b)
    o = (a * S[0], b * S[1])
    Tq = (a * T[0], b * T[1])
    led = ledger(cells, S)
    r = led['r']
    room, t = room_tuple(C, o)
    n = len(t[0])
    m = a * b
    print('== %s, base Lambda = (1/%d)Z x (1/%d)Z, m = %d, n = m n_R = %d, r = %d, 8r = %d, 5r = %d, 4r+4 = %d'
          % (label, a, b, m, n, r, 8 * r, 5 * r, 4 * r + 4))
    if ((Tq[0] - o[0]) % 2, (Tq[1] - o[1]) % 2) != (0, 0):
        print('  marks in different classes over this base: only Rig(t) applies; not tested here')
        return
    LS, LT = lifts(room, t, o, o), lifts(room, t, Tq, o)
    nolift2 = [x for x in (1, 2, 3) if not any(len(c) == 2 for c in cycles(t[x]))]
    print('  corners with no regular point of Q (all vertices):', ['abcd'[x] for x in nolift2])
    cert = {(i, j): set() for i in range(len(LS)) for j in range(len(LT))}
    viol = []
    for xn, x in (('b', 1), ('c', 2), ('d', 3)):
        F = Factor(t, class_congruence(t, [x]))
        z, p = data(F)
        sep = [par(F, x, LS[i][0], LT[j][0]) for i in range(len(LS)) for j in range(len(LT))]
        print('  Par(%s): B_x blocks d = %d, delta = %d, z = %d, p = %d, separates %s'
              % (xn, F.m, n // F.m, z, p, sep))
        for k, s in enumerate(sep):
            if s:
                cert[divmod(k, len(LT))].add(xn)
                if z >= 1 and n > 8 * r:
                    viol.append(('LemmaZ Par', xn))
                if z == 0 and p != 4:
                    viol.append(('zero-free not pillowcase', xn))
    for yn, y in (('b', 1), ('c', 2), ('d', 3)):
        F = Factor(t, rigid(t, y))
        z, p = data(F)
        for xn, x in (('b', 1), ('c', 2), ('d', 3)):
            if x == y:
                continue
            sep = [rig(F, x, LS[i][0], LT[j][0]) for i in range(len(LS)) for j in range(len(LT))]
            poles_ax = sum(1 for yy in (0, x) for L in F.nlen[yy] if L == 1)
            print('  Rig(%s) via R_%s: d = %d, delta = %d, z = %d, p = %d, poles over a,x = %d, separates %s'
                  % (xn, yn, F.m, n // F.m, z, p, poles_ax, sep))
            for k, s in enumerate(sep):
                if s:
                    cert[divmod(k, len(LT))].add(xn)
                    if z >= 1 and n > 5 * r:
                        viol.append(('LemmaZ Rig', xn))
                    if z == 0 and (p != 4 or F.m != 4 or poles_ax):
                        viol.append(('Lemma R0', xn, yn))
    cut_possible = n <= 3 * r or (n <= 4 * r + 4 and bool(nolift2))
    print('  Cut possible by Lemma Z:', cut_possible, '(not searched)' if cut_possible else '')
    full = {k: v == {'b', 'c', 'd'} for k, v in cert.items()}
    print('  targets certified per lift pair (Par/Rig):', {k: sorted(v) for k, v in cert.items()})
    print('  lift pairs with all 3 targets certified by Par/Rig:', [k for k, f in full.items() if f])
    print('  claim violations:', viol)
    print('  CPU', round(time.process_time() - t0, 3))


R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
C22 = cells_from_vertices(R22)
CROSS = {(i, j) for i in range(4) for j in range(1, 3)} | {(i, j) for i in range(1, 3) for j in range(4)}
for (a, b) in ((1, 1), (2, 1), (1, 2), (2, 2)):
    report('22-wall room (normal form of 22-wall x 2), S=(0,0), T=(2,2)', C22, (0, 0), (2, 2), a, b)
for (a, b) in ((1, 1), (2, 1), (1, 2), (2, 2)):
    report('12-wall cross (normal form of cross x 2), S=(1,2), T=(3,2)', CROSS, (1, 2), (3, 2), a, b)
print('total CPU', round(time.process_time(), 3))
