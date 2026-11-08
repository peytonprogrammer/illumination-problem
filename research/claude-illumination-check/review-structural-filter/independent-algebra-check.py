"""Independent algebra check for pocket-structural-obstruction.md Sections 2-3.

No room, ray, direction, word, cylinder, or orbit is generated. Every check
is finite exact arithmetic on local data stated in the reviewed document.
"""
from fractions import Fraction as F
from itertools import product
import json

# 1. Cone angle from the generated local reflection group, not a table.
# Wall directions are k*pi/4. Reflection across the line at angle k*pi/4
# has matrix [[cos 2a, sin 2a], [sin 2a, -cos 2a]], 2a = k*pi/2, integral.
COS = {0: 1, 1: 0, 2: -1, 3: 0}
SIN = {0: 0, 1: 1, 2: 0, 3: -1}


def refl(k):
    j = k % 4
    return ((COS[j], SIN[j]), (SIN[j], -COS[j]))


def mul(a, b):
    return tuple(tuple(sum(a[i][t] * b[t][j] for t in range(2)) for j in range(2))
                 for i in range(2))


def group_order(gens):
    ident = ((1, 0), (0, 1))
    seen, frontier = {ident}, [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for s in gens:
                h = mul(g, s)
                if h not in seen:
                    seen.add(h)
                    nxt.append(h)
        frontier = nxt
    return len(seen)


cone_rows = []
for m in range(1, 8):
    # Every wall pair whose directions differ by m*pi/4 gives the same group order.
    orders = {group_order([refl(k), refl(k + m)]) for k in range(4)}
    assert len(orders) == 1
    n = orders.pop()
    mult = F(n * m, 8)  # n sectors of angle m*pi/4, in units of 2*pi
    assert mult.denominator == 1
    q = int(mult)
    cone_rows.append(dict(m=m, local_group_order=n, cone_multiplicity=q,
                          zero_order=q - 1, zero_order_even=(q - 1) % 2 == 0))
assert all(r['zero_order_even'] for r in cone_rows)

# 2. Pullback order, computed from exponents of (z^e)^k * d(z^e).
# d(z^e) = e z^(e-1) dz, so the source exponent is e*k + (e-1).
# Exhaustive range, both directions of the parity rule.
violations = []
for e, k in product(range(1, 41), range(0, 41)):
    src = e * k + (e - 1)
    if (src % 2 == 0) != (e % 2 == 1 and k % 2 == 0):
        violations.append((e, k))
assert not violations
# EW case: a simple target zero (k=1) never has an even-order preimage.
assert all((e * 1 + e - 1) % 2 == 1 for e in range(1, 1001))

# 3. Section 3: maximal isotropic dimension in a 2r-dim symplectic space is r.
# For r=1, any 2-dim subspace is the whole space, and omega(e1,f1)=1 != 0.
# For r=2, span{e1,e2} is a Lagrangian plane. Both are standard facts;
# this records them as exact matrix checks.
J2 = ((0, 1), (-1, 0))
assert J2[0][1] != 0
J4 = [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]]
e1, e2 = [1, 0, 0, 0], [0, 1, 0, 0]
omega = sum(e1[i] * J4[i][j] * e2[j] for i in range(4) for j in range(4))
assert omega == 0

out = dict(
    status='INDEPENDENT_LOCAL_ALGEBRA_PASS',
    cone_rows=cone_rows,
    pullback_parity_pairs_checked=40 * 41,
    pullback_parity_violations=len(violations),
    ew_simple_zero_preimage_odd_for_e_up_to=1000,
    isotropic_bound_checks=['dim2_no_isotropic_plane', 'dim4_lagrangian_plane_exists'],
    discovery_runs=0,
)
print(json.dumps(out, indent=2))
