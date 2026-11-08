#!/usr/bin/env python3
"""Exact prescribed algebra controls; no room, direction, or path discovery."""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
counts = {}

def record(name, count):
    counts[name] = count

# Copy labels G=(Z/2)^2, iota=3. A lift is a stabilizer coset.
n = 0
for name, stabilizer, expected_count, expected_fixed in [
    ('interior', {0}, 4, 0), ('horizontal_wall', {0, 1}, 2, 0),
    ('vertical_wall', {0, 2}, 2, 0), ('convex_corner', {0, 1, 2, 3}, 1, 1),
    ('reflex_corner', {0, 1, 2, 3}, 1, 1),
]:
    cosets = {frozenset(g ^ h for h in stabilizer) for g in range(4)}
    assert len(cosets) == expected_count
    fixed = sum(frozenset(g ^ 3 for g in c) == c for c in cosets)
    assert fixed == expected_fixed, name
    if 'wall' in name:
        assert all(frozenset(g ^ 3 for g in c) != c for c in cosets)
    n += 1
record('copy_stabilizers', n)

# The two fixed points in an invariant cylinder, in prescribed rational charts.
n = 0
for L in [F(1), F(2, 3), F(7, 4)]:
    for h in [F(1), F(3, 2)]:
        for c0 in [F(0), F(1, 7), F(11, 5)]:
            c = c0 % L
            points = [(c / 2, h / 2), ((c / 2 + L / 2) % L, h / 2)]
            assert points[0] != points[1]
            for x, y in points:
                assert ((-x+c) % L, h-y) == (x, y)
                assert 0 < y < h
            n += 1
record('invariant_cylinder_fixed_point_charts', n)

# A single interior point cannot hit consecutive winding segments.
# Prescribed cylinder-coordinate formula only, not a billiard path catalogue.
n = 0
for denominator in range(2, 34):
    for numerator in range(1, denominator):
        lam = F(numerator, denominator)
        for L in [F(1), F(2, 3), F(7, 4)]:
            for a, d in [(F(0), F(1, 3)), (F(-2, 5), F(7, 9))]:
                q0 = (a + lam * (d-a)) % L
                q1 = (a + lam * (d-a+L)) % L
                assert q0 != q1
                assert (q1-q0) % L == (lam*L) % L
                # Reversing transverse order changes neither lambda nor the test.
                u, v = F(3, 4), F(1, 4)
                w = u + lam*(v-u)
                assert (w-u)/(v-u) == lam
                n += 1
record('consecutive_winding_identities', n)

# Complementary arcs when source and target have equal transverse coordinate.
n = 0
for denominator in range(3, 23):
    for target in range(1, denominator):
        for blocker in range(1, denominator):
            if blocker == target:
                continue
            d, b = F(target, denominator), F(blocker, denominator)
            forward, backward = 0 < b < d, d < b < 1
            assert forward != backward
            n += 1
record('complementary_arc_controls', n)

# Negative control: two arbitrary blockers can cover every integer winding.
# At lambda=1/2, n even hits 1/6 and n odd hits 2/3.
b0, b1, c = F(1, 6), F(2, 3), F(5, 6)
assert (-b0+c) % 1 == b1 and (-b1+c) % 1 == b0
assert (c/2) not in {b0, b1} and ((c/2+F(1, 2)) % 1) not in {b0, b1}
for n in range(-24, 25):
    hit = (F(1, 2)*(F(1, 3)+n)) % 1
    assert hit == (b0 if n % 2 == 0 else b1)
record('arbitrary_two_blocker_negative_control_windings', 49)

# Orthogonal corner-angle and Riemann-Hurwitz identities.
for r in range(41):
    convex, W, genus = r+4, 2*r+4, r+1
    assert convex-r == 4
    assert W == 2*genus+2
    assert 2*genus-2 == -4+W
record('topology_identities', 41)

result = {
    'status': 'PASS', 'checks': counts, 'total': sum(counts.values()),
    'scope': 'Finite exact algebra controls for written cylinder proof; no discovery search.',
    'unproved': [
        'Universal single smooth boundary blocker removal',
        'Existence of common corner-free cylinder for arbitrary lit marks',
        'Exclusion or realization of the critical-leaf remainder',
    ],
}
(ROOT/'check.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
