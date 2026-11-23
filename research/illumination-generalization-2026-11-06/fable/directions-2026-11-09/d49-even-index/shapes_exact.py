"""d49 arithmetic only: exact fibre-shape test for certificates with a zero over an even base.

A factor N of Q -> P_Lambda with degree d, delta = n / d, z zeros, p = z + 4 poles (Gauss-Bonnet).
Over class j: p_j poles, z_j zeros, the rest 2-cycles, so w_j = p_j + 3 z_j <= d, w_j = d (mod 2).
Zeros of N have delta reflex preimages, so delta z <= r, and they lie over vertex classes V only.
Classes: 0 and v form V (|V| = 2, the case m = 2 and any cyclic 2-part); u and u+v are non-V.
Types at target x:
  Par(x): w_x = d.   Rig(x): some y not in {c_s, x} with p_y = d, z_y = 0.
  Cut(x): d = 3 and some w not in {c_s, x} with (p_w, z_w) = (0, 1).
Reports, for each r, the n = m n_R that admit a shape with z >= 1 at a NON-V target x.
"""
from itertools import product

CL = ['0', 'v', 'u', 'u+v']
V = {0, 1}


def dists(d, z):
    """All (p_j, z_j) for the 4 classes with the parity, size, Gauss-Bonnet and V constraints."""
    opts = []
    for j in range(4):
        o = []
        for zj in range(0, (z if j in V else 0) + 1):
            for pj in range(0, z + 5):
                w = pj + 3 * zj
                if w <= d and (w - d) % 2 == 0:
                    o.append((pj, zj))
        opts.append(o)
    for c in product(*opts):
        if sum(a for a, _ in c) == z + 4 and sum(b for _, b in c) == z:
            yield c


def nonV_shapes(n, r):
    out = set()
    for delta in range(1, r + 1):
        if n % delta:
            continue
        d = n // delta
        if d < 3:
            continue
        for z in range(1, r // delta + 1):
            for c in dists(d, z):
                for x in (2, 3):
                    for cs in range(4):
                        if cs == x:
                            continue
                        rest = [y for y in range(4) if y not in (cs, x)]
                        if c[x][0] + 3 * c[x][1] == d:
                            out.add(('Par', delta, d, z))
                        if any(c[y][0] == d and c[y][1] == 0 for y in rest):
                            out.add(('Rig', delta, d, z))
                        if d == 3 and any(c[y] == (0, 1) for y in rest):
                            out.add(('Cut', delta, d, z))
    return sorted(out)


for r in range(1, 9):
    ok = {n: nonV_shapes(n, r) for n in range(3, 5 * r + 1)}
    print('r=%d: n with a non-V-target shape: %s' % (r, [n for n, s in ok.items() if s]))
    if r == 8:
        for n in range(30, 41):
            print('   n=%d: %s' % (n, ok[n]))


def rigV_shapes(n, r):
    """Rig at a V target x (the only target when c_s != c_t), identity at some y not in {c_s, x}."""
    out = set()
    for delta in range(1, r + 1):
        if n % delta:
            continue
        d = n // delta
        if d < 3:
            continue
        for z in range(1, r // delta + 1):
            for c in dists(d, z):
                for x in (0, 1):
                    for cs in range(4):
                        if cs == x:
                            continue
                        if any(c[y][0] == d and c[y][1] == 0 for y in range(4) if y not in (cs, x)):
                            out.add(('Rig', delta, d, z))
    return sorted(out)


print()
for r in range(1, 9):
    ok = {n: rigV_shapes(n, r) for n in range(3, 5 * r + 1)}
    print('r=%d: n with a Rig shape at a V target (c_s != c_t): %s' % (r, [n for n, s in ok.items() if s]))
    if r == 8:
        for n in (32, 34, 36, 38, 40):
            print('   n=%d: %s' % (n, ok[n]))
