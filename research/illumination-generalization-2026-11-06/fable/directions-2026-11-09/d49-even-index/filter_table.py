"""d49 arithmetic only (no room, ray, or word enumeration).

Filter E* for Residue E (d49 memo, section 4).  A lift pair escapes the witness lemma only through
a certificate with a zero (Par, Rig, Cut) or a zero-free Cut.  Necessary shapes, n = m n_R = delta d:
  ParV : Par at a target in V (vertex classes), z >= 1, d <= 4z+4 (d even) or 4z+1 (d odd)
  ParN / Rig : z >= 1, d <= z + 4
  Cut  : z >= 1, d = 3
  Cut0 : zero-free Cut, n <= conv_x + 3 refl_x <= 4r + 4, needs a vertex-only Lambda-class
plus delta z <= r, d >= 3, and z zeros each with delta reflex preimages over one V class:
  sum_{y in V} floor(rho_y / delta) >= z.
delta = 1 Par needs a Lambda-class with no regular point of Q (vertex-only), like Cut0.

Size estimate: fixed room counts per (W, area) from ../d44-cert-check-sizing/est_W*.log (Knuth
estimates, +-25%), divided by 8 for free rooms, times a GUESSED pass rate: the reflex corners'
V-classes modelled as independent fair coins, and the three index-2 lattices as independent.
"""
import re
from math import comb
from pathlib import Path

D44 = Path(__file__).resolve().parent.parent / 'd44-cert-check-sizing'


def shapes(n, r):
    out = []
    for delta in range(1, r + 1):
        if n % delta:
            continue
        d = n // delta
        if d < 3:
            continue
        for z in range(1, r // delta + 1):
            if d <= (4 * z + 4 if d % 2 == 0 else 4 * z + 1):
                out.append(('ParV', delta, d, z))
            if d <= z + 4:
                out.append(('Rig/ParN', delta, d, z))
            if d == 3:
                out.append(('Cut', delta, d, z))
    if n <= 4 * r + 4:
        out.append(('Cut0', n, 1, 0))
    return out


def ok(shape, rho):
    kind, delta, d, z = shape
    if kind == 'Cut0' or delta == 1:
        return None                      # needs a vertex-only class: rare, counted separately
    return sum(x // delta for x in rho) >= z


def pass_rate(n, r, nV=2):
    """P(some non-vertex-only shape passes) for rho ~ Binomial split of r reflex corners."""
    sh = shapes(n, r)
    tot = 0.0
    for k in range(r + 1):
        rho = (k, r - k) if nV == 2 else (r,)
        w = comb(r, k) / 2 ** r if nV == 2 else (1.0 if k == 0 else 0.0)
        if any(ok(s, rho) for s in sh):
            tot += w
    return tot


def fixed_counts():
    out = {}
    for W in (16, 18, 20):
        for line in open(D44 / ('est_W%d.log' % W)):
            mm = re.match(r'\s+W (\d+) area (\d+) est_fixed ([\d.e+]+)', line)
            if mm:
                out[(int(mm.group(1)), int(mm.group(2)))] = float(mm.group(3))
    for line in open(D44 / 'cnt_14_25.log'):
        mm = re.match(r'\s+W (\d+) area (\d+) fixed (\d+)', line)
        if mm and int(mm.group(1)) == 14:
            out[(14, int(mm.group(2)))] = float(mm.group(3))
    return out


FC = fixed_counts()
print('Allowed n = m n_R with an escaping shape (vertex-only shapes delta = 1 / Cut0 marked *)')
for r in range(1, 9):
    al = [n for n in range(2, 8 * r + 1) if any(ok(s, (r, 0)) for s in shapes(n, r))]
    star = [n for n in range(2, 8 * r + 1) if n not in al and shapes(n, r)]
    print(' r=%d: max %d; allowed (non-vertex-only) %s; vertex-only only %s' % (r, 8 * r, al, star))

print()
print('m = 2 (three lattices, |V| = 2), lattice marks: n_R in [21, 32] (any pair), [17, 20] (different-class only)')
total = 0.0
for r in (6, 7, 8):
    W = 2 * r + 4
    for nR in range(17, 4 * r + 1):
        n = 2 * nR
        sh = [s for s in shapes(n, r) if s[0] != 'Cut0' and s[1] > 1]
        if not sh:
            continue
        p1 = pass_rate(n, r)
        p3 = 1 - (1 - p1) ** 3
        free = FC.get((W, nR), 0) / 8
        total += free * p3
        print('  W=%d n_R=%d n=%d shapes %s  p(one lattice)=%.3f p(3)=%.3f free rooms %.2e -> %.2e'
              % (W, nR, n, [s[:4] for s in sh][:6], p1, p3, free, free * p3))
print('  total free rooms (GUESSED pass model) %.2e' % total)
print()
print('m = 4, Lambda = (1/2)Z^2 (|V| = 1) and cyclic order-4 lattices (|V| = 2): allowed n_R')
for r in range(1, 9):
    print('  r=%d: %s' % (r, [nR for nR in range(1, 2 * r + 1)
                              if any(ok(s, (r,)) or ok(s, (r, 0)) for s in shapes(4 * nR, r))]))
