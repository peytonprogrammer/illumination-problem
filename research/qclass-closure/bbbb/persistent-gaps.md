# A rim gap must survive all four representatives of each mark

**Result.** The 57-cell, 12-wall cross CR34 illuminates every pair of distinct real interior points. In either of its saved directions (1,2) and (1,3), both rims miss some even separations. Nevertheless, in each chart separately, every pair that could need a rim connection has representatives with a legal match. No chart change is needed. CR34 has reflexes at (4,4),(4,7),(7,4),(7,7), one in each physical parity. Its horizontal and vertical wall gcds are both one (lengths include 3 and 4).

## Sharper necessary condition for persistence

Assume a normalized room admits a nonaxial primitive chart (p,q) with two geometric cylinders exchanged by the half-turn. Use the earlier [rim-tree proof](adjacent-cylinders.md); the cylinder on the double has integral transverse height one. In the four-copy unfolding the two rim levels are distinguished by transverse parity mod 2, up to a single additive constant. In physical coordinates the transverse values of the four sheet lifts of (x,y) are ±qx±py modulo 2, up to that same constant: integer-coordinate mirror developments use even translations, and the straightening chart is unimodular.

If two distinct physical interior points fail the open-cylinder and opposite-rim connections, **all lifts of both points must be on the same rim**. Any interior lift can be put in the representative cylinder, and its other endpoint in the closure, by the half-turn. Opposite-rim representatives give a straight transverse segment. In either case the open segment avoids the critical graph (for interior endpoints at the same transverse height use an interior horizontal segment). Thus for either mark the four transverse values must be integers of the same parity. Subtract the sign choices separately to get

    qx ∈ ℤ,    py ∈ ℤ.

In addition, qx−py agrees modulo 2 between the marks. This sharpens the bounds 2qx,2py ∈ ℤ obtained from membership in the critical graph alone in [D3 Theorem B](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d3-two-mechanisms/audit.md). Across multiple such charts the coordinate denominators must divide the respective gcds of the |q| and |p|. Retain also every pairwise transverse-parity constraint. For example (1,2) and (1,3) together force both marks integral and of the same physical parity.

For surviving marks let A and B be their four contour representatives on their common rim, and E the union of open differences from regular opposite-rim edges. The exact condition to miss the two-traversal test is (A−B) ∩ E = ∅ (all differences cyclic). A dark pair must satisfy this *with the same physical endpoints* for every applicable chart. A nonempty gap in E, or a gap of the same length in another chart, does not establish this condition.

## CR34 exact continuum check

CR34 is the union of [4,7]×[0,11] and [0,11]×[4,7]. Both saved charts have circumference 114; on both rims the missed nonzero even differences are:

| chart | missed even differences |
|---|---|
| (1,2) | 22,24,…,42 and 72,74,…,92 |
| (1,3) | 12,14,…,20 and 94,96,…,102 |

The pair-specific check keeps the signs and contour representatives in each chart. At (1,2) only x half-integral and y integral can survive the parity test. At (1,3) only x in thirds and y integral can survive. Rescale by 2 or 3 to read the representatives exactly on the unit grid. This is a coordinate refinement of the original room, so the two-cylinder gluing and the open-edge test are unchanged up to scale. All nonzero integral differences in the refined coordinates are tested, including odd differences. They may have nonintegral crossing points; these are legal if they lie strictly inside an edge.

| chart | interior marks in the necessary grid | distinct same-rim pairs | pairs missing every match |
|---|---:|---:|---:|
| (1,2) | 82 | 1,640 | 0 |
| (1,3) | 128 | 4,032 | 0 |

The checker checks the grid independently against all four-cell interior vertices in the refined room with the stipulated coordinates, finds exactly four representatives for each, and verifies that none straddles the two rims. For each pair it intersects its complete difference set with the opposite-rim intervals. Pairs omitted from the table are covered by the geometric argument above. For same-parity lattice pairs the transverse parity changes at the half-time crossing, giving the regular off-class midpoint required by d82. The charts have inequivalent metric trees: their unordered contour edge-length signatures differ. The two individual continuum certificates do not rely on assuming unrelated charts have unrelated gap positions.

As a negative control, the two manuscript charts for R22 again miss the same physical pair, with the separations explained by its [staircase quotient](rim-quotient.md). The auditor also checks the archived admissible BBBB charts against each room’s saved same-parity pairs. This uses no new direction discovery. [Checker](persistent-gaps.py) · [Exact output](persistent-gaps.txt)

**Limit.** This is a pair-specific continuum certificate in a four-reflex-parity room. It neither proves every room has a two-cylinder chart nor rules out persistent pair-specific misses for all rooms with at most eight reflex corners. No independent review of this note has been completed.
